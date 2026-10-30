# S13 Wave 2: three decisions, not three field promotions

**Unapproved, inactive resolution package for #53 / #34.** Baseline:
`7432cd3cb3bc1075706b12c50ab7156bc71ddb8c`. This package selects an adoption
path from #63, #64 and #68; it does not repeat their extraction checklists.
Only new proposal files and isolated synthetic compatibility tests are added.
No scientific semantics, source disposition or review flag is implemented.

## Baseline and evidence boundary

Fetched `origin/main` and local HEAD both matched the baseline before writes.
PRs #63-#73 are merged; the baseline CI run is
[40955988649](https://github.com/aditmer/type1-diabetes-cure-research/actions/runs/40955988649).
Local baseline validation passed all three validators, 286 tests and seven
synthetic controls. A path diff from approved-closeout commit
`119ab961c6021a34b544b8688a256b4ec65c422f` to the baseline showed only
preparation documents, proposals, candidate reviewer packets and tests, not
governing rules, authoritative field objects, source versions or review gates.

Direct counts from `reports.json`: eight reports x 121 fields = 968;
**83 reported / 85 unreported_in_reviewed_material / 1 conflicting /
799 not_yet_extracted**. S13: **33 / 85 / 3 pending**, with all 118 adjudicated
objects protected. The six cohort links remain uncertain. Independent review
is pending; no G2-B acceptance or G2-C authorization is supplied.

The [approved PR #62 record](../../extraction/reviews/S13/human-source-review-approved-2026-10-29.md)
establishes the existing human decisions. This new AI inspection is not an
extension of that human attestation. The governing rules v1.1 SHA-256 is
`56363652016477693ca71cb528cfb35a7162ddc6886d5e8bb7fa64ff647a2566`.
All recommendations are post-exposure and require explicit dated approval.

## A. Follow-up: approve storage separately; defer executable acceptance

**Recommend the #64 tagged-union representation, but reject its activation in
the current classifier until P3's new-case policy is scientifically approved.**
Preserve the exact legacy enum branch. The alternative branch has exactly:

```json
{
  "kind": "variable_duration_summary",
  "unit": "years",
  "minimum": 0.3,
  "maximum": 14.5,
  "mean": 3,
  "mean_plus_minus": 3.7,
  "anchor": "first_cell_administration"
}
```

This is a proposed source mapping, **not an input to a classifier or a ledger
update**. Frozen SPL v3 Section 6.1 supplies range and mean; Section 14 Figure 1
description confirms the first-infusion clock. Preserve the printed precision
and +/- magnitude; its dispersion type remains unspecified. Do not silently
name it SD, SE or CI. Retain all treated participants and repeat infusions.

The storage change can preserve scientific meaning because it need not assign
any predicate. An executable policy cannot yet be certified meaning-preserving:
v1.1 P3 specifies nominal follow-up, not a threshold on a distribution's mean,
minimum or maximum. In particular, minimum below one year is not proof of
P3 failure, and mean/maximum above one year is not proof of P3 success.

**Implementation order after approval:**

1. Assign an approved new extraction-schema identifier in a dated
   representation amendment bound to the rules hash above. Keep archived
   schemas/rules immutable. Accept legacy strings plus the exact #64 object
   only in that version. Reject extra keys, missing statistics, booleans,
   nonfinite/negative values, inverted bounds and means outside the range.
   Preserve field-envelope provenance and separate `followup_attribution`.
2. Update the extraction validator and its explicit version handling to store
   the object, without routing it into `q3_classifier.py`. Old readers must
   reject the new schema, not coerce it to `unspecified` or a nominal horizon.
   A separately authorized ledger PR can then promote this one field after
   actual source verification and representation approval.
3. Keep the synthetic/classification input contract closed to this object
   until a **separate** dated scientific decision approves its P3 handling.
   Prefer unknown/hold rather than an invented horizon if a future version
   needs execution; a candidate reason is `FOLLOWUP_SUMMARY_POLICY_PENDING`.
   That reason and mapping are unapproved design choices, not current output.
   Version the reason registry and output contract if adopted. No H4 endpoint
   horizon, anchor, numerator or denominator is supplied by the summary.

This deliberately chooses a storage-first migration rather than bundling a
new P3 rule into a schema patch. Until that migration is authorized and
implemented, `overall_followup` stays pending. Merging this proposal alone
cannot make even the storage change effective.

## B. Other evidence: scoped clarification, conditional compatibility

**Recommend #68's ancillary-only interpretation of the existing
`surrogate_only` spelling, with no executable behavior change.** Its meaning
would be "this ancillary evidence stream contains surrogate evidence only,"
not "this entire report has no clinical evidence." `none` and
`qualitative_only` remain scoped to that same ancillary stream.
Do not force a mixed qualitative/surrogate stream into an exclusive category.

This is scientifically consistent with the separation of P1 clinical streams
and the existing all-clinical-observations-`none` fallback. It is
**behaviorally compatible in the tested cases, not automatically semantically
compatible for every legacy consumer**. An external reader interpreting
`surrogate_only` report-wide must explicitly opt into the new dictionary
version. No new enum is needed for this particular source context.

The exact frozen source distinction must survive any adoption:

| Stream | Population and timing | Allowed use |
|---|---|---|
| Section 12.2, Table 2 mixed-meal glucose | N=19 selected insulin-independent subjects; one year after final infusion | Ancillary context only |
| Section 14 pooled/Table 4 paragraphs | 25/30 ever insulin-independent during variable follow-up | Existing approved any-time clinical observation, not fixed-horizon efficacy |

Neither 19 nor 30 is a new first-infusion month-12 endpoint analysis N.
The final-infusion visit cannot be reanchored without actual source evidence.
Glucose is not substituted for HbA1c, CGM, insulin-dose or severe-event outcomes.

**Migration decision narrowed by actual ledger audit:** all eight current
`other_evidence` fields are `not_yet_extracted`, value null. There are **zero
approved enum values to migrate in this ledger**. That does not establish
compatibility of unexamined external datasets or downstream readers.

After explicit maintainer and independent scientific approval, publish a dated,
versioned dictionary amendment retaining all three spellings and the current
P1 fallback/precedence. Require a consumer-version acknowledgment. Promote only
S13's ancillary field in a separate authorized ledger PR with Section 12.2
Table 2 locator and the N=19/final-infusion caveat in its adjudication note.
Do not modify the 25/30 observation, fixed-horizon nulls, other reports or
already approved fields. A changed P1 algorithm would require a distinct
scientific amendment, not this clarification.

The new tests extend #68 beyond P1 alone: all three spellings give identical
complete report outputs except the evidence field and its source-material hash when clinical
evidence is present, including wrong-anchor and incomplete-follow-up cases.
They also retain the legacy no-clinical-evidence reason differences.
Invented counts 6/11 and ancillary N=4 are deliberately not the source counts.

## C. Onset: actual frozen image inspected; no numerical extraction claimed

On **2026-10-29 at 21:18:22 UTC**, this agent retrieved the official
[DailyMed archive 940595](https://dailymed.nlm.nih.gov/dailymed/getArchivalFile.cfm?archive_id=940595),
verified the following bytes, and then opened the original JPEG locally for
AI visual inspection. This is a new inspection, not merely reliance on #63.

| Object | Bytes | SHA-256 |
|---|---|---|
| Archive ZIP | 327121 | `db33f66f3b6e3433d0c47667a0e367f4e1b464cc2875e023e950f1f049f1fd33` |
| `a3163e14-0404-4e27-884b-f6f9f7f695bc.xml` | 168862 | `696ebb05a528236ea6077c912785e94cf103aa4d29fa61bacab3282e65307fd4` |
| `lantidra-01.jpg` | 65914 | `6ad0706e8428c4d1cc81af7c38dc74d3e570c18fb56ac4cc313f52729f9f718a` |

XML root ID is `a3163e14-0404-4e27-884b-f6f9f7f695bc`, set ID
`24610d9f-0c5a-4f55-93b3-d456300bfd5d`, version 3, effective `20260113`.
This binds the asset to approved
`SPL-v3-a3163e14-0404-4e27-884b-f6f9f7f695bc`, not the live label.
Section `S14`, paragraph `Fig1`, following rendering reference `MM1`, and
`observationMedia[@ID='MM1']/value/reference` resolve the image member.
The native JPEG is 866 x 433 pixels.

**New inspection result:** Study 1/Study 2 horizontal histories, black insulin-use
and white independence segments, later-infusion arrows, and an axis in months
post first treatment from 0 to 170 are visible. Some early transitions are
crowded near the origin; thin boundaries and infusion marks cannot all be
resolved confidently at native resolution. No numerical onset labels or
source subject IDs were confidently readable in this inspection. This is not
a verified source-wide assertion that such information is absent.

**Recommend keeping onset pending**, not declaring it unreported or filling
the text field with "weeks." The existing text-type schema could accept a
human-verified bounded graphical summary, but accepting text is not evidence
that a summary has been correctly extracted. No participant-level timing,
range, mean, median, censoring or precision was derived. Table 4's duration
categories cannot supply onset. Enlargement cannot add source precision.

The single human visual decision request is:

> Using the exact `lantidra-01.jpg` above alongside frozen-v3 Section 14,
> can you verify all-treated row coverage, the first-infusion scale, and
> distinguish first black-to-white transitions from later-infusion arrows
> sufficiently to approve bounded graphical onset evidence? Record readable
> bounds and unresolved histories without exact-date claims; if not, confirm
> the visual-resolution blocker and leave onset pending.

This replaces a request for exact per-participant onset values with a
readability-and-bounds decision. A negative readability decision is not
`unreported_in_reviewed_material`; inaccessible/unreadable data and source
omission are distinct. If a reviewed summary is later proposed, retain
graphical-estimate provenance, positional labels only if needed, unresolved
coverage and the first-infusion anchor. Do not reset the clock after reinfusion.

Public accessibility and source approval are not blanket copyright permission.
The [NLM policy](https://www.nlm.nih.gov/web_policies.html#copyright) distinguishes
government from privately contributed content. This package redistributes no
ZIP, XML, image, screenshot, crop or tracing. Local temporary source copies
are removed after inspection. No excluded S18/S19 or restricted S23 material
was accessed.

## One compact human batch and gate impact

| Decision to record with actual reviewer/date | Recommended answer | Effect only after authorized implementation |
|---|---|---|
| Approve distribution storage independently of P3? | Yes; exact #64 union; no executable mapping yet | Can resolve follow-up representation, not a P3 result |
| Approve ancillary enum scope and consumer version boundary? | Yes; conditional compatibility; no P1 change | Can resolve S13 `other_evidence`, preserving N=19 vs 25/30 |
| Can the exact Figure 1 support defensible bounded onset evidence? | Human visual decision above; unresolved until answered | Can enable a separately verified onset proposal, never automatic promotion |

These are requests for decisions, not pre-filled approvals. Scientific/dictionary
adoption requires the maintainer and independent scientific reviewer; primary
source inspection requires an actual authorized human attestation. Proposal
merge is not adoption, field promotion, acceptance of #53, or G2-B acceptance.
The smallest adoption sequence is storage/dictionary amendment, authorized
field dispositions, then independent whole-ledger review under #59. Any future
P3 scientific policy is separately versioned and must precede its execution.

## Mechanical validation and protected invariance

Run all three repository validators, full unittest discovery, seven offline
controls and `git diff --check`. Compare protected paths to the exact baseline,
including every existing proposal: this change must consist only of the new
directory here and `tests/test_q3_s13_wave2_compatibility.py`.
Tests do not load real reports or source values into the classifier.
Mechanical success proves contracts and non-regression, not scientific truth,
human approval, sufficient figure readability, or acceptance of any gate.

Executed on 2026-10-29: all three validators passed; full suite **292 tests
passed** (286 baseline plus six new tests); all seven synthetic controls passed;
`git diff --check` passed. A byte comparison against the baseline confirmed
**all 93 existing tracked files unchanged**, including all 118 S13 approved
objects and both prior schema proposals. The two temporary source copies
were deleted after inspection; no source asset is in this change.
