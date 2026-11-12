"""R19 focused resume acceptance. Synthetic capsules only; no connectors or writes."""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "tools" / "debo_r19_continuity.py"
spec = importlib.util.spec_from_file_location("r19", MODULE)
r19 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r19)


class ResumeContractTests(unittest.TestCase):
    def make(self, status="BLOCKED", project="DEBO", objective="Restore focus", next_action="Review PR #73 at 6a2f9b4e"):
        return r19.new_capsule(project, "DEBO-MASTER-025", objective, status,
                               "SYNTHETIC-FIXTURE", next_action, source_key="fixture-task-1")

    def test_exact_resume_and_no_live_claim(self):
        current = self.make(status="PROPOSED", next_action="Run: npx skills add addyosmani/agent-skills (AUDIT ONLY)")
        report = r19.resume_summary([current])
        self.assertEqual(report["next_action"], current["next_action"])
        self.assertEqual(report["reported_status"], "PROPOSED")
        self.assertEqual(report["writes"], 0)
        self.assertEqual(report["cross_chat_activation"], "NOT_VERIFIED")
        self.assertEqual(report["evidence_assurance"], "TYPED_REFERENCES_ONLY_NOT_AUTHENTICATED")

    def test_repeated_blocked_checkpoints_trigger_distinct_path(self):
        report = r19.resume_summary([self.make(), self.make(), self.make()])
        self.assertEqual(report["blocked_checkpoint_count"], 3)
        self.assertTrue(report["repeated_stall"])
        self.assertIn("distinct authorized recovery path", report["recovery_note"])

    def test_single_blocked_checkpoint_not_repeated(self):
        report = r19.resume_summary([self.make()])
        self.assertEqual(report["blocked_checkpoint_count"], 1)
        self.assertFalse(report["repeated_stall"])

    def test_unblocked_latest_not_stuck(self):
        report = r19.resume_summary([self.make(), self.make(status="PROPOSED")])
        self.assertFalse(report["repeated_stall"])
        self.assertEqual(report["blocked_checkpoint_count"], 1)

    def test_cross_project_rejected(self):
        with self.assertRaisesRegex(ValueError, "cross-project"):
            r19.resume_summary([self.make(project="JCT"), self.make(project="DEBO")])

    def test_cross_task_rejected(self):
        with self.assertRaisesRegex(ValueError, "different task_id"):
            r19.resume_summary([self.make(objective="Other objective"), self.make()])

    def test_empty_and_invalid_capsules_rejected(self):
        with self.assertRaises(ValueError):
            r19.resume_summary([])
        with self.assertRaises(ValueError):
            r19.resume_summary([{"schema": "bogus"}])

    def test_cli_json_reads_private_synthetic_file_without_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "capsule.json"
            data = self.make()
            original = json.dumps(data)
            path.write_text(original, encoding="utf-8")
            run = subprocess.run([sys.executable, str(MODULE), "resume", "--input", str(path), "--json"],
                                 check=False, capture_output=True, text=True, timeout=10)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(run.stdout)["next_action"], data["next_action"])
            self.assertEqual(path.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
