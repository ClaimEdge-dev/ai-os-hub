import importlib.util
import json
import unittest
from pathlib import Path

MODULE=Path(__file__).resolve().parents[1]/"tools"/"debo_library_duplicate_review.py"
spec=importlib.util.spec_from_file_location("library_review",MODULE)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
SAMPLE=Path(__file__).resolve().parents[1]

def fixture():
    r1={"duplicate_validation":{"families":[{"family_id":"LIB001-EXACT-001","copies":2,"source_file_ids":["file_a","file_b"],"materialized_names":["f.zip","f(1).zip"],"source_paths":["/f.zip","/f(1).zip"],"sha256":"a"*64,"bytes_each":10,"potential_excess_bytes":10}]}}
    r2={"exact_hash_families_new":[{"family_id":"LIB001-EXACT-005","copies":2,"file_ids":["file_c","file_d"],"source_names":["p.zip","p(1).zip"],"source_scope":"ChatGPT Library root only","sha256":"b"*64,"bytes_each":12,"potential_excess_bytes":12}],"cumulative_with_r1":{"confirmed_excess_copy_count":2}}
    r3={"duplicate_reference_checks":{"additional_verified_family":{"family_id":"LIB001-EXACT-012","copies":2,"source_file_ids":["file_e","file_f"],"source_names":["s.skill","s(1).skill"],"sha256":"c"*64,"bytes_each":5,"potential_excess_bytes":5},"cumulative_verified_families":3,"cumulative_potential_extra_copies":3,"cumulative_potential_excess_bytes":27}}
    return r1,r2,r3

class ReviewTests(unittest.TestCase):
    def test_counts(self):
        self.assertEqual((3,3,27),tuple(m.review(*fixture())[k] for k in ('historical_exact_hash_families','historical_potential_extra_copies','historical_potential_excess_bytes')))
    def test_no_delete(self):self.assertEqual(m.review(*fixture())['mode'],'READ_ONLY_NO_MUTATION')
    def test_invalid_hash(self):
        a,b,c=fixture();a['duplicate_validation']['families'][0]['sha256']='hi'
        with self.assertRaisesRegex(ValueError,'SHA'):m.review(a,b,c)
    def test_byte_arithmetic(self):
        a,b,c=fixture();b['exact_hash_families_new'][0]['potential_excess_bytes']=13
        with self.assertRaisesRegex(ValueError,'arithmetic'):m.review(a,b,c)
    def test_duplicate_family(self):
        a,b,c=fixture();b['exact_hash_families_new'][0]['family_id']='LIB001-EXACT-001'
        with self.assertRaisesRegex(ValueError,'duplicate family'):m.review(a,b,c)
    def test_source_id_collision(self):
        a,b,c=fixture();b['exact_hash_families_new'][0]['file_ids'][0]='file_a'
        with self.assertRaisesRegex(ValueError,'source ID'):m.review(a,b,c)
    def test_coverage_missing_not_auto_delete(self):
        r=m.review(*fixture(),{'complete_scopes':['/'],'files':[]})
        self.assertEqual(r['inventory']['missing'],4)
        self.assertEqual(r['actual_bytes_freed'],0)
    def test_metadata_match_not_hash(self):
        r=m.review(*fixture(),{'complete_scopes':['/'],'files':[{'file_id':'file_a','name':'f.zip','size_bytes':10}]})
        self.assertEqual(r['inventory']['matches'],1)
        self.assertIn('ONLY',r['families'][0]['current_metadata']['findings'][0])
        self.assertEqual(r['families'][0]['byte_status'],'HISTORICAL_RECEIPT_NOT_REHASHED')
    def test_other_scopes_unverified(self):
        r=m.review(*fixture(),{'complete_scopes':[],'files':[]})
        self.assertEqual(r['inventory']['missing'],0)
        self.assertEqual(r['inventory']['out_of_scope'],6)
    def test_selected_ids_without_false_missing(self):
        files=[{"file_id":"file_a","name":"f.zip","size_bytes":10}]
        r=m.review(*fixture(),{"observed_file_ids":["file_a"],"files":files})
        self.assertEqual(r["inventory"]["matches"],1)
        self.assertEqual(r["inventory"]["missing"],0)
        self.assertEqual(r["inventory"]["out_of_scope"],5)
    def test_selected_id_duplicate_invalid(self):
        with self.assertRaisesRegex(ValueError,"observed_file_ids"):
            m.review(*fixture(),{"observed_file_ids":["file_a","file_a"],"files":[]})
    def test_modified_size(self):
        r=m.review(*fixture(),{'complete_scopes':['/'],'files':[{'file_id':'file_a','name':'f.zip','size_bytes':9}]})
        self.assertEqual(r['inventory']['changed'],1)
    def test_root_inventory_duplicate_id(self):
        a={'file_id':'file_a','name':'f.zip','size_bytes':10}
        with self.assertRaisesRegex(ValueError,'duplicate observed'):m.review(*fixture(),{'complete_scopes':['/'],'files':[a,a]})
    def test_bad_cumulative_totals(self):
        a,b,c=fixture();c['duplicate_reference_checks']['cumulative_potential_excess_bytes']=999
        with self.assertRaisesRegex(ValueError,'cumulative totals'):m.review(a,b,c)
    def test_real_receipt_reconciles(self):
        if not (SAMPLE/"DEBO_MASTER_LIB_001_R1_Inventory_Duplicate_Review_2026-11-10.json").is_file():
            self.skipTest("Private historical receipts are not checked into GitHub")
        r1=json.loads((SAMPLE/'DEBO_MASTER_LIB_001_R1_Inventory_Duplicate_Review_2026-11-10.json').read_text())
        r2=json.loads((SAMPLE/'DEBO_MASTER_LIB_001_R2_Supplemental_Duplicate_Review_2026-11-10.json').read_text())
        r3=json.loads((SAMPLE/'DEBO_MASTER_LIB_001_R3_Folder_and_Reference_Audit_2026-11-10.json').read_text())
        r=m.review(r1,r2,r3)
        self.assertEqual((12,17,126231872),(r['historical_exact_hash_families'],r['historical_potential_extra_copies'],r['historical_potential_excess_bytes']))

if __name__=='__main__':unittest.main()
