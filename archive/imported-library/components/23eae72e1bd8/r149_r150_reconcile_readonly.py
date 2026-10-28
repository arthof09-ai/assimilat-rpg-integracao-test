"""Post-R145 additive, read-only reconciliation. Never reruns combat or mutates prior artifacts."""
from pathlib import Path
import csv,hashlib,json,sqlite3
ROOT=Path(__file__).resolve().parent
OLD=ROOT/'R145_17_CONTRACTS_BEFORE_AFTER.json'
NEW=ROOT/'runs'/'R146_MULTI_SOURCE_FERYN_ERISTAN_DEV_S995401.sqlite'
def sha(b):return hashlib.sha256(b).hexdigest()
def write(name,data): (ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
def build():
 old_bytes=OLD.read_bytes();m=json.loads(old_bytes)
 audited=json.loads((ROOT/'R147_INDEPENDENT_COLD_AUDIT.json').read_text())
 source=json.loads((ROOT/'R148_SOURCE_BINDING_AND_PREFIX.json').read_text())
 assert audited['metrics']['commits']==40 and audited['metrics']['native_events']==43
 assert source['source_prereg_before_m']==3 and source['ledger_pulse_pre_m']==3
 assert len(m['rows'])==17 and len({r['id'] for r in m['rows']})==17
 messages={
 'ACTION_CATALOG_AIN01':('R146 PASS: Capa, Marca, Passo, quatro Reconstituições, Pulso e Ataque de Oportunidade na mesma cena contínua, com Pulse a 3m antes do movimento. R138 SPATIAL_HOLD.', 'Cobertura de repertório inteiro, tipagem completa, efeitos duradouros com expiracao autorizada e interação adicional com transformação.'),
 'ACTOR_SNAPSHOT_SCENARIO':('R146 fonte-congelada de Auren+Feryn+Eristan, 12 turnos e readback do prefixo20; perfis ON5 são propostas Mestre-side, não atores oficiais.', 'Materialidade dos NPCs propostos, snapshots de cena canônica e identidades de equipe comparável.'),
 'AUTHORITATIVE_RULES_AND_ADAPTERS':('R146 source-binding Pulso pre-movimento3m comprovado após detectar desvio em R138; R42 LAB-ONLY crítico negativo historicamente reaberto, sem implementação nova neste motor.', 'R42 bridge negativo integrar na cópia multirrodada; definição exata de três turnos de Marca; custo de transformação; regra de dano misto.'),
 'BATTLE_1X1_2X1_20X20':('R146 4 rodadas/40 commits/3 atores distintos e 1x2 contextual, CENSORED_HORIZON; não conta como duelo concluído ou battle power.', 'Duelos fonte-completos, equipe ED comparável, 20x20 de paridade de criaturas e vencedor quando há resultado legítimo.'),
 'BLEED_AND_HEAL_RESTRICTIONS':('R146 4 curas Padrão + Pulso pós-dano em quatro rodadas: 371 PV efetivamente restaurados; R141 14PV-cap e 6 pre-intent source gates mantidos.', 'Sangramento com portador/equipamento admissíveis, persistência de restrição, cura pós-KO e recuperação sob status.'),
 'ED_VS_BE_DAMAGE':('R146 Auren ED vs dois NPCs ON5 apenas: propriedade de integração, NÃO execução ED vs Besta ou resultado de potência.', 'Primeiro confronto ED-Besta de fontes completas, iniciativa válida, habilidades e efeitos reais.'),
 'GENERAL_SPECIFIC_RD':('R146 três ataques físicos com RD22 Feryn e 659 dano efetivo; Dark RD60 de Auren continua unitária e não ocorreu nesta cena.', 'Primeiro Dark com atacante admissível, tratamento multicomponente autoritativo e stacking/bypass explícito.'),
 'ITEM_EQUIPMENT_AND_ENHANCEMENTS':('R146 bônus das Luvas +20 aplicado uma vez por 5 curas (4 Standard + Pulso), sem cobrar compromisso diário de novo.', 'Exibir retirada, supressão, carga/slot e transferência validamente fonte-gated.'),
 'OFFICIAL_QA_NAC_LEDGERS':('R147 auditor frio 40/40 refaz RNG e estado; R148 prova 3m pre-move/2m post e prefix rev20 reaberto; R138 SPATIAL_HOLD preservado.', 'Reviewer competente e gates B1/B2/B3, NAC-PASS-02 homologação terminal, verificação canônica.'),
 'PA_AND_PREBUFF_COSTS':('R146 consumo PA430 com três fontes reais; R143 faults antigos PASS; Passo25 expira ao END, Marca25 sem expiração forçada.', 'Custos de manutenção, pre-buffs ao longo de cenas, renovação temporal completa e regras de recursos condicionais.'),
 'REACTION_TRIGGER_AND_SINGLE_USE':('R146 duas Reações distintas Capa35 e Pulso45 após AOO, com renovação multi-rodada e sem slots duplicados; R138 espacial HOLD.', 'Concorrência real simultânea de múltiplos inimigos, interrupções aninhadas com precedência e recursos cruzados.'),
 'RNG_REPLAY_STATISTICS':('R147 auditou stream determinística e todos os snapshots da seed995401; desenvolvimento novo, NÃO holdout cego.', 'Fonte RNG canônica e holdout independente, estatística em observações independentes e política tática.'),
 'SOURCE_FREEZE_AND_RANK':('R146 URLs de origem de Auren/Feryn/Eristan, Fonte R42 LAB e snapshot da condição espacial 3m auditados; R138 proveniência HOLD isolado.', 'Source-freeze oficial, hierarquias e 27 patamares Besta materializados com personagens válidos.'),
 'TACTICAL_AI_AB_FAIRNESS':('R146 Auren deliberadamente abdicou Padrão, controlando teste temporal. NÃO serve como prova de IA competitiva ou efetividade comparativa.', 'Políticas táticas pré-registradas e justas com variação de escolha, observação independente e resultado de combate.'),
 'TRANSFORMATION_OVERLAY_AI08':('R146 não ativou transformação; conflito Auren 100+15 vs 320 continua isolado e não bloqueou multirrodada.', 'NAC-NORM-01, entrada/salida e overlays completos com Vida/PA/atributos.'),
 'TRANSFORMATION_PER_SCENE_AI09':('R146 expiração de Passo não equivale a transformação; progressão IA09 continua sem teste integrado.', 'Ativação Espírito, descanso, troca, duração, recursos e cena sob autoridade.'),
 'TURN_SCHEDULER_EVENT_SOURCING':('R146 12 turnos, quatro rodadas, 40 commits, 43 subeventos, pulso/interrupt/declarações, Passo END e checkpoint rev20 reconstruído; correção source-bound R138.', 'Expiração validada de efeitos multi-turno, checkpoint nativo salvo vivo e retomado, KO/remoção em cenário completo.'),
 }
 assert set(messages)==set(r['id'] for r in m['rows'])
 for r in m['rows']:
  cid=r['id'];delta,remain=messages[cid]
  r['ANTES_R145']=r.pop('DEPOIS_R145')
  r['DEPOIS_R150']={'R146_new_executed_accepted_evidence':delta,'R138_spatial_status':'SPATIAL_SOURCE_PRECONDITION_HOLD',
   'R145_prior_tests_reused':'R141 healing caps; R142 semantic redteams; R143/R144 crash recovery; R145 legacy 59/59 (not reexecuted here)',
   'minimum_remaining':remain,'independent_review':'R147 cold causal + R148 source binding + R18 prefix readback (technical only)',
   'technical_scope':'PASS R146 LAB-SOURCE-CONDITIONAL','NAC_PASS':'TERMINAL_HOLD',
   'terminal_certified':False}
 matrix={'operation':'OP-VLAB-FUSION-SANDBOX-01','checkpoint':'R150','original_denominator':17,'before_terminal':0,'after_terminal':0,
  'base_matrix_R145_SHA256':sha(old_bytes),'R145_immutable':True,'R138_source_status':'TECHNICAL_REPLAY_PASS/SPATIAL_PARITY_HOLD',
  'R146_status':'TECHNICAL_COLD_PASS/PREREG_SPATIAL_BINDING_PASS/CENSORED_HORIZON',
  'official_power_coverage':{'numerator':0,'denominator':1875},'rows':m['rows']}
 write('R150_17_CONTRACTS_BEFORE_AFTER.json',matrix)
 out=['# R150 — matriz ANTES/DEPOIS dos 17 contratos originais','',
 '**Operação:** OP-VLAB-FUSION-SANDBOX-01 · MESTRE-SIDE · R01–R145 preservada, incluindo o R138 agora em SPATIAL_PARITY_HOLD.','',
 '**DENOMINADOR:** 17/17 contratos reconciliados · **TERMINAL:** 0/17 antes e depois · **GRADE OFICIAL:** 0/1875.','',
 'O histórico R145 não é reescrito. R146 seed995401 substitui **apenas a prova de pré-condição espacial** numa nova execução de desenvolvimento; não são dois ensaios independentes para potência.','']
 for r in m['rows']:
  a=r['ANTES_R145'];b=r['DEPOIS_R150']
  out+=['## '+str(r['position'])+'. `'+r['id']+'`','',
  '**Requisito histórico original:** '+r['original_requirement_verbatim'],
  '**ANTES R145 (relatado/artefato histórico):** '+a['new_executed_or_audited_evidence'],
  '**DEPOIS R150 (R146 verificado):** '+b['R146_new_executed_accepted_evidence'],
  '**Provas independentes:** '+b['independent_review'],
  '**Menor restante:** '+b['minimum_remaining'],
  '**Gate terminal:** HOLD NAC-PASS-02, 0 certificado.','']
 (ROOT/'R150_17_CONTRACTS_BEFORE_AFTER.md').write_text('\n'.join(out)+'\n')
 with sqlite3.connect(NEW) as c: rows=[json.loads(v[0]) for v in c.execute('SELECT row_json FROM events ORDER BY seq')]
 attacks=[]
 for row in rows:
  for v in row['detail']['native_actions']:
   if v['action']!='weapon_attack':continue
   attacks.append({'cohort':'R146_ONLY', 'RUN_ID':NEW.stem, 'seed':995401,
    'revision':row['seq'],'event_ID':row['cmd_id'], 'attacker':v['from'],'target':v['to'],
    'source_attacker':'Sikong Auren L3 Notion 3ebc2b324ede814bb730d47dd7bd5f02',
    'source_target':'Sikong Feryn ON5 proposal Notion 3f6c2b324ede81ce9c61db8127bf0e31',
    'attack_origin':v['attack_origin'], 'reaction_window': 'Capa35' if v.get('defensive_reaction')=='CAPA_POEIRA' else 'AoO_Exit_3m_Pulso' if v['attack_origin']=='OPPORTUNITY' else 'None',
    'critical':v['critical'],'critical_sequence':v['critical_sequence'],'attack_score':v['roll_score'],
    'dice':v['damage_roll_groups'],'raw':v['raw'],'RD_fisica':v['rd_applied'],'post_RD':v['net'],
    'effective_HP_loss':v['hp_loss_actual'],'HP_before':v['before_hp'],'HP_after':v['after_hp'],
    'overkill':v['overkill'],'PA_consumed_by_attack':0,
    'target_healed_later':'YES','scene_status':'CENSORED_4_ROUNDS',
    'spatial_source':'R148_PREREG_PULSO_DISTANCE_3M_BEFORE_MOVE',
    'cold_audit':'R147_R148_PASS','scientific_equivalence':'NO_POWER_BENCHMARK',
    'historical_cohorts_excluded':'R97_1344,R116_212,R125_165,R137_7,R138_3_SPATIAL_HOLD'})
 assert len(attacks)==3
 with (ROOT/'R150_DMG_ATTACK_RECEIPTS_3.csv').open('w',newline='') as f:
  wr=csv.DictWriter(f,fieldnames=list(attacks[0]));wr.writeheader();wr.writerows(attacks)
 write('R150_COEVAL_AND_SCIENCE.json',{
  'accepted_selected_new_run':'R146_MULTI_SOURCE_FERYN_ERISTAN_DEV_S995401',
  'selected_new_run_count':1,'unique_new_seeds_selected':1,'new_audited_selected_commits':40,
  'source_spatial_before_m':3,'source_spatial_after_m':2,'source_spatial_gate':'PASS',
  'R138_historical_scene':'CENSORED; TECHNICAL_PASS; SPATIAL_PARITY_HOLD',
  'R146_4_rounds':True,'R146_healing_effective':371,'R146_damage_effective':659,'R146_PA':430,
  'three_actors':'Auren ED L3; Feryn ON5 NPC/no spirit; Eristan ON5 NPC/no spirit',
  'battle_winner':None,'scientific_grade':'CONDITIONAL_MECHANIC_ONLY',
  'batteries':{'A':'25 individual ED; zero new admitted complete reference','B':'27 same Grifo lineage positions, L2 derived not materialized; zero combat new',
  'C':'25 team tiers; no 2 comparably equipped ED; no new official cell',
  'D':'27 distinct Beast tiers, ADM26/Divina27; zero new official species/cell'},
  'no_concat_legacy_cohorts':True,'official_cells':0,'total_official_cells':1875,'terminal_contracts':0})
 (ROOT/'R150_DMG_HANDOFF_READONLY.md').write_text('''# VLAB → DMG | adendo R150, SOMENTE LEITURA, NÃO ACK\n\nR145 entregou 3 recibos da cena R138 cuja **paridade espacial posterior** entrou em `HOLD`. NÃO tratar esses registros como 3 amostras científica/canonicamente aceitas. R138 físico imutável.\n\nNova coorte **R146_ONLY**: 3 recibos ofensivos do **mesmo duelo censurado, uma seed995401 de desenvolvimento**, Auren L3 contra Feryn ON5 proposta, efeitos de Eristan ON5. Ver `R150_DMG_ATTACK_RECEIPTS_3.csv`, `R147_INDEPENDENT_COLD_AUDIT.json`, `R148_SOURCE_BINDING_AND_PREFIX.json`. Não concatenar automaticamente às coortes R97(1344), R116(212), R125(165), R137(7), R138(3/HOLD).\n\nR146 ação/AoO/Pulso com 3m **ANTES** do movimento e 2m **DEPOIS**; 40 commits, dano físico efetivo659, cura371, PA430, nenhum vencedor em 4 rodadas. Fonte R50/R51 e R42 LAB-ONLY preservada. Sem distribuição de probabilidades de vitória ou representatividade de equipe ED; DMG não confirmou recebimento. Não editar OP-DMG.\n''')
 print(json.dumps({'matrix_rows':len(m['rows']),'cohort_attacks':len(attacks),'selected_run':NEW.stem},ensure_ascii=False))
if __name__=='__main__':build()
