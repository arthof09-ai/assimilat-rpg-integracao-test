"""Ensaios isolados da apresentação, NÃO certificação do motor VLAB."""
from pathlib import Path
import hashlib,importlib.util,json,shutil,tempfile,unittest,zipfile,re
ROOT=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('updater',ROOT/'tools/update_html.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class TestPresentation(unittest.TestCase):
 def test_index_matches_manifest(self):
  manifest=json.loads((ROOT/'manifest.json').read_text())
  html=(ROOT/'index.html').read_text()
  embedded=json.loads(mod.DATAPATTERN.search(html).group(2))
  self.assertEqual(embedded,manifest)
  self.assertEqual(len(manifest['history']),318)
  self.assertEqual(len(manifest['contracts']),17)
  self.assertEqual(len(manifest['canary']['records']),128)
  self.assertEqual(sum(manifest['canary']['counts'].values()),128)
  self.assertEqual(manifest['terminal'],{'complete':0,'total':17})
  self.assertEqual(manifest['r91'],{'complete':0,'total':1875})
  self.assertEqual(manifest['last_verified'],318)
  self.assertEqual(manifest['first_pending'],319)
 def test_sources_unchanged(self):
  manifest=json.loads((ROOT/'manifest.json').read_text())
  for z in manifest['archives']:
   p=ROOT/'source_archives'/z['name'];self.assertEqual(mod.digest(p),z['sha256']);self.assertIsNone(zipfile.ZipFile(p).testzip())
 def test_nonexistent_evidence_rejected(self):
  with tempfile.TemporaryDirectory() as t:
   d=Path(t);shutil.copy2(ROOT/'manifest.json',d);shutil.copy2(ROOT/'index.html',d)
   p=d/'fake.zip';p.write_bytes(b'mock data')
   j={'schema':'VLAB_CODEMOTHER_UPDATE_V1','operation':'OP-VLAB-FUSION-SANDBOX-01','r':319,'title':'SIMULADO NO TESTE','proof':'Somente teste de software, não experimento VLAB','status':'EXECUTADO_TEST','source':'fake.zip','evidence_sha256':'0'*64,'first_pending':320}
   u=d/'update.json';u.write_text(json.dumps(j))
   with self.assertRaises(ValueError):mod.apply(u,p,d)
   self.assertFalse((d/'snapshots').exists())
 def test_simulated_update_roundtrip(self):
  with tempfile.TemporaryDirectory() as t:
   d=Path(t);shutil.copy2(ROOT/'manifest.json',d);shutil.copy2(ROOT/'index.html',d)
   p=d/'mock.txt';p.write_bytes(b'Updater mock fixture, no VLAB execution')
   j={'schema':'VLAB_CODEMOTHER_UPDATE_V1','operation':'OP-VLAB-FUSION-SANDBOX-01','r':319,'title':'TESTE DE SOFTWARE - NAO EVIDENCIA R317','proof':'Ensaio em diretório temporário descartável','status':'EXECUTADO_TEST','source':'mock.txt','evidence_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'first_pending':320}
   u=d/'update.json';u.write_text(json.dumps(j))
   result=mod.apply(u,p,d)
   self.assertEqual(result['to'],319)
   self.assertEqual(json.loads((d/'manifest.json').read_text())['first_pending'],320)
   self.assertTrue((d/'snapshots'/'index_R318.html').exists())
   self.assertEqual(json.loads(mod.DATAPATTERN.search((d/'index.html').read_text()).group(2))['last_verified'],319)
   with self.assertRaises(ValueError):mod.apply(u,p,d)
if __name__=='__main__':unittest.main()
