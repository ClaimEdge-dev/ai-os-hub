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

if __name__ == '__main__':
    unittest.main()
