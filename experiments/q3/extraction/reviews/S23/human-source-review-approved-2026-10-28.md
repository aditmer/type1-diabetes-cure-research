# S23 / Q3-S23 — limited primary human source-review approval (2026-10-28)

**Decision: APPROVED for 40 specifically supported source fields and one documented source conflict; not approval of all 121 fields.**

- **Human reviewer:** `@aditmer`, who reports personally inspecting the publisher source.
- **Decision date:** 2026-10-28 (America/New_York).
- **Human authorization relay:** [Issue #52, approval statement](https://github.com/aditmer/type1-diabetes-cure-research/issues/52#issuecomment-6481495840). The user explicitly replied "I approve" to a request to approve only the limited personally reviewed S23 facts, preserve discrepancies, and enter defensible fields into GitHub.
- **Recorded mechanically by:** assistant through the connected GitHub account; neither this document nor the Issue #52 comment was separately signed by the human in GitHub, and the assistant does not claim to have performed an authorized human source review.
- **Frozen source:** `S23 / Q3-S23`, `publisher-pdf-human-copy-2026-10-23`, `pec-s23-target` / `pec-s23-site-all` (15-person Vancouver PEC-Direct site population), DOI `10.1016/j.stem.2021.10.003`, NCT03163511.
- **Publisher locator:** main PDF (approved human copy; manifest SHA-256 `0c7bf5e8f66a3b44992522b7911a7bd39b473a6b55d47cb8e6a2f81eed45e3f2`) and its independently accessible `mmc1.pdf` supplement. No new archive hash or editorial-version sequence verification claimed. No publisher PDF, private download link, token or credential committed.
- **Reported personal review scope:** main article DOI/registration, Table 1, Results, Figures 1–3 and STAR Methods; supplement Methods S1–S7 (including CONSORT), Table S1 and Figures S1–S5. This **does not certify all pages of the full main article** or all possible original/updated versions.

## Approved typed ledger fields (40 reported)

Each of these fields has the frozen version ID, source-section/table/figure locator, reviewer/date, exactly scoped note and a field-level review-complete marker. Values are source-reported observations rather than derived efficacy claims.

- `target_enrolled`: true
- `population_identified`: true
- `counts.enrolled`: 15
- `counts.treated`: 15
- `counts.withdrawals`: 7
- `counts.missing_data_handling`: Analyses included data available before final withdrawal; mixed-effects longitudinal analyses used available repeated measurements. Some week-26/week-52 tests or visits were missed or incomplete, and seven participant...
- `identity.population`: Single Vancouver site cohort of 15 VC-02-implanted participants with type 1 diabetes; 18 screened and 3 ineligible, 15 allocated, treated and included in the reported overall analysis.
- `identity.disease_stage`: Type 1 diabetes established for 10–54 years in the 15 treated participants; supplemental inclusion criterion required at least five years since T1D diagnosis.
- `identity.eligibility`: Inclusion required established T1D, optimized insulin therapy, and documented hypoglycemia unawareness or substantial glycemic lability. Relevant prior-year glucose/hypoglycemia criterion is disjunctive: a severe hypo...
- `identity.intervention`: ViaCyte PEC-01 human pluripotent stem-cell-derived pancreatic endoderm progenitors implanted in vascularizing, non-immunoprotective VC-02 (PEC-Direct) polytetrafluoroethylene macroencapsulation devices, intended to de...
- `identity.dose`: Approved manuscript describes approximately 250–500 million PEC-01 cells per implanted participant. Device counts in supplement Methods S4: patients 01–14 received 2–4 larger VC-02-300 devices and six VC-02-20 sentine...
- `identity.design`: Vancouver single-site phase 1/2 clinical trial report of NCT03163511, following implanted participants with serial biological and clinical assessments through scheduled visits including weeks 26 and 52, with incomplet...
- `identity.baseline_context`: Table 1 lists 15 participants aged 36–58 years, 7 male and 8 female, T1D duration 10–54 years; 11 used insulin pumps and 4 multiple daily injections.
- `identity.mapping`: The relevant target is all 15 Vancouver implanted participants. Table 1 has six Shapiro et al. E-series ID cross-references; these are candidate linkage clues only and do not prove matching participant identities, dir...
- `identity.linkage`: uncertain
- `burden.co_interventions`: Per supplement Methods S3, methylprednisolone was administered around implantation (days -2 to +2); etanercept was given at implantation and postoperatively. Oral prednisone was assigned to patients 09 and 11, not 08 ...
- `burden.exposure`: The treatment required general anesthesia and surgically created subcutaneous pockets (forearm and/or abdominal wall) for cell-containing VC-02 devices; their vascularizing portals permit host vessel ingrowth but not ...
- `burden.immunosuppression`: Non-immunoprotective VC-02 required systemic immunosuppression: ATG induction (total approximately 6 mg/kg), tacrolimus and mycophenolate maintenance; additional methylprednisolone and etanercept around implantation. ...
- `burden.repeat_procedures`: Methods S5 specifies serial planned device explantation at weeks 4, 12, 26 and 39, with patient-specific removals and restrictions. Histology assessed 14 explanted devices from patients 01–10 at 35–57 weeks; this devi...
- `treatment.first_administration`: Implantation of VC-02 devices under general anesthesia at study Day 0, with baseline measurements prior to implantation.
- `treatment.source_anchors`: Day 0 is first cell-containing VC-02 implantation. Supplemental Methods S5 specifies baseline week -3 (±1 week), MMTT week 26 (±1 week) and week 52 (±1 week), plus serial fasting C-peptide and simple meal challenges a...
- `insulin_independence.observation`: observed
- `insulin_independence.value`: 0
- `insulin_independence.definition`: The source explicitly reports that no participant became independent of exogenous insulin in the observed study follow-up; one participant had a >50% insulin-dose reduction within year one, which is not insulin indepe...
- `insulin_independence.attribution`: target
- `insulin_independence.analysis_population`: uncertain
- `insulin_dose.observation`: observed
- `insulin_dose.attribution`: target
- `insulin_dose.summary`: Mixed-effects longitudinal analysis reported lower insulin requirements after implantation (B = -0.220, SE = 0.03, t(186.3) = -7.25, p < 0.001), remaining significant after exclusion of the post-implant steroid-relate...
- `hba1c.observation`: observed
- `hba1c.attribution`: target
- `hba1c.summary`: Mean HbA1c remained below 7% across visits and was stable; mixed-effects longitudinal slope B = -0.0055, p = 0.193, without statistically significant improvement. A separately verified numeric baseline-to-week-52 mean...
- `cgm.observation`: observed
- `cgm.attribution`: target
- `cgm.range`: CGM: time below range <3.9 mmol/L, target range 3.9–10.0 mmol/L, time above range >10 mmol/L.
- `cgm.summary`: Mixed-effects models: time in target range increased (B = 0.666, p < 0.001); time above target decreased (B = -0.699, p < 0.001); time below 3.9 mmol/L did not significantly change (B = -0.004, p = 0.924). The discuss...
- `safety.population`: The entire 15-person implantation cohort was included in the safety narrative; all participants reported at least one adverse reaction during first-year reporting. Three serious adverse reactions were reported in two ...
- `safety.window`: First-year post-implantation adverse-reaction reporting window in the main Results and Supplement Table S1. Seven participants discontinued intervention; individual endpoint follow-up was incomplete or varied. This is...
- `safety.attribution`: Investigators described the three serious adverse reactions in two participants as possibly associated with immunosuppression; attribution is not proof of causality. The reviewed Results and supplement identify no dea...
- `safety.discontinuations`: Seven of the 15 discontinued intervention: five after sponsor risk-benefit assessment and two who withdrew consent in the supplement CONSORT. The Results relate two serious-event-associated withdrawals (patients 02 an...

## Independently unresolved same-version conflict: `safety.harms`

**Status `conflicting`, value null**, with two independent paper-section locators and `SOURCE_CONFLICT` reason code. Do not silently replace the main source's value or treat `conflicting` as `reported`.

- **Main article, Results safety paragraph:** first-year total 175 adverse reactions.
- **Supplement, Table S1, page 10:** parenthesized totals 175 grade 1 + 24 grade 2 + 4 grade 3 + 2 grade 4 = **205** events. The displayed unparenthesized subtotal 135 + 14 + 2 + 0 = 151 is confined to categories reported in more than one participant. Preserve both totals and the footnote, with no fabricated reconciliation.
- **Separate classification:** Three serious adverse reactions in two participants (grade-4 typhlitis and liver abscess; grade-3 parvovirus infection with aplastic anemia). Six grade 3/4 events do **not** mean six serious adverse reactions. The serious events were described as possibly immunosuppression-related, not conclusively drug- or graft-caused.
- **No zero-event substitution:** No deaths were identified in the personally reviewed sections, but the safety conflict and incomplete full-source review remain explicit.

## Corrections and conservative interpretation

1. **Device exposure:** Patient 15 received **5 VC-02-300 and 5 VC-02-20**, unlike the 2–4 larger plus 6 sentinels used for patients 01–14 (supplement Methods S4). Do not write a uniform device count.
2. **Additional prednisone:** supplement Methods S3 names **09 and 11** (not 08 and 10). Mycophenolate sodium substitution was reported for 09, 10 and 15.
3. **Hypoglycemia eligibility:** supplemental Methods S1 permits a qualifying prior severe event **or** documented CGM low glucose **or** severe lability. This does not prove all 15 had prior severe hypoglycemia.
4. **C-peptide and response:** development of meal-stimulated C-peptide is evidence consistent with endocrine graft function. Four specifically named participants exceeded 30 pM at unspecified common visit, not a single verified 4/15 fixed-week52 response rate. None reported independent of insulin; only one reported >50% dose reduction. Insulin-use and CGM model improvements cannot causally be assigned to graft output.
5. **Attrition and denominator:** 18 screened; 3 excluded; 15 implanted; five discontinued after sponsor risk-benefit review and two consent withdrawals. Main article reports two SAE-associated withdrawals; identity of that pair with CONSORT consent withdrawals is not separately adjudicated. Fifteen in overall analysis is **not** a verified denominator for each test at week 26 or week 52.
6. **Source-wide omission:** The post-implant severe hypoglycemia count was not identified in the Results/supplement personally inspected. The entire main article was not attested exhaustively reviewed; retain the unextracted source-field status instead of declaring no severe events or source-wide `unreported_in_reviewed_material`.
7. **Cohort relationships:** Table 1's six Shapiro E-series IDs are potential matching leads only; all six PEC-Direct S18/S19/S23/S20 cohort links remain `uncertain` until reviewed two-sided source-specific adjudication.

## Rights and process exception

The frozen Path B rule reserves **publisher-material inspection to the sole assigned human reviewer** (`@aditmer`), and no publisher-PDF redistribution/shared-storage right is established. The maintainer reports personally inspecting main and supplement through their own access. During the chat, they also uploaded a supplement copy and requested an assistant to check Table S1; this was **outside the approved human-only inspection restriction**. The assistant check is an AI quality-control observation, **not an authorized human review or independent replication**. This record transparently notes that exception; it does not grant permission to store or redistribute the file. Resolve any governance/rights consequences before a final G2-B acceptance.

## Remaining gate and scope

S23 has **40 `reported` fields, one `conflicting` field and 80 `not_yet_extracted` fields** out of 121. Source-content review, adjudication, and access-attempt completion remain false in the log; only the scoped field-level decisions are approved. No review status is set for material not inspected. The independent-review record remains fully pending (no separate reviewer/date/decision), and an independent S23 reviewer must obtain their **own lawful publisher access** rather than receiving a forwarded PDF. The six cohort links stay `uncertain`.

**No report-level classification, G2-B acceptance, Issue #35 / G2-C authorization, G3 or clinical-cure claim is conferred by this PR.**
