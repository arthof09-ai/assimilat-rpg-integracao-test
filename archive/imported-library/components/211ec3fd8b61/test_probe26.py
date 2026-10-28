import unittest,sys,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from probe26 import corpus,description,run
ENGINE=Path(os.environ.get('PA_R50_BASELINE_ENGINE','/mnt/data/PA_R50_ENGINE_ADAPTER_TEST/original_r26'))
class Probe26Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.corpus=corpus(ROOT);cls.result=run(ROOT,ENGINE)
 def test_census(self):self.assertEqual(len(self.corpus),26)
 def test_unique(self):self.assertEqual(len({x['case_id'] for x in self.corpus}),26)
 def test_whitelist(self):
  for x in self.corpus:self.assertNotIn('rank_proposal_test_only',x)
 def test_no_rank_word_from_image_used_as_output_rank(self):
  for x in self.corpus:
   text=description(x)
   self.assertNotIn('Rank do item: ',text)
 def test_no_research_supplied(self):
  self.assertEqual(self.result['source_scope'],'PA_R45_MANUAL_IMAGE_SUMMARIES_FIELDS_ONLY_NO_RANKS')
 def test_native_sample_count(self):self.assertEqual(self.result['n'],26)
 def test_no_auth_PA(self):
  for x in self.result['rows']:
   self.assertIsNone(x['authorized_PA'])
   self.assertIsNone(x['authoritative_RE'])
 def test_native_candidate_is_not_canonicity(self):
  self.assertEqual(self.result['authoritative_RE_finalized'],0)
 def test_source_images_sha_present(self):
  for r in self.result['rows']:self.assertEqual(len(r['image_sha256']),64)
 def test_no_label_field_in_export(self):
  for r in self.result['rows']:self.assertNotIn('label',r)
if __name__=='__main__':unittest.main()
