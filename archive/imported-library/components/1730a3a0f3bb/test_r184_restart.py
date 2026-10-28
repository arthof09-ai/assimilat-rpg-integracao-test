"""R184: two separate Python processes; same synthetic host readback is NOOP on replay."""
import unittest,sys,json,tempfile,subprocess,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'runtime'),str(ROOT.parent/'src'/'baseline'/'runtime')]
from r173_sqlite_causal_ledger import Ledger,LAB,AUTH,digest
from r182_native_readback import CANARY,TX

class Restart(unittest.TestCase):
 def test_cross_process_reopen_replay(self):
  with tempfile.TemporaryDirectory() as temp:
   db=str(Path(temp)/'local.sqlite');cap=str(Path(temp)/'tool.json');
   with Ledger(db) as led:
    led.create_intent(tx=TX,stage='DOC_CANARY',target=CANARY,parent=LAB,source_version='TEST',
                      before={'target':CANARY,'field':'BRIDGE_PHYSICAL: BEFORE'},
                      after={'target':CANARY,'field':'BRIDGE_PHYSICAL: AFTER'},pre_version='TEST-v0',authority=AUTH)
   sha=digest({'target':CANARY,'field':'BRIDGE_PHYSICAL: AFTER'})
   s=f'<page url="https://app.notion.com/p/{CANARY}"><parent-page url="https://app.notion.com/p/{LAB}"/><content>BRIDGE_EVENT: {TX}\nBRIDGE_PHYSICAL: AFTER\nBRIDGE_JOURNAL: COMMITTED_AFTER_NATIVE_READBACK; tx={TX}; stage=DOC_CANARY; after_sha={sha}; SELF_REVIEW_ONLY</content></page>'
   payload={'structuredContent':{'text':s,'url':'https://app.notion.com/p/'+CANARY,'page_last_edited_at':'SYNTHETIC_TEST_VERSION'}}
   Path(cap).write_text(json.dumps(payload))
   command=[sys.executable,'-c',"import json,sys;from r182_native_readback import import_readback_idempotently;print(json.dumps(import_readback_idempotently(json.load(open(sys.argv[2])),sys.argv[1])))",db,cap]
   env=os.environ.copy();env['PYTHONPATH']=str(ROOT/'runtime')+os.pathsep+str(ROOT.parent/'src'/'runtime')+os.pathsep+str(ROOT.parent/'src'/'baseline'/'runtime')
   first=json.loads(subprocess.check_output(command,env=env,text=True))
   second=json.loads(subprocess.check_output(command,env=env,text=True))
   self.assertEqual((first['new_rows'],second['new_rows']),(1,0))
   with Ledger(db) as led:self.assertEqual(led.verify_chain(TX,'DOC_CANARY')['observations'],1)
if __name__=='__main__':unittest.main()
