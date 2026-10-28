"""R236 source true Fraco and lab stop HP0: PRECREATE Beast physical bilateral/2x1, no official death."""
import json,hashlib,copy,sys,math,random
from pathlib import Path
from fractions import Fraction
from dataclasses import asdict
R=Path(__file__).resolve().parents[1];sys.path[:0]=[str(R/'code'),str(R/'runtime/native'),str(R/'runtime/fusion_stage12')]
import r234_source_complete_beast_battle as b
from vlab_effects_v08 import Scene,ActorActionState,Resistances,begin_source_turn,end_source_turn,move_via_verified_path,apply_weapon_attack,effective_movement_speed
j=b.j;S_B=(R/'sources/R236_FRACO_RULE_EXCERPT.json').read_bytes();S=json.loads(S_B);SH=hashlib.sha256(S_B).hexdigest()
P_B=(R/'sources/R236_PREREG_BEFORE_EXEC.json').read_bytes();P=json.loads(P_B);PH=hashlib.sha256(P_B).hexdigest()
def actors(order):
 out={a:b.c_actor(a) for a in order};out['C']['hp']=P['initial_hp_croc'];return out
def initial(seed,arm):
 order=P['order'][arm];st=j.initial('A',seed)
 st.update({'scene':f'R236-{arm}-S{seed}','seed':seed,'round':1,'turn':0,'phase':'ACTIVE','active':order[0],'order':order,'actors':actors(order),'native_events':[],
 'r236':{'seed':seed,'arm':arm,'source_beast_sha':b.SH,'rule_sha':SH,'prereg_sha':PH,'source_status':'VZ-PRECREATE-NONP4','croc_initial_lab_wound_hp':95,'croc_source_max_hp':5580,
 'weak':True,'own_turns':{a:0 for a in order},'attacks':0,'hits':0,'moves':0,'actual_hp_loss':0,'critical_negative_lab_policy':True,'final_effort_declared':False,'outcome':None}})
 return st
def setup(db,seed,arm):
 if db.exists():raise FileExistsError('SEED_ALREADY_USED')
 j.init_db(str(db),'A',seed);st=initial(seed,arm);gen=j.sha({'r236':PH,'weak_source':SH,'beast_source':b.SH,'seed':seed,'arm':arm})
 c=j.connect(str(db));
 with c:
  for k,v in [('state',j.canonical(st)),('scene',st['scene']),('genesis',gen),('head',gen)]:c.execute('update meta set value=? where key=?',(v,k))
 c.close()
def dice(seed,actor,turn,tag,n,faces):
 h=int.from_bytes(hashlib.sha256(f'R236|{seed}|{actor}|OWN{turn}|{tag}|{n}d{faces}'.encode()).digest(),'big')
 rng=random.Random(h);return tuple(rng.randint(1,faces) for _ in range(n))
def pos(p):return tuple(float(x.strip()) for x in p.strip('()').split(','))
def do_turn(st,p,revision):
 rec=st['r236'];who=st['active'];seed=st['seed'];arm=rec['arm'];order=st['order'];own=rec['own_turns'][who]+1
 if p!={'arm':arm,'seed':seed,'who':who,'own':own,'prereg_sha':PH,'source_sha':SH}:raise ValueError('UNREGISTERED_TURN')
 fighters={k:b.load_actor(v) for k,v in st['actors'].items()};scene=Scene(fighters,events=copy.deepcopy(st['native_events']),seed=seed,provenance='R236-VZ-PRECREATE-TEST-WEAK-HP0')
 first=len(scene.events);begin_source_turn(scene,who);a=fighters[who]
 if own==1:
  new,dist=b.FIRST_MOVE[who];speed=effective_movement_speed(a)
  if not speed>0 or dist>speed:raise ValueError('SOURCE_WEAK_SPEED_GATE')
  move_via_verified_path(scene,who,source=b.M,state=ActorActionState(who,23,a.pa,(b.M.action_id,),movement_available=True,geometry_confirmed=True,environment_contract=True),proofs=(b.PM,),destination=new,path_evidence='R236_OPEN_LAB_NOT_A_WORLD_METRIC_REACH',travel_cost=dist,speed=speed)
  rec['moves']+=1
 target='C' if who in ('G','R') else 'G' if fighters.get('G') and fighters['G'].hp>0 else 'R'
 if math.dist(pos(fighters[who].position),pos(fighters[target].position))>2:raise ValueError('CLOSE_RANGE_GATE')
 weak=b.weak_status(fighters[who]) if hasattr(b,'weak_status') else fighters[who].hp*10<fighters[who].maximum_hp
 attempts=(dice(seed,who,own,'HIT0',6,6),dice(seed,who,own,'HIT1',6,6)) if weak else (dice(seed,who,own,'HIT0',6,6),)
 scores=[sum(x)+b.BE[who]['attack_bonus'] for x in attempts];score=min(scores)-2 if weak else scores[0]
 damage=dice(seed,who,own,'DAMAGE',20,10);critical=dice(seed,who,own,'CRITICAL',3,6)
 scene.record({'action':'R236_WEAK_SOURCE_RNG_TAPE','by':who,'to':target,'own_turn':own,'weak':weak,'source_hp_fraction':f'{fighters[who].hp}/{fighters[who].maximum_hp}',
  'attack_attempts':attempts,'damage_rolls':damage,'critical_sequence':critical,'roll_score':score,'rule_sha':SH,'beast_source_sha':b.SH,'final_effort_not_declared':True})
 ev=apply_weapon_attack(scene,who,target,source=b.ATK[who],state=ActorActionState(who,23,a.pa,(b.ATK[who].action_id,),standard_available=True,range_confirmed=True,enemy_ids_visible=(target,)),proofs=(b.PF[who],),
 roll_score=score,damage=sum(damage),damage_tag=b.BE[who]['damage_type'],rd=Resistances(general=b.BE[target]['rd'],provenance='VZ-SOURCE-RD75-PHYSICAL'),
 damage_dice_groups=((20,10),),damage_roll_groups=(damage,),damage_fixed_bonus=0,critical_sequence=critical,attack_roll_attempts=attempts,attack_bonus=b.BE[who]['attack_bonus'],lab_negative_critical_policy=True,final_effort=False)
 end_source_turn(scene,who);rec['own_turns'][who]=own;rec['attacks']+=1;rec['hits']+=int(ev['hit']);rec['actual_hp_loss']+=ev['hp_loss_actual'];st['turn']+=1
 if any(x.hp<=0 for x in fighters.values()):
  st['phase']='STOP_HP0_LAB_ONLY';st['active']=None;st['finish_reason']='HP0_NOT_CANONICAL_DEATH'
 elif who==order[-1] and st['round']>=P['round_horizon']:
  st['phase']='CENSORED_HORIZON';st['active']=None;st['finish_reason']='HORIZON_NOT_A_WIN'
 else:
  i=order.index(who);st['active']=order[(i+1)%len(order)];st['round']+=(i==len(order)-1)
 if st['phase']!='ACTIVE':
  rec['outcome']={'phase':st['phase'],'hp':{k:v.hp for k,v in fighters.items()},'turns':st['turn'],'source_P4':False,'official_death':False,'official_benchmark':False}
 st['actors']={k:{**asdict(v),'ca':str(v.ca),'base_speed':str(v.base_speed)} for k,v in fighters.items()};st['native_events']=copy.deepcopy(scene.events)
 return {'who':who,'to':target,'own_turn':own,'weak_actor':weak,'attack_seq':ev['seq'],'hit':ev['hit'],'actual_hp_loss':ev['hp_loss_actual'],
  'events_new':copy.deepcopy(scene.events[first:]),'phase':st['phase'],'active_after':st['active']}
def run():
 rep=[]
 for seed in P['seeds']:
  for arm in P['arms']:
   db=R/'evidence/db'/f'R236_{arm}_S{seed}.sqlite';setup(db,seed,arm)
   for _ in range(6*len(P['order'][arm])):
    st,head,rev=j.load(str(db))
    if st['phase']!='ACTIVE':break
    who=st['active'];own=st['r236']['own_turns'][who]+1
    j.event_commit(str(db),f'LAB-CMD-R236-{arm}-{seed}-{st["turn"]+1}','R236_WEAK_BEAST_SOURCE_NATIVE_TURN',{'arm':arm,'seed':seed,'who':who,'own':own,'prereg_sha':PH,'source_sha':SH},do_turn)
   st,head,rev=j.load(str(db));rep.append({'seed':seed,'arm':arm,'commits':rev,'events':len(st['native_events']),'phase':st['phase'],'outcome':st['r236']['outcome'],'hits':st['r236']['hits'],'attacks':st['r236']['attacks'],'movement':st['r236']['moves'],'head':head})
 (R/'evidence/reports/R236_RESULTS.json').write_text(json.dumps({'status':'PENDING_INDEPENDENT_AUDIT','results':rep,'official_benchmark':False,'historical_replays':0},ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(rep,ensure_ascii=False,indent=2))
if __name__=='__main__':run()
