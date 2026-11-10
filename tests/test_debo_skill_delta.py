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


    def test_project_skills_are_optional_scoped_and_delta_tracked(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            root = base / 'skills'
            root_skill = root / 'jct-dispatch-intake'
            root_skill.mkdir(parents=True)
            (root_skill / 'SKILL.md').write_text('core')
            projects = base / 'projects'
            for project in ('jcs-towing', 'rapid-roadside-repair'):
                local = projects / project / 'skills' / 'jct-dispatch-intake'
                local.mkdir(parents=True)
                (local / 'SKILL.md').write_text(project)
            baseline = build_report(REGISTRY, skills_root=root)
            self.assertEqual(baseline['summary']['project_skill_sources'], 0)
            self.assertEqual(len(baseline['skills']), 2)
            report = build_report(REGISTRY, skills_root=root, projects_root=projects)
            self.assertEqual(report['summary']['project_skill_sources'], 2)
            rows = {item['id']: item for item in report['skills']}
            self.assertIn('jct-dispatch-intake', rows)
            self.assertIn('project/jcs-towing/jct-dispatch-intake', rows)
            self.assertIn('project/rapid-roadside-repair/jct-dispatch-intake', rows)
            self.assertEqual(rows['project/jcs-towing/jct-dispatch-intake']['source_path'],
                             'projects/jcs-towing/skills/jct-dispatch-intake/SKILL.md')
            self.assertEqual(rows['project/jcs-towing/jct-dispatch-intake']['runtime_installed'], 'UNVERIFIED')
            local = projects / 'jcs-towing' / 'skills' / 'jct-dispatch-intake' / 'SKILL.md'
            local.write_text('changed')
            delta = build_report(REGISTRY, skills_root=root, projects_root=projects, previous=report)
            self.assertEqual(delta['summary']['changed_skills'], 1)
            changed = {item['id']: item for item in delta['skills']}
            self.assertEqual(changed['project/jcs-towing/jct-dispatch-intake']['delta'], 'CHANGED')
            self.assertEqual(changed['project/rapid-roadside-repair/jct-dispatch-intake']['delta'], 'UNCHANGED')


if __name__ == '__main__':
    unittest.main()
