# VLAB R24 — Primeiro receptor de fonte real e compatibilidade nativa CONDICIONAL

**MESTRE-SIDE / OP-VLAB-FUSION-SANDBOX-01 / CM-000006 (identidade lógica; nenhuma INSTANCE-ID anterior assumida)**  
**Classificação:** implementação real de receptor com falha fechada, **NÃO é admissão de ataque canônico**. Pesquisa de dano DMG e alteração de regras continuam em suas autoridades. A ordem do Mestre exigia, idealmente, o primeiro ataque REAL INTEGRAL; esse marco **não foi atingido**, e este relatório identifica exatamente por quê.

## Entrega funcional R23 → R24

1. R23 íntegro recuperado da Biblioteca (`libfile_b9343973ee908191be76cfebe03c741b`); SHA-256 `e017b356719334de0c26b306c74bbae52de2ea5a6ccc8361137fb98b3c952ce3`; antigo executor, seus 32 combates, R22 e duelo Vigias ficaram **inalterados**.
2. `fusion_stage12/vlab_r24_real_source_receiver.py`: novo ponto de entrada **separado** do simulador, valida envelopes no formato R31, seus `receipt_id`/`content_sha256` e os cinco gates; lê fontes documentais com versão e trechos observados; **recusa** despacho integral nas três ações reais examinadas. Nenhuma regra de dano, iniciativa ou reação foi reimplementada.
3. **Prova física positiva no resolvedor v0.8.1:** o componente **Patada `1d4+DES13`**, proveniente da ficha Galidemus Bronze 1, chegou ao `UnifiedSyntheticGateway`/`RebuiltManualRuntime` preexistente. Com d4=2 obteve **15 de dano solicitado**, produzindo exatamente **um evento nativo com hash** e alteração de um ALVO FICTÍCIO 40→25 HP. Replay determinístico demonstrado. **Essa cena força a pontuação de acerto 999, RD fictícia 0 e custo de PA fictício zero.** Logo o evento **NÃO** prova legalidade de Patada verdadeira, nem autorização para B01–B18, luta canônica ou célula de benchmark. A fonte do número é real, o **contexto do teste é fictício**. Recibo: `R24_GALIDEMUS_NATIVE_COMPONENT_ONLY_RECEIPT.json`.
4. Leitura própria das 3 fichas no Notion e das regras oficiais `Sistema de Combate`, `Criação de Besta`, `DMG-RANK-01` e `Criação de Ficha`; arquivos de pré-flight distinguem valor expresso e inferência geral. SHA dos trechos é **da transcrição numérica observada**, não exportação byte a byte da página. Não foi atestada fonte nativa nem congelamento de cena.
5. Receptor R31: consultados o fornecedor R31 (`libfile_e0844d660140819198a757dab943ffdc`), relatório e guia originais. O texto integral extraído do fornecedor (21.556 bytes, SHA-256 `7a1b5083854e8720c2f6d216b814e532126af20e127477af463398fc9a27b9d8`) foi preservado como **texto extraído, não cópia binária original**. O ZIP R31 da Biblioteca (`libfile_03db9a6705b08191ad5347c55332207c`) foi encontrado, mas a cópia de bytes ao container foi recusada (`no authorized raw-byte materialization path`). Assim, **0 envelopes autênticos produzidos por execução da R31 foram fisicamente consumidos**. Um **EXEMPLO SINTÉTICO DE SCHEMA**, explicitamente rotulado, foi validado em 5 gates com `DENY`, demonstrando funcionamento do receptor; NÃO é ACK, integração DMG→VLAB ou parecer científico. Campo forjado de despacho é recusado mesmo com checksum recomputado. Os checksums R31 são verificações de consistência, **não assinaturas criptográficas de autoridade**.

## Reconciliação DEFENDER — estado normativo versus runtime

Fonte oficial `Sistema de Combate`, página `3ebc2b32-4ede-81f1-be4b-e8804ac113c0`, diz **1 Reação em um turno**; Defender, Esquivar e Contra-atacar são anunciados **antes do ataque adversário**. Ataque de oportunidade e reflexão também consomem Reação. A regra documenta **consumo do orçamento** e instante de declaração; não especifica de modo inequívoco o evento técnico de **recarga** (começo do próprio turno? encerramento de rodada? outra fronteira). O R18 atual renova Standard e Movimento em `_next_turn`, e **deliberadamente deixa `reaction_auto_refresh=False`**. Readback de um banco R23: 6 entradas `TURN_START`, 2 reações DEFENDER (cada participante uma), 0 renovações automáticas. Isso demonstra **desvio/omissão temporal de implementação potencial**; não autoriza assumir reação única para a luta inteira nem inserir novo instante por costume de D&D. **Conclusão: defesa R23 com HOLD de validade como baseline canônica**, preservando todos os recibos originais. Decisão Mestre/NAC-NORM-01 precisa definir janela de restabelecimento aplicável, incluindo ataques de oportunidade, contra-ataques, esquivas, efeito interruptivo e idempotência. Código histórico não alterado.

## Fontes reais — diferenças que NÃO devem ser autocorrigidas

| Fonte Notion (rank) | Ação explícita | Vida ficha / referência geral condicional | Alma ficha / referência geral condicional | CA ficha / referência geral não arredondada | Requisito específico não resolvido |
|---|---|---:|---:|---:|---|
| Galidemus Bronze 1 | Patada `1d4 + DES`, cortante | 32 / 46 | 32 / 46 | 21 / 24,2 | Atributo/perícia de acerto da Patada, geometria, fonte íntegra, custo, reação, integridade do ator |
| Cabra de Chifres Bronze 1 | Investida `1d6 + FOR`, impacto | 38 / 50 | 22 / 42 | 20 / 20 | **Empurrão obrigatoriamente acoplado**: distância, gatilho, momento e aplicação |
| Raposa Flamejante Bronze 2 | Bola de Fogo `1d4+5`, efeito de rastro | 40 / 60 | 52 / 82 | 25 / 25 | Conjuração, alcance, custo, acertar/salvar, rastro e duração |

A referência geral é a fórmula em `Criação de Besta` (`HP=30 + nível×(10+CON)` e `Alma=30 + nível×(10+INT)` para Bronze normal) aplicada **sob hipótese condicional explícita de ausência de outros traits/overrides**; o valor da ficha não foi substituído. CA de Besta normal é `10+DES+CON/5`, e seu arredondamento global depende da norma competente. Referências gerais: `https://app.notion.com/p/3ebc2b324ede81f4992ac88a3588cacd`. Fichas: Galidemus `https://app.notion.com/p/eddc2b324ede829f8a75011e8acbf429`; Cabra `https://app.notion.com/p/391c2b324ede8252b0cc810423cdbfa6`; Raposa `https://app.notion.com/p/4d0c2b324ede827b9925018be01e60ca`. DMG-RANK v1.1 mantém precedência de dano explícito e não recalibra nenhuma ocorrência automaticamente.

### Gate de ação real, não de componente

- A: declaração genérica ataque padrão possível; **atributo/perícia específicos, alvo e janelas ainda não resolvidos**.
- B: dano explícito conhecido, mas **efeito integral ainda incompleto** (empurrão, rastro nos outros casos).
- C: v0.8.1 processou componente **em cena de acerto forçado**, não prova resolução integral da ação real nem alcance/rider/PA.
- D: R18–R23 provaram transação para **fixtures técnicas**, não para essa ação/ator verdadeiro.
- E: fonte atual lida, mas **snapshot completo nativo, versão da relação hierárquica e aceite do dono ainda não atestados**.

Todos os gates requeridos precisam passar. Requisitar ação real pelo novo CLI devolve `HOLD_NO_NATIVE_DISPATCH` **antes de instanciar o motor**. Não transformar código de prova em promoção automática.

## PSV com denominadores separados

| Medida | Estado R24 |
|---|---:|
| Fontes candidatas Notion relidas | 3/3, lote dirigido, não censo global |
| Ações reais **integralmente admitidas** | **0/3** |
| Eventos nativos de **ação real admitida** | **0** |
| Eventos nativos de **componente documental em cena artificial** | **1** (separado) |
| Replays do ensaio nativo condicionado | 1 par idêntico / 1 |
| Combates completos com duas fontes reais | **0** |
| Células científicas efetivamente creditadas | **0/1.875** |
| Cobertura canônica dos 25 rank/estrela | **0/25** |
| Envelopes **reais** R31 consumidos | 0; código do fornecedor consultado |
| Menus de R31 simulados para teste de schema | 1/1, DENY |
| Testes novos R24 | **15/15 PASS** |
| Testes regressivos proporcionais BENCHMARK_AUTO R23 | **9/9 PASS** |
| Total efetivamente reexecutado R24 | **24/24 PASS** |
| VLAB terminal | **0/17** |
| DMG B01–B18 | **1/18** |
| STRICT | **0/2** |

R23 preservou 32 batalhas de engenharia, **não reexecutadas por volume em R24**, e duelo Vigias rev1 permanece congelado no checkpoint `libfile_ce5587e0cafc819182a0c8955aaca966`. Nenhuma UAT real ou combate oficial executado nesta rodada.

## Retomada exata

**P0:** resolver o **menor campo faltante** da primeira fonte Galidemus: critério de ataque/acerto específico para Patada (FOR padrão ou DES? proficiência de Luta? preço de PA/tempo, geometria/alcance, snapshot íntegro e modificadores), em coordenação DMG e competência normativa Mestre; comparar CA/HP/Alma explícitas da ficha com regras gerais sem silenciosamente promover nenhum valor. **P1:** consumível R31 **real**, não testemunho de schema sintético: recuperar do produtor um envelope autêntico com recibo e checksum; verificar gate A–E; somente chamar VLAB nativo após autorização integral verdadeira. **P2:** reconciliar renovação temporal da Reação com o Mestre antes de comparar políticas defensivas canonicamente. **P3:** uma ação real nativa, replay, depois 1×1 canônico e bateria pareada; expansões 2×1, 3×1 depois.

**Governança:** IBX-90/91/92 sem ACK inventado, IBX-56 BLOCKED-EXTERNAL; writer, lease, epoch, fencing, GREEN, NAC-PASS produtivo HOLD. Zero mudanças de DMG-RANK/Bestas/Party/O Primeiro/estoques ou gameplay. Sem novas Inbox, contratos ou regras criados. Nenhum claim de identidade física de instância predecessora.
