"""Source-formula derivation, no synthetic creature promoted and no combat simulation."""
import json,math,collections,itertools
from pathlib import Path
R=Path(__file__).resolve().parent
preregs={'Grifo_L2':{'FOR':110,'DES':112,'CON':80,'INT':70,'SAB':90,'CAR':35},
         'Grifo_L3':{'FOR':115,'DES':116,'CON':85,'INT':72,'SAB':94,'CAR':36}}
assert sum(preregs['Grifo_L2'].values())==497==35+22*21
assert sum(preregs['Grifo_L3'].values())==518==35+23*21

def derive(a,lv):
    return {'rank':f'Lendário {lv-20}★','regular_power_slot':lv,'level':lv,'stats':a,
            'HP_Titan':60+lv*(100+a['CON']),
            'Soul_Titan':60+lv*(100+a['INT']),
            'CA_Titan':20+a['DES']+a['CON']//5,
            'RD_Titan':75,'prof_Titan':22,'base_damage_Titan':'20d10',
            'attack_talon_using_DES':f'6d6+{a["DES"]+22}',
            'speed_m_from_source_formula':34+a['DES']/4}
l2=derive(preregs['Grifo_L2'],22);l3=derive(preregs['Grifo_L3'],23)
assert (l3['HP_Titan'],l3['Soul_Titan'],l3['CA_Titan'],l3['attack_talon_using_DES'])==(4315,4016,153,'6d6+138')
assert (l2['HP_Titan'],l2['Soul_Titan'],l2['CA_Titan'],l2['attack_talon_using_DES'])==(4020,3800,148,'6d6+134')
lineage={'sources':{'numeric_fullspec':'https://app.notion.com/p/3f3c2b324ede813987deda0b382e83c7',
                    'creation':'https://app.notion.com/p/3ebc2b324ede81f4992ac88a3588cacd',
                    'grifo_individual':'https://app.notion.com/p/3f2c2b324ede81f9add8c37889e5a772'},
         'status':'SOURCE_DERIVED_L2_EXPERIMENTAL_CANDIDATE_NOT_REAL_MATERIALIZED_BESTA',
         'predecessor_L2':l2,'existing_fullspec_L3':l3,
         'L2_explicit_delta_from_source':{k:l3['stats'][k]-l2['stats'][k] for k in l2['stats']},
         'L2_L3_same_species_not_2_species':True,
         'unresolved':['earlier historical Matriarch state not physically attested as character','provenance of grant/equipment and current official materialization','scenario special attacks at L2 cannot be inherited without source'],
         'special_power_slots':{'26':{'tier':'ADM','equivalent_regular_rank_star_required':False,'lineage_variant':'PENDING'},
                                '27':{'tier':'Divina','equivalent_regular_rank_star_required':False,'lineage_variant':'PENDING'}}}
(R/'R104_GRIFO_L2_SOURCE_DERIVED.json').write_text(json.dumps(lineage,ensure_ascii=False,indent=2)+'\n')
# exact convolution of two 6d6 rolls, assuming independent equiprobable faces (math control, not campaign roll).
six=collections.Counter({0:1})
for i in range(6):
    nxt=collections.Counter()
    for total,ways in six.items():
        for face in range(1,7):nxt[total+face]+=ways
    six=nxt
assert sum(six.values())==6**6
n=6**12
# Grifo DES116 + possible documented L3 Titan prof 22 vs Auren init166
# score B + prof if trained; corpus doesn't prove training. Calculate bounded alternatives, do not adjudicate actual.
ways=0; ties=0
for b,wb in six.items():
 for a,wa in six.items():
    score_b=b+116+22;score_a=a+166
    if score_b>score_a:ways+=wb*wa
    if score_b==score_a:ties+=wb*wa
out={'source':'Sistema de Combate Iniciativa=6d6+DES+bonus de Iniciativa; Grifo fullspec gives generic +22 prof but no explicit Iniciativa-trained',
     'auren_initiative':'6d6+166 physically written','grifo_initiative_0_case':'6d6+116 conditional; max152 < Auren min172',
     'grifo_initiative_plus22_case':'6d6+138 conditional; max174 > Auren min172; both sides possible on rare dice',
     'croco_initiative_0_case':'6d6+64 max100, Auren min172',
     'croco_initiative_plus22_case':'6d6+86 max122, Auren min172',
     'assuming_generic_bonus_22_and_independent_6d6_math_only':{'grifo_goes_first_strict':ways,'ties':ties,'ordered_pair_outcomes':n,
                                                                  'strict_win_probability':ways/n,'tie_probability':ties/n},
     'minimum_missing_ruling':'Does this specific Besta apply +22 prof to its Initiative? Is Iniciativa trained by default for a Lendário Titã Besta? Do not invent training; tie rule separately use existing source.',
     'statutory_rating':'HOLD_NATURAL_INITIATIVE_NOT_RESOLVED',
     'no_new_fight':True}
(R/'R104_INITIATIVE_INTERVAL_GATE.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'L2':l2,'L3':l3,'init':out},ensure_ascii=False)[:4700])
