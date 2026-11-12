"""Exact-head, zero-skip CI verification. Missing XML fails closed."""
import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

def assess(counts: dict, minimum: int = 1) -> bool:
    return (counts["tests"] >= minimum and counts["tests"] - counts["skipped"] >= minimum
            and counts["skipped"] == counts["failures"] == counts["errors"] == 0)

def main():
    expected = os.environ.get("PR_HEAD_SHA", "")
    actual = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    try:
        root = ET.parse("pytest-report.xml").getroot()
        suites = [root] if root.tag == "testsuite" else root.findall("./testsuite")
        if not suites:
            raise ValueError("missing_test_suites")
        counts = {k: sum(int(s.attrib.get(k, 0)) for s in suites)
                  for k in ("tests", "skipped", "failures", "errors")}
        verified = assess(counts, 10) and expected == actual and len(expected) == 40
    except (OSError, ValueError, ET.ParseError):
        counts = {"tests": 0, "skipped": 0, "failures": 0, "errors": 1}
        verified = False
    receipt = {"pr_head_sha": expected, "checkout_git_head": actual,
               "timestamp_utc": datetime.now(timezone.utc).isoformat(),
               "counts": counts, "security_gate_verified": verified}
    with open("ci-evidence-receipt.json", "w") as f:
        json.dump(receipt, f, indent=2)
    print(json.dumps(receipt, indent=2))
    return 0 if verified else 1

if __name__ == "__main__":
    sys.exit(main())
