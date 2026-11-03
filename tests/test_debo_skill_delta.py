"""Synthetic checks for offline DEBO source/status comparison."""
import tempfile
import unittest
from pathlib import Path
from tools.debo_skill_delta import build_report, github_statuses, load_rows

REGISTRY = '| # | Skill | Purpose | Trigger | Status |\n| 1 | `thread-ops` | a | all | ACTIVE |\n'


class TestDEBOSkillDelta(unittest.TestCase):
    def test_registry_status(self):
        self.assertEqual(github_statuses(REGISTRY)['thread-ops'], 'ACTIVE')

    def test_conflict_and_no_install_claim(self):
        report = build_report(REGISTRY, [{'Name':'thread-ops','Status':'DEPRECATED'}])
        self.assertEqual(report['summary']['catalog_conflicts'], 1)
        self.assertEqual(report['skills'][0]['runtime_installed'], 'UNVERIFIED')

    def test_sha_and_change_detection(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / 'skills'
            (root / 'thread-ops').mkdir(parents=True)
            (root / 'thread-ops' / 'SKILL.md').write_text('one')
            first = build_report(REGISTRY, skills_root=root)
            self.assertEqual(build_report(REGISTRY, skills_root=root, previous=first)['summary']['changed_skills'], 0)
            (root / 'thread-ops' / 'SKILL.md').write_text('two')
            self.assertEqual(build_report(REGISTRY, skills_root=root, previous=first)['summary']['changed_skills'], 1)

    def test_duplicate_rows(self):
        a = [{'Name':'Same Name','Status':'ACTIVE'}, {'Name':'same-name','Status':'ACTIVE'}]
        self.assertEqual(build_report(REGISTRY, a)['summary']['notion_duplicate_names'], ['same-name'])

    def test_optional_exports(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'data.json'
            p.write_text('{"results":[{"Name":"thread-ops"}]}')
            self.assertEqual(len(load_rows(p)), 1)
            self.assertEqual(load_rows(None), [])


if __name__ == '__main__':
    unittest.main()
