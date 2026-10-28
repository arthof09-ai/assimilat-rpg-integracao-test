"""IBX-113 correction: explicit SYNTHETIC fixtures, never campaign history.
Rules source: Notion Criação de Ficha, 2026-10-09 revision.
No Notion I/O. Builds independently auditable 0..19 timeline and receipt amendments.
"""
import json, hashlib
from pathlib import Path
OUT=Path(__file__).parent
ATTRS=('FOR','DES','CON','INT','SAB','CAR')
INITIAL={'FOR':6,'DES':5,'CON':5,'INT':4,'SAB':3,'CAR':2}
# 17 explicitly synthetic +2 allocations. L17 +2 SAB inspired by R144 layout,
# NOT claiming R144 was executed upon R201.
STEPS=[{'INT':2},{'CON':2},{'DES':2},{'INT':2},{'CON':2},
       {'DES':2},{'INT':2},{'CON':2},{'DES':2},{'SAB':2},
       {'INT':2},{'CON':2},{'CAR':2},{'DES':2},{'CON':1,'INT':1},
       {'SAB':2},{'SAB':2}]
RANK=((1,5,'Bronze',4),(6,10,'Prata',5),(11,15,'Ouro',6),(16,20,'Ouro Negro',7),(21,25,'Lendario',12))
# Canon fixed 60%: d6=4 d8=5 d10=6 d12=7 d20=12
GROWTH_SEED='e03f98baac4f5850830852fac5c837def162da0e80c9b7b6ff33d5f1de023bd1'
FF_SEED='3baca309f8ef498c1f94d7359adeaa225ab9d6aeb3fab71b57f686274336ed2a'
GROWTH_LABELS=('L18_VIDA_1D12_PLUS10','L18_ALMA_1D12_PLUS8','L19_VIDA_1D12_PLUS11','L19_ALMA_1D12_PLUS9')
assert sum(INITIAL.values())==25 and all(2<=i<=6 for i in INITIAL.values())
assert len(STEPS)==17 and all(sum(s.values())==2 for s in STEPS)

def rank(level):
    for low,high,r,d in RANK:
        if low<=level<=high:return r,d
    raise AssertionError(level)

def value(seed,label,sides):
    c=0
    while True:
        dg=hashlib.sha256(f'{seed}|{label}|{c}'.encode()).digest()
        # Existing R202 d12 rejection 252; d4 trivial 256 multiple of four.
        if sides==4 or dg[0]<252: return 1+dg[0]%sides
        c+=1

assert hashlib.sha256(bytes.fromhex(GROWTH_SEED)).hexdigest()=='945a30bf99d540a873e3eddc8a801b8cc95e27d36cb66dcd9a066beca5c27783'
assert hashlib.sha256(bytes.fromhex(FF_SEED)).hexdigest()=='e2979cdc4c1052db520a20535760998a04720035e6b81c8ff18f16eef6d9ac8e'
assert [value(GROWTH_SEED,l,12) for l in GROWTH_LABELS]==[5,12,8,9]
assert value(FF_SEED,'FF300_CA_1D4',4)==2

attrs=INITIAL.copy(); hp=10+attrs['CON']; pa=10+attrs['INT']; hist=[]
prev_ff=10*(attrs['FOR']+attrs['DES']+3+attrs['CON']); assert prev_ff==190
# Synthetic equipment active in every synthetic projection; no campaign event date.
# FF100 was already satisfied at fixture level zero; FF200 first at level 2,
# FF300 first at level 9. 100/200 have synthetic test-only Damage d4 values,
# not actual random rolls or campaign locks.
locks={'100':{'choice':'DANO','value':2,'provenance':'IBX113_TEST_DETERMINISTIC_NOT_CAMPAIGN','first_level':0},
       '200':{'choice':'DANO','value':3,'provenance':'IBX113_TEST_DETERMINISTIC_NOT_CAMPAIGN','first_level':2},
       '300':{'choice':'CA','value':2,'provenance':'R202_COMMITTED_REPLAY_RETRO_FITTED_SYNTHETIC_ONLY','first_level':9}}

def state(level,changes,rebase=None,rolls=None):
    eff={k:attrs[k]+({'DES':3,'SAB':2}.get(k,0)) for k in ATTRS}
    ff=10*(eff['FOR']+eff['DES']+eff['CON'])
    active={k:v for k,v in locks.items() if ff>=int(k)}
    ca=6+eff['DES']+4+sum(v['value'] for v in active.values() if v['choice']=='CA')
    return {'level':level,'rank':rank(level)[0] if level else 'Criação','attribute_grants':changes,
            'naturals':attrs.copy(),'natural_sum':sum(attrs.values()),'expected_natural':25+2*level,
            'effective':eff,'hp_max':hp,'pa_max':pa,'hp_current':240 if level==17 else None,
            'pa_current':150 if level==17 else None, 'pa_committed':30,'pa_free':pa-30,
            'ff':ff,'ca':ca,'ff_locks_active':sorted(active),'rank_rebase':rebase,'growth_die_values':rolls,
            'title_SAB':2,'equipment_DES':3,'armor_synthetic_CA':4}

hist.append(state(0,{},rebase='INITIAL_10_PLUS_CON_OR_INT',rolls=[]))
for level,alloc in enumerate(STEPS,1):
    old=attrs.copy()
    for k,v in alloc.items():attrs[k]+=v
    r,fix=rank(level)
    rebase=None
    if level in (6,11,16):
        rebase=f'{r.upper()}_REBASE_ALL_{level}_LEVELS_FIXED60_{fix}'
        hp=15+level*(fix+attrs['CON'])
        pa=14+level*(fix+attrs['INT'])
    else:
        hp+=fix+attrs['CON']
        pa+=fix+attrs['INT']
    hist.append(state(level,alloc,rebase,[fix,fix]))
    assert sum(attrs.values())==25+2*level

assert hist[16]['naturals']=={'FOR':6,'DES':13,'CON':14,'INT':13,'SAB':7,'CAR':4}
assert hist[17]['naturals']=={'FOR':6,'DES':13,'CON':14,'INT':13,'SAB':9,'CAR':4}
assert [hist[17][k] for k in ('natural_sum','hp_max','pa_max','ff','ca')]==[59,372,354,360,28]
first_200=next(p['level'] for p in hist if p['ff']>=200)
first_300=next(p['level'] for p in hist if p['ff']>=300)
assert first_200==2 and first_300==9 and all(p['ff']<400 for p in hist)

old={'FOR':6,'DES':10,'CON':10,'INT':8,'SAB':7,'CAR':4}
delta={k:attrs[k]-old[k] for k in ATTRS}
assert sum(delta.values())==14

for n,alloc in ((18,{'DES':2}),(19,{'CON':1,'INT':1})):
    for k,v in alloc.items():attrs[k]+=v
    q=0 if n==18 else 2
    dice=[value(GROWTH_SEED,l,12) for l in GROWTH_LABELS[q:q+2]]
    hp+=dice[0]+attrs['CON']; pa+=dice[1]+attrs['INT']
    hist.append(state(n,alloc,None,dice))
    assert sum(attrs.values())==25+2*n

assert [hist[18][k] for k in ('hp_max','pa_max','ff','ca')]==[391,379,380,30]
assert [hist[19][k] for k in ('hp_max','pa_max','ff','ca')]==[414,402,390,30]
assert hist[19]['natural_sum']==63

obj={'identity':'IBX17-R201-SYNTHETIC-HUMAN','nature':'TEST_RECONSTRUCTION_NOT_CAMPAIGN_HISTORY',
     'ibx113':'IBX-113','parent_page':'3fec2b324ede8179a8d4f94886ff7510',
     'source_original_r144_is_readonly':True,'initial_attributes':INITIAL,
     'historical_missing14_distribution':delta,'ff_locks':locks,
     'external_layers':{'DES_equipment':3,'SAB_title':2,'CA_armor_reconciled_from23':4},
     'roll_receipts':{'growth_seed_commit_sha256':'945a30bf99d540a873e3eddc8a801b8cc95e27d36cb66dcd9a066beca5c27783','growth_dice':[5,12,8,9],
                      'ff300_seed_commit_sha256':'e2979cdc4c1052db520a20535760998a04720035e6b81c8ff18f16eef6d9ac8e','ff300_ca_d4':2,
                      'original_modifiers_invalidated':[10,8,11,9],'revised_modifiers':[14,13,15,14],
                      'revised_increments':[19,25,23,23],'note':'Original dice numbers remain, old arithmetic bonuses are superseded'},
     'history':hist}
canonical=json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
obj['ledger_sha256']=hashlib.sha256(canonical).hexdigest()
(OUT/'IBX113_SYNTHETIC_LEDGER_LEVEL0_TO19.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
print('LOCKS first200',first_200,'first300',first_300,'add14',delta)
for p in hist:
    print(p['level'],p['attribute_grants'],'sum',p['natural_sum'],'HP',p['hp_max'],'PA',p['pa_max'],'FF',p['ff'],'CA',p['ca'],p['rank_rebase'] or '')
print('LEDGER',obj['ledger_sha256'])
