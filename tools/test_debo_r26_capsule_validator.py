import copy
import unittest
from debo_r26_capsule_validator import fingerprint,validate

def sample():
    return dict(schema_version='1.0',mission_id='DEBO-MASTER-026',project_id='DEBO',canonical_sources=['DEBO_BOOTSTRAP.md'],thread_index_refs=[],objective='Continuity acceptance',completed=[],active_tasks=[dict(task_id='WORK-DEBO-001',state='TESTED')],decisions=[],owner_holds=['WORK-RENTALS-001'],blockers=[],next_action='Verify checkpoint',last_verified_at='2026-11-08T04:00:00-06:00',source_fingerprint='a'*64,checkpoint_location='github:dev/test',save_readback_status='UNVERIFIED')
class CapsuleTests(unittest.TestCase):
 def test_valid(self):self.assertTrue(validate(sample())['valid'])
 def test_deterministic_hash(self):self.assertEqual(fingerprint({'b':2,'a':1}),fingerprint({'a':1,'b':2}))
 def test_changed_hash(self):self.assertNotEqual(fingerprint({'a':1}),fingerprint({'a':2}))
 def test_missing_field(self):
  c=sample();del c['project_id']
  with self.assertRaisesRegex(ValueError,'missing'):validate(c)
 def test_duplicate(self):
  c=sample();c['active_tasks'].append(copy.deepcopy(c['active_tasks'][0]))
  with self.assertRaisesRegex(ValueError,'duplicate'):validate(c)
 def test_false_live(self):
  c=sample();c['active_tasks'][0]['state']='LIVE'
  with self.assertRaisesRegex(ValueError,'false live'):validate(c)
 def test_live_receipt(self):
  c=sample();c['active_tasks'][0].update(state='LIVE',live_receipt='verified:fixture')
  self.assertTrue(validate(c)['valid'])
 def test_owner_hold(self):
  c=sample();c['active_tasks'][0].update(task_id='WORK-RENTALS-001',state='INSTALLED')
  with self.assertRaisesRegex(ValueError,'owner hold'):validate(c)
 def test_secret(self):
  c=sample();c['objective']='password=example-secret'
  with self.assertRaisesRegex(ValueError,'secret'):validate(c)
 def test_bad_fingerprint(self):
  c=sample();c['source_fingerprint']='bad'
  with self.assertRaisesRegex(ValueError,'fingerprint'):validate(c)
 def test_bad_readback(self):
  c=sample();c['save_readback_status']='LIVE'
  with self.assertRaisesRegex(ValueError,'readback'):validate(c)
if __name__=='__main__':unittest.main()
