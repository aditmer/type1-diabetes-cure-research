import copy
import json
import unittest

from scripts.validate_evidence_atlas_taxonomy import (
    TAXONOMY_PATH,
    TaxonomyError,
    serialize_taxonomy,
    validate_taxonomy,
)


def taxonomy():
    return json.loads(TAXONOMY_PATH.read_text(encoding="utf-8"))


class EvidenceAtlasTaxonomyTests(unittest.TestCase):
    def test_committed_taxonomy_is_valid(self):
        validate_taxonomy(taxonomy())

    def test_identifiers_are_unique_across_all_taxonomy_entries(self):
        data = taxonomy()
        data["endpoints"][0]["id"] = data["categories"][0]["id"]
        with self.assertRaisesRegex(TaxonomyError, "duplicate identifier"):
            validate_taxonomy(data)

    def test_category_relationship_references_must_resolve(self):
        data = taxonomy()
        data["relationships"][0]["object_id"] = "TI-NOT-DEFINED"
        with self.assertRaisesRegex(TaxonomyError, "references must resolve"):
            validate_taxonomy(data)

    def test_duplicate_symmetric_relationship_is_rejected(self):
        data = taxonomy()
        relationship = next(r for r in data["relationships"]
                            if r["relation"] == "may_overlap_with")
        data["relationships"].append({
            **relationship,
            "subject_id": relationship["object_id"],
            "object_id": relationship["subject_id"],
        })
        with self.assertRaisesRegex(TaxonomyError, "duplicate taxonomy relationship"):
            validate_taxonomy(data)

    def test_contradictory_overlap_and_exclusion_relationships_are_rejected(self):
        data = taxonomy()
        relationship = next(r for r in data["relationships"]
                            if r["relation"] == "may_overlap_with")
        data["relationships"].append({
            **relationship,
            "relation": "mutually_exclusive_with",
        })
        with self.assertRaisesRegex(TaxonomyError, "contradictory"):
            validate_taxonomy(data)

    def test_ancestor_and_descendant_cannot_be_mutually_exclusive(self):
        data = taxonomy()
        data["relationships"].append({
            "subject_id": "TI-PREVENT-DELAY",
            "relation": "mutually_exclusive_with",
            "object_id": "TI-DISEASE-MODIFICATION",
            "description": "Contradictory hierarchy relation used by validation test.",
        })
        with self.assertRaisesRegex(TaxonomyError, "ancestor and descendant"):
            validate_taxonomy(data)

    def test_parent_cycle_is_rejected(self):
        data = taxonomy()
        data["relationships"].append({
            "subject_id": "TI-DISEASE-MODIFICATION",
            "relation": "is_a",
            "object_id": "TI-PREVENT-DELAY",
            "description": "Contradictory cycle used by validation test.",
        })
        with self.assertRaisesRegex(TaxonomyError, "is_a cycle"):
            validate_taxonomy(data)

    def test_descriptions_are_required(self):
        data = taxonomy()
        data["facets"][0]["values"][0]["description"] = " "
        with self.assertRaisesRegex(TaxonomyError, "description is required"):
            validate_taxonomy(data)

    def test_version_integrity(self):
        data = taxonomy()
        data["version"] = "2.0.0"
        with self.assertRaisesRegex(TaxonomyError, "major version must match"):
            validate_taxonomy(data)
        data = taxonomy()
        data["version"] = "01.0.0"
        with self.assertRaisesRegex(TaxonomyError, "semantic versioning"):
            validate_taxonomy(data)

    def test_endpoint_question_references_are_valid(self):
        data = taxonomy()
        data["endpoints"][0]["research_question_ids"].append("RQ-99")
        with self.assertRaisesRegex(TaxonomyError, "references must be unique and valid"):
            validate_taxonomy(data)

    def test_serialization_is_deterministic_for_object_key_order(self):
        original = taxonomy()
        reordered = copy.deepcopy(original)
        reordered = {key: reordered[key] for key in reversed(list(reordered))}
        reordered["categories"][0] = {
            key: reordered["categories"][0][key]
            for key in reversed(list(reordered["categories"][0]))
        }
        self.assertEqual(serialize_taxonomy(original), serialize_taxonomy(reordered))
        self.assertTrue(serialize_taxonomy(original).endswith("\n"))

    def test_validation_script_targets_committed_file(self):
        self.assertTrue(TAXONOMY_PATH.is_file())
        self.assertEqual(TAXONOMY_PATH.name, "taxonomy-v1.json")


if __name__ == "__main__":
    unittest.main()
