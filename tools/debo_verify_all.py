#!/usr/bin/env python3
"""DEBO verification batch runner: explicit original/readback pairs, no network."""
import argparse
import datetime
import json
import pathlib
import re
import subprocess
import sys


def preflight(data):
    """Reject a malformed or duplicated batch before running any verification gate."""
    issues = []
    if not isinstance(data, dict) or not isinstance(data.get("artifacts"), list):
        return ["Manifest must contain an artifacts list"]
    if not data["artifacts"]:
        return ["Manifest artifacts list is empty"]
    ids, pairs, destinations = set(), set(), set()
    for index, item in enumerate(data["artifacts"], start=1):
        prefix = f"Artifact {index}"
        if not isinstance(item, dict):
            issues.append(f"{prefix}: expected an object")
            continue
        for key in ("id", "original", "readback"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                issues.append(f"{prefix}: {key} must be a nonempty string")
        if any(not isinstance(item.get(k), str) or not item[k].strip()
               for k in ("id", "original", "readback")):
            continue
        if item["id"] in ids:
            issues.append(f"{prefix}: duplicate artifact id {item['id']!r}")
        ids.add(item["id"])
        pair = (item["original"], item["readback"])
        if pair in pairs:
            issues.append(f"{prefix}: duplicate original/readback pair")
        pairs.add(pair)
        destination = item.get("destination")
        if destination is not None:
            if not isinstance(destination, str) or not destination.strip():
                issues.append(f"{prefix}: destination must be a nonempty string when supplied")
            elif destination in destinations:
                issues.append(f"{prefix}: duplicate destination {destination!r}")
            else:
                destinations.add(destination)
        expected = item.get("expected_sha256")
        if expected is not None and (not isinstance(expected, str)
                                     or not re.fullmatch(r"[0-9a-fA-F]{64}", expected)):
            issues.append(f"{prefix}: expected_sha256 must be 64 hex characters")
    return issues


def main():
    p = argparse.ArgumentParser()
    p.add_argument("manifest")
    p.add_argument("--gate", default="tools/debo_durable_save_gate.py")
    p.add_argument("--receipt")
    args = p.parse_args()
    issues = []
    try:
        data = json.loads(pathlib.Path(args.manifest).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        data = None
        issues = [f"Manifest unavailable or invalid JSON: {type(exc).__name__}"]
    if not issues:
        issues = preflight(data)
    results = []
    if not issues:
        for item in data["artifacts"]:
            cmd = [sys.executable, args.gate, item["original"], item["readback"]]
            if item.get("expected_sha256"):
                cmd += ["--expected-sha256", item["expected_sha256"]]
            proc = subprocess.run(cmd, text=True, capture_output=True)
            try:
                detail = json.loads(proc.stdout)
            except json.JSONDecodeError:
                detail = {"stdout": proc.stdout, "stderr": proc.stderr}
            results.append({"id": item["id"], "destination": item.get("destination"),
                            "exit_code": proc.returncode, "result": detail})
    receipt = {"schema": "DEBO-VERIFY-ALL-v1",
               "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "results": results,
               "status": "VERIFIED" if results and all(r["exit_code"] == 0 for r in results) else "BLOCKED"}
    if issues:
        receipt["preflight_issues"] = issues
    receipt["gate_invocations"] = len(results)
    output = json.dumps(receipt, indent=2)
    print(output)
    if args.receipt:
        pathlib.Path(args.receipt).write_text(output + "\n", encoding="utf-8")
    return 0 if receipt["status"] == "VERIFIED" else 1


if __name__ == "__main__":
    sys.exit(main())
