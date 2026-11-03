import csv
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CROSSWALK = ROOT / "docs" / "EVIDENCE-ATLAS-SOURCE-CROSSWALK.md"
TAXONOMY = ROOT / "experiments" / "evidence-atlas" / "taxonomy-v1.json"


def catalog_ids(filename, column):
    with (ROOT / "data" / filename).open(encoding="utf-8", newline="") as stream:
        return {row[column] for row in csv.DictReader(stream)}


class EvidenceAtlasCrosswalkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = CROSSWALK.read_text(encoding="utf-8")
        cls.source_ids = catalog_ids("sources.csv", "source_id")
        cls.trial_ids = catalog_ids("trials.csv", "registry_id")
        cls.taxonomy = json.loads(TAXONOMY.read_text(encoding="utf-8"))

    def test_every_catalog_record_has_exactly_one_crosswalk_row(self):
        source_rows = re.findall(r"^\|\s*(S\d+)\s*\|", self.text, re.MULTILINE)
        trial_rows = re.findall(r"^\|\s*((?:NCT\d+)|(?:ChiCTR\d+))\s*\|",
                                self.text, re.MULTILINE)
        self.assertEqual(set(source_rows), self.source_ids)
        self.assertEqual(len(source_rows), len(self.source_ids))
        self.assertEqual(set(trial_rows), self.trial_ids)
        self.assertEqual(len(trial_rows), len(self.trial_ids))

    def test_all_source_and_registry_references_resolve(self):
        source_refs = set(re.findall(r"\bS\d+\b", self.text))
        trial_refs = set(re.findall(r"\b(?:NCT\d+|ChiCTR\d+)\b", self.text))
        self.assertEqual(source_refs - self.source_ids, set())
        self.assertEqual(trial_refs - self.trial_ids, set())

    def test_taxonomy_and_question_references_resolve(self):
        category_ids = {entry["id"] for entry in self.taxonomy["categories"]}
        question_ids = {entry["id"] for entry in self.taxonomy["research_questions"]}
        category_refs = set(re.findall(r"\b(?:TI|TM)-(?:[A-Z0-9]+-)*[A-Z0-9]+\b", self.text))
        question_refs = set(re.findall(r"\bRQ-\d{2}\b", self.text))
        self.assertEqual(category_refs - category_ids, set())
        self.assertEqual(question_refs - question_ids, set())
        self.assertIsNone(re.search(r"\bRQ-\d{2},\d{2}\b", self.text))

    def test_primary_question_maps_to_human_studies_and_trial_records(self):
        lines = self.text.splitlines()
        for identifier in ("S3", "S11", "S27", "S29", *self.trial_ids):
            with self.subTest(identifier=identifier):
                row = next(line for line in lines if line.startswith(f"| {identifier} |"))
                question_column = 3 if identifier.startswith("S") else 4
                self.assertIn("RQ-00", row.split("|")[question_column])
        preclinical_row = next(line for line in lines if line.startswith("| S14 |"))
        self.assertNotIn("RQ-00", preclinical_row.split("|")[3])

    def test_cell_pouch_is_not_assigned_immune_protection_from_scaffold_alone(self):
        row = next(line for line in self.text.splitlines() if line.startswith("| S21 |"))
        self.assertNotIn("TM-ENCAPSULATED-CELL", row)
        self.assertIn("not immune-isolating", row)

    def test_edited_primary_islet_model_is_identified_without_generalizing(self):
        row = next(line for line in self.text.splitlines() if line.startswith("| S14 |"))
        self.assertIn("TM-GENE-EDITED-CELL for the edited primary-islet model", row)
        self.assertNotIn("TM-STEM-CELL-ISLET", row)
        self.assertIn("does not establish whether the separate iPSC grafts are islets", row)
        self.assertIn("edited primary islets in a rhesus recipient", row)

    def test_allogeneic_transplantation_does_not_imply_editing(self):
        row = next(line for line in self.text.splitlines() if line.startswith("| S15 |"))
        self.assertIn("TM-ALLOGENEIC-CELL", row)
        self.assertNotIn("TM-GENE-EDITED-CELL", row)
        self.assertIn("does not specify cell origin, genetic modification, or mechanism", row)


if __name__ == "__main__":
    unittest.main()
