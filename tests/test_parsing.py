from spiderlens.parsing.answer_output import parse_answer_rows
from spiderlens.parsing.sql_output import extract_sql


def test_extract_sql_from_fence() -> None:
    assert extract_sql("```sql\nSELECT * FROM people\n```") == "SELECT * FROM people;"


def test_parse_answer_rows_from_json_fence() -> None:
    assert parse_answer_rows("```json\n[[\"Ada\", 36]]\n```") == [["Ada", 36]]


def test_parse_answer_rows_accepts_rows_object() -> None:
    assert parse_answer_rows('{"rows": [[6]]}') == [[6]]
