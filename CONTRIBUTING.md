# Contributing

Thanks for helping improve the evidence map. Contributions should make claims more precise, traceable, and useful.

## Before submitting

- Read the [charter](docs/CHARTER.md) and [evidence framework](docs/EVIDENCE-FRAMEWORK.md).
- Prefer primary studies, official trial registries, and regulatory documents.
- Do not include personal health data, identifying patient stories, treatment instructions, or promotional material.
- Disclose relevant financial or professional conflicts.

## Updating evidence

1. Add or revise one principal claim per row in `data/evidence.csv`.
2. Use a stable claim ID and cite a source ID that resolves to a direct source in the landscape or related report.
3. Record model/population, design, denominator, endpoint, follow-up, co-interventions, limitations, and status-check date. Use `unknown` where not reported.
4. For trial status, use the official registry record and record the date checked. Registry status does not guarantee current site availability.
5. Update the report with evidence-consistent language; include negative, inconclusive, and safety evidence.
6. Run `python3 scripts/validate_data.py` and review the resulting diff.

## Review standard

Reviewers should challenge denominator drift, endpoint inflation, causal claims from uncontrolled data, missing harms, stale trial status, and language that implies cure without durable evidence. Corrections should preserve a dated note in the report.
