#!/usr/bin/env python3
"""R06 exact enumeration, deterministic MATH_ONLY addon to existing R04/R05 folder.
Reflection assumes 15% of positive damage AFTER RD25; returned nominal amount is before any attacker mitigation.
"""
from itertools import product
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
from math import floor,ceil
import json
ROOT=Path(__file__).resolve().parent

def dice(sides):
    return Counter(map(sum,product(*(range(1,s+1) for s in sides))))

def hit(ca,bon):
    d=dice((6,6));return F(sum(c for v,c in d.items() if v+54+bon>ca),36)

def expectations(sides,bon,rd=25):
    d=dice(sides);n=sum(d.values());p0=hit(68,bon);p1=hit(71,bon)
    harm=F(sum(max(0,54+x-rd)*c for x,c in d.items()),n)
    e_exact=harm*F(15,100)
    e_floor=F(sum(floor(F(15,100)*max(0,54+x-rd))*c for x,c in d.items()),n)
    e_ceil=F(sum(ceil(F(15,100)*max(0,54+x-rd))*c for x,c in d.items()),n)
    # Round half up non-negative
    e_half=F(sum(floor(F(15,100)*max(0,54+x-rd)+F(1,2))*c for x,c in d.items()),n)
    return dict(p0=p0,p1=p1, harm=harm, before=p0*harm,after=p1*harm,prevented=(p0-p1)*harm,reflection_exact=p1*e_exact,reflection_floor=p1*e_floor,reflection_nearest=p1*e_half,reflection_ceil=p1*e_ceil,reflection_conditional_exact=e_exact,reflection_conditional_floor=e_floor,reflection_conditional_nearest=e_half,reflection_conditional_ceil=e_ceil)

cases={'Patada':expectations((6,6),6),'Mordida':expectations((6,),7)}
assert cases['Patada']['p0']==F(10,36) and cases['Patada']['p1']==F(1,36)
assert cases['Mordida']['p0']==F(15,36) and cases['Mordida']['p1']==F(3,36)
assert cases['Patada']['before']==F(10) and cases['Patada']['after']==F(1)
assert cases['Mordida']['before']==F(325,24) and cases['Mordida']['after']==F(65,24)
assert cases['Patada']['prevented']==F(9)
assert cases['Mordida']['prevented']==F(65,6)
assert cases['Patada']['reflection_exact']==F(3,20)
assert cases['Mordida']['reflection_exact']==F(13,32)
for i in cases.values():
    assert i['reflection_floor']<=i['reflection_nearest']<=i['reflection_ceil']
    assert i['before']-i['after']==i['prevented']

def repr_f(x):return {'fraction':str(x),'decimal':round(float(x),8)}
summary={k:{kk:repr_f(v) for kk,v in x.items()} for k,x in cases.items()}
sum_avoided=sum((x['prevented'] for x in cases.values()),F(0))
sum_reflected=sum((x['reflection_exact'] for x in cases.values()),F(0))
assert sum_avoided==F(119,6)
assert sum_reflected==F(89,160)
# Costs: 20 activation + 3 per maintenance turn, with uncertainty of first turn
costs=[{'turns_covered':t,'activation_PA':20,'upkeep_including_first_turn_PA':3*t,'total_if_upkeep_on_first_turn_PA':20+3*t,'total_if_upkeep_starts_next_turn_PA':20+3*(t-1),'expected_avoided_HP_given_two_attempts_each_turn':repr_f(t*sum_avoided),'expected_nominal_reflection_exact_given_two_attempts_each_turn':repr_f(t*sum_reflected)} for t in (1,2,3,5,10)]
out={'operation':'OP-DMG-CORPUS-EMP-01','round':'R06_FAST_RESEARCH','baseline':'DMG-RANK-01 v1.1 unchanged','evidence':'MATH_ONLY; reuse R05 script and sourced sheets, no new readback from Notion','sourced_defense':'Behemoth Ouro1: Armadura de Gelo +3 CA, reflects 15% of damage received except spells and projectiles, 20PA cast and 3PA/turn maintain','assumptions':['Both Símio physical attacks are melee/nonprojectile, no magic on tested components','Printed Behemoth CA68 rises to 71 when Armor active','Gold normal RD25 both before and after Armor; no extra resistance by damage subtype','Símio Prata 2d6 test, FOR54, hypothetical Luta+6 for Patada and +7 Mordida','No crit, Reactions, extra effects, retargeting, armor action-delay, conditions or retaliation mitigation','Damage and to-hit rolls independent','Reflection measured after defender RD25, and nominal returned damage not further reduced by attacker resistance','Rounds of independent attempts, not real VLAB combat'],'source_ids':{'Símio':'301c2b324ede828caccb813d3979267a','Behemoth':'5dac2b324ede83f39cdb01a904ce3cfd'},'scenarios':summary,'two_attempts_one_each':{'expected_avoided_HP':repr_f(sum_avoided),'expected_reflected_nominal_exact':repr_f(sum_reflected),'expected_reflected_nominal_floor_per_hit':repr_f(sum(x['reflection_floor'] for x in cases.values())),'expected_reflected_nominal_round_half_up_per_hit':repr_f(sum(x['reflection_nearest'] for x in cases.values())),'expected_reflected_nominal_ceil_per_hit':repr_f(sum(x['reflection_ceil'] for x in cases.values()))},'PA_duration_sensitivity':costs,'rounding_scope':'Rounding on each reflected hit rather than end-of-round aggregation; both are unresolved. No adopted rounding rule','restrictions':'Reflections from magic or projectiles excluded; reflected damage final attacker HP loss unresolvable without attacker RD/resistance and order','blocked':['official Luta for Símio','Prata5 vs OuroNegro5 ancestry/title conflict','if armor activation costs Standard Action','if upkeep starts activation turn','reflection rounding scope/order','whether returned damage bypasses attacker own RD','legal Reaction availability','target specific resistances'], 'tests':'Exact-Fraction assertions passed; both attack cases and energy examples readback checked','canon_writes':0}
p=ROOT/'R06_RESULTS_FAST.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');re=json.loads(p.read_text(encoding='utf-8'));assert re['scenarios']==summary and re['two_attempts_one_each']==out['two_attempts_one_each']
print(json.dumps({'cases':summary,'two_attempts':out['two_attempts_one_each'],'costs':costs},ensure_ascii=False,indent=2))
print('PASS: script assertions and JSON readback')
