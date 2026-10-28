"""Independent R174 evidence verifier: does not import executor, R18 or native engine.
Checks source-pinned formulas, RNG, event sequence, resources, SQLite SHA, checkpoint.
Independent CODE here is not an externally appointed auditor/homologation.
"""
from __future__ import annotations
import pathlib,sqlite3,json,hashlib,random,copy,sys,collections
VERSION='R174-ON5-SOURCE-PROPOSAL-TEST-v1'
SOURCE={
 'VAROK':dict(url='https://app.notion.com/p/3f6c2b324ede81f49ea9efbe1a811091',hp=734,pa=324,ca=83,rd=35,init_bonus=29,hit_bonus=100,damage_n=10,damage_faces=10,flat=48,defender=99),
 'ARVETH':dict(url='https://app.notion.com/p/3f6c2b324ede8105891fc647242e61ca',hp=806,pa=344,ca=93,rd=30,init_bonus=25,hit_bonus=72,damage_n=8,damage_faces=10,flat=35)}
def canon(v):return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def sha(v):return hashlib.sha256(canon(v).encode()).hexdigest()
def roll(seed,key,n,faces):
 rng=random.Random(int.from_bytes(hashlib.sha256(f'{VERSION}|{seed}|{key}|{n}d{faces}'.encode()).digest(),'big'))
 return [rng.randint(1,faces) for _ in range(n)]
def tape(seed,actor,turn):
 f=SOURCE[actor]
 return {'critical':roll(seed,f'{actor}-TURN{turn}-CRIT',3,6),
 'hit':roll(seed,f'{actor}-TURN{turn}-HIT',4,6),'hit_weak':roll(seed,f'{actor}-TURN{turn}-HIT-WEAK',4,6),
 'damage':roll(seed,f'{actor}-TURN{turn}-DAMAGE',f['damage_n'],f['damage_faces']),
 'power':roll(seed,f'{actor}-TURN{turn}-POWER',6,12) if actor=='VAROK' else []}
def read_db(db):
 with sqlite3.connect(str(db)) as c:
  meta=dict(c.execute('select key,value from meta'))
  rows=list(c.execute('select seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha from events order by seq'))
  pend=list(c.execute('select cmd_id from pending'))
 return meta,rows,pend

def audit(db):
 db=pathlib.Path(db);meta,rows,pend=read_db(db)
 assert not pend,('pending',db,pend)
 assert int(meta['revision'])==len(rows)
 state=json.loads(meta['state']);seed=state['seed'];policy=state.get('r174_policy')
 assert state['r174_source_status']=='TWO_MASTER_SIDE_ENCOUNTER_PROPOSALS_NOT_ED_OR_OFFICIAL'
 assert state['synthetic'] is True and state['winner'] in ('VAROK','ARVETH')
 for who,f in SOURCE.items():
  sf=state['actors'][who]['stats'];assert sf['source']==f['url'];assert sf['rd_physical']==f['rd'];assert sf['initiative']=='4d6+'+str(f['init_bonus'])
 prev=meta['genesis'];after=None;all_native=[];events=[]
 hp={k:v['hp'] for k,v in SOURCE.items()};pa={k:v['pa'] for k,v in SOURCE.items()};reaction={k:1 for k in SOURCE};std={k:0 for k in SOURCE}
 act_turns={k:0 for k in SOURCE};power_used=False
 metric=collections.Counter();seen_cmd=set();init=None;active=None;turnorder=None;nr=0;defense_prevented=0
 for seq,cmd_id,p,row_json,row_sha,before_sha,after_sha in rows:
  row=json.loads(row_json)
  assert seq==row['seq'] and cmd_id==row['cmd_id'] and cmd_id not in seen_cmd
  seen_cmd.add(cmd_id)
  assert row['prev']==prev and prev==p and sha(row)==row_sha
  assert row['before_sha']==before_sha and row['after_sha']==after_sha
  if after is not None:assert before_sha==after
  after=after_sha;prev=row_sha
  kind=row['kind'];detail=row['detail'];events.append(row)
  if kind=='R174_SOURCE_INIT':
   assert init is None and seq==1
   init=detail['rolls'];assert set(x['actor'] for x in init)==set(SOURCE)
   for item in init:
    x=item['actor'];f=SOURCE[x];t=roll(seed,'INIT-'+x,4,6)
    assert item=={'actor':x,'roll':t,'bonus':f['init_bonus'],'total':sum(t)+f['init_bonus']}
   assert init[0]['total']!=init[1]['total']
   turnorder=[x['actor'] for x in init];active=turnorder[0];assert detail['order']==turnorder
   n=[detail['first_turn_event']]
  elif kind=='R174_SOURCE_ATTACK':
   assert init is not None and active is not None
   a=detail['attacker'];d=detail['target'];assert a==active and d!=a
   act_turns[a]+=1;expected=tape(seed,a,act_turns[a]);assert detail['roll_tape']==expected
   assert row['payload']['roll_tape']==expected and row['payload']['policy']==policy
   f=SOURCE[a];fd=SOURCE[d];at=detail['attack'];critical=expected['critical']
   weak=(0<hp[a]*10<f['hp']);score=(min(sum(expected['hit']),sum(expected['hit_weak']))+f['hit_bonus']-2) if weak else sum(expected['hit'])+f['hit_bonus']
   assert at['roll_score']==score and at['ca_exact']==str(fd['ca']) and at['from']==a and at['to']==d
   assert at['r174_source_actor']==f['url'] and at['r174_source_defender']==fd['url']
   assert detail['source']==f['url']
   crit='POSITIVE' if critical[:2]==[6,6] and critical[2]>=5 else 'NEGATIVE' if critical[:2]==[1,1] and critical[2]<=2 else 'NONE'
   assert at['critical']==crit;hit=(score>fd['ca'] or crit=='POSITIVE') and crit!='NEGATIVE'
   assert at['hit']==hit
   power=detail['energy_activation'];power_hit=power is not None
   assert at['r174_paid_power']==power_hit
   if policy=='DEFEND_NO_POWER':assert not power_hit
   if power_hit:
    assert a=='VAROK' and hit and not power_used and pa[a]>=60
    assert power['ability']=='Quebra do Tronco' and power['cost_pa']==60 and power['after_attack_seq']==at['seq']
    assert power['power_damage_dice']==expected['power'] and power['rd_applied_once'] is True
    assert len(at['damage_roll_groups'])==2 and at['damage_roll_groups'][1]==expected['power']
    power_used=True;pa[a]-=60;metric['pa_spent']+=60;metric['power_uses']+=1
   else:assert len(at['damage_roll_groups'])==1
   assert at['damage_roll_groups'][0]==expected['damage']
   raw_normal=sum(expected['damage'])+f['flat']+(sum(expected['power']) if power_hit else 0)
   assert at['normal_damage']==raw_normal
   positive_bonus=sum(n*faces for n,faces in ([(f['damage_n'],f['damage_faces'])]+([(6,12)] if power_hit else []))) if crit=='POSITIVE' else 0
   defender_event=detail['defense'];defended=defender_event is not None
   assert defended==(d=='VAROK' and policy in ('DEFEND_VAROK','DEFEND_NO_POWER'))
   if defended:
    assert reaction[d]==1
    assert defender_event['action']=='DEFENDER' and defender_event['by']==d
    assert int(defender_event['defense_exact'])==99 and defender_event['attack_score']==score
    assert defender_event['damage_negated']==(score<=99)
    assert at['r174_defense_event_seq']==defender_event['seq']
    reaction[d]=0;metric['reaction_spent']+=1
   else:assert at['r174_defense_event_seq'] is None
   is_negated=defended and score<=99
   assert at['defense_negated']==is_negated
   raw=(raw_normal+positive_bonus) if hit and not is_negated else 0
   net=max(0,raw-fd['rd']) if raw else 0
   loss=min(hp[d],net);over=max(0,net-hp[d])
   assert (at['before_hp'],at['after_hp'],at['hp_loss_actual'],at['overkill'])==(hp[d],hp[d]-loss,loss,over)
   assert (at['raw'],at['rd_applied'],at['net'])==(raw,fd['rd'] if raw else 0,net)
   assert std[a]==1 and at['attack_origin']=='NORMAL'
   std[a]=0;hp[d]-=loss
   assert detail['HP_after']==hp and detail['PA_after']==pa
   metric['attacks']+=1;metric['hits']+=int(hit);metric['hp_loss']+=loss;metric['post_rd']+=net;metric['overkill']+=over
   metric['crit_positive']+=int(crit=='POSITIVE');metric['crit_negative']+=int(crit=='NEGATIVE')
   if is_negated and hit:
    defense_prevented+=max(0,sum(expected['damage'])+f['flat']-fd['rd'])
   n=detail['native_events']
   if hp[d]==0:active=None
   else:active=turnorder[(turnorder.index(a)+1)%2]
  else:raise AssertionError(('unsupported R174 row',kind))
  for e in n:
   nr+=1;assert e['seq']==nr;all_native.append(e)
   if e['action']=='turn_start':
    assert e['by'] in SOURCE
    who=e['by'];assert std[who]==0
    std[who]=1;reaction[who]=1
   elif e['action']=='turn_end':
    assert std[e['by']]==0
   elif e['action']=='DEFENDER':
    assert e['by']=='VAROK' and e['defense_exact']=='99'
   elif e['action']=='weapon_attack':
    assert e['from'] in SOURCE and e['to'] in SOURCE
   elif e['action']=='ON_HIT_ENERGY_RIDER':
    assert e['by']=='VAROK' and e['cost_pa']==60
   else:raise AssertionError(('unrecognized native',e['action']))
  if kind=='R174_SOURCE_ATTACK':
   assert detail['reaction_after']==reaction
   if active is not None:assert detail['scheduler']['next_turn']==active
   assert state['r174_turn_history'][metric['attacks']-1]['attack_seq']==at['seq']
 assert prev==meta['head'] and after==sha(state)
 assert all_native==state['r174_native_events']
 assert hp=={x:state['actors'][x]['resource']['hp'] for x in SOURCE}
 assert pa=={x:state['actors'][x]['resource']['pa'] for x in SOURCE}
 assert reaction=={x:state['actors'][x]['resource']['reaction'] for x in SOURCE}
 assert {x:std[x] for x in SOURCE}=={x:state['actors'][x]['resource']['standard'] for x in SOURCE}
 assert state['r174_metrics']['attacks']==metric['attacks']
 for k in ('hits','hp_loss','post_rd','overkill','reaction_spent','pa_spent','power_uses','crit_positive','crit_negative'):
  assert state['r174_metrics'][k]==metric[k],(k,state['r174_metrics'][k],metric[k])
 assert state['r174_metrics']['defense_prevented_hp']==defense_prevented
 assert len(state['r174_turn_history'])==metric['attacks']
 ck=pathlib.Path(str(db)+'.checkpoint.json')
 assert ck.exists()
 c=json.loads(ck.read_text())
 assert sha(c['body'])==c['sha256']
 assert c['body']['state']==state and c['body']['head']==prev and c['body']['revision']==len(rows)
 return {'db':db.name,'commits':len(rows),'native_events':nr,'attacks':metric['attacks'],'hp':hp,'pa':pa,'reactions':reaction,'winner':state['winner'],'metrics':dict(metric)|{'defense_prevented_hp':defense_prevented},'head':prev,'pass':True}

if __name__=='__main__':
 import glob,argparse
 ap=argparse.ArgumentParser();ap.add_argument('directory');o=ap.parse_args()
 results=[]
 for path in sorted(glob.glob(str(pathlib.Path(o.directory)/'duels/*.sqlite'))):results.append(audit(path))
 print(json.dumps({'audit':'R174_COLD_INDEPENDENT_MATH_CAUSAL_CHECK','results':results,'pass':True},ensure_ascii=False,indent=2))
