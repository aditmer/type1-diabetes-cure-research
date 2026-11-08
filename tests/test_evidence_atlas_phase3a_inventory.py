import csv
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "docs" / "evidence-atlas" / "PHASE-3A-SOURCE-RIGHTS-INVENTORY.md"


def catalog_ids(filename, column):
    with (ROOT / "data" / filename).open(encoding="utf-8", newline="") as stream:
        return {row[column] for row in csv.DictReader(stream)}


class EvidenceAtlasPhase3AInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = INVENTORY.read_text(encoding="utf-8")
        cls.lines = cls.text.splitlines()
        cls.source_ids = catalog_ids("sources.csv", "source_id")
        cls.trial_ids = catalog_ids("trials.csv", "registry_id")

    def test_inventory_has_exactly_one_row_for_every_catalog_source_and_trial(self):
        source_rows = re.findall(r"^\|\s*(S\d+)\s*\|", self.text, re.MULTILINE)
        trial_rows = re.findall(
            r"^\|\s*((?:NCT\d+)|(?:ChiCTR\d+))\s*\|", self.text, re.MULTILINE)
        self.assertEqual(set(source_rows), self.source_ids)
        self.assertEqual(len(source_rows), len(self.source_ids))
        self.assertEqual(set(trial_rows), self.trial_ids)
        self.assertEqual(len(trial_rows), len(self.trial_ids))

    def test_inventory_source_and_trial_references_resolve_to_catalog(self):
        source_refs = set(re.findall(r"\bS\d+\b", self.text))
        trial_refs = set(re.findall(r"\b(?:NCT\d+|ChiCTR\d+)\b", self.text))
        self.assertFalse(source_refs - self.source_ids)
        self.assertFalse(trial_refs - self.trial_ids)

    def test_q3_restrictions_and_uncertain_cohort_links_are_preserved(self):
        rows = {
            re.match(r"^\|\s*(S\d+)\s*\|", line).group(1): line
            for line in self.lines
            if re.match(r"^\|\s*(S\d+)\s*\|", line)
        }
        self.assertIn("mmc2.xlsx", rows["S18"])
        self.assertIn("CC BY-NC-ND 4.0", rows["S18"])
        self.assertIn("clinical_content_reviewed=false", rows["S18"])
        self.assertIn("human review is pending", rows["S18"])
        self.assertIn("third-party exceptions", rows["S19"])
        self.assertIn("MOESM4", rows["S19"])
        self.assertIn("MOESM1", rows["S19"])
        self.assertIn("All six Q3 cohort-link ledger statuses remain uncertain", self.text)
        self.assertIn("NCT04786262-history-v32", rows["S4"])
        self.assertIn("NCT05791201-history-v26", rows["S9"])
        self.assertIn("NCT02239354-history-v13", rows["S17"])
        self.assertIn("NCT03163511-history-v20", rows["S20"])


if __name__ == "__main__":
    unittest.main()
