"""Independent stdlib auditor; NEVER imports executor or historical combat engine."""
import hashlib,json,random,sqlite3
from pathlib import Path
R=Path(__file__).resolve().parent
C=json.loads((R/'R103_SOURCE_AND_PREREG.json').read_text())
VERSION='VLAB-R18-INTERACTIVE-CLI-0.1-EXPERIMENTAL'
def canonical(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def sha(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def dice(seed,seq,label,n,f):
    entropy=hashlib.sha256(f'{seed}|{seq}|{label}|{n}d{f}|{VERSION}'.encode()).digest()
    rng=random.Random(int.from_bytes(entropy,'big'))
    return [rng.randint(1,f) for _ in range(n)]
def audit(db):
    with sqlite3.connect(db) as con:
        assert con.execute('pragma integrity_check').fetchone()[0]=='ok'
        meta=dict(con.execute('select key,value from meta'))
        events=list(con.execute('select seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha from events order by seq'))
        pending=list(con.execute('select * from pending'))
    initial=json.loads(db.with_suffix('.genesis.json').read_text())
    assert meta['mode']=='EXPERIMENTAL_LAB_ONLY'
    assert meta['scene']==initial['scene']
    assert meta['genesis']==sha({'genesis':initial,'frozen':sha(C)})
    assert initial['source_digest']==sha(C)
    assert initial['version']==VERSION and initial['synthetic'] is True
    seed=initial['experiment']['seed']
    label='R103-GRIFO-DESCARGA-AUREN-ALL-SIDES'
    save=dice(seed,1,label+'-SAVE',6,6)
    dmg=dice(seed,1,label+'-LIGHTNING',14,10)
    if not events:
        assert int(meta['revision'])==0 and not pending
        assert json.loads(meta['state'])==initial and meta['head']==meta['genesis']
        assert initial['actors']['E']['resource']['hp']==523
        return {'id':db.stem,'event_count':0,'pass':True,'reason':'PREVALIDATION_REJECTED_OR_HALF_UNDEFINED'}
    assert len(events)==1 and int(meta['revision'])==1 and not pending
    seq,cmd,prev,row_json,row_sha,before,after=events[0]
    row=json.loads(row_json)
    assert (seq,cmd,prev)==(1,row['cmd_id'],meta['genesis'])
    assert cmd.startswith('LAB-CMD-R103-') and row['kind']=='SPECIAL_LIGHTNING'
    assert row['payload']=={'actor':'B','target':'E','source':'Descarga Curta'}
    assert row_sha==sha(row) and row['prev']==prev and before==row['before_sha']==sha(initial)
    assert row['official_effects']==0 and row['synthetic'] is True
    detail=row['detail']
    assert sum(save)+166>94 and sum(dmg)%2==0
    assert detail['save']==save and detail['damage_roll']==dmg and detail['save_score']==sum(save)+166
    assert detail['damage_raw']==sum(dmg) and detail['damage_half']==sum(dmg)//2
    assert detail['PA_before']==4016 and detail['PA_after']==3961
    assert detail['hp_before']==523 and detail['hp_after']==523-sum(dmg)//2
    assert detail['hp_loss']==sum(dmg)//2
    st=json.loads(canonical(initial))
    st['actors']['B']['resource']['pa']=3961
    st['actors']['B']['resource']['standard']=0
    st['actors']['E']['resource']['hp']-=sum(dmg)//2
    assert sha(st)==after==row['after_sha']
    assert meta['head']==row_sha and json.loads(meta['state'])==st
    return {'id':db.stem,'event_count':1,'pass':True,'damage':sum(dmg)//2,'pa_consumed':55,
            'seed':seed,'side':initial['experiment']['side']}

def main():
    dirs=sorted((R/'r103_runs').glob('*.sqlite'))
    rows=[audit(x) for x in dirs]
    positives=[x for x in rows if x['event_count']==1]
    negatives=[x for x in rows if x['event_count']==0]
    assert len(rows)==15 and len(positives)==6 and len(negatives)==9
    pairs={}
    for x in positives:
        pairs.setdefault(x['seed'],[]).append(x)
    assert len(pairs)==3 and all(len(v)==2 and v[0]['damage']==v[1]['damage'] for v in pairs.values())
    out={'cold_audited':len(rows),'positive':len(positives),'held_or_negative':len(negatives),
         'distinct_positive_seeds':len(pairs),'paired_mirrors':len(pairs),
         'new_transactional_events':6,'total_cost_PA_across_synthetic_ledgers':330,
         'scope':'SOURCE_SPECIFIC_SINGLE_SPECIAL_ACTION_NOT_FULL_COMBAT_NOT_TERMINAL',
         'runs':rows,'result':'PASS'}
    (R/'R103_INDEPENDENT_COLD_AUDIT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='runs'},ensure_ascii=False))
if __name__=='__main__':main()
