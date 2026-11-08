import unittest
from debo_r29_neon_adapter import store_capsule,get_capsule,upsert_thread_index
from debo_r26_capsule_validator import fingerprint
class Cursor:
 def __init__(self,db):self.db=db;self.row=None
 def __enter__(self):return self
 def __exit__(self,*a):return False
 def execute(self,sql,args):
  self.db.queries.append((sql,args))
  if sql.startswith('INSERT INTO claimedge_os.debo_resume_capsules'):
   if self.db.capsule is not None:self.row=None
   else:
    import json
    self.db.capsule=json.loads(args[2]);self.db.sha=args[3];self.db.revision=1;self.row=(1,)
  elif sql.startswith('UPDATE claimedge_os.debo_resume_capsules'):
   if self.db.revision!=args[4]:self.row=None
   else:
    import json
    self.db.capsule=json.loads(args[0]);self.db.sha=args[1];self.db.revision+=1;self.row=(self.db.revision,)
  elif 'FROM claimedge_os.debo_resume_capsules' in sql:
   self.row=(self.db.capsule,self.db.sha,self.db.revision) if sql.startswith('SELECT capsule') and self.db.capsule else ((self.db.capsule['mission_id'],self.db.capsule,self.db.sha,self.db.revision) if self.db.capsule else None)
  elif sql.startswith('INSERT INTO claimedge_os.debo_thread_index'):self.db.index=(args[1],args[4]);self.row=None
  elif 'FROM claimedge_os.debo_thread_index' in sql:self.row=self.db.index
 def fetchone(self):return self.row
class DB:
 def __init__(self):self.queries=[];self.capsule=None;self.sha=None;self.revision=0;self.index=None
 def cursor(self):return Cursor(self)
def sample():
 return dict(schema_version='1.0',mission_id='DEBO-MASTER-026',project_id='DEBO',canonical_sources=[],thread_index_refs=[],objective='R29',completed=[],active_tasks=[],decisions=[],owner_holds=['WORK-RENTALS-001'],blockers=[],next_action='Review',last_verified_at='2026-11-08T05:00:00-06:00',source_fingerprint='a'*64,checkpoint_location='neon:isolated',save_readback_status='UNVERIFIED')
class AdapterTests(unittest.TestCase):
 def test_write_readback(self):
  db=DB();self.assertEqual(store_capsule(db,sample())['revision'],1);self.assertEqual(get_capsule(db,'DEBO')['revision'],1)
 def test_duplicate_rejected(self):
  db=DB();store_capsule(db,sample())
  with self.assertRaisesRegex(ValueError,'revision conflict'):store_capsule(db,sample())
 def test_cas_update(self):
  db=DB();store_capsule(db,sample());c=sample();c['next_action']='New';self.assertEqual(store_capsule(db,c,1)['revision'],2)
 def test_stale_revision(self):
  db=DB();store_capsule(db,sample())
  with self.assertRaisesRegex(ValueError,'revision conflict'):store_capsule(db,sample(),3)
 def test_index(self):
  db=DB();c=sample();store_capsule(db,c);self.assertTrue(upsert_thread_index(db,'thread-1',c,fingerprint(c),'R29')['transaction_readback_verified'])
 def test_index_bad_fingerprint(self):
  with self.assertRaisesRegex(ValueError,'fingerprint mismatch'):upsert_thread_index(DB(),'thread-1',sample(),'a'*64,'R29')
 def test_parameterized(self):
  db=DB();store_capsule(db,sample());self.assertTrue(all('%s' in sql for sql,args in db.queries))
 def test_no_commit_claim(self):
  db=DB();self.assertFalse(store_capsule(db,sample())['committed'])
if __name__=='__main__':unittest.main()
