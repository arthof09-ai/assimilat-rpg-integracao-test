import unittest,tempfile,sys,json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(BASE/'runtime'),str(BASE.parent/'src'/'runtime'),str(BASE.parent/'src'/'baseline'/'runtime')]
from r182_native_readback import inspect_native_readback,import_readback_idempotently,NativeReadbackHold,CANARY,TX
from r185_mobile_preview import ReadonlyCharacter,preview_two_levels,rank_label,PreviewHold,mobile_chat_turn
from r173_sqlite_causal_ledger import Ledger,LAB,AUTH

class Tests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.db=str(Path(self.temp.name)/'db.sqlite')
  with Ledger(self.db) as d:
   d.create_intent(tx=TX,stage='DOC_CANARY',target=CANARY,parent=LAB,source_version='test',
     before={'target':CANARY,'field':'BRIDGE_PHYSICAL: BEFORE'},
     after={'target':CANARY,'field':'BRIDGE_PHYSICAL: AFTER'},pre_version='v1',authority=AUTH)
  from r173_sqlite_causal_ledger import digest
  sha=digest({'target':CANARY,'field':'BRIDGE_PHYSICAL: AFTER'})
  self.body=f'<page url="https://app.notion.com/p/{CANARY}"><ancestor-path><parent-page url="https://app.notion.com/p/{LAB}"/></ancestor-path><content>BRIDGE_EVENT: {TX}\nBRIDGE_PHYSICAL: AFTER\nBRIDGE_JOURNAL: COMMITTED_AFTER_NATIVE_READBACK; tx={TX}; stage=DOC_CANARY; after_sha={sha}; reviewer=SELF_REVIEW_ONLY</content></page>'
  self.capture={'structuredContent':{'text':self.body,'url':f'https://app.notion.com/p/{CANARY}?pvs=204','page_last_edited_at':'2026-10-18T15:06:15.211Z'}}
 def tearDown(self):self.temp.cleanup()
 def test_real_shape_readback(self):
  x=inspect_native_readback(self.capture,self.db);self.assertEqual(x['phase'],'AFTER');self.assertTrue(x['journal_verified'])
 def test_actual_ingestion_replay_noop(self):
  self.assertEqual(import_readback_idempotently(self.capture,self.db)['new_rows'],1)
  self.assertEqual(import_readback_idempotently(self.capture,self.db)['new_rows'],0)
  with Ledger(self.db) as d:self.assertEqual(d.verify_chain(TX,'DOC_CANARY')['observations'],1)
 def test_parent_spoof(self):
  with self.assertRaises(NativeReadbackHold):inspect_native_readback({'structuredContent':self.capture['structuredContent']|{'text':self.body.replace(LAB,'a'*32)}},self.db)
 def test_missing_journal(self):
  with self.assertRaises(NativeReadbackHold):inspect_native_readback({'structuredContent':self.capture['structuredContent']|{'text':self.body.replace('BRIDGE_JOURNAL:','OTHER:')}},self.db)
 def test_wrong_tool_page(self):
  with self.assertRaises(NativeReadbackHold):inspect_native_readback({'structuredContent':self.capture['structuredContent']|{'url':'https://app.notion.com/p/'+'b'*32}},self.db)
 def test_extra_marker(self):
  with self.assertRaises(NativeReadbackHold):inspect_native_readback({'structuredContent':self.capture['structuredContent']|{'text':self.body.replace('BRIDGE_PHYSICAL: AFTER','BRIDGE_PHYSICAL: AFTER\nBRIDGE_PHYSICAL: BEFORE')}},self.db)
 def test_preview_two_levels(self):
  x=ReadonlyCharacter('Personagem TEST','f'*32,LAB,'v1','rule-v1',1,{'FOR':2},{'FOR':'fixture'})
  p=preview_two_levels(x);self.assertEqual(p['level_after'],'Bronze 3');self.assertFalse(p['write_authorized']);self.assertEqual(p['native_effects'],0)
 def test_preview_source_bound(self):
  x=ReadonlyCharacter('Personagem TEST','f'*32,LAB,'v1','rule-v1',5,{'FOR':2},{'FOR':'fixture'})
  p=preview_two_levels(x,{'FOR':{'before':2,'after':4,'source_id':'fixture-choice'}})
  self.assertEqual(p['level_after'],'Prata 2');self.assertEqual(p['verified_changes']['FOR']['depois'],4)
 def test_preview_reject_unproven(self):
  x=ReadonlyCharacter('Personagem TEST','f'*32,LAB,'v1','rule-v1',5,{'FOR':2},{'FOR':'fixture'})
  with self.assertRaises(PreviewHold):preview_two_levels(x,{'FOR':{'before':2,'after':4}})
 def test_preview_party_no_write(self):
  x=ReadonlyCharacter('Party','f'*32,'e'*32,'v1','rule-v1',5,{},{});self.assertEqual(preview_two_levels(x)['state'],'HOLD_OUTSIDE_LAB')
 def test_preview_limit(self):
  x=ReadonlyCharacter('TEST','f'*32,LAB,'v1','rule-v1',24,{},{});self.assertEqual(preview_two_levels(x)['state'],'HOLD_LEVEL_OUT_OF_RANGE')
 def test_chat_two_levels(self):
  x=ReadonlyCharacter('Personagem TEST','f'*32,LAB,'v1','rule-v1',2,{},{});
  self.assertEqual(mobile_chat_turn('Quero subir dois níveis',x)['level_after'],'Bronze 4')
 def test_chat_confirmation_not_token(self):
  x=ReadonlyCharacter('Personagem TEST','f'*32,LAB,'v1','rule-v1',2,{},{});
  self.assertEqual(mobile_chat_turn('confirmo, pode aplicar',x)['state'],'AWAITING_TRUSTED_HOST_CONFIRMATION')
 def test_chat_cancel(self):
  self.assertEqual(mobile_chat_turn('cancelar',None)['state'],'CANCELED_NO_WRITE')
 def test_chat_without_source(self):
  self.assertEqual(mobile_chat_turn('Quero subir 2 levels',None)['state'],'AWAITING_SOURCE_BOUND_CHARACTER_SNAPSHOT')
 def test_rank_mapping(self):
  self.assertEqual(rank_label(25),'Lendário 5');self.assertEqual(rank_label(6),'Prata 1')
if __name__=='__main__':unittest.main()
