#!/usr/bin/env python3
"""Validate and rank DEBO handoff JSON. Local/read-only. Needs jsonschema (pip install jsonschema) for full JSON Schema validation; has conservative built-in checks otherwise."""
import argparse
import datetime as dt
import json
import pathlib
import sys
from urllib.parse import urlparse


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_minimal(obj):
    required = ["schema_version", "mission_id", "project_id", "research_date", "status", "source_checkpoint", "scope", "candidates", "selected_candidate_id", "implementation", "checks", "approval_gates", "return_location", "next_action"]
    for key in required:
        require(key in obj, f"Missing required field: {key}")
    require(obj["schema_version"] == "1.0", "Unsupported schema_version")
    require(obj["project_id"] in {"DEBO","DWE","JCT","RRR","MOR","CE","PLG","BULLDOGS","CWA","BBS","CREDIT","SCHOOL","HOUSING","SETTLESURE"}, "Unknown project_id")
    require(obj["status"] in {"PROPOSED","SOURCE_VERIFIED","BUILD_READY","STAGED","TESTED","DEPLOYED","BLOCKED"}, "Unknown status")
    require(isinstance(obj["candidates"], list) and len(obj["candidates"]) <= 3, "At most three candidates")
    dt.date.fromisoformat(obj["research_date"])
    IDs = set()
    for item in obj["candidates"]:
        for key in ["candidate_id","name","existing_equivalent","source_url","version_or_commit","license","last_checked","risk_review","cost_review","status","scores","rationale"]:
            require(key in item, f"Candidate missing: {key}")
        cid = item["candidate_id"]
        require(cid not in IDs, "Duplicate candidate_id")
        IDs.add(cid)
        u = urlparse(item["source_url"])
        require(u.scheme in {"https", "http"} and bool(u.netloc), "Candidate needs source URL")
        dt.date.fromisoformat(item["last_checked"])
        for metric in ["impact", "reuse", "urgency", "effort", "risk", "cost"]:
            val=item["scores"].get(metric)
            require(type(val) is int and 1 <= val <= 5, f"Invalid score: {metric}")
    require(obj["selected_candidate_id"] is None or obj["selected_candidate_id"] in IDs, "Selected candidate not in candidates")
    if obj["status"] in {"BUILD_READY","STAGED","TESTED","DEPLOYED"}:
        require(obj["source_checkpoint"]["access_status"] == "READ_VERIFIED", "Advanced status requires verified checkpoint")
    if obj["status"] == "DEPLOYED":
        require(any(c.get("name") == "Authenticated production verification" and c.get("status") == "PASS" for c in obj["checks"]), "Deployment cannot be asserted without production verification")


def ranking(item):
    s=item["scores"]
    return 3*s["impact"]+2*s["reuse"]+s["urgency"]-s["effort"]-2*s["risk"]-s["cost"]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=pathlib.Path)
    args=parser.parse_args()
    try:
        obj=json.loads(args.packet.read_text(encoding="utf-8"))
        validate_minimal(obj)
        schema_path=pathlib.Path(__file__).with_name("DEBO_HANDOFF_SCHEMA.json")
        if not schema_path.exists():  # repository installation: tools/ -> prompts/
            schema_path=pathlib.Path(__file__).resolve().parent.parent / "prompts" / "DEBO_HANDOFF_SCHEMA.json"
        schema=json.loads(schema_path.read_text(encoding="utf-8"))
        try:
            import jsonschema  # optional dependency
        except ImportError:
            print("NOTE: jsonschema not installed; conservative built-in checks passed, full schema NOT tested")
        else:
            jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(obj)
            print("PASS: full Draft 2020-12 schema validation")
        for c in sorted(obj["candidates"], key=ranking, reverse=True):
            print(f"{c['candidate_id']}: score {ranking(c)} / status {c['status']}")
        print("Validation PASS (not a security scan, approval, skill installation or deployment receipt)")
    except (OSError, ValueError, KeyError, json.JSONDecodeError, TypeError) as exc:
        print(f"Validation FAIL: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Schema validation FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())