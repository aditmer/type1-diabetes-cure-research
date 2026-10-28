# S13 human-review packet

- **Review status:** partial primary human source review recorded for 14 explicitly listed fields; all other S13 fields remain pending. The candidate JSON remains unverified automated extraction, not the human decision record.
- **Report/target:** Q3-S13; all treated Lantidra participants in both pooled label studies, including repeat infusions.
- **Approved source:** DailyMed SPL v3, `SPL-v3-a3163e14-0404-4e27-884b-f6f9f7f695bc`.
- **Version locator:** [DailyMed SPL archive 940595](https://dailymed.nlm.nih.gov/dailymed/getArchivalFile.cfm?archive_id=940595); approved v3 XML member `a3163e14-0404-4e27-884b-f6f9f7f695bc.xml`. ZIP SHA-256 `db33f66f3b6e3433d0c47667a0e367f4e1b464cc2875e023e950f1f049f1fd33`; XML SHA-256 `696ebb05a528236ea6077c912785e94cf103aa4d29fa61bacab3282e65307fd4`. No source archive is committed.

## Candidate evidence to inspect

The fresh archival integrity and candidate cross-check are summarized in the
[2026-10-27 AI-assisted v3 verification](../reviews/S13/ai-assisted-label-verification-2026-10-27.md).
This does not replace human field review.

The candidate field-level values, locators, population scopes, denominators, timing, and limitations are in [`S13-candidates.json`](S13-candidates.json). The limited human decisions are in the [dated S13 source-review record](../reviews/S13/human-source-review-approved-2026-10-28.md) and [Issue #50](https://github.com/aditmer/type1-diabetes-cure-research/issues/50). Candidate fields available for additional review include: `population_identified`, `identity.population`, `identity.disease_stage`, `identity.intervention`, `identity.dose`, `identity.design`, `identity.mapping`, `counts.treated`, `treatment.first_administration`, `treatment.repeat_administrations`, `insulin_independence.observation`, `insulin_independence.attribution`, `insulin_independence.analysis_population`, `insulin_independence.definition`, `independence.duration`, `burden.immunosuppression`, `burden.co_interventions`, `safety.population`, `safety.window`, `safety.harms`.

Key review points:

- The candidate pool is 30 treated participants; repeat infusions are retained (11 received one, 12 received two, 7 received three).
- Insulin independence is reported for 25 participants at any time, while 5 had no days of independence. This does **not** establish a fixed-horizon result.
- The source reports duration counts of 4, 12, and 9, which sum to 25, but the accompanying percentages appear inconsistent. Preserve the source's counts and percentages as reported; do not silently repair them.
- The user-approved Table 3 counts and percentages are recorded as printed; flag basiliximab Study 1 5 (10%), daclizumab Study 2 5 (24%), and mycophenolate mofetil Study 2 5 (24%) without repair. Safety follow-up varies from 0.3 to 14.5 years after first infusion; this is not a fixed-horizon assessment.
- Serious reactions, life-threatening reactions, severe reactions, and deaths are included as unfavorable evidence. Verify each numerator, denominator, and source definition.

## Remaining human decisions

1. Complete the remaining S13 fields only from personally reviewed, permitted source material; an absent candidate does not establish an omission.
2. Determine whether permitted label material supports fixed-horizon endpoints, baselines, CGM/HbA1c/SHE definitions, endpoint denominators, or attrition.
3. Obtain a separate independent review and record its reviewer, date, scope, and decision.

## Unresolved fields and limits

`unresolved_field_count` is **101** for the automated candidate set only; it is not the number of fields still pending in the authoritative ledger. Of the 121 S13 ledger fields, **14** are recorded as `reported` under the partial human decision and **107** remain `not_yet_extracted`. Candidate-file membership is not itself a human decision, and absence from the candidate set is not evidence of `unreported_in_reviewed_material`, `not_applicable`, or another disposition. No fixed-horizon endpoint is established. Independent review, the other reports, cohort links, and the Issue #35 gate remain pending.
