import unittest,copy,hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from benchmark_re_r41 import mask_gold,score_predictions
BASE=json.loads((Path(__file__).parent/'RE_E0_26_INDEX_FROM_R40.json').read_text())
UID=BASE['techniques'][0]['notion_page_id'];RANK=BASE['techniques'][0]['rank_de_efeito_documentado']
TXT='Alvo individual, 1 ação padrão, raio 9 m, efeito imediato; dados independentes de exemplo.'
SHA=hashlib.sha256(TXT.encode()).hexdigest();S={'notion_page_id':UID,'mechanics_verified_text':TXT,'source_mechanics_sha256':SHA}
class R41RETests(unittest.TestCase):
 def test_has_26_labeled(self):self.assertEqual(len(BASE['techniques']),26)
 def test_has_five_ranks(self):self.assertEqual(len(set(x['rank_de_efeito_documentado'] for x in BASE['techniques'])),5)
 def test_no_mechanics_returns_null(self):self.assertIsNone(score_predictions(BASE,[],[])['accuracy'])
 def test_missing_fingerprint_unscorable(self):self.assertEqual(len(mask_gold(BASE,[{'notion_page_id':UID,'mechanics_verified_text':TXT}])['unscorable']),1)
 def test_opaque_name_hidden(self):self.assertNotIn('Rajada',str(mask_gold(BASE,[S])))
 def test_rank_hidden(self):self.assertNotIn('predicted_re',str(mask_gold(BASE,[S])))
 def test_fingerprint_binding(self):self.assertEqual(len(mask_gold(BASE,[S])['cases']),1)
 def test_predict_only_after_lock(self):self.assertIsNone(score_predictions(BASE,[S],[{'opaque_id':hashlib.sha256(UID.encode()).hexdigest()[:12],'predicted_re':RANK}])['accuracy'])
 def test_single_controlled_scoring(self):
  p={'opaque_id':hashlib.sha256(UID.encode()).hexdigest()[:12],'predicted_re':RANK,'prediction_locked':True,'mechanics_sha256':SHA}
  self.assertEqual(score_predictions(BASE,[S],[p])['accuracy'],1.0)
 def test_unknown_case_rejected(self):
  with self.assertRaises(ValueError):mask_gold(BASE,[{'notion_page_id':'fake','mechanics_verified_text':TXT,'source_mechanics_sha256':SHA}])
 def test_rank_in_mechanics_rejected(self):
  s=copy.deepcopy(S);s['mechanics_verified_text']='Classificação: Bronze';s['source_mechanics_sha256']=hashlib.sha256(s['mechanics_verified_text'].encode()).hexdigest()
  with self.assertRaises(ValueError):mask_gold(BASE,[s])
 def test_duplicate_predictions_rejected(self):
  p={'opaque_id':hashlib.sha256(UID.encode()).hexdigest()[:12],'predicted_re':RANK,'prediction_locked':True,'mechanics_sha256':SHA}
  with self.assertRaises(ValueError):score_predictions(BASE,[S],[p,p])
if __name__=='__main__':unittest.main(verbosity=2)
