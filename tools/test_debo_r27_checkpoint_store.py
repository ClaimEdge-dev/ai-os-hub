import json,tempfile,unittest
from pathlib import Path
from debo_r27_checkpoint_store import save_capsule

def capsule():
 return dict(schema_version='1.0',mission_id='DEBO-MASTER-026',project_id='DEBO',canonical_sources=['DEBO_BOOTSTRAP.md'],thread_index_refs=[],objective='Memory continuity',completed=[],active_tasks=[{'task_id':'WORK-DEBO-001','state':'TESTED'}],decisions=[],owner_holds=['WORK-RENTALS-001'],blockers=[],next_action='Verify CI',last_verified_at='2026-11-08T04:00:00-06:00',source_fingerprint='a'*64,checkpoint_location='local:DEBO',save_readback_status='UNVERIFIED')
class StoreTests(unittest.TestCase):
 def test_write_readback_and_index(self):
  with tempfile.TemporaryDirectory() as d:
   result=save_capsule(d,capsule(),'thread-001','DEBO | R27')
   self.assertTrue(result['readback_verified'])
   self.assertEqual(result['external_sync'],'NOT_CONNECTED')
   self.assertEqual(len(json.loads((Path(d)/'thread_index.json').read_text())['threads']),1)
 def test_idempotent_index(self):
  with tempfile.TemporaryDirectory() as d:
   save_capsule(d,capsule(),'thread-001','DEBO | R27');save_capsule(d,capsule(),'thread-001','DEBO | R27')
   self.assertEqual(len(json.loads((Path(d)/'thread_index.json').read_text())['threads']),1)
 def test_owner_hold_preserved(self):
  with tempfile.TemporaryDirectory() as d:
   save_capsule(d,capsule(),'thread-001','DEBO | R27')
   self.assertIn('WORK-RENTALS-001',json.loads((Path(d)/'capsules/DEBO.json').read_text())['owner_holds'])
 def test_preclaimed_verified_rejected(self):
  c=capsule();c['save_readback_status']='VERIFIED'
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaisesRegex(ValueError,'preclaim'):save_capsule(d,c,'thread-001','DEBO')
 def test_path_traversal_rejected(self):
  c=capsule();c['project_id']='../other'
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaisesRegex(ValueError,'unsafe'):save_capsule(d,c,'thread-001','DEBO')
 def test_conflicting_mission_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   save_capsule(d,capsule(),'thread-001','DEBO');c=capsule();c['mission_id']='OTHER'
   with self.assertRaisesRegex(ValueError,'different mission'):save_capsule(d,c,'thread-001','DEBO')
if __name__=='__main__':unittest.main()
