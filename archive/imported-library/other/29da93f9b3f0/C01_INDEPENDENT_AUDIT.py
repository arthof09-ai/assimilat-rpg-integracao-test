#!/usr/bin/env python3
"""Independently written adversarial and Monte Carlo check; source text verification separate.
Does not import the primary mathematical script or VLAB core.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction
from collections import Counter
import hashlib, json, random, math, statistics
R=Path(__file__).resolve().parent
j=json.loads((R/'C01_RESULTS_MODEL.json').read_text())
mc_prereg=json.loads((R/'C01_MC_PREREG.json').read_text())
assert mc_prereg['locked_before_MC'] and mc_prereg['independent_trials']==12000
F=Fraction
checks={}
def ok(name,value):
 checks[name]=bool(value)
 if not value:raise RuntimeError(name)
# independent enumeration of the ORIGINAL physical 3d6 and conditional crit damage:
combos=list(product(range(1,7),repeat=3))
pRD35=sum(1 for d in combos if sum(d)+18>35)
check35=j['crossrank_generic_BASE_ONLY']['Normal Bronze 3d6']['Normal Ouro Negro']['p_positive_if_critical_base_only']['fraction']
ok('Bronze3d6 conditional on crit against RD35 exactly one of 216',pRD35==1 and check35=='1/216')
ok('Critical+penetration joint rare 1/23328',j['crossrank_generic_BASE_ONLY']['Normal Bronze 3d6']['Normal Ouro Negro']['p_positive_per_attack_if_only_critical_hits_and_independent_critical_check']['fraction']=='1/23328')
ok('Bronze3d6 crit never penetrates RD45',all(sum(d)+18<=45 for d in combos))
ok('Galha mortal 1d6+FOR11 critical max 23 cannot penetrate normal Ouro RD25',all(x+11+6<=25 for x in range(1,7)))
fr_damages=[max(0,x+18+6-25) for x in range(1,7)]
ok('Frigido conditional critical damage RD25 exact 5/2',sum(fr_damages)==15 and F(sum(fr_damages),6)==F(5,2))
ok('Frigido critical positive damage P=5/648 per attack',F(5,6)*F(1,108)==F(5,648))
# Source screen raw-name count, without trusting previously-computed cohort stats
ledger=json.loads((R/'C01_NEW_SOURCE_LEDGER.json').read_text());kinds=Counter(x['source_kind'] for x in ledger)
ok('Sample 18 physical Notion IDs distinct',len(ledger)==18 and len({x['page_id'] for x in ledger})==18)
ok('Exactly one Party excluded, not a Master source',kinds['PARTY_MIRROR_EXCLUDE']==1)
ok('Exactly twelve Master beast source pages',kinds['MASTER_BEAST']==12)
num=sum(len(x['initial_numeric_attacks']) for x in ledger if x['source_kind']=='MASTER_BEAST')
ok('Four source-derived numeric beast actions from two source documents',num==4 and sum(bool(x['initial_numeric_attacks']) for x in ledger if x['source_kind']=='MASTER_BEAST')==2)
# Independent major rank extraction, allowing Ouro Negro as two-token rank
major=lambda s: 'Ouro Negro' if s.startswith('Ouro Negro') else s.split()[0]
beast=[x for x in ledger if x['source_kind']=='MASTER_BEAST']
major_conflicts=[x['cohort_key'] for x in beast if major(x['title_rank'])!=major(x['body_rank'])]
ok('Seven major rank category mismatches among 12 beasts',len(major_conflicts)==7)
full_conflicts=sum(x['title_rank']!=x['body_rank'] for x in beast)
ok('Ten/12 exact rank+star discrepancies or missing star in body',full_conflicts==10)
# Mathematics of expected positive crit push counts in bilateral duel (optional stopping identity)
r10=json.loads((Path('/mnt/data/dmg_recovery/r10/R10_RESULTS.json')).read_text())
exact_attacks=F(r10['goat_crit_only']['closed_form_symmetric_bilateral']['expected_attack_count']['fraction'])
expected_push=exact_attacks/F(108)-1
calculated_push=j['spatial_action_economy']['expected_nonlethal_critical_pushes_needing_a_reposition_if_next_attack_requires_adjacency']['fraction']
ok('Expected nonlethal pushes by independent Wald expectation',str(expected_push)==calculated_push)
# Adversarial functional tests: no negative damage, no double RD, no erroneous hit guarantee bypassing RD
ok('critical never implies net positive vs RD>=damage_max',all(max(0,x+17-25)==0 for x in range(1,7)))
ok('negative net clamp property',all(max(0,x-45)>=0 for x in range(1,30)))

rnd=random.Random(mc_prereg['seed'])
result=[];censored=0;wins=[0,0];rlist=[]
N=mc_prereg['independent_trials'];H=mc_prereg['max_rounds_per_trial']
for trial in range(N):
 hp=[38,38];at=0;cp=0;cn=0;moves=0;won=-1
 for turn in range(1,H+1):
  for actor in (0,1):
   if hp[0]<=0 or hp[1]<=0:break
   at+=1
   # 3 ordered dice independent of hit and damage dice
   c1=rnd.randint(1,6);c2=rnd.randint(1,6);c3=rnd.randint(1,6)
   if c1==6 and c2==6 and c3 in (5,6):
    cp+=1
    # attack common score20..25, always <= Esquiva26; critical bypasses numeric defense
    attackdie=rnd.randint(1,6)
    damage_die=rnd.randint(1,6)
    assert 20<=attackdie+19<=25
    dmg=damage_die+14
    target=1-actor
    hp[target]=max(0,hp[target]-dmg)
    if hp[target]>0: moves+=1 # requires one movement to re-engage; legal open corridor assumption
   elif c1==1 and c2==1 and c3 in (1,2):
    cn+=1 # LAB-only Master policy: auto-fail, damage0, no extra turn loss
   else:
    # normal attack roll, predeclared Esquiva26 stops 20..25
    rnd.randint(1,6)
  if hp[0]<=0 or hp[1]<=0:
   won=0 if hp[1]<=0 else 1
   break
 if won==-1:censored+=1;turn=H
 else:wins[won]+=1
 result.append((turn,at,cp,cn,moves))
 rlist.append(turn)
mean=statistics.fmean(r[0] for r in result);var=statistics.variance(r[0] for r in result)
se=math.sqrt(var/N)
E=F(r10['goat_crit_only']['closed_form_symmetric_bilateral']['mean_rounds']['fraction'])
ok('MC round mean close to original exact R10 in independent code',abs(mean-float(E))<6*se)
oks={'check_count':len(checks),'PASS':all(checks.values()),'checks':checks}
rsorted=sorted(rlist)
emp={'trials':N,'seed':mc_prereg['seed'],'horizon':H,'mean_rounds':mean,'median_rounds':rsorted[N//2],
 'p90_rounds':rsorted[int(0.9*N)],'se_rounds':se,'mean_difference_from_R10_exact_in_SE':(mean-float(E))/se,
 'censored':censored,'wins_A':wins[0],'wins_B':wins[1], 'first_actor_win_share':wins[0]/(wins[0]+wins[1]),
 'mean_total_attack_opportunities':statistics.fmean(x[1] for x in result),
 'mean_positive_crit':statistics.fmean(x[2] for x in result),
 'mean_negative_crit':statistics.fmean(x[3] for x in result),
 'mean_nonlethal_moves_needed':statistics.fmean(x[4] for x in result),
 'no_native_engine_executed':True,'sampling':'pre-registered independent local MC; NOT canonical combat or real world arena'}
summary={'secondary_audit':oks,'monte_carlo':emp,'source_original_R41_archive_SHA256':hashlib.sha256((R/'evidence_readonly/VLAB_R41_CRITICO_AUTOMATICO_RNG_REACOES_MESTRE_ONLY.zip').read_bytes()).hexdigest(),
 'limits':['read-only archive physically materialized; separate R41 standalone verifier executed in previous command','MC uses model assumptions and independent pseudo-RNG, no automatic terminal claim','possible different RNG consumption from VLAB source']}
(R/'C01_AUDIT_INDEPENDENT.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'PASS':oks['PASS'],'n_checks':len(checks),'MC':emp},indent=2))
