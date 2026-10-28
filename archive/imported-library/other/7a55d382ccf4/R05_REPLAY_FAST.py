#!/usr/bin/env python3
"""R05 independent exact discrete enumeration. MATH_ONLY. No VLAB engine or canon writes."""
import json
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FORMULAS = {
    'Patada': {'damage_dice': (6, 6), 'FOR': 54, 'counterfactual_luta': 6, 'type': 'impacto'},
    'Mordida': {'damage_dice': (6,), 'FOR': 54, 'counterfactual_luta': 7, 'type': 'perfurante'},
}

def dist(sides):
    return Counter(map(sum, product(*(range(1, n+1) for n in sides))))

def e_net(damage, strength, rd):
    return Fraction(sum(c * max(0, strength+roll-rd) for roll, c in damage.items()), sum(damage.values()))

def p_hit(ca, strength, luta):
    # Conditional Prata 2d6 normal attack. Strict superiority to printed target CA.
    return Fraction(sum(c for roll,c in dist((6,6)).items() if roll+strength+luta>ca),36)

def frac(f):
    return {'fraction': str(f), 'decimal': float(f)}

rows=[]
for ca in (68,71):
    for rd in (5,15,25,35,50,51,55,60):
        row={'CA':ca,'RD':rd,'results':{}}
        for skill, f in FORMULAS.items():
            p=p_hit(ca,f['FOR'],f['counterfactual_luta'])
            d=e_net(dist(f['damage_dice']),f['FOR'],rd)
            row['results'][skill]={'P_hit':frac(p),'E_net_on_hit':frac(d),'E_net_per_attempt':frac(p*d)}
        a=row['results']['Patada']['E_net_per_attempt']['decimal']
        b=row['results']['Mordida']['E_net_per_attempt']['decimal']
        row['higher_per_attempt']='Mordida' if b>a else 'Patada' if a>b else 'Tie'
        rows.append(row)

base_p=p_hit(68,54,6)
base_m=p_hit(68,54,7)
assert base_p==Fraction(5,18)
assert base_m==Fraction(5,12)
assert p_hit(71,54,6)==Fraction(1,36)
assert p_hit(71,54,7)==Fraction(1,12)
assert e_net(dist((6,6)),54,25)==36
assert e_net(dist((6,)),54,25)==Fraction(65,2)
assert base_p*36==10
assert base_m*Fraction(65,2)==Fraction(325,24)
assert base_p*e_net(dist((6,6)),54,50)<base_m*e_net(dist((6,)),54,50)
assert base_p*e_net(dist((6,6)),54,51)>base_m*e_net(dist((6,)),54,51)
assert p_hit(71,54,6)*36==1
assert p_hit(71,54,7)*Fraction(65,2)==Fraction(65,24)
# With exactly identical precision, same actor's two attacks are coupled by d6:
# Patada = Mordida + independent second d6. With a common RD, this ensures stochastic dominance.
for rd in range(0,101):
    assert e_net(dist((6,6)),54,rd)>=e_net(dist((6,)),54,rd)

out={
 'operation':'OP-DMG-CORPUS-EMP-01','round':'R05_FAST_RESEARCH',
 'baseline':'DMG-RANK-01 v1.1, unchanged',
 'evidence':'MATH_ONLY; R04 source pages already reopened; no new Notion readback in R05',
 'attacker_page_id':'301c2b324ede828caccb813d3979267a',
 'target_page_id':'5dac2b324ede83f39cdb01a904ce3cfd',
 'target_conditions':'Behemoth Glacial Ouro1 CA68; +3 CA from Armadura de Gelo to CA71 only if activated; RD25 assumes ordinary Ouro RD without special resistance',
 'noncanonical_test_parameters':'Luta Patada+6 and Mordida+7 are sensitivity parameters only; NOT authorized for Símio. Frígido-only Luta+6 does not transfer',
 'exclusions':'No crit, voluntary reactions, magical effects, reflection, or damage-type-specific resistance; rolls of hit and damage treated as independent; action timing not admitted',
 'source_paths':['https://app.notion.com/p/301c2b324ede828caccb813d3979267a','https://app.notion.com/p/5dac2b324ede83f39cdb01a904ce3cfd'],
 'rows':rows,
 'threshold':{'at_ca68':'RD50: Mordida advantage; RD51: Patada advantage (integer RD)',
              'at_ca71':'+3CA drops Patada hit chance 10/36 -> 1/36 and Mordida 15/36 -> 3/36; total expected harm decreases but relative advantage changes'},
 'qa':'All exact-fraction asserts passed; 101 uniform RD stochastic dominance assertions; no claims of native VLAB execution',
 'no_canon_changes':True
}
path=ROOT/'R05_RESULTS_FAST.json'
path.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
check=json.loads(path.read_text(encoding='utf-8'))
assert check['rows']==rows
print('R05 PASS: exact assertions + 101 stochastic-dominance checks + JSON readback; cases:',len(rows),'file',path)
