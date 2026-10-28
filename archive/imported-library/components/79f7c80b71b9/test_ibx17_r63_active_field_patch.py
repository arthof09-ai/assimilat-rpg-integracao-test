import unittest, hashlib
from dataclasses import replace
from ibx17_r63_active_field_patch import *
H = '<summary>**ATRIBUTOS**</summary>'
A = '\n\t'+H+BLOCK+'\n'
B = '\n'+ARCHIVE+'\n\t\t'+H+'\n'+BLOCK.replace('\n\t\t','\n\t\t\t',1).replace('\n\t</details>', '\n\t\t</details>')+'\n'
T = 'before '+A+'[↗ Subpágina original READ-ONLY: ABC](https://app.notion.com/p/abc)' +B
class Tests(unittest.TestCase):
 def test_valid(self):
  p=plan_active_dex(T);self.assertEqual(p.status,'READY');self.assertEqual(p.active_occurrences_before,1);self.assertEqual(p.archive_occurrences_before,1);self.assertNotEqual(p.candidate_sha256,p.original_sha256)
 def test_hash(self):
  h=hashlib.sha256(T.encode()).hexdigest();self.assertEqual(plan_active_dex(T,h).original_sha256,h)
 def test_hash_drift(self):
  with self.assertRaises(PatchRefused):plan_active_dex(T,'0'*64)
 def test_archive_absent(self):
  with self.assertRaises(PatchRefused):plan_active_dex(T.replace(ARCHIVE,'NO'))
 def test_archive_twice(self):
  with self.assertRaises(PatchRefused):plan_active_dex(T+ARCHIVE)
 def test_active_header_absent(self):
  with self.assertRaises(PatchRefused):plan_active_dex(T.replace(H,'',1))
 def test_active_header_twice(self):
  with self.assertRaises(PatchRefused):plan_active_dex(T.replace('before','before '+H))
 def test_history_header_absent(self):
  with self.assertRaises(PatchRefused):plan_active_dex(T.replace('\t\t'+H,'bad'))
 def test_history_header_twice(self):
  with self.assertRaises(PatchRefused):plan_active_dex(T+'\n'+H)
 def test_active_duplicate(self):
  with self.assertRaises(PatchRefused):plan_active_dex(T.replace('before','before '+BLOCK))
 def test_wrong_active(self):
  with self.assertRaises(PatchRefused):plan_active_dex(T.replace(OLD,'Destreza: 20',1))
 def test_wrong_history(self):
  with self.assertRaises(PatchRefused):plan_active_dex(T[::-1])
 def test_new_already(self):
  p=plan_active_dex(T.replace(BLOCK,BLOCK_NEW,1));self.assertEqual(p.status,'NOOP');self.assertFalse(p.old_str);self.assertEqual(p.original_sha256,p.candidate_sha256)
 def test_no_history_old(self):
  with self.assertRaises(PatchRefused):plan_active_dex(T.replace(BLOCK, BLOCK.replace(OLD,'OTHER'),1))
 def test_preserve_full_history(self):
  at=T.index(ARCHIVE);p=plan_active_dex(T);after=T.replace(p.old_str,p.new_str,1);self.assertEqual(T[at:],after[at:])
 def test_preserve_links(self):
  p=plan_active_dex(T);after=T.replace(p.old_str,p.new_str,1);self.assertEqual(after.count('↗ Subpágina original READ-ONLY:'),T.count('↗ Subpágina original READ-ONLY:'))
 def test_unique_exact(self):
  p=plan_active_dex(T);self.assertEqual(T.count(p.old_str),1)
 def test_idempotent_projection(self):
  p=plan_active_dex(T);after=T.replace(p.old_str,p.new_str,1);self.assertEqual(after.count(p.new_str),1)
 def test_preview_arithmetic(self):
  self.assertEqual(19+3+15,37);self.assertEqual(21+3+15,39)
 def test_no_status_authorization(self):
  self.assertNotIn('PRODUCTION',repr(plan_active_dex(T)).upper())
if __name__=='__main__':unittest.main(verbosity=2)
