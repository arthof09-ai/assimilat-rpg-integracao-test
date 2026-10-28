import unittest,copy,json
from pathlib import Path
import pa_r04 as pa
import qmc02_pa_adapter as adapter
import consultor_pa_r04 as consultant
import avaliacao_holdout_r04 as holdout
ROOT=Path(__file__).resolve().parent
SOURCE=json.loads((ROOT/'BASELINE_QMC02/qmc02/source_readbacks.json').read_text('utf8'))['sources']
BOT=next(s for s in SOURCE if s['title']=='Bota Caminho Veloz')
DAG=next(s for s in SOURCE if 'Adaga' in s['title'])
CANDIDATE=json.loads((ROOT/'CANDIDATO_EXPERIMENTAL_ESPADA.json').read_text('utf8'))
class R04Critical(unittest.TestCase):
 def test_01_real_bota_qmc_and_pa_agree(self):
  x=adapter.emit_historical(BOT);y=adapter.qmc_sidecar_receive(x)
  self.assertEqual(y['historical_daily_pa'],18)
  self.assertEqual(x['message']['pa_engine']['activation_values'],[5])
  self.assertTrue(y['source_qualified_by_original_qmc02'])
 def test_02_adaga_rule_conflict_rejected(self):
  x=adapter.emit_historical(DAG)
  self.assertEqual(x['message']['state'],'CONFLITO_BLOQUEANTE')
  with self.assertRaises(ValueError):adapter.qmc_sidecar_receive(x)
 def test_03_native_qmc_remains_unconnected(self):
  x=adapter.emit_historical(BOT)
  self.assertEqual(adapter.qmc02.validate_external_pa(x['message'])['status'],'INTERFACE_EXTERNA_NAO_CONTRATADA')
 def test_04_tampered_message_rejected(self):
  x=adapter.emit_historical(BOT);x['message']['pa_engine']['daily_value']=9000
  with self.assertRaises(ValueError):adapter.qmc_sidecar_receive(x)
 def test_05_fixture_rejected_by_original(self):
  self.assertEqual(adapter.qmc02.validate_external_pa({'kind':'FIXTURE_SIMULADA','estimated_pa_daily':999})['status'],'SIMULACAO_NAO_OFICIAL')
 def test_06_candidate_unapproved_unknown_damage(self):
  q=pa.proposal(CANDIDATE)
  self.assertIsNone(q['daily_total_pa'])
  self.assertIn('DMG20',q['missing_daily_components'])
  self.assertEqual(q['daily_component_subtotal_scenario'],25)
  self.assertFalse(q['craft_released'])
 def test_07_candidate_sent_sidecar_no_fake_source(self):
  x=adapter.emit_candidate(CANDIDATE);y=adapter.qmc_sidecar_receive(x)
  self.assertEqual(y['receipt_state'],'ACEITO_CANDIDATO_TEST_SEM_VALIDAR_CUSTO')
  self.assertFalse(y['source_qualified_by_original_qmc02'])
 def test_08_no_double_count_in_documented_aggregate(self):
  x=copy.deepcopy(CANDIDATE);x['documented_base_pa_daily']=90;x['daily_base_includes_effects']=True
  q=pa.proposal(x);self.assertEqual(q['daily_total_pa'],90)
 def test_09_budget_unknown_semantics(self):
  self.assertEqual(pa.budget(100,20,18,5)['verdict'],'INDETERMINADO_SEMANTICA_DIA')
 def test_10_budget_scenarios_never_authorize(self):
  enough=pa.budget(120,20,18,5,daily_semantics='COMMIT')
  insufficient=pa.budget(40,20,18,5,daily_semantics='COMMIT')
  self.assertEqual(enough['verdict'],'COBERTURA_NUMERICA_CONDICIONAL')
  self.assertEqual(insufficient['verdict'],'INSUFICIENTE_NO_CENARIO')
  self.assertFalse(enough['can_authorize_use'])
 def test_11_incomplete_cost_is_unknown(self):
  self.assertEqual(pa.budget(120,20,None,5,daily_semantics='DEBIT')['verdict'],'INDETERMINADO_CUSTO_DIA')
 def test_12_damage_rd_math_not_pa(self):
  r=pa.damage_increment(15,20,25,attempts=3,p_hit=.6)
  self.assertAlmostEqual(r['expected_increment'],18)
  self.assertIsNone(r['energy_cost_pa'])
 def test_13_preregistered_outdomain_not_independent_holdout(self):
  r=holdout.calculate();self.assertEqual(r['n_eligible_master_catalog_holdout'],0)
  self.assertEqual(r['n_related_lineage_clusters'],4)
  self.assertEqual(r['out_of_domain_results']['absolute_error_mean'],64.333)
 def test_14_dialogue_retains_modality_unknown_pa(self):
  s=consultant.initial();s,r=consultant.dialogue(s,'Espada mágica +20 de dano em cada acerto')
  s,r=consultant.dialogue(s,'Somente uma vez por dia')
  self.assertEqual(next(e for e in s['effects'] if e['id']=='DMG_BONUS')['mode'],'ATIVO')
  s,r=consultant.dialogue(s,'Agora +5 em Destreza')
  self.assertIsNone(r['estimate']['daily_total_pa'])
  self.assertEqual(r['estimate']['daily_component_subtotal_scenario'],25)
 def test_15_deny_bad_production_flag_even_valid_hash(self):
  x=adapter.emit_historical(BOT)
  x['message']['production_hold']=False
  x['digest_sha256']=adapter._sha(x['message'])
  with self.assertRaises(ValueError):adapter.qmc_sidecar_receive(x)
 def test_16_duplicate_components_blocked(self):
  x=copy.deepcopy(CANDIDATE);x['effects'].append(copy.deepcopy(x['effects'][0]))
  with self.assertRaises(ValueError):pa.proposal(x)

if __name__=='__main__':unittest.main()
