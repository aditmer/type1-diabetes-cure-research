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

## Endpoint and reporting-view constraints

Retain the source endpoint definition and approved taxonomy identifier separately. A difference in threshold, population, time anchor, unit, or analysis rule is not repaired by relabeling or normalization. An unresolved or incompatible definition is quarantined. `EP-12` is a longitudinal reporting view, not an independently measured outcome: it can only reference eligible, separately identified constituent endpoint/outcome records. It must not carry a standalone result, denominator, or independent clinical claim.

The current `taxonomy-v2.json` draft requires EP-12 assessments for `time_origin`, `follow_up_distribution`, `number_at_risk`, `withdrawals`, `censoring`, `retreatment`, `ongoing_cointerventions`, `constituent_endpoint_ids`, and `constituent_outcome_record_refs`. These are required assessments, not assertions that every value is known. A field assessment must retain its original state and nullable value; a pending or unavailable field is not converted into a guessed value or another taxonomy state.

The experimental adapter implements only a synthetic demonstration of that assessment shape. Its `time_origin` assessment retains each eligible constituent's own source-faithful `time_origin` and `timing_anchor` in a `constituent_specific_unharmonized` structure; it does not require the anchors to match, compare them, or translate them to a common origin. An optional view-level `time_origin`/`timing_anchor` pair must be internally consistent, but is not compared with constituent anchors. A claimed constituent common-origin mapping or a mismatch between a timing assessment and its referenced constituent is quarantined because no such rule is approved. The adapter requires all nine assessment slots and exact agreement between eligible constituent records and the two constituent-reference assessments. Other fields may be explicitly marked pending in synthetic fixtures; unreported or conflicting assessments are quarantined because this demonstration cannot represent or verify their required field-specific review or distinct conflict provenance. The resulting view is labeled `synthetic_only_with_pending_required_fields` and is not represented as fully populated or scientifically taxonomy-compliant. Missing timing, assessment, or provenance fails closed by quarantine. This partial implementation does not approve any state mapping or extend to real-source records.

For this prototype, a reported EP-12 `number_at_risk` cannot be negative or an empty value; an explicitly source-reported zero remains valid. Optional view-level cohort links receive the same structural, target, identity, subset-direction, and provenance checks as measured-record links. Self-links are rejected, and an unresolved relationship remains quarantined rather than implying independence or permitting pooling.

## Cohorts, transformation trace and status

Every transformation records the source version, exact locator, original field status/value, target identifier, rule ID/version, and deterministic disposition. Do not edit the source record. A duplicate publication remains a distinct report attached to its cohort; it is not additional participants. `uncertain` cohort links remain visible and block analyses requiring distinctness or aggregation. A transformation without an approved rule is not performed.

The adapter's `synthetic-fixture-only` rights and review markers are test scaffolding, not valid real-source values. No software-generated reviewer, approval, rights grant, or authorization can satisfy this proposed contract.
