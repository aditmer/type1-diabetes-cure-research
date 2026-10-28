# S13 human-review packet

- **Review status:** pending; candidate evidence is not adjudicated.
- **Report/target:** Q3-S13; all treated Lantidra participants in both pooled label studies, including repeat infusions.
- **Approved source:** DailyMed SPL v3, `SPL-v3-a3163e14-0404-4e27-884b-f6f9f7f695bc`.
- **Version locator:** [DailyMed SPL archive 940595](https://dailymed.nlm.nih.gov/dailymed/getArchivalFile.cfm?archive_id=940595); approved v3 XML member `a3163e14-0404-4e27-884b-f6f9f7f695bc.xml`. ZIP SHA-256 `db33f66f3b6e3433d0c47667a0e367f4e1b464cc2875e023e950f1f049f1fd33`; XML SHA-256 `696ebb05a528236ea6077c912785e94cf103aa4d29fa61bacab3282e65307fd4`. No source archive is committed.

## Candidate evidence to inspect

The fresh archival integrity and candidate cross-check are summarized in the
[2026-10-27 AI-assisted v3 verification](../reviews/S13/ai-assisted-label-verification-2026-10-27.md).
This does not replace human field review.

The field-level values, exact section/paragraph/table locators, population scopes, denominators, timing, and limitations are in [`S13-candidates.json`](S13-candidates.json). Reviewable candidate fields: `population_identified`, `identity.population`, `identity.disease_stage`, `identity.intervention`, `identity.dose`, `identity.design`, `identity.mapping`, `counts.treated`, `treatment.first_administration`, `treatment.repeat_administrations`, `insulin_independence.observation`, `insulin_independence.attribution`, `insulin_independence.analysis_population`, `insulin_independence.definition`, `independence.duration`, `burden.immunosuppression`, `burden.co_interventions`, `safety.population`, `safety.window`, `safety.harms`.

Key review points:

- The candidate pool is 30 treated participants; repeat infusions are retained (11 received one, 12 received two, 7 received three).
- Insulin independence is reported for 25 participants at any time, while 5 had no days of independence. This does **not** establish a fixed-horizon result.
- The source reports duration counts of 4, 12, and 9, which sum to 25, but the accompanying percentages appear inconsistent. Preserve the source's counts and percentages as reported; do not silently repair them.
- Immunosuppressant counts/percentages in Table 3 also need direct checking. Safety follow-up varies from 0.3 to 14.5 years after first infusion; this is not a fixed-horizon assessment.
- Serious reactions, life-threatening reactions, severe reactions, and deaths are included as unfavorable evidence. Verify each numerator, denominator, and source definition.

## Human decisions required

1. Verify the pooled all-treated target and whether 30 is the correct denominator for each reported field.
2. Reconcile the apparent duration and Table 3 inconsistencies by recording source values and reviewer rationale, not recalculating the source.
3. Determine whether permitted label material supplies fixed-horizon endpoints, baseline values, CGM/HbA1c/SHE definitions, endpoint denominators, or attrition.
4. Confirm any ledger disposition only through the authorized human-review process, including independent review.

## Unresolved fields and limits

`unresolved_field_count` is **101**. The unresolved set is exactly the 121 `SPECS` field IDs in `scripts/q3_classifier.py` minus this packet's reviewable `candidate_field_ids` listed above. Absence from the candidate set is not evidence of `unreported_in_reviewed_material`, `not_applicable`, or any other disposition. No fixed-horizon endpoint is established by these candidates. The official ledger, review log, independent review, cohort links, and Issue #35 gate remain unchanged and pending.
