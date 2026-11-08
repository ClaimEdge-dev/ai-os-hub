import hashlib, json, tempfile, unittest
from pathlib import Path
from engine import run, validate
from runner import plan, digest
class EngineTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name); self.receipt=self.root/'receipt.json'
    def test_dependency(self): self.assertEqual(run([{'id':'A'},{'id':'B','depends_on':['A']}],self.receipt)['completed'],['A','B'])
    def test_resume(self):
        run([{'id':'A'}],self.receipt)
        self.assertEqual(run([{'id':'A'}],self.receipt)['completed'],[])
    def test_hold(self): self.assertEqual(run([{'id':'WORK-RENTALS-001','owner_hold':True}],self.receipt)['held'],['WORK-RENTALS-001'])
    def test_approval(self): self.assertEqual(run([{'id':'A','approval_required':True}],self.receipt)['completed'],[])
    def test_cycle(self):
        with self.assertRaisesRegex(ValueError,'cycle'): validate([{'id':'A','depends_on':['B']},{'id':'B','depends_on':['A']}])
    def test_unapproved(self):
        with self.assertRaisesRegex(ValueError,'unapproved'): run([{'id':'A','action':'shell'}],self.receipt)
    def test_hash_ok(self):
        p=self.root/'x';p.write_text('safe')
        self.assertEqual(run([{'id':'A','action':'verify_text','path':str(p),'sha256':hashlib.sha256(b'safe').hexdigest()}],self.receipt)['completed'],['A'])
    def test_hash_bad(self):
        p=self.root/'x';p.write_text('bad')
        self.assertEqual(run([{'id':'A','action':'verify_text','path':str(p),'sha256':'0'*64}],self.receipt)['completed'],[])
    def test_failed_dependency(self): self.assertEqual(run([{'id':'A','action':'verify_text','path':'/missing/debo/r20','sha256':'0'*64},{'id':'B','depends_on':['A']}],self.receipt)['pending'],['A','B'])
    def test_receipt(self):
        run([{'id':'A'}],self.receipt)
        self.assertEqual(json.loads(self.receipt.read_text())['events'][0]['id'],'A')
    def test_parallel(self): self.assertEqual(len(run([{'id':str(i)} for i in range(6)],self.receipt,workers=3)['completed']),6)
    def test_limit(self):
        with self.assertRaises(ValueError): run([{'id':'A'}],self.receipt,workers=100)
    def test_failed_task_not_retried_across_batches(self):
        tasks=[{'id':'A'},{'id':'B','action':'verify_text','path':'/missing/debo/r20','sha256':'0'*64},{'id':'C','depends_on':['A']}]
        result=run(tasks,self.receipt,attempts=2)
        self.assertEqual(result['completed'],['A','C'])
        events=json.loads(self.receipt.read_text())['events']
        self.assertEqual([e['id'] for e in events].count('B'),1)
        self.assertEqual(next(e for e in events if e['id']=='B')['result']['attempts'],2)
    def test_duplicate(self):
        with self.assertRaises(ValueError): plan([{'id':'A'},{'id':'A'}],{})
    def test_unknown_dependency(self):
        with self.assertRaises(ValueError): plan([{'id':'A','depends_on':['Z']}],{})
    def test_skip_verified(self): self.assertEqual(plan([{'id':'A'}],{'A':digest({'id':'A'})})[0],[])
    def test_plan_approval(self): self.assertEqual(plan([{'id':'A','approval_required':True}],{})[0],[])
    def test_plan_hold(self): self.assertEqual(plan([{'id':'A','owner_hold':True}],{})[0],[])
    def test_plan_dependency(self): self.assertEqual(plan([{'id':'A'},{'id':'B','depends_on':['A']}],{})[0],[{'id':'A'}])
if __name__=='__main__': unittest.main()
