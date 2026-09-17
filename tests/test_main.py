import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app, RUN_STATUS_STORE, run_benchmark_background

# Initialize TestClient
client = TestClient(app)


# ----------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------

@pytest.fixture(autouse=True)
def clear_status_store():
    """Ensures RUN_STATUS_STORE is clean before and after every test."""
    RUN_STATUS_STORE.clear()
    yield
    RUN_STATUS_STORE.clear()


@pytest.fixture(autouse=True)
def mock_background_execution():
    """Prevents TestClient background tasks from triggering real model runs."""
    with patch("app.main.run_benchmark_background") as mock_bg:
        yield mock_bg


@pytest.fixture
def valid_cluster_payload():
    """Provides a valid ClusterConfig dictionary for payload testing."""
    return {
        "name": "Test-Cluster",
        "gpu_count": 2,
        "gpu_vram_gb": 24,
        "upfront_cost_eur": 10000.0,
        "power_draw_kw": 0.75,
    }


# ----------------------------------------------------------------------
# 1. Health Check Endpoint Tests (Tests 1–3)
# ----------------------------------------------------------------------

def test_01_health_check_status_200():
    response = client.get("/")
    assert response.status_code == 200


def test_02_health_check_payload():
    response = client.get("/")
    data = response.json()
    assert data["status"] == "online"
    assert "ModelEval ROI Engine" in data["engine"]


def test_03_health_check_invalid_method():
    response = client.post("/")
    assert response.status_code == 405  # Method Not Allowed


# ----------------------------------------------------------------------
# 2. Benchmark Execution Endpoint Validation Tests (Tests 4–15)
# ----------------------------------------------------------------------

def test_04_execute_benchmark_default_payload():
    response = client.post("/api/v1/benchmark", json={})
    assert response.status_code == 202
    data = response.json()
    assert "run_id" in data
    assert data["status"] == "pending"


def test_05_execute_benchmark_custom_models():
    payload = {"models": ["llama3:8b", "mistral:7b"]}
    response = client.post("/api/v1/benchmark", json=payload)
    assert response.status_code == 202
    run_id = response.json()["run_id"]
    assert run_id in RUN_STATUS_STORE


def test_06_execute_benchmark_with_valid_cluster_config(valid_cluster_payload):
    payload = {
        "models": ["gemma2:2b"],
        "cluster_config": valid_cluster_payload,
        "required_rps": 5.0
    }
    response = client.post("/api/v1/benchmark", json=payload)
    assert response.status_code == 202


def test_07_execute_benchmark_invalid_required_rps_zero():
    payload = {"required_rps": 0.0}
    response = client.post("/api/v1/benchmark", json=payload)
    assert response.status_code == 422


def test_08_execute_benchmark_invalid_required_rps_negative():
    payload = {"required_rps": -5.0}
    response = client.post("/api/v1/benchmark", json=payload)
    assert response.status_code == 422


def test_09_execute_benchmark_invalid_cluster_config_missing_required():
    payload = {
        "cluster_config": {
            "name": "Incomplete"
        }
    }
    response = client.post("/api/v1/benchmark", json=payload)
    assert response.status_code == 422


def test_10_execute_benchmark_returns_unique_uuids():
    res1 = client.post("/api/v1/benchmark", json={}).json()["run_id"]
    res2 = client.post("/api/v1/benchmark", json={}).json()["run_id"]
    assert res1 != res2


def test_11_execute_benchmark_registers_pending_in_status_store():
    response = client.post("/api/v1/benchmark", json={})
    run_id = response.json()["run_id"]
    assert RUN_STATUS_STORE[run_id]["status"] == "pending"
    assert RUN_STATUS_STORE[run_id]["progress"] == 0.0


def test_12_execute_benchmark_extra_unrecognized_fields_ignored():
    payload = {"models": ["gemma2:2b"], "unknown_field": "value"}
    response = client.post("/api/v1/benchmark", json=payload)
    assert response.status_code == 202


def test_13_execute_benchmark_empty_models_list_accepted():
    payload = {"models": []}
    response = client.post("/api/v1/benchmark", json=payload)
    assert response.status_code == 202


def test_14_execute_benchmark_invalid_json_body():
    response = client.post(
        "/api/v1/benchmark",
        content="invalid json",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 422


def test_15_execute_benchmark_wrong_content_type():
    response = client.post("/api/v1/benchmark", data="string data")
    assert response.status_code == 422


# ----------------------------------------------------------------------
# 3. Status Check Endpoint Tests (Tests 16–20)
# ----------------------------------------------------------------------

def test_16_get_status_nonexistent_run_id():
    response = client.get("/api/v1/status/nonexistent-uuid-123")
    assert response.status_code == 404
    assert response.json()["detail"] == "Run ID not found."


def test_17_get_status_pending_run():
    RUN_STATUS_STORE["test-id"] = {"status": "pending", "progress": 0.0, "message": "Queued"}
    response = client.get("/api/v1/status/test-id")
    assert response.status_code == 200
    assert response.json()["status"] == "pending"


def test_18_get_status_running_run():
    RUN_STATUS_STORE["test-id"] = {"status": "running", "progress": 0.45, "message": "Evaluating model 1"}
    response = client.get("/api/v1/status/test-id")
    assert response.status_code == 200
    assert response.json()["progress"] == 0.45


def test_19_get_status_completed_run():
    RUN_STATUS_STORE["test-id"] = {
        "status": "completed",
        "progress": 1.0,
        "result": {"total_models_evaluated": 2, "executive_summary": "Done"}
    }
    response = client.get("/api/v1/status/test-id")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["result"]["total_models_evaluated"] == 2


def test_20_get_status_failed_run():
    RUN_STATUS_STORE["test-id"] = {"status": "failed", "progress": 1.0, "message": "CUDA OOM"}
    response = client.get("/api/v1/status/test-id")
    assert response.status_code == 200
    assert response.json()["status"] == "failed"
    assert response.json()["message"] == "CUDA OOM"


# ----------------------------------------------------------------------
# 4. Background Task Processing Tests (Tests 21–25)
# ----------------------------------------------------------------------

@pytest.mark.asyncio
@patch("app.main.benchmark_graph.ainvoke")
async def test_21_run_benchmark_background_success(mock_ainvoke):
    mock_ainvoke.return_value = {
        "completed_runs": [{"model_name": "gemma2:2b"}],
        "executive_summary": "Execution successful"
    }

    from app.main import BenchmarkRequest
    req = BenchmarkRequest(models=["gemma2:2b"])
    
    await run_benchmark_background("run-123", req)

    status = RUN_STATUS_STORE["run-123"]
    assert status["status"] == "completed"
    assert status["progress"] == 1.0
    assert status["result"]["total_models_evaluated"] == 1
    assert "**Task: extraction**" in status["result"]["executive_summary"]
    assert "Execution successful" in status["result"]["executive_summary"]


@pytest.mark.asyncio
@patch("app.main.benchmark_graph.ainvoke")
async def test_22_run_benchmark_background_exception_handling(mock_ainvoke):
    mock_ainvoke.side_effect = RuntimeError("Workflow Graph execution error")

    from app.main import BenchmarkRequest
    req = BenchmarkRequest(models=["gemma2:2b"])
    
    await run_benchmark_background("run-err", req)

    status = RUN_STATUS_STORE["run-err"]
    assert status["status"] == "failed"
    assert status["progress"] == 1.0
    assert status["message"] == "Workflow Graph execution error"


@pytest.mark.asyncio
@patch("app.main.benchmark_graph.ainvoke")
async def test_23_run_benchmark_background_passes_run_id_in_initial_state(mock_ainvoke):
    mock_ainvoke.return_value = {}
    from app.main import BenchmarkRequest
    req = BenchmarkRequest(models=["gemma2:2b"], required_rps=2.5)

    await run_benchmark_background("custom-id", req)

    mock_ainvoke.assert_called_once()
    initial_state = mock_ainvoke.call_args[0][0]
    assert initial_state["run_id"] == "custom-id"
    assert initial_state["required_rps"] == 2.5


@pytest.mark.asyncio
@patch("app.main.benchmark_graph.ainvoke")
async def test_24_run_benchmark_background_handles_partial_failures(mock_ainvoke):
    mock_ainvoke.return_value = {
        "completed_runs": [{"model_name": "gemma2:2b"}],
        "executive_summary": "Partial completion"
    }

    from app.main import BenchmarkRequest
    req = BenchmarkRequest(models=["gemma2:2b", "broken-model"])
    
    await run_benchmark_background("run-partial", req)

    status = RUN_STATUS_STORE["run-partial"]
    assert status["status"] == "completed"
    assert status["result"]["total_models_evaluated"] == 1
    assert "failed_models" not in status["result"]


@pytest.mark.asyncio
@patch("app.main.benchmark_graph.ainvoke")
async def test_25_run_benchmark_background_initial_status_set_to_running(mock_ainvoke):
    async def verify_running_state(state):
        assert RUN_STATUS_STORE[state["run_id"]]["status"] == "running"
        return {"completed_runs": []}

    mock_ainvoke.side_effect = verify_running_state
    from app.main import BenchmarkRequest

    await run_benchmark_background("run-check", BenchmarkRequest())


@pytest.mark.asyncio
@patch("app.main.benchmark_graph.ainvoke")
async def test_26_run_benchmark_background_passes_seed(mock_ainvoke):
    mock_ainvoke.return_value = {}
    from app.main import BenchmarkRequest
    req = BenchmarkRequest(models=["gemma2:2b"], seed=123)

    await run_benchmark_background("seed-id", req)

    mock_ainvoke.assert_called_once()
    assert mock_ainvoke.call_args[0][0]["seed"] == 123


def test_36_execute_benchmark_tests_per_task_accepted():
    payload = {"models": ["gemma2:2b"], "tests_per_task": 50}
    response = client.post("/api/v1/benchmark", json=payload)
    assert response.status_code == 202


def test_37_execute_benchmark_tests_per_task_zero_rejected():
    payload = {"models": ["gemma2:2b"], "tests_per_task": 0}
    response = client.post("/api/v1/benchmark", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
@patch("app.main.benchmark_graph.ainvoke")
async def test_38_run_benchmark_background_propagates_tests_per_task(mock_ainvoke):
    mock_ainvoke.return_value = {}
    from app.main import BenchmarkRequest
    req = BenchmarkRequest(models=["gemma2:2b"], tests_per_task=42)

    await run_benchmark_background("run-tpt", req)

    initial_state = mock_ainvoke.call_args[0][0]
    assert initial_state["tests_per_task"] == 42


# ----------------------------------------------------------------------
# 5. Lifespan & App Setup Tests
# ----------------------------------------------------------------------

def test_33_lifespan_initializes_db():
    with patch("app.main.init_db") as mock_init:
        with TestClient(app):
            mock_init.assert_called_once()


def test_34_app_metadata_configured():
    assert app.title == "ModelEval ROI Engine"
    assert app.version == "1.0.0"


def test_35_status_store_isolation_between_requests():
    client.post("/api/v1/benchmark", json={})
    assert len(RUN_STATUS_STORE) == 1
    RUN_STATUS_STORE.clear()
    assert len(RUN_STATUS_STORE) == 0