import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from debo_private_task_snapshot import build_private_snapshot, safe_summary, main
import json, tempfile, io
from contextlib import redirect_stdout

TASK={"task_id":"WORK-DEBO-001","title":"test","status":"In Progress","priority":"P1","assignee_role":"DEBO","pillar":"DEBO"}
class Tests(unittest.TestCase):
    def test_private_snapshot(self):
        x=build_private_snapshot([TASK],authenticated=True,source_branch="slice-day1",verified_at="2026-11-08T00:00:00+00:00")
        self.assertEqual(x["task_count"],1)
        self.assertFalse(x["live_sync"])
        self.assertEqual(x["classification"],"PRIVATE_AUTHENTICATED")
    def test_requires_auth(self):
        with self.assertRaises(PermissionError): build_private_snapshot([TASK],authenticated=False,source_branch="slice-day1")
    def test_rejects_default(self):
        with self.assertRaises(ValueError): build_private_snapshot([TASK],authenticated=True,source_branch="main")
    def test_rejects_duplicates(self):
        with self.assertRaises(ValueError): build_private_snapshot([TASK,TASK],authenticated=True,source_branch="slice-day1")
    def test_rejects_held(self):
        with self.assertRaises(ValueError): build_private_snapshot([{**TASK,"task_id":"WORK-RENTALS-001"}],authenticated=True,source_branch="slice-day1")
    def test_rejects_invalid_status(self):
        with self.assertRaises(ValueError): build_private_snapshot([{**TASK,"status":"LIVE"}],authenticated=True,source_branch="slice-day1")
    def test_summary_omits_private_fields(self):
        x=build_private_snapshot([TASK],authenticated=True,source_branch="slice-day1")
        summary=safe_summary(x)
        self.assertNotIn("tasks",summary)
        self.assertEqual(summary["task_count"],1)
    def test_offline_cli(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"rows.json"
            p.write_text(json.dumps([TASK]),encoding="utf-8")
            output=io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main([str(p),"--authenticated","--branch","slice-day1","--summary-only"]),0)
            result=json.loads(output.getvalue())
            self.assertNotIn("tasks",result)
            self.assertEqual(result["task_count"],1)
if __name__=="__main__": unittest.main()
