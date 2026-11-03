"""Exercise bootstrap integrity against isolated copies; never mutate checkout."""
import importlib.util
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('bootstrap', ROOT / 'tools/debo_bootstrap_check.py')
bootstrap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bootstrap)

class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name in bootstrap.REQUIRED + ['tools/debo_bootstrap_check.py']:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)

    def run_check(self):
        proc = subprocess.run([sys.executable, str(self.root / 'tools/debo_bootstrap_check.py')], capture_output=True, text=True)
        return proc.returncode, json.loads(proc.stdout)

    def test_valid_checkout(self):
        code, data = self.run_check()
        self.assertEqual(code, 0)
        self.assertEqual(data['result'], 'PASS')
        self.assertEqual(data['profiles'], 13)

    def test_each_missing_required_file_fails(self):
        for name in bootstrap.REQUIRED:
            with self.subTest(path=name):
                target = self.root / name
                saved = target.read_bytes()
                target.unlink()
                code, data = self.run_check()
                target.write_bytes(saved)
                self.assertEqual(code, 1)
                self.assertIn('Missing: ' + name, data['errors'])

    def test_empty_profile_fails(self):
        name = 'governance/sister-brains/JCT_PROFILE_v1.md'
        (self.root / name).write_text('\n')
        code, data = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn('Empty: ' + name, data['errors'])

    def test_broken_inheritance_fails(self):
        path = self.root / 'governance/DEBO_RUNTIME_BOOTSTRAP_v2.md'
        path.write_text(path.read_text().replace('DEBO_COMMUNICATION_RECOVERY_STANDARD_v1.md', 'wrong.md'))
        code, data = self.run_check()
        self.assertEqual(code, 1)
        self.assertTrue(any('Bootstrap missing reference' in e for e in data['errors']))

    def assert_anti_repeat_policy(self):
        policy = (self.root / 'governance/DEBO_SELF_IMPROVEMENT_AND_ANTI_REPEAT_ENGINE_v1.md').read_text(encoding='utf-8')
        for n in range(1, 13):
            self.assertIn(f'| AR-{n:02d} |', policy)
        self.assertIn('Mandatory change gate (all sister brains)', policy)
        self.assertIn('October 19 RRR corrective example', policy)

    def test_anti_repeat_regression_controls_present(self):
        self.assert_anti_repeat_policy()

    def test_anti_repeat_regression_missing_control_fails(self):
        path = self.root / 'governance/DEBO_SELF_IMPROVEMENT_AND_ANTI_REPEAT_ENGINE_v1.md'
        text = path.read_text(encoding='utf-8')
        self.assertIn('| AR-08 |', text)
        path.write_text(text.replace('| AR-08 |', '| REMOVED |'), encoding='utf-8')
        with self.assertRaises(AssertionError):
            self.assert_anti_repeat_policy()

    def test_anti_repeat_regression_missing_gate_fails(self):
        path = self.root / 'governance/DEBO_SELF_IMPROVEMENT_AND_ANTI_REPEAT_ENGINE_v1.md'
        text = path.read_text(encoding='utf-8')
        path.write_text(text.replace('Mandatory change gate (all sister brains)', 'Missing gate'), encoding='utf-8')
        with self.assertRaises(AssertionError):
            self.assert_anti_repeat_policy()

    def run_brief(self, project='DEBO'):
        return subprocess.run(
            [sys.executable, str(self.root / 'tools/debo_bootstrap_check.py'),
             '--brief', '--project', project], capture_output=True, text=True)

    def test_project_brief_is_scoped_and_requires_current_state(self):
        proc = self.run_brief('JCT')
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn('## Selected project: JCT', proc.stdout)
        self.assertIn('Project ID: JCT', proc.stdout)
        self.assertNotIn('Project ID: MOR', proc.stdout)
        self.assertIn('## Golden rules', proc.stdout)
        self.assertIn('Current project state: UNKNOWN', proc.stdout)
        self.assertIn('not runtime activation', proc.stdout)

    def test_master_brief_does_not_load_a_sister_profile(self):
        proc = self.run_brief()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn('## Selected project: DEBO', proc.stdout)
        self.assertNotIn('Project ID: JCT', proc.stdout)
        self.assertNotIn('Project ID: MOR', proc.stdout)

    def test_unknown_project_is_rejected(self):
        proc = self.run_brief('NOT_A_PROJECT')
        self.assertEqual(proc.returncode, 2)
        self.assertIn('invalid choice', proc.stderr)
        self.assertNotIn('## Golden rules', proc.stdout)

    def test_missing_golden_rules_fails_closed(self):
        path = self.root / 'governance/DEBO_RUNTIME_BOOTSTRAP_v2.md'
        path.write_text(path.read_text().replace('## Golden rules', '## Removed rules'))
        proc = self.run_brief('JCT')
        self.assertEqual(proc.returncode, 1)
        self.assertIn('Golden rules', proc.stderr)
        self.assertNotIn('## Selected project:', proc.stdout)

    def test_source_change_updates_fingerprint(self):
        proc = self.run_brief('JCT')
        self.assertEqual(proc.returncode, 0, proc.stderr)
        path = self.root / 'governance/DEBO_AUTONOMOUS_EXECUTION_STANDARD_v2.md'
        before = hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertIn(before, proc.stdout)
        path.write_text(path.read_text() + '\nChanged source version for isolated test.\n')
        after = hashlib.sha256(path.read_bytes()).hexdigest()
        changed = self.run_brief('JCT')
        self.assertEqual(changed.returncode, 0, changed.stderr)
        self.assertNotEqual(before, after)
        self.assertNotIn(before, changed.stdout)
        self.assertIn(after, changed.stdout)

    def run_sync(self, write=False):
        return subprocess.run(
            [sys.executable, str(self.root / 'tools/debo_bootstrap_check.py'),
             '--write-briefs' if write else '--check-briefs'],
            capture_output=True, text=True)

    def test_generated_briefs_are_repeatable_and_checked(self):
        absent = self.run_sync()
        self.assertEqual(absent.returncode, 1)
        self.assertFalse((self.root / 'governance/runtime-briefs').exists())
        written = self.run_sync(write=True)
        self.assertEqual(written.returncode, 0, written.stderr)
        self.assertEqual(len(json.loads(written.stdout)['updated']), 14)
        profile = self.root / 'governance/runtime-briefs/JCT.md'
        self.assertIn('Project ID: JCT', profile.read_text())
        self.assertIn('../DEBO_AUTONOMOUS_EXECUTION_STANDARD_v2.md', profile.read_text())
        self.assertEqual(self.run_sync().returncode, 0)
        unchanged = self.run_sync(write=True)
        self.assertEqual(json.loads(unchanged.stdout)['updated'], [])

    def test_changed_shared_source_marks_all_briefs_stale(self):
        self.assertEqual(self.run_sync(write=True).returncode, 0)
        path = self.root / 'governance/DEBO_AUTONOMOUS_EXECUTION_STANDARD_v2.md'
        path.write_text(path.read_text() + '\nChanged shared source in isolated test.\n')
        stale = self.run_sync()
        self.assertEqual(stale.returncode, 1)
        self.assertEqual(len(json.loads(stale.stdout)['stale']), 14)
        self.assertEqual(self.run_sync(write=True).returncode, 0)
        self.assertEqual(self.run_sync().returncode, 0)

    def test_profile_change_only_marks_its_own_brief_stale(self):
        self.assertEqual(self.run_sync(write=True).returncode, 0)
        path = self.root / 'governance/sister-brains/JCT_PROFILE_v1.md'
        path.write_text(path.read_text() + '\nChanged JCT scope in isolated test.\n')
        stale = self.run_sync()
        self.assertEqual(stale.returncode, 1)
        self.assertEqual(json.loads(stale.stdout)['stale'], ['JCT.md'])

    def test_generated_directory_symlink_is_rejected(self):
        outside = self.root / 'untouched'
        outside.mkdir()
        (self.root / 'governance/runtime-briefs').symlink_to(outside, target_is_directory=True)
        proc = self.run_sync(write=True)
        self.assertEqual(proc.returncode, 1)
        self.assertIn('symlink', proc.stderr)
        self.assertEqual(list(outside.iterdir()), [])


    def test_brief_includes_canonical_continuity_and_agent_chain(self):
        proc = self.run_brief('JCT')
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn('## Cross-thread continuity', proc.stdout)
        self.assertIn('## Chain of command', proc.stdout)
        self.assertIn('## Main DEBO agent board', proc.stdout)
        self.assertIn('Mack: Chief of Staff and Mission Control', proc.stdout)
        self.assertIn('Atlas: Chief Systems Architect and Senior Technical Lead', proc.stdout)
        self.assertIn('Current project state: UNKNOWN', proc.stdout)
        self.assertIn('not active workers', proc.stdout)
        self.assertIn('not runtime activation', proc.stdout)

    def test_continuity_rule_removal_fails_closed(self):
        p = self.root / 'governance/DEBO_COMMUNICATION_RECOVERY_STANDARD_v1.md'
        text = p.read_text(encoding='utf-8')
        original = next(line for line in text.splitlines() if line.startswith('7. Create/update a durable project checkpoint'))
        p.write_text(text.replace(original, '7. Missing continuity gate'), encoding='utf-8')
        result = self.run_brief('DEBO')
        self.assertEqual(result.returncode, 1)
        self.assertIn('Continuity policy', result.stderr)
        self.assertNotIn('## Selected project:', result.stdout)

    def test_duplicate_main_agent_alias_fails_closed(self):
        p = self.root / 'governance/DEBO_AGENT_COVERAGE_REGISTER_v1.json'
        data = json.loads(p.read_text(encoding='utf-8'))
        main = [role for role in data['roles'] if role['project_id'] == 'DEBO']
        main[0]['alias'] = main[1]['alias']
        p.write_text(json.dumps(data), encoding='utf-8')
        result = self.run_brief('JCT')
        self.assertEqual(result.returncode, 1)
        self.assertIn('13 unique documented', result.stderr)
        self.assertNotIn('## Selected project:', result.stdout)

    def test_continuity_and_board_changes_mark_all_briefs_stale(self):
        for path, addition in [
            ('governance/DEBO_COMMUNICATION_RECOVERY_STANDARD_v1.md', '\nLocal continuity change.\n'),
            ('governance/DEBO_AGENT_BOARD_ROLE_MAP_v1.md', '\nLocal board change.\n'),
            ('skills/agent-talent-manager/SKILL.md', '\nLocal skill charter change.\n'),
            ('prompts/DEBO_PERPLEXITY_SPEED_RESEARCH_MISSION_v1.md', '\nLocal research prompt change.\n'),
        ]:
            with self.subTest(path=path):
                self.assertEqual(self.run_sync(write=True).returncode, 0)
                file = self.root / path
                existing = file.read_text(encoding='utf-8')
                file.write_text(existing + addition, encoding='utf-8')
                stale = self.run_sync()
                self.assertEqual(stale.returncode, 1, stale.stderr)
                self.assertEqual(len(json.loads(stale.stdout)['stale']), 14)
                file.write_text(existing, encoding='utf-8')

    def test_registry_change_marks_all_briefs_stale(self):
        self.assertEqual(self.run_sync(write=True).returncode, 0)
        p = self.root / 'governance/DEBO_AGENT_COVERAGE_REGISTER_v1.json'
        registry = json.loads(p.read_text(encoding='utf-8'))
        registry['isolated_source_revision_test'] = 1
        p.write_text(json.dumps(registry), encoding='utf-8')
        stale = self.run_sync()
        self.assertEqual(stale.returncode, 1, stale.stderr)
        self.assertEqual(len(json.loads(stale.stdout)['stale']), 14)

if __name__ == '__main__':
    unittest.main()
