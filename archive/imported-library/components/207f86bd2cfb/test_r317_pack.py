import json,hashlib,zipfile,unittest
from pathlib import Path
root=Path(__file__).resolve().parents[1]
class TestR317Package(unittest.TestCase):
 def test_r317_history_source_contract(self):
  m=json.loads((root/'manifest.json').read_text());self.assertEqual(m['last_verified'],317)
  self.assertEqual(m['first_pending'],318)
  self.assertEqual(len(m['history']),317)
  e=m['history'][-1];self.assertEqual(e['r'],317);self.assertEqual(e['status'],'EXECUTADO_TEST')
  z=root/'source_archives'/e['artifact'];self.assertEqual(hashlib.sha256(z.read_bytes()).hexdigest(),e['sha256'])
  with zipfile.ZipFile(z) as f:
   self.assertIsNone(f.testzip())
   self.assertIn('tests/test_r317_bridge.py',f.namelist())
   self.assertIn('overlay/fusion_stage12/audit_r317_counter.py',f.namelist())
 def test_no_terminal_promotion(self):
  m=json.loads((root/'manifest.json').read_text());self.assertEqual(m['terminal'],{'complete':0,'total':17});self.assertEqual(m['r91'],{'complete':0,'total':1875})
