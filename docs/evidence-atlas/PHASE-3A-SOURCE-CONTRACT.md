# Evidence Atlas Phase 3A proposed source contract

**Status: proposed interface, not approved for real-source use.** The contract is versioned independently from the Phase 1 schema and from Q3's frozen extraction ledger. It is not a request to change either one. Pending Issue #92 decisions and Issue #59 gates must fail closed.

## Proposed manifest

One manifest entry identifies one exact source version and an explicitly authorized subset of its fields. A record carries source-faithful facts and their provenance; it does not infer a target value. A batch manifest may refer to multiple sources, but each endpoint record remains bound to its own source version, population, cohort, and locator.

The proposed scope contract is exact by top-level record field: every projected source value must be named in `authorized_field_scope`, and every field emitted by the projection is checked against that allowlist. The nested EP-12 `field_assessments` object is one declared group; its child keys must exactly match the nine required taxonomy-draft assessment IDs, with no extras or missing slots. Identity, original state, and source locators are mandatory scope members. Audit bindings retain only those authorized record fields plus that identity/state/provenance envelope; adapter-control inputs are not projected as source values.

```json
{
  "contract": "evidence-atlas-source-manifest",
  "contract_version": "0.1.0-proposal",
  "manifest_id": "assigned-by-authorized-governance-process",
  "purpose": "explicitly approved purpose",
  "authorization": {
    "decision_id": "human decision reference",
    "decision_date": "YYYY-MM-DD",
    "authority": "authorized human role",
    "scope": ["source/version/field/purpose"],
    "status": "pending | approved | denied | expired"
  },
  "sources": [
    {
      "source_id": "catalog ID",
      "source_version": "exact revision or version identifier",
      "original_record_reference": "exact original reference",
      "document_type": "source-defined type",
      "registry_trial_study_id": "identifier or null",
      "allowed_access_route": "documented permitted route",
      "rights": {
        "status": "not_established | restricted | explicitly_authorized",
        "evidence_reference": "rights decision or terms reference",
        "redistribution": "not_established | prohibited | explicitly_authorized"
      },
      "authorized_field_scope": ["field IDs"],
      "evidence_context": "human | preclinical | registry | regulatory | other",
      "provenance": {
        "extraction_status": "exact source-system state",
        "source_review_status": "exact review state",
        "field_review_status": "per-field review state",
        "human_approval_state": "exact decision state",
        "reviewer_authority": "human role and decision scope"
      },
      "records": [
        {
          "record_id": "stable versioned record ID",
          "field_id": "source field ID",
          "original_field_status": "exact source-system state",
          "supporting_locator": "page, table, figure, section, registry-history field, etc.",
          "endpoint_id": "approved taxonomy ID or unresolved",
          "endpoint_definition": "source-defined wording, threshold and unit",
          "population_id": "source-defined population/analysis set",
          "cohort_id": "versioned cohort identity or unresolved",
          "cohort_links": [
            {
              "other_cohort_id": "identity",
              "relationship": "same | subset | distinct_within_program | uncertain",
              "evidence_locator": "source locator or null",
              "adjudication": "human decision reference or pending"
            }
          ],
          "time_origin": "source-defined anchor or unresolved",
          "follow_up_window": "source-defined window or unresolved",
          "participant_denominator": "source-defined count or unavailable",
          "analysis_denominator": "source-defined analysis count or unavailable",
          "observed_measurement_count": "actual observed count or unavailable",
          "missing_data_method": "source description or unavailable",
          "measurement": "source-reported value or unavailable",
          "co_interventions": "source-defined exposure or unavailable",
          "known_discrepancies": ["unresolved issue references"],
          "transformation": {
            "software": "name",
            "version": "version",
            "rule_id": "approved deterministic rule or none"
          }
        }
      ]
    }
  ]
}
```

This illustrative shape is not a finalized JSON Schema. `not_established`, `unresolved`, and `pending` are explicit barriers, not permissive defaults. A missing required fact produces a rejection or quarantine reason. Values remain source-defined; no placeholder or unavailable status becomes a numeric value.

## Independent facts that must not be conflated

| Fact | What establishes it | Does not establish |
|---|---|---|
| Source exists | Stable catalog/reference record | Lawful access, review, reuse, or evidence validity |
| Source was accessed lawfully | Evidence of the specific user's permitted access route and applicable terms | That all source material was accessed, or that it was reviewed |
| Source was reviewed | Dated human review record describing exact version and scope | Review of every field, independent review, approval, or Atlas authorization |
| Particular fields were reviewed | Field-specific locator and completed review scope | Approval of the value or permission to redistribute it |
| Particular values were human-approved | Explicit human decision for those values and exact source/version/field/use | Approval of other values, sources, transformations, or target mappings |
| Source and fields are authorized for Atlas integration | Applicable, explicit governance decision covering source/version, field, access, transformation, intended use, and rights | Broader source access, publication, redistribution, or any later version |
| Redistribution is permitted | Applicable rights evidence for the specific material and use | Permission inferred from an open URL, catalog inclusion, or an access event |

Every fact is independently recorded and checked. None is automatically inferred from another.

## Status, result and denominator preservation

Q3 field states are exactly `reported`, `unreported_in_reviewed_material`, `inaccessible`, `not_yet_extracted`, `conflicting`, and `not_applicable`. The Phase 1 schema uses the same states for its synthetic fixture, but equality of spelling is not an approved general compatibility rule. The Phase 2 taxonomy draft also proposes separate assessment values such as `not_reported` and `unknown`. Do not map these states, collapse them, or classify a pending review as an omission until a dated Issue #92 decision defines the mapping and its validation.

For quantitative records retain, separately and without coercion:

- total participants, endpoint numerator, event count, analysis denominator, and number with observed measurements;
- source-defined denominator basis, including whether imputation was used and how;
- endpoint definition, population, unit, threshold, assessment time, time origin, and follow-up window;
- planned versus observed status, co-interventions, and source-reported zero/unfavorable values.

The existing evidence tracker defines `analysis_denominator` as the number assessed. The Phase 2 taxonomy proposal discusses a source-defined analysis denominator that may include imputed values. This discrepancy is pending maintainer decision; the contract does not choose between them. An observed measurement count is never substituted for either denominator. An event count is never substituted for affected participants. Missing values are not zero.

The synthetic adapter checks only that `observed_measurement_count` does not exceed `analysis_denominator` when both explicitly identify the same synthetic population. It does not declare a general population basis for `participant_count`; if that value exceeds `analysis_denominator`, the record is quarantined with an unresolved-basis reason rather than treated as impossible or accepted as a total. For the bundled synthetic contract only, a participant-count result unit is compared with `participant_count`, and an event-count result unit is compared with `event_count`; these narrow conventions are not general clinical interpretations, nor evidence that the participant count is total enrollment. `strip`/case-fold classification is used only to select the synthetic count comparator; the source unit text is preserved verbatim in projection and audit, and equality is still required. The controlled measured-result unit vocabulary is the declared participant/event spellings (including case/whitespace variants for comparison only) and exact `synthetic proportion`. That synthetic-only proportion accepts finite numeric values from zero through one; it does not imply a numerator or clinical interpretation. Other unit strings are quarantined as unsupported instead of being accepted without count semantics. In this synthetic shape, `follow_up_window` is exactly `{ "value": <positive number>, "unit": <nonempty text> }`, and each `source_refs` item is exactly `{ "source_id": <text>, "source_version": <text>, "location": <text> }`. Extra nested payloads are rejected rather than ignored. These narrow shape checks apply only to the fixture demonstration; source-defined `co_interventions` remain intentionally open-ended and are preserved without interpretation.

## Endpoint and reporting-view constraints

Retain the source endpoint definition and approved taxonomy identifier separately. A difference in threshold, population, time anchor, unit, or analysis rule is not repaired by relabeling or normalization. An unresolved or incompatible definition is quarantined. `EP-12` is a longitudinal reporting view, not an independently measured outcome: it can only reference eligible, separately identified constituent endpoint/outcome records. It must not carry a standalone result, denominator, or independent clinical claim.

An optional synthetic EP-12 `follow_up_window` uses the same exact positive finite `value`/nonempty `unit` validation as measured records; it does not complete the separate required `follow_up_distribution` assessment or harmonize constituent follow-up. Measured-record `participant_count_status`, `participant_count_review`, and `participant_count_conflicts` are prohibited on EP-12, even when null or empty, alongside the standalone count itself. The reporting view must use its supported assessment objects instead; attaching a participant-review payload does not establish human approval or authorization. Audit-safe representations of invalid supplied values remain in the rejection audit only when their top-level field is included in the applicable synthetic `authorized_field_scope`; otherwise that field is omitted from the audit. They are not emitted in an accepted view projection.

The synthetic EP-12 top-level shape permits only `record_id`, `record_kind`, `source_id`, `source_version`, `endpoint_id`, `field_status`, `source_refs`, `review_evidence`, `constituents`, and `field_assessments`, plus validated optional `time_origin`, `timing_anchor`, `follow_up_window`, `cohort_id`, and `cohort_links`. `requested_state_mapping` is recognized solely for the existing fail-closed quarantine path, not as an authorized transformation. Other measured-only or uninterpreted top-level fields are rejected, including `observation_status`, `co_interventions`, and `mapping_target_definition`; measured-record source-defined `co_interventions` remain open-ended.

Reported values in the EP-12 `follow_up_distribution`, `withdrawals`, `censoring`, `retreatment`, and `ongoing_cointerventions` assessments are quarantined with `REPORTING_VIEW_ASSESSMENT_SCHEMA_UNRESOLVED`: this demonstration has no supported reported-value schema for those slots. This intentionally tightens prior acceptance of unchecked values, including benign scalars/narratives as well as nested measurement or approval payloads, without inventing clinical semantics or filtering by suspicious key names. Audit-safe representations of the original assessment state, value, and provenance remain in the audit only when the `field_assessments` group is included in the applicable synthetic `authorized_field_scope`; otherwise that group is omitted from the audit. Supported pending/unavailable null states remain usable within scope and retain the partial/pending label. Neither audit retention nor a synthetic marker validates an approval claim.

The current `taxonomy-v2.json` draft requires EP-12 assessments for `time_origin`, `follow_up_distribution`, `number_at_risk`, `withdrawals`, `censoring`, `retreatment`, `ongoing_cointerventions`, `constituent_endpoint_ids`, and `constituent_outcome_record_refs`. These are required assessments, not assertions that every value is known. A field assessment must retain its original state and nullable value; a pending or unavailable field is not converted into a guessed value or another taxonomy state.

The experimental adapter implements only a synthetic demonstration of that assessment shape. Its `time_origin` assessment retains each eligible constituent's own source-faithful `time_origin` and `timing_anchor` in a `constituent_specific_unharmonized` structure; it does not require the anchors to match, compare them, or translate them to a common origin. An optional view-level `time_origin`/`timing_anchor` pair must be internally consistent, but is not compared with constituent anchors. A claimed constituent common-origin mapping or a mismatch between a timing assessment and its referenced constituent is quarantined because no such rule is approved. Each constituent reference is exactly an object with `record_id` and `endpoint_id`; extra keys or nested payloads are rejected rather than projected without validation. The adapter requires all nine assessment slots and exact agreement between eligible constituent records and the two constituent-reference assessments. Other fields may be explicitly marked pending in synthetic fixtures; unreported or conflicting assessments are quarantined because this demonstration cannot represent or verify their required field-specific review or distinct conflict provenance. The resulting view is labeled `synthetic_only_with_pending_required_fields` and is not represented as fully populated or scientifically taxonomy-compliant. Missing timing, assessment, or provenance fails closed by quarantine. This partial implementation does not approve any state mapping or extend to real-source records.

For this prototype, a reported EP-12 `number_at_risk` must be a scalar non-negative integer count; an explicitly source-reported zero remains valid. Booleans, fractional or negative values, empty values, and structured or narrative values are rejected because no approved schema interprets them. Do not equate this view-level count with a constituent denominator without an approved matching-population and time-basis rule. Optional view-level cohort links receive the same structural, target, identity, subset-direction, and provenance checks as measured-record links. A view with cohort links requires an explicit synthetic cohort identity; a non-uncertain link also requires a target with a valid synthetic identity. Self-links are rejected, and an unresolved relationship remains quarantined rather than implying independence or permitting pooling.

## Cohorts, transformation trace and status

The synthetic adapter enforces one conservative 2,000,000-credit recursive-expansion/copy budget per call, shared across input preflight, generated diagnostic copying, audit construction, projection snapshot expansion checks, and final report serialization-shape traversal. Each occurrence of a value or dictionary key costs 64 credits, plus 12 per string character or the integer's bit length. These conservative costs cover JSON punctuation/primitive text and ASCII-escaped string expansion, including non-BMP characters. Preflight additionally charges 24 per path character on entry, before building diagnostics, covering path traversal and diagnostic text amplification. Invalid-input issue-copy cost is measured and charged before duplicating reasons per record; audit dictionary-key scans spend credits as they scan. Snapshot expansion is charged before deep copying, and repeated source/audit/projection occurrences spend the same aggregate budget. The final report traversal counts all occurrences, including aliases, and conservatively bounds serialized report size rather than counting only unique containers. Unsupported-type name length is charged before normalization.

Budget exhaustion fails closed with `INPUT_EXPANSION_BUDGET_EXCEEDED`, `status=rejected`, empty `records`/`projection`, and explicit `audit_omission`; no further input audit or serialization of its payload is attempted. This compact fallback deliberately omits even otherwise scoped audit fields, instead of recursively expanding the rejected input again. Standalone preflight and audit helpers likewise return one bounded reason or omission marker on exhaustion. Budget failure replaces partial diagnostics, so it does not promise to retain every other validation reason. Ordinary below-budget scoped audit and small shared-alias detached snapshots are unchanged. The budget intentionally tightens compatibility for large/wide synthetic inputs, repeated aliases, long diagnostic paths, and cross-record source/report copying. It is a deterministic experimental resource/serialization boundary, not a clinical count limit, authorization, process-memory cap, or universal wall-clock guarantee.

Synthetic object keys must be exact built-in strings; string subclasses follow the unsupported-key/value rejection path. Rejected-input audit assembly first filters manifest/source/record envelopes to exact built-in keys and uses only exact built-in identity and scope strings for lookup/membership. Unsupported envelope keys are omitted rather than interpreted; retained nested unsupported keys are represented by audit-safe markers. Neither path invokes their custom copy, text, hash, or equality hooks. Existing applicable synthetic field-scope limits still govern audit retention.

Recursive preflight and audit sanitization recognize only exact built-in primitives and containers, including `float`, `dict`, `list`, and `tuple`; subclasses are unsupported and are never traversed or converted through custom hooks. Invalid-input envelopes likewise traverse only exact built-in containers. Ordinary built-in dictionaries/lists/tuples retain their supported behavior, including detached tuple-preserving projection snapshots and tuple-to-array audit-safe representations. This technical type boundary does not authenticate the caller-supplied synthetic marker.

Built-in type recognition uses identity-only comparisons rather than equality-based class membership, so unsupported classes cannot invoke metaclass equality hooks during preflight or rejection reporting. Audit-safe unsupported-type marker names are read through the built-in `type` name descriptor, bypassing custom metaclass name lookup and shadowing name properties while preserving ordinary class-name marker text.
The descriptor result is normalized through the built-in `str.__str__` method to an exact built-in string without invoking subclass text hooks, including when a string subclass has been assigned as a class name.

For each record kind's local validation, rejection-class reasons take precedence over quarantine reasons: only a nonempty local reason list consisting entirely of that kind's explicitly defined quarantine reasons produces a local `quarantined` disposition; any rejection-class local reason produces `rejected`, preserving all reasons and blocking projection. This local vocabulary includes `REPORTING_VIEW_ASSESSMENT_INVALID`, so it is not a claim that all malformed inputs reject. Graph-only issues, such as `COHORT_LINK_PROVENANCE_MISSING`, can separately quarantine an otherwise accepted record, and related source issues can separately reject it; final quarantined outcomes need not have every reason in the local vocabulary. Thus invalid follow-up windows remain rejected alongside unresolved EP-12 assessments or unsupported measured units. This intentionally tightens prior mixed-failure dispositions, including missing required review fields, state/value mismatches, and uncertain links missing required cohort identity. Unresolved-only controls retain their defined quarantine behavior, not authorization. Result/count and proportion comparisons apply only when the result state is `reported`; null pending/inaccessible/conflicting results do not falsely claim a measured value to compare. Conflicting results still require complete separate provenance, or reject alongside their adjudication requirement.

The experimental synthetic-input preflight conservatively rejects integers with magnitude at least `10**640` anywhere in the input, including nested values and invalid integer dictionary keys, with `INTEGER_MAGNITUDE_EXCEEDED`. It compares integer magnitudes directly without decimal conversion. Accepted integers have at most 640 decimal digits, remaining serializable under CPython 3.11+'s minimum configurable 640-digit conversion limit; the adapter does not change process conversion settings. Audit-safe representations replace oversized integers, including keys, with `{"unsupported_input": "integer magnitude exceeds synthetic limit"}` without calling `str` or `repr` on them. This is a serialization boundary, not a clinical count schema or authorization. The prior `+/-10**400` proportion controls remain within this boundary and reject with `PROPORTION_VALUE_INVALID` rather than overflowing.

In the synthetic cohort-link shape, `subset` requires `direction` to be exactly `this_is_subset` or `other_is_subset`. For `same`, `distinct_within_program`, and `uncertain`, direction has no defined meaning: it must be omitted or explicitly null, and any non-null value is rejected rather than projected as an uninterpreted payload. This rule applies to measured records and reporting views. Structurally valid uncertain links still quarantine without pooling or inferring independence.

Every transformation records the source version, exact locator, original field status/value, target identifier, rule ID/version, and deterministic disposition. Do not edit the source record. A duplicate publication remains a distinct report attached to its cohort; it is not additional participants. `uncertain` cohort links remain visible and block analyses requiring distinctness or aggregation. A transformation without an approved rule is not performed.

The adapter's `synthetic-fixture-only` rights and review markers are test scaffolding, not valid real-source values. No software-generated reviewer, approval, rights grant, or authorization can satisfy this proposed contract.
