"""Independent semantic cold verifier for R93 2x1. Python stdlib ONLY; does not import runner/historic engine.
Recomputes every atomic state, RNG die, CA, RD, KO skip, individual turns, allies win & SQLite.
"""
import json,hashlib,sqlite3,random,copy,sys
from pathlib import Path
R=Path(__file__).resolve().parent
SRC=json.loads((R/'R93_TEAM_FREEZE.json').read_text())['profiles']
PR=json.loads((R/'R93_PREREG_TEAM.json').read_text())
ACT=('F','V','R')
VERSION='VLAB-R18-INTERACTIVE-CLI-0.1-EXPERIMENTAL'
RULING='MESTRE-REACTION-20261014-REFRESH-START-OWN-TURN'
def canon(o):return json.dumps(o,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def sha(o):return hashlib.sha256(canon(o).encode()).hexdigest()
def roll(seed,seq,label,n,f):
    entropy=hashlib.sha256(f'{seed}|{seq}|{label}|{n}d{f}|{VERSION}'.encode()).digest()
    return [random.Random(int.from_bytes(entropy,'big')).randint(1,f)] if n==1 else _multi(entropy,n,f)
def _multi(entropy,n,f):
    rng=random.Random(int.from_bytes(entropy,'big'));return [rng.randint(1,f) for _ in range(n)]
def check(cond,msg):
    if not cond:raise AssertionError(msg)
def alive(s,a):return s['actors'][a]['resource']['hp']>0
def target(s,a):return next((b for b in ('R','V') if alive(s,b)),None) if a=='F' else ('F' if alive(s,'F') else None)
def sidewinner(s):
    if not alive(s,'F'):return 'TEAM_ED_NPC'
    if not alive(s,'R') and not alive(s,'V'):return 'BEAST'
    return None
def small(s):return {x:{k:s['actors'][x]['resource'][k] for k in ('hp','pa','reaction','standard','movement')} for x in ACT}
def init(s,d):
    tapes=[];scores=[]
    for a in s['actors']:
        p=SRC[a];n,f=p['rank_dice'];dice=roll(s['seed'],0,'R52-INIT-'+a,n,f)
        tapes.append({'actor':a,'seq':0,'label':'R52-INIT-'+a,'n':n,'faces':f,'dice':dice})
        scores.append({'a':a,'total':sum(dice)+p['init_bonus'],'des':p['des']})
    check(tapes==d['scheduler']['initial'],'INIT_DICE')
    check(len(set((x['total'],x['des']) for x in scores))==3,'INIT_UNRESOLVED_TIE')
    sorted_order=[x['a'] for x in sorted(scores,key=lambda r:(-r['total'],-r['des']))]
    check(sorted_order==d['scheduler']['order']==d['order'],'INIT_R26_PRIORITY')
    check(d['scheduler']['tie_tape']==[] and d['scheduler']['tie_result']['rerolls']==[],'INIT_NO_TIE_TAPE')
    s['order']=sorted_order;s['active']=sorted_order[0];s['phase']='ACTIVE';s['round']=1;s['turn']=0
    old=s['actors'][s['active']]['resource']['reaction'];s['actors'][s['active']]['resource']['reaction']=1
    s['turn_history'].append({'event':'START','actor':s['active'],'round':1})
    check(d['active']==s['active'] and d['scheduler']['r26_refresh']=={'actor':s['active'],'before':old,'after':1,'trigger':'OWN_TURN_START','no_stockpiling':True,'ruling_id':RULING},'INIT_REFRESH')
    check(d['factions']==s['factions'],'FACTIONS_INIT')
def advance(s,d,ended):
    skipped=[]
    for _ in range(len(s['order'])):
        sturn=(s['turn']+1)%len(s['order']);s['turn']=sturn
        if sturn==0:s['round']+=1
        a=s['order'][sturn];s['active']=a
        rr=s['actors'][a]['resource'];old=copy.deepcopy(rr);rr['standard']=1;rr['movement']=1
        native={'turn_end':ended if not skipped else s['order'][(sturn-1)%len(s['order'])],
                'next_turn':a,'round':s['round'],'standard_refreshed_at_new_turn':True,'reaction_auto_refresh':False}
        if rr['hp']<=0:
            s['actors'][a]['resource']=old;skipped.append(a);continue
        before=rr['reaction'];rr['reaction']=1
        s['turn_history'].append({'event':'START','actor':a,'round':s['round'],'skipped':skipped[:]})
        expected={'complete':False,'active':a,'native':native,'refresh':{'actor':a,'before':before,'after':1,'trigger':'OWN_TURN_START','no_stockpiling':True,'ruling_id':RULING},'skipped_ko':skipped,'round':s['round']}
        check(d['transition']==expected,'TURN_SCHEDULER_TRANSITION')
        return
    raise AssertionError('NO_NEXT_ACTIVE')
def team_turn(s,p,d):
    a=s['active'];b=target(s,a)
    check(p=={'actor':a,'target':b,'reaction':'NONE'},'TEAM_TARGET_POLICY')
    ra=s['actors'][a]['resource'];rb=s['actors'][b]['resource'];prof=SRC[a]
    check(ra['hp']>0 and rb['hp']>0 and ra['standard']==1,'ACTION_ALIVE_OR_SLOT')
    check(sum((x-y)**2 for x,y in zip(ra['position'],rb['position']))<=1.500001**2,'TEAM_ADJACENCY')
    check(prof['attack_pa']==0 and d['positive_PA']==0,'PA_UNDOCUMENTED')
    before=small(s);check(before==d['before'],'RESOURCES_BEFORE')
    check(d['round_before']==s['round'] and d['turn_before']==s['turn'],'ROUND_BEFORE')
    s['action_id'][a]+=1;s['attack_index'][a]+=1;idx=s['attack_index'][a]
    label=f'R52-{s["scene"]}-{a}-{b}-NORMAL-{idx}'
    crit=[];tape=[]
    for j in (1,2,3):
        val=roll(s['seed'],idx,label+'-CRIT-'+str(j),1,6);crit.append(val[0])
        tape.append({'seq':idx,'label':label+'-CRIT-'+str(j),'n':1,'faces':6,'dice':val})
    plus=crit[:2]==[6,6] and crit[2] in (5,6)
    minus=crit[:2]==[1,1] and crit[2] in (1,2)
    n,f=prof['rank_dice'];hit_roll=roll(s['seed'],idx,label+'-HIT-1',n,f)
    tape.append({'seq':idx,'label':label+'-HIT-1','n':n,'faces':f,'dice':hit_roll})
    score=sum(hit_roll)+prof['attack_bonus'];hit=not minus and (plus or score>rb['ca'])
    prior=rb['hp'];raw=net=0
    if hit:
        dn,df=prof['damage_dice'];damage=roll(s['seed'],idx,label+'-DAMAGE',dn,df)
        tape.append({'seq':idx,'label':label+'-DAMAGE','n':dn,'faces':df,'dice':damage})
        raw=sum(damage)+prof['damage_bonus']+(df if plus else 0)
        net=max(0,raw-rb['rd']);rb['hp']=max(0,prior-net)
    ra['standard']=0;s['count']['attacks']+=1
    if plus:s['count']['crits_plus']+=1
    if minus:s['count']['crits_minus']+=1
    if hit and net==0:s['count']['rd_absorbed']+=1
    if prior>0 and rb['hp']==0:s['count']['ko']+=1
    atk=d['exchange']['normal']
    expected={'actor':a,'target':b,'origin':'NORMAL','source':'R93_'+a,'index':idx,'tape':tape,
      'crit_dice':crit,'crit_plus':plus,'crit_minus':minus,'adv':0,'score':score,'ca':rb['ca'],'hit':hit,
      'hit_cause':'CRIT_AUTO' if plus else 'NEG_CRIT_AUTO_MISS' if minus else 'NUMERIC','damage_raw':raw,'rd':rb['rd'],
      'damage_net':net,'hp_before':prior,'hp_after':rb['hp'],'standard_after':0,'reaction_after':ra['reaction']}
    check(atk==expected,'ATTACK_ALL_FIELDS_SEMANTIC')
    check(d['exchange']['defender_reaction_after']==d['exchange']['defender_reaction_before']==rb['reaction'],'DEFENDER_REACTION_UNCHANGED')
    check(d['exchange']['reply'] is None and not d['exchange']['reaction_predeclared'] and not d['exchange']['nested_counter_allowed'],'NO_COUNTER')
    outcome=sidewinner(s)
    if outcome:
        s['phase']='COMPLETE';s['winner']=outcome;s['active']=None
        trans={'complete':True,'winner':outcome,'sides_alive':{'BEAST':alive(s,'F'),'TEAM':alive(s,'V') or alive(s,'R')}}
        check(d['transition']==trans,'TEAM_Faction_END')
    else:advance(s,d,a)
    check(d['active_after']==s['active'] and d['round_after']==s['round'],'POST_ACTIVE_ROUND')
    check(d['actions']==s['action_id'] and d['faction_winner']==outcome,'ACTION_IDS_OUTCOME')
    check(d['after']==small(s),'RESOURCES_AFTER')
def audit_one(db):
    db=Path(db);cp=db.with_suffix('.checkpoint.sqlite')
    with sqlite3.connect(db) as c,sqlite3.connect(cp) as bc:
        check(c.execute('PRAGMA integrity_check').fetchone()[0]=='ok','SQLITE_BAD')
        check(bc.execute('PRAGMA integrity_check').fetchone()[0]=='ok','CP_SQLITE_BAD')
        for table in ('meta','events','pending'):
            check(c.execute('SELECT * FROM '+table+' ORDER BY 1').fetchall()==bc.execute('SELECT * FROM '+table+' ORDER BY 1').fetchall(),'CP_MISMATCH_'+table)
        meta=dict(c.execute('SELECT key,value FROM meta'));rows=c.execute('SELECT seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha FROM events ORDER BY seq').fetchall()
        check(c.execute('SELECT COUNT(*) FROM pending').fetchone()[0]==0,'PENDING_INTENT')
    state=json.loads(db.with_suffix('.genesis.json').read_text())
    check(state['experiment']['source_sha']==sha(SRC),'FREEZE_HASH')
    check(state['factions']=={'BEAST':['F'],'TEAM':['V','R']},'FACTIONS_GENESIS')
    check(state['policy']['canonical_writes']==0 and state['claims']['campaign']==0,'CANONICAL_WRITE')
    check(state['phase']=='INIT' and state['winner'] is None,'START_STATE')
    check(meta['scene']==state['scene'] and int(meta['revision'])==len(rows),'EVENT_COUNT')
    ids=set();prev=meta['genesis'];attacks=0;hits=0;hploss=0
    for seq,cmd,pr,txt,row_sha,before_sha,after_sha in rows:
        row=json.loads(txt);check(row['seq']==seq and row['cmd_id']==cmd and row['prev']==pr==prev,'CHAIN')
        check(cmd not in ids,'CMD_ID_DUPLICATE');ids.add(cmd)
        check(sha(row)==row_sha and row['before_sha']==before_sha==sha(state),'HASH_BEFORE_AND_ROW')
        check(row['official_effects']==0 and row['synthetic'] is True,'OFFICIAL_EFFECT')
        kind=row['kind'];d=row['detail'];payload=row['payload']
        if kind=='INIT':check(seq==1,'INIT_POSITION');init(state,d)
        elif kind=='TEAM_TURN':
            check(state['phase']=='ACTIVE','ATTACK_PHASE');team_turn(state,payload,d)
            attacks+=1;hits+=int(d['exchange']['normal']['hit']);hploss+=min(d['exchange']['normal']['hp_before'],d['exchange']['normal']['damage_net'])
        elif kind=='CENSOR':
            check(state['phase']=='ACTIVE' and payload=={'horizon':PR['horizon']},'CENSOR_GATE')
            state['phase']='CENSORED_HORIZON';state['winner']=None;state['active']=None
        else:raise AssertionError('UNKNOWN_KIND_'+kind)
        check(row['after_sha']==after_sha==sha(state),'AFTER_STATE_'+str(seq)+'_'+kind)
        prev=row_sha
    check(meta['head']==prev and json.loads(meta['state'])==state,'FINAL_SNAPSHOT')
    check(state['phase'] in ('COMPLETE','CENSORED_HORIZON'),'FINISHED')
    return {'run_id':state['run_id'],'side':state['experiment']['side'],'seed':state['seed'],'winner':state['winner'],
     'events':len(rows),'attacks':attacks,'hits':hits,'hp_loss':hploss,
     'hp_final':{a:state['actors'][a]['resource']['hp'] for a in ACT},'phase':state['phase'],'pass':True}
def all_audit():
    out=[]
    for group,seeds in PR['seeds'].items():
        for sd in seeds:
            pair=[]
            for side in PR['sides']:
                x=audit_one(R/'team_runs'/f'R93TEAM_{sd}_{side}.sqlite');x['cohort']=group;out.append(x);pair.append(x)
            check(len(pair)==2 and all(pair[0][k]==pair[1][k] for k in ('winner','events','attacks','hits','hp_loss','hp_final','phase')),'MIRROR_BIAS')
    check(len(set(x['run_id'] for x in out))==len(out),'RUN_ID_UNIQUE')
    result={'audited_runs':len(out),'blocks':len(set(x['seed'] for x in out)),
     'events':sum(x['events'] for x in out),'attacks':sum(x['attacks'] for x in out),
     'hits':sum(x['hits'] for x in out),'censored':sum(x['phase']=='CENSORED_HORIZON' for x in out),
     'all_pass':True,'runs':out}
    (R/'R93_COLD_TEAM_AUDIT.json').write_text(canon(result)+'\n')
    return result
if __name__=='__main__':
    try:
        r=all_audit();print(canon({k:v for k,v in r.items() if k!='runs'}))
    except Exception as e:print('COLD_REJECT',repr(e),file=sys.stderr);sys.exit(1)
