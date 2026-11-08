import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from r21_receipt_adapter import build_card,from_file

RECEIPT=Path(__file__).resolve().parent/'R21_R20_EXECUTION_RECEIPTS_v1.json'

class AdapterTests(unittest.TestCase):
    def test_real_receipt(self):
        card=from_file(RECEIPT)
        self.assertGreaterEqual(card['run_number'],1)
        self.assertEqual(card['ci_conclusion'],'success')
        self.assertEqual(card['live_task_sync'],'NOT_CONNECTED')
        self.assertEqual(card['real_task_imports'],0)
    def test_hold_enforced(self):
        d=json.loads(RECEIPT.read_text());d['owner_holds']=[]
        with self.assertRaises(ValueError):build_card(d)
    def test_no_false_live_claim(self):
        d=json.loads(RECEIPT.read_text());d['execution_receipts_connected']=True
        with self.assertRaises(ValueError):build_card(d)
    def test_no_import_claim(self):
        d=json.loads(RECEIPT.read_text());d['real_task_imports']=1
        with self.assertRaises(ValueError):build_card(d)
    def test_no_production_writes(self):
        d=json.loads(RECEIPT.read_text());d['production_writes']=True
        with self.assertRaises(ValueError):build_card(d)

if __name__=='__main__':unittest.main()
