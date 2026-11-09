#!/usr/bin/env python3
"""Read-only integrity checks for DEBO's execution-first source policy.

This is NOT an agent runner, scheduler, permission grant or cross-chat loader.
Python 3 standard library only; no network and no writes.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CONFIG = "governance/DEBO_ELITE_EXECUTION_DEFAULT_v1.json"
REQUIRED_APPROVALS = {
    "spend", "public_deploy", "production_write", "schema_migration",
    "delete_data", "change_access", "contact_customer",
    "modify_owner_hold", "approve_mapping", "share_restricted_data"
}
REQUIRED_NO_AUTO = {
    "public_deployment", "plugin_install", "permission_change",
    "production_write", "billing_change", "autonomous_agent_launch"
}
REQUIRED_STATES = {
    "EXECUTE_NOW", "VERIFY", "REPAIR", "WAITING",
    "OWNER_APPROVAL", "PARKED", "COMPLETE"
}
SEQUENCE = [
    "RECOVER", "DEFINE", "ROUTE", "EXECUTE", "VERIFY", "FILE", "CHECKPOINT"
]
REQUIRED_DEPLOYMENT_STATES = [
    "PROPOSED", "BUILT", "TESTED", "INSTALLED", "APPROVED", "LIVE"
]


def safe_file(root: Path, name: object) -> bool:
    """Reject absolute paths, traversal and missing/symlinked source files."""
    if not isinstance(name, str) or not name or "\\" in name:
        return False
    relative = Path(name)
    if relative.is_absolute() or ".." in relative.parts:
        return False
    target = root / relative
    try:
        return target.is_file() and not target.is_symlink() and target.resolve().is_relative_to(root.resolve())
    except (OSError, RuntimeError, ValueError):
        return False


def validate(data: object, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["Policy contract must be a JSON object"]

    if data.get("schema_version") != "debo.execution-default.v1":
        errors.append("Wrong schema_version")
    if data.get("mode") != "documented_governance_only":
        errors.append("Mode must remain source-only governance")
    if data.get("active_runtime_verified") is not False:
        errors.append("Runtime activation may not be asserted")
    if data.get("effective_on_source_merge") is not False:
        errors.append("Git merge cannot imply external activation")

    for label in ("source_prompt", "recovery_entrypoint", "runtime_bootstrap", "canonical_agent_board"):
        if not safe_file(root, data.get(label)):
            errors.append("Missing or unsafe referenced file: " + label)

    for label, required in (
        ("approval_required_actions", REQUIRED_APPROVALS),
        ("no_automatic_actions", REQUIRED_NO_AUTO),
        ("task_states", REQUIRED_STATES),
    ):
        values = data.get(label)
        if not isinstance(values, list) or not all(isinstance(x, str) for x in values):
            errors.append("Invalid list " + label)
        elif len(values) != len(set(values)) or not required.issubset(values):
            errors.append("Missing or duplicated required controls in " + label)

    governor = data.get("account_workflow_governor")
    if not isinstance(governor, dict):
        errors.append("Missing account/workflow governor")
    else:
        required = {
            "enabled": True,
            "mode": "evaluate_then_act_only_with_authorized_scope",
            "prefer_existing_settings_and_workflows": True,
            "require_current_state_read": True,
            "require_defined_benefit": True,
            "require_independent_readback": True,
            "unspecified_personalization": "NO_CHANGE_RECOMMENDED",
            "security_and_oauth_expansion": "OWNER_APPROVAL",
            "spending_and_paid_features": "OWNER_APPROVAL",
            "production_and_public_changes": "OWNER_APPROVAL",
            "scheduler_activation_and_material_schedule_changes": "OWNER_APPROVAL",
            "unsupported_setting": "REPORT_NOT_INSTALLED",
            "success_claim_requires": "TARGET_SYSTEM_READBACK",
        }
        for key, expected in required.items():
            if governor.get(key) != expected:
                errors.append("Account governor missing/unsafe control: " + key)
        if governor.get("allow_unambiguous_low_risk_reversible_change") is not True:
            errors.append("Account governor lacks narrow reversible-change permission")

    if data.get("work_sequence") != SEQUENCE:
        errors.append("Workflow sequence changed")
    if data.get("implementation_states") != REQUIRED_DEPLOYMENT_STATES:
        errors.append("Implementation states changed")

    try:
        board = json.loads((root / "governance/DEBO_AGENT_COVERAGE_REGISTER_v1.json").read_text(encoding="utf-8"))
        roles = [r["alias"] for r in board["roles"] if r.get("project_id") == "DEBO"]
        if data.get("agent_board") != roles or len(roles) != 13:
            errors.append("Must reuse exact canonical 13-role board order")
    except (OSError, KeyError, ValueError, TypeError) as exc:
        errors.append("Canonical role board unavailable: " + type(exc).__name__)

    try:
        bootstrap = (root / "DEBO_BOOTSTRAP.md").read_text(encoding="utf-8")
        prompt = (root / "prompts/DEBO_ELITE_EXECUTION_PROMPT_v2.md").read_text(encoding="utf-8")
        if "Elite execution-first default" not in bootstrap or "prompts/DEBO_ELITE_EXECUTION_PROMPT_v2.md" not in bootstrap:
            errors.append("Canonical bootstrap missing elite execution pointer")
        if "## 8. Realistic 30-day mission" not in prompt or "## 9. New universal rules" not in prompt:
            errors.append("Execution prompt missing plan or policy rules")
        if prompt.count("~~~mermaid") < 2:
            errors.append("Execution prompt missing architecture diagrams")
        if "No overnight/background execution claims" not in prompt:
            errors.append("Execution prompt missing background-truth boundary")
    except OSError as exc:
        errors.append("Prompt/bootstrap unavailable: " + type(exc).__name__)

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", default=CONFIG)
    args = parser.parse_args(argv)
    try:
        path = Path(args.contract)
        data = json.loads(path.read_text(encoding="utf-8"))
        errors = validate(data)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors = ["Contract unavailable or invalid JSON: " + type(exc).__name__]
    receipt = {
        "schema": "DEBO-ELITE-POLICY-CHECK-v1",
        "status": "PASS" if not errors else "BLOCKED",
        "errors": errors,
        "note": "Local public source integrity only. No user/account/agent activation is proven."
    }
    print(json.dumps(receipt, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
