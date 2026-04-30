# SpiderLens Milestones

This roadmap tracks the full assignment scope for SpiderLens: implement and evaluate Text-to-SQL and Direct Table QA over a curated Spider subset, preserve the evidence from trial and error, and turn the work into a clear final technical report.

The assignment is graded across implementation, metrics, reproducibility, error analysis, and presentation. These milestones keep those goals visible while the project grows.

## Project Goals

- Compare **Text-to-SQL** and **Direct Table QA** on output data, not only on generated text.
- Use oracle relevant tables so the comparison focuses on reasoning and answer generation rather than table retrieval.
- Build a small curated Spider subset with at least 10 questions across at least 2 databases.
- Cover query patterns including projection, simple selection, multi-condition selection, aggregation, grouping, and ordering.
- Score both pipelines with cell precision, cell recall, and tuple cardinality.
- Treat invalid SQL, execution errors, unparsable outputs, and empty outputs as failed attempts.
- Preserve mistakes, failed prompts, parsing issues, and fixes as part of the research trace.
- Produce a final PDF report from Markdown with methodology, protocol, results, error analysis, and GitHub link.

## Progress Trace Rules

Every meaningful run or refinement should leave a trace:

- Add an entry to `LAB_JOURNAL.md`.
- Keep or regenerate report artifacts under `report/`.
- Record the command, subset, model, prompt version, serialization strategy, metrics, failures, and interpretation.
- Do not manually correct model outputs at evaluation time.
- If a failure leads to a fix, record both the failure and the fix. The difficulty is part of the project, not noise.

Current baseline artifacts:

- `data/subset/manifest.json`
- `report/report.md`
- `report/tables/summary_metrics.md`
- `report/tables/per_example_metrics.md`
- `report/tables/failure_breakdown.md`
- `report/figures/metric_summary.png`

## M0: Baseline Already Achieved

Status: complete

Goal: prove that the scaffold, Spider data wiring, API client, both pipelines, evaluation, and report generation can run end to end.

Completed:

- Created Python package scaffold under `src/spiderlens/`.
- Created local `.venv` workflow with `requirements.txt`.
- Uploaded Spider 1.0 dev/train data under `data/spider/`.
- Built a 3-example `concert_singer` smoke subset.
- Ran Text-to-SQL and Direct Table QA.
- Generated prediction JSONL, metric JSONL, Markdown tables, a plot, and a first report.
- Fixed the Direct Table QA parser to accept both bare JSON row lists and `{"rows": ...}` objects.

Observed mistake worth keeping:

- Direct Table QA initially returned a valid JSON object, but the parser only accepted a bare JSON list.
- After parser support was added, Direct Table QA still over-returned the full singer table for one count question, giving high recall but poor precision/cardinality.

Acceptance evidence:

- `pytest`: 9 passed.
- `ruff`: all checks passed.
- `text_to_sql`: 3 successful records.
- `table_qa`: 3 successful records.
- `metrics`: 6 successful records.

## M1: Strengthen Reporting Pipeline

Goal: make reporting reproducible, traceable, and useful for project decisions before improving prompts.

Steps:

- Add a stable run identifier to output records and generated report assets.
- Generate a single run summary Markdown file for every experiment.
- Include model settings, subset path, prompt/serialization strategy, record counts, metric means, and failure counts.
- Add metric delta tables so later runs can be compared against the previous run or baseline.
- Add failure summaries grouped by pipeline, failure label, database, and query pattern.
- Make report generation tolerate failed examples without hiding them.
- Link report artifacts from the lab journal.

Acceptance criteria:

- A new run can be reproduced from documented commands.
- Report tables clearly show per-example metrics, aggregate metrics, and failure counts.
- Each experiment has enough metadata to explain what changed since the previous run.

Expected artifacts:

- `report/runs/<run_id>/summary.md`
- `report/runs/<run_id>/per_example_metrics.md`
- `report/runs/<run_id>/failure_breakdown.md`
- `report/runs/<run_id>/metric_summary.png`
- Journal entry describing reporting changes and any rough edges.

## M2: Evaluation And Error Tracing

Goal: harden the scoring and failure-labeling layer so later experiments can be trusted.

Steps:

- Ensure failed attempts score recall and precision consistently.
- Add explicit labels for invalid SQL, SQL execution error, parse error, empty output, timeout/API error, and over/under-answering.
- Add tests for empty outputs, duplicate cells, numeric/string normalization, row ordering, and failed records.
- Decide whether tuple order remains optional or gets implemented for ordered queries.
- Preserve raw model output and parsed output for all examples.
- Add an error-analysis helper that extracts representative examples by failure type.

Acceptance criteria:

- Metric behavior is documented and tested.
- Failure labels appear in generated report tables.
- Failed examples are visible in both JSONL artifacts and Markdown reports.

Expected artifacts:

- Updated tests under `tests/`.
- Updated report failure tables.
- Journal entry with at least one intentionally inspected failure.

## M3: Prompt And Parser Iteration

Goal: improve both pipelines through documented trial and error without erasing failed attempts.

Steps:

- Version prompt templates for Text-to-SQL and Direct Table QA.
- Strengthen Direct Table QA output constraints for aggregate answers.
- Test zero-shot prompt variants first.
- Add one few-shot variant only if zero-shot failures justify it.
- Compare Markdown, JSON rows, and compact table serialization for Direct Table QA.
- Keep cached raw responses and journal notes for failed prompt attempts.
- Avoid manual correction of outputs at evaluation time.

Acceptance criteria:

- At least two prompt/serialization iterations are compared.
- The report can explain which changes helped and which did not.
- Parser changes are driven by recurring valid response shapes, not one-off manual fixes.

Expected artifacts:

- Prompt version notes in `LAB_JOURNAL.md`.
- Run summaries comparing baseline vs refined prompts.
- Updated report tables showing metric changes.

## M4: Subset Expansion

Goal: build the assignment subset: at least 10 Spider questions across at least 2 databases and multiple query patterns.

Steps:

- Select examples from Spider dev only.
- Use at least 2 databases.
- Annotate each manifest example with oracle tables and query pattern.
- Include projection, simple selection, multi-condition selection, aggregation, grouping, and ordering.
- Prefer a balanced subset that includes easy and difficult cases.
- Validate that every gold SQL query executes locally.
- Document why each example was chosen.

Acceptance criteria:

- `data/subset/manifest.json` contains at least 10 examples.
- Every example has `db_id`, question, gold SQL, oracle tables, rationale, and query pattern metadata.
- Gold SQL execution succeeds for every example.

Expected artifacts:

- Expanded manifest.
- Subset summary table in report assets.
- Journal entry explaining subset selection choices.

## M5: Main Experiment Run

Goal: run the main comparison on the curated subset and freeze the quantitative evidence.

Steps:

- Run Text-to-SQL and Direct Table QA on the full curated subset.
- Evaluate both pipelines against gold SQL outputs.
- Generate aggregate and per-pattern metrics.
- Produce plots for pipeline comparison and failure distribution.
- Record model settings, prompt versions, serialization strategy, and number of runs.
- If rerunning, preserve separate run IDs rather than overwriting the story.

Acceptance criteria:

- Both pipelines produce one record per subset example.
- Metrics exist for every pipeline/example pair.
- Report assets clearly support the Results section of the final PDF.

Expected artifacts:

- Full prediction JSONL files.
- Full metric JSONL file.
- Report tables and figures for the main run.
- Journal entry with commands, counts, failures, and interpretation.

## M6: Error Analysis

Goal: turn mistakes into the strongest part of the report.

Steps:

- Find examples where Text-to-SQL succeeds and Table QA fails.
- Find examples where Table QA succeeds and Text-to-SQL fails.
- Find examples where both fail for different reasons.
- Include at least one example involving formatting/parsing issues if it occurs.
- Discuss hallucination, context size, serialization choices, SQL ambiguity, aggregation mistakes, and normalization limits.
- Quote or summarize raw model outputs only as needed; focus on diagnosis.

Acceptance criteria:

- The final report has concrete qualitative cases, not only aggregate metrics.
- Each case links back to run artifacts and metrics.
- The discussion distinguishes model failures from system/parser/evaluation failures.

Expected artifacts:

- Error-analysis notes in `LAB_JOURNAL.md`.
- Selected examples table for final report.
- Optional appendix-style Markdown with raw-output excerpts.

## M7: Final Report

Goal: write the assignment deliverable as Markdown first, then export it to PDF.

Required sections:

- Methodology: model, prompts, table serialization, parsing, normalization, and SQL error handling.
- Experimental Protocol: Spider subset, questions, schemas, model settings, number of runs, and failure scoring.
- Results: quantitative tables/plots for cell precision, cell recall, and tuple cardinality.
- Error Analysis: qualitative comparison of failure modes.
- GitHub Link.

Steps:

- Promote the best report notes from `report/report.md` and `LAB_JOURNAL.md`.
- Keep the final narrative honest about small-sample limitations.
- Include reproducibility commands and environment setup.
- Export Markdown to PDF.
- Do a final check that no API key or raw ignored artifact is committed accidentally.

Acceptance criteria:

- Final PDF contains every required assignment section.
- GitHub repository includes executable code, dependencies, and configuration instructions.
- The report uses generated tables/plots instead of hand-copied unsupported claims.

Expected artifacts:

- `report/final_report.md`
- `report/final_report.pdf`
- Final generated tables and figures.

## M8: Future Improvements

Goal: document realistic extensions beyond the assignment scope.

Possible extensions:

- Tuple order and tuple constraint metrics.
- More serialization strategies.
- Few-shot prompt banks.
- Multiple LLMs or local models.
- Multiple runs per prompt for variance analysis.
- Larger Spider subsets.
- Better run dashboard or HTML report.
- Table truncation/windowing strategies for large databases.
- Automatic query pattern tagging.

Acceptance criteria:

- Future work is clearly separated from assignment requirements.
- Extensions are framed as next research steps, not hidden missing work.
