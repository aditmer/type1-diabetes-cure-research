# Project Moonshot — Wave 2 human-adjudication package

**Status: READY FOR HUMAN REVIEW — NO APPROVAL RECORDED BY THIS PACKAGE.** Prepared 2026-10-30 as a coordination aid from the 2026-10-29 Wave 2 AI-prepared candidate proposals. This packet does **not** impersonate a human reviewer, assert fresh source inspection, promote any authoritative field, change the preregistered rules, settle rights questions, or satisfy the independent G2-B gate.

> **Begin here:** [Exact 78-field decision matrix](wave2-human-adjudication-field-matrix-2026-10-30.md) — every proposed typed value, frozen locator, limitation and human check, grouped by source. Do not approve from this summary alone.

## A. Scope, baseline and how to return one decision batch

- **Repository / gate:** `aditmer/type1-diabetes-cure-research`, [Issue #34](https://github.com/aditmer/type1-diabetes-cure-research/issues/34), independent review [#59](https://github.com/aditmer/type1-diabetes-cure-research/issues/59), restricted S23 [#52](https://github.com/aditmer/type1-diabetes-cure-research/issues/52). **G2-B not accepted; G2-C #35 blocked.**
- **Prepared-against authoritative snapshot:** `reports.json` on `main` at commit `ce2655fbc07f8c8660ab3436fcd271c09a8a63fa`. At that snapshot: eight frozen reports x 121 = 968 fields; **83 reported, 85 reviewed omissions, 1 conflicting, 799 pending**; six PEC-Direct cohort links still `uncertain`.
- **Proposal baseline:** nine workstream PRs #74–#82 (plus integration PR #83) were authored from `7432cd3cb3bc1075706b12c50ab7156bc71ddb8c`. The full matrix retrieves each original proposal **by immutable head SHA**. Their merge into `main` changes availability of documents, **not their scientific approval**. Recompute current ledger counts and compare exact field records before any subsequent promotion.
- **Human review scope:** 78 newly proposed field values (S17 6, S20 18, S4 21, S9 13, S19 20), one batch of six cohort-link dispositions, three S13 scientific/schema/visual decisions, S18 access disposition, S19/S20 safety clarification, and independent-review/S23 governance prerequisites. The non-78 items are *separate decisions*, never silently counted as new field approvals.

**Decision codes for every proposed field:** `APPROVE` only if the human actually inspected its exact approved source version, locator, field meaning, target and limitations; `REVISE` with corrected value/status and source locator; `DEFER` if material, rights, version or meaning is unverified; `REJECT` only with an explicit rationale. **No selection is pre-filled in the matrix.** Accepting a candidate means only the scoped field decision, not source-global review completion.

**Efficient batching:** A qualified, authorized reviewer may submit a *source-level blanket approval* **only after personally checking every field listed for that source**; otherwise list exact approved field IDs and exceptions. Record actual reviewer identity, date, source components inspected, provenance, permitted access route, unsupported/contradictory evidence and revised statuses. Do not use a single 'all 78 approved' message merely from reading the AI packet.

### One-pass review workflow

1. **Pin source identity first.** Verify the frozen document/panel actually opened; use its exact manifest version, target/subcohort and the matrix locator. A current live registry API response does not substitute for a historical version; a public source page does not authorize restricted components.
2. **Check the 78 lines source by source.** Confirm each printed/posted fact, numeric type, units, planned vs observed label, target attribution, timing, and safety/attrition denominators. Preserve author/source contradictions instead of silently fixing them.
3. **Make one combined exceptional-decision pass.** Record the special S13, S18, S19/S20, S23 and six-cohort responses in Sections C–G below. You may defer specific blockers without holding up unrelated approved source rows.
4. **Return a signed batch using Section H.** An agent may then prepare source-specific **candidate-to-ledger PRs** for *only* those genuinely approved fields and any approved versioned schema amendments. Independent scientific review remains distinct.

## B. 78 proposed source fields — recommended review order

| Source | Proposed fields | Frozen version / primary locator | Proposal and source-specific caveat | Human disposition |
|---|---:|---|---|---|
| **S17** | 6 | `NCT02239354-history-v13` | [#76](https://github.com/aditmer/type1-diabetes-cure-research/pull/76). Cohort 2 was **never initiated**; Cohort 1 19-person safety cannot be promoted as observed Cohort 2 harms. Confirm baseline and safety *context*, not efficacy. | **PENDING** |
| **S20** | 18 | `NCT03163511-history-v20` | [#79](https://github.com/aditmer/type1-diabetes-cure-research/pull/79). Cohort 2 Started 47, C-peptide assessed N=42, safety N=47; distinct denominators. Serious and severe hypoglycemia language must not be conflated. | **PENDING** |
| **S4** | 21 | `NCT04786262-history-v32` | [#81](https://github.com/aditmer/type1-diabetes-cure-research/pull/81). Only VX-880 Parts A/B/C; **exclude Part D VX-017**. Planned endpoints are not observed outcomes; retain official-title vs structured-phase discrepancy. | **PENDING** |
| **S9** | 13 | `NCT05791201-history-v26` | [#82](https://github.com/aditmer/type1-diabetes-cure-research/pull/82). Enrollment 7 is **not** treated/analyzed N. Day-90 C-peptide and 24-month safety are planned; no posted observed data were established. | **PENDING** |
| **S19** | 20 | `PMC11471599.1` | [#80](https://github.com/aditmer/type1-diabetes-cure-research/pull/80). Full 10-person optimized group. Hash-matched public XML supports candidate locators, **not** recovery of original historical private restore. Safety-scope discrepancy requires a decision. | **PENDING** |
| **Total** | **78** | Five distinct approved frozen versions | Full value/locator/field checks in the [matrix](wave2-human-adjudication-field-matrix-2026-10-30.md). | **No approval yet** |

### High-risk mappings to challenge rather than rubber-stamp

- **S17 (especially `safety.harms`, `.population`, `.window`, `.attribution`):** The posted 114 events/19 analyzed, serious 2/19 and other 18/19 are **Cohort 1 context**, not Cohort 2 observed harms. Decide whether `reported` for each candidate is a faithful *context-only* field with correct attribution, or whether it should be revised/deferred for the frozen target. No subjects in Cohort 2 does **not** mean zero responders or adverse events.
- **S20 (`counts.enrolled`, `safety.harms`, `.discontinuations`, `burden.immunosuppression`):** Confirm how Started 47 maps to enrollment, not actual implantation. The source's **serious hypoglycemia** row reports 5 events in 2/47; separately a **non-serious** AE row has one event in 1/47 with a **severe** footnote. Severity, regulatory seriousness, event counts, participant counts and causality are not synonyms. Do not auto-populate the frozen SHE endpoint. Premature device/unit explantation is not a patient withdrawal or complete therapy-discontinuation count. A described immunosuppression AE endpoint is not an actual drug regimen.
- **S4 (`safety.harms`, `insulin_independence.*`, `hba1c.*`, `severe_hypoglycemia.*`):** A `reported` field may state what the **protocol planned**, not a numerical observed outcome. Preserve Part A vs B/C and the distinct anchors: one year after *achieving* independence, one year after *infusion*, or from Day 90. Never derive a common first-infusion 12-month numerator. No result posted does not mean zero events.
- **S9 (`safety.harms`, `.population`, `.window`):** All 13 proposed fields describe frozen registry identity, enrollment or **plans**; confirm that each `reported` note clearly retains planned-only context. Do not set treated or safety analyzed N to seven without source evidence.
- **S19 (`safety.harms`, `.attribution`, `.discontinuations`, `identity.mapping`):** Two affected people with TE serious AEs is **not** necessarily two events. No TEAE causing withdrawal is not no all-cause attrition. Cadre chronology and same trial do not prove participant identity with S18/S23/S20. See safety-scope decision in Section C.

### S19 ancillary observations outside the 78

The [#80 pinned source proposal](https://github.com/aditmer/type1-diabetes-cure-research/pull/80) separately reports three **graft-function-surrogate C-peptide** observations: 5/10 at month 3 above detection, 4/10 at month 6, and 3/10 above the higher threshold through month 12. Four protocol clinical outcome listings remain **planned**, without observed counts. **Human check:** verify exact thresholds, denominators, timing and target from the approved XML, then record context-only/adjudication notes; do not treat these seven annotations as extra reported field approvals, insulin independence, a severe-hypoglycemia reduction or a fixed-horizon clinical effect.

## C. Additional safety and access decisions — record explicitly

| ID | Decision needed | Proposed default / required evidence | Human response |
|---|---|---|---|
| **C1 — S19 safety scope** | Results `Sec3/Par9` describes a surgery-attributed serious event while Methods `Sec10/Par38` says no adverse events during/after interventions. Determine if the statements refer to different timing, event types or contexts, or are genuinely incompatible. | Review **both** original passages, exact version, definitions and timing. If incompatible, preserve both locators and use the `conflicting` path; do **not** silently resolve or convert a non-TEAE withdrawal statement into zero attrition. | **PENDING** |
| **C2 — S20 hypoglycemia classification** | Decide whether severe-footnoted other-AE, serious hypoglycemia, or neither satisfies the frozen endpoint-specific severe-hypoglycemia definition/window/population. | Keep **five serious events in two people** separate from **one severe-footnoted event in one person**. No unique-participant addition, no default SHE outcome, no assumed causality. | **PENDING** |
| **C3 — S18 lawful source route** | Can an authorized human/custodian obtain a version-bound, permitted *aggregate-only* factual view or attestation without retrieving participant-level/embedded excluded material? | [#75](https://github.com/aditmer/type1-diabetes-cure-research/pull/75) retained **zero verified candidate fields** and six held leads. The previous broad-page route exposed participant-level content, so extraction stopped. **Never access `mmc2.xlsx` or infer from it**. If no safe route, keep all 121 fields pending and record blocker; HEAD HTTP 200 is not clinical source verification. | **PENDING** |
| **C4 — S19 rights/provenance** | What aggregate narrative/Methods components can the authorized reviewer personally inspect; are MOESM1–3 item permissions cleared? | Repeated approved public XML hash does not recreate historical OneDrive restore artifacts. `MOESM4` and rights-pending third-party items remain excluded. Document access/omissions by component. | **PENDING** |

## D. S13 — three decisions **not** part of 78 field approvals

See [#77](https://github.com/aditmer/type1-diabetes-cure-research/pull/77), based on [#63](https://github.com/aditmer/type1-diabetes-cure-research/pull/63), [#64](https://github.com/aditmer/type1-diabetes-cure-research/pull/64), [#68](https://github.com/aditmer/type1-diabetes-cure-research/pull/68), and the approved S13 closeout. Frozen label `SPL-v3-a3163e14-0404-4e27-884b-f6f9f7f695bc`, archive 940595. Its **118 approved field objects remain unchanged; 3 remain pending.**

| ID / field | Review question and recommendation | Human decision (select and document date/scope) |
|---|---|---|
| **D1 — `overall_followup`** | **Storage only:** approve/revise/defer the proposed versioned `variable_duration_summary` preserving minimum 0.3, maximum 14.5, mean 3, printed ±3.7 **without assuming SD/SE/CI**, years, first infusion. **Separate P3 scientific-policy decision** is required; minimum below one year and mean/maximum above one year do not establish a nominal month-12 screen. Keep current classifier rejecting the new object until approved rules/version/reason-code policy exists. | **PENDING**: storage `APPROVE / REVISE / DEFER`; distinct P3 `DEFER / APPROVE VERSIONED POLICY` with scientific rationale |
| **D2 — `other_evidence`** | Approve/revise/defer a **versioned ancillary-stream-only** interpretation of `surrogate_only`, not the whole report. N=19 selected insulin-independent MMTT glucose **one year after final infusion** remains ancillary; 25/30 ever-independent is a separate clinical any-time observation. The proposal tested behavior but does not prove every downstream consumer semantically compatible. No P1 algorithm or fixed-time endpoint change. | **PENDING**: `APPROVE CONDITIONAL / REVISE / DEFER`; document consumer/version compatibility and scientific review |
| **D3 — `independence.onset`** | A human with the frozen image may verify **readability/graphical bounds** for Figure 1, first-infusion axis and black-to-white transitions versus repeat-infusion arrows. Native JPEG is 866×433; AI could not confidently resolve all early transitions. **Do not invent exact onset dates.** If unreadable, explicitly retain pending rather than marking omission or zero. | **PENDING**: `BOUNDED HUMAN-VERIFIED EVIDENCE / UNREADABLE-PENDING / DEFER`; cite actual image/rows/scope |

**D1/D2 governance:** An approved new extraction schema or enum semantics require a dated, version-bound scientific change, compatibility analysis and separately authorized field-level PR. They are not automatically authorized by merging #77 or by the earlier 118-field S13 human approval. An independent qualified reviewer must separately scrutinize any substantive scientific-rule change before its use.

## E. PEC-Direct: single six-link human-adjudication batch

Source [#78](https://github.com/aditmer/type1-diabetes-cure-research/pull/78). The six candidate relationships remain `uncertain`; recommendations are **not** newly adopted cohort decisions. Examine **both** sides of each pair using only permitted version-locked aggregate evidence. Known S18/S23 partial overlap is a contextual fact, not a reliable matching count or accepted subset direction.

| Pair | Proposed relationship | Supporting evidence | Contradictory/limiting evidence | Exact human determination needed | Decision |
|---|---|---|---|---|---|
| **S18–S19** | `uncertain`, no direction | Both population annotations refer to PEC-Direct Cohort 2; S19 explicitly cites S18 as an earlier group. | Earlier versus optimized cadre and different enrollment/device strategy counter an automatic same-cohort inference, but do not prove mutually exclusive people. No affirmative source contradiction establishing disjointness is available. | Decide whether approved aggregate cadre wording explicitly excludes repeat participation across these two full targets. If not, adopt uncertain with no direction; do not infer distinctness from chronology. **Threshold to change:** distinct_within_program requires explicit aggregate non-overlap/re-enrollment exclusion covering both complete targets. A subset requires complete inclusion and direction; same requires full membership equivalence, not common trial registration. | **PENDING** |
| **S18–S23** | `uncertain`, no direction | Known partial overlap and inherited S23 cross-reference annotations support shared membership context, not a counted match or complete inclusion. | Known overlap rules out distinct_within_program. Full targets of 17 and 15 counter same-target equivalence; the smaller site target does not by itself prove it is wholly within the publication data-cut target. | Accept uncertain while preserving known partial overlap, unless @aditmer can verify aggregate evidence that every S23 target member belongs to the exact S18 target. Cross-reference clues alone are insufficient. **Threshold to change:** Only if complete S23-in-S18 inclusion is verified on both frozen sides propose subset/to_is_subset_of_from in this S18-to-S23 row. Never invent a matched count; do not amend vocabulary to force an overlap value. | **PENDING** |
| **S18–S20** | `uncertain`, no direction | S18's aggregate population is described as a Cohort 2 publication selection; S20 is the related Cohort 2 registry report. | Publication data-cut selection is not the registry STARTED accounting definition. Shared NCT03163511 and Cohort 2 labels do not establish inclusion in the exact history-v20 target or endpoint compatibility. | Decide whether every member of S18's full publication selection is included in v20's Cohort 2 target under compatible enrollment/implantation accounting; otherwise adopt uncertain. **Threshold to change:** subset/from_is_subset_of_to requires an explicit aggregate inclusion statement plus verified v20 cohort definition/data-cut mapping. Registry totals, planned labels or a publication citation alone cannot satisfy it. | **PENDING** |
| **S19–S23** | `uncertain`, no direction | S19 cites S23 as an earlier study group within the shared program; S23 is the full Vancouver site population. | A later optimized cadre is not automatically the earlier site group, but chronology/device differences do not exclude repeat participation. S18/S23 overlap is not transitive proof of S19 membership. | Decide whether aggregate source prose excludes all S23-target participation in the optimized S19 cadre. If it does not, adopt uncertain rather than infer distinctness from enrollment timing. **Threshold to change:** distinct_within_program requires two-sided aggregate exclusion of repeat membership across the complete targets; same/subset requires explicit equivalence/inclusion. @aditmer must verify the S23 side under Path B. | **PENDING** |
| **S19–S20** | `uncertain`, no direction | Inherited S19 prose places the ten-recipient optimized cadre in Cohort 2; S20 is the related registry report. | Changed device/cadre strategy and enrollment interval need mapping to v20 cohort categories. Neither common registration nor a registry flow count proves the optimized ten are included in that frozen registry target. | Decide whether the v20 Cohort 2 definition includes all ten optimized recipients despite relevant cadre/device amendments; without aggregate membership verification adopt uncertain. **Threshold to change:** subset/from_is_subset_of_to requires verified v20 categories and explicit inclusion of the entire optimized cadre. Do not use response subsets, endpoint denominators or current-API data as membership proof. | **PENDING** |
| **S23–S20** | `uncertain`, no direction | The Vancouver site target shares NCT03163511 with the related Cohort 2 registry report. | S23 allocated/implanted/overall-analysis membership is not automatically v20 STARTED membership. The single-site target cannot stand for all registry participants; S18 overlap does not independently prove site-to-registry inclusion. | Have @aditmer decide whether all 15 site-target participants map to history-v20 Cohort 2 with compatible allocation/implantation/STARTED definitions; otherwise adopt uncertain. **Threshold to change:** subset/from_is_subset_of_to requires verified aggregate site inclusion and exact v20 accounting on both sides. A shared registry ID, site label or numerical comparison alone is insufficient. | **PENDING** |

**Recording rule:** An authorized reviewer may approve `uncertain` **as an explicit adjudicated decision** only after source-scoped two-sided inspection, with reviewer/date and residual uncertainty. This is not the same as an untouched default uncertainty. Do not upgrade to subset/same/distinct based on chronology, common registry identifiers, matching sample sizes, or response-selected subsets. S23-dependent facts require the designated Path B human reviewer; independent challenge remains required.

## F. S23 and independent reviewer — separate governance response

Human adjudication here **does not** replace S23's restricted human-only Path B or the distinct [#59 independent-review gate](https://github.com/aditmer/type1-diabetes-cure-research/issues/59). [#74](https://github.com/aditmer/type1-diabetes-cure-research/pull/74) contains the detailed response batch and **unsent** follow-up. No reviewer contact/acceptance is presumed.

| Responsibility | Required action and evidence | Decision |
|---|---|---|
| **Nominee / R1–R3** | Reviewer personally confirms accept/decline/limited scope for eight source reports, 968 field dispositions and six link checks; supplies relevant scientific qualifications, contribution/conflict/independence disclosure and public-attribution limits. Nominated/invited is **not** accepted. | **PENDING** |
| **Maintainer / M1** | Personally assesses reviewer scientific competence, independence and any additional qualified coverage; records dated scope. Technical-only review cannot satisfy scientific signoff. | **PENDING** |
| **Maintainer / M2, M3** | Separately authorize S23 human review scope conditional on *reviewer's own lawful publisher access*, and resolve prior restricted-supplement chat-upload/AI-inspection governance exception with rights/provenance effect and remediation plan. | **PENDING** |
| **Reviewer / R4, R5** | Document own source-version access/rights for all eight, exact components actually inspected, qualified independent source/field checks and six-link challenge. For S23 do not forward, upload, archive or let an AI inspect protected publisher PDFs. | **PENDING** |
| **Maintainer / M4** | Only **after** complete authorized primary review, independent findings and rights resolution: explicitly accept/revise/defer/stop eight-report G2-B on [#34](https://github.com/aditmer/type1-diabetes-cure-research/issues/34), linking #59 and reviewed commits. | **PENDING** |

**S23 unresolved clinical point:** The source-level **175 vs 205 adverse-reaction grade-total discrepancy** must be independently challenged with each lawful source locator; do not equate CTCAE grade with regulatory seriousness. No Wave 2 agent had new authority to inspect S23 publisher content, and no S23 new field promotion is requested here.

## G. Post-human-review implementation sequence (agent work)

1. Capture the **actual** signed human decisions in a review artifact linked from the relevant source issue. List every approved/revised/deferred field with exact frozen version and locators. For source-level bulk approval, explicitly attest that the full source-specific candidate row set was personally verified, with exceptions.
2. Agents open **separate source-specific adjudication PRs** for only the approved field-level statuses; preserve existing approvals and source-printed discrepancies byte-for-byte unless an authorized correction is explicitly recorded. Never change independent-review identities/dates on a human's behalf.
3. Preserve planned-versus-observed, context-versus-target, event-versus-person and first-versus-repeat administration boundaries. Recompute 968 field counts directly from merged authoritative ledger after every PR. Hypothetically accepting all 78 would leave **721 still pending**, before any further authorized review; it would **not** complete the eight-source corpus.
4. Versioned S13 schema/semantic implementation, if separately approved, belongs in its **own** PR with frozen-rules hash binding, consumers/regression tests and no retroactive silent reinterpretation. Keep real-source classifier closed until actual G2-B acceptance and explicit #35 authorization.
5. Independent scientific reviewer independently challenges all eight reports, all field statuses (including omissions and conflicting/pending), and six links using lawful personal source access. Then maintainer separately records a dated G2-B decision; do not infer acceptance from green CI or merged proposals.

## H. Copyable human decision record — fill in only after actual inspection

This is an **empty template**. Do not change `PENDING` to `APPROVE` merely by reading the candidate summaries. To minimize repetition, one dated submission may cover multiple personally inspected frozen sources, while retaining source-by-source exact coverage.

```text
WAVE 2 PRIMARY HUMAN ADJUDICATION — ACTUAL REVIEW RECORD
Reviewer identity / role: [actual human]
Review date: [YYYY-MM-DD]
Authoritative ledger commit actually checked: [SHA]
Source versions and permitted components personally inspected: [by source]
Access/rights/version limitations: [by source]

S17 v13 — 6 proposed fields: APPROVE ALL / APPROVE SPECIFIC IDs / REVISE / DEFER
  Approved IDs: [list or ALL if each row personally verified]
  Revised/deferred IDs + source locators/reasons: [list]
  Confirm Cohort 1 safety is contextual only: [decision]
S20 v20 — 18 proposed fields: APPROVE ALL / APPROVE SPECIFIC IDs / REVISE / DEFER
  Approved IDs: [list or ALL after personal verification]
  Revised/deferred IDs + locators/reasons: [list]
  Serious-versus-severe hypoglycemia + unit-explantation decision: [decision]
S4 v32 — 21 proposed fields: APPROVE ALL / APPROVE SPECIFIC IDs / REVISE / DEFER
  Approved IDs: [list or ALL after personal verification]
  Revised/deferred IDs + locators/reasons: [list]
  Parts A/B/C vs D and planned/observed scope: [decision]
S9 v26 — 13 proposed fields: APPROVE ALL / APPROVE SPECIFIC IDs / REVISE / DEFER
  Approved IDs: [list or ALL after personal verification]
  Revised/deferred IDs + locators/reasons: [list]
  Seven enrolled vs treated N and planned/observed scope: [decision]
S19 PMC11471599.1 — 20 proposed fields: APPROVE ALL / APPROVE SPECIFIC IDs / REVISE / DEFER
  Approved IDs: [list or ALL after personal verification]
  Revised/deferred IDs + locators/reasons: [list]
  Section 3 vs 10 safety scope: [decision with both source passages]
  3 surrogate observations / 4 planned listings: [context-only decision]

S18 aggregate-only safe-access decision: [SAFE AUTHORIZED ROUTE / HOLD / OTHER + evidence]
S19 rights and original historical-restore limit: [decision]
Six PEC-Direct links: [each pair -> retain uncertain / justified alternative / defer]
S13 D1 follow-up storage: [approve / revise / defer]; distinct P3 policy: [decision]
S13 D2 ancillary-stream semantics: [approve conditional / revise / defer]
S13 D3 onset Figure 1 legibility: [bounded readable / unreadable pending / defer]
Independent reviewer onboarding and S23 Path B governance: [not assumed complete; actual evidence refs]

Explicit exclusions and unreviewed material: [items and effects]
Previously approved field modifications authorized, if any: [NONE unless documented]
Human conclusion: [specific rows and decisions only; not global G2-B signoff]
Human-authored attribution / signed GitHub comment or PR review link: [link]
```

**Scientific stop:** This document, any answer given in chat, a source-candidate PR merge, or technical CI does **not** by itself satisfy independent reviewer qualification, primary-review completion, S23 rights clearance, G2-B acceptance or G2-C authorization. Retain explicit NO-GO/hold where a source or decision remains unsupported.

