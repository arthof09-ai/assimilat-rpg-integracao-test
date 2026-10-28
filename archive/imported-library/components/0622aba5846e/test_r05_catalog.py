"""R05 directed regression on 12 live-retrieved Mestre pages. All TEST/read-only."""
from __future__ import annotations
import unittest, pathlib,sys,os,json,copy
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import R05_CONSULTA_CATALOGO_READONLY as R05
PROVIDER=pathlib.Path(os.environ.get('R05_R27_ORIGINAL','/mnt/data/pa_10_rodadas/r04/pa_r28/provider_r27'))
CONSUMER=pathlib.Path(os.environ.get('R05_R03_ORIGINAL','/mnt/data/pa_10_rodadas/r04/baseline_r03'))

class TestR05Catalog(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.data=R05.load_sources();provider,engine=R05.load_original_provider(PROVIDER)
  cls.provider=staticmethod(provider);cls.engine=staticmethod(engine)
  sys.path.insert(0,str(CONSUMER))
  cls.by_id={x['id']:x for x in cls.data['pages']}

 def test_census_directed_12_provenance(self):
  self.assertEqual(len(self.by_id),12)
  self.assertEqual(sum(x['surface']=='ITENS_MESTRE_CATALOGO' for x in self.by_id.values()),4)
  self.assertEqual(sum(x['surface']=='PESSOAL_MESTRE_PARTY_ESPELHO' for x in self.by_id.values()),8)
  self.assertEqual(len({x['uuid'] for x in self.by_id.values()}),12)
  for x in self.by_id.values():
   self.assertEqual(x['url'],'https://app.notion.com/p/'+x['uuid'])
   self.assertIn('TRANSCRIBED_EXCERPT',x['source_provenance'])

 def test_historic_typed_units(self):
  self.assertEqual(self.by_id['ZEPHYR_A']['historic'],{'daily_pa':90})
  self.assertEqual(self.by_id['ZEPHYR_B']['historic'],{'per_turn_pa':90})
  self.assertNotEqual(self.by_id['ZEPHYR_A']['uuid'],self.by_id['ZEPHYR_B']['uuid'])
  self.assertEqual(self.by_id['ANEL_ALMA']['historic'],{'capacity_bonus_pa':50})
  self.assertEqual(self.by_id['BOTA_CAMINHO_VELOZ']['historic'],{'daily_pa':18,'per_activation_pa':5})
  self.assertEqual(self.by_id['AMPLIFICADOR_A']['historic'],{'daily_pa':15})

 def test_price_not_paid_pa(self):
  for n in ['TOQUE_CHOCANTE','AMPLIFICADOR_A','ANEL_ALMA']:
   self.assertIsNotNone(self.by_id[n]['price_med'])
   self.assertNotIn('price_med',R05.request_for(self.by_id[n]))

 def test_sources_no_assumed_RI(self):
  for x in self.by_id.values():
   self.assertIsNone(x['source_item_rank'])
   self.assertIsNone(R05.request_for(x,legacy=True)['rank_item'])

 def test_potential_token_untrusted(self):
  self.assertEqual(self.by_id['TOQUE_CHOCANTE']['nominal_technique_rank'],'Ouro')
  self.assertFalse(self.by_id['TOQUE_CHOCANTE']['effect_text_present'])
  self.assertIsNone(R05.request_for(self.by_id['TOQUE_CHOCANTE'])['rank_item'])

 def test_no_authority_claim_in_source_contract(self):
  r=R05.main(PROVIDER,CONSUMER)
  self.assertEqual(r['E0_decisions_issued'],0)
  self.assertEqual(r['notion_writes'],0)
  self.assertEqual(r['party_writes'],0)
  self.assertEqual(r['native_source_page_changes'],0)
  self.assertEqual(r['production_status'],'HOLD')

 def test_legacy_preserved_for_every_page(self):
  for x in self.by_id.values():
   with self.subTest(page=x['id']):
    out=self.provider(R05.request_for(x,legacy=True))
    self.assertEqual(out['gate'],'DIAGNOSTICO_HISTORICO_SEM_REPRECIFICACAO')
    self.assertIsNone(out['custo_pa']['pa_total_no_cenario'])
    self.assertIsNone(out['custo_pa']['pa_por_dia'])
    self.assertEqual(out['custo_pa']['pa_historico_preservado'],x['historic'] or None)
    self.assertFalse(out['governanca']['party_write'])

 def test_all_pages_incomplete_for_new_without_rank(self):
  for x in self.by_id.values():
   with self.subTest(page=x['id']):
    out=self.provider(R05.request_for(x,legacy=False))
    self.assertIsNone(out['custo_pa']['pa_total_no_cenario'])
    self.assertEqual(out['gate'],'CONSULTA_TEST_PARCIAL_COM_PENDENCIAS')
    self.assertFalse(out['governanca']['historico_reprecificado'])

 def test_floor_alone_must_not_be_consumer_result(self):
  x=R05.rank_only_negative_canary(self.provider,self.engine)
  self.assertEqual(x['raw_native_daily_floor'],21)
  self.assertEqual(x['safe_existing_R03_state'],'HOLD_ITEM_SEM_EFEITO_DESCRITO')
  self.assertIsNone(x['safe_scenario_total'])

 def test_generic_attribute_text_not_auto_billed(self):
  x=self.by_id['AMPLIFICADOR_A'];req=R05.request_for(x,legacy=False,rank='Bronze')
  out=self.provider(req)
  self.assertIsNone(out['custo_pa']['pa_total_no_cenario'])
  self.assertTrue(any('BONUS_NAO_RECONHECIDO' in s for s in out['pendencias']))

 def test_conditional_amplifier_all_six_proposals_identical(self):
  d=R05.parametric_amplifier_test(self.data,self.provider)
  self.assertEqual(len(d['variants']),6)
  self.assertEqual({x['result_native_R27'] for x in d['variants']},{15})
  self.assertEqual(d['guard'],'RESULTADO_CONDICIONAL_E3_TEST_SEM_MODIFICAR_HISTORICO')

 def test_true_duplicate_sources_not_destroyed(self):
  self.assertNotEqual(self.by_id['AMPLIFICADOR_A']['uuid'],self.by_id['AMPLIFICADOR_B']['uuid'])
  self.assertEqual(self.by_id['AMPLIFICADOR_A']['excerpt'],self.by_id['AMPLIFICADOR_B']['excerpt'])
  self.assertNotEqual(self.by_id['ZEPHYR_A']['historic'],self.by_id['ZEPHYR_B']['historic'])

 def test_capacity_is_not_spend(self):
  x=self.by_id['ANEL_ALMA'];out=self.provider(R05.request_for(x,legacy=True))
  self.assertEqual(out['custo_pa']['pa_historico_preservado'],{'capacity_bonus_pa':50})
  self.assertIsNone(out['custo_pa']['pa_ativacoes_no_cenario'])
  self.assertIsNone(out['custo_pa']['pa_por_dia'])

 def test_source_family_is_master_only(self):
  for x in self.by_id.values():
   self.assertNotEqual(x['surface'],'PARTY_OFICIAL_PLAYERS')

 def test_complete_transcript_is_not_claimed(self):
  self.assertIn('não' if False else 'nao',self.data['method'].lower())
  self.assertIn('nao representam dump integral',self.data['method'])

 def test_input_is_readonly_even_if_action_override_attempted(self):
  x=self.by_id['AMPLIFICADOR_A'];req=R05.request_for(x,legacy=False,rank='Bronze',bonus=['+3 de Força'])
  req['acao']='FABRICAR'
  with self.assertRaises(Exception):self.provider(req)

 def test_not_assume_product_by_money_price(self):
  x=self.by_id['TOQUE_CHOCANTE']
  self.assertEqual(x['price_med'],4100000)
  o=self.provider(R05.request_for(x,legacy=False))
  self.assertIsNone(o['custo_pa']['pa_total_no_cenario'])

 def test_r27_rejects_duplicate_ability_names(self):
  x=self.by_id['BOTA_CAMINHO_VELOZ'];req=R05.request_for(x,legacy=False)
  req['habilidades'].append(req['habilidades'][0].copy())
  with self.assertRaises(Exception):self.provider(req)

 def test_r27_rejects_unknown_research_key(self):
  x=self.by_id['LÂMINA_ECLIPSE'] if 'LÂMINA_ECLIPSE' in self.by_id else self.by_id['LAMINA_ECLIPSE']
  q=R05.request_for(x,legacy=False);q['pesquisa']={'Nome de outra habilidade':{}}
  with self.assertRaises(Exception):self.provider(q)

 def test_not_assume_primary_zeppelin_on_conflict(self):
  x1,x2=self.by_id['ZEPHYR_A'],self.by_id['ZEPHYR_B']
  self.assertNotEqual(x1['last_edited'],x2['last_edited'])
  self.assertEqual(x1['surface'],x2['surface'])
  self.assertFalse(any('canonical' in z.lower() for z in [x1['source_provenance'],x2['source_provenance']]))

if __name__=='__main__':unittest.main(verbosity=2)
