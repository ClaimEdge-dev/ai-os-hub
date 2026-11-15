"""Rule-based eval harness acceptance: synthetic captures only, no model calls."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'security' / 'r129_promptfoo'
spec = importlib.util.spec_from_file_location('debo_quality_eval', BASE / 'quality_eval.py')
eval_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(eval_mod)
CASES = json.loads((BASE / 'fixtures' / 'quality_cases.json').read_text())
OUTPUTS = json.loads((BASE / 'fixtures' / 'synthetic_outputs.json').read_text())


def changed(index=0, **overrides):
    result = [dict(row) for row in OUTPUTS]
    result[index].update(overrides)
    return result


class QualityEvalAcceptance(unittest.TestCase):
    def test_all_twelve_synthetic_baselines_pass(self):
        result = eval_mod.evaluate_suite(CASES, OUTPUTS)
        self.assertEqual((result['label'], result['passed'], result['total']), ('PASS', 12, 12))
        self.assertEqual(result['evaluation_type'], 'OFFLINE_RULE_BASED_OUTPUT_CLAIMS')
        self.assertEqual(result['model_calls'], 0)

    def test_missing_output_is_not_silently_omitted(self):
        result = eval_mod.evaluate_suite(CASES, OUTPUTS[:-1])
        self.assertEqual(result['total'], 12)
        self.assertEqual(result['passed'], 11)
        self.assertEqual(result['label'], 'FAIL')

    def test_status_truth_mismatch_fails(self):
        result = eval_mod.evaluate_suite(CASES, changed(3, status='LIVE'))
        self.assertIn('status_mismatch', result['cases'][3]['reasons'])

    def test_evidence_requirement_fails_closed(self):
        result = eval_mod.evaluate_suite(CASES, changed(0, evidence_refs=[]))
        self.assertIn('missing_evidence', result['cases'][0]['reasons'])

    def test_example_reference_not_accepted_as_real(self):
        result = eval_mod.evaluate_suite(CASES, changed(0, evidence_refs=['example:fake-document']))
        self.assertIn('example_not_real_evidence', result['cases'][0]['reasons'])

    def test_forbidden_statement_fails(self):
        result = eval_mod.evaluate_suite(CASES, changed(10, answer='Local tests passed and publicly deployed.'))
        self.assertIn('forbidden_term:publicly deployed', result['cases'][10]['reasons'])

    def test_protected_action_requires_external_verification(self):
        result = eval_mod.evaluate_suite(CASES, changed(1, claimed_actions=['public_deploy']))
        reasons = result['cases'][1]['reasons']
        self.assertIn('unapproved_action:public_deploy', reasons)
        self.assertIn('dangerous_action_without_verified_approval:public_deploy', reasons)

    def test_secret_like_material_is_rejected(self):
        result = eval_mod.evaluate_suite(CASES, changed(0, answer='Reuse skill with OPENAI_API_KEY=abc123456789example'))
        self.assertIn('secret_like_material', result['cases'][0]['reasons'])

    def test_duplicate_case_identifiers_rejected(self):
        with self.assertRaisesRegex(ValueError, 'duplicate case IDs'):
            eval_mod.evaluate_suite(CASES + [CASES[0]], OUTPUTS)

    def test_duplicate_output_identifiers_rejected(self):
        with self.assertRaisesRegex(ValueError, 'duplicate output case IDs'):
            eval_mod.evaluate_suite(CASES, OUTPUTS + [OUTPUTS[0]])

    def test_unrecognized_output_not_silently_ignored(self):
        with self.assertRaisesRegex(ValueError, 'unknown output case IDs'):
            eval_mod.evaluate_suite(CASES, OUTPUTS + [{'case_id':'F-999'}])

    def test_empty_suite_never_reports_pass(self):
        self.assertEqual(eval_mod.evaluate_suite([], [])['label'], 'FAIL')

    def test_bad_evidence_type_is_a_failure(self):
        result = eval_mod.evaluate_suite(CASES, changed(0, evidence_refs='some string'))
        self.assertIn('invalid_evidence_refs', result['cases'][0]['reasons'])

    def test_invalid_status_is_failure(self):
        result = eval_mod.evaluate_suite(CASES, changed(0, status='GREAT'))
        self.assertIn('invalid_status', result['cases'][0]['reasons'])

    def test_rule_based_eval_does_not_load_credentials_or_model_sdk(self):
        source = (BASE / 'quality_eval.py').read_text()
        self.assertNotIn('import openai', source)
        self.assertNotIn('requests.', source)
        self.assertNotIn('httpx.', source)


if __name__ == '__main__':
    unittest.main()
