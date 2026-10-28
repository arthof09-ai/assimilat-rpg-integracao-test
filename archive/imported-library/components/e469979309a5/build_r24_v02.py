#!/usr/bin/env python3
"""Add noncanonical stronger Jaku+Manoplas+Blue Dragon source case to archived R24 v01."""
from pathlib import Path
from itertools import product
from fractions import Fraction
import json
D=Path(__file__).parent

def write(name,v): (D/name).write_text(json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf8')
def mean(n,sides):return float(Fraction(sum(sum(v) for v in product(range(1,sides+1),repeat=n)),sides**n))

s={
 'JAKU_NADTA_MASTER':{'id':'07dc2b32-4ede-82ae-b275-01f9414bfc81','url':'https://app.notion.com/p/07dc2b324ede82aeb27501f9414bfc81','asof':'2026-09-30T04:36:35.745Z','evidence_class':'MASTER_SOURCE_DOCUMENT_NOT_SCENE','claims_verified':['same inventory contains Lança (Certeira, Cruel, Infusão Espiritual), base weapon 2d8+2 and +2 attack','in same equipment inventory Manoplas da Fúria Flamejante description includes +1d8+2 fire extra damage per melee hit','additional embedded weapon infusion reads +2d8+2 dano espiritual flamejante; separate rider not authorized to stack without review','ability Estocada Cruel is for melee perforating weapons; spear attack tag still requires exact source effective_at','ficha contains P3 and P4 forms, no duplicate owned set'], 'gates_pending':['current alive and available actor epoch','actual gloves equipped, charge, action, resource and timed effect','damage physical tag explicitly certified for actual spear attack','whether +2d8+2 spiritual flame infusion is automatic and stacks, or replaces pool']},
 'MANOPLAS_CATALOG':{'id':'592c2b32-4ede-8385-b926-013aac7146ca','url':'https://app.notion.com/p/592c2b324ede8385b926013aac7146ca','asof':'2026-09-30T04:45:48.615Z','evidence_class':'MESTRE_SIDE_CATALOG_DOCUMENT','claims_verified':['nonmagical weapon held in these gloves is treated as magical','as bonus action, magical fire envelops 1 or 2 melee weapons within reach','each flaming weapon causes +1d8+2 extra fire damage per hit','flames until the bearer drops or releases a weapon; once used, ability refreshes next dawn; 13 PA per day'], 'gates_pending':['current action economy says Standard, Movement, Reaction, Free but item says bonus action — not automatically resolved','13 PA per day must be reconciled with PA Livre and scene epoch','ownership and equipped status at combat time']},
 'BLUE_DRAGON':{'id':'4fac2b32-4ede-824d-a70d-0189f19533de','url':'https://app.notion.com/p/4fac2b324ede824da70d0189f19533de','asof':'2026-09-30T04:43:29.920Z','evidence_class':'MASTER_SIDE_BEAST_FICHE','claims_verified':['Ouro 1; Vida 523; CA 39','Vulnerabilidade a Fogo: Sofre dano extra de ataques mágicos baseados em fogo'], 'gates_pending':['active weakness in real scene','physical and fire resistance, RD and rounding','target current Vida, reaction, status and range at scene epoch']},
 'COMBAT':{'id':'3ebc2b32-4ede-81f1-be4b-e8804ac113c0','url':'https://app.notion.com/p/3ebc2b324ede81f1be4be8804ac113c0','asof':'2026-10-07T23:51:04.971Z','evidence_class':'CURRENT_RULE','claims_verified':['weakness adds +3 rolls of largest applicable elemental die and preserves physical pool','a character ordinarily has Standard, Movement, Reaction, Free actions; item bonus action translation requires authority'], 'gates_pending':[]}
}
# Deterministic script-only rolls are NEVER source/event dice.
physical=[5,3];fire=[6];bonus=[3,7,4]
base_weapon=sum(physical)+2
base_fire=sum(fire)+2
bonus_fire=sum(bonus)
assert (base_weapon,base_fire,bonus_fire)==(10,8,14)
expected_no=mean(2,8)+2+mean(1,8)+2
expected_yes=expected_no+mean(3,8)
assay={
 'status':'CONDITIONAL_SANDBOX_ONLY_NOT_REAL_EVENT_NOT_STRICT',
 'preferred_candidate':'JAKU_NADTA_MASTER+MANOPLAS_CATALOG vs BLUE_DRAGON',
 'reason_preferred_over_v01':'One existing actor fiche shows both the weapon and the Fire-extra item physically listed in the same inventory; no known title-Morto collision; the item explicitly says Fogo and weapon magic, unlike ambiguous Ong stacking. Still no certified actor status or event.',
 'source_components':['Lança 2d8+2 [physical source type not formally specified]','Manoplas +1d8+2 extra Fogo per melee hit','Fraqueza +3d8 Fogo only if actual melee hit is qualified as magical Fire against this beast'],
 'synthetic_rolls':{'weapon_2d8':physical,'manoplas_fire_1d8':fire,'bonus_fire_3d8':bonus},
 'conditional_gross':{'weapon':base_weapon,'fire':base_fire,'extra_fire':bonus_fire,'without_weakness':base_weapon+base_fire,'with_weakness':base_weapon+base_fire+bonus_fire,'delta_only_fire':bonus_fire},
 'exact_expectation':{'without_weakness':expected_no,'with_weakness':expected_yes,'delta':mean(3,8)},
 'separate_wpn_rider_unknown':'+2d8+2 dano espiritual flamejante — NOT INCLUDED IN ASSAY; do not silently remove from real attack if active',
 'specific_unsatisfied':['No historical physical attack event, no signed actor alive/available at epoch','Bonus action interface is not expressly mapped in current turn economy','Gloves effect activation, time, PA, and charge have no event record','Spear physical type and extra spiritual/flaming rider interaction remain source-gated','Dragon vulnerability says magical Fire; verify composite attack action as magical Fire','No attack hit receipt, actual dice, physical/fire mitigation/rounding, HP before/after, commit, replay, independent NAC-PASS'],
 'nonstack_controls':['Do not combine +2d8+2 weapon infusion into fixture without its own legal source gate','Do not double count repeated P3/P4 equipment','Without magic fire qualification on Dragon, no +3d8','No real event => B15 stays PARTIAL'],
 'actual_result':{'real_events':0,'net_damage':'UNKNOWN','hp_after':'UNKNOWN','strict_full_fight':False,'B15_PASS':False}
}
write('R24_V02_JAKU_B15_EVIDENCE.json',{'version':'R24-v02','sources':s,'assay':assay,'provenance_limit':'Notion textual readback, not binary Notion page SHA or battle evidence','new_source_pages_count':2,'real_events_count':0,'B15':'PARTIAL','notion_writes':0,'decisions_master':'0/5 pending','certifications':{'certified':1,'denominator':18},'i0003':[0,9],'strict':[0,2]})
report='''# R24-v02 — Fonte mais adequada para ensaio B15: Jaku Nadta

**Origem da melhoria:** após fechar R24-v01, foi encontrada uma combinação de arma e item NO MESMO INVENTÁRIO de uma ficha Mestre. R24-v01 permanece aninhado byte-idêntico.

## Novas fontes do Notion reabertas

- [Jaku Nadta — ficha Mestre](https://app.notion.com/p/07dc2b324ede82aeb27501f9414bfc81), as-of 2026-09-30T04:36:35.745Z: lança `2d8+2`, e Manoplas da Fúria Flamejante NO MESMO INVENTÁRIO; a mesma lança também mostra infusão espiritual flamejante `+2d8+2`, que deve ser conciliada, não apagada arbitrariamente.
- [Manoplas da Fúria Flamejante — ficha do item](https://app.notion.com/p/592c2b324ede8385b926013aac7146ca), as-of 2026-09-30T04:45:48.615Z: cada arma sob chamas causa `+1d8+2` **de Fogo extra em um golpe**; armas não mágicas agarradas pela manopla são tratadas como mágicas; exige `ação bônus`, chamas até baixar/soltar arma, custo `13 PA por dia`.
- [Dragão de Gelo Azul — besta](https://app.notion.com/p/4fac2b324ede824da70d0189f19533de): vulnerável a **ataques mágicos de Fogo**, Ouro 1, Vida 523, CA39.

## Exemplo de ensaio condicionado, NUNCA evento real

Se o golpe com a lança **legalmente** mantém pool físico `2d8+2`, se as manoplas estão ativas e concedem `+1d8+2` de Fogo, e se essa instância conta como *ataque mágico de Fogo* perante o Dragão, o Sistema de Combate dá `+3d8 de Fogo` somente no pool elemental.

Rolagens manuais do ensaio, NÃO dados de combate: lança `[5,3]`+2=10; Fogo da manopla `[6]`+2=8; fraqueza Fogo `[3,7,4]`=14. Total bruto hipotético sem fraqueza=18; com fraqueza=32; delta +14 somente no componente Fogo. Médias exatas do modelo condicional: **17,5** sem fraqueza, **31,0** com fraqueza, delta **13,5**.

**Falhas de gate que permanecem:** disponibilidade viva de Jaku no epoch da cena, arma e manoplas equipadas, ativação já realizada (`ação bônus` legado não reconciliada automaticamente com economia atual), PA e janela de ação, natureza física da lança, regra e stacking da infusão espiritual flamejante `+2d8+2`, dano efetivamente mágico Fogo, RD/mitigação e reações do Dragão, rolagem real de acerto/dano, HP antes/depois, recibo de commit e readback independente.

**Comparação com R24-v01:** Jaku é candidata preferida porque a ficha mostra posse simultânea dos dois objetos e a manopla declara expressamente `Fogo extra`; Ong tinha possível `Morto` em espelho Party e concatenação menos clara. A melhoria é documental, não evento: certificado **1/18**, B15 **PARTIAL**, STRICT **0/2**, CSV **0/9**, decisões Mestre **0/5**.

## Próxima execução legítima

Pedir ao operador autorizado (CM-000006) que confirme as interfaces e o estado de cena antes de qualquer evento; observar NAC-CONT-03, NAC-NORM-01, NAC-PASS e autorização expressa. Se o campo `ação bônus` ou stacking físico/espiritual/Fogo não tiver interpretação vigente, não improvisar decisão; escolher outra ação completamente fonte-gated, não alterar regra. O episódio precisa de id, epoch, mapa, PA, acerto, rolagens reais, dano por tag, RD, HP/Alma antes/depois, commit único, readback e auditoria. Nenhum dos testes locais fornece esse evento.
'''
(D/'R24_V02_PREFERENCIA_B15.md').write_text(report,encoding='utf8')
(D/'HANDOFF_R24_V02.md').write_text('''# Continuidade R24-v02 → R25

Abrir `R24_V02_PREFERENCIA_B15.md` e `R24_V02_JAKU_B15_EVIDENCE.json`; preservar `R24_V01_ORIGINAL_READONLY.zip` e R23 aninhado. **Prioridade B15 = Jaku Nadta (lança 2d8+2, manoplas Fogo extra 1d8+2), vs Dragão de Gelo Azul**: resolver 1) ator e equipamento no epoch, 2) `ação bônus` em economia oficial, 3) se a lança mantém pool físico e como integra `+2d8+2 espiritual flamejante`, 4) status mágico Fogo ante fraqueza do Dragão, 5) RD/mitigação e combate efetivo com operador CM-000006. O ensaio condicionado foi 18/32 brutos, nunca cena. Ong R24-v01 continua alternativa documental com risco `(Morto)` no espelho, sem ressurreição implícita. DEC-B11-A/B/C e DEC-B12-A/B pendentes do Mestre. B02 1/18; B15 PARTIAL; B04 BLOCKED; B09 PARTIAL; 0/2 STRICT; 0/9 CSV; NAC-PASS terminal HOLD; Notion writes 0 e Diário sync pending gate. Não reabrir buscas I0003 sem locator novo nem alterar VLAB/Party/Primeiro.\n''',encoding='utf8')
print(json.dumps({'R24_V02_BUILD':'PASS','case':'JAKU_MANOPLAS_DRAGON','rolls':[18,32],'expected':[17.5,31],'certified':'1/18','master_choices':0}))
