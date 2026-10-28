# VLAB — Pós-auditoria de elegibilidade Bateria E e recibo R227 (MESTRE-ONLY)

**Data:** 21/10/2026. **Identidade lógica:** CM-000006. **Operação:** OP-VLAB-FUSION-SANDBOX-01. **Escopo:** READ-ONLY / TEST; NO-WRITE Party, O Primeiro, produção, fichas e regras. **Objeto:** preservar a distinção entre capacidade experimental de combate e admissibilidade de item no benchmark oficial.

## Resultado 1 — Integridade de R227 e reparo de relatório (sem replay)

O pacote R227 original já estava na Biblioteca, com extração fria aprovada e **12 braços válidos / 6 seeds pareadas / 24 commits / 132 eventos**. Reabri seu `R227_EXECUTION_RESULTS.json` em cópia READ-ONLY e reconciliei: **4 acertos nos 6 pares; +100 PV de Raio com RD0; 0 com RD100; 176 PA por ambos os braços; 4 lentidões versus 0**. O RD Raio100 e a velocidade-base 4 m pertencem somente à fixture TEST, **não** à ficha de Varok. São janelas de dois turnos, não combates completos.

**Defeito isolado na camada de apresentação:** o runner histórico R227 construiu corretamente os relatórios e bancos, mas sua linha final de impressão tenta a chave `item_pa_spent_each_arm` quando o par havia sido persistido como `item_PA_spent`. Isso gera exceção **depois** de executar e congelar os arquivos, não invalida os dados auditados. A pós-auditoria recomputa os totais por registros individuais, sem editar o runner antigo nem reexecutar uma seed. O novo auditor independente pode ser executado na extração fria do pacote.

## Resultado 2 — Inspeção dirigida de fontes para Bateria E

Fontes primárias efetivamente lidas:

- **[Manopla do Trovão Cativo](https://app.notion.com/p/3f5c2b324ede81f5ac62fb940204cdac):** sob `Criações do Comestre — Semicanônico / Incubação`, fornece +5d8+3 Raio, gatilho, custo 22 PA, restrição de 1/descanso 8h e lentidão condicionada a 1 ponto efetivo. **Verificado:** tem separação funcional de golpe físico e descarga adicional, provas TEST R226/R227. **Pendente:** canonização específica, usuário/equipamento/velocidade/corpo-a-corpo oficiais e comparação representativa. **Veredito:** `PASS TEST EXPLORATORY`, `BATERIA E OFICIAL = HOLD`.
- **[Espada do Lendário](https://app.notion.com/p/3edc2b324ede81ab9e22e168f6d939a9):** repaginação de item do acervo preserva `14d20+14d12+14d8+14d10+390+FOR`, +60 FOR, +75 ataque, 600 PA/dia. **Pendente:** classificação física/mágica dos quatro pools e modificadores, condição de uso remanescente exata. Não fabricar chassi SEM magia a partir de fórmula agregada. `HOLD_COMPONENT_SPLIT`.
- **[Adaga do Sussurro Mortal](https://app.notion.com/p/85ec2b324ede837f95b6010118e38f5e):** página encontrada no espelho Mestre da Party, com `7d4+7d8`; `7d8` é identificado como **veneno**, não inequivocamente magia separável. `7d4` não foi oficialmente identificado como todo o chassi. Possui efeitos adicionais e custos próprios; não desligá-los por conveniência. Não alterar a página ou expor a fonte a players. `HOLD_PROVENANCE_AND_COMPONENT_TYPE`.
- **[REC-MOD-ARM-01](https://app.notion.com/p/3f1c2b324ede8140b993cc62063b9649)** é um **padrão oficial de engenharia**, não um item da Bateria E por si só: seu censo histórico de 19 armas não certifica automaticamente a separação de componentes num exemplar específico.
- **[PR-ITEM-02](https://app.notion.com/p/3eec2b324ede81ecb058f59f5b67e4f4)** governa itens por categoria e dependências, mas não promove a Manopla semicanônica a cânone.

**Gate mecânico explícito:** classificar um caso na Bateria E *oficial* somente com status do item e fonte de usuário/equipamento comprovados, pool físico e pool mágico atribuídos pela fonte competente, gatilho/custo/alcance/resistências especificados, RNG pareada, comparação do MESMO CHASSI com magia ligada/desligada, auditoria independente e NAC-PASS aplicável. A comparação R226 atinge só o âmbito TEST — não certifica o gate oficial.

O teste `battery_e_readonly_admissibility.py` verifica automaticamente que nenhum dos três candidatos satisfaz todos os requisitos; mutações de um só campo não promovem indevidamente o objeto. O pós-auditor `r227_postread_reconcile.py` confirma aritmética/contagens sem motor e sem replay.

## Estado

- `R225`: confirmação expressa do Mestre de arredondamento de dano SEMPRE PARA BAIXO, independentemente do tipo de ataque. Implementação TEST provada; propagação às fontes oficiais exige procedimento competente NAC-NORM. **Carry fracionário T1 da Transformação não arredondar**, pois regra especializada.
- `R226`: comparação item fonte-bound SEMICANÔNICO COM/SEM Raio, 8 pares, PASS TEST.
- `R227`: sensibilidade à proteção do Raio, 6 pares, PASS TEST; pós-auditoria READ-ONLY aprovada.
- `BATERIA E`: zero células homologadas. `CONTRATOS FINAIS`: 0/17. `MATRIZ`: 0/1.875. `PRODUÇÃO`: HOLD.
- `FIRST-PENDING`: item **explicitamente canônico** com físico/magia separados, usuário compatível e alcance/defesa fonte-bound; em paralelo Controle de Besta com duração/escape e Transformação Prata1+ ED→Espírito→Besta físico. Evitar duplicata de IBX-125/126; nenhuma reivindicação de writer/ACK.

**Evidência auditada nesta pós-etapa:** `BATERIA_E_CANDIDATES_SOURCE_GATE.json`, `R227_EXECUTION_RESULTS_FROZEN.json`, dois scripts READ-ONLY e `POSTAUDIT_RESULTS.json`. Snapshot é **extrato mecânico verificável**, não hash integral de páginas Notion com imagens assinadas dinâmicas. Nenhuma página canônica foi escrita.
