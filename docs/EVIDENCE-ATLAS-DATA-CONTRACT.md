# Evidence Atlas data contract

The machine-readable structural contract is `experiments/evidence-atlas/schema.json`; its cross-entity and scientific-integrity invariants are enforced by `scripts/build_evidence_atlas.py`. The Phase 1 fixture is `experiments/evidence-atlas/synthetic-fixture.json`.

## Entities and relations

| Entity | Key and role |
| --- | --- |
| Therapeutic approach | `approach_id`; category, mechanism description, cell origin, immunosuppression context, and development-status description. |
| Clinical program | `program_id`; links a program/developer to exactly one `approach_id`, its studies, and dated milestones. |
| Study and cohort | `study_id`; preserves design, target population, eligibility, registry identifier when available, follow-up, and cohort identity. Cohort relationships are explicit edges (`same`, `subset`, `distinct_within_program`, or `uncertain`); uncertainty is not treated as independence. |
| Clinical outcome | `outcome_id`; one endpoint for one study, with the original definition, observation state, typed result, denominator, units, time point and anchor, source references, review state, and limitations. |
| Evidence provenance | `source_id` plus `source_version`; reference and exact location, extraction state, human-review state, approval state, adjudication history, and discrepancies. Outcome source references bind to a known source version and specific location. |

The full field definitions and accepted values are in the JSON Schema. `registry_id` and `follow_up` may be `null` when unavailable. A missing value is never encoded as numerical zero.

## Status semantics and promotion rules

Field evidence uses the repository's exact six Q3 field states: `reported`, `unreported_in_reviewed_material`, `inaccessible`, `not_yet_extracted`, `conflicting`, and `not_applicable`. Observation state is a separate dimension: `observed`, `planned`, `not_reported`, or `unknown`. A `reported` field can describe a planned endpoint; it does not mean an observed outcome.

Only an `observed` outcome with `field_status: reported`, a non-null result, source-version-bound references, a denominator where the endpoint is quantitative, and an assessment time/anchor may display a result. Planned, unreported, pending, inaccessible, conflicting, and inapplicable outcomes retain a null result. Conflicting evidence requires at least two distinct source/version/location references and a discrepancy; the locations may be in the same source. Explicitly unreported evidence requires a completed review of the relevant material; `not_yet_extracted` does not mean the source omitted the outcome.

Human review and clinical approval are distinct from extraction status. The prototype's only permissible data scope is `synthetic_only`; synthetic sources must remain explicitly unreviewed for clinical use and unapproved as clinical evidence. Synthetic `reported` records are not clinical findings. Fixture statuses illustrate the contract only and must not be read as evidence that any real source was reviewed.

## Comparison and aggregation constraints

The contract stores source-defined outcome definitions, thresholds, units, population, denominator, timepoint, and anchor. It does not provide harmonization, scoring, ranking, pooled estimates, or a cure label. Different endpoint definitions remain separate. Cohort edges display their source versions and locations when recorded, or explicitly state that no references are recorded. An `uncertain` relationship is never converted to disjointness or used to aggregate counts.

The JSON Schema describes record shape. The Python validator additionally checks unique IDs, references, conditional result requirements, denominator bounds, timing, conflict evidence, synthetic source binding, and relationship integrity. Tests cover each mandatory edge case.
