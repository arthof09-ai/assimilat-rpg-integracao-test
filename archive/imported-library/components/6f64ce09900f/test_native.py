import sys,unittest,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from runner import generate
from source_fence import *
import os
ENGINE=Path(os.environ.get('PA_R50_BASELINE_ENGINE','/mnt/data/PA_R50_ENGINE_ADAPTER_TEST/original_r26'))

class NativeIntegrationTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.result=generate(ROOT,ENGINE)
 def test_four_cases_complete(self):
  self.assertEqual(self.result['count'],4)
  self.assertEqual(len({c['case_id'] for c in self.result['cases']}),4)
 def test_four_have_proposed_rank_but_no_canonical(self):
  self.assertEqual({c['case_id'] for c in self.result['cases']},{'TEC-7F4A4B423743','TEC-968D29765EB1','TEC-AC33D1C9DD16','TEC-D9EF9388353A'})
  for c in self.result['cases']:
   self.assertIsNone(c['canonical_RE'])
   self.assertIsNone(c['authorized_pa_use'])
   self.assertIsNone(c['authorized_pa_daily'])
   self.assertEqual(c['n_effect_rank_adjudicated_comparators'],0)
 def test_all_source_rank_scope_explicit(self):
  for c in self.result['cases']:
   self.assertEqual(len(c['provenance_per_source']),c['source_count'])
   for s in c['provenance_per_source']:
    self.assertIn('scope',s)
    self.assertFalse(s['isolated_effect_RE_adjudicated'])
 def test_no_equivalent_rank_comparator(self):
  for c in self.result['cases']:
   self.assertEqual(sum(x['equivalent_mechanism'] and x['isolated_effect_RE_adjudicated'] for x in c['provenance_per_source']),0)
 def test_four_case_source_count(self):
  self.assertEqual(sorted(c['source_count'] for c in self.result['cases']),[2,3,3,3])
 def test_research_from_source_registry_all(self):
  for c in self.result['cases']:
   self.assertGreaterEqual(c['source_count'],2)
 def test_native_comparator_bug_reproduced(self):
  x=self.result['known_native_r26_duplicate_bug']
  self.assertEqual(x['old_doc_count'],2)
  self.assertEqual(x['old_distinct_types'],2)
  self.assertEqual(x['real_unique_UUID_count'],1)
 def test_outputs_not_authorized(self):
  self.assertEqual(self.result['PA_authorized'],0)
  self.assertEqual(self.result['canonical_RE_finalized'],0)
 def test_provisional_status(self):
  for c in self.result['cases']:
   self.assertEqual(c['status'],'TEST_ADVISORY_NO_CANONICAL_PROMOTION')
   self.assertEqual(c['source_gate']['state'],'EVIDENCE_FOR_ADVISORY_ONLY')
 def test_no_shadow_PA_fields(self):
  out=json.dumps(self.result)
  self.assertNotIn('pa_dia_pelo_rank_proposto',out)
  self.assertNotIn('pa_uso_pelo_rank_proposto',out)
 def test_original_engine_hash_frozen(self):
  from pathlib import Path
  p=ROOT/'original_R42_immutable.zip'
  if p.exists():self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),'6fbaaf8b54e79d5b7e506f580b32495ee3448e5f8c13c75be224e9c9fdbe7800')
 def test_case_snapshots_not_decision(self):
  for c in self.result['cases']:
   self.assertIn(c['peer_frozen'],('Bronze','Prata'))
   self.assertIn(c['R45_frozen'],('Bronze','Prata'))
 def test_sanitized_one_page_no_medium(self):
  from runner import prepare
  avaliar,old=prepare(ENGINE)
  uid='836c2b324ede83e2aae6016379ef2135'
  page='https://app.notion.com/p/'+uid
  text='Item: Amuleto Teste\nHabilidade ativa: Retaliação de Teste: Quando sofre dano pode usar sua reação para aplicar 2d10 de Fogo.'
  sub='Retaliação de Teste'
  explain='Um ataque reativo de fogo condicional não equivale a ataque com arma e carece de RE homólogo.'
  raw=[{'url':page+'?pvs=204','tipo':'familia','source_anchor':'16 PA por dia','comparacao_mecanica':'Responde a dano de arma de perto, não implica defesa contra o golpe.'},
       {'url':page+'?pvs=205','tipo':'vivo','source_anchor':'16 PA por dia','comparacao_mecanica':'Responde a dano de arma de perto, não implica defesa contra o golpe.'}]
  native=avaliar(text,pesquisa={sub:{'rank_sugerido':'Prata','justificativa':explain,'comparadores':raw}})
  status=native['r26']['pareceres'][0]
  self.assertEqual(status['confianca'],'MEDIA')
  reg=source_registry(ROOT/'fixtures/sources.json')
  f=fence(raw,reg,effect_mechanism='REACTIVE_FIRE_SAVE_AT_RANGE')
  self.assertEqual(len(f.unique_sources),1)
  filtered=avaliar(text,pesquisa={sub:{'rank_sugerido':'Prata','justificativa':explain,'comparadores':list(f.sanitized_comparators)}})
  self.assertNotEqual(filtered['r26']['pareceres'][0]['confianca'],'MEDIA')
 def test_real_source_roles_not_fake(self):
  reg=source_registry(ROOT/'fixtures/sources.json')
  self.assertEqual(reg['836c2b324ede83e2aae6016379ef2135']['role'],'familia')
  self.assertEqual(reg['d3fc2b324ede83c3a1bb01356904ce06']['role'],'vivo')

if __name__=='__main__':unittest.main()
