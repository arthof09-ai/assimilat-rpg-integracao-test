import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import readiness_delta as q

class ReadinessTests(unittest.TestCase):
 def test_minimal_salt_patch_still_proposed(self):self.assertFalse(q.p2_decision_packet()['issue_1']['resolved'])
 def test_energy_has_seven_authority_parameters(self):self.assertEqual(len(q.p2_decision_packet()['issue_2']['minimum_authority_fields']),7)
 def test_energy_options_remain_exclusive(self):self.assertEqual(set(q.p2_decision_packet()['issue_2']['BOM_exclusive_branches']),{'Pedra da Luz','Pote de Essência Mágica'})
 def test_oil_current_iron_three(self):self.assertEqual(q.oil_findings()['current_bom']['Pó de Ferro Celestial'],3)
 def test_oil_historical_iron_two(self):self.assertEqual(q.oil_findings()['historical_iron_units'],2)
 def test_oil_lot_not_assumed(self):self.assertEqual(q.oil_findings()['verified_qualified_lots_in_that_scope'],0)
 def test_oil_absence_not_global(self):self.assertFalse(q.oil_findings()['stock_worldwide_assessed'])
 def test_h23_15_fields(self):self.assertEqual(q.h23_filled_dossier()['field_count'],15)
 def test_h23_rejects_apply(self):self.assertEqual(q.h23_filled_dossier()['h23a'],'HOLD_NO_APPLICATION')
 def test_h23_not_fictitiously_effective(self):self.assertEqual(q.h23_filled_dossier()['h23b'],'NOT_REACHABLE')
 def test_no_current_materiality(self):self.assertFalse(q.refine_geometry()['physical_pass'])
 def test_existing_geometry_eight_keys(self):self.assertEqual(len(q.refine_geometry()['eight_existing_geometry_keys']),8)
 def test_eight_new_material_checks(self):self.assertEqual(len(q.refine_geometry()['new_review_requirements']),8)
 def test_geometry_all_claims_still_review(self):
  g={k:1.0 for k in q._GEOMETRY.REQUIRED}
  evidence={k:'synthetic_fixture' for k in q.refine_geometry()['new_review_requirements']}
  self.assertFalse(q.refine_geometry(g,evidence)['physical_pass'])
 def test_geometry_rejects_incompatible_sizes(self):
  g={k:1.0 for k in q._GEOMETRY.REQUIRED};g['crystal_aperture_mm']=0.5
  self.assertEqual(q.refine_geometry(g,{})['existing_geometry']['state'],'SCHEMATIC_CONSTRAINTS_FAIL')
 def test_causal_count_16(self):self.assertEqual(len(q.h25_causal_controls()['arms']),16)
 def test_causal_unique_arms(self):self.assertEqual(len(set(a['control_id'] for a in q.h25_causal_controls()['arms'])),16)
 def test_causal_has_p2_own_energy_without_crystal_herb(self):
  self.assertTrue(any(a['p2_inscription'] and a['p2_own_energy'] and not a['crystal'] and not a['herb'] for a in q.h25_causal_controls()['arms']))
 def test_causal_has_no_p2_with_energy_confound(self):
  self.assertTrue(any(not a['p2_inscription'] and a['p2_own_energy'] for a in q.h25_causal_controls()['arms']))
 def test_causal_review_default_holds(self):self.assertEqual(q.causal_review()['review_gate'],'HOLD_CAUSAL_DEPENDENCIES')
 def test_causal_review_even_forged_all_passes_no_auto_magic(self):
  kwargs={k:True for k in q.causal_review()['missing_conditions']}
  result=q.causal_review(kwargs)
  self.assertNotIn('INTEGRATED',result['review_gate'])
  self.assertEqual(result['item_integrated'],'NOT_CLAIMED')
 def test_no_residual_proof_shortcut(self):self.assertFalse(q.causal_review({'residual_observed':True})['raw_residual_is_sufficient'])
 def test_five_families(self):self.assertEqual(len(q.FAMILIES),5)
 def test_family_unknown_fails_closed(self):self.assertEqual(q.family_review('MAGIA_AVULSA')['status'],'UNKNOWN_FAMILY')
 def test_family_weapon_has_integrity(self):self.assertIn('integrity_test',q.family_review('ARMA')['requirements'])
 def test_family_armor_has_mobility(self):self.assertIn('mobility_test',q.family_review('ARMADURA')['requirements'])
 def test_family_accessory_has_slot(self):self.assertIn('body_or_slot',q.family_review('ACESSORIO')['requirements'])
 def test_family_artifact_requires_replicability(self):self.assertIn('replicability_class',q.family_review('ARTEFATO')['requirements'])
 def test_family_inscription_requires_pattern(self):self.assertIn('authenticated_pattern',q.family_review('INSCRICAO')['requirements'])
 def test_family_claims_cannot_promote(self):
  for k,v in q.FAMILIES.items():
   with self.subTest(k=k):
    result=q.family_review(k,{x:'FAKE' for x in v['requirements']})
    self.assertFalse(result['magical_fabrication_proven']);self.assertFalse(result['rc5'])
 def test_scope_r48_freeze(self):self.assertFalse(q.run_actual_readonly()['R48_replayed'])
 def test_scope_official_writes(self):self.assertEqual(q.run_actual_readonly()['official_recipe_writes'],0)
 def test_scope_pa(self):self.assertFalse(q.run_actual_readonly()['pa_engine_changed'])
 def test_scope_party(self):self.assertEqual(q.run_actual_readonly()['party_writes'],0)
 def test_scope_production(self):self.assertEqual(q.run_actual_readonly()['production'],'HOLD')
 def test_guard_still_denies_on_empty(self):self.assertFalse(q.run_actual_readonly()['source_guard_result']['authorization_to_apply'])

# 16 parametrized cases: no proposed control is an observed magical scene.
for _i,_arm in enumerate(q.h25_causal_controls()['arms']):
 def _case(self, i=_i):
  a=q.h25_causal_controls()['arms'][i]
  self.assertFalse(a['safe_executable_now']);self.assertEqual(a['outcome'],'NOT_OBSERVED')
 setattr(ReadinessTests, f'test_arm_{_i:02d}', _case)

if __name__=='__main__':unittest.main(verbosity=2)
