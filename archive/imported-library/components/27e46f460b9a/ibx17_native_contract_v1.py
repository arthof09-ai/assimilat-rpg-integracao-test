"""R102 operational interface for LEVEL-UP-ENGINE/IBX-17.

Original R95 is preserved unchanged. This aditive adapter prepares deterministic,
source-bound TEST transactions, validates before/after and generates write stages.
It has *no* direct Notion API credentials: the authorized Notion tool bridge
performs guarded calls and must reopen objects after each stage. Never label
`test_authorized` as a player confirmation.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import copy, hashlib, json, sys
from typing import Any
ROOT=Path(__file__).parent
FILES={'UP':'IBX17_R75_UP_PAYLOAD_COMPACT_20261016.json',
       'DOWN':'IBX17_R76_DOWN_PAYLOAD_COMPACT_20261016.json'}
ORDER=('NORMAL','TRANSFORM','LOCKS')
EVENTS={'R103':'IBX17-R103-PARTIAL-UP-20261016-01',
        'R104':'IBX17-R104-NATIVE-DOWN-20261016-01'}
HISTORICAL_FORBIDDEN={'SIM-CHAT-9db12e1347c71251a4e3',
 'SIM-LD-a711880f2315b25a8c69cc88', 'IBX17-R99-NATIVE-UP-20261016-01',
 'IBX17-R88-CORR-DOWN-COPY-20261016-01'}

def canonical(data:Any)->bytes:
 return json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def fp(data:Any)->str:return hashlib.sha256(canonical(data)).hexdigest()
def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()

def source(kind:str):
 p=ROOT/FILES[kind]; raw=p.read_bytes();d=json.loads(raw)
 if d['kind']!=kind or d['fixture_label']!='SYNTHETIC_EXPLICIT_ONLY' or sorted(d['after'])!=sorted(ORDER) or sorted(d['before'])!=sorted(ORDER):raise ValueError('invalid historical receipt')
 return d, {'filename':p.name,'raw_sha256':sha(raw),'raw_bytes':len(raw),
            'fp_before':fp(d['before']),'fp_after':fp(d['after']),
            'engine':d['engine'],'historical_event':d['event_id']}

@dataclass
class Plan:
 event_id:str; target_id:str; source_version:str; kind:str; preview:dict;
 authorized_test:bool; pre_hash:str; writeset:tuple[str,...]; stages:tuple[str,...];
 after_hash:str; status:str='PREPARED'
 def __post_init__(self):
  if self.event_id in HISTORICAL_FORBIDDEN:raise ValueError('historical event reuse')
  if not self.target_id: raise ValueError('missing target')
  if self.writeset!=ORDER or self.stages!=ORDER:raise ValueError('partial/inconsistent stage contract')
  if not self.authorized_test:raise ValueError('test authorization missing')

class IntegrityHold(RuntimeError):pass

def reconcile(receipt:dict,observed:dict,committed:tuple[str,...]):
 """Read-only recovery decision. Never redo an applied group."""
 progress=[]
 for group in ORDER:
  v=observed[group]
  if fp(v)==fp(receipt['after'][group]):progress.append('AFTER')
  elif fp(v)==fp(receipt['before'][group]):progress.append('BEFORE')
  else:raise IntegrityHold(f'{group}: neither BEFORE nor AFTER; unknown effect')
 if progress==['BEFORE']*3:return {'status':'PREPARED','next':'NORMAL','progress':progress}
 if progress==['AFTER']*3:return {'status':'COMMITTED','next':None,'progress':progress}
 # Prefix-only committable; any scattered changes = held.
 if progress not in (['AFTER','BEFORE','BEFORE'],['AFTER','AFTER','BEFORE']):
  raise IntegrityHold(f'non-prefix state {progress}')
 for stage in committed:
  if progress[ORDER.index(stage)]!='AFTER':raise IntegrityHold(f'journal missing committed stage {stage}')
 expected_prefix=[ORDER[i] for i,p in enumerate(progress) if p=='AFTER']
 if tuple(expected_prefix)!=committed:raise IntegrityHold('journal/readback mismatch')
 next_group=ORDER[len(committed)]
 return {'status':'PARTIAL_RECOVERABLE','next':next_group,'progress':progress,
         'skip_already_applied':list(committed),'duplicate_effects_allowed':False}

def preview(d:dict)->dict:
 before,after=d['before']['NORMAL'],d['after']['NORMAL']
 return {'type':d['kind'],'synthetic':True,'old_level':before['level'],
         'new_level':after['level'],
         'natural_attribute_delta':{k:after['attrs'][k]-v for k,v in before['attrs'].items()},
         'life_max':[before['hp_max'],after['hp_max']],
         'pa_max':[before['pa_max'],after['pa_max']],
         'ff':[before['derived']['ff'],after['derived']['ff']],
         'ca':[before['derived']['ca'],after['derived']['ca']],
         'locks_count':[len(d['before']['LOCKS']['milestones']),
                        len(d['after']['LOCKS']['milestones'])],
         'player_confirmed':False,'test_authority_from_order':True}

def build_contract(stage:str,target_id:str,source_version:str)->dict:
 kind='UP' if stage=='R103' else 'DOWN'
 d,m=source(kind)
 contract=Plan(EVENTS[stage],target_id,source_version,kind,preview(d),True,
               m['fp_before'],ORDER,ORDER,m['fp_after'])
 return {'stage':stage,'interface':'R95→ADAPTER-NOTION (explicit, semi-manual)',
         'source':m,'transaction':contract.__dict__,
         'stage_before':{k:fp(d['before'][k]) for k in ORDER},
         'stage_after':{k:fp(d['after'][k]) for k in ORDER},
         'notion_api_direct_from_python':False,
         'native_bridge_requires_reopen_after_each_stage':True,
         'state_machine':['PREPARED','AUTHORIZED_TEST','SNAPSHOT_CAPTURED',
                          'NORMAL_COMMITTED','FAIL_INJECTED','PARTIAL_REOPENED',
                          'TRANSFORM_COMMITTED','LOCKS_COMMITTED','COMMITTED_VERIFIED'],
         'failed_unknown_effect':'HOLD_REOPEN_BEFORE_ANY_RETRY',
         'idempotence_policy':'read-only NOOP when TX marker exists AND 3/3 AFTER; reject collisions'}

if __name__=='__main__':
 assert source('UP')[0]['before']['NORMAL']['level']==16
 assert source('DOWN')[0]['after']['NORMAL']['level']==16
 u=source('UP')[0]
 assert reconcile(u,{k:u['before'][k] for k in ORDER},())['next']=='NORMAL'
 assert reconcile(u,{k:(u['after'] if k=='NORMAL' else u['before'])[k] for k in ORDER},('NORMAL',))['next']=='TRANSFORM'
 assert reconcile(u,{k:u['after'][k] for k in ORDER},ORDER)['status']=='COMMITTED'
 # unknown-effect must remain HOLD, no unjournaled partial accepted.
 broken=copy.deepcopy(u['before']);broken['NORMAL']['level']=99
 for obs,journal in [(broken,()),({k:(u['after'] if k=='NORMAL' else u['before'])[k] for k in ORDER},())]:
  try:reconcile(u,obs,journal)
  except IntegrityHold:pass
  else:raise AssertionError('unknown/un-journaled effect was accepted')
 print(json.dumps({'source_UP':source('UP')[1],'source_DOWN':source('DOWN')[1],
  'unit':'R102','tests':'5/5 state-machine invariants','native_execution':False},indent=2))
