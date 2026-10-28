"""R103 additive source-specific proof of costed Lightning, in NEW isolated SQLite only.
Not a complete fight, nor replacement for v0.8.1 native resolver. One positive PA
transaction and reactionless Reflexo-save half, with odd damage explicitly held.
Original R18 event_commit + v0.8.1 package unchanged; no replay of historical fights.
"""
from __future__ import annotations
import json,sys,sqlite3,hashlib,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'r61_extracted'/'work'/'fusion_stage12'))
import vlab_r18_interactive as core
C=json.loads((ROOT/'R103_SOURCE_AND_PREREG.json').read_text());frozen=core.sha(C)
class Reject(Exception):pass

def snapshot(seed,side,pa=4016,standard=1,dist=1.5):
    s=core.initial('A',seed)
    s['scene']='R103-GRIFO-DESCARGA-'+str(seed)
    s['source_digest']=frozen
    s['test_mode']='SOURCE_RESTRICTED_COSTED_SINGLE_EVENT_NOT_COMBAT'
    s['phase']='ACTIVE';s['order']=['B','E'];s['active']='B';s['round']=1
    s['actors']={
      'B':{'source':'Grifo L3 support-spec','resource':{'hp':4315,'pa':pa,'ca':153,'rd_physical':75,'standard':standard,'movement':1,'reaction':1,'position':[0,0] if side=='B_LEFT' else [dist,0]}},
      'E':{'source':'Sikong Auren L3 natural','resource':{'hp':523,'pa':719,'ca':225,'rd_physical':35,'rd_dark':60,'standard':1,'movement':1,'reaction':1,'position':[dist,0] if side=='B_LEFT' else [0,0]}}
    }
    s['experiment']={'seed':seed,'side':side,'historical_core':'R18 transaction only', 'source_gate':'PREREG_R103', 'official':False}
    return s

def setup(db,seed,side,pa=4016,standard=1,dist=1.5):
    if db.exists():raise Reject('NO_DUPLICATE_RUN')
    core.init_db(db,'A',seed)
    state=snapshot(seed,side,pa,standard,dist)
    genesis=core.sha({'genesis':state,'frozen':frozen})
    with core.connect(db) as con:
        for k,v in [('scene',state['scene']),('head',genesis),('genesis',genesis),('state',core.canonical(state))]:
            con.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
    db.with_suffix('.genesis.json').write_text(core.canonical(state)+'\n')
    return state

def dice(seed):
    label='R103-GRIFO-DESCARGA-AUREN-ALL-SIDES'
    reflexo=core.dice(seed,1,label+'-SAVE',6,6)
    dmg=core.dice(seed,1,label+'-LIGHTNING',14,10)
    return reflexo,dmg

def preflight(state,seed):
    b=state['actors']['B']['resource'];e=state['actors']['E']['resource']
    if b['pa']<55:raise Reject('INSUFFICIENT_PA_NO_INTENT')
    if b['standard']!=1:raise Reject('STANDARD_USED_NO_INTENT')
    if (b['position'][0]-e['position'][0])**2>1.5**2+1e-8:raise Reject('OUT_OF_RANGE_NO_INTENT')
    if state['active']!='B' or state['phase']!='ACTIVE':raise Reject('NOT_ACTIVE_NO_INTENT')
    save,dmg=dice(seed)
    if (sum(save)+166)<=94:raise Reject('UNEXPECTED_SAVE_AUTHORITY')
    if sum(dmg)%2:raise Reject('ODD_HALF_ROUNDING_UNDEFINED_NO_INTENT')
    return save,dmg

def perform(db,seed):
    state,head,rev=core.load(db)
    save,dmg=preflight(state,seed)
    assert rev==0
    def resolver(s,p,seq):
        assert seq==1
        a=s['actors']['B']['resource'];b=s['actors']['E']['resource']
        assert a['pa']>=55 and a['standard']==1 and b['hp']>0
        damage=sum(dmg)//2
        pre=b['hp'];a['pa']-=55;a['standard']=0;b['hp']=max(0,pre-damage)
        return {'source':'Grifo Descarga Curta','source_action':'STANDARD','PA_before':a['pa']+55,
                'PA_after':a['pa'],'standard_before':1,'standard_after':0,'save':save,
                'save_score':sum(save)+166,'save_cd':94,'save_success':True,
                'damage_roll':dmg,'damage_raw':sum(dmg),'damage_half':damage,
                'mitigation':'physical35/dark60 not applicable to typed Lightning; no further source claim',
                'hp_before':pre,'hp_after':b['hp'],'hp_loss':pre-b['hp'],
                'no_reaction_declared':True, 'no_movement':True,'not_full_combat':True}
    cmd='LAB-CMD-R103-'+core.sha({'seed':seed,'scene':state['scene'],'side':state['experiment']['side']})[:36]
    event=core.event_commit(db,cmd,'SPECIAL_LIGHTNING',{'actor':'B','target':'E','source':'Descarga Curta'},resolver)
    core.load(db)
    return {'run_id':state['scene']+'-'+state['experiment']['side'],'seed':seed,'side':state['experiment']['side'],
            'result':'PASS_BOUNDED_SPECIAL_EVENT','PA_spent':55,'damage':event['detail']['hp_loss'],'events':1}

def main():
    out=ROOT/'r103_runs';out.mkdir(exist_ok=True)
    results=[];held=[]
    for seed in C['seed_list']:
        for side in C['side_swap']:
            db=out/f'R103_{seed}_{side}.sqlite'
            st=setup(db,seed,side)
            try:
                results.append(perform(db,seed))
            except Reject as e:
                _,_,rev=core.load(db)
                assert rev==0
                with sqlite3.connect(db) as con:
                    assert con.execute('select count(*) from pending').fetchone()[0]==0
                held.append({'seed':seed,'side':side,'reason':str(e),'events':0,'pending':0,'hp_original':st['actors']['E']['resource']['hp']})
    for testcase,opts in [('INSUFFICIENT_PA_54',{'pa':54}),('NO_STANDARD_ACTION',{'standard':0}),('OUT_OF_RANGE',{'dist':7.5})]:
        db=out/f'NEG_{testcase}.sqlite';st=setup(db,602199,'B_LEFT',**opts)
        try:perform(db,602199)
        except Reject:
            with sqlite3.connect(db) as con:
                assert con.execute('select count(*) from pending').fetchone()[0]==0
            assert core.load(db)[2]==0
        else:raise AssertionError('NEG_TEST_ACCEPTED '+testcase)
    (ROOT/'R103_COSTED_SOURCE_EVENT_RUNS.json').write_text(json.dumps({'pass':results,'held':held,'preflight_negatives':3},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'executed':len(results),'held_rounding':len(held),'unique_seeds_executed':len(set(x['seed'] for x in results)), 'negative_preflight':3,'results':results},ensure_ascii=False))
if __name__=='__main__':main()
