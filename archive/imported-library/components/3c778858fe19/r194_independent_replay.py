"""R194 independent-of-producer semantic auditor, no import of R193 producer.
Does not constitute external human audit or canonical certification.
"""
import json,sqlite3,hashlib,random,pathlib,re,sys,collections
ROOT=pathlib.Path(__file__).resolve().parents[1]
VER='R187-R196-MATERIALIZED-BEAST-LIU-CONCHA-V1'
PRE_SHA=hashlib.sha256((ROOT/'R193_PRE_REGISTRATION.json').read_bytes()).hexdigest()
FIXED={
'LIU':{'hp':235,'pa':73,'ca':46,'rd':10,'attack_bonus':37,'damage_groups':((5,12),(3,8),(1,6)),'flat':45,'page':'https://app.notion.com/p/0b4c2b324ede837cb6be818dc8e36010','tag':'impacto'},
'CONCHA':{'hp':210,'pa':70,'ca':40,'rd':15,'attack_bonus':30,'damage_groups':((3,6),),'flat':30,'page':'https://app.notion.com/p/474c2b324ede82d08ea6819069c17043','tag':'perfurante'}}
def canonical(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def sha(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def rolls(seed,who,turn,label,n,faces):
 s=f'{VER}|{seed}|{who}|{turn}|{label}|{n}d{faces}'
 r=random.Random(int.from_bytes(hashlib.sha256(s.encode()).digest(),'big'))
 return [r.randint(1,faces) for _ in range(n)]
def fail(kind,**extra):raise AssertionError((kind,extra))
def verify(db):
 db=pathlib.Path(db);m=re.fullmatch(r'R193_LIU_CONCHA_SEED(\d+)_LI([02])_BI([08])_BL([08])\.sqlite',db.name)
 if not m:fail('DB_FILENAME_INVALID',db=db.name)
 seed,liu_i,con_i,con_l=map(int,m.groups());b={'liu_named_init':liu_i,'concha_named_init':con_i,'concha_named_luta':con_l}
 c=sqlite3.connect(f'file:{db}?mode=ro',uri=True)
 try:
  meta=dict(c.execute('SELECT key,value FROM meta'))
  pending=list(c.execute('SELECT * FROM pending'))
  if pending:fail('PENDING_EFFECTS',pending=pending)
  rows=list(c.execute('SELECT seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha FROM events ORDER BY seq'))
  state=json.loads(meta['state'])
 finally:c.close()
 if state['pre_reg_sha']!=PRE_SHA or state['branch']!=b or state['seed']!=seed or not state['synthetic'] or state['scene']!='A':fail('SOURCE_PRE_REG_OR_STATE_INVALID')
 geo=state['geometry']
 if not (geo['scene_test_only'] and geo['contact'] and geo['same_layer'] and geo['line_of_effect'] and not geo['motion'] and geo['numeric_reach'] is None):fail('GEOMETRY_UNAUTHORIZED')
 hp={who:FIXED[who]['hp'] for who in FIXED};pa={who:FIXED[who]['pa'] for who in FIXED};init={};attack_turn={'LIU':0,'CONCHA':0};native=[];prev=hashlib.sha256(f'{seed}|A|GENESIS'.encode()).hexdigest() # actual genesis checked by structural prev chain below
 first=None;order=None;current=None;round_num=1;metrics={'attempts':0,'hits':0,'brut':0,'post_rd':0,'hp_loss':0,'overkill':0,'critical_pos':0,'critical_neg':0}
 for idx,(seq,cmd,link,rowj,rowsha,bsha,asha) in enumerate(rows):
  x=json.loads(rowj)
  if seq!=idx+1 or x['seq']!=seq or x['cmd_id']!=cmd or x['prev']!=link or x['before_sha']!=bsha or x['after_sha']!=asha or sha(x)!=rowsha:fail('ROW_CHAIN_TAMPER',seq=seq)
  if first is not None and (link!=prev or bsha!=previous_state_sha):fail('ROW_CHAIN_BROKEN',seq=seq)
  if x['synthetic'] is not True or x['official_effects']!=0:fail('OFFICIAL_CREDIT_OR_FLAG',seq=seq)
  p=x['payload'];d=x['detail'];fresh=d['new_native_events']
  if idx==0:
   if x['kind']!='INIT_AND_SOURCE_SCOPE_START' or d['kind']!=x['kind'] or p['pre_reg_sha']!=PRE_SHA or p['geometry']!=geo:fail('BAD_OPENING')
   ld=rolls(seed,'LIU',0,'INIT',2,6);bd=rolls(seed,'CONCHA',0,'INIT',2,6)
   lv=sum(ld)+16+4+liu_i;bv=sum(bd)+27+con_i
   if lv==bv:fail('TIE_UNRESOLVED')
   init={'LIU':{'dice':ld,'score':lv,'initiative_special':4,'named_prof_hypothesis':liu_i},'CONCHA':{'dice':bd,'score':bv,'named_prof_hypothesis':con_i},'tie':False,'order':['LIU','CONCHA'] if lv>bv else ['CONCHA','LIU']}
   if d['initiative']!=init or p['initiative']!=init:fail('INIT_REWRITTEN')
   order=init['order'];current=order[0]
   if len(fresh)!=1 or fresh[0]['action']!='turn_start' or fresh[0]['by']!=current:fail('START_EVENT_MISSING')
  else:
   if x['kind']!='PHYSICAL_NORMAL_ATTACK' or d['kind']!='PHYSICAL_NORMAL_ATTACK_WITH_HYPOTHESIS_SKILL':fail('WRONG_ACTION_KIND',seq=seq)
   actor=d['actor'];target=d['target'];a=FIXED[actor];t=FIXED[target]
   if actor!=current or target==actor or target not in FIXED or d['branch']!=b or p['branch']!=b or d['source_page']!=a['page'] or d['target_page']!=t['page']:fail('ACTOR_IDENTITY_OR_TURN_DRIFT',seq=seq)
   attack_turn[actor]+=1;tn=attack_turn[actor];ifweak=hp[actor]*10<a['hp']
   if d['actor_turn']!=tn or p['turn_number']!=tn or p['actor']!=actor or p['target']!=target:fail('TURN_NUMBER_DRIFT',seq=seq)
   expected={'crit':rolls(seed,actor,tn,'CRIT',3,6),'hit':rolls(seed,actor,tn,'HIT',2,6),'hit_weak':rolls(seed,actor,tn,'WEAK',2,6),'damage':[rolls(seed,actor,tn,'DAMAGE'+str(i),n,f) for i,(n,f) in enumerate(a['damage_groups'])]}
   if p['tape']!=expected or d['tape']!=expected:fail('RNG_TAPE_TAMPER',seq=seq)
   ev=d['attack'];hitrolls=[expected['hit'],expected['hit_weak']] if ifweak else [expected['hit']]
   bonus=a['attack_bonus']+(con_l if actor=='CONCHA' else 0)
   score=(min(map(sum,hitrolls))+bonus-2) if ifweak else sum(expected['hit'])+bonus
   crit='POSITIVE' if expected['crit'][:2]==[6,6] and expected['crit'][2]>=5 else 'NEGATIVE' if expected['crit'][:2]==[1,1] and expected['crit'][2]<=2 else 'NONE'
   is_hit=(score>t['ca'] or crit=='POSITIVE') and crit!='NEGATIVE'
   rawbase=sum(map(sum,expected['damage']))+a['flat']
   raw=(rawbase+sum(n*f for n,f in a['damage_groups']) if crit=='POSITIVE' else rawbase) if is_hit else 0
   post=max(0,raw-t['rd']) if is_hit else 0
   los=min(hp[target],post);over=max(0,post-hp[target]);newhp=hp[target]-los
   for field,value in {'action':'weapon_attack','from':actor,'to':target,'roll_score':score,'ca_exact':str(t['ca']),'critical':crit,'hit':is_hit,'raw':raw,'net':post,'rd_applied':t['rd'] if is_hit else 0,'before_hp':hp[target],'after_hp':newhp,'hp_loss_actual':los,'overkill':over,'normal_damage':rawbase,'attack_origin':'NORMAL','type':a['tag']}.items():
    if ev[field]!=value:fail('SEMANTIC_ATTACK_TAMPER',seq=seq,field=field,expected=value,actual=ev.get(field))
   if ev['critical_sequence']!=expected['crit'] or ev['attack_roll_attempts']!=hitrolls or ev['damage_roll_groups']!=expected['damage']:fail('ATTACK_EVIDENCE_TAMPER',seq=seq)
   hp[target]=newhp
   for key,v in {'attempts':1,'hits':int(is_hit),'brut':raw,'post_rd':post,'hp_loss':los,'overkill':over,'critical_pos':int(crit=='POSITIVE'),'critical_neg':int(crit=='NEGATIVE')}.items():metrics[key]+=v
   if d['hp_after']!=hp or d['pa_after']!=pa or fresh[0]!=ev:fail('STATE_RECEIPT_MISMATCH',seq=seq)
   if newhp==0:
    if d['nextturn']!={'ko':target,'next_turn':None} or len(fresh)!=2:fail('KO_SEQUENCE_MISMATCH',seq=seq)
    current=None
   else:
    if len(fresh)!=3 or fresh[1]['action']!='turn_end' or fresh[1]['by']!=actor or fresh[2]['action']!='turn_start' or fresh[2]['by']!=target or d['nextturn']['next_turn']!=target:fail('TURN_RENEWAL_MISMATCH',seq=seq)
    if order.index(actor)==len(order)-1:round_num+=1
    current=target
  for evx in fresh:
   if evx['seq']!=len(native)+1 or evx['provenance']!='R187-R196-SOURCE-EXPLICIT-LIU-CONCHA-TEST':fail('EVENT_ORDER_PROVENANCE',seq=seq)
   native.append(evx)
  first=True;prev=rowsha;previous_state_sha=asha
 if state['phase']!='FINISHED' or current is not None or state['winner'] not in FIXED or state['actors']['LIU']['resource']['hp']!=hp['LIU'] or state['actors']['CONCHA']['resource']['hp']!=hp['CONCHA']:fail('FINAL_STATE_DIVERGENCE')
 if state['metrics']!=metrics or state['native_events']!=native or state['round']!=round_num or int(meta['revision'])!=len(rows) or meta['head']!=prev or sha(state)!=rows[-1][6]:fail('CHECKPOINT_OR_RESOURCE_DIVERGENCE')
 check=json.loads((db.parent/(db.name+'.checkpoint.json')).read_text())
 if sha(check['body'])!=check['sha256'] or check['body']['db']!=db.name:fail('CHECKPOINT_HASH')
 return {'db':db.name,'sha256':hashlib.sha256(db.read_bytes()).hexdigest(),'seed':seed,'branch':b,'winner':state['winner'],'hp_final':hp,'rounds':round_num,'commits':len(rows),'native_events':len(native),'attacks':metrics['attempts'],'head':prev,'integrity':'PASS_SEMANTIC_SOURCE_CONDITIONAL'}
if __name__=='__main__':
 paths=sorted((ROOT/'evidence').glob('R193_LIU_CONCHA_*.sqlite'));out=[]
 for p in paths:
  try:out.append(verify(p))
  except Exception as e:print('FAIL',p.name,repr(e));raise
 result={'status':'PASS_R194_INDEPENDENT_LOCAL_SEMANTIC_AUDIT','audited':len(out),'commits':sum(x['commits']for x in out),'native_events':sum(x['native_events']for x in out),'attack_receipts':sum(x['attacks']for x in out),'records':out,'external_human_audit':False,'terminal_certified':0,'official_benchmarks':0}
 (ROOT/'evidence/R194_AUDIT_REPORT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
 print(json.dumps({k:v for k,v in result.items() if k!='records'},ensure_ascii=False,indent=2))
