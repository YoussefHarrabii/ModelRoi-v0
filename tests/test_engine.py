import pytest
from unittest.mock import patch, MagicMock
from app.engine import (
    call_ollama,
    OPTIMIZED_OPTIONS,
)


@pytest.fixture
def ollama_ok():
    return {
        "model": "gemma2:2b",
        "created_at": "2026-03-08T12:00:00Z",
        "response": "  42  ",
        "done": True,
        "prompt_eval_duration": 150_000_000,  # 150ms
        "eval_duration": 800_000_000,         # 800ms
        "prompt_eval_count": 15,
        "eval_count": 8,
    }


def ollama_response(payload):
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = payload
    return mock_resp


# ----------------------------------------------------------------------
# call_ollama
# ----------------------------------------------------------------------

@patch("app.engine.session.post")
def test_call_ollama_success_metrics(mock_post, ollama_ok):
    mock_post.return_value = ollama_response(ollama_ok)

    res = call_ollama("gemma2:2b", "sys", "hi")

    assert res["response"] == "42"  # stripped
    assert res["ttft_ms"] == 150.0  # 150ms / 1e6
    assert res["tps"] == 10.0  # 8 / 0.8s
    assert res["prompt_tokens"] == 15
    assert res["eval_count"] == 8
    assert res["error"] is None
    assert res["latency_ms"] > 0


@patch("app.engine.session.post")
def test_call_ollama_payload_shape(mock_post, ollama_ok):
    mock_post.return_value = ollama_response(ollama_ok)

    call_ollama("gemma2:2b", "sys", "hi")

    payload = mock_post.call_args[1]["json"]
    assert payload["model"] == "gemma2:2b"
    assert payload["system"] == "sys"
    assert payload["prompt"] == "hi"
    assert payload["stream"] is False
    assert payload["think"] is False
    assert payload["keep_alive"] == "10m"
    assert payload["options"] == OPTIMIZED_OPTIONS
    assert "format" not in payload


@patch("app.engine.session.post")
def test_call_ollama_expect_json_sets_format(mock_post, ollama_ok):
    mock_post.return_value = ollama_response(ollama_ok)

    call_ollama("gemma2:2b", "sys", "hi", expect_json=True)

    assert mock_post.call_args[1]["json"]["format"] == "json"


@patch("app.engine.session.post")
def test_call_ollama_custom_options_override(mock_post, ollama_ok):
    mock_post.return_value = ollama_response(ollama_ok)
    custom = {"temperature": 0.7}

    call_ollama("gemma2:2b", "sys", "hi", options=custom)

    assert mock_post.call_args[1]["json"]["options"] == custom


@patch("app.engine.session.post")
def test_call_ollama_zero_durations_fallback(mock_post, ollama_ok):
    ollama_ok["prompt_eval_duration"] = 0
    ollama_ok["eval_duration"] = 0
    mock_post.return_value = ollama_response(ollama_ok)

    res = call_ollama("gemma2:2b", "sys", "hi")

    assert res["tps"] == 0.0
    assert res["ttft_ms"] == res["latency_ms"]


@patch("app.engine.session.post")
def test_call_ollama_http_error_returns_zeroed_payload(mock_post):
    mock_resp = MagicMock()
    mock_resp.raise_for_status.side_effect = Exception("500 Internal Server Error")
    mock_post.return_value = mock_resp

    res = call_ollama("broken-model", "sys", "hi")

    assert res["response"] == ""
    assert res["latency_ms"] == 0.0
    assert res["tps"] == 0.0
    assert "500 Internal Server Error" in res["error"]


@patch("app.engine.session.post")
def test_call_ollama_timeout_returns_zeroed_payload(mock_post):
    mock_post.side_effect = Exception("ReadTimeoutError")

    res = call_ollama("gemma2:2b", "sys", "hi")

    assert res["response"] == ""
    assert res["latency_ms"] == 0.0
    assert res["error"] == "ReadTimeoutError"


@patch("app.engine.session.post")
def test_call_ollama_uses_configured_timeout(mock_post, ollama_ok):
    mock_post.return_value = ollama_response(ollama_ok)

    call_ollama("gemma2:2b", "sys", "hi", timeout=45)

    assert mock_post.call_args[1]["timeout"] == 45
