#!/usr/bin/env python3
"""Research-only exact arithmetic, continuation POST-R10-C01 (not VLAB execution).
Source: read-only Notion fetch 2026-10-15; source records below manually transcribed
from physical readback. Unresolved fields NULL. No official damage/actor mutation.
"""
from __future__ import annotations
import hashlib, json, math, itertools
from fractions import Fraction as F
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parent
assert json.loads((ROOT/'C01_PREREG_SAMPLE_FROZEN.json').read_text())['selection_frozen_new_candidate_count']==18

def src(key,pid,title,body,ancestor,kind,species,ca=None,hp=None,formulas=None,features=None,notes=None):
 return {'cohort_key':key,'page_id':pid,'url':'https://app.notion.com/p/'+pid,'title_rank':title,
 'body_rank':body,'tree_rank':ancestor,'source_kind':kind,'identity':species,'ca':ca,'hp':hp,
 'initial_numeric_attacks':formulas or [],'features':features or [],'notes':notes or []}

S=[
 src('B3','bdbc2b324ede83b09e56014278be74d8','Bronze 3','Bronze 3','Bronze 3','MASTER_BEAST','Corvo carniceiro',24,'45+50',features=['Asas Noturnas: +3 DES and +2 Furtividade at night; not damage','stun CD 6+INT with no duration/procedure'],notes=['HP expression 45+50 not collapsed']),
 src('B4a','8acc2b324ede827b9bc801746ae97409','Bronze 4','Bronze 2','Bronze 4','MASTER_BEAST','veado das montanhas',49,'52+50',formulas=[{'name':'Galha mortal','dice':[1,6],'attribute':'FOR','attribute_value':11,'formula':'1d6+FOR11','damage_type':'antler attack; subtype not declared','cost_PA':None,'hit_Luta':None}],features=['Corrida congelante 20m/turn; maneuver rules incomplete','Caminhada silenciosa +4m movement on snow'],notes=['Body Bronze2, title/tree Bronze4, no rank resolved']),
 src('B4b','109c2b324ede8206bee481f992b7f800','Bronze 4','Bronze 2','Prata 5','MASTER_BEAST','Escorpião de Fogo',41,'104+50',features=['Cauda Incendiária burn unquantified','Carapaça Refletora magic return percentage unspecified','Corrida Ardente residual damage unspecified'],notes=['drops dice excluded from attacks','triple-rank conflict']),
 src('O2a','5fac2b324ede8381a25581194ebf9bd7','Ouro 2','Ouro 2','Ouro 2','MASTER_BEAST','Regalis voltmane (tree); body name blank',78,936,formulas=[{'name':'Raio eletrizante','dice':[2,4],'attribute':'INT','attribute_value':72,'formula':'2d4+INT72','damage_type':'raio; elemental RD unknown','cost_PA':None,'hit_Luta':None,'rider':'on independent 1d4=1 require Fortitude save; on failure paralyze 1 turn; Fortitude DC unlisted'}, {'name':'Raio purificador','dice':[2,4],'attribute':'INT','attribute_value':72,'formula':'2d4+INT72','damage_type':'raio; elemental RD unknown','cost_PA':None,'hit_Luta':None},{'name':'Toque macabro','dice':[1,4],'attribute':'INT','attribute_value':72,'formula':'1d4+INT72','damage_type':'macabro; unspecified precise type','cost_PA':None,'hit_Luta':None}],features=['Refração Luminosa +6CA; creates 3 copies each +2 CA; whether additional stack unclear'],notes=['body species blank','do not assume spells can receive normal attack critical']),
 src('O2b','e66c2b324ede82d4894681c836bb012f','Ouro 2','Ouro Negro (star absent)','Ouro 2','MASTER_BEAST','Dracquático Azur',57,660,features=['Garras de Correnteza can cut through armor; no numeric bypass or damage'],notes=['title/tree Ouro2 vs body Ouro Negro']),
 src('O2c','991c2b324ede8348a25b8165cfb81e1a','Ouro 2','Bronze (star absent)','Ouro Negro 1','MASTER_BEAST','Leviatã Luminescente',32,480,features=['Barbatanas Cortantes no numeric skill damage'],notes=['drop dice excluded','triple-rank conflict']),
 src('ON1a','a0dc2b324ede823e911801087a7331b0','Ouro Negro 1','Ouro (star absent)','Ouro Negro 1','MASTER_BEAST','Cão Infernal de Fogo',86,1824,features=['Mordida Flamejante burning unquantified','Chicote de Fogo area no dice','Aura de Calor persistent no rate','Resistência ao Fogo claimed immunity'],notes=['drop dice excluded']),
 src('ON1b','f28c2b324ede834b8db781887d0019fa','Ouro Negro 1','Lendário (star absent)','Ouro Negro 1','MASTER_BEAST','Espinodonte',66,1120,features=['Investida Espinhosa no numeric damage','Rocha Flamejante area no dice'],notes=['drop dice excluded']),
 src('ON1c','294c2b324ede83cc8529017b8555b5be','Ouro Negro 1','Lendário (star absent)','Ouro Negro 1','MASTER_BEAST','Carpe Draco',75,1040,features=['Sopro de Água area push no numeric damage'],notes=['drop dice excluded']),
 src('L1a','6c6c2b324ede8295ad98813f0db138f4','Lendário 1','Lendário (star absent)','Lendário 4','MASTER_BEAST','Wyvern',150,5250,features=['Garras Afiadas vague damage','Escamas Resistentes undefined specific RD'],notes=['body Legendary without star, tree L4 conflicts title L1']),
 src('L1b','ffec2b324ede8289a99101f42099c55c','Lendário 1 Titã','Bronze (star absent)','Lendário 1','MASTER_BEAST','Elefante Colossal',133,6090,features=['Pisada Sísmica area no dice','resist physical nonmagic amount absent'],notes=['title Lendario Titan vs body Bronze','drops dice excluded']),
 src('L1c','394c2b324ede82a3b9f401465b96f9ed','Lendário 1 Titã','Bronze (star absent)','Lendário 1','MASTER_BEAST','Guardião Etéreo',121,3150,features=['Círculos Místicos DoT lacks magnitude and duration','Explosão Etérea area lacks damage'],notes=['title Lendario Titan vs body Bronze']),
 src('bleed1','7d9c2b324ede83698dc381e76c958649',None,None,None,'PARTY_MIRROR_EXCLUDE','Sangramento (Party Mestre Espelho)',formulas=[],features=[],notes=['PARTY mirror located, content excluded from Master corpus and no cross-surface data propagation']),
 src('bleed2','3f5c2b324ede81b191dac6a379e5781f',None,'Ouro',None,'PS_SEMICANON_EXCLUDE','Pérola Sangue Sereno',formulas=[],features=['proposed healing 4d8+8, 18PA, Action Standard, 1 application/8h'],notes=['healing not damage and incubating PS; no official inference']),
 src('poison1','3efc2b324ede815f9e59efd4445697fb',None,'Bronze 5 proposed',None,'PS_SEMICANON_EXCLUDE','Lótus Veneno Quieto',formulas=[],features=['proposal ingredient, no numeric damage'],notes=['explicit noncanonical/PS only']),
 src('poison2','1a8c2b324ede82068fdd01d6066b2184',None,None,None,'MASTER_NARRATIVE_ITEM','Veneno de Água-viva',features=['poison usable in potions/toxins, no numeric damage or application'],notes=['no numeric recipe, no poison damage']),
 src('cost1','3f6c2b324ede81a78a59d3d81fd5e966','Ouro Negro 5','Ouro Negro 5',None,'MASTER_PROPOSED_ENCOUNTER_EXCLUDE','Sikong Iskiel proposed encounter',features=['many numeric equipment/action costs; not official native character'],notes=['Master-side encounter proposal; not current canonical actor']),
 src('cost2','3edc2b324ede816cbad5ca3880ce144d',None,'Sem classificação',None,'MASTER_EQUIPMENT','Traje águia celeste',features=['20PA/day ongoing','Voo da Águia costs 4PA per activation, at most once/turn, movement 4.5m','Contra-ataque grants +2CA while Counterattacking; no wearer/source data'],notes=['current item, not equipped by selected beast and not an attack']),
]


# Manually recorded Notion last-edited timestamps from the same 18 fetches. These are
# native page metadata, NOT hashes of full source content and NOT complete canonical gates.
TIMESTAMPS={
'B3':'2026-10-01T18:00:33.849Z','B4a':'2026-10-01T18:00:42.529Z','B4b':'2026-10-01T18:00:47.889Z',
'O2a':'2026-10-01T18:00:50.244Z','O2b':'2026-10-01T18:00:40.391Z','O2c':'2026-10-01T18:00:45.311Z',
'ON1a':'2026-10-01T18:00:48.404Z','ON1b':'2026-10-01T18:01:10.358Z','ON1c':'2026-10-01T18:00:46.285Z',
'L1a':'2026-10-01T18:00:50.110Z','L1b':'2026-10-01T18:01:07.676Z','L1c':'2026-10-01T18:00:57.259Z',
'bleed1':'2026-09-30T04:46:05.791Z','bleed2':'2026-10-10T18:38:56.762Z',
'poison1':'2026-10-06T19:09:56.012Z','poison2':'2026-09-30T04:44:25.812Z',
'cost1':'2026-10-11T11:45:05.928Z','cost2':'2026-10-03T13:21:42.496Z'}
assert set(TIMESTAMPS)=={x['cohort_key'] for x in S}
for x in S:
 x['source_last_edited_at']=TIMESTAMPS[x['cohort_key']]
 x['source_content_sha256']='NOT AVAILABLE: fetched Notion content not transported as raw bytes to local corpus'

with open(ROOT/'C01_NEW_SOURCE_LEDGER.json','w',encoding='utf8') as f:json.dump(S,f,ensure_ascii=False,indent=2)
assert len(S)==18 and len({x['page_id'] for x in S})==18
prior_ids=set(json.loads((ROOT/'C01_PREREG_SAMPLE_FROZEN.json').read_text())['already_examined_known_source_page_ids_sorted'])
assert not (prior_ids & {x['page_id'] for x in S}), 'known historical duplicate ID not allowed'
beasts=[x for x in S if x['source_kind']=='MASTER_BEAST']
assert len(beasts)==12
mismatch=[x for x in beasts if x['body_rank']!=x['title_rank'] and x['body_rank']!=x['title_rank'].split(' Titã')[0]]
# Clarification: Legendary without star does NOT resolve actual star; conservatively title-vs-body rank species comparison (strip star)
rank=lambda x: (x or '').split(' ')[0] if not (x or '').startswith('Ouro Negro') else 'Ouro Negro'
rank_mismatches=[x for x in beasts if rank(x['title_rank'])!=rank(x['body_rank'])]
assert len(rank_mismatches)==7,[(x['cohort_key'],x['title_rank'],x['body_rank']) for x in rank_mismatches]
# B4a/B4b both Bronze but different stars; exact rank/star conflict + L1a Legendary1 vs Legendary unspecified
explicit_title_body_exact=[x for x in beasts if x['body_rank']==x['title_rank']]
assert len(explicit_title_body_exact)==2,explicit_title_body_exact
source_numerical=[x for x in beasts if x['initial_numeric_attacks']]
assert len(source_numerical)==2
numeric=[(x,y) for x in beasts for y in x['initial_numeric_attacks']]
assert len(numeric)==4

checks=[]
def check(condition,msg):
 checks.append({'check':msg,'pass':bool(condition)});
 if not condition:raise AssertionError(msg)

def pmf_ndice(n,faces):
 dist=Counter({0:1})
 for _ in range(n):
  new=Counter()
  for a,ct in dist.items():
   for face in range(1,faces+1):new[a+face]+=ct
  dist=new
 assert sum(dist.values())==faces**n
 return {k:F(v,faces**n) for k,v in dist.items()}

def epos(pmf,add,rd):return sum(p*max(0,base+add-rd) for base,p in pmf.items())
def ppos(pmf,add,rd):return sum(p for base,p in pmf.items() if base+add>rd)
def fv(z):return {'fraction':str(z),'decimal':float(z)}

# Real source initial damage and hypothetical ceiling when an actual normal attack/critical were admissible.
formula_stats=[]
for row,a in numeric:
 n,m=a['dice'];attr=a['attribute_value'];dist=pmf_ndice(n,m)
 intrinsic=sum(k*p for k,p in dist.items());gross=intrinsic+attr
 formula_stats.append({'source_id':row['page_id'],'identity':row['identity'],'rank_title':row['title_rank'],'rank_body':row['body_rank'],
   'action':a['name'],'formula':a['formula'],'type_documented':a['damage_type'],'dice_intrinsic_mean':fv(intrinsic),'gross_mean_if_damage_resolves':fv(gross),
   'external_attribute_share_gross':fv(F(attr,1)/gross),'min_gross':attr+n,'max_gross':attr+n*m,
   'critical_damage_if_eligible':{'min':attr+n+n*m,'max':attr+2*n*m,'eligibility':'UNVERIFIED; do not apply crit to elemental ability without source-specific authority'},
   'precision':'UNKNOWN_LUTA/CD/SAVE','action_cost_PA':None})
check(len(formula_stats)==4,'four new literal damage actions')

# DAMAGE-RANK generic bases and RD tables: normative mathematical chassis, NOT individual legal skill.
attacks={'Normal Bronze 3d6':(3,6),'Normal Prata 6d6':(6,6),'Normal Ouro 9d6':(9,6),'Normal Ouro Negro 12d6':(12,6),
 'Titan Bronze 5d10':(5,10),'Titan Prata 8d10':(8,10),'Titan Ouro 11d10':(11,10),'Titan Ouro Negro 13d10':(13,10),'Titan Lendario 20d10':(20,10)}
rds={'Normal Bronze':5,'Normal Prata':15,'Normal Ouro':25,'Normal Ouro Negro':35,'Titan Prata':30,'Titan Ouro':45,'Titan Ouro Negro':60,'Titan Lendario':75,'Divina if explicit flag':120}
frontier={}
for a,(n,faces) in attacks.items():
  d=pmf_ndice(n,faces)
  dd={}
  for typ,rd in rds.items():
   pk=ppos(d,n*faces,rd);dk=epos(d,n*faces,rd)
   dd[typ]={'RD':rd,'crit_base_damage_range':[n+n*faces,2*n*faces],
      'p_positive_if_critical_base_only':fv(pk),
      'E_net_if_critical_base_only':fv(dk),
      'p_positive_per_attack_if_only_critical_hits_and_independent_critical_check':fv(pk*F(1,108)),
      'E_net_per_attempt_if_only_critical_hits_and_independent_check':fv(dk*F(1,108))}
  frontier[a]=dd
# exact high impact cliff
check(frontier['Normal Bronze 3d6']['Normal Ouro Negro']['p_positive_if_critical_base_only']['fraction']=='1/216','Bronze base 3d6 vs RD35 only three sixes')
check(frontier['Normal Bronze 3d6']['Titan Ouro']['p_positive_if_critical_base_only']['fraction']=='0','Bronze 3d6 crit max36 cannot penetrate Titan Gold RD45')
check(frontier['Normal Bronze 3d6']['Normal Ouro Negro']['p_positive_per_attack_if_only_critical_hits_and_independent_critical_check']['fraction']=='1/23328','double rare positive crit + max damage')
# Galha mortal body Bronze2/title Bronze4, but fixed damage remains valid under either rank (no attribute rank infer).
galha=pmf_ndice(1,6)
check(ppos(galha,11+6,25)==0,'Galha crit max23 cannot beat RD25')
# Frigido Rabada B5 independent Luta +6 only for hit; hit vs CA68 impossible noncrit. RD25 0..5 if crit.
check(epos(galha,18+6,25)==F(5,2),'Frigido critical after RD25 has conditional expected 2.5')
check(ppos(galha,18+6,25)==F(5,6),'Frigido critical ppositive 5/6')
check(epos(galha,18+6,30)==0,'Frigido crit no positive dmg vs RD30')
# Required ordinary attack Luta to give a chance vs a CA of 78, e.g body Bronze Galha (1d6+FOR11+Luta)
first_luta=78-11-6+1
check(first_luta==62,'first hypothetical Galha common hit on CA78 needs individual Luta >=62')

# R10 checkpoint exact symmetric two Cabras: expected attack opportunities and probability of first actor win.
r10=json.loads((Path('/mnt/data/dmg_recovery/r10/R10_RESULTS.json')).read_text())
c=r10['goat_crit_only']['closed_form_symmetric_bilateral'];Eatt=F(c['expected_attack_count']['fraction']);Eround=F(c['mean_rounds']['fraction']);Efirst=F(c['p_first']['fraction'])
check(2*Eround-Efirst==Eatt,'R10 bilateral Eattack exact reconciliation')
critical_p=F(1,108)
E_positive_crit=Eatt*critical_p
E_nonlethal_push=E_positive_crit-1
# each positive critical in source Investida damages through RD5 and pushes 1.5m; last kill needs no recovery Move.
check(E_nonlethal_push>0,'expected nonterminal hit count positive')
# negative critical lab decision R42 BEFORE: attack auto-miss, damage0, AP consumed, no further penalty, within LAB only
E_negative_crit=Eatt*critical_p
check(E_negative_crit==E_positive_crit,'negative crit expected number matches probability if 1/108')
# If each non-lethal positive critical knocks adjacent target 1.5 to 3m, and a legal Movement can restore in own turn
# expected count of Movement uses needed IF legal mobility exists and target actively closes distance.
space={'baseline_R10_model_rounds_mean':fv(Eround),
 'expected_total_attacks':fv(Eatt),
 'expected_positive_crit_events_total':fv(E_positive_crit),
 'expected_negative_crit_events_total_if_lab_policy_R42_applies':fv(E_negative_crit),
 'expected_nonlethal_critical_pushes_needing_a_reposition_if_next_attack_requires_adjacency':fv(E_nonlethal_push),
 'forced_push_distance_each_if_source_conditions_hold_m':1.5,
 'distance_after_push_if_start_at_adjacent_1_5m':3.0,
 'movement_action_required':'conditional on capacity/geometry; VLAB R35 permits Movement recover before attack in a legal source-derived scene',
 'impact_on_rounds_if_Move_and_Attack_same_turn_admissible':'zero mathematical added rounds in this restricted one attack per round model, but extra Movement actions',
 'impact_on_rounds_if_Movement_cannot_restore':'NOT DETERMINABLE; reachability and terrain not specified; no free zero-time reposition'},

# PA economic source-real bound; not Vida conversion.
gear={'source_id':'3edc2b324ede816cbad5ca3880ce144d','item':'Traje águia celeste','classification':'sem classificação',
 'daily_PA_commit':20,'on_activation_PA':4,'max_activations_per_turn':1,
 'activation':'Voo da Águia, +4.5m jump if source mechanic legal; not general flight/walk ability',
 'conditional_consumption_for_k_activations':{str(k):20+4*k for k in [0,1,3,5,10,20]},
 'duration':'20PA per day; first payment/timing not specified here',
 'action_cost':'not specified for jump activation; cannot infer standard/free from (Atv.)',
 'comparison_limit':'cannot compare PA to HP; cannot apply to a random beast not documented wearing it'}

cohort={'frozen_prereg_sha256':hashlib.sha256((ROOT/'C01_PREREG_SAMPLE_FROZEN.json').read_bytes()).hexdigest(),
 'fetched_physical_pages':18,'master_pages_excluding_party':17,'party_mirror_excluded':1,
 'master_beast_pages':12,'rank_same_major_category_title_body':len(beasts)-len(rank_mismatches),
 'rank_major_category_mismatch_title_body':len(rank_mismatches),
 'rank_star_full_concordance_title_body':len(explicit_title_body_exact),
 'title_body_not_fully_concordant_count':len(beasts)-len(explicit_title_body_exact),
 'numeric_damage_actions':len(numeric),'unique_new_pages_with_numeric_damage':len(source_numerical),
 'new_numeric_damage_expression_kinds':len({a['formula'] for _,a in numeric}),
 'master_ps_or_unapproved_encounter_excluded':3,
 'master_unclassified_story_item_no_numeric_damage':1,
 'master_equipment_with_cost_no_damage':1,
 'historical_R03_R04_numeric_actions_29_prior':'not promoted to population estimate; compare cohorts exploratory only',
 'L003_membership_per_new_unit':'UNVERIFIED (zero new L003 unit certification)',
 'global_population_total':'UNDETERMINED',
 'bias_disclaimer':'Ranking from search title convenience, nonrandom, includes severe rank conflicts. No Luta, ability casting, PA attack, weakness or rank adjudication inferred.'}
check(cohort['rank_major_category_mismatch_title_body']==7,'7/12 rank CATEGORY differences title body')
check(cohort['rank_star_full_concordance_title_body']==2,'2/12 title/body exact full rank+stars')

out={'operation':'OP-DMG-CORPUS-EMP-01','round':'POST-R10-C01','date':'2026-10-15','source':'Notion MASTER READONLY, exact source pages manually screened, verified 2026-10-15',
 'baseline':'DMG-RANK-01 v1.1 unchanged','critical_auto_hit_authority':'Mestre express 2026-10-15, normative Notion write pending','new_native_VLAB_exec':0,'canonical_writes':0,
 'source_selection':cohort,'literal_new_attack_formulas':formula_stats,'crossrank_generic_BASE_ONLY':frontier,
 'source_specific_contrasts':{'Galha_Bronze_title4_body2_vs_RD25':{'max_gross_normal':17,'max_gross_critical':23,'p_positive_damage_even_if_hit_or_auto_crit':0,'prerequisites':'competent RD25 mitigates antler physical, no other buffs'},
  'Frigido_Rabada_vs_Behemoth_CA68_RD25':{'noncritical_p_common_hit':0,'critical_auto_p':fv(F(1,108)),
   'critical_damage_positive_conditional_probability':fv(F(5,6)),
   'p_damage_positive_per_attack':fv(F(5,648)),
   'E_net_damage_per_attack':fv(F(5,216)),
   'rd30_critical_damage':'always zero',
   'constraints':'zero extra buffs, Rabada 1d6+FOR18, critical independent vs ordinary 1d6 check, general RD25 competent, no extra reactions'},
  'Ouro2_Raio_eltrizante_rider':{'source_id':'5fac2b324ede8381a25581194ebf9bd7',
  'physical_gross_formula_same_as_Raio_purificador':'2d4+INT72',
  'rider_check_probability_if_1d4_separate_uniform':fv(F(1,4)),
  'p_stun_unconditional':'NOT AUTHORIZED; hit, Fortitude DC and resolution missing','none_of_two_spells_assigned_critical':True}},
 'spatial_action_economy':space[0], 'real_source_PA_economy':gear,
 'research_limits':['not a random sample','new sources have unknown Luta; no complete new real-fight','R41 native already handles positive critical; no duplicate test','R42 is REGISTRO ANTES only, laboratory negative crit decision already described but full R42 new native execution unverified','F0 gate 4/8 remains; no production writes','L003 0/71 authenticated unchanged'],
 'local_checks':checks,'check_pass_count':len(checks)}
p=ROOT/'C01_RESULTS_MODEL.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
# separate independent closed-form gate: critical of Bronze generic n=3 requires all 6 to breach RD35
with open(ROOT/'C01_CHECKPOINT_SUBRESULTS.txt','w') as f:
 f.write('NEW 18 fetched, 17 Master, 1 Party excluded, 12 Master beast, 7/12 major rank mismatch\n')
 f.write('BASE3d6 critical vs RD35: only (6,6,6) = 1/216 of positive critical checks; with 1/108 = 1/23328 per attack\n')
 f.write(f'EXPECTED NONLETHAL CRIT-TRIGGERED PUSHES {E_nonlethal_push} ~{float(E_nonlethal_push):.9f}\n')
 f.write(f'EXPECTED LAB NEGATIVE CRIT OBSERVATIONS {E_negative_crit} ~{float(E_negative_crit):.9f}\n')
 f.write(f'FRIGIDO CRIT+RD25 positive per attack 5/648; E_net_per_attack 5/216\n')
 f.write('no VLAB combat performed, zero Notion writes\n')
print(json.dumps({'cohort':cohort,'space':space[0],'FRIGIDO':out['source_specific_contrasts']['Frigido_Rabada_vs_Behemoth_CA68_RD25'],'local_checks_passed':len(checks)},ensure_ascii=False,indent=2))
