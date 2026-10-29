"""DEBO private Business Build Factory contract pilot.

Uses synthetic fixtures only. No network, database, CRM, file writes or production changes.
Run: python -m unittest discover -s tests -p 'test_debo_factory_pilot.py'
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import json
import sys

TRUTH = {"VERIFIED", "LIKELY", "UNRESOLVED", "CONFLICT", "PROPOSED"}

@dataclass
class PilotReceipt:
    project: str
    scenario: str
    result: str
    maturity: str
    performed_actions: list[str]
    blocking_gaps: list[str]
    proposed_outputs: dict[str, Any]
    proof_scope: str = "SYNTHETIC CONTRACT TEST ONLY; NO LIVE CRM/WEBSITE/FINANCIAL WRITE"

    def to_dict(self) -> dict[str, Any]:
        return vars(self)

def _require_keys(obj: dict[str, Any], fields: tuple[str, ...]) -> None:
    missing = [k for k in fields if k not in obj]
    if missing:
        raise ValueError("Missing required contract fields: " + ", ".join(missing))

def validate_adapter(adapter: dict[str, Any]) -> None:
    _require_keys(adapter, ("project_id", "industry", "source_refs", "modules", "approval_gates"))
    if adapter["project_id"] not in {"JCT", "MORGANS"}:
        raise ValueError("Unknown pilot project")
    if not isinstance(adapter["modules"], dict):
        raise ValueError("modules must be object")
    if any(v not in {"REQUIRED", "CONDITIONAL", "NOT_APPLICABLE"} for v in adapter["modules"].values()):
        raise ValueError("Bad module classification")
    if not adapter["source_refs"]:
        raise ValueError("Canonical provenance required")
    if not adapter["approval_gates"].get("external_send_publish_spend", False):
        raise ValueError("Approval firewall must be enabled")

def run_jct(adapter: dict[str, Any], case: dict[str, Any]) -> PilotReceipt:
    validate_adapter(adapter)
    if adapter["project_id"] != "JCT":
        raise ValueError("Wrong adapter")
    _require_keys(case, ("scenario_id", "synthetic", "source", "pickup", "destination",
                         "vehicle_class", "authorized", "evidence_present", "rate_approved"))
    if case["synthetic"] is not True:
        raise ValueError("Private pilot accepts synthetic data only")
    gaps = []
    for k in ("pickup", "destination", "vehicle_class", "source"):
        if not case.get(k):
            gaps.append("MISSING_" + k.upper())
    if case["authorized"] is not True:
        gaps.append("AUTHORIZATION_NOT_VERIFIED")
    if case["evidence_present"] is not True:
        gaps.append("EVIDENCE_MISSING")
    if case["rate_approved"] is not True:
        gaps.append("RATE_AUTHORITY_MISSING")
    out = {
        "lead_id": case["scenario_id"],
        "job_id": "SYN-JCT-JOB-001",
        "dispatch_status": "DRAFT",
        "evidence_status": "NEEDS EVIDENCE" if not case["evidence_present"] else "PASS",
        "invoice_status": "QA HOLD" if gaps else "READY FOR OWNER REVIEW",
        "rate": None,
        "amount_billed": None,
        "actual_work_performed": False,
        "publish_or_send": False,
        "crm_write": False
    }
    return PilotReceipt("JCT",case["scenario_id"],"HOLD" if gaps else "CONTRACT_PASS",
                         "PRIVATE SYNTHETIC",["validated intake contract","mapped dispatch fields",
                         "checked evidence and rate approval gates","constructed draft-only receipt"],gaps,out)

def run_morgans(adapter: dict[str, Any], case: dict[str, Any]) -> PilotReceipt:
    validate_adapter(adapter)
    if adapter["project_id"] != "MORGANS":
        raise ValueError("Wrong adapter")
    _require_keys(case, ("scenario_id", "synthetic", "inquiry_type", "owner_approved_assets",
                         "public_business_truth_verified", "owner_approved_copy"))
    if case["synthetic"] is not True:
        raise ValueError("Private pilot accepts synthetic data only")
    gaps=[]
    if not case.get("inquiry_type"):
        gaps.append("INQUIRY_TYPE_MISSING")
    if not case["owner_approved_assets"]:
        gaps.append("APPROVED_BRAND_ASSET_MISSING")
    if case["public_business_truth_verified"] is not True:
        gaps.append("NAP_MENU_HOURS_TRUTH_UNRESOLVED")
    if case["owner_approved_copy"] is not True:
        gaps.append("OWNER_COPY_APPROVAL_MISSING")
    out={
       "lead_id":case["scenario_id"],"crm_status":"PRIVATE DRAFT",
       "asset_template":"PLACEHOLDER - DO NOT PUBLISH",
       "approved_brand_assets_used":False,
       "publish_or_send":False,"crm_write":False,
       "public_claims_included":False
    }
    return PilotReceipt("MORGANS",case["scenario_id"],"HOLD" if gaps else "CONTRACT_PASS",
                        "PRIVATE SYNTHETIC",["validated hospitality inquiry",
                        "mapped CRM candidate","checked brand and public truth gates",
                        "constructed preview-only template contract"],gaps,out)

def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python tools/debo_factory_pilot.py ADAPTER.json CASE.json",file=sys.stderr)
        return 2
    with open(sys.argv[1],encoding="utf-8") as f: adapter=json.load(f)
    with open(sys.argv[2],encoding="utf-8") as f: case=json.load(f)
    receipt=(run_jct(adapter,case) if adapter.get("project_id")=="JCT"
             else run_morgans(adapter,case))
    print(json.dumps(receipt.to_dict(),indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
