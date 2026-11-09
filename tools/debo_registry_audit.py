#!/usr/bin/env python3
"""Audit Markdown skill registry without equating ACTIVE labels with installed skills."""
import argparse
import collections
import json
import pathlib
import re

def audit(text):
    rows = []
    domain = "unknown"
    for line in text.splitlines():
        if line.startswith("## Domain "):
            domain = line.lstrip("# ").strip()
        match = re.match(r"^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|", line)
        if match:
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            source_status = cells[-1].upper() if cells else "UNSPECIFIED"
            rows.append({"number": int(match.group(1)), "skill": match.group(2),
                         "domain": domain, "source_status": source_status,
                         "installed": "UNVERIFIED"})
    statuses = collections.Counter(row["source_status"] for row in rows)
    # Only the historical numbered catalog counts here; source files are
    # inventoried separately. Status labels do not prove runtime installation.
    declared = {}
    for line in text.splitlines():
        m = re.match(r"^\|\s*(Total Skills|Source-labelled Active|Draft|Deprecated|Archived)\s*\|\s*(\d+)\s*\|\s*$", line)
        if m:
            declared[m.group(1)] = int(m.group(2))
    actual = {"Total Skills": len(rows),
              "Source-labelled Active": statuses["ACTIVE"],
              "Draft": statuses["DRAFT"],
              "Deprecated": statuses["DEPRECATED"],
              "Archived": statuses["ARCHIVED"]}
    differences = {name: {"declared": declared[name], "actual": value}
                   for name, value in actual.items()
                   if name in declared and declared[name] != value}
    numbers = [row["number"] for row in rows]
    counts = collections.Counter(numbers)
    names = collections.Counter(row["skill"] for row in rows)
    return {
        "source_status_counts": dict(statuses),
        "declared_stats": declared,
        "stats_conflicts": differences,
        "stats_match": len(differences) == 0 if declared else None,
        "row_count": len(rows),
        "unique_numbers": len(counts),
        "duplicate_numbers": sorted(n for n, count in counts.items() if count > 1),
        "missing_numbers": sorted(set(range(1, max(numbers) + 1)) - set(numbers)) if numbers else [],
        "duplicate_skill_names": sorted(n for n, count in names.items() if count > 1),
        "domains": dict(collections.Counter(row["domain"] for row in rows)),
        "skills": rows,
        "runtime_installation_verified": False,
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("registry")
    parser.add_argument("--output")
    args = parser.parse_args()
    result = audit(pathlib.Path(args.registry).read_text(encoding="utf-8"))
    output = json.dumps(result, indent=2)
    if args.output:
        pathlib.Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)

if __name__ == "__main__":
    main()
