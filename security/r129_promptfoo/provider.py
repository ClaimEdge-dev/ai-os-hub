"""Promptfoo local Python provider for offline DEBO R31 security contract evaluation.

THIS IS A RULE-ROUTER TEST, NOT AN LLM OR INDEPENDENT AGENT.
Never import source documents or network tools into this provider.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"tools"))
from debo_r31_decision_router import Task,decide  # noqa: E402


def evaluate(prompt: object) -> dict:
    if not isinstance(prompt,str) or len(prompt)>2048:
        return {"decision":"BLOCKED","reason":"invalid_or_oversize_input"}
    try:
        card=json.loads(prompt)
    except (TypeError,ValueError):
        return {"decision":"BLOCKED","reason":"untrusted_freeform_input"}
    if not isinstance(card,dict) or card.get("project_id")!="DEBO":
        return {"decision":"BLOCKED","reason":"project_scope_rejected"}
    allowed_keys={"project_id","task_id","action","untrusted_text"}
    if set(card)-allowed_keys:
        return {"decision":"BLOCKED","reason":"unsupported_input_fields"}
    if not isinstance(card.get("task_id"),str) or len(card["task_id"])>96:
        return {"decision":"BLOCKED","reason":"invalid_id"}
    if not isinstance(card.get("action"),str) or len(card["action"])>100:
        return {"decision":"BLOCKED","reason":"invalid_action"}
    if not isinstance(card.get("untrusted_text",""),str) or len(card.get("untrusted_text",""))>1024:
        return {"decision":"BLOCKED","reason":"invalid_untrusted_text"}
    # Untrusted text is explicitly never interpreted as new authority or action.
    decision,reason=decide(Task(task_id=card["task_id"],action=card["action"]),set(),set())
    return {"decision":decision,"reason":reason}


def call_api(prompt: str, options: dict|None=None, context: dict|None=None) -> dict:
    outcome=evaluate(prompt)
    return {"output":json.dumps(outcome,sort_keys=True),
            "tokenUsage":{"total":0,"prompt":0,"completion":0,"numRequests":0},
            "cost":0}
