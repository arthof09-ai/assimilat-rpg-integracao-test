"""Read-only crosswalk for original 17 contracts and source-backed scientific receipts."""
import json,csv,hashlib,difflib,sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent
SRC=BASE/'r108_r117'

def read(p):return json.loads(Path(p).read_text())
def wr(p,x):Path(p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def dig(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

a=read(SRC/'R117_17_CONTRACTS_BEFORE_AFTER.json');cold=read(ROOT/'R120_COLD_AUDIT.json');scale=read(ROOT/'R124_SCALE_EXECUTIONS.json');scold=read(ROOT/'R124_SCALE_COLD_AUDIT.json');neg=read(ROOT/'R123_8_NEGATIVE_GATES_COLD_READBACK.json');fault=read(ROOT/'R123_NEW_FAULT_RESULTS.json')
assert len(a['rows'])==17 and neg['passed']==8 and len(cold['results'])==3 and len(scold['results'])==3 and fault['status']=='PASS'

updates={
'ACTION_CATALOG_AIN01':('Contra-atacar sob R50/R51, Defender e Esquivar integrados a ataques nativos em 3 atores; Descarga Curta R117 preservada, não rerodada.','Integrar efeitos adicionais documentados, Descarga + reações/PA na MESMA cena, limites de alcance e catálogo integral.'),
'ACTOR_SNAPSHOT_SCENARIO':('Seis genêses novos (3 multiator, 3 escala) com dois perfis documentais congelados, copies técnicas rotuladas e 6 checkpoints.','Snapshots canônicos materializados, divergência de fontes reconciliada e diversidade real.'),
'AUTHORITATIVE_RULES_AND_ADAPTERS':('R50/R51 decisões Mestre fisicamente localizadas na OP histórica; gatilho de counter por HIT efetivo (crítico acerta), proibição de contra-ataque aninhado; v0.8.1 estendida aditivamente.','Saneamento de ambiguidades restantes, sincronização normativa autorizada, revisão independente e NAC-PASS oficial.'),
'BATTLE_1X1_2X1_20X20':('3/3 cenas técnicas 1x2, 5x5 censurado preservado, 10x10/20x20 técnico concluído e auditado sem espécies novas.','Competições comparáveis com atores distintos, habilidade/PA/posição, 1x1/2x1/20x20 juridicamente completas e gates terminais.'),
'BLEED_AND_HEAL_RESTRICTIONS':('Nenhuma nova cura/sangramento executada; preserva material R117.','Adaptadores de sangramento/cura, fonte para stacks e duração, testes de interação e recuperação.'),
'ED_VS_BE_DAMAGE':('Nenhuma nova referência de potência ED×Besta; R112 permanece como fonte de ataques com limitação; escala usa Auren×Feryn NPC, NÃO Besta.','Besta com iniciativa, reação/habilidades legítimas, ED equivalente e análise por famílias com censura.'),
'GENERAL_SPECIFIC_RD':('RD física source-bound de Auren35/Feryn22 aplicada em respostas de contra-ataque e golpes nativos, sem inventar resistência especial.','RD Dark60 em ação tipo Dark realmente autorizada; dano misto, concorrência RD geral/específica e Lightning ainda sem ficha.'),
'ITEM_EQUIPMENT_AND_ENHANCEMENTS':('Bônus equipados do snapshot preservados na validação de CA, inic, reflex e dano; nenhuma carga/item ativo novo.','Inventário com IDs, ativações, desativação, cargas, reação e rollback.'),
'OFFICIAL_QA_NAC_LEDGERS':('3 cenas e 3 escalas auditadas sem importar resolvedor; 8/8 rejeições pré-commit, 2 crash gates novos PASS, 28 regressões nativas.','Auditoria externa competente, 20 gates originais, todos contratos oficiais e NFC/NAC-PASS terminal.'),
'PA_AND_PREBUFF_COSTS':('Verificado que as reações sem custo não consomem indevidamente PA dos perfis; R117 quatro Descargas 55PA continuam base legítima.','Cenas com PA positivo e reações/prebuffs simultâneos, manutenção temporal, insuficiência e falha em escala.'),
'REACTION_TRIGGER_AND_SINGLE_USE':('R119/121 9 declarações de Contra-atacar: 8 respostas após erro e 1 suprimida por crítico autoacertador; 7 Esquivas e 3 Defender; 8 pré-rejeições, segundo gatilho sem slot rejeitado, R51 nesting blocked; crash gates.','Reação contra magia, AoO geometria verdadeira, dois gatilhos efetivamente simultâneos e prioridade competente, nested non-counter paths.'),
'RNG_REPLAY_STATISTICS':('3/3 replays multiator (75 eventos) + 3/3 escala (388 eventos), incluindo desempates R26 e validação da fita RNG por auditor de biblioteca padrão.','Certificação externa de holdout cego, independência por famílias, cobertura de efeitos e comparabilidade das políticas.'),
'SOURCE_FREEZE_AND_RANK':('Iniciativa natural do Auren 6d6+166 e Feryn 4d6+82 documentadas; decisão R50/R51 recuperada; nenhuma atribuição de Iniciativa da Besta.','Competência individual Besta, materialização de fontes, versionamento dos perfis e autorizações.'),
'TACTICAL_AI_AB_FAIRNESS':('Políticas fixas e mudança de alvo documentadas; 20x20 a partir de dois perfis clonados sem simular diversidade.','Contrafactuais por política balanceados, múltiplos papéis ED e holdout cego por famílias.'),
'TRANSFORMATION_OVERLAY_AI08':('Sem ativação; conflito de custo Auren preservado 100PA+15/turno vs 320PA regra especializada.','Aplicar NAC-NORM-01 competente, snapshot transformado verificado e prova de custo/duração/eventos.'),
'TRANSFORMATION_PER_SCENE_AI09':('Histórico mantido sem nova execução; R124 testa apenas modo NORMAL.','Regra T9 por cena/descanso, instanciação, persistência e reversões.'),
'TURN_SCHEDULER_EVENT_SOURCING':('3 atores com iniciativa natural validada, R26 desempate apenas empatados, 75 eventos; escala 10x10 118 eventos, 20x20 232, 5x5 38 censurados; R18 WAL transacional e fault PASS.','Prioridade simultânea/nested adicional, efeitos/PA/condições em três+ atores, escalabilidade canônica e parecer externo.')}
assert set(updates)=={r['id'] for r in a['rows']}
new=[]
for row in a['rows']:
 id=row['id'];new.append({'position':row['position'],'id':id,'original_requirement_verbatim':row['original_requirement_verbatim'],
 'ANTES_R117':row['DEPOIS_R117'],'DEPOIS_R125':{'new_integrated_evidence':updates[id][0],
 'minimum_remaining':updates[id][1],'status':'PARTIAL_LAB_ONLY','terminal_certified':False,
 'independent_audit':'COLD TECHNICAL only, not official independent homologation',
 'NAC_PASS':'PASS BOUNDED LOCAL; TERMINAL HOLD'},'source_R105_SHA256':row['source_R105_SHA256']})
out={'operation':'OP-VLAB-FUSION-SANDBOX-01','AS_OF':'2026-10-16','baseline':'R01–R117 unchanged',
 'fixed_denominator':17,'terminals':0,'source_original_matrix_sha':dig(SRC/'R117_17_CONTRACTS_BEFORE_AFTER.json'),
 'SCIENTIFIC_SCOPE':'LAB_ONLY','rows':new}
wr(ROOT/'R125_17_CONTRACTS_BEFORE_AFTER.json',out)

lines=['# VLAB — R125 Matriz ANTES/DEPOIS dos 17 contratos (MESTRE-SIDE)','',
 '**OP:** OP-VLAB-FUSION-SANDBOX-01 · **Baseline:** R01–R117 intocada · **Terminal:** 0/17','',
 'As linhas conservam IDs e requisito terminal literal R105/R117; evidência nova é local, não certificação.','']
for row in new:
 lines += [f"## {row['position']:02d} — `{row['id']}`",'',
  f"**Requisito terminal original:** {row['original_requirement_verbatim']}",'',
  f"**ANTES R117:** {row['ANTES_R117']['new_scoped_functional_evidence']}",'',
  f"**DEPOIS R125:** {row['DEPOIS_R125']['new_integrated_evidence']}",'',
  f"**Menor restante:** {row['DEPOIS_R125']['minimum_remaining']}",'',
  '**Certificado:** NÃO · **NAC-PASS terminal:** HOLD','']
(ROOT/'R125_17_CONTRACTS_BEFORE_AFTER.md').write_text('\n'.join(lines)+'\n')

# New source-limited receipts: each executed hit/strike/reaction is one event occurrence, not independent statistical draw.
rows=[]
allfiles=[p for p in sorted((ROOT/'runs').glob('R119*.sqlite')) if '.checkpoint' not in p.stem]
allfiles +=[p for p in sorted((ROOT/'runs').glob('R124_TECH_SCALE_*.sqlite')) if '.checkpoint' not in p.stem]
for file in allfiles:
 with sqlite3.connect(file) as c:
  meta=dict(c.execute('select key,value from meta'));st=json.loads(meta['state'])
  chain=[json.loads(x[0]) for x in c.execute('select row_json from events order by seq')]
 seed=st['seed'];size=len(st['actors']);family='R119_3ACTOR' if size==3 else f'R124_{size//2}X{size//2}'
 result='CENSORED_PRE_INTENT' if size==10 else st['phase']
 for evt in chain:
  if evt['kind']!='STRIKE':continue
  rlist=evt['detail']['native_actions']
  for x in rlist:
   if x['action'] not in ('weapon_attack','COUNTER_RESPONSE'):continue
   typ='COUNTER_RESPONSE' if x['action']=='COUNTER_RESPONSE' else 'NORMAL_ATTACK'
   actor=x['from'];target=x['to'];prof=st['actors'][actor]['source_profile'];tprof=st['actors'][target]['source_profile']
   hp_before=x['before_hp'];hp_after=x['after_hp'];raw=x.get('raw',0);net=x.get('net',0)
   rows.append({'run_id':st['run_id'],'seed':seed,'family':family,'scene_phase':result,
     'event_seq':evt['seq'],'action_index':x['seq'],'attack_origin':typ,'actor_instance':actor,'source_actor_profile':prof['source'],
     'target_instance':target,'source_target_profile':tprof['source'],'critical':x.get('critical','NONE'),
     'attack_score':x.get('roll_score'),'hit':x.get('hit'),'raw':raw,'rd_applied':x.get('rd_applied'),
     'effective_post_rd':net,'hp_loss_actual':hp_before-hp_after,'overkill':x.get('overkill'),
     'hp_before':hp_before,'hp_after':hp_after,'pa_cost':'0 BASIC/REACTION; no spell in this batch',
     'source_authority':'Notion Master-side precreation/source character + Combat R4/R6 + Mestre R50/R51',
     'statistical_independence':'SCENE_SEED_FAMILY_NOT_INDEPENDENT_ATTACK','status':'LOCAL_COLD_PASS',
     'official_credit':0})
assert len(rows)==165,len(rows)
with (ROOT/'R125_NATIVE_RECEIPTS_165_FOR_DMG.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

science={'A':{'positions':25,'official':0,'new_evidence':'R119 1x2 Auren vs clones Feryn technical; mixed rank NPC no power inference'},
 'B':{'positions':27,'official':0,'new_evidence':'Grifo L2 experimental R104 unchanged; no Beast natural initiative'},
 'C':{'positions':25,'official':0,'new_evidence':'5x5/10x10/20x20 cloned technical scheduler not 25-rank effectiveness'},
 'D':{'positions':27,'official':0,'new_evidence':'seven candidate species retained, no new species, no unique official spot filled'},
 'extra':{'new_runs':6,'completed':5,'censored':1,'multiactor_3_completed':3,'scale_5x5':'CENSORED','scale_10x10':'COMPLETE_TECH','scale_20x20':'COMPLETE_TECH',
 'events_3actor':75,'events_scale':388,'attacks_normal':152,'counter_responses':13,'attack_receipts':165,
 'seeds_numeric':sorted(set(x['seed'] for x in scale)|{918201,928801,918515}),
 'independence':'No three clones are independent characters; seeds and actions within one scene correlated; no certified blinded holdout'}}
wr(ROOT/'R125_SCIENCE_A_B_C_D.json',science)

oldmodule=SRC/'native_v081_controlled/vlab_effects_v08.py';newmodule=ROOT/'native_v081_controlled/vlab_effects_v08.py'
diff=list(difflib.unified_diff(oldmodule.read_text().splitlines(keepends=True),newmodule.read_text().splitlines(keepends=True),fromfile='R117/native_v081_controlled/vlab_effects_v08.py',tofile='R125/native_v081_controlled/vlab_effects_v08.py'))
(ROOT/'R125_ADD_ONLY_V081_DIFF.patch').write_text(''.join(diff))
wr(ROOT/'R125_NATIVE_PROVENANCE.json',{'historical_R117_SHA256':dig(oldmodule),'controlled_R125_SHA256':dig(newmodule),
 'patch_SHA256':dig(ROOT/'R125_ADD_ONLY_V081_DIFF.patch'),
 'R50_R51_citation':'Notion existing OP page 3f3c2b324ede819496ddd7f93bd7e5d2',
 'role':'append-only counter trigger/response into same module; version string changed; R18 and R26 original files untouched',
 'actual_executable':str(newmodule),'baseline_ZIP_SHA256':dig(BASE.parent/'VLAB_R108_R117_NATIVE_CRITICO_FRACO_DESCARGA_MESTRE_ONLY.zip'),
 'no_new_motor':True,'historical_db_write':False})

(ROOT/'R125_DMG_ROUTE_READONLY.md').write_text('''# VLAB R125 — Handoff científico à operação DMG existente (MESTRE-ONLY)\n\n**STATUS:** PREPARADO LOCALMENTE / ACK DMG AUSENTE / NO WRITE NO DOMÍNIO DMG.\n\n- Arquivo novo `R125_NATIVE_RECEIPTS_165_FOR_DMG.csv`: 165 ocorrências técnicas (152 ataques normais + 13 respostas de contra-ataque), seis cenas, sementes 918201, 918515, 928801, 938211, 938311 e 938411.\n- R119 3/3 cenas completas; R124 10x10 e 20x20 completos; 5x5 censurado por falha crítica sem consequência antes do intent.\n- Cada registro mantém RUN-ID, seed, tipo, atacante/alvo, fonte Mestre-only, bruto, RD física, efetivo, Vida retirada, overkill e crítico.\n- Feryn é NPC Ouro Negro 5 sem Espírito Demoníaco; dois perfis são repetidos em até 40 instâncias técnicas. Nenhuma equivalência de potência ED/Bestas, nenhuma probabilidade de vitória generalizável.\n- Não concatenar com R97 1344 ou R116 212 sem reconciliar fonte, versão, classe, política, censura e unidade de análise.\n- **Histórico:** R97 mantém errata de 6 críticos R93/R95 e `TECHNICAL_REPLAY_PASS / NORMATIVE_PARITY_HOLD`; R116 contém 212 recibos base R117 e handoff não aceito. Ambos residem no ZIP R117 imutável embutido no pacote R125.\n- **Oficial:** DMG-RANK-01 v1.1 não alterado; sem ACK, sem writer DMG, sem importação para corpus oficial.\n''')

print(json.dumps({'contracts':len(new),'receipts':len(rows),'files':len(allfiles),'new_critical_events':cold['totals']['criticals'],
 'integrated_3_actor_events':cold['totals']['event'],'scale_events':sum(z['events'] for z in scale)},indent=2))
