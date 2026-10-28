#!/usr/bin/env python3
"""OP-DMG-CORPUS-EMP-01 POST-R10 C07..C11, Mestre-side, READ ONLY.

This is a bounded mathematical oracle, NOT a native VLAB execution.
Negative critical auto-miss is LAB-only R42 policy; positive auto-hit is Mestre.
Ordinary and sequential critical check rolls assumed independent, as prior R10 oracle.
One normal equipped attack per opportunity; no movement, extra action, magic or
special ability unless the row explicitly documents a sensitivity case.
"""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
from itertools import product
from math import prod
import hashlib,json

ROOT=Path(__file__).resolve().parent
P_PLUS=Q(1,108)
P_MINUS=Q(1,108)
P_PLAIN=Q(106,108)
SOURCES={
 "Veado": "8acc2b324ede827b9bc801746ae97409",
 "Regalis": "5fac2b324ede8381a25581194ebf9bd7",
 "Regalis_parent": "bd4c2b324ede8381929e815d7159fe4d",
 "VLAB":"3f3c2b324ede819496ddd7f93bd7e5d2",
 "Combat":"3ebc2b324ede81f1be4be8804ac113c0",
 "Magic":"3ebc2b324ede81f7b343f7270ff91373",
 "Feryn":"3f6c2b324ede81ce9c61db8127bf0e31",
 "Varok":"3f6c2b324ede81f49ea9efbe1a811091",
 "Arveth":"3f6c2b324ede8105891fc647242e61ca",
 "Goat":"391c2b324ede8252b0cc810423cdbfa6"
}
ACTORS={
 'Feryn':dict(rank='Ouro Negro 5',hp=479,ca=123,evade=125,rd=22,attack_fixed=92,attack_dice=(4,6),dmg_dice=(8,8),dmg_fixed=47,pa_free=424),
 'Varok':dict(rank='Ouro Negro 5',hp=734,ca=83,evade=83,rd=35,attack_fixed=100,attack_dice=(4,6),dmg_dice=(10,10),dmg_fixed=48,pa_free=324),
 'Arveth':dict(rank='Ouro Negro 5',hp=806,ca=93,evade=95,rd=30,attack_fixed=72,attack_dice=(4,6),dmg_dice=(8,10),dmg_fixed=35,pa_free=344),
}

def dice_dist(n,sides):
    a=Counter({0:1})
    for _ in range(n):
        b=Counter()
        for v,c in a.items():
            for die in range(1,sides+1):b[v+die]+=c
        a=b
    assert sum(a.values())==sides**n
    return {v:Q(count,sides**n) for v,count in a.items()}

def mean(d):return sum((Q(v)*p for v,p in d.items()),Q())
def prob(d, fn):return sum((p for v,p in d.items() if fn(v)),Q())
def effective_distribution(n,faces,fixed,rd,crit=False):
    bonus=n*faces if crit else 0
    c=Counter()
    for v,p in dice_dist(n,faces).items(): c[max(0,v+fixed+bonus-rd)]+=p
    assert sum(c.values())==1
    return dict(c)

def qstr(x):return str(x)
def qdata(x):return {'fraction':str(x),'decimal':round(float(x),12)}
def win_pair(attacker,defender,use_evasion=False):
    a=ACTORS[attacker];b=ACTORS[defender]
    dist=dice_dist(*a['attack_dice'])
    defense=b['evade'] if use_evasion else b['ca']
    p_basic=prob(dist,lambda score:score+a['attack_fixed']>defense)
    ordinary=effective_distribution(*a['dmg_dice'],a['dmg_fixed'],b['rd'])
    critical=effective_distribution(*a['dmg_dice'],a['dmg_fixed'],b['rd'],crit=True)
    p_common=P_PLAIN*p_basic
    hit=P_PLUS+p_common
    p_injure=P_PLUS*prob(critical,lambda x:x>0)+p_common*prob(ordinary,lambda x:x>0)
    edam=P_PLUS*mean(critical)+p_common*mean(ordinary)
    assert 0<=p_injure<=hit<=1
    return dict(attacker=attacker,defender=defender,attack='4d6+'+str(a['attack_fixed']),
       defense_kind='Esquiva' if use_evasion else 'CA',defense=defense,
       hit_basic_conditional_noncrit=qdata(p_basic),
       critical_positive=qdata(P_PLUS),critical_negative_LAB=qdata(P_MINUS),
       effective_normal_hits_per_attempt=qdata(p_common),total_hit_per_attempt=qdata(hit),
       p_positive_life_damage=qdata(p_injure),
       E_damage_given_normal_hit=qdata(mean(ordinary)),
       E_damage_given_critical=qdata(mean(critical)),
       E_damage_per_attack=qdata(edam),
       p_normal_damage_positive_given_hit=qdata(prob(ordinary,lambda x:x>0)),
       p_critical_damage_positive_given_hit=qdata(prob(critical,lambda x:x>0)),
       model='LAB_R42_NEGATIVE_FAIL_AND_MESTRE_POSITIVE_AUTOMATIC;no_reactions_except_stated')

# C07 source attributes read physically during this turn; no adjudication.
c07={
 'checkpoint':'POST-R10-C07',
 'source_verified':{
   'Veado':dict(source=SOURCES['Veado'],species_parent='Veado das Montanhas',page_title='Bronze 4',body_rank='Bronze 2 (1d6)',ca=49,force=11,agility=38,constitution=3,ability='Galha mortal: 1d6+forca',normal_raw_range=[12,17],normal_raw_mean=qdata(Q(29,2)),luta='MISSING_NOT_ZERO',attack_mechanic='NOT_ESTABLISHED'),
   'Regalis':dict(source=SOURCES['Regalis'],species_parent=SOURCES['Regalis_parent'],page_title='Ouro 2',body_class='Ouro 2',body_name='EMPTY',ability_copy_text='Aurora Radiante',int=72,ca=78,luta='MISSING_NOT_ZERO',attack_mechanic='NOT_ESTABLISHED',magic_identity='PENDING'),
 },
 'regalis_actions':[
  dict(name='Raio eletrizante',literal='2d4+INT72',raw_min=74,raw_max=80,raw_E=qdata(Q(77)),status_trigger='1d4=1 permits Fortitude check; NOT automatic paralysis',p_fortitude_test_gate=qdata(Q(1,4))),
  dict(name='Raio purificador',literal='2d4+INT72',raw_min=74,raw_max=80,raw_E=qdata(Q(77))),
  dict(name='Toque macabro',literal='1d4+INT72',raw_min=73,raw_max=76,raw_E=qdata(Q(149,2)))
 ],
 'rules_if_magic':dict(combat_magic_no_universal_accuracy=True,magic_no_critical_except_specific_exception=True,conjuration_base_one_standard_action_if_treated_as_magic=True,ability_tag_not_certified=True),
 'blocking_decisions':{
  'Veado':['resolve Bronze4 page versus Bronze2 body','legal Luta for Galha or competent distinct attack mechanic','damage subtype/action/range'],
  'Regalis':['confirm body identity vs Aurora Radiante copied text','classify each ability as magic or another action','legal acquisition and resolution of hit/salvaguarda/target','PA cost/range/cooldown if required; no value zero inferred']
 },'admission':'BLOCKED_NORMATIVE_FOR_FULL_NATIVE; DICE_ONLY_NORMALIZATION_ALLOWED',
 'dedup_note':'Species parent names are indexing evidence, not proof of every copied ability.'}

# C08 physically reverified package via external independent audit; evidence values from
# rechecked 39 SHA256+CRC+6 sqlite+15 events at local audit, not our simulations.
c08={
 'checkpoint':'POST-R10-C08',
 'archive':'VLAB_R47_R48_R49_CRITICO_CONTRA_ANINHAMENTO_ON5_MESTRE_ONLY.zip',
 'documentary_sha256':'fada8b0a413edfcdccc54af60c258c0bd25274848a9c10ff4df37d11cf0ed7d2',
 'archive_crc':'PASS','archive_manifest_internal_sha256':'39/39 PASS',
 'cold_auditor':'extension/verify_r47_r49_independent.py',
 'scenes':6,'events':15,'checkpoints':6,'attacks_aoo_real_source':6,
 'results':{'R47':['positive critical auto-hit, damage 0 after Feryn RD22','Counter response blocked pending precedence'],
            'R47B':['positive critical auto-hit, raw23, Feryn RD22, net1, Feryn479->478','response still blocked'],
            'R48':['first Counter normal Vantagem was tested','nested Counter not authorized without precedence'],
            'R49':['two same ON5 Feryn actors DES80 use 4d6 tie priority','three windows, six armed AoO attacks, net damage by window 83/104/100']},
 'normative_pending':['predeclared Counter on automatic critical with score below CA','nested Counter trigger/own-turn reaction rule'],
 'do_not_repeat_native_R47_R49':True,'new_dmg_native_events':0}

# C09: all six directed matchups same ON5 with LAB R42 negative critical and Mestre critical auto-hit.
c09={
 'checkpoint':'POST-R10-C09', 'actors':ACTORS,
 'model_authorities':['Mestre R41 positive critical auto-hit','VLAB LAB-only R42 negative critical auto-miss','individual ON5 equipment and Luta, no Party source'],
 'pairwise_normal_CA':[win_pair(x,y) for x in ACTORS for y in ACTORS if x!=y],
 'pairwise_evasion':[win_pair(x,y,True) for x in ACTORS for y in ACTORS if x!=y],
 'known_init_order':{'Feryn_before_Varok':'PROVED_BY_SUPPORT 4d6+82 min86 > 4d6+29 max53',
                     'Varok_before_Arveth':'NOT_DETERMINISTIC: 4d6+29 vs 4d6+25 overlap',
                     'Feryn_before_Arveth':'PROVED_BY_SUPPORT 4d6+82 min86 > 4d6+25 max49'},
 'limitations':['attack opportunity model, not multi-turn fight','equipment states are prepared Mestre-only proposed encounters','cannot generalize ON5 species population','no special activation, range/position/adversarial reactions not modelled']}

# C10: R49 AoO exchange between two source-identical Feryn; independent conditional
# no actor dies even if both were crit positive (provided no secondary activation).
f=ACTORS['Feryn'];v=ACTORS['Varok']
min_net_each=max(0,f['dmg_dice'][0]+f['dmg_fixed']-v['rd'])
max_net_each=max(0,f['dmg_dice'][0]*f['dmg_dice'][1]+f['dmg_fixed']+f['dmg_dice'][0]*f['dmg_dice'][1]-v['rd'])
assert min_net_each==20 and max_net_each==140 and 2*max_net_each < v['hp']
# identical attackers with same initiative, damage distributions unaffected by
# resolving A before B vs B before A if no on-hit state changes or elimination.
c10={
 'checkpoint':'POST-R10-C10',
 'R49_bound':dict(source='VLAB R49; two identical equipped Feryn -> Varok, individual 4d6',
    min_effective_dmg_single=20,max_effective_dmg_single_even_critical=140,
    maximum_two_attacks=280,varok_hp=734,
    no_elimination_possible_with_only_two_basic_attacks=True,
    initiative_priority_changes_total_damage_distribution=False,
    caveat='only in frozen two basic attack window; other skills/on-hit effects can invalidate commutativity'),
 'priority_tie_probability':qdata(sum((p*p for p in dice_dist(4,6).values()),Q())),
 'priority_expected_rounds_to_separate':None,
 'observed_R49_sources_selected':dict(scenes=3,damages=[83,104,100],total=287,normal_hits=6,
   selected_seeds_not_random_sample=True),
 'R49_control_conditional_six_normal_hits':dict(expectation_per_attack=qdata(Q(48)),expectation_six=qdata(Q(288)),not_hypothesis_test='selected seeds preclude random sample CI')
}
tie= sum((p*p for p in dice_dist(4,6).values()),Q())
c10['priority_expected_rounds_to_separate']=qdata(1/(1-tie))

# C10 extra: cost and differential physical/elemental damage resistance.
# This is NOT a choice of actual elemental mitigation sequence; deliberately
# keep two incompatible mathematical interpretations as sensitivity.
ACTIVATIONS={
 'Feryn':dict(extra=(5,8),PA=45,actor='Feryn',enemy='Varok',type='Vento'),
 'Varok':dict(extra=(6,12),PA=60,actor='Varok',enemy='Feryn',type='Impacto'),
 'Arveth':dict(extra=(6,10),PA=55,actor='Arveth',enemy='Feryn',type='Terra')
}
expenses=[]
for name,vv in ACTIVATIONS.items():
 a=ACTORS[name];b=ACTORS[vv['enemy']]
 raw=dice_dist(*vv['extra'])
 expected_extra=mean(raw)
 separate_after_RD=sum((max(0,total-b['rd'])*p for total,p in raw.items()),Q())
 # base attack lowest raw BEFORE mitigation exceeds target RD for all three
 assert a['dmg_dice'][0]+a['dmg_fixed']>b['rd']
 base_hit=next(r for r in c09['pairwise_normal_CA'] if r['attacker']==name and r['defender']==vv['enemy'])
 expenses.append(dict(attacker=name,defender=vv['enemy'],kind=vv['type'],PA_trigger=vv['PA'],
           every_hit_activation_limit='once per scene, 0 additional Ação Padrão; paid only on hit',
           PA_free_start=a['pa_free'],PA_free_after_trigger=a['pa_free']-vv['PA'],
           raw_extra_E=qdata(expected_extra),
           one_mitigation_event_increment_E_IF_same_damage_pool=qdata(expected_extra),
           separate_extra_RD_increment_E_IF_separately_mitigated=qdata(separate_after_RD),
           chance_hit_to_allow_trigger=base_hit['total_hit_per_attempt'],
           first_hit_attempts_IF_repeatable_infinite=qdata(1/Q(base_hit['total_hit_per_attempt']['fraction'])),
           legality_note='Mixed damage elemental RD, common strike same event, per-hit declaration and scene frequency must govern; do not choose arithmetic branch without rule'))
c10['activations']=expenses

# C11: Crit branch conditional with goat -> Feryn and potential Feryn counter.
goat_crit_dmg=effective_distribution(1,6,13,22,True) # normal critical extra +6
p_pos_damage=P_PLUS*prob(goat_crit_dmg, lambda d:d>0)
e_pos_damage=P_PLUS*mean(goat_crit_dmg)
assert p_pos_damage==Q(1,216) and e_pos_damage==Q(1,108)
# Feryn normal counter with Vantagem has min attack score 4+92+2 > any Goat
# numeric defense, guaranteed one-hit kill if no LAB-only negative critical.
counter_min_score=4+92+2
counter_min_net=8+47-5
assert counter_min_net==50 and counter_min_score>26 and counter_min_net>38
c11={
 'checkpoint':'POST-R10-C11',
 'goat_vs_Feryn':dict(source='R47/R47B source-derived goat Investida, Feryn RD22',
       raw_critical_values=list(range(20,26)),effective_critical_values=[max(0,r-22) for r in range(20,26)],
       probability_positive_life_per_attack=qdata(p_pos_damage),
       expected_life_lost_per_attack=qdata(e_pos_damage)),
 'R47B_verified_branch':dict(goat_crit_sequence=[6,6,6],goat_damage_die=4,raw=23,Feryn_RD=22,net=1,Feryn_hp_change='479->478',Feryn_reaction_predeclared_and_consumed=True,counter_reply_executed=False),
 'counter_semantic_branches':[{
    'label':'NUMERIC_THRESHOLD_ONLY', 'hypothetical_response_legal':True,
    'minimum_counter_score_Vantagem':counter_min_score,
    'minimum_counter_net_damage':counter_min_net,
    'would_one_hit_KO_Goat_IF_no_negative_critical_and_no_other_interference':True,
    'NOT_CANONIZED':True
   },{
    'label':'ACTUAL_HIT_HAS_PRECEDENCE','hypothetical_response_legal':False,
    'Feryn_hp_after_R47B':478,'Goat_hp_after_R47B':38,'NOT_CANONIZED':True
   }],
 'why_authority_needed':'Counter trigger text not supera CA numeric conflicts with automatic critical hit; combat consequence ranges from no reply to possible goat KO in same reaction window',
 'first_reaction_nested':'R48 pending own-turn reaction and nested response precedence; no new native scene',
 'new_master_question':'Ao receber crítico positivo autoacertador apesar da pontuação comum abaixo da CA, uma Reação de Contra-atacar declarada ANTES autoriza golpe de resposta, ou apenas quando o ataque realmente errou? E a resposta pode, por sua vez, desencadear Contra-atacar aninhado no próprio turno do agressor?',
 'no_canonical_rule_change':True
}

c07['rank_invariants']={
 'Bronze_2_vs_Bronze_4_rank_dice':'both Bronze, 1d6 under rank dice; star conflict does not alter dice category',
 'printed_CA_49_mathematics':'10 + DES38 + CON3/5 = 48.6, compatible with printed 49 under rounding; not rank resolution',
 'normal_Bronze_RD_5':'if creature is normal Bronze and lacks overriding defense, general RD5 rank-invariant across these two stars',
 'attack_admission':'rank dice and CA can be inspected; Galha hit remains blocked without Luta or alternate legitimate resolution'
}

rows=[('C07_SOURCE_AUTHORITY.json',c07),('C08_R47_R49_AUDIT.json',c08),('C09_ON5_LAB_SENSITIVITY.json',c09),('C10_AOO_PRIORITY_PA.json',c10),('C11_COUNTER_NORMATIVE_BRANCH.json',c11)]
for fname,obj in rows:
    (ROOT/fname).write_text(json.dumps(obj,indent=2,ensure_ascii=False,sort_keys=True)+'\n',encoding='utf8')

# Actual old archive and local R10/C02-C06 files are only read, never mutated.
p=ROOT.parent/'evidence_readonly/VLAB_R47_R48_R49_CRITICO_CONTRA_ANINHAMENTO_ON5_MESTRE_ONLY.zip'
actual=hashlib.sha256(p.read_bytes()).hexdigest()
assert actual==c08['documentary_sha256']

print('C07_C11_EXACT_OK')
print('vLAB_original_SHA',actual)
for r in c09['pairwise_normal_CA']:
 print('PAIR',r['attacker'],r['defender'], 'p_common_hit',r['hit_basic_conditional_noncrit']['fraction'],
       'p_anyhit',r['total_hit_per_attempt']['fraction'], 'E_net',r['E_damage_per_attack']['fraction'])
print('R49_tie',str(tie),'expected_rounds_to_resolve',str(1/(1-tie)))
for x in expenses:print('PA',x['attacker'],'extra',x['raw_extra_E']['fraction'],'after separate RD',x['separate_extra_RD_increment_E_IF_separately_mitigated']['fraction'], 'first_hit_attempts',x['first_hit_attempts_IF_repeatable_infinite']['fraction'])
print('COUNTER R47B goat p_pos_damage',p_pos_damage,'E',e_pos_damage)
