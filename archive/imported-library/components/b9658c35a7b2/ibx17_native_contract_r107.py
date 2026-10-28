"""R107 additive correction of R102 contract; historical original in previous ZIP.
No Notion credential, no production writer. This module fails closed on evidence mismatch.
"""
from __future__ import annotations
import json, hashlib
from pathlib import Path
ROOT=Path(__file__).parent
ORDER=('NORMAL','TRANSFORM','LOCKS')
FILES={'UP':'IBX17_R75_UP_PAYLOAD_COMPACT_20261016.json','DOWN':'IBX17_R76_DOWN_PAYLOAD_COMPACT_20261016.json'}
FORBIDDEN={'IBX17-R99-NATIVE-UP-20261016-01','IBX17-R103-PARTIAL-UP-20261016-01','IBX17-R104-NATIVE-DOWN-20261016-01','SIM-CHAT-9db12e1347c71251a4e3','SIM-LD-a711880f2315b25a8c69cc88'}
class IntegrityHold(RuntimeError):pass

def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def fp(v):return hashlib.sha256(canonical(v)).hexdigest()
def source(kind):
 if kind not in FILES:raise IntegrityHold('unknown receipt kind')
 data=(ROOT/FILES[kind]).read_bytes();d=json.loads(data)
 if d['kind']!=kind or d.get('fixture_label')!='SYNTHETIC_EXPLICIT_ONLY' or set(d['before'])!=set(ORDER) or set(d['after'])!=set(ORDER):raise IntegrityHold('invalid historical receipt')
 return d,{'filename':FILES[kind],'sha256':hashlib.sha256(data).hexdigest(),'before_hash':fp(d['before']),'after_hash':fp(d['after']),'historical_event':d['event_id'],'engine':d['engine']}

def prepare_envelope(event_id,target_id,target_parent_id,source_version,receipt_kind,pre_version,authority_marker):
 if not event_id or event_id in FORBIDDEN or not target_id or not target_parent_id or not source_version or not pre_version:raise IntegrityHold('missing/consumed identity')
 if authority_marker!='LAB_TEST_EXPLICIT_FROM_MESTRE':raise IntegrityHold('no test authorization')
 d,s=source(receipt_kind)
 return {'event_id':event_id,'target_id':target_id,'parent_id':target_parent_id,'source_version':source_version,'pre_version':pre_version,'authority':authority_marker,'source_sha256':s['sha256'],'source_event':s['historical_event'],'before_hash':s['before_hash'],'after_hash':s['after_hash'],'kind':receipt_kind,'status':'PREPARED','writeset':list(ORDER)}

def check_envelope(envelope,actual,target_version,receipt):
 """A change to the page after preview requires a new explicit stage readback, never blind retry."""
 keys=['event_id','target_id','parent_id','source_version','pre_version','authority','source_sha256','source_event','before_hash','after_hash','kind']
 for k in keys:
  if not envelope.get(k) or envelope.get(k)!=actual.get(k):raise IntegrityHold('IDENTITY_OR_SOURCE_COLLISION:'+k)
 if actual.get('target_version')!=target_version:raise IntegrityHold('TARGET_VERSION_CHANGED')
 if actual.get('authority')!='LAB_TEST_EXPLICIT_FROM_MESTRE':raise IntegrityHold('NO_AUTHORITY')
 if actual.get('status') in ('ABORTED','CONFLICT','UNKNOWN_EFFECT'):raise IntegrityHold('EVENT_TERMINAL_HOLD')
 _,s=source(envelope['kind'])
 if envelope['source_sha256']!=s['sha256'] or envelope['before_hash']!=fp(receipt['before']) or envelope['after_hash']!=fp(receipt['after']):raise IntegrityHold('SOURCE_RECEIPT_MISMATCH')
 return True

def reconcile(receipt, observed, committed):
 """Legacy R102 signature with FIX: physical stage AND journal must match for all branches.
 committed is persisted ordered list of durable COMMITTED journal entries, not caller guesses.
 All AFTER with missing journal is HOLD_JOURNAL_GAP, not COMMITTED.
 """
 if tuple(x for x in committed if x in ORDER)!=tuple(committed) or len(set(committed))!=len(committed):raise IntegrityHold('JOURNAL_INVALID')
 if set(observed)!=set(ORDER):raise IntegrityHold('INCOMPLETE_STATE')
 states=[]
 for k in ORDER:
  v=observed[k]
  h=fp(v)
  if h==fp(receipt['after'][k]):states.append('AFTER')
  elif h==fp(receipt['before'][k]):states.append('BEFORE')
  else:raise IntegrityHold('UNKNOWN_EFFECT:'+k)
 count=states.count('AFTER')
 if states!=['AFTER']*count+['BEFORE']*(3-count):raise IntegrityHold('NON_PREFIX_EFFECT')
 if tuple(ORDER[:count])!=tuple(committed):raise IntegrityHold('JOURNAL_STATE_CONFLICT')
 return {'status':'COMMITTED' if count==3 else 'PREPARED' if count==0 else 'PARTIAL_RECOVERABLE','next':None if count==3 else ORDER[count], 'progress':states,'skip_already_applied':list(committed),'duplicate_effects_allowed':False}

def reconcile_r107(receipt,observed,journal,envelope,live):
 """Source identity + physical version + journal are jointly necessary; immutable provenance required."""
 check_envelope(envelope,live,live.get('target_version'),receipt)
 if live.get('target_id')!=envelope['target_id'] or live.get('pre_version')!=envelope['pre_version']:raise IntegrityHold('WRONG_TARGET_VERSION')
 if set(journal)!=set(ORDER):raise IntegrityHold('MISSING_JOURNAL_STAGE')
 if any(journal[k] not in ('PREPARED','COMMITTED') for k in ORDER):raise IntegrityHold('INVALID_JOURNAL_STATUS')
 committed=tuple(k for k in ORDER if journal[k]=='COMMITTED')
 result=reconcile(receipt,observed,committed)
 if result['status']=='COMMITTED' and live.get('status') not in ('COMMITTED_VERIFIED','COMMIT_PENDING_REOPEN'):raise IntegrityHold('MISSING_FINAL_COMMIT_MARKER')
 if result['status']=='PREPARED' and live.get('status') not in ('PREPARED','AUTHORIZED_TEST','SNAPSHOT_CAPTURED'):raise IntegrityHold('PREPARED_STATUS_CONFLICT')
 return {**result,'identity_checked':True,'source_checked':True,'journal_checked':True,'final_marker_checked':result['status']=='COMMITTED'}

if __name__=='__main__':
 for kind in FILES:
  d,s=source(kind); print(kind,s['sha256'],s['engine'])

def reconcile_native(receipt, observed, journal, expected, live):
 """R107 generic native contract (R108+). No mechanics invented: BEFORE/AFTER supplied
 by separately sourced planner. This is a VERIFY-ONLY gate, not a Notion writer.
 Must have a page ID, original source version, receipt identity, confirmation marker,
 source SHA, PRE capture and a specific native version from current fetch.
 """
 required=('event_id','target_id','parent_id','source_version','pre_version',
           'source_sha256','receipt_sha256','authority','confirmation')
 for key in required:
  if not expected.get(key) or expected[key]!=live.get(key):raise IntegrityHold('IDENTITY_COLLISION:'+key)
 if live['authority']!='LAB_TEST_EXPLICIT_FROM_MESTRE' or live['confirmation']!='TEST_PLAN_EXPLICIT_NOT_PLAYER':raise IntegrityHold('AUTHORIZATION_HOLD')
 if not live.get('target_version') or not live.get('pre_snapshot_confirmed'):raise IntegrityHold('MISSING_NATIVE_SNAPSHOT')
 if fp(receipt)!=expected['receipt_sha256']:raise IntegrityHold('RECEIPT_HASH_MISMATCH')
 if set(journal)!=set(ORDER) or any(journal[k] not in ('PREPARED','COMMITTED') for k in ORDER):raise IntegrityHold('JOURNAL_INVALID')
 if set(observed)!=set(ORDER):raise IntegrityHold('INCOMPLETE_STATE')
 states=[]
 for k in ORDER:
  bh,ah=fp(receipt['before'][k]),fp(receipt['after'][k]); v=fp(observed[k])
  if bh==ah:
   # A no-op group cannot be proved 'written' by its bytes. Require explicit journal.
   if v!=bh:raise IntegrityHold('UNKNOWN_EFFECT:'+k)
   states.append('AFTER' if journal[k]=='COMMITTED' else 'BEFORE')
  elif v==ah:states.append('AFTER')
  elif v==bh:states.append('BEFORE')
  else:raise IntegrityHold('UNKNOWN_EFFECT:'+k)
 count=states.count('AFTER')
 if states!=['AFTER']*count+['BEFORE']*(3-count):raise IntegrityHold('NON_PREFIX_EFFECT')
 for i,k in enumerate(ORDER):
  if journal[k] != ('COMMITTED' if i<count else 'PREPARED'):raise IntegrityHold('JOURNAL_STATE_CONFLICT:'+k)
 status='PREPARED' if count==0 else 'COMMITTED' if count==3 else 'PARTIAL_RECOVERABLE'
 if status=='COMMITTED' and live.get('status') not in ('COMMITTED_VERIFIED','COMMIT_PENDING_REOPEN'):raise IntegrityHold('MISSING_FINAL_COMMIT_MARKER')
 return {'status':status,'next':ORDER[count] if count<3 else None,
         'states':states,'skip':list(ORDER[:count]),'idempotent':status=='COMMITTED',
         'source_verified':True,'authorization_verified':True}
