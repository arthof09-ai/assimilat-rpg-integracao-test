# PSV R215 — Integração real de Reação defensiva, R50/R51, combate 2×1 e análise pareada

**AS-OF:** 21/10/2026 (America/Recife). **Identidade lógica:** `CM-000006`; INSTANCE-ID/writer/lease/epoch/fencing NÃO reivindicados. **OP existente:** `OP-VLAB-FUSION-SANDBOX-01`. **Ambiente:** MESTRE-SIDE/TEST. **Produção:** HOLD; Party/O Primeiro/fichas/normas NO-WRITE.

## Ponto ANTES / baseline

R214 recuperada nesta instância com SHA-256 `72905eac9fd2a1906a35eb0b593ffe57984986c3351f2177107b46a73e44ff0d`. Baseline R01–R214 e quarentenas intocadas. R214 executava oportunidades reservadas antes da RNG e bilateral Varok×Arveth sem defesas ou cura no mesmo combate. R215 não utiliza runners nem RUN-IDs anteriores.

## Implementação DEPOIS — incremental na cópia v0.8.1

`runtime/native/vlab_effects_v08.py` teve **somente o argumento opcional `post_rd_guard` adicionado à função `apply_weapon_attack`**; outras chamadas antigas seguem `post_rd_guard=None`. A defesa, quando elegível, é validada por `action_menu` contra fonte e reagente reais, após cálculo nativo `mitigate`, antes da mutação de HP, no mesmo `event_commit` R18. Reduções: Varok: 50 PA, até 70 de dano **pós-RD**, 1/cena; Arveth: 40 PA, até 50, 1/cena. Exige recurso suficiente, Reação disponível e fonte própria. Não gera cura/vida negativa e não duplica custo de PA/dia já reservado.

R50/R51 utilizaram `declare_counterattack` **antes da RNG ofensiva** e `execute_declared_counterattack` **após o erro real**; `COUNTER_RESPONSE` é terminal, não abre contragolpe recursivo. O mesmo scheduler renovou turnos; não transformou dano zero por RD em erro.

Equipe 2×1 Varok + Eristan × Arveth reutilizou **sem reimplementação** `apply_pulso_estabilizacao` (3d10+10 +20 luvas, 45 PA, Reação após dano) e `apply_reconstituicao_seiva` (8d10+25 +20 luvas, 75 PA, Ação Padrão), além da função pré-existente `cast_source_specified_spell` para Tempestade de Esporos. As decisões usam Vida corrente do aliado. Geometria TEST: aliados `(0,0)`, Arveth `(1.5,0)`, centro `(6,0)`, raio5, apenas adversário dentro; sem imunidade arbitrária; tradução bloco↔metro continua HOLD. Não houve movimento nestas coortes, portanto ainda não é prova de convergência universal de todos os módulos num único combate.

## Denominadores auditados

**24 execuções TEST válidas; 24 censuras por horizonte de quatro rodadas; 0 KO e 0 vitória.** 16 execuções bilaterais de defesa (8 iniciais com RNG não pareada + 8 em quatro pares com tape ofensivo idêntico); 3 execuções bilaterais com R50/R51; 5 execuções de equipe 2×1 (3 protetivas, 2 agressivas). **212 commits**, **914 eventos**, **192 ataques normais**, **160 acertos**, **12 contra-ataques R50**, **16 defesas após RD** com **767 PV de redução observados**, **10 curas** de **496 Vida efetiva**, **17 conjurações**. 7 curas Pulso e 3 Reconstituição; o bônus de Luvas não foi cobrado nem somado em duplicidade.

**Quatro pares estritamente pareados:** seeds 21581001–21581004, 32 rolagens ofensivas completas idênticas entre os braços. Vida terminal agregada de Arveth COM DEFESA 2.293 vs SEM 2.093; Varok COM 2.505 vs SEM 2.346. **359 Vida agregada preservada**, custo agregado **360 PA e 8 Reações** nesta subcoorte. São diferenças causais condicionais à fixture TEST, não calibração de potência por rank. As quatro seeds iniciais 215610xx utilizam tapes **diferentes** por política e **NÃO** são comparadores pareados científicos. Equipe 2×1 contém duas seeds com ambas políticas mas também streams de ação dependentes de política; são comparações descritivas, **não efeito causal identificado**.

**Quarentenas:** `R215_TEAM_AGGRESSIVE_S21563003_UNKNOWN_HALF_ODD.sqlite` reteve estado pendente em conjuração de dano ímpar com salvaguarda bem-sucedida; regra de arredondamento = `UNKNOWN_EFFECT/HOLD`. Quatro bancos de preflight/integração anteriores foram preservados separadamente em `evidence/quarantine`, não somados a válidos e não reexecutados. Pré-registro REV0, emenda REV1 e preregistro prospectivo PAIR retidos com SHA e justificação.

## Auditor independente, controles e segurança

`code/r215_independent_sql_audit.py` NÃO importa executor nem motor; lê SQLite em modo RO e reconstitui cadeia R18, snapshots finais e invariantes Vida, PA, Reação, RD/defesa, uma vez/cena, cura máxima, decisão de suporte, contra-ataque não recursivo, turnos e integridade das tapes pareadas. PASS: **24 bancos admitidos**, 212 commits/914 eventos. `code/r215_adversarial_audit.py`: 7 clones adversariais com hash-chain final reconstruída foram **7/7 rejeitados** por conservação de PA, Vida, Reação, redução, R51, cura e alvo. Clones de ataque são evidência TEST e nunca originais.

## Fonte, categorias e contratos

Varok, Arveth, Feryn, Eristan: NPCs Mestre-side PROPOSTOS, numericamente reabertos no Notion na execução; somente réplicas TEST. Fonte congelada F/V/R histórica R44 usada sem promoção canônica; Eristan reaberto na página primária, mas o `FrozenRuleEvidence.content_sha256` de E está ancorado no dossiê histórico R44 (não um dump independente integral da página de E). Esta **limitação de proveniência** impede homologação source-complete de Eristan até snapshot específico do seu conteúdo. RD mágica zero permanece convenção R209 TEST; salvaguarda `4d6+CON57` de Arveth é pura, distinta da perícia com proficiência. Gatilhos e ações reabertos, condição de equipamento fabricado não homologada.

**Suporte parcial aos contratos de combate integrado, Reações, ofensiva, cura, multialvo e equipe. NÃO atribuir PASS terminal específico sem contrato R18/gate próprio.** Contratos homologados **0/17**. Matriz de benchmarks canônicos **0/1.875**, esquema R91 das 104 posições e escala das 27 Bestas preservados. Nenhum cálculo de novo DMG/LEVEL-UP ou regra de campanha.

## Inbox e interoperabilidade

A Inbox foi consultada SQL no Notion. `IBX-138` é nova decisão de encaminhamento integral, reaberta e **adotada** no processamento desta ordem; `NOVA`/`Exige ACK=SIM` permanecem, sem INSTANCE-ID legítima para acusar ACK persistente. `IBX-125` Orc→LEVEL-UP e `IBX-126` VLAB→DMG foram **publicadas pela Coordenação e reabertas**, mas ambas possuem propriedade `Destinatário COMESTRE-ID=CM-000001`, embora os campos Operação/Workstream apontem LEVEL-UP e DMG. Logo a entrega ao destinatário executivo final é **PENDENTE DE ROTEAMENTO/READBACK**, não duplicar cartas nem presumir leitura/aceite. Não enviado novo material a DMG/LEVEL-UP nesta instância; os recibos inéditos R215 permanecem em pacote Mestre-side.

## Pendências e governança

- Regra mundial bloco↔metros, diagonais e custo de Movimento interrompido por KO: HOLD; independentes destes ensaios de posição fixa.
- Eristan PROPOSTO, fonte/cópia de evidência não integralmente congelada; RD física de loadout documentada, RD mágica não comprovada.
- Critico negativo na bancada continua política TEST; não norma da campanha.
- Sem prova de produção, writer/INSTANCE-ID, NORM/PA ou publicação Party.
- Transformação Demoníaca Prata1+, controle contra Besta fonte-completa, Bateria E física/mágica e cobertura de benchmarks seguem PENDENTES; pesquisa dirigida executada, sem promoção de candidatos incompletos.

**NAC-PASS proporcional:** defesa bilateral, contragolpe e 2×1 PASS mecânico/scheduler TEST condicionado, com auditor RO; científica global, contratos terminais e produção HOLD. **LAST-VERIFIED-UNIT após readback:** R215, condicionado à recuperação fria do pacote publicado. **FIRST-PENDING:** R216 candidato, sujeito a preflight, além de `R212-R43-ADJACENCY-SOURCE` e `UNKNOWN_HALF_ODD_ROUNDING_SOURCE_HOLD`.

**NEXT-5:** (1) resolver atribuição/rastreio IBX125/126 pela Coordenação competente, sem duplicar; (2) completar snapshot competente de Eristan e seleção de alvo com ambos ataques e cura no mesmo ciclo mais longo; (3) avançar controle de Besta com alvo/regra de salvaguarda/duração completos, evitando arredondamento desconhecido; (4) testar defesa e contragolpe junto com movimento e magia multialvo em 2×1 de maior horizonte; (5) produzir primeiro benchmark TEST com arquétipos fonte-admissíveis e pré-registro independente, sem homologação prematura.

**NO-REPEAT:** não executar R205–R214 novamente; não executar seeds R215 consumidas; não auto-retry dos bancos `UNKNOWN_EFFECT`; não reusar resultados em quarentena como válidos; nenhuma escrita em Party/O Primeiro/DMG/LEVEL-UP/OP protegida.
