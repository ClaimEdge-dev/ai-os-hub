"""R8: public GitHub Actions gate for real pinned canonical source acceptance.

No API keys, external model calls, repository writes or uploaded artifacts.
The test works only in the existing GitHub Actions CI environment and does not
claim the earlier R4/R5 scripts were installed or executed.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

PIN = "ea4891221250719948fb641fd1b52d7fc7e40ff3"


def checked(args, *, cwd=None):
    p = subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, timeout=110, check=False)
    if p.returncode:
        raise AssertionError(f"command failed ({p.returncode}): {args[0]}: {p.stderr[-450:]}")
    return p.stdout.strip()


class TestR8PinnedSourceAcceptance(unittest.TestCase):
    def test_r8_readonly_canonical_and_independent_hashes(self):
        if os.environ.get("GITHUB_ACTIONS") != "true":
            self.skipTest("Real pinned Git checkout is required; not an offline fixture test")
        source = Path(os.environ["GITHUB_WORKSPACE"]).resolve(strict=True)
        self.assertTrue((source / "SKILL_REGISTRY.md").is_file())
        with tempfile.TemporaryDirectory(prefix="debo-r8-", dir=os.environ.get("RUNNER_TEMP")) as td:
            checkout = Path(td) / "pinned"
            result_dir = Path(td) / "reports"
            result_dir.mkdir()
            # The repo is public. Fetch an exact commit, not the moving default branch.
            checked(["git", "fetch", "--no-tags", "--depth=1", "origin", PIN], cwd=source)
            checked(["git", "worktree", "add", "--detach", str(checkout), PIN], cwd=source)
            self.assertEqual(checked(["git", "rev-parse", "HEAD"], cwd=checkout), PIN)
            self.assertEqual(checked(["git", "status", "--porcelain"], cwd=checkout), "")
            output = result_dir / "canonical.json"
            checked([sys.executable, str(checkout / "tools/debo_skill_delta.py"),
                     "--repo", str(checkout), "--include-projects",
                     "--validate-contracts", "--output", str(output)])
            canonical = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(canonical["schema"], "DEBO-SKILL-DELTA-v1")
            records = {r["id"]: r for r in canonical["skills"]}
            paths = []
            for r in records.values():
                if not r.get("source_path"):
                    continue
                path = checkout / r["source_path"]
                self.assertTrue(path.is_file(), r["id"])
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                                 r.get("source_sha256"), r["id"])
                self.assertEqual(r["runtime_installed"], "UNVERIFIED")
                paths.append(r["source_path"])
            self.assertEqual(len(paths), len(set(paths)))
            self.assertEqual(len(paths), 81)  # 22 root + 59 project-local paths
            tree = sorted(checkout.rglob("SKILL.md"))
            self.assertEqual(len(tree), 87)
            missing_from_canonical = sorted(str(p.relative_to(checkout))
                                            for p in tree if str(p.relative_to(checkout)) not in paths)
            self.assertEqual(len(missing_from_canonical), 6)  # 5 nested + 1 plugin
            self.assertEqual(canonical["summary"]["project_skill_sources"], 59)
            # No hidden file or test output is added to the pinned checkout.
            self.assertEqual(checked(["git", "status", "--porcelain"], cwd=checkout), "")
            print("DEBO_R8_ACCEPTANCE", json.dumps({
                "pinned_sha": PIN, "canonical_hashes_match": len(paths),
                "source_files": len(tree), "out_of_scope_nested_plugin": len(missing_from_canonical),
                "project_skills": canonical["summary"]["project_skill_sources"],
                "native_installed": "UNVERIFIED", "source_modified": False,
            }, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
