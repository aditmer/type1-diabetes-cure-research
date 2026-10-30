# Project Moonshot Wave 2 evidence-resolution report

**Execution complete; scientific adjudication remains open.** All five
isolated workstreams delivered nine focused, independently reviewable PRs.
All nine are open against `main`, have green validation checks, and were
not merged by the agents. No authoritative fields or links were promoted.

| Workstream | PRs | Verified progress | Remaining blockers | Required human decision | Gate impact |
|---|---|---|---|---|---|
| Historical registries | [S17 #76](https://github.com/aditmer/type1-diabetes-cure-research/pull/76), [S20 #79](https://github.com/aditmer/type1-diabetes-cure-research/pull/79), [S4 #81](https://github.com/aditmer/type1-diabetes-cure-research/pull/81), [S9 #82](https://github.com/aditmer/type1-diabetes-cure-research/pull/82) | Exact historical browser panels accessed for all four sources; 58 new field proposals with locators and four consolidated checklists | Human verification, remaining field coverage, linked-component version/scope authorization; no historical JSON byte archive claimed | Accept/revise source-specific rows, preserve target/planned-result distinctions, decide remaining coverage and component scope | Browser-access blocker reduced; no source or G2-B gate closed |
| S18/S19 aggregate evidence | [S18 #75](https://github.com/aditmer/type1-diabetes-cure-research/pull/75), [S19 #80](https://github.com/aditmer/type1-diabetes-cure-research/pull/80) | S18 safe-access stop and remedy explicit; S19 approved XML hash reproduced, 20 field proposals and three separate graft-function observations | S18 aggregate-only surface; S19 safety-scope question, rights/supplement coverage, attrition and original restore artifacts | Authorize safe S18 review; accept/revise S19 rows and reconcile safety scope; dispose of component/rights/provenance limits | Public S19 re-fetch reproducibility improved; both authoritative reports remain pending |
| S23 governance / independent review | [#74](https://github.com/aditmer/type1-diabetes-cure-research/pull/74) | Evidence-backed readiness matrix, all-eight checklist, single-response form and unsent follow-up | Acceptance, qualifications, independence/conflicts, own lawful source access, prior Path B exception, incomplete source review | Nominee supplies own attestations; maintainer assesses suitability, scope and governance; independent findings and dated acceptance later | Administrative preparation only; #59 and #35 remain blocked |
| PEC-Direct cohort reconciliation | [#78](https://github.com/aditmer/type1-diabetes-cure-research/pull/78) | Six concrete `uncertain` recommendations with supporting/counterevidence and alternative-decision thresholds | Two-sided membership evidence and authorized source review; S18/S23 partial overlap has no matched count or accepted subset direction | One six-link adjudication batch, including S23 Path B human decisions and later independent challenge | All six authoritative links unchanged |
| S13 final three fields | [#77](https://github.com/aditmer/type1-diabetes-cure-research/pull/77) | Frozen image identity and actual inspection; concrete storage/scope recommendations and six synthetic compatibility tests | Versioned schema/dictionary approvals, separate classifier policy, human visual precision decision | One three-decision batch; no reopening of the approved 118 fields | All three pending fields and scientific rules unchanged |

## Verified baseline

Baseline: `7432cd3cb3bc1075706b12c50ab7156bc71ddb8c` (`origin/main`,
29 October 2026 UTC). All eleven Wave 1 PRs, #63 through #73, were merged
before workstream dispatch. Baseline CI:
[successful validation run](https://github.com/aditmer/type1-diabetes-cure-research/actions/runs/40955988649).

Local baseline checks passed: tracker integrity, extraction and candidate
validators, 286 unit tests, all seven synthetic controls, and `git diff --check`.
These checks establish machine consistency, not scientific source verification.

Comparison with pre-Wave-1 commit `119ab96` found no changes to the frozen
rules, preregistration, governing amendment/gate documents, source manifest,
authoritative `reports.json`, source-review log, cohort links, classifier, or
extraction validator. No baseline repair or reinterpretation was performed.
Historical counts in issue bodies and the extraction README are earlier
snapshots; the counts below were computed directly from `reports.json`.

| Report | Approved version | Reported | Reviewed omissions | Conflicting | Pending |
|---|---|---:|---:|---:|---:|
| S13 | `SPL-v3-a3163e14-0404-4e27-884b-f6f9f7f695bc` | 33 | 85 | 0 | 3 |
| S18 | `PMC8714853.1` | 0 | 0 | 0 | 121 |
| S19 | `PMC11471599.1` | 0 | 0 | 0 | 121 |
| S23 | `publisher-pdf-human-copy-2026-10-23` | 40 | 0 | 1 | 80 |
| S20 | `NCT03163511-history-v20` | 0 | 0 | 0 | 121 |
| S17 | `NCT02239354-history-v13` | 10 | 0 | 0 | 111 |
| S4 | `NCT04786262-history-v32` | 0 | 0 | 0 | 121 |
| S9 | `NCT05791201-history-v26` | 0 | 0 | 0 | 121 |
| **Total** | **8 reports, 121 fields each** | **83** | **85** | **1** | **799** |

Total: 968 fields. Neither `inaccessible` nor `not_applicable` currently has
an authoritative field. All six PEC-Direct cohort links remain `uncertain`.
All source-content-complete, access-attempts-complete, and
adjudication-complete flags remain false. No report has accepted independent
scientific review.

## Execution record

Five coordinated sessions were launched on fresh, isolated worktrees from
the verified `main`. Registry and aggregate-evidence workstreams were
instructed to create separate baseline-derived branches for each source.
File ownership excludes all authoritative fields, frozen rules, source
versions, review-completion flags, and cohort-link records.

| Workstream | Session | Assigned scope |
|---|---|---|
| Historical registries | `5343856a-8a34-4b72-b135-831247a45dd4` | S17, S20, S4, S9; four source-specific proposal PRs |
| Aggregate evidence | `801aae73-970d-4ed3-9f27-1db700a9795c` | S18 and S19; two source-specific proposal PRs |
| Review governance | `e1385b9f-c17b-407a-a427-dfbac3accd09` | S23 Path B and eight-report independent-review readiness |
| Cohort reconciliation | `201d6ab4-5048-4961-83d3-060a7ff038cf` | Six-link human-adjudication proposal only |
| S13 closeout | `75eabbfd-84c4-476f-bcd8-6e17d71ed7ed` | Three pending fields; proposals and synthetic compatibility tests |

Initial attachment-transfer calls failed before session creation because the
staged attachment area was unavailable. All five subsequent session creations
succeeded with instructions to read the original authorized attachment
directly. Failed launch calls are not counted as launched work.

## Independent-review readiness

The governance workstream produced [PR #74](https://github.com/aditmer/type1-diabetes-cure-research/pull/74),
including an updated readiness matrix, all-eight version-bound access and
coverage slots, six-link challenge requirements, and a single-response
onboarding form with a **draft, unsent** follow-up.

The recorded nominee remains invited, not accepted. The live Issue #59
record contains an assistant-authored relay of the maintainer's invitation,
not the nominee's own acceptance, qualifications, conflict disclosure,
source-access attestation, or findings. No invitation or follow-up was sent
by this workstream.

The smallest onboarding batch asks the nominee for acceptance and scope,
qualifications and ability, prior-contribution/conflict disclosure, and
component-specific access. The maintainer must separately assess suitability
and independence, authorize any additional S23 human scope conditional on
the reviewer's own lawful entitlement, and record a dated rights/provenance
disposition of the prior restricted-supplement chat-upload exception.
None of these human prerequisites is newly satisfied by the response form.

The authoritative S23 `safety.harms` conflict remains: main Results reports
175 first-year adverse reactions, while supplement Table S1's parenthesized
grade totals sum to 205 (175 + 24 + 4 + 2). The unparenthesized subset display
is not the full-event total, and severe-grade events are not automatically
regulatory serious adverse events. Both locators remain preserved; no printed
value has been corrected or harmonized. Publisher contents were not accessed
by the governance or integration workstreams.

## Historical registry evidence and proposal counts

Ordinary browser access succeeded for the approved history panels:
S17 v13 dated 2022-02-25, S20 v20 dated 2024-11-07, S4 v32, and S9 v26.
The source proposals record observed titles, version-panel headings, exact
history URLs, review scope, field locators, limitations, and dated attempts.
This establishes version-specific rendered-panel access, not historical
JSON byte identity. Prior internal-endpoint HTTP 403 results remain
historical context; current API output was not substituted.

| Source | New proposed `reported` field values | Other proposal accounting | Authoritative effect |
|---|---:|---|---|
| S17 | 6 | 10 approved objects preserved; 105 fields still pending in proposed inventory | None; authoritative 10 reported / 111 pending |
| S20 | 18 | 103 fields pending in proposed inventory | None; all 121 authoritative fields pending |
| S4 | 21 | 100 fields pending in proposed inventory | None; all 121 authoritative fields pending |
| S9 | 13 | 108 fields pending in proposed inventory | None; all 121 authoritative fields pending |
| S19 | 20 | Three separately scoped surrogate observations; four planned clinical listings with null results | None; all 121 authoritative fields pending |
| S18 | 0 | Six prior aggregate leads held/null/pending; no newly source-verified candidates | None; all 121 authoritative fields pending |
| S13 | 0 | Three pending-field recommendations, not new approved values | None; 118 approved objects preserved |

These are **78 proposed field values**, not 78 approved fields and not an
updated authoritative total. Surrogate observations, planned endpoint
listings, held leads, and schema recommendations are different units and
are not added to that count. Existing candidate packets were assessed
without being relabeled as new primary human review.

S17 keeps planned Cohort 2 non-enrollment distinct from zero responders and
keeps Cohort 1 safety contextual. S20 keeps Cohort 2 separate from Cohort 1.
S4 retains Parts A versus B/C and excludes VX-017 Part D; endpoint anchors
and intervals remain plans, not fixed-horizon observed results. S9 planned
outcomes remain separate from unposted observed outcomes. Linked
protocol/SAP material was not opened; its permitted component/version scope
and relevant coverage still need adjudication.

New S20 safety detail requires deliberate human mapping: a non-serious
`Hypoglycaemia` row contains one event in 1/47, with a footnote describing
it as severe and possibly product-related; a serious `Hypoglycemia` row
contains five events in 2/47. Severity and seriousness are different
dimensions. These rows were not normalized into the frozen severe-
hypoglycemia endpoint or summed into unique participants. Unit-explantation
footnotes, including cartilage described as likely graft-derived, remain
visible aggregate safety context; no endpoint or causality promotion follows.

## S13 three-field recommendations

[PR #77](https://github.com/aditmer/type1-diabetes-cure-research/pull/77)
contains the focused three-decision package and six synthetic compatibility
tests. All 118 previously approved S13 fields remain untouched.

| Pending field | Concrete recommendation | Required human decision |
|---|---|---|
| `overall_followup` | Adopt the range-plus-mean storage contract proposed in #64 only through an explicitly versioned extraction-schema amendment. Keep production classifier rejection of the new object until a separate P3 policy is scientifically approved; never coerce minimum, mean, or maximum into a fixed endpoint horizon. | Approve or revise storage representation separately from any classifier interpretation. |
| `other_evidence` | Adopt #68's ancillary-only enum scope through a dated dictionary/consumer boundary without changing P1. All eight current authoritative values are pending/null, so no already-approved enum values need migration. | Approve or revise the scope clarification, preserving the N=19 selected mixed-meal subgroup one year after final infusion separately from 25/30 any-time insulin independence. |
| `independence.onset` | Retain pending: actual frozen-image inspection does not support confident numerical extraction at its native resolution. | One visual request: verify all-treated row coverage, the first-infusion scale, first black/white transitions versus repeat-infusion arrows, and any defensible bounds or unresolved histories; otherwise record the visual-resolution blocker. |

New inspection bound Figure 1 to DailyMed archive 940595, the approved XML
member, and Section 14 `Fig1` / `MM1` resolving to `lantidra-01.jpg`
(866 by 433 pixels, 65,914 bytes; SHA-256
`6ad0706e8428c4d1cc81af7c38dc74d3e570c18fb56ac4cc313f52729f9f718a`).
Archive and XML hashes matched the frozen provenance. The actual image was
opened by the S13 workstream; no exact participant onset times were inferred.
Temporary source copies were removed and no source assets were committed.
This AI inspection is neither primary human approval nor independent
scientific signoff.

Previously recorded S13 printed duration/percentage and malignancy-count
discrepancies remain flagged as published. Neither the new schema
recommendations nor the image inspection silently corrects them.

## Six PEC-Direct relationships

[PR #78](https://github.com/aditmer/type1-diabetes-cure-research/pull/78)
provides a consolidated two-sided proposal, supporting and limiting evidence,
alternative-disposition thresholds, and one six-link human response batch.
It distinguishes inherited PR #66 annotations, previously approved S23
annotations, and attributed source-stream access/inspection relays. The
cohort workstream did not independently repeat primary-source retrieval.

| Relationship | Recommended decision | Decisive unresolved boundary |
|---|---|---|
| S18-S19 | `uncertain`; no subset direction | Safe S18 aggregate-only review and source-supported S19 re-enrollment/overlap mapping are absent. |
| S18-S23 | `uncertain`; preserve known partial overlap | Partial overlap is established context, not a matched count or directional subset. S23 decisions require authorized Path B human review. |
| S18-S20 | `uncertain`; no subset direction | Shared registration does not establish membership in frozen registry Cohort 2; S18 safe-access stop remains. |
| S19-S23 | `uncertain`; no subset direction | Publication chronology, site, and device changes do not establish participant distinctness or identity; S23 human access remains restricted. |
| S19-S20 | `uncertain`; no subset direction | Exact S20 history is browser-accessible, but participant membership and S19 re-enrollment exclusion are not established. |
| S23-S20 | `uncertain`; no subset direction | Two-sided source-supported membership is missing; the S23 side requires authorized human review. |

These are recommended decisions, not newly adjudicated link records.
`cohort-links.csv` is unchanged. No population totals were pooled, unique
cross-report participant counts estimated, or endpoints borrowed.

## Permitted aggregate evidence and access decisions

S18 [PR #75](https://github.com/aditmer/type1-diabetes-cure-research/pull/75)
retains the full 17-person target and the known participant-data exposure
stop. New HEAD-only checks of the Europe PMC XML and official `.1` locator
returned HTTP 200; no body was retrieved, no new hash was computed, and no
new identity or clinical-content verification is claimed. Six prior aggregate
leads remain held with null values and pending status. `mmc2.xlsx` was not
accessed, reconstructed, or used to infer missingness.

The concrete lawful remedy is for an authorized human/custodian to verify the
exact approved bytes and provide a rights-compliant aggregate-only surface or
factual attestation with version-specific locators, without transmitting
participant-level, excluded, or protected content. Endpoint denominators,
observation timing, harms, and attrition remain a single aggregate-only
human-review batch, not six requests or a claim of access exhaustion.

S19 [PR #80](https://github.com/aditmer/type1-diabetes-cure-research/pull/80)
newly retrieved the approved 122,548-byte Europe PMC XML and reproduced
SHA-256 `3e14ef3dcb7fd0c13a9326976c01511356426b8004dc7a9b78b3ffb2e2c68839`
before author-narrative inspection. DOI/PMCID matched. The XML has no
`pmcid-ver`; its `PMC11471599.1` binding remains the accepted manifest
hash/archive mapping, not a publisher editorial-version number.
**Public re-fetch reproducibility is resolved; recovery of the original
private restore artifacts is not.** Original OneDrive restored bytes and
verifier output remain unavailable for independent reinspection.

The S19 package proposes 20 typed field values for the full ten-person
optimized cadre, plus three separately scoped graft-function observations
and four explicitly planned clinical endpoint listings with null results.
C-peptide observations are not insulin-independence or patient-important
clinical outcomes. No table, figure, rights-pending third-party item, or
supplement was inspected by this workstream. MOESM1-MOESM3 remain unreviewed;
MOESM4 remains excluded. Item-level rights, clinical result denominators,
actual observation/attrition coverage, and the safety window remain open.

**New S19 safety-scope question:** Results `Sec3/Par9` attributes a serious
event to surgery, while Methods `Sec10/Par38` states no adverse events during
or after interventions. Both locators are retained for human timing/scope
adjudication; no printed value is corrected and no authoritative conflict
is promoted. Two affected people do not establish an independently enumerated
event total. No treatment-emergent-event-related withdrawal does not establish
zero all-cause attrition.

## Smallest consolidated human-review batch

Use the existing response forms in the PRs, in one coordinated handoff rather
than serial field-by-field prompts:

1. **Onboarding/governance:** nominee returns #74's acceptance, qualifications,
   independence/conflicts, and own component-access attestations. Maintainer
   records suitability, conditional S23 human scope and the dated Path B
   rights/provenance disposition. The follow-up remains unsent until authorized.
2. **Source decisions:** return one checklist per registry source; supply a
   lawful exact-version aggregate-only S18 surface/attestation; accept/revise
   S19's 20 values and three scoped surrogates, resolve its safety-scope
   question, and record remaining rights, attrition and provenance limits.
   Never access excluded components to resolve these gaps.
3. **S13:** return #77's three decisions on versioned range/mean storage,
   ancillary enum scope, and defensible Figure 1 visual bounds or continued
   visual-resolution blocker. Classifier interpretation remains a separate
   scientific decision, not an automatic consequence of storage approval.
4. **Cohorts:** return one six-link batch against #78, retaining `uncertain`
   where membership cannot be established. S23-dependent source decisions
   remain assigned-human Path B work; independent challenge follows.
5. **Release gate:** once primary decisions and coverage are reviewable, the
   qualified independent reviewer records their own findings for all eight
   reports and six links using their own lawful access; only then may the
   maintainer record a dated accept/revise/defer/stop decision under #59 on #34.

These batches do not claim that all 799 pending fields can be finalized
without additional permitted source review.

## Review order and next-wave priorities

The nine workstream PRs have disjoint paths and independent baseline ancestry;
none depends on another unmerged proposal. Suggested review/merge order is
#74 first for onboarding, then #76, #79 (safety footnotes), #81 (timing/parts),
#82 (plans), #75 (safe-access boundary), #80 (aggregate/safety), #77
(three-field decision package), and #78 after considering the source packages.
Merging a proposal is preparation, not approval of its proposed field values.
No automatic merge was performed or requested.

Next-wave priorities are the safe S18 aggregate-only route, S19 safety
scope/clinical-denominator/attrition and rights gaps, authorized remaining
registry coverage, S23 individual access and governance resolution, the three
S13 approvals, and then the two-sided cohort decisions and independent audit.
Do not prioritize real-source classification over these prerequisites.

## Integration verification

All nine source/workstream PRs were verified open against `main` with green
GitHub validation checks. All share baseline
`7432cd3cb3bc1075706b12c50ab7156bc71ddb8c` with no other workstream head as an
ancestor; S19 has two commits on its independent baseline-derived branch.
The branches touch 25 disjoint paths. The only modified existing file is
#74's governance handoff; the other 24 paths are additions.

Their generated diffs were applied together to a disposable baseline copy
without changing any PR or merging into `main`. Combined tracker,
extraction, and candidate validators passed, **336 unit tests passed**, and
all seven synthetic controls passed. Every PR diff passed `git diff --check`.
The original current-candidate validator does not ingest the new proposal
formats; their dedicated synthetic/structural tests supplement it.

All existing tracked files outside the governance handoff are unchanged
across the combined proposal set. Thus the authoritative field objects,
source versions, rules, classifier, review flags, source-review log, cohort
links and original trackers remain byte-identical to the verified baseline.
No new field-status totals replace the authoritative 83/85/1/799 snapshot.
Machine consistency and successful joint application do not establish the
truth, completeness, rights clearance, or human approval of source facts.

## Gate boundary

**G2-B is not accepted. Issue #35 remains blocked.** Candidate proposals,
green CI, PR creation or merge, and AI technical review cannot replace
authorized primary human adjudication, independent scientific review, or
the maintainer's explicit dated acceptance under Issue #59 on Issue #34.
No real-source paired classification or G2-C result is authorized by this report.
