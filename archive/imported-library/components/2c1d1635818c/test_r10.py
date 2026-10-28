import unittest
from r10_recovery import *
A='''<table header-row="true">\n<tr>\n<td>Magia</td><td>PA</td>\n</tr>\n<tr><td>Projétil fictício</td><td>10</td></tr>\n</table>'''
B='''\t<table header-row="true">\n\t\t<tr>\n\t\t\t<td>Magia</td><td>PA</td>\n\t\t</tr>\n\t\t<tr><td>Projétil fictício</td><td>10</td></tr>\n\t</table>'''
class R10(unittest.TestCase):
 def test_indent_accepted(self):self.assertTrue(compare_tables(A,B)['equal'])
 def test_cell_change_rejected(self):self.assertFalse(compare_tables(A,A.replace('10</td>','11</td>'))['equal'])
 def test_cell_order_rejected(self):self.assertFalse(compare_tables(A,A.replace('<td>Magia</td><td>PA</td>','<td>PA</td><td>Magia</td>'))['equal'])
 def test_row_order_rejected(self):self.assertFalse(compare_tables(A,A.replace('Projétil fictício','AAA'))['equal'])
 def test_col_insert_rejected(self):self.assertFalse(compare_tables(A,A.replace('<td>10</td>','<td>10</td><td>X</td>'))['equal'])
 def test_row_insert_rejected(self):self.assertFalse(compare_tables(A,A.replace('</table>','<tr><td>x</td><td>20</td></tr></table>'))['equal'])
 def test_header_rejected(self):self.assertFalse(compare_tables(A,A.replace('header-row="true"','header-row="false"'))['equal'])
 def test_cell_whitespace_rejected(self):self.assertFalse(compare_tables(A,A.replace('>10</td>','> 10</td>'))['equal'])
 def test_bad_structure_rejected(self):
  with self.assertRaises(StructuralError):table_ast(A.replace('</tr>','</td>',1))
 def test_no_table_rejected(self):
  with self.assertRaises(StructuralError):table_ast('no table')
 def test_media_no_inference(self):
  result=media_evidence(source_block_id='a',clone_block_id='b',source_url='x',clone_url='y')
  self.assertEqual(result['state'],'PENDING')
 def test_media_equal_bytes_still_pending(self):
  self.assertEqual(media_evidence(source_bytes=b'x',clone_bytes=b'x')['state'],'PENDING')
 def test_media_independence_criteria(self):
  self.assertEqual(media_evidence(source_bytes=b'x',clone_bytes=b'x',independent_object_ids=True,delete_restore_verified=True)['state'],'VERIFIED')
 def test_two_page_success(self):
  store=FakeStore({'a':1,'b':2});j=RecoveryController(store).run('ev',{'a':3,'b':4})
  self.assertEqual(j.state,'COMMITTED');self.assertEqual(store.pages,{'a':3,'b':4})
 def test_crash_points(self):
  names=['BEFORE_PREFLIGHT','AFTER_PREFLIGHT','BEFORE_WRITE:a','AFTER_WRITE:a','AFTER_READBACK:a','BEFORE_WRITE:b','AFTER_WRITE:b','AFTER_READBACK:b','AFTER_COMMIT']
  for name in names:
   with self.subTest(name=name):
    store=FakeStore({'a':1,'b':2});ctl=RecoveryController(store)
    j=ctl.run('ev',{'a':3,'b':4},crash_at=name)
    self.assertIn(j.state,('UNKNOWN_EFFECT',))
    ctl.reconcile(j)
    if name=='AFTER_COMMIT':
     # A committed side effect with missing ACK is compensated conservatively in this simulated abort policy.
     pass
    self.assertEqual(store.pages,{'a':1,'b':2})
    self.assertIn(j.state,('ROLLED_BACK_VERIFIED','NOT_APPLIED'))
 def test_concurrent_conflict_no_overwrite(self):
  store=FakeStore({'a':1,'b':2});ctl=RecoveryController(store)
  j=ctl.run('ev',{'a':3,'b':4},crash_at='AFTER_WRITE:a');store.pages['a']=999
  ctl.reconcile(j);self.assertEqual(j.state,'HOLD_CONCURRENT_CONFLICT');self.assertEqual(store.pages['a'],999)
 def test_aba_concurrent_version_conflict(self):
  store=FakeStore({'a':1,'b':2});ctrl=RecoveryController(store)
  j=ctrl.run('ev',{'a':3,'b':4},crash_at='AFTER_WRITE:a')
  store.cas('a',store.versions['a'],999)
  store.cas('a',store.versions['a'],3)
  ctrl.reconcile(j)
  self.assertEqual(j.state,'HOLD_CONCURRENT_CONFLICT')
  self.assertEqual(store.pages['a'],3)
 def test_single_page_refused(self):
  with self.assertRaises(ValueError):RecoveryController(FakeStore({'a':1})).run('ev',{'a':2})
 def test_idempotent_replay(self):
  store=FakeStore({'a':1,'b':2});first=RecoveryController(store).run('ev',{'a':3,'b':4})
  second=RecoveryController(store).run('ev',{'a':3,'b':4})
  self.assertIs(first,second);self.assertEqual(store.versions,{'a':1,'b':1})
 def test_event_payload_collision(self):
  store=FakeStore({'a':1,'b':2});RecoveryController(store).run('ev',{'a':3,'b':4})
  with self.assertRaises(Conflict):RecoveryController(store).run('ev',{'a':99,'b':4})
 def test_journal_export_import(self):
  store=FakeStore({'a':1,'b':2});j=RecoveryController(store).run('ev',{'a':3,'b':4},crash_at='AFTER_WRITE:a')
  restored=import_journal(export_journal(j));self.assertEqual(restored.state,'UNKNOWN_EFFECT')
  RecoveryController(store).reconcile(restored);self.assertEqual(store.pages,{'a':1,'b':2})
 def test_journal_tamper_rejected(self):
  store=FakeStore({'a':1,'b':2});j=RecoveryController(store).run('ev',{'a':3,'b':4})
  payload=export_journal(j)
  with self.assertRaises(StructuralError):import_journal(payload.replace('COMMITTED','FORGED'))
 def test_preflight_abort(self):
  store=FakeStore({'a':1,'b':2});ctl=RecoveryController(store)
  j=ctl.run('ev',{'a':3,'b':4},crash_at='BEFORE_PREFLIGHT')
  self.assertEqual(ctl.reconcile(j).state,'NOT_APPLIED')
if __name__=='__main__':unittest.main()
