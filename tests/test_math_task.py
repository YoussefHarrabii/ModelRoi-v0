"""Regression tests for the hardened math scorer (app/tasks/math_task.py)."""
import random
import pytest
import app.tasks.math_task as mt
from app.tasks.math_task import are_equivalent as eq


def test_clean_text_normalizes():
    assert mt.clean_text("  Yes ") == "yes"
    assert mt.clean_text("$2.00") == "2"


def test_extract_final_strips_prefixes():
    assert mt.extract_final("f'(x) = 5") == "5"
    assert mt.extract_final("d/dx [arctan(2x)] = 2/(1+4x^2)") == "2/(1+4x^2)"
    assert mt.extract_final("3x = 15\nx = 5") == "5"
    assert mt.extract_final("Answer: 42") == "42"


def test_extract_final_preserves_answer_lists():
    assert mt.extract_final("x = -2, x = 2") == "x = -2, x = 2"
    assert mt.extract_final("= [[8, -2], [9, -1]]") == "[[8, -2], [9, -1]]"


def test_trig_power_notation():
    assert eq("2*sec(2*x)^2", "2*sec^2(2x)")
    assert eq("2*sec(2*x)^2", "sec^2(2x)*2")


def test_arcsec_and_euler_mapping():
    assert eq("arcsec(x) + C", "asec(x)+C")
    assert eq("3*e^x", "3*E^x")


def test_numeric_tolerance_1e6():
    assert eq("1/6", "0.166667")
    assert eq("2/3", "0.6666667")
    assert not eq("1/6", "0.17")


def test_root_sets_order_insensitive_with_prefixes():
    assert eq("-2, 2", "x = -2, x = 2")
    assert eq("3, 5", "3,5")
    assert not eq("3, 5", "3, 6")


def test_semicolon_systems_order_insensitive():
    assert eq("3, 4; 4, 3", "4, 3; 3, 4")
    assert not eq("3, 4; 4, 3", "3, 4; 5, 5")


def test_matrices_order_sensitive():
    assert eq("[[1, 3], [2, 4]]", "[[1, 3], [2, 4]]")
    assert not eq("[[1, 3], [2, 4]]", "[[2, 1], [4, 3]]")  # transpose must fail
    assert not eq("[[-1, 0], [0, 1]]", "[[1,0],[0,-1]]")  # reflection must fail


def test_matrices_fraction_decimal_and_delimiters():
    assert eq("[[0.5, 0], [0, 0.2]]", "[[1/2, 0], [0, 1/5]]")
    assert eq("[1; 2; 3]", "[1, 2, 3]")
    assert eq("[3.5, 3.5]", "[7/2, 7/2]")


def test_constant_rule_for_integrals():
    assert eq("x^2/2 + C", "x^2/2 + C")
    assert not eq("x^2/2 + C", "x^2/2")  # missing +C fails per prompt
    assert eq("sin(x)^2/2 + C", "-cos(x)^2/2 + C")  # differ by constant only


def test_genuinely_wrong_stays_wrong():
    assert not eq("-e^(1/x)/x^2", "e^(-1/x^2)*(-1/x^2)")
    assert not eq("2/x", "2/log(10)*1/x")


def test_random_probe_stable_on_sqrt_domain():
    random.seed(0)
    e = "x*sqrt(x^2 - 1)/2 - log(abs(x + sqrt(x^2 - 1)))/2 + C"
    p = "(1/2) * (x * sqrt(x^2 - 1) - ln(x + sqrt(x^2 - 1))) + C"
    assert all(eq(e, p) for _ in range(5))


def test_simplify_guard_bounds_pathological_input(monkeypatch):
    monkeypatch.setattr(mt, "SIMPLIFY_TIMEOUT", 0.2)
    nasty = "sin(" * 30 + "x" + ")" * 30
    assert eq("x^2/2 + C", nasty) is False


def test_score_contract():
    out = mt.score({"response": "5"}, {"answer": "5", "category": 3})
    assert out == {
        "score": 1.0, "is_correct": True, "expected_answer": "5",
        "predicted_answer": "5", "math_category": 3,
    }
    out = mt.score({"response": "6"}, {"answer": "5", "category": 3})
    assert out["score"] == 0.0 and out["is_correct"] is False
