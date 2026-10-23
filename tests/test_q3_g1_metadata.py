import unittest
from pathlib import Path

from scripts.validate_data import (
    Q3_SOURCE_MANIFEST_FIELDS,
    ROOT,
    read_q3_csv,
    validate_q3_amendment,
    validate_q3_metadata,
    validate_q3_source_manifest,
)
import json


class Q3G1MetadataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.q3 = ROOT / "experiments" / "q3"
        cls.rules = json.loads((cls.q3 / "rules-v1.0.json").read_text(encoding="utf-8"))

    def manifest(self):
        return read_q3_csv(self.q3 / "source-manifest.csv", Q3_SOURCE_MANIFEST_FIELDS)

    def retrieval_log(self):
        return read_q3_csv(
            self.q3 / "retrieval-log.csv",
            [
                "artifact_id", "source_id", "retrieved_utc", "request_url",
                "http_status", "media_type", "bytes", "response_sha256",
                "verification_outcome",
            ],
        )

    def test_repository_q3_metadata_is_valid(self):
        self.assertEqual(validate_q3_metadata(), (8, 39))

    def test_manifest_must_match_all_frozen_report_targets(self):
        rows = self.manifest()
        rows[0]["target_population_id"] = "different-target"
        with self.assertRaisesRegex(ValueError, "target_population_id differs"):
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
        with self.assertRaisesRegex(ValueError, "verified archive requires reference and recovery evidence"):
            validate_q3_source_manifest(rows, self.rules["reports"], self.retrieval_log())

    def test_verified_archive_requires_matching_retrieval_records(self):
        rows = self.manifest()
        s13 = next(row for row in rows if row["source_id"] == "S13")
        log = self.retrieval_log()
        archive_record = next(record for record in log if record["artifact_id"] == "S13-archive-v3")
        archive_record["response_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "lacks matching successful retrieval evidence"):
            validate_q3_source_manifest(rows, self.rules["reports"], log)

    def test_recommendation_cannot_populate_maintainer_approval_fields(self):
        rows = self.manifest()
        rows[0]["approved_version_id"] = rows[0]["source_version_id"]
        with self.assertRaisesRegex(ValueError, "recommendations cannot populate approval fields"):
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
