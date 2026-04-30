import sqlite3

import pytest

from spiderlens.execution.sqlite_runner import UnsafeSQLStatement, execute_select


def test_execute_select_reads_rows(tmp_path) -> None:
    database = tmp_path / "fixture.sqlite"
    with sqlite3.connect(database) as connection:
        connection.execute("CREATE TABLE people (name TEXT, age INTEGER)")
        connection.execute("INSERT INTO people VALUES ('Ada', 36)")

    result = execute_select(database, "SELECT name, age FROM people")

    assert result.columns == ["name", "age"]
    assert result.rows == [["Ada", 36]]


def test_execute_select_rejects_mutation(tmp_path) -> None:
    database = tmp_path / "fixture.sqlite"
    with sqlite3.connect(database) as connection:
        connection.execute("CREATE TABLE people (name TEXT)")

    with pytest.raises(UnsafeSQLStatement):
        execute_select(database, "DROP TABLE people")
