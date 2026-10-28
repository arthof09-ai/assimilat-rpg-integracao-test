"""R93 ADDITIVE MESTRE-SIDE 2x1. Uses historic R18 atomic SQLite + R26 initiative/turn refresh.
No movement, no AoO, no NPC Party edits. Source-frozen policy: V(Auren) and R(Feryn)
are allied vs F(Grifo); Beast targets fragile tracker first, party both target Beast.
Auren single-combat Duelist +15 does NOT activate in 2x1 (193-15=178).
"""
from pathlib import Path
import json,copy,sys,sqlite3
ROOT=Path(__file__).resolve().parent
HIST=ROOT.parent/'r61_extracted';sys.path.insert(0,str(HIST/'work'))
import r52_r61_engine as h
core=h.core
FROZEN=json.loads((ROOT/'R93_TEAM_FREEZE.json').read_text())
PREREG=json.loads((ROOT/'R93_PREREG_TEAM.json').read_text())
ACT=('F','V','R')
class Deny(RuntimeError):pass

def alive(s,a):return s['actors'][a]['resource']['hp']>0

def target(s,a):
    if a=='F':return next((x for x in ('R','V') if alive(s,x)),None)
    return 'F' if alive(s,'F') else None

def winner(s):
    if not alive(s,'F'):return 'TEAM_ED_NPC'
    if not alive(s,'R') and not alive(s,'V'):return 'BEAST'
    return None

def create(db,seed,side):
    if db.exists():raise FileExistsError('NO_REPEAT')
    for a,p in FROZEN['profiles'].items():
        h.SOURCES['R93_'+a]={'name':p['name'],'rank_dice':p['rank_dice'],'des':p['des'],
            'hp':p['hp'],'ca':p['ca'],'rd':p['rd'],'pa':p['pa'],
            'initiative_bonus':p['init_bonus'],'attack_bonus':p['attack_bonus'],
            'damage_dice':p['damage_dice'],'damage_bonus':p['damage_bonus'],'dodge_defense':None}
    s=h.snapshot('FIGHT',{a:'R93_'+a for a in ACT},seed,'R93-TEAM')
    s['scene']='R93-TEAM-'+str(seed)
    s['run_id']='R93-2X1-'+str(seed)+'-'+side
    s['factions']={'BEAST':['F'],'TEAM':['V','R']}
    s['lab_type']='SOURCE_BOUNDED_TEAM_2X1_BASIC_ONLY'
    s['experiment']={'seed':seed,'side':side,'no_movement':True,'team_target_order':'F attacks R then V; V/R attack F',
        'no_reactions_declared':True,'source_sha':core.sha(FROZEN['profiles']),
        'no_duel_bonus_in_team':True,'source_admission':'SOURCE_BOUND_2X1_BASIC_INIT_LIMITED'}
    if side=='F_LEFT':positions={'F':[0.,0.],'V':[1.5,0.],'R':[0.,1.5]}
    elif side=='F_RIGHT':positions={'F':[1.5,0.],'V':[0.,0.],'R':[1.5,1.5]}
    else:raise Deny('BAD_SIDE')
    for a in ACT:s['actors'][a]['resource']['position']=positions[a]
    s['action_id']={a:0 for a in ACT}
    s['policy']['predeclared_team_factions']='F vs (V,R)'
    s['policy']['positive_PA']='DENY';s['policy']['movement']='DENY';s['policy']['counter']='NONE_DECLARED'
    s['policy']['canonical_writes']=0
    core.init_db(db,'A',seed)
    digest=core.sha({'source':FROZEN['profiles'],'scene':s['scene'],'r18':core.VERSION,'id':s['run_id']})
    with core.connect(db) as con:
        con.execute('BEGIN IMMEDIATE')
        for k,v in [('scene',s['scene']),('state',core.canonical(s)),('head',digest),('genesis',digest)]:con.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
    db.with_suffix('.genesis.json').write_text(core.canonical(s)+'\n')

def preflight(s,kind,p):
    if kind=='INIT':
        if s['phase']!='INIT' or p!={'action':'INIT'}:raise Deny('INIT_BEFORE_INTENT')
        return
    if kind=='TEAM_TURN':
        if s['phase']!='ACTIVE' or s['active'] not in ACT or p!={'actor':s['active'],'target':target(s,s['active']),'reaction':'NONE'}:raise Deny('TARGET_PRE_INTENT')
        a=p['actor'];b=p['target'];ra=s['actors'][a]['resource'];rb=s['actors'][b]['resource']
        if ra['standard']!=1 or ra['hp']<=0 or rb['hp']<=0:raise Deny('ACTION_SLOT_PRE_INTENT')
        if sum((v-w)**2 for v,w in zip(ra['position'],rb['position']))>1.500001**2:raise Deny('RANGE_PRE_INTENT')
        if FROZEN['profiles'][a]['attack_pa']!=0:raise Deny('PA_PRE_INTENT')
        return
    if kind=='CENSOR':
        if s['phase']!='ACTIVE' or p!={'horizon':PREREG['horizon']}:raise Deny('CENSOR_PRE_INTENT')
        return
    raise Deny('UNKNOWN_KIND')

def commit(db,kind,p,runner):
    s,head,rev=core.load(db);preflight(s,kind,p)
    cmd='LAB-CMD-R93-'+core.sha({'head':head,'kind':kind,'payload':p,'id':s['run_id']})[:35]
    return core.event_commit(db,cmd,kind,p,runner)

def init(s,p,seq):
    out=h.begin(s,p,seq)
    return {'scheduler':out,'factions':s['factions'],'active':s['active'],'order':s['order'][:]}

def turn(s,p,seq):
    a=p['actor'];b=p['target'];before={x:{k:s['actors'][x]['resource'][k] for k in ('hp','pa','reaction','standard','movement')} for x in ACT}
    before_active=s['active'];before_round=s['round'];before_turn=s['turn'];s['action_id'][a]+=1
    fx=h.exchange(s,a,b,'NONE')
    if fx['reply'] is not None:raise Deny('UNDECLARED_COUNTER')
    outcome=winner(s)
    if outcome:
        s['phase']='COMPLETE';s['winner']=outcome;s['active']=None
        change={'complete':True,'winner':outcome,'sides_alive':{'BEAST':alive(s,'F'),'TEAM':alive(s,'V') or alive(s,'R')}}
    else:
        change=h.advance(s)
    after={x:{k:s['actors'][x]['resource'][k] for k in ('hp','pa','reaction','standard','movement')} for x in ACT}
    return {'actor':a,'target':b,'source':s['actors'][a]['source'],'turn_before':before_turn,'round_before':before_round,
      'before':before,'exchange':fx,'after':after,'transition':change,'active_after':s['active'],'round_after':s['round'],
      'faction_winner':outcome,'actions':s['action_id'].copy(),'positive_PA':0,'policy':s['experiment']['team_target_order']}

def censor(s,p,seq):
    s['phase']='CENSORED_HORIZON';s['winner']=None;s['active']=None
    return {'censored':True,'winner':None,'horizon':p['horizon']}

def run(seed,side):
    targetdir=ROOT/'team_runs';targetdir.mkdir(exist_ok=True)
    db=targetdir/f'R93TEAM_{seed}_{side}.sqlite';create(db,seed,side)
    commit(db,'INIT',{'action':'INIT'},init)
    turns=0
    while turns<PREREG['horizon']:
        s,head,rev=core.load(db)
        if s['phase']!='ACTIVE':break
        p={'actor':s['active'],'target':target(s,s['active']),'reaction':'NONE'}
        commit(db,'TEAM_TURN',p,turn);turns+=1
    else:
        s,_,_=core.load(db)
        if s['phase']=='ACTIVE':commit(db,'CENSOR',{'horizon':PREREG['horizon']},censor)
    cp=db.with_suffix('.checkpoint.sqlite')
    with sqlite3.connect(db) as con,sqlite3.connect(cp) as bk:
        con.backup(bk)
    assert core.load(db)==core.load(cp)
    s,head,rev=core.load(db)
    with sqlite3.connect(db) as con:
        events=[json.loads(r[0]) for r in con.execute('SELECT row_json FROM events ORDER BY seq')]
    fx=[ev['detail']['exchange']['normal'] for ev in events if ev['kind']=='TEAM_TURN']
    return {'run_id':s['run_id'],'seed':seed,'side':side,'phase':s['phase'],'winner':s['winner'],'turns':turns,
        'rounds':s['round'],'events':rev,'attacks':len(fx),'hits':sum(a['hit'] for a in fx),
        'by_actor':{a:{'attacks':sum(x['actor']==a for x in fx),'hits':sum(x['actor']==a and x['hit'] for x in fx)} for a in ACT},
        'hp_end':{a:s['actors'][a]['resource']['hp'] for a in ACT},'head':head,'ledger':db.name,'checkpoint':cp.name,
        'cannon_writes':0,'source_admissibility':'SOURCE_BOUND_BASIC_2X1_INIT_SCENARIO'}

if __name__=='__main__':
    res=[]
    for phase,seeds in PREREG['seeds'].items():
        for seed in seeds:
            for side in PREREG['sides']:
                one=run(seed,side);one['cohort']=phase;res.append(one)
    (ROOT/'R93_TEAM_RESULTS.json').write_text(core.canonical(res)+'\n')
    print(json.dumps({'runs':len(res),'events':sum(x['events'] for x in res),'attacks':sum(x['attacks'] for x in res),'matches':[{k:r[k] for k in ('seed','side','winner','turns','events','hp_end')} for r in res]},indent=2))
