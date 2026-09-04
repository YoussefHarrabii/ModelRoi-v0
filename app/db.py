import sqlite3
from pathlib import Path
from typing import Dict, Any, List

# Force absolute path to project root
BASE_DIR = Path(__file__).resolve().parent.parent if "__file__" in locals() else Path.cwd()
DB_PATH = BASE_DIR / "data" / "benchmark_history.db"


def init_db():
    """Initializes SQLite tables for benchmark runs and prompt logs with cluster & category support."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        # Updated benchmark_runs schema to store TCO and Max RPS
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS benchmark_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                model_name TEXT,
                accuracy REAL,
                avg_latency_ms REAL,
                avg_ttft_ms REAL,
                avg_tps REAL,
                total_tokens INTEGER,
                efficiency_score REAL,
                breakeven_requests INTEGER,
                cluster_monthly_tco_eur REAL,
                max_rps REAL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prompt_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER,
                test_id INTEGER,
                model_name TEXT,
                category TEXT,
                expected_id INTEGER,
                predicted_id INTEGER,
                is_correct BOOLEAN,
                latency_ms REAL,
                ttft_ms REAL,
                tps REAL,
                FOREIGN KEY(run_id) REFERENCES benchmark_runs(id) ON DELETE CASCADE
            )
        """)
        conn.commit()


def save_benchmark_results(report: List[Dict[str, Any]]):
    """Saves benchmark runs and individual prompt evaluations including cluster info into SQLite."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        for item in report:
            cursor.execute("""
                INSERT INTO benchmark_runs 
                (model_name, accuracy, avg_latency_ms, avg_ttft_ms, avg_tps, total_tokens, 
                 efficiency_score, breakeven_requests, cluster_monthly_tco_eur, max_rps)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item["model_name"], 
                item["accuracy"], 
                item["avg_latency_ms"], 
                item.get("avg_ttft_ms", 0.0),
                item.get("avg_tps", 0.0),
                item["total_tokens_used"], 
                item["efficiency_score"], 
                item.get("breakeven_monthly_requests"),
                item.get("cluster_monthly_tco_eur"),
                item.get("max_rps")
            ))
            
            run_id = cursor.lastrowid
            
            for eval_item in item["evaluations"]:
                cursor.execute("""
                    INSERT INTO prompt_logs 
                    (run_id, test_id, model_name, category, expected_id, predicted_id, is_correct, latency_ms, ttft_ms, tps)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    run_id,
                    eval_item["test_id"],
                    item["model_name"],
                    eval_item["category"],
                    eval_item["expected_intent_id"],
                    eval_item["predicted_intent_id"],
                    eval_item["is_correct"],
                    eval_item["latency_ms"],
                    eval_item.get("ttft_ms", 0.0),
                    eval_item.get("tps", 0.0)
                ))
                
        conn.commit()