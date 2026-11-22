"""Synthetic-only offline tests for R19 recovery guard."""
import json
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from debo_r19_continuity import new_capsule
from debo_r19_continuity_guard import build_plan

NOW = datetime(2026, 11, 22, 20, 0, tzinfo=timezone.utc)


def example(project='DEBO', status='BUILT', when='2026-11-22T19:00:00+00:00'):
    c = new_capsule(project, 'SYNTHETIC-ONE', 'Synthetic test only', status,
                    'No customer data', 'Use approved source')
    c['as_of_utc'] = when
    return c


class GuardTests(unittest.TestCase):
    def test_plan_contains_no_raw_checkpoint_or_objective(self):
        c = example()
        c['checkpoint'] = 'PRIVATE_ONLY_8765'
        c['objective'] = 'SYNTHETIC_SECRET_1234'
        plan = build_plan([c], now=NOW)
        blob = json.dumps(plan)
        self.assertNotIn('PRIVATE_ONLY_8765', blob)
        self.assertNotIn('SYNTHETIC_SECRET_1234', blob)
        self.assertEqual(plan['writes'], 0)
        self.assertFalse(plan['cortex']['external_write_permitted'])
        self.assertFalse(plan['cost']['paid_calls_allowed'])

    def test_exact_duplicate_suppression(self):
        c = example()
        x = build_plan([c, c.copy()], now=NOW)
        self.assertEqual(x['dedupe']['exact_duplicates'], 1)
        self.assertEqual(x['dedupe']['unique_count'], 1)

    def test_cross_project_refused(self):
        with self.assertRaisesRegex(ValueError, 'cross-project'):
            build_plan([example('DEBO'), example('JCT')], now=NOW)

    def test_cross_task_refused(self):
        a, b = example(), example()
        b['task_id'] = 'OTHER-TASK-001'
        with self.assertRaisesRegex(ValueError, 'cross-project or cross-task'):
            build_plan([a, b], now=NOW)

    def test_same_revision_conflict_holds(self):
        a, b = example(), example()
        a['source_revision'] = b['source_revision'] = 'same-revision'
        b['checkpoint'] = 'Different synthetic checkpoint'
        x = build_plan([a, b], now=NOW)
        self.assertTrue(x['conflicts']['detected'])
        self.assertEqual(x['resume']['decision'], 'HOLD_CONFLICT')

    def test_old_report_needs_recheck(self):
        x = build_plan([example(when='2026-10-01T19:00:00Z')], now=NOW)
        self.assertEqual(x['resume']['freshness'], 'REVERIFY')

    def test_missing_time_keeps_unknown(self):
        c = example(); c.pop('as_of_utc')
        x = build_plan([c], now=NOW)
        self.assertEqual(x['resume']['freshness'], 'UNKNOWN')

    def test_no_cross_ai_claim_or_auto_checkpoint(self):
        x = build_plan([example()], now=NOW)
        self.assertEqual(x['cortex']['second_client_continuity'], 'NOT_VERIFIED')
        self.assertEqual(x['checkpoint']['automatic_runtime_runner'], 'NOT_CONFIGURED')
        self.assertFalse(x['dashboard']['private_task_data'])

    def test_custom_identifiers_are_pseudonymized(self):
        c = example('PRIVATE_PROJ_NAME_9876')
        c['task_id'] = 'SECRET_TASK_REFERENCE_9876'
        out = build_plan([c], now=NOW)
        blob = json.dumps(out)
        self.assertNotIn('PRIVATE_PROJ_NAME_9876', blob)
        self.assertNotIn('SECRET_TASK_REFERENCE_9876', blob)
        self.assertTrue(out['project_id'].startswith('SCOPE-'))
        self.assertTrue(out['task_id'].startswith('DEBO-TASK-'))

    def test_invalid_proof_fails_closed(self):
        c = example(); c['status'] = 'TESTED'; c['evidence'] = []
        with self.assertRaisesRegex(ValueError, 'requires test_receipt'):
            build_plan([c], now=NOW)


if __name__ == '__main__':
    unittest.main()
