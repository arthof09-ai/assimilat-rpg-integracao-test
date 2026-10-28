#!/usr/bin/env python3
"""Narrow audit tests: reject speculative B15 PASS; oracle math is conditional only."""
import unittest, json, hashlib, zipfile
from pathlib import Path
import r13_oracle
D=Path(__file__).parent

def load(name):return json.loads((D/name).read_text(encoding='utf-8'))

class R24GateTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=load('R24_B15_ASSAY_AND_GATES.json');cls.sources=load('R24_SOURCE_CANDIDATE.json');cls.matrix=load('R24_MATRIX_18.json');cls.g=load('R24_BLOCKS_AND_AUTHORITIES.json')
 def test_source_count(self):self.assertEqual(len(self.sources['sources']),5)
 def test_ong_original_fiche(self):self.assertEqual(next(x for x in self.sources['sources'] if x['label']=='ONG_MASTER')['facts']['base_weapon_damage'],'3d6+6')
 def test_ong_fire_explicit(self):self.assertIn('+2d6',next(x for x in self.sources['sources'] if x['label']=='ONG_MASTER')['facts']['punhos_de_fogo'])
 def test_blue_dragon_specific(self):self.assertIn('ataques mágicos',next(x for x in self.sources['sources'] if x['label']=='BLUE_DRAGON')['facts']['weakness_exact'])
 def test_death_title_not_continuity(self):
  s=next(x for x in self.sources['sources'] if x['label']=='ONG_PARTY_MIRROR_STATUS');self.assertIn('Morto',s['facts']['title']);self.assertEqual(s['facts']['death_date'],'NOT_GIVEN')
 def test_synthetic_only(self):self.assertIn('NONCANONICAL',self.a['conditional_assay']['mode'])
 def test_no_actual_events(self):self.assertEqual(self.a['real_events_recovered'],0)
 def test_oracle_unchanged_import(self):self.assertEqual(r13_oracle.__name__,'r13_oracle')
 def test_oracle_3d6_enumeration(self):self.assertEqual(self.a['oracle_exact']['physical_3d6']['outcomes'],216)
 def test_oracle_2d6_enumeration(self):self.assertEqual(self.a['oracle_exact']['fire_base_2d6']['outcomes'],36)
 def test_oracle_3d6_mean(self):self.assertEqual(self.a['oracle_exact']['weakness_bonus_3d6']['mean'],10.5)
 def test_single_fixture_math(self):self.assertEqual(self.a['conditional_assay']['conditional_gross_arithmetic']['with_weakness_raw'],37)
 def test_no_weakness_control(self):self.assertEqual(self.a['conditional_assay']['conditional_gross_arithmetic']['without_weakness_raw'],24)
 def test_bonus_fire_only(self):self.assertTrue(self.a['conditional_assay']['conditional_gross_arithmetic']['bonus_is_only_fire'])
 def test_no_double_infusion(self):self.assertTrue(any('do not add +1d8' in x for x in self.a['conditional_assay']['no_presumptions']))
 def test_no_assumed_tag(self):self.assertEqual(self.a['conditional_assay']['not_determined']['physical_damage_tag'],'UNKNOWN')
 def test_no_assumed_hp_delta(self):self.assertEqual(self.a['conditional_assay']['not_determined']['target_hp_after'],'UNKNOWN')
 def test_no_event_receipt(self):self.assertEqual(self.a['conditional_assay']['not_determined']['real_combat'],'NO')
 def test_reject_illegal_legality(self):self.assertEqual(self.a['conditional_assay']['not_determined']['punhos_with_soqueira_legal'],'UNKNOWN')
 def test_matrix_18(self):self.assertEqual(len(self.matrix['rows']),18)
 def test_predicates_stable(self):
  prior=load_parent_matrix()
  self.assertEqual({x['criterion']:x['predicado_original'] for x in prior},{x['criterion']:x['predicado_original'] for x in self.matrix['rows']})
 def test_no_new_cert(self):self.assertEqual(self.matrix['certified_total'],1)
 def test_only_b02_pass(self):self.assertEqual([r['criterion'] for r in self.matrix['rows'] if 'PASS' in r['estado_R24']],['B02'])
 def test_all_decisions_pending(self):self.assertTrue(all(s=='PENDENTE_MESTRE' for s in self.g['decisions'].values()))
 def test_no_originals(self):self.assertEqual(self.g['i0003']['original_bytes_verified'],0)
 def test_no_csv_recount(self):self.assertEqual((self.g['i0003']['historical_ids'],self.g['i0003']['formula_occurrences'],self.g['i0003']['formula_source_pages']),(198,46,20))
 def test_strict_zero(self):self.assertEqual(self.g['strict_full_fights']['certified'],0)
 def test_master_and_party_safe(self):self.assertEqual((self.g['notion_writes'],self.g['party_first_write'],self.g['vlab_engine_changes']),(0,0,0))
 def test_nac_hold(self):self.assertEqual(self.matrix['nac_pass_terminal'],'HOLD')
 def test_prereg_actor_eligibility(self):self.assertEqual(self.sources['current_actor_eligibility'],'NOT_PROVEN_PARTY_MIRROR_SAYS_MORTO')

def load_parent_matrix():
 with zipfile.ZipFile(D/'R23_ORIGINAL_READONLY.zip') as z:
  return json.loads(z.read('DMG_R23_DECISORIO_SANDBOX/R23_B01_B18_MATRIX.json'))['rows']

if __name__=='__main__':unittest.main()
