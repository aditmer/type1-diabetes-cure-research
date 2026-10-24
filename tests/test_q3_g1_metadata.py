import json
import re
import unittest

from scripts.validate_data import (
    Q3_RETRIEVAL_LOG_FIELDS,
    Q3_SOURCE_MANIFEST_FIELDS,
    ROOT,
    read_q3_csv,
    validate_q3_amendment,
    validate_q3_g1_authorization,
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

    def test_approved_sources_have_matching_version_and_explicit_provenance(self):
        approved = {
            row["source_id"]: row
            for row in self.manifest()
            if row["maintainer_approval_status"] == "approved"
        }
        self.assertTrue(approved)
        for row in approved.values():
            self.assertEqual(row["approved_version_id"], row["source_version_id"])
            self.assertRegex(row["approval_date"], r"^\d{4}-\d{2}-\d{2}$")
            self.assertTrue(row["approving_maintainer"].strip())

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
        self.assertEqual(s19["archive_status"], "verified")
        self.assertTrue(s19["rights_review_evidence"])
        event = next(
            row for row in self.retrieval_log()
            if row["artifact_id"] == "S19-onedrive-restore-2026-10-23T181816Z"
        )
        self.assertEqual(event["verification_outcome"], "archive_restore_success")
        self.assertEqual(event["bytes"], "122548")
        self.assertEqual(event["response_sha256"], s19["sha256"])

    def test_s23_reviewer_access_and_storage_sharing_are_independent(self):
        rows = self.manifest()
        s23 = next(row for row in rows if row["source_id"] == "S23")
        self.approve_source(s23)
        s23["assigned_reviewer_access_evidence"] = ""
        s23["assigned_reviewer_access_status"] = "confirmed"
        with self.assertRaisesRegex(ValueError, "confirmed reviewer access requires evidence"):
            validate_q3_source_manifest(rows, self.rules["reports"], self.retrieval_log())
        s23["assigned_reviewer_access_evidence"] = "Assigned reviewers confirmed individual institutional access."
        validate_q3_source_manifest(rows, self.rules["reports"], self.retrieval_log())
        self.assertIn("assigned_reviewer_access_confirmed", s23["access_outcome"])
        self.assertIn("access is confirmed", s23["terms_or_license"])
        self.assertNotIn("assigned-reviewer access remain unverified", s23["terms_or_license"])

        s23["storage_sharing_status"] = "permitted"
        with self.assertRaisesRegex(ValueError, "resolved storage/sharing status requires evidence"):
            validate_q3_source_manifest(rows, self.rules["reports"], self.retrieval_log())
        s23["storage_sharing_evidence"] = "Applicable account agreement permits private project storage and reviewer sharing."
        validate_q3_source_manifest(rows, self.rules["reports"], self.retrieval_log())

    def test_completed_s19_third_party_review_requires_evidence(self):
        rows = self.manifest()
        s19 = next(row for row in rows if row["source_id"] == "S19")
        self.approve_source(s19)
        s19["rights_review_status"] = "third_party_review_complete"
        s19["rights_review_evidence"] = ""
        with self.assertRaisesRegex(ValueError, "rights review status requires evidence"):
            validate_q3_source_manifest(rows, self.rules["reports"], self.retrieval_log())
        s19["rights_review_evidence"] = "Credit lines reviewed; excluded third-party items were omitted."
        validate_q3_source_manifest(rows, self.rules["reports"], self.retrieval_log())

    def test_g1_decision_is_explicit_and_independently_validated(self):
        decisions = (self.q3 / "G1-MAINTAINER-DECISIONS.md").read_text(encoding="utf-8")
        rows = self.manifest()
        validate_q3_g1_authorization(decisions, rows)
        g1 = next(
            [cell.strip() for cell in line.strip().strip("|").split("|")]
            for line in decisions.splitlines()
            if line.startswith("| G1 |")
        )
        if g1[3] == "pending_maintainer":
            self.assertIn(g1[4], {"—", "-", ""})
            self.assertIn(g1[5], {"—", "-", ""})
        else:
            self.assertTrue(g1[4])
            self.assertTrue(g1[5])
        for source_id in ("S18", "S19", "S23"):
            source = next(row for row in rows if row["source_id"] == source_id)
            self.assertEqual(source["maintainer_approval_status"], "approved")
            self.assertEqual(source["approval_date"], "2026-10-24")
        s19 = next(row for row in rows if row["source_id"] == "S19")
        s23 = next(row for row in rows if row["source_id"] == "S23")
        self.assertEqual(s19["rights_review_status"], "third_party_review_pending")
        self.assertEqual(s23["assigned_reviewer_access_status"], "confirmed")
        self.assertEqual(s23["storage_sharing_status"], "unverified")

    def test_g1_go_links_exact_authenticated_maintainer_comment(self):
        decisions = (self.q3 / "G1-MAINTAINER-DECISIONS.md").read_text(encoding="utf-8")
        approval_url = (
            "https://github.com/aditmer/type1-diabetes-cure-research/"
            "issues/32#issuecomment-6385483877"
        )
        self.assertIn(approval_url, decisions)
        self.assertIn("14:36:43 UTC", decisions)
        row = next(line for line in decisions.splitlines() if line.startswith("| G1 |"))
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        self.assertEqual(cells[3:], ["approved", "2026-10-24", "@aditmer"])

    def test_source_approvals_do_not_imply_final_g1_authorization(self):
        decisions = (self.q3 / "G1-MAINTAINER-DECISIONS.md").read_text(encoding="utf-8")
        rows = self.manifest()
        self.assertTrue(all(row["maintainer_approval_status"] == "approved" for row in rows))
        pending = re.sub(
            r"(?m)^(\| G1 \| Final feasibility gate \|).*?\| approved \| 2026-10-24 \| @aditmer \|$",
            r"\1 Final G1 authorization remains pending. | pending_maintainer | — | — |",
            decisions,
            count=1,
        )
        self.assertNotEqual(pending, decisions)
        validate_q3_g1_authorization(pending, rows)

    def test_g1_requires_s23_access_and_s19_rights_evidence_after_version_approval(self):
        rows = self.manifest()
        s19 = next(row for row in rows if row["source_id"] == "S19")
        s23 = next(row for row in rows if row["source_id"] == "S23")
        for source_id in ("S18", "S19", "S23"):
            self.approve_source(next(row for row in rows if row["source_id"] == source_id))
        decisions = (self.q3 / "G1-MAINTAINER-DECISIONS.md").read_text(encoding="utf-8")
        approved = self.with_g1_decision(decisions, "approved")

        s19["rights_review_evidence"] = ""
        with self.assertRaisesRegex(ValueError, "requires documented S19 rights-review evidence"):
            validate_q3_g1_authorization(approved, rows)
        s19["rights_review_evidence"] = "CC BY conditions documented; third-party material excluded from planned annotations."
        s23["assigned_reviewer_access_status"] = "unverified"
        s23["assigned_reviewer_access_evidence"] = ""
        with self.assertRaisesRegex(ValueError, "requires confirmed S23 assigned-reviewer access"):
            validate_q3_g1_authorization(approved, rows)
        s23["assigned_reviewer_access_status"] = "confirmed"
        s23["assigned_reviewer_access_evidence"] = "Assigned reviewers confirmed individual institutional access."
        validate_q3_g1_authorization(self.with_s19_inventory_confirmation(approved), rows)

    def test_g1_can_be_authorized_after_source_and_access_evidence(self):
        rows = self.manifest()
        s19 = next(row for row in rows if row["source_id"] == "S19")
        s23 = next(row for row in rows if row["source_id"] == "S23")
        validate_q3_source_manifest(rows, self.rules["reports"], self.retrieval_log())
        self.assertEqual(s19["rights_review_status"], "third_party_review_pending")
        self.assertEqual(s23["assigned_reviewer_access_status"], "confirmed")
        self.assertEqual(s23["storage_sharing_status"], "unverified")

        decisions = (self.q3 / "G1-MAINTAINER-DECISIONS.md").read_text(encoding="utf-8")
        approved = self.with_s19_inventory_confirmation(self.with_g1_decision(decisions, "approved"))
        validate_q3_g1_authorization(approved, rows)

    def authorized_g1_fixture(self):
        rows = self.manifest()
        for row in rows:
            self.approve_source(row)
        s23 = next(row for row in rows if row["source_id"] == "S23")
        s23["assigned_reviewer_access_status"] = "confirmed"
        s23["assigned_reviewer_access_evidence"] = "Assigned reviewers confirmed lawful individual access and component hashes."
        decisions = (self.q3 / "G1-MAINTAINER-DECISIONS.md").read_text(encoding="utf-8")
        return self.with_s19_inventory_confirmation(self.with_g1_decision(decisions, "approved")), rows

    def test_g1_requires_matching_explicit_approval_for_every_frozen_source(self):
        for source_id in (report["source_id"] for report in self.rules["reports"]):
            for field, value in (
                ("maintainer_approval_status", "pending_maintainer"),
                ("approved_version_id", "different-version"),
                ("approval_date", ""),
                ("approving_maintainer", ""),
            ):
                with self.subTest(source_id=source_id, field=field):
                    decisions, rows = self.authorized_g1_fixture()
                    next(row for row in rows if row["source_id"] == source_id)[field] = value
                    with self.assertRaisesRegex(ValueError, "requires an approved matching source version"):
                        validate_q3_g1_authorization(decisions, rows)

    def test_g1_requires_separate_dated_s19_inventory_confirmation(self):
        for status, approval_date, approver in (
            ("pending_maintainer", "—", "—"),
            ("approved", "", "@maintainer"),
            ("approved", "2026-02-30", "@maintainer"),
            ("approved", "2026-10-23", ""),
        ):
            with self.subTest(status=status, approval_date=approval_date, approver=approver):
                decisions, rows = self.authorized_g1_fixture()
                decisions = self.with_s19_inventory_confirmation(decisions, status, approval_date, approver)
                with self.assertRaisesRegex(ValueError, "requires a dated maintainer confirmation of S19 private inventory"):
                    validate_q3_g1_authorization(decisions, rows)

    def test_g1_rejects_missing_s19_inventory_confirmation(self):
        decisions, rows = self.authorized_g1_fixture()
        decisions = "\n".join(
            line for line in decisions.splitlines() if not line.startswith("| S19-INVENTORY |")
        )
        with self.assertRaisesRegex(ValueError, "requires a dated maintainer confirmation of S19 private inventory"):
            validate_q3_g1_authorization(decisions, rows)

    def test_g1_can_be_authorized_with_all_approvals_and_separate_inventory_confirmation(self):
        decisions, rows = self.authorized_g1_fixture()
        validate_q3_source_manifest(rows, self.rules["reports"], self.retrieval_log())
        validate_q3_g1_authorization(decisions, rows)

    def test_g1_requires_exactly_the_frozen_source_set(self):
        for mutation in ("missing", "duplicate", "unknown"):
            with self.subTest(mutation=mutation):
                decisions, rows = self.authorized_g1_fixture()
                if mutation == "missing":
                    rows.pop()
                elif mutation == "duplicate":
                    rows.append(rows[0].copy())
                else:
                    rows[0]["source_id"] = "unknown"
                with self.assertRaisesRegex(ValueError, "requires exactly the eight frozen sources"):
                    validate_q3_g1_authorization(decisions, rows)

    def with_s19_inventory_confirmation(
        self, decisions, status="approved", approval_date="2026-10-24", approver="@aditmer",
    ):
        row = (
            "| S19-INVENTORY | Private archive attribution inventory | "
            "Confirm required attribution fields for the exact archived S19 XML; no private location published. "
            f"| {status} | {approval_date} | {approver} |"
        )
        if re.search(r"(?m)^\| S19-INVENTORY \|", decisions):
            return re.sub(r"(?m)^\| S19-INVENTORY \|.*$", row, decisions)
        return decisions + "\n" + row + "\n"

    def approve_source(self, row):
        row["maintainer_approval_status"] = "approved"
        row["approved_version_id"] = row["source_version_id"]
        row["approval_date"] = "2026-10-24"
        row["approving_maintainer"] = "@aditmer"

    def with_g1_decision(self, decisions, status):
        replacement = (
            f"| G1 | Final feasibility gate | Explicitly authorize G1; G2 remains NO-GO. "
            f"| {status} | 2026-10-24 | @aditmer |"
        )
        return re.sub(
            r"(?m)^\| G1 \| Final feasibility gate \|.*$",
            replacement,
            decisions,
            count=1,
        )

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
        s18["maintainer_approval_status"] = "pending_maintainer"
        s18["approved_version_id"] = s18["source_version_id"]
        s18["approval_date"] = ""
        s18["approving_maintainer"] = ""
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
