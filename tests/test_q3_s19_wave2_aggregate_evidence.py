import csv
import json
import unittest
from pathlib import Path

from scripts.q3_classifier import SPECS, _valid_value


ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = ROOT / (
    "experiments/q3/extraction/proposals/"
    "S19-wave2-aggregate-evidence-2026-10-29.json"
)


class S19Wave2AggregateEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proposal = json.loads(PROPOSAL.read_text(encoding="utf-8"))
        with (ROOT / "experiments/q3/source-manifest.csv").open(
            encoding="utf-8", newline=""
        ) as stream:
            cls.manifest = next(
                row for row in csv.DictReader(stream)
                if row["source_id"] == "S19"
            )

    def test_exact_frozen_identity_and_ten_person_target(self):
        proposal = self.proposal
        self.assertEqual(
            proposal["baseline_sha"],
            "7432cd3cb3bc1075706b12c50ab7156bc71ddb8c",
        )
        for key in ("source_id", "report_id", "source_version_id",
                    "target_population_id"):
            self.assertEqual(proposal[key], self.manifest[key])
        self.assertEqual(proposal["subcohort_id"], "pec-s19-optimized-all")
        self.assertEqual(proposal["target_size"], 10)

    def test_new_public_hash_does_not_upgrade_historical_restore(self):
        retrieval = self.proposal["retrieval"]
        self.assertEqual(retrieval["http_status"], 200)
        self.assertEqual(retrieval["method"], "GET")
        self.assertEqual(retrieval["bytes"], int(self.manifest["bytes"]))
        self.assertEqual(retrieval["sha256"], self.manifest["sha256"])
        self.assertTrue(retrieval["manifest_hash_match"])
        self.assertTrue(retrieval["hash_verified_before_narrative_inspection"])
        self.assertEqual(retrieval["pmcid_in_xml"], "PMC11471599")
        self.assertFalse(retrieval["pmcid_ver_in_xml"])
        self.assertIn("not recovery", retrieval["restore_limit"])
        self.assertIn("remain unavailable", retrieval["restore_limit"])

    def test_twenty_distinct_typed_proposed_fields(self):
        fields = self.proposal["field_candidates"]
        self.assertEqual(len(fields), self.proposal["field_candidate_count"])
        self.assertEqual(len(fields), 20)
        self.assertEqual(len({field["field_id"] for field in fields}), 20)
        for field in fields:
            with self.subTest(field=field["field_id"]):
                self.assertIn(field["field_id"], SPECS)
                self.assertEqual(field["proposed_status"], "reported")
                self.assertTrue(_valid_value(
                    field["proposed_value"], SPECS[field["field_id"]]
                ))
                self.assertTrue(field["scope"])
                self.assertTrue(field["limitation"])
                self.assertTrue(field["locators"])

    def test_prior_candidates_are_distinguished_from_fresh_inspection(self):
        self.assertEqual(len(self.proposal["prior_packet_leads_reverified"]), 4)
        self.assertTrue(self.proposal["inspection_scope"]["newly_inspected"])
        self.assertIn(
            "Partial", self.proposal["inspection_scope"]["coverage_limit"]
        )

    def test_all_candidate_locators_are_version_bound_author_narrative(self):
        groups = (
            self.proposal["field_candidates"],
            self.proposal["aggregate_surrogate_observations"],
            self.proposal["planned_protocol_endpoints"],
        )
        for rows in groups:
            for row in rows:
                for locator in row["locators"]:
                    self.assertIn("PMC11471599.1", locator)
                    self.assertIn("Par", locator)
                    for excluded in ("moesm", "table", "fig."):
                        self.assertNotIn(excluded, locator.lower())

    def test_surrogate_denominators_and_actual_nominal_times_are_separate(self):
        observations = self.proposal["aggregate_surrogate_observations"]
        self.assertEqual(
            len(observations),
            self.proposal["aggregate_surrogate_observation_count"],
        )
        self.assertEqual(
            [(row["numerator"], row["denominator"]) for row in observations],
            [(5, 10), (4, 10), (3, 10)],
        )
        self.assertEqual(len({row["observation_id"] for row in observations}), 3)
        for row, timing in zip(observations, ("month 3", "month 6", "month 12")):
            self.assertEqual(row["outcome_type"], "graft_function_surrogate")
            self.assertIn(timing, row["nominal_timing"])
            self.assertTrue(row["denominator_basis"])
            self.assertTrue(row["limitation"])
        field_ids = {
            row["field_id"] for row in self.proposal["field_candidates"]
        }
        self.assertNotIn("insulin_independence.value", field_ids)
        self.assertNotIn("other_evidence", field_ids)
        self.assertNotIn("counts.at_horizon", field_ids)
        self.assertNotIn("overall_followup", field_ids)

    def test_planned_clinical_endpoints_do_not_acquire_observed_results(self):
        endpoints = self.proposal["planned_protocol_endpoints"]
        self.assertEqual(len(endpoints), 4)
        self.assertEqual(
            len(endpoints), self.proposal["planned_protocol_endpoint_count"]
        )
        for row in endpoints:
            self.assertEqual(row["observation"], "planned")
            self.assertIsNone(row["numerator"])
            self.assertIsNone(row["denominator"])
        hypoglycemia = next(
            row for row in endpoints if row["domain"] == "hypoglycemic_events"
        )
        self.assertIn("do not automatically equate", hypoglycemia["definition"])
        timing = self.proposal["timing_and_method_annotations"]
        self.assertIn("104 weeks", timing["protocol_maximum"])
        self.assertIn("not evidence that all 10", timing["actual_report_scope"])

    def test_attribution_withdrawals_and_attrition_are_not_conflated(self):
        fields = {
            row["field_id"]: row for row in self.proposal["field_candidates"]
        }
        self.assertIn("Two patients", fields["safety.harms"]["proposed_value"])
        self.assertIn(
            "affected-person count", fields["safety.harms"]["limitation"]
        )
        self.assertIn(
            "Not zero total withdrawals",
            fields["safety.discontinuations"]["limitation"],
        )
        for fid in ("counts.followed", "counts.censored", "counts.withdrawals",
                    "counts.missing_data_handling", "safety.window"):
            self.assertNotIn(fid, fields)
        blocker = next(
            row for row in self.proposal["blocker_decisions"]
            if row["blocker_id"] == "S19-safety-scope"
        )
        self.assertIn("Sec3/Par9", blocker["decision"])
        self.assertIn("Sec10/Par38", blocker["decision"])
        self.assertEqual(blocker["state"], "requires_human_reconciliation")

    def test_every_remaining_blocker_has_a_disposition_and_lawful_next_step(self):
        blockers = self.proposal["blocker_decisions"]
        self.assertEqual(len(blockers), 8)
        self.assertEqual(len({row["blocker_id"] for row in blockers}), 8)
        for row in blockers:
            self.assertTrue(row["decision"])
            self.assertTrue(row["lawful_next_step"])
            self.assertNotEqual(row["state"], "unreported_in_reviewed_material")
        supplements = next(
            row for row in blockers if row["blocker_id"] == "S19-supplements"
        )
        self.assertIn("MOESM4 excluded", supplements["decision"])
        self.assertIn("never a proposed remedy", supplements["lawful_next_step"])

    def test_authoritative_promotion_is_limited_to_human_supported_fields(self):
        self.assertFalse(self.proposal["authoritative_ledger_data"])
        reports = json.loads(
            (ROOT / "experiments/q3/extraction/reports.json").read_text(
                encoding="utf-8"
            )
        )["reports"]
        report = next(row for row in reports if row["source_id"] == "S19")
        self.assertEqual(len(report["fields"]), 121)
        self.assertEqual(self.proposal["remaining_authoritative_fields"], 121)
        approved = {
            "target_enrolled", "population_identified", "identity.population",
            "identity.design", "identity.disease_stage", "identity.eligibility",
            "identity.baseline_context", "identity.intervention", "counts.enrolled",
            "identity.mapping", "counts.treated", "burden.immunosuppression",
            "burden.co_interventions", "treatment.source_anchors", "safety.harms",
        }
        by_id = {field["field_id"]: field for field in report["fields"]}
        self.assertEqual(
            {field_id for field_id, field in by_id.items()
             if field["status"] == "reported"},
            approved,
        )
        self.assertTrue(all(
            by_id[field_id]["value"] is not None
            and by_id[field_id]["review_complete"]
            and by_id[field_id]["locator"]
            for field_id in approved
        ))
        self.assertTrue(all(
            field["status"] == "not_yet_extracted"
            and field["value"] is None
            and not field["review_complete"]
            for field_id, field in by_id.items()
            if field_id not in approved
        ))
        self.assertEqual(report["human_review"]["reviewer_identity"], "@aditmer")
        self.assertEqual(report["human_review"]["decision_date"], "2026-10-30")
        self.assertTrue(report["human_review"]["independent_review_pending"])
        forbidden = {
            "reviewer_identity", "decision_date", "human_review",
            "review_complete", "adjudication_complete",
            "source_content_review_complete", "independent_review_decision",
            "accepted", "unique_participant_total",
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
