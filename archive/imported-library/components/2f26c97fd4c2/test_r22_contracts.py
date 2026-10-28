"""R22 focused falsification tests: clinical contract evidence, NOT combat official replay."""
import unittest, zipfile, hashlib, json
from fractions import Fraction
from pathlib import Path
from r13_oracle import crit_check,all_critical_outcomes,Rejected
HERE=Path(__file__).resolve().parent
j=lambda fn:json.loads((HERE/fn).read_text())

class TestCriticalLegality(unittest.TestCase):
 def setUp(self):self.x=j('R22_B11_B12_B15_RESOLUTIONS.json')['B11']
 def test_base_crit_exact(self):self.assertEqual(all_critical_outcomes(),2)
 def test_sequence_good(self):self.assertTrue(crit_check((6,6,5)));self.assertTrue(crit_check((6,6,6)))
 def test_out_of_order_rejected(self):self.assertFalse(crit_check((6,5,6)));self.assertFalse(crit_check((5,6,6)))
 def test_margin_5_rejected(self):
  with self.assertRaises(Rejected):crit_check((6,6,4),margin=5)
 def test_patada_additive_max_not_multiplication(self):self.assertEqual(self.x['patada_physical_conditional']['canonical_formula_when_eligible'],'2d6+66');self.assertEqual(self.x['patada_physical_conditional']['max_dice'],12)
 def test_magic_does_not_inherit_physical_critical(self):self.assertFalse(self.x['magic']['default_crit_allowed']);self.assertTrue(self.x['magic']['exception_required'])
 def test_legacy_brutal_operator_unknown(self):self.assertIsNone(self.x['liu_brutal']['derived_multiplier_operator'])
 def test_liu_decep_18_not_other_30(self):self.assertEqual(self.x['liu_decepadora']['printed_extra_cutting'],18);self.assertEqual(self.x['liu_decepadora']['other_instance_extra'],30);self.assertFalse(self.x['liu_decepadora']['cross_item_inheritance_allowed'])
 def test_decep_mounted_axe_text_sword(self):self.assertIn('espada',self.x['liu_decepadora']['mounting_conflict'])
 def test_two_checks_probability_conditional_not_scene(self):self.assertEqual(self.x['if_two_independent_default_check_sequences_purely_math']['base_crit_then_second_conditional']['fraction'],'1/11664');self.assertFalse(self.x['new_full_pass'])
 def test_master_decisions_no_auto_choice(self):self.assertEqual(len(self.x['smallest_master_decisions']),3);self.assertTrue(all(d['not_auto_choice'] for d in self.x['smallest_master_decisions']))

class TestPoisonSemantics(unittest.TestCase):
 def setUp(self):self.x=j('R22_B11_B12_B15_RESOLUTIONS.json')['B12']
 def test_source_cd_save(self):self.assertIn('CD25',self.x['serpente']['trigger'])
 def test_exact_tick_mean(self):self.assertEqual(self.x['one_conditional_tick_expected']['fraction'],'39/2')
 def test_one_tick_support_only(self):self.assertEqual(self.x['serpente']['tick_min'],3);self.assertEqual(self.x['serpente']['tick_max'],36);self.assertIsNone(self.x['full_duration_expected'])
 def test_refresh_without_known_numeric_duration(self):self.assertFalse(self.x['reapplication']['distinct_stacks_allowed']);self.assertFalse(self.x['reapplication']['known_duration_to_renew'])
 def test_do_not_import_1_minute(self):self.assertTrue(self.x['other_item_counterexamples'][0]['not_transferable']);self.assertIsNone(self.x['serpente']['duration_turns'])
 def test_do_not_import_cd80(self):self.assertTrue(self.x['other_item_counterexamples'][1]['not_transferable']);self.assertIsNone(self.x['serpente']['repeat_save'])
 def test_no_immunity_imputed(self):self.assertFalse(self.x['serpente']['immunity_target_confirmed']);self.assertIsNone(self.x['immunity_interlock']['target_poison_immunity']);self.assertEqual(self.x['immunity_interlock']['immediate_weapon_damage_tag'],'UNKNOWN')
 def test_legacy_pre_migration_missing_duration(self):
  x=j('R22_SERPENTE_LEGACY_COMPARISON.json')
  self.assertNotEqual(x['canonical_current'],x['historical_deleted'])
  self.assertTrue(all(z['canonical']==z['archived'] and z['equal'] for z in x['mechanical_fields']))
  self.assertIsNone(next(z['canonical'] for z in x['mechanical_fields'] if z['name']=='duration_numeric'))
  self.assertEqual(self.x['historical_origin']['status'],'ARCHIVAL_NOT_CURRENT_CANON')
 def test_no_full_pass(self):self.assertEqual(self.x['verdict'],'PARTIAL');self.assertFalse(self.x['new_full_pass'])

class TestElementalSemantics(unittest.TestCase):
 def setUp(self):self.x=j('R22_B11_B12_B15_RESOLUTIONS.json')['B15']
 def test_exact_normal_mean(self):self.assertEqual(self.x['mixed_example']['mean_normal']['fraction'],'23/2')
 def test_exact_weak_mean(self):self.assertEqual(self.x['mixed_example']['mean_weak']['fraction'],'22')
 def test_only_fire_extra(self):self.assertEqual(self.x['mixed_example']['increase']['fraction'],'21/2');self.assertEqual(self.x['mixed_example']['physical'],'1d8')
 def test_no_poison_to_fire_conversion(self):self.assertIn('veneno',self.x['negative_cases'][0]['trigger'])
 def test_no_impact_to_fire_conversion(self):self.assertEqual(self.x['negative_cases'][1]['verdict'],'NO_ELEMENTAL_BONUS')
 def test_unknown_weapon_name_tag_rejected(self):self.assertIn('REJECT',self.x['negative_cases'][2]['verdict'])
 def test_need_real_target_weakness_and_scene(self):self.assertEqual(len(self.x['full_predicate_blockers']),4);self.assertFalse(self.x['new_full_pass'])

class TestEvidenceIntegrity(unittest.TestCase):
 def test_source_excerpt_hashes_and_full_page_sha_missing(self):
  for r in j('R22_SOURCE_EXCERPTS.json')['sources']:
   b=json.dumps(r['claims'],ensure_ascii=False,sort_keys=True).encode()
   self.assertEqual(hashlib.sha256(b).hexdigest(),r['snippet_hash_sha256'])
   self.assertIsNone(r['notion_full_page_sha256']);self.assertFalse(r['source_frozen_for_real_scene'])
 def test_no_false_original_certification(self):self.assertEqual(j('R22_I0003_FOCUSED_AUDIT.json')['original_I0003_authenticated'],'0/9')
 def test_no_false_scene_certification(self):
  x=j('R22_LIU_SCENE_AND_STRICT_GAPS.json');self.assertEqual(x['B04_B09']['recovered_real_event_receipts'],0)
  self.assertEqual(x['STRICT_1_LIU_MACACO']['complete_signed_real_event_count'],0)
 def test_source_readback_ibx_is_not_ack(self):self.assertIn('sem INSTANCE-ID/writer',j('R22_SOURCE_EXCERPTS.json')['sources'][-1]['claims']['governance'])
 def test_matrix_original_predicates_and_denominators(self):
  x=j('R22_B01_B18_MATRIX.json'); self.assertEqual(len(x['rows']),18)
  self.assertEqual((x['certified_full_count'],x['full_strict_fights']),(1,0))
  self.assertEqual(sorted({r['criterion'] for r in x['rows']}),[f'B{i:02d}' for i in range(1,19)])
  self.assertTrue(all(r['state_before_R22']==r['state_after_R22'] for r in x['rows']))
 def test_directed_recovery_not_broad_repeat(self):
  x=j('R22_I0003_FOCUSED_AUDIT.json');self.assertEqual(x['R22_NEW_LOCATOR'],'NONE');self.assertIn('suspended',x['decision'])
 def test_R21_parent_sha(self):
  p=HERE/'R21_ORIGINAL_READONLY.zip'
  self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),'06d7a30aa2ae9d9c482ae69c9e8c912741334a8a99e784d66546dd5167ccf3ba')
  with zipfile.ZipFile(p) as z:self.assertIsNone(z.testzip())

if __name__=='__main__':unittest.main()
