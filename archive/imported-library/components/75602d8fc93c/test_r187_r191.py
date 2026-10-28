import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from r188_r189_vertical import initial_test_state,calculate,parse_mobile,VerticalHold
from r191_replay_guard import NativeObservation, classify,cancel,NativeHold,LAB
TX='IBX17-R190-MVP-VERTICAL-20261019-01'
P='3fec2b324ede81d1bed5d6d0a7d60681'
PRE='2026-10-19T16:50:46.069Z'
AFTER='2026-10-19T16:53:02.716Z'
AFTER_TEXT='''## IBX17-R190 — DADOS ATIVOS / TEST
TX_STATE: COMMITTED_AFTER_NATIVE_READBACK
TX_ID: IBX17-R190-MVP-VERTICAL-20261019-01
TX_JOURNAL: COMMITTED_AFTER_NATIVE_READBACK; tx=IBX17-R190-MVP-VERTICAL-20261019-01; stage=NORMAL_TWO_LEVELS;
LEVEL: 19
SPIRIT_ACTIVE: FALSE
## PROVENIÊNCIA E ESCOPO
<details><summary>HISTÓRICO INTEGRAL R190</summary>
	LEVEL: 17
</details>'''
BEFORE_TEXT=AFTER_TEXT.replace('TX_STATE: COMMITTED_AFTER_NATIVE_READBACK','TX_STATE: PRE').replace('TX_ID: IBX17-R190-MVP-VERTICAL-20261019-01','TX_ID: NONE').replace('TX_JOURNAL: COMMITTED_AFTER_NATIVE_READBACK; tx=IBX17-R190-MVP-VERTICAL-20261019-01; stage=NORMAL_TWO_LEVELS;','').replace('LEVEL: 19','LEVEL: 17')
A=[dict(FOR=0,DES=0,CON=0,INT=2,SAB=0,CAR=0),dict(FOR=0,DES=0,CON=0,INT=0,SAB=2,CAR=0)]
class VerticalTests(unittest.TestCase):
 def state(self):return initial_test_state(fixture_id=P)
 def test_two_level_real_math(self):
  p=calculate(self.state(),tx=TX,per_level_allocations=A);n=p['after']['normal'];self.assertEqual((n['level'],n['hp_max'],n['pa_max'],n['pa_free'],n['magic_cd']),(19,307,360,340,15));self.assertEqual(len(p['steps']),2)
 def test_current_preserved(self):
  p=calculate(self.state(),tx=TX,per_level_allocations=A);self.assertEqual((p['after']['normal']['hp_current'],p['after']['normal']['pa_current']),(180,200))
 def test_spirit_inactive_ff_preserved(self):
  p=calculate(self.state(),tx=TX,per_level_allocations=A);self.assertFalse(p['after']['spirit_overlay']['active']);self.assertEqual(p['after']['normal']['ff'],300)
 def test_reverse_choices_preview_changes_not_source(self):
  x=calculate(self.state(),tx=TX,per_level_allocations=A)
  alt=[dict(FOR=0,DES=0,CON=0,INT=0,SAB=2,CAR=0),dict(FOR=0,DES=0,CON=0,INT=2,SAB=0,CAR=0)]
  y=calculate(self.state(),tx=TX+'-ALT',per_level_allocations=alt)
  self.assertEqual(x['after']['normal']['pa_max'],y['after']['normal']['pa_max']+2)
  self.assertEqual(self.state()['normal']['level'],17)
 def test_invalid_alloc(self):
  with self.assertRaises(VerticalHold):calculate(self.state(),tx=TX,per_level_allocations=[dict(FOR=0,DES=0,CON=0,INT=3,SAB=0,CAR=0)])
 def test_input_mobile(self):self.assertEqual(parse_mobile('Quero subir dois níveis com este personagem')['levels'],2)
 def test_cancel_chat(self):self.assertEqual(parse_mobile('Cancelar')['intent'],'CANCEL')
 def test_native_replay_noop(self):self.assertEqual(classify(NativeObservation(P,LAB,AFTER,AFTER_TEXT),tx=TX,expected_target=P,expected_pre_version=PRE)['decision'],'NOOP_ALREADY_CONSUMED_NATIVE')
 def test_cancel_preserves(self):self.assertEqual(cancel(NativeObservation(P,LAB,AFTER,AFTER_TEXT),tx=TX)['writes'],0)
 def test_stale_preview_rejected(self):
  o=NativeObservation(P,LAB,AFTER,BEFORE_TEXT);self.assertEqual(classify(o,tx=TX,expected_target=P,expected_pre_version=PRE)['decision'],'HOLD_STALE_PREVIEW_VERSION')
 def test_fresh_ready_readonly(self):self.assertEqual(classify(NativeObservation(P,LAB,PRE,BEFORE_TEXT),tx=TX,expected_target=P,expected_pre_version=PRE)['decision'],'FRESH_TEST_PREVIEW_CANDIDATE')
 def test_wrong_parent(self):
  with self.assertRaises(NativeHold):classify(NativeObservation(P,'party',AFTER,AFTER_TEXT),tx=TX,expected_target=P,expected_pre_version=PRE)
 def test_wrong_target(self):
  with self.assertRaises(NativeHold):classify(NativeObservation('other',LAB,AFTER,AFTER_TEXT),tx=TX,expected_target=P,expected_pre_version=PRE)
 def test_no_production(self):
  with self.assertRaises(NativeHold):classify(NativeObservation(P,LAB,AFTER,AFTER_TEXT),tx=TX,expected_target=P,expected_pre_version=PRE,allow_test_only=False)
 def test_partially_committed_hold(self):
  s=AFTER_TEXT.replace('TX_STATE: COMMITTED_AFTER_NATIVE_READBACK','TX_STATE: AFTER_PENDING_READBACK')
  self.assertEqual(classify(NativeObservation(P,LAB,AFTER,s),tx=TX,expected_target=P,expected_pre_version=PRE)['decision'],'HOLD_PARTIAL_OR_UNKNOWN_SAME_EVENT')
 def test_missing_history(self):
  with self.assertRaises(NativeHold):classify(NativeObservation(P,LAB,AFTER,AFTER_TEXT.split('<details>')[0]),tx=TX,expected_target=P,expected_pre_version=PRE)
if __name__=='__main__':unittest.main()
