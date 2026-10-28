# HANDOFF R105 → DMG — Recibos de dano R97 sem dupla contagem

**Origem:** CM-000006 VLAB / OP-VLAB-FUSION-SANDBOX-01. **Destino proposto:** CM-000001 / OP-DMG-CORPUS-EMP-01 (somente leitura; sem escrita/ACK na operação DMG). A análise científica do dano permanece exclusiva do DMG; este pacote não muda DMG-RANK-01 v1.1.

## Arquivo principal autenticado

- `R97_ATTACK_RECEIPTS_1344_FOR_DMG.csv` na Biblioteca original `/Comestre/OP-VLAB-FUSION-SANDBOX-01/`, sem sobrescrever.
- `SHA256` do arquivo congelado: `2fd252f2656e11e5dce273c2b7d2857a0f6470b84c9db53d663b6396e89c3740`.
- Manifesto de runs: `R97_VALIDATED_RUNS_24.csv`; hash `f7c1d781722294395bb1dd06f48a7bff84aed6382344a18a0b3a85a173bf72a5`.
- **Denominadores históricos**: 1.344 parcelas de ataque / 24 RUN-IDs / **12** grupos `(matchup, seed)` espelhados. NÃO são 24 amostras independentes. R95 utiliza as mesmas duas seeds em vários confrontos: dependência cruzada preservada.

## Dados separados por coorte

| Coorte | Runs | Blocos `(matchup, seed)` | Ataques | Acertos | Críticos + | Bruto registrado em acertos | Potencial pós RD | Vida efetiva retirada | Overkill | Censuras |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| R95_BASIC_FIXED_OPENING | 16 | 8 | 892 | 452 | 4 | 110836 | 77096 | 76168 | 928 | 8 |
| R93_TEAM_2X1_BASIC | 8 | 4 | 452 | 258 | 2 | 56320 | 39620 | 38352 | 1268 | 0 |

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
