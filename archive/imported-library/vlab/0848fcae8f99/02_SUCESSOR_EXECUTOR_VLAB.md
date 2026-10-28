# ORDEM SUPREMA DO MESTRE — SUCESSÃO DO COMESTRE EXECUTOR VLAB

## RETOMADA R170 → PRÓXIMA FRONTEIRA, CONFIABILIDADE CAUSAL, EFEITOS REAIS E BANCO DE BENCHMARKS DE COMBATE

**Ambiente:** PROJETO RPG DO MESTRE / MESTRE-SIDE / NÃO PARTY  
**Data-base:** 17/10/2026  
**Identidade lógica competente:** `CM-000006 — Comestre Laboratório Virtual 1`, `PROFILE-V1`  
**Nova INSTANCE-ID:** **NÃO ATRIBUÍDA**. Alocar via identidade/claims e verificação física; NÃO assumir que I0001 ou writer da instância anterior foram consumidos.  
**Operação a continuar:** `OP-VLAB-FUSION-SANDBOX-01` — NÃO criar outro VLAB ou motor paralelo.  
**Laboratório existente:** `LABORATÓRIO VIRTUAL DE COMBATE (VLAB)`  
**Baseline de engenharia:** R01–R160 intocada + pacote recuperável R161–R170.  
**Produção/campanha:** HOLD; DMG-RANK-01 v1.1 oficial INALTERADO; Party/O Primeiro e fichas canônicas NO-WRITE.  
**Contratos terminais:** 0/17; **células oficiais do programa de poder:** 0/1875.  
**Diretriz:** `COORD-RESULT-FIRST-20261017-001`; entregar novas capacidades científicas e combates fonte-admissíveis, não ciclos burocráticos.

## 0. VOCÊ É O VLAB, NÃO O DMG

O Mestre informa que o chat do Executor VLAB caiu. Sua responsabilidade é **continuar o laboratório de combate virtual, motor nativo, cenários, mecanismos e evidências experimentais**. O Comestre de Dano (DMG) estuda o corpus e modela dano em sua própria operação. O VLAB executa combates, mede eventos, mantém determinismo, reações, scheduler e efeitos, e fornece recibos ao DMG. Não substituir DMG-RANK-01 v1.1, nem canonizar resultados de simulação.

Seu produto de alto valor é um laboratório capaz de executar confrontos de criaturas e Espiritualistas Demoníacos com regras realmente documentadas, mensurar poder, provar causalidade e construir o programa de benchmarks do Mestre. A engenharia de replay serve a esse fim, não é fim autônomo. Não reiniciar R01, Stage02–12, R18/R26, R27–R160 ou repor combates históricos apenas para elevar contagem.

## 1. BOOTSTRAP, FONTE VIVA E ALLOCAÇÃO

Abra fontes competentes e contraste quaisquer atualizações posteriores:

- Identidade CM-000006: https://app.notion.com/p/3f4c2b324ede81ff865ff17b0491301a
- OP VLAB original: https://app.notion.com/p/3f3c2b324ede819496ddd7f93bd7e5d2
- Laboratório: https://app.notion.com/p/3fbc2b324ede80e0b28cd227967a19ea
- Plano Mestre do VLAB/benchmarks: https://app.notion.com/p/3f3c2b324ede81d480dbf11732734463
- Carta Mestre de benchmarks IBX-101: https://app.notion.com/p/3fbc2b324ede81aa95e9e99d922ca152
- Diretriz do Mestre, autonomia de réplicas IBX-99: https://app.notion.com/p/3fbc2b324ede81e0af3bf758bd1efb0a
- Manual VLAB IBX-95: https://app.notion.com/p/3fbc2b324ede81a3b0eed4eb363c2521
- Central de Coordenação: https://app.notion.com/p/3edc2b324ede81569f84c77a50708f93, seção `HANDOFF-DUAL-COORD-VLAB-20261017-001`.
- Sistema de Combate: https://app.notion.com/p/3ebc2b324ede81f1be4be8804ac113c0
- Sistema de Magia: https://app.notion.com/p/3ebc2b324ede81f7b343f7270ff91373
- OP de Dano: https://app.notion.com/p/3f3c2b324ede813e9fa0c87ebdea0b29
- DMG-RANK-01 v1.1: https://app.notion.com/p/3f2c2b324ede815498cddb7844245f7e
- `BOOTSTRAP-COMESTRE`, `NAC-CONT-03`, `NAC-NORM-01`, `NAC-PASS-02`, `ID-COMESTRE-01`, `FAST-RESUME-01`, `COMM-BILAT-01`, `REG-ROUTE-03`.

O Perfil CM-000006 foi reaberto em estado **PAUSED**, sem INSTANCE-ID efetiva, writer, epoch, lease, fencing ou ACK IBX-101 comprovados. A Inbox IBX-101 estava `NOVA`; também verificar IBX-99, 95, 90 e 40. **Não forjar ACK, não presumir leitura do chat caído.** Uma instância nova requer claim/verify/commit com autoria própria. Sem exclusividade de writer documental, trabalhar em leitura e cópia experimental isolada e comunicar pendência. A autorização Mestre de 16/10 permite livre criação/manutenção/abandono de réplicas em LAB sob limites, mas não libera originais, regras ou produção.

## 2. O DESCOMPASSO HISTÓRICO QUE VOCÊ PRECISA RECONCILIAR

**Não há apenas uma fonte com tudo.** A página principal da OP Notion tem os registros Stage02–12, R29–R51; preserva as decisões vinculantes R50 e R51. A Biblioteca pessoal mantém os pacotes incrementais até R170. Você deve tratá-los como camadas complementares, não apagar a OP antiga nem transformar Biblioteca em prova de escrita normativa no Notion.

**Artefato de retomada principal na Biblioteca /Comestre/OP-VLAB-FUSION-SANDBOX-01:**

`VLAB_R161_R170_RECEIPTS_TEMPORAL_CROC_ED_CORRECTED_MESTRE_ONLY.zip`

- Tamanho: **15.604.260 bytes**.
- SHA-256 real confirmado: `ab34cad5a0b26455f9a0ad659735867fa3a9a430e526e08fa2dcd6a13b776ed0`.
- 150 entradas ZIP, CRC íntegro, 149/149 hashes listados verificados.
- `R160_BASELINE_EXACT.zip` aninhado: SHA-256 `7b208fe553809df6a999a1e4f9a70d7ad116033e929256bc71dbcd61843f3410`; não modificar o original.
- `R170_PSV_MESTRE_ONLY.md` e `r161_r170/README_RECOVERY_R170.md` dentro do ZIP; PSV avulso na mesma pasta.
- Auditor portátil frio já executado nesta sucessão: `python r161_r170/R170_COLD_PORTABLE_RECOVERY.py <R170-ZIP> <novo-recibo-json>`, resultando `PASS_COLD_INDEPENDENT_RECOVERY`, 5 bancos/413 commits/137 ofensivas, 5/5 checkpoints, regressão local 28/28, 2 adulterações semânticas rejeitadas, matriz de contratos 17 IDs mantida, R160 154/154 e 466/466. **Não foi necessário refazer uma única luta histórica.**
- Este PASS valida integridade/reprodução técnica desse corpus, NÃO é auditor externo de norma nem NAC-PASS terminal.

### Última fronteira R170 — numeradores separados

**R160 antigo:** 9 bancos, 466 commits, 154 ataques/recibos. Dano pós-RD 11.870, Vida realmente retirada 11.808, overkill 62. O exportador antigo mostrava 11.845 de Vida retirada, excesso de 37 em três golpes finais de 13, 13 e 11; `R162` corrigiu a exportação SEM mudar histórico/resolvedor. Exemplo essencial: um golpe causa 73 depois RD, mas HP restante=60: perde somente 60 de Vida, 13 é overkill.

**Nova coorte selecionada R161–R170:** cinco bancos, 413 commits, 137 recibos ofensivos, pós-RD agregado 11.831 = 11.563 HP retirado + 268 overkill. **Não misturar** coorte nova com 154 históricos nem usar os 137 ataques como 137 combates independentes.

**Combates completos adicionais R168:** 2/2 combates condicionais `Auren L3 × Crocodilo de Lodo Astral Ancião L3`; seeds 1168001 DEV e 1169001 RESERVADA NÃO CEGA. Auren venceu em ambos sob política básica física restrita. Em conjunto 66 turnos individuais, 198 commits e 66 ataques por batalha (132 ofensivas entre as duas), Crocodilo 0/66 hits, Auren 66/66 hits. Isso NÃO prova chance universal de vitória nem compara todas habilidades especiais; iniciativa da Besta não possuía proficiência natural específica documentada, então abertura foi exógena. Auren 6d6+193 sempre acima CA112 comum; Crocodilo 6d6+134 tem máximo170 abaixo CA225 de Auren exceto crítico autoacerto; interpretar como cenário condicionado.

**Contratos:** 17/17 identidades originais preservadas na matriz `r161_r170/R170_17_CONTRACTS_BEFORE_AFTER.json`, **0/17 certificados terminais**. Potência oficial baterias A–D: **0/1875**. Sem writer/lease/epoch/fencing; Party/O Primeiro e DMG-RANK nunca modificados. Holdout verdadeiramente cego independente: **0**.

## 3. RESULTADOS CIENTÍFICOS R161–R170 QUE DEVEM SER REUTILIZADOS

**R161–R162: recibo correto.** Distinga dano bruto pré-salvaguarda, dano nativo pós-salvaguarda/pré-RD, dano pós-RD, Vida efetivamente perdida e overkill; não dividir ímpar sem regra de arredondamento. A correção só substitui a interpretação do CSV derivado, não modifica eventos antigos.

**R163: falha transacional.** Caso FRESH_AFTER_INTENT possui 0 eventos e 1 intenção pending `UNKNOWN_EFFECT-HOLD`; NÃO retentar. Caso AFTER_COMMIT possui um commit único, pós-RD100, Vida30, overkill70; falha ao publicar CSV não justifica repetir golpe. Evidência de commit ≠ publicação.

**R164: fontes e gaps.** Grifo-Matriarca Sílica L3: HP4315, CA153, RD75, DES116, prof geral +22 mas **não há prova de proficiência específica na Iniciativa**; Descarga Curta 55 PA, 14d10 Lightning, Reflex CD94, “linha curta” sem alcance métrico. Auren L3: HP523, CA225, RD física35, RD Dark60, iniciativa 6d6+166; RD Lightning NÃO documentada — não presumir zero. Crocodilo L3: HP5580, CA112, RD75, DES64, mordida 6d6+134 e 20d10 física, iniciativa natural específica não comprovada; mix Água/físico parcialmente indeterminável. Feryn/Eristan RD Elemental Vento/Planta indeterminada.

**R165 Flecha de Trava:** 55 PA, Iskiel, alcance 65m, modificador real **−6m até o fim do turno seguinte**. Cena V3 seed1185114: velocidade Auren 16→10→16; mover 9m válido, 11m rejeitado antes de intenção; sete commits. R165 V1/V2 são diagnósticos NÃO aprovados, V2 pendente UNKNOWN.

**R166 Casulo de Brotos/duas AoO:** 60PA, CA Auren225→247, speed16→12 (−4m). Duração “2 turnos” ainda sem fronteira inequívoca: HOLD. Feryn DES80 tem prioridade sobre Varok DES29 (regra AoO R43). Em duas cenas V2, falha crítica negativa R42 e sequência de reação funcionam; cena KO: Auren HP60 sofreu pós-RD114, perdeu 60, overkill54, Varok não atacou nem gastou reação e movimento não ocorreu. A primeira tentativa R166 seed1195392 ficou 1 commit + pending UNKNOWN; não reviver.

**R167 equipe/ED:** sete candidatos para segundo Espiritualista Demoníaco; Auren serve como ED1, mas nenhum segundo ED com ficha e Espírito comprovados foi admitido: **0/7 nessa amostra**, não censo global. Feryn/Eristan/Varok/Iskiel podem servir como NPCs técnicos, NÃO ED por aproximação.

**R168 Crocodilo:** as duas vitórias acima são LAB condicionadas, 0 célula oficial do programa. Preservar possibilidade de crítico e censura em cenários sem dano normal; nunca fabricar vitória impossível ou probabilidade populacional com dois seeds.

**R169 auditoria:** auditores frios independentes do resolvedor para novos bancos; duas alterações maliciosas com hashes SQL refeitos foram rejeitadas por auditoria SEMÂNTICA. Pré-registros DEV e RESERVA NÃO CEGA; nenhum holdout verdadeiramente independente.

**R170:** programa de contratos 17 IDs e 0/1875 oficial intactos; NEXT-5 e HOLD nas fontes. O pacote tem prova portátil de integridade, mas não atualização autenticada na OP Notion até R170. Necessita sincronização apenas por escritor documental autorizado e gate específico.

## 4. DECISÕES DO MESTRE VINCULANTES NO NOTION R29–R51

A Library R170 **não revoga** decisões anteriores. Recupere literalmente as redações originais antes de aplicá-las:

- Rabada do Frígido Ossário: **Luta +6 somente nessa ação**. Investida da Cabra: **Luta +6 própria**. Cabra Bronze1 Reflexo = proficiência + CA, +6 no caso validado; Esquiva defesa26. Não generalizar para qualquer criatura.
- Empate do atacante com Esquiva/Defender favorece a DEFESA. Defesa por Defender só com Armadura/Fortitude legitimamente documentadas; fixture sintética não legitima defesa em uma Besta real.
- Empurrão é **1,5m por 300 Força Física**, não “um bloco”; janelas de reação e renovação seguem fonte competente.
- Crítico positivo válido ACERTA AUTOMATICAMENTE, mesmo se escore comum não supera CA. Uma RD suficiente pode zerar dano sem converter acerto em erro. Falha crítica negativa R42 existe no LAB e não pode ser tratada como norma de campanha sem promoção.
- **R43 Ataque de Oportunidade concorrente:** prioridade determinada pela DES, depois rolagem adequada ao rank/ator e desempate R26; não importar d6 Bronze a ON5 ou L3.
- **R50 Contra-atacar:** somente pode responder quando ataque normal original **ERROU** (hit=false). Deve ser declarado antes do RNG e consumida a reação legal; crítico positivo gera acerto, então NÃO gera resposta, mesmo que RD absorva 100% do dano.
- **R51:** **não existe contra-ataque do contra-ataque**. Se A ataca normal e erra, B pode Contra-atacar legalmente, mas A não pode Contra-atacar a resposta de B, mesmo que B erre e A tenha reação. A poderá responder a um NOVO ataque normal no turno legítimo de B se declarar no momento devido e possuir reação. Essas decisões resolveram dúvidas R47/R48 históricas, porém não equivalem a regressões novas executadas nem canonização automática do Sistema de Combate geral.

## 5. O OBJETIVO DO MESTRE: LABORATÓRIO + BENCHMARKS DE PODER

A diretriz `IBX-101` e o Plano Mestre estabeleceram:

**Bateria A:** perfil virtual de Espiritualista Demoníaco comparador em 25 patamares Bronze1–Lendário5, contra Bestas elegíveis 1×1 e depois grupos. O uso de clone não torna uma criatura existente um novo Espírito Demoníaco.

**Bateria B:** linhagem de Besta-âncora em 25 patamares regulares + duas coortes especiais ADM/Besta Divina quando admitidas (total 27 posições operacionais, NÃO 27 ranks), e painel diverso de Bestas referência. Distinguir mutação controlada da linhagem e diversidade de espécies.

**Bateria C:** equipe de até aproximadamente cinco EDs com papéis complementares e versões virtuais admissíveis nas 25 classificações; não aceitar NPC sem Espírito como ED.

**Bateria D:** comparações de contribuição de armas, habilidades, equipamentos e dano/eixos de potência, sem substituir o cálculo DMG.

A matriz Mestre tem 1.875 células oficiais como denominador, **ZERO válidas até R170**. Todas requerem elegibilidade de fonte, política explicitamente admitida, mecânica completa suficiente e auditoria. Combate técnico com policy reduzida NORMAL não comprova eficácia geral de transformação, magia ou equipe. Censuras e combates impassíveis continuam parte dos dados, não fracassos escondidos.

## 6. FIRST-PENDING DE R170 — TRATAR NA ORDEM DE MÍNIMA DECISÃO

1. Localizar nas fontes canônicas a proficiência/regra específica de **Iniciativa natural** para Grifo ou Crocodilo, ou registrar a mínima decisão a pedir ao Mestre; não tratar prof geral +22 como bônus específico nem inventar abertura.
2. Determinar a **RD Lightning de Auren**, ou a inexistência comprovada segundo a fonte competente, e resolver métrica da “linha curta” do Grifo; NÃO interpretar silêncio da ficha como resistência zero.
3. Esclarecer quando terminam os **2 turnos do Casulo de Brotos** para um ciclo causal real de buff/debuff; preservar R165 Flecha (expiração EXPLÍCITA) como comparador, não generalizar.
4. Localizar e qualificar um **segundo ED real fonte-completo** e papéis de equipe com Espírito e transformação verificáveis; não renomear NPCs como ED.
5. Pré-registrar ensaios independentes/holdout genuinamente cego com motor existente e gate científico; depois iniciar células oficiais somente se todos os requisitos completos e homologados.

Priorize a decisão mínima por subcampo. A ausência de RD Lightning não deve bloquear combates físicos com fontes suficientes; a expiração do Casulo não deve impedir testes sem Casulo. Não use deficiência isolada para declarar toda engenharia paralisada.

## 7. DEZ ETAPAS CONCRETAS — R171+ COMO CONTINUIDADE, NÃO RECOMEÇO

**1. RECOVERY SEM REPEAT:** localizar ZIP R170, PSV, fonte OP R50/R51, 17 contratos originais e READBACK última evidência. **Aceite:** manifesto/recovery intactos, sem rerun de batalha e com fontes posteriores reconciliadas.

**2. AUTORIA/FENCING:** verificar PROFILE CM-000006, claim da própria nova INSTANCE e escritor documental real; IBX-101, IBX-99/95; sem ACK forjado. **Aceite:** estado AUTH claro, produção HOLD.

**3. BUGS FONTE/MECHANICS:** pesquisar iniciativa/RD/alcance/limites com fonte primária e versão, abrir pedidos mínimos ao Mestre se indispensável. **Aceite:** matriz fonte→campo→status, sem default indevido.

**4. TEMPO E REAÇÃO:** usar R165 Flecha e R166 Casulo para testar expiração e prioridades documentadas, mais decisões R50/R51 para Contra-atacar. **Aceite:** eventos/checkpoints e rejeições causalmente coerentes em bancos NOVOS; não alterar os antigos.

**5. ATORES COMPLETOS:** montar um novo confronto ED×Besta mais fiel com iniciativas, defesas, custos, habilidades verdadeiras, alcance e condições de derrota; fixture separa escopo reduzido. **Aceite:** primeiro novo duelo fonte-admissível além das políticas reduzidas, ou blocker específico inatacável.

**6. CONTRATOS DOS 17:** priorizar `REACTION_TRIGGER_AND_SINGLE_USE`, `TURN_SCHEDULER_EVENT_SOURCING`, `RNG_REPLAY_STATISTICS` e as lacunas materiais descobertas. Comparar requisito R18 original, evidência anterior e nova; não contar PASS local como terminal. **Aceite:** delta verificável em contratos, preservando 17 IDs.

**7. SEGUNDO ED/EQUIPE:** selecionar ED com Espírito verdadeiro e conjunto de habilidades/custos, depois combinação 2×1 e incremento até papéis complementares; cenários sem fonte ficam em HOLD específico. **Aceite:** equipe/arquétipos realmente elegíveis, sem NPC maquiado.

**8. CIÊNCIA DE BENCHMARKS:** implementar e alimentar com fonte real as primeiras células A/B/C/D legitimamente admissíveis. Controlar p_acerto, dano condicional/bruto/pós-RD/HP, PA, ações, reação, controle, mobilidade, turnos, censura. **Aceite:** matriz mostra 0→N apenas em células que cumpriram TODOS os gates; caso contrário honestos 0/1875.

**9. REPLAY E HOLDOUT:** novos seeds pré-registrados, separação DEV vs HOLDOUT CEGO, auditoria fria independente de causalidade/estatística, cópias adversariais e checkpoints. **Aceite:** reprodução causal, incerteza sem generalização a partir de poucos duelos.

**10. ENTREGA FUNCIONAL/INTEGRAÇÃO:** demonstrar ao Mestre cena turno a turno e relatório de poder, preparar pacote para DMG sem duplicar coortes, registrar por writer competente na OP existente, enviar Inbox real com readback e NAC-PASS proporcional. **Aceite:** capacidade nova versus R170, artefatos SHA e limites claros, zero mutação Party/DMG-RANK/campanha.

## 8. CONTROLE DE UNKNOWN-EFFECT / NÃO REPETIR

**Intocáveis:** R01–R160 originais; R157–R159 bancos/ataques históricos; R163 FRESH_AFTER_INTENT com pending; R165 V2 pending; R166 V1 pending; R169 V1 diagnóstico WAL; R123/R134/R143/R156 UNKNOWN históricos; R130 QA_FAIL, R138 SPATIAL_PARITY_HOLD, R124 5×5 censurado, R159 meia-ímpar bloqueado. Não reexecutar, apagar pending, transplantar evento, editar row-SHA para “fechar” efeitos, reciclar RUN-ID, nem contar cenas técnicas como lutas oficiais. Para novos casos, cópia limpa isolada com IDs e seeds novos.

**Não modificar** o ledger R18 original, R26, v0.8.1, motores históricos, DMG-RANK, páginas de Besta reais, personagens, Party ou O Primeiro. Se a ferramenta precisa ser evoluída, fazer módulo ou fork experimental versionado e prova regressiva.

## 9. RIGOR CIENTÍFICO

Para cada cena registrar origem/versão, atores, equipamentos, nível, Espírito, modo normal/transformado, atributos, CA/defesas, tipo/absorções, recurso PA, ação, reação, seed RNG, stream, comandos aceitos/recusados, eventos, dano e mitigação, estado final, checkpoint, replay, censura, auditor e SHA. Somente o que foi fisicamente executado é `SANDBOX EXECUTADO`. Fixture sintética ≠ combate oficial. Teste de motor ≠ potência populacional. Cinco bancos ≠ cinco espécies independentes. Dois duelos versus Crocodilo ≠ taxa de vitória universal. `RESERVADA NÃO CEGA` ≠ holdout independente.

O motor deverá separar:

- Dano pré-salvaguarda (quando disponível);
- dano bruto nativo pós-salvaguarda;
- bruto condicional ao acerto;
- dano pós-RD;
- **HP realmente retirado** (min entre dano pós-RD e HP restante);
- overkill;
- probabilidade de hit segundo ficha/CA/reação;
- dano esperado por tentativa sob condições explícitas;
- dano real do combate;
- cenários de impasse e censura.

A parceria VLAB↔DMG usa recibos `R162` histórico corrigido (154) e `R169` novo (137) separadamente; envio não significa ACK de DMG. Acordo de contexto e autoridade de dados é obrigatório.

## 10. PRIMEIRA RESPOSTA DO SUCESSOR E GATE FINAL

Comece sua primeira resposta com um PSV de sucessão contendo **AS-OF, CM-000006, INSTANCE-ID candidata (não inventada), OP, BASELINE, LAST-VERIFIED-UNIT, FIRST-PENDING, DENOMINATORS separados, NO-REPEAT, CONFLICTS, UNKNOWN-EFFECT, AUTHORITY/WRITER, NEXT-5, TARGET-REMAINDER, NAC-PASS**. Diga explicitamente que R170 verificador frio passou e que a OP Notion não prova R170 até sincronização competente; verifique fatos posteriores antes de prosseguir.

**Sua primeira meta funcional nova é aproximar um duelo/benchmark Fonte-Completo e reduzir blockers concretos — sem repetir R168.** Se a prova ficar impedida por uma única decisão normativa, formule a pergunta mínima com alternativas e consequências, mas continue em paralelos tecnicamente independentes.

**Não afirme:** 17/17 contratos terminais; uso oficial 1875; win-rate universal; ausência de RD por silêncio documental; segundo ED fictício; implementação geral das decisões R50/R51 sem regressão; ACK IBX-101; tomada de writer pelo encerramento do chat anterior; sincronização OP não realizada; produção liberada.

**Pergunta de encerramento obrigatória:** “O que o VLAB realmente consegue executar e medir agora que não conseguia em R170, e quantos dos 17 contratos e das 1.875 células oficiais foram legitimamente avançados, sem transformar laboratório em campanha?”

**— Ordem do Mestre / Comestre Coordenador, exclusivamente MESTRE-SIDE.**
