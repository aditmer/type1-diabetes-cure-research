# Q3 G2-B human adjudication queue

**Status (2026-10-28): partial S17 and S13 primary human reviews recorded.**
In [merged PR #49](https://github.com/aditmer/type1-diabetes-cure-research/pull/49),
the maintainer `@aditmer` reported manual S17 checklist review and approved
**10 of its 121 source fields**, including revised planned dose with VC-01-20
sentinel units. Those ten fields are `reported` and the remaining **111 S17
fields** remain `not_yet_extracted`.
See the [dated human primary review](reviews/S17/human-source-review-approved-2026-10-28.md).
Neither S17 full-source completion nor independent review or G2-B acceptance
has occurred.

The maintainer also approved 14 specific S13 fields after personally
reviewing DailyMed SPL v3 Sections 5.1, 6.1, and 14, including Table 3. See
the [dated S13 human source-review record](reviews/S13/human-source-review-approved-2026-10-28.md)
and [Issue #50](https://github.com/aditmer/type1-diabetes-cure-research/issues/50).
The S13 record preserves the source's duration, medication-table, and
malignancy-category discrepancies, plus the variable safety follow-up and
non-causal attribution limits. The S13 any-time 25/30 insulin-independence
finding is not promoted as a fixed-horizon result. Overall, 24 of 968 fields
are `reported`; 944 remain `not_yet_extracted`. Both source reviews are
partial, and both independent reviews remain pending.

The original preparatory evidence artifacts remain available:
[S17 AI-assisted source check](reviews/S17/ai-assisted-evidence-verification-2026-10-27.md),
[S13 archival-label verification](reviews/S13/ai-assisted-label-verification-2026-10-27.md),
[S18](reviews/S18/human-review-packet.md) and
[S19](reviews/S19/human-review-packet.md) human-review packets,
[S23 Path B packet](reviews/S23/path-b-human-review-packet.md),
[S20/S4/S9 access-limited status](reviews/remaining-source-check-status-2026-10-27.md),
and [G2-B independent-review handoff](reviews/independent-review-and-g2b-acceptance-handoff-2026-10-27.md).
The earlier AI source evidence checks remain preparation, not independent
human signoff. The other six report reviews and all six PEC-Direct cohort-link
decisions remain pending; Issue #35 stays blocked.

## Checklist required for each report

- [ ] Verify the approved source version and record the exact version-specific
  material examined.
- [ ] Record lawful access and permitted use; retain no restricted source
  content, credential, token, private download URL, or private archive path.
- [ ] Record the main article/label/registry material and each relevant
  supplement actually examined. Do not mark unreported if any relevant,
  permitted material remains unreviewed.
- [ ] Extract all applicable `field_id`s from `scripts/q3_classifier.py` into
  `reports.json`; retain typed values, original units/definitions, exact
  locators, denominator basis, source version, frozen target/subcohort,
  review scope, reason codes, and notes.
- [ ] Keep planned endpoints distinct from observed results; preserve zero,
  false, and unfavorable source values without imputation.
- [ ] Verify target-population and endpoint attribution, analysis population,
  denominator, timing and first-cell-administration anchor. Do not substitute
  another report's cohort or endpoint denominator.
- [ ] Record attrition, censoring, horizon counts, missing-data handling,
  co-interventions, immunosuppression, repeat exposure, harms, windows, and
  discontinuations where applicable.
- [ ] Record unresolved conflicts with both locators and rationale; record
  structural `not_applicable` only with explicit source evidence.
- [ ] Track source-content review, access-attempt completion, and field
  adjudication separately. An inaccessible field may have a final disposition
  only after permitted access attempts are complete; it must not be represented
  as clinical content reviewed.
- [ ] Do not mark source-content review complete while any field remains
  inaccessible or `not_yet_extracted`; do not mark adjudication complete while
  any field remains `not_yet_extracted` or has incomplete field-level review.
  Update the source review log and actual reviewer identity/date.
- [ ] Preserve independent review as pending until it occurs; when completed,
  record the independent reviewer, date, scope, and decision.
- [ ] Keep tracker corrections in `tracker-corrections.csv`, never as source
  facts. Do not produce rule labels or analyses under Issue #34.

## Report-specific handoffs

### S13 / Q3-S13 — Lantidra pooled label

- Approved version: `SPL-v3-a3163e14-0404-4e27-884b-f6f9f7f695bc`.
- Start from the DailyMed version locator in `source-review-log.csv`; record
  the exact label sections reviewed.
- A partial primary human review for 14 specific fields is recorded in
  `reviews/S13/human-source-review-approved-2026-10-28.md` and Issue #50.
  Keep the other 107 fields pending and obtain separate independent review.
- Preserve the full pooled treated population across both label studies,
  including repeat infusions. Do not extract only responders or those ever
  insulin-independent.
- Distinguish all treated participants, repeat infusion exposure, any-time
  independence, duration, and fixed-horizon assessments. Verify source
  units, population definitions, and available safety windows.

### S18 / Q3-S18 — PEC-Direct publication

- Approved version: `PMC8714853.1`.
- Review only the approved version and permitted factual annotations. Record
  each permitted article/supplement component actually reviewed.
- `mmc2.xlsx` is deliberately excluded participant-level material: do not
  retrieve, inspect, upload, reconstruct, or infer an omission from it.
- Preserve the full 17-person publication target. The population's overlap
  with S23 is documented at a broad level, but a subset direction must not be
  asserted without source evidence.

### S19 / Q3-S19 — PEC-Direct optimized publication

- Approved version: `PMC11471599.1`.
- Preserve CC BY 4.0 attribution and third-party material exceptions; item-
  level reuse review remains pending.
- The historical restore was accepted, but original restore bytes/verifier
  output are unavailable for independent reinspection. Do not claim new
  restore verification.
- Preserve the full 10-recipient optimized target. `MOESM4` was not reviewed;
  do not use its absence to assert omission. Participant overlap with other
  PEC-Direct reports remains uncertain unless directly verified.

### S23 / Q3-S23 — PEC-Direct single-site publication

- Approved version: `publisher-pdf-human-copy-2026-10-23`.
- **Sole assigned human reviewer only:** use the previously approved Path B
  individual public-publisher access. The automation must not retrieve or
  inspect the article/supplement or claim to complete this review.
- Do not commit, upload, or share either PDF, credentials, session tokens,
  private download URLs, or shared archives. No storage/sharing permission is
  inferred.
- The manifest's prior component hashes were not re-tested here. Record only
  the materials and locators the assigned reviewer actually verifies.
- Any completed source review or cohort-link adjudication involving S23 must
  identify the authorized Path B reviewer, `@aditmer`.
- Preserve the full 15-person single-site population. S18/S23 overlap is
  documented, but any specific subset direction still requires source
  evidence.

### S20 / Q3-S20 — PEC-Direct registry

- Approved version: `NCT03163511-history-v20`.
- Use the version-specific history panel locator, not the current API response
  as proof of historical byte identity.
- Keep the registry's planned efficacy Cohort 2 separate from Cohort 1 safety
  context. Verify enrollment, posted results, source-defined denominators and
  endpoints in this exact history version.
- Related registry/publication populations are not assumed to be the same
  participants; endpoint attribution and overlap remain unresolved until
  source-supported.

### S17 / Q3-S17 — VC-01 registry

- Approved version: `NCT02239354-history-v13`.
- Use the version-specific history panel and inspect Cohort 2 efficacy facts
  separately from Cohort 1 safety context.
- Verify the source-confirmed zero-enrollment claim for the target Cohort 2.
  Only after that review may the scoped efficacy assessment be
  `not_applicable`; this is not zero responders and not a negative treatment
  result.
- Do not infer no enrollment merely from missing results.

### S4 / Q3-S4 — Zimislecel registry

- Approved version: `NCT04786262-history-v32`.
- Use the approved historical panel. Keep VX-880 Parts A/B/C and their part
  strata as the target; exclude VX-017 Part D from target facts.
- Distinguish planned endpoints from observed results. Do not borrow
  publication outcomes or sponsor announcements.

### S9 / Q3-S9 — VX-264 registry

- Approved version: `NCT05791201-history-v26`.
- Use the approved historical panel. Preserve all VX-264 parts and planned/
  recipient population distinctions.
- Planned outcomes, unposted results, or enrollment are not observed outcomes
  or endpoint analysis denominators. Do not borrow other studies' outcomes.

## Cohort relationships and unresolved decisions

All six PEC-Direct report pairs are currently `uncertain` in
`cohort-links.csv`. The preregistration records S18/S23 population overlap,
without a verified directional subset in this ledger. S19 links remain
uncertain; S20's registry cohort relationship requires explicit verification.
To resolve any link, cite each exact source/version with its own locator,
record the human adjudicator/date, and ensure source-content review is logged
for both reports. A subset direction may state either population is the
subset; keep rows in their deterministic report order.
Do not sum participants, infer unique participants, combine endpoint
measurements across reports, or call reports independent replications.

If source identity contradicts a frozen target, stop and seek adjudication;
do not redefine the target after examining the outcome. If version
reproduction, lawful access, reporting omission, or essential endpoint-to-
target linkage cannot be resolved, preserve the evidence gap and request the
appropriate decision. This queue does not authorize Issue #35.
