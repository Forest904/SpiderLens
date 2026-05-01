# SpiderLens First Project Report

Date: 2026-04-30

## 1. Project Purpose

SpiderLens is a small Python evaluation framework for comparing two LLM-based approaches to question answering over relational data:

- **Text-to-SQL**: the model writes SQL, SpiderLens executes it on SQLite, then evaluates the returned data.
- **Direct Table QA**: the model receives serialized table rows and directly returns answer rows, which are parsed and evaluated with the same data-centric metrics.

The goal is not to declare one method universally better. The goal is to expose strengths, weaknesses, and failure modes under a controlled setup.

## 2. Scaffold And Tech Stack

The initial project scaffold is now in place.

- **Runtime**: Python 3.11 in a local `.venv`.
- **Dependency workflow**: standard `venv` plus `pip install -r requirements.txt`.
- **LLM integration**: OpenAI-compatible API client with disk caching by prompt/model configuration.
- **Database execution**: Python `sqlite3`, restricted to read-only `SELECT`/`WITH` queries.
- **Artifacts**: JSONL records for predictions, metrics, errors, prompts, and cached model outputs.
- **Evaluation**: normalized row/cell comparison with cell precision, cell recall, and tuple cardinality.
- **Reporting**: Markdown tables and a generated metric plot.
- **Quality checks**: `pytest` and `ruff`.

The source package is organized under `src/spiderlens/`, with separate modules for dataset loading, prompt construction, execution, parsing, evaluation, analysis, reporting, and pipelines.

## 3. Dataset Wiring

Spider 1.0 was uploaded under:

```text
data/spider/
```

The project successfully verified the expected development-data layout:

```text
data/spider/dev.json
data/spider/tables.json
data/spider/database/concert_singer/concert_singer.sqlite
```

Local test-only Spider files were removed because this project currently evaluates a curated development subset:

- `data/spider/test.json`
- `data/spider/test_gold.sql`
- `data/spider/test_tables.json`
- `data/spider/test_database/`
- `data/spider/.DS_Store`

The first curated subset is stored in:

```text
data/subset/manifest.json
```

It contains three `concert_singer` examples from Spider dev, all using the oracle table:

```text
singer
```

## 4. First Engine Run

The first live smoke test ran both pipelines on three examples.

Commands used:

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe scripts\run_text_to_sql.py
.\.venv\Scripts\python.exe scripts\run_table_qa.py
.\.venv\Scripts\python.exe scripts\evaluate.py --predictions data\outputs\text_to_sql.jsonl data\outputs\table_qa.jsonl
.\.venv\Scripts\python.exe scripts\make_report_assets.py
```

Pre-run checks passed:

- `pytest`: 9 tests passed.
- `ruff`: all checks passed.

Generated artifacts:

```text
data/outputs/text_to_sql.jsonl
data/outputs/table_qa.jsonl
data/outputs/metrics.jsonl
report/tables/per_example_metrics.md
report/tables/summary_metrics.md
report/tables/failure_breakdown.md
report/figures/metric_summary.png
```

Record counts:

- Text-to-SQL predictions: 3 records, all `ok`.
- Direct Table QA predictions: 3 records, all `ok`.
- Evaluation metrics: 6 records, all `ok`.

## 5. First Results

Summary metrics:

| pipeline | cell_precision | cell_recall | tuple_cardinality |
| --- | ---: | ---: | ---: |
| table_qa | 0.6746 | 1.0 | 0.7222 |
| text_to_sql | 1.0 | 1.0 | 1.0 |

Per-example result:

| pipeline | example_id | status | cell_precision | cell_recall | tuple_cardinality |
| --- | --- | --- | ---: | ---: | ---: |
| text_to_sql | dev-0001 | ok | 1.0 | 1.0 | 1.0 |
| text_to_sql | dev-0002 | ok | 1.0 | 1.0 | 1.0 |
| text_to_sql | dev-0003 | ok | 1.0 | 1.0 | 1.0 |
| table_qa | dev-0001 | ok | 0.0238 | 1.0 | 0.1667 |
| table_qa | dev-0002 | ok | 1.0 | 1.0 | 1.0 |
| table_qa | dev-0003 | ok | 1.0 | 1.0 | 1.0 |

The first data wiring is successful: Spider files load, schemas and table rows are available, the API client runs, both pipelines write JSONL artifacts, SQLite gold execution works, evaluation runs, and report assets are generated.

## 6. Observations And Limitations

The Text-to-SQL pipeline produced perfect results on this very small smoke test.

The Direct Table QA pipeline successfully returned parseable rows for all three examples after the parser was updated to accept both a bare JSON list and a `{"rows": ...}` object. However, on `dev-0001`, the model over-returned the full singer table for a count question. This caused perfect recall but very low precision and cardinality.

This is a useful early finding: Direct Table QA may need stronger answer-format instructions, examples, or stricter parsing/validation to discourage copying table content when the expected answer is an aggregate.

The current result should be treated as a wiring milestone, not as an experimental conclusion. The subset is intentionally tiny and uses a single database/table.
