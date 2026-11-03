"""Mutation/negative tests for the existing 50 JCT skill pointers."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from debo_agent_coverage_audit import audit  # noqa: E402

DATA = json.loads((ROOT / 'governance/DEBO_AGENT_COVERAGE_REGISTER_v1.json').read_text(encoding='utf8'))


class AgentCoverageIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.root = Path(self.dir.name)
        for s in DATA['jct']['skills']:
            path = self.root / s['source_path']
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('# documented skill\n', encoding='utf8')

    def test_fixture_positive(self):
        r = audit(DATA, self.root)
        self.assertEqual(r['status'], 'PASS', r['errors'])
        self.assertEqual(r['source_files_checked'], 50)

    def test_missing_skill_fails(self):
        (self.root / DATA['jct']['skills'][0]['source_path']).unlink()
        self.assertEqual(audit(DATA, self.root)['status'], 'FAIL')

    def test_wrong_location_fails(self):
        broken = copy.deepcopy(DATA)
        broken['jct']['skills'][0]['source_path'] = 'projects/rrr/skills/other/SKILL.md'
        self.assertEqual(audit(broken, self.root)['status'], 'FAIL')

    def test_path_traversal_fails(self):
        broken = copy.deepcopy(DATA)
        broken['jct']['skills'][0]['source_path'] = '../../etc/passwd'
        self.assertEqual(audit(broken, self.root)['status'], 'FAIL')

    def test_cross_project_agent_fails(self):
        broken = copy.deepcopy(DATA)
        broken['jct']['skills'][0]['lead_role'] = 'DEBO-MACK'
        self.assertEqual(audit(broken, self.root)['status'], 'FAIL')

    def test_false_running_role_fails(self):
        broken = copy.deepcopy(DATA)
        broken['roles'][0]['worker_status'] = 'VERIFIED_RUNNING'
        self.assertEqual(audit(broken, self.root)['status'], 'FAIL')

    def test_missing_approval_gate_fails(self):
        broken = copy.deepcopy(DATA)
        broken['approval_gates'].remove('production_mutation')
        self.assertEqual(audit(broken, self.root)['status'], 'FAIL')

    def test_duplicate_skill_fails(self):
        broken = copy.deepcopy(DATA)
        broken['jct']['skills'][1] = copy.deepcopy(broken['jct']['skills'][0])
        self.assertEqual(audit(broken, self.root)['status'], 'FAIL')

    def test_unverified_runtime_is_not_upgraded(self):
        broken = copy.deepcopy(DATA)
        broken['jct']['skills'][0]['installed_in_chatgpt'] = 'VERIFIED'
        self.assertEqual(audit(broken, self.root)['status'], 'FAIL')

    def test_symlink_escape_fails(self):
        outside = Path(self.dir.name).parent / ('external-' + self.root.name + '.md')
        outside.write_text('outside', encoding='utf8')
        self.addCleanup(outside.unlink, missing_ok=True)
        target = self.root / DATA['jct']['skills'][0]['source_path']
        target.unlink()
        target.symlink_to(outside)
        self.assertEqual(audit(DATA, self.root)['status'], 'FAIL')


if __name__ == '__main__':
    unittest.main()
