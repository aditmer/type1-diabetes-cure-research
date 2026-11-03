# Evidence Atlas Phase 1 architecture assessment

**Assessment date: 2 November 2026**

## Live repository and governance snapshot

The fetched `origin/main` and the starting checkout both resolve to `6125da2` (`Record signed-off S19 Wave 2 fields (#89)`); no newer `main` commit was available at inspection. The worktree was clean before this change. The repository's current Q3 extraction ledger validates as 8 reports, 968 fields, 6 cohort links, and 0 tracker corrections. Its states are 138 `reported`, 85 `unreported_in_reviewed_material`, 744 `not_yet_extracted`, and 1 `conflicting`; all six PEC-Direct cohort links remain `uncertain`. Q3 G2-B independent review and acceptance remain pending, and G2-C remains blocked. The source ledger is not complete and does not authorize Atlas clinical claims.

The project has 34 source records, 41 evidence records, 12 trial records, 337 passing unit tests, and seven passing synthetic Q3 controls at this snapshot. These are repository inventory and test results, not a claim that the source set is complete.

## Reusable assets

| Existing asset | Reuse in Atlas | Boundary |
| --- | --- | --- |
| `data/sources.csv`, `data/evidence.csv`, `data/trials.csv` and `scripts/validate_data.py` | Existing research inventory and established source-linked claim conventions. | Not imported by the Phase 1 generator; no approved evidence values are modified or promoted. |
| `docs/CHARTER.md`, `docs/EVIDENCE-FRAMEWORK.md`, `docs/MINIMUM-OUTCOMES-AND-CLAIM-REVIEW.md` | Scope, claim language, denominators, endpoint distinctions, and missing-data principles. | Atlas schema does not supersede these governance documents. |
| `experiments/q3/rules-v1.1.json`, `scripts/q3_classifier.py`, `scripts/validate_q3_extraction.py`, and `experiments/q3/extraction/reports.json` | Exact field-state vocabulary, source-version provenance concepts, human-review distinctions, and explicit overlap relationships. | Q3 classifier remains a separate synthetic-only reporting-robustness experiment; its approvals do not authorize Atlas real-source analysis. |
| `experiments/q3/synthetic/` and `scripts/q3_synthetic.py` | Prior art for deterministic synthetic fixtures and repeatable output. | Atlas uses separate fixtures and does not run or extend Q3 classification. |

## Missing components and Phase 1 choice

The repository has no general normalized model connecting therapeutic approaches, programs, studies, outcomes, and source-level review history, and no read-only explorer for those records. Phase 1 adds a JSON data contract and one invented fixture, a standard-library Python validator/builder, and a standalone HTML viewer. The output is deterministic and requires no network service, database, external dependency, or package installation.

The builder validates foreign keys, synthetic-only identifiers and source locations, typed outcome values, required denominators/timing, conflicting-source references, review/approval state, and cohort links before rendering. Cohort-graph consistency uses a pure helper shared with the Q3 extraction validator; this does not import clinical source records into the Atlas. The viewer shows per-study evidence and provenance; it has no participant aggregation, ranking, or score calculation.

## Governance blockers and dependencies

No Phase 1 dependency on real source material exists. Real evidence integration is blocked until each source and outcome has lawful version-specific provenance, completed authorized human review, required adjudication, explicit approval, and any applicable G2 authorization. Unresolved cohort links cannot be treated as independent, and differing endpoint definitions cannot be harmonized by this prototype. The external clinical/statistical review schedule is deferred to a publication-ready milestone; the required independent review and formal acceptance are not waived.

## Build and demonstration

From the repository root:

```sh
python3 scripts/build_evidence_atlas.py --output experiments/evidence-atlas/index.html
open experiments/evidence-atlas/index.html
python3 -m unittest discover -s tests -p 'test_evidence_atlas.py' -v
```

The committed `index.html` is generated from `experiments/evidence-atlas/index.template.html` and `synthetic-fixture.json`. Rebuild it when either source changes; tests verify stable output and integrity behavior.
