from __future__ import annotations

from collections import Counter

from spiderlens.evaluation.normalize import cells


def safe_divide(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def cell_precision(predicted: list[tuple[str, ...]], expected: list[tuple[str, ...]]) -> float:
    predicted_cells = Counter(cells(predicted))
    expected_cells = Counter(cells(expected))
    overlap = sum((predicted_cells & expected_cells).values())
    return safe_divide(overlap, sum(predicted_cells.values()))


def cell_recall(predicted: list[tuple[str, ...]], expected: list[tuple[str, ...]]) -> float:
    predicted_cells = Counter(cells(predicted))
    expected_cells = Counter(cells(expected))
    overlap = sum((predicted_cells & expected_cells).values())
    return safe_divide(overlap, sum(expected_cells.values()))


def tuple_cardinality(predicted: list[tuple[str, ...]], expected: list[tuple[str, ...]]) -> float:
    if not expected and not predicted:
        return 1.0
    return 1.0 - safe_divide(abs(len(predicted) - len(expected)), max(len(predicted), len(expected)))


def compute_metrics(predicted: list[tuple[str, ...]], expected: list[tuple[str, ...]]) -> dict[str, float]:
    return {
        "cell_precision": cell_precision(predicted, expected),
        "cell_recall": cell_recall(predicted, expected),
        "tuple_cardinality": tuple_cardinality(predicted, expected),
    }
