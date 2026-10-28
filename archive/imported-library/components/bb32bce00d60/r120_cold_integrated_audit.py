"""R120 independent standard-library-only ledger auditor. DOES NOT IMPORT engine/runner."""
from __future__ import annotations
import copy,hashlib,json,sqlite3,random
from pathlib import Path
ROOT=Path(__file__).resolve().parent
R18_VERSION='VLAB-R18-INTERACTIVE-CLI-0.1-EXPERIMENTAL'

def canon(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def sha(x):return hashlib.sha256(canon(x).encode()).hexdigest()
def oracle(seed,seq,actor,kind,n,faces):
 e=hashlib.sha256(f'{seed}|{seq}|R119-{actor}-{kind}|{n}d{faces}|{R18_VERSION}'.encode()).digest()
 rng=random.Random(int.from_bytes(e,'big'));return [rng.randint(1,faces) for _ in range(n)]

def independently_order_initiative(rows,seed,actors):
 """Mestre: descending total, DES; equal total+DES only tied reroll."""
 def resolve(items,n):
  if len(items)==1:return [items[0]['id']]
  if n>128:raise AssertionError('unresolved tie')
  groups={}
  for x in items:
   aid=x['id'];p=actors[aid]['source_profile']
   val=sum(oracle(seed,n,aid,'INIT-TIE',p['init_dice'],6))+p['init_bonus']
   groups.setdefault(val,[]).append(x)
  if len(groups)==1:return resolve(items,n+1)
  return [aid for v in sorted(groups,reverse=True) for aid in resolve(groups[v],n+1)]
 total_groups={}
 for x in rows:total_groups.setdefault(x['total'],[]).append(x)
 out=[]
 for total in sorted(total_groups,reverse=True):
  dexgroups={}
  for x in total_groups[total]:dexgroups.setdefault(x['des'],[]).append(x)
  for dex in sorted(dexgroups,reverse=True):out+=resolve(dexgroups[dex],1)
 return out

def cold(file):
 file=Path(file)
 genesis=json.loads(file.with_suffix('.genesis.json').read_text())
 assert genesis['run_id']==file.stem and genesis['technical_instancing'] and genesis['no_canonical_credit']
 with sqlite3.connect(file) as con:
  meta=dict(con.execute('select key,value from meta'))
  rows=[json.loads(x[0]) for x in con.execute('select row_json from events order by seq')]
  n_events=con.execute('select count(*) from events').fetchone()[0]
  pending=con.execute('select count(*) from pending').fetchone()[0]
 assert pending==0 and len(rows)==n_events==int(meta['revision'])
 st=copy.deepcopy(genesis);head=meta['genesis'];cnt={'event':0,'initiative':0,'normal_attacks':0,'counter_response':0,
 'counter_no_response':0,'esquivar':0,'defender':0,'counter_declarations':0,'criticals':0,
 'ko':0,'target_changes':0,'reaction_refresh':0,'no_reaction_chain':0,'same_window_blocks':0}
 prev_target=None
 for ix,e in enumerate(rows,1):
  assert e['seq']==ix and e['prev']==head and e['before_sha']==sha(st),(file.name,ix,'before_mismatch')
  assert e['synthetic'] is True and e['official_effects']==0
  assert e['kind'] in ('INIT','START','STRIKE','END')
  a=st['active'];kind=e['kind'];acts=e['detail']['native_actions'];payload=e['payload']
  if kind=='INIT':
   assert st['phase']=='INIT' and not acts
   inf=e['detail']['extra']['initiative']; seen=set();rank=[]
   for row in inf:
    who=row['id'];p=st['actors'][who]['source_profile']
    assert who not in seen and row['source']==p['source'] and row['des']==p['dex']
    expected=oracle(st['seed'],0,who,'INIT',p['init_dice'],6)
    assert row['dice']==expected and row['total']==sum(expected)+p['init_bonus']
    assert p['init_bonus']==p['dex']+2 and row['prof_applied']==2
    seen.add(who);rank.append((row['total'],row['des'],who))
   assert len(seen)==len(st['actors'])
   order=e['detail']['extra']['tie_resolution']['order']
   assert order==independently_order_initiative(inf,st['seed'],st['actors']),('initiative_order',file.name)
   for transcript in e['detail']['extra']['tie_resolution']['rerolls']:
    for draw in transcript['draws']:
     aid=draw['id'];profile=st['actors'][aid]['source_profile']
     score=sum(oracle(st['seed'],draw['ordinal'],aid,'INIT-TIE',profile['init_dice'],6))+profile['init_bonus']
     assert draw['roll_total']==score
   st['order']=order;st['active']=order[0];st['round']=1;st['phase']='ACTIVE';cnt['initiative']+=1
  elif kind=='START':
   assert len(acts)==1 and acts[0]['action']=='turn_start' and acts[0]['by']==a and payload['actor']==a
   p=st['actors'][a]['resource'];assert p['hp']>0 and p['standard']==0
   if p['reaction']==0:cnt['reaction_refresh']+=1
   p['standard']=p['movement']=p['reaction']=1
   st['actor_turns'][a]+=1
   assert acts[0]['weak']==(10*p['hp']<p['maximum_hp'])
  elif kind=='STRIKE':
   atk=payload['attack'];target=atk['target'];resp=payload['reaction'];origin=payload['attack_origin']
   assert origin=='NORMAL' and atk['actor']==a and payload['reaction'] in ('NONE','DEFENDER','ESQUIVAR','COUNTER')
   assert st['actors'][a]['resource']['standard']==1 and st['actors'][target]['resource']['hp']>0
   assert st['teams'][a]!=st['teams'][target]
   if prev_target is not None and a=='A' and prev_target!=target:cnt['target_changes']+=1
   if a=='A':prev_target=target
   n=st['action_nonce'][a]+1;p=st['actors'][a]['source_profile'];crit=atk['crit']
   assert crit==[oracle(st['seed'],n,a,f'NORMAL-CRIT-{j}',1,6)[0] for j in range(3)]
   assert not(crit[:2]==[1,1] and crit[2]<=2)
   weak=10*st['actors'][a]['resource']['hp'] < p['hp']
   hits=[oracle(st['seed'],n,a,f'NORMAL-HIT-{j}',p['attack_dice'],6) for j in range(2 if weak else 1)]
   assert atk['hit_rolls']==hits
   score=(min(map(sum,hits))-2 if weak else sum(hits[0]))+p['attack_flat']
   assert score==atk['score']
   dg=[oracle(st['seed'],n,a,f'NORMAL-DMG-{j}',count,face) for j,(count,face) in enumerate(p['damage_dice'])]
   assert atk['damage_rolls']==dg and atk['normal_damage']==sum(map(sum,dg))+p['damage_flat']
   v=0
   if resp!='NONE':
    assert st['actors'][target]['resource']['reaction']==1
    r=acts[0];assert r['by']==target and r['consumes_reaction'] and r['seq']==1
    st['actors'][target]['resource']['reaction']=0;v=1
    if resp=='COUNTER':
     assert r['action']=='COUNTER_DECLARE' and r['against']==a and r['attack_origin']=='NORMAL'
     cnt['counter_declarations']+=1
    else:
     assert r['action']==resp and r['attack_score']==score and r['source']=='ATTACK_DECLARED'
     d=st['actors'][target]['resource'];defense=d['ca']+d['reflex'] if resp=='ESQUIVAR' else 6+d['constitution']+d['armor']+d['fortitude']
     assert str(defense)==r['defense_exact'] and r['damage_negated']==(score<=defense)
     cnt[resp.lower()]+=1
   normal=acts[v];assert normal['action']=='weapon_attack' and normal['from']==a and normal['to']==target
   critical=(crit[:2]==[6,6] and crit[2]>=5)
   hit=score>st['actors'][target]['resource']['ca'] or critical
   assert normal['hit']==hit and normal['roll_score']==score and normal['critical']==('POSITIVE' if critical else 'NONE')
   actual_r=st['actors'][target]['resource'];base=atk['normal_damage']+sum(n*f for n,f in p['damage_dice'])*(1 if critical else 0)
   assert normal['critical_max_bonus']==(sum(n*f for n,f in p['damage_dice']) if critical else 0)
   negated=acts[0].get('damage_negated') if resp in ('DEFENDER','ESQUIVAR') else False
   effective=max(0,base-st['actors'][target]['source_profile']['rd']) if hit and not negated else 0
   assert normal['before_hp']==actual_r['hp'] and normal['net']==effective
   assert normal['after_hp']==max(0,actual_r['hp']-effective) and normal['hp_loss_actual']==actual_r['hp']-normal['after_hp']
   actual_r['hp']=normal['after_hp'];st['actors'][a]['resource']['standard']=0;st['action_nonce'][a]+=1
   cnt['normal_attacks']+=1;cnt['criticals']+=int(critical)
   if resp=='COUNTER':
    assert len(acts)==3;reply=acts[2]
    if hit:
     assert reply['action']=='COUNTER_NO_RESPONSE' and reply['incoming_hit'] and reply['reaction_already_consumed']
     cnt['counter_no_response']+=1
    else:
     assert reply['action']=='COUNTER_RESPONSE' and reply['attack_origin']=='COUNTER' and reply['R51_nested_counter_enabled'] is False
     who=target;tgt=a;cn=st['action_nonce'][who]+1;info=st['actors'][who]['source_profile']
     c=payload['counter'];assert c['nonce']==cn
     assert c['crit']==[oracle(st['seed'],cn,who,f'COUNTER-CRIT-{j}',1,6)[0] for j in range(3)]
     ah=[oracle(st['seed'],cn,who,f'COUNTER-HIT-{j}',info['attack_dice'],6) for j in range(2)]
     assert c['hit_rolls']==ah and reply['advantage_rolls']==ah
     cscore=max(map(sum,ah))+info['attack_flat']+2
     assert reply['roll_score']==cscore
     dmg=[oracle(st['seed'],cn,who,f'COUNTER-DMG-{j}',z,f) for j,(z,f) in enumerate(info['damage_dice'])]
     assert c['dmg_rolls']==dmg
     rcrit=c['crit'][:2]==[6,6] and c['crit'][2]>=5
     rhit=cscore>st['actors'][tgt]['resource']['ca'] or rcrit
     assert reply['hit']==rhit
     nraw=sum(map(sum,dmg))+info['damage_flat']+(sum(z*f for z,f in info['damage_dice']) if rcrit else 0)
     net=max(0,nraw-st['actors'][tgt]['source_profile']['rd']) if rhit else 0
     assert reply['net']==net
     assert reply['before_hp']==st['actors'][tgt]['resource']['hp']
     assert reply['after_hp']==max(0,reply['before_hp']-net)
     st['actors'][tgt]['resource']['hp']=reply['after_hp'];st['action_nonce'][who]+=1
     cnt['counter_response']+=1;cnt['no_reaction_chain']+=1
   else:assert len(acts)==v+1
  elif kind=='END':
   assert len(acts)==1 and acts[0]['action']=='turn_end' and acts[0]['by']==a
   assert st['actors'][a]['resource']['standard']==0
   st['turn_index']+=1
   if all(st['actors'][z]['resource']['hp']<=0 for z in st['teams'] if st['teams'][z]=='ONE'):
    st['phase']='FINISHED';st['winner']='TWO';st['active']=None
   elif all(st['actors'][z]['resource']['hp']<=0 for z in st['teams'] if st['teams'][z]=='TWO'):
    st['phase']='FINISHED';st['winner']='ONE';st['active']=None
   else:
    current=st['order'].index(a)
    for k in range(1,len(st['order'])+1):
     j=(current+k)%len(st['order']);nxt=st['order'][j]
     if st['actors'][nxt]['resource']['hp']>0:
      st['active']=nxt
      if j<=current:st['round']+=1
      break
    assert st['active'] is not None
   assert e['detail']['extra']['next_actor']==st['active']
   cnt['ko']=sum(v['resource']['hp']==0 for v in st['actors'].values())
  assert sha(st)==e['after_sha'],(file.name,ix,'after_mismatch',kind)
  head=sha(e);cnt['event']+=1
 assert head==meta['head'] and canon(st)==meta['state']
 assert st['phase'] in ('FINISHED','ACTIVE') and (st['winner']=='ONE' if st['phase']=='FINISHED' else st['winner'] is None)
 return {'db':file.name,'status':'PASS_COLD_NO_ENGINE_IMPORT','events':len(rows),'pending':pending,
     'counts':cnt,'winner':st['winner'],'last_head':head,'round':st['round']}

if __name__=='__main__':
 result=[cold(p) for p in sorted((ROOT/'runs').glob('R119*.sqlite')) if '.checkpoint' not in p.stem]
 out={'auditor':'standard_library_no_vlab_import','results':result,'status':'PASS',
      'totals':{k:sum(v['counts'][k] for v in result) for k in result[0]['counts']}}
 (ROOT/'R120_COLD_AUDIT.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(out,indent=2,ensure_ascii=False))
