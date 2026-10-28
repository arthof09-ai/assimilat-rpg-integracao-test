"""Independent cold audit: SQLite read-only, no import or execution of R18 combat motor."""
from pathlib import Path
import json,hashlib,sqlite3,collections
ROOT=Path(__file__).resolve().parents[1]
PBYTES=(ROOT/'source/R209_SPORES_AREA_PREREG.json').read_bytes();PRE=json.loads(PBYTES)
PHASH=hashlib.sha256(PBYTES).hexdigest()
E='ERISTAN_ON5_SPORES';B1='DRACOLION_SPORES_A';B2='DRACOLION_SPORES_B';TRIO=(E,B1,B2)
def canon(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def sha(x):return hashlib.sha256(canon(x).encode()).hexdigest()

def audit(path):
 db=sqlite3.connect('file:'+str(path)+'?mode=ro',uri=True)
 try:
  meta=dict(db.execute('SELECT key,value FROM meta'))
  rows=list(db.execute('SELECT seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha FROM events ORDER BY seq'))
  assert not list(db.execute('SELECT * FROM pending')), 'UNKNOWN_EFFECT'
  assert len(rows)==int(meta['revision'])>0 and meta['mode']=='EXPERIMENTAL_LAB_ONLY'
  st=json.loads(meta['state']);r=st['r209'];seed=st['seed'];policy=r['policy'];assert seed in PRE['seeds'] and policy in PRE['policies']
  assert r['prereg_sha']==PHASH and r['source_status']==PRE['source_status'] and set(st['actors'])==set(TRIO)
  prev=meta['genesis'];last_after=None;evs=[]
  for seq,cmd,back,row_text,row_sha,before,after in rows:
   row=json.loads(row_text)
   assert row['seq']==seq and row['cmd_id']==cmd and row['prev']==back==prev
   assert sha(row)==row_sha and row['before_sha']==before and row['after_sha']==after
   assert row['official_effects']==0 and row['synthetic'] is True
   if last_after is not None:assert before==last_after
   evs+=row['detail'].get('events_added',row['detail'].get('new_native_events',[]))
   prev=row_sha;last_after=after
  assert prev==meta['head'] and last_after==sha(st)
  assert evs==st['native_events'] and [v['seq'] for v in evs]==list(range(1,len(evs)+1))
  hp={w:PRE['actors'][w]['hp'] for w in TRIO};pa=804;casts=[];effects=[];attacks=[];pending=None
  for ev in evs:
   ac=ev['action']
   if pending is not None and ac!='r209_area_target':raise AssertionError('MULTITARGET_ATOMIC_SEQUENCE_BROKEN')
   if ac=='weapon_attack':
    assert ev['from'] in (B1,B2) and ev['to']==E
    assert ev['before_hp']==hp[E]
    assert len(ev['damage_roll_groups'])==1 and len(ev['damage_roll_groups'][0])==9
    assert all(1<=v<=6 for v in ev['damage_roll_groups'][0])
    assert ev['normal_damage']==sum(ev['damage_roll_groups'][0])
    assert ev['hp_loss_actual']==min(hp[E],ev['net']) and ev['after_hp']==hp[E]-ev['hp_loss_actual']
    assert ev['ca_exact']=='76'
    hp[E]=ev['after_hp'];attacks.append(ev)
   elif ac=='r209_area_cast':
    assert policy=='SPELL_ON' and ev['by']==E and ev['source']==PRE['source']
    assert ev['action_economy']=='STANDARD' and ev['pa_spent']==80
    assert ev['pa_before']==pa and ev['pa_after']==pa-80
    assert ev['center_m']==PRE['chosen_center_m'] and ev['radius_m']==5
    assert ev['center_max_m']==25 and set(ev['in_area'])==set(TRIO)
    assert len(ev['cast_roll_10d10'])==10 and all(1<=v<=10 for v in ev['cast_roll_10d10'])
    assert ev['common_roll_total']==sum(ev['cast_roll_10d10'])+10
    casts.append(ev);pa-=80
    pending={'cast':ev,'targets':set(ev['in_area'])}
   elif ac=='r209_area_target':
    assert pending is not None and ev['cast_event_seq']==pending['cast']['seq']
    who=ev['target'];assert who in pending['targets'];pending['targets'].remove(who)
    assert ev['source']==PRE['source'] and ev['by']==E
    cfg=PRE['actors'][who];n,faces=cfg['fortitude_dice']
    assert n==ev['save_dice_n'] and len(ev['save_dice'])==n and all(1<=v<=faces for v in ev['save_dice'])
    assert ev['save_attribute_con']==cfg['CON'] and ev['save_total']==sum(ev['save_dice'])+cfg['CON']
    assert ev['CD']==76 and ev['save_success']==(ev['save_total']>76)
    assert not ev['save_success'],'ODD_HALF_ROUNDING_NOT_TESTED'
    assert ev['distance_squared_to_center']<=ev['radius_squared']==25
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
   elif ac=='r209_pass':
    assert ev['by']==E and ev['pa_spent']==0
  assert pending is None
  assert {w:st['actors'][w]['resource']['hp'] for w in TRIO}==hp
  assert st['actors'][E]['resource']['pa']==pa
  assert r['spell_casts']==len(casts) and r['pa_paid']==80*len(casts)==804-pa
  assert r['targets_resolved']==len(effects)==3*len(casts)
  assert r['total_effective']==sum(x['hp_loss_actual'] for x in effects)
  assert r['total_raw']==sum(x['damage_raw'] for x in effects)
  assert r['self_damage']==sum(x['hp_loss_actual'] for x in effects if x['self_target'])
  assert r['beast_damage']==sum(x['hp_loss_actual'] for x in effects if not x['self_target'])
  assert st['metrics']['attempts']==len(attacks)
  if hp[E]==0:assert st['phase']=='FINISHED' and st['winner']=='BEAST_SIDE'
  else:assert st['phase']=='ACTIVE' and st['winner'] is None
  return {'run_id':path.stem,'seed':seed,'policy':policy,'commits':len(rows),'events':len(evs),
    'attacks':len(attacks),'casts':len(casts),'target_events':len(effects),
    'PA_spent':804-pa,'magic_effective':r['total_effective'],
    'self_damage':r['self_damage'],'beast_damage':r['beast_damage'],
    'status':'KO' if hp[E]==0 else 'CENSORED_HORIZON','HP':hp,'head':meta['head'],
    'attack_tapes':{w:[{'normal':x['normal_damage'],'score':x['roll_score'],'rolls':x['damage_roll_groups']}for x in attacks if x['from']==w] for w in (B1,B2)}}
 finally:db.close()

def main():
 dbs=sorted((ROOT/'evidence/db').glob('R209_AREA_SPORES_S*.sqlite'))
 got=[audit(p) for p in dbs]
 assert len(got)==6 and len({x['run_id'] for x in got})==6
 official=json.loads((ROOT/'evidence/R209_COMBAT_RESULTS.json').read_text())
 assert len(official)==8 and sum(x['status']=='PRECOMMIT_INIT_TIE_HOLD' for x in official)==2
 ref={x['run_id']:x for x in official if 'db' in x}
 for x in got:
  y=ref[x['run_id']]
  for k,v in [('commits','commits'),('events','events'),('attacks','attacks'),('casts','casts'),('target_events','area_target_events'),('PA_spent','pa_spent'),('magic_effective','magic_effective'),('self_damage','self_damage'),('beast_damage','beast_damage'),('status','status'),('HP','final_hp')]:
   assert x[k]==y[v],(x['run_id'],k,x[k],y[v])
 groups=collections.defaultdict(dict)
 for x in got:groups[x['seed']][x['policy']]=x
 assert len(groups)==3 and all(set(z)==set(PRE['policies']) for z in groups.values())
 for seed,g in groups.items():
  for b in (B1,B2):
   off=g['SPELL_OFF']['attack_tapes'][b];on=g['SPELL_ON']['attack_tapes'][b]
   assert off[:len(on)]==on,'BEAST_ATTACK_RNG_DRIFT'
 total={'combats':len(got),'seeds':len(groups),'precommit_ties':2,'commits':sum(x['commits'] for x in got),
 'events':sum(x['events'] for x in got),'attacks':sum(x['attacks'] for x in got),
 'casts':sum(x['casts'] for x in got),'target_events':sum(x['target_events'] for x in got),
 'PA_spent':sum(x['PA_spent'] for x in got),'magic_effective':sum(x['magic_effective'] for x in got),
 'self_damage':sum(x['self_damage'] for x in got),'beast_damage':sum(x['beast_damage'] for x in got),
 'KO':sum(x['status']=='KO' for x in got),'censures':sum(x['status']=='CENSORED_HORIZON' for x in got)}
 assert total=={'combats':6,'seeds':3,'precommit_ties':2,'commits':240,'events':795,'attacks':156,
 'casts':30,'target_events':90,'PA_spent':2400,'magic_effective':5779,'self_damage':1875,
 'beast_damage':3904,'KO':3,'censures':3},total
 report={'audit':'PASS_R209_INDEPENDENT_R18_MULTITARGET_GEOMETRY_AREA_WITH_CASTER',
 'combat_reexecutions_during_audit':0,'audited':total,
 'source_grade':'PROPOSED_NPC_AND_CONDITIONAL_BEAST','sample_unit':'three paired seeds',
 'halving_successes':0,'half_rounding':'NOT_PROVEN_NOT_EXERCISED',
 'participants_inside_area':3,'caster_included':True,'outcome_warning':'KO_IN_ON_ARM_IS_CASTER_CAUSED_AREA_DAMAGE_NOT_BEST_POWER_PROOF'}
 (ROOT/'evidence/R209_INDEPENDENT_AUDIT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
 print(json.dumps(report,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
