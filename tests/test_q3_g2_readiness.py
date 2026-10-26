import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
G2_DECISION_URL = (
    "https://github.com/aditmer/type1-diabetes-cure-research/issues/33"
    "#issuecomment-6423910299"
)
REVIEWED_PR_38_COMMIT = "e45c5dca5b623ba9ab7ed607c0ebf9c72be6ad35"
SEPARATE_ACCEPTANCE_GATE = (
    "G1 approval or passing synthetic tests alone do not imply G2 acceptance."
)


class Q3G2ReadinessTests(unittest.TestCase):
    def test_g1_or_synthetic_passes_do_not_imply_g2_acceptance(self):
        for relative_path in ("README.md", "docs/SPRINT-02.md"):
            with self.subTest(document=relative_path):
                document = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn(SEPARATE_ACCEPTANCE_GATE, document)
                self.assertIn(G2_DECISION_URL, document)
                self.assertIn(REVIEWED_PR_38_COMMIT, document)


if __name__ == "__main__":
    unittest.main()
