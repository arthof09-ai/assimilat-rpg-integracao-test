import json,pathlib,hashlib,csv
root=pathlib.Path(__file__).resolve().parents[1]
from r174_source_duel import ACTORS,EXCERPTS,COMBAT,VERSION
sv=[]
for k,f in ACTORS.items():
 sv.append({'actor_id':k,'uuid':f['source'].split('/')[-1],'url':f['source'],'name':f['name'],'last_edited_at':f['last_edit'],'authority':'NOTION_MESTRE_PAGE_PROPOSTA_ENCONTRO','source_status':f['status'],'rank':f['rank'],'source_fields':f,'selected_excerpts':EXCERPTS[k],'selected_excerpt_sha256':hashlib.sha256(EXCERPTS[k].encode()).hexdigest(),'full_notion_binary_signature':False})
(root/'sources/R174_FROZEN_SOURCES.json').write_text(json.dumps({'as_of':'2026-10-18','read_only_connected_notion':True,'combat_page':COMBAT,'actors':sv,'system_excerpts':{k:v for k,v in EXCERPTS.items() if k not in ACTORS},'policy':'NO_CANON_NO_PARTY_NO_ORIGINAL_EDIT','notion_full_page_hashes':False},ensure_ascii=False,indent=2))
rows=[]
for k,f in ACTORS.items():
 for field in ['hp','pa','ca','rd','init_base','hit_base','damage_n','damage_faces','flat','armor','fort','reflex','power_pa']:
  val=f.get(field)
  rows.append({'actor':k,'field':field,'value':val,'source_url':f['source'],'source_version':f['last_edit'],'authority':'MESTRE_PROPOSTA','completeness':'DOCUMENTED' if val is not None else 'NOT_REQUIRED_FOR_TEST_PHYSICAL_ONLY' if field=='power_pa' else 'PENDING','conflict':'NONE_OBSERVED_IN_SELECTED_EXCERPT','effect_scope':'TEST_ONLY'})
for k,field,desc in [('SCENE','initial_position','EXPLICIT_ONE_BLOCK_ADJACENCY_TEST_INPUT'),('SCENE','movement','NOT_EXECUTED'),('SCENE','future_holds','NO_INDEPENDENT_HOLDOUT'),('SCENE','ED_ELIGIBILITY','NONE_BOTH_ARE_NON_ED_NPCS'),('SCENE','canonical_status','PROPOSAL_NOT_CANONIZED')]:
 rows.append({'actor':k,'field':field,'value':desc,'source_url':COMBAT,'source_version':'2026-10-07T23:51:04.971Z','authority':'EXPERIMENTAL_SCENARIO_INPUT','completeness':'SCOPE_LIMIT' ,'conflict':'NOT_PROMOTED','effect_scope':'TEST_ONLY'})
(root/'sources/R174_FIELD_ADMISSIBILITY.json').write_text(json.dumps({'scope':'SOURCE_DERIVED_MELEE_PHYSICAL_1X1_PROPOSAL_TEST','fields':rows,'source_admissibility':'MECHANICAL_SELECTED_FIELDS_VALID_FOR_SANDBOX;NOT_ED_BESTA_BENCHMARK_OR_CAMPAIGN','fully_official_admissible':False},ensure_ascii=False,indent=2))
old=json.loads((root/'deps/r173_work/R173_CONTRACT_DELTA.json').read_text())
evidence={
 'ACTOR_SNAPSHOT_SCENARIO':'Two Notion Mestre ON5 encounter-proposal snapshots frozen with URLs/last-edit and expected field matrix; no fictional ED status',
 'SOURCE_FREEZE_AND_RANK':'Varok and Arveth source UUID/version/excerpt pointers, formulas, rank preserved; proposal vs official distinguished',
 'REACTION_TRIGGER_AND_SINGLE_USE':'Native DEFENDER prevents HP loss with 40 HP directed discriminant; 10 or 11 consumed over 11-12 legitimate own-turn refreshes; attack-first declaration and sqlite receipts',
 'TURN_SCHEDULER_EVENT_SOURCING':'Source-specific ON5 initiatives 4d6+29 vs 4d6+25; 2-actor turn handoff, begin_source_turn, end_source_turn, KO termination, checkpoint replay',
 'RNG_REPLAY_STATISTICS':'DEV seed 1740101 paired per-actor-turn dice tape; 3 dependent policy executions; deterministic cold math audit; NO independent blind holdout',
 'PA_AND_PREBUFF_COSTS':'Varok Quebra do Tronco source-literal 60 PA once/scene, single RD; compared post-hit energy to no-energy exploratory policy; no equipment commitment double-charging',
 'TACTICAL_AI_AB_FAIRNESS':'Paired policy DEFEND_VAROK vs HOLD_VAROK vs exploratory DEFEND_NO_POWER; 437 HP preserved by DEFENDER; 60 PA rider shortened fight from 23 to 21 attempts',
 'BATTLE_1X1_2X1_20X20':'One NEW source-proposal matchup, 3 paired TEST executions (not 3 independent adversaries), no 2x1/20x20; no official ED/Besta full source battle',
 'GENERAL_SPECIFIC_RD':'Source physical RD 35 Varok and 30 Arveth; RD once for source rider; 5 semantic hash-rebuilt clones rejected',
 'ITEM_EQUIPMENT_AND_ENHANCEMENTS':'Uses source-listed Varok axe item power Quebra do Tronco on hit (60 PA, 6d12 Impacto) without creating item/recipe'
}
for row in old['rows']:
 row['R174_new_executed_evidence']=evidence.get(row['id'],'NONE_NEW')
 row['terminal_certified']=False
 row['remaining']='Terminal original requires full contract breadth, external independent auditor, documented authority/approval and NAC-PASS; current test on two proposed NPCs only'
old['R174_terminals']=0;old['official_cells']={'before':0,'after':0,'denominator':1875}
old['original_denominator']=17;old['R174_as_of']='2026-10-18'
old['R174_source_admission']='ONLY_SELECTED_MASTER_SIDE_PROPOSED_NPC_MECHANICS_FOR_TEST'
(root/'R174_17_CONTRACT_CROSSWALK.json').write_text(json.dumps(old,ensure_ascii=False,indent=2))
(root/'R174_ERRATA_R173_MESTRE_ONLY.md').write_text('''# ERRATA DOCUMENTAL DERIVADA — R173, SEM ALTERAR PACOTE HISTÓRICO

**ERRO NO PSV PARCIAL:** a primeira seleção textual mencionou **Auren L3 × Serpente Prismática Regente L3**, quando o pacote executado e auditado contém **Sikong Auren L3 × Leviatã de Ferro Mnemônico L4**. A Serpente era apenas candidata de triagem, não oponente executado. Esta errata não executa novo confronto nem reabre efeitos R173.

| Entidade | Identidade física | Posição correta |
|---|---|---|
| Auren | `3ebc2b324ede814bb730d47dd7bd5f02` | ED Lendário 3, participante R173 |
| Serpente Prismática Regente | `BEAST-FULLSPEC-VZ-06`, precriação Lendário 3, HP4315 CA169 RD75 Alma4752 | candidata não executada |
| Leviatã de Ferro Mnemônico | `BEAST-FULLSPEC-VZ-06`, pré-criação Lendário 4, HP6060 CA110 RD75 Alma4260 | besta efetivamente executada em R173 |

**R173 verdadeiro:** duas políticas sobre uma única seed DEV 1730101, 71 ataques em cada execução, 72 commits em cada banco, 0 benchmark oficial; não tratar duas políticas como dois adversários independentes. `ALWAYS_DODGE` deve ser descrita como **tentar Esquivar na primeira oportunidade com Reação disponível** (sem renovação normativa demonstrada), não 36 Esquivas. Nenhuma alteração aos ZIPs históricos. A classificação R173 permanece cenário condicionado, não FULL-SOURCE-ADMISSIBLE.
''')
(root/'R174_HOLDOUT_PLAN_PENDING.json').write_text(json.dumps({'as_of':'2026-10-18','status':'PENDING_EXTERNAL_INDEPENDENCE','development_seed':1740101,'directed_tape':'predeclared Arveth 4d6 4+4+4+4; crit 2,3,4; damage eight 5; Varok CA83 Defender99','policy_defend':'use DEFENDER for Varok on first eligible announced Arveth attack before RNG, if reaction available','policy_hold':'hold reaction','third_exploratory_policy':'DEFEND_NO_POWER added after initial two DEV results, not preregistered blind','holdout_seed_count_proposed':8,'selection':'external coordinator/auditor freezes source, code and policies first; supplies hidden seeds and only then executes independent holdout','result':'NONE_EXECUTED','independent_observations':0,'statistical_wins_not_claimed':True},indent=2))
print('docs created')
