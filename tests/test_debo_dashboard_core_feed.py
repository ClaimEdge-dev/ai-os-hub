"""Tests for deterministic, non-sensitive DEBO Core feed generation."""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "debo_dashboard_core_feed.py"
sys.path.insert(0, str(MODULE_PATH.parent))
spec = importlib.util.spec_from_file_location("debo_dashboard_core_feed", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class PublicFeedTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        sources = list(mod.PUBLIC_INPUTS) + [p for p in mod.PROFILE_PATHS.values() if p]
        for rel in sources:
            dest = self.repo / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            if rel.endswith("/DEBO.md"):
                body = ("# DEBO compact startup brief v1\n\n"
                        "## Selected project: DEBO\n\n## Golden rules\n"
                        + "".join(f"{i}. Example rule\n" for i in range(1, 11))
                        + "\n## Source fingerprints (local SHA-256)\n- sha\n")
            else:
                body = "# Synthetic public fixture\n"
            dest.write_text(body, encoding="utf-8")

    def test_allowlisted_public_metadata_and_unknown_runtime(self):
        feed = mod.build_feed(self.repo)
        self.assertEqual(feed["schema_version"], "debo.core.public_feed.v1")
        self.assertEqual(feed["golden_rules_count"], 10)
        self.assertEqual(len(feed["projects"]), len(mod.PROFILE_PATHS))
        self.assertEqual(feed["data_classification"], "PUBLIC_GOVERNANCE_METADATA_ONLY")
        self.assertTrue(feed["permissions"]["read_only"])
        self.assertFalse(feed["permissions"]["automatic_approvals"])
        self.assertTrue(all(p["live_operational_status"] == "UNKNOWN" for p in feed["projects"]))
        self.assertNotIn("synthetic public fixture", mod.serialized(feed).lower())

    def test_deterministic_write_and_check(self):
        self.assertTrue(mod.update(self.repo, check_only=False))
        path = self.repo / mod.FEED_PATH
        before = path.read_bytes()
        self.assertFalse(mod.update(self.repo, check_only=False))
        self.assertFalse(mod.update(self.repo, check_only=True))
        self.assertEqual(before, path.read_bytes())

    def test_missing_feed_fails_check(self):
        with self.assertRaisesRegex(mod.FeedError, "absent or stale"):
            mod.update(self.repo, check_only=True)

    def test_source_change_changes_hash_not_operational_status(self):
        mod.update(self.repo, check_only=False)
        old = json.loads((self.repo / mod.FEED_PATH).read_text())
        (self.repo / mod.PUBLIC_INPUTS[0]).write_text("# Changed public policy\n")
        with self.assertRaises(mod.FeedError):
            mod.update(self.repo, check_only=True)
        self.assertTrue(mod.update(self.repo, check_only=False))
        new = json.loads((self.repo / mod.FEED_PATH).read_text())
        self.assertNotEqual(old["source_files"][0]["sha256"], new["source_files"][0]["sha256"])
        self.assertTrue(all(p["live_operational_status"] == "UNKNOWN" for p in new["projects"]))

    def test_missing_project_profile_fails_closed(self):
        (self.repo / next(p for p in mod.PROFILE_PATHS.values() if p)).unlink()
        with self.assertRaisesRegex(mod.FeedError, "Missing canonical"):
            mod.build_feed(self.repo)

    def test_invalid_runtime_brief_rejected(self):
        (self.repo / mod.PUBLIC_INPUTS[2]).write_text("Invalid brief", encoding="utf-8")
        with self.assertRaisesRegex(mod.FeedError, "missing expected"):
            mod.build_feed(self.repo)


if __name__ == "__main__":
    unittest.main()
