#!/usr/bin/env python3
"""Read-only, deterministic Perplexity Pro mode/model selection for DEBO.

Model names are chosen *only* from a caller-provided observed account menu.
The owner reports Pro without Computer. This router never selects Computer.
"""
import argparse
import json

TASKS = {
    "quick_fact": ("Best", None, "Use default automatic model for simple current facts."),
    "source_comparison": ("Pro Search", "sonar", "Check source dates and contradictions."),
    "technical_research": ("Pro Search", "gpt", "Verify specs and code with official sources."),
    "document_analysis": ("Pro Search", "claude", "Validate interpretations against original documents."),
    "multimodal_comparison": ("Pro Search", "gemini", "Recheck extracted details against originals."),
    "deep_research": ("Research", None, "Research chooses models automatically; independently verify decisive claims."),
    "private_account_inventory": ("Authorized account UI/export", None, "Pro Search does not have private account history access."),
}

def route(task, available_models=None, research_available=True, pro_search_available=True,
          account_read_authorized=False):
    """Return an honest source-only routing suggestion; no access or side effects."""
    if task not in TASKS:
        raise ValueError(f"Unknown task: {task}")
    mode, family, check = TASKS[task]
    models = [str(m) for m in (available_models or []) if str(m).strip()]
    if task == "private_account_inventory":
        return {
            "task": task, "mode": mode, "model": None,
            "account_read_state": ("AUTHORIZED_ROUTE_REQUIRES_READBACK" if account_read_authorized
                                   else "ACCESS_NOT_VERIFIED"),
            "computer": "UNAVAILABLE_PER_OWNER",
            "status": "NOT_AN_ACCOUNT_READ",
            "verification": check,
        }
    if mode == "Research" and not research_available:
        mode = "Pro Search" if pro_search_available else "Best"
        check += " Research unavailable; smaller scoped questions required."
    if mode == "Pro Search" and not pro_search_available:
        mode = "Best"
        check += " Pro Search unavailable; depth may be reduced."
    matches = [name for name in models if family and family in name.casefold()]
    selected = matches[0] if matches and mode == "Pro Search" else "Automatic / verify actual model menu"
    return {
        "task": task, "mode": mode, "model": selected,
        "candidate_model_family": family or "automatic",
        "model_confirmed_from_input_menu": bool(matches and mode == "Pro Search"),
        "computer": "UNAVAILABLE_PER_OWNER",
        "status": "SUGGESTION_ONLY_NOT_EXECUTED",
        "verification": check,
    }

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("task", choices=sorted(TASKS))
    p.add_argument("--available-model", action="append", default=[],
                   help="Use only exact model labels observed in the user's account menu")
    p.add_argument("--no-research", action="store_true")
    p.add_argument("--no-pro-search", action="store_true")
    p.add_argument("--authorized-account-read", action="store_true")
    args = p.parse_args()
    print(json.dumps(route(args.task, args.available_model, not args.no_research,
                           not args.no_pro_search, args.authorized_account_read), indent=2))

if __name__ == "__main__":
    main()
