# S18 AI-assisted evidence check — 2026-10-27

**Disposition: partial main-article check only; no authoritative ledger values changed.**
Human source review, complete field adjudication, independent review and
G2-B acceptance remain pending.

## Source and permitted review scope

- Frozen source: `PMC8714853.1`, report `Q3-S18`, target `pec-s18-target`,
  subcohort `pec-s18-all`.
- Retrieved the [Europe PMC full-text XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8714853/fullTextXML)
  for the [PMC version page](https://pmc.ncbi.nlm.nih.gov/articles/PMC8714853.1/)
  at the manifest's official URL. The
  114,747-byte response SHA-256
  `2c33d10d93cd399fadef190447f2ea5778625c476405f3e6cb011eb94e792433` matches
  the approved source-manifest record. The XML identifies PMID 35028608, DOI
  `10.1016/j.xcrm.2021.100466`, and version `PMC8714853.1`.
- Inspected the main article's Study Design and Subject Details, Results,
  Safety Measures, Primary Efficacy Endpoint, Secondary Efficacy Measures,
  Limitations, Table 1 and Tables 2–3 in the article XML. This is a partial
  automated check, not a complete authorized review of every allowed source
  component.
- **`mmc2.xlsx` was not retrieved, opened, uploaded, reconstructed or
  inferred from.** The approved exclusion remains in force. `mmc1` and `mmc3`
  were also not retrieved in this check; do not infer that their contents
  omit anything. In particular, the article points secondary-measure numeric
  data to Table S1 in the excluded material.
- The article is identified as CC BY-NC-ND 4.0. This note records factual
  annotations only; it does not reproduce protected expression, figures or
  tables and does not claim broader reuse rights.

## Candidate facts checked in the main article

- The described publication population is 17 consecutive Cohort 2 participants
  in the ongoing VC-02 study, not only the C-peptide-positive subgroup. The
  article states baseline C-peptide was below its assay quantitation limit.
- The source describes first-in-human, open-label Phase 1/2 study design and
  reports that all 17 participants received the same immunosuppression
  regimen. Cohort 2 is the efficacy cohort; keep Cohort 1 separate.
- The primary endpoint is stimulated C-peptide after MMTT. The article reports
  6/17 with detectable stimulated C-peptide at varying follow-up visits, not a
  patient-important insulin-independence result. Table 3 includes visits at
  6, 9, 12 months and later; do not collapse these into one day-365 value.
- The article's safety section reports 297 adverse events in the first 12
  months, classified by severity, and 10 serious events in 6 participants.
  Preserve event counts, participant counts, attribution and time windows as
  distinct facts.
- The article says it found no statistically significant pre/post differences
  in secondary glycemic measures, with numeric data directed to Table S1.
  Because the referenced participant-level supplement is excluded, this check
  does not validate those numeric values or make an omission finding.
- The limitations section says no statistically significant measurable
  clinical benefit had yet been observed in this pilot. Do not turn the
  surrogate C-peptide findings into a cure or a demonstrated patient-important
  benefit.

## Human reviewer checklist

1. Confirm the full fixed 17-person target and separate any C-peptide-based
   analysis subset from the report population.
2. Review only approved components and record what was actually examined.
   Never access or infer from `mmc2.xlsx`.
3. Verify endpoint definitions, denominator, each follow-up visit, the
   Table S1 cross-reference, adverse-event counts/windows and
   immunosuppression.
4. Leave all fields that require the excluded supplement or unreviewed
   components unresolved; do not use `unreported_in_reviewed_material`.

This packet is not a source-content completion attestation. The independent
reviewer must assess the candidate facts and the exclusion boundary separately.
