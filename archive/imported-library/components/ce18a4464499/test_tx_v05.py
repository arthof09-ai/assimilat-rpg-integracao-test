import unittest
from tx_workflow_v05 import Tx,TxHold

class TxTest(unittest.TestCase):
 def test_full_safe_machine(self):
    t=Tx('LVL-000001','a'*36)
    with self.assertRaises(TxHold):t.advance('CONFIRM_PLAYER_RATE',proof='')
    t.advance('CONFIRM_PLAYER_RATE',proof='player asked; source discord')
    with self.assertRaises(TxHold):t.advance('PREPARE_PREIMAGE',proof='player gave 10 points')
    t.confirmed_player_rate=True
    t.advance('PREPARE_PREIMAGE',proof='player gave 10 points')
    t.source_snapshot_sha='sha'
    t.advance('APPEND_SAVE',proof='append sent to approved writer',op_id='save1')
    t.saved_sha='sha'
    t.advance('VERIFY_SAVE',proof='readback matches current preimage hash')
    t.advance('PLAN_PATCH',proof='signed edit fields with exact anchors')
    t.advance('APPLY_PATCH',proof='writer acknowledged patch operation',op_id='patch1')
    t.updated_sha='updated'
    for step in ('VERIFY_PATCH','RECONCILE','REPORT','NAC_PASS','CLOSED'):
        t.advance(step,proof='documented readback 100%')
    self.assertTrue(t.safe_status()['closed'])
 def test_wrong_order_rejected(self):
    t=Tx('E','a'*36)
    with self.assertRaises(TxHold):t.advance('APPLY_PATCH',proof='should not skip')
 def test_unknown_effect_requires_readback(self):
    t=Tx('E','a'*36);t.ambiguous('save-1')
    with self.assertRaises(TxHold):t.advance('CONFIRM_PLAYER_RATE',proof='player confirmed')
    with self.assertRaises(TxHold):t.reopen_reconcile(observed_state='unknown',proof='no data')
    t.reopen_reconcile(observed_state='operation_applied',proof='source exists in readback')
    self.assertFalse(t.unknown_effect)
 def test_idempotency_rejects_duplicate_ops(self):
    t=Tx('E','a'*36, state='PREPARE_PREIMAGE',confirmed_player_rate=True,source_snapshot_sha='sha')
    t.applied_operations.add('save1')
    with self.assertRaises(TxHold):t.advance('APPEND_SAVE',proof='already done once',op_id='save1')
 def test_save_required_before_patch(self):
    t=Tx('E','a'*36,state='VERIFY_SAVE',source_snapshot_sha='sha1',saved_sha='sha2')
    with self.assertRaises(TxHold):t.advance('PLAN_PATCH',proof='hash mismatch')
 def test_readback_required_after_write(self):
    t=Tx('E','a'*36,state='APPLY_PATCH')
    with self.assertRaises(TxHold):t.advance('VERIFY_PATCH',proof='not actually reopened')

if __name__=='__main__':unittest.main()
