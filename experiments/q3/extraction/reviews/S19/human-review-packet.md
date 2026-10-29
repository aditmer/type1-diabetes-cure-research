# S19 human-review packet

- **Review status:** pending; the AI check covered the main article only.
- **Report/target:** Q3-S19; all 10 recipients in the frozen optimized group,
  not only the responder subgroup.
- **Approved source:** `PMC11471599.1`, DOI `10.1038/s41587-023-02055-5`.
- **AI check:** [`ai-assisted-evidence-check-2026-10-27.md`](ai-assisted-evidence-check-2026-10-27.md).
- **Approved supplement directions:** MOESM1, MOESM2 and MOESM3, subject to
  attribution and third-party exceptions. They were not retrieved in the AI
  check; record their review only after actual inspection.
- **Excluded supplement:** **MOESM4 was not reviewed**. Do not retrieve,
  inspect, upload, reconstruct or infer from it. Do not mark fields unreported
  on the basis of this exclusion.
- **Restore limitation:** the public XML was freshly re-fetched with the
  manifest SHA-256, but the original private OneDrive restore bytes and
  verifier output remain unavailable for independent reinspection.

## Human verification checklist

1. Confirm the complete 10-person target and source-population mapping.
2. Verify intervention/device configuration, dose, MMTT definition and
   baseline, month-6 primary endpoint, month-12 secondary thresholds, and
   visit-specific denominators.
3. Verify insulin dose, HbA1c and CGM measures without using a responder-only
   denominator for the frozen target.
4. Reconcile withdrawals, unavailable visits and censoring; distinguish
   follow-up duration from endpoint observation windows.
5. Verify immunosuppression, co-interventions, repeat exposures, harms,
   seriousness, attribution and discontinuations.
6. Preserve CC BY 4.0 attribution and third-party exceptions. Item-level reuse
   review remains pending.
7. Keep all six PEC-Direct population relationships uncertain unless exact
   source evidence supports a direction.

Record actual reviewer identity/date, source components and sections examined,
exact locators, field decisions and unresolved items. All 121 S19 fields remain
`not_yet_extracted`; the AI note does not establish a human review or an
omission status.

## Aggregate candidate preparation — 2026-10-29

These are **unverified candidate leads**, not human source decisions or
authoritative ledger values. The frozen target remains all 10 recipients in
the optimized group (`Q3-S19`, `pec-s19-optimized-all`), not a responder-only
subset.

| Candidate lead | Exact main-article locator | Scope and unresolved check |
|---|---|---|
| The optimized group is described as 10 patients. | `PMC11471599.1`, Results → Overview of trial design. | Confirm the complete 10-person target and the source-to-registry mapping; do not identify participants across reports. |
| The article describes detectable MMTT-induced C-peptide in 4/10 recipients at month 6 as the primary implant-function endpoint. | `PMC11471599.1`, Results → Meal-stimulated plasma C-peptide in recipients of PEC-Direct, month-6 summary paragraph. | Verify endpoint wording, denominator, LOD and visit window. This is a graft-function surrogate, not insulin independence. |
| The article describes 3/10 recipients above the stated 0.07 nmol/L C-peptide threshold through month 12. | `PMC11471599.1`, Results → Meal-stimulated plasma C-peptide in recipients of PEC-Direct, month-12 secondary-endpoint summary. | Verify threshold and visit-specific scope; do not convert this to a fixed-horizon patient-important outcome. |
| Two patients are reported with treatment-emergent serious adverse events; the article attributes one to surgery and one to protocol-specified immunosuppression. | `PMC11471599.1`, Results → Overview of trial design, treatment-emergent adverse-event paragraph. | Verify event counts and source-attributed explanations; do not infer additional causality or use excluded supplements. |

**Provenance and preparation scope.** Approved source ID/version: S19 /
`PMC11471599.1`, DOI `10.1038/s41587-023-02055-5`; approved manifest XML
SHA-256 `3e14ef3dcb7fd0c13a9326976c01511356426b8004dc7a9b78b3ffb2e2c68839`.
That hash and the historical-restore limitation are copied from the frozen
manifest and were not recalculated in this preparation. The candidate locators
refer only to the main article's aggregate narrative; no excluded supplement
content or third-party figure/table material is used. MOESM4 remains excluded
and unreviewed. CC BY 4.0 attribution and item-level third-party exceptions
remain in force.

This preparation reviewed the issue requirements, manifest, and existing
review packet and consulted the public main-article presentation; it did not
reinspect the private restore or establish that the presentation is byte-
identical to the approved XML. No field was promoted, no reviewer identity or
decision date was added, and all 121 authoritative fields remain pending.
Independent review remains pending.

**Still unresolved:** exact approved-XML verification for these candidate
leads; complete endpoint-specific denominators and visit coverage; attrition
and censoring; treatment exposure and co-interventions; item-level rights
review; and any permitted evidence outside the cited main-article passages.
Do not use these candidates to resolve the S18/S19/S20 cohort relationship or
to change `cohort-links.csv`.
