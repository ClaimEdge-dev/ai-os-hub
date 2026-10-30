import tempfile
import unittest
from pathlib import Path
from tools.debo_command_core import CommandCore


class CommandCoreTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name) / "core.sqlite"
        self.core = CommandCore(self.path, {"CE", "BBS"})
        self.addCleanup(lambda: self.core.close())

    def test_idempotent_restart(self):
        a = self.core.submit("note: Resume checkpoint", "CE", {"CE"}, "one")
        self.core.close()
        self.core = CommandCore(self.path, {"CE", "BBS"})
        self.assertEqual(self.core.execute_note(a["id"], {"CE"})["state"], "VERIFIED")
        self.assertEqual(self.core.execute_note(a["id"], {"CE"})["state"], "VERIFIED")
        self.assertEqual(len(self.core.events(a["id"], {"CE"})), 2)
        self.assertEqual(self.core.submit("note: Resume checkpoint", "CE", {"CE"}, "one")["id"], a["id"])

    def test_project_isolation(self):
        a = self.core.submit("note: CE note", "CE", {"CE"}, "two")
        with self.assertRaises(PermissionError):
            self.core.get(a["id"], {"BBS"})
        with self.assertRaises(PermissionError):
            self.core.execute_note(a["id"], {"BBS"})
        with self.assertRaises(PermissionError):
            self.core.submit("note: bad", "CE", {"BBS"}, "three")

    def test_approval_fails_closed(self):
        a = self.core.submit("send an email", "CE", {"CE"}, "four")
        self.assertEqual(a["state"], "WAITING_APPROVAL")
        with self.assertRaises(PermissionError):
            self.core.transition(a["id"], {"CE"}, "READY")
        with self.assertRaises(PermissionError):
            self.core.execute_note(a["id"], {"CE"})

    def test_invalid_transition_and_missing_evidence(self):
        a = self.core.submit("note: hello", "BBS", {"BBS"}, "five")
        with self.assertRaises(ValueError):
            self.core.transition(a["id"], {"BBS"}, "VERIFIED")
        self.core.transition(a["id"], {"BBS"}, "RUNNING", checkpoint="started")
        self.core.transition(a["id"], {"BBS"}, "VERIFYING")
        with self.assertRaises(ValueError):
            self.core.transition(a["id"], {"BBS"}, "VERIFIED")
        self.assertEqual(self.core.transition(a["id"], {"BBS"}, "VERIFIED", evidence="synthetic test")["state"], "VERIFIED")

    def test_conflicting_key(self):
        self.core.submit("note: first", "CE", {"CE"}, "same")
        with self.assertRaises(ValueError):
            self.core.submit("note: second", "CE", {"CE"}, "same")

    def test_list_scope_and_limit(self):
        self.core.submit("note: CE", "CE", {"CE"}, "list1")
        self.core.submit("note: BBS", "BBS", {"BBS"}, "list2")
        self.assertEqual(len(self.core.list_tasks({"CE"})), 1)
        self.assertEqual(self.core.list_tasks(set()), [])
        with self.assertRaises(ValueError):
            self.core.list_tasks({"CE"}, limit=101)

    def test_backup_integrity_and_restore(self):
        original = self.core.submit("note: checkpoint", "CE", {"CE"}, "backup-key")
        self.core.execute_note(original["id"], {"CE"})
        backup_path = Path(self.folder.name) / "snapshot.sqlite"
        receipt = self.core.backup_to(backup_path)
        self.assertEqual(receipt["integrity"], "ok")
        self.assertEqual(len(receipt["sha256"]), 64)
        with self.assertRaises(FileExistsError):
            self.core.backup_to(backup_path)
        restored = CommandCore(backup_path, {"CE", "BBS"})
        try:
            self.assertEqual(restored.get(original["id"], {"CE"})["state"], "VERIFIED")
            self.assertEqual(len(restored.events(original["id"], {"CE"})), 2)
        finally:
            restored.close()


if __name__ == "__main__":
    unittest.main()
