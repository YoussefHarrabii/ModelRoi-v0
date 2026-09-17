import sqlite3
import pytest
from unittest.mock import patch
from app.db import init_db, save_benchmark_results, BASE_DIR
from pathlib import Path


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    db_file = tmp_path / "data" / "test_benchmark.db"
    monkeypatch.setattr("app.db.DB_PATH", db_file)
    return db_file


@pytest.fixture
def initialized_db(temp_db):
    init_db()
    return temp_db


def math_report(model="M", **kw):
    item = {
        "model_name": model,
        "task": "math",
        "accuracy": 80.0,
        "avg_latency_ms": 100.0,
        "avg_ttft_ms": 10.0,
        "avg_tps": 20.0,
        "total_tokens_used": 500,
        "efficiency_score": 0.8,
        "evaluations": [
            {
                "test_id": 1, "question": "q?", "expected_answer": "4",
                "predicted_answer": "4", "math_category": 3,
                "is_correct": True, "latency_ms": 100.0,
                "ttft_ms": 10.0, "tps": 20.0,
            }
        ],
    }
    item.update(kw)
    return [item]


def sql_report():
    return [{
        "model_name": "S", "task": "sql", "accuracy": 50.0,
        "avg_latency_ms": 60.0, "avg_ttft_ms": 6.0, "avg_tps": 12.0,
        "total_tokens_used": 300, "efficiency_score": 0.5,
        "evaluations": [{
            "test_id": 7, "question": "q?", "expected_sql": "SELECT 1",
            "predicted_sql": "SELECT 1", "is_correct": True, "latency_ms": 60.0,
        }],
    }]


def extraction_report():
    return [{
        "model_name": "E", "task": "extraction", "accuracy": 90.0,
        "avg_latency_ms": 70.0, "avg_ttft_ms": 7.0, "avg_tps": 14.0,
        "total_tokens_used": 350, "efficiency_score": 0.9,
        "evaluations": [{
            "test_id": 3, "category": 1, "expected_indices": [1],
            "predicted_indices": [1], "precision": 1.0, "recall": 1.0,
            "f1": 1.0, "is_correct": True, "latency_ms": 70.0,
        }],
    }]


# ----------------------------------------------------------------------
# schema
# ----------------------------------------------------------------------

def test_init_creates_all_four_tables(initialized_db):
    with sqlite3.connect(initialized_db) as conn:
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert {"benchmark_runs", "extraction_logs", "sql_logs", "math_logs"}.issubset(tables)
    assert "prompt_logs" not in tables


def test_init_idempotent(initialized_db):
    init_db()
    init_db()
    with sqlite3.connect(initialized_db) as conn:
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert "math_logs" in tables


def test_benchmark_runs_has_task_column(initialized_db):
    save_benchmark_results(math_report())
    with sqlite3.connect(initialized_db) as conn:
        row = conn.execute("SELECT model_name, task, accuracy FROM benchmark_runs").fetchone()
    assert row == ("M", "math", 80.0)


def test_runs_require_task_column(initialized_db):
    with sqlite3.connect(initialized_db) as conn:
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("INSERT INTO benchmark_runs (model_name) VALUES ('x')")


def test_math_logs_cascade_on_run_delete(initialized_db):
    save_benchmark_results(math_report())
    with sqlite3.connect(initialized_db) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("DELETE FROM benchmark_runs WHERE id = 1;")
        conn.commit()
        assert conn.execute("SELECT COUNT(*) FROM math_logs").fetchone()[0] == 0


def test_child_fk_enforced(initialized_db):
    with sqlite3.connect(initialized_db) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("INSERT INTO math_logs (run_id) VALUES (999);")


# ----------------------------------------------------------------------
# per-task routing
# ----------------------------------------------------------------------

def test_save_math_routes_to_math_logs(initialized_db):
    save_benchmark_results(math_report())
    with sqlite3.connect(initialized_db) as conn:
        assert conn.execute("SELECT COUNT(*) FROM math_logs").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM sql_logs").fetchone()[0] == 0
        assert conn.execute("SELECT COUNT(*) FROM extraction_logs").fetchone()[0] == 0


def test_save_math_log_fields(initialized_db):
    save_benchmark_results(math_report())
    with sqlite3.connect(initialized_db) as conn:
        row = conn.execute(
            "SELECT question, expected_answer, predicted_answer, math_category, is_correct "
            "FROM math_logs"
        ).fetchone()
    assert row == ("q?", "4", "4", 3, 1)


def test_save_sql_routes_to_sql_logs(initialized_db):
    save_benchmark_results(sql_report())
    with sqlite3.connect(initialized_db) as conn:
        row = conn.execute("SELECT question, expected_sql, predicted_sql, is_correct FROM sql_logs").fetchone()
    assert row == ("q?", "SELECT 1", "SELECT 1", 1)


def test_save_extraction_routes_with_json_indices(initialized_db):
    import json
    save_benchmark_results(extraction_report())
    with sqlite3.connect(initialized_db) as conn:
        row = conn.execute(
            "SELECT category, expected_indices, predicted_indices, precision, recall, f1 "
            "FROM extraction_logs"
        ).fetchone()
    assert row[0] == 1
    assert json.loads(row[1]) == [1]
    assert json.loads(row[2]) == [1]
    assert row[3:6] == (1.0, 1.0, 1.0)


def test_save_unknown_task_raises_value_error(initialized_db):
    bad = math_report()
    bad[0]["task"] = "chess"
    with pytest.raises(ValueError, match="Unknown task"):
        save_benchmark_results(bad)


def test_save_missing_task_key_raises_keyerror(initialized_db):
    bad = math_report()
    del bad[0]["task"]
    with pytest.raises(KeyError):
        save_benchmark_results(bad)


def test_save_optional_metrics_default(initialized_db):
    save_benchmark_results(math_report())
    with sqlite3.connect(initialized_db) as conn:
        row = conn.execute(
            "SELECT breakeven_requests, cluster_monthly_tco_eur, max_rps FROM benchmark_runs"
        ).fetchone()
    assert row == (None, None, None)


def test_save_empty_report_list_no_rows(initialized_db):
    save_benchmark_results([])
    with sqlite3.connect(initialized_db) as conn:
        assert conn.execute("SELECT COUNT(*) FROM benchmark_runs").fetchone()[0] == 0


def test_save_isolated_per_run_id(initialized_db):
    save_benchmark_results(math_report(model="A"))
    save_benchmark_results(sql_report())
    with sqlite3.connect(initialized_db) as conn:
        n_runs = conn.execute("SELECT COUNT(*) FROM benchmark_runs").fetchone()[0]
        n_math = conn.execute("SELECT COUNT(*) FROM math_logs").fetchone()[0]
        n_sql = conn.execute("SELECT COUNT(*) FROM sql_logs").fetchone()[0]
    assert (n_runs, n_math, n_sql) == (2, 1, 1)


def test_base_dir_and_db_path():
    assert isinstance(BASE_DIR, Path) and BASE_DIR.is_absolute()
    from app.db import DB_PATH
    assert DB_PATH.name == "benchmark_history.db"
    assert DB_PATH.parent.name == "data"
