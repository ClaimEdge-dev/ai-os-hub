"""R32 safe bridge from R31 policy to the existing R20 local runner.

No external integrations, emails, public releases, shell, or production writes.
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "neon" / "recovery" / "r20_turbo"))
from engine import run, validate
from debo_r31_decision_router import Task, decide

LOCAL_ACTIONS = frozenset({"noop", "verify_text"})

def preflight(tasks):
    validate(tasks)
    approved, held, blocked = [], [], []
    ids = {t["id"] for t in tasks}
    for t in tasks:
        tid = t["id"]
        if t.get("owner_hold") or t.get("approval_required"):
            held.append(tid)
            continue
        if t.get("action", "noop") not in LOCAL_ACTIONS:
            blocked.append(tid)
            continue
        # The engine's allowlist is narrower than the policy router.
        # Do not reclassify approvals or perform external effects.
        approved.append(t)
    return {"approved": approved, "held": held, "blocked": blocked}

def execute(tasks, receipt_path, workers=3, attempts=2):
    gate = preflight(tasks)
    if gate["blocked"]:
        raise ValueError("unapproved actions: " + ",".join(gate["blocked"]))
    result = run(tasks, receipt_path, workers=workers, attempts=attempts)
    result["policy_held"] = gate["held"]
    return result
