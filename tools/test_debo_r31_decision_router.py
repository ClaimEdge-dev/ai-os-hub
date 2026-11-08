import unittest
from debo_r31_decision_router import Task, decide, batch
class DecisionRouterTests(unittest.TestCase):
    def test_safe_action(self): self.assertEqual(decide(Task("a","run_local_tests"),set(),set())[0],"AUTO")
    def test_production_gate(self): self.assertEqual(decide(Task("a","production_write"),set(),set())[0],"APPROVAL")
    def test_schema_gate(self): self.assertEqual(decide(Task("a","schema_migration"),set(),set())[0],"APPROVAL")
    def test_unknown_denied(self): self.assertEqual(decide(Task("a","execute_shell"),set(),set())[0],"BLOCKED")
    def test_dependencies(self): self.assertEqual(decide(Task("a","run_local_tests",("b",)),set(),set())[0],"BLOCKED")
    def test_dependencies_met(self): self.assertEqual(decide(Task("a","run_local_tests",("b",)),{"b"},set())[0],"AUTO")
    def test_failed_held(self): self.assertEqual(decide(Task("a","run_local_tests"),set(),{"a"})[0],"BLOCKED")
    def test_duplicates(self):
        with self.assertRaises(ValueError): batch([Task("a","read_source"),Task("a","read_source")],set(),set())
    def test_completed_skipped(self): self.assertEqual(batch([Task("a","read_source")],{"a"},set())["auto"],[])
    def test_owner_hold_gate(self): self.assertEqual(decide(Task("a","modify_owner_hold"),set(),set())[0],"APPROVAL")
if __name__=="__main__": unittest.main()
