"""R210 independently validates two-center native R18 journals. READ ONLY, imports no combat engine.
R210 executes NEW fights; this verifies journal causality, not canonical power balance.
"""
from pathlib import Path
import sqlite3,json,hashlib,collections,math
ROOT=Path(__file__).resolve().parents[1]
PRE=json.loads((ROOT/'source/R210_SPORES_CENTERS_PREREG.json').read_text())
PHASH=hashlib.sha256((ROOT/'source/R210_SPORES_CENTERS_PREREG.json').read_bytes()).hexdigest()
E='ERISTAN_ON5_SPORES';B1='DRACOLION_SPORES_A';B2='DRACOLION_SPORES_B';TRIO=(E,B1,B2)

def canon(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def digest(x):return hashlib.sha256(canon(x).encode()).hexdigest()
def included(center,who):
 p=PRE['positions_m'][who];d2=sum((p[i]-center[i])**2 for i in (0,1))
 return d2 <= PRE['spell']['radius_m']**2,d2

def audit(dbfile):
 db=sqlite3.connect('file:'+str(dbfile)+'?mode=ro',uri=True)
 try:
  meta=dict(db.execute('SELECT key,value FROM meta'))
  rows=list(db.execute('SELECT seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha FROM events ORDER BY seq'))
  assert meta['mode']=='EXPERIMENTAL_LAB_ONLY' and not list(db.execute('SELECT * FROM pending'))
  assert len(rows)==int(meta['revision']) and rows
  st=json.loads(meta['state']);r=st['r210'];seed=st['seed'];pol=r['policy']
  assert seed in PRE['seeds'] and pol in PRE['policies']
  assert r['prereg_sha']==PHASH and set(st['actors'])==set(TRIO)
  assert r['source']==PRE['source'] and r['source_status']==PRE['source_status']
  prev=meta['genesis'];last_after=None;evs=[]
  for seq,cmd,back,record,row_sha,before,after in rows:
   row=json.loads(record)
   assert row['seq']==seq and row['cmd_id']==cmd and row['prev']==back==prev
   assert digest(row)==row_sha and row['before_sha']==before and row['after_sha']==after
   assert row['official_effects']==0 and row['synthetic'] is True
   if last_after is not None:assert before==last_after
   evs+=row['detail'].get('events_added',row['detail'].get('new_native_events',[]))
   prev=row_sha;last_after=after
  assert prev==meta['head'] and last_after==digest(st)
  assert evs==st['native_events'] and [v['seq'] for v in evs]==list(range(1,len(evs)+1))
  hp={w:PRE['actors'][w]['hp'] for w in TRIO};pa=PRE['actors'][E]['pa_free']
  casts=[];effects=[];attacks=[];pending=None
  for ev in evs:
   ac=ev['action']
   if pending is not None and ac!='r210_area_target':raise AssertionError('MULTI_TARGET_NOT_ATOMIC')
   if ac=='weapon_attack':
    assert ev['from'] in (B1,B2) and ev['to']==E and ev['before_hp']==hp[E]
    assert len(ev['damage_roll_groups'])==1 and len(ev['damage_roll_groups'][0])==9
    assert all(isinstance(v,int) and 1<=v<=6 for v in ev['damage_roll_groups'][0])
    assert ev['normal_damage']==sum(ev['damage_roll_groups'][0])
    assert ev['ca_exact']=='76'
    assert ev['hp_loss_actual']==min(hp[E],ev['net'])
    assert ev['after_hp']==hp[E]-ev['hp_loss_actual']
    hp[E]=ev['after_hp'];attacks.append(ev)
   elif ac=='r210_area_cast':
    center=PRE['centers_m'][pol]
    assert ev['by']==E and ev['policy']==pol and ev['source']==PRE['source']
    assert ev['action_economy']=='STANDARD' and ev['pa_spent']==80
    assert ev['pa_before']==pa and ev['pa_after']==pa-80
    assert ev['center_m']==center and ev['radius_m']==5 and ev['center_max_m']==25
    assert math.dist(center,PRE['positions_m'][E])<=25
    expected={w for w in TRIO if included(center,w)[0]}
    assert set(ev['in_area'])==expected and len(ev['in_area'])==len(expected)
    assert set(ev['out_of_area'])==set(TRIO)-expected
    assert expected==set(TRIO) if pol=='EXPOSED_CENTER' else expected=={B1,B2}
    assert len(ev['cast_roll_10d10'])==10
    assert all(isinstance(v,int) and 1<=v<=10 for v in ev['cast_roll_10d10'])
    assert ev['common_roll_total']==sum(ev['cast_roll_10d10'])+10
    casts.append(ev);pa-=80
    pending={'cast':ev,'targets':set(expected)}
   elif ac=='r210_area_target':
    assert pending is not None and ev['cast_event_seq']==pending['cast']['seq']
    who=ev['target'];assert who in pending['targets'];pending['targets'].remove(who)
    assert ev['source']==PRE['source'] and ev['by']==E and ev['position_m']==PRE['positions_m'][who]
    inside,d2=included(PRE['centers_m'][pol],who)
    assert inside and abs(ev['distance_squared_to_center']-d2)<1e-9
    assert ev['radius_squared']==25
    cfg=PRE['actors'][who];n,faces=cfg['fortitude_dice']
    assert ev['save_name']=='Fortitude' and len(ev['save_dice'])==n==ev['save_dice_n']
    assert all(isinstance(v,int) and 1<=v<=faces for v in ev['save_dice'])
    assert ev['save_attribute_con']==cfg['CON'] and ev['save_total']==sum(ev['save_dice'])+cfg['CON']
    assert ev['CD']==76 and ev['save_success']==(ev['save_total']>76)
    assert not ev['save_success'],'UNTESTED_SUCCESS_GATE_IN_CURRENT_COHORT'
    assert ev['damage_type']=='PLANTA' and ev['critical']=='NOT_APPLICABLE_MAGIA'
    assert ev['damage_raw']==pending['cast']['common_roll_total']
    assert ev['rd_magic_applied']==0 and ev['damage_after_rd']==ev['damage_raw']
    assert ev['hp_before']==hp[who]
    assert ev['hp_loss_actual']==min(hp[who],ev['damage_after_rd'])
    assert ev['overkill']==max(0,ev['damage_after_rd']-hp[who])
    assert ev['hp_after']==hp[who]-ev['hp_loss_actual']
    assert ev['self_target']==(who==E) and ev['shared_cast_roll']==pending['cast']['cast_roll_10d10']
    hp[who]=ev['hp_after'];effects.append(ev)
    if not pending['targets']:pending=None
   elif ac=='r210_pass':
    assert ev['by']==E and ev['pa_spent']==0
  assert pending is None
  assert {w:st['actors'][w]['resource']['hp'] for w in TRIO}==hp
  assert st['actors'][E]['resource']['pa']==pa
  assert r['spell_casts']==len(casts) and r['pa_paid']==80*len(casts)==804-pa
  assert r['targets_resolved']==len(effects)==len(casts)*(3 if pol=='EXPOSED_CENTER' else 2)
  assert r['total_effective']==sum(ev['hp_loss_actual'] for ev in effects)
  assert r['total_raw']==sum(ev['damage_raw'] for ev in effects)
  assert r['self_damage']==sum(ev['hp_loss_actual'] for ev in effects if ev['self_target'])
  assert r['beast_damage']==sum(ev['hp_loss_actual'] for ev in effects if not ev['self_target'])
  assert st['metrics']['attempts']==len(attacks)
  assert (r['self_damage']>0 if pol=='EXPOSED_CENTER' else r['self_damage']==0)
  if hp[E]==0:assert st['phase']=='FINISHED' and st['winner']=='BEAST_SIDE'
  else:assert st['phase']=='ACTIVE' and st['winner'] is None
  assert len({ev['cast_event_seq'] for ev in effects})==len(casts)
  return {'run_id':dbfile.stem,'seed':seed,'policy':pol,'commits':len(rows),'events':len(evs),
   'attacks':len(attacks),'casts':len(casts),'target_events':len(effects),'PA_spent':804-pa,
   'magic_effective':r['total_effective'],'self_damage':r['self_damage'],'beast_damage':r['beast_damage'],
   'status':'KO' if hp[E]==0 else 'CENSORED_HORIZON','HP':hp,'head':meta['head'],
   'beast_target_rolls':{w:[ev['shared_cast_roll'] for ev in effects if ev['target']==w] for w in (B1,B2)},
   'save_rolls':{w:[ev['save_dice'] for ev in effects if ev['target']==w] for w in TRIO},
   'spell_common_rolls':[ev['cast_roll_10d10'] for ev in casts],
   'attack_tapes':{w:[{'normal':ev['normal_damage'],'score':ev['roll_score'],'rolls':ev['damage_roll_groups']}
        for ev in attacks if ev['from']==w] for w in (B1,B2)}}
 finally:db.close()

def main():
 dbs=sorted((ROOT/'evidence/db').glob('R210_CENTER_SPORES_S*.sqlite'))
 got=[audit(p) for p in dbs]
 assert len(got)==len({x['run_id'] for x in got})
 results=json.loads((ROOT/'evidence/R210_COMBAT_RESULTS.json').read_text())
 ref={x['run_id']:x for x in results if 'db' in x}
 for x in got:
  y=ref[x['run_id']]
  for a,b in [('commits','commits'),('events','events'),('attacks','attacks'),('casts','casts'),('target_events','area_target_events'),('PA_spent','pa_spent'),('magic_effective','magic_effective'),('self_damage','self_damage'),('beast_damage','beast_damage'),('status','status'),('HP','final_hp')]:
   assert x[a]==y[b],(x['run_id'],a,x[a],y[b])
 groups=collections.defaultdict(dict)
 for x in got:groups[x['seed']][x['policy']]=x
 assert all(set(g)==set(PRE['policies']) for g in groups.values())
 assert len(results)==2*len(PRE['seeds'])
 blocked=[x for x in results if x['status']=='PRECOMMIT_INIT_TIE_HOLD']
 assert all(x['seed'] not in groups for x in blocked)
 pairing=[]
 for seed,g in groups.items():
  exposed=g['EXPOSED_CENTER'];safe=g['SAFE_CENTER']
  for w in (B1,B2):
   a=exposed['beast_target_rolls'][w];b=safe['beast_target_rolls'][w]
   assert a[:min(len(a),len(b))]==b[:min(len(a),len(b))], 'TARGET_RNG_NOT_PAIRED'
   q=exposed['save_rolls'][w];z=safe['save_rolls'][w]
   assert q[:min(len(q),len(z))]==z[:min(len(q),len(z))], 'SAVE_RNG_NOT_PAIRED'
  a=exposed['spell_common_rolls'];b=safe['spell_common_rolls']
  assert a[:min(len(a),len(b))]==b[:min(len(a),len(b))], 'SPELL_RNG_NOT_PAIRED'
  for w in (B1,B2):
   a=exposed['attack_tapes'][w];b=safe['attack_tapes'][w]
   assert a[:min(len(a),len(b))]==b[:min(len(a),len(b))],'PHYSICAL_RNG_DRIFT'
  pairing.append({'seed':seed,'self_hp_exposed':exposed['HP'][E],'self_hp_safe':safe['HP'][E],
   'self_damage_exposed':exposed['self_damage'],'self_damage_safe':safe['self_damage'],
   'beasts_damage_exposed':exposed['beast_damage'],'beasts_damage_safe':safe['beast_damage'],
   'KO_exposed':exposed['status']=='KO','KO_safe':safe['status']=='KO'})
 aggregate={k:sum(x[k] for x in got) for k in ('commits','events','attacks','casts','target_events','PA_spent','magic_effective','self_damage','beast_damage')}
 report={'audit':'PASS_R210_INDEPENDENT_R18_TWO_CENTERS_GEOMETRY_CAUSAL_PAIRING',
  'last_baseline':'PASS_R209_COLD_PORTABLE_RECOVERY','prereg_sha256':PHASH,
  'seed_candidates':len(PRE['seeds']),'seed_pairs_admitted':len(groups),'combat_runs':len(got),
  'blocked_precommit_arms':len(blocked),'KO':sum(x['status']=='KO' for x in got),
  'censored':sum(x['status']=='CENSORED_HORIZON' for x in got),'totals':aggregate,'pairing':pairing,
  'source_grade':'NPC_PROPOSTO;_BEAST_RANK_CONFLICT;_MAGIC_RD_ZERO_TEST_ONLY',
  'save_success_events':0,'half_rounding':'HOLD_UNKNOWN_EFFECT_IF_SUCCESS_ODD',
  'combat_reexecutions_during_audit':0,'production':'HOLD','canonical_contracts':'0/17','historical_cells':'0/1875'}
 p=ROOT/'evidence/R210_INDEPENDENT_AUDIT.json';p.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(report,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
