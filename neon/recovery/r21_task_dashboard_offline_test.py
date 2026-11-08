"""R21 safe offline source-ID and dashboard-receipt acceptance. No network or database writes."""
import json
from pathlib import Path
import tempfile
import unittest

IDS = ('WORK-DEBO-001','WORK-JCT-001','WORK-CE-001','WORK-DWING-001','WORK-SETTLE-001','WORK-PLOG-001','WORK-RRR-001','WORK-MOL-001','WORK-BBS-001','WORK-WRESTLE-001','WORK-ATHLETE-001','WORK-BASEBALL-001','WORK-RENTALS-001','WORK-NEON-001','WORK-TPB-001')
ALLOWED = {'Backlog','In Progress','Blocked','Review','Done'}

def reconcile(ids, approved=None):
    approved=approved or {}
    if len(ids)!=len(set(ids)):
        raise ValueError('duplicate task IDs')
    if set(ids)!=set(IDS):
        raise ValueError('source IDs do not match recovered Work Stack')
    return [{'task_id':i,'decision':('HOLD_OWNER' if i=='WORK-RENTALS-001' else 'QUARANTINE' if i not in approved else 'ACCEPT'),'status':approved.get(i) if i!='WORK-RENTALS-001' else None} for i in ids]

def validate_receipt(receipt):
    if receipt.get('mode')!='READ_ONLY_NONPRODUCTION' or receipt.get('production_writes') is not False:
        raise ValueError('unsafe dashboard receipt')
    if receipt.get('execution_receipts_connected') is not False:
        raise ValueError('cannot claim live receipt connection')
    if receipt.get('ci_conclusion') not in {'success','failure','cancelled','skipped'}:
        raise ValueError('unknown CI conclusion')
    return {'run':receipt['run_number'],'ci':receipt['ci_conclusion'],'live_sync':False}

class Acceptance(unittest.TestCase):
    def test_source_identity(self): self.assertEqual(len(set(IDS)),15)
    def test_reconcile_quarantine(self):
        rows=reconcile(IDS)
        self.assertEqual(sum(r['decision']=='QUARANTINE' for r in rows),14)
        self.assertEqual(sum(r['decision']=='HOLD_OWNER' for r in rows),1)
    def test_hold_cannot_be_overridden(self):
        rows=reconcile(IDS,{'WORK-RENTALS-001':'In Progress'})
        self.assertEqual(next(r for r in rows if r['task_id']=='WORK-RENTALS-001')['decision'],'HOLD_OWNER')
    def test_duplicates_rejected(self):
        with self.assertRaises(ValueError): reconcile(IDS+(IDS[0],))
    def test_missing_id_rejected(self):
        with self.assertRaises(ValueError): reconcile(IDS[:-1])
    def test_receipt(self):
        receipt={'mode':'READ_ONLY_NONPRODUCTION','production_writes':False,'execution_receipts_connected':False,'ci_conclusion':'success','run_number':4}
        self.assertEqual(validate_receipt(receipt),{'run':4,'ci':'success','live_sync':False})
        receipt['execution_receipts_connected']=True
        with self.assertRaises(ValueError):validate_receipt(receipt)
    def test_offline_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'dryrun.json'
            p.write_text(json.dumps(reconcile(IDS)))
            self.assertEqual(len(json.loads(p.read_text())),15)

if __name__=='__main__':unittest.main()
