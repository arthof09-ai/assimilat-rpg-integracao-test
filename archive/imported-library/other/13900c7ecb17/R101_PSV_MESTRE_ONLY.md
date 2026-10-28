# PSV — VLAB / OP-VLAB-FUSION-SANDBOX-01 / R92–R101

**AS-OF:** 16/10/2026 · **AMBIENTE:** MESTRE-SIDE · **COMESTRE:** CM-000006 · **NATUREZA:** continuidade aditiva, sem motor alternativo.

**BASELINE VERIFICADA:** R01–R91 intacta; ZIP original R91 SHA-256 `b8da1d74b939fda8d1addaa889ce15d9ca4a96d5cd3c992faa2530379721b5dd`; R81 SHA-256 `a6bd78736dc0eefb512e91acec337b9d0bb608e4b28610486abc3d8d5bb2885a`. Sem refazer os 14 R81, 48 R91, 40 R91 excluídos, R59 ou o R72 problemático. Novas execuções não alteram as fontes históricas nem fichas no Notion.

## I. RESULTADOS TÉCNICOS SELECIONADOS — DENOMINADORES

| Grandeza | R95 1×1 equivalente | R93 2×1 | Soma de execuções selecionadas |
|---|---:|---:|---:|
| Combates com ledger auditado | **16/16** | **8/8** | **24/24** |
| Pares espelhados, não independentes | 8 | 4 | 12 |
| Eventos transacionais | **1.808** | **460** | **2.268** |
| Ataques válidos | **892** | **452** | **1.344** |
| Acertos observados | **452** | **258** | **710** |
| Combates concluídos | 8 | 8 | **16** |
| Combates censurados (sem vencedor) | 8 | 0 | **8** |
| Seeds distintas | 2 | 4 | 6 |
| Blocos independentes definidos por desenho | 4 espécies×seed (2 condições repetidas) | 4 equipe×seed | 8 blocos cruzados por configuração, não 24 |
| Mudanças em Party/OP/Diário/DMG-RANK | 0 | 0 | **0** |

**Resultado 1×1 — fontes do MESMO patamar:** Besta Lendário 3★ **Grifo-Matriarca de Sílica** ou **Crocodilo de Lodo Astral Ancião**, contra **Sikong Auren Lendário 3★ em forma normal**, lança documentada. Dano, CA, RD, Vida e bônus ofensivo com proficiência estão documentados. Grifo: 4/4 condições seed×abertura em Auren vencedor (8/8 espelhadas); Crocodilo: 4/4 condições seed×abertura censuradas depois de **60 turnos individuais realmente executados**, sem vencedor (8/8 espelhadas). A origem de iniciativa do Grifo/Croc NÃO foi inventada: **B-first/E-first são condições EXÓGENAS congeladas, sem teste de iniciativa**; portanto estes são *duelos admissíveis apenas como ensaio de ataque físico básico condicionado à ordem exógena*. NÃO são combate irrestrito, comparador de habilidades totais, nem vitória estimada universal. Auren tem título +8 após dois turnos enfrentando mesmo alvo e foi testado pelo auditor como bônus passivo documentado. Fonte: `BEAST-FULLSPEC-VZ-06`, sua auditoria independente e ficha de Auren.

**Resultado 2×1:** Grifo L3 (F) versus **Auren L3 + Feryn ON5** (V,R), quatro seeds espelhadas, política de alvo Grifo → Feryn → Auren e aliados → Grifo. 8/8 vitória da equipe, mas Feryn morreu em TODOS os quatro blocos. Prova o scheduler real de **três atores, duas facções**, saltos de derrotados, dano por ator, KO de aliado e finalização por equipe com replay semântico, não composição equilibrada de cinco EDs nem desempenho representativo do grupo. Auren **não** recebe seu título de +15 Luta por duelo individual no 2×1; ataca com `6d6+178`, valor derivado de retirar +15 do atalho `6d6+193` exclusivo de 1×1. Feryn é um NPC Ouro Negro 5 de PROPOSTA MESTRE-SIDE sem Espírito, **não** ED virtual de mesmo patamar.

**RELAÇÃO COM R92/R94:** NÃO misturar métricas. Descoberto erro de horizonte: prereg=120, adapter default real=60; por isso R92 é auditável tecnicamente porém **HOLD científico**. R94 foi continuado do último evento após interrupção, sem pending, mas esta continuação atingiu 65 turnos numa cena quando o espelho havia censurado aos 60; auditor do pareamento rejeitou a coerência. Todos os bancos são preservados, sem reescrita. R95 usa **novas seeds**, prereg=60, runner rejeita divergência antes de abrir SQLite, auditor exige contador real de 60 nos censurados. Ver `R92_R94_ERRATA_AND_QUARANTINE.json`.

**R93 PRECOMMIT:** tentativa inicial seed493101 falhou antes de qualquer efeito porque prefixo do comando R18 era inválido. SQLite rev0, eventos0, pending0, mantido em QUARANTINE; nunca repetido; novo sublote 493111/493112/493811/493812.

## II. AUDITORIAS

- Auditor **frio** R95, só Python stdlib, NÃO importa executor: 16/16; todas rolagens RNG, vantagem/crítico, débito de ação, bônus do título, pré/pós-Vida, RD, sequência, estado integral, snapshots, hash ledger, backup SQLite e idempotência observável. Valida 8/8 mirrors e **número exato de turnos contra prereg**.
- Auditor **frio** R93, separado do executor: 8/8; 460 transições; 452 rolagens de ataque, iniciativa dos três atores sob hipótese documentada, reações com renovação no próprio turno sem uso ativo, facções, alvos, exclusão de ator derrotado, empate no gate HOLD, finalização de equipe, SQLite/checkpoints. Limitação: training da iniciativa da Besta não comprovado, por isso 2×1 **condicional quanto à iniciativa**.
- QA redteam: **6/6** alterações em cópias de SQLite com todos hashes reencadeados aceitas estruturalmente, mas rejeitadas pelo auditor causal; **5/5** comandos inválidos recusados ANTES de abrir intenção/publicar efeito. Não editar os originais.
- RUN-ID: 24/24 únicos; genesis/checkpoints presentes e compatíveis; 12/12 pares de lado coerentes. Critérios separados: *integridade técnica* ≠ *fonte admitida no cenário* ≠ *potência integral* ≠ *referência homologada*.

## III. PRODUTO FINALÍSTICO: BATERIAS A–D

**A — Indivíduos 25:** Auren L3 como perfil documentado de duelista e primeiro dado empírico fonte-admissível **só** para ataque básico com abertura fixada; 16 ensaios condicionados, 0 referências universais completas. Feryn é apoio ON5 não ED. Dossiês Serah/Darek da aventura Vhal-Zoryn preservam roles (controladora/guardião) mas declaradamente `NUMERIC-DERIVATION=PENDING-SYSTEM`, não foram falsificados.

**B — Linhagem única 27:** candidata **Grifo-Matriarca**: L3 com ficha aritmética completa em `BEAST-FULLSPEC-VZ-06`, predecessor L2 com atributos explícitos parcialmente documentados e delta L2→L3 de 21 pontos; NÃO alegar L2 com Vida/CA/dano/competências plenamente recuperadas. Portanto **1 perfil L3 pronto para ensaio básico, 1 histórico L2 parcial, 0/27 referências de potência homologadas**, posição26 ADM e posição27 Divina NÃO atribuídas sem fonte da mesma linhagem.

**C — Equipe 25:** somente R93 2×1 experimental, **não equipe equilibrada**, mistura L3 com ON5 e NPC sem Espírito; a composição da one-shot Puxi não foi comprovada. **0/25 equipes homologadas**, cobertura 2 pessoas em 1 configuraçao técnica.

**D — Espécies 27:** inventário de **7 nomes distintos documentados** em Notion: Frígido Ossário B5, Grifo/Crocodilo/Serpente/Roc L3, Leviatã L4, Vaelthyr Divina (source-based L4 da entidade; potência 27). **2 espécies novas testadas em R95**; várias ocupam patamar 23 e não podem preencher 4 células diferentes do painel. **0/27 espécies homologadas como referências universais**. Preenchimento de propostas na matriz documental é candidato e não certificado.

**Escala AUTORAL vincula:** Potência 1–25 Bronze1–Lendário5, **26=ADM, 27=Divina**, ambas acima Lendário5; não exigir rank/estrela adicional inexistente para 26/27, mas preservar os que a **fonte específica** traz. Não são dois novos ranks comuns. Nova matriz V2 com 104 posições primárias, R91 imutável.

## IV. INTERFACE DMG, MÉTODO ESTATÍSTICO, NÃO CATEGORIZAR SEM FONTE

`R97_ATTACK_RECEIPTS_1344_FOR_DMG.csv`: 1.344 tentativas com origem, dano bruto condicionado, dano potencial pós-RD, dano efetivamente retirado, overkill, score/CA, críticos, rolagens, recursos, IDs, grupo de seed, fonte e adversário, combat status no arquivo `R97_VALIDATED_RUNS_24.csv`. Dois espelhos são testes de integridade, não duas amostras independentes. Apenas duas seeds de R95 e quatro seeds de R93: **não estimar chances universais nem recalibrar DMG-RANK**. Um crítico positivo não deve ser confundido com acerto numérico. Ausência de movimento/esquiva/magia/controle/Alma positiva limita potência inferível.

## V. PASSO-A-PASSO R92–R101

R92: par L3, fonte e 1×1 experimental; auditor PASS mas HOLD científico por divergência de horizonte. R93: primeiro 2×1 e aud. causal 8/8, progressão comprovada. R94: abertura exógena e episódio de interrupção; errata de horizonte e espelho rejeitado, preservar. R95: correção nova seeds e limite60 realmente verificado, 16/16 PASS. R96: redteam semântico6/6 e pré-gate5/5 PASS. R97: 24 resultados admitidos só em seus escopos + 1.344 recibos + 12 pares. R98: Grifo L2 parcial/L3 atual, inventário de sete Bestas distintas candidatas, painel27. R99: reconciliação denominadores sem contaminar R91. R100: NAC-CONT, registry/profile/IBX writer HOLD e empacotamento somente isolado. R101: readback, crosswalk17, PSU/PSV, NAC-PASS proporcional.

## VI. GOVERNANÇA E IDENTIDADE

As fontes no Notion foram abertas: OP, PLAN, IBX-101 com correção explícita DIR-MESTRE-VLAB-BENCH-27PATAMARES-20261016-003, Criação de Besta, Sistema de Combate, ficha Auren, Grifo/Croc e auditor de Bestas, ficha Feryn. Perfil CM-000006 estava **PAUSED/PROSPECTIVE**, writer/lease/epoch/fencing/INSTANCE-ID não verificados, Inbox IBX-101 **NOVA sem ACK**. Portanto nenhuma escrita em OP/Diário/Inbox/Party/O Primeiro/campanha/DMG-RANK. Execuções exclusivamente em réplica sandbox autorizada. Quando não há writer, preservar entrega na **Biblioteca da operação original**, sem duplicar operações/diários.

**NAC-PASS:** PASS técnico local circunscrito a 24/24 combates selecionados + integridade ledger/dados/auditoria, 0/17 contratos terminais e 0/1875 células oficiais, **HOLD** para benchmark geral, 25+27 homologação, writer e integração normativa. 17/17 contratos mapeados com nomes e histórico R91 sem alterar os termos de aceite.

## VII. CHECKPOINT DE SUCESSÃO

**AS-OF:** 2026-10-16. **OPERATION:** OP-VLAB-FUSION-SANDBOX-01. **BASELINE:** R01–R91 preservado. **LAST-VERIFIED-UNIT:** lote R95 16/16 + R93 8/8 com auditors frios e corpus corretivo selecionado. **FIRST-PENDING:** introduzir *iniciativa natural autenticada* de Besta (proficiência treinada ou não) antes de comparar resultados como duelo nativo completo; depois RD/ações especiais e outra espécie de L3 de estilo controle com regra concreta.

**DENOMINADORES:** selecionados 24/24 jogos, 12 pares / 8 blocos originais por configuração, 1344/1344 ataques, 2268/2268 eventos, 16 completos, 8 censurados; testes QUARANTINE R92 16, R94 32, R93 pré-commit 1 sem evento (NÃO somar); cobertura A25 B27 C25 D27; 0/17 terminais, 0/1875 oficiais. **NO-REPEAT:** R59, R72 precommit, R81, R91, R92, R94, R93 genesis inválida.

**CONFLICTS:** Prereg120 vs execução60 em R92/R94 (corrigida em R95 sem sobrescrita), Besta iniciativa específica não provada, ED forma normal vs total poderes, NPC Feryn não ED e classe inferior, VZ precreate não live, Puxi roster não comprovado. **UNKNOWN-EFFECT:** R59 HOLD, R72 primeiro HOLD; R93 inválida rev0 sem efeito, R94 interrupção em evento persistido e sem pending, lotes originais selados em HOLD científico.

**NEXT-5:** (1) recuperar competência de Iniciativa da Besta sem criar bônus; (2) ensaiar nativo 1×1 com uma nova seed de holdout e inteiro repertório legal progressivo; (3) incluir Serpente/Roc como terceiro arquétipo de Besta, só efeitos com resoluções comprovadas; (4) derivar Grifo L2 com valores completos autorizados; (5) equipe de dois EDs de funções complementares e mesmo patamar, precedências reacionais + primeiro cenário funcional. **TARGET-REMAINDER:** cobertura 27 e 25 progressiva sem declarar célula vazia como pronta. **AUTHORITY/WRITER:** PAUSED/HOLD, sem retrospectividade.
