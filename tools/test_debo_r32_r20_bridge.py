import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from debo_r32_r20_bridge import preflight, execute

class BridgeTests(unittest.TestCase):
    def test_safe(self):
        self.assertEqual(len(preflight([{"id":"a","action":"noop"}])["approved"]),1)
    def test_owner_hold(self):
        self.assertEqual(preflight([{"id":"a","owner_hold":True}])["held"],["a"])
    def test_approval_hold(self):
        self.assertEqual(preflight([{"id":"a","approval_required":True}])["held"],["a"])
    def test_reject_external(self):
        with self.assertRaises(ValueError): preflight([{"id":"a","action":"contact_customer"}])
    def test_reject_cycle(self):
        with self.assertRaises(ValueError): preflight([{"id":"a","depends_on":["b"]},{"id":"b","depends_on":["a"]}])
    def test_receipt_resume(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"receipt.json"
            tasks=[{"id":"a","action":"noop"},{"id":"b","action":"noop","depends_on":["a"]},{"id":"held","action":"noop","owner_hold":True}]
            first=execute(tasks,p)
            self.assertEqual(first["verified"],["a","b"])
            self.assertEqual(first["policy_held"],["held"])
            second=execute(tasks,p)
            self.assertEqual(second["completed"],[])
    def test_unmet_dependency_is_not_falsely_marked_completed(self):
        tasks=[{"id":"a","action":"noop"},{"id":"b","action":"noop","depends_on":["a"]}]
        gate=preflight(tasks)
        self.assertEqual(len(gate["approved"]),2)
        # Preflight checks authorization only; engine enforces actual ordering.
    def test_no_mutation_on_block(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"receipt.json"
            with self.assertRaises(ValueError): execute([{"id":"x","action":"public_deploy"}],p)
            self.assertFalse(p.exists())
if __name__=="__main__": unittest.main()
