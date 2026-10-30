# Wave 2 PEC-Direct: one six-link human decision batch

**Recommendation: retain `uncertain` and empty subset direction for all six
links.** This is an explicit recommended disposition, not a human decision.
Known S18/S23 partial overlap remains visible; S19 overlap is not assumed
distinct. Related registry records are not participant identities. No matched
count, pooled population, unique-person total or borrowed endpoint is proposed.

For #34 / #58, baseline `7432cd3cb3bc1075706b12c50ab7156bc71ddb8c`.
The [structured batch](pec-direct-wave2-adjudication-2026-10-29.json) is the
decision inventory: four exact frozen identities, inherited evidence records,
supporting and counterevidence per pair, precise access/review blockers, and
six concrete human decisions with thresholds for changing the recommendation.
Display order follows `cohort-links.csv`; it does not imply subset direction.

## What this establishes, and what it inherits

New work is the explicit six-row decision recommendation and the distinction
between a plausible linkage and sufficient evidence for each alternative.
**No new primary-source evidence or access resolution is claimed.** No primary
source was retrieved. Other Wave 2 streams own source retrieval; this proposal
does not depend on their unmerged work for its six recommendations.

PR #66's main-prose population locators for S18/S19 are inherited AI
annotations, not primary human verification. Its hash-reproduction statements
describe that earlier task, not a new verification here. S20 population/flow
locators remain inherited candidates, not a new historical-panel inspection.
S23 identity annotations have limited human field approval, not six-link or
full-source approval. The existing preregistration and approved review record
constrain interpretation; this proposal does not elevate candidate evidence.

| Source | Exact approved version | Full fixed target / subcohort |
|---|---|---|
| S18 / Q3-S18 | `PMC8714853.1` | `pec-s18-target` / `pec-s18-all`: all 17 publication participants |
| S19 / Q3-S19 | `PMC11471599.1` | `pec-s19-target` / `pec-s19-optimized-all`: all 10 optimized recipients |
| S23 / Q3-S23 | `publisher-pdf-human-copy-2026-10-23` | `pec-s23-target` / `pec-s23-site-all`: all 15 Vancouver implanted participants |
| S20 / Q3-S20 | `NCT03163511-history-v20` | `pec-registry-cohort2` / `pec-registry-cohort2-all`: planned efficacy Cohort 2, not Cohort 1 or overall enrollment |

All four remain `pec-direct`. Frozen manifest version locators, rights and
hash provenance are unchanged. The structured evidence registry points back
to exact existing records and source locators, without reproducing restricted
material or participant-level details.

## Six recommendations and actual decisions needed

Every row recommends **`uncertain`, direction empty**. Counterevidence below
includes evidence against overconfident alternatives and limitations; where
no affirmative contradiction proves non-overlap, it says so rather than
manufacturing one.

| Pair | Supporting aggregate context | Counterevidence / limiting evidence | Concrete human decision and alternative threshold |
|---|---|---|---|
| S18-S19 | Cohort 2 publication population; S19 cites S18 as an earlier group. | Optimized strategy and chronology counter automatic sameness but do not prove different people. No affirmative proof of disjointness. | Determine whether aggregate cadre wording explicitly excludes repeat membership across both complete targets. Only explicit non-overlap supports `distinct_within_program`; otherwise retain `uncertain`. |
| S18-S23 | Known partial overlap; existing S23 cross-reference clues. | Overlap rules out `distinct_within_program`; 17-person versus 15-person full targets counter `same`. Smaller size does not establish inclusion. | Retain `uncertain` with known partial overlap unless the human verifies **every S23 member** lies in the frozen S18 population. Only then consider `subset`, `to_is_subset_of_from` in this display order. No matched count is inferred. |
| S18-S20 | S18 describes a publication selection within Cohort 2. | Publication data-cut selection and v20 STARTED accounting are not interchangeable. Registry identity is not membership evidence. | Verify complete S18 inclusion under exact v20 Cohort 2 definitions and data-cut accounting. Only explicit aggregate inclusion supports `subset`, `from_is_subset_of_to`; otherwise retain `uncertain`. |
| S19-S23 | S19 cites the earlier S23 report in the shared program. | Later optimized cadre does not establish re-enrollment exclusion; S18/S23 overlap cannot be transferred to S19. | Determine whether aggregate prose excludes any S23-target membership in S19. Only verified two-sided non-overlap supports `distinct_within_program`; otherwise retain `uncertain`. |
| S19-S20 | S19 optimized cadre is described in Cohort 2. | Cadre/device amendments and enrollment interval require version-specific mapping; common labels do not prove inclusion. | Verify all ten optimized recipients belong to v20's cohort definition. Only explicit inclusion supports `subset`, `from_is_subset_of_to`; otherwise retain `uncertain`. |
| S23-S20 | Site report shares the trial registration. | Allocated/implanted/site-analysis scope is not automatically registry STARTED scope. S18 overlap does not prove registry inclusion. | Assigned Path B human verifies all 15 site participants map to exact v20 Cohort 2 accounting. Only explicit complete inclusion supports `subset`, `from_is_subset_of_to`; otherwise retain `uncertain`. |

For any `same` alternative, require aggregate evidence of full membership
equivalence across the exact two targets. For any subset alternative, require
complete inclusion and a direction, not merely some overlap. Neither absence
of a crosswalk nor inability to access it is evidence of no overlap.

## Exact access and review blockers

**S18 / B18:** PR #66's aggregate leads are Results `sec2/p0120` and STAR
Methods `sec6.2.2.1/p0045`. The separate
[S18 packet](../reviews/S18/human-review-packet.md) records a broad-page
response exposing participant-level material and stopped extraction. Do not
silently override that stop using PR #66's earlier annotations. Source owners
must establish safely version-bound aggregate-only review; a human must
verify the population passages. `mmc2.xlsx` and participant-level information
remain excluded. No supplement omission is inferred.

**S19 / B19:** inherited leads are Main `Sec1/Par7`, Methods
`Sec9/Par31,Par33`, references `CR17` and `CR18`. These do not resolve repeat
participation. Original private historical-restore bytes and verifier output
remain unavailable; new public retrieval would not recreate those artifacts.
Item-level third-party rights review is pending. No MOESM4, rights-pending
material or participant-level reconstruction is permitted. The
[existing packet](../reviews/S19/human-review-packet.md) expressly does not
authorize its endpoint candidates to resolve cohort links.

**S23 / B23:** use only the
[existing limited human annotations](../reviews/S23/human-source-review-approved-2026-10-28.md).
The assigned human `@aditmer`, not the agent, must inspect Table 1 pp. 3-4
and supplement Methods S2 CONSORT p. 4 through lawful individual Path B access.
No publisher file retrieval, inspection, upload, common archive or forwarded
PDF is authorized here. Existing access attestation is not a new hash test;
editorial-version sequence and storage/sharing permission remain unresolved.
A separate independent reviewer needs their own lawful access. The earlier
upload/assistant-inspection governance exception remains unresolved.
The existing **`safety.harms` conflict and incomplete source review remain
visible and unchanged**; no cohort decision reconciles that discrepancy.

**S20 / B20:** verify selected history panel `a=20`, submitted 2024-11-07,
Cohort 2 design/arm definitions and `participantFlowModule` STARTED accounting.
Full paths are in the structured evidence registry and
[existing packet](../candidates/S20-reviewer-packet.md). Historical JSON
previously returned HTTP 403; this cohort task performed no fresh access. Internal
`history/19` is an index, not version 19. The current-API hash is not
historical-v20 byte identity. Preserve the approved official locator method;
do not bypass access restrictions or substitute current data.

### Supplementary source-stream relays (not baseline evidence)

On 2026-10-29, source session
`801aae73-970d-4ed3-9f27-1db700a9795c` reported an S18 HEAD-only HTTP 200,
without a response body or new identity/hash check; it retained the prior
extraction stop. It also reported fresh S19 XML HTTP 200, 122,548 bytes and
the exact manifest hash. The XML lacks `pmcid-ver`; this does not establish
an editorial version or recover private restore artifacts. No overlap claim
was established. The stream subsequently confirmed author-prose locators
`Sec9/Par31` (ten-person cadre), `Sec9/Par33` (most recent cadre, enrollment
August 2020 through October 2021, changed device strategy), and reference
metadata `CR17`/`CR18` for S18/S23. This newly inspected aggregate evidence
corroborates PR #66's chronology leads, but does not exclude re-enrollment
or prove distinct participants. It involved no S23 publisher inspection.

Registry session `5343856a-8a34-4b72-b135-831247a45dd4` reported successful
official S20 browser access at `a=20`, title `ver.20:2024-11-07` and
`Viewing V20`, with aggregate Study Design and Overall Study Participant
Flow inspection. This relieves the historical **browser-access** obstacle
according to the source-owning stream; it does not recover historical JSON
or establish publication membership. Prior JSON HTTP 403 and byte-provenance
limitations remain distinct.

These are attributed source-stream reports, not independently repeated
retrievals, new human approvals or evidence incorporated from an unmerged PR.
Their exact provenance is preserved in `later_source_stream_updates` in the
companion. All six recommendations are unchanged. The source streams'
separate version-bound packets should be reviewed for their primary checks.

## One batch, no simulated approval

The human reviews these six decisions together, not six separate prompts.
For each row, record the actual relationship (including a deliberate
`uncertain` decision), direction if applicable, both exact versions and
targets, aggregate locators and components actually inspected, rationale,
remaining blockers, actual reviewer and date. If evidence does not meet the
stated alternative threshold, the actionable decision is to retain
`uncertain` with that exact limitation, not to seek prohibited case-level data.

The JSON contains no filled approval records. An authorized later change
may record human decisions in `cohort-links.csv`; this PR changes none.
Human cohort disposition, source-wide completeness, and independent
eight-source scientific approval are distinct gates. Independent scientific
review and explicit dated maintainer acceptance under #59 are still required.
**G2-B remains unaccepted; #35 remains blocked.** No real-source paired
classification or G2-C output was run.

## Baseline and mechanical verification

Before writes: PRs #63-#73 merged, baseline CI successful, tracker/extraction/
candidate validators passed, 286 unit tests and seven synthetic controls
passed. Direct ledger counts: eight reports, 121 fields each, **83 reported,
85 reviewed omissions, 1 conflicting, 799 pending**, six uncertain links and
no independent acceptance. Wave 1 changed no frozen or authoritative files.

Final checks passed: all three existing validators, **298 unit tests**
(including 12 new proposal checks), seven synthetic controls and staged
`git diff --check`. Exact baseline comparison confirmed only these two new
proposal files and the unique test file changed; all existing files,
including PR #66, frozen rules, manifest, field objects, review flags and
cohort links, are byte-unchanged. Main was re-fetched and remained the exact
baseline. Proposal tests check pair inventory, frozen identities, inherited
provenance, two-sided evidence, pair-specific thresholds, explicit blockers
and no approval/pooling/classification records. These are machine checks,
not scientific source validation.
