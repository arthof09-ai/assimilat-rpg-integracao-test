# Tabletop Assimilação — TEST 06 / RUN-004 (somente laboratório)

**Data:** 22/10/2026. **Escopo:** MESTRE-SIDE / LAB Inovador / TEST. Não canônico. Não alterar Party/O Primeiro, VLAB, DMG, CRAFT, LEVEL-UP ou outros laboratórios.

## Baseline, proveniência e decisões

- **RUN-003 TEST05** gravado e relido na página `https://app.notion.com/p/401c2b324ede809585d3d1907c194df9` neste ciclo.
- TEST05 fonte local SHA256 `7d90e3e1504e2c078ee2e59612af633a2d139a6ec3e3cb82674405919c4b9c52`, 35.097 bytes; ZIP `3d18a6c5f2e7933040c8bde3d2b5e9f133a0e91bb2ca9f6f0f9fc24570f61670`, 790.207 bytes, 21 entradas, CRC PASS, 20/20 manifest PASS. Arquivos TEST05 originais **preservados**.
- RUN-001 LAB-INOV-UI-001 v0.3.0 é linha histórica distinta. RUN-002 TEST02/03/04 lido diretamente no Notion; TEST04 fonte indexada, bytes/ZIP TEST04 ainda não recuperados.
- PESQ-INOV-20261022-001/002 e despachos D-INOV-001 a 004 lidos na página do laboratório. Recomendações de Pointer Events, touch-action, segurança do replay e escopo aplicadas de forma independente. O pesquisador **não** alterou código do desenvolvedor.
- VLAB R205 e laboratório VLAB consultados somente por leitura; documentos e GitHub do projeto descrevem artefatos SQLite/TSV/JSON, mas **schema de coordenadas/topologia da série real não verificado**. Sem integração real; sem inventar posição.

## Código efetivamente construído

O novo `TABLETOP_ASSIMILACAO_INOVADOR_TEST_06.html` evolui a fonte TEST05, com `build_test06.py` registrando substituições verificadas e SHA da nova fonte. Sem bibliotecas externas nem backend.

1. **Minimapa funcional:** visão reduzida com paredes, perigo, aliados, inimigos, seleção e moldura da região visível; toque no minimapa desloca a câmera, sem movimentar tokens.
2. **Camadas visuais independentes:** alternância de coordenadas, ameaça e alcance sintéticos, sem mutação do estado lógico nem exportação de evento. Obstáculos, perigos e peças permanecem representados.
3. **Focar personagem:** centraliza a câmera na unidade selecionada, sem teleportar ou disparar ação.
4. **Pointer Events robustos:** captura quando aplicável, `pointercancel`/`lostpointercapture`, limpeza de estado após gesto, pinça ancorada em ponto mundial, arraste em modo explícito, prevenção de clique acidental. Zoom/botões anteriores preservados.
5. **Replay melhorado:** painel mostra diferenças antes→depois nas coordenadas dos tokens, sem recalcular dano/PA/alcance e sem alterar Arena.
6. **Validador sintético endurecido:** rejeita chaves de identidade reservadas `__proto__`, `prototype` e `constructor`, além das proteções já implementadas no TEST05.
7. **Correção da suíte de regressão adaptada:** espera nome de exportação TEST06 em vez de TEST05 e aguarda término assíncrono de leitura do arquivo antes de validar importação; TEST05 histórico não alterado.

## Matriz digital — execução presente

| Suíte | Assertions PASS | Classe |
| --- | ---: | --- |
| `test05_regress_22.py` adaptada TEST06 | 22/22 | Regressão da Arena |
| `test05_regress_13.py` adaptada TEST06 | 13/13 | Regressão da Arena |
| `test_test05_novos.py` adaptada TEST06 | 50/50 | Zoom/pan/redo/JSON/replay/segurança |
| `test_test05_pinca.py` adaptada TEST06 | 7/7 | Pointer Events/viewport |
| `test06_novos.py` | 54/54 | Novas funções e casos negativos em 390×844 e 360×740 |
| **Total no código TEST06** | **146/146** | Digital Chromium headless (não Android físico) |

As 54 verificações novas são **27 por viewport**, incluindo inspeção de minimapa, camadas sem alterar motor, câmera, cancelamento de ponteiro, pinch, toque pós-gesto, replay read-only, chave reservada e ausência de rede. Capturas `TABLETOP_TEST06_390x844.png` e `TABLETOP_TEST06_360x740.png` são screenshots reais do HTML testado em Chromium, não imagens geradas artisticamente.

**Correções durante desenvolvimento:** (a) teste inicial de pinça usou zoom máximo 96 e esperava zoom maior — corrigida pré-condição do teste para zoom 44; (b) fixture independente usa IDs próprios, e a mutação adversarial assumia `b` — corrigido o teste para usar ID real; (c) suíte de regressão anterior fazia assert antes do `await file.text()` completar — corrigida espera assíncrona da suíte adaptada. Sem ocultar falhas intermediárias.

## Segurança, limites e gate

- O TEST06 importa apenas snapshots sintéticos com schema `assim.lab.vlab.readonly.v1`. O contrato é **experimental do Inovador**, não exportador canônico VLAB.
- Não usa autenticação remota, não envia dados a Notion/Party, não processa arquivos VLAB reais, não resolve dano/PA/turnos por motor alternativo, nem altera fontes canônicas.
- **PASS TEST local** para funcionalidades verificadas; **HOLD** para Android físico, `file://` no telefone do Mestre, sincronização Mestre↔Party, VLAB espacial real e NAC-PASS-02 produção.
- Upload ZIP/HTML ao Notion bloqueado na etapa TEST05 por DNS `curl: (6) Could not resolve host: api.notion.com`; somente registro textual Notion comprovado, nenhuma alegação de anexo binário.

## Reproduzir

É necessária uma instalação existente de Python, Playwright e Chromium headless (neste ambiente `/usr/bin/chromium`). Execute as cinco suítes na pasta do pacote, ou abra o HTML em navegador compatível. Não há dependências JS externas. Verifique manifesto SHA256 e CRC do ZIP antes de confiar na integridade. Testes em viewport emulada não comprovam toque no Android físico.

## Ponto de retomada exato

1. Confirmar RUN-004 via readback no Notion; HASH do pacote final e arquivos incluídos.
2. Se precisar de cópia binária persistente no Notion, transferir os ZIPs no ambiente com DNS/rota de upload funcional, conferir hash após download; nenhum anexo presumido.
3. Solicitar ao Mestre teste curto Android de: entrar no 20×20, pinça, alternar arraste, minimapa, foco, desfazer e replay/exportar. Registrar resultado real.
4. Obter amostra de payload real VLAB (R205/R237/R238 autorizado) e documentação de campos; mapear apenas tipos e identidades realmente presentes. Sem coordenada comprovada, mostrar linha do tempo textual em vez de mover tokens.
5. Continuar TEST07: otimização de render para 20×20 (reuso de DOM/canvas), acessibilidade e animação puramente visual de replay, caso testes indiquem ganho; nenhuma engine extra por modismo.
