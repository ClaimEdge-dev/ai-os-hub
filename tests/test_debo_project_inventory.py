"""Synthetic safety and determinism tests for read-only DEBO project inventory."""
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from debo_project_inventory import SCHEMA, inventory, main


class ProjectInventoryTests(unittest.TestCase):
    def test_directory_hashes_duplicates_and_skips_generated(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "source"
            root.mkdir()
            (root / "a.txt").write_text("same", encoding="utf-8")
            (root / "b.txt").write_text("same", encoding="utf-8")
            (root / "other.txt").write_text("different", encoding="utf-8")
            (root / "node_modules").mkdir()
            (root / "node_modules" / "ignored.js").write_text("secret", encoding="utf-8")
            first = inventory(root, "TEST")
            second = inventory(root, "TEST")
            self.assertEqual(first, second)
            self.assertEqual(first["schema"], SCHEMA)
            self.assertEqual(first["summary"]["hashed"], 3)
            self.assertEqual(first["summary"]["coverage"], "PARTIAL")
            self.assertEqual(first["summary"]["exact_duplicate_groups"], 1)
            self.assertEqual(first["exact_duplicates"][0]["paths"], ["a.txt", "b.txt"])
            self.assertNotIn("ignored.js", json.dumps(first))
            self.assertIn("SKIPPED_GENERATED_DIRECTORY", json.dumps(first))

    def test_casefold_collision_is_not_automatic_duplicate(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "Alpha.txt").write_text("one", encoding="utf-8")
            (root / "alpha.txt").write_text("two", encoding="utf-8")
            result = inventory(root, "TEST")
            self.assertEqual(result["summary"]["potential_name_collisions"], 1)
            self.assertEqual(result["summary"]["exact_duplicate_groups"], 0)

    def test_zip_traversal_duplicate_and_symlink_are_not_hashed(self):
        with tempfile.TemporaryDirectory() as temp:
            archive = Path(temp) / "test.zip"
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                with zipfile.ZipFile(archive, "w") as z:
                    z.writestr("good.txt", "hello")
                    z.writestr("../escape.txt", "bad")
                    z.writestr("..\\windows.txt", "bad")
                    z.writestr("good.txt", "duplicate member")
                    link = zipfile.ZipInfo("link.txt")
                    link.create_system = 3
                    link.external_attr = (0o120777 << 16)
                    z.writestr(link, "target")
            result = inventory(archive, "TEST")
            statuses = [e["status"] for e in result["entries"]]
            self.assertEqual(result["summary"]["hashed"], 1)
            self.assertEqual(statuses.count("UNSAFE_PATH"), 2)
            self.assertIn("DUPLICATE_MEMBER_NAME", statuses)
            self.assertIn("SKIPPED_SYMLINK", statuses)
            self.assertEqual(result["summary"]["coverage"], "PARTIAL")

    def test_zip_compression_ratio_guard(self):
        with tempfile.TemporaryDirectory() as temp:
            archive = Path(temp) / "bomb.zip"
            with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
                z.writestr("compressible.bin", b"0" * (2 * 1024 * 1024))
            result = inventory(archive, "TEST")
            self.assertEqual(result["entries"][0]["status"], "SKIPPED_LIMIT")
            self.assertEqual(result["summary"]["hashed"], 0)

    def test_cli_private_report_outside_source_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "source"
            root.mkdir()
            (root / "confidential-name.txt").write_text("content", encoding="utf-8")
            report = Path(temp) / "private" / "manifest.json"
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                main([str(root), "--project-id", "TEST", "--private-report", str(report)])
            stdout = buffer.getvalue()
            self.assertNotIn("confidential-name", stdout)
            self.assertTrue(report.exists())
            self.assertEqual(json.loads(report.read_text())["summary"]["hashed"], 1)
            with self.assertRaises(SystemExit):
                main([str(root), "--project-id", "TEST", "--private-report", str(report)])
            with self.assertRaises(SystemExit):
                main([str(root), "--project-id", "TEST",
                      "--private-report", str(root / "report.json")])

    def test_symlink_not_followed(self):
        if not hasattr(os, "symlink"):
            self.skipTest("symlinks unavailable")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "root"
            root.mkdir()
            outside = Path(temp) / "outside.txt"
            outside.write_text("private outside", encoding="utf-8")
            try:
                (root / "pointer").symlink_to(outside)
            except OSError:
                self.skipTest("symlink creation not permitted")
            result = inventory(root, "TEST")
            self.assertEqual(result["summary"]["hashed"], 0)
            self.assertEqual(result["entries"][0]["status"], "SKIPPED_SYMLINK")
            self.assertNotIn("private outside", json.dumps(result))


if __name__ == "__main__":
    unittest.main()
