import logging
import time
from typing import Any, Dict, Optional
import requests

from app.config import settings

logger = logging.getLogger(__name__)

OLLAMA_URL = settings.OLLAMA_HOST
session = requests.Session()

OPTIMIZED_OPTIONS = {
    "temperature": 0.0,
    "num_ctx": 2048,
    "num_predict": 128,
}

def call_ollama(
    model_name: str,
    system_prompt: str,
    user_prompt: str,
    options: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
    expect_json: bool = False,
) -> Dict[str, Any]:
    payload = {
        "model": model_name,
        "system": system_prompt,
        "prompt": user_prompt,
        
        "stream": False,
        "think": False,
        "keep_alive": "10m",
        "options": options or OPTIMIZED_OPTIONS,
    }

    if expect_json:
        payload["format"] = "json"

    start = time.perf_counter()
    try:
        resp = session.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()

        total_latency = (time.perf_counter() - start) * 1000.0

        prompt_eval_ns = data.get("prompt_eval_duration", 0)
        eval_ns = data.get("eval_duration", 0)
        eval_count = data.get("eval_count", 0)
        prompt_eval_count = data.get("prompt_eval_count", 0)

        ttft = (prompt_eval_ns / 1e6) if prompt_eval_ns > 0 else total_latency
        tps = (eval_count / (eval_ns / 1e9)) if eval_ns > 0 else 0.0

        return {
            "response": data.get("response", "").strip(),
            "latency_ms": round(total_latency, 2),
            "ttft_ms": round(ttft, 2),
            "tps": round(tps, 2),
            "prompt_tokens": prompt_eval_count,
            "eval_count": eval_count,
            "error": None,
        }

    except Exception as e:
        logger.error(f"Ollama call failed: {e}")
        return {
            "response": "",
            "latency_ms": 0.0,
            "ttft_ms": 0.0,
            "tps": 0.0,
            "prompt_tokens": 0,
            "eval_count": 0,
            "error": str(e),
        }