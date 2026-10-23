#!/usr/bin/env python3
"""Verify exact bytes for Q3 source files and fresh archive restores."""
import argparse
import hashlib
import json
import re
import stat
import sys
from pathlib import Path

SHA256 = re.compile(r"[0-9a-fA-F]{64}")


def verify_file(path, expected_bytes, expected_sha256, purpose):
    expected_sha256 = expected_sha256.lower()
    result = {
        "purpose": purpose,
        "status": "error",
        "expected_bytes": expected_bytes,
        "expected_sha256": expected_sha256,
        "actual_bytes": None,
        "actual_sha256": None,
    }
    try:
        if not stat.S_ISREG(path.stat().st_mode):
            result["error"] = "not_regular_file"
            return result
        digest = hashlib.sha256()
        actual_bytes = 0
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                actual_bytes += len(chunk)
                digest.update(chunk)
        actual_sha256 = digest.hexdigest()
    except OSError:
        result["error"] = "file_read_failed"
        return result

    result["actual_bytes"] = actual_bytes
    result["actual_sha256"] = actual_sha256
    result["status"] = (
        "verified"
        if actual_bytes == expected_bytes and actual_sha256 == expected_sha256
        else "mismatch"
    )
    return result


def positive_integer(value):
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a positive integer") from exc
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def sha256_argument(value):
    if not SHA256.fullmatch(value):
        raise argparse.ArgumentTypeError("must be a 64-character SHA-256 hex digest")
    return value.lower()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="local source or freshly downloaded archive file")
    parser.add_argument("--expected-bytes", required=True, type=positive_integer)
    parser.add_argument("--expected-sha256", required=True, type=sha256_argument)
    parser.add_argument("--purpose", choices=("source", "restore"), required=True)
    args = parser.parse_args(argv)

    result = verify_file(args.file, args.expected_bytes, args.expected_sha256, args.purpose)
    print(json.dumps(result, separators=(",", ":"), sort_keys=True))
    return 0 if result["status"] == "verified" else 1


if __name__ == "__main__":
    sys.exit(main())
