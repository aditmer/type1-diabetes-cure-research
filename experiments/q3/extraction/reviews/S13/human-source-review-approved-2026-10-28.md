# S13 / Q3-S13 — partial primary human source-review record

**Decision: approved as a partial primary human source review, for the fields
listed below only.** The user's explicit decision was relayed in the Working
Chat conversation and recorded in [Issue #50](https://github.com/aditmer/type1-diabetes-cure-research/issues/50).

- **Reviewer:** `@aditmer` (the authenticated maintainer who reported personally reviewing the source).
- **Decision date:** 2026-10-28 (America/New_York).
- **Recorded mechanically by:** AI assistant; this record relays the user's statement and is not a claim that the assistant performed human review or that the reviewer separately authored this file or Issue #50.
- **Source/report:** S13 / Q3-S13, Lantidra.
- **Frozen source version:** `SPL-v3-a3163e14-0404-4e27-884b-f6f9f7f695bc`.
- **Exact version locator:** [DailyMed archive 940595](https://dailymed.nlm.nih.gov/dailymed/getArchivalFile.cfm?archive_id=940595), XML member `a3163e14-0404-4e27-884b-f6f9f7f695bc.xml`.
- **Recorded identity evidence:** ZIP SHA-256 `db33f66f3b6e3433d0c47667a0e367f4e1b464cc2875e023e950f1f049f1fd33`; XML SHA-256 `696ebb05a528236ea6077c912785e94cf103aa4d29fa61bacab3282e65307fd4`, matching `source-manifest.csv`.
- **Reviewed scope:** Sections 5.1, 6.1, and 14, including Table 3, limited to the findings and field decisions below. This does not claim exhaustive review of all label content.

## Approved field decisions

The following 14 `reports.json` fields are recorded as `reported` for the approved source version and frozen target `lantidra-treated` / `lantidra-pooled-all`:

- `population_identified`: the pooled Study 1 and Study 2 treated population is identified.
- `identity.population`: two label studies pooled; 30 treated subjects.
- `counts.treated`: 30 treated subjects. This is not an enrolled count.
- `treatment.repeat_administrations`: 11 subjects received one infusion, 12 received two, and 7 received three.
- `insulin_independence.observation`: observed at any time; 25 subjects achieved insulin independence at some point and 5 had no days of insulin independence.
- `insulin_independence.attribution`: source summary refers to the pooled treated target.
- `insulin_independence.analysis_population`: the reviewed any-time context refers to the full pooled treated target, not a responder-only target.
- `independence.duration`: 4 subjects for less than 1 year (13.3%), 12 for 1 to 5 years (36.7%), and 9 for greater than 5 years (33.3%), exactly as reported.
- `burden.immunosuppression`: Section 5.1 describes the requirement, risks, precautions, and discontinuation circumstances; Table 3 medication counts and percentages are recorded as printed.
- `burden.repeat_procedures`: 56 infusion procedures.
- `safety.population`: pooled treated population with the source-specific participant denominators retained.
- `safety.window`: follow-up of 0.3–14.5 years after first infusion (mean 3 ± 3.7 years); variable follow-up.
- `safety.harms`: serious reactions 27/30; severe reactions 26/30; life-threatening reactions 8/30; deaths 2/30; 211 infection events among 26 participants; 16 malignancy reactions among 11 participants; anemia in 24/30 with 90 reactions; transfusions in 5/30; and 56 infusion procedures.
- `safety.attribution`: both participants who died were receiving immunosuppression at the time; these observations do not establish that Lantidra caused either death or establish causal attribution for other reactions.

Each promoted field in `reports.json` contains the approved SPL-v3 identifier and a section/paragraph/table locator, the frozen target and subcohort, reviewer/date, limited field scope, and a link to Issue #50.

## Discrepancies preserved

- The source-reported duration counts (4, 12, 9) and percentages (13.3%, 36.7%, 33.3%) are retained together. The percentages do not reconcile consistently; no corrected values are substituted.
- Table 3's counts and percentages are retained as printed for all ten medications. Three count/percentage pairs are flagged: basiliximab Study 1, 5 (10%); daclizumab Study 2, 5 (24%); and mycophenolate mofetil Study 2, 5 (24%). The displayed study Ns are Study 1 N=10 and Study 2 N=20. No value is silently repaired.
- Section 6.1 reports 16 malignancy reactions among 11 participants, while its listed category counts total 15. Both source statements are retained.
- The 211 infection count is an event count among 26 participants, not 211 participants.

## What this approval does not establish

- The 25/30 finding is **ever** insulin independence during variable follow-up. It is not a fixed 12-month, day-365, or week-52 outcome, and no such endpoint value or denominator is approved here.
- Safety counts reflect variable follow-up and are not uniform 12-month risks.
- Neither deaths nor other reactions are attributed causally to Lantidra by this record.
- Only the 14 listed fields are approved. The other 107 of 121 S13 fields remain `not_yet_extracted`; omissions elsewhere in the label are not classified.
- Source-content review remains partial. Access-attempt exhaustion, complete source review, and complete adjudication remain false/pending. Independent review remains pending with no reviewer or decision recorded.
- This is not full S13 review, G2-B acceptance, or G2-C / Issue #35 authorization. No report classification or paired analysis is authorized.

NLM/DailyMed terms remain as recorded in the manifest; no blanket redistribution right is inferred. No source archive is committed.
