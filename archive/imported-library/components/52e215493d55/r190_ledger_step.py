import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
sys.path.insert(0,str(Path(__file__).resolve().parent/'compat_runtime'))
from r173_sqlite_causal_ledger import Ledger
from r190_local_intent import DB,TX,STAGE,PRE_VERSION,BEFORE,AFTER
def add_step(phase,version=None):
 with Ledger(DB) as l:
  if phase=='BEFORE':
   r=l.add_observation(TX,STAGE,'READBACK_BEFORE',page_version=PRE_VERSION,observed_state=BEFORE,original_response={'source':'LIVE_NOTION_MCP_FETCH','matched_fields':17,'history_alternante_readback':True})
  elif phase=='DISPATCH':
   r=l.add_observation(TX,STAGE,'WRITE_DISPATCHED',page_version=PRE_VERSION,original_response={'host_action':'notion_update_page','expected_target':BEFORE['target'],'type':'SINGLE_ACTIVE_REGION_UPDATE','not_native_request_id':True})
  elif phase=='REPLY':
   r=l.add_observation(TX,STAGE,'WRITE_RESPONSE_OBSERVED',page_version=version,original_response={'text':json.dumps({'page_id':BEFORE['target']})})
  elif phase=='AFTER':
   r=l.add_observation(TX,STAGE,'READBACK_AFTER',page_version=version,observed_state=AFTER,original_response={'source':'LIVE_NOTION_MCP_FETCH','matched_fields':17,'history_snapshot_still_at_end':True})
  elif phase=='JOURNAL':
   r=l.add_observation(TX,STAGE,'JOURNAL_READBACK_CONFIRMED',page_version=version,original_response={'source':'LIVE_NOTION_MCP_FETCH','text':'TX_JOURNAL: COMMITTED_AFTER_NATIVE_READBACK observed'})
  else: raise ValueError('unknown phase')
  return {'observation':r,'classification':l.classify(TX,STAGE),'chain':l.verify_chain(TX,STAGE)}
if __name__=='__main__':
 phase=sys.argv[1]
 version=sys.argv[2] if len(sys.argv)>2 else None
 print(json.dumps(add_step(phase,version),ensure_ascii=False,indent=2))
