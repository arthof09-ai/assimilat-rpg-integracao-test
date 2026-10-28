#!/usr/bin/env python3
"""Audit authored co-GM rule adjudications and immutable source artifacts.
This program NEVER adjudicates magic nor creates imaginary witness observations.
"""
from __future__ import annotations
import hashlib,json,zipfile,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PREV_ZIP='CRAFT_E21_E30_R39_R48_NATIVE_TEST_20261020.zip'
PREV_SHA='d0b113244cf590a9c30be34c5893c332a08a8e15daa3c17aa9be4cf5356104f0'
OLD_ORDER='SBX-R48-ORDER-48322'
case='LAB-CRAFT-VIGILIA-BOREAL-20261020-001'

def read(name):return json.loads((ROOT/name).read_text('utf8'))
SCENE=read('CENA_H1_RECEIPT_TEST.json')
GATE=read('GATES_E43_E50.json')
PA=read('PA_R39_H1_CONSULTA_REAL.json')
SOURCES=read('FONTES_H1_H2_SNAPSHOTS.json')
class TestIntegrity(unittest.TestCase):
 def test_master_exact_authority(self):self.assertIn('H1-SIM',SCENE['authority'])
 def test_unique_scene(self):self.assertEqual(SCENE['case_id'],case);self.assertEqual(len(SCENE['events']),5)
 def test_distinct_ids(self):self.assertEqual(len({e['event_id'] for e in SCENE['events']}),5)
 def test_rules_scope(self):self.assertEqual(SCENE['configurations_rule_resolved'],4);self.assertEqual(SCENE['configurations_outside_authority'],1)
 def test_c_retains_crystal_light(self):self.assertEqual(SCENE['events'][2]['resultado_adjudicado']['cristal'],'LUZ_CRISTALINA_PRESERVADA')
 def test_d_retains_herb_light(self):self.assertEqual(SCENE['events'][3]['resultado_adjudicado']['erva'],'ILUMINACAO_BOTANICA_PRESERVADA')
 def test_b_no_object_magic(self):self.assertEqual(SCENE['events'][1]['resultado_adjudicado']['suporte'],'SEM_HABILIDADE_MAGICA_PROPRIA')
 def test_e_scope_limited(self):self.assertEqual(SCENE['events'][4]['resultado_adjudicado']['observacao'],'INDETERMINADA_SEM_REGRA_ESPECIFICA_DE_OBSTRUCAO_MAGICA')
 def test_no_new_transaction(self):
  self.assertEqual(GATE['r48_new_orders'],0)
  self.assertEqual(GATE['r48_previous_consumed_order'],OLD_ORDER)
  self.assertTrue(all(e['pa_debitado'] is None and e['estoque_oficial_debitado'] is False for e in SCENE['events']))
 def test_no_faked_independent_witness(self):
  self.assertEqual(SCENE['observations_external_or_independent'],0)
  self.assertTrue(all(e['testemunha_externa_independente'] is False for e in SCENE['events']))
 def test_no_transfer_claim(self):self.assertFalse(SCENE['h2_transfer']);self.assertFalse(GATE['h2_inscription_executed'])
 def test_named_darkness_not_cast(self):self.assertEqual(SCENE['magic_darkness_comparator']['execution'].split(';')[0],'NAO_CONJURADA_NESTA_CENA')
 def test_provider_is_original(self):self.assertEqual(PA['contrato_craft_original'],'PA-CRAFT-QMC05-COMPAT-R27/1.0.0-TEST')
 def test_h1_provider_no_price(self):self.assertEqual(PA['gate_r39'],'CONSULTA_TEST_PARCIAL_EVIDENCIA_INSUFICIENTE');self.assertIsNone(PA['custo_pa_qualificado']['pa_por_dia'])
 def test_h1_unpriced_is_not_free(self):self.assertFalse(GATE['pa_h1_is_zero']);self.assertIsNone(GATE['pa_h1_daily'])
 def test_prior_item_pa_untouched(self):self.assertEqual(GATE['pa_v13_historic_prospective']['two_activation_scenario'],26)
 def test_source_excerpts_traceable(self):self.assertTrue(all(v.get('modified') and v.get('notion_id') for v in SOURCES.values()))
 def test_no_promotion(self):self.assertEqual(GATE['f5'],'RED');self.assertEqual(GATE['rc5_p4_production'],'HOLD')
 def test_scene_receipt_hash(self):
  got=hashlib.sha256((ROOT/'CENA_H1_RECEIPT_TEST.json').read_bytes()).hexdigest()
  self.assertEqual(got,(ROOT/'CENA_H1_RECEIPT_TEST.sha256').read_text().split()[0])
 def test_no_party_changes(self):self.assertEqual(GATE['party_write']+GATE['o_primeiro_write'],0)
 def test_previous_archive_hash_if_available(self):
  p=ROOT/'baselines'/PREV_ZIP
  if not p.exists():self.skipTest('Previous historical archive not bundled in this replay')
  self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),PREV_SHA)
 def test_previous_zip_receipt_readback(self):
  p=ROOT/'baselines'/PREV_ZIP
  if not p.exists():self.skipTest('Previous historical archive not bundled in this replay')
  with zipfile.ZipFile(p) as z:
   self.assertIsNone(z.testzip())
   curr=json.loads(z.read('CRAFT_E21_E30/results/R48_TEST_DURABLE_NEW/CURRENT.json'))
   self.assertEqual(curr.get('sequence'),1)
   commits=[n for n in z.namelist() if '/results/R48_TEST_DURABLE_NEW/commits/' in n and n.endswith('.json')]
   self.assertEqual(len(commits),2)

if __name__=='__main__':
 unittest.main(verbosity=1)
