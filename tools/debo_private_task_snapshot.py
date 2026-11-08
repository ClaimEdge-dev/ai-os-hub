"""Private, read-only DEBO task snapshot adapter. Never writes or publishes data.

Caller must supply already-authorized task rows from an isolated/private source.
Output is PRIVATE_SNAPSHOT, not a public governance feed or live sync claim.
"""
from collections import Counter
from datetime import datetime, timezone
import json
import sys

ALLOWED = {"Backlog", "In Progress", "Blocked", "Review", "Done"}
FIELDS = ("task_id", "title", "status", "priority", "assignee_role", "pillar")

def build_private_snapshot(rows, *, authenticated, source_branch, verified_at=None):
    if authenticated is not True:
        raise PermissionError("authenticated private source required")
    if not source_branch or source_branch == "main":
        raise ValueError("explicit nonproduction branch required")
    if not isinstance(rows, list):
        raise TypeError("rows must be a list")
    seen = set()
    output = []
    for row in rows:
        if not isinstance(row, dict) or any(not isinstance(row.get(k), str) or not row[k].strip() for k in FIELDS):
            raise ValueError("missing required task fields")
        if row["status"] not in ALLOWED:
            raise ValueError("invalid normalized status")
        if row["task_id"] in seen:
            raise ValueError("duplicate task ID")
        if row["task_id"] == "WORK-RENTALS-001":
            raise ValueError("held Rentals task must not appear")
        seen.add(row["task_id"])
        output.append({k: row[k] for k in FIELDS})
    return {
        "schema_version": "debo.private.tasks.v1",
        "classification": "PRIVATE_AUTHENTICATED",
        "mode": "READ_ONLY_NONPRODUCTION",
        "live_sync": False,
        "source_branch": source_branch,
        "checked_at": verified_at or datetime.now(timezone.utc).isoformat(),
        "task_count": len(output),
        "status_counts": dict(Counter(r["status"] for r in output)),
        "tasks": output,
    }

def safe_summary(snapshot):
    """Display-safe counts; never include task titles, people or project details."""
    if snapshot.get("classification") != "PRIVATE_AUTHENTICATED":
        raise ValueError("not a private snapshot")
    return {
        "schema_version": snapshot["schema_version"],
        "mode": snapshot["mode"],
        "live_sync": False,
        "task_count": snapshot["task_count"],
        "status_counts": snapshot["status_counts"],
        "checked_at": snapshot["checked_at"],
    }

def main(argv=None):
    """Offline file adapter. No network, no credential storage, no automatic publishing."""
    import argparse
    p=argparse.ArgumentParser(description="Private offline task snapshot validation")
    p.add_argument("source_json",help="locally authorized JSON array of task rows")
    p.add_argument("--authenticated",action="store_true",help="assert source was retrieved with authorized access")
    p.add_argument("--branch",required=True,help="nonproduction source branch name")
    p.add_argument("--summary-only",action="store_true",help="omit private task fields from stdout")
    args=p.parse_args(argv)
    with open(args.source_json,encoding="utf-8") as stream:
        rows=json.load(stream)
    snapshot=build_private_snapshot(rows,authenticated=args.authenticated,source_branch=args.branch)
    print(json.dumps(safe_summary(snapshot) if args.summary_only else snapshot,sort_keys=True))
    return 0

if __name__ == "__main__":
    sys.exit(main())
