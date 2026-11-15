import unittest, tempfile, sys, json, zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from debo_export_inventory import inventory
class Tests(unittest.TestCase):
 def test_synthetic_conversations_and_index(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'test.zip'
   with zipfile.ZipFile(p,'w') as z:
    z.writestr('conversation_asset_file_names.json',json.dumps({'file_a.dat':'source.txt','file_b.dat':'missing.txt'}))
    z.writestr('conversations-000.json',json.dumps([{'title':'DEBO test','conversation_id':'synthetic-id','mapping':{'n1':{},'n2':{}}}]))
    z.writestr('file_a.dat',b'testing')
   r=inventory(p)
   self.assertEqual(r['conversations'],1)
   self.assertEqual(r['message_nodes'],2)
   self.assertEqual(r['assets_indexed_present'],1)
   self.assertEqual(r['assets_indexed_missing'],1)
   self.assertEqual(r['matched_threads'][0]['title'],'DEBO test')
 def test_missing_index_graceful(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'test.zip'
   with zipfile.ZipFile(p,'w') as z:z.writestr('conversations-000.json','[]')
   r=inventory(p);self.assertEqual(r['assets_declared'],0)
if __name__=='__main__':unittest.main()
