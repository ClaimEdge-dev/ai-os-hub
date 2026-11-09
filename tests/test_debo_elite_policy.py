"""Regression tests for source-only DEBO elite execution rules."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from debo_elite_policy_check import validate  # noqa: E402


class EliteExecutionPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = json.loads(
            (ROOT / "governance/DEBO_ELITE_EXECUTION_DEFAULT_v1.json").read_text(encoding="utf-8")
        )

    def changed(self, field, value):
        copy = deepcopy(self.original)
        copy[field] = value
        return validate(copy, ROOT)

    def test_current_canonical_source_passes(self):
        self.assertEqual(validate(self.original, ROOT), [])

    def test_tampered_active_runtime_claim_is_blocked(self):
        self.assertTrue(self.changed("active_runtime_verified", True))

    def test_source_merge_does_not_claim_cross_chat_installation(self):
        self.assertTrue(self.changed("effective_on_source_merge", True))

    def test_no_duplicate_fictional_agent_board(self):
        self.assertTrue(self.changed("agent_board", self.original["agent_board"] + ["Mack"]))

    def test_owner_spend_gate_cannot_disappear(self):
        actions = [x for x in self.original["approval_required_actions"] if x != "spend"]
        self.assertTrue(self.changed("approval_required_actions", actions))

    def test_production_write_gate_cannot_disappear(self):
        actions = [x for x in self.original["no_automatic_actions"] if x != "production_write"]
        self.assertTrue(self.changed("no_automatic_actions", actions))

    def test_rejects_unsafe_public_source_path(self):
        self.assertTrue(self.changed("source_prompt", "../private/task.txt"))

    def test_rejects_arbitrary_task_status(self):
        self.assertTrue(self.changed("task_states", ["COMPLETE"]))

    def test_does_not_reorder_verify_after_file(self):
        self.assertTrue(self.changed("work_sequence", [
            "RECOVER", "DEFINE", "ROUTE", "EXECUTE", "FILE", "VERIFY", "CHECKPOINT"
        ]))

    def test_requires_real_status_provenance(self):
        self.assertTrue(self.changed("implementation_states", ["LIVE", "DONE"]))


if __name__ == "__main__":
    unittest.main()
