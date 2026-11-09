"""Source-only regression of R127 gated task editing in the EXISTING DEBO-05 app.

No database writes, billing, deployments or credentials are used by these tests.
"""
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "projects" / "debo-05" / "task-editor-r127"

class R127TaskEditorReview(unittest.TestCase):
    def test_js_endpoint_negative_and_positive_cases(self):
        node=shutil.which("node")
        if not node: self.skipTest("Node unavailable; JS tests NOT RUN")
        proc=subprocess.run([node,"--test",str(APP/"tests/test-editor.mjs")],
                            capture_output=True,text=True,timeout=30)
        self.assertEqual(proc.returncode,0,proc.stdout + "\n" + proc.stderr)
        self.assertIn("# pass 18",proc.stdout)

    def test_read_role_stays_separate_from_owner_editor(self):
        api=(APP/"src/api/task-editor.js").read_text(encoding="utf-8")
        sql=(APP/"sql/001_task_editor_review_only.sql").read_text(encoding="utf-8")
        summary=(APP/"src/api/summary.candidate.js").read_text(encoding="utf-8")
        self.assertIn("DEBO_NEON_EDITOR_DSN",api)
        self.assertNotIn("DEBO_NEON_READONLY_DSN",api)
        self.assertIn("DEBO_NEON_READONLY_DSN",summary)
        self.assertIn("archived_at IS NULL",summary)
        self.assertIn("editor_revision",summary)
        self.assertIn("SECURITY DEFINER",sql)
        self.assertIn("REVOKE ALL ON FUNCTION",sql)
        self.assertIn("WORK-RENTALS-001",sql)
        self.assertIn("task_editor_authorizations",sql)
        self.assertIn("FOR UPDATE",sql)
        self.assertIn("task_editor_audit",sql)
        self.assertNotIn("GRANT INSERT ON claimedge_os.tasks",sql)
        self.assertNotIn("GRANT UPDATE ON claimedge_os.tasks",sql)
        self.assertNotIn("GRANT DELETE ON claimedge_os.tasks",sql)

    def test_editor_never_persists_user_key_in_browser_storage(self):
        ui=(APP/"src/ui/task-editor-widget.js").read_text(encoding="utf-8")
        self.assertNotIn("localStorage.setItem",ui)
        self.assertNotIn("sessionStorage",ui)
        self.assertNotIn("innerHTML",ui)
        self.assertIn("type='password'",ui)
        self.assertIn("window.confirm(",ui)

    def test_existing_deployment_is_not_silently_mutated(self):
        readme=(APP/"README.md").read_text(encoding="utf-8")
        self.assertIn("REVIEW CANDIDATE",readme)
        self.assertIn("NOT",readme)
        self.assertIn("separate",readme.lower())

if __name__=="__main__":
    unittest.main()
