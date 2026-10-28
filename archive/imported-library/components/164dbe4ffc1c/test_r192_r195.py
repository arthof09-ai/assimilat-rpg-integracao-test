"""Incremental tests on the EXISTING IBX17 integrated engine; no Notion writes."""
import unittest
from r195_mobile_flow import MobileSession,ConversationHold
from r192_r193_extensions import rank_cross_readonly,spirit_nonzero_readonly
A=[dict(FOR=0,DES=0,CON=0,INT=2,SAB=0,CAR=0), dict(FOR=0,DES=0,CON=0,INT=0,SAB=2,CAR=0)]
B=[dict(FOR=0,DES=0,CON=0,INT=0,SAB=2,CAR=0),dict(FOR=0,DES=0,CON=0,INT=2,SAB=0,CAR=0)]
AUTH='DIR-MESTRE-LABS-REPLICAS-20261016-001'
class MobileFunctionalTests(unittest.TestCase):
 def session(self):return MobileSession(fixture_id='SYNTH-LOCAL-ONLY',physical_version='synthetic-pre-v1',source_binding='R99-SYNTHETIC',tx='NEW-TEST-NON-NATIVE-TX')
 def test_two_level_request_and_choices(self):
  s=self.session();z=s.start('Quero subir dois níveis com este personagem');self.assertEqual(z['levels'],2);p=s.choose(A);self.assertEqual(p['after_level'],19);self.assertEqual(p['changes']['hp_max']['depois'],307);self.assertEqual(p['changes']['pa_max']['depois'],360);self.assertEqual(p['writes'],0)
 def test_revising_choices_changes_digest_no_write(self):
  s=self.session();s.start('Subi dois níveis');a=s.choose(A);b=s.choose(B);self.assertNotEqual(a['preview_sha'],b['preview_sha']);self.assertEqual(b['changes']['natural_attrs']['depois']['SAB'],8);self.assertEqual(s.stage,'PREVIEW_READY')
 def test_cancel_before_choice(self):
  s=self.session();s.start('Quero subir dois níveis');self.assertEqual(s.cancel()['native_writes'],0);self.assertEqual(s.stage,'CANCELED')
 def test_cancel_after_preview(self):
  s=self.session();s.start('Quero subir dois níveis');s.choose(A);self.assertEqual(s.cancel()['state'],'CANCELED_NO_WRITE')
 def test_no_apply_after_cancel(self):
  s=self.session();s.start('Quero subir dois níveis');s.cancel();
  with self.assertRaises(ConversationHold):s.choose(A)
 def test_stale_prevents_apply(self):
  s=self.session();s.start('Quero subir dois níveis');s.choose(A);z=s.request_apply('confirmo',target_current_version='v2',lab_directive=AUTH);self.assertFalse(z['write_authorized']);self.assertEqual(z['state'],'STALE_PREVIEW_MUST_RECALCULATE')
 def test_attestation_absent_is_not_production(self):
  s=self.session();s.start('Quero subir dois níveis');s.choose(A);z=s.request_apply('confirmo',target_current_version='synthetic-pre-v1',lab_directive=AUTH);self.assertFalse(z['host_attestation']);self.assertFalse(z['production_authorized']);self.assertEqual(z['state'],'PENDING_CONNECTED_WRITE')
 def test_absent_lab_directive_is_hold(self):
  s=self.session();s.start('Quero subir dois níveis');s.choose(A);z=s.request_apply('confirmo',target_current_version='synthetic-pre-v1',lab_directive=None);self.assertEqual(z['state'],'LAB_AUTHORITY_NOT_ESTABLISHED')
 def test_partial_native_effect_is_not_pass(self):
  s=self.session();s.start('Quero subir dois níveis');s.choose(A);s.request_apply('confirmo',target_current_version='synthetic-pre-v1',lab_directive=AUTH);z=s.observe_after(physical_after_matches=True,history_verified=True,journal_verified=False);self.assertEqual(z['state'],'HOLD_PARTIAL_AFTER')
 def test_mock_observed_native_is_review_only(self):
  s=self.session();s.start('Quero subir dois níveis');s.choose(A);s.request_apply('confirmo',target_current_version='synthetic-pre-v1',lab_directive=AUTH);z=s.observe_after(physical_after_matches=True,history_verified=True,journal_verified=True);self.assertEqual(z['source'],'NATIVE_READBACK_SELF_REVIEW');self.assertFalse(z['production'])
 def test_bad_allocation_rejected(self):
  s=self.session();s.start('Quero subir dois níveis');
  with self.assertRaises(ConversationHold):s.choose([dict(FOR=0,DES=0,CON=0,INT=3,SAB=0,CAR=0),A[1]])
 def test_rank_cross_readonly_never_native(self):
  z=rank_cross_readonly();self.assertEqual((z['before_level'],z['after_level'],z['hp_after'],z['pa_after']),(5,6,54,142));self.assertEqual(z['native_new_effects'],0)
 def test_spirit_half_carry_nonzero(self):
  z=spirit_nonzero_readonly();self.assertEqual(z['spirit_increment_steps'],[6,5]);self.assertEqual(z['carry_after'],'1/2');self.assertFalse(z['form_active']);self.assertEqual(z['native_writes'],0)
if __name__=='__main__':unittest.main()
