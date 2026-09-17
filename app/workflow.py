import time
import json
import requests
import traceback
from typing import TypedDict, List, Any, Optional
from langgraph.graph import StateGraph, END
import random

import os

from app.engine import call_ollama
from app.calculator import calculate_financial_roi
from app.db import save_benchmark_results
from app.config import settings, ClusterConfig

from data.extractiontests import TEST_CASES as extraction_cases
from data.sqltests import SQL_TESTS as sql_cases
from data.mathtests import MATH_TESTS as math_cases

from app.tasks import extraction, math_task, sql


# ---------- State Definition ----------
class BenchmarkState(TypedDict):
    run_id: Optional[str]
    models: List[str]
    task: str                     # "extraction", "sql", "math"
    tests_per_task: Optional[int]
    seed: Optional[int]
    current_index: int
    cluster_config: Optional[ClusterConfig]
    required_rps: float
    completed_runs: List[dict]
    last_run_failed: bool
    executive_summary: str


# ---------- Node Implementations ----------
async def initialize_pipeline(state: BenchmarkState) -> dict:
    """Run once at the beginning to set the state."""
    return {
        "current_index": 0,
        "completed_runs": [],
        "last_run_failed": False,
        "executive_summary": "",
    }


def route_after_evaluation(state: BenchmarkState) -> str:
    if state["last_run_failed"]:
        return "increment_index"
    return "calculate_financials"


def route_next_model(state: BenchmarkState) -> str:
    """Route to the next evaluator if there are more models, else to summary."""
    if state["current_index"] < len(state["models"]):
        # Route to the evaluator for the current task
        return {
            "extraction": "evaluate_extraction",
            "sql": "evaluate_sql",
            "math": "evaluate_math",
        }.get(state["task"], "evaluate_extraction")
    return "synthesize_summary"


# ---- Generic evaluation loop ----
def run_task_evaluation(
    model_name: str,
    test_cases: list,
    task_handler,
    limit: Optional[int] = None,
    expect_json: bool = False,
    task_name: str = "",
    seed: Optional[int] = None,
) -> dict:
    """
    Evaluates a single model on a list of test cases for a given task.
    If `limit` is provided, shuffles and samples that many tests across the task.
    `seed` makes the sample reproducible; None = non-deterministic.
    Returns raw_run_data (including evaluations) and success flag.
    """
    # ---- Sampling: limit total per task ----
    if limit and limit > 0:
        test_cases = list(test_cases)
        random.Random(seed).shuffle(test_cases)
        test_cases = test_cases[:limit]
        print(f"DEBUG: Sampled {len(test_cases)} cases (limit {limit} per task)")

    # ---- Original evaluation loop ----
    run_results = []
    total = len(test_cases)
    print(f"🔍 Starting evaluation for {model_name} on {total} cases")

    for idx, case in enumerate(test_cases, start=1):
        print(f"  Case {idx}/{total}: building prompt...")
        system_prompt, user_prompt = task_handler.build_prompt(case)

        print(f"  Case {idx}/{total}: calling Ollama...")
        raw = call_ollama(model_name, system_prompt, user_prompt, expect_json=expect_json)
        print(f"  Case {idx}/{total}: got response (latency: {raw.get('latency_ms', 'N/A')} ms)")

        print(f"  Case {idx}/{total}: scoring...")
        scored = task_handler.score(raw, case)
        print(f"  Case {idx}/{total}: scored -> {scored.get('score', 'N/A')}")

        eval_record = {
            "test_id": case.get("id"),
            "latency_ms": raw["latency_ms"],
            "ttft_ms": raw["ttft_ms"],
            "tps": raw["tps"],
            "prompt_tokens": raw["prompt_tokens"],
            "eval_count": raw["eval_count"],
            "error": raw["error"],
            **scored,
        }
        run_results.append(eval_record)
        print(f"  Case {idx}/{total}: done.\n")

    # Aggregate metrics
    scores = [r.get("score", 0.0) for r in run_results if "score" in r]
    avg_score = (sum(scores) / len(scores)) * 100 if scores else 0.0
    avg_latency = sum(r["latency_ms"] for r in run_results) / len(run_results)
    avg_ttft = sum(r["ttft_ms"] for r in run_results) / len(run_results)
    avg_tps = sum(r["tps"] for r in run_results) / len(run_results)
    total_tokens = sum(r["prompt_tokens"] + r["eval_count"] for r in run_results)

    raw_run_data = {
        "model_name": model_name,
        "accuracy": round(avg_score, 2),
        "avg_latency_ms": round(avg_latency, 2),
        "avg_ttft_ms": round(avg_ttft, 2),
        "avg_tps": round(avg_tps, 2),
        "total_tokens": total_tokens,
        "evaluations": run_results,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

        # --- Write debug logs (passed/failed) to disk (overwrite each run) ---
    LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "debug_logs")
    os.makedirs(LOG_DIR, exist_ok=True)

    # Build logged entries (same as before)
    logged_entries = []
    for idx, eval_record in enumerate(run_results):
        case = test_cases[idx]
        question = case.get("question", case.get("query", ""))
        entry = {
            "question": question,
            "score": eval_record.get("score"),
            "is_correct": eval_record.get("is_correct"),
            "expected": eval_record.get("expected_answer") or eval_record.get("expected_indices") or eval_record.get("expected_sql"),
            "predicted": eval_record.get("predicted_answer") or eval_record.get("predicted_indices") or eval_record.get("predicted_sql"),
            "latency_ms": eval_record.get("latency_ms"),
        }
        logged_entries.append(entry)

    # Split into passed and failed
    passed = [e for e in logged_entries if e.get("score", 0) >= 0.5]
    failed = [e for e in logged_entries if e.get("score", 0) < 0.5]

    # Use fixed filenames per task+model (overwrites previous run, no cross-task clobbering)
    model_safe = model_name.replace(":", "_")
    prefix = f"{task_name}_" if task_name else ""
    passed_path = os.path.join(LOG_DIR, f"passed_{prefix}{model_safe}.json")
    failed_path = os.path.join(LOG_DIR, f"failed_{prefix}{model_safe}.json")

    if passed:
        with open(passed_path, "w", encoding="utf-8") as f:
            json.dump(passed, f, indent=2)
    else:
        # Remove empty passed file if exists
        if os.path.exists(passed_path):
            os.remove(passed_path)

    if failed:
        with open(failed_path, "w", encoding="utf-8") as f:
            json.dump(failed, f, indent=2)
    else:
        if os.path.exists(failed_path):
            os.remove(failed_path)

    print(f"📁 Logged {len(passed)} passed, {len(failed)} failed for {model_name} (overwritten)")

    return raw_run_data


# ---- Individual evaluator nodes ----
async def evaluate_extraction(state: BenchmarkState) -> dict:
    model = state["models"][state["current_index"]]
    raw_data = run_task_evaluation(
        model, extraction_cases, extraction,
        limit=state.get("tests_per_task"),
        expect_json=True,
        task_name=state.get("task", ""),
        seed=state.get("seed")
    )
    return {"completed_runs": state["completed_runs"] + [raw_data], "last_run_failed": False}


async def evaluate_sql(state: BenchmarkState) -> dict:
    model = state["models"][state["current_index"]]
    try:
        raw_data = run_task_evaluation(
            model, sql_cases, sql,
            limit=state.get("tests_per_task"),
            expect_json=False,
            task_name=state.get("task", ""),
            seed=state.get("seed")
        )
        print(f"DEBUG: raw_data type = {type(raw_data)}")
        print(f"DEBUG: raw_data content = {raw_data}")
    except Exception:
        print(f"ERROR in evaluate_sql:")
        traceback.print_exc()
        return {"completed_runs": state["completed_runs"], "last_run_failed": True}
    return {"completed_runs": state["completed_runs"] + [raw_data], "last_run_failed": False}


async def evaluate_math(state: BenchmarkState) -> dict:
    model = state["models"][state["current_index"]]
    try:
        raw_data = run_task_evaluation(
            model, math_cases, math_task,
            limit=state.get("tests_per_task"),
            expect_json=False,
            task_name=state.get("task", ""),
            seed=state.get("seed")
        )
        print(f"DEBUG evaluate_math: raw_data type = {type(raw_data)}")
        print(f"DEBUG evaluate_math: keys = {raw_data.keys() if isinstance(raw_data, dict) else 'NOT A DICT'}")
    except Exception:
        print(f"ERROR in evaluate_math:")
        traceback.print_exc()
        return {"completed_runs": state["completed_runs"], "last_run_failed": True}
    return {"completed_runs": state["completed_runs"] + [raw_data], "last_run_failed": False}


# ---- Shared nodes (fully implemented) ----
async def calculate_financials(state: BenchmarkState) -> dict:
    latest_run = state["completed_runs"][-1]
    total_input_tokens = sum(e.get("prompt_tokens", 0) for e in latest_run.get("evaluations", []))
    total_output_tokens = sum(e.get("eval_count", 0) for e in latest_run.get("evaluations", []))
    roi_data = calculate_financial_roi(
        model_name=latest_run["model_name"],
        total_input_tokens=total_input_tokens,
        total_output_tokens=total_output_tokens,
        total_requests=len(latest_run.get("evaluations", [])),
        local_avg_latency_ms=latest_run["avg_latency_ms"],
        local_accuracy=latest_run["accuracy"],
        cluster=state.get("cluster_config"),
        required_rps=state.get("required_rps", 1.0)
    )
    latest_run["efficiency_score"] = roi_data["efficiency_score"]
    latest_run["cloud_cost_per_request_eur"] = roi_data["cloud_cost_per_request_eur"]
    cluster_analysis = roi_data.get("cluster_analysis")
    if cluster_analysis:
        latest_run["cluster_monthly_tco_eur"] = cluster_analysis["tco"]["total_monthly_tco_eur"]
        latest_run["max_rps"] = cluster_analysis["throughput"]["max_rps"]
        latest_run["breakeven_requests"] = cluster_analysis["breakeven"].get("breakeven_monthly_requests")
        latest_run["cluster_feasible"] = cluster_analysis["breakeven"].get("feasible", True)
        latest_run["recommendation"] = cluster_analysis["breakeven"].get("recommendation", "")
    else:
        latest_run["breakeven_requests"] = None
    latest_run["roi_data"] = roi_data
    updated_runs = state["completed_runs"][:-1] + [latest_run]
    return {"completed_runs": updated_runs}


async def persist_data(state: BenchmarkState) -> dict:
    latest_run = state["completed_runs"][-1]
    formatted_report = [{
        "model_name": latest_run["model_name"],
        "task": state["task"],
        "accuracy": latest_run["accuracy"],
        "avg_latency_ms": latest_run["avg_latency_ms"],
        "avg_ttft_ms": latest_run["avg_ttft_ms"],
        "avg_tps": latest_run["avg_tps"],
        "total_tokens_used": latest_run["total_tokens"],
        "efficiency_score": latest_run.get("efficiency_score", 0.0),
        "breakeven_monthly_requests": latest_run.get("breakeven_requests"),
        "cluster_monthly_tco_eur": latest_run.get("cluster_monthly_tco_eur"),
        "max_rps": latest_run.get("max_rps"),
        "evaluations": latest_run.get("evaluations", []),
    }]
    save_benchmark_results(formatted_report)
    return {}


async def increment_index(state: BenchmarkState) -> dict:
    return {"current_index": state["current_index"] + 1}


def generate_deterministic_summary(completed_runs: list[dict]) -> str:
    if not completed_runs:
        return "No completed runs available to summarize."
    best_acc = max(completed_runs, key=lambda x: x.get("accuracy", 0))
    fastest_ttft = min(completed_runs, key=lambda x: x.get("avg_ttft_ms", float("inf")))
    highest_tps = max(completed_runs, key=lambda x: x.get("avg_tps", 0))
    bullets = [
        f"• **Top Accuracy:** {best_acc['model_name']} reached {best_acc['accuracy']:.1f}% accuracy.",
        f"• **Latency & Velocity:** {fastest_ttft['model_name']} achieved the fastest TTFT ({fastest_ttft['avg_ttft_ms']:.1f} ms), while {highest_tps['model_name']} hit peak throughput ({highest_tps['avg_tps']:.1f} tok/s).",
    ]
    be_runs = [r for r in completed_runs if r.get("breakeven_requests")]
    if be_runs:
        lowest_be = min(be_runs, key=lambda x: x["breakeven_requests"])
        bullets.append(f"• **Cloud Breakeven:** {lowest_be['model_name']} offers the lowest breakeven threshold at {lowest_be['breakeven_requests']:,} monthly requests.")
    return "[Rule-Based Fallback Synthesis]\n" + "\n".join(bullets)


async def synthesize_summary(state: BenchmarkState) -> dict:
    if not state["completed_runs"]:
        return {"executive_summary": "No models were successfully evaluated."}
    lean_telemetry = []
    for run in state["completed_runs"]:
        lean_run = {k: v for k, v in run.items() if k != "evaluations"}
        lean_telemetry.append(lean_run)
    summary_prompt = f"""You are a senior AI Infrastructure Architect.
Analyze the following local LLM benchmark results and produce a concise 3-bullet executive summary comparing model performance, speed, accuracy, cluster capacity (RPS), and cloud breakeven volumes.

Benchmark Telemetry:
{lean_telemetry}

Keep the response professional, highly direct, and actionable."""

    clean_api_key = str(settings.OPENROUTER_API_KEY).strip("'\" ")
    headers = {
        "Authorization": f"Bearer {clean_api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "ModelEval ROI Engine"
    }
    payload = {
        "model": settings.OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": summary_prompt}],
        "temperature": 0.3
    }
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=15
        )
        response.raise_for_status()
        data = response.json()
        if "error" not in data and "choices" in data and len(data["choices"]) > 0:
            summary_text = data["choices"][0]["message"].get("content", "")
            return {"executive_summary": f"[Cloud Synthesis - OpenRouter]\n{summary_text}"}
    except Exception as e:
        print(f"OpenRouter synthesis failed ({e}). Generating deterministic fallback summary...")
    fallback_text = generate_deterministic_summary(state["completed_runs"])
    return {"executive_summary": fallback_text}


# ---------- Graph Construction ----------
workflow = StateGraph(BenchmarkState)

# Nodes
workflow.add_node("initialize", initialize_pipeline)
workflow.add_node("evaluate_extraction", evaluate_extraction)
workflow.add_node("evaluate_sql", evaluate_sql)
workflow.add_node("evaluate_math", evaluate_math)
workflow.add_node("calculate_financials", calculate_financials)
workflow.add_node("persist_data", persist_data)
workflow.add_node("increment_index", increment_index)
workflow.add_node("synthesize_summary", synthesize_summary)

# Entry point
workflow.set_entry_point("initialize")

# From initialize -> route to the first evaluator based on task
workflow.add_conditional_edges(
    "initialize",
    lambda state: state["task"],
    {
        "extraction": "evaluate_extraction",
        "sql": "evaluate_sql",
        "math": "evaluate_math",
    }
)

# From each evaluator -> after evaluation
workflow.add_conditional_edges(
    "evaluate_extraction",
    route_after_evaluation,
    {"calculate_financials": "calculate_financials", "increment_index": "increment_index"}
)
workflow.add_conditional_edges(
    "evaluate_sql",
    route_after_evaluation,
    {"calculate_financials": "calculate_financials", "increment_index": "increment_index"}
)
workflow.add_conditional_edges(
    "evaluate_math",
    route_after_evaluation,
    {"calculate_financials": "calculate_financials", "increment_index": "increment_index"}
)

# Success path
workflow.add_edge("calculate_financials", "persist_data")
workflow.add_edge("persist_data", "increment_index")

# From increment_index -> next model or summary
workflow.add_conditional_edges(
    "increment_index",
    route_next_model,
    {
        "evaluate_extraction": "evaluate_extraction",
        "evaluate_sql": "evaluate_sql",
        "evaluate_math": "evaluate_math",
        "synthesize_summary": "synthesize_summary"
    }
)

# Final edge
workflow.add_edge("synthesize_summary", END)

benchmark_graph = workflow.compile()