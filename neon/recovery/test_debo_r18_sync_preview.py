import unittest
from debo_r18_sync_preview import plan, row_hash

BASE = dict(work_id='WORK-T-001', project_id='DEMO', project_name='Synthetic', objective='Test only', state='REVIEW / SOURCE', priority='P2', owner='Test')
APP = {'mappings': {BASE['state']: dict(raw_state=BASE['state'], status='Review', approved_by='Owner', approved_at='2026-11-08T03:00:00-06:00')}}

class SyncPreviewTests(unittest.TestCase):
    def test_quarantine(self): self.assertEqual(plan([BASE])['decisions']['QUARANTINE'],1)
    def test_owner_hold(self): self.assertEqual(plan([{**BASE,'state':'PARKED BY OWNER'}])['decisions']['HOLD_OWNER'],1)
    def test_hold_overrides_mapping(self):
        a={'mappings':{'PARKED BY OWNER':dict(raw_state='PARKED BY OWNER',status='Done',approved_by='Owner',approved_at='2026-11-08')}}
        self.assertEqual(plan([{**BASE,'state':'PARKED BY OWNER'}],a)['decisions']['HOLD_OWNER'],1)
    def test_duplicate(self):
        with self.assertRaisesRegex(ValueError,'Duplicate'): plan([BASE,BASE])
    def test_missing_id(self):
        with self.assertRaisesRegex(ValueError,'Missing work_id'): plan([{**BASE,'work_id':''}])
    def test_invalid_priority(self): self.assertEqual(plan([{**BASE,'priority':'P9'}])['decisions']['REJECT_REQUIRED_FIELDS'],1)
    def test_unreviewed_mapping(self):
        self.assertEqual(plan([BASE],{'mappings':{BASE['state']:{'status':'Review'}}})['decisions']['QUARANTINE'],1)
    def test_target_fields_required(self): self.assertEqual(plan([BASE],APP)['decisions']['REVIEW_FIELD_MAPPING'],1)
    def test_accepted_only_if_fields_and_reviewed(self):
        self.assertEqual(plan([{**BASE,'assignee_role':'Proof','pillar':'DEBO'}],APP)['decisions']['ACCEPT'],1)
    def test_preservation(self):
        x=plan([BASE])['rows'][0]
        self.assertEqual(x['raw_source_state'],BASE['state'])
        self.assertEqual(x['source_row_hash'],row_hash(BASE))
    def test_no_write(self): self.assertFalse(plan([BASE],APP)['write_eligible'])
    def test_determinism(self): self.assertEqual(plan([BASE]),plan([{**BASE}]))

if __name__=='__main__': unittest.main()
