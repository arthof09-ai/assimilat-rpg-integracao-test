# RPG Assimilação — Decisão expressa do Mestre: armas e armaduras

**Data:** 19/10/2026  
**Ambiente:** MESTRE-SIDE  
**Natureza:** determinação do Mestre para alteração sistêmica; implantação e canonização físicas pendentes de verificação segundo NAC-CONT-03, NAC-NORM-01, NAC-EVOL/MIE e NAC-PASS-02.  
**Não constitui prova de alteração no Notion.**

## 1. Armas — progressão de dano físico por classificação

O dano físico base da arma sem classificação é um conjunto de dados `NdX` proveniente da tabela de chassis vigente (DMG-RANK-01 v1.1, salvo dano específico explícito). A cada classificação posterior, **repete-se todo o conjunto base de dados** uma vez adicional:

- Sem classificação: `1 × (NdX)`.
- Bronze: `2 × (NdX)`.
- Prata: `3 × (NdX)`.
- Ouro: `4 × (NdX)`.
- Ouro Negro: `5 × (NdX)`.
- Lendário: `6 × (NdX)`.

Exemplos: espada `1d8 → 2d8 → 3d8 → 4d8 → 5d8 → 6d8`; adaga `1d4 → 2d4 → 3d4 → 4d4 → 5d4 → 6d4`; arma brutal `2d6 → 4d6 → 6d6 → 8d6 → 10d6 → 12d6`.

Não somar apenas +1 dado para armas que começam com múltiplos dados. Não multiplicar automaticamente atributos, dano mágico, bônus fixos, títulos, efeitos, crítico ou dano de habilidades; separar as fontes. Classificação física/material do equipamento não é, por si, encantamento. Regra específica de dano explicitamente registrada no item anterior deve ser preservada como fato histórico até revisão dirigida; não sobrescrever o acervo sem gate de migração.

## 2. Armaduras — bônus físico de CA por tipo e classificação

| Rank | Leve | Média | Pesada |
|---|---:|---:|---:|
| Sem classificação | +3 | +7 | +10 |
| Bronze | +5 | +9 | +14 |
| Prata | +7 | +11 | +18 |
| Ouro | +9 | +13 | +22 |
| Ouro Negro | +11 | +15 | +26 |
| Lendário | +13 | +17 | +30 |

Fórmula: `CA física da armadura = CA base do tipo + (número de classificações acima de comum × incremento do tipo)`, onde incremento leve/média `+2 CA` e incremento pesada `+4 CA`. O valor integra a parcela `Armadura` nas fórmulas raciais existentes; não é uma fórmula nova de CA racial.

A CA física é conservada mesmo com encantamentos desligados. Propriedades mágicas de CA, atributos, RD, resistência e técnicas ficam em camadas separadas quando documentadas. Não somar a antiga CA publicada de um item à nova CA física como se fossem bônus independentes sem antes decompor a ficha: risco de dupla contagem. A nova tabela não cria automaticamente RD.

## 3. Mobilidade e arquétipos

- Armadura leve: **0%** de redução de deslocamento, movimento final `1,0 × deslocamento base`.
- Armadura média: **25%** de redução, movimento final `0,75 × deslocamento base`.
- Armadura pesada: **50%** de redução, movimento final `0,50 × deslocamento base`.
- Exemplo: 10 m de deslocamento básico → 10 m / 7,5 m / 5 m para leve/média/pesada, respectivamente.

Mago/conjurador normalmente utiliza vestes; se utilizar armadura, normalmente leve. A composição de referência do VLAB não deve otimizar um mago usando armadura pesada. Exceções textualmente documentadas e itens específicos exigem análise; não migrar personagens reais automaticamente.

## 4. Critério da Bateria E do VLAB

Duas versões pareadas de cada Espiritualista sintético de benchmark, por nível:

**Com efeitos mágicos:** item físico classificado + efeitos/bônus/atributos/PA de propriedades mágicas documentadas.

**Sem efeitos mágicos:** MESMO tipo e classificação física de arma/armadura, preservando dano físico e CA física por rank, munição e instrumentos necessários, magias naturais, habilidades pessoais e transformação legal; desabilitar apenas poderes, atributos, bônus e custos derivados das propriedades mágicas dos itens.

Dinheiro e aquisição NÃO restringem as construções sintéticas. Ter recursos financeiros ilimitados não significa equipar tudo: selecionar conjuntos equilibrados, coerentes com função/rank, sem outliers arbitrários. Transformação Demoníaca é proibida em Bronze 1–5; somente elegível a partir de Prata 1 e mediante os demais requisitos.

## 5. Fontes e superfícies que exigem reconciliação coordenada

- Sistema de Combate: https://app.notion.com/p/3ebc2b324ede81f1be4be8804ac113c0
- Criação de Ficha: https://app.notion.com/p/3ebc2b324ede81449222f3c06b840613
- DMG-RANK-01 v1.1: https://app.notion.com/p/3f2c2b324ede815498cddb7844245f7e
- REC-MOD-ARM-01 — Armas: https://app.notion.com/p/3f1c2b324ede8140b993cc62063b9649
- REC-MOD-ARD-01 — Armaduras: https://app.notion.com/p/3f1c2b324ede8116bd3cc6606a1c6687
- PR-ITEM-02: https://app.notion.com/p/3eec2b324ede81ecb058f59f5b67e4f4
- Atlas PR-ECO-01: https://app.notion.com/p/3eec2b324ede81ea8920c52473ecc3ab
- CRAFT / OP-ARQ-RIN-REC-01: https://app.notion.com/p/3f1c2b324ede81d7aa79c83106240516
- VLAB / OP-VLAB-FUSION-SANDBOX-01 (sem alterar produção)
- LEVEL-UP ENGINE (apenas interfaces de bônus de itens, CA e pré-cálculos, sem criar outro motor)

A regra do Mestre tem precedência na divergência específica, mas a fonte DMG-RANK-01 ainda dimensiona o orçamento do dano total pela RE/FIP e o módulo REC-MOD-ARM-01 referencia essa regra. Integrar **dano físico da arma por classificação** com **efeitos intrínsecos mágicos e orçamento de poder**, evitando soma dupla e hipóteses retroativas. Manter rank do item (RI), rank do usuário (RU) e rank dos insumos (RIn) semanticamente distintos. Não criar estrelas públicas em itens.

## 6. Plano de aplicação e gate

1. Confirmar identidade, writer/lease, operação e colisões aplicáveis; preservar bloqueio CRAFT/F5 para produção/receitas.
2. Capturar ANTES das páginas-mãe e dos módulos especializados, sem reproduzir logs dentro de páginas de regra.
3. Aplicar NAC-NORM-01 com versão, precedência e conflitos existentes, registrando a decisão expressa do Mestre.
4. Atualizar uma fonte-mãe competente e inserir pontes nos pontos de entrada existentes, sem novas normas ou páginas duplicadas.
5. Reconciliar a regra física com DMG-RANK-01, Atlas, REC-MOD-ARM/ARD, Criação de Ficha e Sistema de Combate.
6. Propagar aos fluxos CRAFT e classificadores de itens, separando CA/dano físico de habilidades mágicas e seus custos de PA.
7. Adicionar adaptador correspondente ao VLAB; testes pares com e sem efeitos mágicos, sem reexecutar historical RUN-IDs.
8. Testar bases `1d4`, `1d8`, `2d6`, fronteiras Bronze5→Prata1 e todas as CA e penalidades; verificar fonte específica legada e ausência de dupla contagem.
9. Tratar migração de itens e fichas já publicados como tarefa distinta, fonte por fonte, preservando valores explícitos até autorização/gate apropriados; Party e O Primeiro NO-WRITE por padrão.
10. Reabrir as fontes alteradas, comparar ANTES/DEPOIS, reconciliar Diário, MIE, regressão, NAC-PASS-02, e comunicar status real de implantação.

**Estado desta cópia:** documentação de decisão e plano de implantação preparado em conversa; nenhuma alteração canônica inferida a partir deste arquivo.
