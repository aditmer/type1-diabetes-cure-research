# Contributing

Thanks for helping improve the evidence map. Contributions should make claims more precise, traceable, and useful.

## Before submitting

- Read the [charter](docs/CHARTER.md) and [evidence framework](docs/EVIDENCE-FRAMEWORK.md).
- Prefer primary studies, official trial registries, and regulatory documents.
- Do not include personal health data, identifying patient stories, treatment instructions, or promotional material.
- Disclose relevant financial or professional conflicts.

## Updating evidence

1. Add or revise the source in `data/sources.csv`, with direct URL, source identifiers, publication/source date, and access date.
2. Add or revise one principal claim per row in `data/evidence.csv`, citing catalog IDs with `|` separators.
3. Record model/population, design, sample size, analysis denominator, endpoint, follow-up, co-interventions, limitations, and check date. Use `unknown` where not reported and explain why a denominator is unavailable.
4. For trial status, use the official registry record and record the date checked. Registry status does not guarantee current site availability. Distinguish registry state from sponsor program decisions.
5. Update the report with evidence-consistent language; include negative, inconclusive, and safety evidence, including uncertainty in causality and mechanism.
6. For failure-mode research, maintain `data/failure-modes.csv` as the single source of truth. Cite every observed claim through `source_ids`, distinguish evidence from hypotheses and unknowns, and keep modality-specific outcomes separate. Use the scoring rubric in [Sprint 02 Research Priorities](docs/SPRINT-02-RESEARCH-PRIORITIES.md); do not create a separately maintained Markdown copy of the matrix.
7. Label dataset candidates as unverified until access, reuse terms, metadata, and controls have been checked directly. A missing dataset or outcome is an evidence gap, not evidence that a mechanism occurred.
8. Run `python3 scripts/validate_data.py` and `python3 -m unittest discover -s tests -v`, then review the resulting diff. Open a pull request; scientific changes should pass the required validation check before merge.

## Review standard

Reviewers should challenge denominator drift, endpoint inflation, causal claims from uncontrolled data, missing harms, stale trial status, and language that implies cure without durable evidence. Corrections should preserve a dated note in the report.
