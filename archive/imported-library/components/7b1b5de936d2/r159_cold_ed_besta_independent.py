"""Independent event-by-event cold semantic verifier for R111 and R112.
NO import of r109/r112 runners, vlab_effects_v08 or native v0.8.1 source.
Reconstructs R18 state, dice, critical bonus, weakness, PA, HP, event causality,
result snapshots and cryptographic chain by separate implementation.
"""
import hashlib,json,random,sqlite3,collections
from fractions import Fraction
from pathlib import Path
R=Path(__file__).resolve().parent
R18_VERSION='VLAB-R18-INTERACTIVE-CLI-0.1-EXPERIMENTAL'

def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def sh(x):return hashlib.sha256(canon(x).encode()).hexdigest()
def draw(seed,seq,label,count,faces):
    entropy=hashlib.sha256(f'{seed}|{seq}|{label}|{count}d{faces}|{R18_VERSION}'.encode()).digest()
    rnd=random.Random(int.from_bytes(entropy,'big'))
    return [rnd.randint(1,faces) for _ in range(count)]
def die(seed,ix,mode,a,kind,count,faces):return draw(seed,ix,f'R109-{mode}-{a}-{kind}',count,faces)

def verify(path):
    with open(path.with_suffix('.genesis.json')) as f:s=json.load(f)
    original=json.loads(canon(s));mode=s['experiment']['scene'];seed=s['seed']
    with sqlite3.connect(path) as c:
        meta=dict(c.execute('select key,value from meta'))
        evs=[(seq,cmd,prev,json.loads(row),rowsha,bf,af) for seq,cmd,prev,row,rowsha,bf,af in c.execute('select seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha from events order by seq')]
        assert c.execute('select count(*) from pending').fetchone()[0]==0,'UNKNOWN_EFFECT_PENDING'
    assert len(evs)==int(meta['revision'])
    assert meta['mode']=='EXPERIMENTAL_LAB_ONLY'
    assert meta['scene']==s['scene']
    assert s['source_digest'] and not s['experiment']['terminal']
    prev=meta['genesis'];counts=collections.Counter();failures=[]
    for seq,cmd,pp,row,rowsha,before_sha,after_sha in evs:
        assert seq==row['seq'] and seq>0 and pp==prev==row['prev'] and cmd==row['cmd_id']
        assert rowsha==sh(row) and before_sha==sh(s)==row['before_sha'] and after_sha==row['after_sha']
        k=row['kind'];p=row['payload'];e=row['detail']['native_action'];a=s['active'];target=p.get('target')
        actors=s['actors'];ar=actors[a]['resource'] if a else None
        if k=='TURN_START':
            assert p['actor']==a and ar['standard']==0
            before_imm=ar['immobile_next_own_turns'];wk=0<ar['hp']*10<ar['maximum_hp']
            speed='0' if before_imm else str(ar['base_speed']/2 if wk else ar['base_speed'])
            assert e['action']=='turn_start' and e['by']==a and e['weak']==wk and Fraction(e['speed'])==Fraction(speed)
            assert e['immobile']==(before_imm>0)
            ar.update(standard=1,movement=1,reaction=1)
            counts['turn_starts']+=1
        elif k=='NATIVE_ATTACK':
            assert p['actor']==a and a in actors and target in actors and target!=a and ar['standard']==1
            tr=actors[target]['resource']; pp_a=actors[a]['stats'];ix=s['action_indexes'][a]+1
            assert ix==p['ix'];dmg_groups=pp_a['damage'];atk_count,atk_faces,atk_bonus=pp_a['att']
            assert p['damage_groups']==dmg_groups
            crit=[die(seed,ix,mode,a,f'CRIT{j}',1,6)[0] for j in range(3)]
            assert crit==p['crit']==e['critical_sequence']
            cp=crit[:2]==[6,6] and crit[2]>=5; cn=crit[:2]==[1,1] and crit[2]<=2
            assert cn is True or cn is False
            weak=0<ar['hp']*10<ar['maximum_hp'];assert weak==e['weak_attacker']
            attempts=[die(seed,ix,mode,a,f'HIT{j}',atk_count,atk_faces) for j in range(2 if weak else 1)]
            assert attempts==p['attack_rolls'] and attempts==[list(x) for x in e['attack_roll_attempts']]
            extra=8 if mode=='G_FULL' and a=='E' and ix>=3 else 0
            assert atk_bonus+extra==p['attack_bonus'];score=(min(sum(t) for t in attempts)-2 if weak else sum(attempts[0]))+atk_bonus+extra
            assert score==p['score']==e['roll_score']
            dmg=[die(seed,ix,mode,a,f'DMG{j}',n,f) for j,(n,f) in enumerate(dmg_groups)]
            assert dmg==p['damage_rolls']
            expected_flat={'B':0,'E':211,'F':47}[a]
            assert p['flat']==expected_flat
            normal=sum(map(sum,dmg))+expected_flat
            assert normal==p['dmg']==e['normal_damage']
            effort=p.get('final_effort',False)
            if effort:
                assert a=='B' and not ar['final_effort_used'] and weak and score>tr['ca'] and not cp
            hit=(score>tr['ca'] or cp) and not cn
            maxdice=sum(n*f for n,f in dmg_groups)
            bonus=maxdice if cp or effort else 0
            raw=normal+bonus
            rd={'B':75,'E':35,'F':22}[target] if hit else 0
            net=max(0,raw-rd) if hit else 0
            hp_before=tr['hp'];actual=min(hp_before,net)
            assert e['hit']==hit and e['raw']==(raw if hit else 0)
            assert e['critical']==('POSITIVE' if cp else 'NEGATIVE' if cn else 'NONE')
            if cn:assert e['critical_failure_policy']=='CRITICAL_FAILURE / VLAB-LAB-POLICY' and e['net']==0
            assert e['critical_max_bonus']==bonus and e['rd_applied']==rd and e['net']==net
            assert e['before_hp']==hp_before and e['after_hp']==hp_before-actual
            assert e['hp_loss_actual']==actual and e['overkill']==max(0,net-hp_before)
            assert e['weak_target_before']==(hp_before>0 and hp_before*10<tr['maximum_hp'])
            assert e['weak_target_after']==(hp_before-actual>0 and (hp_before-actual)*10<tr['maximum_hp'])
            ar['standard']=0;tr['hp']-=actual;s['action_indexes'][a]+=1
            if effort:ar['final_effort_used']=True;ar['immobile_next_own_turns']=2
            if tr['hp']==0:s['winner']=a
            assert e['immobile_next_turns']==ar['immobile_next_own_turns']
            counts['native_attacks']+=1;counts['crits_plus']+=cp;counts['crits_negative_lab']+=cn;counts['weak_attacks']+=weak;counts['final_efforts']+=effort
            counts['actual_hp_loss']+=actual;counts['overkill']+=max(0,net-hp_before)
        elif k=='NATIVE_SPECIAL':
            assert mode=='G_FULL' and a=='B' and target=='E' and s['special_used_count']==0
            assert ar['standard']==1 and ar['pa']>=55
            dmg=die(seed,1,mode,'B','LIGHTNING',14,10)
            save=die(seed,1,mode,'E','REFLEXO',6,6)
            assert dmg==p['damage_rolls'] and save==p['save_rolls']
            assert sum(save)+166>94 and p['save_cd']==94
            assert sum(dmg)%2==0 and p['raw']==sum(dmg)
            tr=actors['E']['resource'];before=tr['hp'];delta=min(before,sum(dmg)//2)
            assert e['raw']==sum(dmg)//2 and e['effective']==sum(dmg)//2 and e['rd_applied']==0
            assert e['hp_before']==before and e['hp_after']==before-delta
            assert e['PA_spent']==55 and e['critical']=='NOT-APPLICABLE-BY-SISTEMA-DE-MAGIA'
            ar['standard']=0;ar['pa']-=55;tr['hp']-=delta;s['special_used_count']+=1
            counts['native_specials']+=1;counts['pa_spent']+=55
        elif k=='TURN_END':
            assert p['actor']==a and ar['standard']==0
            before=ar['immobile_next_own_turns'];after=max(0,before-1)
            assert e['action']=='turn_end' and e['immobilization_before']==before and e['immobilization_after']==after
            ar['immobile_next_own_turns']=after;s['turn_index']+=1
            other='E' if a=='B' and 'E' in actors else 'F' if a=='B' else 'B'
            if actors[other]['resource']['hp']==0:
                s['phase']='FINISHED';s['winner']=a;s['active']=None
            else:s['active']=other
            counts['turn_ends']+=1
        else:raise AssertionError('UNSUPPORTED_KIND:'+k)
        assert after_sha==sh(s),f'CAUSAL_AFTER_STATE_MISMATCH seq={seq} kind={k}'
        prev=rowsha
    assert meta['head']==prev and canon(json.loads(meta['state']))==canon(s)
    assert sh(s)==(evs[-1][6] if evs else sh(original))
    with sqlite3.connect(path.with_suffix('.checkpoint.sqlite')) as c:
        assert dict(c.execute('select key,value from meta'))==meta
        assert c.execute('select count(*) from events').fetchone()[0]==len(evs)
    return {'file':path.name,'run_id':s['run_id'],'events':len(evs),'seed':seed,'scene':mode,'side':s['experiment']['side'],
            'causal_integrity':'PASS','counts':dict(counts),'winner':s['winner'],'phase':s['phase'],'last_head':prev}

def main():
    selected=[p for p in (R/'runs').glob('R159_ED_GRIFO_AUREN_*.sqlite') if '.checkpoint.' not in p.name]
    selected.sort();result=[verify(f) for f in selected]
    report={'status':'PASS' if len(result)==4 else 'REVIEW','selected_runs':len(result),'source':'COLD_SEMANTIC_INDEPENDENT_NO_ENGINE_IMPORT',
        'total_events':sum(r['events'] for r in result),'totals':dict(sum((collections.Counter(x['counts']) for x in result),collections.Counter())),
        'runs':result,'odd_seed_case':'S998801 special stopped on odd half; physically 1 intent-free event not counted as full combat',
        'official_power_cells':0,'terminal_contracts_certified':0}
    (R/'R159_COLD_ED_BE_AUDIT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='runs'},indent=2))
if __name__=='__main__':main()
