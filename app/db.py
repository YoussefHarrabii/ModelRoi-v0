import json
import sqlite3
from pathlib import Path
from typing import Dict, Any, List

BASE_DIR = Path(__file__).resolve().parent.parent if "__file__" in locals() else Path.cwd()
DB_PATH = BASE_DIR / "data" / "benchmark_history.db"


def init_db():
    """Initialize the multi‑task benchmark database schema."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        # --- 1. Parent table: benchmark_runs (universal metrics) ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS benchmark_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                model_name TEXT,
                task TEXT NOT NULL,           -- 'extraction', 'sql', 'math'
                accuracy REAL,                -- task‑specific score (F1, exact‑match, etc.)
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

        # --- 2. Child table for extraction task ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS extraction_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER NOT NULL,
                test_id INTEGER,
                category INTEGER,
                expected_indices TEXT,   -- JSON list
                predicted_indices TEXT,  -- JSON list
                precision REAL,
                recall REAL,
                f1 REAL,
                is_correct BOOLEAN,
                latency_ms REAL,
                ttft_ms REAL,
                tps REAL,
                FOREIGN KEY (run_id) REFERENCES benchmark_runs(id) ON DELETE CASCADE
            )
        """)

        # --- 3. Child table for SQL task ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sql_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER NOT NULL,
                test_id INTEGER,
                question TEXT,
                expected_sql TEXT,
                predicted_sql TEXT,
                is_correct BOOLEAN,
                latency_ms REAL,
                ttft_ms REAL,
                tps REAL,
                FOREIGN KEY (run_id) REFERENCES benchmark_runs(id) ON DELETE CASCADE
            )
        """)

        # --- 4. Child table for math task ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS math_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            test_id INTEGER,
            question TEXT,
            expected_answer TEXT,
            predicted_answer TEXT,
            math_category INTEGER,   -- <-- NEW (1-7 for derivatives, integrals, etc.)
            is_correct BOOLEAN,
            latency_ms REAL,
            ttft_ms REAL,
            tps REAL,
            FOREIGN KEY (run_id) REFERENCES benchmark_runs(id) ON DELETE CASCADE
        )
        """)

        conn.commit()


def save_benchmark_results(report: List[Dict[str, Any]]):
    """
    Save benchmark results to the database.

    Each item in `report` must contain:
        - model_name, accuracy, avg_latency_ms, avg_ttft_ms, avg_tps,
          total_tokens, efficiency_score, breakeven_requests,
          cluster_monthly_tco_eur, max_rps, task, evaluations
        - `task` must be one of 'extraction', 'sql', 'math'.
        - `evaluations` is a list of per‑query result dicts.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        for item in report:
            # 1. Insert into benchmark_runs
            cursor.execute("""
                INSERT INTO benchmark_runs (
                    model_name, task, accuracy,
                    avg_latency_ms, avg_ttft_ms, avg_tps, total_tokens,
                    efficiency_score, breakeven_requests,
                    cluster_monthly_tco_eur, max_rps
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item["model_name"],
                item["task"],
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
            task = item["task"]

            # 2. Route evaluations to the correct child table
            for eval_item in item["evaluations"]:
                # Common fields
                latency = eval_item.get("latency_ms", 0.0)
                ttft = eval_item.get("ttft_ms", 0.0)
                tps = eval_item.get("tps", 0.0)

                if task == "extraction":
                    cursor.execute("""
                        INSERT INTO extraction_logs (
                            run_id, test_id, category,
                            expected_indices, predicted_indices,
                            precision, recall, f1, is_correct,
                            latency_ms, ttft_ms, tps
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        run_id,
                        eval_item["test_id"],
                        eval_item.get("category"),
                        json.dumps(eval_item.get("expected_indices", [])),
                        json.dumps(eval_item.get("predicted_indices", [])),
                        eval_item.get("precision", 0.0),
                        eval_item.get("recall", 0.0),
                        eval_item.get("f1", 0.0),
                        eval_item.get("is_correct", False),
                        latency,
                        ttft,
                        tps
                    ))

                elif task == "sql":
                    cursor.execute("""
                        INSERT INTO sql_logs (
                            run_id, test_id, question,
                            expected_sql, predicted_sql, is_correct,
                            latency_ms, ttft_ms, tps
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        run_id,
                        eval_item["test_id"],
                        eval_item.get("question", ""),
                        eval_item.get("expected_sql", ""),
                        eval_item.get("predicted_sql", ""),
                        eval_item.get("is_correct", False),
                        latency,
                        ttft,
                        tps
                    ))

                elif task == "math":
                    cursor.execute("""
                        INSERT INTO math_logs (
                            run_id, test_id, question,
                            expected_answer, predicted_answer, math_category, is_correct,
                            latency_ms, ttft_ms, tps
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        run_id,
                        eval_item["test_id"],
                        eval_item.get("question", ""),
                        eval_item.get("expected_answer", ""),
                        eval_item.get("predicted_answer", ""),
                        eval_item.get("math_category"),  # <-- ADD THIS
                        eval_item.get("is_correct", False),
                        latency,
                        ttft,
                        tps
                    ))

                else:
                    raise ValueError(f"Unknown task: {task}")

        conn.commit()