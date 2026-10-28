# PSV — VLAB CM-000006 / OP-VLAB-FUSION-SANDBOX-01 — sucessão científica, 15/10/2026

**Público:** MESTRE-SIDE exclusivamente. **Status:** RECUPERAÇÃO FÍSICA DO R27 VERIFICADA, PESQUISA R27 CONDICIONAL SUBSTANTIVA, HOMOLOGAÇÃO CANÔNICA HOLD. Não é nova versão do motor nem alteração de regras. **Antecessor:** R26 última entrega expressamente reconhecida pelo Mestre; R27 posterior fisicamente recuperada da Biblioteca. **Autoridade:** última Ordem Suprema de desbloqueio + ciência, reiterada pelo Mestre na sucessão.

## 1. Objetivo e verificação da fronteira

A Biblioteca `/Comestre/OP-VLAB-FUSION-SANDBOX-01/` contém pacotes históricos e **R27** posterior a R26. Foram materializados R26 original (17.541.213 bytes) e R27 original (21.563.581 bytes). **R27 é o último pacote encontrável nessa pasta** na listagem examinada; não foi localizado R28 nessa pasta, o que não prova sua inexistência em outros locais.

- SHA-256 ZIP R26: `0375f64f884ac9d85b1bfa5f9f01099c53873f4c6e1a76d126de31b423927e75`.
- SHA-256 ZIP R27: `d8a384f8d6d8b94ef494fc67bac704c1aa87c1ada64359342f8cdcab6da31ab1`.
- R27: ZIP CRC PASS, 3.300/3.300 hashes de conteúdo; **2.597/2.597 arquivos herdados de R26 idênticos** (auditoria independente).
- Certificado readback pré-existente de R27 na Biblioteca; não substitui auditoria independente.
- **24/24 checkpoints ZIP portáteis**: hashes SHA-256 conferidos diretamente contra `R27_CHECKPOINT_INDEX.json`, todos CRC PASS, sem reexecutar seus efeitos.
- Nova auditoria independente nesta sucessão: **328/328 pares de recibo JSON/SQLite** examinados, PRAGMA integrity_check, digest SHA, eventos, revisão, pendências nativas, dano e transições de Vida; **zero divergências**.
- Regressão nativa R27: **10/10** testes aprovados nesta recuperação; replay novo do par OFENSIVO × DEFENSIVO / semente 11 reproduziu campos e SQLite byte-exact. **Não alegar replay independente novo das 328 configurações**: as outras foram auditadas nos seus registros persistidos.
- 2 intenções preliminares UNKNOWN_EFFECT existentes (`DEFENSIVO__OFENSIVO__SEED_37` e `...41`) preservadas em HOLD, sem retry cego; sucessor anterior produziu sessões separadas para 320 slots analisados, não apagou os originais. Duas tentativas abortadas não aumentam artificialmente 320/320.

## 2. Método e separação de autoridade

Quatro perfis Bronze1 **virtuais condicionais** com 43 pontos = 35 base + 8 primeira estrela da regra de Criação de Besta; orçamento igual não transforma perfis em fichas de criatura real. Proficiência Bronze normal +6 aplicada em Luta é **hipótese de alocação**, não prova de treinamento individual. Ataque técnico `1d6 + FOR + 6` supera CA para acertar, 3d6 de dano genérico, RD5, sem reações voluntárias, PA não-positivo e HP0 para término laboratorial. Política de falha crítica de sequências 1-1-1 / 1-1-2: falha automática e ação consumida; zero dano ao alvo, sem dano próprio, perda de arma ou penalidade extra; **LAB-only**. Crítico positivo preserva máximo extra dos dados (18 em 3d6). Criação de Besta e Sistema de Combate lidos na fonte do Notion. DMG-RANK v1.1 não alterado.

| Perfil | FOR | DES | CON | CA | Vida | Alma |
|---|---:|---:|---:|---:|---:|---:|
| Ofensivo | 20 | 4 | 10 | 16 | 50 | 43 |
| Defensivo | 6 | 12 | 15 | 25 | 55 | 44 |
| Equilibrado | 12 | 9 | 10 | 21 | 50 | 44 |
| Assimétrico | 2 | 22 | 10 | 34 | 50 | 43 |

## 3. Resultado empírico recontado

**Universo completo preservado:** 16 combinações ordenadas × 20 sementes = **320**. Destas, **120/320 (37,5%)** tiveram encerramento condicionado HP0 e **200/320 (62,5%)** foram censuradas no preflight com impossibilidade de acerto em ambas as direções sob ataque único. **Nenhuma configuração censurada é vitória, derrota ou empate de combate completo.** Seis células com 20 combates; dez células com 20 censuras.

**Matriz: vitórias da linha sobre 20 execuções; “C” indica 20/20 censuradas, sem vencedor:**

| Lado A / B | Ofensivo | Defensivo | Equilibrado | Assimétrico |
|---|---:|---:|---:|---:|
| Ofensivo | 9 | 20 | 5 | C |
| Defensivo | 0 | C | C | C |
| Equilibrado | 13 | C | 7 | C |
| Assimétrico | C | C | C | C |

**Contabilidade de 120 combates / 2.506 ataques:** 1.890 acertos (**75,42%** por ataque), 7.454 eventos A1, 19.913 dano bruto de acertos, 9.391 mitigação por RD, 10.522 dano líquido, 10.131 Vida efetivamente removida, 391 overkill. Taxa de absorção = **47,16%** do dano bruto contabilizado. Dano bruto por acerto = **10,536**; líquido por acerto **5,567**; líquido por ataque nativo **4,199**; Vida removida por ataque **4,043**. Rodadas por combate completo: média **10,675**, mediana 10, intervalo observado **6–23**. Reações voluntárias 0; PA positivo despendido 0 conforme a política, **não prova equilíbrio de reações ou custos reais**. Críticos positivos **28/2.506 (1,117%)**, falhas críticas LAB **18/2.506 (0,718%)**; frequência esperada teórica para cada gatilho **0,926%** (2/216), dispersão amostral compatível e dependência por rodada não eliminada. Intervalo Wilson meramente ilustrativo para acerto 73,7–77,1%, desconsidera agrupamento intraluta e não é IC inferencial válido para todas as políticas/categorias do RPG.

**Dispersão e incerteza por célula (n=20 cada):** Ofensivo × Ofensivo: 9/20, rodadas médias 8,85. Ofensivo × Defensivo: 20/20, 10,40. Ofensivo × Equilibrado: 5/20, 8,75. Defensivo × Ofensivo: 0/20, 10,85. Equilibrado × Ofensivo: 13/20, 8,75. Equilibrado × Equilibrado: 7/20, 16,45. Para vitória 13/20, Wilson95% 43,3–81,9%; para 20/20 83,9–100%. Amostras de 20 são exploratórias.

## 4. Causalidade, iniciativa, inversão e anomalias

**Precisão versus CA:** com ataque básico 1d6+FOR+6, as chances puras antes de falha crítica são:

| Atacante → alvo | Ofensivo CA16 | Defensivo CA25 | Equilibrado CA21 | Assimétrico CA34 |
|---|---:|---:|---:|---:|
| Ofensivo | 6/6 | 6/6 | 6/6 | 0/6 |
| Defensivo | 2/6 | 0/6 | 0/6 | 0/6 |
| Equilibrado | 6/6 | 0/6 | 3/6 | 0/6 |
| Assimétrico | 0/6 | 0/6 | 0/6 | 0/6 |

A CA do Assimétrico é uma defesa inviolável neste recorte, MAS ele também não acerta; “tanque invencível” seria interpretação enganosa. Com acerto garantido, FOR além do limiar não eleva o dano intrínseco 3d6 sem outra regra/efeito; logo Equilibrado pode superar Ofensivo mesmo com FOR menor. O alto número de censuras é **problema de cobertura/política de uma ação**, não evidência isolada de bug ou balanço geral.

**Inversão pareada, preservando sementes:** Equilibrado vence Ofensivo em 13/20 como lado A e 15/20 como lado B = **28/40 execuções, mas somente 20 blocos de semente**; vence nas duas inversões em 9 blocos, vence em apenas uma inversão em 10, e perde nas duas em 1. Ofensivo vence Defensivo em **20/20 tanto como lado A quanto lado B**, com 20 blocos de semente e vitória nas duas orientações em todos os blocos. Concluir que 28/40 são 40 observações independentes seria erro.

**Nova verificação independente dos eventos de iniciativa nos 120 bancos:** o primeiro a agir vence **56/120 (46,7%)** no agregado heterogêneo. Por célula: Ofensivo×Ofensivo 14/20; Equilibrado×Equilibrado 14/20; Equilibrado×Ofensivo 13/20; Ofensivo×Equilibrado 15/20; Ofensivo×Defensivo 0/20; Defensivo×Ofensivo 0/20. **O Equilibrado sempre vence iniciativa contra Ofensivo nos 40 confrontos** devido às diferenças de DES (9 contra 4) e critério de desempate; o Defensivo também vence iniciativa contra Ofensivo nos 40, mas perde todos por precisão insuficiente. Portanto **não** se identificou efeito causal puro de iniciativa: DES e escolha do perfil variam conjuntamente. Proposto para futuro: experimento controlado mudando apenas iniciativa com ações mantidas, separado da baseline.

**Experimentos novos nesta sucessão:** nenhum confronto novo inserido na matriz congelada; executados auditoria independente integral das 328 transações/recibos, testes unitários 10/10, replay byte-exact 1/1, recomputação de métricas e abertura direta do primeiro evento de iniciativa dos 120 bancos. Esses procedimentos de verificação não substituem certificação terminal de 17 contratos.

## 5. Análise matemática de fronteiras (não são combates)

Derivação **exata** da distribuição de dados normais versus RD típica da mesma classificação, se o dano for compatível e se o golpe atingir:

| Rank | Dano básico | RD | E bruto | E líquido após RD | P(0 líquido) |
|---|---|---:|---:|---:|---:|
| Bronze | 3d6 | 5 | 10,50 | 5,523 | 4,630% |
| Prata | 6d6 | 15 | 21,00 | 6,133 | 9,647% |
| Ouro | 9d6 | 25 | 31,50 | 6,743 | 12,278% |
| Ouro Negro | 12d6 | 35 | 42,00 | 7,339 | 13,762% |
| Lendário Titã | 20d10 | 75 | 110,00 | 35,010 | 0,329% |

A eficiência do dano líquido isolado aumenta apenas ~33% de Bronze→Ouro Negro (5,523→7,339), mas ~4,77 vezes de Ouro Negro→Lendário Titã (7,339→35,010). **Hipótese científica a investigar**, não prova desequilíbrio: Titã acrescenta alterações de Vida/atributos/etc.; ranking de 25 estrelas examinado como índice, não como 25 atores testados. As quatro fronteiras de classificação foram examinadas matematicamente, mas **0/4** por enfrentamento cruzado completo; apenas Bronze1 tem confrontos condicionais, 1/25.

## 6. Frente de Bestas reais: bloqueio documental, não de infraestrutura geral

**Galidemus** Bronze1: `Patada 1d4+DES13` cortante; dano documental mas atributo de acerto e treino de Luta, ação/custo, alcance, cenário inicial e recibo integral não atestados. **Cabra de Chifres** Bronze1: `Investida 1d6+FOR13`, efeito de empurrar exige distância/ordem/possível salvaguarda e custos/posições. **Raposa Flamejante** Bronze2: Bola de Fogo `1d4+5` e rastro de fogo, sem conjunto completo de custos/alcance/alvo, gatilhos/DoT. **Macaco Rei Titã** Prata5: efeitos/gates do fornecedor DMG R31 e autorização nativa ainda incompletos. **0/4 fontes examinadas oferecem ação integralmente admitida**; múltiplas ações específicas podem existir, portanto 0/4 é taxa *de fichas candidatas com primeira ação admitida*, e não denominador universal de todas as ações. 0 ações reais executadas legalmente, 0 combates reais. R24 foi mero componente da Patada com acerto forçado e alvo fictício e continua sem crédito.

Próxima frente real: Galidemus Patada pode ser menor lacuna documental, mas requer atribuição autorizada da precisão/treino, categoria de ação/custo, alvo/alcance, regra de dano e recibo transacional. Nenhuma regra inventada para desbloquear.

## 7. Fatos versus hipóteses e pendências

- **VERIFICADO:** presença e hashes R26/R27, integridade 328/328 recibos e seus bancos, contagem estatística, testes 10/10, replay parcial 1/1, dados oficiais abertos read-only no Notion, política crítica LAB nos rastros, 200/320 censuras e 120/320 encerramentos condicionais.
- **INFERIDO:** precisão versus CA é gargalo primário sob política de ataque básico; RD absorve fração expressiva; iniciativas correlacionadas com perfis; possíveis pontos de transição brusca no Lendário.
- **PROPOSTO:** variar CA/treino com builds legais, incorporar reações e ações documentadas em coorte separada, isolar iniciativa experimentalmente e avançar fronteiras com atores oficiais completos.
- **PENDENTE:** oito seeds reexecutadas de novo por este sucessor (oito recibos auditados, mas replay fresco de todos não realizado); atributos completos de ações reais; 4 fronteiras com atores completos; contratação de revisão independente para event sourcing; gate NAC-PASS produtivo; eventual persistência deste adendo no Diário da operação após autorização apropriada.
- **Anomalias editoriais pré-existentes R27:** relatório de texto contém dois placeholders não interpolados na tabela de hipóteses e descrição da lista de perfis. Os JSONs contêm números/lista válidos. Corrigir apenas em material derivado, sem alterar arquivo original ou contar como nova versão do motor.
- **HOLD conhecido:** IBX-56 BLOCKED-EXTERNAL; IBX-90, 91, 92 mantidos; writer/lease/epoch/fencing/GREEN de produção não reivindicados; Duelo dos Vigias congelado; nenhum resultado de teste homologado como canônico; nenhum crédito automático às 1.875 células.

## 8. PSV final / estado antes e depois

| Indicador | Estado anterior reconhecido R26 | Estado recuperado R27 auditado | Universo |
|---|---:|---:|---:|
| Sementes originais completas | 7 | 8 materializadas e auditadas | 8 |
| Combates originais condicionais completos | 7 | 8 | 8 |
| Combinações Bronze1 avaliadas | 0 na R26 | 16 | 16 |
| Perfis Bronze1 criados condicionalmente | não demonstrado na R26 | 4 | 4 planejados |
| Configurações matriz executadas/avaliadas | 0 | 320 = 120 completas + 200 censuradas | 320 |
| Patamares modelados matematicamente | parcial | 25 indexados; 5 grupos calculados | 25 |
| Patamares com combate condicionado | 1 | 1 | 25 |
| Fronteiras matemáticas examinadas | pendente | 4 | 4 |
| Fronteiras com duelo completo | 0 | 0 | 4 |
| Fontes de Besta real com ação admissível | 0 | 0 | 4 fichas examinadas |
| Combates reais completos | 0 | 0 | 0 verificáveis |
| Células canônicas creditadas | 0 | 0 | 1875 |
| Contratos VLAB terminais certificados | 0 | 0 | 17 |
| Critérios DMG certificados (registro histórico, não auditado nesta sucessão) | 1 | 1, sem mudança reivindicada | 18 |

**Checkpoint exato / próximo passo:** R27 recuperada em arquivo original SHA `d8a384...`, nova auditoria transacional SHA calculável nos arquivos deste adendo, baseline congelada `R27_FROZEN_ANTES_CONFIGURATION.json`. Não retomar da R26. **Continuar no mesmo VLAB**, usando R27 como ANTES e uma coorte **separada**, com fonte atestada para ações/treinamento ou cruzamento Bronze5→Prata1; não reescrever nem perturbar a baseline. Ação real segue bloqueada enquanto os contratos essenciais e 5 gates não fecharem. **NAC-PASS-02 não declarado PASS terminal produtivo**; auditoria local e sanidade copy-first aplicadas; homologação em HOLD.

## Fontes canônicas e artefatos

- Operação: https://app.notion.com/p/3f3c2b324ede819496ddd7f93bd7e5d2
- Plano: https://app.notion.com/p/3f3c2b324ede81d480dbf11732734463
- Sistema de Combate: https://app.notion.com/p/3ebc2b324ede81f1be4be8804ac113c0
- Criação de Besta: https://app.notion.com/p/3ebc2b324ede81f4992a-c88a3588cacd
- Bootstrap/Kit: https://app.notion.com/p/3edc2b324ede81d0b25ec2f3be128db6
- R27, ZIP: `/Comestre/OP-VLAB-FUSION-SANDBOX-01/VLAB_STAGE12_A1A2A3_SCIENTIFIC_BASELINE_R27_SANDBOX.zip` (biblioteca do Projeto).
- Evidência independente: `R27_SUC_INDEPENDENT_AUDIT.json`, `R27_SUC_CIENTIFICA_ANALISE.json`, `R27_SUC_INICIATIVA_ANALISE.json`, scripts de leitura associados em diretório de auditoria local.
