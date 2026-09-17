"""
Shared scoring functions used across all tasks.
"""
from typing import List


def calculate_retrieval_metrics(expected: List[int], predicted: List[int]) -> dict:
    """Calculate Precision, Recall, F1 for a set of indices (used for extraction)."""
    if not expected and not predicted:
        return {"precision": 1.0, "recall": 1.0, "f1": 1.0}
    if not predicted or not expected:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}

    expected_set = set(expected)
    predicted_set = set(predicted)

    true_positives = len(expected_set & predicted_set)
    precision = true_positives / len(predicted_set) if len(predicted_set) > 0 else 0.0
    recall = true_positives / len(expected_set) if len(expected_set) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
    }