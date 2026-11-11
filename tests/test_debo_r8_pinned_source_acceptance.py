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
            checked([sys.executable, "-B", str(checkout / "tools/debo_skill_delta.py"),
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
            # R9: verify EVERY previously excluded nested/plugin source by
            # exact relative path and pinned Git blob, not a filename count.
            # Git blob SHA is independent of the canonical SHA-256 inventory.
            expected_extras = {
                "plugins/claimedge-policy-review-coverage-analyzer/SKILL.md":
                    "01ede85562792b2a919fd61d57b0917331e143c3",
                "skills/claimedge/inspection/field-evidence/v1/SKILL.md":
                    "70d55b7170429dcc7834302d8dae1dc793285d40",
                "skills/claimedge/intake/claimedge__intake__client-intake-suite__v1/SKILL.md":
                    "d9364d665c12e3628325d186e521fd9cbf9a8bca",
                "skills/claimedge/policy/coverage-review/v1/SKILL.md":
                    "ca8428d1083225fa3b78f46945196a362829b720",
                "skills/claimedge/policy/policy-review-coverage-analyzer/v1/SKILL.md":
                    "594e1c4e242b778d16a396f19fc35aba4fbb116f",
                "skills/claimedge/policy/policy-review-endorsement-tracker/v1/SKILL.md":
                    "893a54232d6d5a6c706c355edaa3a02532c1f601",
            }
            self.assertEqual(missing_from_canonical, sorted(expected_extras))
            extras_report = {}
            for source_path, expected_blob in sorted(expected_extras.items()):
                absolute = checkout / source_path
                self.assertTrue(absolute.is_file(), source_path)
                self.assertFalse(absolute.is_symlink(), source_path)
                tracked = checked(["git", "ls-tree", "HEAD", "--", source_path], cwd=checkout)
                self.assertTrue(tracked.endswith("\t" + source_path), source_path)
                tree_blob = tracked.split()[2]
                self.assertEqual(tree_blob, expected_blob, source_path)
                local_blob = checked(["git", "hash-object", "--", source_path], cwd=checkout)
                self.assertEqual(local_blob, expected_blob, source_path)
                extras_report[source_path] = {
                    "git_blob_sha1": expected_blob,
                    "content_sha256": hashlib.sha256(absolute.read_bytes()).hexdigest(),
                    "scope": "NESTED_OR_PLUGIN_SOURCE_ONLY",
                    "native_installed": "UNVERIFIED",
                }
            print("DEBO_R9_SIX_SOURCE_ACCEPTANCE", json.dumps({
                "pinned_sha": PIN, "verified": len(extras_report),
                "paths": extras_report, "source_modified": False,
            }, sort_keys=True))
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
