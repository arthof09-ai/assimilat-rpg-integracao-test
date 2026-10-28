# PSV R225 — DIREÇÃO UNIVERSAL DE ARREDONDAMENTO EM DANO (MESTRE-SIDE / TEST)

**As-of:** 21/10/2026. **Identidade lógica:** CM-000006. **Operação:** OP-VLAB-FUSION-SANDBOX-01. **Produção:** HOLD. **Party/O Primeiro:** NO-WRITE.

## Decisão do Mestre recebida

O Mestre confirmou no chat que, em qualquer tipo de ataque, quando um cálculo de dano precisar ser arredondado, deve ser **arredondado para baixo**. A dúvida anterior, restrita à metade de dano ímpar, está **resolvida na direção aritmética**. A escrita em `Sistema de Combate` depende dos gates de canonização NAC-NORM-01/NAC-PASS e não foi executada por CM-000006.

- Ex.: físico, mágico ou elemental: 61/2 -> 30; 60/2 -> 30; 21/2 -> 10; 1/2 -> 0.
- **Fronteira:** a decisão não cria um gatilho para reduzir ataques físicos à metade. Uma fonte mecânica ainda deve autorizar o cálculo fracionário. A decisão também **não** apaga o carry fracionário TAP/BAP da Transformação Espiritual.
- **Código:** cópia isolada v0.8.1, gate `FLOOR_MASTER_CONFIRMED_TEST`, autoridade `USER_MESTRE_CONFIRMED_ALL_COMBAT_DAMAGE_2026-10-21`; não modifica produção.

## Resultados materiais

Três novos SQLite de **magia real source-gated** com Esporos de Eristan, salvaguarda bem-sucedida e rolagens dirigidas *não aleatórias* previamente registradas de `10d10+10`, resolução nativa `cast_source_specified_spell` e journal R18.

| Caso | Dados de dano | Bruto | Metade piso | PA | Commit |
|---|---|---:|---:|---:|---:|
| R225 SOURCE ODD61 | nove 5 e um 6 +10 | 61 | 30 | 80 | 1 |
| R225 SOURCE EVEN60 | dez 5 +10 | 60 | 30 | 80 | 1 |
| R225 SOURCE ODD21 | nove 1 e um 2 +10 | 21 | 10 | 80 | 1 |

**Denominadores:** 3 cenários dirigidos, 3 seeds distintas, 3 commits R18, 3 eventos de magia. **0 combates completos**, **0 KO**, **3 censuras após uma conjuração**. Atesta temporalidade da resolução matemática e orçamento, não estimativa de dano aleatório ou benchmark.

**Controles:** 8 casos de aritmética exata por tipo de dano, incluindo uso do resolvedor histórico RD (`30 - 5 = 25`), preservação TAP carry de `1/2`; quatro rejeições source/TEST/dice antes de mutação; três adulterações adversariais rejeitadas após reconstrução de hash.

**Quarentena:** 3 bancos R225 preliminares usavam escalares sem fita `10d10+10`. Não são prova fonte-completa; preservados e não repetidos, como registro de falha de admissibilidade.

**Auditoria independente:** `code/r225_independent_readonly_audit.py` não importa o motor, reconstitui SHA por row, head e estado SQLite, valida fonte, rolagens, PA, Vida e gates. Os três bancos aceitos PASS; arquivos de quarentena não integram o denominador válido.

## Interfaces e continuidade

**ANTES:** R223/R224 usavam política provisória `FLOOR_MASTER_TENTATIVE_TEST`, decisão verbal incerta, escopo comprovado principalmente para Salvaguarda de Esporos.

**DEPOIS:** a decisão expressa possui escopo de todo dano que **já requer** arredondamento, independente da origem; a cópia TEST usa novo token de autoridade e confronta aritmética de dano físico, mágico, elemental e carry de Transformação. NÃO promove os pacotes R223–R224 retroativamente.

**LAST-VERIFIED-UNIT:** R225 ciência/teste local, pendente arquivo final + readback ao momento de escrita deste PSV.

**FIRST-PENDING:** R226 TEST com o item semicanônico *Manopla do Trovão Cativo* (Raio mágico após golpe físico, PA22, lentidão -3m por dano elétrico positivo, até fim do próximo turno do alvo); depois benchmarks E e controle, sem dizer que o item semicanônico é canônico.

**NAC-PASS:** local condicional PASS para aritmética e ataque mágico source-gated; canonização/documentação normativa PENDENTE; 0/17 contratos terminais, 0/1.875 células oficiais, produção HOLD.
