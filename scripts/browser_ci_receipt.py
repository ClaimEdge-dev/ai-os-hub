"""Fail-closed, exact-commit, zero-skip QA receipt (not a digital signature)."""
import hashlib
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


def assess(counts: dict, minimum: int = 1) -> bool:
    return (counts["tests"] >= minimum and counts["tests"] - counts["skipped"] >= minimum
            and counts["skipped"] == counts["failures"] == counts["errors"] == 0)


def verify_receipt(expected: str, actual: str, outcome: str, counts: dict) -> bool:
    return (bool(re.fullmatch(r"[0-9a-f]{40}", expected)) and
            expected == actual and outcome == "success" and assess(counts, minimum=20))


def main():
    expected = os.environ.get("PR_HEAD_SHA", "")
    outcome = os.environ.get("QA_OUTCOME", "unavailable")
    try:
        actual = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        actual = ""
    report = Path("pytest-report.xml")
    report_hash = None
    try:
        raw = report.read_bytes()
        report_hash = hashlib.sha256(raw).hexdigest()
        root = ET.fromstring(raw)
        suites = [root] if root.tag == "testsuite" else root.findall("./testsuite")
        if not suites:
            raise ValueError("missing_test_suites")
        counts = {k: sum(int(s.attrib.get(k, 0)) for s in suites)
                  for k in ("tests", "skipped", "failures", "errors")}
        verified = verify_receipt(expected, actual, outcome, counts)
    except (OSError, ValueError, ET.ParseError):
        counts = {"tests": 0, "skipped": 0, "failures": 0, "errors": 1}
        verified = False

    receipt = {
        "schema": "debo-browser-ci-receipt-v2",
        "pr_head_sha": expected,
        "checkout_git_head": actual,
        "github_run_id": os.environ.get("GITHUB_RUN_ID", ""),
        "github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT", ""),
        "pytest_step_outcome": outcome,
        "pytest_report_sha256": report_hash,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "counts": counts,
        "security_gate_verified": verified,
        "attestation": "UNSIGNED; independent GitHub checks and human review required",
    }
    Path("ci-evidence-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))
    return 0 if verified else 1


if __name__ == "__main__":
    sys.exit(main())
