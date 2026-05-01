# Lab Journal: run_0001

Date: 2026-05-01
Goal: Strengthen the reporting pipeline with reproducible run-scoped artifacts.
Run ID / command:

```powershell
.\.venv\Scripts\python.exe scripts\run_experiment.py --manifest data\subset\manifest.json --run-id run_0001 --baseline-metrics data\outputs\runs\run_0000\metrics.jsonl
```

Generated metrics:

| pipeline | records | cell_precision | cell_recall | tuple_cardinality |
| --- | --- | --- | --- | --- |
| table_qa | 3 | 0.6746 | 1.0 | 0.7222 |
| text_to_sql | 3 | 1.0 | 1.0 | 1.0 |

Report artifacts:

- [summary](summary.md)
- [per-example metrics](per_example_metrics.md)
- [failure breakdown](failure_breakdown.md)
- [metric deltas](metric_deltas.md)
- [metric plot](metric_summary.png)
- [run journal](lab_journal.md)
- [metadata](metadata.json)

Failures or surprises:
- Failed metric records: 0

Interpretation:
- This run preserves metadata, metrics, failures, deltas, and report links in one run folder.

Next action:
- Use these run folders as the baseline trace before prompt and parser iteration.
