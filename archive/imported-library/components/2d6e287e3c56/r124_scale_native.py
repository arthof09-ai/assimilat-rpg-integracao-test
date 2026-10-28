"""Stage R124 progressive technical scale of the SAME v0.8.1/R18/R26 gateway.
No new creature or power profile: identical technical copies of Auren and Feryn.
This is NOT canonical 5x5/10x10/20x20 combat coverage.
"""
import sys,json,sqlite3,copy
from pathlib import Path
from hashlib import sha256
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import r119_integrated_three_actor as r
BASE_PROFILES=copy.deepcopy(r.PROFILES)
import vlab_r18_interactive as core
PREREG={'operation':'OP-VLAB-FUSION-SANDBOX-01','baseline':'R01-R117 IMMUTABLE','stage':'R124_SCALE_TECH',
 'tiers':[{'size':5,'seed':938211,'max_turns':24},{'size':10,'seed':938311,'max_turns':45},
          {'size':20,'seed':938411,'max_turns':85}],
 'source':'Auren L3 + Feryn ON5 reference profiles used as labelled technical clones, NO new NPCs',
 'mechanical_scope':'same R119 copied native v081+R18 event_commit+R26 order; basic normal attack, native defense/counter and KO skip',
 'no_official_combat':True,'no_source_species_multiplied':True,'no_terminal_certificates':True,
 'limits':['no physical arena geometry','no positional movement','no simultaneous trigger priority',
           'no spell/PA in scale tier','Feryn lower rank NPC, not ED or balanced power comparison',
           'on negative crit block before intent; do not retry same file'],
 'family':'DEVELOPMENT_TECH_SCALE_NOT_HOLDOUT'}
p=ROOT/'R124_PREREG_SCALE.json'
if p.exists():assert json.loads(p.read_text())==PREREG
else:p.write_text(json.dumps(PREREG,indent=2,ensure_ascii=False)+'\n')

def profile_setup(size):
 profiles={};teams={}
 for i in range(1,size+1):
  a=f'A{i:02d}';f=f'F{i:02d}'
  profiles[a]=copy.deepcopy(BASE_PROFILES['A']);profiles[f]=copy.deepcopy(BASE_PROFILES['F1'])
  teams[a]='ONE';teams[f]='TWO'
 return profiles,teams

def target_policy(st,actor):
 enemy='TWO' if st['teams'][actor]=='ONE' else 'ONE'
 return sorted([a for a in st['actors'] if st['teams'][a]==enemy and st['actors'][a]['resource']['hp']>0])[0]

def reaction_policy(st,actor,target):
 if st['actors'][target]['resource']['reaction']!=1:return 'NONE'
 if st['teams'][target]=='ONE':return 'COUNTER'
 return 'ESQUIVAR' if int(target[1:])%2 else 'DEFENDER'

results=[]
original_profiles,original_teams=r.PROFILES,r.TEAM_MAP
for item in PREREG['tiers']:
 size=item['size'];seed=item['seed'];r.PROFILES,r.TEAM_MAP=profile_setup(size)
 file=ROOT/'runs'/f'R124_TECH_SCALE_{size}X{size}_S{seed}.sqlite'
 if file.exists():
  # The 5x5 was already executed and censored in the prior attempt; read ONLY.
  st,_,_=core.load(file);count=st['turn_index']
  censored='NEGATIVE_CRITICAL_PRE_INTENT_FROM_FIRST_EXECUTION_RETAINED' if st['phase']=='ACTIVE' else None
 else:
  r.init_db(file,seed);r.command(file,'INIT',{'seed':seed})
  count=0;censored=None
  while count<item['max_turns']:
   st,_,_=core.load(file)
   if st['phase']!='ACTIVE':break
   actor=st['active'];r.command(file,'START',{'actor':actor});st,_,_=core.load(file)
   target=target_policy(st,actor);at=r.atk_payload(st,actor,target)
   policy=reaction_policy(st,actor,target)
   payload={'attack':at,'reaction':policy,'attack_origin':'NORMAL'}
   if policy=='COUNTER':payload['counter']=r.counter_payload(st,target,actor)
   try:r.command(file,'STRIKE',payload)
   except r.Hold as exc:
    if 'CRITICAL_FAILURE_UNRESOLVED_PRE_INTENT' in str(exc) or 'COUNTER_CRITICAL_FAILURE_PRE_INTENT' in str(exc):
     censored=str(exc);break
    raise
   r.command(file,'END',{'actor':actor});count+=1
 st,head,revision=core.load(file)
 ck=file.with_suffix('.checkpoint.sqlite')
 if not ck.exists():
  with sqlite3.connect(file) as c1, sqlite3.connect(ck) as c2:c1.backup(c2)
 assert core.load(file)==core.load(ck)
 with sqlite3.connect(file) as c:events=[json.loads(x[0]) for x in c.execute('select row_json from events order by seq')]
 effects=[a for ev in events for a in ev['detail']['native_actions']]
 result={'size':f'{size}x{size}','instances':2*size,'distinct_source_profiles':2,
  'seed':seed,'run_id':st['run_id'],'phase':st['phase'] if censored is None else 'CENSORED_BEFORE_INTENT',
  'censor':censored,'winner':st['winner'],'actor_turns':count,'round':st['round'],
  'events':revision,'head':head,'basic_attacks':sum(x['action']=='weapon_attack' for x in effects),
  'reaction_events':sum(x['action'] in ('ESQUIVAR','DEFENDER','COUNTER_DECLARE') for x in effects),
  'counter_responses':sum(x['action']=='COUNTER_RESPONSE' for x in effects),
  'hp_zero_count':sum(a['resource']['hp']==0 for a in st['actors'].values()),
  'checkpoint':ck.name,'file':file.name,'official_credit':0}
 results.append(result)
r.PROFILES,r.TEAM_MAP=original_profiles,original_teams
(ROOT/'R124_SCALE_EXECUTIONS.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False,indent=2))
