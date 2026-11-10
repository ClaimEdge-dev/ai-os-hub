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


    def test_duplicate_notion_aliases_are_quarantined_regardless_of_row_order(self):
        rows = [{'Name': 'Thread Ops', 'Status': 'ACTIVE', 'Version': '1'},
                {'Name': 'thread-ops', 'Status': 'DEPRECATED', 'Version': '0'}]
        first = build_report(REGISTRY, rows)
        reverse = build_report(REGISTRY, list(reversed(rows)))
        self.assertEqual(first['summary']['notion_rows'], 2)
        self.assertEqual(first['summary']['notion_unique'], 1)
        self.assertEqual(first['summary']['notion_duplicate_names'], ['thread-ops'])
        self.assertEqual(first['summary']['catalog_conflicts'], 0)
        record = next(s for s in first['skills'] if s['id'] == 'thread-ops')
        other = next(s for s in reverse['skills'] if s['id'] == 'thread-ops')
        self.assertTrue(record['notion_alias_ambiguous'])
        self.assertEqual(record['notion_status'], 'AMBIGUOUS_NOTION_ALIAS')
        self.assertEqual(record['fingerprint'], other['fingerprint'])
        self.assertEqual(record['delta'], 'NEW')
        self.assertEqual(build_report(REGISTRY, rows, previous=first)['summary']['changed_skills'], 0)
        resolved = build_report(REGISTRY, [rows[0]], previous=first)
        fixed = next(s for s in resolved['skills'] if s['id'] == 'thread-ops')
        self.assertFalse(fixed['notion_alias_ambiguous'])
        self.assertEqual(fixed['notion_status'], 'ACTIVE')
        self.assertEqual(fixed['delta'], 'CHANGED')

    def test_duplicate_only_notion_alias_is_not_dropped(self):
        rows = [{'Name': 'Orphan Skill', 'Status': 'DRAFT'},
                {'Name': 'orphan-skill', 'Status': 'ACTIVE'}]
        report = build_report(REGISTRY, rows)
        records = [s for s in report['skills'] if s['id'] == 'orphan-skill']
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['notion_status'], 'AMBIGUOUS_NOTION_ALIAS')
        self.assertTrue(records[0]['notion_alias_ambiguous'])


if __name__ == '__main__':
    unittest.main()
