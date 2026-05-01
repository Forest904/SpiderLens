# SpiderLens Lab Journal

This journal keeps the chronological trace of the project: runs, mistakes, fixes, metrics, and interpretation. The point is not to look perfectly linear. The point is to make the work inspectable and human.

## Entry Template

```text
Date:
Goal:
Run ID / command:
Changed files:
Generated metrics:
Report artifacts:
Failures or surprises:
Interpretation:
Next action:
```

## 2026-04-30 - First Data Wiring Smoke Test

Goal: prove that SpiderLens can load Spider data, run both pipelines, evaluate outputs, and generate report assets.

Run ID / command:

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe scripts\run_text_to_sql.py
.\.venv\Scripts\python.exe scripts\run_table_qa.py
.\.venv\Scripts\python.exe scripts\evaluate.py --predictions data\outputs\text_to_sql.jsonl data\outputs\table_qa.jsonl
.\.venv\Scripts\python.exe scripts\make_report_assets.py
```

Changed files:

- `data/subset/manifest.json`
- `src/spiderlens/parsing/answer_output.py`
- `tests/test_parsing.py`
- `report/report.md`

Generated metrics:

| pipeline | cell_precision | cell_recall | tuple_cardinality |
| --- | ---: | ---: | ---: |
| table_qa | 0.6746 | 1.0 | 0.7222 |
| text_to_sql | 1.0 | 1.0 | 1.0 |

Report artifacts:

- `report/report.md`
- `report/tables/summary_metrics.md`
- `report/tables/per_example_metrics.md`
- `report/tables/failure_breakdown.md`
- `report/figures/metric_summary.png`

Failures or surprises:

- Direct Table QA initially returned JSON objects with a `rows` field, while the parser accepted only bare JSON lists.
- After parser support was added, Direct Table QA still over-returned the full `singer` table for one count question.

Interpretation:

- The data wiring is successful: Spider dev files, SQLite databases, API calls, JSONL outputs, evaluation, and report generation all work.
- Text-to-SQL is strong on this tiny easy subset.
- Direct Table QA needs stricter prompting or validation for aggregate/count questions, because parseable output can still be semantically too broad.

Next action:

- Strengthen reporting so future runs have stable run IDs, metric deltas, failure labels, and reproducible run summaries.

## 2026-05-01 - M1 Run-Scoped Reporting Pipeline

Goal: make experiment reporting reproducible, traceable, and grouped by stable run ID.

Run ID / command:

```powershell
.\.venv\Scripts\python.exe scripts\run_experiment.py --manifest data\subset\manifest.json --run-id run_0001
```

Changed files:

- `scripts/run_experiment.py`
- `scripts/make_report_assets.py`
- `scripts/evaluate.py`
- `scripts/run_text_to_sql.py`
- `scripts/run_table_qa.py`
- `src/spiderlens/reporting/`
- `src/spiderlens/evaluation/compare.py`
- `src/spiderlens/dataset/subset.py`
- `tests/test_reporting.py`

Generated metrics:

| pipeline | cell_precision | cell_recall | tuple_cardinality |
| --- | ---: | ---: | ---: |
| table_qa | 0.6746 | 1.0 | 0.7222 |
| text_to_sql | 1.0 | 1.0 | 1.0 |

Report artifacts:

- `report/runs/run_0001/summary.md`
- `report/runs/run_0001/per_example_metrics.md`
- `report/runs/run_0001/failure_breakdown.md`
- `report/runs/run_0001/metric_deltas.md`
- `report/runs/run_0001/metric_summary.png`
- `report/runs/run_0001/lab_journal.md`
- `data/outputs/runs/run_0001/metrics.jsonl`

Failures or surprises:

- No failed examples in this smoke run.
- `query_pattern` reports as `unknown` because the current M0 manifest does not yet annotate patterns.
- Metric deltas intentionally report that no baseline was provided.

Interpretation:

- M1 now has a run-scoped path for predictions, metrics, Markdown summaries, timestamped report snapshots, plots, metadata, and a per-run journal.
- Failed examples will remain visible in per-example metrics and failure breakdowns because evaluation attaches `failure_label` and scores non-`ok` predictions as empty outputs.

Next action:

- Use `run_0001` as the reporting baseline before prompt, parser, or subset changes.
