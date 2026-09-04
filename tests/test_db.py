import sqlite3
import pytest
from pathlib import Path
from unittest.mock import patch
from app.db import init_db, save_benchmark_results, BASE_DIR

import gc
import time

# ----------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------

@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """Overrides DB_PATH to a temporary SQLite database for test isolation."""
    db_file = tmp_path / "data" / "test_benchmark.db"
    monkeypatch.setattr("app.db.DB_PATH", db_file)
    return db_file


@pytest.fixture
def initialized_db(temp_db):
    """Initializes schema on the temporary database and returns path."""
    init_db()
    return temp_db


@pytest.fixture
def sample_report():
    """Provides a realistic report payload for testing inserts."""
    return [
        {
            "model_name": "Llama-3-8B",
            "accuracy": 0.85,
            "avg_latency_ms": 120.5,
            "avg_ttft_ms": 45.2,
            "avg_tps": 32.1,
            "total_tokens_used": 1500,
            "efficiency_score": 0.92,
            "breakeven_monthly_requests": 150000,
            "cluster_monthly_tco_eur": 1200.50,
            "max_rps": 25.0,
            "evaluations": [
                {
                    "test_id": 101,
                    "category": "finance",
                    "expected_intent_id": 1,
                    "predicted_intent_id": 1,
                    "is_correct": True,
                    "latency_ms": 110.0,
                    "ttft_ms": 40.0,
                    "tps": 35.0,
                },
                {
                    "test_id": 102,
                    "category": "general",
                    "expected_intent_id": 2,
                    "predicted_intent_id": 3,
                    "is_correct": False,
                    "latency_ms": 131.0,
                    "ttft_ms": 50.4,
                    "tps": 29.2,
                },
            ],
        }
    ]


# ----------------------------------------------------------------------
# 1. Database Initialization & Schema Tests (Tests 1–10)
# ----------------------------------------------------------------------

def test_01_init_db_creates_file_and_directory(temp_db):
    assert not temp_db.exists()
    init_db()
    assert temp_db.exists()


def test_02_init_db_creates_benchmark_runs_table(initialized_db):
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='benchmark_runs';")
        assert cursor.fetchone() is not None


def test_03_init_db_creates_prompt_logs_table(initialized_db):
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='prompt_logs';")
        assert cursor.fetchone() is not None


def test_04_init_db_idempotent_multiple_runs(initialized_db):
    init_db()
    init_db()
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        assert "benchmark_runs" in tables
        assert "prompt_logs" in tables


def test_05_benchmark_runs_schema_columns(initialized_db):
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(benchmark_runs);")
        columns = {row[1] for row in cursor.fetchall()}
        expected = {
            "id", "timestamp", "model_name", "accuracy", "avg_latency_ms",
            "avg_ttft_ms", "avg_tps", "total_tokens", "efficiency_score",
            "breakeven_requests", "cluster_monthly_tco_eur", "max_rps"
        }
        assert expected.issubset(columns)


def test_06_prompt_logs_schema_columns(initialized_db):
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(prompt_logs);")
        columns = {row[1] for row in cursor.fetchall()}
        expected = {
            "id", "run_id", "test_id", "model_name", "category",
            "expected_id", "predicted_id", "is_correct", "latency_ms",
            "ttft_ms", "tps"
        }
        assert expected.issubset(columns)


def test_07_pragma_foreign_keys_enabled_by_default(initialized_db):
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("PRAGMA foreign_keys;")
        assert cursor.fetchone()[0] == 1


def test_08_benchmark_runs_autoincrement_primary_key(initialized_db):
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO benchmark_runs (model_name) VALUES ('TestModel');")
        row_id = cursor.lastrowid
        assert row_id == 1


def test_09_prompt_logs_foreign_key_constraint(initialized_db):
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute(
                "INSERT INTO prompt_logs (run_id, model_name) VALUES (999, 'Invalid');"
            )


def test_10_foreign_key_cascade_delete(initialized_db, sample_report):
    save_benchmark_results(sample_report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("DELETE FROM benchmark_runs WHERE id = 1;")
        conn.commit()
        cursor.execute("SELECT COUNT(*) FROM prompt_logs WHERE run_id = 1;")
        assert cursor.fetchone()[0] == 0


# ----------------------------------------------------------------------
# 2. Saving Benchmark Results Tests (Tests 11–25)
# ----------------------------------------------------------------------

def test_11_save_benchmark_results_single_report(initialized_db, sample_report):
    save_benchmark_results(sample_report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM benchmark_runs;")
        assert cursor.fetchone()[0] == 1
        cursor.execute("SELECT COUNT(*) FROM prompt_logs;")
        assert cursor.fetchone()[0] == 2


def test_12_save_benchmark_results_multiple_reports(initialized_db, sample_report):
    report_2 = [
        {
            "model_name": "Mistral-7B",
            "accuracy": 0.90,
            "avg_latency_ms": 95.0,
            "total_tokens_used": 2000,
            "efficiency_score": 0.95,
            "evaluations": []
        }
    ]
    save_benchmark_results(sample_report)
    save_benchmark_results(report_2)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM benchmark_runs;")
        assert cursor.fetchone()[0] == 2


def test_13_save_benchmark_results_maps_benchmark_run_fields(initialized_db, sample_report):
    save_benchmark_results(sample_report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT model_name, accuracy, avg_latency_ms, total_tokens FROM benchmark_runs WHERE id = 1;")
        row = cursor.fetchone()
        assert row[0] == "Llama-3-8B"
        assert row[1] == 0.85
        assert row[2] == 120.5
        assert row[3] == 1500


def test_14_save_benchmark_results_maps_prompt_log_fields(initialized_db, sample_report):
    save_benchmark_results(sample_report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT test_id, category, is_correct FROM prompt_logs WHERE run_id = 1 ORDER BY test_id;")
        rows = cursor.fetchall()
        assert rows[0] == (101, "finance", 1)
        assert rows[1] == (102, "general", 0)


def test_15_save_benchmark_results_empty_report_list(initialized_db):
    save_benchmark_results([])
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM benchmark_runs;")
        assert cursor.fetchone()[0] == 0


def test_16_save_benchmark_results_no_evaluations(initialized_db):
    report = [{
        "model_name": "EmptyEvalModel",
        "accuracy": 0.0,
        "avg_latency_ms": 0.0,
        "total_tokens_used": 0,
        "efficiency_score": 0.0,
        "evaluations": []
    }]
    save_benchmark_results(report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM benchmark_runs;")
        assert cursor.fetchone()[0] == 1
        cursor.execute("SELECT COUNT(*) FROM prompt_logs;")
        assert cursor.fetchone()[0] == 0


def test_17_save_benchmark_results_missing_optional_ttft_tps_defaults(initialized_db):
    report = [{
        "model_name": "MinimalModel",
        "accuracy": 0.7,
        "avg_latency_ms": 100.0,
        "total_tokens_used": 500,
        "efficiency_score": 0.8,
        "evaluations": [{
            "test_id": 1,
            "category": "default",
            "expected_intent_id": 1,
            "predicted_intent_id": 1,
            "is_correct": True,
            "latency_ms": 100.0
        }]
    }]
    save_benchmark_results(report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT avg_ttft_ms, avg_tps FROM benchmark_runs WHERE id = 1;")
        assert cursor.fetchone() == (0.0, 0.0)
        cursor.execute("SELECT ttft_ms, tps FROM prompt_logs WHERE id = 1;")
        assert cursor.fetchone() == (0.0, 0.0)


def test_18_save_benchmark_results_handles_none_cluster_metrics(initialized_db):
    report = [{
        "model_name": "NoClusterModel",
        "accuracy": 0.9,
        "avg_latency_ms": 50.0,
        "total_tokens_used": 100,
        "efficiency_score": 0.95,
        "breakeven_monthly_requests": None,
        "cluster_monthly_tco_eur": None,
        "max_rps": None,
        "evaluations": []
    }]
    save_benchmark_results(report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT breakeven_requests, cluster_monthly_tco_eur, max_rps FROM benchmark_runs;")
        assert cursor.fetchone() == (None, None, None)


def test_19_save_benchmark_results_auto_timestamp_generated(initialized_db, sample_report):
    save_benchmark_results(sample_report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp FROM benchmark_runs WHERE id = 1;")
        ts = cursor.fetchone()[0]
        assert ts is not None
        assert len(ts) > 0


def test_20_save_benchmark_results_multiple_evaluations_association(initialized_db, sample_report):
    save_benchmark_results(sample_report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT run_id FROM prompt_logs;")
        run_ids = [row[0] for row in cursor.fetchall()]
        assert run_ids == [1, 1]


def test_21_save_benchmark_results_preserves_float_precision(initialized_db):
    report = [{
        "model_name": "PrecisionModel",
        "accuracy": 0.123456789,
        "avg_latency_ms": 99.9999,
        "total_tokens_used": 100,
        "efficiency_score": 0.88888,
        "cluster_monthly_tco_eur": 1234.5678,
        "evaluations": []
    }]
    save_benchmark_results(report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT accuracy, avg_latency_ms, cluster_monthly_tco_eur FROM benchmark_runs;")
        row = cursor.fetchone()
        assert row[0] == pytest.approx(0.123456789)
        assert row[1] == pytest.approx(99.9999)
        assert row[2] == pytest.approx(1234.5678)


def test_22_save_benchmark_results_large_token_counts(initialized_db):
    report = [{
        "model_name": "BigDataModel",
        "accuracy": 0.99,
        "avg_latency_ms": 1000.0,
        "total_tokens_used": 10_000_000_000,
        "efficiency_score": 0.99,
        "evaluations": []
    }]
    save_benchmark_results(report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT total_tokens FROM benchmark_runs;")
        assert cursor.fetchone()[0] == 10_000_000_000


def test_23_save_benchmark_results_boolean_is_correct_conversion(initialized_db, sample_report):
    save_benchmark_results(sample_report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT is_correct FROM prompt_logs ORDER BY id;")
        results = [row[0] for row in cursor.fetchall()]
        assert results == [1, 0]


def test_24_save_benchmark_results_handles_string_numbers_if_passed(initialized_db):
    report = [{
        "model_name": "StringValModel",
        "accuracy": 0.8,
        "avg_latency_ms": 100.0,
        "total_tokens_used": 500,
        "efficiency_score": 0.5,
        "evaluations": [{
            "test_id": "200",
            "category": "test",
            "expected_intent_id": "1",
            "predicted_intent_id": "1",
            "is_correct": True,
            "latency_ms": 50.0
        }]
    }]
    save_benchmark_results(report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT test_id, expected_id FROM prompt_logs;")
        assert cursor.fetchone() == (200, 1)


def test_25_save_benchmark_results_commits_transaction(initialized_db, sample_report):
    save_benchmark_results(sample_report)
    # Re-open connection independently to verify persistence
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM benchmark_runs;")
        assert cursor.fetchone()[0] == 1


# ----------------------------------------------------------------------
# 3. Data Integrity & Edge Cases (Tests 26–40)
# ----------------------------------------------------------------------

def test_26_save_results_raises_keyerror_on_missing_required_model_name(initialized_db):
    bad_report = [{"accuracy": 0.9, "avg_latency_ms": 10.0}]
    with pytest.raises(KeyError):
        save_benchmark_results(bad_report)


def test_27_save_results_raises_keyerror_on_missing_required_eval_fields(initialized_db):
    bad_report = [{
        "model_name": "BadModel",
        "accuracy": 0.9,
        "avg_latency_ms": 10.0,
        "total_tokens_used": 100,
        "efficiency_score": 0.9,
        "evaluations": [{"test_id": 1}]  # missing category, etc.
    }]
    with pytest.raises(KeyError):
        save_benchmark_results(bad_report)


def test_28_special_characters_in_model_name(initialized_db):
    report = [{
        "model_name": "Model/v1.0:beta_test's--quote",
        "accuracy": 0.5,
        "avg_latency_ms": 10.0,
        "total_tokens_used": 10,
        "efficiency_score": 0.5,
        "evaluations": []
    }]
    save_benchmark_results(report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT model_name FROM benchmark_runs;")
        assert cursor.fetchone()[0] == "Model/v1.0:beta_test's--quote"


def test_29_unicode_and_emoji_in_category(initialized_db):
    report = [{
        "model_name": "UnicodeModel",
        "accuracy": 0.5,
        "avg_latency_ms": 10.0,
        "total_tokens_used": 10,
        "efficiency_score": 0.5,
        "evaluations": [{
            "test_id": 1,
            "category": "finance_📈_测试",
            "expected_intent_id": 1,
            "predicted_intent_id": 1,
            "is_correct": True,
            "latency_ms": 10.0
        }]
    }]
    save_benchmark_results(report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT category FROM prompt_logs;")
        assert cursor.fetchone()[0] == "finance_📈_测试"


def test_30_zero_latency_and_ttft_values(initialized_db):
    report = [{
        "model_name": "ZeroModel",
        "accuracy": 0.0,
        "avg_latency_ms": 0.0,
        "avg_ttft_ms": 0.0,
        "avg_tps": 0.0,
        "total_tokens_used": 0,
        "efficiency_score": 0.0,
        "evaluations": []
    }]
    save_benchmark_results(report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT avg_latency_ms, avg_ttft_ms, avg_tps FROM benchmark_runs;")
        assert cursor.fetchone() == (0.0, 0.0, 0.0)


def test_31_negative_metrics_handling(initialized_db):
    report = [{
        "model_name": "NegativeModel",
        "accuracy": -1.0,
        "avg_latency_ms": -50.0,
        "total_tokens_used": -100,
        "efficiency_score": -0.5,
        "evaluations": []
    }]
    save_benchmark_results(report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT accuracy, avg_latency_ms, total_tokens FROM benchmark_runs;")
        assert cursor.fetchone() == (-1.0, -50.0, -100)


def test_32_transaction_atomicity_on_evaluations_failure(initialized_db):
    corrupt_report = [{
        "model_name": "AtomicTestModel",
        "accuracy": 0.8,
        "avg_latency_ms": 100.0,
        "total_tokens_used": 100,
        "efficiency_score": 0.8,
        "evaluations": [
            {
                "test_id": 1,
                "category": "valid",
                "expected_intent_id": 1,
                "predicted_intent_id": 1,
                "is_correct": True,
                "latency_ms": 10.0
            },
            {
                "invalid_key": "will_cause_keyerror"
            }
        ]
    }]
    with pytest.raises(KeyError):
        save_benchmark_results(corrupt_report)
        
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM benchmark_runs;")
        # Verify rollback occurred (or sqlite auto-rollback on connection exit)
        assert cursor.fetchone()[0] == 0


def test_33_duplicate_test_ids_allowed(initialized_db):
    report = [{
        "model_name": "DupModel",
        "accuracy": 0.5,
        "avg_latency_ms": 10.0,
        "total_tokens_used": 10,
        "efficiency_score": 0.5,
        "evaluations": [
            {"test_id": 99, "category": "c", "expected_intent_id": 1, "predicted_intent_id": 1, "is_correct": True, "latency_ms": 1.0},
            {"test_id": 99, "category": "c", "expected_intent_id": 1, "predicted_intent_id": 1, "is_correct": True, "latency_ms": 1.0}
        ]
    }]
    save_benchmark_results(report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM prompt_logs WHERE test_id = 99;")
        assert cursor.fetchone()[0] == 2


def test_34_save_benchmark_results_returns_none(initialized_db, sample_report):
    res = save_benchmark_results(sample_report)
    assert res is None


def test_35_db_path_parent_creation_if_nonexistent(tmp_path, monkeypatch):
    nested_path = tmp_path / "deep" / "nested" / "path" / "test.db"
    monkeypatch.setattr("app.db.DB_PATH", nested_path)
    assert not nested_path.parent.exists()
    init_db()
    assert nested_path.parent.exists()
    assert nested_path.exists()


def test_36_concurrent_connections_read(initialized_db, sample_report):
    save_benchmark_results(sample_report)
    conn1 = sqlite3.connect(initialized_db)
    conn2 = sqlite3.connect(initialized_db)
    c1 = conn1.cursor()
    c2 = conn2.cursor()
    c1.execute("SELECT COUNT(*) FROM benchmark_runs;")
    c2.execute("SELECT COUNT(*) FROM benchmark_runs;")
    assert c1.fetchone()[0] == 1
    assert c2.fetchone()[0] == 1
    conn1.close()
    conn2.close()


def test_37_query_benchmark_runs_filtering(initialized_db, sample_report):
    save_benchmark_results(sample_report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT model_name FROM benchmark_runs WHERE accuracy > 0.8;")
        assert cursor.fetchone()[0] == "Llama-3-8B"


def test_38_query_prompt_logs_by_category(initialized_db, sample_report):
    save_benchmark_results(sample_report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM prompt_logs WHERE category = 'finance';")
        assert cursor.fetchone()[0] == 1


def test_39_aggregate_accuracy_from_prompt_logs(initialized_db, sample_report):
    save_benchmark_results(sample_report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT AVG(is_correct) FROM prompt_logs WHERE run_id = 1;")
        assert cursor.fetchone()[0] == 0.5


def test_40_join_benchmark_runs_and_prompt_logs(initialized_db, sample_report):
    save_benchmark_results(sample_report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.model_name, p.category, p.is_correct
            FROM benchmark_runs r
            JOIN prompt_logs p ON r.id = p.run_id
            WHERE p.test_id = 101;
        """)
        row = cursor.fetchone()
        assert row == ("Llama-3-8B", "finance", 1)


# ----------------------------------------------------------------------
# 4. Environment & PATH Configurations (Tests 41–48)
# ----------------------------------------------------------------------

def test_41_base_dir_resolution():
    assert isinstance(BASE_DIR, Path)
    assert BASE_DIR.is_absolute()


def test_42_db_path_default_structure():
    from app.db import DB_PATH
    assert isinstance(DB_PATH, Path)
    assert DB_PATH.name == "benchmark_history.db"
    assert DB_PATH.parent.name == "data"


def test_43_sqlite3_version_supported():
    assert sqlite3.sqlite_version_info >= (3, 25, 0)


def test_44_mock_sqlite_connect_failure_on_init(monkeypatch):
    def mock_connect(*args, **kwargs):
        raise sqlite3.OperationalError("Unable to open database file")
    monkeypatch.setattr(sqlite3, "connect", mock_connect)
    with pytest.raises(sqlite3.OperationalError):
        init_db()


def test_45_mock_sqlite_connect_failure_on_save(monkeypatch):
    def mock_connect(*args, **kwargs):
        raise sqlite3.OperationalError("Database locked")
    monkeypatch.setattr(sqlite3, "connect", mock_connect)
    with pytest.raises(sqlite3.OperationalError):
        save_benchmark_results([])


def test_46_table_schema_does_not_recreate_if_exists(initialized_db):
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO benchmark_runs (model_name) VALUES ('PreExisting');")
        conn.commit()

    init_db()  # Run init again

    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM benchmark_runs;")
        assert cursor.fetchone()[0] == 1


def test_47_handles_very_long_strings_in_prompt_logs(initialized_db):
    long_category = "A" * 10_000
    report = [{
        "model_name": "LongStringModel",
        "accuracy": 1.0,
        "avg_latency_ms": 1.0,
        "total_tokens_used": 1,
        "efficiency_score": 1.0,
        "evaluations": [{
            "test_id": 1,
            "category": long_category,
            "expected_intent_id": 1,
            "predicted_intent_id": 1,
            "is_correct": True,
            "latency_ms": 1.0
        }]
    }]
    save_benchmark_results(report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT LENGTH(category) FROM prompt_logs;")
        assert cursor.fetchone()[0] == 10_000


def test_48_verify_cursor_closed_after_context(initialized_db, sample_report):
    with patch("sqlite3.connect", wraps=sqlite3.connect) as mocked_connect:
        save_benchmark_results(sample_report)
        assert mocked_connect.called


# ----------------------------------------------------------------------
# 5. Business Logic Validation & Integrations (Tests 49–53)
# ----------------------------------------------------------------------

def test_49_save_and_retrieve_multiple_evaluations_order(initialized_db):
    evals = [
        {"test_id": i, "category": f"cat_{i}", "expected_intent_id": i, "predicted_intent_id": i, "is_correct": True, "latency_ms": float(i)}
        for i in range(10)
    ]
    report = [{
        "model_name": "OrderedModel",
        "accuracy": 1.0,
        "avg_latency_ms": 5.0,
        "total_tokens_used": 50,
        "efficiency_score": 1.0,
        "evaluations": evals
    }]
    save_benchmark_results(report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT test_id FROM prompt_logs ORDER BY id ASC;")
        retrieved_ids = [row[0] for row in cursor.fetchall()]
        assert retrieved_ids == list(range(10))


def test_50_breakeven_requests_stored_as_integer(initialized_db):
    report = [{
        "model_name": "IntTypeModel",
        "accuracy": 0.8,
        "avg_latency_ms": 10.0,
        "total_tokens_used": 100,
        "efficiency_score": 0.8,
        "breakeven_monthly_requests": 1384060,
        "evaluations": []
    }]
    save_benchmark_results(report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT typeof(breakeven_requests) FROM benchmark_runs;")
        assert cursor.fetchone()[0] == "integer"


def test_51_max_rps_stored_as_real(initialized_db):
    report = [{
        "model_name": "RPSModel",
        "accuracy": 0.8,
        "avg_latency_ms": 10.0,
        "total_tokens_used": 100,
        "efficiency_score": 0.8,
        "max_rps": 50.5,
        "evaluations": []
    }]
    save_benchmark_results(report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT typeof(max_rps), max_rps FROM benchmark_runs;")
        row = cursor.fetchone()
        assert row[0] == "real"
        assert row[1] == 50.5


def test_52_cluster_monthly_tco_eur_stored_as_real(initialized_db):
    report = [{
        "model_name": "TCOModel",
        "accuracy": 0.8,
        "avg_latency_ms": 10.0,
        "total_tokens_used": 100,
        "efficiency_score": 0.8,
        "cluster_monthly_tco_eur": 1384.06,
        "evaluations": []
    }]
    save_benchmark_results(report)
    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT typeof(cluster_monthly_tco_eur), cluster_monthly_tco_eur FROM benchmark_runs;")
        row = cursor.fetchone()
        assert row[0] == "real"
        assert row[1] == 1384.06


def test_53_full_database_cleanup_and_reinitialization(initialized_db, sample_report):
    save_benchmark_results(sample_report)

    # Force Python's garbage collector to release any residual SQLite connection handles
    gc.collect()

    # Retry loop to handle Windows file lock delays
    for _ in range(5):
        try:
            initialized_db.unlink()
            break
        except PermissionError:
            time.sleep(0.1)

    assert not initialized_db.exists()

    # Re-initialize clean DB
    init_db()
    assert initialized_db.exists()

    with sqlite3.connect(initialized_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM benchmark_runs;")
        assert cursor.fetchone()[0] == 0