"""Tests for extraction handler + shared scorers (previously untested)."""
from app.tasks import extraction
from app.scorers import calculate_retrieval_metrics


def test_extraction_build_prompt_shape():
    case = {"query": "What?", "paragraphs": ["aaa", "bbb"]}
    system, user = extraction.build_prompt(case)
    assert "valid JSON" in system
    assert "QUERY: What?" in user
    assert "[0] aaa" in user and "[1] bbb" in user


def test_extraction_score_exact():
    raw = {"response": '{"indices": [1]}'}
    case = {"expected_indices": [1]}
    out = extraction.score(raw, case)
    assert out["is_correct"] is True
    assert out["f1"] == 1.0
    assert out["predicted_indices"] == [1]


def test_extraction_score_filters_out_of_range_and_types():
    raw = {"response": '{"indices": [1, 99, "x", -2]}'}
    case = {"expected_indices": [1]}
    out = extraction.score(raw, case)
    assert out["predicted_indices"] == [1]
    assert out["is_correct"] is True


def test_extraction_score_invalid_json_is_incorrect():
    out = extraction.score({"response": "nope"}, {"expected_indices": [1]})
    assert out["is_correct"] is False
    assert out["score"] == 0.0


def test_extraction_partial_credit_f1():
    out = extraction.score({"response": '{"indices": [1]}'}, {"expected_indices": [1, 2]})
    assert out["is_correct"] is False
    assert 0.0 < out["f1"] < 1.0


def test_retrieval_metrics_empty_both():
    assert calculate_retrieval_metrics([], []) == {"precision": 1.0, "recall": 1.0, "f1": 1.0}


def test_retrieval_metrics_empty_predicted():
    assert calculate_retrieval_metrics([1], [])["f1"] == 0.0


def test_retrieval_metrics_partial():
    m = calculate_retrieval_metrics([1, 2], [1, 3])
    assert m["precision"] == 0.5 and m["recall"] == 0.5 and m["f1"] == 0.5
