import copy,tempfile,unittest
from engine_r13 import *
from durable_r14 import *

class DurableR14(unittest.TestCase):
    def setUp(self):self.before=make_fixture();self.prepared=plan(self.before,make_choices_single(),'SIM-DURABLE-001')
    def test_wal_persisted_commit_reopen_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            ctl=DurableController(DurableStore(d,self.before));e=ctl.run(self.prepared)
            ctl2=DurableController(DurableStore(d))
            self.assertEqual(e['state'],'COMMITTED');self.assertEqual(ctl2.run(self.prepared)['state'],'COMMITTED')
            self.assertEqual(ctl2.store.get_all(),self.prepared['updates'])
    def test_explicit_inverse_durable_and_original_receipt(self):
        with tempfile.TemporaryDirectory() as d:
            ctl=DurableController(DurableStore(d,self.before));ctl.run(self.prepared)
            reverse=DurableController(DurableStore(d)).explicit_rollback('SIM-DURABLE-001')
            self.assertEqual(reverse['state'],'COMMITTED')
            self.assertEqual(DurableStore(d).get_all(),self.before)
            self.assertIn('EXPLICIT_INVERSE_COMMITTED:',str(DurableStore(d).event('SIM-DURABLE-001')))
    def test_crash_every_boundary_reopen_reconcile(self):
        boundaries=['BEFORE_PREPARE','AFTER_PREPARE']
        for key in ('NORMAL','TRANSFORM','LOCKS'):
            boundaries.extend(['BEFORE_WRITE:'+key,'AFTER_WRITE:'+key,'AFTER_READBACK:'+key])
        boundaries.append('AFTER_COMMIT')
        for boundary in boundaries:
            with self.subTest(boundary=boundary), tempfile.TemporaryDirectory() as d:
                ctl=DurableController(DurableStore(d,self.before))
                with self.assertRaises(SimulatedProcessCrash):ctl.run(self.prepared,crash_at=boundary)
                reopened=DurableController(DurableStore(d))
                state=reopened.recover('SIM-DURABLE-001')
                if boundary=='AFTER_COMMIT':
                    self.assertEqual(state,'COMMITTED');self.assertEqual(reopened.store.get_all(),self.prepared['updates'])
                else:
                    self.assertIn(state,('NOT_APPLIED_NO_WAL','ROLLED_BACK_VERIFIED'))
                    self.assertEqual(reopened.store.get_all(),self.before)
    def test_crash_during_compensation_resumes(self):
        with tempfile.TemporaryDirectory() as d:
            ctl=DurableController(DurableStore(d,self.before))
            with self.assertRaises(SimulatedProcessCrash):ctl.run(self.prepared,crash_at='AFTER_READBACK:LOCKS')
            for failure in ['AFTER_COMPENSATE:LOCKS','AFTER_COMPENSATE:TRANSFORM']:
                reopened=DurableController(DurableStore(d))
                with self.assertRaises(SimulatedProcessCrash):reopened.recover('SIM-DURABLE-001',crash_at=failure)
            self.assertEqual(DurableController(DurableStore(d)).recover('SIM-DURABLE-001'),'ROLLED_BACK_VERIFIED')
            self.assertEqual(DurableStore(d).get_all(),self.before)
    def test_persistent_event_collision_denied(self):
        with tempfile.TemporaryDirectory() as d:
            ctl=DurableController(DurableStore(d,self.before));ctl.run(self.prepared)
            fake=copy.deepcopy(self.prepared);fake['updates']['NORMAL']['hp_max']=999
            with self.assertRaises(Conflict):DurableController(DurableStore(d)).run(fake)
    def test_concurrent_page_change_denied(self):
        with tempfile.TemporaryDirectory() as d:
            ctl=DurableController(DurableStore(d,self.before))
            with self.assertRaises(SimulatedProcessCrash):ctl.run(self.prepared,crash_at='AFTER_WRITE:NORMAL')
            store=DurableStore(d);page,ver=store.read('NORMAL');page['hp_current']=2;store.cas('NORMAL',ver,page)
            self.assertEqual(DurableController(DurableStore(d)).recover('SIM-DURABLE-001'),'HOLD_CONCURRENT_CONFLICT')
            self.assertEqual(DurableStore(d).read('NORMAL')[0]['hp_current'],2)
    def test_integrity_tamper_detected(self):
        with tempfile.TemporaryDirectory() as d:
            ctl=DurableController(DurableStore(d,self.before));ctl.run(self.prepared)
            path=DurableStore(d)._event_path('SIM-DURABLE-001')
            x=path.read_text();path.write_text(x.replace('COMMITTED','FAKE-COMMIT'))
            with self.assertRaises(LedgerIntegrityError):DurableStore(d).event('SIM-DURABLE-001')
    def test_inverse_collision_concurrent_denied(self):
        with tempfile.TemporaryDirectory() as d:
            ctl=DurableController(DurableStore(d,self.before));ctl.run(self.prepared)
            store=DurableStore(d);value,v=store.read('LOCKS');store.cas('LOCKS',v,value)
            with self.assertRaises(Conflict):DurableController(DurableStore(d)).explicit_rollback('SIM-DURABLE-001')
    def test_filename_escape_denied(self):
        with tempfile.TemporaryDirectory() as d:
            s=DurableStore(d,self.before)
            with self.assertRaises(ValueError):s.event('../outside')

if __name__=='__main__':unittest.main()

# Exercise actual competing operating-system processes, not only sequential CAS.
def _competing_cas(directory,before_ver,value,barrier,queue):
    from durable_r14 import DurableStore,Conflict
    try:
        barrier.wait(timeout=8)
        s=DurableStore(directory)
        p,_=s.read('NORMAL');p['hp_current']=value
        s.cas('NORMAL',before_ver,p)
        queue.put('OK')
    except Conflict:queue.put('CONFLICT')
    except Exception as e:queue.put('OTHER:'+repr(e))

class LocalMultiprocessCAS(unittest.TestCase):
 def test_exactly_one_wins_concurrent_cas(self):
  import multiprocessing as mp
  with tempfile.TemporaryDirectory() as d:
   DurableStore(d,make_fixture())
   context=mp.get_context('fork')
   barrier=context.Barrier(2);q=context.Queue()
   p1=context.Process(target=_competing_cas,args=(d,0,8,barrier,q))
   p2=context.Process(target=_competing_cas,args=(d,0,9,barrier,q))
   p1.start();p2.start();p1.join(8);p2.join(8)
   self.assertEqual(p1.exitcode,0);self.assertEqual(p2.exitcode,0)
   self.assertEqual(sorted([q.get(timeout=2),q.get(timeout=2)]),['CONFLICT','OK'])
   self.assertEqual(DurableStore(d).read('NORMAL')[1],1)
