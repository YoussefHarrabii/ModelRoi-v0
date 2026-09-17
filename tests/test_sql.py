"""Tests for the SQL scorer (app/tasks/sql.py) against an isolated in-memory DB."""
import sqlite3
import pytest
from unittest.mock import patch
from app.tasks import sql as sql_task


@pytest.fixture
def memdb(monkeypatch):
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.execute("CREATE TABLE students (student_id INTEGER PRIMARY KEY, first_name TEXT, gpa REAL)")
    cur.execute("INSERT INTO students VALUES (1, 'Ann', 3.5), (2, 'Bob', 2.0)")
    con.commit()

    def fake_conn():
        # fresh read-only-style connection per call over shared cache
        return con

    monkeypatch.setattr(sql_task, "get_test_connection", lambda: con)
    yield con
    con.close()


def test_exact_match_passes(memdb):
    out = sql_task.score(
        {"response": "SELECT first_name FROM students WHERE gpa > 3.0;"},
        {"sql": "SELECT first_name FROM students WHERE gpa > 3.0;"},
    )
    assert out["score"] == 1.0 and out["is_correct"] is True and out["error"] is None


def test_different_rows_fail(memdb):
    out = sql_task.score(
        {"response": "SELECT first_name FROM students WHERE gpa < 3.0;"},
        {"sql": "SELECT first_name FROM students WHERE gpa > 3.0;"},
    )
    assert out["score"] == 0.0 and out["is_correct"] is False


def test_projection_strictness_documented(memdb):
    # Same rows, different projection -> fail by design (questions must pin columns)
    out = sql_task.score(
        {"response": "SELECT * FROM students WHERE gpa > 3.0;"},
        {"sql": "SELECT first_name FROM students WHERE gpa > 3.0;"},
    )
    assert out["is_correct"] is False


def test_execution_error_fails_without_raising(memdb):
    out = sql_task.score(
        {"response": "SELECT nope FROM nowhere;"},
        {"sql": "SELECT first_name FROM students;"},
    )
    assert out["is_correct"] is False
    assert out["error"] is not None


def test_empty_predicted_fails(memdb):
    out = sql_task.score({"response": "   "}, {"sql": "SELECT 1;"})
    assert out["is_correct"] is False
    assert out["error"] == "Empty SQL statement"


def test_markdown_fences_and_semicolon_stripped(memdb):
    out = sql_task.score(
        {"response": "```sql\nSELECT first_name FROM students WHERE gpa > 3.0;\n```"},
        {"sql": "SELECT first_name FROM students WHERE gpa > 3.0"},
    )
    assert out["is_correct"] is True
    assert out["predicted_sql"] == "SELECT first_name FROM students WHERE gpa > 3.0"


def test_build_prompt_contract():
    system, user = sql_task.build_prompt({"question": "List all students."})
    assert "ONLY the raw SQL query" in system
    assert "List all students." in user
    assert "SQL Query:" in user
