#!/usr/bin/env python3
"""DEBO R9 cross-AI handoff contract regression checks; synthetic fixtures only."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
VALIDATOR = HERE / 'validate_handoff.py'
if not VALIDATOR.exists():
    VALIDATOR = REPO / 'tools' / 'validate_debo_handoff.py'
SCHEMA = HERE / 'DEBO_HANDOFF_SCHEMA.json'
if not SCHEMA.exists():
    SCHEMA = REPO / 'prompts' / 'DEBO_HANDOFF_SCHEMA.json'
EXAMPLE = HERE / 'DEBO_HANDOFF_EXAMPLE.json'
if not EXAMPLE.exists():
    EXAMPLE = REPO / 'prompts' / 'DEBO_HANDOFF_EXAMPLE.json'
SPEC = importlib.util.spec_from_file_location('debo_validator', VALIDATOR)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class HandoffPacketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = json.loads(EXAMPLE.read_text('utf-8'))

    def check_fails(self, edit):
        packet = copy.deepcopy(self.base)
        edit(packet)
        with self.assertRaises((ValueError, KeyError, TypeError)):
            MOD.validate_minimal(packet)

    def test_valid_synthetic_packet(self):
        MOD.validate_minimal(self.base)
        try:
            import jsonschema
        except ImportError:
            self.skipTest('optional jsonschema package unavailable')
        schema = json.loads(SCHEMA.read_text('utf-8'))
        jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(self.base)

    def test_unknown_project_rejected(self):
        self.check_fails(lambda packet: packet.update(project_id='OTHER'))

    def test_unverified_checkpoint_cannot_claim_deployed(self):
        self.check_fails(lambda packet: packet.update(status='DEPLOYED'))

    def test_duplicate_candidate_rejected(self):
        self.check_fails(lambda packet: packet['candidates'].append(copy.deepcopy(packet['candidates'][0])))

    def test_zero_score_rejected(self):
        self.check_fails(lambda packet: packet['candidates'][0]['scores'].update(risk=0))

    def test_deployed_requires_auth_proof(self):
        def mutate(packet):
            packet.update(status='DEPLOYED')
            packet['source_checkpoint'].update(access_status='READ_VERIFIED')
        self.check_fails(mutate)


if __name__ == '__main__':
    unittest.main()