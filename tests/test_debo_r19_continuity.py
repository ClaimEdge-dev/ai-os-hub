import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "tools" / "debo_r19_continuity.py"
spec = importlib.util.spec_from_file_location('r19', MODULE)
r19 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r19)

class ContinuityTests(unittest.TestCase):
    def make(self, **changes):
        a = r19.new_capsule('DEBO','DEBO-MASTER-025','Verify thread continuity','PROPOSED','R19-CANDIDATE','Test fresh-thread recovery')
        a.update(changes)
        return a

    def test_stable_case_and_whitespace(self):
        self.assertEqual(r19.stable_task_id('debo', '  Check    Rules'),r19.stable_task_id('DEBO','check rules'))
    def test_project_isolation(self):
        self.assertNotEqual(r19.stable_task_id('JCT','check staff'),r19.stable_task_id('RRR','check staff'))
    def test_source_key_across_threads(self):
        self.assertEqual(r19.stable_task_id('DEBO','new title','task-15'),r19.stable_task_id('DEBO','other title','task-15'))
    def test_different_source_key(self):
        self.assertNotEqual(r19.stable_task_id('DEBO','new title','task-15'),r19.stable_task_id('DEBO','new title','task-16'))
    def test_invalid_project(self):
        with self.assertRaises(ValueError): r19.stable_task_id('','task')
    def test_invalid_objective(self):
        with self.assertRaises(ValueError): r19.stable_task_id('DEBO','')
    def test_proposed_without_proof(self):
        self.assertEqual('PROPOSED',r19.validate_capsule(self.make())['status'])
    def test_tested_requires_proof(self):
        with self.assertRaisesRegex(ValueError,'test_receipt'): r19.validate_capsule(self.make(status='TESTED'))
    def test_live_requires_probe(self):
        with self.assertRaisesRegex(ValueError,'runtime_probe'): r19.validate_capsule(self.make(status='LIVE'))
    def test_approved_requires_owner(self):
        with self.assertRaisesRegex(ValueError,'owner_approval'): r19.validate_capsule(self.make(status='APPROVED'))
    def test_valid_test_receipt(self):
        self.assertEqual('TESTED',r19.validate_capsule(self.make(status='TESTED',evidence=[{'type':'test_receipt','ref':'local:test-log'}]))['status'])
    def test_no_private_public(self):
        with self.assertRaises(ValueError): r19.validate_capsule(self.make(scope='public_metadata',private_data=True))
    def test_unknown_status(self):
        with self.assertRaises(ValueError): r19.validate_capsule(self.make(status='FINISHED_UNVERIFIED'))
    def test_invalid_evidence(self):
        with self.assertRaises(ValueError): r19.validate_capsule(self.make(evidence=[{'type':'unknown','ref':'x'}]))
    def test_atomic_readback(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'checkpoint.json'; result=r19.atomic_write_readback(p,self.make())
            self.assertEqual('PASS',result['readback'])
            self.assertEqual(self.make().keys(),json.loads(p.read_text()).keys())
    def test_repeated_atomic_write_no_byte_drift(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'checkpoint.json'; capsule=self.make()
            self.assertEqual(r19.atomic_write_readback(p,capsule)['sha256'],r19.atomic_write_readback(p,capsule)['sha256'])
    def test_failed_path_no_corrupt_prior_file(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'checkpoint.json'; original=self.make()
            r19.atomic_write_readback(p,original)
            with self.assertRaises(ValueError): r19.atomic_write_readback(p,self.make(status='LIVE'))
            self.assertEqual(original,json.loads(p.read_text()))
    def test_refuse_different_checkpoint_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'checkpoint.json'
            r19.atomic_write_readback(p, self.make())
            with self.assertRaises(FileExistsError):
                r19.atomic_write_readback(p, self.make(objective='Different objective'))
            self.assertEqual('Verify thread continuity', json.loads(p.read_text())['objective'])
    def test_refuse_symlink_destination(self):
        with tempfile.TemporaryDirectory() as d:
            real = Path(d) / 'original.json'
            real.write_text('preserve')
            link = Path(d) / 'link.json'
            link.symlink_to(real)
            with self.assertRaisesRegex(ValueError, 'symlink'):
                r19.atomic_write_readback(link, self.make())
            self.assertEqual('preserve', real.read_text())
    def test_event_stable_dedupe(self):
        c=self.make(status='TESTED',evidence=[{'type':'test_receipt','ref':'local:test-log'}])
        self.assertEqual(r19.prepare_event('TASK_VERIFIED',c,'rev-1')['event_id'],r19.prepare_event('TASK_VERIFIED',c,'rev-1')['event_id'])
    def test_unverified_complete_rejected(self):
        with self.assertRaises(ValueError): r19.prepare_event('TASK_VERIFIED',self.make(),'rev-1')
    def test_source_revision_affects_event_identity(self):
        c=self.make(status='TESTED',evidence=[{'type':'test_receipt','ref':'local:test-log'}])
        self.assertNotEqual(r19.prepare_event('TASK_VERIFIED',c,'rev-1')['event_id'],r19.prepare_event('TASK_VERIFIED',c,'rev-2')['event_id'])

if __name__=='__main__':unittest.main()
