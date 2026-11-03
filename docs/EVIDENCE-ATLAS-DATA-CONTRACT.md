# Evidence Atlas data contract

The machine-readable structural contract is `experiments/evidence-atlas/schema.json`; its cross-entity and scientific-integrity invariants are enforced by `scripts/build_evidence_atlas.py`. The Phase 1 fixture is `experiments/evidence-atlas/synthetic-fixture.json`.

## Entities and relations

| Entity | Key and role |
| --- | --- |
| Therapeutic approach | `approach_id`; category, mechanism description, cell origin, immunosuppression context, and development-status description. |
| Clinical program | `program_id`; links a program/developer to exactly one `approach_id`, its studies, and dated milestones. |
| Study and cohort | `study_id`; preserves design, target population, eligibility, registry identifier when available, follow-up, and cohort identity. Cohort relationships are explicit edges (`same`, `subset`, `distinct_within_program`, or `uncertain`); uncertainty is not treated as independence. For `subset`, `from_study_id` is a proper subset of `to_study_id`; the other relationships are symmetric. `distinct_within_program` requires non-overlapping studies in the same program. |
| Clinical outcome | `outcome_id`; one endpoint for one study, with the original definition, observation state, typed result, denominator, units, time point and anchor, source references, review state, and limitations. |
| Evidence provenance | `source_id` plus `source_version`; reference and exact location, extraction state, human-review state, approval state, adjudication history, and discrepancies. Outcome and cohort source references bind to a known source version and a location explicitly cataloged by that source or a slash-delimited descendant of one. |

The full field definitions and accepted values are in the JSON Schema. `registry_id` and `follow_up` may be `null` when unavailable. A missing value is never encoded as numerical zero. An observed result declares `value_kind`: `participant_count` requires its integer value to equal its participant numerator, while `source_defined` retains other values such as percentages, event counts, and continuous or qualitative measurements. A `source_defined` result need not include a participant numerator when one is unavailable. The units `participant(s)` and `synthetic participant(s)` are reserved for participant counts. The kind does not harmonize or convert the source's units.

## Status semantics and promotion rules

Field evidence uses the repository's exact six Q3 field states: `reported`, `unreported_in_reviewed_material`, `inaccessible`, `not_yet_extracted`, `conflicting`, and `not_applicable`. Observation state is a separate dimension: `observed`, `planned`, `not_reported`, or `unknown`. A `reported` field can describe a planned endpoint; it does not mean an observed outcome.

Only an `observed` outcome with `field_status: reported`, a non-null result, source-version-bound references, a denominator where the endpoint is quantitative, and an assessment time/anchor may display a result. Planned, unreported, pending, inaccessible, conflicting, and inapplicable outcomes retain a null result. A planned endpoint may have a timepoint, anchor, both, or neither; available timing is labeled as planned, never observed. Conflicting evidence requires at least two distinct source/version/location references and a discrepancy; the locations may be in the same source. Explicitly unreported evidence requires a completed review of the relevant material; `not_yet_extracted` does not mean the source omitted the outcome.

Human review and clinical approval are distinct from extraction status. The prototype's only permissible data scope is `synthetic_only`; synthetic sources must remain explicitly unreviewed for clinical use and unapproved as clinical evidence. Synthetic `reported` records are not clinical findings. Fixture statuses illustrate the contract only and must not be read as evidence that any real source was reviewed.

## Comparison and aggregation constraints

The contract stores source-defined outcome definitions, thresholds, units, population, denominator, timepoint, and anchor. It does not provide harmonization, scoring, ranking, pooled estimates, or a cure label. Different endpoint definitions remain separate. Cohort edges display their source versions and locations when recorded, or explicitly state that no references are recorded. An `uncertain` relationship is never converted to disjointness or used to aggregate counts.

The JSON Schema describes record shape. The Python validator additionally checks unique IDs, references, conditional result requirements, denominator bounds, timing, conflict evidence, synthetic source binding, and relationship integrity. It rejects subset cycles and distinct cohorts that share a known subset, after accounting for transitive `same` links; `uncertain` links assert neither overlap nor disjointness. Tests cover each mandatory edge case.

## Cohort identity and evidence scope

`cohort_id` is a global population identity within one Atlas dataset, not a source-local label. Reusing an ID asserts that the studies concern the same population, even across programs. Namespace source-local identifiers before assigning them. Shared identities enter graph validation as `same` edges, so they cannot also be declared distinct or proper subsets, directly or transitively. Different IDs alone do not prove disjointness.

Every cohort reference must be attached to at least one linked study through its `source_ids`, or explicitly scoped to it through the source's optional `study_scope`. Resolved relationships require the cited evidence collectively to cover both studies. `study_scope` contains known, unique `study_ids` and a nonempty `note` documenting why the source covers those populations; it permits cross-study mapping sources without attaching unrelated outcome evidence. Scope declarations remain synthetic metadata, not human clinical approval. Uncertain links may have incomplete or absent evidence, but unrelated citations are rejected.

## Build boundary and provenance display

The standard-library builder enforces required fields and field allowlists for every record, including nested results, milestones, source references, review history, and study scopes. The allowlists are read from the committed schema to avoid drift; this is record-shape enforcement, not a general JSON Schema engine. Explicit runtime checks enforce the scientific and scalar-value constraints. Unknown properties are rejected rather than silently removed or embedded. CI rebuilds the viewer and compares it byte-for-byte with the committed HTML.

Source references retain their visible version and location. Expand **Source review and discrepancies** for extraction, human-review and approval states, adjudication entries, discrepancies, and documented cross-study scope. Empty history and discrepancy lists are identified explicitly. The same provenance display is used in the explorer, comparison cards, and cohort links.
