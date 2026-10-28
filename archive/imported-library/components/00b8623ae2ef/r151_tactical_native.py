"""R151-R160 controlled additive tactical driver, original V081 + R18 + R26.
All experimental profiles taken from reopened Notion docs; no canonical consequences.
"""
import copy,hashlib,json,sqlite3,sys
from pathlib import Path
from dataclasses import asdict
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import r138_multiround_native as base
from r138_multiround_native import core,r26,Combatant,Scene,AbilitySource,FrozenRuleEvidence,ActorActionState,EffectBlocked
from vlab_effects_v08 import begin_source_turn,end_source_turn,apply_weapon_attack,cast_source_specified_spell
from vlab_rd_v08 import Resistances
P={'F':copy.deepcopy(base.PROFILE['F1']),'E':copy.deepcopy(base.PROFILE['E']),'A':copy.deepcopy(base.PROFILE['A'])}
P['E']['attack_flat']=30
AUTHORITIES={'Combat':'3ebc2b324ede81f1be4be8804ac113c0','F':base.FERYN,'E':base.ERISTAN,'A':base.old.base.AUREN,'R42_R43':'3f3c2b324ede819496ddd7f93bd7e5d2'}

PREREG={'operation':'OP-VLAB-FUSION-SANDBOX-01','stage':'R151-R160','baseline':'R01-R150 frozen',
 'new_sessions':[
  {'id':'R156_TACTIC_FERYN_ERISTAN_S997601','seed':997601,'F':'BASIC','E':'SPORES','round_horizon':16},
  {'id':'R156_TACTIC_FERYN_ERISTAN_S997601_WIND','seed':997601,'F':'TURB','E':'SPORES','round_horizon':16}],
 'actors':'Feryn ON5 and Eristan ON5, independent Master-side proposals, NOT ED and not power benchmark',
 'initiative':'R26 documented 4d6+82 F, 4d6+30 E; DES tie, replay',
 'attack_mechanics':'v0.8.1 advanced physical and spell adapters; critical failure R42 LAB-ONLY only for normal physical',
 'F_BASIC':'4d6+92 normal 8d8+47 physical, E RD physical25',
 'F_TURB':'Turbilhao Cinzento 60PA Standard 9d10+8 WIND; E Reflexo 4d6+28 against 4d6+92; source line cone8m fixture',
 'E_SPORES':'Tempestade de Esporos 80PA Standard 10d10+10 Planta; F Fortitude 4d6+24 vs CD76; source radius5m/center<=25m fixture',
 'source_conditional':'NO E Wind RD or F Plant RD documented: lab0 assumption solely for conditional simulations, NOT official zero',
 'policy':'F picks basic or TURB per variant while PA available, else basic; E casts SPORES while PA>=80, else no legal offensive fallback established, horizon STOP_SOURCE_CAPACITY not forced victory',
 'no_waiver':'Every living active actor uses a source-legal offensive action if available. No deliberate standard forfeiture in active combat.',
 'complete':'HP0 winner and last turn END, or censored at 16 rounds; no extrapolated winner',
 'preserve':['R01–R150 immutable','R138 spatial parity hold','R123 R134 R143 UNKNOWN_EFFECT','R130 QA_FAIL','R124 5x5 CENSORED'],
 'holdout':'NONE; paired seed same across policies, NOT independent samples, development only'}

def canonical(obj):return json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def sha(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def proof(page,rule):return (FrozenRuleEvidence(page,rule,hashlib.sha256((page+'|'+rule+'|R151_REOPENED').encode()).hexdigest(),'2026-10-16_NOTION_READ','R151_LOCAL_EVIDENCE_POINTER_NONCANON'),)
def rolls(st,who,kind,ix,count,faces):return core.dice(st['seed'],ix,f'R151-{who}-{kind}',count,faces)
def prefile():
 p=ROOT/'R151_PREREG_TACTICAL.json'
 if p.exists():assert json.loads(p.read_text())==PREREG
 else:p.write_text(json.dumps(PREREG,sort_keys=True,ensure_ascii=False,indent=2)+'\n')
 return p

def init(runid,seed,variant,actors=('F','E')):
 out=ROOT/'runs'/f'{runid}.sqlite';out.parent.mkdir(exist_ok=True)
 if out.exists():raise ValueError('NO_REPEAT_RUN_DB')
 core.init_db(out,'A',seed)
 st=core.initial('A',seed);st.update({'scene':runid,'run_id':runid,'phase':'INIT','stage':'R151-R160','seed':seed,
  'order':[],'active':None,'round':0,'turn_index':0,'horizon':16,'action_nonce':{x:0 for x in actors},
  'teams':{'F':'F','E':'E','A':'A'},'winner':None,'variant':variant,
  'source_policy':sha(PREREG),'source_RD_assumptions':'WIND_PLANT_UNDOCUMENTED_LAB_RD0',
  'terminal_contracts':0,'scientific_comparison_only':True,'snapshots':'TECHNICAL_PROPOSAL_NOT_LIVE_CAMPAIGN',
  'authorities':AUTHORITIES})
 st['actors']={}
 for x in actors:
  p=P[x];pos='LAB-LINE-F' if x=='F' else 'LAB-LINE-E' if x=='E' else 'LAB-LINE-A'
  c=Combatant(x,p['hp'],p['pa'],p['ca'],p['con'],p['armor'],p['fort'],p['reflex'],pos,rank=p['rank'],standard=0,movement=0,reaction=1,maximum_hp=p['hp'],base_speed=p['speed'])
  st['actors'][x]={'source':p['source'],'source_profile':p,'resource':asdict(c)}
 anchor=sha({'genesis':st,'lineage':'R18_R26_V081_R151_ADDITIVE_TACTICAL'})
 with core.connect(out) as con:
  for k,v in [('scene',runid),('genesis',anchor),('head',anchor),('state',core.canonical(st))]:con.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
 out.with_suffix('.genesis.json').write_text(core.canonical(st)+'\n')
 return out

def initiative(st):
 rows=[]
 for who in st['actors']:
  p=P[who];d=rolls(st,who,'INIT',0,p['init_dice'],6)
  rows.append({'id':who,'dice':d,'total':sum(d)+p['init_bonus'],'des':p['dex'],'source':p['source']})
 def tie(who,n):return sum(rolls(st,who,'TIE',n,P[who]['init_dice'],6))+P[who]['init_bonus']
 return rows,r26.tie_order(rows,tie)

def physical_tape(st,who,target,origin='NORMAL',adv=0,dis=0):
 p=P[who];nonce=st['action_nonce'][who]+1;rr=st['actors'][who]['resource'];weak=rr['hp']*10<p['hp']
 net=max(-4,min(4,adv-dis-int(weak)))
 hit=[rolls(st,who,origin+'-HIT-'+str(i),nonce,p['attack_dice'],6) for i in range(1+abs(net))]
 score=(max(map(sum,hit))+2*net if net>0 else min(map(sum,hit))+2*net if net<0 else sum(hit[0]))+p['attack_flat']
 crit=[rolls(st,who,origin+'-CRIT-'+str(i),nonce,1,6)[0] for i in range(3)]
 d=[rolls(st,who,origin+'-DMG-'+str(i),nonce,n,f) for i,(n,f) in enumerate(p['damage_dice'])]
 return {'who':who,'target':target,'origin':origin,'nonce':nonce,'hit':hit,'score':score,'crit':crit,'damage_rolls':d,
  'damage':sum(map(sum,d))+p['damage_flat'],'adv':adv,'dis':dis,'weak':weak}

def magic_tape(st,who,target,which):
 p=P[who];nonce=st['action_nonce'][who]+1
 if which=='SPORES':
  dmg=rolls(st,who,'SPORES-DAMAGE',nonce,10,10)
  save=rolls(st,target,'SPORES-FORTITUDE',nonce,4,6);score=sum(save)+24;cd=76;cost=80
 elif which=='TURB':
  dmg=rolls(st,who,'TURB-DAMAGE',nonce,9,10)
  save=rolls(st,target,'TURB-REFLEX',nonce,4,6);score=sum(save)+28
  atk=rolls(st,who,'TURB-OFFENSE',nonce,4,6);cd=sum(atk)+92;cost=60
 else:raise ValueError(which)
 return {'who':who,'target':target,'which':which,'nonce':nonce,'dmg':dmg,'save':save,'save_score':score,'cd':cd,
   'attack_roll':atk if which=='TURB' else None,'raw':sum(dmg)+(10 if which=='SPORES' else 8),'cost':cost,'save_success':score>cd}

def source(st,who,target,which):
 pr=P[who];r=st['actors'][who]['resource'];spell=which in ('SPORES','TURB')
 kind='spell' if spell else 'attack';cost={'SPORES':80,'TURB':60}.get(which,0)
 name='R151_'+who+'_'+which
 sp=AbilitySource(name,kind,'STANDARD',pr['source'],which,'RULE-DERIVED',required_pa=cost,target_scope='ENEMY',effect_adapter_ready=True,effect_adapter_id='V081_R151_CONTROLLED_SOURCE')
 state=ActorActionState(who,pr['rank_index'],r['pa'],(name,),standard_available=r['standard']==1,movement_available=r['movement']==1,reaction_available=r['reaction']==1,
  range_confirmed=True,los_confirmed=True,geometry_confirmed=True,enemy_ids_visible=(target,))
 return sp,state,proof(pr['source'],which)

def validate(st,kind,p):
 a=st['active'];rr=st['actors'].get(a,{}).get('resource')
 if kind=='INIT':assert st['phase']=='INIT' and p=={'seed':st['seed']};return
 if st['phase']!='ACTIVE':raise ValueError('NOT_ACTIVE')
 if kind in ('START','END'):
  if p!={'actor':a} or rr['hp']<=0 and kind=='START':raise ValueError('TURN_ACTOR')
  if kind=='START' and rr['standard']!=0:raise ValueError('DUP_START')
  if kind=='END' and rr['standard']!=0:raise ValueError('UNSPENT_STANDARD_NOT_ALLOWED')
 elif kind=='STRIKE':
  if rr['standard']!=1 or rr['hp']<=0 or p.get('tape')!=physical_tape(st,a,p['tape']['target']):raise ValueError('TAPE_OR_ACTION')
 elif kind=='SPELL':
  t=p.get('tape',{});which=t.get('which');tar=t.get('target')
  if a!=t.get('who') or which not in ('TURB','SPORES') or (a=='F' and which!='TURB') or (a=='E' and which!='SPORES'):
   raise ValueError('SOURCE_SPELL')
  if t!=magic_tape(st,a,tar,which) or rr['standard']!=1 or rr['pa']<t['cost'] or st['actors'][tar]['resource']['hp']<=0:
   raise ValueError('SPELL_TAPE_OR_COST')
  if t['save_success'] and t['raw']%2:raise ValueError('ODD_HALF_HOLD')
 else:raise ValueError('UNKNOWN_KIND')

def commit(db,kind,p):
 st,head,rev=core.load(db);validate(st,kind,p)
 cmd='LAB-CMD-R151-'+sha({'run':st['run_id'],'rev':rev,'kind':kind,'payload':p})[:40]
 def red(c,p,seq):
  sc=Scene({x:Combatant(**v['resource']) for x,v in c['actors'].items()},seed=c['seed'],provenance='MESTRE_ONLY_V081_SOURCE_CONDITIONAL_R151')
  e=[];extra={};a=c['active']
  if kind=='INIT':
   rows,t=initiative(c);c.update({'order':t['order'],'active':t['order'][0],'phase':'ACTIVE','round':1});extra={'rows':rows,'tie':t}
  elif kind=='START':e.append(begin_source_turn(sc,a))
  elif kind=='END':
   e.append(end_source_turn(sc,a));c['turn_index']+=1
   living={x:c['teams'][x] for x,z in sc.actors.items() if z.hp>0};groups=set(living.values())
   if len(groups)<=1:
    c['phase']='FINISHED_HP0';c['winner']=next(iter(living),None);c['active']=None
   else:
    ind=c['order'].index(a)
    for inc in range(1,len(c['order'])+1):
     nxt=(ind+inc)%len(c['order']);target=c['order'][nxt]
     if sc.actors[target].hp>0:
      c['active']=target
      if nxt<=ind:c['round']+=1
      break
    if c['round']>c['horizon']:c['phase']='CENSORED_HORIZON';c['active']=None;c['winner']=None
  elif kind=='STRIKE':
   t=p['tape'];target=t['target'];spec,state,pr=source(c,a,target,'BASIC');pp=P[a]
   e.append(apply_weapon_attack(sc,a,target,source=spec,state=state,proofs=pr,roll_score=t['score'],damage=t['damage'],damage_tag='perfurante',
    rd=Resistances(general=P[target]['rd'],provenance='SOURCE_PHYSICAL_RD'),damage_dice_groups=tuple(map(tuple,pp['damage_dice'])),
    damage_roll_groups=tuple(map(tuple,t['damage_rolls'])),damage_fixed_bonus=pp['damage_flat'],critical_sequence=tuple(t['crit']),
    attack_roll_attempts=tuple(map(tuple,t['hit'])),attack_bonus=pp['attack_flat'],advantage_levels=t['adv'],disadvantage_levels=t['dis'],
    attack_origin=t['origin'],lab_negative_critical_policy=True))
   c['action_nonce'][a]+=1
  elif kind=='SPELL':
   t=p['tape'];target=t['target'];spec,state,pr=source(c,a,target,t['which'])
   e.append(cast_source_specified_spell(sc,a,target,source=spec,state=state,proofs=pr,damage=t['raw'],
    damage_tag='vento' if a=='F' else 'planta',rd=Resistances(general=0,specific=(),provenance='LAB_CONDITIONAL_UNDOCUMENTED_ELEMENTAL_RD0'),
    explicit_save_effect='SAVE-HALF',target_save_exceeds_cd=t['save_success'],damage_rolls=tuple(t['dmg']),damage_faces=10,documented_flat_bonus=(10 if a=='E' else 8)))
   c['action_nonce'][a]+=1;extra={'save_rolls':t['save'],'save_score':t['save_score'],'save_cd':t['cd'],'single_target_metric_fixture':True,
   'source_RD_uncertain':True,'not_official_RD0':True}
  for who,x in sc.actors.items():
   r=asdict(x);r['ca']=int(r['ca']);r['base_speed']=int(r['base_speed']) if r['base_speed'] is not None else None
   c['actors'][who]['resource']=r
  return {'engine':'R18_R26_V081_R151_CONTROLLED','native_actions':e,'extra':extra,'LAB_ONLY':True,
  'contracts':['ACTION_CATALOG_AIN01','ED_VS_BE_DAMAGE','TACTICAL_AI_AB_FAIRNESS','RNG_REPLAY_STATISTICS']}
 return core.event_commit(db,cmd,kind,p,red)

def battle(runid,seed,variant,horizon=16):
 db=init(runid,seed,variant)
 commit(db,'INIT',{'seed':seed})
 reason='';actions=[]
 while True:
  st,head,rev=core.load(db)
  if st['phase']!='ACTIVE':break
  if rev>=horizon*8+4:reason='SAFETY_MAX';break
  who=st['active'];other='E' if who=='F' else 'F'
  commit(db,'START',{'actor':who})
  st,_,_=core.load(db)
  if st['actors'][other]['resource']['hp']<=0:raise ValueError('STOP_ON_KO')
  if who=='F' and variant=='TURB' and st['actors']['F']['resource']['pa']>=60:
   t=magic_tape(st,'F','E','TURB');kind='SPELL'
  elif who=='E' and st['actors']['E']['resource']['pa']>=80:
   t=magic_tape(st,'E','F','SPORES');kind='SPELL'
  elif who=='F':t=physical_tape(st,'F','E');kind='STRIKE'
  else:
   reason='NO_E_SOURCE_OFFENSIVE_WITH_AVAILABLE_PA';break
  try:commit(db,kind,{'tape':t})
  except ValueError as exc:
   reason='SOURCE_GATE_'+str(exc);break
  actions.append({'round':st['round'],'actor':who,'action':t.get('which','BASIC')})
  commit(db,'END',{'actor':who})
 st,head,rev=core.load(db)
 with sqlite3.connect(db) as con:
  rows=[json.loads(x[0]) for x in con.execute('SELECT row_json FROM events ORDER BY seq')]
  pending=con.execute('SELECT COUNT(*) FROM pending').fetchone()[0]
 with sqlite3.connect(db) as src,sqlite3.connect(db.with_suffix('.checkpoint.sqlite')) as dst:src.backup(dst)
 assert core.load(db)==core.load(db.with_suffix('.checkpoint.sqlite'))
 events=[ev for row in rows for ev in row['detail']['native_actions']]
 return {'run_id':runid,'seed':seed,'variant':variant,'phase':st['phase'],'winner':st['winner'],'rev':rev,
  'stop':reason,'pending':pending,'rounds':st['round'],'actions':actions,
  'native_events':len(events),'phys_attacks':sum(e['action']=='weapon_attack' for e in events),'spells':sum(e['action']=='spell' for e in events),
  'critical_negative':sum(e.get('critical')=='NEGATIVE' for e in events),'critical_positive':sum(e.get('critical')=='POSITIVE' for e in events),
  'effective_damage':sum(e.get('hp_loss_actual',e.get('hp_before',0)-e.get('hp_after',0) if e['action']=='spell' else 0) for e in events),
  'pa_spent':sum(e.get('PA_spent',0) for e in events),'hp_final':{x:z['resource']['hp'] for x,z in st['actors'].items()},
  'pa_final':{x:z['resource']['pa'] for x,z in st['actors'].items()},'head':head,'checkpoint_equal':True}

if __name__=='__main__':
 prefile();out=[]
 for it in PREREG['new_sessions']:out.append(battle(it['id'],it['seed'],it['F'],it['round_horizon']))
 (ROOT/'R156_TACTICAL_RESULTS.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(out,indent=2,ensure_ascii=False))
