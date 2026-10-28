"""Independent R211 SQLite-only auditor; imports neither R211 runner nor native combat resolver."""
from pathlib import Path
import sqlite3,hashlib,json,collections,math
ROOT=Path(__file__).resolve().parents[1]
PRE=json.loads((ROOT/'source/R211_DYNAMIC_CENTER_PREREG.json').read_text())
SHA=hashlib.sha256((ROOT/'source/R211_DYNAMIC_CENTER_PREREG.json').read_bytes()).hexdigest()
E='ERISTAN_ON5_SPORES';A='DRACOLION_SPORES_A';B='DRACOLION_SPORES_B';ACT=(E,A,B)
def canon(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def dig(x):return hashlib.sha256(canon(x).encode()).hexdigest()
def d2(a,b):return sum((a[i]-b[i])**2 for i in (0,1))
def legal_centers(pos,hp):
 out=[]
 for center in PRE['center_candidates_m']:
  if d2(center,pos[E])>625:continue
  included=[w for w in ACT if hp[w]>0 and d2(center,pos[w])<=25]
  enemies=[w for w in included if w in (A,B)]
  score=[len(enemies),-int(E in included),-sum(d2(center,pos[w]) for w in enemies)]
  out.append({'center':center,'in':included,'enemy':enemies,'self_risk':int(E in included),'score':score})
 return out
def choose(candidates,pol):
 if pol=='FIXED':return next(x for x in candidates if x['center']==[8,0])
 return sorted(candidates,key=lambda x:(-x['score'][0],-x['score'][1],-x['score'][2],tuple(x['center'])))[0]
def audit(p):
 c=sqlite3.connect('file:'+str(p)+'?mode=ro',uri=True)
 try:
  meta=dict(c.execute('select key,value from meta'))
  rows=list(c.execute('select seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha from events order by seq'))
  assert meta['mode']=='EXPERIMENTAL_LAB_ONLY' and not list(c.execute('select * from pending'))
  assert rows and len(rows)==int(meta['revision'])
  st=json.loads(meta['state']);pol=st['r211']['policy'];seed=st['seed']
  assert pol in PRE['policies'] and seed in PRE['seeds'] and st['r211']['prereg_sha']==SHA
  assert set(st['actors'])==set(ACT)
  prev=meta['genesis'];last=None;evs=[]
  for seq,cmd,back,raw,row_sha,before,after in rows:
   row=json.loads(raw)
   assert seq==row['seq'] and cmd==row['cmd_id'] and back==prev==row['prev']
   assert row_sha==dig(row) and before==row['before_sha'] and after==row['after_sha']
   assert row['official_effects']==0 and row['synthetic'] is True
   if last is not None:assert before==last
   evs+=row['detail'].get('events_added',row['detail'].get('new_native_events',[]))
   prev=row_sha;last=after
  assert prev==meta['head'] and last==dig(st)
  assert evs==st['native_events'] and [x['seq'] for x in evs]==list(range(1,len(evs)+1))
  pos={k:v[:] for k,v in PRE['position_start_m'].items()}
  hp={E:630,A:1104,B:1104};pa=804;turn_by={k:0 for k in ACT};moves=[];casts=[];targets=[];decisions=[]
  last_decision=None;last_cast=None;cast_targets=[]
  for ev in evs:
   typ=ev['action']
   if typ=='turn_start':turn_by[ev['by']]+=1
   if typ=='move':
    assert ev['by']==A and ev['from']==str(tuple(pos[A]))
    expected=PRE['patrol_own_turn_odd_to'] if turn_by[A]%2 else PRE['patrol_own_turn_even_to']
    assert ev['to']==str(tuple(expected))
    step=math.dist(pos[A],expected)
    assert abs(float(ev['travel_cost'])-step)<1e-9 and step<=27 and ev['speed']=='27'
    assert ev['path_proof'].startswith('R211_PRESET_OPEN_STRAIGHT_X8_')
    assert pos[A][0]==expected[0]==8 and min(d2(pos[A],pos[E]),d2(expected,pos[E]))>=64
    pos[A]=expected[:];moves.append(ev)
   if typ=='r211_path_no_aoo':
    assert ev['safe_min_distance_to_enemy_m']==8 and ev['trigger']=='NO_ADJACENT_BLOCK_EXIT'
   if typ=='r211_center_decision':
    assert ev['by']==E and ev['policy']==pol and ev['state_positions_m']==pos
    legal=legal_centers(pos,hp);picked=choose(legal,pol)
    assert ev['centers_evaluated']==legal
    assert ev['center_chosen_m']==picked['center'] and ev['eligible_targets']==picked['in']
    assert set(ev['excluded_targets'])==set(ACT)-set(picked['in'])
    assert E not in picked['in'] and ev['rng_not_observed']=='NO_FUTURE_DAMAGE_OR_SAVES_READ'
    last_decision=ev;decisions.append(ev)
   if typ=='r211_area_cast':
    assert last_decision is not None and ev['cast_event_seq']==last_decision['seq']
    assert ev['center_m']==last_decision['center_chosen_m'] and ev['action_economy']=='STANDARD'
    assert ev['pa_before']==pa and ev['pa_after']==pa-80 and ev['pa_cost']==80
    assert len(ev['common_roll'])==10 and all(1<=n<=10 for n in ev['common_roll'])
    assert ev['raw_spell_damage']==sum(ev['common_roll'])+10
    pa-=80;casts.append(ev);last_cast=ev;cast_targets=[]
   if typ=='r211_area_target':
    assert last_cast is not None and ev['cast_seq']==last_cast['seq']
    who=ev['target'];assert who in last_decision['eligible_targets'] and who not in cast_targets
    assert ev['position_m']==pos[who] and ev['distance2_to_center']==d2(last_cast['center_m'],pos[who])<=25
    assert ev['save_total']==sum(ev['save_dice'])+ev['save_attribute_pure']
    assert ev['save_cd']==76 and not ev['save_success']
    assert ev['damage_raw']==last_cast['raw_spell_damage'] and ev['damage_post_rd']==ev['damage_raw'] and ev['rd_magic']==0
    assert ev['hp_before']==hp[who] and ev['hp_effective']==min(hp[who],ev['damage_post_rd'])
    assert ev['hp_after']==max(0,hp[who]-ev['damage_post_rd'])
    assert ev['overkill']==max(0,ev['damage_post_rd']-hp[who]);hp[who]=ev['hp_after']
    cast_targets.append(who);targets.append(ev)
    if len(cast_targets)==last_cast['target_count']:
     assert set(cast_targets)==set(last_decision['eligible_targets']);last_cast=None;last_decision=None
  assert last_cast is None and last_decision is None
  assert st['r211']['positions_m']==pos
  assert {k:st['actors'][k]['resource']['hp'] for k in ACT}==hp
  assert st['actors'][E]['resource']['pa']==pa
  assert st['r211']['movements']==len(moves) and st['r211']['casts']==len(casts) and st['r211']['targets']==len(targets)
  assert st['r211']['PA_cast']==len(casts)*80==804-pa
  assert st['r211']['beast_damage']==sum(x['hp_effective'] for x in targets if x['target'] in (A,B))
  assert st['r211']['self_damage']==0 and all(x['target']!=E for x in targets)
  assert st['r211']['magic_effective']==sum(x['hp_effective'] for x in targets)
  assert all(x['resource']['movement'] in (0,1) and x['resource']['standard'] in (0,1) for x in st['actors'].values())
  assert st['phase']=='ACTIVE' and st['winner'] is None # censored, not victory
  return {'run_id':p.stem,'seed':seed,'policy':pol,'events':len(evs),'commits':len(rows),'moves':len(moves),'casts':len(casts),'targets':len(targets),
          'pa':804-pa,'enemy_hp_loss':sum(x['hp_effective'] for x in targets if x['target'] in (A,B)),
          'centers':[x['center_chosen_m'] for x in decisions],'initiative':st.get('initiative_receipt'),
          'rolls':{(int(x['turn']),x['center_chosen_m'][1]):[] for x in decisions},
          'casts_dice':[x['common_roll'] for x in casts], 'head':meta['head']}
 finally:c.close()
def main():
 files=sorted((ROOT/'evidence/db').glob('R211_DYN_AOE_S*.sqlite'));got=[audit(p) for p in files]
 results=json.loads((ROOT/'evidence/R211_COMBAT_RESULTS.json').read_text());ref={x['run_id']:x for x in results if 'db' in x}
 assert len(got)==len(results)==len(ref) and len({x['run_id'] for x in got})==len(got)
 for x in got:
  r=ref[x['run_id']]
  for a,b in [('events','events'),('commits','rev'),('moves','moves'),('casts','casts'),('targets','targets'),('pa','PA_spent'),('enemy_hp_loss','beast_hp_effective'),('centers','centers')]:assert x[a]==r[b],(a,x['run_id'])
 pairs=collections.defaultdict(dict)
 for x in got:pairs[x['seed']][x['policy']]=x
 assert len(pairs)==len(PRE['seeds']) and all(set(z)==set(PRE['policies']) for z in pairs.values())
 for seed,g in pairs.items():
  a,b=g['FIXED'],g['ADAPTIVE']
  assert a['moves']==b['moves']==3 and a['casts']==b['casts']==3
  assert a['centers']==[[8,0],[8,0],[8,0]]
  assert b['centers']==[[8,4],[8,0],[8,4]]
  assert a['targets']==4 and b['targets']==6
  assert a['casts_dice']==b['casts_dice'] # keyed RNG as intended
  assert b['enemy_hp_loss']>=a['enemy_hp_loss']
 report={'audit':'PASS_R211_INDEPENDENT_R18_NATIVE_MOVEMENT_DYNAMIC_CENTER_CAUSAL_SQLITE',
  'preregister_sha256':SHA,'seeds':len(pairs),'runs':len(got),
  'commits':sum(x['commits'] for x in got),'events':sum(x['events'] for x in got),
  'moves':sum(x['moves'] for x in got),'casts':sum(x['casts'] for x in got),'targets':sum(x['targets'] for x in got),
  'PA':sum(x['pa'] for x in got),'fixed_targets':sum(z['FIXED']['targets'] for z in pairs.values()),
  'adaptive_targets':sum(z['ADAPTIVE']['targets'] for z in pairs.values()),
  'fixed_beast_hp_loss':sum(z['FIXED']['enemy_hp_loss'] for z in pairs.values()),
  'adaptive_beast_hp_loss':sum(z['ADAPTIVE']['enemy_hp_loss'] for z in pairs.values()),
  'censored':len(got),'KO':0,'rolls_paired':'IDENTICAL_CAST_TAPES_ON_COMMON_OWN_TURNS',
  'strength':'STATE_CHANGES_NATIVE_SCHEDULER_COMMIT_AND_ADAPTIVE_CENTER_CHANGES, ATTACKS_NONE_IN_THIS_TEST',
  'source_limitations':PRE['limits'],
  'canonical':{'terminal_contracts':'0/17','historical_cells':'0/1875','production':'HOLD'},
  'historic_combat_replays':0}
 (ROOT/'evidence/R211_INDEPENDENT_AUDIT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(report,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
