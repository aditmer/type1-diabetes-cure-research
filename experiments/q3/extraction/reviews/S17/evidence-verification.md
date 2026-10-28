# S17 automated evidence cross-check

> **Historical PR #45 access-blocker snapshot.** This note predates the
> maintainer's subsequent JSON download, v13 latest-version screenshot, and
> explicit approval of ten source-backed field decisions. For the current
> partial source-review state and provenance limits, see
> [`partial-adjudication-2026-10-27.md`](partial-adjudication-2026-10-27.md).
> The original findings are retained for audit, not as the latest ledger state.

**Status: source verification blocked; human adjudication pending.** This is an
automated preparation note, not a human attestation or an accepted extraction.
The authoritative `reports.json` and `source-review-log.csv` remain unchanged.

## Frozen source and access

- Report: `Q3-S17`; source: S17; program: `vc01`.
- Frozen target: `vc01-cohort2`; subcohort: `vc01-cohort2-planned` (planned
  efficacy Cohort 2, not Cohort 1).
- Approved version identifier: `NCT02239354-history-v13`.
- Approved version locator:
  [ClinicalTrials.gov history v13](https://clinicaltrials.gov/study/NCT02239354?tab=history&a=13#version-content-panel).
- The manifest identifies history v13 as submitted 2022-02-25, with the
  history panel as the approved reproducibility locator rather than a
  byte-identical archive. The official page URL returned page HTML, but the
  historical data endpoint returned HTTP 403 in this session. The version
  title, version-specific sections, and facts below therefore could not be
  independently inspected here. The manifest/candidate claims about version
  identity are retained as provenance metadata, not represented as a fresh
  verification.
- No current registry record or alternate history version was substituted.
  Search-result snippets and third-party registry mirrors were not used as
  evidence. The authorized human reviewer must attempt access through the
  approved locator. If the exact history-v13 content cannot be retrieved and
  identified, record the permitted access attempts and blocker, then keep S17
  unadjudicated; do not substitute another version.

The candidate packet says its source review was previously performed in a
browser and identifies history v13 as submitted 2022-02-25. This task could
not reproduce that review. The only independently confirmed access observation
is that the ClinicalTrials.gov page URL resolves to the registry page shell;
the historical record contents were blocked.

## Candidate-by-candidate comparison

The input contains 13 candidate facts: nine `candidate_for_human_review`
facts and four `context_only` facts. All 13 cite the approved version ID and
specific registry-module paths in their locator strings. Those locator strings
meet the repository's syntactic locator shape (approved version plus a
`protocolSection` or `resultsSection` path); syntactic validity does not prove
the location or value is present in the source. Because the historical payload
could not be read, **none of the source contents, values, units, precision,
denominators, or cohort attributions is independently confirmed in this
cross-check**.

| Candidate field or fact | Candidate claim and cited location | Automated cross-check / mapping assessment | Proposed handling |
|---|---|---|---|
| `target_enrolled` | `false`; `resultsSection.participantFlowModule.periods[Overall Study].milestones[STARTED].achievements[group=Cohort 2]` | A Boolean is compatible with the frozen field type, but the cited row and its value were not accessible. Its relation to the frozen Cohort 2 target is plausible from the group label, not independently established. | Defer; retain `not_yet_extracted`. Do not infer no enrollment from missing results. |
| `counts.enrolled` (Cohort 2) | `0 participants`; same Cohort 2 `STARTED` participant-flow achievement | An integer count is compatible with the field type. Source value, units, cohort label, and period were not verified. If confirmed, this would be the target count; it would not be a responder count. | Defer; retain `not_yet_extracted`; keep zero distinct from a clinical outcome. |
| `population_identified` | `true`; `protocolSection.designModule` and `armsInterventionsModule.armGroups[label=Cohort 2]` | Boolean mapping is type-compatible; source and frozen-target correspondence remain unverified. | Defer; retain `not_yet_extracted`. |
| `identity.population` | Planned efficacy Cohort 2, distinguished from Cohort 1; `protocolSection.designModule.designInfo` and `resultsSection.participantFlowModule.groups` | Text mapping is compatible. Exact wording and whether the history record consistently maps the planned efficacy target to this result group require human inspection. | Defer; retain `not_yet_extracted`. |
| `identity.disease_stage` | “Type 1 diabetes mellitus”; `protocolSection.identificationModule` and `eligibilityModule` | Text mapping is compatible; exact source statement not verified. | Defer; retain `not_yet_extracted`. |
| `identity.eligibility` | Adults 18–55 years; T1D for at least 3 years; stable treatment; CGM willingness; acceptable implant candidate; `protocolSection.eligibilityModule` | Text mapping is compatible, but criteria, units, and precision were not checked against the exact history version. CGM willingness is eligibility, not an observed CGM endpoint. | Defer; retain `not_yet_extracted`. |
| `identity.intervention` | VC-01 combination product described as biologic and device; `protocolSection.armsInterventionsModule.interventions[name=VC-01 Combination Product]` | Text mapping is compatible. The candidate explicitly does not establish that Cohort 2 received treatment. | Defer; retain `not_yet_extracted`; do not infer exposure from an intervention description. |
| `identity.design` | Interventional, non-randomized sequential two-cohort design, no masking; terminated status; `protocolSection.designModule` and `statusModule.overallStatus` | Text mapping is compatible. These are whole-study descriptors; they cannot replace target-specific participant flow. Exact values were not verified. | Defer; retain `not_yet_extracted`. |
| `identity.mapping` | Cohort 2 linked to C-peptide efficacy and Cohort 1 to adverse-event outcomes; `protocolSection.outcomesModule.primaryOutcomes` and `resultsSection.outcomeMeasuresModule` | Text mapping is compatible, but the outcome/group linkage and any denominator association need source review. No Cohort 1 safety or enrollment value may be assigned to Cohort 2. | Defer; retain `not_yet_extracted`; keep target and contextual cohort distinct. |
| Whole-study actual enrollment (context only; shares `counts.enrolled` field ID) | `19 participants`; `protocolSection.designModule.enrollmentInfo` | Candidate says this is whole-study enrollment, not the Cohort 2 denominator. It is not a second value for the frozen target field. The protocol enrollment and flow counts were not source-checked. | Do not propose `19` as Cohort 2 enrollment; retain only as a review prompt. |
| Participant-flow completion (context only; `counts.at_horizon`) | Cohort 2 completed `0` / not completed `0`; Cohort 1 completed `9` / not completed `10`; `resultsSection.participantFlowModule.periods[Overall Study].milestones[COMPLETED and NOT COMPLETED]` | The candidate is a prose bundle across two cohorts, whereas `counts.at_horizon` is a single count. It also describes overall flow status, not necessarily endpoint follow-up at the fixed clinical horizon. | No typed field value proposed; human reviewer should inspect each cohort and the source's definitions before mapping. |
| C-peptide result (context only; `other_evidence`) | Cohort 2 primary C-peptide change planned baseline to Month 6; candidate says denominator `0` and no numerical result; `protocolSection.outcomesModule.primaryOutcomes` and `resultsSection.outcomeMeasuresModule.outcomeMeasures[Change in C-peptide]` | The candidate does not establish an observed clinical result. `other_evidence` is a frozen enum (`none`, `surrogate_only`, `qualitative_only`), not a free-text field for this sentence; this prose is not a type-valid value for that field. C-peptide is not one of the specified P1 clinical endpoints. | No typed `other_evidence` value proposed. Do not treat denominator zero or absent numeric data as zero response, treatment failure, or observed efficacy. |
| Adverse events (context only; `safety.harms`) | Cohort 1: candidate reports 114 adverse events, denominator 19 participants, through Month 24; `resultsSection.outcomeMeasuresModule.outcomeMeasures[Number of Adverse Events Reported During the Study]` | The field is text-compatible, but the candidate explicitly scopes this result to Cohort 1, outside the frozen Cohort 2 efficacy target. Event definition, attribution, and window were not verified. | Do not enter as Cohort 2 safety evidence. Human may retain it as contextual information outside the target ledger record. |

### Zero-enrollment question

The four enrollment statements are internally **scope-compatible as candidate
claims**, not source-confirmed facts: Cohort 2 `Started=0`; Cohort 1
`Started=19`; whole-study actual enrollment `19`; and a Cohort 2 C-peptide
result denominator `0` with no candidate numerical outcome. The packet locates
each in the same approved-version identifier, `NCT02239354-history-v13`, but
this session could not read that version's payload to confirm the rows or that
they all belong to the same historical record.

If a human reviewer confirms target Cohort 2 enrollment is zero, the report's
eventual v1.1 classification must use the frozen no-enrollment precedence
(`not_applicable` at the report-label level, with `NO_TARGET_ENROLLMENT` as
applicable). This does **not** make zero responders, a negative clinical
result, or lack of efficacy. Preserve `target_enrolled` and `counts.enrolled`
as source-supported target facts if the reviewer approves them. Do not mark
all outcome fields or the whole record `not_applicable`: the extraction
validator restricts field-level `not_applicable` to supported baseline and
insulin-independence onset/duration cases with their structural evidence.
Nothing in this automated cross-check qualifies as that evidence or as a
human decision.

If the exact version or either flow row cannot be confirmed, retain target
enrollment as unknown/unextracted and stop before classification; do not infer
zero enrollment from the zero-denominator C-peptide row or from absence of
posted results.

## Additional permitted material and 121-field inventory

The frozen inventory has 121 IDs; the current S17 authoritative record has all
121 at `not_yet_extracted`. The nine candidate fields above are not an
exhaustive source review. For the human reviewer, the approved version's
protocol/eligibility/intervention/outcome sections and results participant
flow, outcome-measure, and adverse-event modules may potentially inform the
following unresolved field families:

- **Treatment exposure and procedures:** `treatment.first_administration`,
  `treatment.repeat_administrations`, `treatment.source_anchors`,
  `identity.intervention`, `identity.dose`, `burden.exposure`,
  `burden.repeat_procedures`, `burden.co_interventions`,
  `burden.immunosuppression`.
- **Baseline, eligibility, and design:** `identity.baseline_context`,
  `identity.eligibility`, `identity.disease_stage`, `identity.design`,
  `identity.comparator`, `identity.mapping`, `identity.linkage`,
  `identity.population`, `population_identified`.
- **Endpoints, result status, and analysis denominators:** `other_evidence`,
  `overall_followup`, `followup_attribution`, `counts.enrolled`,
  `counts.treated`, `counts.followed`, `counts.at_horizon`,
  `counts.censored`, `counts.withdrawals`, `counts.missing_data_handling`,
  and endpoint-specific `observation`, `attribution`, `value`, `baseline`,
  `definition`, `hierarchy`, `denominator`, `denominator_basis`, `units`,
  `summary`, `analysis_population`, `population_link`, `horizon`, `anchor`,
  and interval fields for each of the five frozen clinical domains.
- **Follow-up and attrition:** the global count fields above, plus
  endpoint-specific interval start/end, endpoint population, anchor, horizon,
  censoring, withdrawals, and missing-data handling.
- **Adverse events and safety:** `safety.harms`, `safety.population`,
  `safety.window`, `safety.attribution`, `safety.discontinuations`, and
  `severe_hypoglycemia.*` fields. Cohort 1 records cannot fill Cohort 2 fields.
- **Immunosuppression and other burden:** `burden.immunosuppression`,
  `burden.co_interventions`, `burden.exposure`, `burden.repeat_procedures`,
  `treatment.*`, and `identity.dose`.

No material in these modules was independently inspected here. This list
identifies relevant review directions, not evidence that the modules contain
qualifying facts or that any field is absent. No field is proposed as
`unreported_in_reviewed_material` or `not_applicable`; all unconfirmed fields
remain `not_yet_extracted`.

## Discrepancies, unresolved questions, and limitations

1. **Access blocker:** the approved historical payload returned HTTP 403;
   the source values and historical version title/date were not independently
   verified in this run.
2. **Cohort mapping:** human review must confirm the planned Cohort 2 target
   maps to the participant-flow and C-peptide result groups, rather than
   inferring it from group labels in the candidate.
3. **Denominators:** do not substitute whole-study actual enrollment `19`,
   Cohort 1 `Started=19`, Cohort 2 flow `Started=0`, or a C-peptide result
   denominator `0` for one another. Each candidate claim needs its exact
   source row and scope checked.
4. **Typed mappings:** the `counts.at_horizon` candidate is a multi-cohort
   prose statement, not a typed count; the `other_evidence` candidate is
   prose, not one of that field's three permitted enum values. Neither maps
   directly into those fields as written.
5. **Planned versus observed:** the candidate describes a planned C-peptide
   outcome and a zero analysis denominator, not a measured zero. It cannot
   establish an observed P1 outcome or a negative treatment result.
6. **Context-only Cohort 1:** the candidate's 19-participant flow and
   adverse-event record are contextual, not Cohort 2 efficacy/safety
   denominators.
7. **Additional evidence:** treatment, baseline, endpoint, follow-up, attrition,
   adverse-event, and intervention-burden fields remain unreviewed. Automated
   non-detection has not been used to declare any omission.
8. **Provenance limit:** the manifest's version-specific locator is the
   accepted provenance method; it is not a byte archive. Current API material
   or third-party mirrors must not be substituted for the approved version.

**Recommendation:** authorized human inspection of the exact approved
history-v13 panel is required before any proposed candidate is approved or
the record is classified. Preserve the authoritative ledger and Issue #35
gate unchanged until then.
