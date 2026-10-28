# Q3 G2-B independent-review and acceptance handoff

**Decision requested: defer G2-B acceptance.** This is a prepared handoff, not
an independent review, formal acceptance, or authorization to run G2-C.

## Current evidence state

- Eight frozen reports remain in scope: S13, S18, S19, S23, S20, S17, S4
  and S9. **Update 2026-10-28:** [merged PR #49](https://github.com/aditmer/type1-diabetes-cure-research/pull/49)
  recorded the maintainer's primary manual S17 checklist review and ten
  specifically approved `reported` fields. All **111 remaining S17 fields**,
  and **958 of 968 total fields**, stay `not_yet_extracted`.
  S17 source-completion/adjudication and all independent-review flags remain
  pending. No report classification or paired analysis has been run.
- AI-assisted evidence checks are prepared for S13 and S17; partial main-text
  checks and rights limits are recorded for S18 and S19. S20, S4 and S9 retain
  their existing source-specific human-review packets, with the retrieval
  limit summarized in `remaining-source-check-status-2026-10-27.md`.
- S23 has a Path B human-only packet. Only `@aditmer` has the recorded
  individual publisher access; no additional reviewer access or shared-PDF
  right is established.
- S18 `mmc2.xlsx` remains excluded. S19 `MOESM4` remains unreviewed and
  excluded from this work. No omission is inferred from either source.
- The six PEC-Direct cohort links remain `uncertain`.

## Independent reviewer checklist

The independent reviewer must be distinct from each primary source reviewer
and must document actual identity, date, scope, evidence checked and a decision
for each report and cohort link.

1. Reconcile each report/source-version/target/subcohort tuple to the frozen
   manifest and rules without substituting a current API record for a frozen
   history version.
2. Inspect the source-specific AI notes and candidate locators. Challenge
   version identity, exact selectors, population boundaries, endpoint
   definitions, source denominators, visit windows, first-treatment anchors,
   safety attribution and rights restrictions.
3. **Independently** verify the ten primary-human-reviewed S17 fields
   against approved v13 material and [the actual review record](S17/human-source-review-approved-2026-10-28.md).
   The human primary review was completed for those ten fields only;
   retain the other 111 fields as unresolved. Separate planned Cohort 2
   from Cohort 1 results and scrutinize the revised planned dose.
4. Verify the entire S13 all-treated pool and reconcile source-displayed
   duration/Table 3 values without correcting the source.
5. Review S18 without accessing or inferring from `mmc2.xlsx`; review S19
   without accessing or inferring from `MOESM4`, and preserve third-party
   reuse exceptions.
6. Obtain the authorized S23 Path B review and a lawful individual-access
   path for any independent reviewer before marking that report independently
   reviewed. Do not copy or share the publisher PDF.
7. Verify S20, S4 and S9 against their exact approved history records; retain
   planned/unposted outcomes as plans and keep cohorts/endpoints separate.
8. Confirm `cohort-links.csv` still contains all six conservative PEC-Direct
   relationships and that no report or source has been silently retargeted.
9. Confirm `tracker-corrections.csv` remains separate from source facts and
   no authoritative source/evidence/trial tracker is modified by this handoff.

## Acceptance record — leave pending until independently completed

| Required record | Status |
|---|---|
| Authorized primary source review for all eight reports | **Partial:** S17 ten-field primary review recorded; seven other sources and 111 S17 fields remain pending |
| Field-level human decisions and source-review logs | **Partial:** ten S17 source facts accepted in ledger; 958 other fields unresolved |
| Independent reviewer identity, date, scope and decision | Pending |
| Independent review of all six cohort links | Pending |
| Explicit G2-B acceptance by authorized maintainer | Pending |
| G2-C / Issue #35 authorization | **Blocked pending the above** |

After the human and independent reviews are complete, the authorized maintainer
must record an explicit `accept`, `revise`, `reject`, or `defer` decision and
its rationale. Only an explicit acceptance may satisfy the G2-B handoff. This
document does not make that decision or authorize real-source classification.
