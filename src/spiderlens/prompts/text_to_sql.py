from __future__ import annotations


def build_text_to_sql_prompt(question: str, schema: str, oracle_tables: list[str]) -> str:
    tables = ", ".join(oracle_tables) if oracle_tables else "not provided"
    return f"""You translate natural-language questions into SQLite SQL.

Return only one SQL query. Do not include prose.

Relevant tables: {tables}

Schema:
{schema}

Question:
{question}
"""
