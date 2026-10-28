"""Code-separated local magic PA & HP auditor over original R18 SQLite, no combat producer/effects call."""
import json,hashlib,sqlite3,random, pathlib,re,sys,collections
ROOT=pathlib.Path(__file__).resolve().parents[1]
MAG=json.loads((ROOT/'source/R198_MAGIC_PRE_REG.json').read_text());MAG_SHA=hashlib.sha256((ROOT/'source/R198_MAGIC_PRE_REG.json').read_bytes()).hexdigest()
PRE_SHA=hashlib.sha256((ROOT/'source/R198_PRE_REG.json').read_bytes()).hexdigest()
ONG=json.loads((ROOT/'source/R198_ONG_SOURCE.json').read_text())
VER='R198-R18-SOURCE-SCOPED-MICROBENCH-1'; PA_COST=8
Lobo={'hp':240,'pa':180,'ca':34,'rd':15,'attack_bonus':24,'attack_dice':(2,6),'damage_dice':((1,6),),'flat':24,'tag':'impacto'}
Ong={'hp':99,'pa':91,'ca':30,'rd':0,'attack_bonus':19,'attack_dice':(4,6),'damage_dice':((8,6),),'flat':28,'tag':'agua'}
ACT={'LOBO_P1':Lobo,'ONG_P2':Ong}
def fail(msg,**kw):raise AssertionError((msg,kw))
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def sha(x):return hashlib.sha256(canon(x).encode()).hexdigest()
def dice(seed,who,own_turn,label,n,faces):
 s=f'{VER}|{seed}|ONG_P2-LOBO_P1|{who}|{own_turn}|{label}|{n}d{faces}'
 r=random.Random(int.from_bytes(hashlib.sha256(s.encode()).digest(),'big'))
 return [r.randint(1,faces) for _ in range(n)]
def audit(db):
 path=pathlib.Path(db);m=re.fullmatch(r'R198_MAGIC_ONG_VS_LOBO_(\d+)_(CAST_WHIP|DECLINE_WHIP)\.sqlite',path.name)
 if not m:fail('BAD_ID')
 seed=int(m.group(1));policy=m.group(2)
 if seed not in MAG['seeds'] or policy not in MAG['policies']:fail('UNREGISTERED_RUN')
 conn=sqlite3.connect(f'file:{path}?mode=ro',uri=True)
 try:
  meta=dict(conn.execute('SELECT key,value FROM meta'))
  rows=list(conn.execute('SELECT seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha FROM events ORDER BY seq'))
  pend=conn.execute('SELECT count(*) FROM pending').fetchone()[0]
 finally:conn.close()
 st=json.loads(meta['state'])
 if pend or st['magic_pre_reg_sha']!=MAG_SHA or st['magic_policy']!=policy or st['pre_reg_sha']!=PRE_SHA or st['seed']!=seed or st['pair']!=['ONG_P2','LOBO_P1']:fail('SOURCE_STATE_DRIFT')
 hp={k:v['hp'] for k,v in ACT.items()};pa={k:v['pa'] for k,v in ACT.items()};nturn=collections.Counter();numcasts=0;gross=0;lost=0;attacks=0;native=[]
 order=sorted(ACT,key=lambda a:sum(dice(seed,a,0,'INIT',2,6))+ (15 if a=='ONG_P2' else 20),reverse=True)
 if sum(dice(seed,order[0],0,'INIT',2,6))+ (15 if order[0]=='ONG_P2' else 20)==sum(dice(seed,order[1],0,'INIT',2,6))+(15 if order[1]=='ONG_P2' else 20):fail('TIE_COMMITTED')
 active=None;head=meta['genesis'];prev_after=None;roundno=1
 for index,(seq,cmd,prev,rowj,rowsha,bsha,asha) in enumerate(rows):
  x=json.loads(rowj);ctx=seq
  if seq!=index+1 or x['seq']!=seq or x['prev']!=prev or prev!=head or x['before_sha']!=bsha or x['after_sha']!=asha or x['cmd_id']!=cmd or sha(x)!=rowsha or (prev_after and bsha!=prev_after):fail('HASH_LEDGER',seq=seq)
  if x.get('synthetic') is not True or x.get('official_effects')!=0:fail('OFFICIAL_STATUS_DRIFT')
  d=x['detail'];p=x['payload']
  if seq==1:
   if x['kind']!='SPELL_SCENE_INIT' or p['magic_policy']!=policy or d['order']!=order:fail('INIT_DRIFT')
   active=order[0]
   fresh=d['new_native_events'];
   if len(fresh)!=1 or fresh[0]['action']!='turn_start' or fresh[0]['by']!=active:fail('INIT_EVENT')
  else:
   actor=active;nturn[actor]+=1;turn=nturn[actor];other='LOBO_P1' if actor=='ONG_P2' else 'ONG_P2'
   if actor=='ONG_P2' and (policy=='DECLINE_WHIP' or pa[actor]<PA_COST):
    if x['kind']!='SOURCE_SPELL_DECLINE' or d['kind']!='PASS_SPELL' or p['who']!=actor or d['pa_after']!=pa[actor]:fail('PASS_SEMANTICS',seq=seq)
    fresh=d['new_native_events'];
    if len(fresh)!=3 or fresh[0]['action']!='spell_declined' or fresh[0]['by']!=actor or fresh[0]['PA_spent']!=0:fail('PASS_EVENT')
   else:
    shouldmagic=actor=='ONG_P2'
    if x['kind']!=('SOURCE_SPELL_WHIP_WITH_PA' if shouldmagic else 'SOURCE_BASIC_NORMAL_ATTACK'):fail('ATTACK_KIND',seq=seq)
    f=ACT[actor];t=ACT[other];weak=10*hp[actor]<f['hp']
    roll={'crit':dice(seed,actor,turn,'CRIT',3,6),
     'hit':[dice(seed,actor,turn,'HIT'+str(i),*f['attack_dice']) for i in range(2 if weak else 1)],
     'damage':[dice(seed,actor,turn,'DMG'+str(i),n,faces) for i,(n,faces) in enumerate(f['damage_dice'])]}
    if p['roll_tape']!=roll or d['tape']!=roll:fail('ROLL_TAPE',seq=seq)
    score=(min(map(sum,roll['hit']))+f['attack_bonus']-2) if weak else sum(roll['hit'][0])+f['attack_bonus']
    crit=('POSITIVE' if roll['crit'][:2]==[6,6] and roll['crit'][2]>=5 else 'NEGATIVE' if roll['crit'][:2]==[1,1] and roll['crit'][2]<=2 else 'NONE')
    hit=(score>t['ca'] or crit=='POSITIVE') and crit!='NEGATIVE'
    nominal=sum(map(sum,roll['damage']))+f['flat']
    amount=(nominal+(sum(n*faces for n,faces in f['damage_dice']) if crit=='POSITIVE' else 0)) if hit else 0
    net=max(0,amount-t['rd']) if hit else 0
    hp_before=hp[other];change=min(net,hp_before);hp[other]-=change
    ev=d['attack']
    for k,v in {'from':actor,'to':other,'roll_score':score,'ca_exact':str(t['ca']),'critical':crit,'hit':hit,'raw':amount,'net':net,'rd_applied':t['rd'] if hit else 0,'hp_loss_actual':change,'before_hp':hp_before,'after_hp':hp[other],'type':f['tag'],'normal_damage':nominal}.items():
     if ev[k]!=v:fail('MATH_TAMPER',seq=seq,field=k,want=v,got=ev[k])
    if ev['damage_roll_groups']!=roll['damage'] or ev['critical_sequence']!=roll['crit'] or ev['attack_roll_attempts']!=roll['hit']:fail('TAPE_EVENT_TAMPER')
    gross+=amount;lost+=change;attacks+=1
    fresh=d['new_native_events'] if shouldmagic else d['events_added']
    if fresh[0]!=ev:fail('NATIVE_ATTACK_MISMATCH')
    if shouldmagic:
     if pa[actor]<8:fail('INSUFFICIENT_PA_CAST')
     paid=d['PA_debit_event'];before=pa[actor];pa[actor]-=8;numcasts+=1
     for k,v in {'action':'spell_pa_cost','by':actor,'PA_spent':8,'PA_before':before,'PA_after':pa[actor],'attack_event_seq':ev['seq'],'source':ONG['url']}.items():
      if paid[k]!=v:fail('PA_SEMANTICS',seq=seq,field=k)
     if fresh[1]!=paid:fail('PA_EVENT_MISSING')
     if d['hp_after']!=hp or d['pa_after']!=pa:fail('RESOURCE_DIVERGENCE',seq=seq)
    else:
     if d['resources'][actor]['pa']!=pa[actor] or d['resources'][other]['pa']!=pa[other]:fail('BASIC_PA_CHANGED')
   if hp[other]==0:
    if len(fresh)!=(3 if actor=='ONG_P2' and x['kind']=='SOURCE_SPELL_WHIP_WITH_PA' else 2):fail('KO_EVENTS')
    active=None
    if seq!=len(rows):fail('ATTACK_AFTER_KO')
   else:
    if fresh[-1]['action']!='turn_start' or fresh[-1]['by']!=other or fresh[-2]['action']!='turn_end' or fresh[-2]['by']!=actor:fail('TURN_CAUSALITY')
    if actor==order[-1]:roundno+=1
    active=other
  for event in fresh:
   if event['seq']!=len(native)+1 or event['provenance']!=VER+'-EXP-NOT-CAMPAIGN':fail('NATIVE_EVENT_ORIGIN')
   native.append(event)
  head=rowsha;prev_after=asha
 if st['phase']!='FINISHED' or active is not None or st['metrics']['pa_spent']!=numcasts*8 or st['metrics']['attempts']!=attacks or st['native_events']!=native or st['round']!=roundno or sha(st)!=prev_after or head!=meta['head']:fail('FINAL_STATE')
 if st['metrics']['damage_gross']!=gross or st['metrics']['hp_loss']!=lost:fail('DAMAGE_TOTAL')
 for who in ACT:
  if st['actors'][who]['resource']['hp']!=hp[who] or st['actors'][who]['resource']['pa']!=pa[who]:fail('HP_PA_FINAL',actor=who)
 check=json.loads((path.parent/(path.name+'.checkpoint.json')).read_text())
 if sha(check['body'])!=check['sha256']:fail('CHECKPOINT_BAD')
 return {'db':path.name,'seed':seed,'policy':policy,'winner':st['winner'],'rounds':roundno,'commits':len(rows),'events':len(native),'attack_attempts':attacks,'casts':numcasts,'pa_spent':8*numcasts,'magic_hp_removed':99-hp['ONG_P2'] if policy=='DECLINE_WHIP' else 240-hp['LOBO_P1'],'hp_final':hp,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
def batch():
 results=[audit(p) for p in sorted((ROOT/'evidence/magic_db').glob('R198_MAGIC*.sqlite'))]
 rep={'status':'PASS_R198_MAGIC_CODE_SEPARATE_AUDIT','runs':len(results),'casts':sum(x['casts']for x in results),'PA_spent':sum(x['pa_spent']for x in results),'commits':sum(x['commits']for x in results),'native_events':sum(x['events']for x in results),'records':results,'external_audit':False,'spell_attack_critical_status':'LAB_HYPOTHESIS'}
 (ROOT/'evidence/R198_MAGIC_AUDIT.json').write_text(json.dumps(rep,ensure_ascii=False,indent=2))
 print(json.dumps({k:v for k,v in rep.items() if k!='records'}))
 return rep
if __name__=='__main__':batch()
