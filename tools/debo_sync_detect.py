#!/usr/bin/env python3
"""DEBO change-detection preview. Offline, standard library only, NO database writes.

Uses existing Neon ledger concepts (public.debo_core_change_events and
debo_evolution.execution_receipts). Verify actual schemas before any writer.
"""
import argparse
import hashlib
import json
import pathlib
import re
import sys
from typing import Any

ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,79}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
KINDS = {"repo_file": "repo_file"}
PUBLIC_PATHS = {"AUTO_SYNC_PROTOCOL.md", "SKILL_REGISTRY.md", "projects/jcs-towing/AGENT_SYSTEM.md"}


class PreviewBlocked(ValueError):
    """Malformed or unsafe sources fail closed."""


def validate_path(root: pathlib.Path, path: str) -> pathlib.Path:
    if not isinstance(path, str) or not path or "\\" in path or "\x00" in path:
        raise PreviewBlocked("Unsafe repository path")
    p = pathlib.PurePosixPath(path)
    if p.is_absolute() or any(s in {".", "..", ""} for s in path.split("/")):
        raise PreviewBlocked("Unsafe repository path")
    if any(not re.fullmatch(r"[a-zA-Z0-9_.-]+", s) for s in path.split("/")):
        raise PreviewBlocked("Unsafe repository path")
    cursor = root.resolve()
    for s in path.split("/"):
        cursor = cursor / s
        if cursor.is_symlink():
            raise PreviewBlocked("Symlinks are not allowed")
    resolved = cursor.resolve()
    if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
        raise PreviewBlocked("Source missing or outside checkout")
    return resolved


def fingerprint_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for piece in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(piece)
    return digest.hexdigest()


def _read_history(state: dict[str, Any], source_id: str) -> tuple[str | None, int]:
    if not isinstance(state, dict) or not isinstance(state.get("sources"), dict):
        raise PreviewBlocked("State requires a sources object")
    old = state["sources"].get(source_id)
    if old is None:
        return None, 0
    if not isinstance(old, dict):
        raise PreviewBlocked("Invalid source history")
    old_fp = old.get("fingerprint")
    old_version = old.get("version")
    if not isinstance(old_fp, str) or not SHA256_RE.fullmatch(old_fp):
        raise PreviewBlocked("Invalid historical fingerprint")
    if type(old_version) is not int or old_version < 1:
        raise PreviewBlocked("Invalid historical version")
    return old_fp, old_version


def preview(root: pathlib.Path, manifest: dict[str, Any], state: dict[str, Any]) -> dict[str, Any]:
    """Build deterministic proposed events. Never mutate state or touch the network."""
    if not isinstance(manifest, dict) or manifest.get("version") != 1:
        raise PreviewBlocked("Manifest version 1 required")
    sources = manifest.get("sources")
    if not isinstance(sources, list):
        raise PreviewBlocked("Manifest sources must be an array")
    if not isinstance(state, dict) or not isinstance(state.get("sources"), dict):
        raise PreviewBlocked("State sources must be an object")
    seen_ids, seen_entities = set(), set()
    records = []
    for source in sources:
        if not isinstance(source, dict) or not ID_RE.fullmatch(str(source.get("id", ""))):
            raise PreviewBlocked("Invalid source id")
        sid = source["id"]
        if sid in seen_ids:
            raise PreviewBlocked("Duplicate source id")
        seen_ids.add(sid)
        if source.get("kind") not in KINDS:
            raise PreviewBlocked("Only public repo_file sources are supported")
        source_path = source.get("path")
        if source_path not in PUBLIC_PATHS:
            raise PreviewBlocked("Source not in approved public document allowlist")
        file_path = validate_path(root, source_path)
        if source_path in seen_entities:
            raise PreviewBlocked("Duplicate source path")
        seen_entities.add(source_path)
        old_fp, old_version = _read_history(state, sid)
        new_fp = fingerprint_file(file_path)
        unchanged = new_fp == old_fp
        action = "SKIPPED_UNCHANGED" if unchanged else "PROPOSE_CHANGE"
        version = old_version if unchanged else old_version + 1
        event = None if unchanged else {
            "entity_type": "repo_file",
            "entity_id": source_path,
            "version": version,
            "payload": {"fingerprint_sha256": new_fp, "hash_algorithm": "sha256"},
        }
        records.append({
            "source_id": sid,
            "source_path": source_path,
            "action": action,
            "prior_version": old_version,
            "proposed_version": version,
            "old_fingerprint": old_fp,
            "new_fingerprint": new_fp,
            "change_event_proposal": event,
            "receipt_preview": {
                "source_ref": f"https://github.com/ClaimEdge-dev/ai-os-hub/blob/main/{source_path}",
                "result": "skipped_unchanged" if unchanged else "change_detected_not_applied",
                "persisted": False,
            },
        })
    return {
        "mode": "DRY_RUN_ONLY",
        "runtime_writes": False,
        "database_connected": False,
        "persistent_receipts_written": False,
        "requires_schema_verification": [
            "public.debo_core_change_events",
            "debo_evolution.execution_receipts",
            "debo_evolution.diagnostics",
            "debo_evolution.connector_health",
        ],
        "total_sources": len(records),
        "proposed_changes": sum(r["action"] == "PROPOSE_CHANGE" for r in records),
        "skipped_unchanged": sum(r["action"] == "SKIPPED_UNCHANGED" for r in records),
        "records": records,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Offline DEBO change detection; dry run only")
    parser.add_argument("--root", default=".")
    parser.add_argument("--manifest", default="sync/debo-change-manifest.json")
    parser.add_argument("--state", help="Optional read-only snapshot of existing ledger versions")
    parser.add_argument("--dry-run", choices=["true"], default="true")
    args = parser.parse_args(argv)
    root = pathlib.Path(args.root).resolve()
    try:
        manifest_file = validate_path(root, args.manifest)
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
        state = {"sources": {}}
        if args.state:
            state = json.loads(validate_path(root, args.state).read_text(encoding="utf-8"))
        print(json.dumps(preview(root, manifest, state), indent=2, sort_keys=True))
        return 0
    except (PreviewBlocked, json.JSONDecodeError, OSError, UnicodeError) as exc:
        print(json.dumps({"status": "BLOCKED", "stage": "read_or_validate", "reason": str(exc), "wrote": False}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
