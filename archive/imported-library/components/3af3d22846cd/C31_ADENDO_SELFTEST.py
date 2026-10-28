from pathlib import Path
import unittest,csv,json,zipfile,io
ROOT=Path(__file__).parent
class GateTests(unittest.TestCase):
 def test_sources_exact(self):
  with (ROOT/'C31_ADENDO_D0_120_PERSONAGENS_FONTE_A_FONTE.csv').open(encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
  self.assertEqual(len(rows),120);self.assertEqual(len(set(r['source_page_id'] for r in rows)),120)
 def test_correct_scopes(self):
  x=json.loads((ROOT/'C31_ADENDO_DENOMINADORES_RECONCILIADOS.json').read_text())
  self.assertEqual(x['personagens_index_coverage'],'233/233 DIRECT CHILD PAGE IDS')
  self.assertEqual(x['known_named_source_universe_sample_ancestor_pageids'],799)
  self.assertEqual(x['global_D0'],'NOT_CLOSED')
 def test_raw_dice_independent_means(self):
  d=json.loads((ROOT/'C31_ADENDO_RAW_DAMAGE_NEGATIVE_CONTROLS.json').read_text())
  result={}
  for samp in d['samples']:
   for ex in samp['expressions']:
    total=0
    for part in ex['literal'].split('+'):
     if 'd' in part:
      n,f=part.split('d');total+=int(n)*(int(f)+1)/2
     else:total+=int(part)
    self.assertEqual(total,ex['DME'])
 def test_no_canonical_write(self):
  x=json.loads((ROOT/'C31_ADENDO_DENOMINADORES_RECONCILIADOS.json').read_text())
  self.assertEqual((x['notion_write'],x['party_write'],x['OPrimeiro_write']),(0,0,0))
 def test_unapproved_effect_not_claimed(self):
  x=json.loads((ROOT/'C31_ADENDO_DENOMINADORES_RECONCILIADOS.json').read_text())
  self.assertEqual(x['strict_F6_effect_admission'],'NO_NEW_VERIFIED_EFFECT_RE_FIP')
if __name__=='__main__': unittest.main(verbosity=2)
