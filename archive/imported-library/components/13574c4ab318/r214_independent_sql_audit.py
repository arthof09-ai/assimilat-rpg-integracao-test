"""Independent READ-ONLY R214 SQL/JSON validator: NO import of combat engine or runner.
Checks R18 chain, native causality, resource conservation, R49 priority, and bilateral two-sided turns.
"""
import json,hashlib,sqlite3,sys,collections
from pathlib import Path
R=Path(__file__).resolve().parents[1]
PRE=json.loads((R/'sources/R214_PREREG.json').read_text()); PH=hashlib.sha256((R/'sources/R214_PREREG.json').read_bytes()).hexdigest()
SOURCE=json.loads((R/'sources/R44_R46_FROZEN_MASTER_SOURCE.json').read_text())['sources']

def canon(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def sha(x):return hashlib.sha256(canon(x).encode()).hexdigest()
def scan(db):
 c=sqlite3.connect('file:'+str(db)+'?mode=ro',uri=True)
 try:
  meta=dict(c.execute('SELECT key,value FROM meta'));rows=c.execute('SELECT seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha FROM events ORDER BY seq').fetchall()
  assert meta['mode']=='EXPERIMENTAL_LAB_ONLY'
  assert c.execute('SELECT count(*) FROM pending').fetchone()[0]==0,'pending nonzero'
  assert len(rows)==int(meta['revision'])
  state=json.loads(meta['state']);prev=meta['genesis'];prev_state=None
  for idx,cmd,p,row_json,row_sha,before_hash,after_hash in rows:
   record=json.loads(row_json)
   assert idx==record['seq'] and cmd==record['cmd_id'] and p==prev and record['prev']==prev
   assert sha(record)==row_sha and record['before_sha']==before_hash and record['after_sha']==after_hash
   assert prev_state is None or before_hash==prev_state
   assert record['synthetic']==True and record['official_effects']==0
   prev=row_sha;prev_state=after_hash
  assert prev==meta['head'] and (prev_state is None or prev_state==sha(state))
  assert state['scene']==meta['scene'] and state['synthetic']==True
  ev=state['native_events'];assert [x['seq'] for x in ev]==list(range(1,len(ev)+1))
  assert all(x['provenance']=='R214-TEST-CONDITIONAL' for x in ev)
  counters=collections.Counter(x['action'] for x in ev)
  intents=[x for x in ev if x['action']=='opportunity_reaction_reserved']
  attacks=[x for x in ev if x['action']=='weapon_attack']
  aoos=[x for x in attacks if x['attack_origin']=='OPPORTUNITY']
  rng=[x for x in ev if x['action']=='r214_offensive_rng_generated']
  assert len(rng)==len(attacks)
  for atk in attacks:
   if atk['hit']:
    assert atk['net']==max(0,atk['raw']-atk['rd_applied'])
   else:assert atk['net']==0 and atk['raw']==0
   assert atk['hp_loss_actual']==atk['before_hp']-atk['after_hp']==min(atk['before_hp'],atk['net'])
   assert atk['overkill']==max(0,atk['net']-atk['before_hp'])
   assert atk['after_hp']>=0
   rr=[x for x in rng if x['seq']==atk['seq']-1 and x['by']==atk['from']]
   assert len(rr)==1,'exact RNG event before attack'
   r=rr[0];assert tuple(r['crit'])==tuple(atk['critical_sequence'])
   rr_attempts=[tuple(a) for a in r['attack_attempts']];used=[tuple(a) for a in atk['attack_roll_attempts']]
   assert (used==rr_attempts if atk['attack_origin']=='OPPORTUNITY' else used==rr_attempts[:1])
   assert atk['advantage_levels']==(1 if atk['attack_origin']=='OPPORTUNITY' else 0)
   if atk['attack_origin']=='OPPORTUNITY':
    ident=atk['opportunity_intent_seq'];res=[x for x in intents if x['seq']==ident]
    assert len(res)==1
    claim=res[0]; assert claim['seq']<r['seq']<atk['seq'] and r['intent_seq']==claim['seq']
    assert claim['by']==atk['from'] and claim['to']==atk['to']
    assert claim['reaction_before']==1 and claim['reaction_after']==0 and claim['before_offensive_rng']==True
   else:assert atk['opportunity_intent_seq'] is None
  assert len(set(x['seq'] for x in intents))==len(intents)==len(aoos)
  assert all(x['attack_origin']=='OPPORTUNITY' for x in aoos)
  assert len({x['opportunity_intent_seq'] for x in aoos})==len(aoos)
  if 'r214' in state:
   m=state['r214']['stats'];case=state['r214']['case']
   assert len(aoos)==m['aoo']==m['reactions'] and len(intents)==len(aoos)
   assert sum(x['hp_loss_actual'] for x in aoos)==m['hp_loss']
   assert sum(x['hit'] for x in aoos)==m['hits']
   assert m['misses']==len(aoos)-m['hits']
   assert counters['move']==m['moves']
   assert counters['r214_movement_declared']==m['windows']
   priorities=[x for x in ev if x['action']=='r214_r43_priority']
   if case=='TIE':
    assert len(priorities)==1 and priorities[0]['R49_4d6']==True
    draws=priorities[0]['tie_draws'];assert len(draws)>=2
    assert all(len(x['dice'])==4 and all(1<=v<=6 for v in x['dice']) and x['rank']=='ON5' for x in draws)
    assert priorities[0]['order']==[x['from'] for x in aoos]
    rounds=collections.defaultdict(list)
    for x in draws:rounds[x['round']].append(x)
    assert len(rounds[1])==2
    # recompute winner after ties until first non-equal draw on both.
    winner=None
    for v in sorted(rounds):
     rr=rounds[v]
     if len(rr)==2 and rr[0]['sum']!=rr[1]['sum']:
      winner=max(rr,key=lambda x:x['sum'])['actor'];break
    assert winner==priorities[0]['order'][0],'tie winner wrong'
   if case=='MISS':assert m['aoo']==1 and m['misses']==1 and m['hp_loss']==0 and state['actors']['A']['resource']['reaction']==0
   if case=='SPENT_CHAIN':
    assert len(rows)==2 and m['windows']==2 and m['aoo']==1 and m['moves']==2
    assert len(intents)==1 and state['actors']['F']['resource']['reaction']==0
    assert len([x for x in ev if x['action']=='r214_reaction_window_open' and x['eligible']==[]])==1
    assert attacks[0]['seq']<ev[-1]['seq']
   if case=='NO_ADJ':assert len(aoos)==len(intents)==0 and m['moves']==1
   if case=='LETHAL':
    assert len(aoos)==1 and state['actors']['R']['resource']['hp']==0 and m['moves']==0
    assert state['actors']['V']['resource']['reaction']==1
    assert counters['r214_move_interrupted_HP0']==1
    assert state['r214']['interrupt_movement_cost']=='UNKNOWN_EFFECT_HOLD'
   if case=='DOUBLE':assert len(aoos)==2 and priorities[0]['order']==['F','V']
  else:
   m=state['r214bi'];assert m['phash']==PH
   assert counters['move']==0 and len(aoos)==0
   assert m['turns']['V']>=2 and m['turns']['R']>=2
   assert m['attacks']==len(attacks)==len(rows)
   assert sum(x['hit'] for x in attacks)==m['hits']
   assert sum(x['hp_loss_actual'] for x in attacks)==m['hp_loss']
   assert all(x['attack_origin']=='NORMAL' for x in attacks)
   assert counters['turn_end']==len(attacks)
   assert counters['turn_start']>=len(attacks)-1
   who=[x['from'] for x in attacks];assert all(who[i]!=who[i-1] for i in range(1,len(who)))
   assert len(set(who))==2
   assert state['phase'] in ('CENSORED_HORIZON','KO_TEST')
  return {'db':db.name,'rev':len(rows),'events':len(ev),'attacks':len(attacks),'aoo':len(aoos),'reactions':len(intents),
    'hp_loss':sum(x['hp_loss_actual'] for x in attacks),'case':state.get('r214',{}).get('case','BILATERAL'),'phase':state['phase']}
 finally:c.close()

def main():
 dbs=sorted((R/'evidence/db').glob('R214_*.sqlite'))
 out=[scan(x) for x in dbs if 'FAULT' not in x.name]
 assert len(out)==sum(len(x) for x in PRE['aoo_cases'].values())+len(PRE['bilateral_seeds'])
 assert len(set(x['db'] for x in out))==len(out)
 result={'status':'PASS_R214_INDEPENDENT_SQL_CAUSAL_AOO_AND_BILATERAL','dbs':len(out),'commits':sum(x['rev'] for x in out),
  'events':sum(x['events'] for x in out),'aoo':sum(x['aoo'] for x in out),'total_physical_attacks':sum(x['attacks'] for x in out),
  'reactions_consumed':sum(x['reactions'] for x in out),'total_hp_loss':sum(x['hp_loss'] for x in out),'cases':out}
 if '--readonly' not in sys.argv:
  (R/'evidence/R214_INDEPENDENT_AUDIT.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
 print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))
if __name__=='__main__':main()
