#!/usr/bin/env python3
"""R128 read-only recovery and delegation pilot, reusing existing R31 router.

Private/approved checkpoint stores are authoritative in real operations.
This harness never fetches apps, creates agents, writes a database, sends a
message, deploys code, or claims actual runtime installation.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
from typing import Any

from debo_r31_decision_router import APPROVAL_ACTIONS, Task, batch

PASS_TYPES = frozenset({"source_readback", "test_receipt", "runtime_probe", "owner_approval"})
ACTION_EVIDENCE = {
    "read_source": {"source_readback"}, "compare_fingerprints": {"source_readback"},
    "run_local_tests": {"test_receipt"}, "fix_nonproduction_code": {"test_receipt"},
    "write_dev_checkpoint": {"source_readback"}, "verify_readback": {"source_readback", "runtime_probe"},
    "prepare_migration": {"source_readback"}, "prepare_mapping_review": {"source_readback"},
    "retry_read_only": {"runtime_probe", "source_readback"},
}

ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{3,95}$")
MAX_TASKS = 50


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(document: object) -> dict:
    if not isinstance(document, dict) or document.get("schema") != "debo.r128.pilot.v1":
        raise ValueError("invalid R128 pilot schema")
    for name in ("project_id", "source_revision"):
        if not _nonempty(document.get(name)):
            raise ValueError("missing project or source revision")
    tasks, receipts = document.get("tasks"), document.get("receipts")
    if not isinstance(tasks, list) or not 0 < len(tasks) <= MAX_TASKS or not isinstance(receipts, list):
        raise ValueError("bounded tasks and receipts required")
    ids = []
    for row in tasks:
        if not isinstance(row, dict) or not ID_RE.fullmatch(str(row.get("id", ""))):
            raise ValueError("invalid task row/id")
        if row.get("project_id") != document["project_id"]:
            raise ValueError("cross-project task is not allowed")
        if not _nonempty(row.get("action")):
            raise ValueError("missing action")
        deps = row.get("depends_on", [])
        if not isinstance(deps, list) or any(not isinstance(d, str) for d in deps):
            raise ValueError("invalid dependencies")
        ids.append(row["id"])
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate task ids")
    for row in tasks:
        if row["id"] in row.get("depends_on", []) or not set(row.get("depends_on", [])).issubset(ids):
            raise ValueError("self-reference or unknown dependency")
    receipt_ids = []
    for row in receipts:
        if not isinstance(row, dict) or row.get("task_id") not in ids or row.get("project_id") != document["project_id"]:
            raise ValueError("unrecognized or cross-project receipt")
        # The same task may have receipts for successive source revisions.
        # A duplicate for the same task AND revision remains an error.
        receipt_ids.append((row["task_id"], row.get("source_revision")))
        if row.get("state") not in ("PASS", "FAILED", "BLOCKED"):
            raise ValueError("unknown receipt state")
        if row["state"] == "PASS":
            if row.get("evidence_type") not in PASS_TYPES or not _nonempty(row.get("evidence_ref")):
                raise ValueError("passed receipt missing typed evidence ref")
        if not _nonempty(row.get("source_revision")):
            raise ValueError("receipt revision missing")
    if len(receipt_ids) != len(set(receipt_ids)):
        raise ValueError("duplicate receipts")
    return document


def plan(document: dict) -> dict:
    """Return only an execution *plan*. Evidence pointers are not authenticated here."""
    data = validate(document)
    source_revision = data["source_revision"]
    matching = {r["task_id"]: r for r in data["receipts"]
                if r["source_revision"] == source_revision}
    actions = {t["id"]: t["action"] for t in data["tasks"]}
    # Typed refs are an offline candidate gate, never a substitute for real approvals.
    verified = {task_id for task_id, receipt in matching.items()
                if receipt["state"] == "PASS"
                and actions[task_id] not in APPROVAL_ACTIONS
                and receipt.get("evidence_type") in ACTION_EVIDENCE.get(actions[task_id], set())}
    ignored_approval_receipts = sorted(
        task_id for task_id, receipt in matching.items()
        if receipt["state"] == "PASS" and actions[task_id] in APPROVAL_ACTIONS)
    mismatched_proof_receipts = sorted(
        task_id for task_id, receipt in matching.items()
        if receipt["state"] == "PASS" and actions[task_id] not in APPROVAL_ACTIONS
        and receipt.get("evidence_type") not in ACTION_EVIDENCE.get(actions[task_id], set()))
    failed = {t for t, r in matching.items() if r["state"] in ("FAILED", "BLOCKED")}
    stale = sorted(r["task_id"] for r in data["receipts"] if r["source_revision"] != source_revision)
    tasks = [Task(row["id"], row["action"], tuple(row.get("depends_on", []))) for row in data["tasks"]]
    decisions = batch(tasks, verified, failed)
    # The returned counts describe a static fixture, NOT observed tool invocations.
    out = {
        "schema": "debo.r128.plan.v1",
        "mode": "DRY_RUN_NO_EXTERNAL_EFFECT",
        "project_id": data["project_id"],
        "source_revision": source_revision,
        "skipped_verified": sorted(verified),
        "ignored_approval_receipts": ignored_approval_receipts,
        "ignored_mismatched_proof_receipts": mismatched_proof_receipts,
        "stale_receipts_need_reverification": stale,
        "route": decisions,
        "metrics_fixture": {
            "candidate_steps": len(tasks),
            "already_verified_steps": len(verified),
            "routed_auto_steps": len(decisions["auto"]),
            "owner_approval_steps": len(decisions["approval"]),
            "blocked_steps": len(decisions["blocked"]),
            "actual_external_tool_calls": 0
        },
        "limits": ["typed evidence refs are not independently authenticated",
                   "no ChatGPT or external agent runtime was installed",
                   "no actual speed/cost savings measured"]
    }
    return out


def mack_forge_proof_pilot(values: list[int]) -> dict:
    """Mock three *logical roles* using a pure local function with trace."""
    trace: list[dict[str, Any]] = []
    if not isinstance(values, list) or not values or any(type(v) is not int for v in values):
        return {"status": "BLOCKED", "trace": [{"role": "Mack", "result": "invalid_input"}]}
    trace.append({"role": "Mack", "action": "route_pure_math", "to": "Forge"})
    result = sum(values)
    trace.append({"role": "Forge", "action": "compute_sum", "output": result, "to": "Proof"})
    # Independent-style verification using a second implementation, not a second agent.
    independent_total = 0
    for value in values:
        independent_total += value
    passed = result == independent_total and all(-10**9 <= v <= 10**9 for v in values)
    trace.append({"role": "Proof", "action": "verify_output", "passed": passed})
    return {"status": "TESTED" if passed else "BLOCKED",
            "trace": trace, "independent_agents_running": False}


def classify_failure(code: str) -> dict:
    """Demo classification only, no real retries/calls."""
    routes = {
        "AUTH_401": ("OWNER_APPROVAL", 0),
        "AUTH_403": ("OWNER_APPROVAL", 0),
        "NETWORK_TIMEOUT": ("RETRY_READ_ONLY_ONCE", 1),
        "RATE_LIMIT": ("WAIT_FOR_RETRY_AFTER", 0),
        "DUPLICATE_REQUEST": ("SKIP_DUPLICATE", 0),
        "DATA_CONFLICT": ("VERIFY_SOURCE", 0),
        "UNKNOWN": ("BLOCKED", 0),
    }
    route, retries = routes.get(code, routes["UNKNOWN"])
    return {"error": code, "route": route, "max_automatic_retries": retries}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="public synthetic fixture only; real private checkpoints remain private")
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    print(json.dumps({"routing": plan(data),
                      "handoff_demo": mack_forge_proof_pilot([2, 3, 5]),
                      "failure_demo": [classify_failure(k) for k in
                          ("AUTH_403", "NETWORK_TIMEOUT", "DUPLICATE_REQUEST")]},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
