import csv
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXTRACTION = ROOT / "experiments/q3/extraction"
PROPOSAL = (
    EXTRACTION / "proposals/pec-direct-wave2-adjudication-2026-10-29.json"
)
PAIRS = [
    ("S18", "S19"), ("S18", "S23"), ("S18", "S20"),
    ("S19", "S23"), ("S19", "S20"), ("S23", "S20"),
]


class Wave2CohortAdjudicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proposal = json.loads(PROPOSAL.read_text(encoding="utf-8"))
        cls.prior = json.loads(
            (ROOT / cls.proposal["prior_proposal"]).read_text(encoding="utf-8")
        )
        with (ROOT / "experiments/q3/source-manifest.csv").open(
            encoding="utf-8", newline=""
        ) as stream:
            cls.manifest = {r["source_id"]: r for r in csv.DictReader(stream)}
        with (EXTRACTION / "cohort-links.csv").open(
            encoding="utf-8", newline=""
        ) as stream:
            cls.links = list(csv.DictReader(stream))
        cls.reports = {
            r["source_id"]: r
            for r in json.loads(
                (EXTRACTION / "reports.json").read_text(encoding="utf-8")
            )["reports"]
        }

    def test_exact_baseline_and_no_new_source_verification(self):
        p = self.proposal
        self.assertEqual(p["baseline_sha"],
                         "7432cd3cb3bc1075706b12c50ab7156bc71ddb8c")
        self.assertEqual(p["artifact_status"], "human_adjudication_proposal")
        self.assertIs(p["authoritative_ledger_data"], False)
        scope = p["evidence_scope"]
        for key in ("primary_source_retrieval_performed",
                    "new_primary_evidence_established",
                    "independent_scientific_approval"):
            self.assertIs(scope[key], False)
        updates = scope["later_source_stream_updates"]
        self.assertEqual(len(updates), 2)
        self.assertEqual(
            {u["reporting_session_id"] for u in updates},
            {"801aae73-970d-4ed3-9f27-1db700a9795c",
             "5343856a-8a34-4b72-b135-831247a45dd4"},
        )
        for update in updates:
            self.assertEqual(
                update["evidence_class"],
                "source_stream_relay_not_independently_reperformed",
            )
            for key in ("access_result", "limitations", "recommendation_impact"):
                self.assertTrue(update[key])
        self.assertTrue(scope["new_work"])
        self.assertTrue(scope["inherited_evidence"])

    def test_all_six_pairs_match_frozen_ledger_order(self):
        sources = self.proposal["sources"]
        self.assertEqual(set(sources), {"S18", "S19", "S23", "S20"})
        relations = self.proposal["relations"]
        self.assertEqual(
            [(r["from_source_id"], r["to_source_id"]) for r in relations],
            PAIRS,
        )
        self.assertEqual(
            [(sources[a]["target_population_id"],
              sources[b]["target_population_id"]) for a, b in PAIRS],
            [(r["from_population_id"], r["to_population_id"])
             for r in self.links],
        )

    def test_identities_match_manifest_ledger_and_pr66(self):
        for sid, source in self.proposal["sources"].items():
            with self.subTest(source=sid):
                for key in ("report_id", "program_id", "target_population_id",
                            "source_version_id"):
                    self.assertEqual(source[key], self.manifest[sid][key])
                    self.assertEqual(source[key], self.reports[sid][key])
                    self.assertEqual(source[key], self.prior["sources"][sid][key])
                self.assertEqual(source["subcohort_id"],
                                 self.reports[sid]["subcohort_id"])
                self.assertEqual(source["subcohort_id"],
                                 self.prior["sources"][sid]["subcohort_id"])
                self.assertTrue(source["population_scope"])

    def test_every_decision_has_two_sided_evidence_and_counterevidence(self):
        evidence = self.proposal["evidence"]
        for row in self.proposal["relations"]:
            pair = {row["from_source_id"], row["to_source_id"]}
            with self.subTest(pair=pair):
                for key in ("supporting_evidence_ids", "counterevidence_ids"):
                    ids = row[key]
                    self.assertEqual(len(ids), len(set(ids)))
                    sides = set()
                    for eid in ids:
                        sides.update(evidence[eid]["source_ids"])
                    self.assertTrue(pair.issubset(sides))
                for key in ("supporting_evidence",
                            "contradictory_or_limiting_evidence",
                            "decision_rationale", "human_decision",
                            "change_threshold"):
                    self.assertGreater(len(row[key]), 60)

    def test_evidence_records_and_version_bound_locators_exist(self):
        for item in self.proposal["evidence"].values():
            self.assertTrue((ROOT / item["record"]).is_file())
            self.assertTrue(item["record_pointer"])
            self.assertIn("Inherited", item["review_basis"])
            self.assertTrue(item["source_locators"])
            for sid in item["source_ids"]:
                version = self.proposal["sources"][sid]["source_version_id"]
                self.assertTrue(any(version in loc
                                    for loc in item["source_locators"]))
            for loc in item["source_locators"]:
                self.assertNotIn("mmc2", loc.lower())
                self.assertNotIn("moesm4", loc.lower())

    def test_exact_source_blockers_apply_to_each_pair(self):
        sources = self.proposal["sources"]
        blockers = self.proposal["blockers"]
        for blocker in blockers.values():
            self.assertTrue((ROOT / blocker["record"]).is_file())
            self.assertTrue(blocker["limitation"])
            self.assertTrue(blocker["required_action"])
        for row in self.proposal["relations"]:
            expected = {"BREVIEW"}
            for sid in (row["from_source_id"], row["to_source_id"]):
                expected.update(sources[sid]["blocker_ids"])
            self.assertEqual(set(row["blocker_ids"]), expected)
            self.assertTrue(expected.issubset(blockers))
        self.assertIn("participant-level table", blockers["B18"]["limitation"])
        self.assertIn("mmc2.xlsx", blockers["B18"]["required_action"])
        self.assertIn("MOESM4", blockers["B19"]["required_action"])
        self.assertIn("third-party", blockers["B19"]["limitation"])
        self.assertIn("HTTP 403", blockers["B20"]["limitation"])
        self.assertIn("not historical-v20 byte identity",
                      blockers["B20"]["limitation"])

    def test_uncertain_recommendations_have_no_subset_direction(self):
        for row in self.proposal["relations"]:
            self.assertEqual(row["recommended_relationship"], "uncertain")
            self.assertEqual(row["direction_if_subset"], "")
            self.assertIn("uncertain", row["human_decision"])
        decisions = [r["human_decision"] for r in self.proposal["relations"]]
        self.assertEqual(len(set(decisions)), 6)

    def test_partial_overlap_and_s19_uncertainty_are_not_erased(self):
        row = self.proposal["relations"][1]
        self.assertEqual((row["from_source_id"], row["to_source_id"]),
                         ("S18", "S23"))
        self.assertIn("known partial overlap", row["decision_rationale"])
        self.assertIn("rules out distinct_within_program",
                      row["contradictory_or_limiting_evidence"])
        self.assertIn("to_is_subset_of_from", row["change_threshold"])
        self.assertIn("No partial-overlap enum", row["decision_rationale"])
        for row in self.proposal["relations"]:
            if "S19" in (row["from_source_id"], row["to_source_id"]):
                self.assertIn("uncertain", row["decision_rationale"])
        self.assertIn("no exact matched count",
                      self.proposal["evidence"]["EOVERLAP"]["fact"])

    def test_registry_subset_alternatives_require_inclusion_not_shared_id(self):
        for row in self.proposal["relations"]:
            if row["to_source_id"] == "S20":
                self.assertIn("from_is_subset_of_to", row["change_threshold"])
                self.assertIn("inclusion", row["change_threshold"])
                self.assertIn("v20", row["human_decision"])
                self.assertIn("uncertain", row["human_decision"])

    def test_path_b_conflict_and_independent_access_remain_visible(self):
        b23 = self.proposal["blockers"]["B23"]
        self.assertIn("Path B human-only", b23["limitation"])
        self.assertIn("@aditmer", b23["required_action"])
        self.assertIn("Independent reviewer needs own lawful access",
                      b23["required_action"])
        self.assertIn("safety.harms conflict", b23["required_action"])
        self.assertIn("incomplete review", b23["required_action"])
        self.assertIn("governance exception unresolved", b23["limitation"])

    def test_one_unfilled_batch_and_no_gate_closure(self):
        batch = self.proposal["human_batch"]
        self.assertEqual(batch["status"], "not_submitted_for_approval")
        self.assertEqual(batch["decision_count"], len(PAIRS))
        self.assertIn("no completed decision", batch["instructions"])
        self.assertIn("separately authorized", batch["recording_boundary"])
        self.assertIn("G2-B remains unaccepted", batch["gate_impact"])
        self.assertIn("Issue35 stays blocked", batch["gate_impact"])
        self.assertEqual(len(self.proposal["prohibitions"]), 5)

    def test_no_completed_review_outcome_or_participant_records(self):
        forbidden = {
            "reviewer_identity", "decision_date", "human_review",
            "adjudication_complete", "source_content_review_complete",
            "independent_review_decision", "review_complete", "accepted",
            "unique_participant_total", "pooled_total", "participant_ids",
            "matched_count", "endpoint_value", "classification",
        }

        def check(value):
            if isinstance(value, dict):
                self.assertFalse(forbidden.intersection(value))
                for child in value.values():
                    check(child)
            elif isinstance(value, list):
                for child in value:
                    check(child)

        check(self.proposal)


if __name__ == "__main__":
    unittest.main()
