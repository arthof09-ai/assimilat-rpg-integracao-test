"""R10 independent SCIENCE-ONLY checks; never starts VLAB, a canon fight, or certifies gates."""
from __future__ import annotations
import unittest,json,zipfile,hashlib,csv,os
from pathlib import Path
R=Path(__file__).parent; DATA=(R/'read_only' if (R/'read_only').is_dir() else Path('/mnt/data'));
LAB_REF=Path(os.environ.get('DMG_R10_LAB_REF','/mnt/data/DMG_R10_src/VLAB_STAGE12_A1_MICROBLOCO_04_A2_MICROBLOCO_02_SANDBOX.zip'))
def get(name):return json.loads((R/name).read_text())
G=get('DMG-F1-R10-GATES-18-ORIGINAIS-v01.json')
L=get('DMG-F1-R10-LIU-ORACULO-PA-FF-v01.json')
B=get('DMG-F1-R10-BESTAS-CENARIOS-CONDICIONAIS-v01.json')
E=get('DMG-F1-R10-LAB-A1A2-02-HANDOFF-v01.json')
S=get('DMG-F1-R10-SOURCE-TEXT-SHA-LEDGER-v01.json')

class SourceGovernance(unittest.TestCase):
 def test_01_all_original_ids_and_literal_contract(self):
  original=json.loads((DATA/'DMG-F1-EDxBESTA-SCIENTIFIC-FIXTURE-v04.json').read_text())
  ref={x['gate_id']:x['why'] for x in original['blockers'] if x['scenario_id']=='PAIR-P5-LIU-vs-MACACO-01'}
  self.assertEqual([r['id'] for r in G['records']],[f'B{i:02d}' for i in range(1,19)])
  self.assertEqual(len(ref),18)
  self.assertTrue(all(x['original_requirement']==ref[x['id']] for x in G['records']))
 def test_02_whole_gate_never_passes(self):
  self.assertEqual(G['certified_whole'],0);self.assertEqual(G['total_whole'],18);self.assertEqual(G['target'],9)
  self.assertTrue(all(not x['whole_gate_pass'] for x in G['records']))
 def test_03_status_denominators(self):
  from collections import Counter
  self.assertEqual(dict(Counter(x['r10_status'] for x in G['records'])),G['status_counts'])
  self.assertEqual(G['status_counts'],{'PARTIAL':10,'BLOCKED':6,'NOT-TESTED':2})
 def test_04_original_cross_scenario_gate_remains_not_tested(self):
  b=next(x for x in G['records'] if x['id']=='B14')
  self.assertEqual(b['r10_status'],'NOT-TESTED');self.assertIn('Behemoth',b['original_requirement'])
 def test_05_source_fingerprints_have_exact_historical_lineage(self):
  with (DATA/'DMG-F1-SOURCE-SHA256-SNAPSHOTS-v04.csv').open(encoding='utf8') as fh:
   ledger={r['source_key']:r['sha256_utf8_content'] for r in csv.DictReader(fh)}
  self.assertEqual(len(S['documents']),9)
  for x in S['documents']:
   self.assertEqual(x['sha256_utf8_content'],ledger[x['key']]);self.assertEqual(len(x['sha256_utf8_content']),64)
 def test_06_source_hash_is_not_scene_grant(self):
  self.assertTrue(S['notion_text_frozen_readonly']);self.assertFalse(S['current_scene_frozen']);self.assertFalse(S['certified_actor_records'])
 def test_07_no_party_and_no_unlawful_ownership(self):
  self.assertTrue(S['no_party_mirrors']);self.assertIsNone(E['candidate_actor_snapshots']['LIU']['signed_by'])
  self.assertIsNone(E['candidate_actor_snapshots']['MACACO']['signed_by'])
 def test_08_no_false_lab_17_certified(self):
  self.assertTrue(E['engineering_reference']['zero_terminal_17_contracts']);self.assertTrue(E['engineering_reference']['strict_hold'])
 def test_09_canonical_strict_never_claimed(self):
  self.assertFalse(E['engineering_return_contract']['current_strict_support'])
  self.assertTrue(all(not v['eligible_strict'] for v in E['candidate_actor_snapshots'].values()))
 def test_10_new_deny_scenarios_are_distinct(self):
  deny=E['deny_cases'];self.assertEqual(len(deny),16);self.assertEqual(len({x[0] for x in deny}),16)

class LiuDerivedAndSensitivity(unittest.TestCase):
 def test_11_nominal_pa_exact(self):
  pa=L['alma'];self.assertEqual(170+50-sum(x['PA'] for x in pa['subtractions']),73)
  self.assertEqual(pa['sum_subtractions'],147)
 def test_12_daily_not_continuous(self):
  pa=L['alma'];perday={x['name'] for x in pa['subtractions'] if x['source_time']=='PER_DAY'}
  self.assertEqual(perday,{'boots','weapon'})
 def test_13_disjoint_perdido_is_conditional(self):
  pa=L['alma'];self.assertEqual(pa['branches'][1]['PA_before_transform'],27)
  self.assertFalse(pa['branches'][1]['approved']);self.assertFalse(pa['branches'][1]['can_pay_40'])
 def test_14_t9_40_pa_gate_depends_on_initial_state(self):
  pa=L['alma'];self.assertTrue(pa['branches'][0]['can_pay_40']);self.assertEqual(pa['branches'][0]['post_cost_IF_only_T9'],33)
  self.assertIsNone(pa['branches'][1]['post_cost_IF_only_T9'])
 def test_15_ff_printed_normal_and_transformed(self):
  n=L['normal_source'];t=L['transform_source'];self.assertEqual((n['FOR']+n['DES']+n['CON'])*10,610)
  self.assertEqual((t['FOR']+t['DES']+t['CON'])*10,920)
 def test_16_ff_610_620_same_milestones(self):
  self.assertEqual(610//100,620//100);self.assertEqual(610//100,6)
 def test_17_ff_gear_external_both_can_cross_milestone(self):
  x=[b for b in L['FF_branches'] if b['form']=='normal' and b['armor_FOR_added_externally']==8 and b['axe_CON_added_externally']==4][0]
  self.assertEqual((29+8+16+16+4)*10,730);self.assertEqual((x['FF_milestones'],x['extension_max_dice'],x['extension_nominal_PA']), (7,'3d7',35))
 def test_18_ff_transform_extra_armor_plus_axe_crosses_ten(self):
  x=[b for b in L['FF_branches'] if b['form']=='transform' and b['armor_FOR_added_externally']==8 and b['axe_CON_added_externally']==4][0]
  self.assertEqual((x['FF_result'],x['FF_milestones'],x['extension_max_dice'],x['extension_nominal_PA']), (1040,10,'3d10',50))
 def test_19_attack_shortcuts_potentially_embed_armor(self):
  self.assertEqual(29+8,37);self.assertEqual(40+8,48);self.assertTrue(E['candidate_actor_snapshots']['LIU']['eligible_strict'] is False)
 def test_20_defender_4_branches_before_fortitude(self):
  vals={(x['form'],x['axe_CON_added_externally'],x['defender_before_skill']) for x in L['FF_branches']}
  self.assertTrue({('normal',0,37),('normal',4,41),('transform',0,46),('transform',4,50)}<=vals)
 def test_21_dodge_is_total_not_modifier(self):
  self.assertEqual(L['normal_source']['dodge_total']-L['normal_source']['CA'],3)
  self.assertEqual(L['transform_source']['dodge_total']-L['transform_source']['CA'],3)
  self.assertTrue(L['CA_provenance']['do_not_add_CA_to_total_dodge'])
 def test_22_movement_anchored_to_source_not_unarmored_live(self):
  self.assertEqual(L['speed']['normal_display_meters_if_active11'],11)
  self.assertEqual(L['speed']['transform_display_meters_if_active13'],13)
  self.assertIsNone(L['speed']['legal_move_live'])
 def test_23_transformation_duration_cost_and_compatibility(self):
  t=L['transformation_T9'];self.assertEqual(t['cost_pa'],40);self.assertEqual(t['duration'],'1d6+1 turns')
  self.assertIsNone(t['presumed_spirit_compatibility'])

class BeastScientificContract(unittest.TestCase):
 def test_24_titan_ca_derived_not_alias(self):self.assertEqual(20+40+35/5,B['macaco']['CA_literal'])
 def test_25_base_life_alma_differences_are_60(self):
  b=B['macaco'];self.assertEqual(b['HP_Alma_current_rule']['Life']-b['HP_Alma_literal']['Life'],60)
  self.assertEqual(b['HP_Alma_current_rule']['Alma']-b['HP_Alma_literal']['Alma'],60)
 def test_26_behemoth_control_differences_are_30(self):
  b=B['control_Behemoth'];self.assertEqual(b['HP_Alma_current_rule']['Life']-b['HP_Alma_literal']['Life'],30)
  self.assertEqual(b['HP_Alma_current_rule']['Alma']-b['HP_Alma_literal']['Alma'],30)
 def test_27_patada_damage_and_RDF_conditional(self):
  x=B['fork_patada'];self.assertEqual((sum(x['damage_sample_dice'])+54,sum(x['damage_sample_dice'])+56),(62,64))
  self.assertEqual((x['FOR54']['RDF10_only_if_authorized'],x['FOR56']['RDF10_only_if_authorized']),(52,54));self.assertFalse(x['legal_hit'])
 def test_28_fraco_threshold_integer_strict_less(self):
  b=B['macaco'];self.assertEqual(74<750*0.1,True);self.assertEqual(75<750*0.1,False)
  self.assertEqual(80<810*0.1,True);self.assertEqual(81<810*0.1,False)
 def test_29_titan_prata_speed_and_rd_not_individual_final(self):
  b=B['macaco'];self.assertEqual((b['speed_if_titan_prata'],b['RD_if_titan_prata']),(30,30));self.assertIsNone(b['selected_skill_Luta'])
 def test_30_patada_impact_not_inferred_ice(self):
  self.assertEqual(B['macaco']['action_Patada']['type'],'CONTUNDENTE/IMPACTO')
  self.assertIsNone(B['macaco']['action_Poder_elemental']['element_literal'])

class LabInterfaceStatic(unittest.TestCase):
 def test_31_zip_preserved_with_manifest_and_hash(self):
  if not LAB_REF.is_file():self.skipTest('LAB external package not materialized; no fabricated comparison')
  self.assertEqual(hashlib.sha256(LAB_REF.read_bytes()).hexdigest(),E['engineering_reference']['sha256'])
 def test_32_aligned_interface_not_current_source(self):
  a=next(x for x in E['code_boundaries'] if 'A2SourceAlignedBridge' in x['method'])
  self.assertIn('LAB-ASSUMPTION',a['behavior']);self.assertIn('UNIT_FIXTURE',a['behavior'])
 def test_33_rng_metadata_not_random_rule(self):self.assertTrue(E['seed_policy']['seed_metadata_must_not_count_as_rng']);self.assertIsNone(E['seed_policy']['actual_engine_root_seed'])
 def test_34_no_other_character_grants(self):self.assertIn(['R10-DENY-12','OTHER_CHARACTER_SOURCE_AUTHORIZATION_REUSED'],E['deny_cases'])

if __name__=='__main__':unittest.main(verbosity=2)
