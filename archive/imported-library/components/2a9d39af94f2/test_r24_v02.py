import unittest,json,zipfile
from pathlib import Path
D=Path(__file__).parent
class V02Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.j=json.loads((D/'R24_V02_JAKU_B15_EVIDENCE.json').read_text());cls.a=cls.j['assay'];cls.s=cls.j['sources']
 def test_same_owner(self):self.assertIn('same inventory', ' '.join(self.s['JAKU_NADTA_MASTER']['claims_verified']))
 def test_weapon(self):self.assertTrue(any('2d8+2' in x for x in self.s['JAKU_NADTA_MASTER']['claims_verified']))
 def test_explicit_fire(self):self.assertIn('1d8+2', ' '.join(self.s['MANOPLAS_CATALOG']['claims_verified']))
 def test_magic_weapon(self):self.assertTrue(any('magical' in x for x in self.s['MANOPLAS_CATALOG']['claims_verified']))
 def test_magic_fire_target(self):self.assertTrue(any('ataques mágicos' in x for x in self.s['BLUE_DRAGON']['claims_verified']))
 def test_roll_delta(self):self.assertEqual((self.a['conditional_gross']['without_weakness'],self.a['conditional_gross']['with_weakness']),(18,32))
 def test_expected_delta(self):self.assertEqual(self.a['exact_expectation']['delta'],13.5)
 def test_missing_rider_stack(self):self.assertIn('NOT INCLUDED',self.a['separate_wpn_rider_unknown'])
 def test_bonus_action_unmapped(self):self.assertTrue(any('Bonus action' in x for x in self.a['specific_unsatisfied']))
 def test_no_event(self):self.assertEqual(self.j['real_events_count'],0)
 def test_b15_partial(self):self.assertEqual(self.j['B15'],'PARTIAL')
 def test_master_decisions(self):self.assertEqual(self.j['decisions_master'],'0/5 pending')
 def test_nac_strict(self):self.assertEqual(self.j['strict'],[0,2])
 def test_csv_originals(self):self.assertEqual(self.j['i0003'],[0,9])
 def test_no_notion_writes(self):self.assertEqual(self.j['notion_writes'],0)
if __name__=='__main__':unittest.main()
