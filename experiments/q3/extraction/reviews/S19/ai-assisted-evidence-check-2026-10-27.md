# S19 AI-assisted evidence check — 2026-10-27

**Disposition: main-article check only; no authoritative ledger values changed.**
Human source review, complete field adjudication, independent review and
G2-B acceptance remain pending.

## Source and rights boundary

- Frozen source: `PMC11471599.1`, report `Q3-S19`, target `pec-s19-target`,
  subcohort `pec-s19-optimized-all`.
- A fresh [Europe PMC XML retrieval](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11471599/fullTextXML)
  for the [PMC version page](https://pmc.ncbi.nlm.nih.gov/articles/PMC11471599.1/)
  returned 122,548 bytes with SHA-256
  `3e14ef3dcb7fd0c13a9326976c01511356426b8004dc7a9b78b3ffb2e2c68839`, matching
  the public manifest's source hash and the accepted historical restore
  record. This re-fetch reproduces the public XML bytes; it does not recreate
  the unavailable original OneDrive restore artifacts or its verifier output.
- The main article states CC BY 4.0 with third-party-material exceptions.
  Item-level third-party reuse review remains pending. This packet contains
  factual annotations and source locators only, not article text or figures.
- **MOESM4 was not retrieved or inspected.** Do not cite, summarize, upload,
  reconstruct, or infer from it. MOESM1–3 were not retrieved in this check;
  their contents remain unreviewed. Do not infer omissions from them.

## Candidate facts checked in the main article

- The frozen report target is the full optimized group of 10 recipients, not
  the three-person responder subgroup. The Results section describes
  baseline-depleted recipients and treatment with PEC-Direct under
  immunosuppression.
- The main article describes a first-in-human, open-label Phase 1/2 study.
  It identifies anti-thymocyte globulin induction and mycophenolate mofetil
  plus tacrolimus maintenance. Verify detailed regimen and co-interventions
  against approved, reviewed components before ledger entry.
- The primary endpoint was MMTT-stimulated C-peptide above the detection limit
  at month 6. The paper reports 4/10 meeting this endpoint; 3/10 met the
  secondary threshold above 0.07 nmol/L through month 12. These are graft
  function endpoints, not insulin independence.
- The article reports glucose-control improvements in three of the ten
  recipients from month 6 onward, with best reported time-in-range of 85% at
  month 12 in one case. Keep all 10 as the fixed target and retain
  endpoint-specific denominators and visits.
- The Results section reports two treatment-emergent serious events, one
  attributed to the surgical procedure and one to immunosuppression; no
  treatment-emergent events led to study withdrawal. The article's case-level
  outcome table marks some later visits unavailable. Reconcile follow-up and
  attrition using the full permitted material before ledger decisions.
- S18, S19, S23 and S20 all relate to PEC-Direct/NCT03163511, but program
  identity is not participant identity. Keep the frozen S19 cohort links
  `uncertain`; do not transfer endpoint values among reports.

The numeric claims above are candidates for human verification, not accepted
ledger entries. Confirm the target population, measurement definitions,
endpoint-specific denominators, MMTT visits, CGM windows, insulin dosing,
withdrawal handling, safety windows and third-party exceptions.

## Human reviewer checklist

1. Review the full 10-person optimized target, not only responders.
2. Examine only the approved source components, preserve CC BY 4.0 attribution
   and third-party exceptions, and do not access MOESM4.
3. Resolve the table-level denominators, follow-up/withdrawal status, endpoint
   anchors and safety attribution before applying field statuses.
4. Keep all six PEC-Direct relationships unresolved unless both approved
   sources and exact population locators support a direction.
