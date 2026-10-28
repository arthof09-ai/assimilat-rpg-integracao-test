from pathlib import Path
import copy,csv,sys,unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from audit import notion_uuid,audit
R=Path(__file__).resolve().parents[1]
class TestComparatorAudit(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  with (R/'inputs'/'peer12_frozen.csv').open(encoding='utf-8-sig',newline='') as f:cls.rows=list(csv.DictReader(f))
  cls.d=audit(cls.rows)
 def test_slots(self):self.assertEqual(self.d['slots'],36)
 def test_filled(self):self.assertEqual(self.d['filled'],35)
 def test_unique_pages(self):self.assertEqual(self.d['unique_notion_pages'],9)
 def test_missing_role(self):self.assertEqual(self.d['missing_roles'],[{'case_id':'TEC-988589FB9716','role':'family'}])
 def test_no_same_case_reuse(self):self.assertEqual(self.d['per_case_duplicate_ids'],[])
 def test_system_role(self):self.assertEqual(self.d['unique_per_role']['system'],3)
 def test_live_role(self):self.assertEqual(self.d['unique_per_role']['live'],4)
 def test_family_role(self):self.assertEqual(self.d['unique_per_role']['family'],4)
 def test_12(self):self.assertEqual(self.d['record_count'],12)
 def test_source_roles_are_not_re(self):self.assertFalse(self.d['judgement']['model_promotion_allowed'])
 def test_notion_query_ignored(self):self.assertEqual(notion_uuid('https://app.notion.com/p/b06c2b324ede8279a0f4014c14125a98?pvs=204'),'b06c2b324ede8279a0f4014c14125a98')
 def test_reject_foreign_host(self):self.assertIsNone(notion_uuid('https://evilmimic.example/p/b06c2b324ede8279a0f4014c14125a98'))
 def test_reject_path_trailing(self):self.assertIsNone(notion_uuid('https://app.notion.com/p/b06c2b324ede8279a0f4014c14125a98/extras'))
 def test_permutation_invariant_counts(self):
  q=audit(list(reversed(self.rows)));self.assertEqual(q['usage_per_page'],self.d['usage_per_page'])
 def test_detect_same_case_duplicate(self):
  rr=copy.deepcopy(self.rows);rr[0]['live_comparator_url']=rr[0]['system_comparator_url']+'?pvs=204';self.assertIn(rr[0]['case_id'],audit(rr)['per_case_duplicate_ids'])
 def test_reject_bad_ref(self):
  rr=copy.deepcopy(self.rows);rr[0]['system_comparator_url']='https://somewhere.net/p/hello'
  with self.assertRaisesRegex(ValueError,'NOTION_URL_INVALID'):audit(rr)
 def test_reject_duplicate_peer(self):
  rr=copy.deepcopy(self.rows);rr[0]['case_id']=rr[1]['case_id']
  with self.assertRaisesRegex(ValueError,'PEER_12_CENSUS'):audit(rr)
if __name__=='__main__': unittest.main()
