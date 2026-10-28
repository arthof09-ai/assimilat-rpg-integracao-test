import copy,hashlib,json,multiprocessing,tempfile,unittest
from pathlib import Path
from roll_ledger_r17 import RollLedger,RollHold,derive
from durable_r14 import LedgerIntegrityError,_atomic_json,_sealed
from r10_recovery import digest,Conflict


def worker(root,q):
    r=RollLedger(root).draw('SIM-R17-CONCUR-001','SIM-R17-CONCUR','FF_MILESTONE_006_CA',4,1)
    q.put(r[1]['rolls'])

class R17DiceReceipts(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.ledger=RollLedger(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def test_commit_then_reveal_distinct_durable_steps(self):
        c=self.ledger.commit('SIM-R17-001','SIM-R17-A','LV07_NORMAL_HP',8,1)
        self.assertEqual(c['state'],'COMMITTED_HIDDEN')
        self.assertIsNone(self.ledger.read('SIM-R17-001')['receipt'])
        r=self.ledger.reveal('SIM-R17-001','SIM-R17-A','LV07_NORMAL_HP',8,1)
        self.assertEqual(r['source'],'OS_ENTROPY_LOCAL_SIMULATION')
        self.assertTrue(RollLedger.verify(r));self.assertIn(r['rolls'][0],range(1,9))
        self.assertEqual(r,RollLedger(self.tmp.name).reveal('SIM-R17-001','SIM-R17-A','LV07_NORMAL_HP',8,1))
    def test_roll_idempotent_same_contract(self):
        x=self.ledger.draw('SIM-R17-B','SIM-R17-Z','LV07_NORMAL_PA',8,1)
        y=self.ledger.draw('SIM-R17-B','SIM-R17-Z','LV07_NORMAL_PA',8,1)
        self.assertEqual(x[1],y[1])
        self.assertEqual(x[0]['commitment'],y[0]['commitment'])
    def test_roll_conflict_different_die(self):
        self.ledger.commit('SIM-R17-B','SIM-R17-Z','LV07_NORMAL_PA',8,1)
        with self.assertRaises(Conflict):self.ledger.commit('SIM-R17-B','SIM-R17-Z','LV07_NORMAL_PA',10,1)
    def test_roll_conflict_different_event(self):
        self.ledger.commit('SIM-R17-B','SIM-R17-Z','LV07_NORMAL_PA',8,1)
        with self.assertRaises(Conflict):self.ledger.commit('SIM-R17-B','SIM-R17-OTHER','LV07_NORMAL_PA',8,1)
    def test_roll_conflict_different_purpose(self):
        self.ledger.commit('SIM-R17-B','SIM-R17-Z','LV07_NORMAL_PA',8,1)
        with self.assertRaises(Conflict):self.ledger.commit('SIM-R17-B','SIM-R17-Z','LV07_NORMAL_HP',8,1)
    def test_no_reveal_before_commit(self):
        with self.assertRaises(RollHold):self.ledger.reveal('SIM-R17-UNSEEN','SIM-R17-A','LV07_NORMAL_PA',8,1)
    def test_non_synthetic_denied(self):
        with self.assertRaises(RollHold):self.ledger.commit('PLAYER-001','SIM-R17-A','LV07_NORMAL_PA',8,1)
        with self.assertRaises(RollHold):self.ledger.commit('SIM-R17-X','REAL-PLAYER','LV07_NORMAL_PA',8,1)
    def test_invalid_sides_and_count(self):
        for sides,count in [(0,1),(1,1),(61,1),(8,0),(8,26),(8,True)]:
            with self.subTest(sides=sides,count=count):
                with self.assertRaises(RollHold):self.ledger.commit('SIM-R17-X','SIM-R17-A','LV07_NORMAL_PA',sides,count)
    def test_replay_detects_value_tampering(self):
        r=self.ledger.draw('SIM-R17-B','SIM-R17-Z','LV07_NORMAL_PA',8,1)[1]
        f=copy.deepcopy(r);f['rolls'][0]=f['rolls'][0]%8+1
        f['sum']=sum(f['rolls']);f['receipt_sha256']=digest({k:v for k,v in f.items() if k!='receipt_sha256'})
        with self.assertRaises(LedgerIntegrityError):RollLedger.verify(f)
    def test_replay_detects_hash_tampering(self):
        r=self.ledger.draw('SIM-R17-B','SIM-R17-Z','LV07_NORMAL_PA',8,1)[1]
        f=copy.deepcopy(r);f['receipt_sha256']='0'*64
        with self.assertRaises(LedgerIntegrityError):RollLedger.verify(f)
    def test_replay_detects_commit_tampering(self):
        r=self.ledger.draw('SIM-R17-B','SIM-R17-Z','LV07_NORMAL_PA',8,1)[1]
        f=copy.deepcopy(r);f['commitment']='a'*64
        f['receipt_sha256']=digest({k:v for k,v in f.items() if k!='receipt_sha256'})
        with self.assertRaises(LedgerIntegrityError):RollLedger.verify(f)
    def test_crash_after_commit_reopen_returns_same_values(self):
        self.ledger.commit('SIM-R17-X','SIM-R17-Y','LV07_NORMAL_HP',8,3)
        reopened=RollLedger(self.tmp.name)
        rec=reopened.reveal('SIM-R17-X','SIM-R17-Y','LV07_NORMAL_HP',8,3)
        self.assertEqual(len(rec['rolls']),3)
        self.assertTrue(RollLedger.verify(rec))
    def test_fsync_storage_integrity(self):
        self.ledger.commit('SIM-R17-X','SIM-R17-Y','LV07_NORMAL_HP',8,3)
        f=Path(self.tmp.name)/'SIM-R17-X.json'
        payload=json.loads(f.read_text());payload['body']['commitment']='a'*64
        f.write_text(json.dumps(payload))
        with self.assertRaises(LedgerIntegrityError):self.ledger.reveal('SIM-R17-X','SIM-R17-Y','LV07_NORMAL_HP',8,3)
    def test_receipts_multiple_counts_and_dice(self):
        for die in (4,6,8,10,12,20,30,40,50,60):
            r=self.ledger.draw(f'SIM-R17-D{die}','SIM-R17-C',f'DIE_{die}',die,25)[1]
            self.assertTrue(RollLedger.verify(r))
            self.assertEqual(len(r['rolls']),25)
            self.assertTrue(all(1<=x<=die for x in r['rolls']))
    def test_process_lock_single_receipt(self):
        q=multiprocessing.Queue()
        a=multiprocessing.Process(target=worker,args=(self.tmp.name,q))
        b=multiprocessing.Process(target=worker,args=(self.tmp.name,q))
        a.start();b.start();a.join(10);b.join(10)
        self.assertEqual(a.exitcode,0);self.assertEqual(b.exitcode,0)
        self.assertEqual(q.get(timeout=2),q.get(timeout=2))
        self.assertEqual(len(self.ledger.all_receipts()),1)
    def test_spec_is_in_hash(self):
        a=self.ledger.draw('SIM-R17-X','SIM-R17-Y','LV07_NORMAL_HP',8,3)[1]
        b=self.ledger.draw('SIM-R17-V','SIM-R17-Y','LV07_NORMAL_PA',8,3)[1]
        self.assertNotEqual(a['commitment'],b['commitment'])
        self.assertNotEqual(a['receipt_sha256'],b['receipt_sha256'])

if __name__=='__main__':unittest.main()
