"""Regression: never duplicate recovered steps or accept stale journal authority."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from debo_r129_interrupt_recovery import run_fixture

class RecoveryInterruptionTests(unittest.TestCase):
    def setUp(self):
        self.fixture=json.loads((ROOT/"tests"/"fixtures"/"debo_r128_recovery_synthetic.json").read_text())
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.journal=Path(self.temp.name)/"journal.json"

    def test_interrupt_then_resume_skips_persisted_step(self):
        first=run_fixture(self.fixture,self.journal,interrupt_after=1)
        second=run_fixture(self.fixture,self.journal)
        third=run_fixture(self.fixture,self.journal)
        self.assertEqual(len(first["executed_now"]),1)
        self.assertEqual(len(second["executed_now"]),1)
        self.assertEqual(third["executed_now"],[])
        self.assertNotEqual(first["executed_now"],second["executed_now"])
        saved=json.loads(self.journal.read_text())
        self.assertEqual(len(saved["receipts"]),2)
        self.assertEqual(len({r["task_id"] for r in saved["receipts"]}),2)
        self.assertEqual(first["real_tool_calls"],0)

    def test_fake_owner_approval_remains_owner_gate(self):
        run_fixture(self.fixture,self.journal)
        again=run_fixture(self.fixture,self.journal)
        self.assertEqual([a["action"] for a in again["remaining"]["approval"]],["approve_mapping"])
        self.assertNotIn("DEBO-R128-DOWNSTREAM",again["skipped_verified"])

    def test_changed_source_revision_blocks_old_journal(self):
        run_fixture(self.fixture,self.journal,interrupt_after=1)
        self.fixture["source_revision"]="synthetic-rev-2"
        with self.assertRaisesRegex(ValueError,"stale/cross-project"):
            run_fixture(self.fixture,self.journal)

    def test_changed_project_scope_blocks_old_journal(self):
        run_fixture(self.fixture,self.journal,interrupt_after=1)
        self.fixture["project_id"]="JCT"
        for task in self.fixture["tasks"]: task["project_id"]="JCT"
        for receipt in self.fixture["receipts"]: receipt["project_id"]="JCT"
        with self.assertRaisesRegex(ValueError,"stale/cross-project"):
            run_fixture(self.fixture,self.journal)

    def test_malformed_journal_cannot_trigger_rerun(self):
        self.journal.write_text('{"schema":"untrusted"}')
        with self.assertRaisesRegex(ValueError,"unrecognized"):
            run_fixture(self.fixture,self.journal)

    def test_no_journal_written_on_invalid_fixture(self):
        self.fixture["tasks"].append(self.fixture["tasks"][0].copy())
        with self.assertRaises(ValueError):
            run_fixture(self.fixture,self.journal)
        self.assertFalse(self.journal.exists())

    def test_no_existing_parent_is_error(self):
        with self.assertRaises(ValueError):
            run_fixture(self.fixture,Path(self.temp.name)/"other"/"state.json")

if __name__=="__main__":
    unittest.main()
