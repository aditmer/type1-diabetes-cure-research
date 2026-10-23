import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.q3_archive_verify import main, verify_file


class Q3ArchiveVerifyTests(unittest.TestCase):
    def test_verifies_exact_bytes_and_sha256(self):
        content = b"complete archive bytes\n"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "source.xml"
            path.write_bytes(content)
            result = verify_file(path, len(content), hashlib.sha256(content).hexdigest(), "source")
        self.assertEqual(result["status"], "verified")
        self.assertEqual(result["actual_bytes"], len(content))
        self.assertEqual(result["actual_sha256"], hashlib.sha256(content).hexdigest())

    def test_rejects_corrupted_or_wrong_sized_restore(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "restored.xml"
            path.write_bytes(b"corrupted")
            result = verify_file(path, 10, hashlib.sha256(b"expected!!").hexdigest(), "restore")
        self.assertEqual(result["status"], "mismatch")
        self.assertNotEqual(result["actual_bytes"], result["expected_bytes"])
        self.assertNotEqual(result["actual_sha256"], result["expected_sha256"])

    def test_rejects_empty_or_incomplete_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "placeholder.xml"
            path.write_bytes(b"")
            result = verify_file(path, 1, hashlib.sha256(b"x").hexdigest(), "restore")
        self.assertEqual(result["status"], "mismatch")
        self.assertEqual(result["actual_bytes"], 0)

    def test_rejects_non_regular_file(self):
        with tempfile.TemporaryDirectory() as directory:
            result = verify_file(Path(directory), 1, "0" * 64, "restore")
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["error"], "not_regular_file")

    def test_cli_emits_machine_readable_result_without_path(self):
        content = b"private path must not appear"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "private-source.xml"
            path.write_bytes(content)
            output = []
            with patch("builtins.print", side_effect=output.append):
                exit_code = main([
                    str(path),
                    "--expected-bytes", str(len(content)),
                    "--expected-sha256", hashlib.sha256(content).hexdigest(),
                    "--purpose", "restore",
                ])
        self.assertEqual(exit_code, 0)
        result = json.loads(output[0])
        self.assertEqual(result["status"], "verified")
        self.assertEqual(result["purpose"], "restore")
        self.assertNotIn(str(path), output[0])


if __name__ == "__main__":
    unittest.main()
