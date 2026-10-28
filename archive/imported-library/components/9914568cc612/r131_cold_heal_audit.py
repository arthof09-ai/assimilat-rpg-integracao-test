"""R131 independent causal check for R130 heal. Imports no native engine and no R18.
RNG replay implemented with stdlib, chain/hash and HP/PA independently derived.
"""
import json,hashlib,sqlite3,random,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parent
VER='VLAB-R18-INTERACTIVE-CLI-0.1-EXPERIMENTAL'

def can(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def dig(x):return hashlib.sha256(can(x).encode()).hexdigest()
def dice(seed,n,label,count,faces):
 data=hashlib.sha256(f'{seed}|{n}|{label}|{count}d{faces}|{VER}'.encode()).digest()
 rng=random.Random(int.from_bytes(data,'big'));return [rng.randint(1,faces) for _ in range(count)]
def cold(path):
 p=Path(path);st=json.loads(p.with_suffix('.genesis.json').read_text())
 with sqlite3.connect(p) as con:
  meta=dict(con.execute('SELECT key,value FROM meta'))
  rows=[json.loads(row[0]) for row in con.execute('SELECT row_json FROM events ORDER BY seq')]
  assert con.execute('SELECT count(*) FROM pending').fetchone()[0]==0
 assert len(rows)==10 and int(meta['revision'])==10
 h=meta['genesis'];metrics={'events':0,'damage_events':0,'heal_events':0,'PA_heal':0,'heal_effective':0,'source_heal_rolls':0,'item_bonus':0}
 for n,e in enumerate(rows,1):
  assert e['seq']==n and e['prev']==h and e['before_sha']==dig(st)
  kind=e['kind'];aid=st['active'];evt=e['detail']['native_actions'];payload=e['payload']
  if kind=='INIT':
   assert aid is None and st['phase']=='INIT'
   rows_init=e['detail']['extra']['initiative'];out=[]
   for entry in rows_init:
    a=entry['id'];p0=st['actors'][a]['source_profile']
    roll=dice(st['seed'],0,f'R130-{a}-INIT',p0['init_dice'],6)
    assert entry['dice']==roll and entry['total']==sum(roll)+p0['init_bonus']
    out.append(entry)
   # In these three profiles rank order is strict; fail rather than invent tie procedure.
   assert len({entry['total'] for entry in out})==3
   order=[r['id'] for r in sorted(out,key=lambda q:(q['total'],q['des']),reverse=True)]
   assert e['detail']['extra']['tie']['order']==order
   st['order']=order;st['active']=order[0];st['phase']='ACTIVE';st['round']=1
  elif kind=='START':
   assert payload=={'actor':aid} and evt[0]['action']=='turn_start'
   st['actors'][aid]['resource']['standard']=1;st['actors'][aid]['resource']['movement']=1;st['actors'][aid]['resource']['reaction']=1
   st['actor_turns'][aid]+=1
  elif kind=='ATTACK':
   tape=payload['attack'];target=tape['target'];att=st['actors'][aid]['source_profile'];tar=st['actors'][target]['source_profile']
   k=st['action_nonce'][aid]+1;assert tape['nonce']==k and tape['actor']==aid
   rolled=[dice(st['seed'],k,f'R130-{aid}-HIT-0',att['attack_dice'],6)]
   c=[dice(st['seed'],k,f'R130-{aid}-CRIT-{i}',1,6)[0] for i in range(3)]
   assert tape['crit']==c and tape['hit_rolls']==rolled
   d=[dice(st['seed'],k,f'R130-{aid}-DMG-{i}',nfaces[0],nfaces[1]) for i,nfaces in enumerate(att['damage_dice'])]
   assert tape['damage_rolls']==d
   score=sum(rolled[0])+att['attack_flat'];normal=sum(sum(group) for group in d)+att['damage_flat']
   assert tape['score']==score and tape['damage']==normal
   crit=c[:2]==[6,6] and c[2]>=5
   hit=score>st['actors'][target]['resource']['ca'] or crit
   raw=normal+(sum(u*v for u,v in att['damage_dice']) if crit else 0)
   net=max(0,raw-tar['rd']) if hit else 0
   before=st['actors'][target]['resource']['hp'];after=max(0,before-net)
   record=evt[0]
   assert record['action']=='weapon_attack' and record['roll_score']==score and record['hit']==hit
   assert record['raw']==(raw if hit else 0) and record['net']==net
   assert record['before_hp']==before and record['after_hp']==after
   st['actors'][target]['resource']['hp']=after;st['actors'][aid]['resource']['standard']=0;st['action_nonce'][aid]+=1
   metrics['damage_events']+=1
  elif kind=='HEAL':
   assert aid=='E' and payload['target']=='F1' and payload['range']
   assert st['actors'][aid]['resource']['pa']>=75 and st['actors'][aid]['resource']['standard']==1
   vals=dice(st['seed'],1,'R130-E-HEAL',8,10);assert vals==payload['dice']
   rec=evt[0];before=st['actors']['F1']['resource']['hp'];base=sum(vals)+25;bonus=20
   cap=st['actors']['F1']['resource']['maximum_hp'];heal=min(cap-before,base+bonus)
   assert rec['action']=='RECONSTITUICAO_SEIVA' and rec['healing_rolls']==vals
   assert rec['base_heal']==base and rec['equipped_gloves_bonus']==20 and rec['gross_heal']==base+20
   assert rec['hp_before']==before and rec['hp_after']==before+heal and rec['actual_healed']==heal
   assert rec['excess_heal']==base+20-heal and rec['PA_spent']==75 and not rec['target_resurrected'] and not rec['bleeding_removed']
   st['actors']['F1']['resource']['hp']=before+heal;st['actors']['E']['resource']['pa']-=75;st['actors']['E']['resource']['standard']=0
   metrics['heal_events']+=1;metrics['PA_heal']+=75;metrics['heal_effective']+=heal;metrics['source_heal_rolls']+=sum(vals);metrics['item_bonus']+=20
  elif kind=='END':
   assert payload=={'actor':aid} and evt[0]['action']=='turn_end'
   index=st['order'].index(aid);st['turn_index']+=1
   for off in range(1,4):
    j=(index+off)%3;t=st['order'][j]
    if st['actors'][t]['resource']['hp']>0:
     st['active']=t
     if j<=index:st['round']+=1
     break
  else:raise AssertionError('Unknown event '+kind)
  assert e['after_sha']==dig(st),(kind,n)
  h=dig(e);metrics['events']+=1
 assert dig(st)==dig(json.loads(meta['state'])) and h==meta['head']
 assert metrics=={'events':10,'damage_events':2,'heal_events':1,'PA_heal':75,'heal_effective':96,'source_heal_rolls':51,'item_bonus':20}
 return {'run_id':st['run_id'],'metrics':metrics,'head':h,'seed':st['seed'],
 'auditor_imports_native_or_R18':False,'recovery_state':'PASS_ATOMIC_REOPEN','terminal_certificate':False}
if __name__=='__main__':
 r=cold(ROOT/'runs'/'R130_HEAL_SOURCE_3ACTOR_S963211.sqlite')
 (ROOT/'R131_HEAL_COLD_AUDIT.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(r,indent=2,ensure_ascii=False))
