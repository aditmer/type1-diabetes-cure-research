# S18 Wave 2: aggregate-access decision

**Extraction remains stopped, not completed.** Baseline:
`7432cd3cb3bc1075706b12c50ab7156bc71ddb8c`; Issues #34 and #55.
The [structured decision](S18-wave2-access-decision-2026-10-29.json) holds six
prior aggregate leads, proposes **zero newly source-verified candidates**, and
leaves all 121 authoritative S18 fields pending. No existing packet or ledger
is edited.

## What was actually attempted

On 2026-10-29, HEAD requests to the approved Europe PMC XML endpoint
(21:17:51 UTC) and official `PMC8714853.1` locator (21:19:17 UTC) returned
HTTP 200, XML and HTML respectively. No response body was requested or
inspected. These checks establish reachability only, **not exact-version
identity, matching bytes, content access, or scientific verification**.
The manifest's 114,747-byte XML SHA-256
`2c33d10d93cd399fadef190447f2ea5778625c476405f3e6cb011eb94e792433`
was not recomputed here.

The existing S18 packet documents broad-page participant-level exposure and
an extraction stop. Reopening the same mixed-content article merely to
remove participant material afterward would not satisfy this workstream's
access boundary. No full-body retrieval, participant table inspection,
supplement retrieval, or reconstruction was attempted. This is a concrete
scope/access blocker, **not a network failure** and not completed access
exhaustion. Earlier AI checks are historical annotations, not new inspection
or human review.

## Field-level disposition, not another extraction claim

| Prior lead held | Decision now | Verification needed |
|---|---|---|
| Full 17-person Cohort 2 publication population | Keep identity/enrollment fields pending; never select six responders | Safe aggregate population/design and dose passages |
| Common immunosuppression regimen | Keep regimen/exposure pending | Exact drugs, regimen, duration and co-interventions |
| Detectable stimulated C-peptide 6/17 at varying visits | Keep as unverified surrogate lead, not a ledger clinical outcome | Aggregate endpoint definition and actual visit denominators; no participant-table reconstruction |
| 297 adverse events in first 12 months | Keep harms/window pending | Event count, population and time basis |
| 10 serious events in six people | Keep harms/attribution/discontinuations pending | Separate events from affected people and verify attributed causes |
| Secondary measures and lack of measurable clinical benefit | No numeric result, zero or omission proposed | Permitted aggregate patient-important evidence, not excluded numeric material |

Locators in the JSON are **prior locator leads**, not passages reverified in
this workstream. In particular, variable follow-up does not establish a
month-12 analysis population; 17 enrolled/treated cannot be reused as every
endpoint denominator. Attrition, censoring, missing-data handling and actual
clinical endpoint coverage remain unavailable in the current safe review
scope. They are not established as unreported in the source.

## One consolidated human batch

1. Establish a lawful aggregate-only review surface: the authorized
   human/source custodian verifies the exact approved XML hash and embedded
   `PMC8714853.1` identity, and records the permitted passages and scope.
   Provide factual attestations and precise locators, not participant data,
   excluded files, copied protected expression or figures. If this cannot be
   done safely, retain the blocker rather than widen automated access.
2. Verify or reject the six held leads together, including population,
   device/procedure exposure, endpoint-specific denominators and actual
   times from first cell administration, immunosuppression, harms and
   aggregate attrition. State which facts remain inaccessible versus simply
   unreviewed; do not fill unknowns with zero.
3. Decide lawful aggregate-only scope for unreviewed mmc1/mmc3 after
   item-specific rights/identity checks. **mmc2.xlsx remains excluded**;
   exclusion is not source omission and is not cured by inspecting,
   reconstructing or inferring its contents.

No human attestation, independent scientific approval, cohort adjudication,
completion flag, real-source classification or G2-B acceptance is recorded.
Machine checks only establish proposal structure and preserved boundaries.
Attribution: Shapiro et al. (2021), DOI `10.1016/j.xcrm.2021.100466`,
CC BY-NC-ND 4.0; factual annotations only.
