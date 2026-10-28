"""Independent SQLite-only science audit R226. No combat-runtime imports."""
from pathlib import Path
import json,sqlite3,hashlib,collections
ROOT=Path(__file__).resolve().parents[1]
def sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def req(cond,label):
 if not cond:raise AssertionError(label)
def one(path,seed,arm,pre,item):
 c=sqlite3.connect('file:'+str(path)+'?mode=ro&immutable=1',uri=True)
 try:
  m=dict(c.execute('select key,value from meta'))
  st=json.loads(m['state'])
  rows=[json.loads(x[0]) for x in c.execute('select row_json from events order by seq')]
  receipts=list(c.execute('select seq,cmd_id,prev,row_sha,before_sha,after_sha from events order by seq'))
  pending=c.execute('select count(*) from pending').fetchone()[0]
 finally:c.close()
 req(len(rows)==len(receipts)==2 and int(m['revision'])==2 and pending==0,'TWO_COMMITS_NO_PENDING')
 last=m['genesis']
 for i,(r,rec) in enumerate(zip(rows,receipts),1):
  req(r['seq']==i and rec==(i,r['cmd_id'],r['prev'],sha(r),r['before_sha'],r['after_sha']),'ROW_HASH_FORGED')
  req(r['prev']==last,'BROKEN_CHAIN')
  last=sha(r)
 req(m['head']==last and sha(st)==rows[-1]['after_sha'],'FINAL_HASH')
 req(rows[0]['kind']=='R226_ATTACK_AND_ITEM' and rows[1]['kind']=='R226_NEXT_OWN_TURN','R18_KIND')
 req(all(x['official_effects']==0 for x in rows) and st['r226']['world_canon'] is False,'PRODUCTION_LEAK')
 req(st['r226']['pre_sha256']==pre and st['r226']['item_excerpt_sha256']==item,'SOURCE_EVIDENCE')
 req(st['r226']['arm']==arm and st['seed']==seed and st['phase']=='CENSORED_SOURCE_EFFECT_WINDOW','RUN_ID_AND_CENSURE')
 ev=st['native_events'];req(ev==rows[0]['detail']['events_added']+rows[1]['detail']['events_added'],'R18_NATIVE_EVENTS_NOT_LAUNDERED')
 for k,e in enumerate(ev,1):req(e['seq']==k,'NATIVE_EVENT_SEQUENCING')
 by={}
 for e in ev:by.setdefault(e['action'],[]).append(e)
 attack=by['weapon_attack'][0];rng=by['R226_ATTACK_HIT_AND_CRITICAL_RNG'][0];dmg=by['R226_DAMAGE_RNG_AFTER_DECLARATION'][0]
 req(attack['from']=='R' and attack['to']=='V' and attack['attack_origin']=='NORMAL','ATTACK_ORIGIN')
 req(len(attack['attack_roll_attempts'])==1 and len(attack['attack_roll_attempts'][0])==4 and
   all(1<=x<=6 for x in attack['attack_roll_attempts'][0]),'HIT_4D6')
 req(attack['attack_roll_attempts'][0]==rng['rolls'],'HIT_DICE_SHARE')
 req(attack['critical_sequence']==rng['crit_rolls'] and attack['roll_score']==sum(rng['rolls'])+72,'SCORE_TAPE')
 crit=rng['critical'];req(crit in ('NONE','POSITIVE','NEGATIVE'),'CRIT_KIND')
 positive=rng['crit_rolls'][:2]==[6,6] and rng['crit_rolls'][2]>=5
 negative=rng['crit_rolls'][:2]==[1,1] and rng['crit_rolls'][2]<=2
 req(crit==('POSITIVE' if positive else 'NEGATIVE' if negative else 'NONE'),'CRIT_CLASS')
 hit=(attack['roll_score']>83 or positive) and not negative
 req(hit==attack['hit']==rng['hit'],'HIT_CA_OR_CRITICAL')
 req(attack['ca_exact']=='83' and attack['type']=='perfurante','CA_AND_TYPE')
 phys_rolls=dmg['physical_rolls'];req(len(phys_rolls)==8 and all(1<=x<=10 for x in phys_rolls),'PHY_DICE')
 raw=sum(phys_rolls)+35+(80 if positive and hit else 0)
 phy=max(0,raw-35) if hit else 0
 req(attack['raw']==(raw if hit else 0) and attack['net']==phy and attack['hp_loss_actual']==phy,'PHYSICAL_RD_ACCOUNTING')
 req(attack['before_hp']==734 and attack['after_hp']==734-phy,'PHY_HP')
 req(dmg['magic_active']==(hit and arm=='SAME_PHYSICAL_WITH_MAGIC'),'ITEM_ONLY_AFTER_HIT')
 lightning=by.get('R226_ITEM_LIGHTNING_AND_CONDITION',[])
 item_decl=by.get('R226_ITEM_DECLARATION_BEFORE_DAMAGE_RNG',[])
 if arm=='SAME_PHYSICAL_WITH_MAGIC' and hit:
  req(len(item_decl)==len(lightning)==1,'SOURCE_ITEM_EFFECT_MISSING')
  decl=item_decl[0];light=lightning[0]
  req(rng['seq']<decl['seq']<dmg['seq']<attack['seq']<light['seq'],'AFTER_HIT_BEFORE_DAMAGE')
  req(decl['pa_spent']==22 and decl['once_per_8h'] and decl['item_equipped'] and decl['no_extra_standard'],'ITEM_BUDGET_AND_TRIGGER')
  lr=dmg['lightning_rolls'];req(len(lr)==5 and all(1<=x<=8 for x in lr),'MAGIC_5D8')
  magic_raw=sum(lr)+3+(40 if positive else 0)
  req(light['magic_raw']==magic_raw and light['magic_effective']==magic_raw and light['magic_rd']==0,'MAGICAL_RD_ZERO_LAB_HYPOTHESIS')
  req(light['hp_before']==734-phy and light['hp_after']==734-phy-magic_raw,'MAGICAL_FOLLOW_PHY')
  req(light['slow_applied'] and light['slow_m']==3 and light['slow_until']=='END_TARGET_NEXT_OWN_TURN','SOURCE_ITEM_SLOW')
  spent=22; magic=magic_raw
 else:
  req(not item_decl and not lightning and len(by.get('R226_ITEM_NO_ACTIVATION',[]))==1,'FORBIDDEN_EXTRA_MAGIC')
  req(dmg['lightning_rolls']==[] and by['R226_ITEM_NO_ACTIVATION'][0]['magic_effective']==0,'NO_MAGIC_ROLLS')
  spent=0;magic=0
 req(st['actors']['R']['pa']==344-spent and st['actors']['V']['hp']==734-phy-magic,'RESOURCE_FINAL')
 req(st['actors']['V']['timed_source_speed_penalty_m']==0 and st['actors']['R']['standard']==0,'FINAL_COOLDOWN_AND_BUDGET')
 observed=by['R226_SLOWED_TARGET_TURN_OBSERVATION'][0]
 req(observed['available_speed_in_declared_4m_lab_fixture']==('1' if magic>0 else '4'),'TEST_SPEED_OBSERVATION')
 req(observed['no_metric_world_block_mapping'] and observed['source_speed_4m_is_TEST_assumption'],'METRIC_NOT_CANON')
 req(len(by.get('R226_SOURCE_ITEM_SLOW_EXPIRES',[]))==(1 if magic>0 else 0),'EXPIRY_REQUIRED_OR_ABSENT')
 req(by['turn_start'][0]['by']=='R' and by['turn_start'][1]['by']=='V' and
   by['turn_end'][0]['by']=='R' and by['turn_end'][1]['by']=='V','SCHEDULER_CAUSAL')
 return {'seed':seed,'arm':arm,'hit':hit,'physical_hp_loss':phy,'magic_hp_loss':magic,'item_PA':spent,'native_events':len(ev),'commits':len(rows),'speed_test':observed['available_speed_in_declared_4m_lab_fixture']}
def run(root=ROOT):
 p=(root/'sources/R226_PREREG_BEFORE_EXEC.json').read_bytes();pr=json.loads(p);h=hashlib.sha256(p).hexdigest()
 ib=(root/'sources/R226_MANOPLA_PRIMARY_MECHANICAL_EXCERPT.json').read_bytes();ih=hashlib.sha256(ib).hexdigest()
 req(pr['candidate']=='R226' and len(pr['seeds'])==8 and len(pr['arms'])==2,'PREREG_COUNTS')
 outs=[];files=[]
 for seed in pr['seeds']:
  for arm in pr['arms']:
   path=root/'evidence/db'/f'R226_MANOPLA_{arm}_S{seed}.sqlite';req(path.exists(),'MISSING_RUN')
   files.append(path.name);outs.append(one(path,seed,arm,h,ih))
 req(set(files)=={x.name for x in (root/'evidence/db').glob('*.sqlite')},'EXTRA_OR_HIDDEN_RUNS')
 pairs=[]
 for seed in pr['seeds']:
  a,b=[next(x for x in outs if x['seed']==seed and x['arm']==arm) for arm in pr['arms']]
  req(a['hit']==b['hit'] and a['physical_hp_loss']==b['physical_hp_loss'],'PAIR_PHYSICAL_INVARIANT')
  req(b['magic_hp_loss']==(0 if not b['hit'] else b['magic_hp_loss']),'PAIR_HIT_GATES')
  pairs.append({'seed':seed,'magic_added_hp_loss':b['magic_hp_loss'],'pa_added':b['item_PA'],'source_slow':b['magic_hp_loss']>0})
 return {'status':'PASS_R226_INDEPENDENT_PAIR_SQL_AUDIT_SEMICANON_TEST','independent_pairs':len(pairs),'valid_arms':len(outs),'new_commits':sum(x['commits'] for x in outs),'events':sum(x['native_events'] for x in outs),'hits':sum(x['hit'] for x in outs if x['arm']=='SAME_PHYSICAL_WITH_MAGIC'),'magic_extra_hp':sum(x['magic_added_hp_loss'] for x in pairs),'item_pa':sum(x['pa_added'] for x in pairs),'slows':sum(x['source_slow'] for x in pairs),'historical_replays':0,'pairs':pairs}
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
