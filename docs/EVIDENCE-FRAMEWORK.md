# Evidence and Claim Framework

**Version 1.1 — 22 October 2026**

## Source hierarchy

1. Peer-reviewed primary human studies and full protocols/results.
2. Official ClinicalTrials.gov or other national registries for study design and status.
3. FDA/EMA/regulatory primary documents for authorization, labeling, and safety.
4. Primary animal or laboratory studies, explicitly labeled non-human/preclinical.
5. Systematic reviews for context and references, not as substitutes for pivotal primary data.
6. Sponsor/institution communications only for dated operational updates, clearly labeled and corroborated when possible.

News, advocacy, and commercial pages may help discover sources but are not sufficient support for efficacy claims.

## Scientific evidence level (E0–E5)

- **E0 — Hypothesis:** rationale or proposal without direct test.
- **E1 — In vitro:** cells, organoids, or ex vivo material; no whole-animal clinical evidence.
- **E2 — Animal:** in vivo non-human evidence.
- **E3 — Early human:** first-in-human, case report, or small uncontrolled feasibility/safety cohort.
- **E4 — Controlled human:** randomized or otherwise robust comparative human evidence, replicated or with a meaningful confirmatory dataset.
- **E5 — Established clinical benefit:** replicated, durable patient-important benefit reflected in authoritative clinical/regulatory evidence for the specific population and endpoint.

This scale grades scientific efficacy or safety evidence behind a specific claim, not overall therapy quality, regulatory action, or sponsor program status. Use an E0–E5 level only for scientific claims. For regulatory, registry, and sponsor status claims, record the independent `evidence_basis` (`regulatory_action`, `trial_registry`, or `sponsor_report`) and set `evidence_level` to `NA`. A registered trial is not efficacy evidence. Preclinical evidence never supports claims of human cure.

## Confidence score (0–5)

Score each claim separately across five one-point checks: (1) source is primary/authoritative and accessible; (2) design fits the claim; (3) endpoint is patient-important and clearly defined; (4) sample, follow-up, and analysis are adequate for the claim; (5) independent confirmation or durable replication exists. Record the integer and rationale. A low score is not a recommendation against a therapy; it means uncertainty is high.

## Claim rules

- Use exact denominators and time points; distinguish enrolled, treated, analyzed, and followed participants.
- State whether immunosuppression, device implantation, or another co-intervention was used.
- Prefer “was associated with” for uncontrolled data; reserve causal wording for designs that justify it.
- Distinguish protocol endpoint from observed benefit and surrogate endpoint from clinical benefit.
- Never turn a single case, biomarker, mouse result, press release, or insulin-independence interval into a cure claim.
- Use “no evidence identified” rather than “proven ineffective” when the search is incomplete.
- Note follow-up limits and unknown long-term safety, durability, manufacturing, and generalizability.
- Report contradictory, null, safety, and discontinuation evidence alongside favorable results.

## Tracker fields

`claim_id`, `claim_type`, `claim`, `source_id`, `evidence_level`, `evidence_basis`, `confidence_0_to_5`, `population_or_model`, `design`, `n`, `outcome_numerator`, `analysis_denominator`, `endpoint`, `follow_up`, `cointerventions`, `limitations`, `status_checked`, `notes`, `outcome_type`, `outcome_value`, `outcome_unit`, `outcome_timepoint`, `baseline_value`, `baseline_unit`, and `baseline_timepoint`. Each cited source ID must resolve in `data/sources.csv`. Claims are typed as clinical outcome, regulatory status, trial status, or program status, and the evidence basis must match that type. For a binary clinical outcome, `n` is the study sample, `outcome_numerator` is the number with the stated outcome, and `analysis_denominator` is the number assessed for that outcome. For a continuous outcome, set `outcome_numerator=NA`, preserve `analysis_denominator` as the number assessed (a positive integer no larger than `n` when known), and record the reported value, unit, time point, and (when available) baseline value, unit, and time point. If the analyzed denominator is unavailable, enter `not reported` and explain why in notes or limitations. Use `outcome_type=not_reported` when a clinical outcome is explicitly unavailable; do not populate measured result or baseline fields, and explain the gap. The validator checks that binary denominators are positive and no larger than `n` when known, and applies the same denominator bounds to continuous outcomes. Non-outcome status claims use `NA` evidence counts and `outcome_type=not_applicable`. Trial records use a registry-neutral `registry_id` and `registry_name`; registry-specific status and metadata precision are recorded, with unknown/unverified values left blank or marked `unknown` and explained. Keep one principal claim per row. Use `unknown` rather than guessing, and link all source IDs in the companion source catalog/report.
