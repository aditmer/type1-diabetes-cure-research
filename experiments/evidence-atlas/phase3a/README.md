# Phase 3A synthetic adapter

This experimental module is a synthetic-only contract demonstration. It is not
a production adapter, source importer, rights checker, approval service, or
authorization control. It does not discover production data, make network
requests, or write to trackers or the Phase 1 Atlas.

Run the bundled fixture and print its deterministic report:

```sh
python3 experiments/evidence-atlas/phase3a/adapter.py
```

Run the 20-case adversarial matrix and determinism checks:

```sh
python3 -m unittest tests.test_evidence_atlas_phase3a -v
```

Only `synthetic-manifest.json` is read by the CLI. Its invented values and
synthetic-only rights/review placeholders do not represent clinical evidence,
human approval, or a source-use grant. Rejection and quarantine reasons are
machine-readable and the input is never mutated.

The EP-12 demo accepts only scalar non-negative integer reported
`number_at_risk` counts, preserving explicit zero; booleans, fractions,
negative, empty, structured, and narrative values are rejected. It validates
view-level cohort links with the same structural and provenance checks as
measured records; self-links are invalid, and unresolved overlap remains
quarantined.
