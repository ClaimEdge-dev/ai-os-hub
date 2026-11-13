"""Identity completeness is review evidence, never automatic skill matching."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools import debo_skill_delta as delta


SOURCES = {'thread-ops': 'skills/thread-ops/SKILL.md',
           'project/jcs-towing/intake': 'projects/jcs-towing/skills/intake/SKILL.md'}
LINK = 'https://github.com/ClaimEdge-dev/ai-os-hub/blob/main/'


class TestSkillIdentityAudit(unittest.TestCase):
    def test_keeps_blank_and_duplicate_title_rows_without_inventing_identity(self):
        rows = [{}, {'Name': 'Thread Ops', 'GitHub Link': LINK + SOURCES['thread-ops']},
                {'Name': 'Thread Ops'}]
        report = delta.audit_notion_identities(rows, SOURCES)
        self.assertEqual(report['summary']['rows'], 3)
        self.assertEqual(report['summary']['missing_skill_ids'], 3)
        self.assertEqual(report['summary']['missing_source_links'], 2)
        self.assertEqual(report['summary']['missing_names'], 1)
        self.assertIsNone(report['entries'][1]['skill_id'])
        self.assertIsNone(report['entries'][1]['source_path'])
        self.assertEqual([e['row_number'] for e in report['entries']], [1, 2, 3])

    def test_duplicate_declared_ids_are_quarantined_even_when_titles_differ(self):
        rows = [{'Name': 'First', 'skill_id': 'thread-ops'},
                {'Name': 'Second', 'skill_id': 'thread-ops'}]
        report = delta.audit_notion_identities(rows, SOURCES)
        self.assertEqual(report['summary']['duplicate_skill_ids'], ['thread-ops'])
        for entry in report['entries']:
            self.assertIn('DUPLICATE_SKILL_ID', entry['issues'])
            self.assertIsNone(entry['source_path'])

    def test_explicit_scoped_id_preserves_provenance_without_title_matching(self):
        skill_id = 'project/jcs-towing/intake'
        row = {'Name': 'Owner display title', 'skill_id': skill_id, 'Version': 'v1.0',
               'url': 'https://app.notion.com/p/example',
               'GitHub Link': LINK + SOURCES[skill_id]}
        entry = delta.audit_notion_identities([row], SOURCES)['entries'][0]
        self.assertEqual(entry['source_path'], SOURCES[skill_id])
        self.assertEqual(entry['notion_url'], row['url'])
        self.assertEqual(entry['version'], 'v1.0')
        self.assertEqual(entry['issues'], [])
        self.assertEqual(entry['runtime_installed'], 'UNVERIFIED')
        self.assertEqual(row['skill_id'], skill_id)

    def test_local_link_path_mismatch_and_outside_repository_remain_distinct(self):
        links = [LINK + 'skills/other/SKILL.md',
                 'https://github.com/Other/repo/blob/main/skills/thread-ops/SKILL.md',
                 'https://github.com.evil.example/ClaimEdge-dev/ai-os-hub/blob/main/'
                 + SOURCES['thread-ops']]
        for link, issue in zip(links, ['SOURCE_LINK_ID_MISMATCH',
                                     'SOURCE_LINK_OUTSIDE_LOCAL_REPOSITORY',
                                     'SOURCE_LINK_OUTSIDE_LOCAL_REPOSITORY']):
            with self.subTest(link=link):
                entry = delta.audit_notion_identities(
                    [{'Name': 'Thread Ops', 'skill_id': 'thread-ops', 'GitHub Link': link}],
                    SOURCES)['entries'][0]
                self.assertIn(issue, entry['issues'])

    def test_source_outside_scan_is_not_reported_as_missing_from_all_sources(self):
        entry = delta.audit_notion_identities(
            [{'Name': 'Other', 'skill_id': 'elsewhere', 'GitHub Link':
              'https://github.com/Other/repo/blob/main/SKILL.md'}], SOURCES)['entries'][0]
        self.assertIn('LOCAL_SOURCE_NOT_IN_SCAN', entry['issues'])
        self.assertIsNone(entry['source_path'])

    def test_optional_cli_leaves_default_report_unchanged(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'SKILL_REGISTRY.md').write_text(
                '| 1 | `thread-ops` | purpose | trigger | ACTIVE |\n')
            snapshot = root / 'notion.json'
            snapshot.write_text(json.dumps({'results': [{'Name': 'Thread Ops'}]}))
            command = [sys.executable, str(Path(delta.__file__).resolve()),
                       '--repo', str(root), '--notion', str(snapshot)]
            default = json.loads(subprocess.check_output(command, text=True))
            optional = json.loads(subprocess.check_output(
                command + ['--audit-identities'], text=True))
            self.assertEqual(optional.pop('identity_audit')['summary']['missing_skill_ids'], 1)
            self.assertEqual(default, optional)

    def test_missing_export_does_not_masquerade_as_zero_identity_gaps(self):
        result = subprocess.run([sys.executable, str(Path(delta.__file__).resolve()),
                                 '--audit-identities'], text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('requires an authorized --notion export', result.stderr)
        self.assertEqual(result.stdout, '')


if __name__ == '__main__':
    unittest.main()
