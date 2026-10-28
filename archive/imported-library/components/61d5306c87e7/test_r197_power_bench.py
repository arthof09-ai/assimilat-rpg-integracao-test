"""R197 scoped tests, not R196 historical combat replays."""
import copy,json,pathlib,tempfile,unittest
from fractions import Fraction
from r197_power_bench import load,report,generate,dice_stats,dice_sum_prob,hit_prob,legacy_safety_check,expected_post_rd,rank_peers
SRC=load()
ACT={a['id']:a for a in SRC['actors']}
class PowerBenchTests(unittest.TestCase):
 def test_snapshot_nine(self):self.assertEqual(len(ACT),9)
 def test_concha_damage(self):self.assertEqual(dice_stats(ACT['CONCHA_P1']['attack'])['mean'],40.5)
 def test_tigris_damage(self):self.assertEqual(dice_stats(ACT['TIGRIS_P1']['attack'])['mean'],31)
 def test_same_rank_star_five(self):self.assertEqual(len(rank_peers(ACT['CONCHA_P1'],SRC['actors'])),5)
 def test_prata_five_titan_not_pooled(self):self.assertEqual(len(rank_peers(ACT['MACACO_P5'],SRC['actors'])),1)
 def test_profile_median_dmg(self):self.assertEqual(report(ACT['CONCHA_P1'],SRC['actors'])['peer_comparison']['damage_mean']['sample_median'],30)
 def test_percent_35(self):self.assertEqual(report(ACT['CONCHA_P1'],SRC['actors'])['peer_comparison']['damage_mean']['percent_difference'],35)
 def test_hp_median(self):self.assertEqual(report(ACT['CONCHA_P1'],SRC['actors'])['peer_comparison']['hp']['sample_median'],216)
 def test_concha_skill_lost_hit(self):
  r=report(ACT['CONCHA_P1'],SRC['actors'],target_ca=46)['target_ca_analysis']['branches']
  self.assertEqual(r['untrained']['hit_probability_excluding_critical'],0)
  self.assertAlmostEqual(r['trained_if_confirmed']['hit_probability_excluding_critical'],10/36)
 def test_hit_tie_favors_defense(self):self.assertEqual(hit_prob([2,6],30,42),Fraction(0))
 def test_certain_hit(self):self.assertEqual(hit_prob([2,6],193,40),Fraction(1))
 def test_dice_prob_sum(self):self.assertEqual(sum(dice_sum_prob(6,6).values()),Fraction(1))
 def test_mean_after_rd_if_damage_all_physical(self):self.assertEqual(expected_post_rd(ACT['CONCHA_P1']['attack'],15),Fraction(51,2))
 def test_unknown_damage_type_not_promoted(self):
  r=report(ACT['CONCHA_P1'],SRC['actors'],target_rd=15)
  self.assertEqual(r['conditional_rd_projection']['status'],'SCENARIO_ASSUME_ALL_DAMAGE_AFFECTED_BY_THIS_RD')
  self.assertEqual(r['attack']['damage_type'],'UNKNOWN')
 def test_no_power_index(self):self.assertIsNone(report(ACT['AUREN_L3'],SRC['actors'])['power_index'])
 def test_existing_guard(self):self.assertFalse(legacy_safety_check()['historical_rank_change_authorized'])
 def test_degenerate_peer_single_no_rank_claim(self):
  r=report(ACT['AUREN_L3'],SRC['actors']);self.assertEqual(r['peer_cohort']['n'],1)
  self.assertIn('REFERENCE_SPARSE',r['recommendation'])
 def test_duplicate_id_rejected(self):
  s=copy.deepcopy(SRC);s['actors'].append(copy.deepcopy(s['actors'][0]))
  with tempfile.TemporaryDirectory() as t:
   p=pathlib.Path(t)/'src.json';p.write_text(json.dumps(s))
   with self.assertRaisesRegex(ValueError,'DUPLICATE_SOURCE_ID'):load(p)
 def test_fake_source_url_rejected(self):
  s=copy.deepcopy(SRC);s['actors'][0]['url']='https://fake.example.org'
  with tempfile.TemporaryDirectory() as t:
   p=pathlib.Path(t)/'src.json';p.write_text(json.dumps(s))
   with self.assertRaisesRegex(ValueError,'PROVENANCE_MISSING'):load(p)
 def test_negative_life_rejected(self):
  s=copy.deepcopy(SRC);s['actors'][0]['hp']=-5
  with tempfile.TemporaryDirectory() as t:
   p=pathlib.Path(t)/'src.json';p.write_text(json.dumps(s))
   with self.assertRaisesRegex(ValueError,'INVALID_SOURCE_STATS'):load(p)
 def test_rank_no_reclassification(self):
  o=generate();self.assertEqual(o['official_contracts_certified'],0);self.assertEqual(o['official_benchmark_cells'],0)
  self.assertTrue(all(not x['rank_reclassification_authorized'] for x in o['actors']))
 def test_stable_profile_generation(self):self.assertEqual(generate(),generate())
 def test_lobo_effect_not_included(self):self.assertEqual(dice_stats(ACT['LOBO_P1']['attack'])['mean'],27.5)
 def test_special_ability_not_auto_activated(self):self.assertIsNone(ACT['BEHEMOTH_P5']['attack']['cost_pa'])
if __name__=='__main__':unittest.main(verbosity=2)
