#!/usr/bin/env python3
"""DEBO R19 optional, private-first continuity adapter.

Not a new master or ChatGPT runtime. Never sends network requests.
Input must be project-scoped; checkpoint files should remain in approved private storage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path

STATUS = frozenset({"UNKNOWN", "PROPOSED", "BUILT", "TESTED", "APPROVED", "DEPLOYED", "LIVE", "BLOCKED"})
EVIDENCE_REQUIRED = frozenset({"TESTED", "APPROVED", "DEPLOYED", "LIVE"})
EVIDENCE_TYPES = frozenset({"source_readback", "test_receipt", "owner_approval", "deployment_receipt", "runtime_probe"})
MILESTONE_PROOF = {
    "TESTED": "test_receipt",
    "APPROVED": "owner_approval",
    "DEPLOYED": "deployment_receipt",
    "LIVE": "runtime_probe",
}
EVENT_TYPES = frozenset({"TASK_VERIFIED", "SOURCE_SAVED", "TEST_FAILED", "BLOCKER_RESOLVED", "VERSION_APPROVED", "CHECKPOINT_ADVANCED"})


def normalize(text: str) -> str:
    if not isinstance(text, str) or not text.strip():
        raise ValueError("nonempty text required")
    return re.sub(r"\s+", " ", text).strip().casefold()


def stable_task_id(project_id: str, objective: str, source_key: str | None = None) -> str:
    """Identity is scoped to project, never to thread. Explicit source IDs win.

    This fingerprints exact normalized objectives, not semantic paraphrases.
    Similar-looking tasks require human/source-backed reconciliation.
    """
    project = normalize(project_id).upper()
    value = f"source:{normalize(source_key)}" if source_key and source_key.strip() else f"objective:{normalize(objective)}"
    digest = hashlib.sha256(f"debo-task-v1\0{project}\0{value}".encode()).hexdigest()[:20]
    return f"DEBO-TASK-{digest}"


def _valid_proofs(proofs: object) -> list[dict]:
    if not isinstance(proofs, list):
        raise ValueError("evidence must be a list")
    for item in proofs:
        if not isinstance(item, dict) or item.get("type") not in EVIDENCE_TYPES:
            raise ValueError("evidence must carry recognized type")
        if not isinstance(item.get("ref"), str) or not item["ref"].strip():
            raise ValueError("evidence must carry source reference")
    return proofs


def validate_capsule(c: dict) -> dict:
    if not isinstance(c, dict):
        raise ValueError("capsule must be an object")
    if c.get("schema") != "debo.r19.capsule.v1":
        raise ValueError("invalid capsule schema")
    for field in ("project_id", "mission_id", "objective", "checkpoint", "next_action"):
        normalize(c.get(field))
    if c.get("status") not in STATUS:
        raise ValueError("unknown status")
    evidence = _valid_proofs(c.get("evidence", []))
    required = MILESTONE_PROOF.get(c["status"])
    if required and not any(p["type"] == required for p in evidence):
        raise ValueError(f"{c['status']} requires {required} evidence")
    if c.get("scope", "private") not in ("private", "public_metadata"):
        raise ValueError("unsupported scope")
    if c.get("scope", "private") == "public_metadata" and c.get("private_data"):
        raise ValueError("private data cannot be put in public metadata")
    if c.get("status") in EVIDENCE_REQUIRED and not evidence:
        raise ValueError("evidence required for status")
    if not isinstance(c.get("task_id"), str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{3,127}", c["task_id"]):
        raise ValueError("invalid task_id")
    return c


def new_capsule(project_id: str, mission_id: str, objective: str, status: str,
                checkpoint: str, next_action: str, evidence: list[dict] | None = None,
                source_key: str | None = None, scope: str = "private") -> dict:
    c = {
        "schema": "debo.r19.capsule.v1",
        "project_id": project_id, "mission_id": mission_id,
        "task_id": stable_task_id(project_id, objective, source_key),
        "objective": objective, "status": status,
        "checkpoint": checkpoint, "evidence": evidence or [],
        "next_action": next_action, "scope": scope,
        "as_of_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    return validate_capsule(c)


def canonical_bytes(data: dict) -> bytes:
    return (json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def atomic_write_readback(path: Path, data: dict) -> dict:
    """Write only a new or byte-identical local capsule, then verify readback.

    This does not authorize overwriting an approved checkpoint. A caller who needs
    a new revision should choose a new versioned filename in the owning private
    project store. This is a local-file utility, not a connector or scheduler.
    """
    validate_capsule(data)
    path = Path(path)
    if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
        raise ValueError("symlink destination refused")
    content = canonical_bytes(data)
    if path.exists():
        previous = path.read_bytes()
        if previous != content:
            raise FileExistsError("checkpoint differs; preserve old and choose a versioned path")
        return {"path": str(path), "sha256": hashlib.sha256(previous).hexdigest(),
                "bytes": len(previous), "readback": "PASS", "unchanged": True}
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=".debo-r19-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(content)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(temp, path)
        verified = path.read_bytes()
        if verified != content:
            raise IOError("checkpoint readback mismatch")
        return {"path": str(path), "sha256": hashlib.sha256(verified).hexdigest(), "bytes": len(verified), "readback": "PASS"}
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def prepare_event(event_type: str, capsule: dict, source_revision: str) -> dict:
    validate_capsule(capsule)
    if event_type not in EVENT_TYPES:
        raise ValueError("unrecognized event type")
    normalize(source_revision)
    if event_type == "TASK_VERIFIED" and not (capsule["status"] in ("TESTED", "APPROVED", "DEPLOYED", "LIVE")):
        raise ValueError("unverified task completion event")
    payload = {"schema": "debo.r19.event.v1", "event_type": event_type,
               "project_id": capsule["project_id"], "task_id": capsule["task_id"],
               "checkpoint": capsule["checkpoint"], "status": capsule["status"],
               "source_revision": source_revision, "evidence": capsule["evidence"],
               "scope": capsule.get("scope", "private")}
    payload["event_id"] = "DEBO-EVENT-" + hashlib.sha256(canonical_bytes(payload)).hexdigest()[:20]
    return payload


def main() -> None:
    ap = argparse.ArgumentParser(description="DEBO R19 offline continuity helper (never contacts network)")
    sub = ap.add_subparsers(dest="command", required=True)
    fp = sub.add_parser("fingerprint")
    fp.add_argument("project_id"); fp.add_argument("objective"); fp.add_argument("--source-key")
    check = sub.add_parser("checkpoint")
    check.add_argument("--input", type=Path, required=True)
    check.add_argument("--output", type=Path, required=True)
    valid = sub.add_parser("validate")
    valid.add_argument("--input", type=Path, required=True)
    event = sub.add_parser("event")
    event.add_argument("--input", type=Path, required=True)
    event.add_argument("--type", required=True)
    event.add_argument("--revision", required=True)
    args = ap.parse_args()
    if args.command == "fingerprint":
        print(stable_task_id(args.project_id, args.objective, args.source_key))
    else:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        if args.command == "validate":
            validate_capsule(data)
            print("PASS: capsule schema/evidence guards")
        elif args.command == "checkpoint":
            print(json.dumps(atomic_write_readback(args.output, data), indent=2))
        else:
            print(json.dumps(prepare_event(args.type, data, args.revision), indent=2))


if __name__ == "__main__":
    main()
