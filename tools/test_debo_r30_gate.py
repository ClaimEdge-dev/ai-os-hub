import unittest
from debo_r30_gate import assess
def sample():
 return dict(source_ids=["WORK-RENTALS-001","WORK-T-001"],approved_mappings=["WORK-T-001"],owner_hold_ids=["WORK-RENTALS-001"],required_fields_verified=True,isolation_approved=True,schema_approved=True,sync_receipts_installed=True,authenticated_sync_verified=True,core_readbacks_match=True,dashboard_live_readback=True,mobile_qa_passed=True,release_approved=True)
class TestGate(unittest.TestCase):
 def test_all(self):self.assertTrue(assess(sample())["ready_for_live"])
 def test_mapping(self):
  x=sample();x["approved_mappings"]=[]
  self.assertIn("mapping_approval",assess(x)["blockers"])
 def test_hold(self):
  x=sample();x["owner_hold_ids"]=[]
  with self.assertRaises(ValueError):assess(x)
 def test_duplicate(self):
  x=sample();x["source_ids"].append("WORK-T-001")
  with self.assertRaises(ValueError):assess(x)
 def test_missing(self):
  x=sample();del x["release_approved"]
  with self.assertRaises(ValueError):assess(x)
 def test_schema(self):
  x=sample();x["schema_approved"]=False
  self.assertFalse(assess(x)["ready_for_live"])
 def test_sync(self):
  x=sample();x["authenticated_sync_verified"]=False
  self.assertFalse(assess(x)["ready_for_live"])
 def test_mobile(self):
  x=sample();x["mobile_qa_passed"]=False
  self.assertFalse(assess(x)["ready_for_live"])
 def test_release(self):
  x=sample();x["release_approved"]=False
  self.assertFalse(assess(x)["ready_for_live"])
 def test_unknown_hold(self):
  x=sample();x["owner_hold_ids"].append("MISSING")
  with self.assertRaises(ValueError):assess(x)
