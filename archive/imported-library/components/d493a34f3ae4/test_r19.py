"""Targeted negative controls, deliberately NOT a third evolution simulation."""
from __future__ import annotations
import copy, hashlib, unittest
from native_tree_gate_r19 import (GateHold, validate_complete_native_tree,
    native_differential_proof,native_restoration_proof,admission_gate,
    MCP_OBSERVATION,sha,tool_gap_report)

ROOT='3f4c2b32-4ede-81fe-b8cb-ed633a28daf0'
A='11111111-2222-4333-8444-555555555555'
B='99999999-2222-4333-8444-555555555555'


def graph():
    return {'page_id':ROOT, 'page_version':'e01','captured_at':'2026-10-09T14:00Z',
        'provider':'NOTION_NATIVE_BLOCK_API', 'complete_enumeration':True,
        'binary_backups_complete':True,'relation_closure_complete':True,'child_pages_complete':True,
        'nodes':[
            {'id':A,'parent_id':ROOT,'position':0,'type':'toggle','payload':{'text':'Vida 50/100','collapsed':False},'children_ids':[B],'last_edited_at':'e01'},
            {'id':B,'parent_id':A,'position':0,'type':'paragraph','payload':{'text':'Detalhe protegido'},'children_ids':[],'last_edited_at':'e01'}],
        'assets':[{'id':'fake-image-1','sha256':hashlib.sha256(b'png').hexdigest(),'byte_length':3,'backup_location':'sealed:/synthetic/image','restorable':True}],
        'relations':[{'source_block_id':A,'target_page_id':'fake-target','relation_type':'mention'}],
        'child_pages':[{'page_id':'fake-child-page','snapshot_sha256':hashlib.sha256(b'child').hexdigest(),'restorable':True}]
        }


def changed(g):
    y=copy.deepcopy(g);y['page_version']='e02';y['captured_at']='2026-10-09T14:01Z';y['nodes'][0]['payload']['text']='Vida 50/110';y['nodes'][0]['last_edited_at']='e02';return y


class NativeTreeR19(unittest.TestCase):
    def test_01_closed_graph_descriptive_hash(self):self.assertEqual(len(validate_complete_native_tree(graph())),64)
    def test_02_valid_bounded_diff(self):
        x=graph();y=changed(x);self.assertEqual(native_differential_proof(x,y,(A,'text'),'Vida 50/110')['notion_write_executed'],False)
    def test_03_valid_reversible_structure(self):
        x=graph();r=copy.deepcopy(x);r['page_version']='e03';r['captured_at']='2026-10-09T14:02Z';r['nodes'][0]['last_edited_at']='e03'
        self.assertEqual(native_restoration_proof(x,r)['notion_rollback_executed'],False)
    def test_04_missing_block_ids(self):
        t=graph();del t['nodes'][0]['id'];self.assertRaises(GateHold,validate_complete_native_tree,t)
    def test_05_false_claim_of_fullness(self):
        t=graph();t['complete_enumeration']=False;self.assertRaises(GateHold,validate_complete_native_tree,t)
    def test_06_NFM_not_native(self):
        t=graph();t['provider']='NOTION_ENHANCED_MARKDOWN';self.assertRaises(GateHold,validate_complete_native_tree,t)
    def test_07_missing_parent(self):
        t=graph();t['nodes'][1]['parent_id']='ghost';self.assertRaises(GateHold,validate_complete_native_tree,t)
    def test_08_missing_child(self):
        t=graph();t['nodes'][0]['children_ids']=[];self.assertRaises(GateHold,validate_complete_native_tree,t)
    def test_09_position_duplicate(self):
        t=graph();t['nodes'][1]['parent_id']=ROOT;t['nodes'][0]['children_ids']=[];t['nodes'][1]['position']=0
        self.assertRaises(GateHold,validate_complete_native_tree,t)
    def test_10_missing_media_backup(self):
        t=graph();t['assets'][0]['backup_location']='';self.assertRaises(GateHold,validate_complete_native_tree,t)
    def test_11_bad_media_hash(self):
        t=graph();t['assets'][0]['sha256']='0';self.assertRaises(GateHold,validate_complete_native_tree,t)
    def test_12_unrestorable_child(self):
        t=graph();t['child_pages'][0]['restorable']=False;self.assertRaises(GateHold,validate_complete_native_tree,t)
    def test_13_orphan_relation(self):
        t=graph();t['relations'][0]['source_block_id']='ghost';self.assertRaises(GateHold,validate_complete_native_tree,t)
    def test_14_unauthorized_change_to_other_node(self):
        x=graph();y=changed(x);y['nodes'][1]['payload']['text']='Alterado';self.assertRaises(GateHold,native_differential_proof,x,y,(A,'text'),'Vida 50/110')
    def test_15_media_change_detected(self):
        x=graph();y=changed(x);y['assets'][0]['sha256']=hashlib.sha256(b'bad').hexdigest();self.assertRaises(GateHold,native_differential_proof,x,y,(A,'text'),'Vida 50/110')
    def test_16_child_graph_change_detected(self):
        x=graph();y=changed(x);y['child_pages'][0]['snapshot_sha256']=hashlib.sha256(b'bad').hexdigest();self.assertRaises(GateHold,native_differential_proof,x,y,(A,'text'),'Vida 50/110')
    def test_17_bad_restoration_rejected(self):
        x=graph();y=changed(x);y['page_version']='e03';self.assertRaises(GateHold,native_restoration_proof,x,y)
    def test_18_nonce_replay_without_new_revision_rejected(self):
        x=graph();y=changed(x);y['page_version']=x['page_version'];self.assertRaises(GateHold,native_differential_proof,x,y,(A,'text'),'Vida 50/110')
    def test_19_incomplete_tool_surface_blocks(self):
        report=tool_gap_report();self.assertTrue(report['missing_verified_operations']);self.assertEqual(report['status'],'NO_NATIVE_WRITE_GATE')
    def test_20_no_ack_blocks(self):
        x=admission_gate(MCP_OBSERVATION);self.assertEqual(x['decision'],'HOLD');self.assertEqual(x['native_completed'],0)
    def test_21_forged_flags_cannot_unlock(self):
        a={'CM000005_ACK':True,'specific_copy_authorization':True,'writer_epoch':1,'lease':'fake','fencing':'fake'}
        x=admission_gate({k:'PROVIDER_VERIFIED' for k in MCP_OBSERVATION},graph(),a)
        self.assertEqual(x['decision'],'HOLD');self.assertIn('No authorized native writer/compensating rollback executable in this runtime',x['blockers'])
    def test_22_unknown_children_cannot_claim_closed(self):
        t=graph();t['child_pages_complete']=False;self.assertRaises(GateHold,validate_complete_native_tree,t)
    def test_23_missing_image_list_cannot_be_assumed_empty(self):
        t=graph();del t['assets'];self.assertRaises(GateHold,validate_complete_native_tree,t)
    def test_24_forged_total_text_equivalence_not_accepted(self):
        t=graph();del t['nodes'];self.assertRaises(GateHold,validate_complete_native_tree,t)
    def test_25_wrong_target_field(self):
        x=graph();y=changed(x);self.assertRaises(GateHold,native_differential_proof,x,y,(B,'text'),'Vida 50/110')

if __name__=='__main__': unittest.main()
