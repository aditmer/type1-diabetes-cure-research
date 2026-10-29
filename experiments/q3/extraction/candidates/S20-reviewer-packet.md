# S20 human-review packet

- **Review status:** pending; candidate evidence is not adjudicated.
- **Report/target:** Q3-S20; planned efficacy Cohort 2 of the PEC-Direct registry, not Cohort 1 safety.
- **Approved source:** ClinicalTrials.gov history v20, submitted 2024-11-07; `NCT03163511-history-v20`.
- **Version locator:** [ClinicalTrials.gov history v20](https://clinicaltrials.gov/study/NCT03163511?tab=history&a=20#version-content-panel). The history panel's internal request index is `/history/19`; it is not the version label. No byte-identical historical JSON archive is claimed.

## Candidate evidence to inspect

The field-level values, precise historical record locators, population scopes, denominators, endpoint timings, and limitations are in [`S20-candidates.json`](S20-candidates.json). Reviewable candidate fields: `population_identified`, `identity.population`, `identity.disease_stage`, `identity.eligibility`, `identity.intervention`, `identity.dose`, `identity.design`, `identity.mapping`, `counts.enrolled`, `other_evidence`, `safety.population`, `safety.window`, `safety.harms`.

Key review points:

- The candidate Cohort 2 participant-flow Started count is 47. The record's actual overall enrollment is 49; do not conflate overall enrollment with Cohort 2, or either with a treated count.
- The Cohort 2 C-peptide result is a baseline-to-Week-26 surrogate result with analyzed N=42, not N=47 and not a P1 patient-important outcome.
- Cohort 2 safety is reported for 47 at risk through Week 104. Cohort 1 safety and its Week-26 window must remain separate.
- The serious-event term “Hypoglycemia” is not established as the frozen severe-hypoglycemia endpoint. Preserve the event term, participant/event counts, and frequency threshold without reclassifying it.
- The versioned registry-to-publication relationship remains uncertain. Do not edit the six PEC-Direct cohort links based on this packet.

## Human decisions required

1. Verify the Cohort 2 Started count and its use as the frozen enrollment fact; distinguish it from 49 overall and from treated participants.
2. Verify the Week-26 C-peptide result, units, summary statistics, and N=42.
3. Review the cohort-specific safety denominators/windows and determine whether any event wording can support a frozen SHE field.
4. Keep Cohort 1 context separate and leave all cohort links unchanged.
5. Determine whether the full permitted record supplies target-linked observed insulin, HbA1c, CGM, fixed-horizon, immunosuppression, and attrition evidence.

## Unresolved fields and limits

`unresolved_field_count` is **108**. The unresolved set is exactly the 121 `SPECS` field IDs in `scripts/q3_classifier.py` minus this packet's reviewable `candidate_field_ids` listed above. The Week-26 C-peptide endpoint is surrogate/contextual evidence and does not resolve a P1 endpoint. Absence from the candidate set is not an accepted disposition. Human and independent review remain pending; the official ledger, cohort links, and Issue #35 gate remain unchanged.

## Candidate provenance update — 2026-10-29

This update records the current evidence boundary; it is not a new source
review. The candidate facts and their frozen-version-prefixed field locators
remain in [`S20-candidates.json`](S20-candidates.json). The key paths for
human verification are:

- Cohort 2 flow: `resultsSection.participantFlowModule.periods[Overall Study].milestones[STARTED].achievements[group=Cohort 2]`.
- Cohort 2 C-peptide result: `resultsSection.outcomeMeasuresModule.outcomeMeasures[Change in C-peptide for Cohort 2 Subjects]`.
- Cohort 2 adverse events: `resultsSection.adverseEventsModule.eventGroups[title=Cohort 2]`, including its `timeFrame`, `seriousEvents`, and `frequencyThreshold`.

The approved source remains `NCT03163511-history-v20`, at
https://clinicaltrials.gov/study/NCT03163511?tab=history&a=20#version-content-panel.
The prior source-status note records HTTP 403 for the historical JSON endpoint.
No historical page was reopened in this preparation, and the current API
snapshot/hash is not a substitute for the frozen history. The 47 Cohort 2
Started count, 49 whole-study enrollment, Week-26 C-peptide result, and
Week-104 safety facts therefore remain candidate-only.

Repository materials reviewed for this update: Issue #57, the frozen source
manifest, this candidate file, and this packet. No new primary-source sections
were reviewed; no field status, reviewer identity/date, cohort link, or
independent-review state was changed. The 108-field unresolved complement
remains exactly as stated above.

**Still unresolved:** human verification of Cohort 2 enrollment versus actual
treatment exposure; endpoint-specific denominators and timing; whether any
registry event wording meets the frozen severe-hypoglycemia definition; and
any exact evidence for a publication-cohort relationship. Do not equate
“Hypoglycemia” with severe hypoglycemia or infer participant identity from
the registry identifier.
