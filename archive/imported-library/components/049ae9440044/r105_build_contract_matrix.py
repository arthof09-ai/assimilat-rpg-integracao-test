"""Audits 17 original IDs; never changes official contract definitions or statuses."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent
BASE=R.parent
origp=BASE/'r61_extracted/work/reconstruction/r17_delivery/VLAB_R17_MATRIX_17_MASTER_ONLY.json'
r18p=BASE/'r61_extracted/work/reconstruction/r18_delivery/VLAB_R18_MATRIX_17_MASTER_ONLY.json'
r60p=BASE/'r61_extracted/evidence/R60_17_CONTRACTS_CROSSWALK.json'
r70p=BASE/'r71_extracted/R70_CROSSWALK_17.json'
r81p=BASE/'r81_extracted/r72_r81/R81_17_CONTRACTS_RECONCILED.json'
r91p=BASE/'r91_extracted/r82_r91/R91_17_CONTRACTS_RECONCILED.json'
r101p=BASE/'r92_r101/R101_17_CONTRACTS_RECONCILED.json'
files=[origp,r18p,r60p,r70p,r81p,r91p,r101p]
for p in files:assert p.is_file(),p
source_sha={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
orig=json.loads(origp.read_text())['rows'];r60=json.loads(r60p.read_text())['rows'];r70=json.loads(r70p.read_text())['contracts']
r81=json.loads(r81p.read_text())['contracts'];r91=json.loads(r91p.read_text())['contracts'];r101=json.loads(r101p.read_text())['contracts']
assert len(orig)==len(r60)==len(r70)==len(r81)==len(r91)==len(r101)==17
lists=[orig,r60,r70,r81,r91,r101]
for li in lists:
 keys=[x.get('contract_id',x.get('id')) for x in li]
 assert len(keys)==17 and len(set(keys))==17
ids=[x['contract_id'] for x in orig]
for li in lists[1:]:assert set(ids)=={x.get('contract_id',x.get('id')) for x in li}
# requirement source is original R15 admission, preserved in R17, physically read from source JSON.
scenarios={
'ACTION_CATALOG_AIN01':('Catalogar Magia, Talão, Bico, Descarga, reação, prebuff e equipamento em catálogo com seleção autorizada; usar adaptador original com fontes congeladas.','Native v0.8.1 SAVE-HALF explicitamente bloqueado; escolhas/efeitos/custos especiais incompletos.', 'R103 6 recibos da Descarga Curta em adaptador aditivo fonte-limitado, NÃO prova menu v0.8.1.'),
'ACTOR_SNAPSHOT_SCENARIO':('Reabrir e congelar snapshots canônicos das identidades e diferentes estados, 14 gates conforme contrato, testar mutação/reabertura e isolamento de fonte.','VZ PRECREATE não materializado, perfil VLAB PAUSED e snapshots de personagens da campanha sem licença de escrita.', 'R103 15 genesis/SQLite isolados auditados, nenhuma ficha canônica escrita.'),
'AUTHORITATIVE_RULES_AND_ADAPTERS':('Comparar literalmente Sistema de Combate com implementações e reproduzir TODOS os divergentes; bloquear efeitos conflitantes.', 'R95 usou +10 no crítico de 20d10 quando norma atual manda +200; FRACO/esforço final omitidos; v0.8.1 SAVE-HALF bloqueado.', 'R102 4 ocorrências físicas espelhadas read-only discrepantes, 1 seed real; não alterar R95.'),
'BATTLE_1X1_2X1_20X20':('Admitir lutas completas 1x1, 2x1 e 20x20 com políticas legais, cenários fonte-autênticos, reações, custos, KO, replay.','1x1 R95 com crítico divergente; 2x1 R93 NPC desigual; 20x20 não executado; políticas incompletas.', 'Nenhum duelo antigo repetido; R103 apenas habilidade isolada.'),
'BLEED_AND_HEAL_RESTRICTIONS':('Recuperar efeito físico real, cura/tick/duração/stacks, gates por fonte; executar testes de evento, expiração, negativos e recuperação.','Sem fonte competente para efeito de sangramento e cura com duração/limites completos no perfil selecionado.', 'Não se fabricou sangramento/cura.'),
'ED_VS_BE_DAMAGE':('Nova comparação física ED x Besta sob regras completas com não acerto, mitigação, crítico, vários patamares e efeitos especiais.','R95 crítica/Fraco divergence e source PRECREATE; fonte da real life/canon de VZ pendente; falta ampla diversidade.', 'R102 isolou impacto bruto/pós-RD/realizado e corrigiu interpretação da assimetria.'),
'GENERAL_SPECIFIC_RD':('Teste separadamente RD geral, específica, múltiplos tipos, maior/adição/empilhamento e bypass com autoridade documentada.', 'Regra normativa para empilhamento e bypass ainda HOLD; RD de Auren é físico/Dark tipado.', 'R103 tipo Lightning foi delimitado sem RD tipada de Lightning; não testa múltiplas tags.'),
'ITEM_EQUIPMENT_AND_ENHANCEMENTS':('Equipamento atual, ativação, compromissos de PA, charges, troca, duração, carga diária, perda/remoção e recuperação.', 'Snapshots completos de equip. e cobrança de PA de peças do cenário não testados; nenhum write em ficha.', 'Auren forma equipada conhecida, prova de cobrança isolada é de habilidade do Grifo, não de item.'),
'OFFICIAL_QA_NAC_LEDGERS':('Provar B1/B2/B3, status do writer, fencing, ledger oficial, auditor externo e NAC-PASS terminal com readback.', 'CM-000006 PAUSED; writer/lease/fencing/IBX-101 ACK ausentes; OFFICIAL_READBACK=0.', 'R103 auditor frio local PASS, sem pretensão de QA oficial.'),
'PA_AND_PREBUFF_COSTS':('Gasto PA positivo de fontes e prebuffs em transações indivisíveis, falta PA, rollback, timing, charges, custo em cada turno.', 'v0.8.1 SAVE-HALF recusa; regra arredondamento ímpar ausente; lifecycle de buff/prebuff ainda não validado.', 'R103 6 eventos com -55 PA, standard1->0, 6 half ímpares HOLD sem pending, 3 negativas sem efeito.'),
'REACTION_TRIGGER_AND_SINGLE_USE':('Dois gatilhos mesmo turno, consumo único, janela/renovação, simultâneas, aninhadas, rollback e precedência documentada.', 'Prioridade concorrente/nested não adjudicada; nenhum gatilho novo pós-R71.', 'R71 mantém 10 AoO e 181 counters históricos, sem rerun.'),
'RNG_REPLAY_STATISTICS':('Source-canonical RNG, seed freeze, pares lado, replays completos, estatística pré-registrada, holdout independente cego por famílias.', '2 seeds R95, 3 seeds R103 e espelhos não fornecem validação independente de famílias nem RNG de rolagem oficial.', 'R102 recontou blocos independentes; R103 3 seeds em 6 ledgers causalmente frios; não são seis seeds.'),
'SOURCE_FREEZE_AND_RANK':('Congelar identidades/versionamento e pelo menos 14 gateways de atores fontes canônicas, rank/estrela/27 patamares de potência.', 'BEAST-FULLSPEC=suporte PRECREATE VZ, 0/14 físicos no HANDOFF; sem equivalência automática às fichas principais.', 'R104 derivação de Grifo L2, 7 candidatas agrupadas em 4 patamares, sem promoção.'),
'TACTICAL_AI_AB_FAIRNESS':('Duas políticas legítimas A/B blindadas, targeting, movimento, controle, recursos, contrajogo e equidade verificada independentemente.', 'R93 2x1 targeting fixo, sem sinergia de papéis; fonte de equipe equilibrada não formada.', 'Nenhuma vitória do Auren foi creditada como sinergia coletiva.'),
'TRANSFORMATION_OVERLAY_AI08':('Usar Espírito compatível/overlay materializado, ficha transformada, fórmulas derivadas, PA, duração, dispel, regressão.', 'Auren fonte individual descreve ativação 100PA/15 por turno, Sistema de Combate Lendário 320PA; resolver precedência antes de executar.', 'Auditoria documental registra o conflito, 0 transformações novas.'),
'TRANSFORMATION_PER_SCENE_AI09':('Provar limites por cena, gasto e renovação/rest/cooldown, reentrância, salvamento/recovery, fonte genuína v0.9.', 'Falta fonte dos limites por cena e paridade v0.9 genuína; nenhuma ativação legítima executada.', 'Nenhum contador de cena inventado.'),
'TURN_SCHEDULER_EVENT_SOURCING':('Iniciativa natural real, tie, turnos 3+ e 20x20, interrupção, KO, reação/ressuprimento, snapshots e recuperação causal.', 'Competência de Iniciativa do Grifo/Croc não publicada; R95 exógena, R93 usa hipótese de iniciativa; v0.9 parity/rewind não certificada.', 'R104 demonstrou intervalo matemático sem atribuir proficiência à Besta; R103 ação isolada não comprova scheduler.')}
assert len(scenarios)==17
record=[]
for idx,row in enumerate(orig,1):
 cid=row['contract_id']
 rr60=next(x for x in r60 if x['contract_id']==cid);rr70=next(x for x in r70 if x['id']==cid)
 rr81=next(x for x in r81 if x['id']==cid);rr91=next(x for x in r91 if x['id']==cid);rr101=next(x for x in r101 if x['id']==cid)
 tests,block,new=scenarios[cid]
 record.append({'position':idx,'id':cid,
  'original_requirement_verbatim':row['exact_terminal_requirement_from_r15'],
  'original_closure_action':row['concrete_closure_action'],
  'original_dependency_owner':row['dependency_owner'],
  'R01_R17':{'R15':row['r15_evidence'],'R16':row['r16_delta_scope'],'R17':row['r17_documentary_delta']},
  'R18_R49':{'original_R18_priority_bucket':row['r15_status'],'R18_original_acceptance_retained':True},
  'R52_R61':rr60['R52_R61_evidence'],
  'R62_R71':rr70['delta'],
  'R72_R81':rr81['R72_R81_delta'],
  'R82_R91':rr91['R82_R91_evidence'],
  'R92_R101':rr101['R92_R101_delta'],
  'R102_R105_new_evidence':new,
  'tests_remaining':tests,'blocker':block,
  'minimum_terminal_acceptance':row['exact_terminal_requirement_from_r15'],
  'independent_terminal_acceptor':'PENDING_COMPETENT_AUTHORITY',
  'nac_pass_terminal':'HOLD', 'terminal_certified':False,'official_cells_promoted':0,
  'classification':'LAB_COMPONENT_ADVANCED_NOT_TERMINAL' if any(t in new for t in ['R103 6','R102','R104']) else 'HISTORICAL_PARTIAL_OR_NOT_EXERCISED'})
result={'schema':'R105_ORIGINAL_17_CONTRACTS_FULL_LINEAGE_CROSSWALK',
        'baseline_original':'R17 rows contain R15 exact terminal requirements; R18 certified matrix preserved',
        'source_file_hashes':source_sha,'denominator':17,'original_ids_unchanged':True,
        'terminal_certified':0,'official_cells_promoted':0,'official_cells_denominator':1875,
        'NAC_PASS_PRODUCTION':'HOLD','writer':'PAUSED/NOT_ACQUIRED',
        'historical_evidence_status':'R92_R101 adapter technically audited; current Combat normative critical mismatch found in R102',
        'contracts':record}
(R/'R105_ORIGINAL_17_CONTRACTS_MATRIX.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
md=['# R105 — Matriz de auditoria individual dos 17 contratos originais',
    'MESTRE-SIDE / OP-VLAB-FUSION-SANDBOX-01 / R01–R101 intacto. Matriz ancorada R17/R18. **0/17 terminais; 0/1875 células oficiais.**',
    '', 'Fonte primária: `reconstruction/r17_delivery/VLAB_R17_MATRIX_17_MASTER_ONLY.json` (requisito de R15 preservado em R17), `reconstruction/r18_delivery/VLAB_R18_MATRIX_17_MASTER_ONLY.json`; ligações comprovadas R60/R70/R81/R91/R101.',
    'R95: auditor local PASS técnico, mas **HOLD de conformidade normativa** após conflito no crítico da Besta +200 vs +10, mais Fraco/esforço final. Não elevar estados.',
    '', '| Nº | Contrato original | Requisito terminal original (R15→R17) | Evidência funcional histórica R01–R101 | Novo teste/evidência R102+ | Testes pendentes | Bloqueio | Gate terminal |',
    '|---:|---|---|---|---|---|---|---|']
for row in record:
 hist='R52–61: '+row['R52_R61']+' R62–71: '+row['R62_R71']+' R72–81: '+row['R72_R81']+' R82–91: '+row['R82_R91']+' R92–101: '+row['R92_R101']
 fields=[str(row['position']),row['id'],row['original_requirement_verbatim'],hist,
         row['R102_R105_new_evidence'],row['tests_remaining'],row['blocker'],
         'HOLD — '+row['minimum_terminal_acceptance']+'; auditor independente, writer e NAC-PASS competente']
 md.append('| '+' | '.join(t.replace('|',' / ').replace('\n',' ') for t in fields)+' |')
md.extend(['','## Gate e controle',
   '- **Documental:** 17/17 IDs e requisitos encontrados sem alterar a fonte.',
   '- **Funcional subcontrato:** testes originais e recentes separados por proveniência; não reexecutar combates homologados tecnicamente.',
   '- **Terminal:** 0/17; nenhuma linha encerra somente por replay de 24 combates R101.',
   '- **Original de R95:** imutável; errata normativa R102 aditiva, sem reprocessar/editar ledgers.',
   '- **Destravamento comum:** autoridade de fonte/cenário, paridade com motor competente, auditor independente, ACK/lease válido quando exigido e NAC-PASS-02.',
   '- **Próxima frente:** native-critical + Fraco/paridade e SAVE-HALF em fonte nova; iniciativa Besta; subescopo 2×1 equilibrado; PA/prebuff e reações; 20×20 só após garantias de escala.',
   ''])
(R/'R105_ORIGINAL_17_CONTRACTS_MATRIX.md').write_text('\n'.join(md))
print('17 contracts verified:',len(record),'bytes json',(R/'R105_ORIGINAL_17_CONTRACTS_MATRIX.json').stat().st_size,'md',(R/'R105_ORIGINAL_17_CONTRACTS_MATRIX.md').stat().st_size)
