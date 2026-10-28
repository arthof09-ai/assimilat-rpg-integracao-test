# PSV — VLAB / R138–R145 | integração multirrodada e recuperação temporal

**AS-OF:** 16/10/2026, Recife · **OPERATION:** `CM-000006 / OP-VLAB-FUSION-SANDBOX-01` · **MESTRE-SIDE** · **BASELINE:** R01–R137 preservada sem nova escrita · **LAST-VERIFIED-UNIT:** R145 após readback independente (ver recibo de ZIP) · **FIRST-PENDING:** expiração normativa de efeitos de 3 turnos, ataque Dark admissível para RD específica, origem equipada de sangramento e combate fonte-completo com vencedor legítimo.

## ANTES, execução e DEPOIS

**ANTES:** R137: três cenas de uma rodada, 32 commits, Capa/Marca/AoO/Reconstituição, corrigido problema de serialização R130; R125 multiator/escala; R117 crítico reparado; R42 decisão experimental anterior do Mestre sobre falha crítica negativa; contratos terminais 0/17. Incidentes R123/R130/R134, R124 censurado intocados. Readback R137 administrativamente corrigido para **15/15 arquivos comparados**, comprovante adicional recuperado separadamente pela Coordenação; nenhum upload corretivo nem duplicata R137.

**R138 — cena nova tecnicamente contínua, seed 991402, 4 rodadas, 3 atores distintos de fonte:** Sikong Auren ED L3 (ficha Mestre-side); Sikong Feryn e Sikong Eristan ON5, fichas **Mestre-side propostas e SEM Espírito Demoníaco**. Ordem individual de iniciativa da própria ficha, R26 DES/tie. 12 turnos próprios; **40 commits R18, 43 registros de efeitos nativos, 3 ataques** (2 Padrão físicos + 1 Ataque de Oportunidade); Capa de Poeira35PA, Marca25PA, Passo da Fuligem25PA, Reconstituição75PA ×4, Pulso de Estabilização45PA. Dano físico **672 PV efetivos**, cura **411 PV efetivos**, PA total **430** (Feryn85, Eristan345). Auren 523 PV/719 PA, Feryn218 PV/339PA, Eristan630 PV/459PA no fim. **CENSORED_HORIZON / NO WINNER** após quatro rodadas, NÃO duelo completo/cientificamente comparável. Os turnos sem ataque de Auren são escolha dirigida pela política laboratorial, não IA tática competitiva.

**R138 temporalidade:** `Passo da Fuligem` fonte diz `este turno`, ativação no turno próprio de Feryn +12 m no seu deslocamento e fim no `END` do mesmo turno, sem multiplicar Movimento; expiração causal comprovada. `Marca dos Passos Perdidos` permanece +10 só Percepção/Sobrevivência (nunca Luta), sem atravessar paredes, e exige fixação competente do exato marco de vencimento dos `três turnos`; dados de ativação e início de turnos preservados; no limite é `HOLD_EXACT_3_TURNS`, sem remoção inventada. O bônus de Passo não converte B0–B3 em metros: alcance métrico das habilidades é uma **premissa física específica do cenário**, separada da topologia B0–B3 experimental.

**R139:** auditor stdlib independente, sem importar o resolvedor v0.8.1/R18/R138, reconstituiu **40/40 transações**, 43 subeventos, stream SHA-RNG experimental, iniciativa, R26 para o caso sem empate, PA/HP, cura e luvas, retorno do slot, Movimento, RD física22, crítico, ações e expiração, todos os `before_sha/after_sha` e head final. Não valida dado físico/canônico nem holdout cego.

**R140:** extração a frio do **prefixo de 20 commits**, após segunda rodada. Base existente não foi reexecutada: copiou-se apenas registros duráveis e reconstruiu-se snapshot prefixo do auditor. A cópia foi reaberta com o leitor nativo R18, `prefix_rev20 PASS`, HP A523/F435/E630, PA A719/F339/E654. **É CHECKPOINT RECONSTRUÍDO A FRIO, não salvamento contemporâneo**, e não prova retomada de um motor em execução naquela hora.

**R141/R142:** fixture nova de Eristan (Feryn com 14 PV faltantes, condição de laboratório pré-cena, não lesão histórica), `8d10`+25+Luvas20 = **96 bruto**, **14 efetivo**, **82 excesso**, PA **804→729**, alvo 465→479. Auditor independente reconstituiu commit e dados. Mais **6/6 rejeições PRÉ-INTENT**: Vida cheia, PA74, sem Padrão, alcance6m, alvo Vida0, fita RNG errada; nenhum evento, pending ou efeito nesses bancos. Duas cópias de ledger de R138 semanticamente adulteradas e re-hashadas (PA75→0 e remoção temporária12→0), **2/2 rejeitadas** pelo auditor independente; cópias adversariais rotuladas e isoladas, originais imutáveis.

**R143/R144:** duas falhas reais de processo sobre Passo (25 PA) em bancos novos. `AFTER_INTENT`: pending1, rev0, PA424 e Movimento1 íntegros, core.load rejeita `UNKNOWN_EFFECT`; **SEM RETRY**. `AFTER_COMMIT`: rev1, PA399 e Movimento0, efeito ativo; readback físico; então dois comandos NOVOS `FOREGO`, `END` publicaram rev2–3 e expiração; PA continua399, nenhuma ativação duplicada. Auditor stdlib independente 2/2, sem importar engine. Esses casos não são novos combates.

**R145 / suíte histórica:** 59/59 testes unitários existentes passaram sobre a cópia v0.8.1 aditiva; 28/28 mínimo histórico também preservado, sem reexecutar combates anteriores. `R145_NATIVE_ADDITIVE_PATCH.diff` demonstra modificações em um arquivo da mesma linhagem, acrescentando `apply_passo_fuligem` e `apply_pulso_estabilizacao`, com `_require_option`/ActionCatalog, `Scene`, e RD v0.8.1 originais. Não foi construído motor alternativo.

## Autoridades normativas e limites localizados

- **Falha crítica negativa**: ao reabrir a OP original, **R42** já registra decisão expressa LAB-ONLY do Mestre: 1-1-1 / 1-1-2 dão **erro automático**, 0 dano e Ação consumida, sem perda de arma/autodano/penalidade extra. Evidência técnica R42 é histórica, não prova nova executada R145. O caminho de ataque R138 ainda bloqueia crítico negativo antes da intenção: **integração com resolvedor corrigido é FIRST-PENDING**, sem inventar regra universal. R124 5×5 censurado NÃO é reclassificado.
- **Marca**: marco exato `3 turnos` não encontrado no Sistema de Combate atual, Sistema de Magia e fichas Mestre-side consultados. Vencimento=HOLD. Passo `este turno` não tem essa ambiguidade e passou.
- **Sangramento**: não existe criatura equipada elegível e congelada nas três fichas de R138, embora haja registros históricos de aprimoramento no acervo; nenhum tick, dano ou cura de sangramento inventados. `SOURCE-HOLD` localizado.
- **RD específica**: Auren tem RD Dark60, física35, mas nenhum dos três atores R138 apresenta ataque Dark específico admissível contra ele. RD física22 de Feryn aplicada a três golpes. Nenhuma RD Dark integrada, nenhum stacking, nenhuma redução de componentes mistos sem fonte.
- **Transformação Auren**: Sistema de Combate e transformação especializada exigem Lendário320PA; ficha específica 100PA+15/turno; NAC-NORM-01 pendente, nenhuma transformação ativada.
- **Geometria/Alcance**: B0–B3 são vértices de topologia não métrica. Distâncias de 1,5m, 2m e 3m registradas como pressupostos explícitos e condicionais do cenário, não conversão universal. AoO pelo evento de saída adjacente, reação única, não em movimento forçado.

## Ciência de potência e coortes DMG

A: 25 arquétipos ED, sem nova referência (só Auren tem Espírito); B: 27 patamares da MESMA linhagem Grifo (L2 derivada, L3 documento), não houve duelo novo; C: 25 patamares de equipes, um 1×2 de técnica Feryn/Eristan SEM ED e censurado NÃO preenche painel; D: 27 Bestas distintas, ADM26 e Divina27 acima de L5, nenhum novo exemplar homologado. **0/1875 células oficiais**; 1 seed de desenvolvimento, não holdout independente; sem taxa de vitória.

`R145_DMG_ATTACK_RECEIPTS_3.csv` preserva 3 ataques de R138 em coorte independente; reporta brutos, RD, PV, overkill, reações e censura. Não adicionar automaticamente aos 7 R137, 165 R125, 212 R116 nem 1344 R97. Errata R93/R95 `TECHNICAL_REPLAY_PASS / NORMATIVE_PARITY_HOLD` permanece imutável. Handoff DMG **PREPARADO somente na Biblioteca VLAB, ACK ausente**, sem escrita na OP-DMG.

## Denominadores e NAC-PASS

- **17/17 contratos históricos** reconciliados na matriz `R145_17_CONTRACTS_BEFORE_AFTER`, mesmos nomes e critérios originais; **0/17 certificados terminais**, 0/1875 células. Prova local R138 não atende requisito original de combate completo 2×1 ou 20×20 canônicos.
- **ANTES/DEPOIS material:** R137 3 cenas curtas; R145 +1 cena nova de 4 rodadas e 40 commits, +1 cura-cap fixture de um commit, +6 negativas pré-intent, +2 fault banks novos, +2 redteams rehashed e prefixo reconstruído. Não contar fixtures, adversários ou prefixo como combates.
- **NO-REPEAT:** R01–R137, IDs e seeds 943207/953209/963212, incidentes R123/R130/R134, R124 5×5 censurado, old R93/R95, tudo intocado. R138 seed991401 tem banco **pré-gênese abortado rev0/events0/pending0**, isolado em `quarantined`; não é replay/duelo, seed991402 é o fallback previamente reservado (NÃO holdout cego). R143 AFTER_INTENT novo fica em `UNKNOWN_EFFECT/HOLD`. Não retomar automaticamente.
- **Writer:** CM-000006 `PAUSED`, sem `INSTANCE-ID`, writer, lease, epoch, fencing ou ACK IBX-101 verificados; não houve escrita na OP, Diário, Party, O Primeiro, fichas, regra ou DMG. Biblioteca VLAB é armazenamento de artefatos experimental permitido pela ordem.
- **NAC-CONT-03:** LER → estado ANTES → executar somente em cópia → reopen/chain/auditoria → DEPOIS/checkpoint/PSV. **NAC-PASS:** PASS técnico local para os caminhos evidenciados; terminal/release/produção **HOLD**.

## NEXT-5 (ponto exato de retomada)

1. Implementar decisão **R42 LAB-ONLY** de falha crítica negativa na extensão do resolvedor corrigido, sem tocar R124 censurado e sem canonizar globalmente.
2. Reconciliar contagem de expiração da Marca de 3 turnos em autoridade competente; caso não resolva, preservar HOLD e implementar duração de outras fontes inequívocas.
3. Construir segundo confronto multirrodada com políticas não abdicativas e condições de vitória fonte-suficientes, sem alterar source snapshots nem confundir NPCs ON5 com ED.
4. Encontrar ataque Dark completo admissível e equipamento de sangramento efetivamente usado em perfil fonte elegível; ensaiar RD/bleed em cenários separados, sem generalizar ausência de regra.
5. Preparar handoff e ACK de DMG por rota competente, depois expandir matriz original 17 contratos com novas provas e NAC-PASS terminal somente quando todas as dependências originais satisfizerem.

**TARGET-REMAINDER:** 17 contratos ainda sem terminal; cobertura global completa de requisitos não quantificável em percentual; fontes, efeitos e espécies incompletos são denominadores diferentes. R145 reduz dívida de ciclo temporal, suporte reativo e cura com cap, mas não a dívida integral.
