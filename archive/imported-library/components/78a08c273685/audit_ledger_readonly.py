"""Read and audit the consumed R190 local SQLite; no insert or native request."""
import json
from pathlib import Path
from r190_local_intent import DB,TX,STAGE
from r173_sqlite_causal_ledger import Ledger

def audit():
 with Ledger(DB) as l:
  chain=l.verify_chain(TX,STAGE)
  state=l.classify(TX,STAGE)
  result={'chain':chain,'classification':state,'journal_integrity':chain['observations']==5 and state['state']=='READBACK_AND_JOURNAL_OBSERVED_NOT_NATIVE_ATTESTATION','does_not_authorize_write':not state['native_write_authorized'],'replay_auto_denied':not state['automatic_retry_allowed']}
  if not(result['journal_integrity'] and result['does_not_authorize_write'] and result['replay_auto_denied']):raise ValueError('R190 ledger not in expected terminal observed self-review state')
  return result
if __name__=='__main__':print(json.dumps(audit(),ensure_ascii=False,indent=2))
