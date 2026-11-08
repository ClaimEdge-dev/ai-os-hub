import unittest
from r21_task_flow_acceptance import build_projection

class FlowTests(unittest.TestCase):
    def test_full_offline_projection(self):
        p=build_projection()
        self.assertEqual(p['source_id_count'],15)
        self.assertEqual(p['decision_counts'],{'ACCEPT':0,'QUARANTINE':14,'HOLD_OWNER':1})
        self.assertEqual(p['held_ids'],['WORK-RENTALS-001'])
        self.assertFalse(p['dashboard_live_connected'])
        self.assertEqual(p['database_writes'],0)
        self.assertEqual(p['ci_evidence']['ci_conclusion'],'success')
        self.assertEqual(p['ci_evidence']['live_task_sync'],'NOT_CONNECTED')

if __name__=='__main__':unittest.main()
