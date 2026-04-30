from spiderlens.evaluation.metrics import cell_precision, cell_recall, tuple_cardinality


def test_cell_metrics_count_multiset_overlap() -> None:
    predicted = [("a", "b"), ("b",)]
    expected = [("a", "b"), ("c",)]

    assert cell_precision(predicted, expected) == 2 / 3
    assert cell_recall(predicted, expected) == 2 / 3


def test_tuple_cardinality_rewards_matching_row_count() -> None:
    assert tuple_cardinality([("a",), ("b",)], [("x",), ("y",)]) == 1.0
    assert tuple_cardinality([("a",)], [("x",), ("y",)]) == 0.5
