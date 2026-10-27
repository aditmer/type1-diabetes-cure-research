# S9 human-review packet

- **Review status:** pending; candidate evidence is not adjudicated.
- **Report/target:** Q3-S9; all VX-264 recipients or planned recipients, retaining part distinctions.
- **Approved source:** ClinicalTrials.gov history v26, submitted 2026-10-06; `NCT05791201-history-v26`.
- **Version locator:** [ClinicalTrials.gov history v26](https://clinicaltrials.gov/study/NCT05791201?tab=history&a=26#version-content-panel). The panel's internal request index is `/history/25`; it is not the version label. No byte-identical historical JSON archive is claimed.

## Candidate evidence to inspect

The field-level values, precise historical record locators, population scopes, denominators, endpoint timings, and limitations are in [`S9-candidates.json`](S9-candidates.json). Reviewable candidate fields: `counts.enrolled`, `identity.design`, `identity.disease_stage`, `identity.eligibility`, `identity.intervention`, `identity.mapping`, `identity.population`, `population_identified`, `safety.harms`, `safety.window`.

Key review points:

- The registry lists actual overall enrollment=7. It does not establish that all 7 were treated, how participants split across parts, or any outcome denominator.
- The Part B peak C-peptide endpoint is planned from baseline to Day 90; it is not an observed patient-important endpoint.
- Parts A/B have a planned adverse-event endpoint from Day 1 up to 24 months. No results module is posted in this version; that does not mean no adverse events occurred.
- Keep Part A and Part B endpoint windows and populations separate where the approved record permits; do not infer participant-level part assignment.
- S10 is contextual only and must not be used to replace the approved S9 source.

## Human decisions required

1. Confirm whether overall actual enrollment=7 is in scope for the frozen target; do not call it treated count or endpoint denominator.
2. Verify any part-specific participant mapping the approved record actually supports; preserve uncertainty where it does not.
3. Keep the Part B C-peptide endpoint planned and unobserved, with the baseline-to-Day-90 window.
4. Confirm the safety endpoint is a plan only; do not infer no harms from `hasResults=false`.
5. Determine whether complete permitted review supplies observed P1 outcomes, denominators, treatment exposure, immunosuppression, or follow-up.

## Unresolved fields and limits

`unresolved_field_count` is **111**. The unresolved set is exactly the 121 `SPECS` field IDs in `scripts/q3_classifier.py` minus this packet's reviewable `candidate_field_ids` listed above. Enrollment and planned outcomes do not establish treated counts or observed endpoints. The official ledger and review gates remain unchanged; Issue #35 remains blocked.
