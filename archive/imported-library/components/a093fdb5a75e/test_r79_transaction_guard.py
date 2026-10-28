import sys,unittest,copy,json
from pathlib import Path
HERE=Path(__file__).parent;sys.path.insert(0,str(HERE))
from ibx17_r79_transaction_guard import *
DATA=json.loads((HERE/'R75_R76_FULL_MOTOR_RECEIPTS.json').read_text())

class FullStateGuardTests(unittest.TestCase):
 def setUp(self):
  self.before=copy.deepcopy(DATA['down']['full_before']);self.after=copy.deepcopy(DATA['down']['full_after']);self.doc=fixture_doc(self.before)
  self.event='SIM-R79-ADVERSARIAL-TEST';self.plan=preview(self.doc,self.after,self.event)
 def test_01_stale_preview(self):
  self.doc['active']['NORMAL']['attrs']['DES']+=1
  with self.assertRaisesRegex(Hold,'STALE_PREIMAGE'):commit(self.doc,self.plan)
 def test_02_duplicate_value_across_active_and_history_not_ambiguous(self):
  result,status=commit(self.doc,self.plan);self.assertEqual(status,'COMMITTED')
  self.assertEqual(result['history'][0]['state'],self.before)
  self.assertEqual(result['active'],self.after)
 def test_03_crash_after_archive_is_fail_closed(self):
  with self.assertRaisesRegex(Hold,'CRASH_AFTER_ARCHIVE'):commit(self.doc,self.plan,fault='after_archive')
  self.assertEqual(recover(self.doc,self.doc,self.plan),'CLEAN_PREIMAGE_SAFE_TO_RETRY')
 def test_04_crash_after_partial_derivatives_has_no_committed_effect(self):
  with self.assertRaisesRegex(Hold,'BEFORE_SINGLE_ATOMIC'):commit(self.doc,self.plan,fault='after_some_derivatives')
  self.assertEqual(self.doc['active'],self.before)
 def test_05_same_event_idempotent(self):
  committed,status=commit(self.doc,self.plan);again,stat=commit(committed,self.plan)
  self.assertEqual(stat,'IDEMPOTENT_NOOP');self.assertEqual(len(again['event_log']),1)
 def test_06_missing_normal_field(self):
  self.after['NORMAL'].pop('id');
  with self.assertRaises((KeyError,Hold)):preview(self.doc,self.after,self.event)
 def test_07_missing_child_page(self):
  self.doc['child_count']=23
  with self.assertRaisesRegex(Hold,'NATIVE_CHILD_ABSENT'):preview(self.doc,self.after,self.event)
 def test_08_external_reference_in_write_scope(self):
  self.doc['external_writes']=1
  with self.assertRaisesRegex(Hold,'EXTERNAL_REF_WRITE'):preview(self.doc,self.after,self.event)
 def test_09_equipment_state_changed(self):
  self.doc['equipment_identity']['equipment']['DES']+=1
  with self.assertRaisesRegex(Hold,'EQUIPMENT_DRIFT'):preview(self.doc,self.after,self.event)
 def test_10_transform_interruption(self):
  with self.assertRaisesRegex(Hold,'TRANSFORM_CRASH'):commit(self.doc,self.plan,fault='transform_interrupt')
  self.assertEqual(self.doc['active']['TRANSFORM'],self.before['TRANSFORM'])
 def test_11_recovery_checkpoint(self):
  done,_=commit(self.doc,self.plan)
  self.assertEqual(recover(self.doc,done,self.plan),'COMMITTED_NEVER_REAPPLY')
  forged=copy.deepcopy(done);forged['active']['NORMAL']['attrs']['DES']=999
  self.assertEqual(recover(self.doc,forged,self.plan),'UNKNOWN_EFFECT_HOLD_READBACK')
 def test_12_missing_choice(self):
  with self.assertRaisesRegex(Hold,'MISSING_COMPETENT_CHOICE'):preview(self.doc,self.after,self.event,choice_kind='ASSUMED_PLAYER_HISTORY')

if __name__=='__main__':unittest.main(verbosity=2)
