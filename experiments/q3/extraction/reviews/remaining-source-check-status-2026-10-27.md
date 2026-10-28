# Remaining Q3 source-check status — 2026-10-27

This note extends the existing S20, S4 and S9 candidate/reviewer packets. It
does not add authoritative source facts. Their official history locators were
approved at G1, but the version-specific internal JSON endpoints returned HTTP
403 during this check; current registry API snapshots are not substitutes for
the frozen historical records. Candidate values remain unadjudicated.

## S20 / Q3-S20 — PEC-Direct Registry Cohort 2

- Frozen source: `NCT03163511-history-v20`, target `pec-registry-cohort2`.
- Existing packet: [`S20 human-review packet`](../candidates/S20-reviewer-packet.md).
- Candidate distinctions that must survive review: Cohort 2 Started=47 is not
  the registry's overall enrollment=49 or a treated denominator; C-peptide
  AUC is a Week-26 surrogate with N=42; safety, windows and events remain
  Cohort-specific; “Hypoglycemia” is not automatically the frozen severe-
  hypoglycemia endpoint.
- Six PEC-Direct cohort links remain `uncertain`. Registry and publication
  identifiers alone do not establish participant identity.

## S4 / Q3-S4 — VX-880 Parts A/B/C

- Frozen source: `NCT04786262-history-v32`, target `vx880-parts-abc`.
- Existing packet: [`S4 human-review packet`](../candidates/S4-reviewer-packet.md).
- Candidate distinctions that must survive review: exclude VX-017 Part D;
  preserve the title/structured-phase discrepancy; enrollment 57 is estimated
  for the mixed master protocol; planned outcomes are not observations; and
  `Day 90`, “one year after infusion” and “one year after insulin-independence
  onset” are different anchors.

## S9 / Q3-S9 — VX-264

- Frozen source: `NCT05791201-history-v26`, target `vx264-all-parts`.
- Existing packet: [`S9 human-review packet`](../candidates/S9-reviewer-packet.md).
- Candidate distinctions that must survive review: overall enrollment 7 does
  not establish treated or endpoint counts; Part B C-peptide is planned through
  Day 90; planned adverse-event follow-up is not a results record; and absence
  of a results module is not evidence that no harms occurred.

The field-level locators and human questions remain in the candidate JSON and
the three existing packets. No reviewed-omission status, source-content
completion, reviewer identity or date is set by this note.
