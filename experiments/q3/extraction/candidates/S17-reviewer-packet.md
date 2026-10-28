# S17 human-review packet

- **Review status (2026-10-28):** primary human checklist review and approval of ten specific S17 fields recorded in [merged PR #49](https://github.com/aditmer/type1-diabetes-cure-research/pull/49); **111 fields still pending**. This original nine-field candidate packet is a historical pre-review artifact, not the updated authoritative ledger.
- **Report/target:** Q3-S17; planned efficacy Cohort 2 only, not Cohort 1.
- **Approved source:** ClinicalTrials.gov history v13, submitted 2022-02-25; `NCT02239354-history-v13`.
- **Version locator:** [ClinicalTrials.gov history v13](https://clinicaltrials.gov/study/NCT02239354?tab=history&a=13#version-content-panel). The panel's internal request index is `/history/12`; it is not the version label. No byte-identical historical JSON archive is claimed.

## Candidate evidence to inspect

The fresh current-API hash reconciliation and exact-field candidate checks are
in the [2026-10-27 AI-assisted verification](../reviews/S17/ai-assisted-evidence-verification-2026-10-27.md).
It does not establish byte identity to an archived history-v13 JSON and does
not replace human field review.

The field-level values, precise historical record locators, population scopes, denominators, endpoint timings, and limitations are in [`S17-candidates.json`](S17-candidates.json). Reviewable candidate fields: `counts.enrolled`, `identity.design`, `identity.disease_stage`, `identity.eligibility`, `identity.intervention`, `identity.mapping`, `identity.population`, `population_identified`, `target_enrolled`.

Key review points:

- The approved history's participant-flow record shows Cohort 2 Started=0; Cohort 1 Started=19, matching the whole-study actual enrollment. The zero is candidate source evidence only, not a human-adjudicated no-enrollment conclusion.
- The Cohort 2 C-peptide result row has denominator 0 and no numerical outcome. This is not a zero clinical response.
- Cohort 1 adverse-event results (19 participants) are safety context only and must not be assigned to Cohort 2.
- `target_enrolled=false` and `counts.enrolled=0` were primary-human-approved on 2026-10-28 with explicit no-enrollment wording, not merely `STARTED=0`. This does **not** approve a report-level classification or any observed efficacy outcome; independent review and G2-B acceptance remain pending.

## Human decisions required

1. Verify the Cohort 2 Started=0 entry in the exact v13 record and decide whether it establishes the frozen target enrollment fact.
2. Keep the candidate zero enrollment distinct from zero responders; determine the authorized ledger disposition through human adjudication.
3. Verify Cohort 1 enrollment and safety separately, without treating it as Cohort 2 efficacy evidence.
4. Confirm the zero-denominator C-peptide row is Cohort 2 and is not an observed zero outcome.
5. Determine whether permitted registry material supplies target treatment exposure, immunosuppression, harms, or fixed-horizon outcomes.

## Unresolved fields and limits

`unresolved_field_count` is **112**. The unresolved set is exactly the 121 `SPECS` field IDs in `scripts/q3_classifier.py` minus this packet's reviewable `candidate_field_ids` listed above. This is the original 2026-10-27 candidate inventory, so its **112** unresolved count represents the pre-review nine-candidate coverage, **not** today's authoritative ledger. As of 2026-10-28 the ledger contains ten primary-human-reviewed fields and **111 still unextracted**, including the revised `identity.dose` with planned sentinel units. The old candidate inventory remains an audit snapshot. No report-level `not_applicable` classification has been executed; independent review and Issue #35 authorization remain blocked.
