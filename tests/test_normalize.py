from spiderlens.evaluation.normalize import normalize_rows


def test_normalize_rows_lowercases_sorts_and_stringifies() -> None:
    rows = [[" Bob ", 2.0], ["alice", None]]

    assert normalize_rows(rows) == [("alice", ""), ("bob", "2")]
