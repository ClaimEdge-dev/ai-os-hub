"""R10: run R4 inventory, R5 bridge and R6 orchestrator on one real pinned Git checkout.

All reports remain in RUNNER_TEMP and are not uploaded or printed.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

PIN = "ea4891221250719948fb641fd1b52d7fc7e40ff3"

def checked(args, cwd):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=120)
    if p.returncode:
        raise AssertionError("git operation failed: " + p.stderr[-350:])
    return p.stdout.strip()

class TestDEBOR10CombinedAcceptance(unittest.TestCase):
    def test_real_pinned_source_r4_r5_r6(self):
        if os.environ.get("GITHUB_ACTIONS") != "true":
            self.skipTest("Real pinned GitHub Actions checkout required")
        root = Path(os.environ["GITHUB_WORKSPACE"]).resolve(strict=True)
        tools = root / "tests" / "r10"
        for name in ("debo_recover.py", "debo_recovery_bridge.py", "run_pinned_acceptance.py"):
            self.assertTrue((tools / name).is_file(), name)
        with tempfile.TemporaryDirectory(prefix="debo-r10-", dir=os.environ.get("RUNNER_TEMP")) as temp:
            tempdir = Path(temp)
            pinned = tempdir / "pinned"
            report_dir = tempdir / "output"
            checked(["git", "fetch", "--no-tags", "--depth=1", "origin", PIN], cwd=root)
            checked(["git", "worktree", "add", "--detach", str(pinned), PIN], cwd=root)
            self.assertEqual(checked(["git", "rev-parse", "HEAD"], cwd=pinned), PIN)
            self.assertEqual(checked(["git", "status", "--porcelain"], cwd=pinned), "")
            env = os.environ.copy()
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            p = subprocess.run([
                sys.executable, "-B", str(tools / "run_pinned_acceptance.py"),
                "--repo", str(pinned),
                "--r4-script", str(tools / "debo_recover.py"),
                "--r5-script", str(tools / "debo_recovery_bridge.py"),
                "--output", str(report_dir)],
                cwd=root, env=env, capture_output=True, text=True, timeout=200)
            self.assertEqual(p.returncode, 0, "R6 run failed: " + p.stderr[-800:])
            a = json.loads((report_dir / "acceptance.json").read_text())
            canonical = json.loads((report_dir / "canonical.json").read_text())
            recovery = json.loads((report_dir / "recovery.json").read_text())
            bridge = json.loads((report_dir / "bridge.json").read_text())
            self.assertEqual(a["run_status"], "PASS_LOCAL_PINNED_CHECKOUT")
            self.assertEqual(a["pinned_checkout"], PIN)
            self.assertEqual(canonical["schema"], "DEBO-SKILL-DELTA-v1")
            self.assertEqual(recovery["schema_version"], 1)
            self.assertEqual(bridge["schema"], "DEBO-RECOVERY-DELTA-BRIDGE-v1")
            self.assertEqual(bridge["summary"]["skill_sources"], 81)
            self.assertEqual(bridge["summary"]["hash_matches"], 81)
            self.assertEqual(bridge["summary"]["hash_mismatches"], 0)
            self.assertEqual(bridge["summary"]["not_matched_or_unverifiable"], 0)
            self.assertEqual(bridge["summary"]["ambiguous_names"], 0)
            self.assertEqual(canonical["summary"]["project_skill_sources"], 59)
            self.assertGreaterEqual(recovery["summary"]["files"], 87)
            self.assertEqual(checked(["git", "status", "--porcelain"], cwd=pinned), "")
            # This receipt contains counts only, not filenames or document contents.
            print("DEBO_R10_ACCEPTANCE", json.dumps({
                "pin": PIN, "status": "PASS_REAL_COMBINED_SOURCE",
                "canonical_skill_hash_matches": bridge["summary"]["hash_matches"],
                "mismatches": 0, "ambiguous": 0,
                "all_SKILL_md_paths": 87,
                "nested_plugin_already_verified_in_R9": 6,
                "source_modified": False,
                "native_chatgpt_installed": "UNVERIFIED"
            }, sort_keys=True))

if __name__ == "__main__":
    unittest.main()
