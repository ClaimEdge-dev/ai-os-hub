#!/usr/bin/env python3
"""Read-only local project inventory. Detailed filenames and hashes stay in a private report.

Does not extract ZIPs, follow symlinks, rename, move, upload, execute, or delete.
This is a generic complement to the existing DEBO skill and export-recovery tools.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import ntpath
import os
import re
import stat
import unicodedata
import zipfile
from collections import defaultdict
from pathlib import Path

SCHEMA = "debo.project-inventory.v1"
GENERATED_DIRS = frozenset({".git", ".next", ".venv", "node_modules", "__pycache__"})
MAX_ENTRIES = 5000
MAX_FILE_BYTES = 128 * 1024 * 1024
MAX_TOTAL_BYTES = 512 * 1024 * 1024
MAX_COMPRESSION_RATIO = 200
CHUNK = 1024 * 1024


def _digest(stream):
    sha = hashlib.sha256()
    total = 0
    while True:
        block = stream.read(CHUNK)
        if not block:
            break
        total += len(block)
        if total > MAX_FILE_BYTES:
            raise ValueError("file exceeds safe hashing limit")
        sha.update(block)
    return sha.hexdigest(), total


def _safe_zip_name(name):
    normalized = name.replace("\\", "/")
    parts = normalized.split("/")
    if (not normalized or normalized.startswith("/") or ntpath.splitdrive(normalized)[0]
            or any(part in ("", ".", "..") for part in parts)
            or "\x00" in normalized):
        return None
    return normalized


def _entry(path, status, size=None, sha256=None):
    return {"path": path, "status": status, "size": size, "sha256": sha256}


def _directory_entries(root, include_generated):
    entries = []
    total_hashed = 0

    def record(row):
        if len(entries) >= MAX_ENTRIES:
            raise ValueError("too many entries; inventory a smaller scope")
        entries.append(row)

    def unreadable_dir(error):
        # os.walk normally ignores scandir failures. Never report full coverage
        # if a root/subdirectory was inaccessible.
        try:
            rel = Path(error.filename).relative_to(root).as_posix()
        except (TypeError, ValueError):
            rel = "[unreadable directory]"
        record(_entry(rel, "UNREADABLE_DIRECTORY"))

    for parent, dirs, files in os.walk(root, topdown=True, followlinks=False,
                                       onerror=unreadable_dir):
        relative = Path(parent).relative_to(root)
        retained = []
        for dirname in sorted(dirs):
            rel = (relative / dirname).as_posix()
            target = Path(parent) / dirname
            if target.is_symlink():
                record(_entry(rel, "SKIPPED_SYMLINK"))
            elif not include_generated and dirname in GENERATED_DIRS:
                record(_entry(rel, "SKIPPED_GENERATED_DIRECTORY"))
            else:
                retained.append(dirname)
        dirs[:] = retained
        for filename in sorted(files):
            path = Path(parent) / filename
            rel = (relative / filename).as_posix()
            if path.is_symlink():
                record(_entry(rel, "SKIPPED_SYMLINK"))
                continue
            try:
                size = path.stat().st_size
                if not path.is_file():
                    record(_entry(rel, "SKIPPED_NONREGULAR"))
                elif size > MAX_FILE_BYTES:
                    record(_entry(rel, "SKIPPED_OVERSIZE", size))
                elif total_hashed + size > MAX_TOTAL_BYTES:
                    record(_entry(rel, "SKIPPED_TOTAL_LIMIT", size))
                else:
                    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
                    fd = os.open(path, flags)
                    with os.fdopen(fd, "rb") as stream:
                        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                            record(_entry(rel, "SKIPPED_NONREGULAR"))
                        else:
                            digest, actual = _digest(stream)
                            total_hashed += actual
                            record(_entry(rel, "HASHED", actual, digest))
            except (OSError, ValueError):
                record(_entry(rel, "UNREADABLE"))
    return entries


def _zip_entries(archive):
    entries = []
    with zipfile.ZipFile(archive) as source:
        members = source.infolist()
        if len(members) > MAX_ENTRIES:
            raise ValueError("too many ZIP members; inventory a smaller scope")
        total_declared = 0
        seen = set()
        for member in members:
            if member.is_dir():
                continue
            name = _safe_zip_name(member.filename)
            if name is None:
                entries.append(_entry("[unsafe ZIP path]", "UNSAFE_PATH"))
                continue
            if name in seen:
                entries.append(_entry(name, "DUPLICATE_MEMBER_NAME"))
                continue
            seen.add(name)
            if stat.S_IFMT(member.external_attr >> 16) == stat.S_IFLNK:
                entries.append(_entry(name, "SKIPPED_SYMLINK"))
                continue
            if member.flag_bits & 1:
                entries.append(_entry(name, "SKIPPED_ENCRYPTED"))
                continue
            if member.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED):
                entries.append(_entry(name, "SKIPPED_COMPRESSION"))
                continue
            total_declared += member.file_size
            ratio = member.file_size / max(member.compress_size, 1)
            if (member.file_size > MAX_FILE_BYTES or total_declared > MAX_TOTAL_BYTES
                    or ratio > MAX_COMPRESSION_RATIO):
                entries.append(_entry(name, "SKIPPED_LIMIT", member.file_size))
                continue
            try:
                with source.open(member) as stream:
                    digest, actual = _digest(stream)
                if actual != member.file_size:
                    entries.append(_entry(name, "SIZE_MISMATCH"))
                else:
                    entries.append(_entry(name, "HASHED", actual, digest))
            except (OSError, RuntimeError, ValueError, zipfile.BadZipFile):
                entries.append(_entry(name, "UNREADABLE"))
    return entries


def inventory(source, project_id, include_generated=False):
    """Return deterministic evidence about accessible bytes, not semantic authority."""
    source = Path(source)
    if source.is_symlink():
        raise ValueError("source symlink not allowed")
    if source.is_dir():
        kind = "directory"
        entries = _directory_entries(source, include_generated)
    elif source.is_file() and zipfile.is_zipfile(source):
        kind = "zip"
        entries = _zip_entries(source)
    else:
        raise ValueError("source must be an existing directory or valid ZIP")
    entries.sort(key=lambda row: (row["path"], row["status"]))
    hashes = defaultdict(list)
    names = defaultdict(list)
    for row in entries:
        names[unicodedata.normalize("NFC", row["path"]).casefold()].append(row["path"])
        if row["status"] == "HASHED":
            hashes[(row["size"], row["sha256"])].append(row["path"])
    duplicates = [
        {"size": size, "sha256": digest, "paths": sorted(paths)}
        for (size, digest), paths in sorted(hashes.items())
        if len(paths) > 1
    ]
    collisions = [
        {"normalized_path": key, "paths": sorted(set(paths))}
        for key, paths in sorted(names.items())
        if len(set(paths)) > 1
    ]
    hashed = sum(row["status"] == "HASHED" for row in entries)
    return {
        "schema": SCHEMA,
        "project_id": project_id,
        "source": {"type": kind, "label": source.name, "scope": "LOCAL_READ_ONLY"},
        "limits": {"max_entries": MAX_ENTRIES, "max_file_bytes": MAX_FILE_BYTES,
                   "max_total_zip_bytes": MAX_TOTAL_BYTES},
        "entries": entries,
        "exact_duplicates": duplicates,
        "potential_name_collisions": collisions,
        "summary": {
            "total_entries": len(entries), "hashed": hashed,
            "skipped_or_unreadable": len(entries) - hashed,
            "exact_duplicate_groups": len(duplicates),
            "potential_name_collisions": len(collisions),
            "coverage": "PARTIAL" if hashed != len(entries) else "HASHED_ACCESSIBLE_FILES",
        },
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--private-report", type=Path, required=True)
    parser.add_argument("--include-generated", action="store_true")
    parser.add_argument("--replace-report", action="store_true")
    args = parser.parse_args(argv)
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{1,63}", args.project_id):
        parser.error("invalid project ID")
    source = args.source.resolve()
    report = args.private_report.resolve()
    if args.source.is_dir() and report.is_relative_to(source):
        parser.error("private report must be outside the inventoried directory")
    if source == report:
        parser.error("report cannot overwrite source")
    if report.exists() and not args.replace_report:
        parser.error("report exists; use --replace-report only with explicit authorization")
    result = inventory(args.source, args.project_id, args.include_generated)
    report.parent.mkdir(parents=True, exist_ok=True)
    with report.open("w" if args.replace_report else "x", encoding="utf-8") as output:
        json.dump(result, output, indent=2, ensure_ascii=False)
        output.write("\n")
    print(json.dumps({"schema": SCHEMA, "coverage": result["summary"]["coverage"],
                      "total_entries": result["summary"]["total_entries"],
                      "hashed": result["summary"]["hashed"],
                      "skipped_or_unreadable": result["summary"]["skipped_or_unreadable"],
                      "exact_duplicate_groups": result["summary"]["exact_duplicate_groups"],
                      "private_report_written": True}, sort_keys=True))


if __name__ == "__main__":
    main()
