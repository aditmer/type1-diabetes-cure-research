import json
import re
import unittest

from scripts.validate_data import (
    Q3_RETRIEVAL_LOG_FIELDS,
    Q3_SOURCE_MANIFEST_FIELDS,
    ROOT,
    read_q3_csv,
    validate_q3_amendment,
    validate_q3_metadata,
    validate_q3_source_manifest,
)


class Q3G1MetadataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.q3 = ROOT / "experiments" / "q3"
        cls.rules = json.loads((cls.q3 / "rules-v1.0.json").read_text(encoding="utf-8"))

    def manifest(self):
        return read_q3_csv(self.q3 / "source-manifest.csv", Q3_SOURCE_MANIFEST_FIELDS)

    def retrieval_log(self):
        return read_q3_csv(self.q3 / "retrieval-log.csv", Q3_RETRIEVAL_LOG_FIELDS)

    def test_repository_q3_metadata_is_valid(self):
        self.assertEqual(validate_q3_metadata(), (8, 44))

    def test_only_explicitly_accepted_source_versions_are_approved(self):
        approved = {
            row["source_id"]: row
            for row in self.manifest()
            if row["maintainer_approval_status"] == "approved"
        }
        self.assertEqual(set(approved), {"S13", "S20", "S17", "S4", "S9"})
        for row in approved.values():
            self.assertEqual(row["approved_version_id"], row["source_version_id"])
            self.assertEqual(row["approval_date"], "2026-10-23")
            self.assertEqual(row["approving_maintainer"], "@aditmer")

    def test_governing_v1_1_matches_approved_amendment(self):
        validate_q3_amendment(self.q3, self.rules)
        amendment = json.loads(
            (self.q3 / "rules-v1.1-amendment-2026-10-23-01.json").read_text(encoding="utf-8")
        )
        self.assertEqual(amendment["status"], "approved_prospectively")
        self.assertEqual(amendment["effective_version"], "1.1")
        governing = json.loads((self.q3 / "rules-v1.1.json").read_text(encoding="utf-8"))
        self.assertEqual(governing["reports"], self.rules["reports"])
        for key in ("sample_size", "context_only_source_ids", "source_version_policy",
                    "overlap", "classification", "primary_outcome", "sensitivity",
                    "invariants_and_stops"):
            with self.subTest(key=key):
                self.assertEqual(governing[key], self.rules[key])

    def test_public_restore_record_uses_only_the_opaque_archive_alias(self):
        record = next(
            event for event in self.retrieval_log()
            if event["artifact_id"] == "S19-onedrive-restore-2026-10-23T181816Z"
        )
        self.assertEqual(record["request_url"], "archive-alias://OD-S19-3e14ef3dcb7f")
        self.assertNotIn("Ditmer", record["request_url"])
        s19 = next(row for row in self.manifest() if row["source_id"] == "S19")
        self.assertEqual(s19["archive_reference"], "private-archive-alias:OD-S19-3e14ef3dcb7f")

    def test_source_version_archive_and_rights_statuses_are_independent(self):
        s19 = next(row for row in self.manifest() if row["source_id"] == "S19")
        self.assertEqual(s19["maintainer_approval_status"], "pending_maintainer")
        self.assertEqual(s19["approved_version_id"], "")
        self.assertEqual(s19["archive_status"], "verified")
        self.assertEqual(s19["rights_review_status"], "third_party_review_pending")
        event = next(
            row for row in self.retrieval_log()
            if row["artifact_id"] == "S19-onedrive-restore-2026-10-23T181816Z"
        )
        self.assertEqual(event["verification_outcome"], "archive_restore_success")
        self.assertEqual(event["bytes"], "122548")
        self.assertEqual(event["response_sha256"], s19["sha256"])

    def test_s23_account_rights_cannot_be_represented_as_verified(self):
        rows = self.manifest()
        s23 = next(row for row in rows if row["source_id"] == "S23")
        self.assertEqual(s23["rights_review_status"], "account_terms_unverified")
        self.assertEqual(s23["maintainer_approval_status"], "pending_maintainer")
        self.assertEqual(s23["archive_status"], "pending_maintainer")
        self.assertEqual(s23["approved_version_id"], "")
        s23["rights_review_status"] = "conditions_documented"
        with self.assertRaisesRegex(ValueError, "S23 account-specific rights cannot be represented as verified"):
            validate_q3_source_manifest(rows, self.rules["reports"], self.retrieval_log())

    def test_g1_authorization_is_not_inferred_from_individual_approvals(self):
        decisions = (self.q3 / "G1-MAINTAINER-DECISIONS.md").read_text(encoding="utf-8")
        g1_row = next(line for line in decisions.splitlines() if line.startswith("| G1 |"))
        self.assertIn("| pending_maintainer |", g1_row)
        self.assertIn("| — | — |", g1_row)
        self.assertIn("Final G1 authorization remains pending", decisions)

    def test_public_q3_metadata_contains_no_private_onedrive_locations(self):
        private_location = re.compile(
            r"https?://[^\s,;\"<>]*(?:1drv\.ms|onedrive(?:\.live)?\.com|"
            r"(?:[\w-]+\.)*sharepoint\.com|d\.docs\.live\.net)",
            re.IGNORECASE,
        )
        account_email = re.compile(
            r"\b[^\s,;\"<>@]+@(?:outlook|hotmail|live|msn)\.[a-z.]+\b",
            re.IGNORECASE,
        )
        for path in self.q3.iterdir():
            if path.is_file() and path.suffix in {".csv", ".md", ".json"}:
                text = path.read_text(encoding="utf-8")
                with self.subTest(path=path.name):
                    self.assertIsNone(private_location.search(text))
                    self.assertIsNone(account_email.search(text))

    def test_manifest_must_match_all_frozen_report_targets(self):
        rows = self.manifest()
        rows[0]["target_population_id"] = "different-target"
        with self.assertRaisesRegex(ValueError, "target_population_id differs"):
            validate_q3_source_manifest(rows, self.rules["reports"], self.retrieval_log())

    def test_manifest_identifiers_must_match_all_frozen_reports(self):
        for field in ("source_id", "report_id", "program_id", "target_population_id"):
            with self.subTest(field=field):
                rows = self.manifest()
                rows[0][field] = "changed-identifier"
                with self.assertRaises(ValueError):
                    validate_q3_source_manifest(rows, self.rules["reports"], self.retrieval_log())

    def test_manifest_rejects_malformed_hashes(self):
        rows = self.manifest()
        rows[0]["sha256"] = "not-a-hash"
        with self.assertRaisesRegex(ValueError, "invalid SHA-256"):
            validate_q3_source_manifest(rows, self.rules["reports"], self.retrieval_log())

    def test_verified_archive_requires_recovery_evidence(self):
        rows = self.manifest()
        s19 = next(row for row in rows if row["source_id"] == "S19")
        s19["archive_status"] = "verified"
        s19["archive_object_id"] = ""
        with self.assertRaisesRegex(ValueError, "verified archive requires object and restore evidence"):
            validate_q3_source_manifest(rows, self.rules["reports"], self.retrieval_log())

    def test_onedrive_archive_cannot_be_verified_without_a_restore_event(self):
        rows = self.manifest()
        s19 = next(row for row in rows if row["source_id"] == "S19")
        s19.update({
            "archive_status": "verified",
            "archive_reference": "private-archive-alias:OD-S19-3e14ef3dcb7f",
            "archive_recovery_evidence": "fresh cloud download checked",
            "archive_object_id": "OD-S19-3e14ef3dcb7f",
            "archive_restore_event_id": "S19-onedrive-restore-pending",
            "archive_restore_bytes": s19["bytes"],
            "archive_restore_sha256": s19["sha256"],
        })
        with self.assertRaisesRegex(ValueError, "lacks a successful restore event"):
            validate_q3_source_manifest(rows, self.rules["reports"], self.retrieval_log())

    def test_verified_archive_requires_matching_retrieval_records(self):
        rows = self.manifest()
        s13 = next(row for row in rows if row["source_id"] == "S13")
        log = self.retrieval_log()
        restore_record = next(
            record for record in log
            if record["artifact_id"] == s13["archive_restore_event_id"]
        )
        restore_record["response_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "restored bytes and SHA-256 must match"):
            validate_q3_source_manifest(rows, self.rules["reports"], log)

    def test_archive_restore_does_not_require_http_transport(self):
        rows = self.manifest()
        s13 = next(row for row in rows if row["source_id"] == "S13")
        log = self.retrieval_log()
        restore_record = next(
            record for record in log
            if record["artifact_id"] == s13["archive_restore_event_id"]
        )
        restore_record["http_status"] = ""
        self.assertIsNone(validate_q3_source_manifest(rows, self.rules["reports"], log))

    def test_archive_restore_requires_exact_byte_count(self):
        rows = self.manifest()
        s13 = next(row for row in rows if row["source_id"] == "S13")
        s13["archive_restore_bytes"] = "1"
        with self.assertRaisesRegex(ValueError, "restored bytes and SHA-256 must match"):
            validate_q3_source_manifest(rows, self.rules["reports"], self.retrieval_log())

    def test_archive_restore_requires_success_for_the_identified_object(self):
        rows = self.manifest()
        s13 = next(row for row in rows if row["source_id"] == "S13")
        for field, value in (
            ("verification_outcome", "restore_failed"),
            ("archive_object_id", "different-object"),
        ):
            with self.subTest(field=field):
                log = self.retrieval_log()
                event = next(
                    record for record in log
                    if record["artifact_id"] == s13["archive_restore_event_id"]
                )
                event[field] = value
                with self.assertRaisesRegex(ValueError, "lacks a successful restore event"):
                    validate_q3_source_manifest(rows, self.rules["reports"], log)

    def test_official_version_locator_requires_successful_retrieval(self):
        rows = self.manifest()
        s18 = next(row for row in rows if row["source_id"] == "S18")
        log = self.retrieval_log()
        locator_record = next(
            record for record in log
            if record["source_id"] == "S18" and record["request_url"] == s18["archive_reference"]
        )
        locator_record["http_status"] = "403"
        with self.assertRaisesRegex(ValueError, "official version locator lacks successful retrieval evidence"):
            validate_q3_source_manifest(rows, self.rules["reports"], log)

    def test_recommendation_cannot_populate_maintainer_approval_fields(self):
        rows = self.manifest()
        s18 = next(row for row in rows if row["source_id"] == "S18")
        s18["approved_version_id"] = s18["source_version_id"]
        with self.assertRaisesRegex(ValueError, "recommendations cannot populate approval fields"):
            validate_q3_source_manifest(rows, self.rules["reports"], self.retrieval_log())

    def test_approved_version_must_match_manifest_version(self):
        rows = self.manifest()
        s13 = next(row for row in rows if row["source_id"] == "S13")
        s13["maintainer_approval_status"] = "approved"
        s13["approved_version_id"] = "SPL-v1"
        s13["approval_date"] = "2026-10-23"
        s13["approving_maintainer"] = "Maintainer"
        with self.assertRaisesRegex(ValueError, "approved version must match source_version_id"):
            validate_q3_source_manifest(rows, self.rules["reports"], self.retrieval_log())

    def test_manifest_requires_provenance_locators(self):
        rows = self.manifest()
        rows[0]["relevant_locators"] = ""
        with self.assertRaisesRegex(ValueError, "empty required provenance fields"):
            validate_q3_source_manifest(rows, self.rules["reports"], self.retrieval_log())

    def test_s19_requires_citation_attribution(self):
        rows = self.manifest()
        s19 = next(row for row in rows if row["source_id"] == "S19")
        s19["citation_title"] = ""
        with self.assertRaisesRegex(ValueError, "S19 citation title is required"):
            validate_q3_source_manifest(rows, self.rules["reports"], self.retrieval_log())

    def test_amendment_patch_matches_frozen_base_without_changing_population(self):
        validate_q3_amendment(self.q3, self.rules)

    def test_q3_csv_rejects_inconsistent_column_width(self):
        path = self.q3 / "temporary-malformed-q3.csv"
        try:
            path.write_text("a,b\none,two,three\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "column count does not match header"):
                read_q3_csv(path, ["a", "b"])
        finally:
            path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
