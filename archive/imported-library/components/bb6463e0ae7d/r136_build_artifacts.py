"""R136 scientific inventory and continuity, fixed 17-contract denominator.
Artifact generation only: no historical combat reruns, no Notion/Party write.
"""
from pathlib import Path
import json,csv,hashlib,sqlite3,difflib
ROOT=Path(__file__).resolve().parent
BASE=Path('/mnt/data/vlab_r126_work/r118_r125')

sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
arr=json.loads((BASE/'R125_17_CONTRACTS_BEFORE_AFTER.json').read_text())
assert arr['fixed_denominator']==17 and len(arr['rows'])==17
up={
 'ACTION_CATALOG_AIN01':('R126: Capa de Poeira 35PA como Reação e Marca dos Passos Perdidos 25PA como Padrão; R132: Reconstituição de Seiva 75PA como Cura, integrada no módulo v0.8.1.','Outras habilidades, efeitos de área, salvaguarda/reflexão completa, alcance não-condicional.'),
 'ACTOR_SNAPSHOT_SCENARIO':('R126: Auren e duas instâncias técnicas de Feryn; R132: Auren/Feryn/Eristan, três perfis fonte distintos, mas 2 NPCs são precreation Mestre-side.','Admissão oficial/materialidade das fichas, snapshot de cena canônica, recursos e itens reais.'),
 'AUTHORITATIVE_RULES_AND_ADAPTERS':('Regra 3 de oportunidade e afastamento seguro consultada diretamente; Regra 5 cancelamento Vantagem/Desvantagem em motor, falha crítica e stacking preservados HOLD.','Resolver precedência concorrente, dano misto, falha crítica, critérios de alcance e transformações sem conjectura.'),
 'BATTLE_1X1_2X1_20X20':('Três cenas com três atores e uma rodada de ataques/habilidades/PA/reação/posição/recuperação; R125 10×10 e 20×20 preservados.','Combates completos com all mechanics/rank, equipes não clonadas, 2×1 equivalente e 20×20 fonte completa.'),
 'BLEED_AND_HEAL_RESTRICTIONS':('R132 Eristan: cura nativa 8d10+25+luvas20, cap Vida máxima, 75 PA, 10 transações; R130 com perda de speed foi bloqueado pelo auditor e preservado.','Sangramento admitido por fonte de portador, restrição de cura de ferida real, ticks/resistências, gatilhos pós-morte e independência de fontes.'),
 'ED_VS_BE_DAMAGE':('Nenhuma nova execução ED×Besta foi iniciada: R126 usa dois NPCs ON5; R132 adiciona healer NPC.','Besta com iniciativa/documentação plena, efeitos, balanced ED, run completo e científica confiança.'),
 'GENERAL_SPECIFIC_RD':('R135: Dark RD60 de Auren testada isoladamente no resolvedor; físico geral35 isolado; empilhamento e duas tags explicitamente REJECT.','Ataque real Dark contra alvo com resistência, convenção stacking e distribuição de dano misto com auditor independente.'),
 'ITEM_EQUIPMENT_AND_ENHANCEMENTS':('R132: Luvas do Vaso da Vida equipadas de Eristan adicionaram +20 à cura direta, uma vez na conjuração; source item explicit.','Cargas e contratos de itens existentes, remoção/equipamento, custo comprometido e rollback sob ataque.'),
 'OFFICIAL_QA_NAC_LEDGERS':('Auditor frio sem engine 11+11+10 eventos; R135 9 negativas; R134 2 falhas de processo; R132 retest após detectar drift em R130.','Auditoria competente externa, gates B1/B2/B3/NAC-PASS; lacunas das outras funcionalidades.'),
 'PA_AND_PREBUFF_COSTS':('R126 dois gatilhos Capa 35PA; uma Marca 25PA; R132 uma Cura 75PA. 170 PA pagos em 3 cenas distintas, sem doppio commit; crash pago R134.','Manutenção temporal real, equipamentos ativos com reserva PA, habilidades adicionais, batida simultânea de ações/PA em full fight.'),
 'REACTION_TRIGGER_AND_SINGLE_USE':('R126 Capa pago antes do hit e debitado uma vez; AoO consumiu Reação e não ação padrão; afastar seguro negou AoO. R135 cancelamento Fraco/AoO.','Concorrência multi-inimigos, reações contra magias válidas, gatilho forçado sob decisão competente, encerramento integral.'),
 'RNG_REPLAY_STATISTICS':('R128 e R133 auditores stdlib independentes confrontaram RNG/estado/cadeia; R130 drift detectado e nova seed963212 corrigida.','Holdout verdadeiramente cego, famílias independentes, referências oficiais, estatística com censura.'),
 'SOURCE_FREEZE_AND_RANK':('Perfil Eristan ON5 com papel de curandeiro agora fonte reaberta e snapshot mecânico para teste (sem ED).','Perfis 25 A/B e 27 D homologados, autorização material, não confundir NPC proposta com official.'),
 'TACTICAL_AI_AB_FAIRNESS':('Políticas one-round fixas source-bounded separadas desenvolvimento/reserva; zero A/B causal de vitória.','IA real/holdout independente, justiça por posição/papéis/condições.'),
 'TRANSFORMATION_OVERLAY_AI08':('Auren não transformado; conflito 100PA+15/turno vs 320PA preservado.','Conciliação NAC-NORM, snapshot transformado admissível e demais overlays.'),
 'TRANSFORMATION_PER_SCENE_AI09':('Sem efeito de transformação executado; todas fontes e holds históricos retidos.','Cena, duração e recarga/descanso reais com autoridade.'),
 'TURN_SCHEDULER_EVENT_SOURCING':('R126 duas cenas 3 atores de 11 transações; R132 cenário 3 fontes de 10 transações; PA, AoO e cura atravessam scheduler R18/R26.','Cenas multirrodadas com habilidades e reação, morte real sem ambiguidade, concorrência e range completo.')}
assert {v['id'] for v in arr['rows']}==set(up)
rows=[]
for old in arr['rows']:
 a,b=up[old['id']]
 rows.append({'position':old['position'],'id':old['id'],
  'original_requirement_verbatim':old['original_requirement_verbatim'],
  'ANTES_R125':old['DEPOIS_R125'],
  'DEPOIS_R135':{'new_executed_evidence':a,'minimum_remaining':b,'terminal_certified':False,
    'independent_audit':'LOCAL COLD auditor for selected scenes; no external homologation',
    'status':'PARTIAL_LAB_ONLY' if a[:3]!='Sem' else 'HOLD','NAC_PASS':'BOUNDED_TECHNICAL_ONLY_TERMINAL_HOLD'},
  'source_R105_SHA256':old.get('source_R105_SHA256')})
final={'as_of':'2026-10-16','operation':arr['operation'],'baseline':'R01–R125 IMMUTABLE',
 'source_original_matrix_sha':arr['source_original_matrix_sha'],'fixed_denominator':17,
 'terminals_before':0,'terminals_after':0,'reference_power_cells_official':0,'total_power_cells':1875,
 'rows':rows}
(ROOT/'R135_17_CONTRACTS_BEFORE_AFTER.json').write_text(json.dumps(final,indent=2,ensure_ascii=False)+'\n')
md=['# VLAB R126–R135 — MATRIZ ORIGINAL DOS 17 CONTRATOS (MESTRE-ONLY)',
     '**OP:** OP-VLAB-FUSION-SANDBOX-01 · **BASELINE:** R01–R125 imutável · **TERMINAL:** 0/17',
     'Provas R126+ são técnicas condicionais; R130 inválida por drift de speed; R132 é a cura aprovada por auditor frio.', '']
for x in rows:
 md+=['## %02d — `%s`'%(x['position'],x['id']), '**Gate original:** '+x['original_requirement_verbatim'],
       '**ANTES R125:** '+x['ANTES_R125']['new_integrated_evidence'],
       '**DEPOIS R135:** '+x['DEPOIS_R135']['new_executed_evidence'],
       '**Menor restante:** '+x['DEPOIS_R135']['minimum_remaining'],
       '**Revisão:** Auditoria fria escopada, não homologação independente competente.',
       '**NAC-PASS terminal:** HOLD · **Certificado:** NÃO','']
(ROOT/'R135_17_CONTRACTS_BEFORE_AFTER.md').write_text('\n'.join(md))
# Native code exact reproducible unified diff.
old=(BASE/'native_v081_controlled/vlab_effects_v08.py').read_text().splitlines(keepends=True)
new=(ROOT/'native_v081_controlled/vlab_effects_v08.py').read_text().splitlines(keepends=True)
patch=''.join(difflib.unified_diff(old,new,fromfile='R125/vlab_effects_v08.py',tofile='R135/vlab_effects_v08.py'))
(ROOT/'R135_NATIVE_V081_PATCH.diff').write_text(patch)
# Source-only selected receipts: not concatenate 165, 212 or 1344.
input_runs=['R126_PA_REACTION_AOO_DEV_943207','R126_SAFE_DISENGAGE_RESERVED_NOT_BLIND_953209','R132_HEAL_SOURCE_3ACTOR_CORRECTED_S963212']
receipts=[]
for run in input_runs:
 with sqlite3.connect(ROOT/'runs'/f'{run}.sqlite') as con:
  events=[json.loads(r[0]) for r in con.execute('SELECT row_json FROM events ORDER BY seq')]
 for row in events:
  for n,ev in enumerate(row['detail']['native_actions'],1):
   if ev['action']!='weapon_attack':continue
   receipts.append({'run_id':run,'seed':int(run.split('_')[-1].lstrip('S')),'event_seq':row['seq'],
    'native_seq':n,'actor':ev['from'],'target':ev['to'],'attack_origin':ev.get('attack_origin','NORMAL'),
    'score':ev['roll_score'],'hit':ev['hit'],'critical':ev['critical'],
    'source_raw':ev['raw'],'RD_applied':ev['rd_applied'],'net_after_RD':ev['net'],
    'HP_before':ev['before_hp'],'HP_after':ev['after_hp'],
    'HP_loss_actual':ev['hp_loss_actual'],'overkill':ev['overkill'],
    'PA_paid_in_attack_event':0,'reaction_mode':ev.get('defensive_reaction'),
    'audit':'R128/R133_INDEPENDENT_COLD','denominator_unit':'ATTACK_RECEIPT_DEPENDENT',
    'official':False,'full_combat':False})
assert len(receipts)==7,len(receipts)
with (ROOT/'R135_DMG_ATTACK_RECEIPTS_7.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(receipts[0]));w.writeheader();w.writerows(receipts)
# Science and quarantines.
science={'batteries':{'A':'25 individual ED; 0 new official cells, 1 Eristan ON5 healer not ED',
 'B':'27 same lineage; Grifo L2 derivation and L3 source preserved; no new battle',
 'C':'25 team power; A/Feryn clones not balanced ED teams; no score',
 'D':'27 distinct beasts; ADM26, Divine27, no new distinct species or canonical measurements'},
 'official_cells':0,'total_cells':1875,'new_selected_scenes':3,'new_selected_seed_families':3,
 'selected_one_round_events':32,'selected_offensive_attack_receipts':7,
 'selected_PA_paid':170,'auditor_failed_run':'R130_HEAL_SOURCE_3ACTOR_S963211',
 'auditor_pass_heal_run':'R132_HEAL_SOURCE_3ACTOR_CORRECTED_S963212',
 'not_official_full_combat':True,'blind_holdout_certified':False}
(ROOT/'R135_SCIENCE_A_B_C_D.json').write_text(json.dumps(science,indent=2,ensure_ascii=False)+'\n')
quarantine={'no_repeat_historical':'R01–R125 preserved in exact original ZIP including R123 unknown and R124 5×5 censored',
 'R130_HEAL_SOURCE_3ACTOR_S963211':{'status':'QUARANTINE','cause':'native generator unexpectedly set all actor speed to None; independent cold audit rejected state at INIT', 'no_retry':True},
 'R134_AFTER_INTENT_973211':{'status':'DIAGNOSTIC_PREVALIDATION_HOLD','cause':'payload JSON conversion vs tuple comparison rejected before intent; no unknown effect', 'no_credit':True},
 'R134_AFTER_INTENT_973213':{'status':'UNKNOWN_EFFECT_HOLD','pending':1,'no_retry':True},
 'R134_AFTER_COMMIT_973214':{'status':'FAULT_PROBE_PASS','pending':0,'exactly_one_paid_reaction':True},
 'R135_NEGATIVE_PRE_INTENT_983211':{'status':'REJECTION_PROBE_VALID','pending':0},
 'R132_HEAL_SOURCE_3ACTOR_CORRECTED_S963212':{'status':'SELECTED_COLD_PASS','healing':79,'pa':75},
 'source_constraints':['R126 Marca duration source3 turns but expiration boundary unresolved; mark stored only',
   'R126 distances/range asserted experimental fixture; do not certify positional metric/line of sight canon',
   'R135 specific RD Dark60 source unit only, not a real attack',
   'R130 initial readback failed; preserve all; no reverse mutation'],
 'writer':'CM-000006 PAUSED, no lease/ACK/epoch/fencing'}
(ROOT/'R135_QUARANTINE_NO_REPEAT.json').write_text(json.dumps(quarantine,indent=2,ensure_ascii=False)+'\n')
# handoff without impersonating DMG writer
handoff='''# VLAB → DMG | R126–R135 novo handoff preparado, NÃO ACEITO (MESTRE-SIDE)

Nova seleção: **7 recibos de ataques** em 3 cenas de apenas 1 rodada, **não 7 ataques independentes**. RUN-IDs R126 dev/reserva e R132 cura. Fonte Auren/Feryn/Eristan propostas Mestre-side, sem benchmarks oficiais. Ataque de oportunidade representado pelo tipo OPPORTUNITY; efeito da Capa de Poeira 35 PA e Marca25 / Cura75 constam dos ledgers de evento, não nos sete recibos ofensivos.

Separar dos **165 recibos R125**, **212 R116** e **1344 R97**, que possuem outras famílias, limitações e errata histórica R93/R95 (erro do crítico máximo por face corrigido só a partir de R117; R93/R95 TECH_REPLAY_PASS/NORMATIVE_PARITY_HOLD). Não produzir probabilidade populacional de vitória.

Recibos: `R135_DMG_ATTACK_RECEIPTS_7.csv`. Cura R132: 79 PV + luvas20, 75PA. Status `LOCAL_COLD_AUDIT_PASS`, não DMG_ACK; `R130_HEAL_*` é apenas QUARENTENA e nunca entra no corpus selecionado.

Fonte R130 ficha Eristan: https://app.notion.com/p/3f6c2b324ede819cae98ec0f6a63de76
Fonte Feryn: https://app.notion.com/p/3f6c2b324ede81ce9c61db8127bf0e31
Fonte Auren: https://app.notion.com/p/3ebc2b324ede814bb730d47dd7bd5f02
**Rota:** Biblioteca VLAB existente. O executor DMG deve buscar/reabrir o artefato pelo roteamento competente e confirmar recebimento; nenhuma escrita na OP-DMG foi realizada.
'''
(ROOT/'R135_DMG_HANDOFF_READONLY.md').write_text(handoff)
print(json.dumps({'rows':len(rows),'offensive_selected':len(receipts),'selected_paid_pa':science['selected_PA_paid'], 'patch_bytes':len(patch),'build_done':True},ensure_ascii=False))
