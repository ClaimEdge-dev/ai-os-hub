#!/usr/bin/env python3
"""DEBO verification batch runner: explicit original/readback pairs, no network."""
import argparse
import datetime
import json
import pathlib
import subprocess
import sys

def main():
    p = argparse.ArgumentParser()
    p.add_argument("manifest")
    p.add_argument("--gate", default="tools/debo_durable_save_gate.py")
    p.add_argument("--receipt")
    args = p.parse_args()
    data = json.loads(pathlib.Path(args.manifest).read_text())
    results = []
    for item in data.get("artifacts", []):
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
    output = json.dumps(receipt, indent=2)
    print(output)
    if args.receipt:
        pathlib.Path(args.receipt).write_text(output + "\n")
    return 0 if receipt["status"] == "VERIFIED" else 1

if __name__ == "__main__":
    sys.exit(main())
