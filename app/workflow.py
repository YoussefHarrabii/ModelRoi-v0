import time
import requests
from typing import TypedDict, List, Any, Optional
from langgraph.graph import StateGraph, END
from data.test_cases import TEST_CASES as test_cases
from app.engine import eval_prompt_streaming, unload_model
from app.calculator import calculate_financial_roi
from app.db import save_benchmark_results
from app.config import settings, ClusterConfig

class BenchmarkState(TypedDict):
    run_id: Optional[str]
    models: List[str]
    current_index: int
    cluster_config: Optional[ClusterConfig]  # Replaces electricity_cost
    required_rps: float                     # Added target workload requirement
    completed_runs: List[dict]
    failed_models: List[dict]
    last_run_failed: bool
    executive_summary: str

async def initialize_pipeline(state: BenchmarkState) -> dict:
    return {
        "current_index": 0,
        "completed_runs": [],
        "failed_models": [],
        "last_run_failed": False,
        "executive_summary": ""
    }

async def evaluate_model(state: BenchmarkState) -> dict:
    from app.main import RUN_STATUS_STORE  # Deferred import to prevent circular dependencies
    
    model_name = state["models"][state["current_index"]]
    total_models = len(state["models"])
    current_model_idx = state["current_index"]
    run_id = state.get("run_id")  # Ensure run_id is passed in initial_state

    if run_id and run_id in RUN_STATUS_STORE:
        model_progress_weight = 0.80 / max(total_models, 1)
        base_progress = 0.10 + (current_model_idx * model_progress_weight)
        RUN_STATUS_STORE[run_id] = {
            "status": "running",
            "progress": round(base_progress, 2),
            "message": f"Starting evaluation for {model_name}"
        }
    
    run_results = []
    total_cases = len(test_cases)
    
    try:
        for case_idx, case in enumerate(test_cases, start=1):
            result = eval_prompt_streaming(model_name, case)
            run_results.append(result)
            
            # Update global status store per prompt completion
            if run_id and run_id in RUN_STATUS_STORE:
                # Calculate progress: model chunk + prompt fraction inside model
                model_progress_weight = 0.80 / max(total_models, 1)
                base_progress = 0.10 + (current_model_idx * model_progress_weight)
                prompt_progress = (case_idx / total_cases) * model_progress_weight
                
                current_pct = min(base_progress + prompt_progress, 0.90)
                
                RUN_STATUS_STORE[run_id] = {
                    "status": "running",
                    "progress": round(current_pct, 2),
                    "message": f"Evaluating {model_name}: prompt {case_idx}/{total_cases} complete"
                }
            
        unload_model(model_name)
            
        avg_latency = sum(r["latency_ms"] for r in run_results) / len(run_results)
        avg_ttft = sum(r["ttft_ms"] for r in run_results) / len(run_results)
        avg_tps = sum(r["tps"] for r in run_results) / len(run_results)
        accuracy = (sum(1 for r in run_results if r["is_correct"]) / len(run_results)) * 100
        total_tokens = sum(r["eval_count"] for r in run_results)
        
        raw_run_data = {
            "model_name": model_name,
            "accuracy": accuracy,
            "avg_latency_ms": avg_latency,
            "avg_ttft_ms": avg_ttft,
            "avg_tps": avg_tps,
            "total_tokens": total_tokens,
            "evaluations": run_results,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return {
            "completed_runs": state["completed_runs"] + [raw_run_data],
            "last_run_failed": False
        }
        
    except Exception as e:
        error_log = {"model_name": model_name, "error": str(e)}
        return {
            "failed_models": state["failed_models"] + [error_log],
            "last_run_failed": True
        }

async def calculate_financials(state: BenchmarkState) -> dict:
    latest_run = state["completed_runs"][-1]
    
    total_input_tokens = sum(e.get("prompt_tokens", 0) for e in latest_run.get("evaluations", []))
    total_output_tokens = sum(e.get("eval_count", 0) for e in latest_run.get("evaluations", []))
    
    # Run the dynamic ROI & cluster capacity evaluation
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
    
    # Store top-level metrics
    latest_run["efficiency_score"] = roi_data["efficiency_score"]
    latest_run["cloud_cost_per_request_eur"] = roi_data["cloud_cost_per_request_eur"]
    
    # Extract cluster analysis metrics if present
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
        "accuracy": latest_run["accuracy"],
        "avg_latency_ms": latest_run["avg_latency_ms"],
        "avg_ttft_ms": latest_run["avg_ttft_ms"],
        "avg_tps": latest_run["avg_tps"],
        "total_tokens_used": latest_run["total_tokens"],
        "efficiency_score": latest_run["efficiency_score"],
        "breakeven_monthly_requests": latest_run.get("breakeven_requests"),
        "cluster_monthly_tco_eur": latest_run.get("cluster_monthly_tco_eur"),
        "max_rps": latest_run.get("max_rps"),
        "evaluations": latest_run.get("evaluations", [])
    }]
    
    save_benchmark_results(formatted_report)
    return {}

async def increment_index(state: BenchmarkState) -> dict:
    return {"current_index": state["current_index"] + 1}

def generate_deterministic_summary(completed_runs: list[dict]) -> str:
    """Generates a structured bulleted summary without LLM inference."""
    if not completed_runs:
        return "No completed runs available to summarize."

    # Identify top performers programmatically
    best_acc = max(completed_runs, key=lambda x: x.get("accuracy", 0))
    fastest_ttft = min(completed_runs, key=lambda x: x.get("avg_ttft_ms", float("inf")))
    highest_tps = max(completed_runs, key=lambda x: x.get("avg_tps", 0))

    bullets = [
        f"• **Top Accuracy:** {best_acc['model_name']} reached {best_acc['accuracy']:.1f}% accuracy.",
        f"• **Latency & Velocity:** {fastest_ttft['model_name']} achieved the fastest TTFT ({fastest_ttft['avg_ttft_ms']:.1f} ms), while {highest_tps['model_name']} hit peak throughput ({highest_tps['avg_tps']:.1f} tok/s).",
    ]

    # Include financial breakeven if recorded
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

    # Secondary Path: Pure Rule-Based Fallback (No extra LLM required)
    fallback_text = generate_deterministic_summary(state["completed_runs"])
    return {"executive_summary": fallback_text}

def route_after_evaluation(state: BenchmarkState) -> str:
    if state["last_run_failed"]:
        return "increment_index"
    return "calculate_financials"

def route_next_model(state: BenchmarkState) -> str:
    if state["current_index"] < len(state["models"]):
        return "evaluate_model"
    return "synthesize_summary"

workflow = StateGraph(BenchmarkState)

workflow.add_node("initialize", initialize_pipeline)
workflow.add_node("evaluate_model", evaluate_model)
workflow.add_node("calculate_financials", calculate_financials)
workflow.add_node("persist_data", persist_data)
workflow.add_node("increment_index", increment_index)
workflow.add_node("synthesize_summary", synthesize_summary)

workflow.set_entry_point("initialize")
workflow.add_edge("initialize", "evaluate_model")

workflow.add_conditional_edges(
    "evaluate_model",
    route_after_evaluation,
    {
        "calculate_financials": "calculate_financials",
        "increment_index": "increment_index"
    }
)

workflow.add_edge("calculate_financials", "persist_data")
workflow.add_edge("persist_data", "increment_index")

workflow.add_conditional_edges(
    "increment_index",
    route_next_model,
    {
        "evaluate_model": "evaluate_model",
        "synthesize_summary": "synthesize_summary"
    }
)

workflow.add_edge("synthesize_summary", END)

benchmark_graph = workflow.compile()