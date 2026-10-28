"""R200/R201/R202/R203 TEST-only source-grounded Orc profile and physical equipment.
No rewriting of historical gear; magical ring grade is NOT source-certified.
"""
from __future__ import annotations
import hashlib,json,random
from fractions import Fraction
RANKS=['COMUM','BRONZE','PRATA','OURO','OURO_NEGRO','LENDARIO']
CHASSIS={'improvisada':(1,3),'adaga':(1,4),'leve_marcial':(1,6),'espada':(1,8),'arco':(1,8),'lanca':(1,8),'pesada':(1,10),'brutal':(2,6)}
ARMOR={'LEVE':(3,2,Fraction(1)),'MEDIA':(7,2,Fraction(3,4)),'PESADA':(10,4,Fraction(1,2))}
SOURCES={'creation':'https://app.notion.com/p/3ebc2b324ede81449222f3c06b840613','combat':'https://app.notion.com/p/3ebc2b324ede81f1be4be8804ac113c0','beast':'https://app.notion.com/p/3ebc2b324ede81f4992ac88a3588cacd','dmg':'https://app.notion.com/p/3f2c2b324ede815498cddb7844245f7e','ring':'https://app.notion.com/p/168c2b324ede82d6b8ce013ec82217ad','galinha':'https://app.notion.com/p/eddc2b324ede829f8a75011e8acbf429','wolf':'https://app.notion.com/p/be5c2b324ede832e8b7a81c5460571c1','master_prospective':'https://app.notion.com/p/3ffc2b324ede81c5a5c3d56cc6a29f84'}

def weapon(kind,rank):
    n,s=CHASSIS[kind];return (n*(RANKS.index(rank)+1),s)
def armor(kind,rank):
    base,step,mobility=ARMOR[kind]; return {'physical_ca':base+step*RANKS.index(rank),'speed_factor_num':mobility.numerator,'speed_factor_den':mobility.denominator}
def ff_roll(level):
    h=hashlib.sha256(f'R200|ED-REF-01|FF-MILESTONE-{level}'.encode()).digest();return random.Random(int.from_bytes(h,'big')).randint(1,4)
def build_profile(level=1):
    assert 1<=level<=25
    # Orc racial 25 starting +12 FOR/DES/CON. 37 total; deterministic planned deltas for first five transitions only.
    initial={'FOR':15,'DES':8,'CON':5,'INT':4,'SAB':3,'CAR':2}
    if level>6: raise ValueError('UNVALIDATED_LEVEL_GT6: LEVELUP bridge/source and choices not reviewed')
    progression=[{'FOR':1,'DES':1,'CON':2,'INT':1},{'FOR':1,'DES':1,'CON':1,'INT':2},{'FOR':1,'DES':1,'CON':2,'INT':1},{'FOR':1,'DES':1,'CON':1,'INT':2},{'FOR':1,'DES':1,'CON':1,'INT':2}]
    attrs=initial.copy()
    for j in range(level-1):
        for k,v in progression[j].items():attrs[k]+=v
    assert sum(initial.values())==37 and sum(attrs.values())==37+5*(level-1)
    rank='BRONZE' if level<=5 else 'PRATA'
    # Orc Life +2 die categories: Bronze d10 fixed 6, Prata d12 fixed 7; Alma normal Bronze d6 fixed4, Prata d8 fixed5.
    life_initial=10+initial['CON'];alma_initial=10+initial['INT']
    if level<=5:
        # Per-level growth is NOT retroactive within one classification.
        hist=[];prev=initial.copy()
        for j in range(level):
            if j>0:
                for k,v in progression[j-1].items():prev[k]+=v
            hist.append(dict(hp=6+prev['CON'],pa=4+prev['INT']))
        hp=life_initial+sum(z['hp'] for z in hist);pa=alma_initial+sum(z['pa'] for z in hist)
    else:
        hist=[];hp=life_initial+level*(7+attrs['CON']);pa=alma_initial+level*(5+attrs['INT'])
    ff=10*sum(attrs[k] for k in ('FOR','DES','CON'))
    milestones={str(i):{'purpose':'DAMAGE','roll_d4':ff_roll(i),'permanent_seed_label':f'R200|ED-REF-01|FF-MILESTONE-{i}'} for i in range(1,ff//100+1)}
    dmg_ff=sum(x['roll_d4'] for x in milestones.values())
    armor_def=armor('LEVE',rank)
    # Orc formula 12 + DES/4 + CON + armor. All values exact Fraction.
    racial_base=Fraction(12)+Fraction(attrs['DES'],4)+attrs['CON']
    attack_stat=attrs['FOR']; init_stat=attrs['DES']
    return {'id':'ED-REF-01','role':'COMBATENTE_EQUILIBRADO','race':'ORC','level':level,'rank':rank,
       'rank_star':level if level<=5 else level-5,'natural_initial':initial,'natural_current':attrs,
       'initial_distribution':{'baseline':{'FOR':6,'DES':5,'CON':5,'INT':4,'SAB':3,'CAR':2},'orc_racial':{'FOR':9,'DES':3,'CON':0,'INT':0,'SAB':0,'CAR':0}},
       'progression':progression[:level-1],'natural_hp_max':hp,'natural_pa_max':pa,
       'proficiencies':['Lutar(FOR)','Iniciativa(DES)','Reflexo(DES)','Fortitude(CON)','Vontade(SAB)','Arcanismo(INT)'],
       'luta_prof_bonus':2,'initiative_prof_bonus':2,'ff':ff,'ff_milestones':milestones,'ff_damage_bonus':dmg_ff,
       'weapon':{'kind':'espada','rank':rank,'physical_dice':weapon('espada',rank),'magic_layer':None},
       'armor':{'kind':'LEVE','rank':rank,**armor_def,'magic_layer':None},'ca_racial_exact':str(racial_base),
       'ca_physical_exact':str(racial_base+armor_def['physical_ca']),
       'ring_proxy':{'original_source':SOURCES['ring'],'magic_ca_bonus':2,'daily_pa_literal':13,'rank':'NOT_PUBLISHED','eligibility':'NOT_CERTIFIED_TEST_ONLY','paid_at_entry':'LAB_CONVENTION_NOT_NORMATIVE'},
       'physical_damage_modifier_source':{'FF':dmg_ff,'FOR_addition':0,'reason':'DMG-RANK chassi does not automatically add FOR without explicit weapon source'},
       'life_and_alma_growth_fixed':'60_PERCENT_OFFICIAL','transform':'PROHIBITED' if level<=5 else 'ELIGIBLE_ONLY_NO_SPIRIT_IDENTIFIED',
       'derived_source':SOURCES['creation'],'status':'TEST_DOCUMENTED_CHOICES_NOT_NATIVE_LEVELUP_ENGINE_VERIFIED'}

def state(profile,magic_on=False):
    layer=2 if magic_on else 0
    # Ring is an isolated overlay proxy: never class-certified; no power beyond the +2 published.
    return {'profile':profile['id'],'level':profile['level'],'weapon_dice':profile['weapon']['physical_dice'],
     'armor_physical_ca':profile['armor']['physical_ca'],'mobility':profile['armor']['speed_factor_num'] / profile['armor']['speed_factor_den'],
     'hp':profile['natural_hp_max'],'base_pa':profile['natural_pa_max'],
     'ca':str(Fraction(profile['ca_physical_exact'])+layer),
     'ring_magic_on':magic_on,'ring_ca_bonus':layer,
     'ring_PA_daily_debited_TEST':13 if magic_on else 0,'pa_free_at_entry':profile['natural_pa_max']-(13 if magic_on else 0),
     'magic_source_rank_admitted':False,'status':'EXPERIMENTAL_UNRANKED_RING_PROXY_NOT_ELIGIBLE_FOR_CERTIFIED_BATTERY_E'}

if __name__=='__main__':
    import pathlib
    p=pathlib.Path(__file__).resolve().parents[1]/'evidence'
    p.mkdir(exist_ok=True)
    sample={'actor':build_profile(1),'prata_1':build_profile(6)}
    sample['states']={str(l):{mode:state(build_profile(l),on) for mode,on in [('COM_MAGIA',True),('SEM_MAGIA',False)]} for l in (1,6)}
    (p/'R200_ED_REF_01_B1_P1_PROFILES.json').write_text(json.dumps(sample,indent=2,ensure_ascii=False))
    print(json.dumps({'B1_HP':sample['actor']['natural_hp_max'],'B1_PA':sample['actor']['natural_pa_max'],'B1_FF':sample['actor']['ff'],'P1_HP':sample['prata_1']['natural_hp_max'],'P1_PA':sample['prata_1']['natural_pa_max']}))
