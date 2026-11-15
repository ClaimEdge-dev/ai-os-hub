#!/usr/bin/env python3
"""DEBO R153 optional Codex hooks. Read-only, stdlib-only, no external calls.

Reuses the canonical tools/debo_bootstrap_check.py. This is not an
authentication service, a secret scanner, or a substitute for Codex sandbox,
GitHub branch protection, approval policy, or a verified private checkpoint.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

from debo_bootstrap_check import PROJECT_PROFILES, ROOT, render_brief, section

CONTEXT_LIMIT = 4800
# Intentionally narrow, conservative protection of direct high-impact commands.
# This is not a complete Bash parser and can have false positives/negatives.
SHELL_HOLD = re.compile(
    r"(?i)(?:^|[;&|]\s*)(?:sudo\s+)?(?:"
    r"rm\s+-(?:[A-Za-z]*r[A-Za-z]*f|[A-Za-z]*f[A-Za-z]*r)\b"
    r"|gh\s+pr\s+merge\b"
    r"|gh\s+repo\s+delete\b"
    r"|gh\s+release\s+create\b"
    r"|git\s+push\b[^\n]{0,220}(?:--force(?:-with-lease)?\b|-f\b|\bmain\b)"
    r"|vercel\s+(?:deploy\s+)?--prod\b"
    r"|npm\s+publish\b"
    r"|terraform\s+(?:apply|destroy)\b"
    r"|kubectl\s+delete\b"
    r")"
)
MCP_HOLD = re.compile(
    r"(?i)^mcp__[^\s]+__(?:"
    r"delete(?:_|$)|merge(?:_|$)|send(?:_|$)|publish(?:_|$)|"
    r"deploy(?:_|$)|share(?:_|$)|remove_collaborator|"
    r"update_access|change_permissions|enable_auto_merge"
    r")"
)


def _output(event_name: str, **fields: object) -> dict:
    return {"hookSpecificOutput": {"hookEventName": event_name, **fields}}


def _deny(reason: str) -> dict:
    return _output(
        "PreToolUse",
        permissionDecision="deny",
        permissionDecisionReason=reason,
    )


def session_start(event: dict) -> dict:
    """Load a source-derived view; never claim a fresh private checkpoint."""
    if event.get("hook_event_name") != "SessionStart":
        return {"systemMessage": "DEBO hook event mismatch; no recovery asserted."}

    project = os.environ.get("DEBO_PROJECT_ID", "DEBO").strip().upper()
    if project not in PROJECT_PROFILES:
        return {
            "systemMessage": "DEBO recovery: unsupported project ID; no project instructions loaded."
        }
    try:
        rendered = render_brief(project)
        rules = section(rendered, "## Golden rules")
        saved_path = ROOT / "governance" / "runtime-briefs" / (project + ".md")
        saved_fresh = (saved_path.is_file()
                       and not saved_path.is_symlink()
                       and saved_path.read_text(encoding="utf-8") == rendered)
    except (OSError, ValueError, KeyError) as exc:
        # No internal paths, private details, or exception values are emitted.
        return {"systemMessage": "DEBO recovery source unavailable or invalid; verify canonical bootstrap manually."}

    freshness = "MATCHES_GENERATED_SOURCE" if saved_fresh else "STALE_OR_MISSING"
    context = (
        "DEBO source recovery: project=" + project + "; saved brief=" + freshness + ".\n"
        "These are public repository instructions, NOT current private project state.\n"
        "Before changes, recover the latest authorized private checkpoint through a "
        "connected source. If inaccessible, mark current state UNKNOWN.\n"
        "Preserve owner approvals, existing builds, and the selected project adapter.\n"
        "The original DEBO_BOOTSTRAP.md and detailed governing policies remain authoritative.\n"
        + rules[:CONTEXT_LIMIT - 650]
    )
    return _output("SessionStart", additionalContext=context[:CONTEXT_LIMIT])


def pre_tool_use(event: dict) -> dict:
    """Deny a small set of unmistakably high-impact actions, never grant access."""
    if event.get("hook_event_name") != "PreToolUse":
        return _deny("Unrecognized hook event; no authorization is established.")
    tool = event.get("tool_name")
    args = event.get("tool_input")
    if not isinstance(tool, str) or not tool or not isinstance(args, dict):
        return _deny("Tool identity or arguments missing; verify before retrying.")
    if tool == "Bash":
        command = args.get("command")
        if not isinstance(command, str):
            return _deny("Shell command could not be inspected.")
        if SHELL_HOLD.search(command):
            return _deny(
                "High-impact shell operation held for owner-governed review. "
                "A local hook cannot grant approval or override sandbox policy."
            )
    elif MCP_HOLD.search(tool):
        return _deny(
            "High-impact connected-app action held for owner-governed review. "
            "Use the authorized application approval path."
        )
    # No positive 'allow' decision: normal Codex sandbox/approvals still apply.
    return {}


def post_tool_use(event: dict) -> dict:
    """Minimal non-leaking QA nudge for tool failures; no retry loops."""
    if event.get("hook_event_name") != "PostToolUse":
        return {}
    response = event.get("tool_response")
    if not isinstance(response, dict):
        return {}
    exit_code = response.get("exit_code", response.get("exitCode"))
    failure = (isinstance(exit_code, int) and not isinstance(exit_code, bool)
               and exit_code != 0) or response.get("status") in ("failed", "error")
    if not failure:
        return {}
    return _output(
        "PostToolUse",
        additionalContext=(
            "A tool reported failure. Inspect the actual error, take at most one "
            "distinct authorized recovery path, rerun the smallest applicable "
            "test, and state what was actually verified. Do not invent success."
        ),
    )


HANDLERS = {
    "session-start": session_start,
    "pre-tool-use": pre_tool_use,
    "post-tool-use": post_tool_use,
}


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1 or argv[0] not in HANDLERS:
        print("Expected one known DEBO Codex hook action.", file=sys.stderr)
        return 2
    action = argv[0]
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            raise ValueError("object required")
    except (ValueError, TypeError):
        result = (_deny("Invalid hook input; cannot verify tool permissions.")
                  if action == "pre-tool-use" else
                  {"systemMessage": "DEBO hook input invalid; no recovery or QA claimed."})
    else:
        result = HANDLERS[action](payload)
    print(json.dumps(result, separators=(",", ":"), ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
