"""New, separate species L3 Crocodile vs ED Auren 1x1; original R18/v0.8.1 driver reused, not a new motor.
Crocodile initiative is exogenously fixed; not official evidence. No new post-dice choices.
"""
from pathlib import Path
import sys,json,sqlite3,hashlib
from dataclasses import asdict
HERE=Path(__file__).resolve().parent
BASE=Path('/mnt/data/vlab_r161_work/baseline_r160/r151_r160')
sys.path.insert(0,str(BASE))
import r159_ed_besta_native as b
b.SRC['B']={'name':'Crocodilo de Lodo Astral Ancião L3','page':'3f3c2b324ede813987deda0b382e83c7',
 'hp':5580,'pa':3625,'ca':112,'con':140,'reflex':0,'rd':75,'speed':50,'rank':'Lendário',
 'rank_index':23,'atk':[6,6,134],'dmg':[[20,10]],'flat':0,'tag':'perfurante'}
b.SOURCE_TEXT['B']='Crocodilo L3 P3-02|Vida5580|PA3625|CA112|RD75|Mordida 6d6+134|Mordida de Lodo 20d10 perfurante/impacto físico|Iniciativa individual NÃO demonstrada'
PREREG={'operation':'OP-VLAB-FUSION-SANDBOX-01','baseline':'R01-R160 locked','experimental_scenario':'Crocodilo de Lodo Astral Ancião L3 vs Auren L3',
 'source_beast':'3f3c2b324ede813987deda0b382e83c7','source_auren':'3ebc2b324ede814bb730d47dd7bd5f02',
 'development_seed':1168001,'reserved_nonblind_seed':1169001,
 'family':'LAB_CONDITIONAL_NOT_CANON','independent_holdout':False,
 'starting_state':'Full documented HP, free PA and physical RD; 1.5m adjacent lab positioning; exogenous Besta first; no natural Besta Initiative claim',
 'combat_policy':'Each active living actor makes 1 eligible documented physical melee attack per turn; no deliberate passes; no unspecified special/aoo; LAB_ONLY R42 negative critical',
 'B_attack':'Crocodilo mordida 6d6+134, 20d10 physical piercing/impact; vs Auren physical RD35 and CA225',
 'E_attack':'Auren lance 6d6+193, 8d8+211 physical; vs Crocodile physical RD75 and CA112; documented duel +8 from third own attack',
 'scope':'Physical common RD only; piercing/impact physical common applicability; no material RD zero for element',
 'horizon_actor_turns':120,'end':'HP0 or censorship; do not infer official strength hierarchy',
 'do_not_repeat':['R159 Grifo 998803','R93/R95 historical','R01-R160','any R16x existing ID']}
PREREG_PATH=HERE/'R168_PREREG_CROCODILE_ED.json'
if not PREREG_PATH.exists():PREREG_PATH.write_text(json.dumps(PREREG,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
else:assert json.loads(PREREG_PATH.read_text())==PREREG

def init(path,seed):
 if path.exists():raise RuntimeError('NO_REPEAT_DB')
 b.core.init_db(path,'A',seed)
 s=b.core.initial('A',seed)
 s.update({'scene':path.stem,'run_id':path.stem,'test_mode':'NATIVE_V081_SOURCE_CONDITIONAL_R168',
 'stage':'R168','phase':'ACTIVE','seed':seed,'order':['B','E'],'active':'B','turn_index':0,
 'action_indexes':{'B':0,'E':0},'special_used_count':0,'winner':None,
 'source_digest':b.core.sha(b.SOURCE_TEXT),'experiment':{'scene':'G_FULL','opening':'EXOGENOUS_BESTA_FIRST_NOT_NATURAL_INIT','side':'CROC_BASIC_ONLY',
 'source_RD':'PHYSICAL_35_AND_75','terminal':False,'no_elemental_assumption':True,
 'compared_as_independent_seed':False,'runid_unique':path.stem}})
 actors={}
 for actor in s['order']:
  p=b.profile(actor)
  c=b.Combatant(actor,p['hp'],p['pa'],p['ca'],p['con'],0,0,p['reflex'],f'CROC_SOURCE_ADJACENT_1.5m-{actor}',rank=p['rank'],standard=0,
                maximum_hp=p['hp'],base_speed=p['speed'],beast_rank_index=p['rank_index'] if actor=='B' else None)
  v=asdict(c)
  for k in ('ca','base_speed'):v[k]=int(v[k]) if v[k] is not None else None
  actors[actor]={'source':p['page'],'stats':{'rank':p['rank'],'damage':p['dmg'],'att':p['atk'],'label':p['name']},'resource':v}
 s['actors']=actors
 genesis=b.core.sha({'genesis':s,'source_digest':s['source_digest'],'engine':'R18+NATIVE_V081_CONTROLLED_R168'})
 with b.core.connect(path) as con:
  for k,v in [('scene',s['scene']),('head',genesis),('genesis',genesis),('state',b.core.canonical(s))]:con.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
 path.with_suffix('.genesis.json').write_text(b.core.canonical(s)+'\n')
 return path

def duel(seed,family):
 db=HERE/'runs'/f'R168_ED_AUREN_VS_CROC_BASIC_{family}_S{seed}.sqlite';init(db,seed)
 while True:
  s,head,rev=b.core.load(db)
  if s['phase']!='ACTIVE' or s['turn_index']>=PREREG['horizon_actor_turns']:break
  actor=s['active'];target='E' if actor=='B' else 'B'
  b.commit(db,'TURN_START',{'actor':actor})
  s,_,_=b.core.load(db)
  tape=b.attack_inputs(s,actor,target)
  b.commit(db,'NATIVE_ATTACK',tape)
  b.commit(db,'TURN_END',{'actor':actor})
 s,h,r=b.core.load(db)
 with sqlite3.connect(db) as con:
  rows=[json.loads(t[0]) for t in con.execute('SELECT row_json FROM events ORDER BY seq')]
  pending=con.execute('SELECT COUNT(*) FROM pending').fetchone()[0]
 with sqlite3.connect(db) as src,sqlite3.connect(db.with_suffix('.checkpoint.sqlite')) as dest:src.backup(dest)
 assert b.core.load(db)==b.core.load(db.with_suffix('.checkpoint.sqlite')) and pending==0
 acts=[t['detail']['native_action'] for t in rows if t['kind']=='NATIVE_ATTACK']
 assert len(rows)==3*len(acts)
 out={'run':db.stem,'seed':seed,'family':family,'phase':s['phase'] if s['phase']!='ACTIVE' else 'CENSORED_HORIZON',
 'winner':s['winner'] if s['phase']!='ACTIVE' else None,'turns':s['turn_index'],'R18_commits':r,
 'attack_receipts':len(acts),'physical_hit':sum(e['hit'] for e in acts),'Auren_attacks':sum(e['from']=='E' for e in acts),
 'Croc_attacks':sum(e['from']=='B' for e in acts),'Croc_hits':sum(e['from']=='B' and e['hit'] for e in acts),
 'negative_lab_criticals':sum(e['critical']=='NEGATIVE' for e in acts),'positive_criticals':sum(e['critical']=='POSITIVE' for e in acts),
 'post_RD':sum(e['net'] for e in acts),'hp_effective':sum(e['hp_loss_actual'] for e in acts),'overkill':sum(e['overkill'] for e in acts),
 'final_hp':{k:v['resource']['hp'] for k,v in s['actors'].items()},'checkpoint_equal':True,'pending':pending,'head':h,
 'source_limitation':['Besta Initiative exogenous','Physical damage tag piercing/impact shared physical RD','not independent blind holdout','no special attacks']}
 return out
if __name__=='__main__':
 results=[duel(PREREG['development_seed'],'DEV'),duel(PREREG['reserved_nonblind_seed'],'RESERVED_NONBLIND')]
 (HERE/'R168_ED_CROCODILE_RESULTS.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(results,ensure_ascii=False,indent=2))
