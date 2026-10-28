"""Independent R216 READ-ONLY scientific auditor. NO engine imports, NO runner imports.
Full journal hash chain, stored native events, HP/PA, reactions, action budgets, geometry,
movement, RNG action linkage and source limits. Evidence-only, no DB writes.
"""
import argparse,hashlib,json,math,sqlite3,ast
from pathlib import Path
from collections import Counter
BASE=Path(__file__).resolve().parents[1]
def cj(v):return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def hs(v):return hashlib.sha256(cj(v).encode()).hexdigest()
def check(c,msg):
 if not c:raise AssertionError(msg)
def xy(s):
 a=ast.literal_eval(s) if isinstance(s,str) else s
 return tuple(float(v) for v in a)

def audit_one(f,allow_pending=False):
 con=sqlite3.connect(f'file:{f}?mode=ro&immutable=1',uri=True)
 try:
  m=dict(con.execute('SELECT key,value FROM meta'));rev=int(m['revision']);state=json.loads(m['state']);rows=list(con.execute('SELECT seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha FROM events ORDER BY seq'));pending=list(con.execute('SELECT cmd_id FROM pending'))
  check(rev==len(rows),'REVISION_DRIFT');check(state.get('seed') and state['r216']['pre_hash'],'NON_R216_STATE')
  if pending:
   check(allow_pending,'UNEXPECTED_PENDING');check(len(pending)==1,'PENDING_MULTIPLICITY');return {'file':f.name,'status':'QUARANTINE_PENDING','revision':rev,'pending':pending[0][0]}
  prev=m['genesis'];all_ev=[];past=None
  for idx,(seq,cmd,pr,rj,rsha,bef,aft) in enumerate(rows,1):
   row=json.loads(rj);check(seq==idx and row['seq']==seq and row['cmd_id']==cmd,'CMD_SEQ');check(pr==prev==row['prev'],'HASH_CHAIN');check(hs(row)==rsha,'ROW_SHA');check(bef==row['before_sha'] and aft==row['after_sha'],'STATE_SHA_RECEIPT');check(past is None or bef==past,'STATE_BEFORE_CONTIGUITY');check(cmd.startswith('LAB-CMD-R216'),'CMD_PREFIX');check(row['kind']=='R216_INTEGRATED_TURN','KIND');check(row['payload']['seed']==state['seed'],'SEED');
   ev=row['detail']['events_added'];check(ev and ev[0]['action']=='turn_start' and ev[-1]['action']=='turn_end','TURN_EVENTS');check(row['detail']['who']==ev[0]['by']==ev[-1]['by'],'TURN_ACTOR')
   all_ev+=ev;prev=rsha;past=aft
  check(prev==m['head'],'HEAD_HASH');check(past==hs(state),'STATE_HEAD_MATCH');check(len(all_ev)==len(state['native_events']) and all_ev==state['native_events'],'NATIVE_EVENTS_DRIFT')
  check(state['phase'] in ('CENSORED_HORIZON','KO_HP0'),'TERMINAL_PHASE');check(all(e['seq']==i for i,e in enumerate(all_ev,1)),'EVENT_SEQ')
  initial={'V':{'hp':734,'pa':324,'max':734,'reactions':1,'std':0,'movement':1,'pos':(0,0)},'R':{'hp':806,'pa':344,'max':806,'reactions':1,'std':0,'movement':1,'pos':(3,1)},'E':{'hp':630,'pa':804,'max':630,'reactions':1,'std':0,'movement':1,'pos':(0,3)}}
  actors=initial;uses=set();roll_counter=Counter();guard_used=set();move_count=0;opportunities=0;attack_count=0;heals=0;spells=0;physical_loss=0;mag_loss=0;actual_healed=0;guards=0
  active=None;last_action=None;last_rng={};intent={};tally=Counter();attack_sequence=[];heal_seen=0
  for e in all_ev:
   a=e['action'];tally[a]+=1
   if a=='turn_start':
    check(active is None,'OVERLAPPING_TURN');active=e['by'];check(actors[active]['hp']>0,'KO_ACTOR_TURN');actors[active]['reactions']=1;actors[active]['std']=1;actors[active]['movement']=1
   elif a=='turn_end':check(e['by']==active and actors[active]['std']==0,'INVALID_TURN_END');active=None
   elif a=='R216_PATH_DECISION':
    k=e['by'];check(e['from']==str(tuple(int(x) for x in actors[k]['pos'])) or xy(e['from'])==actors[k]['pos'],'PATH_SOURCE_POS');check(e['declared_travel_m']>=e['geometric_distance'],'BAD_PATH_LENGTH')
   elif a=='move':
    k=e['by'];check(k==active and actors[k]['movement']==1,'MOVE_ACTION');check(xy(e['from'])==actors[k]['pos'],'MOVE_POS_FROM');cost=float(e['travel_cost']);spd=float(e['speed']);check(0<=cost<=spd<=4,'MOVE_VERIFIED_TEST_SPEED');check(math.dist(xy(e['from']),xy(e['to']))<=cost+1e-8,'MOVE_DISTANCE');check(bool(e['path_proof']),'MOVE_PATH');actors[k]['movement']=0;actors[k]['pos']=xy(e['to']);move_count+=1
   elif a=='opportunity_reaction_reserved':
    k=e['by'];check(actors[k]['reactions']==1,'AOO_REACTION_REPEAT');actors[k]['reactions']=0;intent[e['seq']]=(k,e['to']);uses.add(('AOO',e['seq']))
   elif a in ('r214_offensive_rng_generated','R215_OFFENSIVE_RNG'):
    tag=e.get('stream',e.get('source_tape_stream'))
    last_rng[e['by']]=e
    if a=='r214_offensive_rng_generated':
     k=e['by'];matched=[(i,p) for i,p in intent.items() if p[0]==k]
     check(matched,'AOO_RNG_BEFORE_RESERVE')
   elif a=='R215_POST_RD_GUARD':
    k=e['by'];check(k in ('V','R') and k not in guard_used,'GUARD_ONCE_SCENE');guard_used.add(k);check(actors[k]['reactions']==1 and actors[k]['pa']>=e['PA_spent'],'GUARD_RESOURCES');check((k,e['PA_spent']) in (('V',50),('R',40)),'GUARD_SOURCE_PA');check(e['post_rd_damage']==max(0,e['raw']-e['rd_applied']),'GUARD_AFTER_RD');check(e['reduction']==min(e['post_rd_damage'],70 if k=='V' else 50),'GUARD_LIMIT');check(e['remaining']==e['post_rd_damage']-e['reduction'],'GUARD_NET');actors[k]['reactions']=0;actors[k]['pa']-=e['PA_spent'];guards+=1
   elif a=='weapon_attack':
    k=e['from'];z=e['to'];attack_count+=1;attack_sequence.append((k,z,e['attack_origin']))
    check(actors[z]['hp']==e['before_hp'],'ATTACK_HP_BEFORE');check(actors[k]['hp']>0,'ATTACK_BY_KO');
    if e['attack_origin']=='NORMAL':check(k==active and actors[k]['std']==1,'ATTACK_ACTION');actors[k]['std']=0
    else:
     check(e['attack_origin']=='OPPORTUNITY' and e['opportunity_intent_seq'] in intent,'AOO_INTENT_MISSING')
     check(intent[e['opportunity_intent_seq']]==(k,z),'AOO_LINK');check(e['advantage_levels']>=1,'AOO_ADV');opportunities+=1
    rolls=e['damage_roll_groups'];check(all(1<=v<= (10 if k in ('V','R') else 8) for group in rolls for v in group),'ATTACK_DICE_FACE')
    check(e['raw']==(0 if not e['hit'] else e['normal_damage']+e['critical_max_bonus']),'ATTACK_GROSS');
    check(e['hit']==(e['roll_score']>float(e['ca_exact']) or e['critical']=='POSITIVE') and e['critical']!='NEGATIVE','ATTACK_HIT_RULE')
    rd={'V':35,'R':30,'E':25}[z];check(e['rd_applied']==(rd if e['hit'] else 0),'ATTACK_RD');check(e['post_rd_pre_guard']==(max(0,e['raw']-rd) if e['hit'] else 0),'ATTACK_RD_NET')
    check(e['net']==max(0,e['post_rd_pre_guard']-e['post_rd_guard_reduction']),'ATTACK_POST_GUARD_NET');check(e['after_hp']==max(0,e['before_hp']-e['net']),'ATTACK_HP_AFTER');check(e['hp_loss_actual']==e['before_hp']-e['after_hp'],'ATTACK_REAL_DAMAGE');actors[z]['hp']=e['after_hp'];physical_loss+=e['hp_loss_actual']
    if e['post_rd_guard_reduction']:
     check(z in guard_used,'GUARD_EVENT_BEFORE_ATTACK');check(e['guard_source'],'GUARD_RECEIPT_SOURCE')
   elif a=='PULSO_ESTABILIZACAO':
    k=e['by'];z=e['to'];check(k=='E' and z=='V','PULSO_ACTORS');check(actors[k]['reactions']==1 and actors[k]['pa']>=45,'PULSO_REACTION');check(e['before_hp']==actors[z]['hp'],'PULSO_HP_BEFORE');check(e['gross_heal']==sum(e['healing_rolls'])+10+20,'PULSO_DICE');check(e['actual_heal']==min(actors[z]['max']-actors[z]['hp'],e['gross_heal']),'PULSO_CAP');check(e['after_hp']==actors[z]['hp']+e['actual_heal'],'PULSO_HP_AFTER');actors[k]['reactions']=0;actors[k]['pa']-=45;actors[z]['hp']=e['after_hp'];heals+=1;actual_healed+=e['actual_heal'];heal_seen+=1
   elif a=='RECONSTITUICAO_SEIVA':
    k=e['by'];z=e['to'];check(k==active=='E' and z=='V' and actors[k]['std']==1 and actors[k]['pa']>=75,'RECONST_ACTION');check(e['hp_before']==actors[z]['hp'],'RECONST_BEFORE');check(e['gross_heal']==sum(e['healing_rolls'])+25+20,'RECONST_DICE');check(e['actual_healed']==min(actors[z]['max']-actors[z]['hp'],e['gross_heal']),'RECONST_CAP');check(e['hp_after']==e['hp_before']+e['actual_healed'],'RECONST_AFTER');actors[k]['std']=0;actors[k]['pa']-=75;actors[z]['hp']=e['hp_after'];heals+=1;actual_healed+=e['actual_healed'];heal_seen+=1
   elif a=='spell':
    k=e['by'];z=e['target'];check(k==active=='E' and z=='R' and actors[k]['std']==1 and actors[k]['pa']>=80,'SPELL_ACTION');check(e['hp_before']==actors[z]['hp'],'SPELL_HP_BEFORE');check(e['damage_rolls'] and sum(e['damage_rolls'])+10 in (e['raw'],2*e['raw']),'SPELL_DAMAGE_ROLLS');check(e['PA_spent']==80,'SPELL_PA_SOURCE_COST');check(e['save_effect']=='SAVE-HALF','SPELL_SAVE_KIND');check(e['rd_applied']==0,'SPELL_MAGICAL_RD_TEST0');check(e['hp_after']==max(0,e['hp_before']-e['effective']),'SPELL_HP_AFTER');actors[k]['pa']-=80;actors[k]['std']=0;actors[z]['hp']=e['hp_after'];spells+=1;mag_loss+=e['hp_before']-e['hp_after']
   elif a=='R216_GEOMETRY_STATE_DECISION':
    check(e['by']=='E' and e['included']==['R'],'GEOMETRY_TARGETS');p=e['position_snapshot'];c=e['chosen_center'];check(math.dist(p['E'],c)<=25,'SPELL_CENTER_RANGE');check(math.dist(p['R'],c)<=5+1e-9,'SPELL_R_MISSED');check(math.dist(p['E'],c)>5 and math.dist(p['V'],c)>5,'SPELL_FRIENDLY_FIRE_FABRICATED');check(e['save_passed']==(e['save_total']>76),'SAVE_TOTAL');check(e['save_total']==sum(e['save_rolls'])+57,'SAVE_CON_ATTRIBUTE')
   elif a=='R216_SUPPORT_OBSERVED_STATE':
    check(e['by']=='E' and e['missing_hp']==actors['V']['max']-actors['V']['hp'],'SUPPORT_STALE_HP');expect='HEAL' if e['missing_hp']>=e['policy_threshold'] and e['heal_legal'] else 'SPORES';check(e['choice']==expect,'SUPPORT_WRONG_POLICY')
   elif a=='R216_ENEMY_TARGET_DECISION':
    check(e['by']=='R' and e['observed_heals']==heal_seen,'ENEMY_HEAL_OBSERVABLE');check(e['chosen'] in ('V','E'),'ENEMY_TARGET_INVALID')
  check(active is None,'OPEN_TURN_FINAL')
  for k,st in state['actors'].items():
   for prop,key in [('hp','hp'),('pa','pa'),('reaction','reactions'),('position','pos')]:
    expected=actors[k][key] if key!='pos' else xy(st['position'])
    got=st[prop] if prop!='position' else xy(st[prop]);check(got==expected, f'FINAL_{prop}_DRIFT:{k}: {got}!={expected}')
   check(0<=st['hp']<=st['maximum_hp'] and st['pa']>=0,'FINAL_RESOURCES')
  check(move_count==state['r216']['stats']['moves'],'METRIC_MOVES');check(opportunities==state['r216']['stats']['aoo'],'METRIC_AOO');check(attack_count==state['r216']['stats']['attacks']+state['r216']['stats']['aoo'],'METRIC_ATTACKS');check(guards==state['r216']['stats']['guard'],'METRIC_GUARDS');check(heals==state['r216']['stats']['heals'],'METRIC_HEALS');check(spells==state['r216']['stats']['spells'],'METRIC_SPELLS');check(actual_healed==state['r216']['stats']['healed'],'METRIC_HEAL_ACTUAL')
  check(physical_loss==state['r216']['stats']['physical_hp_loss']+sum(e['hp_loss_actual'] for e in all_ev if e.get('action')=='weapon_attack' and e.get('attack_origin')=='OPPORTUNITY'),'METRIC_PHYSICAL')
  return {'file':f.name,'status':'PASS','seed':state['seed'],'policy':state['r216']['policy'],'team_label':state['r216']['team_label'],'commits':rev,'events':len(all_ev),'moves':move_count,'opportunities':opportunities,'physical_attacks':attack_count,'guards':guards,'heals':heals,'healed_actual':actual_healed,'spells':spells,'physical_hp_loss':physical_loss,'magic_hp_loss':mag_loss,'phase':state['phase'],'HP':{k:st['hp'] for k,st in state['actors'].items()},'PA':{k:st['pa'] for k,st in state['actors'].items()}}
 finally:con.close()

def audit(root=BASE):
 paths=sorted((root/'evidence/db').glob('R216_TEAM_*.sqlite'));check(paths,'NO_R216_DB')
 rows=[audit_one(p) for p in paths];check(all(r['status']=='PASS' for r in rows),'AUDIT_FAILURE')
 return {'status':'PASS_R216_INDEPENDENT_READ_ONLY_DYNAMIC_MULTI_ACTOR_SQLITE','admitted':len(rows),'commits':sum(r['commits'] for r in rows),'events':sum(r['events'] for r in rows),'moves':sum(r['moves'] for r in rows),'attacks':sum(r['physical_attacks'] for r in rows),'aoo':sum(r['opportunities'] for r in rows),'heals':sum(r['heals'] for r in rows),'spells':sum(r['spells'] for r in rows),'censures':sum(r['phase']=='CENSORED_HORIZON' for r in rows),'KO':sum(r['phase']=='KO_HP0' for r in rows),'rows':rows}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--root',default=str(BASE));args=ap.parse_args();r=audit(Path(args.root));(Path(args.root)/'evidence/reports/R216_INDEPENDENT_AUDIT.json').write_text(json.dumps(r,indent=2,ensure_ascii=False));print(json.dumps({k:v for k,v in r.items() if k!='rows'},indent=2))
