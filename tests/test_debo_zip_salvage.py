import tempfile, zipfile, unittest, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from debo_zip_salvage import rebuild, scan_local_headers

class SalvageTests(unittest.TestCase):
 def test_truncated_archive_recovers_only_complete_members(self):
  with tempfile.TemporaryDirectory() as d:
   src=Path(d)/'full.zip';t=Path(d)/'truncated.zip';out=Path(d)/'restored.zip'
   with zipfile.ZipFile(src,'w',compression=zipfile.ZIP_DEFLATED) as z:
    z.writestr('a.txt','one');z.writestr('b.txt','two');z.writestr('c.txt','three')
   data=src.read_bytes(); entries,_=scan_local_headers(src)
   # Simulate data truncated halfway through c.txt, before central directory.
   t.write_bytes(data[:entries[1]['end']+35])
   r=rebuild(t,out)
   self.assertEqual(r['complete_members'],2)
   self.assertTrue(r['crc_all_complete_members_pass'])
   self.assertEqual(t.read_bytes(),data[:entries[1]['end']+35])
   with zipfile.ZipFile(out) as z:self.assertEqual(z.namelist(),['a.txt','b.txt'])
 def test_original_can_be_rebuilt_without_mutation(self):
  with tempfile.TemporaryDirectory() as d:
   src=Path(d)/'a.zip';out=Path(d)/'b.zip'
   with zipfile.ZipFile(src,'w',compression=zipfile.ZIP_DEFLATED) as z:z.writestr('hello.txt','hello')
   original=src.read_bytes();r=rebuild(src,out)
   self.assertTrue(r['crc_all_complete_members_pass'])
   self.assertEqual(src.read_bytes(),original)
 def test_rejects_unsafe_archive_paths(self):
  with tempfile.TemporaryDirectory() as d:
   src=Path(d)/'unsafe.zip';out=Path(d)/'clean.zip'
   with zipfile.ZipFile(src,'w',compression=zipfile.ZIP_DEFLATED) as z:z.writestr('../escape.txt','payload')
   with self.assertRaises(ValueError):rebuild(src,out)
   self.assertFalse(out.exists())
 def test_duplicate_name_stops_recovery(self):
  with tempfile.TemporaryDirectory() as d:
   src=Path(d)/'dupe.zip';out=Path(d)/'dupe_out.zip'
   import warnings
   with warnings.catch_warnings():
    warnings.simplefilter('ignore',UserWarning)
    with zipfile.ZipFile(src,'w') as z:
     z.writestr('same.txt','first');z.writestr('same.txt','second')
   r=rebuild(src,out)
   self.assertEqual(r['complete_members'],1)
   self.assertIn('duplicate_member',r['stopped_because'])
 def test_does_not_overwrite_source(self):
  with tempfile.TemporaryDirectory() as d:
   src=Path(d)/'a.zip';src.write_bytes(b'x')
   with self.assertRaises(ValueError):rebuild(src,src)
if __name__=='__main__':unittest.main()
