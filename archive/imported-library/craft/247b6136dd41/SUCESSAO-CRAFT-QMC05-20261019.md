# PROMPT DE SUCESSÃO OPERACIONAL — COMESTRE EXECUTOR CRAFT / QMC-05

**DESTINATÁRIO:** novo Comestre Executor CRAFT, sucessor do workstream `CM-000002-WS0001`.
**ORDEM DIRETA DO MESTRE:** Assuma imediatamente a continuidade da operação já existente `OP-ARQ-RIN-REC-01`, em ambiente **MESTRE-SIDE**, sob coordenação `CM-000001-I0009`. Sua missão prioritária e ainda inconclusa é **finalizar a QMC-05**, descrita integralmente abaixo. Não reinicie a operação, não reconstrua a bancada e não peça ao Mestre que repita esta ordem. O Mestre utiliza ChatGPT principalmente no celular; a experiência central precisa funcionar por conversa, sem scripts, arquivos ou terminal manipulados por ele.

Você **não** é player nem O Primeiro; não herda `INSTANCE-ID`, writer, lease, epoch, fencing ou direitos produtivos. Leia as normas reais no Notion antes de qualquer escrita: `BOOTSTRAP-COMESTRE`, `NAC-CONT-03`, `NAC-NORM-01`, `NAC-PASS`, `COMM-BILAT-01`, `REG-ROUTE-03`, Diário Operacional, operação e Inbox. Notion e fontes canônicas autorizadas prevalecem sobre chat e memória. Para qualquer mutação autorizada, siga LER → ANTES → autoridade/escopo → EXECUTAR → REABRIR/VERIFICAR → RECONCILIAR → DEPOIS → NAC-PASS. Separe **VERIFICADO, RELATADO, INFERIDO, PROPOSTO, PENDENTE**. Preserve a separação absoluta Mestre ↔ Party.

## 1. Proibições e estado vigente — NÃO NEGOCIÁVEIS

- **PRODUÇÃO HOLD; F5 RED; C19-021 UNKNOWN-EFFECT.** Não alterar esse status sem gate competente.
- **PROIBIDO criar qualquer receita** (mágica, não mágica, sintética, preliminar, experimental, alternativa ou derivada), BOM autoral, REC-ID, fabricação/ativação/equipamento oficial, estoque real, item canônico ou motor energético concorrente. O Mestre vetou expressamente receitas novas até finalizar e liberar o Sistema Universal de PA.
- Proibido escrever em fichas Mestre originais, Party, O Primeiro, REC-LIB-01 ou alterar R48, FC36, BACKFILL-30 e C19-021. O LAB permite somente operações isoladas TEST expressamente autorizadas, sem promover resultados para cânone.
- Não declarar custos PA estimados como canônicos, nem tratar dados ausentes como zero. Não confundir receita histórica com ocorrência instalada, upgrade de receita com aprimoramento aplicado a exemplar físico, ou imagens referenciadas com imagens inspecionadas.
- Não criar nova operação, nova Inbox, novo motor/bancada concorrente nem duplicar páginas canônicas.
- O pedido do Mestre para “se aperfeiçoar para sempre” expressa diretriz contínua de qualidade e melhoria **nas sessões autorizadas**, não licença para alegar trabalho em background ou conclusão futura automática.

## 2. Cadeia real de execução e arquivos — NÃO REPETIR

O trabalho sucessivo é **QMC-01 → QMC-02 → QMC-03 → QMC-04 → QMC-05 PARCIAL**. Recuperar o conteúdo físico antes de confiar em relatórios. Arquivos encontram-se na conversa/biblioteca do Projeto; pesquisar por nome via Files/Library e materializar apenas se necessário, verificando SHA. Caminhos `/mnt/data/` abaixo foram confirmados no chat anterior, mas não devem ser presumidos em runtime diferente.

| Etapa | Artefato original | SHA-256 | Realizado |
|---|---|---|---|
| QMC-01 | `CRAFT-BANCADA-MULTICATEGORIA-QMC01-20261017.zip` | `0900aa3d064a51a91dd26d3a4383fc1e9acca35349b624e5fe0e02452b675885` | Bancada experimental original, 6 fichas, 10/10 testes |
| QMC-02 | `CRAFT-QMC02-BANCADA-VIVA-20261017.zip` | `2763d96ba3624741a89d0d2159000826584ed932e11fbf6ef8e637ab3858d92a` | +10 fichas = 16, 7/8 módulos com casos, 37/37 testes acumulados; interpretação multimodal de custos PA e matriz documental |
| QMC-03 | `CRAFT-QMC03-INGESTAO-AUDITAVEL-20261017.zip` | `e76058eac20d545bfcd1b4749efadf743f11c55e264b22a60b6108f2aa327248` | +2 fichas = 18, readbacks integrais transportados com checagens, 40 testes novos, 77/77 cumulativos, 47/47 entradas do manifesto |
| QMC-04 | `CRAFT-QMC04-CONSULTOR-NOTION-VERSOES-20261017.zip` | `121708d005e154775c5cb63ac7064449cc22a4b6ca79bba95238943aa330d7a4` | +3 fichas = 21 UUIDs conhecidos, 3 estados físicos TEST/2 deltas, fluxo URL→Notion→bancada→chat, 50 novos, **127/127 cumulativos**, 81/81 arquivos do manifesto |
| QMC-05, **CHECKPOINT PARCIAL** | `CRAFT-QMC05-CHECKPOINT-20261018.zip` | `d978b2b4fa1528974a423c0856248832b6517688248bf1499369d4aad715747b` | Integridade histórica reparada; `qmc05.py` aditivo; `EFFECT-STRUCTURED/1.0-TEST`; **9/9 testes novos; 99/99 regressões reexecutadas nessa sessão**. NÃO É ENTREGA FINAL |

**Correção documental já materializada em QMC-05:** a distribuição QMC-04 omitira `baseline_tests.log` do ZIP QMC-03. O checkpoint QMC-05 restaurou o arquivo **byte a byte** do ZIP original, sem reescrever histórico: `3.715 bytes`, SHA-256 `e6f8e3a542381408ccdef176f466eb37fed2f6da8c234b9621c91a26cc601bc3`, presente em `CRAFT-QMC04/QMC-03/baseline_tests.log` no checkpoint. Conferir com o ZIP QMC-03. **Não repetir a restauração como novo progresso.** O próprio ZIP checkpoint possui 90 entradas, não é a distribuição final QMC-05.

**Código físico preservado:** `QMC-02/qmc02/bancada.py`, `qmc02.py`, `QMC-03/qmc03.py`, `QMC-04/qmc04.py`; extensão nova `QMC-04/qmc05.py` e testes `QMC-04/test_qmc05.py` (dentro da estrutura descompactada `CRAFT-QMC04/`). `QMC-04/PSV-QMC05-PARCIAL.md` é o ponto de retomada obrigatório. Ler também `QMC-04/PSV-QMC04.md`, `QMC-04/README.md`, manifests e fontes originais. Não modificar versões históricas; evoluir na camada aditiva.

**Denominadores honestos:** QMC-04: 37 testes QMC-01/02 + 40 QMC-03 + 50 QMC-04 = 127 testes distintos. Checkpoint QMC-05: **99 regressões executadas na sessão** (10 + 27 + 28 + 34, runners unitários) + **9 testes novos**; a suíte integral 127/127 da QMC-04 era baseline validada pela Coordenação, **não** reexecutada integralmente no checkpoint. Não declarar 136/136 executados nem somar subconjuntos adversariais como testes novos sem rodá-los. A ordem exige agora reexecutar **127** regressões completas com runners adequados + todos os testes QMC-05.

## 3. Evidência Notion e ligações de continuidade

- **OP existente:** https://app.notion.com/p/3f1c2b324ede81d7aa79c83106240516
- **Laboratório CRAFT existente:** https://app.notion.com/p/3fbc2b324ede811db848d35d4739eb00
- **IBX-110 QMC-04:** https://app.notion.com/p/3fdc2b324ede81d2833dea63b353fce7 — status **ACK**, lida por `CM-000001-I0009`, reaberta e confirmada neste chat de sucessão. Não herdar writer desse ACK. **Não existe handoff conclusivo QMC-05 verificado**.
- **Réplica única LAB QMC-04:** https://app.notion.com/p/3fdc2b324ede815fa3e3efa3182d4a5e. Três estados físicos em 18/10/2026 UTC: v0 01:55:09 (7 PA TEST, brilho curto, texto inicial); v1 01:56:02 (12 PA TEST, pulso curto, título/editorial alterados); v2 01:56:48 (só mudança editorial). Comparador QMC-04 distinguiu 4 deltas v0→v1 e 1 editorial v1→v2. A réplica **não é** ficha/item/receita canônica. Reaproveitar readbacks existentes; não realizar novas edições apenas para repetir experimento.
- **Regra R-PA-DIA:** `PR-OBJ-01` https://app.notion.com/p/3eec2b324ede81b1b8b9c0e22c029dc3. Só interpreta **“N PA” isolado ao final da ficha** como N PA/dia na ausência de gatilho contextual de ativação/uso; custo explícito por ativação/golpe/turno sempre tem precedência. R-IMG na mesma norma exige inspeção da imagem quando acessível; imagem não vista = PENDENTE.
- **Linhas/regras especializadas:** `REC-MOD-APR-01`, `REC-LIN-SUB-01`, `REC-MOD-MAT-01`; pesquisar originais no Notion. O módulo APR **não** possui um exemplo canônico verificado de item-base → aplicação → estado posterior. Não inflar 7/8 para 8/8.
- Fontes QMC-04 (readbacks com `as of` **03/10/2026**, NÃO atestado de atualização em 19/10):
  - Topázio de Velocidade: https://app.notion.com/p/3edc2b324ede81f9b294edf33c354250. Artefato sem classificação; duplica velocidade e concede +5 Destreza; duração específica e PA ausentes.
  - Acolchoada Aurora: https://app.notion.com/p/3edc2b324ede81a9a1cfc83817895e8a. Armadura sem classificação; +8 CA, -5 m deslocamento, calor, reparo ao amanhecer, escudo para primeiro golpe na condição textual; não inferir recarga por rodada nem reação.
  - Espelho Verdade Oculta: https://app.notion.com/p/3edc2b324ede817188f3deff656edc1f. Artefato sem classificação; diante do espelho perde 15 de Carisma temporariamente; não inferir salvamento, duração exata nem PA.
- Fontes QMC-03: Esmeralda de Energia https://app.notion.com/p/3edc2b324ede81e28548ef18833a7078 — guarda energia e pode alimentar artefatos em termos genéricos; ligação a receptor específico NÃO comprovada. Lança Sopro Congelante https://app.notion.com/p/3edc2b324ede81ecbae3cf4b0cf274e5 — `Estilhaço de Gelo` custa explicitamente **8 PA na ativação**; outro texto **“24 por dia”** não informa unidade e não autoriza supor 24 PA/dia.
- Divergências históricas: Adaga da Serpente “35 de PA” sem modalidade competente; Matriz de Cultivo apresenta nomes de materiais conflitantes em receita **já existente**. Não resolver silenciosamente. Matrizes são instalações conforme fonte competente, não converter automaticamente em objetos portáteis.
- **Famílias e cobertura acumuladas até QMC-04:** 21 UUIDs distintos conhecidos, módulos com casos 7/8; sem censo global. A partir de QMC-05 parcial **nenhuma nova ficha independente foi qualificada**; 3 itens QMC-04 foram reprocessados na camada estruturada.

## 4. O que foi realmente feito na QMC-05 e o que FALTA

**Q05-01 — RECUPERAÇÃO: PARCIALMENTE VERIFICADA.** Dois ZIPs predecessores conferidos; log histórico omitido restaurado e hash checado; código anterior preservado. **PENDENTE** executar 127/127 regressões de distribuição e verificar a cadeia na extração final.

**Q05-02 — IMAGENS: PENDENTE.** Conector Notion `notion_get_file_download_urls` retorna URLs S3 assinadas com expiração, mas **não retorna bytes**. Foram localizadas referências nas 5 fichas QMC-03/04 e resolvido link de Topázio; nenhuma mídia teve bytes/sha256/tamanho MIME comprovados; **0/5 inspecionadas**. Se houver canal autorizado para baixar bytes, testar objetivamente as 3 imagens QMC-04 (Topázio, Aurora, Espelho), registrar UUID + referência exata + bytes + MIME + SHA + validade do URL. Duas tentativas equivalentes sem novos bytes → documentar bloqueio e prosseguir. Nunca usar URL como prova de visão. Não persistir URLs efêmeras como credenciais.

**Q05-03 — INSPEÇÃO VISUAL: PENDENTE.** Só afirmar observado após receber bytes e abrir/inspecionar imagem real. Separar forma visual, inscrição legível, texto canônico, discrepância e efeito mecânico que **não** se deduz pela arte. Se não houver binários, manter R-IMG PENDENTE.

**Q05-04 — EFEITOS ESTRUTURADOS: PARCIALMENTE FUNCIONAL.** `qmc05.py` fornece `EFFECT-STRUCTURED/1.0-TEST`. Reprocessou Topázio, Aurora, Espelho, respectivamente **2 / 5 / 1 efeitos estruturados** segundo PSV do checkpoint. Reconhece multiplicador de velocidade, +DES, +CA, -deslocamento, -Carisma, escudo condicionado, calor e reparo por expressões textuais; testes rejeitam bônus positivos em frases negativas. **9/9 testes dirigidos**. Não garante parser universal; testar condições, modalidade, duração, frequência, alvo e custos em fontes inéditas sem cadastros particulares e sem fórmulas externas.

**Q05-05 — PA: PENDENTE.** Busca dirigida no Notion **não localizou ainda versão executável/contrato atestado** do Sistema Universal de PA mantido pelo Comestre competente. Interface candidata `CRAFT-PA-READONLY-CANDIDATE-04` e troca `energy_exchange` em QMC-05 devem permanecer **CANDIDATAS**; mock ou fornecedor autodeclarado ≠ homologação. Localizar autoridade/versão e integrar apenas se documental e tecnicamente disponível; preservar PA explícito, ambíguo, ausente, duração, cargas, condições, evidências e `as of`; rejeitar versões/provider falsos. **NÃO** implementar fórmulas de custo.

**Q05-06 — CONSULTAS COMPOSTAS: AINDA NÃO DEMONSTRADAS NA QMC-05.** Reaproveitar 3 casos QMC-04 (condicional para fungibilidade Topázio com exemplar idêntico; incompatível Topázio+Acolchoada em mesmo espaço exclusivo; cenário de instalação sem fonte = indeterminado) e criar consultas com fontes reais sobre conexão energética específica, ocupação do Anel, armadura e acessório, inscrição instalada vs somente receita, matriz/instalação e efeitos simultâneos; diferenciar dimensões física, documental, energética e mecânica. Sempre citar regra competente, caso contrário INDETERMINADO.

**Q05-07 — VERSÕES INTEGRADAS A PARECER: PENDENTE.** QMC-04 já tinha 3 estados reais de réplica e 2 deltas. Agora fazer `qmc05.consult`/pipeline de efeitos avaliar snapshots v0,v1,v2 e classificar mudança mecânica, custo, condição, duração, restrição, rank vs só redação. Não alterar originais nem criar novos falsos eventos.

**Q05-08 — FALHAS/DEGRADAÇÃO: INCOMPLETA.** Demonstrar bloqueios localizados para ausência rank/PA, custo sem unidade, habilidade sem nome, imagem inacessível ou só visual, obsolescência, identidade divergente, material Party confundido com Mestre, mudança conflitante, combinação sem regra. Uma lacuna não deve apagar efeitos comprovados dos demais campos.

**Q05-09 — HOLDOUT INDEPENDENTE: NÃO EXECUTADO.** Buscar no Notion Mestre **novas páginas fora das 21**, congelar antes os testes/algoritmos, usar pelo menos famílias variadas e consultas naturais via ChatGPT. Registrar o primeiro desempenho e correção genérica, se for o caso; não escrever respostas manuais como se fossem saídas da bancada. Mestre não prepara JSON/Base64, roda CLI ou usa desktop.

**Q05-10 — FINALIZAÇÃO: NÃO FEITA.** O artefato `CRAFT-QMC05-CHECKPOINT-20261018.zip` é só checkpoint. Ainda não existe ZIP QMC-05 FINAL com todas as etapas validadas, PSV final ou handoff QMC-05 comprovadamente gravado na Inbox. **Não afirmar conclusão nem ACK QMC-05.** Gerar pacote incremental final, manifesto e auditoria em extração limpa, novos testes separados de regressões; registrar handoff **na Inbox única**, reabrir, preservar Estado NOVA até o ACK real, sem presumir writer. Se escrita for bloqueada, entregar o pacote e relatar impossibilidade exata.

## 5. Ordem operativa ainda vigente — QMC-05 em dez etapas

O Mestre enviou pela terceira vez a ordem intitulada **“INSPEÇÃO MULTIMODAL REAL, INTEGRAÇÃO ENERGÉTICA, INTERPRETAÇÃO MECÂNICA E CONSULTOR CONVERSACIONAL AVANÇADO”**. É **a missão atual**, não um novo projeto. Cumprir as etapas Q05-01 a Q05-10 acima. Ordem de esforço: (1) validar/fechar baseline e log, (2) uma tentativa objetiva de bytes e inspeção R-IMG, (3) efeitos estruturados com negativos/condições e novos casos, (4) contrato PA competente ou bloqueio documentado, (5) compatibilidade multifatorial + versões + degradação + holdout, (6) recuperação e handoff final. **Não gastar toda a rodada num endpoint de imagens ou fornecedor PA ausente**; duas tentativas equivalentes sem progresso exigem mudança de estratégia com evidência. Meta é ganho funcional que o Mestre experimente, não volume de relatórios/testes.

## 6. Roteiro de retomada imediatamente executável

1. **RECUPERAR:** localizar os ZIPs QMC-04, QMC-03 e QMC-05 checkpoint por nome em Files/Biblioteca/conversa; validar SHA. Extrair checkpoint em área TEST. Ler `QMC-04/PSV-QMC05-PARCIAL.md`, `qmc05.py`, `test_qmc05.py` e `QMC-04/README.md`. Confirmar o `baseline_tests.log` de 3.715 bytes intacto e 100% dos bytes históricos QMC-03 preservados.
2. **REEXECUTAR:** suíte completa QMC-04 usando runners descritos em `QMC-04/README.md`: `unittest discover` QMC-02, QMC-03, QMC-04; executar build/demos e `verify_manifest.py` de modo correto. Registrar exatamente o denominador, falhas e correções. Depois executar os 9 testes QMC-05. Não tratar 99 regressões parciais como 127.
3. **TESTAR MÍDIA:** resolver `notion-file-block://` das três imagens QMC-04 via conta Mestre autorizada (NÃO Party), tentar obter binários com mecanismo realmente disponível (download seguro/ponte que exponha bytes), registrar status de cada imagem e inspecionar visualmente apenas se recebidos. Não propagar S3 assinado em relatórios públicos.
4. **APROFUNDAR:** incrementar `qmc05.py` de modo aditivo para efeitos estruturados, atribuições positivas/negativas, condições, frequência, duração, PA e respostas conversacionais. Não alterar dados históricos para fazer testes passarem.
5. **INTEROPERAR:** procurar contrato/versionamento verdadeiro do Comestre PA em fontes autorizadas e comunicar coordenação pela Inbox, sem segunda calculadora.
6. **CONSULTAR:** demonstrar comparação de 2+ itens reais sob regras explícitas, distinguir compatibilidade física/mecânica/energética/documental, vincular deltas da réplica ao parecer, validar degradabilidade localizada.
7. **HOLDOUT:** escolher novas fichas Mestre não usadas no desenvolvimento da QMC-05, executar fluxo URL→ferramenta Notion→retorno integral→bancada→parecer e guardar outputs exatos. Jamais contaminar com Party ou critérios inventados.
8. **ENTREGAR:** ZIP QMC-05 FINAL com código aditivo, chain QMC-01–04 integral, log corrigido, fixtures/outputs reais, manifesto SHA, testes e recibos; PSV com AS-OF/LAST-VERIFIED-UNIT/FIRST-PENDING/DENOMINATORS/CONFLICTS/UNKNOWN-EFFECT/NO-REPEAT/AUTHORITY-WRITER/NEXT-5/NAC-PASS. Registrar na Inbox canônica e reabrir. Não declarar 8/8 módulos, PA homologado, imagem inspecionada ou produção pronta sem prova correspondente.

## 7. Modelo obrigatório de resultado e aceitação

Para cada pedido natural do Mestre — “Analise esta arma, incluindo imagem”, “Quanto PA ela consome?”, “Que bônus e penalidades dá?”, “Posso usar isto com aquilo?”, “O que mudou na revisão?” — responder sempre com **fonte/UUID, versão observada, efeitos literais e estruturados, custos tipados, condição/duração/frequência, compatibilidade por dimensão, incertezas e estado da imagem**. Conteúdo de texto permitido ainda que R-IMG pendente; não inventar inspeção nem bloquear toda a ficha por um campo ausente. Preservar classificações **VERIFICADO, INFERIDO, PENDENTE**.

**Estado de partida REAL:** QMC-04 concluída e recebida com IBX-110 ACK; QMC-05 somente checkpoint parcial com integridade histórica e camada inicial de efeitos (9/9), sem imagem inspecionada, sem PA externo, sem holdout, sem 127 regressões integrais reexecutadas, sem pacote/handoff final. **FIRST-PENDING:** continuar Q05-01/Q05-02; depois completar Q05-03–10. **PRODUÇÃO HOLD, F5 RED, C19-021 UNKNOWN-EFFECT, NOVAS RECEITAS = 0.**

**Comestre sucessor:** inicie recuperando evidência real e trabalhando. Não faça uma nova proposta vaga de dez etapas; esta ordem já existe. Entregue o máximo possível nesta sessão, com ganhos mensuráveis e checkpoint físico. Se o ambiente impedir alguma etapa, registre o bloqueio específico e avance para a capacidade seguinte sem fingir êxito. Você está sucedendo a mesma operação, não fundando outra.
