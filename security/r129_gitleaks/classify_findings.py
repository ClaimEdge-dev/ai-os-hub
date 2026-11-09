#!/usr/bin/env python3
"""R129 redacted Gitleaks triage. Never prints actual source keys or finding secrets.

Only a public Supabase sb_publishable_ key in the two exact historical JCT
demo preview files is accepted. This is NOT a generic rule suppression.
Production use of that key remains governed by RLS/RPC and John approval.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

KNOWN_FILES = {
    "projects/jcs-towing/website-v2-preview/app.js",
    "projects/jcs-towing/website-v2-preview/preview-standalone.html",
}
KEY_LINE = re.compile(r"^\s*const KEY=['\"](sb_publishable_[A-Za-z0-9_]{20,80})['\"];\s*$")
MAX_FINDS = 2


def classify(report: object, root: Path, scanner_exit: int) -> dict:
    if scanner_exit not in (0, 1):
        return {"status": "BLOCKED", "reason": "scanner_failed", "findings": None}
    if not isinstance(report, list):
        return {"status": "BLOCKED", "reason": "invalid_scanner_report", "findings": None}
    if scanner_exit == 0 and report:
        return {"status": "BLOCKED", "reason": "inconsistent_scan_status", "findings": len(report)}
    if scanner_exit == 1 and not report:
        return {"status": "BLOCKED", "reason": "finding_report_unavailable", "findings": 0}
    if len(report) > MAX_FINDS:
        return {"status": "BLOCKED", "reason": "additional_findings", "findings": len(report)}
    seen = set()
    observed_keys = set()
    for item in report:
        if not isinstance(item, dict):
            return {"status": "BLOCKED", "reason": "malformed_finding", "findings": len(report)}
        raw_path = str(item.get("File", ""))
        if raw_path.startswith("/source/"):
            relative = raw_path[len("/source/"):]
        else:
            relative = raw_path.removeprefix("./")
        lineno = item.get("StartLine")
        if relative not in KNOWN_FILES or item.get("RuleID") != "generic-api-key":
            return {"status": "BLOCKED", "reason": "unexpected_path_or_rule", "findings": len(report)}
        if not isinstance(lineno, int) or not 1 <= lineno <= 10000 or (relative, lineno) in seen:
            return {"status": "BLOCKED", "reason": "invalid_or_duplicate_location", "findings": len(report)}
        seen.add((relative, lineno))
        source = root / relative
        if not source.is_file():
            return {"status": "BLOCKED", "reason": "missing_source", "findings": len(report)}
        lines = source.read_text(encoding="utf-8").splitlines()
        if lineno > len(lines):
            return {"status": "BLOCKED", "reason": "invalid_line_number", "findings": len(report)}
        match = KEY_LINE.fullmatch(lines[lineno - 1])
        if not match:
            return {"status": "BLOCKED", "reason": "not_pure_publishable_key", "findings": len(report)}
        observed_keys.add(match.group(1))
    if len(observed_keys) > 1:
        return {"status": "BLOCKED", "reason": "public_key_conflict", "findings": len(report)}
    return {
        "status": "PASS_PUBLIC_PUBLISHABLE_KEY_ONLY" if report else "PASS_NO_FINDINGS",
        "findings": len(report),
        "accepted_type": "supabase_publishable_browser_key" if report else None,
        "private_keys_exempted": 0,
        "authorization_note": "JCT RPC/RLS owner acceptance remains separate",
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("report", type=Path)
    p.add_argument("repo_root", type=Path)
    p.add_argument("scanner_exit", type=int)
    a = p.parse_args()
    if not a.report.exists():
        outcome = {"status": "BLOCKED", "reason": "report_missing"}
    else:
        try:
            outcome = classify(json.loads(a.report.read_text(encoding="utf-8")), a.repo_root, a.scanner_exit)
        except (ValueError, OSError, UnicodeError):
            outcome = {"status": "BLOCKED", "reason": "invalid_report_or_files"}
    print(json.dumps(outcome, sort_keys=True))
    if outcome["status"] == "BLOCKED" and a.report.exists():
        # The scan report itself remains private. Surface only sanitized public
        # source locations, never Secret, Match, Context, Commit, or entropy.
        try:
            raw = json.loads(a.report.read_text(encoding="utf-8"))
            if isinstance(raw, list):
                locations = []
                for entry in raw[:20]:
                    if not isinstance(entry, dict):
                        continue
                    filename = str(entry.get("File", "")).removeprefix("/source/")[:180]
                    filename = re.sub(r"[^A-Za-z0-9_./-]", "?", filename)
                    rule = re.sub(r"[^A-Za-z0-9_-]", "?", str(entry.get("RuleID", ""))[:80])
                    line = entry.get("StartLine")
                    if not isinstance(line, int):
                        line = 0
                    locations.append({"file":filename,"line":line,"rule":rule})
                print(json.dumps({"redacted_finding_locations":locations},sort_keys=True))
        except (ValueError, OSError, UnicodeError):
            print("Finding metadata unreadable; scanner remains blocking.")
    raise SystemExit(0 if str(outcome["status"]).startswith("PASS_") else 1)


if __name__ == "__main__":
    main()
