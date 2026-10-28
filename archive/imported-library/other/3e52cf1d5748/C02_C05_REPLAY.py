#!/usr/bin/env python3
"""Four read-only research cycles after DMG POST-R10 C01. No VLAB engine invoked.
Source figures: frozen Notion fetches 2026-10-16 in project's Master workspace.
All character encounters are sandbox-source/proposed NPC figures, not campaign results.
"""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
from itertools import product
import hashlib, json, math, random, statistics

root=Path(__file__).resolve().parent
old=Path('/mnt/data/dmg_recovery/post_r10_c01')
old_names=['C01_NEW_SOURCE_LEDGER.json','C01_RESEARCH_MODEL.py','C01_RESULTS_MODEL.json','PSV_DMG_POST_R10_C01.md']
old_hashes={name:hashlib.sha256((old/name).read_bytes()).hexdigest() for name in old_names}

def conv(n,sides):
    c=Counter({0:1})
    for _ in range(n):
        z=Counter()
        for v,k in c.items():
            for d in range(1,sides+1):z[v+d]+=k
        c=z
    assert sum(c.values())==sides**n
    return c

def fv(f): return {'numerator':f.numerator,'denominator':f.denominator,'approx':round(float(f),12)}

def write(name,obj):
    p=root/name
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return p

def wh(name,text):
    p=root/name;p.write_text(text,encoding='utf-8');return p

# === Cycle 1: physical source lineage, ability eligibility, no inferred Luta/rank ===
cycle1={
 'id':'POST-R10-C02','operation':'OP-DMG-CORPUS-EMP-01','state':'VERIFIED_SOURCE_IDENTITIES / BLOCKED_NATIVE_ATTACK_FIELDS',
 'sources':[{'id':'8acc2b324ede827b9bc801746ae97409','parent':'d8fc2b324ede8363af1601b68774a7e7','title':'Bronze 4','body':'Bronze 2 (1d6)','identity':'Veado das Montanhas','action':'Galha Mortal','gross':'1d6+FOR11','CA':49,'FOR':11,'DES':38,'CON':3,'missing':['rank star conflict','Luta for Galha','damage subtype','activation PA','range/geometry'],'classification':'BLOCKED_NORMATIVE_AND_SOURCE'},
            {'id':'5fac2b324ede8381a25581194ebf9bd7','parent':'bd4c2b324ede8381929e815d7159fe4d','title':'Ouro 2','body':'Ouro 2','identity_parent':'Regalis voltmane','body_name':'BLANK','ability_text_mentions':'Aurora Radiante','actions':['Raio eletrizante 2d4+INT72','Raio purificador 2d4+INT72','Toque macabro 1d4+INT72'],'CA':78,'INT':72,'missing':['same-species identity text in body','whether abilities are MAGIA','hit/CD/salvaguarda for each ability','PA each ability','distance','elemental RD and save DC'],'classification':'SOURCE_VALUES_VERIFIED / MECHANICS_PARTIAL'}],
 'additional_identity_reconciliation':{'parent_suffices_to_label_veado':'YES, source index; does not resolve rank','parent_suffices_to_label_regalis':'YES, indexed parent; does not fix blank body name or Aurora wording','aurora_siblings':['1c6c2b324ede8252872c81bd287fb516','6c9c2b324ede83e9b7130113b18fd2a7','2e9c2b324ede829eba23815d22d51794'],'cross_family_warning':'Aurora Radiante phrases occur in Regalis ability lines; do NOT dedupe as same entity or import magical properties'},
 'normative':['System of Combat: 1 standard action per normal attack; attack roll class dice + suitable attribute + INDIVIDUAL Luta','System of Magic: spells do NOT crit, and no universal attack roll to hit; needs spell identity before applying','Besta creation rank proficiency table not equal automatic trained Luta; do not assume absent Luta is zero'],
 'v_lab_receipt':'no new VLAB admission; source gate only', 'scientific_discovery':'three Regalis numeric attacks cannot automatically be entered into critical-capable physical attack cohort; classifying them as spells also requires proof',
 'before':'C01: child body Regalis blank, Veado rank conflict, Luta unknown',
 'after':'C02: parent chain physically found for both, Aurora copy contamination verified, spell no-critical exclusion located, Luta/cost remain genuinely unresolved',
 'next':'C03: use available source-complete equipped ON5 attacks rather than filling either B4/O2 skill Luta.'}
write('C02_SOURCE_ADMISSION.json',cycle1)
wh('C02_PSV.md','# C02 — Proveniência e admissão\n\n**Resultado:** parent `Regalis voltmane` confirma rótulo indexador da folha Ouro2, mas corpo ainda não nomeia espécie e técnicas mencionam Aurora Radiante. `Veado das Montanhas` confirmado pelo parent, mas Bronze4 (título/árvore) × Bronze2 (corpo) mantém estrela conflitante. Habilidade Galha Mortal tem `1d6+FOR11`, mas Luta e tipo de dano são ausentes. Regalis possui `2d4+INT72` (2 raios) e `1d4+INT72` (toque), sem PA e sem teste ofensivo definido.\n\n**Revelação normativa:** o Sistema de Magia determina que MAGIAS não causam crítico nem exigem teste universal de acerto; é proibido transferir o crítico automático da R10 para os raios de Regalis sem provar que são golpes e não magias. Da mesma forma, não podem ser tratados como magias apenas pelo elemento Raio. Nenhuma nova cena READY; não assumir Luta+10 da tabela de proficiência ou ausência = zero.\n\n**Próxima fronteira executada:** C03, ataques de NPCs ON5 fonte-equipada que o VLAB já admitiu em R44–R46.\n')

# === Cycle 2: actual source-equipped all ON5, every component mechanically explicit ===
P=Q(1,108); attack=conv(4,6)
actors={
 'Feryn':{'rank':'Ouro Negro 5','CA':123,'evade':125,'defend':56,'RD':22,'HP':479,'initiative_fixed':82,'DES':80,'attack_fixed':92,'damage_dice':[8,8],'damage_fixed':47,'free_PA':424,'source_id':'3f6c2b324ede81ce9c61db8127bf0e31'},
 'Varok':{'rank':'Ouro Negro 5','CA':83,'evade':83,'defend':99,'RD':35,'HP':734,'initiative_fixed':29,'DES':27,'attack_fixed':100,'damage_dice':[10,10],'damage_fixed':48,'free_PA':324,'source_id':'3f6c2b324ede81f49ea9efbe1a811091'},
 'Arveth':{'rank':'Ouro Negro 5','CA':93,'evade':95,'defend':97,'RD':30,'HP':806,'initiative_fixed':25,'DES':23,'attack_fixed':72,'damage_dice':[8,10],'damage_fixed':35,'free_PA':344,'source_id':'3f6c2b324ede8105891fc647242e61ca'}}

def pcommon(a,dc):return Q(sum(v for die,v in attack.items() if die+a['attack_fixed']>dc),sum(attack.values()))

def dm(a,rd,critical=False):
 n,s=a['damage_dice'];normal=conv(n,s);fixed=a['damage_fixed']+(n*s if critical else 0)-rd
 return {max(0,score+fixed):ways for score,ways in normal.items()}

def E_onhit(a,rd,critical=False):
 n,s=a['damage_dice'];d=conv(n,s)
 return Q(sum(ways*max(0,score+a['damage_fixed']+(n*s if critical else 0)-rd) for score,ways in d.items()),sum(d.values()))

def expected_by_attack(a,t,defense):
 q=pcommon(a,t[defense]);e1=E_onhit(a,t['RD']);e2=E_onhit(a,t['RD'],True)
 # Independent critical verification from ordinary attack roll (R41/R18 experimental)
 return {'p_common_if_no_critical':fv(q),'p_auto_critical':fv(P),
 'p_total_success':fv(P+(1-P)*q),
 'E_normal_net_on_common_hit':fv(e1),'E_critical_net_on_auto_hit':fv(e2),
 'E_net_per_attempt':fv(P*e2+(1-P)*q*e1),
 'p_net_positive_per_attempt':fv(P*(Q(sum(v for x,v in dm(a,t['RD'],True).items() if x>0),sum(dm(a,t['RD'],True).values())))+(1-P)*q*(Q(sum(v for x,v in dm(a,t['RD']).items() if x>0),sum(dm(a,t['RD']).values()))))}

def pmt(a,t,defense):
 """Compute probability mass net damage including misses, using fractional per-event PMF."""
 q=pcommon(a,t[defense]);n,s=a['damage_dice'];den=s**n
 out={0:float((1-P)*(1-q))}
 for critical,weight in [(False,(1-P)*q),(True,P)]:
  for x,count in dm(a,t['RD'],critical).items():out[x]=out.get(x,0)+float(weight)*count/den
 assert abs(sum(out.values())-1)<1e-9
 return out

def e_attacks_to_hp(hp,pmf):
 """Float renewal equation, explicit 0 damage self-loop. Exact PMF rational upstream."""
 p0=pmf.get(0,0);assert 0<=p0<1
 nonzero=[(damage,prob) for damage,prob in pmf.items() if damage>0]
 e=[0.0]*(hp+1)
 for h in range(1,hp+1):
  e[h]=(1+sum(prob*e[max(0,h-d)] for d,prob in nonzero))/(1-p0)
 return e[hp]

pairs=[('Feryn','Varok','CA'),('Feryn','Arveth','CA'),('Varok','Feryn','CA'),('Varok','Feryn','evade'),('Arveth','Feryn','CA'),('Arveth','Varok','CA'),('Feryn','Varok','defend')]
cases={}
for who,whom,defn in pairs:
 a,t=actors[who],actors[whom];x=expected_by_attack(a,t,defn)
 x['target_HP']=t['HP'];x['attacker_equipped_source']=a['source_id'];x['defender_equipped_source']=t['source_id'];
 x['model_expected_attacks_to_defeat_single_stationary_target']=round(e_attacks_to_hp(t['HP'],pmt(a,t,defn)),8)
 cases[f'{who}_vs_{whom}_{defn}']=x
assert cases['Feryn_vs_Varok_CA']['p_common_if_no_critical']['numerator']==1
assert cases['Varok_vs_Feryn_CA']['p_common_if_no_critical']['approx']==round(1/1296,12)
assert cases['Varok_vs_Feryn_evade']['p_common_if_no_critical']['numerator']==0
assert cases['Arveth_vs_Feryn_CA']['p_common_if_no_critical']['numerator']==0
assert cases['Feryn_vs_Varok_defend']['p_common_if_no_critical']['numerator']==1261 and cases['Feryn_vs_Varok_defend']['p_common_if_no_critical']['denominator']==1296
# initiative Feryn > Varok regardless of dice, source-complete
assert 82+4 > 29+24
cycle2={'id':'POST-R10-C03','method':'exact d6/d8/d10 convolution; critical + regular hit disjoint event model; explicit E renewal','p_critical_auto':fv(P),'actors':actors,'cases':cases,
 'policy':'one baseline equipped standard attack per valid adjacent attack opportunity; damage of physical chosen against printed kit RD; crit verification independent of common roll; no reactions unless defense policy specifically selected; no movement/range changes, no failure critical consequence',
 'initiative_distinction':'Feryn 4d6+82 always acts before Varok 4d6+29 in a two-actor initiative roll; NOT evidence of a full fight',
 'scientific_hypothesis':'same-rank ON5 equally starred combatants need not have remotely equal realized damage; sufficient CA can null conventional high base damage',
 'status':'MATH_ONLY_FROM_SOURCE_ADMITTED_ON5 / not native bilateral fight',
 'next':'C04 quantify once-per-scene boosts and PA accounting to test whether burst powers change precision asymmetry.'}
write('C03_EQUIPPED_ON5_EXACT.json',cycle2)
wh('C03_PSV.md','# C03 — Contraste ON5 com Luta e equipamento documentados\n\nOs três NPCs Sikong ON5 foram admitidos como FONTES MESTRE-SIDE propostas, com ataques equipados e iniciativas numéricas já usadas nas janelas VLAB R44–R46. Não se atribuiu proficiência geral por rank.\n\n**Pergunta:** se Varok causa mais por acerto do que Feryn, por que sua eficiência contra Feryn pode ser muito menor? Resposta: Varok `4d6+100` contra CA123 supera a defesa apenas com `24/24` (uma combinação em 1296), ao passo que Feryn `4d6+92` supera CA83 de Varok sempre. O crítico válido ultrapassa defesa mas não torna o acerto comum frequente. Veja `C03_EQUIPPED_ON5_EXACT.json` para esperanças e E[ataques] exatas/recorrenciais.\n\n**Contraprova:** Arveth também possui ataque completo mas não supera CA123 com `4d6+72` em resultado comum. A inferência é sobre estas fontes e equipamento, não sobre todos os ON5. Reações escolhidas e deslocamento completo não modelados como combate real.\n\n**Próxima fronteira executada:** C04, dano por ação e custo de disparos únicos.\n')

# === Cycle 3: once per scene marginal damages without assuming PA -> HP conversion ===
boosts={
 'Feryn':{'name':'Presas da Noite sem Pegadas: descarga Vento','cost_PA':45,'dice':[5,8],'frequency':1,'on_hit':True,'action':'same equipped standard hit','target_sample':'Varok'},
 'Varok':{'name':'Machado do Juramento: Quebra do Tronco','cost_PA':60,'dice':[6,12],'frequency':1,'on_hit':True,'action':'same equipped standard hit','target_sample':'Feryn'},
 'Arveth':{'name':'Bastião das Sete Gargantas: Fissura','cost_PA':55,'dice':[6,10],'frequency':1,'on_hit':True,'action':'same equipped standard hit','target_sample':'Varok'}
}
for who,b in boosts.items():
 a,t=actors[who],actors[b['target_sample']];n,d=b['dice'];e=Q(n*(d+1),2)
 # if the activation is deferred UNTIL confirmed hit, p_hit is the chance this one action provides legal activation
 ph=expected_by_attack(a,t,'CA')['p_total_success'];prob=Q(ph['numerator'],ph['denominator'])
 b.update({'mean_extra_raw_dice_if_activation':fv(e),'gross_dice_mean_per_PA_spent':fv(e/b['cost_PA']),
           'max_legal_activations_in_ONE_SCENE':1,'max_legal_paid_PA_this_specific_boost_in_ONE_SCENE':b['cost_PA'],
           'p_eligible_hit_on_this_one_attempt':fv(prob),
           'expected_extra_raw_dice_if_activate_on_first_hit_opportunity_and_ONE_attempt':fv(prob*e),
           'PA_max_free_source':a['free_PA'],
           'not_claimed':'net elemental damage/combined RD/total scene sustained DPS not determined'} )
assert boosts['Varok']['mean_extra_raw_dice_if_activation']['numerator']==39
assert boosts['Feryn']['mean_extra_raw_dice_if_activation']['numerator']==Q(45,2).numerator
cycle3={'id':'POST-R10-C04','source':'three existing ON5 equipped NPCs','boosts':boosts,
 'action_consistency':'1 Standard action for equipped normal weapon; activation on-hit no new Standard; once per scene, not per turn, not per-day recharge',
 'equipment_contract':'Feryn 90PA/day, Varok 95PA/day, Arveth 85PA/day already included in total committed PA; never subtract again in a 1-hit model',
 'limits':['wind/earth elemental mitigation may be separate from physical attack; cannot assume no second RD','PA free maximum is capacity not unlimited resource','cannot compare PA expense to HP saved as universal exchange rate','all three skill boosts are one per scene; never extrapolate to all rounds'],
 'scientific_hypothesis':'raw burst per paid PA fails as predictor of realized burst when probability of landing attack differs',
 'negative_finding':'Varok has higher raw +damage than Feryn per activation but much lower immediate probability of legally spending that resource on hit vs Feryn; not a global power ranking',
 'next':'C05 audit reaction priority, tie RNG, critical-counter incompatibility and VLAB future delta without overwriting R47–R49.'}
write('C04_PA_ACTION_BUDGET.json',cycle3)
wh('C04_PSV.md','# C04 — Custos genuínos por cena e precisão\n\nAs três armas equipadas ON5 têm ataques Padrão com poderes ativáveis **após acertar** na MESMA ação, **uma vez por cena**. Feryn paga +45PA por +5d8 Vento, Varok +60PA por +6d12 impacto, Arveth +55PA por +6d10 Terra. Seus custos de vínculo 90/95/85PA por DIA já estão nos compromissos; não podem ser novamente debitados por golpe.\n\nO marginal bruto médio por ativação é 22,5/39/33, respectivamente. Não se pode transformar isso em dano líquido sem resolver RD por subtipo e consequências por alvo. A eficiência do recurso depende da chance de abrir a janela de ativação: Feryn contra Varok acerta sempre no modelo comum, enquanto Varok contra Feryn enfrenta um limite de precisão. Portanto **maior burst nominal não é maior burst realizável**.\n\n**Próxima fronteira executada:** C05, prioridade, reação e fonte versus VLAB R47–R49.\n')

# === Cycle 4: decision of Master AoO tie, independent probability, known initiative ===
D=conv(4,6)
num=sum(v*v for v in D.values());den=sum(D.values())**2
p_tie=Q(num,den)
check=D[4]==1 and D[24]==1
P_Ffirst=Q(1,2)  # same dex tie; fair winner after any R26 tie rounds; no ID preference
indep_init={
 'Feryn_vs_Varok':{'difference_min':(82+4)-(29+24),'different_rank_dice':'both ON5 4d6','certainty':'Feryn acts earlier'},
 'Varok_vs_Arveth':{'difference_min':(29+4)-(25+24),'certainty':'may change by dice'},
 'Feryn_vs_Arveth':{'difference_min':(82+4)-(25+24),'certainty':'Feryn acts earlier'}
}
# 4d6 two sources independent same DEX, tie -> R26 reroll. #priority shots 1/(1-p_tie)
pref=Q(1,1)/(1-p_tie)
cycle4={'id':'POST-R10-C05','VLAB_physically_recovered_latest':'R47-R49 REGISTRO ANTES, no readback DEPOIS at checkpoint; R43-46 already after verified','master_authority':'R43 same trigger highest DES before dice; if DES tie: competent dice of class then R26 reroll only tied; no universal d6','sources_ongoing':['3f6c2b324ede81ce9c61db8127bf0e31','3f6c2b324ede81f49ea9efbe1a811091','3f6c2b324ede8105891fc647242e61ca','3f3c2b324ede819496ddd7f93bd7e5d2'],
 'same_dex_ON5_4d6':{'one_round_tie_probability':fv(p_tie),'prob_Feryn1_first_eventually':fv(P_Ffirst),'expected_tiebreak_rounds_until_nontie':fv(pref),'dice_domain':'4d6 per participating ON5 instance; tie reroll R26; chosen winner not ID'},
 'documented_individual_initiatives':indep_init,
 'counter_critical_collision':{'trigger_source':'Contra-atacar announced before incoming attack; if attack score DOES NOT EXCEED CA then eligible response','master_critical_rule':'valid positive critical auto-hit even when ordinary score below CA','unresolved':'whether counter triggers despite an auto-hit: numeric threshold and attack-hit status conflict; neither allowed nor forbidden without authority','VLAB':'R47 planned; DMG no writer, no R47 replay claimed'},
 'AOO_sequential':{'Feryn_DES':80,'Varok_DES':27,'Arveth_DES':23,'priority_order':'Feryn > Varok > Arveth if all eligible','R44_receipt':'Feryn and Varok normals admitted with equipped Luta, sequential damage, original lab replay; NOT repeated by DMG'},
 'adversarial_tests':['same DES do not sort by ID','ON5 tie dice 4d6 not 1d6','two simultaneous Reactions from different actors legal, not duplicate on same actor','no second strike on dead or movement completion (R46)','critical cannot be negated solely by CA, but counter trigger after auto-hit remains normative HOLD','no full fight initiative from Bronze unknown bonus'],
 'next':'Four-cycle scientific branch closed; next test: collect VLAB R47–R49 DEPOIS, if it appears, compare evidence against frozen C05 oracle; otherwise hold collision source and expand source-complete elemental/PA contracts.'}
write('C05_AOO_COUNTER_ORACLE.json',cycle4)
wh('C05_PSV.md','# C05 — Reações concorrentes e VLAB\n\n**VERIFICADO R43–R46 (relatórios Notion):** maior DES primeiro em AoO concorrente (Mestre); igual DES disputa no dado competente; ON5 utiliza 4d6 e R26 rerrola somente empatados. As janelas reais de Feryn e Varok já provaram Luta do ataque NORMAL sem importar +6 exclusivo da Cabra/Frígido. R45 original com declaração tardia foi QUARENTENADO; R45B corrigiu a causalidade; R46 não publicou segundo golpe depois de uma morte. Não são combates completos.\n\n**Experimento matemático novo:** entre duas instâncias ON5 idênticas de DES80, probabilidade exata de empate no primeiro 4d6 de prioridade e quantidade média de disputas estão no oráculo JSON; nunca usar d6 universal ou ordenação de ID. Iniciativas documentadas Feryn4d6+82, Varok4d6+29, Arveth4d6+25 resolvem parte das prioridades entre espécies distintas, em especial Feryn sempre antes de Varok.\n\n**COLISÃO normativa ainda genuína:** Contra-atacar exige ataque recebido de score <=CA, enquanto crítico Mestre R41 é acerto automático mesmo com score baixo. A declaração ocorre antes dos dados. Não equiparar o score baixo a erro em hit crítico e nem publicar contra sem regra de precedência. O VLAB R47–R49 possui REGISTRO ANTES; DMG prepara oráculo, não executa.\n')

# independent cold reproducibility checks without running any VLAB engine or revising history
assert hashlib.sha256((old/'C01_NEW_SOURCE_LEDGER.json').read_bytes()).hexdigest()==old_hashes['C01_NEW_SOURCE_LEDGER.json']
assert P==Q(1,108) and pcommon(actors['Varok'],actors['Feryn']['CA'])==Q(1,1296)
assert pcommon(actors['Feryn'],actors['Varok']['CA'])==Q(1)
assert pcommon(actors['Varok'],actors['Feryn']['evade'])==0
assert all(q>=0 for q in [p_tie,1-p_tie])
assert all(hashlib.sha256((old/name).read_bytes()).hexdigest()==digest for name,digest in old_hashes.items())

checkpoint={'operation':'OP-DMG-CORPUS-EMP-01','checkpoint':'POST-R10-C02-C05','cycles_completed':4,'all_in_same_operation':True,
 'before':'POST-R10-C01; source identities unresolved; no complete Luta for two skills; VLAB R42 known at C01',
 'after':'C02-source lineage/nature; C03-source-equipped ON5 contrast; C04-PA budget; C05-AoO/counter bridge and initiative numbers',
 'canonical_writes':0,'VLAB_new_combat_runs_DMGSIDE':0,'baseline':'DMG-RANK-01 v1.1 untouched',
 'F0':'4/8 historical; no terminal new credit','L003':'0/71 individual authed as of inherited checkpoint','VLAB_terminal':'0/17','VLAB_canonical_cells':'0/1875',
 'old_hashes':old_hashes,'new_artifacts':{},'master_only':True,'gate':'NAC-PASS productive HOLD'}
write('C02_C05_CHECKPOINT.json',checkpoint)
for name in ['C02_SOURCE_ADMISSION.json','C02_PSV.md','C03_EQUIPPED_ON5_EXACT.json','C03_PSV.md','C04_PA_ACTION_BUDGET.json','C04_PSV.md','C05_AOO_COUNTER_ORACLE.json','C05_PSV.md']:
 checkpoint['new_artifacts'][name]=hashlib.sha256((root/name).read_bytes()).hexdigest()
write('C02_C05_CHECKPOINT.json',checkpoint)
print(json.dumps({'cycles':4,'C03_case_snapshot':{k:{'pcommon':v['p_common_if_no_critical']['approx'],'expected':v['E_net_per_attempt']['approx'],'E_n':v['model_expected_attacks_to_defeat_single_stationary_target']} for k,v in cases.items()},'C04':{x:{'mean_extra':v['mean_extra_raw_dice_if_activation']['approx'],'extra_per_PA':v['gross_dice_mean_per_PA_spent']['approx']} for x,v in boosts.items()},'C05_tie':float(p_tie),'artifacts':len(checkpoint['new_artifacts'])},ensure_ascii=False,indent=2))
