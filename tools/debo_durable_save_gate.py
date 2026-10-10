#!/usr/bin/env python3
"""DEBO durable-save verification. Python 3 standard library only."""
import argparse
import hashlib
import json
import pathlib
import sys
import zipfile

def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def verify(local, remote, expected=None):
    a, b = pathlib.Path(local), pathlib.Path(remote)
    if not a.is_file() or not b.is_file():
        return {"status": "BLOCKED", "reason": "Local or read-back file missing"}
    if a.suffix.lower() == ".zip":
        try:
            with zipfile.ZipFile(a) as z:
                if z.testzip() is not None:
                    return {"status": "FAILED_VERIFICATION", "reason": "Invalid local ZIP"}
        except (OSError, zipfile.BadZipFile):
            return {"status": "FAILED_VERIFICATION", "reason": "Unreadable local ZIP"}
    ah, bh = digest(a), digest(b)
    if expected and ah.lower() != expected.lower():
        return {"status": "FAILED_VERIFICATION", "reason": "Local hash differs from expected", "local_sha256": ah}
    return {"status": "VERIFIED" if ah == bh else "FAILED_VERIFICATION", "local_sha256": ah, "readback_sha256": bh, "matching": ah == bh}

def main():
    p = argparse.ArgumentParser(description="Compare a local artifact against an independently downloaded durable copy")
    p.add_argument("local")
    p.add_argument("readback")
    p.add_argument("--expected-sha256")
    args = p.parse_args()
    result = verify(args.local, args.readback, args.expected_sha256)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "VERIFIED" else 1

if __name__ == "__main__":
    sys.exit(main())
