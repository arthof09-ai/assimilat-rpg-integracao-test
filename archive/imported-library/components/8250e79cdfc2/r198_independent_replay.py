"""R198 independent-code local audit of frozen R18 SQLite; never invoke combat producer or effects.
Recomputes seeded roll tapes, crit, hit, general RD, HP, KO, turns, final state and hash chain.
This is NOT external certification, and its plain-Python arithmetic is verification, not another damage motor.
"""
from __future__ import annotations
import json,hashlib,random,pathlib,sqlite3,collections,re,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
PRE_PATH=ROOT/'source/R198_PRE_REG.json'
PREG=json.loads(PRE_PATH.read_text());PRE_HASH=hashlib.sha256(PRE_PATH.read_bytes()).hexdigest()
SRC_PATH=ROOT.parent/'work/r197/source/R197_SOURCE_SNAPSHOTS.json'
SRC=json.loads(SRC_PATH.read_text());SRC_HASH=hashlib.sha256(SRC_PATH.read_bytes()).hexdigest()
EXTRA=json.loads((ROOT/'source/R198_ACTOR_EXTENSION.json').read_text())['actors']
VER='R198-R18-SOURCE-SCOPED-MICROBENCH-1'
REFERENCE={}
for a in SRC['actors']:
 if a['id'] not in ('LOBO_P1','CABRA_P1','LIU_P5'):continue
 att=a['attack'];ed=a['id']=='LIU_P5'
 REFERENCE[a['id']]={'hp':a['hp'],'max_hp':a['hp'],'pa':a['pa'],'ca':a['ca'],'dex':a['stats']['DES'],
 'init_bonus':a['stats']['DES']+(4 if ed else 0),'hit_bonus':att['hit_flat_source'] if ed else a['stats'][att['hit_stat']],
 'attack_dice':list(att['hit_test_dice']),'damage_dice':list(att['damage_dice']),'fixed':att['damage_flat'],
 'tag':'cortante' if a['id']=='CABRA_P1' else 'impacto','rd':10 if ed else 15,'url':a['url'],'name':a['name']}
for a in EXTRA:
 REFERENCE[a['id']]={'hp':a['hp'],'max_hp':a['maximum_hp'],'pa':a['pa'],'ca':a['ca'],'dex':a['dex'],
 'init_bonus':a['initiative_bonus'],'hit_bonus':a['attack_bonus'],'attack_dice':a['attack_dice'],
 'damage_dice':a['damage_dice'],'fixed':a['damage_flat'],'tag':a['damage_tag'],'rd':a['rd'],
 'url':a['url'],'name':a['name']}

def canonical(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def sha(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def fail(key,**kw):raise AssertionError(f'{key} '+str(kw))
def dice(seed,pair,actor,nturn,label,n,faces):
 s=f'{VER}|{seed}|{pair[0]}-{pair[1]}|{actor}|{nturn}|{label}|{n}d{faces}'
 return [random.Random(int.from_bytes(hashlib.sha256(s.encode()).digest(),'big')).randint(1,faces)] if False else _dice(s,n,faces)
def _dice(s,n,faces):
 r=random.Random(int.from_bytes(hashlib.sha256(s.encode()).digest(),'big'))
 return [r.randint(1,faces) for _ in range(n)]
def chk(record,key,expected,ctx):
 if record.get(key)!=expected:fail('SEMANTIC_INTEGRITY',where=ctx,field=key,want=expected,got=record.get(key))

def audit(db,checkpoint=True):
 db=pathlib.Path(db)
 m=re.fullmatch(r'R198_(CAPANGA_P3|LIU_P5)_VS_(LOBO_P1|CABRA_P1)_(\d+)\.sqlite',db.name)
 if not m:fail('UNEXPECTED_RUN_ID',db=db.name)
 aa,bb,ss=m.groups();pair=(aa,bb);seed=int(ss)
 c=sqlite3.connect(f'file:{db}?mode=ro',uri=True)
 try:
  meta=dict(c.execute('SELECT key,value FROM meta'))
  pending=c.execute('SELECT count(*) FROM pending').fetchone()[0]
  rows=list(c.execute('SELECT seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha FROM events ORDER BY seq'))
  st=json.loads(meta['state'])
 finally:c.close()
 if pending:fail('UNRESOLVED_INTENT')
 if (seed not in sum(PREG['seeds'].values(),[]) or list(pair) not in PREG['pairs'] or st.get('pre_reg_sha')!=PRE_HASH or st.get('source_snap_sha')!=SRC_HASH or st.get('seed')!=seed or st.get('pair')!=list(pair)):fail('SCENE_SOURCE_PRE_REG_DRIFT')
 if st.get('version_description')!=VER or st.get('synthetic') is not True or st.get('scene')!='A' or st['position']!={'contact':True,'same_layer':True,'line_of_effect':True,'movement':False,'campaign_location':False}:fail('INVALID_SCENE_SCOPE')
 if st['initial_hypotheses']!=PREG['assumptions']:fail('UNCERTAINTY_ERASED')
 if st.get('winner') not in pair and st['phase']=='FINISHED':fail('WINNER_UNKNOWN')
 hp={x:REFERENCE[x]['hp'] for x in pair};pa={x:REFERENCE[x]['pa'] for x in pair}
 native=[];metrics={'attempts':0,'hits':0,'crit_positive':0,'crit_negative':0,'damage_gross':0,'post_rd':0,'hp_loss':0,'overkill':0,'pa_spent':0}
 actor_turns={x:0 for x in pair};roundno=1;prevhead=meta['genesis'];prevafter=None;active=None;order=None;ko=None;init_payload=None
 for index,(seq,cmd,prev,rowj,rowsha,before_sha,after_sha) in enumerate(rows):
  x=json.loads(rowj);ctx=f'{db.name}:{seq}';expected_seq=index+1
  if seq!=expected_seq or x['seq']!=seq or x['cmd_id']!=cmd or x['prev']!=prev or sha(x)!=rowsha or prevhead!=prev or x['before_sha']!=before_sha or x['after_sha']!=after_sha or (prevafter is not None and prevafter!=before_sha):fail('STRUCTURE_CHAIN',ctx=ctx)
  if x.get('official_effects')!=0 or x.get('synthetic') is not True:fail('IMPROPER_CANON_STATUS',ctx=ctx)
  detail=x['detail'];payload=x['payload'];fresh=detail['new_native_events'] if seq==1 else detail['events_added']
  if seq==1:
   if x['kind']!='SOURCE_INIT_AND_POSITION' or detail['kind']!='INIT_START' or payload['pre_reg_sha']!=PRE_HASH or payload['source_snap_sha']!=SRC_HASH:fail('INIT_SCOPE',ctx=ctx)
   vals={}
   for who in pair:
    z=REFERENCE[who];t=dice(seed,pair,who,0,'INIT',2,6)
    vals[who]={'roll':t,'bonus':z['init_bonus'],'result':sum(t)+z['init_bonus'],
      'named_prof_status':'SOURCE_INSTINTO_SELVAGEM_PLUS4' if who=='LIU_P5' else 'LAB_HYPOTHESIS_UNTRAINED'}
   order=sorted(pair,key=lambda k: vals[k]['result'],reverse=True)
   if vals[order[0]]['result']==vals[order[1]]['result']:fail('TIE_COMMITTED')
   if payload['order']!=order or payload['initiative']!=vals or detail['results']!=vals or detail['order']!=order:fail('INIT_FALSIFIED')
   active=order[0];init_payload=vals
   if len(fresh)!=1 or fresh[0]['action']!='turn_start' or fresh[0]['by']!=active:fail('INIT_TURN_START_MISSING')
  else:
   if x['kind']!='SOURCE_BASIC_NORMAL_ATTACK' or detail['kind']!='SOURCE_SCOPED_BASIC_ATTACK':fail('ACTION_NOT_SUPPORTED',ctx=ctx)
   who=detail['from'];target=detail['to']
   if who!=active or who not in pair or target not in pair or who==target or detail['source_page']!=REFERENCE[who]['url'] or detail['target_page']!=REFERENCE[target]['url']:fail('ACTOR_PROVENANCE',ctx=ctx)
   actor_turns[who]+=1;nturn=actor_turns[who];a=REFERENCE[who];t=REFERENCE[target]
   if payload['actor']!=who or payload['target']!=target or payload['own_turn']!=nturn or detail['own_turn']!=nturn:fail('ACTOR_OWN_TURN',ctx=ctx)
   weak=hp[who]>0 and 10*hp[who]<a['max_hp']
   cr=dice(seed,pair,who,nturn,'CRIT',3,6)
   hits=[dice(seed,pair,who,nturn,'HIT'+str(i),*a['attack_dice']) for i in range(2 if weak else 1)]
   dams=[dice(seed,pair,who,nturn,'DMG'+str(i),n,faces) for i,(n,faces) in enumerate(a['damage_dice'])]
   tape={'crit':cr,'hit':hits,'damage':dams}
   if payload['roll_tape']!=tape or detail['tape']!=tape:fail('RNG_OR_TAPE_TAMPER',ctx=ctx)
   score=(min(map(sum,hits))+a['hit_bonus']-2) if weak else sum(hits[0])+a['hit_bonus']
   crit=('POSITIVE' if cr[:2]==[6,6] and cr[2]>=5 else 'NEGATIVE' if cr[:2]==[1,1] and cr[2]<=2 else 'NONE')
   hit=(score>t['ca'] or crit=='POSITIVE') and crit!='NEGATIVE'
   raw_base=sum(map(sum,dams))+a['fixed'];base_with_crit=raw_base+(sum(n*faces for n,faces in a['damage_dice']) if crit=='POSITIVE' else 0)
   raw=base_with_crit if hit else 0;net=max(0,raw-t['rd']) if hit else 0
   loss=min(hp[target],net);over=max(0,net-hp[target]);after=hp[target]-loss
   ev=detail['attack']
   for k,v in {'action':'weapon_attack','from':who,'to':target,'roll_score':score,'ca_exact':str(t['ca']),'critical':crit,'hit':hit,'raw':raw,'net':net,'rd_applied':t['rd'] if hit else 0,'before_hp':hp[target],'after_hp':after,'hp_loss_actual':loss,'overkill':over,'normal_damage':raw_base,'attack_origin':'NORMAL','type':a['tag'],'weak_attacker':weak,'critical_max_bonus':sum(n*faces for n,faces in a['damage_dice']) if crit=='POSITIVE' else 0}.items():chk(ev,k,v,ctx)
   if ev['damage_roll_groups']!=dams or ev['critical_sequence']!=cr or ev['attack_roll_attempts']!=hits:fail('CRITICAL_OR_DICE_EVIDENCE',ctx=ctx)
   hp[target]=after
   for k,v in {'attempts':1,'hits':int(hit),'crit_positive':int(crit=='POSITIVE'),'crit_negative':int(crit=='NEGATIVE'),'damage_gross':raw,'post_rd':net,'hp_loss':loss,'overkill':over}.items():metrics[k]+=v
   if detail['resources']!={k:{'hp':hp[k],'pa':pa[k],'reaction':st['actors'][k]['resource']['reaction'],'standard':detail['resources'][k]['standard']} for k in pair}:fail('RESOURCE_CHANGE_OUTSIDE_LEDGER',ctx=ctx)
   if fresh[0]!=ev:fail('FIRST_NATIVE_NOT_ATTACK',ctx=ctx)
   if after==0:
    if len(fresh)!=2 or fresh[1]['action']!='turn_end' or fresh[1]['by']!=who or detail['next_turn']!={'ko':target}:fail('KO_EVENT_SEQUENCE',ctx=ctx)
    ko=target;active=None
    if seq!=len(rows):fail('POST_KO_ACTION',ctx=ctx)
   else:
    if len(fresh)!=3 or fresh[1]['action']!='turn_end' or fresh[1]['by']!=who or fresh[2]['action']!='turn_start' or fresh[2]['by']!=target or detail['next_turn']['next_turn']!=target:fail('TURN_CAUSALITY',ctx=ctx)
    if who==order[-1]:roundno+=1
    active=target
  for evn in fresh:
   if evn['seq']!=len(native)+1 or evn['provenance']!=VER+'-EXP-NOT-CAMPAIGN':fail('NATIVE_EVENT_ORDER_ORIGIN',ctx=ctx)
   native.append(evn)
  prevhead=rowsha;prevafter=after_sha
 if st['phase']!='FINISHED' and len(rows)-1<PREG['scene']['maximum_attacks']:fail('PREMATURE_CENSOR')
 if st['phase']=='FINISHED' and (ko is None or st['winner'] not in pair or st['winner']==ko):fail('FALSE_WINNER')
 if st['metrics']!=metrics or st['native_events']!=native or len(st['history'])!=metrics['attempts'] or st['round']!=roundno or meta['head']!=prevhead or int(meta['revision'])!=len(rows) or prevafter!=sha(st):fail('SUMMARY_OR_CHECKPOINT_DRIFT')
 for who in pair:
  if st['actors'][who]['resource']['hp']!=hp[who] or st['actors'][who]['resource']['pa']!=pa[who]:fail('RESOURCE_FINAL_TAMPER')
 if checkpoint:
  chkfile=db.with_name(db.name+'.checkpoint.json')
  check=json.loads(chkfile.read_text())
  if sha(check['body'])!=check['sha256'] or check['body']['db']!=db.name:fail('CHECKPOINT_TAMPER')
 return {'db':db.name,'seed':seed,'pair':list(pair),'rounds':roundno,'winner':st['winner'],'attacks':metrics['attempts'],'commits':len(rows),'native_events':len(native),'metrics':metrics,'hp_final':hp,'pa_final':pa,'sha256':hashlib.sha256(db.read_bytes()).hexdigest(),'head':prevhead,'result':'PASS_SOURCE_SCOPED_SEMANTIC'}

def batch(directory=None):
 folder=pathlib.Path(directory or ROOT/'evidence/db');out=[]
 for db in sorted(folder.glob('R198_*.sqlite')):out.append(audit(db))
 result={'status':'PASS_R198_CODE_SEPARATE_SEMANTIC_AUDIT','run_count':len(out),'attacks':sum(y['attacks'] for y in out),'commits':sum(y['commits'] for y in out),'native_events':sum(y['native_events'] for y in out),'records':out,'external_human_audit':False,'official_certifications':0}
 (ROOT/'evidence/R198_AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
 print(json.dumps({k:v for k,v in result.items() if k!='records'},ensure_ascii=False))
 return result
if __name__=='__main__':batch()
