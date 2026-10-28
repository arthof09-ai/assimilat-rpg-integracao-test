"""R201-202 source-only independent fixture auditor (TEST, not LEVEL-UP native API).
Reads R200 profiles as DATA (not builder code); source rules re-derived independently.
"""
import json,hashlib,pathlib
from fractions import Fraction
root=pathlib.Path(__file__).resolve().parents[1]
p=root/'source/R201_ED_REF_01_SOURCE_PROFILE_SNAPSHOTS.json'
levels=json.loads(p.read_text())
initial={'FOR':15,'DES':8,'CON':5,'INT':4,'SAB':3,'CAR':2}
racial={'FOR':9,'DES':3,'CON':0,'INT':0,'SAB':0,'CAR':0}
base={k:initial[k]-racial[k] for k in initial}
assert sum(initial.values())==37 and sum(base.values())==25 and sum(racial.values())==12
assert all(5<=initial[k]<=15 for k in ('FOR','DES','CON'))
assert all(initial[k]>=0 for k in initial)
for i in range(1,7):
    a=levels[str(i)]
    assert a['id']=='ED-REF-01' and a['race']=='ORC' and a['level']==i
    attr=a['natural_current'];assert sum(attr.values())==37+5*(i-1)
    assert len(a['progression'])==i-1 and all(sum(x.values())==5 for x in a['progression'])
    expected=initial.copy()
    for step in a['progression']:
        for k,v in step.items():expected[k]+=v
    assert attr==expected
    assert a['ff']==10*sum(attr[x] for x in ('FOR','DES','CON'))
    rank='BRONZE' if i<=5 else 'PRATA'
    assert a['rank']==rank and a['rank_star']==(i if i<=5 else 1)
    assert a['weapon']['physical_dice']==([2,8] if i<=5 else [3,8])
    assert a['armor']['physical_ca']==(5 if i<=5 else 7)
    ca=Fraction(12)+Fraction(attr['DES'],4)+attr['CON']+a['armor']['physical_ca']
    assert Fraction(a['ca_physical_exact'])==ca
    # Built from source Rule 5, not by reimporting LEVEL-UP code
    if i<=5:
        con=int(initial['CON']);inte=int(initial['INT']);hp=10+con;pa=10+inte
        for lv in range(1,i+1):
            if lv>1:
                st=levels[str(i)]['progression'][lv-2]
                con+=st.get('CON',0);inte+=st.get('INT',0)
            hp+=6+con;pa+=4+inte
    else:
        hp=10+initial['CON']+i*(7+attr['CON'])
        pa=10+initial['INT']+i*(5+attr['INT'])
    assert a['natural_hp_max']==hp and a['natural_pa_max']==pa
    assert a['transform']=='PROHIBITED' if i<=5 else a['transform'].startswith('ELIGIBLE_ONLY_NO_SPIRIT')
    assert len(a['proficiencies'])==2+initial['INT']
    assert len(a['ff_milestones'])==a['ff']//100
    assert a['ring_proxy']['rank']=='NOT_PUBLISHED'
assert levels['1']['natural_hp_max']==26 and levels['1']['natural_pa_max']==22
assert levels['2']['natural_hp_max']==39 and levels['2']['natural_pa_max']==31
assert levels['5']['natural_hp_max']==86 and levels['5']['natural_pa_max']==68
assert levels['6']['natural_hp_max']==129 and levels['6']['natural_pa_max']==116
report={'status':'PASS_R201_ED_REF01_SOURCE_RULE_CHECK','profiles_checked':6,'levels':[1,2,3,4,5,6],
        'HP_PA':{str(i):[levels[str(i)]['natural_hp_max'],levels[str(i)]['natural_pa_max']] for i in range(1,7)},
        'level6_ca_exact':levels['6']['ca_physical_exact'],'progression_orc':'+5_PER_LEVEL','classification_rebase':'REPLACE_NATURAL',
        'native_LEVELUP_engine_called':False,'native_parity':'PENDING','master_new_equipment_rules':'TEST_PROSPECTIVE',
        'source_refs':['https://app.notion.com/p/3ebc2b324ede81449222f3c06b840613','https://app.notion.com/p/3fcc2b324ede81aab6d5df4f337ce936'],
        'scope':'INDEPENDENT_SOURCE_CALCULATION_OF_EXISTING_R200_PROFILE_DATA_NOT_LEVELUP_EXECUTION',
        'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
out=root/'evidence/R201_ED_REF_01_SOURCE_RULE_AUDIT.json';out.write_text(json.dumps(report,indent=2,ensure_ascii=False))
print(json.dumps(report,indent=2,ensure_ascii=False))
