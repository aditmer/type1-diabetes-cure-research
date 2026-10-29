# Overall follow-up representation proposal 2026-10-29-01

**Status: PROPOSAL ONLY; unapproved, inactive.** Issue #53 task 1; gate #34.
Single schema/enum owner: the S13 schema proposals preparation track.
Baseline: `119ab961c6021a34b544b8688a256b4ec65c422f` (dispatch and fetched
`origin/main` agree). This proposal is independently reviewable from the
`other_evidence` clarification and the separately owned Figure 1 packet.

## Evidence and exposure

This is informed by already disclosed source findings, **not a blinded or
prospective scientific amendment**. No new source inspection or human
attestation is asserted. The
[approved closeout record](../../extraction/reviews/S13/human-source-review-approved-2026-10-29.md)
and [latest work queue](https://github.com/aditmer/type1-diabetes-cure-research/issues/53#issuecomment-6506671471)
identify the representation blocker:

- Frozen source `SPL-v3-a3163e14-0404-4e27-884b-f6f9f7f695bc`, XML member
  `a3163e14-0404-4e27-884b-f6f9f7f695bc.xml`, Section 6.1 follow-up paragraph;
  Section 14 Figure 1 description supplies timeline context.
- XML SHA-256 remains
  `696ebb05a528236ea6077c912785e94cf103aa4d29fa61bacab3282e65307fd4`.
- Overall follow-up is variable **0.3-14.5 years, mean 3 +/- 3.7 years from
  first infusion**, for the pooled treated target, retaining repeat infusions.
  The source-reported +/- magnitude is retained without inferring that it
  denotes standard deviation, standard error, or a confidence interval.

The range is not maximum-only, later-only, a nominal common visit, or an
endpoint interval. Its minimum is below one year; its maximum and mean do
not show how many participants reached a horizon. Do not select only
participants who were insulin-independent.

## Minimal proposed value contract

In a **new, explicitly approved extraction schema version**, extend only
`overall_followup.value` from the existing enum to a tagged union:
unchanged legacy enum strings OR the following duration-summary object.
All existing field-envelope provenance/status/review requirements still apply.
The object is an alternative value, not an extra report or a new source.
Neither current extraction nor current synthetic schema accepts it.

Illustrative S13 mapping **after approval only**, not a ledger update:

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

For this narrowly scoped proposal these are the exact keys; the unit and tag
are fixed. Numeric values must be finite, nonnegative, and not booleans;
`minimum <= mean <= maximum`. The anchor is source-stated, not calculated:
`first_cell_administration`, `repeat_administration`, or `unspecified`.
For sources lacking one of these summary statistics, retain the current
pending state and seek a separately reviewed contract rather than inventing
numbers. The proposal does not claim a universal follow-up schema.

Source precision is preserved as numbers (3 remains 3); units stay years.
No multiplication by 365, conversion to day 365/week 52/month 12, implied
fixed assessment, inferred N, or reset to a final infusion is permitted.
`followup_attribution` remains a separate field. The first-infusion anchor is
descriptive here: P3 does **not** acquire H4's anchor requirement.

## Classifier semantics and compatibility

The proposal separates **storage from rule adjudication**. The test-local
contract checker validates shape only; it returns no predicate or label.
There is deliberately no adapter from the proposed object to the production
enum and no alternate classifier. Adding the enum name alone without the
statistics would lose the evidence and is not the recommended amendment.

Current P3 (rules v1.1, `provisional_v1_0.requirements.P3`) asks for stated
overall target follow-up at least nominal 12 months; later-only is accepted,
without endpoint-specific timing or a treatment-anchor requirement.
The current implementation maps nominal horizons and `later_only` to met,
`below_12_months` to unmet, and `maximum_only`/`unspecified` to unmet.
All these **existing mappings stay unchanged**.

**Recommended decision boundary:** approve the representation separately
from P3 interpretation. Do not infer either P3 met from the maximum/mean or
P3 unmet merely from a minimum below one year. Requiring every participant
to reach one year would retrospectively tighten the permissive screen;
using an average as a nominal visit would relax it. Neither follows from
the current preregistration. The source summary alone does not encode a
nominal screen horizon.

If a future executable version must accept this object before a distinct
source-supported nominal P3 adjudication is available, recommend an
**explicitly approved unknown/hold**, retaining the distribution and the
schema-adjudication uncertainty. This is a proposed new-case policy, **not
an already approved v1.1 mapping or an S13 P3 result**. Its precise
reason-code and provenance contract need approval before implementation;
do not misuse `FOLLOWUP_UNREPORTED` for positively reported follow-up or
`SOURCE_CONFLICT` for an enum mismatch. Until that decision, reject the new
shape at the executable boundary and leave the real field pending.

H4 is untouched: the object cannot satisfy any endpoint's horizon, anchor,
interval, population, or denominator. No harmonized label, paired transition,
support-loss fraction, sensitivity, or robustness result is produced here.

## Decisions required before adoption

1. Maintainer and independent scientific reviewer must explicitly approve
   the duration-summary contract, confirm preservation of the +/- notation, and
   decide whether it is a representation-only amendment. Record actual
   identities, dates, scope and decision; this proposal supplies none.
2. Separately approve the P3 boundary for variable summaries under the
   preregistered wording, including the recommended unknown/hold and its
   reason-code/provenance design if needed. If a changed threshold or new
   scientific rule is wanted, disclose it as a new version after exposure,
   not a silent clarification or outcome-selected reclassification.
3. Use a dated, separately committed amendment bound to the exact governing
   rules hash. Allocate new schema/rule version identifiers only on approval;
   preserve v1.0, v1.1 and the prior approved amendment byte-for-byte.
   A later implementation PR must update both validators and synthetic
   contract tests, preserve every legacy mapping, and reject implicit
   downgrade/coercion. Old readers must fail explicitly on the new version.
4. A separate authorized field-adjudication change may then populate this
   one S13 field with exact version/target/subcohort/locators and the approved
   review provenance. Representation approval is not field promotion or
   approval to change other fields. Preserve all prior approved field objects.

Current governing rules v1.1 SHA-256:
`56363652016477693ca71cb528cfb35a7162ddc6886d5e8bb7fa64ff647a2566`.
The original v1.0 and amendment hashes remain respectively
`6cc2408d40072ccc83943cc9e7baca8bb653bb16d8ef36a8d2a6a802e48806a2`
and `ac0fc63bf8d836f780b4d1838e482c98bad66a3cb3e3bf5290462a94a01f37a1`.

## Isolation, regression coverage, and gates

`synthetic-summary.json` uses invented numbers deliberately different from
S13. `tests/test_q3_followup_proposal.py` checks the proposed value shape,
invalid ranges/types/units/anchors, production rejection, and every legacy
P3 mapping. Only synthetic identifiers enter the current classifier.
Run `python3 -m unittest discover -s tests -p 'test_q3_followup_proposal.py' -v`.

This directory is not imported by production scripts, does not update
`SPECS`, and is not a sanctioned input to either live validator.
Production files, frozen rules, source manifest, rights, trackers, all eight
report records and six uncertain cohort links remain unchanged.
S13 stays **33 reported / 85 unreported in reviewed material / 3 pending**.
The human-review sprint finished, but source-content review and adjudication
remain globally incomplete; independent review remains pending. Figure 1
onset is separately owned. No excluded S18/S19 component or restricted S23
content was accessed. #59 independent review and explicit maintainer G2-B
acceptance are still required; #35 remains blocked. Merging this proposal
does not approve adoption or open any analysis gate.
