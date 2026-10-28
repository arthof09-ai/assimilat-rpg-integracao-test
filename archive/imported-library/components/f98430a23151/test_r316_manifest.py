"""Integrity of the new R316 mother. No official campaign authority is inferred."""
from pathlib import Path
from hashlib import sha256
import json,zipfile,re,unittest
ROOT=Path(__file__).resolve().parents[1]
class R316Packaging(unittest.TestCase):
 def test_r316_archived_evidence_and_source_hash(self):
  d=json.loads((ROOT/'manifest.json').read_text())
  self.assertEqual(len(d['archives']),10)
  self.assertEqual(d['last_verified'],316)
  self.assertEqual(d['first_pending'],317)
  a=next(x for x in d['archives'] if x['name']=='VLAB_R316_COUNTER_NATIVE_MESTRE_ONLY.zip')
  z=ROOT/'source_archives'/a['name']
  self.assertEqual(sha256(z.read_bytes()).hexdigest(),a['sha256'])
  with zipfile.ZipFile(z) as f:
   self.assertIsNone(f.testzip())
   mf=json.loads(f.read('SHA256_MANIFEST.json'))
   for name,v in mf['files'].items():self.assertEqual(sha256(f.read(name)).hexdigest(),v)
 def test_synthetic_cases_are_distinct_from_r314(self):
  d=json.loads((ROOT/'manifest.json').read_text())
  self.assertEqual(len(d['history']),316)
  self.assertEqual(len(d['canary']['records']),128)
  r=d['r316'];self.assertEqual(r['paired_runs'],128)
  self.assertEqual(len(r['cases']),64)
  self.assertEqual(r['identical'],64)
  self.assertEqual(sum(c['counter_executed'] for c in r['cases']),54)
  self.assertFalse(r['r22_exposed'])
  self.assertEqual(d['terminal'],{'complete':0,'total':17})
  self.assertEqual(d['r91'],{'complete':0,'total':1875})
 def test_render_has_new_view_and_no_external_scripts(self):
  s=(ROOT/'index.html').read_text()
  d=json.loads((ROOT/'manifest.json').read_text())
  self.assertEqual(json.loads(re.search(r'<script id="vlab-dataset" type="application/json">(.*?)</script>',s,re.S).group(1)),d)
  self.assertIn('data-view="counter"',s)
  self.assertIn('data-frame="counter"',s)
  self.assertIn("function renderCounter()",s)
  self.assertNotIn('src="https://',s)
if __name__=='__main__':unittest.main()
