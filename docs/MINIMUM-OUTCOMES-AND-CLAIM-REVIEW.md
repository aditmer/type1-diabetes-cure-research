# Minimum Outcomes and Claim Review

**Project standard — 22 October 2026**

This rubric supports consistent comparison of type 1 diabetes interventions. It is a project-defined reporting standard, not a clinical guideline, regulatory requirement, or consensus cure threshold. A missing outcome is unknown, not evidence of no effect.

## Minimum outcome set

Report outcomes by domain; do not let a favorable surrogate replace patient-important benefit.

| Domain | Minimum outcomes to seek | Interpretation safeguards |
| --- | --- | --- |
| **Biological function** | Fasting and stimulated C-peptide; stimulation method, assay, units, baseline, and assessment time; graft survival/function where relevant | C-peptide or graft persistence supports biological activity, not by itself clinical benefit, insulin independence, or cure. |
| **Clinical benefit** | Insulin dose (including units/kg/day) and insulin independence with its definition and duration; HbA1c; CGM time in range (70–180 mg/dL) with the aggregation window; severe hypoglycemia events and participants affected | State baseline and follow-up values, endpoint definitions, and whether results are participant-level. Distinguish protocol primary endpoints from secondary, post hoc, surrogate, and composite endpoints. |
| **Harms and treatment burden** | Adverse events by seriousness, attribution, and observation window; immunosuppressive regimen and exposure; infections, malignancy, discontinuation, procedures/reoperations, device complications, monitoring, and follow-up burden | Report harms alongside benefits, including events after treatment stops. “Not reported” is not “none.” Separate observed events from causal attribution. |
| **Durability and access** | Persistence or loss of graft function and clinical benefit over time; repeat treatment; manufacturing and supply constraints; practical access and treatment burden | State time from treatment, censoring, withdrawals, and ongoing co-interventions. Durability is not inferred from a single assessment or a short insulin-free interval. |

## Follow-up and denominator standard

- For a clinical benefit comparison beyond early feasibility, this project uses **12 months of observed follow-up as its minimum reporting expectation**. Studies with less follow-up remain eligible, but label them early/short-term and do not use them to imply durability. This is an internal comparison rule, not an external threshold.
- A 12-month result alone does not establish durable benefit or cure. Use “durable” only with multi-year follow-up, a stated assessment schedule, and transparent reporting of ongoing immunosuppression, devices, or other co-interventions. State when available follow-up is too short to assess durability.
- At each reported outcome and time point, distinguish the numbers **enrolled, treated, analyzed for that outcome, and followed**. Give the outcome numerator and its analysis denominator for binary endpoints; give the analyzed denominator for continuous endpoints. Do not silently substitute one denominator for another.
- Describe baseline and comparator, observation window, endpoint hierarchy and definition, censoring, withdrawals, and missing-data handling. Give reasons for missingness when reported. Identify overlapping publications or cohorts; repeated reports are not independent participants.
- Preserve the source's precision. If counts or measurements cannot be extracted, mark the outcome qualitative or not reported as appropriate, explain the gap, and do not infer a value or denominator.

The 12-month expectation provides a common comparison horizon, not proof that every participant was observed that long. Report the number reaching that horizon, the follow-up distribution, and the number still at risk; do not apply the longest observed follow-up to the full cohort. Preclinical findings retain their model-specific observation windows and are not subject to the human follow-up expectation.

## How design and missing data affect confidence

Uncontrolled studies cannot separate treatment effects from selection, co-interventions, natural disease variation, or changes in care. Randomized comparative studies can support stronger causal conclusions, but endpoint selection, precision, attrition, and applicability still matter. A registered endpoint is not an observed result; exploratory or interim analyses need explicit qualification.

Analyzing only participants with complete follow-up can overstate benefit if those who withdraw, die, or lose graft function are omitted. Report the analysis population, missingness and reasons, censoring assumptions, and any sensitivity analyses. Do not invent missing outcomes or silently treat missing participants as successes or failures. Unexplained or outcome-related missingness lowers confidence, even when a reported fraction looks favorable. Abstract-only extraction limits what can be assessed; distinguish information unavailable to this review from information not collected by the study.

## Tracker representation

Use one principal claim per row. `n` holds the study sample and `analysis_denominator` the outcome-specific analyzed sample; record enrolled/treated/followed counts, censoring, withdrawals, baseline/comparator details, and cohort overlap in `notes`, `limitations`, or the accompanying report when they do not have dedicated fields.

Use `qualitative` for an observed/described finding without extractable endpoint counts or measurements; use `not_reported` when the outcome itself is unavailable in the reviewed material (for example, EV-016). Both require `outcome_numerator=NA`, a positive known analyzed denominator no greater than known `n` or `not reported`, an explicit `outcome_timepoint` (including an unknown-time note), and blank value/unit and baseline fields. Explain the unavailable quantitative result in notes or limitations; for `qualitative`, also explicitly identify the observed/qualitative finding. The validator checks these structural rules, not whether the source supports the claim; that remains a reviewer responsibility.

## Worked examples from the tracker

1. **Allogeneic donor-islet infusion (Lantidra; EV-017–EV-022; [S13 prescribing information](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=24610d9f-0c5a-4f55-93b3-d456300bfd5d)).** Two pooled open-label single-arm studies in selected adults report insulin independence at some point for 25/30 treated participants and for more than five years for 9/30; they also report serious adverse reactions in 27/30 and loss of islet-cell function after immunosuppression discontinuation in 8/30. These are participant counts, not independent cohorts or event rates per year. Follow-up ranged from 0.3 to 14.5 years and infusion exposure varied; the longest follow-up does not apply to all 30. Systemic immunosuppression remained a co-intervention. Baseline C-peptide, HbA1c/CGM changes, and endpoint-specific withdrawal/censoring details are not extracted in these tracker rows; this does not mean they are absent from the source. With no concurrent comparator and variable exposure, the E3, 3/5-confidence claims support reported outcomes in this selected cohort, not a comparative causal estimate or cure.
2. **Gene-edited hypoimmune islets in humanized mice (EV-033; [S16, Hu et al.](https://doi.org/10.1126/scitranslmed.adg5794)).** The accessible abstract describes survival, engraftment, and diabetes amelioration without immunosuppression in the described models, but sample sizes, observation durations, and endpoint-specific denominators were unavailable to this review. Quantitative baseline/comparator results and a comprehensive harms assessment cannot be extracted from this record. Represent the finding as `qualitative`, with `n=not reported`, `outcome_numerator=NA`, `analysis_denominator=not reported`, blank measurement fields, and an explicit unknown-time note. Do not infer a responder percentage. EV-034 reports another experiment in the same source, not independent replication. The tracker records E2 and 2/5 confidence; abstract-only access, model limitations, and Sana affiliation constrain interpretation. This is observed animal evidence, not human efficacy, safety, or cure evidence.

## Reviewer checklist

Before accepting a claim, check each item:

- [ ] **Source and design:** Is the primary/authoritative source accessible, and does the design support the wording (association versus causation)?
- [ ] **Population and cohort:** Are model/population, eligibility, modality, baseline, comparator, sample, and co-interventions stated? Are duplicate or overlapping reports identified rather than counted as independent cohorts?
- [ ] **Denominators:** Are enrolled, treated, outcome-analyzed, and followed counts distinguished at each time point? Do numerators match the stated denominator? Are withdrawals, censoring, and missing data visible?
- [ ] **Endpoint hierarchy:** Is the claim tied to the prespecified endpoint and definition? Are secondary, post hoc, composite, and surrogate endpoints labeled? Does it avoid inflating C-peptide, graft survival, HbA1c, or time-in-range into insulin independence or cure?
- [ ] **Follow-up and durability:** Is the observation window explicit and at least 12 months for claims beyond early feasibility, or clearly labeled shorter-term? Is multi-year evidence available before using “durable”?
- [ ] **Harms and burden:** Are adverse events, immunosuppression, infection, malignancy, procedures/device risks, discontinuations, and treatment/follow-up burden reported, including important missing safety data?
- [ ] **Registry status:** Before presenting status as current, was the official registry rechecked for this review, with `status_checked`, last-posted, and last-verified dates distinguished? If access fails or the record is old, is the status qualified as a dated/unverified snapshot rather than silently refreshed? Registry status is not efficacy evidence.
- [ ] **Conflicts and completeness:** Are funding and relevant author conflicts disclosed? Are null, contradictory, and unfavorable findings included?
- [ ] **Claim language:** Does the wording distinguish prevention/delay, remission, insulin independence, and cure; qualify short follow-up and uncertainty; and avoid an unqualified “cure” claim or implying project thresholds are consensus?

Use the evidence framework's claim-specific confidence score and rationale after completing the checklist. A completed checklist does not make weak or incomplete evidence conclusive.
