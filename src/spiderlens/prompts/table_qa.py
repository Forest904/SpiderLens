from __future__ import annotations


def build_table_qa_prompt(question: str, serialized_tables: str) -> str:
    return f"""Answer the question using only the table data below.

Return the answer as JSON: a list of rows, where each row is a list of cell values.
Do not include prose or Markdown fences.

Tables:
{serialized_tables}

Question:
{question}
"""
