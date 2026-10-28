"""Independent Python-stdlib auditor for R82–R91 source-conditional 1v1.
Does not import the executing adapter or the historical engine. Replays the ledger
from genesis, verifies every state SHA, causal turn, deterministic rolls,
resource debit, fixed source profile, results and checkpoint. No network/writes.
"""
import copy,csv,hashlib,json,random,sqlite3,sys
from pathlib import Path
R=Path(__file__).resolve().parent
VERSION='VLAB-R18-INTERACTIVE-CLI-0.1-EXPERIMENTAL'

def canon(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def sha(x):return hashlib.sha256(canon(x).encode()).hexdigest()
def ensure(cond,msg):
    if not cond:raise AssertionError(msg)
def roll(seed,seq,label,n,faces):
    entropy=hashlib.sha256(f'{seed}|{seq}|{label}|{n}d{faces}|{VERSION}'.encode()).digest()
    x=random.Random(int.from_bytes(entropy,'big'));return [x.randint(1,faces) for _ in range(n)]
def audit(db,profile):
    db=Path(db); con=sqlite3.connect(db)
    try:
        ensure(con.execute('PRAGMA integrity_check').fetchone()[0]=='ok','SQLITE_INTEGRITY')
        meta=dict(con.execute('select key,value from meta'))
        ensure(con.execute('SELECT COUNT(*) FROM pending').fetchone()[0]==0,'UNKNOWN_EFFECT_PENDING')
        rows=[(a,b,c,d,e,f,g) for a,b,c,d,e,f,g in con.execute('SELECT seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha FROM events ORDER BY seq')]
        ensure(len(rows)==int(meta['revision']),'EVENT_DENOMINATOR')
        ensure(len(set(x[1] for x in rows))==len(rows),'DUPLICATE_COMMAND')
        final=json.loads(meta['state'])
    finally:con.close()
    genesis=db.with_suffix('.genesis.json')
    ensure(genesis.exists(),'MISSING_GENESIS');state=json.loads(genesis.read_text());initial=copy.deepcopy(state)
    ensure(state['source_gate']['sha']==sha({k:profile[k] for k in ('B','E')}),'SOURCE_HASH');ensure(state['source_gate']['official'] is False,'OFFICIAL_SOURCE_GATE_NOT_ALLOWED')
    ensure(state['policy']['canonical_writes']==0 and state['claims']['campaign']==0,'CANONICAL_SIDE_EFFECT')
    seed=state['seed'];expected_side='B_LEFT' if state['actors']['B']['resource']['position'][0]==0 else 'E_LEFT'
    ensure(state['experiment']['side']==expected_side,'MIRROR_GENESIS')
    prev=meta['genesis'];natt=nhit=ndmg=0
    ensure(meta['scene']==state['scene'],'SCENE_GENESIS')
    for i,cmd_id,prior,serialized,row_sha,before_sha,after_sha in rows:
        ensure(i>0 and i<=len(rows),'SEQ_RANGE')
        row=json.loads(serialized)
        ensure(row['seq']==i and row['cmd_id']==cmd_id and prior==prev and row['prev']==prev,'HASH_LINK')
        ensure(row_sha==sha(row),'ROW_HASH')
        ensure(row['before_sha']==before_sha==sha(state),'BEFORE_FULL_STATE')
        ensure(row['official_effects']==0 and row['synthetic'] is True,'OFFICIAL_WRITE')
        kind=row['kind'];d=row['detail'];p=row['payload']
        if kind=='INIT':
            ensure(state['phase']=='INIT' and i==1,'INIT_PRECONDITION')
            freeze=json.loads((R/'R94_SOURCE_FREEZE.json').read_text())
            mt=next(m for m in freeze['matchups'] if m['id']==state['experiment']['matchup_id'])
            first=mt['opening'];second='E' if first=='B' else 'B';order=[first,second]
            ensure(d['initiatives']==[] and d['tie']==[] and d['order']==order,'NO_INVENTED_INIT_SKILL')
            ensure(d['opening']==first and d['initiative_control']=='EXOGENOUS_FIXED_ORDER_NO_SKILL_ROLL','INIT_SCENARIO_FREEZE')
            ensure(d['r26']=={'order':order,'rule':'EXOGENOUS_OPENING_NOT_NATIVE_INITIATIVE'},'INIT_SCOPE')
            state['order']=order;state['active']=first;state['phase']='ACTIVE';state['round']=1;state['turn']=0
            state['actors'][first]['resource']['reaction']=1
            state['turn_history'].append({'event':'START','actor':first,'round':1})
        elif kind=='NORMAL_ATTACK':
            ensure(state['phase']=='ACTIVE','ATTACK_PHASE')
            a=state['active'];b='B' if a=='E' else 'E';atk=d['attack'];r=state['actors'][a]['resource'];target=state['actors'][b]['resource']
            ensure(p=={'actor':a,'target':b,'reaction':'NONE'},'ATTACK_PAYLOAD')
            ensure(atk['actor']==a and atk['target']==b and atk['source']==profile[a]['source'],'ATTACK_SOURCE')
            ensure(atk['attack_name']==profile[a]['attack_name'],'ATTACK_NAME')
            ensure(atk['reaction_declared']=='NONE' and atk['no_movement'] and atk['pa_spent']==0,'ATTACK_SIDE_EFFECT')
            ensure(r['hp']>0 and target['hp']>0 and r['standard']==1,'ATTACK_SLOT')
            rb={x:{k:state['actors'][x]['resource'][k] for k in ('hp','pa','reaction','standard','movement')} for x in ('B','E')}
            ensure(rb==d['resource_before'],'RESOURCES_BEFORE')
            state['action_id'][a]+=1;idx=state['action_id'][a]
            ensure(atk['index']==idx,'ACTION_IDX')
            label=f'BENCH-R92-{state["scene"]}-{a}-{b}-NORMAL-{idx}'
            c=[roll(seed,idx,label+'-CRIT-'+str(j),1,6)[0] for j in (1,2,3)]
            plus=(c[:2]==[6,6] and c[2]>=5);minus=(c[:2]==[1,1] and c[2]<=2)
            x=profile[a];(dn,df)=x['rank_dice'];hd=roll(seed,idx,label+'-HIT',dn,df)
            passive_bonus=(8 if a=='E' and x.get('duel_bonus_after_two_own_turns',False) and idx>=3 else 0)
            score=sum(hd)+x['attack_bonus']+passive_bonus;hit=not minus and (plus or score>target['ca'])
            pre=target['hp'];dt=[];raw=pot=actual=0
            if hit:
                for j,(n,f) in enumerate(x['damage_groups']):dt.append(roll(seed,idx,label+'-DAMAGE-'+str(j),n,f))
                raw=sum(sum(v) for v in dt)+x['damage_bonus']
                if plus:raw+=max(f for _,f in x['damage_groups'])
                pot=max(0,raw-target['rd']);actual=min(pre,pot)
            target['hp']=pre-actual;r['standard']=0
            state['count']['attacks']+=1
            if plus:state['count']['crits_plus']+=1
            if minus:state['count']['crits_minus']+=1
            if hit and pot==0:state['count']['rd_absorbed']+=1
            if pre>0 and target['hp']==0:state['count']['ko']+=1
            expected_tape=[]
            for j,v in enumerate(c,1):expected_tape.append({'dice':[v],'faces':6,'label':label+'-CRIT-'+str(j),'n':1,'seq':idx})
            expected_tape.append({'dice':hd,'faces':df,'label':label+'-HIT','n':dn,'seq':idx})
            for j,(n,f) in enumerate(x['damage_groups']):
                if hit:expected_tape.append({'dice':dt[j],'faces':f,'label':label+'-DAMAGE-'+str(j),'n':n,'seq':idx})
            checks={'passive_bonus_after_two_turns':passive_bonus,'crit_dice':c,'crit_plus':plus,'crit_minus':minus,'roll_hit':hd,'score':score,
                'ca':target['ca'],'hit':hit,'damage_groups':x['damage_groups'], 'damage_fixed_bonus':x['damage_bonus'],
                'damage_raw':raw,'rd':target['rd'],'damage_net_potential':pot,'hp_loss_actual':actual,
                'hp_before':pre,'hp_after':target['hp'],'standard_after':0,'tape':expected_tape,
                'hit_cause':'CRIT_AUTO' if plus else 'NEG_CRIT_AUTO_MISS' if minus else 'NUMERIC'}
            for k,v in checks.items():ensure(atk[k]==v,'ATTACK_SEMANTIC_'+k)
            ra={x:{k:state['actors'][x]['resource'][k] for k in ('hp','pa','reaction','standard','movement')} for x in ('B','E')}
            ensure(ra==d['resource_after'],'RESOURCES_AFTER')
            natt+=1;nhit+=int(hit);ndmg+=actual
        elif kind=='TURN_END':
            ensure(state['phase']=='ACTIVE','TURN_END_PHASE')
            ended=state['active'];ensure(p=={'actor':ended} and d['ended_actor']==ended,'TURN_ACTOR')
            ensure(state['actors'][ended]['resource']['standard']==0,'TURN_ACTION')
            living=[a for a in state['order'] if state['actors'][a]['resource']['hp']>0]
            if len(living)<=1:
                state['phase']='COMPLETE' if living else 'DRAW_NO_LIVING';state['winner']=living[0] if living else None;state['active']=None
                ensure(d['transition']=={'complete':True,'winner':state['winner'],'survivors':living},'KO_TRANSITION')
            else:
                state['turn']=(state['turn']+1)%len(state['order'])
                if state['turn']==0:state['round']+=1
                state['active']=state['order'][state['turn']]
                next_actor=state['active'];ensure(state['actors'][next_actor]['resource']['hp']>0,'KO_SCHEDULER')
                state['actors'][next_actor]['resource']['standard']=1
                state['actors'][next_actor]['resource']['movement']=1
                oldreact=state['actors'][next_actor]['resource']['reaction'];state['actors'][next_actor]['resource']['reaction']=1
                state['turn_history'].append({'event':'START','actor':next_actor,'round':state['round'],'skipped':[]})
                ensure(d['transition']['active']==next_actor and d['transition']['refresh']['before']==oldreact and d['transition']['refresh']['after']==1,'REFRESH_OR_ORDER')
            ensure(d['winner']==state['winner'] and d['active_after']==state['active'] and d['round_after']==state['round'],'END_RECEIPT')
        elif kind=='CENSOR':
            ensure(state['phase']=='ACTIVE' and p=={'horizon':120},'CENSOR_PHASE')
            state['phase']='CENSORED_HORIZON';state['winner']=None;state['active']=None
        else:ensure(False,'UNKNOWN_KIND')
        ensure(after_sha==row['after_sha']==sha(state),'AFTER_FULL_STATE_'+kind)
        prev=row_sha
    ensure(prev==meta['head'] and state==final,'FINAL_STATE')
    ensure(state['phase'] in ('COMPLETE','CENSORED_HORIZON'),'RUN_FINISHED')
    return {'id':state['run_id'],'seed':seed,'side':state['experiment']['side'],'winner':state['winner'],'phase':state['phase'],
            'events':len(rows),'attacks':natt,'hits':nhit,'hp_loss':ndmg,'hp_final':{a:state['actors'][a]['resource']['hp'] for a in ('B','E')},'turns':sum(row[3].find('"kind":"NORMAL_ATTACK"')>=0 for row in rows),
            'cold_reconstructed_full_states':len(rows),'semantic_dice_verified':natt,'pass':True}

def all_runs(root=R):
    frozen=json.loads((root/'R94_SOURCE_FREEZE.json').read_text());prereg=json.loads((root/'R94_PREREG_FIXED_OPENING.json').read_text());runs=[]
    for matchup in frozen['matchups']:
        prof={side:frozen['profiles'][matchup[side]] for side in ('B','E')}
        for group,v in prereg['seeds'].items():
            for seed in v:
                one=[]
                for side in prereg['sides']:
                    fp=root/'fixed_runs'/matchup['id']/f'R94BENCH_{seed}_{side}.sqlite';cp=fp.with_suffix('.checkpoint.sqlite')
                    with sqlite3.connect(fp) as original, sqlite3.connect(cp) as checkpoint:
                        for table in ('meta','events','pending'):
                            ensure(original.execute('SELECT * FROM '+table+' ORDER BY 1').fetchall()==checkpoint.execute('SELECT * FROM '+table+' ORDER BY 1').fetchall(),'CHECKPOINT_LOGICAL_'+table)
                        ensure(checkpoint.execute('PRAGMA integrity_check').fetchone()[0]=='ok','CHECKPOINT_INTEGRITY')
                    a=audit(fp,prof);a['group']=group;a['matchup_id']=matchup['id'];one.append(a);runs.append(a)
                ensure(one[0]['winner']==one[1]['winner'] and one[0]['hp_final']==one[1]['hp_final'] and one[0]['attacks']==one[1]['attacks'] and one[0]['hits']==one[1]['hits'] and one[0]['events']==one[1]['events'],'SIDE_SWAP_BIAS')
    return {'runs':runs,'matchups':len(frozen['matchups']),'unique_seed_values':len(set(r['seed'] for r in runs)),'independent_matchup_seed_blocks':len(set((r['matchup_id'],r['seed']) for r in runs)),'mirrored_pairs':len(set((r['matchup_id'],r['seed']) for r in runs)),'total_events':sum(r['events'] for r in runs),'total_attacks':sum(r['attacks'] for r in runs),'total_hits':sum(r['hits'] for r in runs),'total_realized_damage':sum(r['hp_loss'] for r in runs),'censored_runs':sum(r['phase']=='CENSORED_HORIZON' for r in runs),'all_pass':True}

if __name__=='__main__':
    try:
        result=all_runs();(R/'R94_COLD_FIXED_OPENING.json').write_text(canon(result)+'\n');print(canon({k:v for k,v in result.items() if k!='runs'}))
    except Exception as e:
        print('COLD_AUDIT_REJECT:',str(e),file=sys.stderr);sys.exit(1)
