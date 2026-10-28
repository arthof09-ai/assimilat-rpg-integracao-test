"""Read-only derivation of R145 evidence, 17 original contracts and DMG cohort."""
import json,sqlite3,hashlib,csv,difflib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'r126_r132'
def write(name,obj): (ROOT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
def sha(b):return hashlib.sha256(b).hexdigest()

def build():
 old=json.loads((BASE/'R135_17_CONTRACTS_BEFORE_AFTER.json').read_text())
 audit=json.loads((ROOT/'R139_INDEPENDENT_COLD_AUDIT.json').read_text())
 cap=json.loads((ROOT/'R142_COLD_CAP_AND_REDTEAM.json').read_text())
 fault=json.loads((ROOT/'R144_INDEPENDENT_FAULT_AUDIT.json').read_text())
 prefix=json.loads((ROOT/'R140_COLD_PREFIX_CHECKPOINT.json').read_text())
 source_r137=sha(Path('/mnt/data/VLAB_R126_R137_PA_REACAO_AOO_CURA_MESTRE_ONLY.zip').read_bytes())
 assert source_r137=='cb616e562970e9fb6e8e08465cdf1fbbf4070d85f99c0000ea8f0756f7b8371e'
 scope={
 'ACTION_CATALOG_AIN01':('R138 Passo da Fuligem (25 PA Movimento, +12m só neste turno) e Pulso de Estabilização (45 PA Reação) agora integrados com R132 cura/Capa/Marca em QUATRO rodadas.','Faltam catálogo integral, efeitos mágicos, alcance pleno, ativos de área e cobertura de todas as ações.'),
 'ACTOR_SNAPSHOT_SCENARIO':('R138 três perfis distintos efetivamente ligados a fontes Mestre-side, com genêses, vida/PA/posição e readback de quatro rodadas; NÃO são perfis canônicos vivos.','Materialização canônica, integridade das propostas de item, identidades vivas e snapshot do encontro real.'),
 'AUTHORITATIVE_RULES_AND_ADAPTERS':('R138 source-freeze documentado, uso explícito de exceção R42 LAB-ONLY para falha crítica negativa DESCOBERTA, mas NÃO integrada ainda no R138; Passo ESTE TURNO explícito.','R42 bridge negativo no resolutor corrigido ainda precisa implementação; Marca 3 turnos sem fronteira normativa; conflitos de custos de transformação.'),
 'BATTLE_1X1_2X1_20X20':('R138: cena 1×2 de 4 rodadas 40 commits, habilidades reais, reação, cura e AoO coexistindo; fim CENSORED_HORIZON sem vencedor. Escala técnica R125 preservada.','Primeiros duelos fonte-completos com resultado final, composição equilibrada 2 ED, 20×20 paridade real.'),
 'BLEED_AND_HEAL_RESTRICTIONS':('R138 quatro curas em cena após dano + Pulso reativo pós-AoO: 411 PV efetivos; R141 cura faltando 14 PV: bruto96/efetivo14/overheal82, 6 gates fail-closed.','Sangramento equipado real/portador elegível, duração e retirada sob regras específicas, comportamento KO, cicatrização prolongada e recuperação pós-status.'),
 'ED_VS_BE_DAMAGE':('R138 prova técnica de Espiritualista L3 contra propostas de NPC ON5, NÃO ED×Besta; preservado dado R107 de Grifo.','Combate ED×Besta completo com proficiência individual de Iniciativa da Besta, habilidades completas e RD.'),
 'GENERAL_SPECIFIC_RD':('R138 3 ataques físicos com RD22 source Feryn, 672 PV de dano efetivo; RD Dark 60 de Auren conhecida mas NÃO acionada nesta cena.','Ataque Dark literal e perfil completo para Auren, mistura de componentes e adjudicação de RD gerais/específicas sem acumulação inventada.'),
 'ITEM_EQUIPMENT_AND_ENHANCEMENTS':('R138 Eristan luvas +20 por cura de fonte, cinco aplicações auditadas (4 Padrão +1 Pulso); R141 cap sem segunda cobrança de PA vinculado.','Equipamento retirado, suprimido, transferência legítima, efeitos de item não-heal e compromisso ao longo de descanso/cenas.'),
 'OFFICIAL_QA_NAC_LEDGERS':('R139 auditor independente 40/40, R140 prefix checkpoint reconstruído com R18 load; R142 dois redteams semânticos; R143/144 crash fault 2/2.','Revisão independente competente, NAC-PASS-02 original, homologação normativa e escrita autorizada.'),
 'PA_AND_PREBUFF_COSTS':('R138 consome 430 PA ao longo de 4 rodadas (F85/E345); turno/ação Padrão+Movimento+Reação; Passo25 expira no END; R143 fault sem débito duplo.','Manutenção temporal distinta, pré-buffs completos, recarga oficial e classificação custos variáveis.'),
 'REACTION_TRIGGER_AND_SINGLE_USE':('R138 Capa35 em R1 e Pulso45 após dano de AoO em R3, slots próprios sem duplicação; R143 crash de Passo preserva slots; R125 R50/R51 mantidos.','Concorrência real de múltiplas oportunidades simultâneas, stack de reações incluindo defesa+evento temporal.'),
 'RNG_REPLAY_STATISTICS':('R139 reexecuta offline todos os dados e 40 snapshots sem motor; R142 dois payloads adulterados com hash refabricado recusados. Seed991402 de fallback desenvolvimento, NÃO blind holdout.','Holdout realmente independente e pré-registrado, amostragem estatística de lutas integrais e RNG oficial.'),
 'SOURCE_FREEZE_AND_RANK':('Fonte Auren L3 e ON5 Feryn/Eristan + sistemas reabertos; R42 Mestre LAB-only localizado; fonte Grifo L2 derivada preservada.','Snapshots canônicos, 27 patamares Besta materializados, rankings e nível homólogos.'),
 'TACTICAL_AI_AB_FAIRNESS':('R138 política de testes propositalmente inclui A abdicando Padrão em R2/R3; isso testa duração NÃO IA competitiva.','Políticas táticas A/B comparáveis, fair match, cegamento e vitória final inferível.'),
 'TRANSFORMATION_OVERLAY_AI08':('R138 não ativou transformação. Consulta Normas confirma custos Lendário 320PA ainda divergentes da ficha Auren100+15/turno.','NAC-NORM-01: resolver precedente e execução temporal overlay em cena completa.'),
 'TRANSFORMATION_PER_SCENE_AI09':('R138 Passo temporal é efeito H, NÃO transformação; preserva terminal HOLD.','Descanso/recarga por cena, duração e estado de Espírito fonte-vinculado.'),
 'TURN_SCHEDULER_EVENT_SOURCING':('R138 4 rodadas/12 próprios turnos/40 commits com Capa, Marca, Passo e expiração, AoO, Pulso, quatro curas, readback independente; R140 prefixo 20 eventos reconstruído e reaberto.','Persistência de estados multirrodada completa, efeitos 3 turnos com fronteira válida, KO, participantes removidos e retomada LIVE de checkpoint intermediário.')}
 assert len(scope)==17
 rows=[]
 for row in old['rows']:
  cid=row['id'];e,remaining=scope[cid]
  rows.append({'position':row['position'],'id':cid,
   'original_requirement_verbatim':row['original_requirement_verbatim'],
   'ANTES_R135':row['DEPOIS_R135'],
   'DEPOIS_R145':{'new_executed_or_audited_evidence':e,
       'minimum_remaining':remaining,'status':'PARTIAL_LAB_ONLY',
       'terminal_certified':False,
       'independent_audit':'R139 cold causal only for R138; R142 independent heal cap/adversarial; not official independent cert',
       'NAC_PASS':'PASS_TECHNICAL_BOUNDED; TERMINAL_HOLD'},
   'source_R105_SHA256':row['source_R105_SHA256']})
 assert len(rows)==17 and [r['id'] for r in rows]==[r['id'] for r in old['rows']]
 matrix={'as_of':'2026-10-16','operation':'OP-VLAB-FUSION-SANDBOX-01',
 'baseline':'R01-R137 preserved','reference_matrix_SHA':sha((BASE/'R135_17_CONTRACTS_BEFORE_AFTER.json').read_bytes()),
 'denominator_original':17,'terminal_before':0,'terminal_after':0,
 'source_status':'MESTRE_SIDE_TECHNICAL_PRECREATE','power_grid_official':0,'power_grid_total':1875,
 'rows':rows}
 write('R145_17_CONTRACTS_BEFORE_AFTER.json',matrix)
 lines=['# R145 — Os 17 contratos originais | ANTES R135 → DEPOIS R145','',
        '**Autoridade:** MESTRE-SIDE / OP-VLAB-FUSION-SANDBOX-01; sem writer OP, sem certificado terminal. 17/17 IDs, 0/17 PASS terminal.','']
 for row in rows:
  a=row['ANTES_R135'];b=row['DEPOIS_R145']
  lines+=['## '+str(row['position'])+'. `'+row['id']+'`','',
    '**Requisito original:** '+row['original_requirement_verbatim'],
    '**ANTES R135:** '+a.get('new_executed_evidence','(nenhuma prova nova)'),
    '**Nova prova R145:** '+b['new_executed_or_audited_evidence'],
    '**Menor restante:** '+b['minimum_remaining'],
    '**Revisão:** '+b['independent_audit'],
    '**Gate terminal:** HOLD; NAC-PASS-02 não homologado.','']
 (ROOT/'R145_17_CONTRACTS_BEFORE_AFTER.md').write_text('\n'.join(lines)+'\n')
 # Attack receipt only the 3 new attacks; all legacy cohorts strictly segregated.
 db=ROOT/'runs'/'R138_MULTI_SOURCE_FERYN_ERISTAN_DEV_S991402.sqlite'
 with sqlite3.connect(db) as conn:
  events=[json.loads(r[0]) for r in conn.execute('SELECT row_json FROM events ORDER BY seq')]
 rec=[]
 for row in events:
  for v in row['detail']['native_actions']:
   if v['action']!='weapon_attack':continue
   rec.append({'cohort':'R138_ONLY','RUN_ID':db.stem,'seed':991402,
    'revision':row['seq'],'combat_event_id':row['cmd_id'],
    'attacker':v['from'],'target':v['to'],'source_attacker':'Auren L3; Notion '+old.base.AUREN if False else 'Auren L3 Notion 3ebc2b324ede814bb730d47dd7bd5f02',
    'source_target':'Feryn ON5 Mestre-side proposal 3f6c2b324ede81ce9c61db8127bf0e31',
    'attack_origin':v['attack_origin'],'reaction_window':'CAPA_BEFORE_ATTACK' if v.get('defensive_reaction')=='CAPA_POEIRA' else 'AOO_WHEN_EXIT' if v['attack_origin']=='OPPORTUNITY' else 'NONE',
    'critical':v['critical'],'critical_sequence':v['critical_sequence'],'attack_score':v['roll_score'],
    'damage_rolls':v['damage_roll_groups'],'raw':v['raw'],'rd_applied':v['rd_applied'],'post_rd':v['net'],
    'HP_lost':v['hp_loss_actual'],'HP_before':v['before_hp'],'HP_after':v['after_hp'],
    'overkill':v['overkill'],'PA_consumed_by_attack':0,'outcome_censor':'CENSORED_AT_FOUR_ROUNDS',
    'causal_audit':'R139_COLD_PASS','power_reference':'NO',
    'historical_cohorts_not_appended':'R97_1344,R116_212,R125_165,R137_7'})
 assert len(rec)==3
 with (ROOT/'R145_DMG_ATTACK_RECEIPTS_3.csv').open('w',newline='') as out:
  csvw=csv.DictWriter(out,fieldnames=list(rec[0]));csvw.writeheader();csvw.writerows(rec)
 write('R145_SCIENCE_A_B_C_D.json',{
  'A':{'goal':'25 individual Spiritualist archetypes','new_official_cells':0,
   'observation':'Auren has source L3; Feryn and Eristan ON5 proposed without Demon Spirit and CANNOT count.'},
  'B':{'goal':'27 power positions same Beast lineage','new_official_cells':0,
   'observation':'Grifo L2 virtual derived as single species continuity; no source complete fight here.'},
  'C':{'goal':'25 team power levels','new_official_cells':0,
   'observation':'Auren vs Feryn/Eristan is 1x2 conditional, intentionally forego actions and censored; no balanced ED team.'},
  'D':{'goal':'27 distinct Beast species','new_official_cells':0,
   'observation':'ADM26 and Besta Divina27 above Lendario5; distinct source species insufficient.'},
  'additional_science':{'R138':'4 rounds, 40 commits, 3 attacks, 411 HP healed, 672 HP lost, CENSORED; outcome/power not estimable',
     'R141':'14 HP cap laboratory fixture, not realized combat','official_cells':'0/1875',
     'independent_seeds':'one executed new multiround development seed; no blind holdout'}})
 write('R145_NORMATIVE_GATES.json',{
 'Marca_3_turns':'HOLD; no established exact expiry boundary; timeline data stored not applied to attack',
 'Passo_este_turno':'PASS technical source expiration within same own turn',
 'Falha_critica':'Mestre R42 LAB-ONLY decision physically recovered: miss auto; zero damage; standard consumed, no extra penalty. v0.8.1 R138 still pre-intent HOLD for negative; integration next; historical R124 unchanged.',
 'RD_Dark60':'Auren has explicit specific Dark RD60; no source-eligible Dark attack among three R138 frozen actors; integrated test HOLD',
 'RD_mix':'Source formula for true separate components + selection lacking; HOLD, no RD stacking',
 'bleeding':'Sangramento catalogued historically but no proven equipped eligible actor in R138 team; no bleed effect simulated; SOURCE-HOLD',
 'Auren_transformation':'specialized Combat/Transformation Lendario activation320 PA contradicts historical Auren100PA +15/turn; unresolved under NAC-NORM-01; transformation NOT used',
 'Eristan_equipment':'Mestre-only proposal, not materialized official gear; tested as frozen proposal',
 'metric_geometry':'B0-B3 topology non-metric; distances 1.5m/2m/3m separate source-scoped scenario facts not a block scale',
 'combat_outcome':'R138 four-round censor, zero official victory or power cells'})
 (ROOT/'R145_DMG_HANDOFF_READONLY.md').write_text('''# VLAB R145 → DMG | Handoff MESTRE-SIDE preparado — ACK não comprovado

Nova coorte **R138**: 3 recibos ofensivos em `R145_DMG_ATTACK_RECEIPTS_3.csv`, 2 ataques normais + 1 Ataque de Oportunidade, seed 991402, 1 cena fonte-condicional de 4 rodadas. Separar **R97 1344**, **R116 212**, **R125 165**, **R137 7**: nenhum concat automático.

R138: bruto, RD física22, net, HP retirado, overkill, sequência crítico, reação Capa, AoO, custos de 430 PA totais da cena, 411 PV curados (4 Reconstituições + Pulso), conclusão **CENSORED_HORIZON sem vencedor**. Apenas 1 seed desenvolvimental, nenhuma prova de holdout independente, Eristan/Feryn ON5 sem Espírito Demoníaco e com equipamentos Mestre-side PROPOSTOS. Não usar para média populacional, win rate ou 1.875 células oficiais.

R97 R93/R95 históricos continuam `TECHNICAL_REPLAY_PASS / NORMATIVE_PARITY_HOLD` por erro de bônus crítico; seis recibos, duas famílias de seeds, nunca corrigidos retroativamente. R138 usa v0.8.1 reparado mas não confirma todas as regras.

**Rota:** cópia documental depositada apenas na Biblioteca original VLAB, não enviada à operação DMG por writer não verificado; DMG precisa ACK físico antes de estado RECEBIDO.
''')
 original=(BASE/'native_v081_controlled'/'vlab_effects_v08.py').read_text().splitlines(keepends=True)
 new=(ROOT/'native_v081_controlled'/'vlab_effects_v08.py').read_text().splitlines(keepends=True)
 patch=''.join(difflib.unified_diff(original,new,fromfile='R137/vlab_effects_v08.py',tofile='R138/vlab_effects_v08.py'))
 (ROOT/'R145_NATIVE_ADDITIVE_PATCH.diff').write_text(patch)
 assert patch and len(patch)>500
 output={'original_R137_SHA256':source_r137,'new_multi_round_seed':991402,'new_scenes':1,
  'complete_battles':0,'censored_battles':1,'runs_technical_not_battles':7,
  'R138':audit,'R141':{'healing_cap':cap['cap'],'negative_gates':6},
  'R142_redteam':cap['redteam'],'R140_prefix':prefix,'R143_faults':fault['fault_cases'],
  'contracts_total':17,'contracts_certified_terminal':0,'power_cells_official':0,'power_cells_total':1875,
  'DMG_attack_receipts_new':len(rec),'readback_complete':False,
  'source_status':'MESTRE_SIDE_PROPOSALS_LAB_ONLY'}
 write('R145_EVIDENCE_SUMMARY.json',output)
 return output
if __name__=='__main__':
 report=build();print(json.dumps({k:v for k,v in report.items() if k not in ['R138','R142_redteam','R140_prefix','R143_faults']},indent=2,ensure_ascii=False))
