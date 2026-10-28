"""Regressão R05 mínima e dirigida aos novos riscos, sem repetir suites R03/QMC02."""
from pathlib import Path
import unittest, copy, json
import pa_r05 as pa
import consultor_pa_r05 as cons
import qmc_pa_r05_wire as wire

P=Path(__file__).resolve().parent
BASE=P.parent/'BASELINES'/'R04_EXTRAIDO'/'PA_UNIVERSAL_R04_TEST_20261017'
SOURCES=json.loads((BASE/'BASELINE_QMC02'/'qmc02'/'source_readbacks.json').read_text('utf8'))['sources']
BOTA=[s for s in SOURCES if s['uuid']=='3edc2b324ede8135b199fd0cdbb5463c'][0]

class RegressionR05(unittest.TestCase):
 def test_attribute_rule_exact_and_historical(self):
  q=pa.quote_attribute({'DES':5});self.assertEqual(q['daily_pa'],25);self.assertEqual(q['rule'],pa.RULE_ID)
 def test_attribute_additive_distinct_types(self):
  self.assertEqual(pa.quote_attribute({'DES':5,'INT':10})['daily_pa'],75)
 def test_attribute_invalid_mode(self):
  self.assertIsNone(pa.quote_attribute({'DES':5},mode='ATIVO_POR_USO')['per_use_pa'])
 def test_attribute_unknown_never_zero(self):
  self.assertIsNone(pa.component_model([])['daily_total_pa'])
 def test_standalone_new_attribute_exact(self):
  x=pa.component_model([{'id':'a','kind':'ATRIBUTO','mode':'PASSIVO_DIARIO','attribute':'DES','magnitude':5}]);self.assertEqual(x['daily_total_pa'],25)
 def test_mixed_damage_indeterminate(self):
  x=pa.component_model([{'id':'a','kind':'ATRIBUTO','attribute':'DES','magnitude':5},{'id':'d','kind':'dano_passivo_por_acerto','magnitude':20}]);self.assertEqual(x['daily_pa_subtotal_identified'],25);self.assertIsNone(x['daily_total_pa'])
 def test_rd_elemental_no_invented_rate(self):
  x=pa.component_model([{'id':'rd','kind':'rd_elemental','magnitude':20}]);self.assertIsNone(x['daily_total_pa'])
 def test_daily_vs_per_use_exclusive(self):
  x=pa.component_model([{'id':'a','kind':'ATRIBUTO','attribute':'INT','magnitude':3,'mode':'ATIVO_POR_USO'}]);self.assertIsNone(x['daily_total_pa']);self.assertIsNone(x['activation_total_pa_per_use'])
 def test_duplicate_effect_rejected(self):
  with self.assertRaises(ValueError):pa.component_model([{'id':'a','kind':'ATRIBUTO','attribute':'DES','magnitude':5}]*2)
 def test_original_historical_unchanged(self):
  h=pa.history('Bota Caminho Veloz');self.assertEqual(h['pa_daily']['value'],18);self.assertEqual(h['pa_activation']['value'],5)
 def test_adaga_ambiguity_preserved(self):
  h=pa.history('Adaga da Serpente Enfeitiçada (ON)');self.assertIsNone(h['R05_reconciliation']['usable_daily_pa_R05']);self.assertEqual(h['pa_daily']['value'],35)
 def test_sabedoria_conflict_master(self):
  x=pa.history('Sabedoria Ancestral')['audit_attribute_rule'];self.assertEqual(x['issues'][0]['deficit_pa_day_at_least'],30)
 def test_colar_conditional_conflict_master(self):
  x=pa.history('Colar cadente')['audit_attribute_rule'];self.assertEqual(x['issues'][0]['condition'],'LUZ_DAS_ESTRELAS');self.assertEqual(x['issues'][0]['deficit_pa_day_at_least'],6)
 def test_amuleto_mirror_conflict_not_master(self):
  x=pa.history('(AI) Amuleto de Inteligência')['audit_attribute_rule'];self.assertEqual(x['surface'],'PARTY_MESTRE_ESPELHO');self.assertEqual(x['issues'][0]['deficit_pa_day_at_least'],20)
 def test_invalid_boolean_not_numeric(self):
  with self.assertRaises(ValueError):pa.quote_attribute({'DES':True})
 def test_budget_free_no_second_deduction_unknown(self):
  x=pa.available_pa_budget(pa_free_declared=80,daily_pa=25,semantics='UNKNOWN');self.assertIsNone(x['free_after_daily_if_commit']);self.assertEqual(x['status'],'INDETERMINADO')
 def test_budget_commit_conditional(self):
  x=pa.available_pa_budget(pa_total=100,pa_committed_other=20,daily_pa=25,activation_pa=5,activation_count=2,semantics='COMMIT');self.assertEqual(x['free_after_uses_if_commit'],45);self.assertFalse(x['item_use_authorized'])
 def test_budget_mismatch_rejected(self):
  with self.assertRaises(ValueError):pa.available_pa_budget(pa_total=100,pa_committed_other=20,pa_free_declared=79)
 def test_free_phrase_parser(self):
  st,rep=cons.interpret(cons.initial(),'Esse item funciona com 80 PA livres?');self.assertEqual(st['pa_free_declared'],80)
 def test_natural_order_attribute(self):
  st,rep=cons.interpret(cons.initial(),'Quanto PA custaria um item que aumenta Destreza em +5?');self.assertEqual(rep['energy']['daily_total_pa'],25)
 def test_one_per_day_active_vs_conditional(self):
  s,_=cons.interpret(cons.initial(),'espada com +20 dano em cada acerto')
  s,_=cons.interpret(s,'e se acontecer uma vez por dia?');d=next(x for x in s['effects'] if x['id']=='DANO_BONUS');self.assertEqual(d['mode'],'CONDICIONAL_DIARIO')
  s,_=cons.interpret(s,'e se for ativada uma vez por dia?');d=next(x for x in s['effects'] if x['id']=='DANO_BONUS');self.assertEqual(d['mode'],'ATIVO_POR_USO')
 def test_qmc_original_qualify_and_extract(self):
  w=wire.wrap_qualified_source(BOTA);self.assertEqual(w['message']['daily_pa'],18);self.assertEqual(w['message']['activation_pa_values'],[5]);self.assertEqual(wire.strict_local_validation(w)['status'],'RECEBIDO_R05_TEST_FORA_DO_ENTRYPOINT_NATIVO')
 def test_original_native_validator_is_still_rejecting(self):
  w=wire.wrap_qualified_source(BOTA);p=wire.native_qmc_probe(w);self.assertFalse(p['native_accepted']);self.assertEqual(p['native_return']['status'],'INTERFACE_EXTERNA_NAO_CONTRATADA')
 def test_candidate_wire_unknown_damage(self):
  w=wire.wrap_candidate({'candidate_id':'ESPADA','evidence_type':'USER_EXPERIMENTAL_SPEC','qmc_family':'ARMA','effects':[{'id':'a','kind':'ATRIBUTO','attribute':'DES','magnitude':5},{'id':'d','kind':'dano_passivo_por_acerto','magnitude':20}]});self.assertIsNone(w['message']['daily_pa']);self.assertEqual(w['message']['identified_daily_subtotal'],25);self.assertFalse(wire.strict_local_validation(w)['approved_for_recipe'])
 def test_tamper_digest_rejected(self):
  w=wire.wrap_qualified_source(BOTA);w['message']['daily_pa']=0
  with self.assertRaises(ValueError):wire.strict_local_validation(w)
 def test_tamper_digest_recomputed_still_test(self):
  w=wire.wrap_qualified_source(BOTA);w['message']['daily_pa']=0;w['digest_sha256']=wire.sha(w['message'])
  with self.assertRaises(ValueError):wire.strict_local_validation(w)
  # SHA de payload NÃO é assinatura/autenticidade; o recálculo local agora confere baseline imutável.
 def test_fake_production_rejected(self):
  w=wire.wrap_qualified_source(BOTA);w['message']['new_recipe_permitted']=True;w['digest_sha256']=wire.sha(w['message'])
  with self.assertRaises(ValueError):wire.strict_local_validation(w)
 def test_fake_master_source_candidate_rejected(self):
  w=wire.wrap_candidate({'candidate_id':'XX','evidence_type':'USER_EXPERIMENTAL_SPEC','effects':[]});w['message']['uuid']='3edc2b324ede8135b199fd0cdbb5463c';w['digest_sha256']=wire.sha(w['message'])
  with self.assertRaises(ValueError):wire.strict_local_validation(w)
 def test_unknown_units_rejected(self):
  w=wire.wrap_qualified_source(BOTA);w['message']['daily_unit']='PA/uso';w['digest_sha256']=wire.sha(w['message'])
  with self.assertRaises(ValueError):wire.strict_local_validation(w)
 def test_activation_cost_requires_source(self):
  with self.assertRaises(ValueError):pa.component_model([{'id':'a','kind':'CUSTO_ATIVACAO_HISTORICO','mode':'ATIVO_POR_USO','magnitude':5}])
 def test_ambiguous_coverage_no_holdout(self):
  o=pa.scientific_status();self.assertEqual(o['independent_master_holdout_numeric_n'],0);self.assertEqual(o['empirically_estimated_universal_coefficients'],0)

if __name__=='__main__':unittest.main(verbosity=2)
