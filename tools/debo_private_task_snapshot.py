"""Private, read-only DEBO task snapshot adapter. Never writes or publishes data.

Caller must supply already-authorized task rows from an isolated/private source.
Output is PRIVATE_SNAPSHOT, not a public governance feed or live sync claim.
"""
from collections import Counter
from datetime import datetime, timezone

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
