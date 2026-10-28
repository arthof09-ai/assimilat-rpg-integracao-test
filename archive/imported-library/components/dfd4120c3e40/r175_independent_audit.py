"""R175 independent maths/causal verifier; no producer, v0.8.1 or R18 import.
In addition to SHA/SQLite chain it reconstructs RNG tapes, score, critical,
mitigation, effective lost HP, overkill, resource, scheduler, native events.
Not an external human NAC-PASS audit.
"""
import sqlite3,json,pathlib,hashlib,random,collections,sys,copy
VERSION='VLAB-R175-ED-BE-SOURCE-PHYSICAL-TEST-v1'
F={
 'AUREN':dict(url='https://app.notion.com/p/3ebc2b324ede814bb730d47dd7bd5f02',hp=523,pa=719,ca=225,rd=35,bonus=193,n=8,faces=8,flat=211,status='FICHA_MESTRE'),
 'ROC':dict(url='https://app.notion.com/p/3f3c2b324ede813987deda0b382e83c7',hp=4200,pa=3740,ca=164,rd=75,bonus=150,n=20,faces=10,flat=0,status='PRECREATE_BLUEPRINT')}
def canon(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def sha(v):return hashlib.sha256(canon(v).encode()).hexdigest()
def dice(seed,key,n,faces):
 rng=random.Random(int.from_bytes(hashlib.sha256(f'{VERSION}|{seed}|{key}|{n}d{faces}'.encode()).digest(),'big'))
 return [rng.randint(1,faces) for _ in range(n)]
def tape(seed,actor,turn):
 f=F[actor];return {'critical':dice(seed,f'{actor}-TURN{turn}-CRIT',3,6),'hit':dice(seed,f'{actor}-TURN{turn}-HIT',6,6),'hit_weak':dice(seed,f'{actor}-TURN{turn}-HIT-WEAK',6,6),'damage':dice(seed,f'{actor}-TURN{turn}-DAMAGE',f['n'],f['faces'])}
def audit(db):
 db=pathlib.Path(db);c=sqlite3.connect(db);meta=dict(c.execute('select key,value from meta'));rows=list(c.execute('select seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha from events order by seq'));pending=list(c.execute('select cmd_id from pending'));c.close()
 assert not pending and int(meta['revision'])==len(rows)
 st=json.loads(meta['state']);seed=st['seed'];order=st['r175_order_branch'];assert st['synthetic'] and st['r175_version']==VERSION and seed==1750101
 assert st['source_status']=='SOURCE_DOCUMENTED_ED_AND_PRECREATE_BE_SCOPE_CONDITIONAL'
 for k in F:
  src=st['actors'][k]['stats'];f=F[k];assert src['source']==f['url'] and src['status']==f['status'] and src['physical_rd']==f['rd'] and src['attack_bonus']==f['bonus']
 seq_order=['AUREN','ROC'] if order=='AUREN_FIRST' else ['ROC','AUREN']
 hp={k:v['hp'] for k,v in F.items()};pa={k:v['pa'] for k,v in F.items()};reaction={k:1 for k in F};standard={k:0 for k in F};cnt=collections.Counter();turns=collections.Counter();native=[]
 previous=meta['genesis'];after=None;active=None;end_actor=None;hit_by=collections.Counter();effective_by=collections.Counter();attempt_by=collections.Counter();critical_by=collections.Counter()
 for i,cmd,p,rowjson,rowsha,bef,aft in rows:
  row=json.loads(rowjson);assert i==row['seq'] and row['cmd_id']==cmd and row['prev']==p==previous and sha(row)==rowsha
  assert row['before_sha']==bef and row['after_sha']==aft
  if after is not None:assert bef==after
  after=aft;previous=rowsha
  detail=row['detail'];fresh=[]
  if row['kind']=='R175_SOURCE_START':
   assert i==1 and active is None and detail['kind']=='EXOGENOUS_INIT_ORDER_SENSITIVITY'
   assert detail['order']==seq_order and row['payload']['order']==order
   active=seq_order[0];fresh=detail['native_events']
  elif row['kind']=='R175_SOURCE_PHYSICAL_ATTACK':
   a=detail['actor'];d=detail['target'];assert a==active and d!=a
   assert row['payload']['actor']==a and row['payload']['target']==d and row['payload']['seed']==seed
   turns[a]+=1;expected=tape(seed,a,turns[a]);assert row['payload']['tape']==expected==detail['tape']
   assert row['payload']['actor_turn']==turns[a] and detail['actor_turn']==turns[a]
   assert detail['source_page']==F[a]['url'] and detail['target_page']==F[d]['url']
   ev=detail['attack'];f=F[a];fd=F[d]
   assert ev['from']==a and ev['to']==d and ev['attack_origin']=='NORMAL'
   assert ev['weak_attacker']==(hp[a]*10<f['hp'])
   weak=hp[a]*10<f['hp'];attempts=[tuple(expected['hit']),tuple(expected['hit_weak'])] if weak else [tuple(expected['hit'])]
   score=(min(map(sum,attempts))+f['bonus']-2) if weak else sum(expected['hit'])+f['bonus']
   assert ev['roll_score']==score and ev['ca_exact']==str(fd['ca'])
   assert [list(t) for t in ev['attack_roll_attempts']]==[list(t) for t in attempts]
   crit='POSITIVE' if expected['critical'][:2]==[6,6] and expected['critical'][2]>=5 else 'NEGATIVE' if expected['critical'][:2]==[1,1] and expected['critical'][2]<=2 else 'NONE'
   assert ev['critical']==crit and ev['critical_sequence']==expected['critical']
   hit=(score>fd['ca'] or crit=='POSITIVE') and crit!='NEGATIVE';assert ev['hit']==hit
   raw0=sum(expected['damage'])+f['flat'];assert ev['normal_damage']==raw0
   total=raw0+(f['n']*f['faces'] if crit=='POSITIVE' else 0) if hit else 0
   post=max(0,total-fd['rd']) if hit else 0;loss=min(hp[d],post);over=max(0,post-hp[d]);assert (ev['raw'],ev['rd_applied'],ev['net'])==(total,fd['rd'] if hit else 0,post)
   assert (ev['before_hp'],ev['after_hp'],ev['hp_loss_actual'],ev['overkill'])==(hp[d],hp[d]-loss,loss,over)
   assert standard[a]==1;standard[a]=0;hp[d]-=loss
   assert detail['HP_after']==hp and detail['PA_after']==pa and detail['reactions_after']==reaction
   cnt['attempts']+=1;cnt['hits']+=int(hit);cnt['post_rd']+=post;cnt['hp_loss']+=loss;cnt['overkill']+=over;cnt['crit_positive']+=int(crit=='POSITIVE');cnt['crit_negative']+=int(crit=='NEGATIVE')
   hit_by[a]+=int(hit);effective_by[a]+=loss;attempt_by[a]+=1;critical_by[a+'_'+crit]+=1
   fresh=detail['new_native_events']
   if hp[d]==0:
    assert detail['scheduler']['ko']==d and detail['scheduler']['next'] is None;active=None;end_actor=a
   else:
    active=seq_order[(seq_order.index(a)+1)%2];assert detail['scheduler']['next_turn']==active
  else:raise AssertionError(('unexpected',row['kind']))
  for ev in fresh:
   assert ev['seq']==len(native)+1;native.append(ev)
   name=ev['action'];who=ev.get('by')
   if name=='turn_start':
    assert standard[who]==0 and hp[who]>0;standard[who]=1;reaction[who]=1
   elif name=='turn_end':assert standard[who]==0
   elif name=='weapon_attack':assert ev['from'] in F and ev['to'] in F
   else:raise AssertionError(('native non-source event',name))
 assert st['phase']=='FINISHED' and st['winner']=='AUREN' and st['active'] is None
 assert prev==meta['head'] if (prev:=previous) else False
 assert after==sha(st)
 assert st['r175_native_events']==native
 assert st['r175_counts']==dict(cnt)|{'pa_spent':0,'reactions_spent':0} or all(st['r175_counts'].get(k)==cnt.get(k,0) for k in st['r175_counts'])
 assert hp=={k:st['actors'][k]['resource']['hp'] for k in F}
 assert pa=={k:st['actors'][k]['resource']['pa'] for k in F}
 assert len(st['r175_history'])==cnt['attempts']
 assert len(rows)==1+cnt['attempts']
 cp=pathlib.Path(str(db)+'.checkpoint.json');assert cp.exists();doc=json.loads(cp.read_text());assert sha(doc['body'])==doc['sha256'];assert doc['body']['state']==st and doc['body']['revision']==len(rows) and doc['body']['head']==previous
 return {'file':db.name,'audit':'PASS','winner_conditional':st['winner'],'order':order,'rounds':st['round'],'commits':len(rows),'native_events':len(native),'attacks':dict(attempt_by),'hits':dict(hit_by),'effective_hp_removed':dict(effective_by),'hp_end':hp,'pa_end':pa,'metrics':st['r175_counts'],'criticals':dict(critical_by),'head':previous}
if __name__=='__main__':
 results=[audit(p) for p in sorted(pathlib.Path(sys.argv[1]).glob('*.sqlite'))]
 print(json.dumps({'verifier':'R175_INDEPENDENT_MATH_CAUSAL','source_based_conditional':True,'results':results,'passed':len(results)},indent=2,ensure_ascii=False))
