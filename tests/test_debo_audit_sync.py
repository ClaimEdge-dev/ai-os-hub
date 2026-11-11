"""Offline source-only tests; credentials and network are never used."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import debo_audit_sync as a

class FakeApi:
    def __init__(self):
        self.calls = []
        self.blocks = {}
        self.files = {}
        self.branch = False
        self.main_sha = 'a' * 40
    def github(self, method, path, data=None, missing_ok=False):
        self.calls.append(('gh', method, path))
        if path.startswith('/git/ref/heads/main'):
            return {'object': {'sha': self.main_sha}}
        if path.startswith('/git/ref/heads/' + a.BRANCH):
            return {'object': {'sha': self.main_sha}} if self.branch else None
        if method == 'POST' and path == '/git/refs':
            self.branch = True
            return {}
        if path.startswith('/contents/'):
            key = path.split('?')[0]
            if method == 'GET':
                return self.files.get(key)
            self.files[key] = {'content': data['content'], 'sha': 'blob-' + str(len(self.calls))}
            return {}
        if path.startswith('/commits/'):
            return {'commit': {'tree': {'sha': 'b'*40}}}
        if path.startswith('/git/trees/'):
            return {'truncated': False, 'tree':[{'type':'blob','path':'tests/test_debo.py','sha':'abc','size':4}]}
        raise AssertionError(path)
    def notion(self, method, path, data=None):
        self.calls.append(('notion', method, path))
        if method == 'GET' and path.startswith('/blocks/') and path.endswith('/children?page_size=100'):
            return {'results':[{'id':k,'paragraph':{'rich_text':[{'plain_text':v}]}} for k,v in self.blocks.items()], 'has_more':False}
        if method == 'PATCH' and path.endswith('/children'):
            txt = data['children'][0]['paragraph']['rich_text'][0]['text']['content']
            self.blocks['block1'] = txt
            return {'results':[{'id':'block1'}]}
        if method == 'PATCH':
            self.blocks[path.split('/')[-1]] = data['paragraph']['rich_text'][0]['text']['content']
            return {}
        if method == 'GET':
            return {'paragraph':{'rich_text':[{'plain_text':self.blocks[path.split('/')[-1]]}]}}
        raise AssertionError(path)

class AuditTests(unittest.TestCase):
    def test_stable_sha_and_release_tag(self):
        self.assertEqual(a.stable_id('commit','a'*40), 'commit-'+'a'*40)
        self.assertEqual(a.stable_id('release','v1'),a.stable_id('release','v1'))
        with self.assertRaises(a.SyncError): a.stable_id('commit','../bad')
    def test_inventory_metadata_only(self):
        s=a.tree_summary([{'type':'blob','path':'docs/a.md','sha':'x','size':3},{'type':'blob','path':'tests/t.py','sha':'y','size':2}])
        self.assertEqual(s['categories']['documentation'],1)
        self.assertEqual(s['file_count'],2)
        self.assertNotIn('path',s)
    def test_unapproved_branch_refused(self):
        with self.assertRaises(a.SyncError):a.source_from_event('push',{'ref':'refs/heads/feature','after':'a'*40},FakeApi())
    def test_truncated_inventory_is_failure(self):
        f=FakeApi()
        real=f.github
        def truncated(method,path,data=None,missing_ok=False):
            if path.startswith('/git/trees/'):return {'truncated':True,'tree':[]}
            return real(method,path,data,missing_ok)
        f.github=truncated
        with self.assertRaises(a.SyncError):a.build_manifest(f,'push',{'ref':'refs/heads/main','after':'a'*40},'1','2026-11-10T00:00:00Z')
    def test_git_upsert_one_file_no_duplicates_and_readback(self):
        f=FakeApi();m={'audit_id':'commit-'+'a'*40}
        url=a.github_archive(f,m)
        self.assertIn('audits/debo/entries/',url)
        a.github_archive(f,m)
        self.assertEqual(len(f.files),1)
        self.assertEqual(sum(c[1]=='PUT' for c in f.calls),1)
    def test_notion_upsert_in_place(self):
        f=FakeApi();m={'audit_id':'commit-'+'a'*40,'inventory_status':'VERIFIED_PUBLIC_GITHUB_METADATA','source_type':'commit','source':'a'*40,'inventory':{'file_count':1},'last_run_id':'1','last_observed_utc':'2026-11-10'}
        a.notion_upsert(f,a.PAGE_ID,m,'https://github.com/ClaimEdge-dev/ai-os-hub')
        m['last_run_id']='2'
        a.notion_upsert(f,a.PAGE_ID,m,'https://github.com/ClaimEdge-dev/ai-os-hub')
        self.assertEqual(len(f.blocks),1)
        self.assertEqual(sum(c[1]=='PATCH' for c in f.calls),2)
    def test_duplicate_notion_blocks_fail(self):
        f=FakeApi();m={'audit_id':'commit-'+'a'*40,'inventory_status':'OK','source_type':'commit','source':'a'*40,'inventory':{},'last_run_id':'1','last_observed_utc':'2026-11-10'}
        f.blocks={'x':'DEBO-AUDIT-ID:'+m['audit_id'],'y':'DEBO-AUDIT-ID:'+m['audit_id']}
        with self.assertRaises(a.SyncError):a.notion_upsert(f,a.PAGE_ID,m,'https://example.com')
    def test_release_metadata_does_not_fake_commit(self):
        m=a.build_manifest(FakeApi(),'release',{'release':{'tag_name':'v1.0','html_url':'https://github.com/release'}},'1','2026-11-10')
        self.assertIsNone(m['source_commit_sha'])
        self.assertIsNone(m['inventory'])
    def test_dry_run(self):
        import subprocess
        result=subprocess.run([sys.executable,str(Path(a.__file__).resolve()),'--dry-run'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0)
        self.assertIn('"dry_run": true',result.stdout)

if __name__=='__main__':unittest.main()