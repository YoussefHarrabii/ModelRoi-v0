from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import sqlite3
import traceback
import uuid

from app.db import init_db, DB_PATH
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
        
        initial_state = {
            "run_id": run_id,  # <--- Pass run_id here so evaluate_model can find it
            "models": payload.models,
            "cluster_config": payload.cluster_config,
            "required_rps": payload.required_rps,
            "current_index": 0,
            "completed_runs": [],
            "failed_models": [],
            "last_run_failed": False,
            "executive_summary": ""
        }
        
        # Run workflow directly (evaluate_model handles live progress updates internally)
        final_state = await benchmark_graph.ainvoke(initial_state)
        
        RUN_STATUS_STORE[run_id] = {
            "status": "completed",
            "progress": 1.0,
            "message": "Benchmark completed successfully!",
            "result": {
                "total_models_evaluated": len(final_state.get("completed_runs", [])),
                "failed_models": final_state.get("failed_models", []),
                "executive_summary": final_state.get("executive_summary", ""),
                "report": final_state.get("completed_runs", [])
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
    run_id = str(uuid.uuid4())
    RUN_STATUS_STORE[run_id] = {"status": "pending", "progress": 0.0, "message": "Queued benchmark task..."}
    
    # Hand off to background execution immediately
    background_tasks.add_task(run_benchmark_background, run_id, payload)
    return {"run_id": run_id, "status": "pending"}


@app.get("/api/v1/status/{run_id}")
def get_benchmark_status(run_id: str) -> Dict[str, Any]:
    if run_id not in RUN_STATUS_STORE:
        raise HTTPException(status_code=404, detail="Run ID not found.")
    return RUN_STATUS_STORE[run_id]


@app.get("/api/v1/history")
def get_benchmark_history() -> List[Dict[str, Any]]:
    if not DB_PATH.exists():
        return []
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM benchmark_runs ORDER BY id DESC")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")