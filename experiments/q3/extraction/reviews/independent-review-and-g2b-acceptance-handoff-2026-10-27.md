# Q3 G2-B independent-review and acceptance handoff

**Readiness update: 2026-10-29. G2-B acceptance remains PENDING; defer
acceptance on the present evidence. Issue #35 remains BLOCKED.** This is an
AI-prepared administrative handoff for a separate qualified human reviewer,
not primary source review, independent scientific approval, or a maintainer
gate decision. It improves the existing handoff in place; the filename is its
original creation date, not the current evidence date.

## Baseline and authority

Dispatch main SHA and actual fetched `origin/main` baseline both equal
`119ab961c6021a34b544b8688a256b4ec65c422f` (S13 PR #62 merged).
The isolated branch was clean and fast-forward checked against that baseline
on 2026-10-29. Counts below were derived from baseline
[`reports.json`](../reports.json), not copied from Issue #59's older totals.
Reconcile against a newly pinned commit before the human review starts and
again before any gate decision; preparation on other branches is not an
approved ledger update.

Read [Issue #59](https://github.com/aditmer/type1-diabetes-cure-research/issues/59),
its [reviewer onboarding record](https://github.com/aditmer/type1-diabetes-cure-research/issues/59#issuecomment-6497871495),
and
[Issue #34's latest gate note](https://github.com/aditmer/type1-diabetes-cure-research/issues/34#issuecomment-6506676395)
alongside the actual discussion. The governing repository artifacts are
[`rules-v1.1.json`](../../rules-v1.1.json),
[`source-manifest.csv`](../../source-manifest.csv),
[`source-review-log.csv`](../source-review-log.csv), the ledger, and
[`cohort-links.csv`](../cohort-links.csv). Issue summaries, candidate packets,
AI checks and this document do not override those records. The
[adjudication queue](../adjudication-queue.md) and
[extraction README](../README.md) include dated historical totals; their
2026-10-28 summaries must not be used as current counts.

### Baseline review matrix (121 fields per source; 968 total)

| Source | Reported | Unreported in reviewed material | Conflicting | Not yet extracted | Primary human field scope | Independent review |
|---|---:|---:|---:|---:|---|---|
| S13 | 33 | 85 | 0 | 3 | 118 field decisions; partial source review, October 28/29 records | PENDING |
| S18 | 0 | 0 | 0 | 121 | None; AI preparation only | PENDING |
| S19 | 0 | 0 | 0 | 121 | None; AI preparation only | PENDING |
| S23 | 40 | 0 | 1 | 80 | 41 scoped decisions; partial source review, October 28 record | PENDING |
| S20 | 0 | 0 | 0 | 121 | None; candidates only | PENDING |
| S17 | 10 | 0 | 0 | 111 | Ten scoped decisions, October 28 record | PENDING |
| S4 | 0 | 0 | 0 | 121 | None; candidates only | PENDING |
| S9 | 0 | 0 | 0 | 121 | None; candidates only | PENDING |
| **Total** | **83** | **85** | **1** | **799** | **169 field-level review-complete markers, not 169 resolved facts** | **All eight PENDING** |

`inaccessible` and `not_applicable` currently have zero entries. Preserve all
six frozen statuses. The conflict is reviewed but unresolved; omissions are
limited to the material actually reviewed and are never zero outcomes.
All eight source-content-review, access-attempt-completion and
adjudication-completion flags remain false. Five sources have no primary human
review. All eight independent-review-pending flags remain true.

For exact reviewed/unreviewed field IDs, use each report's 121 `fields`
records, `review_complete`, `review_scope`, locators and adjudication notes,
not a new parallel field dictionary. The human reviewer must independently
challenge **all 968 dispositions**, including pending fields and omissions,
as primary adjudications become available; checking only the 169 reviewed
entries or the candidate subset cannot complete #59. Primary completion and
independent scientific review are separate requirements.

## Eight-source version and rights checklist

For every row, the reviewer must personally open the permitted source,
record access date, exact component/version and target/subcohort, and compare
it with the manifest and rules. Record a new hash only if actually computed
on a lawfully acquired representation; a different serialization is a
discrepancy to document, not permission to change the frozen version.
The identities below are **baseline recorded evidence, not new hash tests**.
No source material was retrieved or clinically inspected for this handoff.

| Source / frozen target and subcohort | Identity the reviewer must check | Permitted material and boundary |
|---|---|---|
| S13 / `lantidra-treated` / `lantidra-pooled-all` | `SPL-v3-a3163e14-0404-4e27-884b-f6f9f7f695bc`; DailyMed archive **940595**, member `a3163e14-0404-4e27-884b-f6f9f7f695bc.xml`; match root id/setId/versionNumber/effectiveTime. XML SHA-256 `696ebb05a528236ea6077c912785e94cf103aa4d29fa61bacab3282e65307fd4`; ZIP SHA-256 `db33f66f3b6e3433d0c47667a0e367f4e1b464cc2875e023e950f1f049f1fd33`. | Frozen label, especially Sections 2, 5.1, 6.1, 12.2, 14 and Figure 1. NLM terms apply; facts and locators, no blanket redistribution right. No protocols/SAPs or participant-level records inferred inspected. |
| S18 / `pec-s18-target` / `pec-s18-all` | `PMC8714853.1`; DOI `10.1016/j.xcrm.2021.100466`; exact Europe PMC XML SHA-256 `2c33d10d93cd399fadef190447f2ea5778625c476405f3e6cb011eb94e792433`. Check article metadata, embedded version, history and permissions. PMC `.1` is an archive locator, not a publisher editorial-version number. | Main article and permitted `mmc1`/`mmc3` only; separately record each component actually inspected. CC BY-NC-ND 4.0: noncommercial factual annotations/locators only, no protected expression, figures or adaptations. **Never access, reconstruct or infer from `mmc2.xlsx` / its Table S1.** |
| S19 / `pec-s19-target` / `pec-s19-optimized-all` | `PMC11471599.1`; DOI `10.1038/s41587-023-02055-5`; recorded XML SHA-256 `3e14ef3dcb7fd0c13a9326976c01511356426b8004dc7a9b78b3ffb2e2c68839`. No embedded `pmcid-ver`; `.1` is an archive locator. Historical OneDrive restore attestation was accepted, but original restored bytes/verifier output are unavailable for independent reinspection. A matching public XML does not recreate that restore event. | Main article; MOESM1/2/3 directions only where item-level permission permits. Retain author attribution, CC BY 4.0 and third-party exceptions. **No MOESM4 or rights-pending third-party material.** Identify blocked items from permissions/metadata without opening restricted content; obtain rights/governance disposition first. |
| S23 / `pec-s23-target` / `pec-s23-site-all` | `publisher-pdf-human-copy-2026-10-23`; DOI `10.1016/j.stem.2021.10.003`, NCT03163511, full 15-person site target. Recorded main PDF: 3,927,356 bytes, SHA-256 `0c7bf5e8f66a3b44992522b7911a7bd39b473a6b55d47cb8e6a2f81eed45e3f2`. Compare own lawful copy to this identity; document differences or inability to match. Editorial-version sequence and exact supplement URL remain unresolved. Do not claim new component hash verification. | **Separate restricted human-only workflow.** Own lawful publisher access to main pp. 1-21 and separate `mmc1.pdf`: Methods S1-S7, Tables S1-S2, Figures S1-S5. Elsevier copyright; no established storage/sharing permission. No forwarded/shared/chat-uploaded PDF, common archive, AI inspection, restricted copies or private URLs in repository. Prior sole-reviewer access does not authorize the independent reviewer. |
| S20 / `pec-registry-cohort2` / `pec-registry-cohort2-all` | `NCT03163511-history-v20`, submitted 2024-11-07; [official history v20](https://clinicaltrials.gov/study/NCT03163511?tab=history&a=20#version-content-panel). Match study ID, version label, submission date and modules actually inspected. | Approved historical protocol/results panel under registry terms. Current API SHA is **not** historical byte identity; no current-version substitution. Cohort 2 target, not pooled Cohort 1 safety or presumed publication identity. |
| S17 / `vc01-cohort2` / `vc01-cohort2-planned` | `NCT02239354-history-v13`, submitted 2022-02-25; [official history v13](https://clinicaltrials.gov/study/NCT02239354?tab=history&a=13#version-content-panel). Match version and explicit no-enrollment statements, not just flow Started=0. | Historical panel under registry terms; current API hash/normalized agreement is corroboration only, not archived v13 bytes. Linked `Prot_SAP_000.pdf` is not separately attested inspected; do not infer omissions from it. |
| S4 / `vx880-parts-abc` / `vx880-parts-abc-all` | `NCT04786262-history-v32`, submitted 2026-08-27; [official history v32](https://clinicaltrials.gov/study/NCT04786262?tab=history&a=32#version-content-panel). Match part mapping and approved no-results-module state. | Historical panel under registry terms; exclude VX-017 Part D, retain A/B/C strata. Current API hash is not historical identity. Do not import S3 publication outcomes. |
| S9 / `vx264-all` / `vx264-all-parts` | `NCT05791201-history-v26`, submitted 2026-10-06; [official history v26](https://clinicaltrials.gov/study/NCT05791201?tab=history&a=26#version-content-panel). Match parts and approved no-results-module state. | Historical panel under registry terms; enrollment/planned endpoints are not observed outcomes. Current API hash is not historical identity; S10 sponsor context cannot replace S9. |

Use the manifest's official/version locators for S13/S18/S19; do not replace
them with live-source search results. A CAPTCHA, 403, missing history panel,
unmatched hash or inaccessible component must be logged with date, route,
result and effect on scope. Do not bypass warnings or infer source absence.
Access may be incomplete while individual field review is valid; neither
fact establishes source completion.

## What the independent reviewer must personally inspect

Read the governing field contract in
[`scripts/q3_classifier.py`](../../../../scripts/q3_classifier.py) and the
rules without running a real-source classifier. For **each field**, check
the permitted primary source at the exact ledger locator, original value
and units, target/part, numerator and analyzed denominator, endpoint
definition, timing/first-administration anchor, attrition and attribution.
Check actual zeros, unfavorable data and missingness as rigorously as
favorable findings. Record agreement, revise, defer or stop with reasons;
do not simply sign an AI packet.

| Source | Existing evidence packet to use, not duplicate | Personal inspection and unresolved challenge |
|---|---|---|
| S13 | [October 28 record](S13/human-source-review-approved-2026-10-28.md), [October 29 closeout](S13/human-source-review-approved-2026-10-29.md), [original packet](../candidates/S13-reviewer-packet.md) | Recheck all 118 field decisions and their scoped omission basis against frozen label sections, including Table 2 in Section 12.2, Table 3 and Table 4/Figure 1 in Section 14. Preserve duration counts 4/12/9 with incompatible printed percentages, medication count/percentage discrepancies, and 16 malignancy reactions versus 15 accounted for in listed categories. Distinguish infections/events/affected people. Keep 25/30 ever independent separate from a common first-infusion 12-month numerator/denominator; N=19 after final infusion is not that denominator. Three pending fields: `overall_followup` enum cannot represent range plus mean; `independence.onset` needs human visual Figure 1 inspection; `other_evidence` ancillary-evidence enum scope needs clarification. Other tracks own proposals; none is adopted here. |
| S18 | [Human packet](S18/human-review-packet.md) and linked AI note | Personally inspect permitted main text including article metadata, sec6.2.2.1, Table 1, population/flow, MMTT and visit denominators, co-interventions, clinical outcomes, harms and limitations; assess permitted mmc1/mmc3 separately. Target all 17 Cohort 2 participants, not only C-peptide-positive participants. All 121 fields await primary human decisions; excluded Table S1 cannot establish omission or fill a value. |
| S19 | [Human packet](S19/human-review-packet.md) and linked AI note | Inspect permitted main text/Section 9 and permission-cleared MOESM1/2/3; all 10 optimized recipients, not responders only. Challenge month-6 primary versus month-12 secondary thresholds, MMTT definitions, visit-specific N, missing visits/withdrawals, immunosuppression and harms. All 121 primary decisions remain pending. Explicitly assess whether unavailable historical restore artifacts prevent replication; do not claim new restore verification. |
| S23 | [Path B packet](S23/path-b-human-review-packet.md) and [approved limited record](S23/human-source-review-approved-2026-10-28.md) | After own access is confirmed, personally inspect main pp. 1-21: DOI/title pp. 1-2, NCT p. 3, Table 1 pp. 3-4, Results/Figures 1-3 and STAR Methods p. 20; separately Methods S1-S7, Tables S1-S2, Figures S1-S5/CONSORT. Recheck all 40 reported fields and the conflict; do not treat prior selected-section review as full coverage. Inspect main Results **175** adverse reactions versus Table S1 p. 10 parenthesized grades 175+24+4+2=**205**, distinct from restricted-category subtotal 151. Grade 3/4 events are not automatically serious events; three serious reactions affected two people. Check Methods S3 prednisone 09/11, S4 patient 15 device exception, seven discontinuations and withdrawal-category uncertainty, week-26/52 visit denominators and missing severe-hypoglycemia counts. Zero reported independence is not a verified fixed-week52 analyzed denominator. Eighty fields remain pending. |
| S20 | [Existing packet](../candidates/S20-reviewer-packet.md) and linked candidate JSON | Personally inspect frozen history identification, arms/interventions, flow, baseline, outcome and adverse-event modules at candidate selectors. Challenge 47 Cohort 2 Started versus 49 overall enrollment and treated N; Week-26 C-peptide analyzed N=42 is surrogate context, safety N=47 through Week 104 is not Cohort 1's window. Event term Hypoglycemia is not automatically the frozen severe endpoint. All 121 primary decisions pending; candidate coverage is not full-source review. |
| S17 | [Ten-field approval](S17/human-source-review-approved-2026-10-28.md), [human checklist](S17/human-review-checklist.md) and [packet](../candidates/S17-reviewer-packet.md) | Personally verify the ten approved fields at their version-prefixed registry selectors, including explicit Cohort 2 no-enrollment statements, baseline group and outcome descriptions. Planned 4-or-6 VC-01 implants plus up to 3 sentinel units are not exposure; Cohort 1's 19 participants/safety cannot supply Cohort 2 results. Remaining 111 fields and relevant permitted linked material need actual primary review; no enrollment is not zero responders or treatment failure. |
| S4 | [Existing packet](../candidates/S4-reviewer-packet.md) and linked candidate JSON | Inspect historical title, structured phase, arm/part mapping, enrollment, outcomes and results-module absence. Preserve title versus structured-phase discrepancy; estimated 57 mixed-protocol participants is not A/B/C treated N. Endpoint anchors (Day 90, one year after infusion, one year after independence) differ. All 121 primary decisions pending; no borrowing Part D or publication results. |
| S9 | [Existing packet](../candidates/S9-reviewer-packet.md) and linked candidate JSON | Inspect historical identification, enrollment, part mapping, planned outcomes and results-module absence. Overall actual enrollment 7 is not treated N or part-specific denominator; Part B baseline-to-Day-90 C-peptide and Parts A/B Day-1-to-24-month safety are plans, not observations. All 121 primary decisions pending; absent results never mean no harms. |

For every source, record actual components/pages/selectors inspected,
inaccessible or excluded components, field IDs challenged and decisions,
discrepancies with both locators, remaining access/rights limits and
replication limits. Use source-specific review artifacts and the existing
ledger/log workflow in a separately authorized change; do not invent a
second authoritative field inventory. This preparation changes none of them.

## Six PEC links: separate two-sided human challenge

All six rows are still `uncertain` with no human reviewer/date or specific
two-sided locators. Candidate linkage analysis by another track is a proposal,
not identity adjudication. The independent reviewer must personally inspect
both permitted frozen sources for each pair, challenge the primary
adjudication, and record two version-specific locators, reviewer/date,
relationship rationale and any subset direction, or an explicit unresolved
blocker. S23-side inspection requires the separate lawful-access workflow.

| Frozen pair | Evidence to inspect and decision still required |
|---|---|
| S18 / S19 | Full 17-person versus optimized 10-person population definitions, treatment/device configuration, recruitment/site/time descriptions and permitted explicit overlap statements; do not infer subset from sample sizes. |
| S18 / S23 | Full 17-person versus 15-person site definitions and S23 Table 1's six Shapiro E-series cross-references, checked on both sides. Preregistration documents overlap; do not assert distinct populations, a directional subset or complete identity without evidence. |
| S18 / S20 | Publication methods/registration versus frozen registry Cohort 2 flow, sites, exposure and analysis populations; shared NCT is not identical participants or endpoint attribution. |
| S19 / S23 | Optimized 10-person and 15-person site eligibility, devices, dates and explicit population statements; neither cross-study identifiers nor denominator similarity alone prove linkage. |
| S19 / S20 | Optimized publication population versus registry Cohort 2 arm/flow/outcome groups, time and device definitions; no borrowed registry denominator. |
| S23 / S20 | Site publication flow/Table 1/CONSORT versus registry Cohort 2 flow/arms/results and windows; establish or explicitly block participant/endpoint mapping. |

No participant-level reconstruction or excluded supplement access is allowed.
Retaining `uncertain` is legitimate after actual review if reasons and
two-sided evidence are recorded; a blank untouched row is not a reviewed
uncertainty. A decisive unresolved linkage must remain a named gate blocker,
not be silently accepted or used for pooling.

## Independent reviewer onboarding and access requirements

**Nomination only:** Issue #59 records `@joe-ucp` as invited by the maintainer.
Affirmative acceptance, consent to the public review/signoff scope,
qualifications, conflicts/independence disclosure and S23 individual lawful
access are all **PENDING**. Repository read access proves none of these.
This handoff makes no professional claim or personal inference about the
nominee, contacts or assigns nobody, and does not attest on anyone's behalf.

| Step / responsible human | Required evidence before proceeding | Current state |
|---|---|---|
| Acceptance / nominee | Reviewer personally agrees, with date, to eight sources, 968 fields and six link challenges; states any limits and consent to public attribution. | PENDING |
| Qualifications / reviewer, assessed by maintainer | Reviewer supplies relevant source-extraction, clinical-trial endpoint/denominator, safety, provenance and overlapping-cohort expertise and limitations. Maintainer documents suitability or obtains additional qualified coverage. Do not publish unnecessary personal details or unverified credentials. | PENDING |
| Independence / reviewer, assessed by maintainer | Own dated disclosure of relevant preparation/adjudication roles, prior repository contributions and financial/intellectual/professional conflicts; reviewer must be distinct from each relevant primary human reviewer and preparatory AI. Maintainer assesses scope and any need for replacement/additional review. No inferred independence from a nomination. | PENDING |
| Repository onboarding / reviewer | Pin review commit; read CONTRIBUTING, charter, evidence framework, frozen rules, manifest, ledger/log, source packets and gate notes. Independently reproduce deterministic checks if able, stating exact replication scope and limits. Read permission does not grant source rights. | PENDING |
| Individual source access / reviewer | Own dated component-by-component access record for all eight sources, version match, terms and permitted scope; failed attempts/rights limits stay explicit. No credentials, private paths, tokens, private URLs or restricted files in public artifacts. | PENDING |
| S23 restricted onboarding / reviewer and maintainer | Reviewer obtains own subscription, purchase, institutional entitlement or explicit publisher permission; records route/date and components personally opened without exposing account details. Maintainer documents separate authorized human review scope before inspection; nomination alone does not extend the existing sole-reviewer Path B authorization. | PENDING |
| Human primary adjudications / authorized primary reviewers | Complete lawful source review and field dispositions in existing workflow, with precise scope and unresolved discrepancies. Other agents' source/cohort/S13 proposals require human disposition and cannot substitute. | PARTIAL |
| Independent findings / reviewer | Own dated, human-authored findings per source/field and per link, exact locators, disagreements, access/rights limits, replication scope and scientific decision. AI technical review and green CI are not this review. | PENDING |

### S23 governance exception remains a separate blocker

The [October 28 record](S23/human-source-review-approved-2026-10-28.md)
documents assistant inspection of a chat-uploaded supplement outside the
approved human-only Path B restriction. Keep that exception visible and
separate from the lawful primary human field attestations. It does not grant
permission for further uploads, shared/forwarded PDFs, AI source inspection
or common storage. Independent access must not use that copy.

Before any acceptance, the authorized maintainer must record a dated
governance disposition identifying the exception, rights/provenance
consequences, any necessary remediation and the authorized independent
access/review plan. The reviewer must disclose the effect on replication and
personally recheck the relevant permitted evidence through their own access.
If rights or version identity cannot be established, log the precise scope
as blocked; neither this packet nor CI can waive it. Do not put source copies,
private account/access details or restricted content into that disposition.

## Dated decision requirements: maintainer only

**As of 2026-10-29 no decision below has been executed by this handoff.**
After full independent review, only the authorized maintainer may post the
explicit dated G2-B decision on
[Issue #34](https://github.com/aditmer/type1-diabetes-cure-research/issues/34),
cross-linking #59. The record must identify the exact reviewed ledger and
review-artifact commits, primary reviewers/scope, independent reviewer and
dated findings, all eight version/access checks, all six link decisions,
discrepancy and rights/governance dispositions, checks and remaining limits.

| Decision | Required human basis and consequence |
|---|---|
| `accept` | Only after full primary adjudication and separate qualified independent scientific review of the entire eight-source ledger and six links; frozen validation contract truly satisfied; decisive version/access/rights/denominator/endpoint/timing/attrition conflicts resolved or explicitly assessed with a justified disposition that does not conceal a blocker. S23 own access and governance exception must be addressed. Maintainer states rationale and exact accepted scope/date. Only a separate explicit maintainer action after this acceptance may record #35 unblocked; this preparation does not do so. |
| `revise` | After reviewing independent findings, specify exact source/field/link defects, responsible human roles and evidence needed; require re-review of changes and affected downstream mappings. G2-B pending and #35 blocked. |
| `defer` | After reviewing independent findings, name unresolved access, qualification, rights, source completeness or scientific blockers and dated conditions for reconsideration. No implied acceptance; #35 blocked. Before full review is available, a dated administrative defer may record the wait but cannot stand in for the final review-based decision. |
| `stop` / NO-GO | Record why review cannot lawfully or scientifically support continuation, affected scope and conditions (if any) for reopening. Preserve audit history and unresolved identities; no real-source execution. |

Do not check off completion flags, accept G2-B, unblock #35, close #34/#59,
or run real-source paired classifiers, robustness or outcome analysis as
part of this preparation. G3 #36 remains later. PR merge, nomination, primary
field approval, synthetic controls and AI code review are not scientific
acceptance.

## Safe deterministic readiness checks

The following commands inspect repository metadata or synthetic fixtures,
not external sources or real-source outcome classifications:

```sh
python3 scripts/validate_data.py
python3 scripts/validate_q3_extraction.py
python3 scripts/validate_q3_candidates.py
python3 -m unittest discover -s tests -v
python3 -m scripts.q3_synthetic --output-dir /tmp/q3-reviewer-synthetic-UNIQUE
git diff --check
```

Use a fresh task-specific synthetic output directory, record the actual
commands/results and reviewed commit, and keep generated output outside the
repository. Deterministic passes establish structural consistency only, not
source truth, rights, qualifications, exhaustive clinical review or scientific
approval. Preserve the authoritative trackers, all original field records,
frozen schemas/versions, restrictions and unresolved identities.
