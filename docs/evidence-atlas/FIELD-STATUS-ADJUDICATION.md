# Evidence Atlas field-status adjudication

**Status: proposed human decision aid; no status mapping is approved or implemented here.**

## Purpose and invariants

This document supports a maintainer decision about how the proposed Evidence Atlas field-assessment vocabulary relates to the existing Q3 extraction contract. It does not implement a technical mapping, change an approved record, or authorize extraction.

Q3's canonical field status is exactly one of these six values:

1. `reported`
2. `unreported_in_reviewed_material`
3. `inaccessible`
4. `not_yet_extracted`
5. `conflicting`
6. `not_applicable`

These are field-evidence states. They do not encode source-access permission, human clinical approval, G2-B/G2-C status, or whether an outcome is planned versus observed. Those dimensions must remain separate.

## Proposed conceptual adjudication

The table below is a decision aid for human review, **not an approved machine crosswalk**. Agent B owns any technical mapping, implementation, or tests, and must not infer approval from this table.

| Canonical Q3 field state | Closest proposed Atlas field state | Required interpretation and guardrail |
|---|---|---|
| `reported` | `reported` | A source-reported value or statement is locatable and attributable to an identified source/version. The field state alone does not mean an outcome was observed; planned/observed status is separate. |
| `unreported_in_reviewed_material` | `not_reported` | Use only after the relevant permitted material has actually been reviewed for the field. A search of an incomplete excerpt, an unreviewed source, or a registry record alone cannot establish this state. |
| `inaccessible` | `inaccessible` | Relevant material could not be accessed within permitted routes. Do not relabel it as not reported or treat it as a negative result. |
| `not_yet_extracted` | `not_yet_extracted` | Extraction has not been completed. Do not equate pending extraction with omission, zero, or a reviewed absence. |
| `conflicting` | `conflicting` | Material contains unresolved inconsistent values/statements. Preserve each locator and the discrepancy; do not choose a value or average them without an authorized adjudication. |
| `not_applicable` | `not_applicable` | The field does not apply to the defined record, with rationale under the governing contract. Do not use this as a substitute for missing or unknown information. |

### Atlas-only vocabulary and separate dimensions

- `unknown` is present in the proposed Atlas vocabulary but is **not** a seventh Q3 field state. It must not be automatically emitted from Q3 or used to collapse `inaccessible`, `not_yet_extracted`, `conflicting`, or `unreported_in_reviewed_material`.
- `pending` is not a canonical Q3 field state and is not an Atlas missingness state. Use it only as a decision/approval workflow status when the relevant process defines it. Pending approval cannot be represented as a source field status.
- `planned`, `observed`, `not_reported`, and `unknown` in the proposed taxonomy's observation dimension do not replace the field-status dimension. A source may report that an endpoint was planned, without an observed result.
- “Not reported” and `unreported_in_reviewed_material` are not warranted merely because a result is absent from a repository catalog, abstract, partial excerpt, or unreviewed registry snapshot.
- A reported zero requires an explicit source report. Missing, inaccessible, unextracted, conflicting, or inapplicable values are never converted to zero.

**Decision status: PENDING.** A maintainer must approve, revise, defer, or reject the conceptual relationship before Agent B's technical mapping work is treated as approved. Even after approval, implementation requires its own review and validation.

## Status-by-status crosswalk detail

The Q3 vocabulary is defined in `experiments/q3/rules-v1.1.json` and consumed by `scripts/validate_q3_extraction.py`; Q3 extraction records also carry source version, locator, review scope, access log, review-complete flag, reason codes, and adjudication notes. The draft taxonomy-v2 field-assessment contract defines seven distinct Atlas statuses and unavailable values as null. The Phase 1 builder currently uses the canonical six Q3 statuses, not this seven-state draft taxonomy-v2 vocabulary. That is an unresolved interface, not permission to change either contract.

| Exact Q3 source state and review meaning | Candidate Atlas destination / classification | Required provenance and review prerequisite | Human approval and round-trip rule |
|---|---|---|---|
| `reported` — field value is explicitly available under the Q3 report/field contract. Review still requires the source/version and a field-specific locator; `reported` alone does not mean observed outcome. | `reported` — **conditional; exact only when** the Atlas field represents the same source-defined field/value and separately preserves observation state. Mapping to `not_reported`, `not_yet_extracted`, `inaccessible`, `not_applicable`, `conflicting`, or `unknown` is **prohibited**. | Preserve source ID/version, target population/subcohort, exact locator, review scope, raw value/units/timepoint and the status separately from planned/observed state. | Maintainer approval is required before any mapping. Keep original `reported` state and source value; a target-only value without source binding cannot round-trip. |
| `unreported_in_reviewed_material` — reviewer completed review of the relevant permitted material and did not find the field. This is not equivalent to absent-from-catalog, inaccessible, or not yet extracted. | `not_reported` — **conditional and lossy** because the target status does not itself encode the Q3 review scope or what material was reviewed. Mapping to any other target status, especially `unknown` or `not_yet_extracted`, is **prohibited**. | Preserve the complete relevant-material review scope, source/version, access limits, exact field definition, reviewer/date and locations or documented search boundary supporting the absence. | Maintainer approval is required. Preserve the canonical state and its review evidence alongside the target status; without that pair, reverse mapping is unsupported. Never infer this state from a partial abstract, missing tracker row, or unreviewed source. |
| `inaccessible` — material needed to assess the field could not be accessed under the documented route/rights context. | `inaccessible` — **conditional and potentially lossy** if the target status collapses restricted, unavailable, failed-access, and unreviewed cases. Mapping to `not_reported`, `not_yet_extracted`, or `unknown` is **prohibited** as a substitute for the access state. | Preserve source/version, attempted/available route, access log, rights and restrictions, material not reviewed, reviewer/date and affected field. Do not copy restricted content. | Maintainer approval is required. Preserve original state and access log to round-trip; the Atlas value alone is not sufficient. Inaccessibility never means zero or source omission. |
| `not_yet_extracted` — field extraction/review is incomplete; absence from the ledger is not evidence that the source omitted the field. | `not_yet_extracted` — **conditional and potentially lossy** if the target's generic “not extracted or reviewed” wording merges extraction-pending and review-pending details. Mapping to `not_reported`, `inaccessible`, `not_applicable`, or `unknown` is **prohibited**. | Preserve source/version, field ID, outstanding extraction/review step, current review scope, and any known access/rights limitation separately. | Maintainer approval is required. Preserve canonical status and workflow detail; target-only status cannot recover stage-of-review distinctions. Pending extraction never becomes zero or “not reported in reviewed material.” |
| `conflicting` — source evidence for the field is contradictory and unresolved; Q3 retains review and adjudication details. | `conflicting` — **conditional and lossy** unless all competing values and provenance remain separately available. Mapping to a selected `reported` value or to `unknown` is **prohibited**. | Preserve each competing source/version/locator/value, population/timepoint context, discrepancy description, reviewer/date, and unresolved state. No silent choice, average, or reconciliation. | Maintainer approval is required. Preserve the original state and conflict bundle; `conflicting` alone cannot round-trip the source evidence. |
| `not_applicable` — the field does not apply under the specified record/field context, with the Q3 structural basis/reason. | `not_applicable` — **conditional and potentially lossy** if the target status omits why and to what context it applies. Mapping to `not_reported` or `unknown` is **prohibited**. | Preserve field definition, population/endpoint context, reason code or structural basis, source/version and reviewer note. | Maintainer approval is required. Retain the canonical state and rationale for round-trip; do not use it as a generic missing-value status. |

For each row, candidate mapping quality is a property of the **proposed representation**, not of the source evidence. All mappings remain inactive unless separately approved. Any destination status not named as the candidate for a source row is prohibited for that row; in particular, `unknown` is not a catch-all mapping for any canonical Q3 state. No status is mapped to zero.

### Destination vocabulary meanings and prohibited conflations

| Draft Atlas destination | Candidate meaning in taxonomy-v2 | Use boundary |
|---|---|---|
| `reported` | A non-null field value is explicitly available in source. | Preserve source value/provenance; does not establish observed outcome. |
| `not_reported` | Reviewed material does not report the value; this does not establish that it was not collected. | Requires review of the relevant permitted material. Not a substitute for Q3's complete review scope unless that provenance is retained. |
| `not_yet_extracted` | Value has not yet been extracted or reviewed. | Must remain distinct from `not_reported` and `inaccessible`. |
| `inaccessible` | Needed material is inaccessible or restricted. | Preserve access attempts, rights boundary, and unreviewed material. |
| `not_applicable` | Field does not apply to the stated endpoint/reporting context. | Requires explicit context and rationale. |
| `conflicting` | Source values conflict and remain unresolved. | Conflicting values and locators must live outside this null-valued status record. |
| `unknown` | Value or availability cannot be established. | Not a canonical Q3 state and not an allowed substitute for any of the six states. Use only under a separately approved Atlas-only definition. |

`pending` is not a destination status in this list. Approval state, source-review state, field availability, outcome observation state, and access/rights status are separate dimensions. A pending approval never changes source evidence into a field status.

### Reversibility and approval gate

For a future interface, the minimum loss-avoidance proposal is to retain the original Q3 `status` and associated Q3 provenance as immutable source-side values, then store any separately approved Atlas assessment as an additional, versioned representation with an explicit mapping-rule version. The mapping must not overwrite Q3 data. A round-trip test must prove that every original state and its relevant provenance can be recovered; where this cannot be proven, retain the original state and do not claim reversibility. This recommendation is a proposed design constraint, not an implemented schema.

Approval dependencies are: maintainer decision on terminology; Agent B's reviewed technical mapping and tests; separate review of status collisions, null behavior, and round-trip; and exact source-specific authorization before transforming any real record. None is satisfied by this document.

## Denominator and imputation illustration (fully synthetic)

**Every number, unit, participant, and result below is invented. This is not a real source, patient record, clinical result, or extraction instruction.**

Imagine a wholly synthetic endpoint with 12 fictional participants (`SYN-P01` through `SYN-P12`). The invented measurements for `SYN-P01`–`SYN-P10` are 4.7, 5.0, 5.2, 5.4, 4.9, 5.3, 4.8, 5.1, 5.5, and 4.6 synthetic units. `SYN-P11` and `SYN-P12` have no observed measurement. For this demonstration only, a single synthetic completed dataset imputes 5.0 and 5.2 for those two missing measurements, respectively. Its illustrative completed-dataset mean is 5.06 synthetic units (60.7 / 12). This is a toy single-imputation calculation, not a recommended clinical method or a result from a source.

| Quantity | Synthetic illustration | Meaning |
|---|---:|---|
| Analysis population in the hypothetical report | 12 fictional participants | The example analysis includes all 12, including the two with imputed measurements. |
| Participants assessed / observed measurement count | 10 | Number with an actually observed measurement for this endpoint and timepoint. |
| Missing measurements | 2 | No observed measurement; their missingness remains explicit. |
| Synthetic imputed values | 5.0 and 5.2 invented units | Made up solely to demonstrate the arithmetic; never claim these are observed values or sourced data. |
| Synthetic completed-dataset mean | 5.06 invented units | One toy completed-dataset calculation; not a pooled multiple-imputation estimate or clinical result. |
| Existing tracker `analysis_denominator` under its current definition | 10 | Number assessed; retain this meaning unless a separately reviewed contract change is approved. |
| Proposed versioned Atlas analysis population, if approved in future | 12 population; 10 observed; 2 missing; method/value provenance separately recorded | A distinct structure could represent the analysis population and measurement observation without redefining the existing tracker field. No such structure is implemented here. |

The example shows the semantic conflict if a single `analysis_denominator` is expected to mean both number assessed and the analysis population used by an analysis. It does **not** direct anyone to update a tracker or create a real-source Atlas record. For real sources, the project must preserve only source-reported method/values; no participant-specific imputation may be invented. The alternatives and decision dependency are documented in the [maintainer decision brief](PHASE-2-MAINTAINER-DECISION-BRIEF.md).

## Adjudication and implementation dependencies

Before any future source-specific field adjudication, authorized reviewers would need the exact source/version, lawful access route, relevant material actually reviewed, precise field definition, source locator, observed/planned distinction, denominator type, timepoint, missingness method, and any unresolved discrepancy. This package does not perform those steps.

Before any technical status or denominator mapping is implemented, dependencies include:

1. An explicit maintainer decision on the relevant semantics.
2. Agent B's separately reviewed proposal for the technical interface, schema, validation, and migration behavior, if any.
3. Tests proving that no state is collapsed, that the existing tracker meaning is preserved unless explicitly changed, and that no missing value becomes zero.
4. Any additional source-rights, human review, and governance approvals required for the proposed scope.

These dependencies do not alter Issue #59. Q3 G2-B remains pending; G2-C remains blocked. No status mapping authorizes source access or real-source integration.
