"""R166 cold stdlib semantic verifier; never imports native resolver, never writes the ledgers."""
import json,sqlite3,hashlib,random,copy
from pathlib import Path
HERE=Path(__file__).parent
R18='VLAB-R18-INTERACTIVE-CLI-0.1-EXPERIMENTAL'
def can(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def sha(x):return hashlib.sha256(can(x).encode()).hexdigest()
def dice(seed,who,tag,nonce,n,f):
 d=hashlib.sha256(f'{seed}|{nonce}|R166-{who}-{tag}|{n}d{f}|{R18}'.encode()).digest()
 rng=random.Random(int.from_bytes(d,'big'));return [rng.randint(1,f) for _ in range(n)]
def verify(db):
 s=json.loads(db.with_suffix('.genesis.json').read_text());seed=s['seed']
 with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as c:
  assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
  meta=dict(c.execute('select key,value from meta'))
  assert c.execute('select count(*) from pending').fetchone()[0]==0
  rows=[(i,json.loads(data),rsha) for i,data,rsha in c.execute('select seq,row_json,row_sha from events order by seq')]
 assert len(rows)==5 and [r['kind'] for _,r,_ in rows]==['START','COCOON','END_E','START','AOO_CHAIN']
 assert meta['genesis']==sha({'genesis':s,'lineage':'R18_R26_V081_R166_R42_R43_CASULO'})
 prev=meta['genesis'];data=[]
 for i,r,row_sha in rows:
  assert i==r['seq'] and r['prev']==prev and row_sha==sha(r) and r['before_sha']==sha(s),(i,'hash-before')
  event=r['kind'];e=r['detail']['native_actions'];p=r['payload']
  if event=='START':
   a=p['actor'];assert a==s['active']
   assert e[0]['action']=='turn_start' and e[0]['by']==a
   aa=s['actors'][a]['resource'];assert aa['standard']==0
   aa.update(standard=1,movement=1,reaction=1)
   if a=='A':assert e[0]['speed']=='12'
  elif event=='COCOON':
   assert p=={'target':'A','range_m':3} and s['active']=='E' and not s['cocoon']
   assert e[0]['action']=='CASULO_BROTOS' and e[0]['CA_delta']==22 and e[0]['movement_delta_m']==-4 and e[0]['expiration_boundary']=='HOLD_SOURCE_NOT_DEFINED'
   ee=s['actors']['E']['resource'];aa=s['actors']['A']['resource']
   assert ee['standard']==1 and ee['pa']>=60
   ee['standard']=0;ee['pa']-=60;aa['ca']=247;aa['cocoon_source_speed_penalty_m']=4;s['cocoon']=True
  elif event=='END_E':
   assert p=={'actor':'E'} and s['active']=='E' and s['actors']['E']['resource']['standard']==0
   assert e[0]['action']=='turn_end';s['active']='A'
  elif event=='AOO_CHAIN':
   assert s['active']=='A' and s['cocoon'] and not s['aoo_trigger']
   assert p['voluntary'] and p['distance_m']==1.5 and p['order']==['F','V']
   assert s['actors']['A']['resource']['ca']==247 and s['actors']['A']['resource']['base_speed']==16
   aa=s['actors']['A']['resource'];native_attacks=[z for z in e if z['action']=='weapon_attack']
   skipped=[];nets=[];actuals=[]
   for who,t in zip(['F','V'],p['tapes']):
    if aa['hp']<=0:
     skipped.append(who);continue
    cfg=(4,92,8,8,47,'perfurante') if who=='F' else (4,100,10,10,48,'impacto')
    n,bonus,count,faces,flat,damage_tag=cfg
    assert t['who']==who and t['nonce']==1
    assert t['rolls']==[dice(seed,who,f'AOO-HIT-{j}',1,n,6) for j in range(2)]
    assert t['crit']==[dice(seed,who,f'AOO-CRIT-{j}',1,1,6)[0] for j in range(3)]
    assert t['damage_roll_groups']==[dice(seed,who,'AOO-DMG-0',1,count,faces)]
    score=max(map(sum,t['rolls']))+bonus+2
    positive=t['crit'][:2]==[6,6] and t['crit'][2]>=5
    negative=t['crit'][:2]==[1,1] and t['crit'][2]<=2
    hit=(positive or score>247) and not negative
    base=sum(t['damage_roll_groups'][0])+flat
    raw=(base+count*faces*int(positive)) if hit else 0
    net=max(0,raw-35) if hit else 0;actual=min(aa['hp'],net)
    na=native_attacks[len(nets)]
    assert t['score']==score and t['dmg']==base
    assert na['from']==who and na['to']=='A' and na['attack_origin']=='OPPORTUNITY'
    assert na['type']==damage_tag and na['critical']==('POSITIVE' if positive else 'NEGATIVE' if negative else 'NONE')
    assert na['hit']==hit and na['raw']==raw and na['net']==net and na['hp_loss_actual']==actual
    assert na['ca_exact']=='247' and na['overkill']==net-actual and na['before_hp']==aa['hp'] and na['after_hp']==aa['hp']-actual
    assert na['attack_roll_attempts']==t['rolls'] and na['critical_sequence']==t['crit']
    if negative:assert na['critical_failure_policy']=='CRITICAL_FAILURE / VLAB-LAB-POLICY' and raw==0 and actual==0
    s['actors'][who]['resource']['reaction']=0;s['action_nonce'][who]+=1;aa['hp']-=actual
    nets.append(net);actuals.append(actual)
   assert len(native_attacks)==len(nets)
   assert [x['attacker'] for x in r['detail']['skipped']]==skipped
   if aa['hp']>0:
    assert len(e)==len(nets)+1 and e[-1]['action']=='move' and e[-1]['by']=='A'
    assert e[-1]['speed']=='12' and e[-1]['travel_cost']=='3/2'
    aa['position']='OUT_OF_ADJACENCY';aa['movement']=0
   else:
    assert len(e)==len(nets) and aa['position']=='CENTER' and s['actors']['V']['resource']['reaction']==1
   s['aoo_trigger']=True;s['phase']='TECHNICAL_AOO_PREFIX_COMPLETE';s['active']=None
   data.append({'run':db.stem,'roll_crit_first':p['tapes'][0]['crit'],'net':nets,'actual':actuals,'skipped':skipped,'move':aa['position'],'target_hp':aa['hp']})
  else:raise AssertionError(event)
  assert r['after_sha']==sha(s),(i,event,'CAUSAL_AFTER_MISMATCH',r['after_sha'],sha(s))
  prev=row_sha
 assert prev==meta['head'] and can(s)==can(json.loads(meta['state']))
 return {'run':db.stem,'PASS':True,'commits':len(rows),'HP_final':s['actors']['A']['resource']['hp'],'actor_ca':247,'actor_speed_penalty_m':4,'casulo_expiry':'HOLD','records':data,'head':prev}
if __name__=='__main__':
 p=sorted(x for x in (HERE/'runs').glob('R166_V2_CASULO_AOO_*.sqlite') if '.checkpoint.' not in x.name)
 assert len(p)==2,p
 result=[verify(x) for x in p]
 (HERE/'R166_COLD_CONCURRENT_CASULO_R42_R43_AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(result,ensure_ascii=False,indent=2))
