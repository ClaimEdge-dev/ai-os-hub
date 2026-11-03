#!/usr/bin/env python3
"""Validate a DEBO v0.3 dashboard SNAPSHOT, not a live system.

Only standard-library Python. This enforces the critical source/approval gates.
The adjacent JSON Schema defines the full surface for downstream renderers.
A passed snapshot check does NOT prove its underlying sources or runtime are live.
"""
import argparse
from datetime import datetime
import json
from pathlib import Path
import sys

TRUTH = {"VERIFIED", "SOURCE_ONLY", "SYNTHETIC_TESTED", "BLOCKED", "UNKNOWN", "STALE", "PROPOSED"}
READINESS = {"SOURCE_ONLY", "SYNTHETIC_TESTED", "AUTHENTICATED_TESTED",
             "OWNER_APPROVED", "LIVE_VERIFIED", "BLOCKED", "UNKNOWN"}
KIND = {"SKILL", "PLUGIN", "BUILTIN"}
CAP_STATE = {"DISCOVERED", "INSTALLED", "CONNECTED", "AUTHORIZED", "WORKFLOW_TESTED", "UNKNOWN", "BLOCKED"}


def has_timezone(value):
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.tzinfo is not None and dt.utcoffset() is not None
    except ValueError:
        return False


def validate(data):
    errors = []
    if not isinstance(data, dict):
        return ["Root must be an object"]
    if data.get("schema_version") != "0.3":
        errors.append("schema_version must be 0.3")
    if not has_timezone(data.get("generated_at")):
        errors.append("generated_at must have an explicit timezone")
    kind = data.get("snapshot_kind")
    if kind not in {"OFFLINE_SNAPSHOT", "VERIFIED_REFRESH"}:
        errors.append("snapshot_kind must be OFFLINE_SNAPSHOT or VERIFIED_REFRESH")
    if not isinstance(data.get("mission_id"), str) or not data["mission_id"].strip():
        errors.append("mission_id required")

    sources = data.get("sources")
    if not isinstance(sources, list):
        errors.append("sources must be a list")
        sources = []
    ids = set()
    source_states = {}
    for i, source in enumerate(sources):
        if not isinstance(source, dict):
            errors.append(f"sources[{i}] must be an object")
            continue
        sid = source.get("id")
        if not isinstance(sid, str) or not sid.strip() or sid in ids:
            errors.append(f"sources[{i}] invalid or duplicate id")
        else:
            ids.add(sid)
            source_states[sid] = source.get("truth_state")
        if source.get("truth_state") not in TRUTH:
            errors.append(f"sources[{i}] invalid truth_state")
        if not has_timezone(source.get("checked_at")):
            errors.append(f"sources[{i}] checked_at requires timezone")
        if not isinstance(source.get("uri"), str) or not source["uri"].strip():
            errors.append(f"sources[{i}] uri required")

    if kind == "VERIFIED_REFRESH":
        if not data.get("refresh_receipt"):
            errors.append("VERIFIED_REFRESH needs an independent refresh_receipt")
        if not any(s.get("truth_state") == "VERIFIED" for s in sources if isinstance(s, dict)):
            errors.append("VERIFIED_REFRESH needs at least one verified source")

    def refs(record, location, must_verify=False):
        source_ids = record.get("source_ids")
        if not isinstance(source_ids, list):
            errors.append(f"{location}.source_ids must be a list")
            return
        if len(source_ids) != len(set(x for x in source_ids if isinstance(x, str))):
            errors.append(f"{location}.source_ids duplicate")
        for sid in source_ids:
            if not isinstance(sid, str) or sid not in ids:
                errors.append(f"{location}: dangling source reference {sid!r}")
        if must_verify and not any(source_states.get(sid) == "VERIFIED" for sid in source_ids):
            errors.append(f"{location}: verified claim requires verified source evidence")

    cards = data.get("cards")
    if not isinstance(cards, dict) or set(cards) != {"now", "money", "blocked", "done"}:
        errors.append("cards must have exactly now/money/blocked/done")
    else:
        for name, card in cards.items():
            if not isinstance(card, dict):
                errors.append(f"cards.{name} must be object")
                continue
            state = card.get("truth_state")
            if state not in TRUTH:
                errors.append(f"cards.{name} invalid truth_state")
            for key in ("label", "detail", "next_action"):
                if not isinstance(card.get(key), str):
                    errors.append(f"cards.{name}.{key} must be a string")
            refs(card, f"cards.{name}", must_verify=(state == "VERIFIED"))
            if name in {"money", "done"} and state == "VERIFIED" and not card.get("source_ids"):
                errors.append(f"cards.{name} cannot be VERIFIED without proof")

    for list_name in ("projects", "capabilities", "automations", "ideas", "thread_index"):
        items = data.get(list_name)
        if not isinstance(items, list):
            errors.append(f"{list_name} must be a list")
            continue
        key = {"projects": "project_id", "capabilities": "name", "automations": "title",
               "ideas": "idea_id", "thread_index": "thread_id"}[list_name]
        seen = set()
        for i, entry in enumerate(items):
            loc = f"{list_name}[{i}]"
            if not isinstance(entry, dict):
                errors.append(f"{loc} must be object")
                continue
            value = entry.get(key)
            if not isinstance(value, str) or not value.strip() or value in seen:
                errors.append(f"{loc} invalid or duplicate {key}")
            else:
                seen.add(value)
            if list_name != "thread_index":
                refs(entry, loc, must_verify=False)
            if list_name == "projects":
                rd = entry.get("readiness")
                if rd not in READINESS:
                    errors.append(f"{loc} invalid readiness")
                if entry.get("owner_gate") not in {"REQUIRED", "NOT_REQUIRED", "UNVERIFIED"}:
                    errors.append(f"{loc} invalid owner_gate")
                if rd in {"AUTHENTICATED_TESTED", "OWNER_APPROVED", "LIVE_VERIFIED"}:
                    refs(entry, loc, must_verify=True)
                if rd in {"AUTHENTICATED_TESTED", "LIVE_VERIFIED"} and entry.get("authenticated_test") != "VERIFIED":
                    errors.append(f"{loc}: authenticated readiness needs real authenticated test")
                if rd in {"OWNER_APPROVED", "LIVE_VERIFIED"} and entry.get("owner_gate") == "REQUIRED" and entry.get("owner_approval") != "VERIFIED":
                    errors.append(f"{loc}: owner-gated readiness needs real owner approval")
                if rd == "LIVE_VERIFIED" and entry.get("owner_gate") == "UNVERIFIED":
                    errors.append(f"{loc}: can't claim live with unknown owner gate")
            if list_name == "capabilities":
                if entry.get("kind") not in KIND or entry.get("state") not in CAP_STATE:
                    errors.append(f"{loc}: invalid kind or capability state")
                if entry.get("state") == "WORKFLOW_TESTED":
                    refs(entry, loc, must_verify=True)
            if list_name == "automations":
                if type(entry.get("enabled")) is not bool:
                    errors.append(f"{loc}: enabled must be true/false")
                if entry.get("truth_state") not in TRUTH:
                    errors.append(f"{loc}: invalid truth_state")
                last = entry.get("last_run_at")
                if last is not None and not has_timezone(last):
                    errors.append(f"{loc}: last_run_at needs timezone")
            if list_name == "ideas":
                if entry.get("disposition") not in {"USE_NOW", "RESEARCH_LATER", "WAIT", "NOT_RELEVANT"}:
                    errors.append(f"{loc}: invalid disposition")
                if not isinstance(entry.get("trigger"), str):
                    errors.append(f"{loc}: trigger must be text")
            if list_name == "thread_index" and entry.get("status") not in {"ACTIVE", "BUILD", "CHECKPOINT", "HOLD", "UNKNOWN"}:
                errors.append(f"{loc}: invalid status")
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("snapshot", type=Path)
    args = ap.parse_args()
    try:
        data = json.loads(args.snapshot.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "BLOCKED", "errors": [str(exc)]}))
        return 2
    errors = validate(data)
    print(json.dumps({"status": "PASS" if not errors else "BLOCKED",
                      "snapshot": str(args.snapshot), "errors": errors}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
