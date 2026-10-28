# Q3 G2-B source extraction and adjudication ledger

**Status: partial human-approved S17, S13 and S23 field decisions recorded; full G2-B
source review and independent acceptance remain pending.** This package is authorized by the authenticated G1 GO on Issue #32
and G2 readiness acceptance on Issue #33 for Issue #34's eight approved
source versions only. It implements source extraction and conservative
cohort-link recording. It does **not** classify reports, produce paired
provisional/harmonized labels, estimate support loss, run sensitivities, or
make scientific conclusions. Issue #35 remains unauthorized until this
ledger is independently reviewed and accepted.

At initial scaffold creation, none of the 968 fields had clinical source
review, and no real-source analysis was authorized. **Update 2026-10-28:**
the maintainer `@aditmer` explicitly reports having personally completed
the S17 source-review checklist and approved **ten specified source fields**,
including a revised planned `identity.dose` value with both 4-or-6 VC-01
combination-product implants and up to 3 VC-01-20 sentinel units. The
source-review audit, exact locators, and limits are recorded in
[`reviews/S17/human-source-review-approved-2026-10-28.md`](reviews/S17/human-source-review-approved-2026-10-28.md)
and [Issue #34's human-approval relay](https://github.com/aditmer/type1-diabetes-cure-research/issues/34#issuecomment-6471095071).
At that point, `reports.json` contained **10 reviewed `reported` fields**;
**111 S17 fields** and **958 total fields** remained `not_yet_extracted`.
The later S13 update below records the additional approved fields.

**Update 2026-10-28:** the maintainer `@aditmer` also explicitly approved a
partial primary human source review for **14 specified S13 fields** from
DailyMed SPL v3 Sections 5.1, 6.1, and 14, including Table 3. The exact source
version, fields, counts, printed percentages, discrepancies, and limitations
are recorded in
[`reviews/S13/human-source-review-approved-2026-10-28.md`](reviews/S13/human-source-review-approved-2026-10-28.md)
and [Issue #50](https://github.com/aditmer/type1-diabetes-cure-research/issues/50).
The 25 participants ever insulin-independent are not a fixed-horizon result;
Table 3 and duration discrepancies remain exactly as reported. The ledger has
24 reviewed `reported` fields in total; 107 S13 fields, 111 S17 fields, and
726 fields across the other six reports remain `not_yet_extracted` (944 total).
Both reviews were partial. **Subsequent 2026-10-28 S23 update:** `@aditmer` approved 40 specific S23 fields and one `conflicting` safety field after personally inspecting publisher main sections and supplement. See [S23 review record](reviews/S23/human-source-review-approved-2026-10-28.md) and [Issue #52](https://github.com/aditmer/type1-diabetes-cure-research/issues/52#issuecomment-6481495840). Main Results' first-year 175 adverse reactions remain inconsistent with Table S1's 205 four-grade total; no correction is made. Source-rights/human-only Path B chat-upload exception is documented. The authoritative ledger now has **64 `reported`, 1 `conflicting`, 903 `not_yet_extracted`** across 968; S23 has 80 still unextracted. All three source reviews remain partial, with independent review pending.

The maintainer's own statement—not the AI assistant's inspection—is the
primary human-review attestation. It describes a partial ten-field review,
not all 121 S17 fields or the linked protocol/SAP. The S17 evidence class
remains `version_specific_locator`: its current-API JSON hash is **not**
historical-v13 byte identity. Source-content review is **partial**,
adjudication/access attempts remain incomplete, **independent review is
still pending**, and Issue #35 (G2-C) remains **BLOCKED** until full
eight-source G2-B acceptance. S23's assigned human has now completed a **partial** source review only; separate lawful independent-reviewer access remains unconfirmed.

## Files and schema

- `reports.json` has eight report records in frozen rules order. Each record
  repeats the exact source/report/program/target/subcohort/version tuple, a
  version-evidence note, a human-review record, and the complete 121-field
  inventory from `SPECS` in `scripts/q3_classifier.py`. It contains no outcome
  values or classifications.
- The human-review record includes the primary reviewer/date, independent
  review pending state, and—if closed—the independent reviewer/date/scope/
  decision. Reviewer identities are normalized before requiring distinct
  primary and independent reviewers.
- Each field retains the governing `field_id`, one of the six v1.1 statuses,
  typed `value` or `null`, source version, target population, subcohort,
  locator list, review scope, reason codes, adjudication note, review
  completeness, access log, and structural rationale. Existing nulls are not
  converted into zeroes or negative outcomes.
- `source-review-log.csv` records the scope actually reviewed (manifest
  metadata only), accepted-version evidence class and limitations, approved
  review directions, explicitly excluded or unreviewed materials,
  source-specific access and rights restrictions, and pending reviewer fields.
  Review directions are not claims that the cited source material was examined.
  Its separate `clinical_content_reviewed`, `source_content_review_complete`,
  `access_attempts_complete`, and `adjudication_complete` flags distinguish
  inspected source content, exhaustive source review, completed access attempts,
  and final field-level dispositions. An inaccessible-only report may have
  completed access attempts and adjudication but cannot claim clinical-content
  review.
- `cohort-links.csv` contains the six PEC-Direct pairings, all conservatively
  marked `uncertain`. It retains the preregistration's documented S18/S23
  overlap without asserting a directional subset; S19 and registry-to-
  publication relationships remain unresolved. Resolved links require
  exact source-version identifiers and specific locators for both records,
  actual content-review evidence for both reports, and the human adjudicator
  and date. The validator also preserves the preregistration's known
  S18/S23 overlap across `same` normalization and transitive subset links, so
  a distinct relationship cannot separate populations known to overlap. A
  reviewer may retain `uncertain` after reviewing both sources;
  when doing so, record the same source-specific locators, reviewer, and date
  rather than leaving the relationship indistinguishable from untouched
  scaffold. Subset direction can point either way while canonical row ordering
  remains fixed.
- `tracker-corrections.csv` is a separate, currently empty correction ledger.
  It is not consumed as source evidence. Use only `LEDGER_EXTRACTION_GAP`,
  `LEDGER_EXTRACTION_ERROR`, or `SOURCE_VERSION_CHANGE`, with the original
  tracker commit/row, annotations, approved version, a locator bound to that
  report's exact source version and specific location, and rationale. The
  source-specific excluded/unreviewed component restrictions also apply to
  correction locators. Do not modify `data/evidence.csv`, `data/trials.csv`,
  or `data/sources.csv`.
- `adjudication-queue.md` is the report-by-report handoff and reviewer
  checklist.

## Inventory and version provenance

The eight frozen identifiers below reconcile to both
`experiments/q3/rules-v1.1.json` and `source-manifest.csv`; they cover exactly
five programs. The `manifest_sha256` in `reports.json` is copied from the
approved manifest as provenance metadata and is not independently recomputed
in this task.

| Source / report | Program | Target / subcohort | Approved source version | Evidence class recorded |
|---|---|---|---|---|
| S13 / Q3-S13 | lantidra-pooled | lantidra-treated / lantidra-pooled-all | `SPL-v3-a3163e14-0404-4e27-884b-f6f9f7f695bc` | Recorded byte-identity and archive-member hash evidence |
| S18 / Q3-S18 | pec-direct | pec-s18-target / pec-s18-all | `PMC8714853.1` | Recorded XML identity/hash evidence |
| S19 / Q3-S19 | pec-direct | pec-s19-target / pec-s19-optimized-all | `PMC11471599.1` | Accepted historical restore attestation, with independent-reinspection limitation |
| S23 / Q3-S23 | pec-direct | pec-s23-target / pec-s23-site-all | `publisher-pdf-human-copy-2026-10-23` | Sole assigned reviewer's access attestation; no new hash test |
| S20 / Q3-S20 | pec-direct | pec-registry-cohort2 / pec-registry-cohort2-all | `NCT03163511-history-v20` | Version-specific history locator |
| S17 / Q3-S17 | vc01 | vc01-cohort2 / vc01-cohort2-planned | `NCT02239354-history-v13` | Version-specific history locator |
| S4 / Q3-S4 | zimislecel | vx880-parts-abc / vx880-parts-abc-all | `NCT04786262-history-v32` | Version-specific history locator |
| S9 / Q3-S9 | vx264 | vx264-all / vx264-all-parts | `NCT05791201-history-v26` | Version-specific history locator |

The registry history locators, not hashes of current ClinicalTrials.gov API
responses, identify the approved historical versions. S19's restore record is
accepted but its original verification output and restored bytes are
unavailable for independent reinspection. S23's recorded component hashes
were not re-tested here. These distinctions are preserved rather than
presented as equal forms of byte verification.

## Field states and provenance contract

The six exact statuses are `reported`,
`unreported_in_reviewed_material`, `inaccessible`, `not_yet_extracted`,
`conflicting`, and `not_applicable`, as defined by
`experiments/q3/rules-v1.1.json`. Use `reported` only with a typed,
source-supported value and exact locator, including source-reported zero,
false, or unfavorable values. Every field locator must name the exact approved
source-version identifier carried by that report and a specific page, section,
table, figure, or history field; copied version metadata alone does not bind a
citation to the source. Other statuses retain a null value and their
required review/access/conflict evidence. A completed omission requires
completed human review of the relevant permitted material; an unreviewed
supplement cannot establish omission. Conflicts need both locators. Structural
inapplicability needs explicit source-supported rationale and cannot waive a
required domain or denominator.

The complete field inventory is intentionally the classifier's frozen
`SPECS` set, not an alternate field dictionary. It covers target enrollment,
population and design, treatment and co-interventions, global and endpoint
denominators, baseline and endpoint definitions, observed versus planned
clinical measurements, endpoint-specific timing/anchor/population, insulin
independence onset/duration, CGM range/aggregation, attrition, harms, and
safety. Preserve source units, definitions, precision, nominal dates, and
denominator basis. Planned endpoints are not observed outcomes. Do not borrow
another endpoint's denominator or another report's source/version/population.

## Human reviewer workflow

For each report, the assigned reviewer should:

1. Confirm the exact approved version and lawful individual access before
   examining contents. Record only the materials and sections actually
   examined, with page/table/section or version-specific history-field
   locators; distinguish prior manifest attestations from new review.
2. Check source-use conditions and exclusions. Do not reproduce protected
   expression or figures, store or share publisher PDFs, or put credentials,
   tokens, private download links, or private archive locations in this
   repository.
3. Complete the field-by-field checklist in `adjudication-queue.md`. Link each
   fact to the frozen target, endpoint, denominator basis, time window and
   first-administration anchor. Keep planned outcomes separate from observed
   results, and retain explicit unfavorable and zero values.
4. Mark an omission only after complete review of all relevant permitted
   material. Otherwise use `not_yet_extracted` or `inaccessible` as
   appropriate. For unresolved conflicts, retain both exact locators and an
   explanation. Use `not_applicable` only for allowed, evidence-backed
   structural cases.
5. Mark source-content review complete only after the permitted source content
   has been reviewed and no fields remain inaccessible or unextracted. Mark
   access attempts complete only after all permitted access routes have been
   exhausted. Mark adjudication complete only after every field has a final
   reviewed state; inaccessible fields require completed access attempts but
   do not count as clinical-content review. Record the actual reviewer/date.
   S23 source review and any cohort-link adjudication involving S23 must be
   performed by the specifically authorized Path B reviewer, `@aditmer`. If
   independent review is closed, record its reviewer, date, scope, and
   decision. Do not mark the ledger accepted or use it to execute Issue #35.

Source-specific guardrails:

- **S13:** retain the entire pooled treated population and repeat infusions;
  do not select responders or only participants ever insulin-independent.
- **S18:** `mmc2.xlsx` participant-level material is deliberately excluded.
  Do not retrieve, inspect, upload, reconstruct it, or infer source omission
  from its absence.
- **S19:** retain CC BY 4.0 attribution and third-party exceptions. Item-level
  reuse review remains pending; the accepted restore has the limitation above.
  MOESM4 was not reviewed.
- **S23:** only the sole assigned human reviewer has the approved Path B
  access. This package contains no publisher PDF or supplement and makes no
  claim the assigned review was completed.
- **S20:** relation to publication cohorts is not identity proof; verify
  Cohort 2 mapping and endpoint attribution.
- **S17:** verify the target Cohort 2 enrollment finding in the approved
  history version. If source-confirmed as un-enrolled, record
  `not_applicable` for its scoped efficacy assessment, not zero responders;
  keep Cohort 1 safety context separate.
- **S4/S9:** distinguish planned outcomes and unposted results from observed
  outcomes. Do not borrow VX-880 publication, sponsor, or other-study facts.

## Validation and limitations

From the repository root:

```sh
python3 scripts/validate_q3_extraction.py
python3 -m unittest discover -s tests -p 'test_q3_extraction.py' -v
```

The validator compares every report/version/target with the approved rules
and manifest, requires the exact classifier field inventory, validates value
types and provenance, checks review evidence for omissions/inapplicability,
validates cohort vocabulary and correction separation, and rejects
subset cycles and contradictory distinct relationships by directed
subset-reachability (shared larger cohorts are allowed; a known shared
subcohort is not), including contradictions with the documented S18/S23
overlap after normalization or transitive subset links. S13 and S18 are bound
to their recorded byte-identity evidence class; report and review-log classes
cannot be changed together to bypass that provenance requirement. Shared
classifier consistency checks also reject contradictory field records.
Excluded S18/S19 components cannot be cited in field, cohort, or tracker
correction locators, and those citations are bound to their report's approved
source version and specific location. Private filesystem paths and mismatched
version-evidence classes are rejected. It does not verify the truth of source
facts or substitute for human rights/access review. The existing classifier
remains synthetic-only; this package adds no real-source classification path.

As of 2026-10-28, **S13, S17 and S23 have partial primary human source review only**; five other reports remain pending. There are **64 `reported`, 1 `conflicting`, 903 `not_yet_extracted`** out of 968; all six PEC-Direct links remain `uncertain` and the tracker-correction ledger remains separate and empty. Nothing here is a
report-level classification, a complete human adjudication, or an acceptance decision.
