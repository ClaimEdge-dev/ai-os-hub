#!/usr/bin/env python3
"""Deterministic public, read-only DEBO Core feed from canonical runtime sources.

No customer data, private records, approvals, deployments or extra task database.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys

DEFAULT_REPO = Path(__file__).resolve().parents[1]
FEED_PATH = Path("governance/dashboard/DEBO_CORE_FEED_v1.json")
PUBLIC_INPUTS = (
    "DEBO_BOOTSTRAP.md",
    "governance/DEBO_RUNTIME_BOOTSTRAP_v2.md",
    "governance/runtime-briefs/DEBO.md",
)
# Existing checker owns the canonical project-to-profile map.
from debo_bootstrap_check import PROJECT_PROFILES as PROFILE_PATHS


class FeedError(ValueError):
    pass


def file_hash(path: Path) -> str:
    if not path.is_file():
        raise FeedError(f"Missing canonical public source: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_feed(repo: Path) -> dict:
    """Publish allowlisted public metadata only, not raw source or private state."""
    sources = [{"path": str(path), "sha256": file_hash(repo / path)} for path in PUBLIC_INPUTS]
    brief = (repo / PUBLIC_INPUTS[2]).read_text(encoding="utf-8")
    if "## Selected project: DEBO" not in brief or "## Golden rules" not in brief:
        raise FeedError("Current DEBO runtime brief missing expected source sections")
    if "## Source fingerprints (local SHA-256)" not in brief:
        raise FeedError("Expected governed source fingerprints are missing")
    rules = brief.split("## Golden rules", 1)[1].split("\n## ", 1)[0]
    count = sum(line.lstrip().startswith(f"{i}. ") for i in range(1, 11)
                for line in rules.splitlines())
    if count != 10:
        raise FeedError("Expected exactly ten published DEBO golden rules")
    projects = [{
        "project_id": project_id,
        "profile_path": profile,
        "profile_sha256": file_hash(repo / profile) if profile else None,
        "last_live_verification": None,
        "live_operational_status": "UNKNOWN",
        "approval_state": "UNKNOWN",
    } for project_id, profile in PROFILE_PATHS.items()]
    return {
        "schema_version": "debo.core.public_feed.v1",
        "feed_id": "DEBO_CORE_PUBLIC_READ_ONLY",
        "source_repository": "ClaimEdge-dev/ai-os-hub",
        "data_classification": "PUBLIC_GOVERNANCE_METADATA_ONLY",
        "derived_from": "DEBO_RUNTIME_BRIEFS_EXISTING_WORKFLOW",
        "source_files": sources,
        "golden_rules_count": count,
        "projects": projects,
        "permissions": {
            "read_only": True, "writes_enabled": False,
            "customer_data_included": False, "financial_records_included": False,
            "youth_data_included": False, "automatic_approvals": False,
            "automatic_deployment": False,
        },
        "status_definitions": {
            "source_policy_state": "DOCUMENTED_SOURCE",
            "project_runtime_state": "UNKNOWN_UNTIL_PROJECT_CHECKPOINT_VERIFIED",
            "source_feed_is_live_business_data": False,
            "automatic_cross_project_sync": False,
        },
        "refresh_contract": {
            "producer": ".github/workflows/debo-runtime-briefs.yml",
            "mode": "ON_CANONICAL_SOURCE_CHANGE",
            "consumer": "DEBO_DASH_005_LOCAL_READ_ONLY",
            "last_successful_live_client_refresh": None,
            "note": "Source hashes do not prove runtime operation, owner approval or deployment.",
        },
    }


def serialized(feed: dict) -> str:
    return json.dumps(feed, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def update(repo: Path, check_only: bool) -> bool:
    destination = repo / FEED_PATH
    expected = serialized(build_feed(repo))
    if check_only:
        if not destination.is_file() or destination.read_text(encoding="utf-8") != expected:
            raise FeedError("Derived dashboard Core feed is absent or stale; regenerate using --write")
        return False
    if destination.is_file() and destination.read_text(encoding="utf-8") == expected:
        return False
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(expected, encoding="utf-8")
    return True


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--write", action="store_true")
    modes.add_argument("--check", action="store_true")
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    args = parser.parse_args(argv)
    try:
        changed = update(args.repo, args.check)
    except FeedError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print("DEBO dashboard feed: " + ("regenerated" if changed else "unchanged"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
