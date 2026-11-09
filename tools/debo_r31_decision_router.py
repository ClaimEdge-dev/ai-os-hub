"""DEBO R31: deterministic, fail-closed action routing. No external side effects."""
from dataclasses import dataclass
from typing import Literal

Decision = Literal["AUTO", "APPROVAL", "BLOCKED"]
AUTO_ACTIONS = frozenset({
    "read_source", "compare_fingerprints", "run_local_tests",
    "fix_nonproduction_code", "write_dev_checkpoint", "verify_readback",
    "prepare_migration", "prepare_mapping_review", "retry_read_only",
})
APPROVAL_ACTIONS = frozenset({
    "spend", "public_deploy", "production_write", "delete_data",
    "change_access", "contact_customer", "schema_migration",
    "approve_mapping", "release", "modify_owner_hold",
})
@dataclass(frozen=True)
class Task:
    task_id: str
    action: str
    dependencies: tuple[str, ...] = ()
    retries: int = 0

def decide(task: Task, completed: set[str], failed: set[str]) -> tuple[Decision, str]:
    if not task.task_id or task.retries < 0:
        return "BLOCKED", "invalid task"
    if task.action in APPROVAL_ACTIONS:
        return "APPROVAL", "specific owner approval required"
    if task.action not in AUTO_ACTIONS:
        return "BLOCKED", "action not allowlisted"
    if task.task_id in failed:
        return "BLOCKED", "failed; inspect before retry"
    if not set(task.dependencies).issubset(completed):
        return "BLOCKED", "unmet dependencies"
    return "AUTO", "authorized reversible action"

def batch(tasks: list[Task], completed: set[str], failed: set[str]) -> dict:
    ids = [t.task_id for t in tasks]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate task IDs")
    result = {"auto": [], "approval": [], "blocked": []}
    for t in tasks:
        if t.task_id in completed:
            continue
        decision, reason = decide(t, completed, failed)
        result[{"AUTO":"auto","APPROVAL":"approval","BLOCKED":"blocked"}[decision]].append(
            {"task_id": t.task_id, "action": t.action, "reason": reason}
        )
    return result
