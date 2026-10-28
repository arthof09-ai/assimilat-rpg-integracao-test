import unittest, copy
from ibx17_native_contract_v1 import source,reconcile,reconcile_r107,prepare_envelope,IntegrityHold,ORDER
class TestR107(unittest.TestCase):
 def setUp(self):
  self.d,_=source('UP');self.before=self.d['before'];self.after=self.d['after']
 def mixed(self,count):return {k:(self.after if i<count else self.before)[k] for i,k in enumerate(ORDER)}
 def test_prepared(self):self.assertEqual(reconcile(self.d,self.mixed(0),())['status'],'PREPARED')
 def test_partial(self):self.assertEqual(reconcile(self.d,self.mixed(1),('NORMAL',))['next'],'TRANSFORM')
 def test_committed(self):self.assertEqual(reconcile(self.d,self.mixed(3),ORDER)['status'],'COMMITTED')
 def test_after_empty_journal_holds(self):
  with self.assertRaises(IntegrityHold):reconcile(self.d,self.mixed(3),())
 def test_before_claimed_normal_holds(self):
  with self.assertRaises(IntegrityHold):reconcile(self.d,self.mixed(0),('NORMAL',))
 def test_after_prepared_holds(self):
  with self.assertRaises(IntegrityHold):reconcile(self.d,self.mixed(3),())
 def test_write_before_journal_holds(self):
  with self.assertRaises(IntegrityHold):reconcile(self.d,self.mixed(1),())
 def test_unknown_holds(self):
  v=copy.deepcopy(self.mixed(0));v['NORMAL']['level']=900
  with self.assertRaises(IntegrityHold):reconcile(self.d,v,())
 def test_nonprefix_holds(self):
  v={'NORMAL':self.before['NORMAL'],'TRANSFORM':self.after['TRANSFORM'],'LOCKS':self.before['LOCKS']}
  with self.assertRaises(IntegrityHold):reconcile(self.d,v,())
 def test_identity_collision(self):
  e=prepare_envelope('IBX17-R108-TEST','target-test','lab','v1','UP','native-v1','LAB_TEST_EXPLICIT_FROM_MESTRE')
  live={**e,'target_version':'native-v1','status':'PREPARED'}
  self.assertEqual(reconcile_r107(self.d,self.mixed(0),{k:'PREPARED' for k in ORDER},e,live)['status'],'PREPARED')
  live['target_id']='OTHER'
  with self.assertRaises(IntegrityHold):reconcile_r107(self.d,self.mixed(0),{k:'PREPARED' for k in ORDER},e,live)
 def test_source_collision(self):
  e=prepare_envelope('IBX17-R108-TEST','target-test','lab','v1','UP','native-v1','LAB_TEST_EXPLICIT_FROM_MESTRE')
  live={**e,'target_version':'native-v1','status':'PREPARED','source_sha256':'0'*64}
  with self.assertRaises(IntegrityHold):reconcile_r107(self.d,self.mixed(0),{k:'PREPARED' for k in ORDER},e,live)
 def test_r104_positive(self):
  d,_=source('DOWN');self.assertEqual(reconcile(d,d['after'],ORDER)['status'],'COMMITTED')
if __name__=='__main__':unittest.main(verbosity=2)
