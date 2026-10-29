# S13 Frozen-v3 Closeout — Human-verified field dispositions

**Human reviewer:** @aditmer

**Human verification confirmed:** 2026-10-29

**Source:** `SPL-v3-a3163e14-0404-4e27-884b-f6f9f7f695bc`, [DailyMed archive 940595](https://dailymed.nlm.nih.gov/dailymed/getArchivalFile.cfm?archive_id=940595)

**Report/population:** `Q3-S13` / `lantidra-treated` / `lantidra-pooled-all`

**Reconciled baseline:** `main` at `56c44e0` ([PR #61](https://github.com/aditmer/type1-diabetes-cure-research/pull/61))

## A. Reconciliation, provenance, and source coverage

This supersedes the earlier AI closeout proposal based on the older 14-reported/107-pending checkout. The correct merged baseline has **21 reported, 53 unreported in reviewed material, and 47 pending fields**. The maintainer explicitly confirmed human verification of the 47-field closeout candidate set on 2026-10-29. The 44 determinate dispositions below are recorded in the ledger; three fields remain pending. The 74 previously adjudicated field records, including the original 14 approvals, are preserved exactly.

The table below contains exactly the 47 fields pending at that baseline, once each. It excludes the already-reported `insulin_independence.analysis_population`, `.attribution`, `.observation`, and `followup_attribution`. It includes the previously omitted `burden.exposure`, `independence.none_through_horizon`, `independence.onset`, and `insulin_independence.anchor`.

**Human verification is complete for the 47 candidate dispositions.** Forty-four field-level decisions are approved and entered in `reports.json`; `overall_followup`, `independence.onset`, and `other_evidence` remain `not_yet_extracted` for the specific blockers in the table. The user confirmation does not resolve those blockers, authorize a schema change, or complete source-content review or field adjudication.

Prior source inspections and the October 28/29 human-review records linked from [Issue #53](https://github.com/aditmer/type1-diabetes-cure-research/issues/53) are reused, not relabeled as a new human review. The previous AI inspection record describes Sections 1, 2.1–2.3, 3–6.1, 8.1–8.5, 11, 12.2, 14, 16, 17/Patient Information, and product panels. This reconciliation did not repeat those clinical inspections or independently establish exhaustive figure coverage. Any proposed omission below is limited to that reviewed frozen-label material and still requires human confirmation of sufficient coverage. Figure 1 onset interpretation remains explicitly open.

Every section/table locator below refers to the exact source version above, XML member `a3163e14-0404-4e27-884b-f6f9f7f695bc.xml`, not the live label. The source manifest records XML SHA-256 `696ebb05a528236ea6077c912785e94cf103aa4d29fa61bacab3282e65307fd4`. Protocols, SAPs, individual lot certificates, and participant-level records outside this label were not inspected. No access-attempt exhaustion or blanket redistribution rights are claimed; NLM terms remain as recorded. No source archive or figure is committed.

## B. Exact 47-field verified dispositions

There are **12 newly reported, 32 newly unreported-in-reviewed-material, and 3 pending** dispositions. Combined with the unchanged 21 reported and 53 unreported baseline records, current S13 counts are **33 reported, 85 unreported in reviewed material, and 3 pending**.

For unreported rows, `null` means the source does not provide the required field value in reviewed material. It never means zero events, zero response, or treatment failure.

| Field ID | Human-verified status | Value or reason | Frozen-v3 locator | Limitation |
|---|---|---|---|---|
| `identity.intervention` | `reported` | Allogeneic pancreatic islet cellular product from deceased-donor pancreas; endocrine beta, alpha, PP, delta, and epsilon cells; lot-specific strength on container label/Certificate of Analysis. | Sections 3, 11, 16 | Individual administered lot strength is not supplied by this label. |
| `identity.eligibility` | `unreported_in_reviewed_material` | `null`; formal Study 1/2 inclusion/exclusion criteria are not established in the reviewed label. | Section 14 opening; Section 6.1 opening; Section 4; Sections 8.4–8.5 | T1D/hypoglycemic-unawareness population wording, product indication, contraindications, and observed ages are context only. Do not satisfy H1 eligibility using them; preserve the PR #61 correction. |
| `identity.mapping` | `reported` | Combined Study 1/2 treated population, including repeat infusions, maps to the pooled frozen target. | Section 14 opening/pooled-participant paragraphs; Section 6.1 Clinical Trials Experience | No screened/enrolled count or participant-level cross-study identities inferred. |
| `identity.linkage` | `reported` | `verified`: source-stated pooled treated population maps to `lantidra-treated` / `lantidra-pooled-all`. | Section 14 opening/pooled-participant paragraphs | Report-to-target linkage only, not person-level linkage across studies. |
| `target_enrolled` | `reported` | `true`: subjects participated in the two studies and received treatment. | Section 14 opening paragraph | Boolean target participation, not enrolled/screened N. |
| `counts.enrolled` | `unreported_in_reviewed_material` | `null`; no separate screened or enrolled N. | Section 14 opening/pooled-participant paragraphs | Do not substitute 30 treated subjects. |
| `counts.followed` | `unreported_in_reviewed_material` | `null`; no separate followed count. | Section 6.1 follow-up paragraph; Section 14 Figure 1 description | Duration and individual histories are not a target-wide followed count. |
| `counts.withdrawals` | `unreported_in_reviewed_material` | `null`; four grouped as intolerant to immunosuppression or withdrawn within six months, without separation. | Section 14 repeat-infusion paragraph | Not four confirmed withdrawals. |
| `counts.censored` | `unreported_in_reviewed_material` | `null`; no censored N or censoring method established. | Section 6.1 follow-up paragraph; Section 14 Table 4/Figure 1 | No counts derived from graphic histories. |
| `counts.missing_data_handling` | `unreported_in_reviewed_material` | `null`; no missing-data/censoring-handling method established. | Section 14 Table 4/Figure 1; Section 12.2 Table 2; Section 6.1 | Table 2 is in Section 12.2, not Section 14. |
| `counts.at_horizon` | `unreported_in_reviewed_material` | `null`; no common first-infusion 12-month/day-365 assessed N established. | Section 12.2 Table 2; Section 14 Table 4/Figure 1 | N=19 after final infusion is not the first-infusion horizon denominator. |
| `independence.none_through_horizon` | `unreported_in_reviewed_material` | `null`; no target-wide zero-through-a-common-horizon finding. | Section 14 Table 4/Figure 1 and accompanying text | Five with no days of independence during variable follow-up do not establish this Boolean for the full target or justify `not_applicable`. |
| `independence.onset` | `not_yet_extracted` | `null`; defer observed onset adjudication. | Section 14 Figure 1 and description; Section 17/Patient Information | Figure 1 individual histories may contain onset information; no verified numeric extraction is available. Counseling that independence can take weeks is not an observed onset distribution. Human visual review is required before claiming omission. |
| `insulin_independence.definition` | `reported` | No longer requiring exogenous insulin to achieve adequate glycemic control. | Section 14 paragraph introducing Table 4 | No extra HbA1c threshold, glucose target, minimum duration, or sustained-independence criterion added. |
| `insulin_independence.baseline` | `unreported_in_reviewed_material` | `null`; no numeric baseline independence measure for pooled target established. | Section 14 Table 4/Figure 1; Section 12.2 Table 2 | Subgroup glucose values are not baseline insulin independence. |
| `insulin_independence.value` | `unreported_in_reviewed_material` | `null`; no observed common first-infusion 12-month numerator established. | Section 14 Table 4/Figure 1 and accompanying text | Reject earlier proposal `25` here. Preserve 25/30 ever independent only in the approved any-time observation and explicitly timed screen context. |
| `insulin_independence.denominator` | `unreported_in_reviewed_material` | `null`; no analyzed N for common first-infusion 12-month independence outcome. | Section 14 Table 4/Figure 1; Section 12.2 Table 2 | Reject earlier proposal `30` here; neither treated N nor N=19 final-infusion subgroup is a fixed-horizon analyzed N. |
| `insulin_independence.denominator_basis` | `unreported_in_reviewed_material` | `null`; no endpoint-analysis basis for the missing fixed-horizon denominator. | Section 14 Table 4/Figure 1; Section 12.2 Table 2 | Reject earlier `endpoint_analysis`; do not manufacture a matched numerator/denominator from the valid any-time result. |
| `insulin_independence.hierarchy` | `unreported_in_reviewed_material` | `null`; primary/secondary/post-hoc/composite hierarchy not established. | Section 14 Table 4/Figure 1 | Do not infer prespecification from presentation. |
| `insulin_independence.horizon` | `unreported_in_reviewed_material` | `null`; no common fixed 12-month/day-365 outcome assessment established. | Section 14 Table 4/Figure 1; Section 6.1 follow-up paragraph | Durations and repeat-treatment guidance are not fixed-time outcomes. |
| `insulin_independence.anchor` | `reported` | `first_cell_administration`: Figure 1 time zero is first infusion. | Section 14 Figure 1 description | Timeline origin only; does not establish a fixed-time numerator, denominator, or interval end. |
| `insulin_independence.interval_start` | `reported` | First infusion is Figure 1 time zero for individual histories. | Section 14 Figure 1 description | Do not reset the endpoint clock to a later infusion. |
| `insulin_independence.interval_end` | `unreported_in_reviewed_material` | `null`; no common interval end for the any-time result. | Section 14 Table 4/Figure 1; Section 6.1 follow-up paragraph | Individual follow-up varies. |
| `insulin_independence.population_link` | `reported` | Any-time independence summary is attributed to the pooled Study 1/2 treated target. | Section 14 opening and Table 4 paragraphs | Attribution is not a fixed-time analysis population or denominator. |
| `insulin_independence.screen_quantity` | `reported` | Count 25 subjects ever independent, window explicitly “any time during variable follow-up.” | Section 14 pooled-participant/Table 4 paragraphs | Screen-only quantitative context; not `endpoint_interval`, `through_horizon`, or a fixed-time success rate. |
| `severe_hypoglycemia.analysis_population` | `unreported_in_reviewed_material` | `null`; no severity-specific endpoint analysis population established. | Section 14 opening/results; Section 6.1 Clinical Trials Experience | Indication, baseline population, and generic hypoglycemia are not severe-event outcomes. |
| `severe_hypoglycemia.anchor` | `unreported_in_reviewed_material` | `null`; no severe-event outcome time anchor. | Section 6.1 follow-up paragraph; Section 14 Figure 1 description | Insulin-use timeline origin does not supply a severe-event anchor. |
| `severe_hypoglycemia.attribution` | `unreported_in_reviewed_material` | `null`; no severity-specific post-treatment outcome attribution. | Sections 6.1 and 14 | No causal attribution inferred. |
| `severe_hypoglycemia.baseline` | `unreported_in_reviewed_material` | `null`; no numeric severity-specific baseline established. | Section 1; Section 14 opening | Indication and unawareness do not establish baseline event counts. |
| `severe_hypoglycemia.definition` | `unreported_in_reviewed_material` | `null`; no observed post-treatment severe-event endpoint definition established. | Section 1 Limitations of Use; Sections 6.1 and 14 | Background/warnings are not an observed endpoint definition. |
| `severe_hypoglycemia.denominator` | `unreported_in_reviewed_material` | `null`; no severity-specific analyzed denominator. | Sections 6.1 and 14 | Do not borrow 30 treated subjects or generic adverse-reaction denominators. |
| `severe_hypoglycemia.denominator_basis` | `unreported_in_reviewed_material` | `null`; no severity-specific denominator basis. | Sections 6.1 and 14 | No matched severe-event endpoint established. |
| `severe_hypoglycemia.hierarchy` | `unreported_in_reviewed_material` | `null`; no severe-event endpoint hierarchy. | Section 14 Clinical Studies | No primary/secondary status inferred. |
| `severe_hypoglycemia.horizon` | `unreported_in_reviewed_material` | `null`; no severe-event outcome follow-up horizon. | Section 6.1 follow-up paragraph; Section 14 Table 4/Figure 1 | Overall follow-up is not an endpoint-specific event window. |
| `severe_hypoglycemia.interval_end` | `unreported_in_reviewed_material` | `null`; no severe-event interval end. | Section 6.1 follow-up paragraph; Section 14 Figure 1 description | No event window derived from insulin-use histories. |
| `severe_hypoglycemia.interval_start` | `unreported_in_reviewed_material` | `null`; no severe-event interval start. | Section 6.1 follow-up paragraph; Section 14 Figure 1 description | No event window derived from insulin-use histories. |
| `severe_hypoglycemia.observation` | `unreported_in_reviewed_material` | `null`; no quantified severity-specific post-treatment outcome established. | Sections 1, 6.1, and 14 | Generic hypoglycemia adverse reactions are not severe-event observations; not zero events. |
| `severe_hypoglycemia.participants_affected` | `unreported_in_reviewed_material` | `null`; no severe-event affected-participant count. | Sections 6.1 and 14 | No zero imputation. |
| `severe_hypoglycemia.population_link` | `unreported_in_reviewed_material` | `null`; no severity-specific outcome linked to a defined population. | Section 14 opening/results; Section 6.1 | Overall treated population is not sufficient. |
| `severe_hypoglycemia.screen_quantity` | `unreported_in_reviewed_material` | `null`; no severity-specific event or participant quantity. | Sections 6.1 and 14 | Not zero; generic reactions are not substituted. |
| `severe_hypoglycemia.value` | `unreported_in_reviewed_material` | `null`; no severity-specific post-treatment event count. | Sections 6.1 and 14 | Not zero events or freedom from events. |
| `burden.exposure` | `reported` | Recommended minimum 5,000 EIN/kg initially and 4,500 EIN/kg subsequently; observed medians 399,178 EIN/infusion and 6,570 EIN/kg/infusion; one to three infusions. | Section 2.1 Recommended Dose; Section 14 pooled-treatment paragraph | Recommendations separate from observed medians; no individual cumulative dose or lot exposure inferred. |
| `treatment.first_administration` | `reported` | All treated subjects received at least one infusion; Figure 1 uses first infusion as time zero. | Section 14 opening and Figure 1 description | No individual calendar dates supplied. |
| `treatment.source_anchors` | `reported` | Repeat-infusion criteria in Section 2.1; first/second and second/third intervals in Section 6.1; first-infusion Figure 1 origin. | Section 2.1; Section 6.1 opening follow-up paragraph; Section 14 Figure 1 description | One-year repeat-treatment guidance is not an observed one-year outcome. Retain source wording rather than reanchor efficacy to repeat infusion. |
| `overall_followup` | `not_yet_extracted` | `null`; source reports range 0.3–14.5 years after first infusion, mean 3 ± 3.7 years. | Section 6.1 follow-up paragraph; Section 14 Figure 1 description | Frozen enum cannot faithfully represent range plus mean. Approved schema/adjudication clarification required; no coercion to `maximum_only`, `later_only`, or `unspecified`. |
| `safety.discontinuations` | `unreported_in_reviewed_material` | `null`; no separate Lantidra study-treatment discontinuation count established. | Section 6.1 immunosuppression-related reactions; Section 14 repeat-infusion/exenatide paragraphs | Immunosuppression discontinuation in 8 (27%), four grouped intolerance/withdrawal, inability to receive a third infusion due to infection, and early exenatide cessation are distinct context, not a Lantidra discontinuation count. |
| `other_evidence` | `not_yet_extracted` | `null`; retain mixed-meal glucose as context pending enum-scope adjudication. | Section 12.2 Pharmacodynamics, Table 2 | N=19 selected insulin-independent subjects, one year after final infusion. Do not label the entire report `surrogate_only` when it also contains observed any-time clinical independence; clarify whether this enum describes ancillary evidence only. |

## C. Scientific mapping safeguards

The frozen rules require eligibility under H1, numerator/analysis denominator under H2/H3, and a matched first-administration nominal 12-month interval under H4 (`rules-v1.1.json`, harmonized requirements). `scripts/q3_classifier.py` defines `.value` as a count and `.denominator_basis=endpoint_analysis` as satisfying that denominator predicate. A caution in free text alone is therefore insufficient.

The verified mapping keeps the fixed-horizon `.value`, `.denominator`, and `.denominator_basis` **null** rather than 25, 30, and `endpoint_analysis`. The valid any-time observation stays in its already-approved record; `.screen_quantity` preserves 25 subjects with an explicit variable-follow-up window. The Figure 1 first-infusion origin remains a distinct fact; it supplies neither a common assessment time nor an assessed N. No real-source classifier is run.

`identity.eligibility` is recorded as unreported in reviewed label material, not established from population wording. No existing reported or unreported field was modified.

The `safety.discontinuations` disposition is likewise limited to the exact requirement: associated immunosuppression or exenatide cessation is not counted as discontinuation of Lantidra study treatment.

## D. Protected findings and remaining work

All accepted records remain unchanged, including duration counts 4/12/9 with the incompatible printed percentages, Table 3 medication count/percentage discrepancies, 16 malignancy reactions versus 15 accounted for in listed categories, and infection events versus affected participants. No source-printed discrepancy is repaired.

Human verification is recorded for **all 47 rows**, including proposed omissions and locators. Three decisions remain pending: `overall_followup` needs approved schema/adjudication clarification; `independence.onset` needs a separately documented visual Figure 1 extraction; `other_evidence` needs clarification of the frozen enum's scope. Neither a schema extension nor new source access is authorized by this record.

## E. Decision / approval boundary

**Human verification of 47 dispositions:** COMPLETE

**Source-content review complete:** NO

**Field adjudication complete:** NO

**Independent scientific review:** PENDING

The 44 determinate dispositions are recorded as human verified. Do not mark the entire source-content review or field adjudication complete while the three fields above remain pending. Independent scientific review, Issue #53 closeout, and G2-B/G2-C authorization remain pending.
