from pathlib import Path
import csv,collections,json,hashlib
R=Path(__file__).resolve().parent
P=R.parent/'r92_r101'/'R97_ATTACK_RECEIPTS_1344_FOR_DMG.csv'
runP=R.parent/'r92_r101'/'R97_VALIDATED_RUNS_24.csv'
rows=list(csv.DictReader(P.open()));runs=list(csv.DictReader(runP.open()))
assert len(rows)==1344 and len(runs)==24
out={'source_csv_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),
     'run_manifest_sha256':hashlib.sha256(runP.read_bytes()).hexdigest(),
     'original_library':'/Comestre/OP-VLAB-FUSION-SANDBOX-01/R97_ATTACK_RECEIPTS_1344_FOR_DMG.csv',
     'source_operation':'OP-VLAB-FUSION-SANDBOX-01',
     'destination_intended':'CM-000001 OP-DMG-CORPUS-EMP-01 READONLY_HANDOFF_PENDING_COMPETENT_ROUTING',
     'authority':'MESTRE_SIDE; no write in DMG operation',
     'batch_rules':'Original R97 unchanged; R102 errata compensates only selected critical events; no corrected combat outcome claim',
     'columns':['run_id','cohort','matchup','seed','group','side','event_seq','actor','target','actor_source','rank','dice','fixed_bonus','roll_tape','score','ca','hit','crit_plus','crit_minus','raw','rd','mitigation_on_hit','net_potential','hp_loss_actual','overkill_potential','hp_before','hp_after','source_gate','audited'],
     'cohorts':{},'flags':['R93/R95 critical mismatch: max face not max all damage dice',
                           'FRACO below10percent and Besta final effort not resolved in R95',
                           'R95 opening exogenous; R93 Besta initiative skill unproven',
                           'PRECREATE_VZ support-origin, not canon physical real sheet',
                           'Mirror sides share seed and do not provide independent trial',
                           'PA paid is 0 in every original R97 attack; R103 PA55 is distinct test and not to add to original attack corpus']}
for cohort in sorted(set(x['cohort'] for x in rows)):
 rr=[x for x in rows if x['cohort']==cohort]
 ids={x['run_id'] for x in rr}
 rsel=[x for x in runs if x['run_id'] in ids]
 assert len(rsel)==len(ids)
 fields=['hit','crit_plus','crit_minus','raw','net_potential','hp_loss_actual','overkill_potential']
 sums={x:sum(int(y[x]) for y in rr) for x in fields}
 out['cohorts'][cohort]={**sums,'attacks':len(rr),'runs':len(ids),
    'mirror_blocks':len(set((y['matchup'],y['seed']) for y in rr)),
    'distinct_seed_values':len(set(y['seed'] for y in rr)),
    'censored_runs':sum(y['phase']!='COMPLETE' for y in rsel),
    'source_gates':sorted(set(y['source_gate'] for y in rsel)),
    'max_actor_turn_horizon':max(int(y['turn_limit']) for y in rsel),
    'rank_versions':sorted(set(y['rank'] for y in rr))}
assert sum(x['attacks'] for x in out['cohorts'].values())==1344
assert sum(x['hit'] for x in out['cohorts'].values())==710
assert sum(x['hp_loss_actual'] for x in out['cohorts'].values())==114520
(R/'R105_DMG_INTEROP_RECEIPT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
md='''# HANDOFF R105 → DMG — Recibos de dano R97 sem dupla contagem

**Origem:** CM-000006 VLAB / OP-VLAB-FUSION-SANDBOX-01. **Destino proposto:** CM-000001 / OP-DMG-CORPUS-EMP-01 (somente leitura; sem escrita/ACK na operação DMG). A análise científica do dano permanece exclusiva do DMG; este pacote não muda DMG-RANK-01 v1.1.

## Arquivo principal autenticado

- `R97_ATTACK_RECEIPTS_1344_FOR_DMG.csv` na Biblioteca original `/Comestre/OP-VLAB-FUSION-SANDBOX-01/`, sem sobrescrever.
- `SHA256` do arquivo congelado: `{sha}`.
- Manifesto de runs: `R97_VALIDATED_RUNS_24.csv`; hash `{runs_sha}`.
- **Denominadores históricos**: 1.344 parcelas de ataque / 24 RUN-IDs / **12** grupos `(matchup, seed)` espelhados. NÃO são 24 amostras independentes. R95 utiliza as mesmas duas seeds em vários confrontos: dependência cruzada preservada.

## Dados separados por coorte

| Coorte | Runs | Blocos `(matchup, seed)` | Ataques | Acertos | Críticos + | Bruto registrado em acertos | Potencial pós RD | Vida efetiva retirada | Overkill | Censuras |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{row1}
{row2}

`Dano bruto` em R97 inclui bônus de crítico do ADAPTADOR HISTÓRICO; não é dano crítico conforme a regra atual. `net_potential` aplica RD da variante original. `hp_loss_actual` fica limitada pela Vida remanescente, `overkill_potential` não significa dano aplicado. O `R97` original não é retificado retroativamente: usar `R102_R93_R95_CRITICAL_PARITY_ERRATA.json` como delta e **não somar os valores contrafactuais aos resultados sem execução de novo motor**.

## Proveniência e admissão

**R95 (16 duelos; 8 blocos; 8 censuras):** Grifo/Crocodilo L3 de BEAST-FULLSPEC-VZ-06 (especificação de pré-criação Mestre-side), versus Sikong Auren L3 (ficha normal equipada); abertura exógena B/E. R95 omite Fraco/esforço final e contém crítico +face máxima, em conflito com atual Sistema de Combate, devendo ser `HOLD_NORMATIVE_PARITY`; o auditor frio antigo atestou integridade do adaptador, não correção normativa.

**R93 (8 duelos; 4 blocos; 0 censuras):** Grifo L3 contra Auren L3 + Feryn ON5, o último NPC de proposta sem Espírito comprovado, seleção de alvo fixa, sem ações especiais, movimento ou reações. Também contém discrepância crítica +8 em vez de +64 nos dois espelhos da seed 493112. Não é equipe equilibrada homologada.

**Erro de classificação:** jamais chamar Grifo/Crocodilo de fichas live canônicas apenas por haver dossiê e auditoria aritmética; HANDOFF-PRECREATE-VZ-14-01 registra 0/14 materializadas. A Besta Divina Vaelthyr é potência posição 27 nesta escala autoral, não um sexto rank.

## Análises recomendadas ao DMG (sem transferir motor)

1. Separar potencial de acerto comum, crítico automático, dano bruto, RD aplicável, pós-RD e Vida realmente retirada.
2. Reconstruir o efeito corrigido de críticos em cenários NOVOS conforme Sistema de Combate; não corrigir somente totais e alegar replays históricos.
3. Usar blocos `(matchup,seed)` como clusters, condicionar à abertura exógena e espécie, evitar intervalos ingênuos sobre 1.344 ataques correlacionados.
4. Controlar Vida inicial Grifo 4.315 vs Crocodilo 5.580 (diferença 1.265), RD comum 75, CA 153 vs112 e Vida de Auren 523; definir impasses censurados sem vitória fictícia.
5. Evitar fusão com R71/81/91 sem deduplicação física de RUN-ID, ator, efeito e unidade estatística.
6. Manter DMG-RANK-01 v1.1 oficial inalterado e produzir somente hipóteses pesquisáveis.

**Transferência institucional:** este artefato é um HANDOFF preparado e persistido na Biblioteca da operação VLAB; o Inbox/ACK da operação DMG não foi escrito nem concedido.
'''
def line(cohort):
 d=out['cohorts'][cohort]
 return '| '+cohort+' | '+' | '.join(str(d[k]) for k in ['runs','mirror_blocks','attacks','hit','crit_plus','raw','net_potential','hp_loss_actual','overkill_potential','censored_runs'])+' |'
md=md.format(sha=out['source_csv_sha256'],runs_sha=out['run_manifest_sha256'],row1=line('R95_BASIC_FIXED_OPENING'),row2=line('R93_TEAM_2X1_BASIC'))
(R/'R105_DMG_HANDOFF_READONLY.md').write_text(md)
print('handoff',len(rows),out['cohorts'])
