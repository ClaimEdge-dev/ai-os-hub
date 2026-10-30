"""Regression tests for read-only change previews; no credentials or network."""
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("debo_sync_detect", ROOT / "tools/debo_sync_detect.py")
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class ChangeDetectTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = pathlib.Path(temp.name)
        original_paths = MOD.PUBLIC_PATHS.copy()
        MOD.PUBLIC_PATHS.add("docs/example.md")
        MOD.PUBLIC_PATHS.add("docs/link.md")
        MOD.PUBLIC_PATHS.add("docs/not-here.md")
        self.addCleanup(lambda: MOD.PUBLIC_PATHS.clear() or MOD.PUBLIC_PATHS.update(original_paths))
        (self.root / "docs").mkdir()
        (self.root / "docs/example.md").write_text("first", encoding="utf-8")
        self.manifest = {"version": 1, "sources": [{"id": "public-doc", "kind": "repo_file", "path": "docs/example.md"}]}
        self.state = {"sources": {}}

    def run_preview(self):
        return MOD.preview(self.root, self.manifest, self.state)

    def test_first_observation_stages_version_one_without_writes(self):
        result = self.run_preview()
        self.assertEqual(result["proposed_changes"], 1)
        self.assertEqual(result["records"][0]["proposed_version"], 1)
        self.assertFalse(result["runtime_writes"])
        self.assertFalse(result["persistent_receipts_written"])

    def test_same_fingerprint_skipped_without_new_version(self):
        current = self.run_preview()["records"][0]
        self.state["sources"]["public-doc"] = {"fingerprint": current["new_fingerprint"], "version": 7}
        result = self.run_preview()
        self.assertEqual(result["skipped_unchanged"], 1)
        self.assertIsNone(result["records"][0]["change_event_proposal"])
        self.assertEqual(result["records"][0]["proposed_version"], 7)

    def test_changed_fingerprint_proposes_next_version(self):
        self.state["sources"]["public-doc"] = {"fingerprint": "a" * 64, "version": 7}
        result = self.run_preview()
        self.assertEqual(result["records"][0]["change_event_proposal"]["version"], 8)

    def test_repeat_dry_run_is_stable_and_does_not_mutate_snapshot(self):
        before = json.dumps(self.state, sort_keys=True)
        self.assertEqual(self.run_preview(), self.run_preview())
        self.assertEqual(before, json.dumps(self.state, sort_keys=True))

    def test_duplicate_source_prevented(self):
        self.manifest["sources"].append(dict(self.manifest["sources"][0]))
        with self.assertRaises(MOD.PreviewBlocked):
            self.run_preview()

    def test_duplicate_entity_prevented(self):
        self.manifest["sources"].append({"id": "other", "kind": "repo_file", "path": "docs/example.md"})
        with self.assertRaises(MOD.PreviewBlocked):
            self.run_preview()

    def test_secrets_cannot_be_scanned_from_manifest(self):
        (self.root / ".env").write_text("do-not-read", encoding="utf-8")
        self.manifest["sources"][0]["path"] = ".env"
        with self.assertRaises(MOD.PreviewBlocked):
            self.run_preview()

    def test_parent_traversal_prevented(self):
        self.manifest["sources"][0]["path"] = "../secret.txt"
        with self.assertRaises(MOD.PreviewBlocked):
            self.run_preview()

    def test_symlink_prevented(self):
        (self.root / "docs/link.md").symlink_to(self.root / "docs/example.md")
        self.manifest["sources"][0]["path"] = "docs/link.md"
        with self.assertRaises(MOD.PreviewBlocked):
            self.run_preview()

    def test_unverified_state_blocks(self):
        self.state["sources"]["public-doc"] = {"fingerprint": "bad", "version": 1}
        with self.assertRaises(MOD.PreviewBlocked):
            self.run_preview()

    def test_missing_source_blocks(self):
        self.manifest["sources"][0]["path"] = "docs/not-here.md"
        with self.assertRaises(MOD.PreviewBlocked):
            self.run_preview()

    def test_unsupported_connector_type_blocks(self):
        self.manifest["sources"][0]["kind"] = "drive_file"
        with self.assertRaises(MOD.PreviewBlocked):
            self.run_preview()

    def test_private_snapshot_is_read_only_and_git_excluded(self):
        fp = self.run_preview()["records"][0]["new_fingerprint"]
        snapshot_dir = self.root / "sync" / ".private"
        snapshot_dir.mkdir(parents=True)
        snapshot = snapshot_dir / "ledger_state.json"
        snapshot.write_text(json.dumps({"sources": {"public-doc": {"fingerprint": fp, "version": 7}}}), encoding="utf-8")
        self.assertEqual(MOD.validate_snapshot_path(self.root, "sync/.private/ledger_state.json"), snapshot)
        previous = snapshot.read_bytes()
        result = self.run_preview_with_snapshot(snapshot)
        self.assertEqual(result["skipped_unchanged"], 1)
        self.assertEqual(result["records"][0]["proposed_version"], 7)
        self.assertEqual(snapshot.read_bytes(), previous)

    def run_preview_with_snapshot(self, snapshot):
        state = json.loads(snapshot.read_text(encoding="utf-8"))
        return MOD.preview(self.root, self.manifest, state)

    def test_snapshot_outside_private_directory_blocks(self):
        with self.assertRaises(MOD.PreviewBlocked):
            MOD.validate_snapshot_path(self.root, "docs/example.md")

    def test_cli_fails_closed_on_non_dry_run(self):
        proc = subprocess.run([sys.executable, str(ROOT / "tools/debo_sync_detect.py"), "--dry-run=false"], text=True, capture_output=True)
        self.assertNotEqual(proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()
