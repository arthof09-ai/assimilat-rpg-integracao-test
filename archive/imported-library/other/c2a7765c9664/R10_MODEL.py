#!/usr/bin/env python3
"""DMG R10 — MESTRE-SIDE science only, no VLAB native combat, no Notion writes.
Source-aware independent mathematical engine; preserves R01-R09 files read-only.
Prerecord R10_PREREG.json frozen before computations. Explicit simplifying assumptions
in prereg and output. Do not equate these state models with official battles.
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction as Q
from math import comb, sqrt
from pathlib import Path
import json, hashlib
import numpy as np

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent
PREREG=json.loads((ROOT/'R10_PREREG.json').read_text())
CHECKS=[]
def check(condition, reason):
    if not condition: raise AssertionError(reason)
    CHECKS.append(reason)
def fv(q):return {'fraction':str(q), 'decimal':float(q)}
def crit_seq(d1,d2,d3,margin=0):
    if not all(isinstance(d,int) and 1<=d<=6 for d in (d1,d2,d3)):
        raise ValueError('impossible d6')
    if not (0<=margin<=4): raise ValueError('critical margin out of bounds')
    return d1==6 and d2==6 and d3 >= 5-margin

def resolve(source, base_roll, critical_roll, damage_roll, defense, rd, reaction_predeclared, *, margin=0):
    if base_roll not in range(1,7) or damage_roll not in range(1,7):
        raise ValueError('d6 domain')
    if source not in ('goat_investida','frigido_rabada'):raise ValueError('attack source')
    positive=crit_seq(*critical_roll,margin)
    strength=13 if source=='goat_investida' else 18
    attack=base_roll+strength+6
    if reaction_predeclared not in (True,False): raise ValueError('predeclare boolean')
    defense_numeric=defense if reaction_predeclared else defense
    hit= positive or attack>defense_numeric
    bruto=damage_roll+strength+(6 if positive else 0) if hit else 0
    net=max(0,bruto-rd) if hit else 0
    return {'attack':attack,'crit':positive,'hit':hit,'damage_dice':damage_roll,
            'gross':bruto,'net':net,'defense':defense_numeric}

# Precommitted adversarial tests. These are fixture-input calculations, NOT VLAB engine.
a=resolve('goat_investida',6,(4,4,4),6,20,5,False)
b=resolve('goat_investida',1,(4,4,4),6,20,5,False)
c=resolve('goat_investida',1,(6,6,5),3,20,5,False)
d=resolve('goat_investida',1,(6,6,6),3,26,5,True)
e=resolve('goat_investida',1,(6,5,6),3,26,5,True)
f=resolve('goat_investida',1,(6,6,4),3,26,5,True,margin=1)
g=resolve('goat_investida',1,(6,6,5),6,26,100,True)
h=resolve('goat_investida',1,(6,6,5),6,26,5,True)
for key,cond in {
'A_score_normal_hit':a['hit'] and not a['crit'] and a['net']==14,
'B_score_normal_miss':not b['hit'] and b['net']==0,
'C_crit_auto_over_CA':c['hit'] and c['attack']==20 and c['net']==17,
'D_crit_auto_over_evasion':d['hit'] and d['attack']==20 and d['defense']==26,
'E_wrong_order_6_5_6_rejected':not e['crit'] and not e['hit'],
'F_margin_plus_one_valid_6_6_4':f['crit'] and f['hit'],
'G_RD_not_ignored':g['crit'] and g['hit'] and g['net']==0,
'H_damage_correct':h['gross']==25 and h['net']==20,
}.items():check(cond,key)
check(sum(crit_seq(i,j,k,0) for i in range(1,7) for j in range(1,7) for k in range(1,7))==2,'seq_positive_2_of_216')
check(sum(crit_seq(i,j,k,4) for i in range(1,7) for j in range(1,7) for k in range(1,7))==6,'margin_limit_6_of_216')
for bad in ((6,6,7), (0,6,6)):
    try:crit_seq(*bad);check(False,'bad_d6_rejection')
    except ValueError:CHECKS.append('reject_bad_d6_'+str(bad))
for bad_margin in (-1,5):
    try:crit_seq(6,6,5,bad_margin);check(False,'bad_margin_rejection')
    except ValueError:CHECKS.append('reject_bad_margin_'+str(bad_margin))
# Mutant-first numeric gate would incorrectly discard the newly authoritative crit.
mutant_hit=(d['attack']>26) and d['crit']
check(not mutant_hit and d['hit'],'synthetic_mutant_numeric_first_detected')

# Critical check probability, 1d6 hit score independently rolled from ordered 3d6 check.
def attack_pmf(*,force=13, vs_ca=20, evade=False, margin=0,rd=5):
    q=Q(margin+2,216)
    p_normal=Q(sum(i+force+6 > vs_ca for i in range(1,7)),6)
    normal_w=Q(0) if evade else p_normal*(1-q)
    result=defaultdict(Q)
    result[0]+=1-q-normal_w
    for d in range(1,7):
        result[max(0,d+force-rd)]+=normal_w/6
        result[max(0,d+force+6-rd)]+=q/6
    check(sum(result.values())==1,'PMF sums to 1')
    return dict(sorted((d,p) for d,p in result.items() if p))

def build_transition(hp, pmf):
    M=np.zeros((hp+1,hp+1),dtype=float)
    M[0,0]=1
    for h in range(1,hp+1):
        for dmg,pr in pmf.items():M[h,max(0,h-dmg)]+=float(pr)
    check(np.max(abs(M.sum(axis=1)-1))<2e-15,'transition mass normalized')
    return M

def isolated_survival(hp,pmf,H=2200,first_pmf=None):
    T=build_transition(hp,pmf)
    vec=np.zeros(hp+1);vec[hp]=1
    alive=np.empty(H+1,dtype=float);alive[0]=1
    for n in range(1,H+1):
        if n==1 and first_pmf is not None:
            vec=vec @ build_transition(hp,first_pmf)
        else:vec=vec@T
        alive[n]=sum(vec[1:])
    check(np.all(np.diff(alive)<2e-12),'survival nonincreasing')
    return alive

def bilateral(SA,SB):
    # A acts first each round; if B is dead after A's attack, B never acts that round.
    end=1-SA*SB
    p=SA[:-1]-SA[1:]
    g=SB[:-1]-SB[1:]
    pa=np.sum(p*SB[:-1])
    pb=np.sum(g*SA[1:])
    E=np.sum(SA[:-1]*SB[:-1])
    quantiles={str(x):int(np.searchsorted(end,x,side='left')) for x in (.1,.25,.5,.75,.9,.95,.99,.999)}
    check(abs(pa+pb-1)<2e-8,'bilateral terminal mass')
    return {'mean_rounds':float(E),'p_first_actor_wins':float(pa),'p_second_actor_wins':float(pb),
        'expected_total_attack_opportunities':float(2*E-pa),
        'quantile_rounds':quantiles,'survival_horizon':{str(n):float(SA[n]*SB[n]) for n in PREREG['fixed_horizons_rounds']},
        'tail_survival_at_H':float(SA[-1]*SB[-1])}

def exact_sums(q=Q(1,108)):
    # In crit-only fight a fighter is killed after 2 crits with probability 1/6,
    # otherwise after 3. All critical damage uniform 15..20 and independent.
    r=1-q;x=r*r
    a=q/r;b=Q(5,12)*(q/r)**2
    c0=Q(1);c1=a-b;c2=b
    S0=1/(1-x);S1=x/(1-x)**2;S2=x*(1+x)/(1-x)**3
    S3=x*(1+4*x+x*x)/(1-x)**4
    S4=x*(1+11*x+11*x*x+x**3)/(1-x)**5
    mean=c0*c0*S0+2*c0*c1*S1+(c1*c1+2*c0*c2)*S2+2*c1*c2*S3+c2*c2*S4
    # probability two identically independent knockout times tie, favor A.
    A=q*q/(6*r);B=Q(5,12)*q**3/(r*r)
    ptie=(A-B)**2*S2+2*(A-B)*B*S3+B*B*S4
    return {'mean_rounds':mean,'p_first':(1+ptie)/2,'p_equal_isolated_KO_time':ptie,
            'expected_attack_count':2*mean-(1+ptie)/2}

# Compute exact source-authorized PMFs and expectations; crit independence is model assumption.
q=Q(1,108)
crit_goat=attack_pmf(evade=True)
normal_goat=attack_pmf(evade=False)
frig_attack_noevade=attack_pmf(force=18,vs_ca=20,evade=False)
frig_attack_goat_evasion=attack_pmf(force=18,vs_ca=26,evade=False)
goat_attack_frig_ca31=attack_pmf(force=13,vs_ca=31,evade=False)
check(crit_goat == {0:Q(107,108), **{d:Q(1,648) for d in range(15,21)}},'crit-only exact PMF')
check(min(k for k in crit_goat if k>0)==15 and max(crit_goat)==20,'crit damage mitigated range 15 to 20')
check(sum(a+b>=38 for a in range(15,21) for b in range(15,21))==6,'2-critical lethal outcomes 6 of 36')
check(sum(a+b+c>=38 for a in range(15,21) for b in range(15,21) for c in range(15,21))==216,'3 critical hits guaranteed to KO')
check(q*Q(35,2)==Q(35,216),'crit-only damage expected per attack')

H=2400
s_crit=isolated_survival(38,crit_goat,H)
s_decline=isolated_survival(38,normal_goat,H)
s_first=isolated_survival(38,normal_goat,H,first_pmf=crit_goat)
exact=exact_sums(q)
primary=bilateral(s_crit,s_crit)
check(abs(primary['mean_rounds']-float(exact['mean_rounds']))<1e-9,'independent exact closed-form mean versus Markov')
check(abs(primary['p_first_actor_wins']-float(exact['p_first']))<1e-11,'independent exact closed-form first win versus Markov')
base=bilateral(s_decline,s_decline)
first=bilateral(s_first,s_first)
fr_no=bilateral(isolated_survival(38,frig_attack_noevade,H),isolated_survival(125,goat_attack_frig_ca31,H))
fr_ev=bilateral(isolated_survival(38,frig_attack_goat_evasion,H),isolated_survival(125,goat_attack_frig_ca31,H))

margins={}
for margin in PREREG['fixed_margin_sensitivity']:
    crit_only=attack_pmf(evade=True,margin=margin)
    ss=isolated_survival(38,crit_only,H)
    bd=bilateral(ss,ss)
    margins[str(margin)]={'q_crit':fv(Q(margin+2,216)), 'mean_rounds':bd['mean_rounds'],
             'median_rounds':bd['quantile_rounds']['0.5'],
             'p_first_actor_wins':bd['p_first_actor_wins'],
             'survive_after_8_rounds':bd['survival_horizon']['8']}
check(all(margins[str(m)]['mean_rounds']>margins[str(m+1)]['mean_rounds'] for m in range(4)),'increased crit margin shortens symmetric duel')

# Additional source-real one-sided contrast Cabra Investida against Galidemus B1 CA21 (Galidemus Patada Luta missing):
goat_vs_gal=attack_pmf(force=13,vs_ca=21,evade=False,rd=5)
gal_survive=isolated_survival(32,goat_vs_gal,H)
gal_E=float(np.sum(gal_survive[:-1])); goat_vs_gal_expected=sum(Q(d)*p for d,p in goat_vs_gal.items())
check(Q(sum(x+13+6>21 for x in range(1,7)),6)==Q(2,3),'source 4/6 common hit vs Galidemus CA21')
check(gal_survive[-1]<1e-12,'source Galidemus one-sided finite expected tries')

# Adversarial source-damage mutators; hard failure where source domains violated.
class ModelEventGuard:
    def __init__(self): self.slot=1;self.commands=set();self.hp=38;self.alive=True
    def apply(self, *, cmd,actor_alive=True,attack_die,damage_die,crit_roll=(2,3,4),defense_declared=False, predeclared=True):
        if cmd in self.commands:raise ValueError('duplicate event command id')
        if not actor_alive or not self.alive:raise ValueError('KO cannot act')
        if not predeclared and defense_declared:raise ValueError('retroactive reaction')
        if defense_declared and self.slot<1:raise ValueError('extra reaction without refresh')
        self.commands.add(cmd)
        if defense_declared:self.slot-=1
        result=resolve('goat_investida',attack_die,crit_roll,damage_die,26 if defense_declared else 20,5,defense_declared)
        self.hp=max(0,self.hp-result['net'])
        if self.hp==0:self.alive=False
        return result
    def refresh(self):self.slot=1

def rejected(fn):
    try:fn()
    except ValueError:return True
    return False
for label, func in {
    'reject_impossible_attack_die_7':lambda:ModelEventGuard().apply(cmd='A',attack_die=7,damage_die=3),
    'reject_impossible_damage_die_7':lambda:ModelEventGuard().apply(cmd='A',attack_die=4,damage_die=7),
    'reject_retroactive_evasion':lambda:ModelEventGuard().apply(cmd='A',attack_die=4,damage_die=3,defense_declared=True,predeclared=False),
}.items():check(rejected(func),label)
guard=ModelEventGuard(); guard.apply(cmd='A',attack_die=4,damage_die=3,defense_declared=True)
check(rejected(lambda:guard.apply(cmd='B',attack_die=4,damage_die=3,defense_declared=True)),'reject_second_reaction_before_refresh')
check(rejected(lambda:guard.apply(cmd='A',attack_die=4,damage_die=3)),'reject_duplicate_command')
check(rejected(lambda:ModelEventGuard().apply(cmd='K',actor_alive=False,attack_die=4,damage_die=3)),'reject_KO_attacker')
check(guard.slot==0 and guard.hp==38,'defense spent and no damage')

# One independent holdout sampled from actual ordered sequential d6 with designated seed;
# entirely different from VLAB R40 and no post-hoc seed selection.
rng=np.random.default_rng(PREREG['independent_seed_MC']+1)
rolls=rng.integers(1,7,size=(108000,3))
positive=np.count_nonzero((rolls[:,0]==6)&(rolls[:,1]==6)&(rolls[:,2]>=5))
negative=np.count_nonzero((rolls[:,0]==1)&(rolls[:,1]==1)&(rolls[:,2]<=2))
observed_diff=abs(positive/108000-1/108)
check(observed_diff<.001,'positive critical empirical frequency not far from theoretical in independent PCG64 holdout')

# Independent MC simulation uses ordered triples, independent attack d6 and damage d6.
def mc_bilateral(name,n,seed,horizon=1800,forceA=13,forceB=13,caA=20,caB=20,
                 hpA=38,hpB=38,rdA=5,rdB=5,evadeA='always',evadeB='always',margin=0):
    # defensive policies describe which incoming attacks each defender evades
    ra=np.random.default_rng(seed+1001)
    rb=np.random.default_rng(seed+2002)
    hp_a=np.full(n,hpA,np.int32);hp_b=np.full(n,hpB,np.int32)
    wins=np.zeros(n,dtype=np.int8);rounds=np.zeros(n,dtype=np.int32)
    for step in range(1,horizon+1):
        active=wins==0
        if not np.any(active):break
        for side,rng1 in ((1,ra),(2,rb)):
            active=wins==0
            if not np.any(active):break
            order=rng1.integers(1,7,size=(n,3))
            attackdie=rng1.integers(1,7,size=n)
            damage_die=rng1.integers(1,7,size=n)
            positive=(order[:,0]==6)&(order[:,1]==6)&(order[:,2]>=5-margin)
            if side==1:
                defender_evasion= (evadeB=='always') or (evadeB=='first' and step==1)
                defense = caB+6 if defender_evasion else caB
                att=forceA+6+attackdie
                hit=active&(positive|(att>defense))
                damage=np.maximum(0,damage_die+forceA+(6*positive)-rdB)
                hp_b-=hit*damage
                justdied=active&(hp_b<=0)
                wins[justdied]=1;rounds[justdied]=step
            else:
                defender_evasion= (evadeA=='always') or (evadeA=='first' and step==1)
                defense = caA+6 if defender_evasion else caA
                att=forceB+6+attackdie
                hit=active&(positive|(att>defense))
                damage=np.maximum(0,damage_die+forceB+(6*positive)-rdA)
                hp_a-=hit*damage
                justdied=active&(hp_a<=0)
                wins[justdied]=2;rounds[justdied]=step
    censored=int(np.count_nonzero(wins==0))
    if censored:rounds[wins==0]=horizon
    successes=wins!=0
    quant={str(t):float(np.quantile(rounds[successes],t)) for t in (.1,.5,.9,.99)}
    return {'case':name,'n':n,'seed':seed,'horizon_rounds':horizon,'censored':censored,
     'mean_rounds_observed_uncensored':float(np.mean(rounds[successes])) if np.any(successes) else None,
     'median_rounds_observed_uncensored':quant['0.5'],
     'p_A_win_unconditional':float(np.count_nonzero(wins==1)/n),
     'p_B_win_unconditional':float(np.count_nonzero(wins==2)/n),
     'round_quantiles_observed_uncensored':quant,
     'sampled_branch':'per-attack ordered 3d6 + separately sampled ordinary and damage d6, no native combat'}

MC={}
MC['goat_symmetric_always_evasion']=mc_bilateral('GvG_EVADE_ALWAYS',PREREG['MC_n_primary'],PREREG['independent_seed_MC'])
MC['goat_symmetric_decline']=mc_bilateral('GvG_DECLINE',PREREG['MC_n_comparators'],PREREG['independent_seed_MC']+301,evadeA='decline',evadeB='decline')
MC['goat_symmetric_first_once']=mc_bilateral('GvG_FIRST_ONCE',PREREG['MC_n_comparators'],PREREG['independent_seed_MC']+501,evadeA='first',evadeB='first')
MC['goat_symmetric_margin1_conditional']=mc_bilateral('GvG_EVADE_MARGIN1_CONTRAFACTUAL',PREREG['MC_n_comparators'],PREREG['independent_seed_MC']+701,margin=1)
for key,v in [('goat_symmetric_always_evasion',primary),('goat_symmetric_decline',base),('goat_symmetric_first_once',first)]:
    check(MC[key]['censored']==0, 'MC sample uncensored within 1800 rounds '+key)
    check(abs(MC[key]['mean_rounds_observed_uncensored']-v['mean_rounds'])<max(.4,.04*v['mean_rounds']),
        'Monte Carlo sanity mean '+key)
    check(abs(MC[key]['p_A_win_unconditional']-v['p_first_actor_wins'])<.025,'Monte Carlo sanity winner '+key)

# Structural replay integrity and baseline immutability
historical=['r04/R09_REPLAY_EXACT.py','r04/R09_RESULTS_EXACT.json','r04/R09_VLAB_HANDOFF_READONLY.json',
 'r04/R08_RESULTS_MECHANICAL.json','r04/R07_RESULTS_EXACT.json','r04/DMG_R04_MECHANICAL_ROBUSTNESS_MASTER_ONLY.zip',
 'r03/DMG_R03_INDEPENDENT_COHORT_CROSSRANK_MASTER_ONLY.zip',
 'DMG_R02_RECONSTRUCAO_CIENTIFICA_MESTRE_SIDE.zip']
parents=ROOT.parent
originals={file:hashlib.sha256((parents/file).read_bytes()).hexdigest() for file in historical}

RESULTS={
 'research':'DMG R10','operation':'OP-DMG-CORPUS-EMP-01','baseline':'DMG-RANK-01 v1.1','canonical_writes':0,'new_VLAB_combats':0,
 'method':'independent exact closed-form Q + absorbing health-state Markov + registered random PCG64 Monte Carlo',
 'master_binding_change':'positive critical automatically hits even if ordinary score <= CA or Esquiva; critical damage and RD remain',
 'prereg_sha256':hashlib.sha256((ROOT/'R10_PREREG.json').read_bytes()).hexdigest(),
 'sources':{'cabramestre':'391c2b324ede8252b0cc810423cdbfa6','frigido':'f0dc2b324ede820ab9470168d4a53315','galidemus':'eddc2b324ede829f8a75011e8acbf429',
  'vLab':'3f3c2b324ede819496ddd7f93bd7e5d2','combat':'3ebc2b324ede81f1be4be8804ac113c0',
  'beast':'3ebc2b324ede81f4992ac88a3588cacd'},
 'goat_crit_only':{
  'p_crit':fv(q),'p_noncrit_hit_evasion26':fv(Q(0)),'damage_crit_net_range':[15,20],
  'damage_crit_net_pmf':{str(i):'1/6' for i in range(15,21)},
  'p_two_crit_KO':fv(Q(1,6)),'p_three_crit_required':fv(Q(5,6)),
  'E_crit_hits_for_KO':fv(Q(17,6)),'E_attacks_one_attacker_HP38':fv(Q(306)),
  'E_time_until_first_crit_opportunities':fv(Q(108)),
  'p_at_least_one_crit_after_n_independent_checks':{str(n):float(1-(Q(1)-q)**n) for n in [8,16,50,100,200,500,1000]},
  'closed_form_symmetric_bilateral':{k:fv(v) for k,v in exact.items()},'health_state_matrix_bilateral':primary},
 'goat_defense_policies':{'DECLINE':base,'EVADE_FIRST_ONCE':first,'EVADE_WHEN_AVAILABLE':primary},
 'margins_counterfactual':margins,
 'other_source_real_contrasts':{
  'FRIGIDO_ATTACK_FIRST_GOAT_DECLINE':fr_no,
  'FRIGIDO_ATTACK_FIRST_GOAT_EVADE_WHEN_AVAILABLE':fr_ev,
  'GALIDEMUS_B1_AS_TARGET_ONE_SIDED':{'target_HP':32,'target_CA':21,'target_RD':5,'goat_attack_luta6':'1d6+13+6','common_hit_p':'4/6',
        'expected_net_per_attack_inc_auto_crit':fv(goat_vs_gal_expected),'expected_attacks_to_KO_HP32':gal_E,
        'target_counterattack_Luta':'UNRESOLVED; not a full fight'}
 },
 'sampling':{'PCG64_ordered_3d6_holdout':{'seed':PREREG['independent_seed_MC']+1,'n':len(rolls),
                     'critical_positive_count':int(positive),'critical_negative_count':int(negative),
                     'p_positive':float(positive/len(rolls))},'MC_BILATERAL':MC},
 'R40_from_notion_document_only':{
  'fully_completes_new_lab_fights':2,'total_lab_fights':18,'native_attacks':42,'observed_positive_crit_in_fights':0,
  'reaction_valid':15,'refused_reactions':9,'KO_native':4,'terminal_17':0,
  'source_document_SHA256_claim':'2be2d7b8cb39fd4aa340afc07a200c8c1c5234475256635e2dad85a2aeeb1e71',
  'physical_zip_audit_by_DMG':'NOT DONE. Notion source opened; no original ZIP bytes materialized.'},
 'original_immutable_sha256':originals,
 'QA_local_pass_count':len(CHECKS),'QA_local_assertions':CHECKS,
 'scientific_caveats':['critical verification and ordinary score treated as independent in R10 mathematical model',
  'critical negative has no invented fumble effects',
  'infinite duration only for miss-only R09 model, now refuted by positive auto-critical',
  'geometry and forced push simplified as movement can restore adjacency in open space; blocked map can change results',
  'regular combat critical auto-hit override is the new Mestre decision, not physically edited in Notion',
  'initiative ORDER condition A first, not fixed initiative bonuses for any new scene',
  'increased crit margins are counterfactual not assigned to official Goat',
  'results are analytics on independent models, not native VLAB engine nor canon outcomes']
}
output=ROOT/'R10_RESULTS.json'
output.write_text(json.dumps(RESULTS,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
loaded=json.loads(output.read_text())
check(loaded['goat_crit_only']['closed_form_symmetric_bilateral']['mean_rounds']['fraction']==str(exact['mean_rounds']), 'output readback exact rational')
check(all(hashlib.sha256((parents/f).read_bytes()).hexdigest()==originals[f] for f in historical),'immutability of eight existing R02-R09 artifacts')
RESULTS['QA_local_pass_count']=len(CHECKS);RESULTS['QA_local_assertions']=CHECKS
output.write_text(json.dumps(RESULTS,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
print(json.dumps({'QA_pass':len(CHECKS), 'primary_exact_E_rounds':float(exact['mean_rounds']),
                 'primary_E_rounds_matrix':primary['mean_rounds'], 'p_first':primary['p_first_actor_wins'],
                 'quantiles':primary['quantile_rounds'], 'survival_horizons':primary['survival_horizon'],
                 'decline':{'Erounds':base['mean_rounds'],'pFirst':base['p_first_actor_wins']},
                 'first_once':first['mean_rounds'], 'Frig_without_evasion':fr_no['mean_rounds'],
                 'Frig_with_evasion':fr_ev['mean_rounds'], 'Galidemus_Eattacks':gal_E,
                 'MC':MC,'out_sha256':hashlib.sha256(output.read_bytes()).hexdigest()},ensure_ascii=False,indent=2))
