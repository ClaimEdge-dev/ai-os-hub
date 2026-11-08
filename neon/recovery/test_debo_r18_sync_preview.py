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

    def test_rentals_id_hold_after_state_drift(self):
        row = {**BASE, 'work_id':'WORK-RENTALS-001', 'state':'READY',
               'assignee_role':'Proof', 'pillar':'SYSTEMS'}
        approval = {'mappings':{'READY':{'raw_state':'READY',
                     'status':'In Progress', 'approved_by':'Owner',
                     'approved_at':'2026-11-08T03:00:00-06:00'}}}
        self.assertEqual(plan([row], approval)['rows'][0]['decision'], 'HOLD_OWNER')

    def test_rentals_id_never_accepted(self):
        row = {**BASE, 'work_id':'WORK-RENTALS-001', 'state':'READY',
               'assignee_role':'Proof', 'pillar':'SYSTEMS'}
        approval = {'mappings':{'READY':{'raw_state':'READY',
                     'status':'In Progress', 'approved_by':'Owner',
                     'approved_at':'2026-11-08T03:00:00-06:00'}}}
        self.assertEqual(plan([row], approval)['decisions'].get('ACCEPT', 0), 0)

    def test_rentals_id_hold_without_parked_wording(self):
        row = {**BASE, 'work_id':'WORK-RENTALS-001', 'state':'IN PROGRESS'}
        self.assertEqual(plan([row])['decisions']['HOLD_OWNER'], 1)

    def test_other_id_can_accept_reviewed_ready_state(self):
        row = {**BASE, 'work_id':'WORK-TEST-001', 'state':'READY',
               'assignee_role':'Proof', 'pillar':'SYSTEMS'}
        approval = {'mappings':{'READY':{'raw_state':'READY',
                     'status':'In Progress', 'approved_by':'Owner',
                     'approved_at':'2026-11-08T03:00:00-06:00'}}}
        self.assertEqual(plan([row], approval)['decisions']['ACCEPT'], 1)


if __name__=='__main__': unittest.main()
