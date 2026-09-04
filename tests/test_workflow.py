import pytest
from unittest.mock import patch, MagicMock
from app.workflow import (
    BenchmarkState,
    initialize_pipeline,
    evaluate_model,
    calculate_financials,
    persist_data,
    increment_index,
    generate_deterministic_summary,
    synthesize_summary,
    route_after_evaluation,
    route_next_model,
    benchmark_graph,
)
from app.config import ClusterConfig

# ----------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------

@pytest.fixture
def base_state() -> BenchmarkState:
    """Returns a fresh, default BenchmarkState dictionary."""
    return {
        "run_id": "test_run_123",
        "models": ["model-a", "model-b"],
        "current_index": 0,
        "cluster_config": ClusterConfig(
            name="A10G-Cluster",
            gpu_type="A10G",
            gpu_count=2,
            gpu_vram_gb=24,
            nodes=1,
            upfront_cost_eur=10000.0,
            server_hardware_cost_eur=10000.0,
            power_draw_kw=0.75,
            cloud_cost_per_request_eur=0.001,
        ),
        "required_rps": 10.0,
        "completed_runs": [],
        "failed_models": [],
        "last_run_failed": False,
        "executive_summary": "",
    }


@pytest.fixture
def mock_eval_result():
    """Provides a standardized mock response for app.engine.eval_prompt_streaming."""
    return {
        "test_id": 1,
        "category": "unit_test",
        "expected_intent_id": 100,
        "predicted_intent_id": 100,
        "is_correct": True,
        "latency_ms": 100.0,
        "ttft_ms": 20.0,
        "tps": 50.0,
        "prompt_tokens": 150,
        "eval_count": 50
    }


# ----------------------------------------------------------------------
# 1. Pipeline Initialization Tests (Tests 1–3)
# ----------------------------------------------------------------------

@pytest.mark.asyncio
async def test_01_initialize_pipeline_resets_defaults(base_state):
    base_state["current_index"] = 5
    base_state["completed_runs"] = [{"some": "data"}]
    base_state["failed_models"] = [{"some": "error"}]
    base_state["last_run_failed"] = True
    base_state["executive_summary"] = "Old summary"

    res = await initialize_pipeline(base_state)

    assert res["current_index"] == 0
    assert res["completed_runs"] == []
    assert res["failed_models"] == []
    assert res["last_run_failed"] is False
    assert res["executive_summary"] == ""


@pytest.mark.asyncio
async def test_02_initialize_pipeline_returns_dict(base_state):
    res = await initialize_pipeline(base_state)
    assert isinstance(res, dict)


@pytest.mark.asyncio
async def test_03_initialize_pipeline_does_not_mutate_models(base_state):
    res = await initialize_pipeline(base_state)
    assert "models" not in res  # LangGraph node returns state delta, not mutating models


# ----------------------------------------------------------------------
# 2. Model Evaluation Node Tests (Tests 4–10)
# ----------------------------------------------------------------------

@pytest.mark.asyncio
@patch("app.workflow.eval_prompt_streaming")
@patch("app.workflow.unload_model")
async def test_04_evaluate_model_success_path(mock_unload, mock_eval, base_state, mock_eval_result):
    mock_eval.return_value = mock_eval_result

    res = await evaluate_model(base_state)

    assert res["last_run_failed"] is False
    assert len(res["completed_runs"]) == 1
    
    run_data = res["completed_runs"][0]
    assert run_data["model_name"] == "model-a"
    assert run_data["accuracy"] == 100.0
    assert run_data["avg_latency_ms"] == 100.0
    assert run_data["avg_ttft_ms"] == 20.0
    assert run_data["avg_tps"] == 50.0
    mock_unload.assert_called_once_with("model-a")


@pytest.mark.asyncio
@patch("app.workflow.eval_prompt_streaming")
@patch("app.workflow.unload_model")
async def test_05_evaluate_model_calculates_mixed_accuracy(mock_unload, mock_eval, base_state, mock_eval_result):
    wrong_result = dict(mock_eval_result, is_correct=False)
    mock_eval.side_effect = [mock_eval_result, wrong_result]

    with patch("app.workflow.test_cases", [{}, {}]):
        res = await evaluate_model(base_state)

    run_data = res["completed_runs"][0]
    assert run_data["accuracy"] == 50.0


@pytest.mark.asyncio
@patch("app.workflow.eval_prompt_streaming")
@patch("app.workflow.unload_model")
async def test_06_evaluate_model_exception_handling(mock_unload, mock_eval, base_state):
    mock_eval.side_effect = RuntimeError("Ollama OOM")

    res = await evaluate_model(base_state)

    assert res["last_run_failed"] is True
    assert len(res["failed_models"]) == 1
    assert res["failed_models"][0] == {"model_name": "model-a", "error": "Ollama OOM"}


@pytest.mark.asyncio
@patch("app.workflow.eval_prompt_streaming")
@patch("app.workflow.unload_model")
async def test_07_evaluate_model_updates_run_status_store(mock_unload, mock_eval, base_state, mock_eval_result):
    mock_eval.return_value = mock_eval_result
    
    # Pre-populate store in main
    from app.main import RUN_STATUS_STORE
    RUN_STATUS_STORE["test_run_123"] = {}

    await evaluate_model(base_state)
    
    assert RUN_STATUS_STORE["test_run_123"].get("status") == "running"


@pytest.mark.asyncio
@patch("app.workflow.eval_prompt_streaming")
@patch("app.workflow.unload_model")
async def test_08_evaluate_model_appends_to_existing_completed_runs(mock_unload, mock_eval, base_state, mock_eval_result):
    mock_eval.return_value = mock_eval_result
    base_state["completed_runs"] = [{"model_name": "previous-model"}]

    res = await evaluate_model(base_state)

    assert len(res["completed_runs"]) == 2
    assert res["completed_runs"][0]["model_name"] == "previous-model"
    assert res["completed_runs"][1]["model_name"] == "model-a"


@pytest.mark.asyncio
@patch("app.workflow.eval_prompt_streaming")
@patch("app.workflow.unload_model")
async def test_09_evaluate_model_accumulates_total_tokens(mock_unload, mock_eval, base_state, mock_eval_result):
    mock_eval.return_value = mock_eval_result

    with patch("app.workflow.test_cases", [{}, {}, {}]):
        res = await evaluate_model(base_state)

    assert res["completed_runs"][0]["total_tokens"] == 150  # 50 * 3


@pytest.mark.asyncio
@patch("app.workflow.eval_prompt_streaming")
@patch("app.workflow.unload_model")
async def test_10_evaluate_model_unloads_even_on_partial_tokens(mock_unload, mock_eval, base_state, mock_eval_result):
    mock_eval.return_value = mock_eval_result
    await evaluate_model(base_state)
    mock_unload.assert_called_once()


# ----------------------------------------------------------------------
# 3. Financial Calculation Node Tests (Tests 11–15)
# ----------------------------------------------------------------------

@pytest.mark.asyncio
@patch("app.workflow.calculate_financial_roi")
async def test_11_calculate_financials_with_cluster_analysis(mock_roi, base_state):
    base_state["completed_runs"] = [{
        "model_name": "model-a",
        "avg_latency_ms": 120.0,
        "accuracy": 85.0,
        "evaluations": [{"prompt_tokens": 100, "eval_count": 50}]
    }]

    mock_roi.return_value = {
        "efficiency_score": 0.95,
        "cloud_cost_per_request_eur": 0.0005,
        "cluster_analysis": {
            "tco": {"total_monthly_tco_eur": 1500.0},
            "throughput": {"max_rps": 30.0},
            "breakeven": {
                "breakeven_monthly_requests": 3000000,
                "feasible": True,
                "recommendation": "Use local cluster"
            }
        }
    }

    res = await calculate_financials(base_state)
    latest = res["completed_runs"][0]

    assert latest["efficiency_score"] == 0.95
    assert latest["cluster_monthly_tco_eur"] == 1500.0
    assert latest["max_rps"] == 30.0
    assert latest["breakeven_requests"] == 3000000
    assert latest["cluster_feasible"] is True
    assert latest["recommendation"] == "Use local cluster"


@pytest.mark.asyncio
@patch("app.workflow.calculate_financial_roi")
async def test_12_calculate_financials_without_cluster_analysis(mock_roi, base_state):
    base_state["completed_runs"] = [{
        "model_name": "model-a",
        "avg_latency_ms": 120.0,
        "accuracy": 85.0,
        "evaluations": []
    }]

    mock_roi.return_value = {
        "efficiency_score": 0.70,
        "cloud_cost_per_request_eur": 0.001,
        "cluster_analysis": None
    }

    res = await calculate_financials(base_state)
    latest = res["completed_runs"][0]

    assert latest["efficiency_score"] == 0.70
    assert latest["breakeven_requests"] is None


@pytest.mark.asyncio
@patch("app.workflow.calculate_financial_roi")
async def test_13_calculate_financials_extracts_tokens_correctly(mock_roi, base_state):
    base_state["completed_runs"] = [{
        "model_name": "model-a",
        "avg_latency_ms": 100.0,
        "accuracy": 90.0,
        "evaluations": [
            {"prompt_tokens": 10, "eval_count": 20},
            {"prompt_tokens": 15, "eval_count": 25}
        ]
    }]

    mock_roi.return_value = {"efficiency_score": 0.8, "cloud_cost_per_request_eur": 0.001}

    await calculate_financials(base_state)

    mock_roi.assert_called_once_with(
        model_name="model-a",
        total_input_tokens=25,
        total_output_tokens=45,
        total_requests=2,
        local_avg_latency_ms=100.0,
        local_accuracy=90.0,
        cluster=base_state["cluster_config"],
        required_rps=10.0
    )


@pytest.mark.asyncio
@patch("app.workflow.calculate_financial_roi")
async def test_14_calculate_financials_preserves_previous_runs(mock_roi, base_state):
    base_state["completed_runs"] = [
        {"model_name": "model-0", "efficiency_score": 0.5},
        {"model_name": "model-a", "avg_latency_ms": 100.0, "accuracy": 90.0, "evaluations": []}
    ]
    mock_roi.return_value = {"efficiency_score": 0.9, "cloud_cost_per_request_eur": 0.001}

    res = await calculate_financials(base_state)

    assert len(res["completed_runs"]) == 2
    assert res["completed_runs"][0]["model_name"] == "model-0"


@pytest.mark.asyncio
@patch("app.workflow.calculate_financial_roi")
async def test_15_calculate_financials_fallback_required_rps(mock_roi, base_state):
    del base_state["required_rps"]
    base_state["completed_runs"] = [{"model_name": "m", "avg_latency_ms": 100, "accuracy": 100, "evaluations": []}]
    mock_roi.return_value = {"efficiency_score": 0.9, "cloud_cost_per_request_eur": 0.001}

    await calculate_financials(base_state)

    assert mock_roi.call_args.kwargs["required_rps"] == 1.0


# ----------------------------------------------------------------------
# 4. Persistence Node Tests (Tests 16–18)
# ----------------------------------------------------------------------

@pytest.mark.asyncio
@patch("app.workflow.save_benchmark_results")
async def test_16_persist_data_formats_report_correctly(mock_save, base_state):
    base_state["completed_runs"] = [{
        "model_name": "model-a",
        "accuracy": 95.0,
        "avg_latency_ms": 80.0,
        "avg_ttft_ms": 15.0,
        "avg_tps": 60.0,
        "total_tokens": 1200,
        "efficiency_score": 0.92,
        "breakeven_requests": 500000,
        "cluster_monthly_tco_eur": 800.0,
        "max_rps": 40.0,
        "evaluations": [{"test_id": 1}]
    }]

    res = await persist_data(base_state)

    assert res == {}
    mock_save.assert_called_once_with([{
        "model_name": "model-a",
        "accuracy": 95.0,
        "avg_latency_ms": 80.0,
        "avg_ttft_ms": 15.0,
        "avg_tps": 60.0,
        "total_tokens_used": 1200,
        "efficiency_score": 0.92,
        "breakeven_monthly_requests": 500000,
        "cluster_monthly_tco_eur": 800.0,
        "max_rps": 40.0,
        "evaluations": [{"test_id": 1}]
    }])


@pytest.mark.asyncio
@patch("app.workflow.save_benchmark_results")
async def test_17_persist_data_handles_none_optional_values(mock_save, base_state):
    base_state["completed_runs"] = [{
        "model_name": "model-a",
        "accuracy": 50.0,
        "avg_latency_ms": 200.0,
        "avg_ttft_ms": 50.0,
        "avg_tps": 10.0,
        "total_tokens": 100,
        "efficiency_score": 0.5,
        "evaluations": []
    }]

    await persist_data(base_state)

    report = mock_save.call_args[0][0][0]
    assert report["breakeven_monthly_requests"] is None
    assert report["cluster_monthly_tco_eur"] is None
    assert report["max_rps"] is None


@pytest.mark.asyncio
async def test_18_increment_index_advances_counter(base_state):
    base_state["current_index"] = 1
    res = await increment_index(base_state)
    assert res == {"current_index": 2}


# ----------------------------------------------------------------------
# 5. Executive Summary & Synthesis Tests (Tests 19–24)
# ----------------------------------------------------------------------

def test_19_generate_deterministic_summary_empty_runs():
    summary = generate_deterministic_summary([])
    assert summary == "No completed runs available to summarize."


def test_20_generate_deterministic_summary_highlights_top_performers():
    runs = [
        {"model_name": "SlowAccurate", "accuracy": 95.0, "avg_ttft_ms": 100.0, "avg_tps": 20.0, "breakeven_requests": 1000000},
        {"model_name": "FastInaccurate", "accuracy": 70.0, "avg_ttft_ms": 10.0, "avg_tps": 100.0, "breakeven_requests": 500000}
    ]

    summary = generate_deterministic_summary(runs)

    assert "[Rule-Based Fallback Synthesis]" in summary
    assert "SlowAccurate" in summary and "95.0%" in summary
    assert "FastInaccurate" in summary and "10.0 ms" in summary
    assert "lowest breakeven threshold at 500,000 monthly requests" in summary


@pytest.mark.asyncio
async def test_21_synthesize_summary_empty_runs(base_state):
    base_state["completed_runs"] = []
    res = await synthesize_summary(base_state)
    assert res == {"executive_summary": "No models were successfully evaluated."}


@pytest.mark.asyncio
@patch("requests.post")
async def test_22_synthesize_summary_openrouter_success(mock_post, base_state):
    base_state["completed_runs"] = [{"model_name": "model-a", "accuracy": 90.0}]

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Bullet 1\nBullet 2\nBullet 3"}}]
    }
    mock_post.return_value = mock_response

    res = await synthesize_summary(base_state)

    assert "[Cloud Synthesis - OpenRouter]" in res["executive_summary"]
    assert "Bullet 1" in res["executive_summary"]


@pytest.mark.asyncio
@patch("requests.post")
async def test_23_synthesize_summary_openrouter_http_error_triggers_fallback(mock_post, base_state):
    base_state["completed_runs"] = [{"model_name": "model-a", "accuracy": 90.0, "avg_ttft_ms": 10.0, "avg_tps": 50.0}]
    mock_post.side_effect = Exception("API Timeout")

    res = await synthesize_summary(base_state)

    assert "[Rule-Based Fallback Synthesis]" in res["executive_summary"]
    assert "model-a" in res["executive_summary"]


@pytest.mark.asyncio
@patch("requests.post")
async def test_24_synthesize_summary_openrouter_invalid_payload_triggers_fallback(mock_post, base_state):
    base_state["completed_runs"] = [{"model_name": "model-a", "accuracy": 90.0, "avg_ttft_ms": 10.0, "avg_tps": 50.0}]
    
    mock_response = MagicMock()
    mock_response.json.return_value = {"error": "Invalid API Key"}
    mock_post.return_value = mock_response

    res = await synthesize_summary(base_state)

    assert "[Rule-Based Fallback Synthesis]" in res["executive_summary"]


# ----------------------------------------------------------------------
# 6. Graph Routing Edge Functions (Tests 25–28)
# ----------------------------------------------------------------------

def test_25_route_after_evaluation_success(base_state):
    base_state["last_run_failed"] = False
    assert route_after_evaluation(base_state) == "calculate_financials"


def test_26_route_after_evaluation_failure(base_state):
    base_state["last_run_failed"] = True
    assert route_after_evaluation(base_state) == "increment_index"


def test_27_route_next_model_continues_loop(base_state):
    base_state["models"] = ["m1", "m2"]
    base_state["current_index"] = 0
    assert route_next_model(base_state) == "evaluate_model"


def test_28_route_next_model_ends_loop(base_state):
    base_state["models"] = ["m1", "m2"]
    base_state["current_index"] = 2
    assert route_next_model(base_state) == "synthesize_summary"


# ----------------------------------------------------------------------
# 7. End-to-End Compiled Graph Execution Tests (Tests 29–32)
# ----------------------------------------------------------------------

@pytest.mark.asyncio
@patch("app.workflow.eval_prompt_streaming")
@patch("app.workflow.unload_model")
@patch("app.workflow.calculate_financial_roi")
@patch("app.workflow.save_benchmark_results")
@patch("requests.post")
async def test_29_full_graph_execution_single_model_success(
    mock_post, mock_save, mock_roi, mock_unload, mock_eval, base_state, mock_eval_result
):
    base_state["models"] = ["model-a"]
    mock_eval.return_value = mock_eval_result
    mock_roi.return_value = {"efficiency_score": 0.9, "cloud_cost_per_request_eur": 0.001}
    
    mock_response = MagicMock()
    mock_response.json.return_value = {"choices": [{"message": {"content": "Summary"}}] }
    mock_post.return_value = mock_response

    final_state = await benchmark_graph.ainvoke(base_state)

    assert final_state["current_index"] == 1
    assert len(final_state["completed_runs"]) == 1
    assert len(final_state["failed_models"]) == 0
    assert "[Cloud Synthesis - OpenRouter]" in final_state["executive_summary"]
    mock_save.assert_called_once()


@pytest.mark.asyncio
@patch("app.workflow.eval_prompt_streaming")
@patch("app.workflow.unload_model")
@patch("app.workflow.calculate_financial_roi")
@patch("app.workflow.save_benchmark_results")
@patch("requests.post")
async def test_30_full_graph_execution_multi_model_partial_failure(
    mock_post, mock_save, mock_roi, mock_unload, mock_eval, base_state, mock_eval_result
):
    base_state["models"] = ["working-model", "failing-model"]
    
    # Restrict test cases to 1 so working-model completes in 1 iteration
    with patch("app.workflow.test_cases", [{"test_id": 1}]):
        mock_eval.side_effect = [mock_eval_result, RuntimeError("CUDA Out of Memory")]
        mock_roi.return_value = {"efficiency_score": 0.8, "cloud_cost_per_request_eur": 0.001}
        mock_post.side_effect = Exception("No OpenRouter")

        final_state = await benchmark_graph.ainvoke(base_state)

    assert len(final_state["completed_runs"]) == 1
    assert len(final_state["failed_models"]) == 1
    assert final_state["failed_models"][0]["model_name"] == "failing-model"


@pytest.mark.asyncio
@patch("app.workflow.eval_prompt_streaming")
@patch("app.workflow.unload_model")
@patch("requests.post")
async def test_31_full_graph_execution_all_models_failed(
    mock_post, mock_unload, mock_eval, base_state
):
    base_state["models"] = ["fail-1", "fail-2"]
    mock_eval.side_effect = RuntimeError("Fatal Crash")

    final_state = await benchmark_graph.ainvoke(base_state)

    assert len(final_state["completed_runs"]) == 0
    assert len(final_state["failed_models"]) == 2
    assert final_state["executive_summary"] == "No models were successfully evaluated."


def test_32_benchmark_graph_structure_nodes():
    nodes = set(benchmark_graph.nodes.keys())
    expected_nodes = {
        "initialize",
        "evaluate_model",
        "calculate_financials",
        "persist_data",
        "increment_index",
        "synthesize_summary"
    }
    assert expected_nodes.issubset(nodes)