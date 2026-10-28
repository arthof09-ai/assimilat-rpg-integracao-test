# COMESTRE INOVADOR — EXECUÇÃO TEST 05

**Data:** 22/10/2026 — MESTRE-SIDE / Laboratório do Inovador / TEST. **Cânone, Party, O Primeiro e motores existentes: NO-WRITE.**

## Evidências e estado anterior

- TEST 02: fonte HTML local `ARENA_INOVADOR_TEST_02.html`, SHA256 `b22c99dafca8c26414abf9d7f228ebc8ca8f5e5e7309f28ee8e7bb120f73daaa`, corresponde byte a byte ao ZIP original recuperado, CRC ZIP PASS.
- TEST 03: fonte `ADAPTADOR_VLAB_READONLY_TEST_03.html`, SHA256 `3b8744d8ac0b8f60e5170312832aeeb36e701255c584fdae1e7f7b045f68a628`, corresponde byte a byte ao ZIP original, CRC PASS.
- TEST 04: arquivo `ARENA_PONTE_REPLAY_INOVADOR_TEST_04.html` **localizado na Biblioteca do projeto**; conteúdo textual lido com Files (26.805 bytes informados). O materializador negou cópia de bytes brutos (`does not have an authorized raw-byte materialization path`). Logo, **NÃO foi recuperada versão binária, ZIP nem SHA-256 TEST 04; 41/41 é apenas resultado histórico reportado, NÃO reexecutado**. Conteúdo legível confirma ponte de snapshots TEST 02→schema TEST 03, sem consumo VLAB real. Arquivo histórico preservado na Biblioteca; não modificado.
- Notion: `https://app.notion.com/p/401c2b324ede809585d3d1907c194df9`. Foram tentados `get_tool_access`, `fetch` exato e `search`. Todos retornaram `link_id must identify an eligible linked account`. Logo **RUN-002, regras locais, Diário e readback NÃO foram auditados; escrita Notion NÃO executada**.
- VLAB: referência Mestre-only R205 a partir de relatório DMG C16 indica 20 combates, 2.812 eventos, dados SQLite/TSV/JSON, mas **não confirma esquema de coordenadas, frames espaciais ou exportador para VTT**. Fontes primárias do VLAB e esquema real continuam sem auditoria direta. Não declarar integração canônica.

## Alterações reais do TEST 05

1. Reconstrução evolutiva **sobre o TEST 02 binariamente verificado**, usando informações legíveis do TEST 04 para preservar a ponte sintética; **não é patch byte a byte do TEST 04**.
2. Zoom do mapa 28–96px/casa com botões ±, slider e ajuste da janela.
3. Modo arrastar mapa independente do clique em token; botão centralizar; rolagem no tabuleiro 20×20.
4. Gesto de pinça via pointer events, com controles para telas pequenas; melhorias de `touch-action`.
5. `Desfazer` e `Refazer` com pilha de estados por sessão; nova ação invalida redo; reset/importação limpam ambos.
6. Replay visual em painel distinto da arena: capturar linha de snapshots, avançar, retroceder, primeiro/último, slider, selecionar quadro, limpar sem editar arena.
7. Exportar/importar JSON sintético no schema `assim.lab.vlab.readonly.v1`, compatível com o Observatório TEST 03. Texto importado é aplicado por `textContent`.
8. Validação por documento: até 25 unidades, 100 eventos, arquivo até 250 KB; rejeita paredes e IDs duplicados, posições fora da grade, unidade em parede, coordenadas sobrepostas, eventos inválidos e textos maliciosos. **Rejeita `VLAB_TEST_EXPORT` enquanto a origem real não estiver homologada.**
9. Harden da importação TEST 02 rejeitando paredes/terrenos duplicados.
10. Correção de defeito descoberto em teste: ao desligar `Arrastar mapa`, o toque posterior era indevidamente descartado. O estado `dragged` agora é limpo ao sair desse modo.

## Testes executados nesta operação (Chromium headless; NÃO Android físico)

| Suíte | Cenários | Resultado |
|---|---:|---|
| `test05_regress_22.py` (derivada da TEST 02 histórica; reexecutada) | 22 | 22 PASS |
| `test05_regress_13.py` (derivada da TEST 02 histórica; reexecutada) | 13 | 13 PASS |
| `test_test05_novos.py` (zoom, arraste, undo/redo, replay, JSON, segurança) | 50 | 50 PASS |
| `test_test05_pinca.py` (pinça, tela 360, pan) | 7 | 7 PASS |
| **Total verificações locais desta execução** | **92** | **92 PASS** |

- Viewports 390×844 e 360×740; interação em Chromium automatizado, e 2 capturas geradas do HTML efetivo.
- **Não adicionar 41 históricos do TEST 04 nem 35 históricos do TEST 03 ao denominador 92.**
- O navegador usou `page.set_content`, que não prova funcionamento de `file://` no Android físico.
- Não houve execução de simulação VLAB real, dano, PA, iniciativa, fichas ou multiplayer.

## Gate proporcional

**PASS digital local restrito TEST05** para os cenários cobertos por suítes automatizadas e integridade reproduzível.

**HOLD:** Notion autenticação, readback RUN-002, normas operacionais vigentes, integração VLAB real, autenticação de proveniência de JSON Mestre-only (etiqueta NÃO comprova identidade), Android físico, segurança multiplayer, publicação canônica. NAC-PASS-02 global NÃO declarado.

## Próximo ponto exato

1. No chat com conexão funcional do Notion, abrir laboratório existente, BOOTSTRAP, NAC-CONT-03, NAC-NORM-01, NAC-PASS-02, LONG-RUN-01, Diário; conferir RUN-002 e nenhum registro duplicado; publicar este relatório e anexos no destino competente, com **readback**.
2. Testar `TABLETOP_ASSIMILACAO_INOVADOR_TEST_05.html` no Android do Mestre (5×5, 20×20, pinça, arraste, movimento, undo/redo, replay, importação/exportação local). Registrar navegador/aparelho/resultado. Não presumir homologação física.
3. Auditar evento real do VLAB usando arquivo primário autorizado e cadeia de hashes/schema; determinar se contém coordenadas, unit IDs, rodada/turno. Só então elaborar adaptador **read-only** específico; sem inferir posicionamento a partir de eventos numéricos.
4. Avançar TEST06 no mesmo laboratório: desenho de mapas por camadas e controles visuais progressivos, sem motor de regras novo; preservar TEST05 original e executar suíte regressiva.

## Reproduzir

Em Python + Playwright + Chromium instalado, dentro do diretório extraído execute:

```bash
python test05_regress_22.py
python test05_regress_13.py
python test_test05_novos.py
python test_test05_pinca.py
```

Abra o HTML diretamente num navegador compatível para testar a interface; nenhuma dependência JS externa nem cadastro necessário. Código permanece integralmente local/offline.

## Replay de custódia em diretório limpo

O primeiro pacote TEST05 foi extraído em diretório temporário independente. As quatro suítes fornecidas no próprio ZIP foram reexecutadas nesse diretório, retornando **22/22, 13/13, 50/50, 7/7 PASS**, sem depender dos caminhos do diretório de desenvolvimento. Esta validação demonstrou portabilidade digital da distribuição; não demonstra execução Android física nem autenticação da origem de dados externos.
