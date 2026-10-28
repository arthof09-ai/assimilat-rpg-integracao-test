from __future__ import annotations
import csv,io,copy,json,unittest,sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import metrics,craft_design
R=Path(__file__).resolve().parents[1]

class ScienceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.f,cls.peer,cls.lineage=metrics.load_inputs(R/'inputs')
  cls.o=metrics.metrics(cls.f,cls.peer,cls.lineage)
 def test_census_frozen_26(self):self.assertEqual(len(self.f['cases']),26)
 def test_peer_12(self):self.assertEqual(len(self.peer),12)
 def test_cohorts_12_and_14(self):
  c=__import__('collections').Counter(x['blind_cohort'] for x in self.lineage['images']);self.assertEqual(c,{'HOLDOUT14':14,'PEER12':12})
 def test_source_image_hash_matches_csv(self):metrics.identity_check(self.f,self.peer,self.lineage)
 def test_reject_changed_hash(self):
  p=copy.deepcopy(self.peer);p[0]['image_sha256']='0'*64
  with self.assertRaisesRegex(ValueError,'MASKED_SHA_MISMATCH'):metrics.identity_check(self.f,p,self.lineage)
 def test_reject_duplicate_id(self):
  p=copy.deepcopy(self.peer);p[0]['case_id']=p[1]['case_id']
  with self.assertRaisesRegex(ValueError,'PEER_CENSUS_FAILED'):metrics.identity_check(self.f,p,self.lineage)
 def test_reject_missing_line(self):
  with self.assertRaisesRegex(ValueError,'PEER_CENSUS_FAILED'):metrics.identity_check(self.f,self.peer[:-1],self.lineage)
 def test_reject_bad_lineage_union(self):
  l=copy.deepcopy(self.lineage);l['images'][0]['id']='TEC-FAKE'
  with self.assertRaisesRegex(ValueError,'IMAGE_CENSUS_FAILED'):metrics.identity_check(self.f,self.peer,l)
 def test_11_usable(self):self.assertEqual(self.o['n_usable'],11)
 def test_e353_exposure(self):self.assertEqual(self.o['exposed_ids'],['TEC-E3532F6A98AC'])
 def test_agreement_r45(self):self.assertEqual(self.o['hits_R45'],7)
 def test_baseline_prata(self):self.assertEqual(self.o['hits_constant_Prata'],7)
 def test_kappa(self):self.assertAlmostEqual(self.o['kappa_nominal_R45_peer'],5/27,places=9)
 def test_peer_rank_counts(self):self.assertEqual(self.o['class_counts_peer'],{'Bronze':3,'Prata':7,'Ouro':1})
 def test_macro_recall(self):self.assertAlmostEqual(self.o['macro_recall_R45_vs_peer'],(0+6/7+1)/3)
 def test_no_bronze_agreement(self):self.assertEqual(self.o['by_class']['Bronze']['R45_recall'],0)
 def test_mcnemar_pair(self):self.assertEqual((self.o['paired_R45_only_wins'],self.o['paired_constant_only_wins']),(1,1))
 def test_mcnemar_p(self):self.assertEqual(self.o['mcnemar_exact_p'],1)
 def test_evidence_fisher(self):
  a=self.o['evidence_by_agreement'];self.assertEqual(a['counts'],[[0,4],[7,0]])
  self.assertAlmostEqual(a['Fisher_two_sided_conditional_p'],1/330)
 def test_fisher_symmetry(self):
  self.assertAlmostEqual(metrics.exact_fisher_2x2([[0,4],[7,0]]),metrics.exact_fisher_2x2([[7,0],[0,4]]))
 def test_mean_interval(self):self.assertAlmostEqual(self.o['R45_interval_mean_cardinality'],24/11)
 def test_intervals_constant_prata(self):self.assertTrue(self.o['R45_range_includes_Prata_all'])
 def test_intervals_cover_peer(self):self.assertEqual(self.o['R45_band_hits_vs_peer'],11)
 def test_holdout_no_rank_or_oracle(self):
  plan=metrics.future_review_protocol(self.lineage);s=json.dumps(plan,ensure_ascii=False)
  self.assertEqual(plan['denominator'],14)
  self.assertNotIn('proposed_RE',s);self.assertNotIn('R45_range',s)
 def test_integrity_status_not_scientific(self):self.assertEqual(self.o['status'],'AGREEMENT_ONLY_NOT_ACCURACY')
 def test_permutation_invariance_of_peer_rows(self):
  reversed_o=metrics.metrics(self.f,list(reversed(self.peer)),self.lineage)
  for k in ('hits_R45','hits_constant_Prata','agreement_R45','evidence_by_agreement','class_counts_peer'):
   self.assertEqual(self.o[k],reversed_o[k])

class CraftTests(unittest.TestCase):
 def test_four_physical_stages(self):self.assertEqual(len(craft_design.STAGES),4)
 def test_all_contrasts_match_names(self):self.assertEqual(len(craft_design.CONTRASTS),3)
 def test_default_preflight_hold(self):self.assertEqual(craft_design.gate_plan({})['gate'],'HOLD_NO_PHYSICAL_APPLICATION')
 def test_default_preflight_does_not_make_magic(self):self.assertFalse(craft_design.gate_plan({})['effect_magic_observed'])
 def test_salt_open_blocks(self):self.assertIn('P2_SALT_AUTHORITY_PENDING',craft_design.gate_plan({})['blockers'])
 def test_energy_open_blocks(self):self.assertIn('P2_ENERGY_AUTHORITY_PENDING',craft_design.gate_plan({})['blockers'])
 def test_oil_open_blocks(self):self.assertIn('OIL_FORMULA_AUTHORITY_PENDING',craft_design.gate_plan({})['blockers'])
 def test_stage_feasibility_required(self):
  p=self.example_plan();p['stage_feasibility_confirmed']=False
  self.assertIn('STAGE_FEASIBILITY_UNCONFIRMED',craft_design.gate_plan(p)['blockers'])
 def test_matched_substrate_required(self):
  p=self.example_plan();p['matched_substrate_confirmed']=False
  self.assertIn('MATCHED_SUBSTRATE_UNCONFIRMED',craft_design.gate_plan(p)['blockers'])
 def test_readout_registration_required(self):
  p=self.example_plan();p['assay_readout_predefined']=False
  self.assertIn('ASSAY_READOUT_NOT_PREREGISTERED',craft_design.gate_plan(p)['blockers'])
 def test_separate_witness(self):
  p={'qualified_operator_id':'A','independent_witness_id':'A'}
  self.assertIn('WITNESS_NOT_INDEPENDENT',craft_design.gate_plan(p)['blockers'])
 def test_optimistic_form_alone_not_proof(self):
  p=self.example_plan();z=craft_design.gate_plan(p)
  self.assertEqual(z['gate'],'FORM_READY_EXTERNAL_AUTHENTICATION_REQUIRED')
  self.assertFalse(z['effect_magic_observed'])
 def test_incomplete_experiment(self):
  z=craft_design.evaluate_record({'observations':[{'arm':'C1','outcome':12}]},self.example_plan())
  self.assertIn('MISSING_COMPARISON_ARM',z['blockers'])
 def test_numeric_causal_differences_are_descriptive_only(self):
  z=craft_design.evaluate_record(self.example_observations(),self.example_plan())
  self.assertEqual(z['contrasts'],{'natural_source_C1_minus_C0':4.,'P2_increment_C2_minus_C1':2.,'own_spell_C3_minus_C2':5.})
  self.assertEqual(z['status'],'DESCRIPTIVE_ONLY_UNAUTHENTICATED')
 def test_reject_nan(self):
  o=self.example_observations();o['observations'][0]['outcome']=float('nan')
  self.assertEqual(craft_design.evaluate_record(o,self.example_plan())['status'],'HOLD')
 def test_reject_inf(self):
  o=self.example_observations();o['observations'][0]['outcome']=float('inf')
  self.assertEqual(craft_design.evaluate_record(o,self.example_plan())['status'],'HOLD')
 def test_reject_bool_observation(self):
  o=self.example_observations();o['observations'][0]['outcome']=True
  self.assertEqual(craft_design.evaluate_record(o,self.example_plan())['status'],'HOLD')
 def test_bad_arm(self):
  o=self.example_observations();o['observations'][0]['arm']='I5'
  self.assertEqual(craft_design.evaluate_record(o,self.example_plan())['status'],'HOLD')
 def test_cost_is_never_charged(self):
  z=craft_design.evaluate_record(self.example_observations(),self.example_plan())
  self.assertFalse(z['PA_charged']);self.assertFalse(z['item_created'])
 def test_gate_prevents_partial_records(self):
  o=self.example_plan();o['p2_recipe_salt_resolved']=False
  self.assertEqual(craft_design.evaluate_record(self.example_observations(),o)['status'],'HOLD')
 def test_8_arm_not_forced(self):
  p=craft_design.design_record()
  self.assertEqual(len(p['stages']),4)
  self.assertIn('OPTIONAL_FEASIBILITY',p['other_R47_factorial_arms'])
 def test_no_inference_from_form(self):
  d=craft_design.design_record();self.assertEqual(d['claim_rules']['form_complete'],'NOT_AUTHENTICATED')
 @staticmethod
 def example_plan():
  return {'source_identity_and_lot':'synthetic_source','oil_identity_and_lot':'synthetic_oil',
  'stage_feasibility_confirmed':True,'matched_substrate_confirmed':True,'assay_readout_predefined':True,
  'p2_recipe_salt_resolved':True,'p2_recipe_energy_stage_resolved':True,
  'oil_recipe_reconciled':True,'installation_procedure_approved':True,
  'qualified_operator_id':'A','independent_witness_id':'B',
  'instrument_calibration_id':'synthetic_instrument'}
 @staticmethod
 def example_observations():
  return {'observations':[{'arm':k,'outcome':v} for k,v in [('C0',3),('C1',7),('C2',9),('C3',14)]]}

if __name__=='__main__':unittest.main(verbosity=1)
