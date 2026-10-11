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
            rows.append({"number": int(match.group(1)), "skill": match.group(2),
                         "domain": domain, "installed": "UNVERIFIED"})
    numbers = [row["number"] for row in rows]
    counts = collections.Counter(numbers)
    names = collections.Counter(row["skill"] for row in rows)
    return {
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
