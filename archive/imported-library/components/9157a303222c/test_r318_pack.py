import unittest,json,hashlib,zipfile,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class R318Packaging(unittest.TestCase):
 def test_mother_has_r318_archives_and_history(self):
  d=json.loads((R/'manifest.json').read_text())
  self.assertEqual((d['last_verified'],d['first_pending'],len(d['history'])),(318,319,318))
  h=d['history'][-1];self.assertEqual(h['status'],'EXECUTADO_TEST');self.assertEqual(h['r'],318)
  src=R/'source_archives'/h['source'] if 'source' in h else R/'source_archives'/h['artifact']
  self.assertEqual(hashlib.sha256(src.read_bytes()).hexdigest(),h['sha256'])
  with zipfile.ZipFile(src) as z:
   self.assertIsNone(z.testzip())
   self.assertIn('tests/test_r318.py',z.namelist())
   self.assertIn('overlay/fusion_stage12/audit_r318_counter.py',z.namelist())
 def test_html_and_terminal_hold(self):
  d=json.loads((R/'manifest.json').read_text())
  raw=(R/'index.html').read_text()
  self.assertEqual(json.loads(re.search('<script id="vlab-dataset" type="application/json">(.*?)</script>',raw,re.S).group(1)),d)
  self.assertIn('R318 · RNG condicional',raw)
  self.assertEqual(d['terminal'],{'complete':0,'total':17})
  self.assertEqual(d['r91'],{'complete':0,'total':1875})
if __name__=='__main__':unittest.main()
