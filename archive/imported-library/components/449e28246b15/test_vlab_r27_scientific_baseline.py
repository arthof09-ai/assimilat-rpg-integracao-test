import json,pathlib,tempfile,copy,hashlib
import unittest
import vlab_r27_scientific_baseline as v
import vlab_r26_master_rulings as r26
import vlab_r25_rule_derived_benchmark as r25

class R27ScienceTests(unittest.TestCase):
 def test_01_profile_budget_and_distinct_ca(self):
  for p,attrs in v.PROFILES.items():
   self.assertTrue(v.validation_alloc(attrs));self.assertEqual(sum(attrs.values()),43)
   r=v.roster(p,p)
   self.assertEqual(r[0]['ca'],10+attrs['DES']+attrs['CON']//5)
   self.assertEqual(r[0]['hp'],40+attrs['CON']);self.assertEqual(r[0]['pa'],40+attrs['INT'])
 def test_02_critical_failure_83_real_native(self):
  with tempfile.TemporaryDirectory() as td:
   r=v.run(pathlib.Path(td),83)
   self.assertEqual(r['status'],'COMPLETE_CONDITIONAL_RULE_DERIVED')
   failures=[x for x in r['events'] if x['critical']=='NEGATIVE'];self.assertEqual(len(failures),1)
   e=failures[0];self.assertEqual(e['critical_check'][:2],[1,1]);self.assertIn(e['critical_check'][2],[1,2]);self.assertEqual(e['roll_used_by_native'],0)
   self.assertEqual((e['native_hit'],e['native_raw'],e['native_net']), (False,0,0))
   self.assertEqual(e['before_hp'],e['after_hp'])
   self.assertEqual(e['critical_failure_overlay'],v.CRIT_FAIL_POLICY)
   self.assertGreater(r['summary']['attacks'],3)
 def test_03_same_8_preregistered_seeds(self):
  self.assertEqual(r25.DEFAULT_SEEDS,(11,23,37,41,53,67,71,83))
  self.assertEqual(v.SEEDS[:8],r25.DEFAULT_SEEDS)
 def test_04_exact_hit_probability(self):
  g=v.exact_hit_grid();self.assertEqual(len(g),16)
  self.assertEqual(g['OFENSIVO__DEFENSIVO'][0]['hit_faces'],6)
  self.assertEqual(g['OFENSIVO__DEFENSIVO'][1]['hit_faces'],2)
  self.assertEqual(g['ASSIMETRICO__ASSIMETRICO'][0]['hit_faces'],0)
 def test_05_no_hit_refusal_is_structural(self):
  with tempfile.TemporaryDirectory() as td:
   r=v.run(pathlib.Path(td),11,'ASSIMETRICO','ASSIMETRICO')
   self.assertEqual(r['status'],'CENSORED_PROVABLE_NO_HIT_POTENTIAL');self.assertEqual(r['revision'],0)
   self.assertEqual(r['summary']['attacks'],0)
 def test_06_revision_and_intent_idempotency(self):
  with tempfile.TemporaryDirectory() as td:
   p=pathlib.Path(td)/'b.sqlite';v.create(p,23,'OFENSIVO','DEFENSIVO')
   st,h,rev=v.checked(p);v.decision(p,rev,h,'START')
   st,h,rev=v.checked(p);pre=v.pre(st,rev+1);v.decision(p,rev,h,'ATTACK',pre)
   st2,h2,rev2=v.checked(p);self.assertEqual(rev2,2)
   with self.assertRaises(v.R27Hold):v.decision(p,rev,h,'ATTACK',pre)
   self.assertEqual((v.checked(p)[1],v.checked(p)[2]),(h2,rev2))
 def test_07_checkpoint_and_restore(self):
  with tempfile.TemporaryDirectory() as td:
   root=pathlib.Path(td);db=root/'run.sqlite';v.create(db,11,'OFENSIVO','DEFENSIVO')
   st,h,r=v.checked(db);v.decision(db,r,h,'START')
   cp=root/'checkpoint.zip';receipt=v.export_checkpoint(db,cp)
   self.assertEqual(receipt['status'],'PASS');rest=root/'new.sqlite'
   self.assertEqual(v.verify_checkpoint(cp,restore_to=rest)['status'],'PASS')
   self.assertEqual(v.history(db),v.history(rest))
   with self.assertRaises(v.R27Hold):v.verify_checkpoint(cp,restore_to=rest)
 def test_08_tie_ruling_existing(self):
  a=[{'id':'A','total':12,'des':8},{'id':'B','total':12,'des':8},{'id':'C','total':15,'des':4}]
  r=r26.tie_order(a,lambda aid,n: 12 if aid=='A' else 13)
  self.assertEqual(r['order'],['C','B','A'])
 def test_09_positive_critical_historical_resolver(self):
  with tempfile.TemporaryDirectory() as td:
   r=v.run(pathlib.Path(td),71)
   ev=[x for x in r['events'] if x['critical']=='POSITIVE']
   self.assertGreaterEqual(len(ev),1)
   self.assertTrue(any(x['requested_damage']==sum(x['dice_damage'])+18 for x in ev))
 def test_10_noncannonical_tag(self):
  for key in v.PROFILES:
   m=v.manifest(key,key,'PROFILE_MATRIX')
   self.assertTrue(m['no_canonical_credit'])
   self.assertIn('luta_training',m['conditioned_assumptions'])

if __name__=='__main__':unittest.main(verbosity=2)
