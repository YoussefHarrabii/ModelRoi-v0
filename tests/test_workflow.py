import pytest
from unittest.mock import patch, MagicMock
from app.workflow import (
    BenchmarkState,
    initialize_pipeline,
    run_task_evaluation,
    evaluate_extraction,
    evaluate_math,
    evaluate_sql,
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


@pytest.fixture
def base_state() -> BenchmarkState:
    return {
        "run_id": "test_run_123",
        "models": ["model-a", "model-b"],
        "task": "math",
        "tests_per_task": 5,
        "current_index": 0,
        "cluster_config": ClusterConfig(
            name="A10G-Cluster",
            gpu_count=2,
            gpu_vram_gb=24,
            upfront_cost_eur=10000.0,
            power_draw_kw=0.75,
        ),
        "required_rps": 10.0,
        "completed_runs": [],
        "last_run_failed": False,
        "executive_summary": "",
    }


@pytest.fixture
def ollama_result():
    return {
        "response": "4",
        "latency_ms": 100.0,
        "ttft_ms": 20.0,
        "tps": 50.0,
        "prompt_tokens": 150,
        "eval_count": 50,
        "error": None,
    }


# ----------------------------------------------------------------------
# initialize + routing
# ----------------------------------------------------------------------

async def test_initialize_pipeline_resets_defaults(base_state):
    base_state["current_index"] = 5
    base_state["completed_runs"] = [{"some": "data"}]
    base_state["last_run_failed"] = True
    base_state["executive_summary"] = "Old summary"

    res = await initialize_pipeline(base_state)

    assert res["current_index"] == 0
    assert res["completed_runs"] == []
    assert res["last_run_failed"] is False
    assert res["executive_summary"] == ""


def test_route_after_evaluation_success(base_state):
    base_state["last_run_failed"] = False
    assert route_after_evaluation(base_state) == "calculate_financials"


def test_route_after_evaluation_failure(base_state):
    base_state["last_run_failed"] = True
    assert route_after_evaluation(base_state) == "increment_index"


def test_route_next_model_per_task(base_state):
    base_state["models"] = ["m1", "m2"]
    base_state["current_index"] = 0
    base_state["task"] = "math"
    assert route_next_model(base_state) == "evaluate_math"
    base_state["task"] = "sql"
    assert route_next_model(base_state) == "evaluate_sql"
    base_state["task"] = "extraction"
    assert route_next_model(base_state) == "evaluate_extraction"


def test_route_next_model_ends_loop(base_state):
    base_state["models"] = ["m1", "m2"]
    base_state["current_index"] = 2
    assert route_next_model(base_state) == "synthesize_summary"


# ----------------------------------------------------------------------
# run_task_evaluation sampling + scoring loop
# ----------------------------------------------------------------------

def _math_case(answer="4"):
    return {"question": "Solve for x: 2x + 5 = 13", "answer": answer, "category": 3}


@patch("app.workflow.call_ollama")
def test_run_task_evaluation_limits_total_per_task(mock_call, ollama_result):
    from app.tasks import math_task
    mock_call.return_value = dict(ollama_result)
    cases = [_math_case() for _ in range(10)]

    out = run_task_evaluation("m", cases, math_task, limit=4)

    assert len(out["evaluations"]) == 4
    assert mock_call.call_count == 4


@patch("app.workflow.call_ollama")
def test_run_task_evaluation_no_limit_runs_full_bank(mock_call, ollama_result):
    from app.tasks import math_task
    mock_call.return_value = dict(ollama_result)
    cases = [_math_case() for _ in range(6)]

    out = run_task_evaluation("m", cases, math_task)

    assert len(out["evaluations"]) == 6
    assert out["accuracy"] == 100.0
    assert out["avg_latency_ms"] == 100.0
    assert out["total_tokens"] == 1200  # (150 + 50) * 6


@patch("app.workflow.call_ollama")
def test_run_task_evaluation_scores_incorrect(mock_call, ollama_result):
    from app.tasks import math_task
    mock_call.return_value = dict(ollama_result, response="999")
    out = run_task_evaluation("m", [_math_case()], math_task)
    assert out["accuracy"] == 0.0
    assert out["evaluations"][0]["is_correct"] is False


@patch("app.workflow.call_ollama")
def test_run_task_evaluation_ollama_error_counts_as_failure(mock_call):
    from app.tasks import math_task
    mock_call.return_value = {
        "response": "", "latency_ms": 0.0, "ttft_ms": 0.0, "tps": 0.0,
        "prompt_tokens": 0, "eval_count": 0, "error": "boom",
    }
    out = run_task_evaluation("m", [_math_case()], math_task)
    assert out["accuracy"] == 0.0


@patch("app.workflow.call_ollama")
def test_run_task_evaluation_seed_reproducible(mock_call, ollama_result):
    from app.tasks import math_task
    mock_call.return_value = dict(ollama_result)
    cases = [
        {"id": i, "question": "Solve for x: 2x + 5 = 13", "answer": "4", "category": 3}
        for i in range(10)
    ]

    out1 = run_task_evaluation("m", cases, math_task, limit=4, seed=42)
    out2 = run_task_evaluation("m", cases, math_task, limit=4, seed=42)

    ids1 = [e["test_id"] for e in out1["evaluations"]]
    ids2 = [e["test_id"] for e in out2["evaluations"]]
    assert len(ids1) == 4
    assert ids1 == ids2


# ----------------------------------------------------------------------
# per-task evaluator nodes
# ----------------------------------------------------------------------

@patch("app.workflow.call_ollama")
async def test_evaluate_math_appends_completed_run(mock_call, base_state, ollama_result):
    mock_call.return_value = dict(ollama_result)
    base_state["task"] = "math"
    with patch("app.workflow.math_cases", [_math_case()]):
        res = await evaluate_math(base_state)
    assert res["last_run_failed"] is False
    assert len(res["completed_runs"]) == 1
    assert res["completed_runs"][0]["model_name"] == "model-a"


@patch("app.workflow.call_ollama")
async def test_evaluate_math_marks_failed_run(mock_call, base_state):
    mock_call.side_effect = RuntimeError("Ollama OOM")
    base_state["task"] = "math"
    with patch("app.workflow.math_cases", [_math_case()]):
        res = await evaluate_math(base_state)
    assert res["last_run_failed"] is True
    assert res["completed_runs"] == []


@patch("app.workflow.call_ollama")
async def test_evaluate_sql_routes_and_scores(mock_call, base_state):
    mock_call.return_value = {
        "response": "SELECT 1;", "latency_ms": 10.0, "ttft_ms": 2.0, "tps": 5.0,
        "prompt_tokens": 10, "eval_count": 2, "error": None,
    }
    base_state["task"] = "sql"
    res = await evaluate_sql(base_state)
    assert res["last_run_failed"] is False
    assert len(res["completed_runs"]) == 1


@patch("app.workflow.call_ollama")
async def test_evaluate_extraction_json_mode(mock_call, base_state):
    mock_call.return_value = {
        "response": '{"indices": [1]}', "latency_ms": 10.0, "ttft_ms": 2.0, "tps": 5.0,
        "prompt_tokens": 10, "eval_count": 2, "error": None,
    }
    base_state["task"] = "extraction"
    cases = [
        {"query": "q1", "paragraphs": ["p0", "p1"], "expected_indices": [1]},
        {"query": "q2", "paragraphs": ["p0", "p1"], "expected_indices": [0]},
    ]
    with patch("app.workflow.extraction_cases", cases):
        res = await evaluate_extraction(base_state)
    assert res["last_run_failed"] is False
    assert len(res["completed_runs"]) == 1
    assert mock_call.call_args[1]["expect_json"] is True


# ----------------------------------------------------------------------
# financials / persist / summaries (unchanged behavior)
# ----------------------------------------------------------------------

@patch("app.workflow.calculate_financial_roi")
async def test_calculate_financials_with_cluster_analysis(mock_roi, base_state):
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
            "breakeven": {"breakeven_monthly_requests": 3000000, "feasible": True, "recommendation": "Use local cluster"}
        }
    }
    res = await calculate_financials(base_state)
    latest = res["completed_runs"][0]
    assert latest["efficiency_score"] == 0.95
    assert latest["cluster_monthly_tco_eur"] == 1500.0
    assert latest["max_rps"] == 30.0
    assert latest["breakeven_requests"] == 3000000
    assert latest["cluster_feasible"] is True


@patch("app.workflow.calculate_financial_roi")
async def test_calculate_financials_token_accounting(mock_roi, base_state):
    base_state["completed_runs"] = [{
        "model_name": "model-a", "avg_latency_ms": 100.0, "accuracy": 90.0,
        "evaluations": [{"prompt_tokens": 10, "eval_count": 20}, {"prompt_tokens": 15, "eval_count": 25}]
    }]
    mock_roi.return_value = {"efficiency_score": 0.8, "cloud_cost_per_request_eur": 0.001}
    await calculate_financials(base_state)
    mock_roi.assert_called_once_with(
        model_name="model-a", total_input_tokens=25, total_output_tokens=45,
        total_requests=2, local_avg_latency_ms=100.0, local_accuracy=90.0,
        cluster=base_state["cluster_config"], required_rps=10.0,
    )


@patch("app.workflow.save_benchmark_results")
async def test_persist_data_formats_report(mock_save, base_state):
    base_state["task"] = "math"
    base_state["completed_runs"] = [{
        "model_name": "model-a", "accuracy": 95.0, "avg_latency_ms": 80.0,
        "avg_ttft_ms": 15.0, "avg_tps": 60.0, "total_tokens": 1200,
        "efficiency_score": 0.92, "breakeven_requests": 500000,
        "cluster_monthly_tco_eur": 800.0, "max_rps": 40.0,
        "evaluations": [{"test_id": 1}]
    }]
    res = await persist_data(base_state)
    assert res == {}
    saved = mock_save.call_args[0][0][0]
    assert saved["task"] == "math"
    assert saved["total_tokens_used"] == 1200
    assert saved["breakeven_monthly_requests"] == 500000


async def test_increment_index_advances_counter(base_state):
    base_state["current_index"] = 1
    assert await increment_index(base_state) == {"current_index": 2}


def test_generate_deterministic_summary_empty_runs():
    assert generate_deterministic_summary([]) == "No completed runs available to summarize."


def test_generate_deterministic_summary_highlights_top_performers():
    runs = [
        {"model_name": "SlowAccurate", "accuracy": 95.0, "avg_ttft_ms": 100.0, "avg_tps": 20.0, "breakeven_requests": 1000000},
        {"model_name": "FastInaccurate", "accuracy": 70.0, "avg_ttft_ms": 10.0, "avg_tps": 100.0, "breakeven_requests": 500000}
    ]
    summary = generate_deterministic_summary(runs)
    assert "[Rule-Based Fallback Synthesis]" in summary
    assert "SlowAccurate" in summary and "95.0%" in summary
    assert "500,000 monthly requests" in summary


async def test_synthesize_summary_empty_runs(base_state):
    base_state["completed_runs"] = []
    assert await synthesize_summary(base_state) == {"executive_summary": "No models were successfully evaluated."}


@patch("requests.post")
async def test_synthesize_summary_openrouter_success(mock_post, base_state):
    base_state["completed_runs"] = [{"model_name": "model-a", "accuracy": 90.0}]
    mock_response = MagicMock()
    mock_response.json.return_value = {"choices": [{"message": {"content": "Bullet 1"}}]}
    mock_post.return_value = mock_response
    res = await synthesize_summary(base_state)
    assert "[Cloud Synthesis - OpenRouter]" in res["executive_summary"]


@patch("requests.post")
async def test_synthesize_summary_falls_back_on_error(mock_post, base_state):
    base_state["completed_runs"] = [{"model_name": "model-a", "accuracy": 90.0, "avg_ttft_ms": 10.0, "avg_tps": 50.0}]
    mock_post.side_effect = Exception("API Timeout")
    res = await synthesize_summary(base_state)
    assert "[Rule-Based Fallback Synthesis]" in res["executive_summary"]


def test_benchmark_graph_structure_nodes():
    nodes = set(benchmark_graph.nodes.keys())
    assert {
        "initialize", "evaluate_extraction", "evaluate_sql", "evaluate_math",
        "calculate_financials", "persist_data", "increment_index", "synthesize_summary",
    }.issubset(nodes)


@patch("app.workflow.call_ollama")
@patch("app.workflow.calculate_financial_roi")
@patch("app.workflow.save_benchmark_results")
@patch("requests.post")
async def test_full_graph_single_math_model(mock_post, mock_save, mock_roi, mock_call, base_state, ollama_result):
    base_state["models"] = ["model-a"]
    base_state["task"] = "math"
    mock_call.return_value = dict(ollama_result)
    mock_roi.return_value = {"efficiency_score": 0.9, "cloud_cost_per_request_eur": 0.001}
    mock_response = MagicMock()
    mock_response.json.return_value = {"choices": [{"message": {"content": "Summary"}}]}
    mock_post.return_value = mock_response
    with patch("app.workflow.math_cases", [_math_case()]):
        final_state = await benchmark_graph.ainvoke(base_state)
    assert final_state["current_index"] == 1
    assert len(final_state["completed_runs"]) == 1
    assert "[Cloud Synthesis - OpenRouter]" in final_state["executive_summary"]
    mock_save.assert_called_once()
