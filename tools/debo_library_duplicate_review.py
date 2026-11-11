#!/usr/bin/env python3
"""Read-only DEBO Library exact-duplicate receipt reconciliation.

Consumes *existing* source receipts and optional observed file metadata. Never
opens, edits, moves or deletes the files named by those receipts. SHA-256 values
are historical source claims until bytes are independently rehashed.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

HEX64 = re.compile(r"^[0-9a-f]{64}$")


def _read(path):
    with Path(path).open(encoding="utf-8") as f:
        return json.load(f)


def _family(row, source):
    ident = row.get("family_id")
    count = row.get("copies")
    ids = row.get("source_file_ids", row.get("file_ids"))
    names = row.get("materialized_names", row.get("source_names"))
    h = row.get("sha256")
    size = row.get("bytes_each")
    excess = row.get("potential_excess_bytes")
    if not isinstance(ident, str) or not re.fullmatch(r"LIB001-EXACT-\d{3}", ident):
        raise ValueError(f"invalid family ID: {ident!r}")
    if not isinstance(h, str) or not HEX64.fullmatch(h):
        raise ValueError(f"invalid historical SHA-256 for {ident}")
    if not isinstance(count, int) or count < 2 or not isinstance(size, int) or size < 0:
        raise ValueError(f"invalid copy count or file size for {ident}")
    if not isinstance(ids, list) or len(ids) != count or len(set(ids)) != count:
        raise ValueError(f"missing or duplicate source file IDs for {ident}")
    if not all(isinstance(i, str) and i.startswith("file_") for i in ids):
        raise ValueError(f"invalid source file ID for {ident}")
    if names is None:
        names = [None] * count  # R3 records source IDs but omits original filenames.
    if not isinstance(names, list) or len(names) != count:
        raise ValueError(f"missing or malformed filenames for {ident}")
    paths = row.get("source_paths")
    if paths is None and row.get("source_scope") == "ChatGPT Library root only":
        paths = ["/" + name if name else None for name in names]
    if paths is None:
        paths = [None] * count
    if len(paths) != count:
        raise ValueError(f"source path count mismatch for {ident}")
    if excess != (count - 1) * size:
        raise ValueError(f"excess byte arithmetic mismatch for {ident}")
    return {"family_id":ident,"basename":row.get("basename",row.get("canonical_candidate",row.get("subject",ident))),
            "copies":count,"historical_sha256":h,"bytes_each":size,"potential_extra_copies":count-1,
            "potential_excess_bytes":excess,"file_ids":ids,"names":names,"source_paths":paths,"receipt":source,
            "byte_status":"HISTORICAL_RECEIPT_NOT_REHASHED"}


def review(r1, r2, r3, snapshot=None):
    rows = ([(_family(x,"R1")) for x in r1["duplicate_validation"]["families"]]
           +[(_family(x,"R2")) for x in r2["exact_hash_families_new"]]
           +[_family(r3["duplicate_reference_checks"]["additional_verified_family"],"R3")])
    ids = [f["family_id"] for f in rows]
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate family ID")
    source_ids = [i for f in rows for i in f["file_ids"]]
    if len(set(source_ids)) != len(source_ids):
        raise ValueError("one Library source ID occurs in multiple exact-hash families")
    bytes_total = sum(f["potential_excess_bytes"] for f in rows)
    extra_total = sum(f["potential_extra_copies"] for f in rows)
    prior = r3["duplicate_reference_checks"]
    if (len(rows),extra_total,bytes_total) != (prior["cumulative_verified_families"],prior["cumulative_potential_extra_copies"],prior["cumulative_potential_excess_bytes"]):
        raise ValueError("R1/R2/R3 cumulative totals disagree")
    if (sum(f["potential_extra_copies"] for f in rows if f["receipt"]!="R3")
            !=r2["cumulative_with_r1"]["confirmed_excess_copy_count"]):
        raise ValueError("R1/R2 prior copy totals disagree")
    meta = {"coverage":"NOT_PROVIDED","expected_observed":0,"matches":0,"changed":0,"missing":0,"out_of_scope":sum(f["copies"] for f in rows)}
    if snapshot is not None:
        scopes = snapshot.get("complete_scopes", [])
        selected = snapshot.get("observed_file_ids", [])
        if not isinstance(selected, list) or len(set(selected)) != len(selected):
            raise ValueError("observed_file_ids must be a unique list")
        if not isinstance(scopes, list) or not all(isinstance(s,str) for s in scopes):
            raise ValueError("complete_scopes must be a list")
        indexed = {}
        for x in snapshot.get("files",[]):
            k=x.get("file_id")
            if not k or k in indexed:
                raise ValueError("missing or duplicate observed file ID")
            indexed[k]=x
        def in_scope(path, fid):
            return fid in selected or (path is not None and any(path.startswith(scope) and (scope == "/" and path.count("/") == 1 or scope != "/") for scope in scopes))
        meta={"coverage":"SCOPED_METADATA_ONLY" if scopes else "SELECTED_IDS_METADATA_ONLY","expected_observed":0,"matches":0,"changed":0,"missing":0,"out_of_scope":0}
        for f in rows:
            matches=[]
            for fid,name,path in zip(f["file_ids"],f["names"],f["source_paths"]):
                if not in_scope(path,fid):
                    meta["out_of_scope"]+=1
                    continue
                meta["expected_observed"]+=1
                x=indexed.get(fid)
                if x is None:
                    meta["missing"]+=1; matches.append("NOT_LISTED_IN_COMPLETE_SCOPE")
                elif x.get("size_bytes")!=f["bytes_each"] or x.get("name")!=name:
                    meta["changed"]+=1; matches.append("METADATA_CHANGED")
                else:
                    meta["matches"]+=1; matches.append("ID_NAME_SIZE_MATCH_ONLY")
            f["current_metadata"]={"checked":len(matches),"findings":matches}
    return {"schema":"debo.library_duplicate_review.v1","mode":"READ_ONLY_NO_MUTATION",
            "historical_exact_hash_families":len(rows),"historical_potential_extra_copies":extra_total,
            "historical_potential_excess_bytes":bytes_total,"actual_bytes_freed":0,
            "inventory":meta,"families":rows,
            "limitations":["Existing hashes are historical receipts, not freshly computed hashes.",
            "Listing ID/name/size is not byte or reference verification.",
            "No deletion, move, merge, archive, installation or link clearance is authorized or performed."]}


def main():
    p=argparse.ArgumentParser(description="Read-only reconciliation of existing DEBO Library receipts")
    for arg in ("r1","r2","r3"):p.add_argument("--"+arg,type=Path,required=True)
    p.add_argument("--snapshot",type=Path)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    out=review(_read(a.r1),_read(a.r2),_read(a.r3),_read(a.snapshot) if a.snapshot else None)
    content=json.dumps(out,indent=2,ensure_ascii=False)+"\n"
    if a.output:
        # Exclusive creation avoids a check-then-write overwrite race.
        with a.output.open("x",encoding="utf-8") as stream:
            stream.write(content)
        print(f"Wrote new read-only review: {a.output}")
    else:print(content)

if __name__=="__main__":main()
