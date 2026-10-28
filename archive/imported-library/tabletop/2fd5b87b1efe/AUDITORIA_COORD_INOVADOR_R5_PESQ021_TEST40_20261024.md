# AUDITORIA INDEPENDENTE R5 — PESQ-021 × TEST40 × CODEX0.4

**Projeto:** RPG Assimilação — Tabletop Assimilação. **Classificação:** MESTRE-SIDE / PRIVADO. **Data da pesquisa:** 24/10/2026. **Operações:** as mesmas, sem novo executor/writer/backend. **Status:** auditoria e orientação concluídas; código Dev/Codex intocado.

## Baseline material

- PESQ-021: `PACOTE_PESQ_INOV_20261024_021.zip`, 120.980 bytes, SHA-256 `fd0bd1b6298dfecb34900a5ada7b62862b922d760914d138b0b4e89e87fab0ee`, Library `libfile_a0f8c51d874481919c00e89de23bc993`.
- DEV RUN017 / TEST40: `PACOTE_TECNICO_TABLETOP_TEST39_A_TEST40_20261024.zip`, 8.992.561 bytes, SHA-256 `88cda222272436f1d30acae87852c6a27416118b514c56e4c0c3f10ff251fd8e`, Library `libfile_799c7407e3ac8191a6de8c99c4eff2df`.
- CODEX 0.4.0 original, backend READ-ONLY, SHA-256 `5d3155e25ab9b1a6fa07e85ef43e92cf42de16c12e0cae25e70d868556f31a4a`, Drive Mestre privado / Library Mestre privada `libfile_caead0091de08191be740e2a64958e27`. Executor Codex indisponível por relato Mestre, sem prazo ou escritor transferido.
- PESQ-020 baseline original SHA-256 `c8ba30a17138e417fca1008224bb4a951ed3f7df948166edcc9168d531b16209`. As duas falhas da PESQ-020 já eram conhecidas e não foram recanonizadas aqui como novas.

## Execução independente da coordenação

1. Verificados SHA-256, ZIP CRC e integridade: PESQ-021 18 entries e manifesto 17/17; DEV TEST40 77 entries; CODEX0.4 65; PESQ020 15.
2. Executado `bash run_all.sh ../inputs` com fontes ZIP autoritativas em diretórios separados e sem editar originais, completando:
   - TEST40 `RoomClient`/HUD em Chromium DOM com `fetch` simulado: **9/9 canários PASS** (original RED de contexto perdido após cold-reopen, candidato GREEN apenas em memória).
   - TEST40 `native_port.js` original + Authority Codex0.4 real HTTP/SQLite + Node.js: **14/14 PASS** (original RED perfil exibido p2 usando token TEST p1 ao consultar/finalizar, candidato GREEN em memória).
   - API Codex0.4 rejeita consulta com token fake Player2 `NOT_FOUND` para recibo Player1; **exatamente 1 receipt, 0 eventos mecânicos** no SQLite temporário.
   - Manifesto independente 17/17 PASS.
3. Os **23/23 PASS são PASS dos canários científicos**, incluindo detecção RED de defeito original; NÃO são 23 funções implementadas nem comprovante de GREEN instalado. Testes Chromium DOM utilizam rede simulada; Node HTTP não equivale a POST browser nativo.

## Achados e prioridade

**P0 — identidade de consulta/finalização:** `connected_test/native_port.js` verifica perfil Player1 em envio/reserva, mas não replica guarda em `query`/`finish` e utiliza `FAKE_TEST_PLAYER1` fixo. Em ensaio sintético, UI p2 pode consultar/limpar intenção p1 sem que a Authority tenha falhado: o servidor vê autenticação FAKE p1, não p2. Exigir vincular perfil original, sessão/sala/principal, comando e origem antes de `reserve`, `send`, `query`, `finish` e `restore`; não persistir credencial real e não tratar FAKE como autorização de produção. O `restore` ainda exige cobertura adicional.

**P1 — contexto após aba fria:** o jornal existente guarda `sceneId`, `actorId`, `targetId`, `action`, `commandId`; `public/app.js` reconstrói a apresentação apenas com ID/status/code/querying e a UI exibe receipt de c1 sobre c2 sem origem. Deve carregar o contexto do MESMO jornal no estado de UI e apresentar origem corrente/diferente claramente, inclusive `tacticReadout`. Incluir caso duplicidade roomId/commandId da PESQ020, ainda RED no TEST40 pela auditoria R4, sem nova outbox nem novo motor.

**P2 — teste navegador nativo:** `ERR_BLOCKED_BY_ADMINISTRATOR` no Chromium→127.0.0.1 sob a bancada de origem PESQ021 e auditorias anteriores: gate HOLD; sem prova browser POST→Authority, sem bypass. Podem prosseguir Node HTTP e frontend, mas não promover ao mesmo gate.

**P3 — mecânica VLAB:** o checkpoint `CONSULTA-INOV-VLAB-INTEROP-20261023-001`/IBX-176 está relatado como solicitação NOVA sem ACK nem ABI homologada; combate oficial HOLD. Não construir motor paralelo, não gastar PA/Vida por `MECHANICS_UNAVAILABLE`.

## Gates NAC-PASS-02

- Fonte/CRC/manifesto/custódia inicial: PASS. Testes originais 23/23 PASS científicos RED→candidate GREEN.
- Proteção de contexto cena e perfil na fonte DEV original: **RED**, patch candidato não instalado.
- Segregação de recibo na Authority original com FAKE tokens: PASS restrito à fixture, não auth real.
- HTTP nativo do Chrome/Android real: HOLD. VLAB ABI, combate e multiplayer produção: HOLD.
- LAST-VERIFIED: PESQ021 scripts originais 9/9+14/14 e fonte DEV TEST40 confrontada, SQLite 1 receipt/0 events.
- FIRST-PENDING: DEV instalar e provar guards de perfil + recuperação de contexto e G4 browser nativo.
- NEXT: DEV produzir TEST41 ou candidato novo sem assumir backend; Pesquisador auditar GREEN instalado e retorno de ABI competente.
- NO-REPEAT: PESQ012–021, R4, CODEX0.4 receipts, RUN017/TEST40 baseline, motores/outras outboxes, regressões massivas sem hipótese, publicações.

**Nota sobre segurança:** não foi demonstrado vazamento de dados reais da Party, comprometimento de login produtivo, nem falha real de autorização do backend; o achado é de identidade de UI inconsistente com credencial FAKE em uma DEMO. Sem escrita em Party/O Primeiro/GitHub, CODEX ou VLAB.
