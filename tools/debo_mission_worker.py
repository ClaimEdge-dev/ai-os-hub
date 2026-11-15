#!/usr/bin/env python3
"""DEBO scoped read-only worker: validate canonical agent registry and emit dashboard-safe receipt."""
import argparse
import datetime
import json
from pathlib import Path
from debo_agent_coverage_audit import audit

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "governance/DEBO_AGENT_COVERAGE_REGISTER_v1.json"

def execute(root=ROOT):
    registry = json.loads((root / "governance/DEBO_AGENT_COVERAGE_REGISTER_v1.json").read_text())
    report = audit(registry, root=root, check_files=True)
    return {
        "schema_version": "debo.worker.receipt.v1",
        "job_id": "DEBO-MASTER-011-WORKER-01",
        "project_id": "DEBO",
        "role_route": ["Mack", "Scout", "Proof", "Vault"],
        "operation": "read_only_agent_coverage_audit",
        "result": report["status"],
        "roles_checked": report["roles"],
        "sister_projects_checked": report["sister_projects"],
        "specialist_skills_checked": report["jct_skills"],
        "errors": report["errors"],
        "dashboard_lane": "DONE" if report["status"] == "PASS" else "BLOCKED",
        "runtime_scope": "local_or_ci_process_only",
        "autonomous_background_worker_verified": False,
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    result = execute()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf8")
    print(json.dumps(result))
    return 0 if result["result"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
