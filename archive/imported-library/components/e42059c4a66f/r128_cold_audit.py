"""Independent R126 causality auditor. No import from native resolver, R18 or run generator.
Pure stdlib recomputes RNG, physical/PA/reaction math and turn, hash chain.
"""
import json,sqlite3,hashlib,random,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parent
VER='VLAB-R18-INTERACTIVE-CLI-0.1-EXPERIMENTAL'


def canon(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def digest(x):return hashlib.sha256(canon(x).encode()).hexdigest()
def die(seed,nonce,aid,kind,count,faces):
 q=hashlib.sha256(f'{seed}|{nonce}|R126-{aid}-{kind}|{count}d{faces}|{VER}'.encode()).digest()
 return [random.Random(int.from_bytes(q,'big')).randint(1,faces) for _ in ()] if False else roll(q,count,faces)
def roll(q,count,faces):
 rng=random.Random(int.from_bytes(q,'big'));return [rng.randint(1,faces) for _ in range(count)]
def dice_tape(st,aid,tar,kind='NORMAL',adv=0,dis=0):
 p=st['actors'][aid]['source_profile'];rr=st['actors'][aid]['resource'];n=st['action_nonce'][aid]+1
 weak=10*rr['hp']<p['hp'];net=max(-4,min(4,adv-dis-int(weak)))
 hits=[die(st['seed'],n,aid,kind+'-HIT-'+str(i),p['attack_dice'],6) for i in range(1+abs(net))]
 score=(max(map(sum,hits))+2*net if net>0 else min(map(sum,hits))+2*net if net<0 else sum(hits[0]))+p['attack_flat']
 groups=p['damage_dice'];dmg=[die(st['seed'],n,aid,kind+'-DAMAGE-'+str(i),nf[0],nf[1]) for i,nf in enumerate(groups)]
 return {'actor':aid,'target':tar,'kind':kind,'nonce':n,'adv':adv,'dis':dis,'crit':[die(st['seed'],n,aid,kind+'-CRIT-'+str(j),1,6)[0] for j in range(3)],
 'hit_rolls':hits,'score':score,'dmg_rolls':dmg,'normal_damage':sum(map(sum,dmg))+p['damage_flat'],
 'flat':p['damage_flat'],'bonus':p['attack_flat'],'damage_groups':[list(x) for x in groups],'weak':weak}
def init_order(st):
 rows=[]
 for aid,p in st['actors'].items():
  src=p['source_profile'];d=die(st['seed'],0,aid,'INIT',src['init_dice'],6)
  rows.append({'id':aid,'dice':d,'total':sum(d)+src['init_bonus'],'des':src['dex'],'source':src['source']})
 groups={}
 for r in rows:groups.setdefault((r['total'],r['des']),[]).append(r)
 out=[]
 for key in sorted(groups,reverse=True):
  team=groups[key]
  if len(team)==1:out.append(team[0]['id']);continue
  # R26 only the tied (total+DEX equal) roll again; no source material variance.
  def decide(team,n):
   if len(team)==1:return [team[0]['id']]
   if n>100:raise AssertionError('unbroken tie')
   g={}
   for a in team:
    p=st['actors'][a['id']]['source_profile'];roll_total=sum(die(st['seed'],n,a['id'],'INIT-TIE',p['init_dice'],6))+p['init_bonus']
    g.setdefault(roll_total,[]).append(a)
   if len(g)==1:return decide(team,n+1)
   return [j for score in sorted(g,reverse=True) for j in decide(g[score],n+1)]
  out+=decide(team,1)
 return rows,out

def cold(db):
 db=Path(db);st=json.loads(db.with_suffix('.genesis.json').read_text());initial=copy.deepcopy(st)
 with sqlite3.connect(db) as con:
  meta=dict(con.execute('SELECT key,value FROM meta'))
  rows=[json.loads(x[0]) for x in con.execute('SELECT row_json FROM events ORDER BY seq')]
  pending=con.execute('SELECT count(*) FROM pending').fetchone()[0]
 assert pending==0 and len(rows)==int(meta['revision'])
 head=meta['genesis'];counts={'events':0,'ordinary_attacks':0,'capa':0,'marca':0,'aoo':0,'movement':0,'safe':0,'negative_critical':0,'critical_positive':0,'ko':0,'paid_pa':0,'reactions':0}
 for idx,row in enumerate(rows,1):
  assert row['seq']==idx and row['prev']==head and row['before_sha']==digest(st),(db.name,idx,'chain/state-before')
  assert row['official_effects']==0 and row['synthetic'] is True
  detail=row['detail'];acts=detail['native_actions'];kind=row['kind'];cmd=row['payload'];actor=st['active']
  if kind=='INIT':
   observed,order=init_order(st)
   assert detail['extra']['initiative']==observed and detail['extra']['tie']['order']==order
   assert st['phase']=='INIT';st['phase']='ACTIVE';st['order']=order;st['round']=1;st['active']=order[0];assert acts==[]
  elif kind=='START':
   a=st['actors'][actor]['resource'];assert a['hp']>0 and a['standard']==0 and cmd=={'actor':actor}
   assert len(acts)==1 and acts[0]['action']=='turn_start' and acts[0]['by']==actor
   a['standard']=a['movement']=a['reaction']=1;st['actor_turns'][actor]+=1
  elif kind=='STRIKE':
   tar=cmd['attack']['target'];mode=cmd['reaction'];assert st['teams'][actor]!=st['teams'][tar]
   assert st['actors'][actor]['resource']['standard']==1
   expected=dice_tape(st,actor,tar,dis=int(mode=='CAPA'))
   assert cmd['attack']==expected,('rng',db.name,idx)
   crit=expected['crit'];assert crit[:2]!=[1,1] or crit[2]>2
   if mode=='CAPA':
    r=st['actors'][tar]['resource'];assert r['reaction']==1 and r['pa']>=35
    assert acts[0]['action']=='CAPA_POEIRA' and acts[0]['adds_disadvantage']==1 and acts[0]['PA_spent']==35
    r['reaction']=0;r['pa']-=35;counts['capa']+=1;counts['paid_pa']+=35;counts['reactions']+=1
   else:assert mode=='NONE'
   hit_raw=expected['normal_damage'];critical=crit[:2]==[6,6] and crit[2]>=5
   if critical:hit_raw+=sum(n*f for n,f in st['actors'][actor]['source_profile']['damage_dice'])
   defender=st['actors'][tar]['resource'];hit=expected['score']>defender['ca'] or critical
   net=max(0,hit_raw-st['actors'][tar]['source_profile']['rd']) if hit else 0
   before=defender['hp'];after=max(0,before-net)
   weapon=acts[-1]
   assert weapon['action']=='weapon_attack' and weapon['from']==actor and weapon['to']==tar
   assert weapon['hit']==hit and weapon['raw']==(hit_raw if hit else 0)
   assert weapon['net']==net and weapon['before_hp']==before and weapon['after_hp']==after
   assert weapon['hp_loss_actual']==before-after and weapon['overkill']==max(0,net-before)
   assert weapon['roll_score']==expected['score'] and weapon['disadvantage_levels']==int(mode=='CAPA')
   if critical:counts['critical_positive']+=1
   if before>0 and after==0:counts['ko']+=1
   defender['hp']=after;st['actors'][actor]['resource']['standard']=0;st['action_nonce'][actor]+=1;counts['ordinary_attacks']+=1
  elif kind=='MARCA':
   assert actor=='F1' and cmd['target']=='A' and cmd['range_verified'] and cmd['los_verified']
   r=st['actors'][actor]['resource'];assert r['pa']>=25 and r['standard']==1
   assert len(acts)==1 and acts[0]['action']=='MARCA_PASSOS_PERDIDOS' and acts[0]['PA_spent']==25
   assert acts[0]['attack_bonus_granted']==0 and acts[0]['duration_own_turns']==3
   r['pa']-=25;r['standard']=0;counts['paid_pa']+=25;counts['marca']+=1;st['ability_events']+=1
   st['marks']['F1']={'target':'A','bonus':'PERCEPTION_SURVIVAL_ONLY_+10',
    'declared_duration_turns':3,'elapsed_turns':0,'timing':'HOLD_SOURCE_BOUNDARY',
    'source':st['actors']['F1']['source'],'revision_created':idx}
  elif kind=='DISENGAGE':
   assert actor=='F1' and cmd=={'actor':'F1','enemy':'A'}
   r=st['actors'][actor]['resource'];assert r['standard']==1
   assert acts[0]['action']=='SAFE_DISENGAGE' and acts[0]['scope']=='ONE_ENEMY_ONLY'
   r['standard']=0;st['safe_named_enemy']='A';counts['safe']+=1
  elif kind in ('MOVE','SAFE_MOVE'):
   assert actor=='F1' and cmd['path']==['B1','B2'] and cmd['to']=='B2' and not cmd['forced']
   rr=st['actors'][actor]['resource'];assert rr['movement']==1 and rr['position']=='B1'
   aa=st['actors']['A']['resource'];assert aa['position']=='B0'
   if kind=='SAFE_MOVE':
    assert st['safe_named_enemy']=='A' and 'aoo' not in cmd and aa['reaction']==1
   elif aa['reaction']==1:
    tape=dice_tape(st,'A','F1',kind='AOO',adv=1)
    assert cmd['aoo']==tape and len(tape['hit_rolls'])==2
    assert tape['crit'][:2]!=[1,1] or tape['crit'][2]>2
    weapon=acts[0];assert weapon['action']=='weapon_attack' and weapon['attack_origin']=='OPPORTUNITY'
    assert weapon['advantage_levels']==1 and weapon['net_levels']==1
    crit=tape['crit'][:2]==[6,6] and tape['crit'][2]>=5
    raw=tape['normal_damage']+(sum(n*f for n,f in st['actors']['A']['source_profile']['damage_dice']) if crit else 0)
    hit=tape['score']>rr['ca'] or crit
    eff=max(0,raw-st['actors']['F1']['source_profile']['rd']) if hit else 0
    before=rr['hp'];after=max(0,before-eff)
    assert weapon['hit']==hit and weapon['raw']==(raw if hit else 0) and weapon['net']==eff
    assert weapon['after_hp']==after and weapon['hp_loss_actual']==before-after
    rr['hp']=after;aa['reaction']=0;st['action_nonce']['A']+=1;st['aoo_events']+=1
    counts['aoo']+=1;counts['reactions']+=1
    if crit:counts['critical_positive']+=1
    if before>0 and after==0:counts['ko']+=1
   if rr['hp']>0:
    mv=acts[-1];assert mv['action']=='move' and mv['from']=='B1' and mv['to']=='B2' and mv['travel_cost']=='1'
    rr['movement']=0;rr['position']='B2';counts['movement']+=1
   else:
    assert acts[-1]['action']=='MOVEMENT_INTERRUPTED_BY_KO' and rr['position']=='B1'
  elif kind=='END':
   assert cmd=={'actor':actor} and st['actors'][actor]['resource']['standard']==0
   assert len(acts)==1 and acts[0]['action']=='turn_end' and acts[0]['by']==actor
   i=st['order'].index(actor);st['turn_index']+=1
   for off in range(1,len(st['order'])+1):
    j=(i+off)%len(st['order']);w=st['order'][j]
    if st['actors'][w]['resource']['hp']>0:
     st['active']=w
     if j<=i:st['round']+=1
     break
   else:st['phase']='CENSORED_NO_LIVING';st['active']=None
  else:raise AssertionError(('unhandled',kind))
  assert row['after_sha']==digest(st),(db.name,idx,'causal state mismatch')
  head=digest(row);counts['events']+=1
 assert head==meta['head'] and digest(st)==digest(json.loads(meta['state']))
 assert len(rows)==int(meta['revision'])
 return {'file':db.name,'run_id':st['run_id'],'seed':st['seed'],'counts':counts,'final_state_digest':digest(st),
  'head':head,'genesis_digest':digest(initial),'pending':pending,'official':False,
  'terminal_pass':False,'native_solver_imported':False}

if __name__=='__main__':
 files=[ROOT/'runs'/'R126_PA_REACTION_AOO_DEV_943207.sqlite',
        ROOT/'runs'/'R126_SAFE_DISENGAGE_RESERVED_NOT_BLIND_953209.sqlite']
 reports=[cold(f) for f in files]
 out=ROOT/'R128_INDEPENDENT_COLD_AUDIT.json';out.write_text(json.dumps(reports,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(reports,indent=2,ensure_ascii=False))
