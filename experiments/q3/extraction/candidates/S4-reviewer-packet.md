# S4 human-review packet

- **Review status:** pending; candidate evidence is not adjudicated.
- **Report/target:** Q3-S4; VX-880 Parts A/B/C, retaining part strata; exclude VX-017 Part D.
- **Approved source:** ClinicalTrials.gov history v32, submitted 2026-08-27; `NCT04786262-history-v32`.
- **Version locator:** [ClinicalTrials.gov history v32](https://clinicaltrials.gov/study/NCT04786262?tab=history&a=32#version-content-panel). The panel's internal request index is `/history/31`; it is not the version label. No byte-identical historical JSON archive is claimed.

## Candidate evidence to inspect

The field-level values, precise historical record locators, part mappings, denominators, endpoint timings, and limitations are in [`S4-candidates.json`](S4-candidates.json). Reviewable candidate fields: `hba1c.attribution`, `hba1c.observation`, `identity.design`, `identity.disease_stage`, `identity.eligibility`, `identity.intervention`, `identity.mapping`, `identity.population`, `insulin_independence.attribution`, `insulin_independence.observation`, `population_identified`, `safety.harms`, `safety.window`, `severe_hypoglycemia.attribution`, `severe_hypoglycemia.interval_start`, `severe_hypoglycemia.observation`.

Key review points:

- The master protocol includes VX-880 and VX-017; Part D is outside the frozen VX-880 target. Do not borrow Part D participants or outcomes.
- The registry's structured Phase 3 value and its title's Phase 1/2/3 VX-880 and Phase 1/2 VX-017 descriptions differ. Preserve both source statements; do not reconcile them automatically.
- Enrollment 57 is estimated for the mixed master protocol, not actual VX-880 Parts A/B/C enrollment or an endpoint denominator.
- The listed insulin-independence, SHE, HbA1c, and safety outcomes are plans; this approved version has no results module.
- Preserve endpoint-specific parts and anchors. In particular, one year after achieving independence differs from one year after infusion; Day 90 and “one year” must not be converted into an unstated fixed numeric endpoint.

## Human decisions required

1. Verify each endpoint's VX-880 part mapping and exclude VX-017 Part D.
2. Preserve the structured phase and title statements separately; resolve framing only through human source review.
3. Verify each planned outcome's exact definition, part, interval, and anchor. Do not infer observed results, denominators, or fixed numeric time points.
4. Keep estimated enrollment 57 as mixed-protocol context only.
5. Confirm the absence of a results module in the approved version without treating it as clinical failure.

## Unresolved fields and limits

`unresolved_field_count` is **105**. The unresolved set is exactly the 121 `SPECS` field IDs in `scripts/q3_classifier.py` minus this packet's reviewable `candidate_field_ids` listed above. Planned outcomes and absent registry results do not resolve observed outcomes. The official ledger and human-review gates remain unchanged; Issue #35 remains blocked.
