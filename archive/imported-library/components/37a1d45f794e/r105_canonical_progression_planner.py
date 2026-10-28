"""R105: source-bound, nonmutating preview planner (NOT a replacement for R17/R30).
Canonical evidence: Notion Mestre Criação de Ficha, edited 2026-10-09T04:07:06.313Z.
This module validates *explicit* synthetic allocations/dice policy and yields
preview receipts. Never rolls randomly, grants player consent, or writes Notion.
"""
import copy, json
from dataclasses import dataclass
from pathlib import Path
from ibx17_native_contract_v1 import fp
SOURCE_URL='https://app.notion.com/p/3ebc2b324ede81449222f3c06b840613'
SOURCE_LAST_EDITED='2026-10-09T04:07:06.313Z'
ATTRS=('FOR','DES','CON','INT','SAB','CAR')
RANKS=('Bronze','Prata','Ouro','Ouro Negro','Lendario')
LIFE_DICE={'Bronze':6,'Prata':8,'Ouro':10,'Ouro Negro':12,'Lendario':20}
FIXED60={6:4,8:5,10:6,12:7,20:12}
class Hold(ValueError): pass

def rank_at(level):
    if level==0:return None
    if not isinstance(level,int) or not 1<=level<=25:raise Hold('invalid level')
    return RANKS[(level-1)//5]

def fixed_growth(level):
    """Only use when caller has chosen the fixed 60% policy."""
    return FIXED60[LIFE_DICE[rank_at(level)]]

def require_attrs(attrs,initial=False):
    if set(attrs)!=set(ATTRS):raise Hold('missing/extra attributes')
    if any(not isinstance(v,int) or isinstance(v,bool) or v<0 for v in attrs.values()):raise Hold('invalid natural attributes')
    if initial and (sum(attrs.values())!=25 or any(v<2 or v>6 for v in attrs.values())):
        raise Hold('Humano initial allocation violates 25 points or creation range 2–6')

def explicit_delta(delta):
    if set(delta)!=set(ATTRS) or any(not isinstance(v,int) or isinstance(v,bool) or v<0 for v in delta.values()) or sum(delta.values())!=2:
        raise Hold('Human evolution requires exact 2-point explicit allocation per star')

def generate(initial:dict,choices:list[dict], modes:list[str], initial_hp=None, initial_pa=None):
    """All level choices must be independently supplied; no implicit default choices.

    For a level crossing rank, the canonical rebase *replaces* prior natural
    progression; it is not added. Synthetic fixture uses no equipment/titles,
    no transformation, no tiered dice enhancements. No FF milestone allowed
    unless separate permanent lock+roll data exist.
    """
    require_attrs(initial,initial=True)
    if len(choices)!=len(modes) or len(choices)>25:raise Hold('every level requires a choice + growth policy')
    if any(x!='FIXED60_EXPLICIT' for x in modes):raise Hold('missing/unknown official growth choice')
    if initial_hp is not None or initial_pa is not None:raise Hold('initial resource overrides require independent authority')
    initial_hp=10+initial['CON'];initial_pa=10+initial['INT']
    attrs=copy.deepcopy(initial);hp=initial_hp;pa=initial_pa
    history=[{'level':0,'rank':None,'attrs':copy.deepcopy(attrs),
              'hp_max':hp,'pa_max':pa,'ff':(attrs['FOR']+attrs['DES']+attrs['CON'])*10,
              'ca':6+attrs['DES'],'before_level':None,'synthetic_fixture':True}]
    if history[0]['ff']>=100:raise Hold('FF lock history at creation required')
    for i,(delta,mode) in enumerate(zip(choices,modes),start=1):
        explicit_delta(delta)
        for k in ATTRS:attrs[k]+=delta[k]
        new_rank=rank_at(i);roll=fixed_growth(i)
        rank_changed=i==1 or rank_at(i-1)!=new_rank
        if i==1:
            hp=initial_hp+roll+attrs['CON'];pa=initial_pa+roll+attrs['INT']
            action='FIRST_LEVEL_FIXED60'
        elif rank_changed:
            # Rank rules recalc ALL levels at current rank die and current CON/INT.
            hp=initial_hp+i*roll+i*attrs['CON']
            pa=initial_pa+i*roll+i*attrs['INT']
            action='RANK_REBASE_REPLACE_NATURAL'
        else:
            hp+=roll+attrs['CON'];pa+=roll+attrs['INT']
            action='SAME_RANK_ADD_ONCE'
        ff=(attrs['FOR']+attrs['DES']+attrs['CON'])*10
        if ff>=100:raise Hold('physical FF100 lock roll/choice not supplied: do not invent')
        history.append({'level':i,'before_level':i-1,'rank':new_rank,
            'attrs':copy.deepcopy(attrs),'hp_max':hp,'pa_max':pa,'ff':ff,
            'ca':6+attrs['DES'],'fixed_die_value':roll,
            'natural_allocation':copy.deepcopy(delta),'mode':mode,
            'rank_changed':rank_changed,'calculation':action,
            'synthetic_fixture':True,'player_approval':False})
    return {'source_url':SOURCE_URL,'source_last_edited':SOURCE_LAST_EDITED,
            'contract':'LEVEL_0_TO_N_PREVIEW_LOCAL',
            'input_provenance':'SYNTHETIC_EXPLICIT_TEST_ONLY',
            'initial_attributes':initial,'initial_resource_hp':initial_hp,'initial_resource_pa':initial_pa,
            'levels':history, 'preview_hash_sha256':fp(history),
            'notion_native_commits':0, 'real_player_confirmation':False,
            'required_for_real_execution':['real character identity and current source','per-level attributes allocated by player','dice roll or player fixed-60% choice for each level','FF first-hit milestone choices/roll receipts if encountered','effect/item/Spirit conditions and activation receipts','explicit preview approval']}

BASE={'FOR':2,'DES':3,'CON':2,'INT':6,'SAB':6,'CAR':6}
def delta(**kwargs):return {k:kwargs.get(k,0) for k in ATTRS}

def run():
    first=generate(BASE,[delta(FOR=2)],['FIXED60_EXPLICIT'])
    assert first['levels'][0]['hp_max']==12 and first['levels'][0]['pa_max']==16
    a=first['levels'][1]
    assert (a['level'],a['rank'],a['hp_max'],a['pa_max'],a['ff'],a['ca'])==(1,'Bronze',18,26,90,9)
    three=generate(BASE,[delta(FOR=2),delta(INT=2),delta(SAB=2)],['FIXED60_EXPLICIT']*3)
    assert [x['hp_max'] for x in three['levels']]==[12,18,24,30]
    assert [x['pa_max'] for x in three['levels']]==[16,26,38,50]
    six=generate(BASE,[delta(FOR=2)]+[delta(INT=2)]*5,['FIXED60_EXPLICIT']*6)
    rank=six['levels'][6]
    assert rank['rank']=='Prata' and rank['calculation']=='RANK_REBASE_REPLACE_NATURAL'
    assert rank['hp_max']==54 and rank['pa_max']==142
    adversarial=[
      lambda:generate(BASE,[delta(FOR=1)],['FIXED60_EXPLICIT']),
      lambda:generate(BASE,[delta(FOR=2)],[]),
      lambda:generate(BASE,[delta(FOR=2)],['MISSING']),
      lambda:generate({**BASE,'FOR':3},[delta(FOR=2)],['FIXED60_EXPLICIT']),
      lambda:generate({'FOR':6,'DES':5,'CON':5,'INT':4,'SAB':3,'CAR':2},[delta(FOR=2)],['FIXED60_EXPLICIT']),
      lambda:generate(BASE,[delta(FOR=2),delta(CON=2)],['FIXED60_EXPLICIT']*2),
    ]
    rejected=[]
    for index,case in enumerate(adversarial):
        try:case()
        except Hold as e: rejected.append({'case':index,'reason':str(e)})
        else:raise AssertionError(f'unguarded case {index}')
    data={'status':'PASS_LOCAL_PREVIEW_ONLY','canonical_source':SOURCE_URL,
        'models':[{'case':'0_TO_1','result':first},{'case':'0_TO_3','result':three},
                  {'case':'0_TO_6_BRONZE_TO_PRATA','result':six}],
        'rejected_cases':rejected,
        'passed_assertions':3,'rejected_cases_count':len(rejected),
        'current_next':'NATIVE_APPLICATION_HOLD (no player confirmation; demonstration local fixture only)',
        'nonclaimed':['Notion TEST execution','R17 native engine rerun','new actual dice or player choices','canonical rule change']}
    path=Path(__file__).with_name('R105_CANONICAL_PREVIEW_LOCAL_20261016.json')
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({'result':'PASS_LOCAL_PREVIEW','assertions':3,'rejections':len(rejected),
      'level0_to_1':{k:a[k] for k in ['level','rank','hp_max','pa_max','ff','ca']},
      'sixth_rank':rank['rank'],'output':str(path)},ensure_ascii=False))
if __name__=='__main__':run()
