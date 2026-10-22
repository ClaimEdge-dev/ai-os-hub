#!/usr/bin/env python3
"""Offline validation of DEBO registry JSON. No external dependencies."""
import json, pathlib, re, sys
VALID = {"DISCOVERED","DRAFT","TESTED","APPROVED","PACKAGED","INSTALLED","VERIFIED","BLOCKED","RETIRED"}
def validate(item):
    for key in ("skill_id","version","source_path","status"):
        if not isinstance(item.get(key),str) or not item[key].strip():
            raise ValueError(f"Missing/invalid {key}")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*",item["skill_id"]):
        raise ValueError("Invalid skill_id")
    if item["status"] not in VALID: raise ValueError("Invalid status")
    if item["status"]=="VERIFIED" and not item.get("evidence_url"):
        raise ValueError("VERIFIED requires evidence_url")
def main():
    path=pathlib.Path(sys.argv[1])
    rows=json.loads(path.read_text())
    if not isinstance(rows,list): raise ValueError("Expected JSON array")
    seen=set()
    for row in rows:
        validate(row)
        if row["skill_id"] in seen: raise ValueError("Duplicate skill_id")
        seen.add(row["skill_id"])
    print(f"PASS: {len(rows)} skill records validated")
if __name__=="__main__": main()
