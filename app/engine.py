import json
import logging
import time
from typing import Any, Dict
import requests

from app.config import settings
from data.test_cases import GROUND_TRUTH

logger = logging.getLogger(__name__)

OLLAMA_URL = settings.OLLAMA_HOST

# Re-use TCP connection pool across all benchmark evaluations
session = requests.Session()

SYSTEM_PROMPT = f"""You are an intent classification engine. Classify the user input into exactly one intent ID:
{GROUND_TRUTH}

Respond strictly with valid JSON: {{"intent_id": <number>}}"""

# Lock payload options across all warmups and evaluation calls to preserve KV cache
OPTIMIZED_OPTIONS = {
    "temperature": 0.0,
    "num_ctx": 512,
    "num_predict": 16,
}


def prewarm_model(model_name: str) -> None:
    """Pre-warms and locks model context in VRAM prior to benchmark execution."""
    try:
        session.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": model_name,
                "prompt": "ping",
                "stream": False,
                "keep_alive": "10m",
                "options": OPTIMIZED_OPTIONS,
            },
            timeout=10,
        )
    except Exception as e:
        logger.warning(f"Failed to prewarm model '{model_name}': {e}")


def eval_prompt_streaming(model_name: str, test_case: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluates prompt with fixed option schemas to prevent Windows thread locks."""
    payload = {
        "model": model_name,
        "system": SYSTEM_PROMPT,
        "prompt": test_case["prompt"],
        "format": "json",
        "stream": False,
        "think": False,
        "keep_alive": "10m",
        "options": OPTIMIZED_OPTIONS,
    }

    start_time = time.perf_counter()

    try:
        response = session.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()

        total_latency_ms = (time.perf_counter() - start_time) * 1000.0

        # Native internal timings from Ollama
        prompt_eval_ns = data.get("prompt_eval_duration", 0)
        eval_ns = data.get("eval_duration", 0)
        eval_count = data.get("eval_count", 0)
        prompt_eval_count = data.get("prompt_eval_count", 0)

        ttft_ms = (prompt_eval_ns / 1e6) if prompt_eval_ns > 0 else total_latency_ms
        tps = (eval_count / (eval_ns / 1e9)) if eval_ns > 0 else 0.0

        raw_output = data.get("response", "").strip()

        # Parse JSON output safely
        predicted_id = None
        try:
            parsed = json.loads(raw_output)
            predicted_id = parsed.get("intent_id")
        except Exception:
            predicted_id = None

        return {
            "test_id": test_case["id"],
            "prompt": test_case["prompt"],
            "category": test_case["expected_intent_id"],
            "expected_intent_id": test_case["expected_intent_id"],
            "predicted_intent_id": predicted_id,
            "raw_output": raw_output,
            "is_correct": (predicted_id == test_case["expected_intent_id"]),
            "latency_ms": round(total_latency_ms, 2),
            "prompt_tokens": prompt_eval_count,
            "ttft_ms": round(ttft_ms, 2),
            "tps": round(tps, 2),
            "eval_count": eval_count,
            "error": None,
        }

    except Exception as e:
        return {
            "test_id": test_case["id"],
            "prompt": test_case["prompt"],
            "category": test_case["expected_intent_id"],
            "expected_intent_id": test_case["expected_intent_id"],
            "predicted_intent_id": None,
            "raw_output": "",
            "is_correct": False,
            "latency_ms": 0.0,
            "prompt_tokens": 0,
            "ttft_ms": 0.0,
            "tps": 0.0,
            "eval_count": 0,
            "error": str(e),
        }


def unload_model(model_name: str) -> None:
    """Safely unloads model from VRAM/RAM by setting keep_alive to 0."""
    try:
        requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": model_name, "keep_alive": 0},
            timeout=10,
        )
    except Exception as e:
        logger.warning(f"Failed to unload model '{model_name}': {e}")