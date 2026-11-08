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
view-level cohort links with the same structural, identity, target, and
provenance checks as measured records. Linked views and non-uncertain link
targets require explicit synthetic cohort identities; self-links are invalid,
and unresolved overlap remains quarantined.

Measured-result units use a controlled synthetic vocabulary: declared
participant/event count units (case/whitespace variants select the same
comparator but the original text is preserved) and `synthetic proportion`
(finite numeric values from zero through one). Count values must match their
corresponding synthetic participant/event count. Unknown units and participant
counts exceeding the analysis denominator are quarantined because their
semantics or basis are unresolved; no clinical unit mapping or enrollment
interpretation is implied. Reference objects have exact shapes: source
references contain only `source_id`, `source_version`, and `location`; EP-12
constituent references contain only `record_id` and `endpoint_id`; follow-up
windows contain only `value` and `unit`. See
`docs/evidence-atlas/PHASE-3A-SOURCE-CONTRACT.md` for the detailed synthetic
contract and limits.
