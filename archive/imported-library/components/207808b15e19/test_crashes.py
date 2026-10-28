"""Hard process-exit tests, not just Python exception injection."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from vlab_gateway import Gateway, Rejected, UncertainEffect

MASTER=b'Z'*32
OPERATOR='operator-secret-hardcrash-0123456789-abcdef'
CONTROLLER='controller-secret-hardcrash-0123456789-abcdef'

class CrashProcess(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.db=str(Path(self.tmp.name)/'crash.sqlite')
        self.g=Gateway(self.db,MASTER)
        self.g.bootstrap_principal('op','CM-000006','OPERATOR',OPERATOR,bootstrap_secret=MASTER)
        self.g.bootstrap_principal('control','CM-000001','CONTROLLER',CONTROLLER,bootstrap_secret=MASTER)
        self.claim=self.g.allocate(OPERATOR,'A');self.epoch=self.g.claim_domain(OPERATOR,self.claim)
        self.g.prepare(OPERATOR,self.claim,self.epoch,'crash-op','idem-crash','sandbox/crash',{'foo':'bar'},expected_revision=0)

    def tearDown(self):self.tmp.cleanup()

    def _run_crash(self, code):
        command="import os,sys,json;from vlab_gateway import Gateway;"+code+";os._exit(87)"
        env=os.environ.copy()
        env['PYTHONPATH']=str(Path(__file__).resolve().parents[1])
        p=subprocess.run([sys.executable,'-c',command],env=env,capture_output=True,timeout=8)
        self.assertEqual(p.returncode,87,p.stderr.decode())

    def test_external_dispatch_then_killed_process(self):
        self._run_crash("g=Gateway("+repr(self.db)+",b'Z'*32);g.begin_external_dispatch_simulation("+repr(OPERATOR)+","+repr(self.claim)+","+str(self.epoch)+",'crash-op')")
        gate=Gateway(self.db,MASTER)
        receipt=gate.recover_uncertain(CONTROLLER)
        self.assertEqual(receipt['unknown'],['crash-op'])
        self.assertEqual(gate.snapshot(CONTROLLER)['state'],'HOLD_UNKNOWN')
        with self.assertRaises(UncertainEffect):gate.revoke_and_fence(CONTROLLER)

    def test_local_commit_then_killed_process(self):
        self._run_crash("g=Gateway("+repr(self.db)+",b'Z'*32);g.commit_local("+repr(OPERATOR)+","+repr(self.claim)+","+str(self.epoch)+",'crash-op')")
        gate=Gateway(self.db,MASTER)
        self.assertEqual(gate.local_cell(CONTROLLER,'sandbox/crash')['revision'],1)
        self.assertEqual(gate.commit_local(OPERATOR,self.claim,self.epoch,'crash-op')['status'],'IDEMPOTENT_REPLAY')

    def test_no_leaked_real_credentials(self):
        self.assertEqual(self.g.snapshot(CONTROLLER)['notion_enforcement'],'NOT_IMPLEMENTED')

if __name__=='__main__':unittest.main()
