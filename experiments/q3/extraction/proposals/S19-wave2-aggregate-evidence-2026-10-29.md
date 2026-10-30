# S19 Wave 2: hash-bound aggregate evidence

**20 proposed field values and three separately scoped C-peptide observations;
no authoritative promotion.** Issues #34 and #56. Baseline:
`7432cd3cb3bc1075706b12c50ab7156bc71ddb8c`. The
[structured proposal](S19-wave2-aggregate-evidence-2026-10-29.json) supplies
typed values, exact XML paragraph locators, scope and limitations. All 121
authoritative S19 fields remain pending; this is not a replacement ledger.

## New retrieval versus prior candidates

Europe PMC GET on **2026-10-29 at 21:18:10 UTC** returned HTTP 200,
**122,548 bytes**, SHA-256
`3e14ef3dcb7fd0c13a9326976c01511356426b8004dc7a9b78b3ffb2e2c68839`.
Length/hash matched the approved manifest **before narrative inspection**.
XML DOI `10.1038/s41587-023-02055-5` and PMCID `PMC11471599` match.
There is **no embedded `pmcid-ver`**: `PMC11471599.1` remains bound through
the accepted manifest hash/archive mapping, not an invented editorial-version
claim. Fresh public XML does **not** recover the unavailable original private
OneDrive restore bytes/verifier or upgrade the historical attestation.

The prior packet's four leads (full ten-person group, month-6 4/10,
month-12 threshold 3/10, and two people with serious events) were rechecked
against these bytes. New detail includes eligibility versus observed baseline,
unit-dose estimates, protocol timing, testing method, safety scope and
planned patient-important endpoints. Prior AI notes are not human review.

Only author-narrative aggregate facts and reference identities support the
proposal. No raw source, participant table, individual trajectory, figure or
supplement is committed. Tables/figures and rights-pending third-party items
were not inspected. A narrative cross-reference is not inspection of its
target. MOESM1-3 remain unreviewed; **MOESM4 remains excluded**.

## Concrete source decisions

All locators below are within `PMC11471599.1`.

| Domain | Proposed finding | Exact locator and boundary |
|---|---|---|
| Population | Entire optimized 10-person cadre, enrolled August 2020-October 2021; 10 enrolled/treated | Sec9/Par31, Par33; not all registry Cohort 2 and not only responders |
| Baseline | Basal and 90-minute MMTT C-peptide below 0.03 nmol/L in all ten | Sec3/Par8; below LOD is not zero, and differs from eligibility cutoff 0.07 |
| Dose | Approximately 75 million cells/dose-finding unit, 7 million/sentinel; reported mean initial dose 14 million cells/kg | Sec11/Par42, Sec7/Par29; no derived individual or common total dose |
| Immunosuppression | ATG induction adjusted to lymphocyte counts, tacrolimus and mycophenolate maintenance | Sec10/Par38, Sec3/Par8; duration/adherence not established |
| First administration | Subcutaneous cell-containing implantation two days after ATG start | Sec10/Par38; no invented dates or repeat-administration history |
| Testing | Baseline four weeks before transplant, then three-month intervals; selected 90-minute MMTT sample | Sec10/Par39-40; method is not visit completeness |
| Month-3 graft function | 5/10 above LOD 0.03 nmol/L | Sec4/Par10, Sec3/Par8; surrogate, not insulin independence |
| Month-6 graft function | 4/10 above LOD, primary endpoint | Sec4/Par10, Sec9/Par33; month 6 and protocol week 26 retained as printed |
| Secondary graft function | 3/10 above 0.07 nmol/L sustained until month 12 | Sec4/Par10, Sec7/Par23 aggregate summary; not ten confirmed complete month-12 records |
| Patient-important endpoints | Insulin dose, insulin independence, CGM bands and hypoglycemic events listed in protocol | Sec9/Par35-37; **planned**, no observed result/denominator inferred; hypoglycemic events are not automatically severe events |
| Harms | Two people with treatment-emergent serious events, one attributed to surgery and one to immunosuppression | Sec3/Par9; affected people are not a separately enumerated total event count |
| Withdrawal | No TEAE led to withdrawal | Sec3/Par9; not zero all-cause withdrawal or complete follow-up |

Protocol maximum secondary follow-up is **104 weeks** (Sec9/Par33).
It is not actual full-cadre follow-up. No common month-12 clinical denominator
is derived from the treated population or C-peptide responder counts.
Patient-important numeric outcomes, visit coverage, censoring and missing-data
handling remain **not established in this permitted aggregate review scope**,
not adjudicated source omissions.

**Safety scope requires reconciliation:** Sec10/Par38 reports no adverse events
during/after interventions, whereas Sec3/Par9 attributes a serious event to
surgery. Both locators remain visible. Different timing or scope might explain
the wording; this proposal neither silently corrects it nor prematurely marks
the authoritative field conflicting. The safety exposure window remains pending.

Sec9/Par33 and references CR17/18 identify the S18/S23 publications as earlier
groups. Chronology and device differences do not prove disjoint people or
exclude re-enrollment. All six PEC-Direct relationships remain uncertain.

## Smallest consolidated human batch

1. Verify/approve/reject the 20 proposed fields and three aggregate surrogate
   observations together against the exact hash-bound representation. Confirm
   the full ten-person target, endpoint-specific denominator basis, LOD versus
   eligibility cutoff, actual timing and first-cell anchor. Do not transfer
   C-peptide results into insulin independence or other clinical domains.
2. Resolve safety wording using both locators, actual safety exposure,
   all-cause attrition and clinical endpoint coverage from permitted aggregate
   material. Keep unresolved fields pending; no-event-related withdrawal is
   not proof of no withdrawals.
3. Confirm item-level rights and identity before any MOESM1-3 or third-party
   inspection, and retain the excluded MOESM4 boundary. Explicitly acknowledge
   the historical restore limitation if original verifier evidence cannot be
   lawfully recovered. A fresh public hash match is not that recovery.

The JSON records a separate disposition and lawful next step for all eight
access/provenance/evidence blockers. No source-content completion, adjudication
completion, reviewer signoff, real-source classification or G2-B acceptance is
claimed. Machine tests verify shape and safeguards, not scientific truth.

Attribution: Keymeulen, De Groot, Jacobs-Tulleneers-Thevissen et al.,
*Nature Biotechnology* (2023), DOI `10.1038/s41587-023-02055-5`;
The Authors 2023, CC BY 4.0 with third-party exceptions. Factual paraphrases
only; no figure/table reproduction.
