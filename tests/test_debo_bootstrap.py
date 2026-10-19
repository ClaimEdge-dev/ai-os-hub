"""Exercise bootstrap integrity against isolated copies; never mutate checkout."""
import importlib.util
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

    def test_anti_repeat_regression_controls_present(self):
        policy = (self.root / 'governance/DEBO_SELF_IMPROVEMENT_AND_ANTI_REPEAT_ENGINE_v1.md').read_text(encoding='utf-8')
        for n in range(1, 13):
            with self.subTest(control=n):
                self.assertIn(f'| AR-{n:02d} |', policy)
        self.assertIn('Mandatory change gate (all sister brains)', policy)
        self.assertIn('October 19 RRR corrective example', policy)

    def test_anti_repeat_regression_missing_control_fails(self):
        path = self.root / 'governance/DEBO_SELF_IMPROVEMENT_AND_ANTI_REPEAT_ENGINE_v1.md'
        text = path.read_text(encoding='utf-8')
        self.assertIn('| AR-08 |', text)
        path.write_text(text.replace('| AR-08 |', '| REMOVED |'), encoding='utf-8')
        with self.assertRaises(AssertionError):
            self.test_anti_repeat_regression_controls_present()

    def test_anti_repeat_regression_missing_gate_fails(self):
        path = self.root / 'governance/DEBO_SELF_IMPROVEMENT_AND_ANTI_REPEAT_ENGINE_v1.md'
        text = path.read_text(encoding='utf-8')
        path.write_text(text.replace('Mandatory change gate (all sister brains)', 'Missing gate'), encoding='utf-8')
        with self.assertRaises(AssertionError):
            self.test_anti_repeat_regression_controls_present()

if __name__ == '__main__':
    unittest.main()
