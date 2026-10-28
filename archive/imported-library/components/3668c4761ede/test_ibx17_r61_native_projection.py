"""Offline regression of additive projection guards; no Notion mutations."""
import unittest, json, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from ibx17_r61_native_projection import *

F=Path(__file__).with_name('R61_ORIGINAL_ENGINES_FULL_RECEIPTS.json')
R=json.loads(F.read_text())
PAIRS=(('up','UP','SIM-CHAT-2f1b6dba208c7d3cae8e','0cbafa7a90a8e9457648f001fa2b0ec8f2c0928f40fa5f6fb5873a38bc64755b','ba36dc424ccc098f8add6fcfd7a3dbdffd172bca83693599ea46bba301b2f1fb'),
       ('down','DOWN','SIM-LD-a711880f2315b25a8c69cc88','d4e25699e9c47a5751d0a8e3fee489d0ca18b6c4c683979af97da6eddb0988a0','2b570ca97cef3c614f5dff90c56775e9a5b1b33aaeba84d9aa32dd85b2e1ed02'))

class NativeProjectionGuardTest(unittest.TestCase):
 def data(self,row):
  k,kind,event,hb,ha=row;v=R[k]
  before=make_expected(v['full_before'],event,hb,'INITIAL_TEST_ONLY',kind)
  after=make_expected(v['full_after'],event,ha,'COMMITTED_TEST_R17_VERIFIED_LOCAL' if kind=='UP' else 'COMMITTED_TEST_R30_VERIFIED_LOCAL',kind)
  doc='## ESTADO ATIVO — PROJEÇÃO NOTION\n'+'\n'.join(f'{k}: {v}' for k,v in before.items())+'\n## PROVENIÊNCIA\ntext\n<details>\n<summary>ARQUIVO NATIVO TEST</summary>\n'+hb+'\n</details>\n'
  return before,after,doc
 def test_preview_project_matches_original_r17(self):
  before,after,doc=self.data(PAIRS[0]);self.assertEqual(after['NIVEL'],'17');self.assertEqual(after['FF'],'300');self.assertEqual(after['PA_MAX'],'320');self.assertEqual(after['VIDA_ATUAL'],'180');self.assertEqual(after['FF_LOCK_COUNT'],'3')
 def test_preview_project_matches_original_r30(self):
  before,after,doc=self.data(PAIRS[1]);self.assertEqual(after['NIVEL'],'16');self.assertEqual(after['DES'],'13');self.assertEqual(after['FF'],'290');self.assertEqual(after['FF_LOCK_COUNT'],'14')
 def test_both_atomic_patches(self):
  for row in PAIRS:
   with self.subTest(row=row[0]):
    before,after,doc=self.data(row)
    patch=plan_patch(doc,before,after,page_parent=LAB_PARENT)
    self.assertTrue(patch)
    written=doc.replace(*patch)
    validate(parse_active(written),after)
    verify_archived(written,row[2],row[3])
    self.assertIsNone(plan_patch(written,before,after,page_parent=LAB_PARENT))
 def test_reject_production_target(self):
  before,after,doc=self.data(PAIRS[0])
  with self.assertRaises(ProjectionHold):plan_patch(doc,before,after,page_parent='anything_else')
  with self.assertRaises(ProjectionHold):plan_patch(doc,before,after,page_parent=LAB_PARENT,source_is_official=True)
 def test_reject_source_drift(self):
  before,after,doc=self.data(PAIRS[0]);doc=doc.replace('FF: 290','FF: 295')
  with self.assertRaises(ProjectionHold):plan_patch(doc,before,after,page_parent=LAB_PARENT)
 def test_reject_duplicate_field(self):
  before,after,doc=self.data(PAIRS[1]);doc=doc.replace('FOR: 6','FOR: 6\nFOR: 6',1)
  with self.assertRaises(ProjectionHold):parse_active(doc)
 def test_reject_duplicate_active_region(self):
  before,after,doc=self.data(PAIRS[0]);doc=doc+doc
  with self.assertRaises(ProjectionHold):parse_active(doc)
 def test_reject_tampered_receipt_hash(self):
  before,after,doc=self.data(PAIRS[0]);after['ENGINE_FULL_STATE_SHA256']='c'*64
  patch=plan_patch(doc,before,after,page_parent=LAB_PARENT)
  with self.assertRaises(ProjectionHold):validate(parse_active(doc.replace(*patch)),self.data(PAIRS[0])[1])
 def test_reject_missing_archive(self):
  before,after,doc=self.data(PAIRS[1]);doc=doc.replace('ARQUIVO NATIVO','ARQ')
  with self.assertRaises(ProjectionHold):verify_archived(doc,PAIRS[1][2],PAIRS[1][3])
 def test_prevent_conflicting_event(self):
  before,after,doc=self.data(PAIRS[0]);doc=doc.replace(before['ENGINE_EVENT'],'SIM-CONFLICT',1)
  with self.assertRaises(ProjectionHold):plan_patch(doc,before,after,page_parent=LAB_PARENT)
 def test_unknown_extra_field(self):
  before,after,doc=self.data(PAIRS[0]);doc=doc.replace('VIDA_MAX: 255','VIDA_MAX: 255\nMYSTERY: 1',1)
  with self.assertRaises(ProjectionHold):plan_patch(doc,before,after,page_parent=LAB_PARENT)
 def test_recovery_noop_after_readback(self):
  for row in PAIRS:
   before,after,doc=self.data(row);old,new=plan_patch(doc,before,after,page_parent=LAB_PARENT)
   self.assertIsNone(plan_patch(doc.replace(old,new),before,after,page_parent=LAB_PARENT))
if __name__=='__main__':unittest.main(verbosity=2)
