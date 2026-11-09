"""R129 interruption/recovery test harness. Synthetic fixtures ONLY.

Reuse installed R128 planner and R31 router; not a production job queue,
autonomous agent, user data store, or authorized tool-execution endpoint.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import tempfile
from typing import Any

from debo_r128_recovery_pilot import plan,validate

EVIDENCE_KIND={
    "read_source":"source_readback",
    "run_local_tests":"test_receipt",
    "verify_readback":"runtime_probe",
    "compare_fingerprints":"source_readback",
    "retry_read_only":"runtime_probe",
    "write_dev_checkpoint":"source_readback",
}


def run_fixture(document: dict[str,Any], journal: Path, interrupt_after: int | None=None)->dict:
    """Run synthetic routing steps; persist each completed fixture before next."""
    validate(document)
    if not journal.parent.is_dir():
        raise ValueError("journal directory must already exist")
    if journal.exists():
        previous=json.loads(journal.read_text(encoding="utf-8"))
        if previous.get("schema")!="debo.r129.synthetic-journal.v1":
            raise ValueError("unrecognized resume journal")
        if previous["project_id"]!=document["project_id"] or previous["source_revision"]!=document["source_revision"]:
            raise ValueError("stale/cross-project journal")
        if not isinstance(previous.get("receipts"),list):
            raise ValueError("invalid journal receipts")
        if previous.get("fixtures")!="PUBLIC_SYNTHETIC_ONLY":
            raise ValueError("non-synthetic journal forbidden")
        entries=previous["receipts"]
    else:entries=[]
    data={**document,"receipts":[*document["receipts"],*entries]}
    plan_before=plan(data)
    completed=set(plan_before["skipped_verified"])
    auto=plan_before["route"]["auto"]
    executed=[]
    for row in auto:
        action=row["action"]
        if action not in EVIDENCE_KIND:
            continue
        receipt={
            "task_id":row["task_id"],"project_id":document["project_id"],
            "state":"PASS","source_revision":document["source_revision"],
            "evidence_type":EVIDENCE_KIND[action],
            "evidence_ref":"fixture:r129:"+row["task_id"]
        }
        data["receipts"].append(receipt)
        plan(data)  # fail-closed validation before durable write
        entries.append(receipt)
        journal_data={
            "schema":"debo.r129.synthetic-journal.v1",
            "project_id":document["project_id"],
            "source_revision":document["source_revision"],
            "fixtures":"PUBLIC_SYNTHETIC_ONLY",
            "receipts":entries
        }
        fd,name=tempfile.mkstemp(prefix=".r129-",suffix=".tmp",dir=journal.parent)
        try:
            with os.fdopen(fd,"w",encoding="utf-8") as stream:
                json.dump(journal_data,stream,indent=2,sort_keys=True)
                stream.flush();os.fsync(stream.fileno())
            os.replace(name,journal)
        finally:
            if os.path.exists(name):os.unlink(name)
        executed.append(row["task_id"])
        completed.add(row["task_id"])
        if interrupt_after is not None and len(executed)>=interrupt_after:
            break
    return {
        "mode":"SYNTHETIC_ONLY",
        "executed_now":executed,
        "skipped_verified":plan_before["skipped_verified"],
        "remaining":plan(data)["route"],
        "persisted_receipt_count":len(entries),
        "real_tool_calls":0,
    }
