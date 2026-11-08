"""Fail-closed readiness gate, no network or database writes."""
def assess(e):
    keys=["source_ids","approved_mappings","owner_hold_ids","required_fields_verified","isolation_approved","schema_approved","sync_receipts_installed","authenticated_sync_verified","core_readbacks_match","dashboard_live_readback","mobile_qa_passed","release_approved"]
    if any(k not in e for k in keys): raise ValueError("missing evidence")
    ids=e["source_ids"]
    if not ids or len(ids)!=len(set(ids)):raise ValueError("duplicate or empty IDs")
    held=set(e["owner_hold_ids"])
    if not held.issubset(set(ids)):raise ValueError("unknown hold")
    if "WORK-RENTALS-001" in ids and "WORK-RENTALS-001" not in held:raise ValueError("rentals hold missing")
    blockers=[]
    if not (set(ids)-held).issubset(set(e["approved_mappings"])):blockers.append("mapping_approval")
    for k in keys[3:]:
        if e[k] is not True:blockers.append(k)
    return {"ready_for_live":not blockers,"blockers":blockers}
