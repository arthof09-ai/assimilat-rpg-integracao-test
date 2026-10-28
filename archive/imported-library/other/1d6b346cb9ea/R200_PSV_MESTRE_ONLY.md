# PSV — VLAB R200 | MARCO TEST EXECUTADO + R201–R203 PARCIAIS

**As-of** 2026-10-20 | **MESTRE-SIDE** | **Produção HOLD** | **Autor lógico** CM-000006 sem INSTANCE-ID verificado, writer/lease/epoch/fencing não reivindicados.

## 01 OPERAÇÃO / IDENTIDADE / AUTORIDADE / BASELINE
Operação única `OP-VLAB-FUSION-SANDBOX-01`; baseline R01–R199 preservada. Primeira ordem consolidada R200–R209 recebida expressamente; nenhuma R200 anterior foi executada. A autonomia experimental do laboratório é expressa, sem promoção de norma, Party, O Primeiro, fichas ou equipamento histórico. Não escrever na OP/Diário compartilhados sem autoria e fencing verificados. Versões históricas, UNKNOWN_EFFECT e R199 `DRY_V1_R199` não retomadas.

## 02 ESTADO ANTES E DEPOIS
**ANTES:** R199 com 32 novos combates, 30 KO, 2 censuras; R198 com 46 concluídos; bancada com cinco abas, sem novos comparativos de armas/armaduras prospectivas. **DEPOIS TEST:** um ED novo Bronze1 e sua projeção Prata1, 32 intenções novas com 30 lutas SQLite finalizadas/auditadas (16 KO, 14 censuras de horizonte) e 2 empates pré-commit; 8 sementes distintas pareadas em duas políticas e dois níveis. 6ª aba preserva cinco anteriores. Fonte LEVEL-UP nativa ainda não atestada para este ator e P1 tem progresso condicional.

## 03 FONTES E VERSÕES RECUPERADAS
- R199 pacote físico SHA256 `533782992f7c16dfd79c06a7113b38d49d4e487cede9f42c1a19d073de0fd015`, 743/743 manifesto, cold `PASS_R199_COLD_PORTABLE_RECOVERY` nesta execução; cópia preservada byte-a-byte dentro do novo pacote.
- Criação Ficha: https://app.notion.com/p/3ebc2b324ede81449222f3c06b840613; Combate https://app.notion.com/p/3ebc2b324ede81f1be4be8804ac113c0; Magia https://app.notion.com/p/3ebc2b324ede81f7b343f7270ff91373; Besta https://app.notion.com/p/3ebc2b324ede81f4992ac88a3588cacd; Transformação https://app.notion.com/p/3f2c2b324ede81c0ae0ee4e66212edc9; DMG-RANK-01 v1.1 https://app.notion.com/p/3f2c2b324ede815498cddb7844245f7e.
- Handoff Mestre com regras prospectivas novas https://app.notion.com/p/3ffc2b324ede81c5a5c3d56cc6a29f84; REC-MOD-ARM-01 https://app.notion.com/p/3f1c2b324ede8140b993cc62063b9649; REC-MOD-ARD-01 https://app.notion.com/p/3f1c2b324ede8116bd3cc6606a1c6687.
- Galinha real Bronze1 https://app.notion.com/p/eddc2b324ede829f8a75011e8acbf429; Lobo P1 https://app.notion.com/p/be5c2b324ede832e8b7a81c5460571c1.
- Anel fonte publicada +2 CA/+2 resistência, 13PA/dia MAS SEM CLASSIFICAÇÃO visível https://app.notion.com/p/168c2b324ede82d6b8ce013ec82217ad.

## 04 ARQUIVOS / CÓDIGO / BANCOS / CHECKPOINTS
`baseline/VLAB_R199_MAGIC_TRANSFORM_BEAST_COMBAT_MESTRE_ONLY.zip`, `new/code/r200_equipment_and_profiles.py`, `r200_geometry.py`, `r200_paired_fights.py`, `r200_read_only_audit.py`, `r200_adversarial.py`, `r200_benchmark_from_receipts.py`, `r200_build_dashboard.py`, `test_r200_geometry.py`, `test_r200_equipment.py`; `new/evidence/db/*.sqlite` e checkpoints; `new/evidence/R200_EXECUTED_FIGHTS.json`, `R200_AUDIT.json`, `R200_BENCHMARK_FROM_RECEIPTS.json`, `new/evidence/adversarial`; dashboard em `new/ui`.

## 05 FICHA DE REFERÊNCIA
`ED-REF-01` ORC TEST, função **combatente equilibrado** (papel experimental, NÃO classe oficial). Base humana universal 25 distribuída [FOR6, DES5, CON5, INT4, SAB3, CAR2], extra racial Orc +12 exclusivo [FOR+9, DES+3], total 37, checks raciais FOR15 DES8 CON5 dentro 5–15; seis perícias entre 6 permitidas (2+INT inicial4). REF B1 HP26 PA22 FF280, ca física24, espada Bronze2d8, armadura leve Bronze+5CA, sem magia inata arbitrária, sem transformação. 2 marcos de FF de dano travados (rolagens pseudodeterminísticas TEST), não alterar originais.

## 06 NÍVEIS / LEVEL-UP
B1 totalmente modelado a partir das fórmulas; P1 matemática TEST com 5 transições raciais +5 pontos/nivel até nível6, total atributos62, atributos P1 FOR20 DES13 CON12 INT12 SAB3 CAR2; HP129 e PA116 pelas regras de recálculo Prata (Orc Vida d12 fixo7; Alma d8 fixo5), FF450 e CA física 137/4. **NÃO declarar paridade comprovada com LEVEL-UP ENGINE**: a interface nativa está PENDENTE; escolhas, proficiência evoluída, habilidades/transformação não homologadas. Níveis 7–25 NOT-EXECUTABLE a partir do construtor atual: falha explícita sem fake snapshots.

## 07 EQUIPAMENTO FÍSICO / MAGIA / PA
Dano físico prospectivo de arma `NdS × classificação` (COMUM1 BRONZE2 PRATA3 OURO4 OURO_NEGRO5 LENDARIO6). Espada B1 `2d8`, P1 `3d8`, brutal Ouro `8d6`, brutal Lendário `12d6`. Armadura leve Bronze +5 CA, Prata +7 CA; leve/medio/pesado seguem tabelas prospectivas. Mobilidade leve100%, média75%, pesada50%, sem arredondamento. A mesma espada/armadura física, FF e HP em ambos os ramos. Efeito mágico hipotético de anel +2CA (retirado ao desligar), 13PA/dia publicado cobrado na **entrada da cena por convenção TEST** — a fonte não demonstra classificação Bronze/Prata nem momento de débito. No Bronze B1 com anel livre PA9 vs PA22 sem. Este ramo **NÃO é comparador legal homologado Bateria E**. NÃO recolocar equipamento inferior ao desligar magia, nem apagar magia própria.

## 08 GEOMETRIAS / MAGIAS
Validador exato racional A–L: ofensiva alvo único 9m inclusivo; área circular raio6m, centro até9m; caster dentro só se geometria e fonte efetivamente permitem; especificidade prevalece. Cone de 4,5m sem ângulo publicado: recusa canônica; cunha auxiliar explicitamente `LAB_TEST_ONLY` **não é a abertura oficial**. **TESTES espaciais somente unitários de preflight**, NÃO novos combates mágicos com posicionamento. Segunda magia distinta ainda PENDENTE. A regra canônica Sistema de Magia proíbe críticos mágicos na ausência de exceção, alerta específico para futuros adaptadores — não invalidar nem reescrever R198/R199.

## 09 TESTES ESPACIAIS A–L
`new/code/test_r200_geometry.py`: 14/14 testes; sem violação de PA em preflight inválido. A–L e regressões auxiliares, com C correspondente à cunha explicitamente TEST (com ângulo real NOT-EXECUTABLE canônico). Outros 6/6 testes `test_r200_equipment.py`: física/magia separadas, todos seis ranks, HP/PA atributos e proibição Bronze.

## 10 TRANSFORMAÇÃO / ESPÍRITO / RESERVAS
Bronze1–5 marcado PROHIBITED no ator; P1 apenas elegível condicionada à assimilação, não transformado. Nenhum espírito identificado, nenhum TAP/BAP transformado gerado, zero ativações novas neste bloco. R199 transformações Ong preservadas como TEST condicional, não prova legitimidade. T6-B/T9-A reservas/cena/descanso pendem para novo cenário.

## 11 HABILIDADES DE BESTAS
Galinha B1 ataque publicado Patada `1d4+DES`, 32 HP, CA21; RD Bronze5 derivado da Criação de Besta. O bônus de proficiência genérico da Besta +6 aplicado à Patada continua hipótese de Luta não publicada como perícia nomeada. Lobo P1 herda snapshot condicionado R198/R199. Zero habilidade de controle nova; Força Ancestral R199 não repetida.

## 12 POLÍTICAS TÁTICAS
Duas políticas pareadas testadas `SEM_MAGIA_ITEM` e `COM_MAGIA_ITEM_PROXY_UNRANKED_TEST`; ataques básicos físicos determinísticos com rolagens por seed, contato adjacente inicial. Sem nova IA adaptativa, reação especial, deslocamento ou área multialvo nos novos combates. Iniciativa empate duas recusas pré-commit preservadas sem rerun. Não contar física do Orc como conjuração.

## 13 COMBATES / IDENTIDADES
CASE `R200_EDREF_L1_GALINHA_B1`, `R200_EDREF_L6_LOBO_P1`; RUN IDs `R200_EDREF_L{level}_{enemy}_S{seed}_{policy}`; 8 seeds `20021001..20021008` e duas políticas, 32 tentativas. 30 SQLite novos, 2 empates precommit; nenhuma seed/RUN histórica reutilizada. B1: sem efeito mágico 4 ED/3 Galinha, um empate; com proxy 7 ED/0 Galinha, um empate. P1: sem 2 Lobo/6 censurados; com 8 censurados, zero vencedor. Total 16 KO e14 censurados; **não alegar 30 KO**.

## 14 MÉTRICAS / PA / DANO / KO / CENSURAS
Independent replay `R200_AUDIT.json`: 1497 commits, 4415 eventos nativos, 1467 ataques, 16 KO, 14 censurados, 2 precommit holds; não foram lançadas magias próprias em R200. `R200_BENCHMARK_FROM_RECEIPTS.json` contém por grupo ataques, acertos, HP efetivo, Rodadas, PA TEST; efeitos do anel não gastam PA em transação nativa, iniciam com 13 PA debitados por modelagem de estado TEST; **não declarar débito atômico de ativação**. RD5 Bronze Galinha, RD15 P1 Lobo condicional herdado e RD0 Orc hipótese; dano bruto/pós-RD verificável nos recibos.

## 15 PAREAMENTO / INTERAÇÕES
8 blocos seed por nível; B1 7 pares com combates efetivos +1 par sem commit, mudança 3/7 vitórias a favor ED com anel. Nenhuma modificação física entre políticas. P1 8 pares, 2 KO da Besta sem anel versus todos censurados com anel; **não afirmar vitória por censura**. Comparações de RNG em políticas geram divergência de turnos quando KO diferente.

## 16 BATERIAS A–E / DENOMINADORES
A: 1 ED-REF TEST em dois snapshots B1/P1, 30 combates exploratórios submetidos a auditoria, zero células oficiais homologadas. B: zero linhagens 25/27 estados criadas. C: zero equipes/2–5 novos confrontos. D: zero painel 25/27 Bestas distintas montado. E: duas políticas por ED e seed com **anel sem rank**: estudo de sensibilidade TEST, **0 comparações E legalmente certificadas**. 0/17 contratos terminais, 0/1.875 células homologadas, não aumentar denominador. **CORREÇÃO DE ESCALA:** IBX-101 registra patamares de potência 26/27 ADM/Divina para Bestas, não níveis ordinais 26/27 de ED; a atual ordem usa expressão "coortes especiais, não níveis 26/27" — registrar distinção e conflito de nomenclatura à coordenação, sem decidir silenciosamente nem preencher coorte.

## 17 DIAGNÓSTICO CIENTÍFICO
Bronze: a proteção +2CA TEST eliminou todos os acertos ordinários de Galinha nas sete seeds experimentais e mudou resultados 3/7 pares, mas seu item fonte não é rank-admissível comprovado, a despesa de PA é convencional e a IA usa ataques básicos sem deslocamento. Prata: o ataque Orc P1 `2d6+22` atinge no máximo34 e NÃO supera CA34 Lobo; somente crítico LAB consegue acertar, déficit ofensivo desta build em contato. Resultado não prova rank geral. As 14 censuras P1 impedem taxa terminal de vitória. Não há diagnóstico oficial de rebalanceamento.

## 18 BANCADA
HTML offline R200 adiciona sexta aba, mantém R197/R198/R199 e 30 recibos com 1.467 ataques, selector de nível/seed/política e indicadores. Navegador móvel headless 390×844: seis tabs, seleção/teste de trace funciona, 0 JS errors. Não inicia Python.

## 19 HASHES / REPLAY / RECUPERAÇÃO
Novo ZIP contém ZIP R199 exato, novos scripts, 30 DB/SQLite, checkpoint, auditor separado, benchmark e novo HTML; manifesto SHA no root. Scripts de recuperação fria incluem verificações 30/30 source-semantic replay, 4/4 adulterações semânticas rejeitadas após recomputar hashes e testes 20/20 em extração limpa. Sem executar novos combates ao recuperar.

## 20 GOVERNANÇA
Autonomia Mestre LAB TEST; Notion laboratório poderá conter página específica do novo experimento; OP compartilhada/Diário, regras, fichas, Party/O Primeiro 0 novas escritas. Writer I0001/lease/epoch/fencing não presumidos; NAC-PASS proporcional de artefato e leitura não constitui homologação do VLAB. INC-DRY_V1_R199 original preservado.

## 21 PENDÊNCIAS / INCIDENTES / NOT EXECUTABLE
- Rank do anel ausente, tempo do pagamento 13PA/dia; sem prova para Bateria E homologada.
- Proficiência Luta de Besta, dano de arma com FOR, ca exata fracionária e iniciativa empate não certificados para uso universal; cenários explícitos.
- Falta utilização efetiva de magia espacial no combate novo; segunda magia funcional; cone ângulo canônico; transformação com Espírito real T1–T9-A; controle de Besta; tática adaptativa; combate 2–5.
- Falta integração LEVEL-UP ENGINE e progressão robusta 7–25, cinco ED; baterias B/C/D/E legais.
- Alerta: magia sem crítico segundo Sistema de Magia; overlays antigos R198/R199 não são prova de crit legitimado.

## 22 PRÓXIMO PONTO EXATO DE RETOMADA
1. Recuperar classificação de item mágico de proteção documentada Bronze/Prata ou escolher **outro** já classificado com efeito mensurável e custo; preservar runs proxy e iniciar NOVAS seeds/políticas legalmente pareadas.
2. Abrir interface real de LEVEL-UP/IBX-17 e validar ED-REF-01 evolução nível1→2 e 5→6 com escolhas/proficiências/PA/FF; manter P1 atual PROVISIONAL.
3. Fechar referência e fonte de segunda magia não ofensiva ou AoE, implementar preflight espacial na ação R18 de conjuração, custo nativo e recibos; nenhuma magia crítica sem exceção.
4. Buscar Espírito fonte-documentado e habilidade de Besta de controle, sem alterar originais ou reutilizar RUN-ID.
5. Só então expandir as baterias A–E e os cinco papéis, mantendo execução real como prioridade.

**PSV técnico:** artefato TEST verificável, terminal VLAB = HOLD. Nenhuma sequência R200–R209 declarada integralmente concluída.
