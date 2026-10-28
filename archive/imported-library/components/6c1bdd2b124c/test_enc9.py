import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import enc9_dependency as x
class Corpus(unittest.TestCase):
 def test_9(self):self.assertEqual(len(x.CATALOG),9)
 def test_9_source_pages(self):self.assertEqual(x.corpus_report()['inscription_source_pages'],9)
 def test_9_recipe_pages_minus_one_inline(self):self.assertEqual(x.corpus_report()['recipe_source_pages'],9)
 def test_8_oil(self):self.assertEqual(x.corpus_report()['oil_dependency_count'],8)
 def test_1_oilfree(self):self.assertEqual(x.corpus_report()['oil_independent_count'],1)
 def test_only_reflexo(self):self.assertEqual(x.corpus_report()['oil_independent_names'],['REFLEXO_PROFUNDEZAS_P'])
 def test_four_weapon_surface(self):self.assertEqual(len(x.corpus_report()['cross_family_weapon_inscriptions']),4)
 def test_soil_not_accessory(self):self.assertFalse(x.corpus_report()['soil_is_accessory'])
 def test_oil8_units(self):self.assertEqual(x.corpus_report()['oil_requirements_for_selected_cases'],8)
 def test_none_oil_from_reflexo(self):self.assertEqual(x.corpus_report({'REFLEXO_PROFUNDEZAS_P':2})['oil_requirements_for_selected_cases'],0)
 def test_demand_scaling(self):self.assertEqual(x.corpus_report({'RAIO_POENTE_B':4,'VEDACAO_P2':6})['oil_requirements_for_selected_cases'],10)
 def test_rank_bronze3(self):self.assertEqual(x.corpus_report()['rank_counts']['Bronze'],3)
 def test_rank_prata5(self):self.assertEqual(x.corpus_report()['rank_counts']['Prata'],5)
 def test_rank_ouro1(self):self.assertEqual(x.corpus_report()['rank_counts']['Ouro'],1)
 def test_knowledge_sim5(self):self.assertEqual(x.corpus_report()['knowledge_counts']['SIM'],5)
 def test_knowledge_nao1(self):self.assertEqual(x.corpus_report()['knowledge_counts']['NAO'],1)
 def test_knowledge_unknown3(self):self.assertEqual(x.corpus_report()['knowledge_counts']['NAO_INDICADO'],3)
 def test_unknown_not_no(self):self.assertNotEqual(x.CATALOG['RAIO_POENTE_B']['knowledge'],'NAO')
 def test_reflexo_not_quantified(self):self.assertFalse(x.CATALOG['REFLEXO_PROFUNDEZAS_P']['all_quantified'])
 def test_others_quantified(self):self.assertTrue(all(x.CATALOG[k]['all_quantified'] for k in x.CATALOG if k!='REFLEXO_PROFUNDEZAS_P'))
 def test_oil_all_ones(self):self.assertTrue(all(x.CATALOG[k]['oil']==1 for k in x.corpus_report()['oil_dependency_names']))
 def test_no_source_edit(self):self.assertFalse(x.corpus_report()['p2_recipe_edited'])
 def test_no_magic(self):self.assertEqual(x.corpus_report()['real_magic_acts'],0)
 def test_no_order(self):self.assertEqual(x.corpus_report()['r48_orders_created'],0)
 def test_no_pa(self):self.assertEqual(x.corpus_report()['pa_debits'],0)
 def test_no_party(self):self.assertEqual(x.corpus_report()['party_writes'],0)
 def test_no_primeiro(self):self.assertEqual(x.corpus_report()['o_primeiro_writes'],0)
 def test_f5_red(self):self.assertEqual(x.corpus_report()['f5'],'RED')
 def test_c19_unknown(self):self.assertEqual(x.corpus_report()['c19'],'UNKNOWN-EFFECT')
 def test_stock_not_zero_universe(self):self.assertEqual(x.corpus_report()['oil_world_stock_conclusion'],'UNKNOWN')
 def test_noil_not_authorized(self):self.assertFalse(x.route_decision(['REFLEXO_PROFUNDEZAS_P'])['ability_to_apply_now'])
 def test_oil_route_not_authorized(self):self.assertFalse(x.route_decision(['VEDACAO_P2'])['ability_to_apply_now'])
 def test_noil_path_false_ready(self):self.assertFalse(x.route_decision(['REFLEXO_PROFUNDEZAS_P'])['independent_research_paths'][0]['fully_quantified'])
 def test_unknown_rejected(self):
  with self.assertRaises(ValueError):x.corpus_report({'MISSING':1})
 def test_empty_list_rejected(self):
  with self.assertRaises(ValueError):x.route_decision([])
 def test_duplicate_candidate_rejected(self):
  with self.assertRaises(ValueError):x.route_decision(['VEDACAO_P2','VEDACAO_P2'])
 def test_bool_quantity_rejected(self):
  with self.assertRaises(ValueError):x.corpus_report({'VEDACAO_P2':True})
 def test_float_quantity_rejected(self):
  with self.assertRaises(ValueError):x.corpus_report({'VEDACAO_P2':1.5})
 def test_zero_quantity_rejected(self):
  with self.assertRaises(ValueError):x.corpus_report({'VEDACAO_P2':0})
 def test_all_refs_source(self):self.assertTrue(all(a['recipe_url'].startswith('https://app.notion.com/p/') for a in x.corpus_report()['source_evidence'].values()))
 def test_case_by_case_no_magic(self):self.assertFalse(any(a['magic_ever_observed_by_this_audit'] for a in x.corpus_report()['source_evidence'].values()))
 def test_no_factory_from_recipe(self):self.assertTrue(x.corpus_report()['uses_oil_not_equal_to_fabricated_oil'])
 def test_iron_three(self):self.assertEqual(x.corpus_report()['oil_recipe_current_iron_units'],3)
 def test_original_oil_conflicts(self):self.assertEqual(len(x.corpus_report()['oil_ingredient_process_conflicts']),3)
 def test_request_4_disjoint_surfaces(self):self.assertEqual(x.route_decision(['TERRA_FERTIL_P','RAIO_POENTE_B','REFLEXO_PROFUNDEZAS_P'])['oil_units_minimum_for_one_of_each'],2)
 def test_stress_27(self):self.assertEqual(x.stress(3)['synthetic_test_vectors'],27)

if __name__=='__main__':unittest.main()
