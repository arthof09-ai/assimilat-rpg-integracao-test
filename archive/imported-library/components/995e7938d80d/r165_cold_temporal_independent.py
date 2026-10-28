"""Independent stdlib causal audit of R165 V3 explicit duration. No resolver import, no ledger writes."""
import json,sqlite3,hashlib,random,copy
from pathlib import Path
from fractions import Fraction
HERE=Path(__file__).parent
R18='VLAB-R18-INTERACTIVE-CLI-0.1-EXPERIMENTAL'
def can(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def sha(x):return hashlib.sha256(can(x).encode()).hexdigest()
def roll(seed,who,tag,nonce,n,f):
 d=hashlib.sha256(f'{seed}|{nonce}|R165-{who}-{tag}|{n}d{f}|{R18}'.encode()).digest();rng=random.Random(int.from_bytes(d,'big'));return [rng.randint(1,f) for _ in range(n)]
def check(t,msg):
 if not t:raise AssertionError(msg)
def audit(db):
 st=json.loads(db.with_suffix('.genesis.json').read_text());seed=st['seed'];initial=copy.deepcopy(st)
 con=sqlite3.connect(f'file:{db.as_posix()}?mode=ro',uri=True)
 meta=dict(con.execute('select key,value from meta'));rows=[(seq,json.loads(r),rsha) for seq,r,rsha in con.execute('select seq,row_json,row_sha from events order by seq')]
 assert len(rows)==7 and con.execute('select count(*) from pending').fetchone()[0]==0
 assert con.execute('pragma integrity_check').fetchone()[0]=='ok';con.close()
 assert [r['kind'] for _,r,_ in rows]==['START','FLECHA','END','START','MOVE','STRIKE','END']
 prev=meta['genesis'];damage=0;pa=0
 for seq,row,rhash in rows:
  assert seq==row['seq'] and row['prev']==prev and rhash==sha(row)
  assert row['before_sha']==sha(st)
  kind=row['kind'];p=row['payload'];a=st['active'];ev=row['detail']['native_actions'];ra=st['actors'][a]['resource']
  if kind=='START':
   assert ra['standard']==0 and p=={'actor':a}
   assert ev[0]['action']=='turn_start' and ev[0]['by']==a
   if a=='A':
    assert ra['base_speed']==16 and ra['timed_source_speed_penalty_m']==6 and ev[0]['speed']=='10'
   ra.update(standard=1,movement=1,reaction=1)
  elif kind in ('FLECHA','STRIKE'):
   target='A' if a=='I' else 'I';rt=st['actors'][target]['resource'];t=p['tape']
   assert t['who']==a and t['nonce']==st['action_nonce'][a]+1
   cfg=(4,89,8,10,33,35) if a=='I' else (6,193,8,8,211,25)
   diceN,attackbonus,damagen,damagefaces,damageflat,rd=cfg;prefix='FLECHA' if a=='I' else 'LANCE'
   crit=[roll(seed,a,f'{prefix}-CRIT-{j}',t['nonce'],1,6)[0] for j in range(3)]
   hit_roll=roll(seed,a,prefix+'-HIT',t['nonce'],diceN,6)
   dmg_roll=roll(seed,a,f'{prefix}-DAMAGE-0',t['nonce'],damagen,damagefaces)
   assert t['crit']==crit and t['hit']==[hit_roll] and t['dmg_rolls']==[dmg_roll]
   positive=crit[:2]==[6,6] and crit[2]>=5
   negative=crit[:2]==[1,1] and crit[2]<=2
   score=sum(hit_roll)+attackbonus
   hit=(score>rt['ca'] or positive) and not negative
   raw=sum(dmg_roll)+damageflat+damagen*damagefaces*int(positive) if hit else 0
   net=max(0,raw-rd) if hit else 0
   actual=min(net,rt['hp'])
   assert t['score']==score and t['damage']==sum(dmg_roll)+damageflat
   e=ev[0];assert e['action']=='weapon_attack' and e['from']==a and e['to']==target
   assert e['critical']==('POSITIVE' if positive else 'NEGATIVE' if negative else 'NONE')
   assert e['raw']==raw and e['net']==net and e['rd_applied']==(rd if hit else 0)
   assert e['before_hp']==rt['hp'] and e['after_hp']==rt['hp']-actual and e['hp_loss_actual']==actual
   ra['standard']=0;rt['hp']-=actual;damage+=actual;st['action_nonce'][a]+=1
   if kind=='FLECHA':
    assert positive and hit and len(ev)==2 and ra['pa']>=55
    effect=ev[1];assert effect['action']=='FLECHA_TRAVA_SOURCE_POST_HIT'
    assert effect['speed_delta_m']==-6 and effect['duration_until']=='END_OF_TARGET_NEXT_OWN_TURN' and effect['pa_spent']==55
    assert p['distance_m']==10 and target=='A' and rt['base_speed']==16
    ra['pa']-=55;pa+=55;rt['timed_source_speed_penalty_m']=6
    st['temporal_status']['A']='ACTIVE_UNTIL_END_OF_A_NEXT_TURN'
   else:assert len(ev)==1 and p['distance_m']==1 and st['actors']['A']['resource']['position']=='X9'
  elif kind=='MOVE':
   assert a=='A' and ra['timed_source_speed_penalty_m']==6 and ra['base_speed']==16
   assert p['distance_m']==9 and ra['movement']==1 and ra['position']=='X0'
   assert ev[0]['action']=='move' and ev[0]['speed']=='10' and ev[0]['travel_cost']=='9'
   assert ev[0]['to']=='X9' and ev[0]['path_proof']=='R165_METRIC_10M_TO_1M_NOT_TOPOLOGY_SCALE'
   ra['position']='X9';ra['movement']=0
  elif kind=='END':
   assert ra['standard']==0 and p=={'actor':a} and ev[0]['action']=='turn_end'
   st['turn_index']+=1
   if a=='I':assert len(ev)==1;st['active']='A'
   else:
    assert len(ev)==2 and ev[1]['action']=='FLECHA_TRAVA_EXPIRES' and ev[1]['speed_before']=='10' and ev[1]['speed_after']=='16'
    ra['timed_source_speed_penalty_m']=0;st['temporal_status']['A']='EXPIRED_AT_END_OF_TARGET_NEXT_OWN_TURN';st['active']=None;st['phase']='ENDED_EXPLICIT_TEMPORAL_AFTER_A_TURN'
  else:raise AssertionError('unknown '+kind)
  assert row['after_sha']==sha(st),(seq,kind,'FULL_CAUSAL_POSTSTATE')
  prev=rhash
 assert prev==meta['head'] and can(st)==can(json.loads(meta['state'])) and damage>0
 return {'run':db.stem,'PASS':True,'commits':len(rows),'actual_HP_loss':damage,'PA':pa,'documented_end_of_next_own_turn_applied':True,'source_expiration_Casulo':'HOLD','final_state_sha':sha(st),'root_sha':prev}
if __name__=='__main__':
 p=next(x for x in (HERE/'runs').glob('R165_FLECHA_TURN_EXPLICIT_V3_DEV_*.sqlite') if '.checkpoint.' not in x.name)
 r=audit(p)
 (HERE/'R165_COLD_TEMPORAL_AUDIT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(r,ensure_ascii=False,indent=2))
