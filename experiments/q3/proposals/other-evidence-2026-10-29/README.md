# Ancillary evidence scope proposal 2026-10-29-02

**Status: PROPOSAL ONLY; unapproved, inactive.** Issue #53 task 3; gate #34.
Single schema/enum owner: the S13 schema proposals preparation track.
Baseline: `119ab961c6021a34b544b8688a256b4ec65c422f` (dispatch and fetched
`origin/main` agree). Independent of the overall-followup proposal, with
disjoint proposal/test paths and no shared-schema edits. Figure 1 onset is
owned separately.

## Evidence, exposure, and the ambiguity

This proposal uses already disclosed findings in the
[approved closeout record](../../extraction/reviews/S13/human-source-review-approved-2026-10-29.md),
not a new source inspection or human attestation. It is source-informed,
not blinded or prospectively specified before outcome exposure.

For frozen `SPL-v3-a3163e14-0404-4e27-884b-f6f9f7f695bc`, XML member
`a3163e14-0404-4e27-884b-f6f9f7f695bc.xml`:

- Section 12.2, Table 2 describes ancillary mixed-meal glucose among **N=19
  selected insulin-independent participants one year after FINAL infusion**.
- Section 14's pooled-participant/Table 4 paragraphs also report **25 of 30
  ever insulin-independent during variable follow-up**. The previously
  approved any-time observation and screen quantity must remain unchanged.
- XML SHA-256 remains
  `696ebb05a528236ea6077c912785e94cf103aa4d29fa61bacab3282e65307fd4`.

The report is **not surrogate-only**. Mixed-meal glucose is not an observed
HbA1c, CGM time-in-range, insulin-dose, or severe-hypoglycemia endpoint under
P1. N=19 is neither the full pooled target nor its first-infusion month-12
analysis denominator. Do not equate final infusion with first infusion or
calculate a reanchored visit. The label's repeat-infusion context matters.

The current enum can store a *category* but not these measurement, selection,
denominator and timing details. Those details require the existing field
envelope's review scope, locators and adjudication note; no new endpoint
values or denominators should be populated from this ancillary table.

## Recommended minimal semantic amendment

In a separately approved, versioned dictionary clarification, define
`other_evidence` as **ancillary evidence outside the qualifying P1 clinical
endpoint streams**, not a mutually exclusive characterization of the report.
Keep the existing three enum spellings:

| Value | Proposed explicitly scoped meaning |
| --- | --- |
| `none` | Reviewed ancillary stream has no such other evidence; not absence of clinical outcomes. |
| `surrogate_only` | The ancillary stream described by this field contains surrogate/biological evidence only; qualifying clinical outcomes may coexist in their own fields. |
| `qualitative_only` | The ancillary stream described by this field is qualitative only; not a report-wide absence of quantitative clinical evidence. |

This resolves the present category/scope ambiguity without adding a clinical
domain, endpoint, denominator, or a redundant `mixed_report` enum. It does
not cover every hypothetical mix of ancillary types; do not force a mixed
surrogate/qualitative ancillary stream into either exclusive category.
The six field statuses retain their existing meaning. Do not choose `none`
as a placeholder for a pending ancillary decision.

**S13 candidate after explicit approval only:**
`other_evidence.status=reported`, `value=surrogate_only`, with review scope
limited to *ancillary mixed-meal glucose*, exact frozen-version Section 12.2
Table 2 locator, and an adjudication note retaining **N=19 selected
insulin-independent subjects, one year after final infusion; not full target,
not a first-infusion 12-month outcome; clinical any-time independence is
recorded separately in Section 14**. Reuse only the actual approved review
provenance and obtain explicit approval of this interpretation. This text is
not a completed field object or a new human decision.

If reviewers require `surrogate_only` to retain report-wide scope, reject
this candidate rather than hiding its meaning in free text. The alternative
is a new versioned ancillary category/structured field with explicit scope
and compatibility review; **do not** silently reinterpret approved records.
The preferred narrow clarification needs explicit approval because an enum's
meaning is part of the frozen contract even when its spelling is unchanged.

## Why this need not change the classifier

At baseline `scripts/q3_classifier.py` builds P1 from observed quantitative
clinical candidates and their target attribution. `_evaluate(other_evidence)`
is not itself a P1 support gate. The ancillary field can select the existing
`SURROGATE_ONLY` **failure reason only when P1 is already unmet and every
clinical observation is explicitly `none`**. The planned-only branch has
precedence over that fallback. Incomplete clinical review does not satisfy
the all-none guard.

Consequently this clarification must not:

- erase an observed any-time clinical finding or call the whole report
  `surrogate_only`;
- make glucose ancillary evidence meet P1, H2, H3 or H4;
- override unknown clinical evidence, invent an endpoint assessment, or use
  a successful P1 screen to fill missing fixed-horizon clinical fields.

Keep the current all-none guard, P1 candidates, reason code meaning,
precedence, target attribution, H4 first-administration convention and all
existing outputs unchanged. A report-wide `SURROGATE_ONLY` reason remains
appropriate only under the existing confirmed-no-clinical-evidence guard.
This PR runs that behavior **only on invented controls**, not S13.

## Compatibility, governance, and required decisions

1. Maintainer and independent scientific reviewer must explicitly decide
   ancillary-vs-report scope and whether the proposed S13 category is valid.
   Record real approvers, dates, scope and exposure; no approval is inferred
   from proposal merge or the prior field-review attestation.
2. Record a dated dictionary/schema semantic amendment bound to governing
   v1.1 SHA-256
   `56363652016477693ca71cb528cfb35a7162ddc6886d5e8bb7fa64ff647a2566`.
   Preserve original rules and approved amendments. Assign an approved
   semantic version and require consumers to acknowledge it; the fixture's
   proposal identifier is **not** an approved rules/schema version.
3. Before implementation, audit existing `other_evidence` uses for scope
   compatibility without rewriting approved field objects. Unambiguous
   ancillary uses may be carried forward with recorded provenance;
   ambiguous legacy uses require separate adjudication, not automatic
   migration. Versioned consumers must not silently equate newly scoped
   records with a report-wide old interpretation. Retain the three legacy
   enum spellings and production behavior unless separately approved.
4. Any future S13 field promotion is a separate authorized ledger change
   after semantic approval. Preserve 25/30 any-time independence, all
   fixed-horizon nulls and all other approved field objects. Never copy
   N=19 to `counts.at_horizon` or any required clinical denominator.

This is a dictionary clarification proposal, not a threshold change. If
review instead calls for changed P1 behavior, treat that as a separate
scientific rule amendment with source-exposure disclosure, independently
reviewed deterministic controls and explicit approval before implementation.
No post-hoc reinterpretation is presented as preregistered behavior.

## Tests and unchanged gates

`synthetic-context.json` uses invented counts (not 19, 25 or 30).
`tests/test_q3_other_evidence_proposal.py` exercises the current classifier
with synthetic-only IDs: clinical any-time plus ancillary evidence, absent/
unknown/planned/contextual clinical observations, wrong-anchor rejection,
legacy enums, and rejection of the proposed context container as production
input. Ancillary timing stays separate from every clinical endpoint field.
Run `python3 -m unittest discover -s tests -p 'test_q3_other_evidence_proposal.py' -v`.

No production path reads this directory. No frozen rules, schema, manifest,
rights, trackers, report record, human attestation, completion/acceptance
flag, or cohort link is edited. Six cohort links stay uncertain. S13 remains
**33 reported / 85 unreported in reviewed material / 3 pending**. The human
review sprint is finished but source-content review/adjudication are
globally incomplete; independent review is pending. No excluded S18/S19 or
restricted S23 content was accessed. #59 and explicit G2-B acceptance remain
required; #35 remains blocked. No real-source paired classifier, robustness,
or outcome analysis is authorized or executed. Proposal merge is not adoption.
