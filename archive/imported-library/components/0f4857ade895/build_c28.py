#!/usr/bin/env python3
"""C28 — reproducible exact conditional arithmetic and documentary-diagnostic datasets.
Never mutates Notion, Party, O Primeiro, VLAB or canonical rules.
"""
import os,csv,json,hashlib,math
from collections import Counter
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'publication';OUT.mkdir(parents=True,exist_ok=True)
# Literal source identifiers and mechanical portions read directly on 2026-10-21 in Mestre Notion.
SOURCES=[
('O01','Manopla do Trovão Cativo','3f5c2b324ede81f5ac62fb940204cdac','2026-10-11T10:48:42.335Z','equipamento','Ouro','Entrada','RI+FIP item','Descarga ofensiva','5d8+3','Raio','ADDITIONAL_AFTER_CONFIRMED_HIT','22 PA','1 por descanso 8h','condiciona -3 m se >0 dano Raio','not individually certified'),
('O02','Lâmina da Queda Contida','3f5c2b324ede81e9aa8ec51f568600e8','2026-10-11T10:48:44.164Z','arma','Ouro Negro','Entrada','RI+FIP item','Ataque básico','7d8+15','Cortante','STANDARD_ACTION_ON_HIT','0 PA especificado','ataque padrão','ancoragem defensiva 18 PA reação 1/8h','not individually certified'),
('O03','Martelo do Portão Faminto','3f5c2b324ede81658982d8f47b3ad647','2026-10-10T18:39:05.841Z','arma','Ouro Negro','Média','RI+FIP item','Ataque comum','8d10+12','Impacto/Contundente','STANDARD_ACTION_ON_HIT','0 PA especificado','ataque padrão','duas mãos, requer acerto','not individually certified'),
('O04','Martelo do Portão Faminto','3f5c2b324ede81658982d8f47b3ad647','2026-10-10T18:39:05.841Z','arma','Ouro Negro','Média','RI+FIP item','Destruidor de barreiras (incremento)','6d8','Impacto/Contundente','ONLY_NONLIVING_STRUCTURE_ALREADY_HIT','25 PA','1 por descanso 8h','somar uma vez ao ataque comum contra estrutura','not individually certified'),
('O05','Selo do Último Refúgio','3f5c2b324ede81d0874ed4d96752812c','2026-10-10T18:38:13.784Z','consumível defensivo','Lendário','Entrada','RI+FIP item','Absorção','cap_60','Proteção Vida','REACTION_ON_SINGLE_EVENT','55 PA','uso único','até 3 alvos MESMA ocorrência depois da RDF','not an offensive RE'),
('O06','Anel do Último Marco','3f5c2b324ede81ceabf6fc2b97344e43','2026-10-10T18:37:42.475Z','mobilidade','Ouro Negro','Baixa','RI+FIP item','Marcação/Retorno','NO_DAMAGE','Espaço','STANDARD_8PA_then_REACTION_28PA','8+28 PA','1 retorno por 8h; marca dura 10min','não cancela ataque se ponto de retorno ainda dentro da área','not an offensive RE'),
('O07','Pó da Brasa Clara','3f5c2b324ede8145a12febac8558aeb8','2026-10-10T18:37:48.975Z','consumível climático','Prata','Entrada','RI+FIP item','Mitigação ambiental','cap_12','Frio ambiental','STANDARD_TO_APPLY','uma dose, 0 PA','3 doses, 30min cada','não protege contra magia de Gelo direcionada','not an offensive RE'),
('O08','Estandarte do Trono Desfeito','3f5c2b324ede816a9683e0ad40bad4b3','2026-10-11T10:48:48.028Z','suporte','Lendário','Entrada','RI+FIP item','Proteção mental','NO_DAMAGE','Mental','CONDITIONAL','na fonte','na fonte','controle negativo, suporte','not an offensive RE'),
('O09','Véu do Rastro Apagado','3f5c2b324ede81bab332f518b2e6a211','2026-10-11T10:48:45.877Z','ocultação','Ouro Negro','Entrada','RI+FIP item','Ocultação de vestígios','NO_DAMAGE','Utilidade','CONDITIONAL','na fonte','na fonte','controle negativo, ocultação','not an offensive RE'),
('O10','Adaga da Serpente Enfeitiçada','3edc2b324ede811787a0de913622b14d','2026-10-03T04:47:17.045Z','arma','Ouro Negro','UNKNOWN','RI item, FIP não documentada','Dano direto','5d4+5d8+10','UNKNOWN','DELIVERY_UNSPECIFIED','35 PA sem verbo claro','na fonte','veneno condicionado salvaguarda CON CD25','not individually certified'),
('O11','Adaga da Serpente Enfeitiçada','3edc2b324ede811787a0de913622b14d','2026-10-03T04:47:17.045Z','arma','Ouro Negro','UNKNOWN','RI item, FIP não documentada','Veneno por turno','3d12','Veneno','PER_TICK_ON_FAILED_CON_SAVE_CD25','35 PA ambíguos','duração não documentada','não somar duração presumida','not individually certified'),
('O12','Cajado do Eclipse Lunar','1cdc2b324ede82ed892f815f21f79ac1','2026-10-09T04:37:20.771Z','cajado','UNKNOWN','UNKNOWN','sem RI/FIP no texto consultado','Drenagem passiva','7d8','Necrótico+PV','PASSIVE_ON_ATTACK','na fonte','na fonte','dano adicionado ao ataque, PV curado pelo resultado','not individually certified'),
('O13','Cajado do Eclipse Lunar','1cdc2b324ede82ed892f815f21f79ac1','2026-10-09T04:37:20.771Z','cajado','UNKNOWN','UNKNOWN','sem RI/FIP no texto consultado','Lua de Sangue — dano inimigos','20d8','Necrótico','AREA_6M_PER_TICK','na fonte','2/dia; 3 rodadas','somente inimigos presentes/expostos','not individually certified'),
('O14','Cajado do Eclipse Lunar','1cdc2b324ede82ed892f815f21f79ac1','2026-10-09T04:37:20.771Z','cajado','UNKNOWN','UNKNOWN','sem RI/FIP no texto consultado','Lua de Sangue — cura aliados','16d8','Cura PV','AREA_6M_PER_TICK','na fonte','2/dia; 3 rodadas','não é dano ofensivo','not an offensive RE'),
('O15','Cajado do Eclipse Lunar','1cdc2b324ede82ed892f815f21f79ac1','2026-10-09T04:37:20.771Z','cajado','UNKNOWN','UNKNOWN','sem RI/FIP no texto consultado','Toque Vampírico','20d8','PV drenado','MELEE','na fonte','3/dia','dreno e cura do mesmo montante','not individually certified'),
('O16','Cajado do Eclipse Lunar','1cdc2b324ede82ed892f815f21f79ac1','2026-10-09T04:37:20.771Z','cajado','UNKNOWN','UNKNOWN','sem RI/FIP no texto consultado','Ritual da Noite bônus','28d10','Necrótico','MIDNIGHT_CONDITIONAL','na fonte','passivo meia-noite','sem duplicar dano-base que é maximizado','not individually certified'),
('O17','Espada do Lendário','3edc2b324ede81ab9e22e168f6d939a9','2026-10-04T02:03:41.273Z','arma degradada','Lendário','Ápice','RI+FIP analítico item','Dano da arma','14d20+14d12+14d8+14d10+390+FOR','UNKNOWN','STANDARD_HIT_UNSPECIFIED','600 PA/dia','deteriorada, 1–2 usos provável não fechado','FOR e +60 FOR requerem interpretação específica','not individually certified'),
('O18','Arco Exterminador Elemental','3edc2b324ede8156849bf1aae0ce9fb5','2026-10-03T13:15:40.242Z','arma','Lendário','UNKNOWN','RI item','Dano de base','8d8+25','UNKNOWN','ATTACK','64 PA/dia','na fonte','bônus contra elementais em linha separada','not individually certified'),
('O19','Arco Exterminador Elemental','3edc2b324ede8156849bf1aae0ce9fb5','2026-10-03T13:15:40.242Z','arma','Lendário','UNKNOWN','RI item','Bônus anti-elementais','8d12+10','UNKNOWN','ONLY_ELEMENTALS','64 PA/dia','na fonte','não presumir todos alvos elementais','not individually certified'),
]
with open(OUT/'C28_PRIMARY_EFFECT_CONTRACTS.csv','w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['effect_id','item_name','notion_page_id','source_last_edited_at','object_class','RI','FIP_item','authority_scope','effect_name','literal','nature','delivery','resource','frequency','restriction','RE_effect_certification']);w.writerows(SOURCES)

# Exact convolution with integer counts and rational expectations.
def pmf(expr):
 # Only strictly positive integer dice and fixed numeric constants here. External FOR excluded.
 import re
 t=expr.upper().replace(' ','').replace('+FOR','')
 dice=list(re.finditer(r'(\d+)D(\d+)',t));constant_part=re.sub(r'\d+D\d+','',t)
 constant=sum(int(x) for x in re.findall(r'\+?(\d+)',constant_part)) if constant_part else 0
 counts={0:1}
 for m in dice:
  n,faces=map(int,m.groups())
  for i in range(n):
   nxt={}
   for subtotal,ct in counts.items():
    for face in range(1,faces+1):nxt[subtotal+face]=nxt.get(subtotal+face,0)+ct
   counts=nxt
 return {k+constant:v for k,v in counts.items()}

def asfloat(x): return float(x)
def expec(dist,f=lambda d:d):
 den=sum(dist.values());return Fraction(sum(ct*f(d) for d,ct in dist.items()),den)
def prob(dist,f):
 den=sum(dist.values());return Fraction(sum(ct for d,ct in dist.items() if f(d)),den)
def stats(expr):
 p=pmf(expr);return {'min':min(p),'max':max(p),'mean':float(expec(p)),'support':len(p)}

# RI band diagnostic only; NOT claim of RE certification.
BANDS={'Bronze':{'Entrada':(4,6),'Baixa':(7,9),'Média':(10,12),'Alta':(13,15),'Ápice':(16,18)},
'Prata':{'Entrada':(14,18),'Baixa':(19,22),'Média':(23,26),'Alta':(27,31),'Ápice':(32,36)},
'Ouro':{'Entrada':(22,28),'Baixa':(29,35),'Média':(36,44),'Alta':(45,52),'Ápice':(53,62)},
'Ouro Negro':{'Entrada':(38,48),'Baixa':(49,58),'Média':(59,69),'Alta':(70,82),'Ápice':(83,96)},
'Lendário':{'Entrada':(58,72),'Baixa':(73,90),'Média':(91,112),'Alta':(113,136),'Ápice':(137,160)}}
PROXY=[('O01','5d8+3','Ouro','Entrada','added after prior confirmed hit; not standalone attack'),('O02','7d8+15','Ouro Negro','Entrada','normal attack plus defensive rider'),('O03','8d10+12','Ouro Negro','Média','general baseline; structural niche excluded'),('O04','8d10+12+6d8','Ouro Negro','Média','structure-only burst; 25PA 1/8h'),('O17','14d20+14d12+14d8+14d10+390','Lendário','Ápice','unique deteriorated historical outlier; FOR excluded')]
rows=[]
for id,expr,rank,fip,context in PROXY:
 s=stats(expr);lo,hi=BANDS[rank][fip];other=next((k for k,(a,b) in BANDS[rank].items() if a<=s['mean']<=b),'OUTSIDE_OPERATIONAL')
 rows.append([id,expr,rank,fip,lo,hi,s['mean'],s['min'],s['max'],other,round(s['mean']-lo,5),round(s['mean']-hi,5),context,'DIAGNOSTIC_RI_FIP_PROXY_NOT_RE'])
with open(OUT/'C28_RI_FIP_NONAUTHORITATIVE_PROXY.csv','w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['effect_id','expression','RI','FIP_item','band_min','band_max','dme_intrinsic','support_min','support_max','literal_dme_position_in_RI_band','dme_minus_lower','dme_minus_upper','context','status']);w.writerows(rows)

# Two real physical attacks vs 4 actual physical resistance defenders + 0 control, with/without one-use Selo post-resistance.
DEFENDERS=[('NONE','none',0),('Rinolupo Prata1','034c2b324ede83ffa7118144011beaf3',10),('Guardião Pétreo Prata3','549c2b324ede8375b21181335038aad1',15),('Guardião Pétreo Ouro1','b0ec2b324ede835a927601b4cbd8fca6',20),('Guardião Pétreo Ouro5','371c2b324ede837fad4c01bbfe9a95fb',25)]
attacks=[('O02','7d8+15'),('O03','8d10+12')];defense=[]
for id,expr in attacks:
 p=pmf(expr)
 for name,source,rd in DEFENDERS:
  before=expec(p,lambda x:max(0,x-rd));after=expec(p,lambda x:max(0,x-rd-60));saved=before-after
  chance=prob(p,lambda x:max(0,x-rd-60)>0)
  defense.append([id,expr,name,source,rd,float(before),float(after),float(saved),float(chance),str(before),str(after),str(saved),str(chance),min(max(0,x-rd) for x in p),max(max(0,x-rd) for x in p),'one hit already confirmed; physical RDF applied first; Selo one event only'])
with open(OUT/'C28_PHYSICAL_RDF_SELO_10_CONDITIONAL_FIXTURES.csv','w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['effect_id','attack_expr','defender','source_page_id','RDF','mean_before_seal','mean_after_seal','mean_prevented','prob_residual_positive','before_fraction','after_fraction','prevented_fraction','residual_prob_fraction','postRDF_min','postRDF_max','contract']);w.writerows(defense)

# Manopla's electric component vs hypothetical electricity protection, not physical RDF; trigger rider only if damage passes.
resist=[];p=pmf('5d8+3')
for r in [0,10,20,25,30,35,40,43]:
 avg=expec(p,lambda x:max(0,x-r));chance=prob(p,lambda x:x>r)
 resist.append([r,float(avg),float(chance),str(avg),str(chance),'pure hypothetical Raio mitigation; not a documented defender; conditional on confirmed prior attack; no independent hit'])
with open(OUT/'C28_MANOPLA_ELECTRIC_RESISTANCE_THRESHOLDS.csv','w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['hypothetical_Raio_resistance','mean_electric_after','conditional_probability_slow3m','exact_mean_fraction','exact_probability_fraction','caveat']);w.writerows(resist)

# Parsed expression baseline and source literality: no fabricated extra attacks/ticks.
CAND=[('O10','5d4+5d8+10','one base attack, timing unknown'),('O11','3d12','per poison tick after failed CON CD25, duration unknown'),('O12','7d8','passive increment per actual attacking event'),('O13','20d8','one enemy in blood moon, per exposed round up to 3; not guaranteed'),('O14','16d8','one ally PV healed per exposed round up to3'),('O15','20d8','melee siphon 3/day, ability action unspecified'),('O16','28d10','midnight ritual increment on qualifying spell'),('O18','8d8+25','bow base'),('O19','8d12+10','elemental-target specialized addition')]
r2=[]
for id,expr,context in CAND:
 s=stats(expr);r2.append([id,expr,s['min'],s['max'],s['mean'],context,'RE_effect=UNVERIFIED'])
with open(OUT/'C28_LEGACY_MULTIEFFECT_DECOMPOSITION.csv','w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['effect_id','formula','min','max','mean','condition','classification']);w.writerows(r2)

# Discrete tick counts are exposure scenarios, not observed results. Do not multiply by enemies or days.
ticks=[]
for tick_count in [0,1,2,3]:
 for expr,kind in [('20d8','enemy_dmg'),('16d8','ally_heal')]:
  avg=stats(expr)['mean']*tick_count
  ticks.append([kind,tick_count,avg,'CONDITIONAL: that same target remains in effect, one instance, no deaths/immunities; not DPT guaranteed'])
with open(OUT/'C28_ECLIPSE_ONE_TARGET_EXPOSURE_SCENARIOS.csv','w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['outcome','exposed_rounds','total_expected_conditional','caveat']);w.writerows(ticks)

# Assertions as independent documented fixture values + invariants, not false independent human documentary review.
checks=[]
def test(name,value,expected):
 if value!=expected:raise AssertionError(f'{name}: {value} != {expected}')
 checks.append({'test':name,'pass':True,'value':str(value),'expected':str(expected)})
for expr,mn,mx,avg in [('5d8+3',8,43,Fraction(51,2)),('7d8+15',22,71,Fraction(93,2)),('8d10+12',20,92,Fraction(56)),('6d8',6,48,Fraction(27)),('5d4+5d8+10',20,70,Fraction(45)),('20d8',20,160,Fraction(90)),('16d8',16,128,Fraction(72)),('28d10',28,280,Fraction(154)),('8d8+25',33,89,Fraction(61))]:
 p=pmf(expr);test(expr+' min',min(p),mn);test(expr+' max',max(p),mx);test(expr+' mean',expec(p),avg);test(expr+' outcomes',sum(p.values()),math.prod(int(b)**int(a) for a,b in __import__('re').findall(r'(\d+)d(\d+)',expr)))
# The big sword expected mean and extremes without materializing enormous joint sample space.
test('Sword DME',14*Fraction(21,2)+14*Fraction(13,2)+14*Fraction(9,2)+14*Fraction(11,2)+390,Fraction(768))
test('Sword min',14+14+14+14+390,446)
test('Sword max',14*20+14*12+14*8+14*10+390,1090)
for id,ex in attacks:
 p=pmf(ex)
 for name,src,rd in DEFENDERS:
  a=expec(p,lambda x:max(0,x-rd));b=expec(p,lambda x:max(0,x-rd-60))
  test(f'nonnegative {id} {rd}',b>=0,True)
  test(f'seal not increases {id} {rd}',b<=a,True)
  test(f'prevent bounded 60 {id} {rd}',a-b<=60,True)
for a in resist:
 test(f'Raio chance in range {a[0]}',0<=a[2]<=1,True)
test('Selo sword not full event automatic',len(defense),10)
test('C28 source count',len(SOURCES),19)
test('C28 proxy count',len(rows),5)
# Exact gold vs ON thresholds, no 'RE inferred' status.
test('Blade ON Entrada DME',expec(pmf('7d8+15')),Fraction(93,2))
test('Hammer ON Média DME baseline',expec(pmf('8d10+12')),Fraction(56))
test('Hammer structure conditional DME',expec(pmf('8d10+12+6d8')),Fraction(83))
with open(OUT/'C28_MATH_ASSERTIONS.json','w',encoding='utf-8') as f:json.dump({'n':len(checks),'all_pass':True,'tests':checks},f,ensure_ascii=False,indent=2)

# Hypotheses and counterfactuals.
H=[
('H1','Item FIP implies identical RE for every attack','CONTRADICTED_AS_GENERAL_RULE','Selo/Anel rank by defense/space; hammer regular and demolition have separate effects','RE remains UNVERIFIED for all offensive effects'),
('H2','General attack and special anti-structure burst can be compared as same target','REFUTED_BY_CONTRACT','hammer +6d8 only nonliving structures','no unauthorized creature benchmark'),
('H3','Expected post-RDF+Selo = max(0,DME-RDF-60)','FALSE_AT_THRESHOLDS','exact convolution shows Jensen threshold cases for martelo/blade','use full discrete distributions'),
('H4','Manopla slow always triggers once a hit lands','REFUTED_BY_CONTRACT','source requires >=1 electric damage after resistance','conditional hit and electric resistance independent of physical RDF'),
('H5','Cajado area effect grants three guaranteed damage ticks per enemy','REFUTED_BY_CONTRACT','source says up to3 rounds, individual survival/exposure unknown','1/2/3 rounds scenario only'),
('H6','Martelo has inconsistent documented FIP because baseline DME56 below 59','NOT_ESTABLISHED','item FIP includes special structural burst 83 and cost/target restrictions','do not edit item or norm'),
('H7','The unusual Sword 768 requires moving Legendary median upward','REFUTED_AS_CALIBRATION_METHOD','norm already identifies unique artifacts/stacked bonuses as outliers','retain exceptional stratum')]
with open(OUT/'C28_HYPOTHESIS_RECONCILIATION.csv','w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['ID','hypothesis','result','evidence','limitation']);w.writerows(H)
# Machine-readable summary, exact denominators.
summary={'cycle':'C28','baseline':'C27','source_effect_rows':len(SOURCES),'unique_primary_pages':len(set(x[2] for x in SOURCES)),'RI_FIP_proxy_rows':len(rows),'certified_individual_RE_new':0,'physicalRDF_seal_condition_cells':len(defense),'electrical_hypothetical_resistance_cells':len(resist),'legacy_numeric_effects':len(CAND),'exposure_scenarios':len(ticks),'checks':len(checks),'F0':'4/8 HOLD','A5_original_bytes':'0/7 authenticated','DMG_RANK':'v1.1 UNCHANGED','production':'HOLD','Party_O_Primeiro':'NO_WRITE'}
with open(OUT/'C28_DENOMINATOR_MANIFEST.json','w',encoding='utf-8') as f:json.dump(summary,f,ensure_ascii=False,indent=2)
print(json.dumps(summary,ensure_ascii=False))
