"""R27 MESTRE-SIDE: baseline científico condicionado sobre motores históricos R18/R25/R26.
Sem motor paralelo, sem escrita canônica. Automatic miss POLICY = Mestre-exclusive VLAB.
"""
from __future__ import annotations
import copy, hashlib, json, os, sqlite3, tempfile, zipfile
from pathlib import Path
from dataclasses import asdict
import vlab_r18_interactive as core
import vlab_r20_configured as r20
import vlab_r21_dynamic_a1 as a1
import vlab_r25_rule_derived_benchmark as r25
import vlab_r26_master_rulings as r26
from a1_event_reducer import A1WindowReducer

VERSION='VLAB-R27-SCIENTIFIC-BASELINE-CONDITIONAL-1'
MODE='RULE_DERIVED_VIRTUAL_CONDITIONAL_MESTRE_CRIT_FAIL_LAB'
CRIT_FAIL_POLICY='MESTRE-20261015-VLAB-CRITICAL_FAILURE-AUTOMATIC_MISS_NO_PENALTY'
PROFILES={
 'OFENSIVO':{'FOR':20,'DES':4,'CON':10,'INT':3,'SAB':3,'CAR':3},
 'DEFENSIVO':{'FOR':6,'DES':12,'CON':15,'INT':4,'SAB':3,'CAR':3},
 'EQUILIBRADO':{'FOR':12,'DES':9,'CON':10,'INT':4,'SAB':4,'CAR':4},
 'ASSIMETRICO':{'FOR':2,'DES':22,'CON':10,'INT':3,'SAB':3,'CAR':3},
}
SEEDS=(11,23,37,41,53,67,71,83,97,101,113,127,131,149,157,163,173,181,191,197)
PRE_REG_CELLS=16
PRE_REG_ATTEMPTS=PRE_REG_CELLS*len(SEEDS)
MAX_ROUNDS=24

class R27Hold(r26.R26Hold):pass

def validation_alloc(attrs):
 if set(attrs)!=set(r25.ATTRIBUTE_ALLOCATION['RULE_BEAST_A']) or any(type(x)!=int or x<0 for x in attrs.values()) or sum(attrs.values())!=43:
  raise R27Hold('ALLOCATION_NOT_RULE_DERIVED_35_PLUS_8')
 if attrs['CON']%5:raise R27Hold('FRACTIONAL_CA_WITHOUT_ROUNDING_RULE')
 return True

def roster(left,right):
 out=[]
 for i,profile in enumerate((left,right)):
  v=PROFILES[profile];validation_alloc(v)
  out.append({'name':'RULE-DERIVED-'+profile+'-'+str(i),
    'hp':40+v['CON'],'pa':40+v['INT'],'ca':10+v['DES']+v['CON']//5,
    'for':v['FOR'],'des':v['DES'],'con':v['CON'],
    'luta':6,'init_bonus':0,'damage_bonus':0,'damage_tag':'impacto','fort':0,'reflex':0})
 return out

def manifest(left,right,kind):
 return {'schema':'R27_FROZEN_EXPERIMENT','version':VERSION,'mode':MODE,'kind':kind,
  'rank':'BRONZE1','universe':'TWO_NONCANONICAL_NORMAL_BEAST_ARCHETYPES',
  'profiles':{'LEFT':left,'RIGHT':right},'allocations':{k:copy.deepcopy(PROFILES[k]) for k in (left,right)},
  'conditioned_assumptions':{
    'luta_training':'+6 assigned to Luta for both as declared experimental choice, not source verified individual training',
    'attack': 'STANDARD basic attack 1d6+FOR+6; selected as scenario policy',
    'attack_PA':'0 via historical v0.7 test fixture, not proved for a named ability',
    'damage':'3d6 generic Bronze1 Besta normal, no named ability',
    'damage_tag':'impacto transport placeholder (typed special interactions excluded)',
    'rd':'5 generic normal Bronze1 Besta',
    'reaction':'no voluntary DEFENDER; reaction temporal reset historical R26 still logged',
    'geometry':'two actors initially adjacent, no movement or opportunity triggers',
    'hp_zero':'terminal LAB only, not canonical death',
    'critical_negative':CRIT_FAIL_POLICY,
    'critical_positive':'3d6+18 max-dice overlay fed to v0.8.1',
    'initiative':'Mestre DES then repeat only tied; historical dice'},
  'source_pages':['3ebc2b32-4ede-81f4-992a-c88a3588cacd','3ebc2b32-4ede-81f1-be4b-e8804ac113c0',
                  '3f3c2b32-4ede-81d4-80db-f11732734463'],
  'no_canonical_credit':True,'DMG_RANK_v11_UNCHANGED':True}

def create(db,seed,left,right,kind='PROFILE_MATRIX'):
 if Path(db).exists():raise R27Hold('GENESIS_EXISTS_NO_OVERWRITE')
 if (left,right)!=(None,None):
  if left not in PROFILES or right not in PROFILES:raise R27Hold('UNKNOWN_PROFILE')
  fighters=roster(left,right)
  a1.create(db,seed,fighters,defender=False)
 else:
  r26.create(db,seed)
  left,right='ORIGINAL_A','ORIGINAL_B'
  kind='ORIGINAL_R26_FROZEN_ROSTER'
 conf=manifest(left,right,kind) if kind=='PROFILE_MATRIX' else {'schema':'R27_FROZEN_ORIGINAL_R26','version':VERSION,'mode':MODE,
  'kind':kind,'source_manifest_sha':core.sha(r25.source_manifest()),'old_rulings':list(r26.DECISION_IDS),
  'critical_failure':CRIT_FAIL_POLICY,'no_canonical_credit':True}
 con=core.connect(db)
 try:
  con.execute('BEGIN IMMEDIATE');m=dict(con.execute('SELECT key,value FROM meta'))
  if m['revision']!='0':raise R27Hold('NOT_GENESIS')
  st=json.loads(m['state']);st['r27_science']={'version':VERSION,'mode':MODE,'kind':kind,'configuration':conf,
    'config_sha':core.sha(conf),'policy':'FIRST_NORMAL_ATTACK_NO_VOLUNTARY_REACTION',
    'critical_failure':CRIT_FAIL_POLICY,'no_canon':True}
  con.execute("UPDATE meta SET value=? WHERE key='state'",(core.canonical(st),));con.commit()
 except Exception:con.rollback();raise
 finally:con.close()
 return checked(db)

def checked(db):
 st,head,rev=a1.checked_load(db)
 cfg=st.get('r27_science')
 if not cfg or cfg['version']!=VERSION or cfg['mode']!=MODE or core.sha(cfg['configuration'])!=cfg['config_sha'] or cfg['critical_failure']!=CRIT_FAIL_POLICY:
  raise R27Hold('CONFIGURATION_OR_VERSION_TAMPERED')
 if cfg['kind']=='PROFILE_MATRIX':
  pair=cfg['configuration']['profiles']; expected=r20.validated_roster(roster(pair['LEFT'],pair['RIGHT']))
  if st['r20_setup']['fighters']!=expected or cfg['configuration']!=manifest(pair['LEFT'],pair['RIGHT'],'PROFILE_MATRIX'):
   raise R27Hold('PROFILE_ROSTER_OR_DERIVATION_CHANGED')
 elif cfg['kind']=='ORIGINAL_R26_FROZEN_ROSTER':
  r26.checked(db)
 else:raise R27Hold('UNKNOWN_EXPERIMENT_KIND')
 return st,head,rev

def pre(st,seq):
 return r26.preview(st,seq)

def runner(st,payload,seq):
 if st['r27_science']['critical_failure']!=CRIT_FAIL_POLICY:raise R27Hold('NO_LAB_CRITICAL_POLICY')
 kind=payload['action']
 if st['phase']=='INIT':
  if kind!='START':raise R27Hold('START_EXPECTED')
  detail=r26.resolve_initial_state(st)
  st['r21_control']['order']=st['order'][:]
  red=A1WindowReducer(a1._gateway(st,st['order']),order=tuple(st['order']),test_only=True)
  refresh=r26.refresh_own_turn(st,st['active'])
  ev=[a1._append(st,red,'ROUND_START',None),a1._append(st,red,'TURN_START',st['active'])]
  detail['reaction_refresh']=refresh
 else:
  if kind!='ATTACK':raise R27Hold('ONLY_ATTACK')
  red=a1._fresh(st);a1._assert_alignment(st,red)
  p=pre(st,seq)
  if p is None or p!=payload['preview']:raise R27Hold('PREVIEW_CHANGED')
  critical_fail=p['critical_trigger']=='NEGATIVE'
  applied=copy.deepcopy(p)
  if critical_fail:
   # Explicit Mestre LAB POLICY: automatic miss. Native v0.8.1 consumes
   # STANDARD and persists zero HP delta; rolls remain unmodified in p.
   # 0 is a synthetic reducer input *only* for forced miss; NOT a real attack roll.
   applied['hit_total']=0
   applied['damage_requested']=0
  n=r25.native(st,applied,seq)
  if critical_fail:
   e=n['effect']
   if e['roll_score']!=0 or e['hit'] or e['raw'] or e['net'] or e['before_hp']!=e['after_hp']:
    raise R27Hold('CRITFAIL_POLICY_NOT_ATOMIC_ZERO_DAMAGE')
   if st['actors'][p['actor']]['resource']['standard']!=0:raise R27Hold('CRITFAIL_STANDARD_NOT_CONSUMED')
  st['roll_nonce']=p['nonce'];actor=p['actor']
  fallen=[aid for aid,obj in st['actors'].items() if obj['resource']['hp']<=0]
  if fallen:
   st['phase']='COMPLETE_LAB';st['winner']=actor;st['finish_reason']='HP_ZERO_LAB_CONDITIONAL'
   st['active']=None;change={'combat_ended':True};refresh=None
  else:
   change=core._next_turn(st)
   refresh=r26.refresh_own_turn(st,st['active'])
  ev=[a1._append(st,red,'TURN_END',actor)]
  if st['phase']=='ACTIVE':
   if st['turn']==0:
    ev.extend([a1._append(st,red,'ROUND_END',None),a1._append(st,red,'ROUND_START',None)])
   ev.append(a1._append(st,red,'TURN_START',st['active']))
  detail={'kind':'RULE_DERIVED_ATTACK','preview':p,'native':n,'turn_control':change,'reaction_refresh':refresh,
   'critical_failure_policy':CRIT_FAIL_POLICY if critical_fail else None,
   'native_forced_miss_input_for_lab_policy':0 if critical_fail else None,
   'preserved_natural_hit_roll':p['hit_total'],'native_hit_roll_used':applied['hit_total'],
   'normal_damage_roll':p['base_damage_3d6'],
   'remaining_hp':{aid:v['resource']['hp'] for aid,v in st['actors'].items()}}
 a1._assert_alignment(st,red)
 return {'kind':'R27_SCIENCE_DECISION','action':kind,'inner':detail,'a1_events':ev,'a1_chain':red.chain,
  'policy':CRIT_FAIL_POLICY,'canonical_credit':0,'no_narrative_rolling':True}

def decision(db,rev,head,action,pval=None):
 st,h,v=checked(db)
 if (rev,head)!=(v,h):raise R27Hold('STALE_REOPEN')
 if st['phase']=='INIT' and action!='START':raise R27Hold('INIT_START_ONLY')
 if st['phase']=='ACTIVE' and action!='ATTACK':raise R27Hold('ACTIVE_ATTACK_ONLY')
 if st['phase']=='COMPLETE_LAB':raise R27Hold('TERMINAL_ACTION_FORBIDDEN')
 if action=='ATTACK' and pval!=pre(st,v+1):raise R27Hold('ATTACK_PREVIEW_CHANGED_BEFORE_INTENT')
 payload={'action':action,'preview':pval,'expected_rev':v,'head':h,'actor':st['active']}
 # Exact intention ID and expected revision, idempotency from core.event_commit
 cmd='LAB-CMD-R27-'+core.sha({'seed':st['seed'],'payload':payload,'config_sha':st['r27_science']['config_sha']})[:32]
 row=core.event_commit(db,cmd,'R27_RULE_DERIVED_SCIENCE',payload,runner)
 checked(db)
 return row

def history(db):
 st,h,rev=checked(db);e=core.history(db)
 return {'state':st,'head':h,'revision':rev,'events':e['events']}

def run(root,seed,left=None,right=None,max_rounds=MAX_ROUNDS):
 root=Path(root);root.mkdir(parents=True,exist_ok=True)
 name=('ORIGINAL_R26' if left is None else left+'__'+right)+'__SEED_'+str(seed)
 db=root/(name+'.sqlite')
 if not db.exists():create(db,seed,left,right)
 st,h,rev=checked(db)
 status=None;reason=None
 # Pre-execution no-hit impossibility can censor with mathematical proof:
 preflight=[]
 for a in st['actors']:
  t=next(x for x in st['actors'] if x!=a)
  fs=st['actors'][a]['stats'];tar=st['actors'][t]['stats'];faces=[f+fs['for']+fs['luta']>tar['ca'] for f in range(1,7)]
  preflight.append({'actor':a,'target':t,'hit_faces':[f for f,good in zip(range(1,7),faces) if good],
    'hit_probability_exact_1d6':sum(faces)/6,'target_CA':tar['ca'],'rd':5})
 if all(not x['hit_faces'] for x in preflight):
  status='CENSORED_PROVABLE_NO_HIT_POTENTIAL';reason='BOTH_SIDES_MAX_TO_HIT_NOT_GREATER_THAN_TARGET_CA'
 else:
  while True:
   st,h,rev=checked(db)
   if st['phase']=='COMPLETE_LAB':status='COMPLETE_CONDITIONAL_RULE_DERIVED';break
   if st['round']>max_rounds or rev>2*max_rounds+1:
    status='CENSORED_LIMIT';reason='MAX_ROUNDS_OR_EVENTS';break
   action='START' if st['phase']=='INIT' else 'ATTACK'
   decision(db,rev,h,action,pre(st,rev+1) if action=='ATTACK' else None)
 hist=history(db);st=hist['state'];events=[]
 for e in hist['events']:
  d=e['detail'];x=d.get('inner',{})
  if d.get('action')=='ATTACK':
   p=x['preview'];effect=x['native']['effect']
   events.append({'seq':e['seq'],'actor':p['actor'],'target':p['target'],'natural_hit_total':p['hit_total'],
     'roll_used_by_native':effect['roll_score'],'dice_hit':p['hit_dice'],
     'dice_damage':p['damage_dice'],'critical_check':p['critical_sequence'],
     'critical':p['critical_trigger'],'requested_damage':p['damage_requested'],
     'native_hit':effect['hit'],'native_raw':effect['raw'],'native_net':effect['net'],
     'native_rd':effect['rd_applied'],'before_hp':effect['before_hp'],'after_hp':effect['after_hp'],
     'native_sha':x['native']['native_trace_hash'],'event_hash':e.get('chain_hash'),
     'critical_failure_overlay':x.get('critical_failure_policy')})
 summary={'attacks':len(events),'hits':sum(v['native_hit'] for v in events),
   'raw_damage':sum(v['native_raw'] for v in events),'net_damage':sum(v['native_net'] for v in events),
   'rd_mitigation':sum(v['native_raw']-v['native_net'] for v in events),
   'nominal_RD_slots':sum(v['native_rd'] for v in events),
   'raw_dice_requested_all_attempts':sum(v['requested_damage'] for v in events),
   'hp_removed':sum(v['before_hp']-v['after_hp'] for v in events),
   'overkill':sum(v['native_net']-(v['before_hp']-v['after_hp']) for v in events),
   'critical_positive':sum(v['critical']=='POSITIVE' for v in events),
   'critical_failure':sum(v['critical']=='NEGATIVE' for v in events),
   'native_trace_count':len(events),'reactions_used':0,'positive_pa_spent':0,
   'rounds':st['round'] if status.startswith('COMPLETE') else None}
 res={'schema':'R27_SCIENCE_RUN','id':name,'seed':seed,'left':left,'right':right,'status':status,
   'censor_reason':reason,'mode':MODE,'revision':hist['revision'],'head':hist['head'],
   'initial_preflight':preflight,'winner':st['winner'],'round_reached':st['round'],
   'last_state_hp':{k:v['resource']['hp'] for k,v in st['actors'].items()},
   'a1_events':len(st['r21_control']['events']),'a1_chain':st['r21_control']['chain'],
   'config_sha':st['r27_science']['config_sha'],'sqlite_sha256':hashlib.sha256(db.read_bytes()).hexdigest(),
   'summary':summary,'events':events,'canonical_credit':0}
 return res

# Audit-only independent exact 1d6 enumeration; never classifies as combat execution.
def exact_hit_grid():
 out={}
 for p in PROFILES:
  for q in PROFILES:
   f=roster(p,q);vals=[]
   for i,j in ((0,1),(1,0)):
    scores=[x+f[i]['for']+f[i]['luta'] for x in range(1,7)]
    target=f[j]['ca'];good=sum(x>target for x in scores)
    vals.append({'attack_profile':(p,q)[i],'defender_profile':(p,q)[j],
      'score_faces':scores,'target_ca':target,'hit_faces':good,'probability_exact':good/6,
      'rd':5,'base_3d6_max':18,'base_3d6_min':3,'probability_nonzero_net_on_hit':1-10/216})
   out[p+'__'+q]=vals
 return out

def export_checkpoint(db,path):
 """Atomic SQLite snapshot, source config and full ledger; no original overwrite."""
 db=Path(db);path=Path(path)
 if path.exists():raise R27Hold('CHECKPOINT_ALREADY_EXISTS')
 path.parent.mkdir(parents=True,exist_ok=True)
 hist=history(db)
 with tempfile.TemporaryDirectory(prefix='R27-CP-',dir=path.parent) as td:
  snap=Path(td)/'snapshot.sqlite'
  c=sqlite3.connect(db);dest=sqlite3.connect(snap)
  try:c.backup(dest)
  finally:dest.close();c.close()
  verify=history(snap)
  if verify!=hist:raise R27Hold('BACKUP_LEDGER_DIVERGED')
  b=snap.read_bytes();r=core.canonical(hist).encode('utf8')
  m={'schema':'R27_PORTABLE_SCIENCE_CHECKPOINT','source_db_basename':db.name,
    'db_sha256':hashlib.sha256(b).hexdigest(),'history_sha256':hashlib.sha256(r).hexdigest(),
    'config_sha':hist['state']['r27_science']['config_sha'],
    'head':hist['head'],'revision':hist['revision'],'a1_chain':hist['state']['r21_control']['chain'],
    'no_canonical_credit':True}
  with zipfile.ZipFile(path,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
   z.writestr('manifest.json',core.canonical(m));z.writestr('snapshot.sqlite',b);z.writestr('history.json',r)
 return verify_checkpoint(path)

def verify_checkpoint(path,restore_to=None):
 path=Path(path)
 with zipfile.ZipFile(path) as z:
  if sorted(z.namelist())!=['history.json','manifest.json','snapshot.sqlite'] or z.testzip():
   raise R27Hold('CORRUPT_CHECKPOINT_ZIP')
  m=json.loads(z.read('manifest.json')); b=z.read('snapshot.sqlite');rb=z.read('history.json')
 if m['schema']!='R27_PORTABLE_SCIENCE_CHECKPOINT':raise R27Hold('CHECKPOINT_INVALID_SCHEMA')
 if hashlib.sha256(b).hexdigest()!=m['db_sha256'] or hashlib.sha256(rb).hexdigest()!=m['history_sha256']:
  raise R27Hold('CHECKPOINT_SHA_MISMATCH')
 with tempfile.TemporaryDirectory(dir=path.parent) as td:
  tmp=Path(td)/'snapshot.sqlite';tmp.write_bytes(b)
  hist=history(tmp)
  if core.canonical(hist).encode()!=rb or (hist['revision'],hist['head'],hist['state']['r21_control']['chain'],hist['state']['r27_science']['config_sha'])!= (m['revision'],m['head'],m['a1_chain'],m['config_sha']):
   raise R27Hold('CHECKPOINT_READBACK_MISMATCH')
 if restore_to is not None:
  restore_to=Path(restore_to)
  if restore_to.exists():raise R27Hold('RESTORE_OVERWRITE_FORBIDDEN')
  with open(restore_to,'xb') as f:
   f.write(b);f.flush();os.fsync(f.fileno())
  if history(restore_to)!=hist:raise R27Hold('RESTORE_FAILED_INTEGRITY')
 return {'status':'PASS','sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
  'revision':m['revision'],'head':m['head'],'source_db_sha256':m['db_sha256']}
