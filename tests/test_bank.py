"""Bank-level regression guards: uniqueness, structure, and DB consistency."""
import re
import sqlite3
import pytest
from pathlib import Path
from data.mathtests import MATH_TESTS
from data.sqltests import SQL_TESTS

SEEDED_DB = Path(__file__).resolve().parent.parent / "app" / "data" / "test_data.db"
needs_seed_db = pytest.mark.skipif(
    not SEEDED_DB.exists(), reason="seeded test_data.db not present"
)


# ---------------------------------------------------------------- math bank
def test_math_bank_unique_questions():
    questions = [t["question"] for t in MATH_TESTS]
    assert len(questions) == len(set(questions))


def test_math_bank_schema_and_categories():
    assert {t["category"] for t in MATH_TESTS} == {1, 2, 3, 4, 5, 6, 7}
    for t in MATH_TESTS:
        assert t["question"] and t["answer"] and t["answer"].strip()


def test_math_bank_balanced_parens_in_answers():
    for t in MATH_TESTS:
        a = t["answer"]
        assert a.count("(") == a.count(")"), t["question"][:60]
        assert a.count("[") == a.count("]"), t["question"][:60]


def test_math_bank_no_prompt_violating_answers():
    for t in MATH_TESTS:
        a = t["answer"]
        assert "$" not in a, t["question"][:60]
        assert not re.search(r"\b(AM|PM)\b", a), t["question"][:60]
        assert not re.search(r"\b(profit|decrease|increase)\b", a, re.I), t["question"][:60]


def test_math_bank_regression_pinned_fixes():
    by_q = {t["question"]: t["answer"] for t in MATH_TESTS}
    assert by_q["A worker earns $15 per hour for the first 40 hours, and $22.50 per hour for overtime. If they work 45 hours, how much do they earn?"] == "712.5"
    assert by_q["If the expected value of playing a game once is -$0.50, what is the expected net gain or loss after playing 10 times? Use a negative value for a loss."] == "-5"
    assert by_q["Find the indefinite integral of \u222b 1/(x * (1 + x^4)) dx."] == "log(abs(x^4/(1 + x^4)))/4 + C"


# ---------------------------------------------------------------- sql bank
def test_sql_bank_unique_questions():
    questions = [t["question"] for t in SQL_TESTS]
    assert len(questions) == len(set(questions))


def test_sql_bank_schema():
    for t in SQL_TESTS:
        assert t["question"] and t["sql"] and t["sql"].strip().endswith(";")


def test_sql_bank_columns_pinned():
    unpinned = [
        t["question"] for t in SQL_TESTS
        if "Return " not in t["question"]
    ]
    assert len(unpinned) <= 5, [q[:70] for q in unpinned]


@needs_seed_db
def test_sql_bank_all_expected_execute():
    con = sqlite3.connect(f"file:{SEEDED_DB}?mode=ro", uri=True)
    errors = []
    for t in SQL_TESTS:
        try:
            con.execute(t["sql"].strip().rstrip(";")).fetchall()
        except Exception as e:
            errors.append((t["question"][:60], str(e)[:60]))
    con.close()
    assert errors == []


@needs_seed_db
def test_sql_bank_no_empty_expected():
    con = sqlite3.connect(f"file:{SEEDED_DB}?mode=ro", uri=True)
    empties = []
    for t in SQL_TESTS:
        rows = con.execute(t["sql"].strip().rstrip(";")).fetchall()
        if len(rows) == 0:
            empties.append(t["question"][:60])
    con.close()
    assert empties == []
