"""Additive 1x1 VLAB benchmark adapter using original R18 sqlite transactions and R26 turn authority.
No modifications to source R18/R26/R52/R71 files. No network, no canonical writes.
Authentic sources (one Besta and one ED) frozen in fixture_r73_source_freeze.json.
Capanga RD0 is CONDITIONAL; no canonical assertion or promotion.
"""
from __future__ import annotations
import copy,hashlib,json,math,sqlite3,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
HIST=ROOT.parent/'r61_extracted'
sys.path.insert(0,str(HIST/'work'))
import r52_r61_engine as history
core=history.core
r26=history.r26
FIXTURE=json.loads((ROOT/'R92_SOURCE_FREEZE.json').read_text())
PREREG=json.loads((ROOT/'R92_PREREG_1X1.json').read_text())
PROFILE={}
MATCHUP={}
def configure(matchup):
    global PROFILE,MATCHUP
    MATCHUP=matchup
    PROFILE={a:FIXTURE['profiles'][matchup[a]] for a in ('B','E')}
    if PROFILE['B']['kind'] not in ('Besta','Besta Titã'):raise Deny('B_NOT_BESTA')
    if 'Espiritualista' not in PROFILE['E']['kind']:raise Deny('E_NOT_SPIRITUALIST_CANDIDATE')
class Deny(RuntimeError):pass

def canon(o):return core.canonical(o)
def sh(o):return core.sha(o)
def profile_sha():return sh(PROFILE)
def alive(s,a):return s['actors'][a]['resource']['hp']>0

def start(db,seed,side):
    if side not in PREREG['sides']:raise Deny('UNKNOWN_SIDE')
    if db.exists():raise FileExistsError('NO_REPEAT_EXISTING_SQLITE')
    # history reads its SOURCES when deriving its snapshot; this is a local in-process
    # adapter registry, not a mutation of any historical source file or persistent engine.
    for a,p in PROFILE.items():
        history.SOURCES['BENCH_'+a]={'name':p['name'],'rank_dice':p['rank_dice'],'des':p['des'],
          'hp':p['hp'],'ca':p['ca'],'rd':p['rd'],'pa':p['pa'],'initiative_bonus':p['initiative_bonus'],
          'attack_bonus':p['attack_bonus'],'damage_dice':p['damage_groups'][0],
          'damage_bonus':p['damage_bonus'],'dodge_defense':None}
    s=history.snapshot('DIRECTED',{a:'BENCH_'+a for a in ('B','E')},seed,'R92BENCH')
    s['phase']='INIT'
    s['scene']=f'BENCH-R92-{MATCHUP["id"]}-{seed}'  # same RNG label on sides
    s['run_id']=f'R92R101_{MATCHUP["id"]}_{seed}_{side}'
    s['lab_type']='SOURCE_BOUNDED_ONE_VS_ONE_MATCHED_L3_R92'
    s['source_gate']={'sha':profile_sha(),'admission':MATCHUP['admission'],'official':False,'matched_source_ids':[PROFILE['B']['id'],PROFILE['E']['id']]}
    s['experiment']={'seed':seed,'side':side,'no_movement':True,'no_reaction':True,
      'horizon':PREREG['horizon'],'rank_mismatch':PROFILE['B']['rank']!=PROFILE['E']['rank'],'matchup':[PROFILE['B']['rank'],PROFILE['E']['rank']],
      'benchmark_grid':'PLAN-SIM-DMG-VLAB-01/'+MATCHUP['id'],'admission':MATCHUP['admission'],'matchup_id':MATCHUP['id']}
    s['policy']['schema']='BENCH-A-R92-R101_SOURCE_BOUND_L3'
    s['policy']['rng_label_source_identity']=True
    s['policy']['PA_positive']='DENY'
    s['policy']['max_turns']=PREREG['horizon']
    s['policy']['reactions']='NONE_DECLARED'
    s['policy']['critical']='R52_R50_R51_SCOPED'
    s['actors']['B']['resource']['position']=[0.,0.] if side=='B_LEFT' else [1.5,0.]
    s['actors']['E']['resource']['position']=[1.5,0.] if side=='B_LEFT' else [0.,0.]
    s['action_id']={a:0 for a in ('B','E')}
    core.init_db(db,'A',seed)
    head=sh({'scene':s['scene'],'source_sha':profile_sha(),'r18':core.VERSION,'r26_module':'HISTORIC','mode':'LAB_SOURCE_BOUNDED_R82'})
    con=core.connect(db)
    try:
        con.execute('BEGIN IMMEDIATE')
        for k,v in [('scene',s['scene']),('state',canon(s)),('head',head),('genesis',head)]:con.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
        con.commit()
    except:con.rollback();raise
    finally:con.close()
    (db.parent/(db.stem+'.genesis.json')).write_text(canon(s)+'\n')

def validate_command_pre_intent(s,kind,payload):
    # This validation MUST run before durable R18.pending insert. Validations in
    # runner alone are too late for rejected user commands and create UNKNOWN_EFFECT.
    if kind=='INIT':
        if s['phase']!='INIT' or payload!={'operation':'INIT'}:raise Deny('INIT_PRE_INTENT')
    elif kind=='NORMAL_ATTACK':
        a=s['active'];b='E' if a=='B' else 'B'
        if s['phase']!='ACTIVE' or payload!={'actor':a,'target':b,'reaction':'NONE'}:
            raise Deny('ATTACK_PAYLOAD_PRE_INTENT')
        if any(not alive(s,x) for x in (a,b)) or s['actors'][a]['resource']['standard']!=1:
            raise Deny('ATTACK_SLOT_ALIVE_PRE_INTENT')
        ra=s['actors'][a]['resource'];rb=s['actors'][b]['resource']
        if math.dist(ra['position'],rb['position'])>1.500001:raise Deny('ATTACK_RANGE_PRE_INTENT')
        if PROFILE[a]['attack_pa']!=0:raise Deny('PA_SOURCE_PRE_INTENT')
    elif kind=='TURN_END':
        if s['phase']!='ACTIVE' or payload!={'actor':s['active']} or s['actors'][s['active']]['resource']['standard']!=0:
            raise Deny('TURN_END_PRE_INTENT')
    elif kind=='CENSOR':
        if s['phase']!='ACTIVE' or payload!={'horizon':PREREG['horizon']}:raise Deny('CENSOR_PRE_INTENT')
    else:raise Deny('UNKNOWN_COMMAND_PRE_INTENT')

def commit(db,kind,payload,runner):
    s,head,rev=core.load(db)
    validate_command_pre_intent(s,kind,payload)
    command='LAB-CMD-R92-'+sh({'scene':s['scene'],'head':head,'rev':rev,'kind':kind,'p':payload})[:40]
    return core.event_commit(db,command,kind,payload,runner)

def do_init(s,p,seq):
    if s['phase']!='INIT' or p!={'operation':'INIT'} or seq!=1:raise Deny('INIT_GATE')
    rows=[];tapes=[]
    for a in ('B','E'):
        prof=PROFILE[a]
        t=history.roll(s['seed'],0,'BENCH-R92-INIT-'+a,*prof['rank_dice'])
        score=sum(t['dice'])+prof['initiative_bonus']
        rows.append({'id':a,'total':score,'des':prof['des']});tapes.append({'actor':a,**t,'score':score})
    tie=[]
    def reroll(a,k):
        pp=PROFILE[a];t=history.roll(s['seed'],k,'BENCH-R92-INIT-TIE-'+a+'-'+str(k),*pp['rank_dice']);tie.append({'actor':a,**t});return sum(t['dice'])+pp['initiative_bonus']
    order=r26.tie_order(rows,reroll)
    s['order']=order['order'];s['active']=s['order'][0];s['phase']='ACTIVE';s['round']=1;s['turn']=0
    ref=r26.refresh_own_turn(s,s['active'])
    s['turn_history'].append({'event':'START','actor':s['active'],'round':1})
    return {'initiatives':tapes,'order':s['order'][:],'tie':tie,'r26':order,'refresh':ref}

def attack(s,a,b):
    if a==b or a not in PROFILE or b not in PROFILE:raise Deny('IDENTITY')
    ra=s['actors'][a]['resource'];rb=s['actors'][b]['resource']
    if ra['standard']!=1 or not alive(s,a) or not alive(s,b):raise Deny('PRE_ATTACK_SLOT_OR_ALIVE')
    if math.dist(ra['position'],rb['position'])>1.500001:raise Deny('UNAUTHORIZED_NONADJACENT_ATTACK')
    if PROFILE[a]['attack_pa']!=0:raise Deny('POSITIVE_PA_UNDOCUMENTED')
    ra['standard']=0;s['action_id'][a]+=1;idx=s['action_id'][a];p=PROFILE[a]
    label=f'BENCH-R92-{s["scene"]}-{a}-{b}-NORMAL-{idx}'
    crit=[history.roll(s['seed'],idx,label+'-CRIT-'+str(i),1,6) for i in (1,2,3)]
    c=[t['dice'][0] for t in crit];plus=c[:2]==[6,6] and c[2]>=5;minus=c[:2]==[1,1] and c[2]<=2
    h=history.roll(s['seed'],idx,label+'-HIT',*p['rank_dice'])
    passive_bonus=(8 if a=='E' and p.get('duel_bonus_after_two_own_turns',False) and idx>=3 else 0)
    score=sum(h['dice'])+p['attack_bonus']+passive_bonus;hit=bool(not minus and (plus or score>rb['ca']))
    tape=crit+[h];dmg_tape=[];raw=potential=actual=0;pre=rb['hp']
    if hit:
        for i,(count,faces) in enumerate(p['damage_groups']):
            t=history.roll(s['seed'],idx,label+'-DAMAGE-'+str(i),count,faces);dmg_tape.append(t)
        raw=sum(sum(t['dice']) for t in dmg_tape)+p['damage_bonus']
        if plus:raw+=max(faces for _,faces in p['damage_groups'])
        potential=max(0,raw-rb['rd']);actual=min(pre,potential)
        rb['hp']=pre-actual
    s['count']['attacks']+=1
    if plus:s['count']['crits_plus']+=1
    if minus:s['count']['crits_minus']+=1
    if hit and potential==0:s['count']['rd_absorbed']+=1
    if pre>0 and rb['hp']==0:s['count']['ko']+=1
    return {'actor':a,'target':b,'origin':'NORMAL','source':p['source'],'attack_name':p['attack_name'],
            'index':idx,'passive_bonus_after_two_turns':passive_bonus,'tape':tape+dmg_tape,'crit_dice':c,'crit_plus':plus,'crit_minus':minus,
            'roll_hit':h['dice'],'score':score,'ca':rb['ca'],'hit':hit,
            'hit_cause':'CRIT_AUTO' if plus else 'NEG_CRIT_AUTO_MISS' if minus else 'NUMERIC',
            'damage_groups':p['damage_groups'],'damage_fixed_bonus':p['damage_bonus'],
            'damage_raw':raw,'rd':rb['rd'],'damage_net_potential':potential,
            'hp_loss_actual':actual,'hp_before':pre,'hp_after':rb['hp'],'no_movement':True,
            'reaction_declared':'NONE','pa_spent':0,'standard_after':ra['standard']}

def do_attack(s,p,seq):
    if s['phase']!='ACTIVE' or p!={'actor':s['active'],'target':('E' if s['active']=='B' else 'B'),'reaction':'NONE'}:raise Deny('ATTACK_GATE')
    a=p['actor'];b=p['target'];r_before={x:{k:s['actors'][x]['resource'][k] for k in ('hp','pa','reaction','standard','movement')} for x in ('B','E')}
    out=attack(s,a,b)
    r_after={x:{k:s['actors'][x]['resource'][k] for k in ('hp','pa','reaction','standard','movement')} for x in ('B','E')}
    return {'attack':out,'resource_before':r_before,'resource_after':r_after}

def do_end(s,p,seq):
    if s['phase']!='ACTIVE' or p!={'actor':s['active']} or s['actors'][s['active']]['resource']['standard']!=0:raise Deny('TURN_END_GATE')
    a=s['active'];before={k:s['actors'][a]['resource'][k] for k in ('standard','movement','reaction')}
    result=history.advance(s)
    return {'ended_actor':a,'before':before,'transition':result,'winner':s['winner'],'active_after':s['active'],'round_after':s['round']}

def do_censor(s,p,seq):
    if s['phase']!='ACTIVE' or p!={'horizon':PREREG['horizon']}:raise Deny('CENSOR_GATE')
    s['phase']='CENSORED_HORIZON';s['winner']=None;s['active']=None
    return {'censored':True,'reason':'60_TURNS_NO_SURVIVOR'}

def run(seed,side,outdir,max_turns=60):
    outdir.mkdir(parents=True,exist_ok=True)
    file=outdir/f'R92BENCH_{seed}_{side}.sqlite';start(file,seed,side)
    commit(file,'INIT',{'operation':'INIT'},do_init)
    turncount=0
    while turncount<max_turns:
        s,head,rev=core.load(file)
        if s['phase']!='ACTIVE':break
        a=s['active'];b='B' if a=='E' else 'E'
        commit(file,'NORMAL_ATTACK',{'actor':a,'target':b,'reaction':'NONE'},do_attack)
        commit(file,'TURN_END',{'actor':a},do_end)
        turncount+=1
    else:
        s,_,_=core.load(file)
        if s['phase']=='ACTIVE':commit(file,'CENSOR',{'horizon':PREREG['horizon']},do_censor)
    con=sqlite3.connect(file);out=sqlite3.connect(file.with_suffix('.checkpoint.sqlite'))
    try:con.backup(out)
    finally:con.close();out.close()
    if core.load(file)!=core.load(file.with_suffix('.checkpoint.sqlite')):raise Deny('CHECKPOINT_MISMATCH')
    s,head,rev=core.load(file)
    con=sqlite3.connect(file)
    try:
        rows=[json.loads(x[0]) for x in con.execute('SELECT row_json FROM events ORDER BY seq')]
    finally:con.close()
    attacks=[r['detail']['attack'] for r in rows if r['kind']=='NORMAL_ATTACK']
    return {'run_id':s['run_id'],'seed':seed,'side':side,'source_sha':profile_sha(),
            'admission':MATCHUP['admission'],'matchup_id':MATCHUP['id'],'phase':s['phase'],
            'winner':s['winner'],'turn_count':turncount,'rounds':s['round'],
            'events':rev,'head':head,'attacks':len(attacks),'hits':sum(a['hit'] for a in attacks),
            'crit_plus':sum(a['crit_plus'] for a in attacks),'damage_raw_hit':sum(a['damage_raw'] for a in attacks),
            'damage_post_rd_potential':sum(a['damage_net_potential'] for a in attacks),
            'hp_loss_actual':sum(a['hp_loss_actual'] for a in attacks),
            'hp_final':{a:s['actors'][a]['resource']['hp'] for a in ('B','E')},
            'attack_receipts':attacks,'ledger':file.name,'checkpoint':file.with_suffix('.checkpoint.sqlite').name,
            'no_repeat':True,'official_credits':0}

if __name__=='__main__':
    results=[]
    for matchup in FIXTURE['matchups']:
        configure(matchup)
        for phase,seeds in PREREG['seeds'].items():
            for sd in seeds:
                for side in PREREG['sides']:
                    folder=ROOT/'runs'/matchup['id'];r=run(sd,side,folder)
                    r['cohort']=phase;results.append(r)
    (ROOT/'R92_RESULTS_1X1.json').write_text(canon(results)+'\n')
    print(json.dumps({'scenes':len(results),'seeds':len(set(x['seed'] for x in results)),'matches':len(FIXTURE['matchups']),'results':[{k:x[k] for k in ('matchup_id','seed','side','winner','phase','turn_count','attacks','hits','hp_final')} for x in results]},indent=2))
