# PSV consolidado — VLAB R218–R222

**Operação:** `OP-VLAB-FUSION-SANDBOX-01` · **Workstream:** `CM-000006-WS0001` · **Identidade:** CM-000006 lógica · **Data-base:** 21/10/2026 · **Ambiente:** MESTRE-SIDE / TEST.

**Status geral:** PROD HOLD; Party/O Primeiro/fichas originais/normas NO-WRITE; writer/INSTANCE-ID/lease/epoch/fencing não comprovados; 0/17 contratos terminais homologados; 0/1.875 células oficiais homologadas. O presente documento reúne nova evidência experimental, não uma promoção do sistema ou uma ordem à Party.

## Resultado material da execução prolongada

A continuidade não parou na R218. Foram executadas cinco coortes incrementalmente, com pré-registros congelados antes dos RUN-IDs novos, dados do motor R18/v0.8.1, auditores READ-ONLY, recuperação fria em extração limpa e upload + readback da Biblioteca Mestre. **Zero reexecuções de combate histórico.**

| Etapa | Tentativas/validas/bloqueadas | Unidade completa | Ação científica nova | Commits/Eventos |
|---|---:|---:|---|---:|
| R218 | 48 / 33 / 15 | 13 pares | Iniciativa realmente rolada entre V, R e E, 10 pares com ordem diferente e nenhum delta HP/PA | 396 / 2.452 |
| R219 | 48 / 36 / 12 | 16 pares | Varok inicia ferido (TEST), 15 pares com ordem diferente, sem delta terminal | 432 / 2.636 |
| R220 | 48 / 33 / 15 | 13 pares | Eristan a 4m (cura padrão possível, Pulso indisponível), Varok conserva defesa no round1, 2 pares alteraram decisão e 1 delta HP | 396 / 2.410 |
| R221 | 48 / 33 / 15 | 13 pares | CRN por ocorrência da habilidade: 3 pares alteraram decisão, 0 delta HP terminal | 396 / 2.409 |
| R222 | 96 / 76 / 20 | 14 quadruplas | Fatorial iniciativa A/B × atribuição RNG por rodada/ocorrência, com critérios causalmente distintos | 912 / 5.610 |
| **Total bruto de execução** | **288 / 211 / 77** | **Unidades não intercambiáveis** | **211 lutas TEST novas, todas censuradas; zero KO e zero vitórias** | **2.532 / 15.517** |

Mais métricas somadas por coortes heterogêneas, sem tratá-las como n independentes: **633 movimentos**, **1.899 ataques físicos**, dos quais **211 oportunidades**, **230 curas** e **707 conjurações**. As 211 execuções incluem braços pareados; não confundir este total com 211 seeds independentes.

## Descobertas que mudam a ciência do laboratório

**1. Iniciativa operacional não equivale a mera troca de rótulo.** A R218 provou rolagens reais ON5 `4d6+29` Varok, `4d6+25` Arveth, `4d6+30` Eristan e execução de ordem efetiva no journal. Desempate em iniciativa ficou BLOQUEADO antes do commit quando o valor empatou, pois não se localizou regra normativa competente.

**2. Uma fixture pouco discriminante oculta riscos.** Na R218 (cenário R216 normal) e na R219 (Varok previamente ferido), as ordens mudaram, mas as quantidades de ações e somas de ataques/curas acabaram com estados terminais iguais. Isso não autoriza declarar justiça universal.

**3. O estado espacial e o uso de Reação alteram a árvore de escolhas.** Na R220, Eristan foi posicionado a 4m de Varok: ação de cura padrão é admissível, mas Pulso Reativo exige até 3m e não é legal naquele estado. Varok decidiu não gastar a Reação defensiva na rodada inicial — opção fonte-admissível, igual nos dois braços. Duas seeds produziram escolha diferente de suporte; na seed `22045003`, Arveth apresentou delta terminal de **34 PV**. Mas a fita de Esporos era indexada pelo número da rodada, confundindo ordem de ação e atribuição da amostra RNG.

**4. Não atribuir automaticamente 34 PV à iniciativa.** Na R221, a fita dos efeitos foi indexada à n-ésima execução de cada habilidade; 13 pares, três mudanças de decisão, **nenhuma diferença terminal de Vida**. Isso não corrige retroativamente a R220 porque as seeds são novas, mas justificou um fatorial explícito.

**5. R222 separou os fatores sobre as MESMAS seeds.** Foram 14 quadruplas completas, não 56 experiências independentes: 2 iniciativas roladas e 2 regimes de mapeamento dos mesmos bancos de dados. Três quadruplas tiveram diferença terminal por iniciativa no modo por rodada; uma continuou com diferença no modo por ocorrência. Em cinco quadruplas de cada iniciativa, apenas mudar o regime RNG também alterou Vida. A seed `22288014` registrou `INIT_A - INIT_B` de **−69 PV Arveth e −35 PV Varok nos dois mapeamentos**, evidência delimitada de não comutatividade de turno nessa fixture. Este é o contraste mais robusto da campanha; **não representa vitória nem potência canônica**.

## Auditoria, novos defeitos e quarentenas

- Todos os SQLite admitidos foram lidos por auditores independentes que **não importam o executor ou resolutores nativos**, além da revisão das cadeias de hashes, turnos, posições, custos, recursos e dados de origem.
- R218: três adulterações com hashes reconstruídos foram rejeitadas por fonte, não por nome de arquivo (corrigiu-se uma falsa prova de rejeição por filename no primeiro protótipo).
- R219: detector herdado da R216 possuía precedência booleana incorreta para crítico negativo: a expressão errava ao tratar `NEGATIVE` como reprovação incondicional da auditoria, mesmo quando ataque corretamente falhava. Corrigido na **cópia do auditor R219**, sem alterar o motor ou o histórico R216.
- R222: quatro adulterações com hash reconstruído (mapeamento da fita, dados de iniciativa, ordem e pré-registro) passam pela checagem mecânica genérica mas são rejeitadas por auditor fatorial específico.
- Em todas as coortes, bancos com `UNKNOWN_HALF_ODD` possuem intenção pendente e não são reexecutados automaticamente; empates de iniciativa bloqueados pré-commit não viraram combates válidos. A R220 possui duas quarentenas com `revision=0` e `pending=1`: intenção sem efeito publicado, preservada como tal.
- Todas as baterias terminaram por horizonte e **nenhuma** produziu KO, vitória, empate canônico ou classificação oficial.

## Recuperação física e hashes dos cinco checkpoints

| Pacote Mestre-side | SHA-256 verificado na Biblioteca | Estado |
|---|---|---|
| `VLAB_R218_SOURCE_ROLLED_INITIATIVE_NEGATIVE_AUDITED_MESTRE_ONLY.zip` | `19a1223fd1a92451a5e92adee1eb87aa0965c68a3a3b4b16f2946a915190d40b` | COLD PASS, readback PASS |
| `VLAB_R219_WOUNDED_INITIATIVE_NEGATIVE_COLD_AUDITED_MESTRE_ONLY.zip` | `6a0faa5fbcacbdad4d914320af4443e7f92c773db8044dc6ed94526d2ef72fd9` | COLD PASS, readback PASS |
| `VLAB_R220_ORDER_NONCOMMUTATIVE_TIMING_COLD_AUDITED_MESTRE_ONLY.zip` | `98cc0447d7a2cb63832c02f2520d079f26f16144b85616d2914f0a18db8b5282` | COLD PASS, readback PASS |
| `VLAB_R221_ABILITY_INDEX_RNG_STABLE_COLD_AUDITED_MESTRE_ONLY.zip` | `32690d1af02385e355d367237d6ff9b0765605381fd066f5d45558bcd9ee93fa` | COLD PASS, readback PASS |
| `VLAB_R222_FACTORIAL_INITIATIVE_RNG_ASSIGNMENT_COLD_AUDITED_MESTRE_ONLY.zip` | `d2820b7bab02e294805848ef0d7a7d7898d7c1c5a1b0b0495edddd41eb58d5cd` | COLD PASS, readback PASS |

Cada ZIP contém código original add-only, pré-registro fonte-vinculado, SQLite, quarentenas, auditores, relatórios e recuperação fria. Extração limpa revalidou hashes, CRC e dados sem executar runners históricos. Os PSVs individuais também foram publicados e recuperados da Biblioteca com bytes idênticos.

## Contratos normativos preservados e fonte-escassez

- **INICIATIVA:** Sistema de Combate estabelece rank dice+DES+bônus. Os cálculos `4d6+29/25/30` foram extraídos das fichas ON5 Mestre-side. Empate de iniciativa permanece sem regra competente localizada, portanto `BLOCKED-SOURCE` no ramo raro.
- **MAGIA:** Sistema de Magia e DMG-RANK usam “metade” em seus efeitos, mas os trechos autoritativos recuperados não esclarecem arredondamento de resultados ímpares; preservar `UNKNOWN_EFFECT/HOLD`, sem importar convenção de outro sistema.
- **OPORTUNIDADE:** relação de bloco adjacente das fixtures R43–R49 permanece TEST, não há metragem universal de bloco validada; custo de Movimento interrompido por KO segue UNKNOWN.
- **BESTAS/CONTROLE:** `BEAST-FULLSPEC-VZ-06` contém técnicas como Raiz de Ressonância (120PA, imobilização em falha), e Arrasto ao Canal (50PA, agarrar/arrastar), mas persistem campos não fechados de duração, oposição/escape e páginas físicas das seis Bestas (`PHYSICAL PAGES=0/6` na fonte); não fabriquei controle completo no scheduler.
- **TRANSFORMAÇÃO:** Sistema de Transformação Espiritual v1.0 oficial determina `TAP=BAP÷2` e ativação só Prata1+. Não se demonstrou neste conjunto vínculo fonte-completo ED↔Espírito real↔Besta, seus recursos e expiração; ficou PENDENTE, sem usar R199 como homologação.
- **BATERIA E:** a amostra de equipamentos pertence a NPCs Mestre-side propostos, sem item canônico de chassi físico+mágico separado. Não converter em benchmark homologado.

## Estrato R91 e ciência exploratória

A planilha oficial existente `R82_CORRECTED_BENCHMARK_SCHEMA_PRIMARY_104.csv` confirma **104 posições primárias**. O estrato `C_BALANCED_TEAM_25`, posição ordinal **20 = Ouro Negro5★**, permanece `SOURCE_MISSING`, `NOT_BUILT`, `reference_homologated=0`. O CSV `R222_R91_C20_SOURCE_LIMITED_FACTORIAL_EXPLORATORY.csv` preserva os 14 conjuntos completos com quatro braços cada, para consulta Mestre-only e análise de sensibilidade de iniciativa, não altera nenhuma célula oficial.

## Inbox, escritor, continuidade e NAC-PASS

- `IBX-125` Orc×LEVEL-UP e `IBX-126` VLAB×DMG existem, porém `Destinatário COMESTRE-ID=CM-000001` em ambos; nenhuma leitura do Executor final comprovada. Não criei duplicatas nem reivindiquei ACK.
- `IBX-138` de encaminhamento integral adotada quanto ao significado da ordem copiada, mas ACK persistente não reivindicado por ausência de INSTANCE-ID/writer legitimamente atribuído.
- Sem writes Notion produtivos, DMG, Party, O Primeiro, fichas ou normas. Biblioteca Mestre recebeu os pacotes em pasta existente sob a operação VLAB, com leitura de volta.
- **NAC-PASS:** mecânico/científico experimental delimitado = PASS local; científico global = HOLD; normativo = HOLD; produção = HOLD. Zero contratos terminais homologados e zero células oficiais promovidas.

**LAST-VERIFIED-UNIT:** R222 recuperada fria do binário publicado; R218–R221 preservadas. **FIRST-PENDING:** R223 candidato sujeito a preflight, focado em primeiros testes fonte-completos de Controle de Besta ou Transformação; independentemente, resolver fontes para empate de Iniciativa, dano ímpar e adjacência, e ampliar o contrato R91 C20 sem promover NPCs propostos.

**NEXT-5 concreto:** (1) contrato normativo do desempate de iniciativa com fonte; (2) regra da metade ímpar e retrovalidação com seeds NOVAS; (3) primeira Besta com alvo, oposição, duração e escape completamente verificáveis, senão diagnóstico de campos faltantes; (4) transformar um ED Prata1+ ligado a Espírito real com TAP/BAP e recursos de forma; (5) arquétipos/equipamentos canônicos fonte-completos para substituir a fixture proposta C20, preservando dimensão 25 ED / 27 Bestas / 104 primárias.

**NO REPEAT:** não reexecutar R01–R222, não reusar seeds, não tratar o nº de braços como denominador de seeds, não promover hipóteses TEST ao cânone.
