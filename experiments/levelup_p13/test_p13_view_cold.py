import json, unittest
from pathlib import Path
D=json.loads((Path(__file__).parent/'ORC_P13_25_LEVELS_20_TRANSFORMATIONS_FIELD_CORRECTED_VIEW.json').read_text())
class ViewContract(unittest.TestCase):
 def test_25_normal(self):self.assertEqual(len(D['profiles']),25)
 def test_20_transform(self):self.assertEqual(sum(t['available'] for t in D['transformations']),20)
 def test_80_item_test_only(self):self.assertEqual(sum(len(v) for v in D['gear_ranked'].values()),80)
 def test_no_false_canon(self):self.assertFalse(D['world_canon']);self.assertFalse(D['VLAB_accepted'])
 def test_all_attack_separated(self):
  for p in D['profiles']:
   with self.subTest(level=p['ordinal']):
    x=p['FULL']['combat_attack_dme_preview_TEST'];self.assertTrue(x['physical_attack_expression']==x['physical_dice']);self.assertTrue(x['attack_test_separate_not_damage_TEST']);self.assertIn('original_P12_RETAINED_HISTORY','physical_attack_expression_original_P12_RETAINED_HISTORY');self.assertEqual(x['FOR_damage_bonus_applied'],0)
 def test_pa_and_transform(self):
  for p,t in zip(D['profiles'],D['transformations']):
   with self.subTest(level=p['ordinal']):
    self.assertEqual(p['pa_max_with_rings'],p['natural_pa']+100);self.assertEqual(p['FULL']['daily_pa_two_soul_rings_TEST'],0);self.assertEqual(p['FULL']['pa_free'],p['pa_max_with_rings']-p['FULL']['daily_pa_items'])
    if t['available']:
     self.assertEqual(t['tap_total_distributed'],11*p['ordinal']);self.assertEqual(sum(t['tap_allocation'].values()),t['tap_total_distributed'])
 def test_source_provenance(self):self.assertTrue(D['P13_base_source_sha256']);self.assertEqual(D['Party_writes'],0)
if __name__=='__main__':unittest.main()