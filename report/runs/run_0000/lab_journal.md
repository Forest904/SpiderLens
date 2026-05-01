# Lab Journal: run_0000

Date: 2026-04-30

Goal: preserve the first SpiderLens smoke-test reporting artifacts as the historical baseline before run-scoped reporting was added.

Run ID / command:

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe scripts\run_text_to_sql.py
.\.venv\Scripts\python.exe scripts\run_table_qa.py
.\.venv\Scripts\python.exe scripts\evaluate.py --predictions data\outputs\text_to_sql.jsonl data\outputs\table_qa.jsonl
.\.venv\Scripts\python.exe scripts\make_report_assets.py
```

Generated metrics:

| pipeline | cell_precision | cell_recall | tuple_cardinality |
| --- | ---: | ---: | ---: |
| table_qa | 0.6746 | 1.0 | 0.7222 |
| text_to_sql | 1.0 | 1.0 | 1.0 |

Report artifacts:

- `report/runs/run_0000/report.md`
- `report/runs/run_0000/summary_metrics.md`
- `report/runs/run_0000/per_example_metrics.md`
- `report/runs/run_0000/failure_breakdown.md`
- `report/runs/run_0000/metric_summary.png`

Failures or surprises:

- Direct Table QA initially needed parser support for JSON objects with a `rows` field.
- Direct Table QA over-returned the full `singer` table for one count question.

Interpretation:

- This run proves the original scaffold could load Spider data, run both pipelines, evaluate outputs, and generate first-pass report assets.
- It is intentionally preserved as `run_0000` because it predates the stable M1 run ID system.
