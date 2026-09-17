"""
Task handler for the extraction task (paragraph index selection).
Uses the same prompt format as your original benchmark.
"""


def build_prompt(case: dict) -> tuple[str, str]:
    """
    Build the system and user prompts for extraction.
    Returns (system_prompt, user_prompt).
    """
    system_prompt = """You are a text comprehension and information retrieval assistant.

Your task is to identify which paragraphs are most relevant to answering a given query.

You will receive:
- A QUERY (a specific question)
- A set of 10 numbered PARAGRAPHS (labeled [0] through [9])

Your job is to return the indices of the paragraphs that directly help answer the query.

IMPORTANT RULES:
1. Only include indices that are clearly relevant to answering the query.
2. Each index must be an integer between 0 and 9.
3. Return between 1 and 3 indices.
4. Output strictly as valid JSON: {"indices": [0, 2, 5]}

Example:
QUERY: What is the primary mechanism of antibiotic resistance?
PARAGRAPHS:
[0] Antibiotic resistance occurs when bacteria evolve...
[1] One primary mechanism involves the production of enzymes...
[2] Efflux pumps transport antibiotics out of the cell...
...
Output: {"indices": [1]}

Respond with valid JSON only. No explanation, no markdown."""

    paragraphs = case.get("paragraphs", [])
    paragraphs_text = "\n".join([f"[{i}] {p}" for i, p in enumerate(paragraphs)])
    user_prompt = f"QUERY: {case['query']}\n\nPARAGRAPHS:\n{paragraphs_text}"

    return system_prompt, user_prompt


def score(raw: dict, case: dict) -> dict:
    """
    Score the extraction result.
    raw: output from call_ollama (contains "response" field)
    case: the test case (contains "expected_indices")
    Returns dict with "score", "is_correct", and task‑specific fields.
    """
    import json
    import logging

    logger = logging.getLogger(__name__)

    expected = case.get("expected_indices", [])
    predicted = []

    try:
        raw_output = raw.get("response", "").strip()
        parsed = json.loads(raw_output)
        raw_indices = parsed.get("indices")
        if isinstance(raw_indices, list):
            predicted = [int(i) for i in raw_indices if isinstance(i, int) and 0 <= i <= 9]
    except Exception as e:
        logger.warning(f"Failed to parse extraction output: {raw_output} | Error: {e}")

    from app.scorers import calculate_retrieval_metrics

    metrics = calculate_retrieval_metrics(expected, predicted)

    return {
        "score": metrics["f1"],          # 0-1
        "is_correct": set(expected) == set(predicted),
        "expected_indices": expected,
        "predicted_indices": predicted,
        "precision": metrics["precision"],
        "recall": metrics["recall"],
        "f1": metrics["f1"],
    }