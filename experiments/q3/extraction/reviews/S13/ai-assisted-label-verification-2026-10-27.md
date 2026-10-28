# S13 AI-assisted DailyMed v3 verification — 2026-10-27

**Disposition: candidate verification only; no authoritative ledger values changed.**
This is not an authorized human review, field adjudication, independent review,
or G2-B acceptance. The S13 ledger remains pending.

## Source identity and scope

- Frozen source: `SPL-v3-a3163e14-0404-4e27-884b-f6f9f7f695bc`, target
  `lantidra-treated`, subcohort `lantidra-pooled-all`.
- Retrieved the official [DailyMed archival ZIP 940595](https://dailymed.nlm.nih.gov/dailymed/getArchivalFile.cfm?archive_id=940595).
  The ZIP was 327,121 bytes, SHA-256
  `db33f66f3b6e3433d0c47667a0e367f4e1b464cc2875e023e950f1f049f1fd33`.
  The XML member `a3163e14-0404-4e27-884b-f6f9f7f695bc.xml` was 168,862 bytes,
  SHA-256 `696ebb05a528236ea6077c912785e94cf103aa4d29fa61bacab3282e65307fd4`;
  both match `source-manifest.csv`.
- Checked the candidate locators in SPL Sections 2.1, 5.1, 6.1 and 14. The
  source archive is not included in this repository. NLM/DailyMed terms are
  recorded in the manifest; this note contains factual annotations only and
  does not assert blanket redistribution rights.

## Candidate findings checked against v3

- Section 14 describes 30 treated participants pooled across Study 1 and Study
  2. It reports 11 participants with one infusion, 12 with two and 7 with
  three. Keep all 30 and every repeat infusion in the frozen target.
- The label reports insulin independence at any time for 25 participants and
  no days of independence for 5. This is not a fixed day-365 numerator or
  denominator.
- The source reports duration counts of 4, 12 and 9, alongside 13.3%, 36.7%
  and 33.3%. The count/percentage pairs do not reconcile to either 25 or 30;
  preserve the source statements and flag them for human review without
  recalculating or repairing the label.
- Section 6.1 reports variable follow-up of 0.3–14.5 years after first
  infusion (mean 3 ± 3.7 years). Section 14 and Figure 1 use first infusion as
  time zero and mark repeat infusions. Variable maximum follow-up does not
  establish a fixed month-12/day-365/week-52 outcome assessment.
- Sections 5.1 and 14 identify concomitant immunosuppression and the
  exenatide co-intervention. Table 3's study-specific counts and percentages
  still require line-by-line human review.
- Section 6.1 reports serious reactions, deaths, severe and life-threatening
  reactions with differing definitions and follow-up windows. Retain these
  unfavorable safety facts with their source denominators and attribution;
  do not infer treatment causality beyond the label.

The existing [candidate extraction](../../candidates/S13-candidates.json)
holds field-level values, exact locators and limitations. The existing
[human-review packet](../../candidates/S13-reviewer-packet.md) identifies the
reviewable fields and remaining decisions. Its unresolved count remains 101;
omission from the candidate file is not a reviewed absence.

## Human action still required

Confirm the all-treated pooled target, each endpoint's denominator and timing,
the displayed duration percentages, Table 3 values, co-interventions,
attrition, and safety attribution. Record actual reviewer identity/date and
scope. Do not promote any field from this AI check alone.
