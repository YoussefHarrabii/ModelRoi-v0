from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import traceback
import uuid

from app.db import init_db
from app.workflow import benchmark_graph
from app.config import ClusterConfig


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="ModelEval ROI Engine",
    description="Hardware-safe benchmarking & financial unit economics engine for local LLMs",
    version="1.0.0",
    lifespan=lifespan
)

RUN_STATUS_STORE: Dict[str, Dict[str, Any]] = {}


class BenchmarkRequest(BaseModel):
    models: List[str] = ["gemma2:2b", "granite3.1-dense:2b", "qwen3.5:2b"]
    tasks: List[str] = ["extraction"]  # <-- NEW: task selection
    tests_per_task: int = Field(
        default=5,
        ge=1,
        description="Max total tests per task, sampled across categories",
    )
    seed: Optional[int] = Field(
        default=None,
        description="Random seed for test sampling; None = non-deterministic",
    )
    cluster_config: Optional[ClusterConfig] = Field(
        default=None,
        description="Hardware cluster specs for TCO & capacity analysis"
    )
    required_rps: float = Field(
        default=1.0,
        gt=0,
        description="Target requests per second to test feasibility"
    )


@app.get("/")
def health_check():
    return {"status": "online", "engine": "ModelEval ROI Engine v1.0.0"}


async def run_benchmark_background(run_id: str, payload: BenchmarkRequest):
    try:
        RUN_STATUS_STORE[run_id] = {
            "status": "running",
            "progress": 0.0,
            "message": "Initializing benchmark suite..."
        }

        all_results = []
        total_tasks = len(payload.tasks)
        completed_runs_combined = []

        for task_idx, task in enumerate(payload.tasks):
            # Update progress: 0% to 90% across all tasks
            progress_base = (task_idx / total_tasks) * 0.9 if total_tasks > 0 else 0.0
            RUN_STATUS_STORE[run_id] = {
                "status": "running",
                "progress": progress_base,
                "message": f"Running task {task_idx+1}/{total_tasks}: {task}"
            }

            initial_state = {
                "run_id": run_id,
                "models": payload.models,
                "task": task,
                "tests_per_task": payload.tests_per_task,
                "seed": payload.seed,
                "cluster_config": payload.cluster_config,
                "required_rps": payload.required_rps,
                "current_index": 0,
                "completed_runs": [],
                "last_run_failed": False,
                "executive_summary": ""
            }

            final_state = await benchmark_graph.ainvoke(initial_state)

            # Collect results from this task
            completed_runs_combined.extend(final_state.get("completed_runs", []))

            all_results.append({
                "task": task,
                "completed_runs": final_state.get("completed_runs", []),
                "executive_summary": final_state.get("executive_summary", "")
            })

        # Build combined summary
        combined_summary_parts = []
        for r in all_results:
            if r["executive_summary"]:
                combined_summary_parts.append(f"**Task: {r['task']}**\n{r['executive_summary']}")
            else:
                combined_summary_parts.append(f"**Task: {r['task']}**\nNo summary available.")

        combined_summary = "\n\n---\n\n".join(combined_summary_parts)

        RUN_STATUS_STORE[run_id] = {
            "status": "completed",
            "progress": 1.0,
            "message": "All benchmarks completed successfully!",
            "result": {
                "total_models_evaluated": len(completed_runs_combined),
                "executive_summary": combined_summary,
                "report": completed_runs_combined
            }
        }
    except Exception as e:
        traceback.print_exc()
        RUN_STATUS_STORE[run_id] = {
            "status": "failed",
            "progress": 1.0,
            "message": str(e)
        }


@app.post("/api/v1/benchmark", status_code=202)
def execute_benchmark(payload: BenchmarkRequest, background_tasks: BackgroundTasks) -> Dict[str, str]:
    # Validate that at least one task is selected
    if not payload.tasks:
        raise HTTPException(status_code=400, detail="At least one task must be selected.")

    run_id = str(uuid.uuid4())
    RUN_STATUS_STORE[run_id] = {"status": "pending", "progress": 0.0, "message": "Queued benchmark task..."}

    background_tasks.add_task(run_benchmark_background, run_id, payload)
    return {"run_id": run_id, "status": "pending"}


@app.get("/api/v1/status/{run_id}")
def get_benchmark_status(run_id: str) -> Dict[str, Any]:
    if run_id not in RUN_STATUS_STORE:
        raise HTTPException(status_code=404, detail="Run ID not found.")
    return RUN_STATUS_STORE[run_id]
