import pytest
from unittest.mock import patch, MagicMock
from app.engine import (
    prewarm_model,
    eval_prompt_streaming,
    unload_model,
    SYSTEM_PROMPT,
    OPTIMIZED_OPTIONS,
)


# ----------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------

@pytest.fixture
def valid_test_case():
    return {
        "id": 101,
        "prompt": "Book a flight to Berlin",
        "expected_intent_id": 12
    }


@pytest.fixture
def mock_ollama_success():
    return {
        "model": "gemma2:2b",
        "created_at": "2026-03-08T12:00:00Z",
        "response": '{"intent_id": 12}',
        "done": True,
        "prompt_eval_duration": 150_000_000,  # 150ms
        "eval_duration": 800_000_000,         # 800ms
        "prompt_eval_count": 15,
        "eval_count": 8
    }


# ----------------------------------------------------------------------
# 1. Prewarm Model Tests (Tests 1–3)
# ----------------------------------------------------------------------

@patch("app.engine.session.post")
def test_01_prewarm_model_success(mock_post):
    mock_post.return_value.status_code = 200
    prewarm_model("gemma2:2b")

    mock_post.assert_called_once()
    url = mock_post.call_args[0][0]
    payload = mock_post.call_args[1]["json"]

    assert "/api/generate" in url
    assert payload["model"] == "gemma2:2b"
    assert payload["prompt"] == "ping"
    assert payload["keep_alive"] == "10m"
    assert payload["options"] == OPTIMIZED_OPTIONS


@patch("app.engine.session.post")
def test_02_prewarm_model_handles_exception_gracefully(mock_post):
    mock_post.side_effect = Exception("Ollama connection refused")
    # Must not raise an exception or break caller execution
    try:
        prewarm_model("gemma2:2b")
    except Exception as e:
        pytest.fail(f"prewarm_model raised unexpected exception: {e}")


@patch("app.engine.session.post")
def test_03_prewarm_model_passes_timeout(mock_post):
    prewarm_model("gemma2:2b")
    assert mock_post.call_args[1]["timeout"] == 10


# ----------------------------------------------------------------------
# 2. Benchmark Evaluation Success & Metric Tests (Tests 4–8)
# ----------------------------------------------------------------------

@patch("app.engine.session.post")
def test_04_eval_prompt_streaming_success_correct_prediction(mock_post, valid_test_case, mock_ollama_success):
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = mock_ollama_success
    mock_post.return_value = mock_resp

    result = eval_prompt_streaming("gemma2:2b", valid_test_case)

    assert result["test_id"] == 101
    assert result["predicted_intent_id"] == 12
    assert result["is_correct"] is True
    assert result["prompt_tokens"] == 15
    assert result["eval_count"] == 8
    assert result["error"] is None


@patch("app.engine.session.post")
def test_05_eval_prompt_streaming_incorrect_prediction(mock_post, valid_test_case, mock_ollama_success):
    mock_ollama_success["response"] = '{"intent_id": 999}'  # Mismatched ID
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = mock_ollama_success
    mock_post.return_value = mock_resp

    result = eval_prompt_streaming("gemma2:2b", valid_test_case)

    assert result["predicted_intent_id"] == 999
    assert result["is_correct"] is False


@patch("app.engine.session.post")
def test_06_eval_prompt_streaming_metric_calculations(mock_post, valid_test_case, mock_ollama_success):
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = mock_ollama_success
    mock_post.return_value = mock_resp

    result = eval_prompt_streaming("gemma2:2b", valid_test_case)

    # TTFT = 150,000,000 ns / 1e6 = 150.0 ms
    assert result["ttft_ms"] == 150.0
    # TPS = 8 tokens / (800,000,000 ns / 1e9) = 10.0 TPS
    assert result["tps"] == 10.0


@patch("app.engine.session.post")
def test_07_eval_prompt_streaming_zero_duration_metric_fallbacks(mock_post, valid_test_case, mock_ollama_success):
    mock_ollama_success["prompt_eval_duration"] = 0
    mock_ollama_success["eval_duration"] = 0
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = mock_ollama_success
    mock_post.return_value = mock_resp

    result = eval_prompt_streaming("gemma2:2b", valid_test_case)

    assert result["tps"] == 0.0
    assert result["ttft_ms"] == result["latency_ms"]


@patch("app.engine.session.post")
def test_08_eval_prompt_streaming_sends_required_payload_options(mock_post, valid_test_case, mock_ollama_success):
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = mock_ollama_success
    mock_post.return_value = mock_resp

    eval_prompt_streaming("gemma2:2b", valid_test_case)

    payload = mock_post.call_args[1]["json"]
    assert payload["model"] == "gemma2:2b"
    assert payload["system"] == SYSTEM_PROMPT
    assert payload["format"] == "json"
    assert payload["stream"] is False
    assert payload["think"] is False
    assert payload["keep_alive"] == "10m"


# ----------------------------------------------------------------------
# 3. Output Parsing & Edge Case Resilience Tests (Tests 9–12)
# ----------------------------------------------------------------------

@patch("app.engine.session.post")
def test_09_eval_prompt_streaming_invalid_json_output(mock_post, valid_test_case, mock_ollama_success):
    mock_ollama_success["response"] = "Not valid JSON output from LLM"
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = mock_ollama_success
    mock_post.return_value = mock_resp

    result = eval_prompt_streaming("gemma2:2b", valid_test_case)

    assert result["predicted_intent_id"] is None
    assert result["is_correct"] is False
    assert result["raw_output"] == "Not valid JSON output from LLM"
    assert result["error"] is None  # Handled as prediction parsing failure, not network crash


@patch("app.engine.session.post")
def test_10_eval_prompt_streaming_missing_intent_id_key_in_json(mock_post, valid_test_case, mock_ollama_success):
    mock_ollama_success["response"] = '{"other_key": "some_value"}'
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = mock_ollama_success
    mock_post.return_value = mock_resp

    result = eval_prompt_streaming("gemma2:2b", valid_test_case)

    assert result["predicted_intent_id"] is None
    assert result["is_correct"] is False


@patch("app.engine.session.post")
def test_11_eval_prompt_streaming_http_status_error(mock_post, valid_test_case):
    mock_resp = MagicMock()
    mock_resp.raise_for_status.side_effect = Exception("500 Internal Server Error")
    mock_post.return_value = mock_resp

    result = eval_prompt_streaming("broken-model", valid_test_case)

    assert result["predicted_intent_id"] is None
    assert result["is_correct"] is False
    assert "500 Internal Server Error" in result["error"]


@patch("app.engine.session.post")
def test_12_eval_prompt_streaming_network_timeout(mock_post, valid_test_case):
    mock_post.side_effect = Exception("ReadTimeoutError")

    result = eval_prompt_streaming("gemma2:2b", valid_test_case)

    assert result["predicted_intent_id"] is None
    assert result["latency_ms"] == 0.0
    assert result["error"] == "ReadTimeoutError"


# ----------------------------------------------------------------------
# 4. Unload Model Tests (Tests 13–15)
# ----------------------------------------------------------------------

@patch("requests.post")
def test_13_unload_model_success(mock_post):
    mock_post.return_value.status_code = 200
    unload_model("gemma2:2b")

    mock_post.assert_called_once()
    url = mock_post.call_args[0][0]
    payload = mock_post.call_args[1]["json"]

    assert "/api/generate" in url
    assert payload["model"] == "gemma2:2b"
    assert payload["keep_alive"] == 0


@patch("requests.post")
def test_14_unload_model_exception_suppression(mock_post):
    mock_post.side_effect = Exception("Connection reset by peer")
    try:
        unload_model("gemma2:2b")
    except Exception as e:
        pytest.fail(f"unload_model raised unexpected exception: {e}")


@patch("requests.post")
def test_15_unload_model_timeout_parameter(mock_post):
    unload_model("gemma2:2b")
    assert mock_post.call_args[1]["timeout"] == 10