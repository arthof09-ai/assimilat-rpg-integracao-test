# AUDITORIA COORD-INOVADOR — R4: RUN-017/TEST40 × PESQ-020 × Codex 0.4.0

**Data:** 24/10/2026 | **Perímetro:** Mestre-only / Tabletop Assimilação existente | **Tipo:** auditoria independente da Coordenação (sem writes nos executores).

## Resultado executivo

A versão TEST40 **é avanço concreto** na fronteira cliente: inclui capacidade `connected_test/native_port.js` com `fetch('/bridge')` para same-origin local e persistência da intenção externa no journal já existente `assim-tabletop-room-pending-test`. Reexecução independente confirmou a Authority original Python/SQLite servindo assets TEST40, requisição Node `fetch` com perda pós-COMMIT e recuperação da mesma commandId após reinício, e os comportamentos de UX/journal/offline em Chromium com fetch simulado.

**Não há PASS de navegador Chromium originando o POST real**: `tests/test40_native_probe.py` foi executado e `page.goto(http://127.0.0.1:<port>/)` falhou com `net::ERR_BLOCKED_BY_ADMINISTRATOR`. Não se tentou contornar a política administrativa.

**Achado prioritário novo na fronteira TEST40:** PESQ-020 tinha reproduzido dois RED no TEST39. Nesta auditoria, os **mesmos dois canários executáveis, alimentados com as fontes originais de TEST40**, também reproduziram os RED. Portanto há duas pendências objetivas de vínculo de contexto (cena de origem / porta-sala original) ainda não tratadas no frontend TEST40. Não há prova de vazamento real nem de manipulação da Party. A Authority Codex 0.4.0 demonstrou separar corretamente recibos de salas.

## Fontes físicas e custódia de origem

- Desenvolvedor `PACOTE_TECNICO_TABLETOP_TEST39_A_TEST40_20261024.zip`: 8.992.561 bytes, SHA256 `88cda222272436f1d30acae87852c6a27416118b514c56e4c0c3f10ff251fd8e`, Biblioteca Mestre `libfile_799c7407e3ac8191a6de8c99c4eff2df`, ZIP CRC PASS (77 entradas). Original TEST39 preservado dentro do ZIP.
- Pesquisador `PACOTE_PESQ_INOV_20261024_020.zip`: 307.836 bytes, SHA256 `c8ba30a17138e417fca1008224bb4a951ed3f7df948166edcc9168d531b16209`, Biblioteca Mestre `libfile_afce81fc52c88191b27a0751f2ca680f`, ZIP CRC PASS (15 entradas).
- Codex0.4 base privada `ponte-vlab-tabletop-0.4.0-test38.zip`: 1.163.331 bytes, SHA256 `5d3155e25ab9b1a6fa07e85ef43e92cf42de16c12e0cae25e70d868556f31a4a`, Drive Mestre `https://drive.google.com/file/d/1FviMApTDDcvtO1yt9dfGiFh_6IUhAUHw/view`; biblioteca espelho `libfile_caead0091de08191be740e2a64958e27`. Codex executor indisponível por relato Mestre; fontes Código original apenas read-only na auditoria.
- Offline `TABLETOP_ASSIMILACAO_TEST40_OFFLINE.html` 150.749 bytes, SHA256 `330ee0c2c104f2002f35df421a633f703d47e430de225cdb02ba4ac362fab814`.

O presente relatório usa a custódia já existente, sem reproduzir/copiar páginas ou operações canônicas, nem modificar as fontes do Codex, Desenvolvedor ou Pesquisador.

## Reexecuções independentes nesta rodada

1. `python tests/test40_http_assets.py` — **14/14 PASS**: Authority Codex 0.4.0 original (em diretório temporário com assets TEST40 de autoria DEV) respondeu por HTTP e serviu os bytes de JS/CSS reais, CSP same-origin, sem modificação de `authority.py` ou prefixo original do transporte.
2. `python tests/test40_native_node.py` — **PASS**: `node` executa `fetch` real à Authority HTTP/SQLite; ACK pós-COMMIT descartado; processo reiniciado no mesmo banco; consulta recuperou mesma commandId e recibo. Contagem no SQLite: **1 receipt, 0 events, revision 0**. **Node não é Chrome/Android**.
3. `python tests/test40_browser_journal.py` — **30/30 PASS**: Chromium DOM com mock de `fetch`, em 390×844 e 360×740; preservação de ID/journal, UI `UNKNOWN`, recuperação de recibo, journal corrompido fail-closed. A origem foi simulada no harness; não usar como prova de POST nativo de navegador.
4. `python tests/test40_offline.py` — **39/39 PASS**, após disponibilizar a cópia byte-idêntica do HTML offline verificado na pasta `dist/` exigida pelo script, sem modificar conteúdo do artefato.
5. PESQ-020 baseline TEST39: `python prepare_sources.py TEST39-original.zip CODEX0.4.zip`, `bash run_all.sh` — **5/5 cross-scene + 5/5 cross-room + manifesto 14/14 PASS**. Provas RED/Green científicas; patches GREEN existem apenas em memória do Pesquisador, não instalados na fonte.
6. **NOVO confronto físico PESQ-020 × TEST40**: mesmas duas suítes, com variáveis `PESQ020_DEV=.../dev40/public` e `PESQ020_CODEX=.../codex04/experiments/tabletop_vlab_bridge`. **5/5 cross-scene RED→candidate GREEN e 5/5 cross-room RED→candidate GREEN**, agora contra a fonte TEST40. `app.js` ainda cria `authorityAttempt={id,status,code,querying}`, sem `sceneId/actorId/targetId`; consulta usa global `window.TabletopTestAuthorityPort` e valida apenas `commandId/status/code`, em vez de vincular o recibo ao contexto original da intenção. Estes RED são de laboratório com portas sintéticas/cena TEST, NÃO exploração em produção. Atenção: os scripts preservam nomenclatura `TEST39` nos textos porque foram criados na PESQ-020; a prova de aplicação em TEST40 é a variável de ambiente explícita e a fonte extratada, não a descrição interna do script.
7. `python tests/test40_native_probe.py` — **HOLD**, navegador Chromium bloqueado em `http://127.0.0.1:40479/` com `net::ERR_BLOCKED_BY_ADMINISTRATOR`. Script exit0 relata bloqueio, NÃO PASS de navegador.

O Desenvolvedor relatou `716/716` verificações dirigidas, com **83/83 novos** e **633/633 regressões**. Foram reexecutados independentemente **14+30+39=83** desses novos ensaios e a prova HTTP Node; **as 633 regressões não foram reexecutadas integralmente pela Coordenação**. Nenhum número de testes é apresentado como quantidade de funcionalidades entregues.

## Defeito prioritário de contexto / ancoragem

**CENA:** a tentativa em c1 pode ter seu recibo exibido no HUD de c2 após mudança de cena sem marcar `c1`. Correção deve fixar/mostrar contexto de origem, inclusive após cold reload, sem substituir a cena de origem por cena atual. A versão TEST40 guarda `sceneId` no payload do journal externo, mas não copia essa origem para `authorityAttempt` nem a valida na apresentação.

**SALA/PORTA:** uma intenção em rooma e uma consulta na sala roomb com a mesma `commandId` podem apresentar `ACCEPTED` alheio em lugar de `REJECTED` da sala correta no harness com troca de port. A Authority original corretamente isola por `(room_id, principal, command_id)`. O addon native TEST40 fixa constante `ROOM='arena-test'`, reduzindo o risco na sua demonstração padrão, mas o componente de UI genérico usa a porta global mutável, permanece sem vínculo suficiente de contexto (não marcar este teste como exploit nativo do addon). A solução precisa de vínculo robusto e validado entre `roomId/principal/commandId/sceneId/actorId/targetId/action` tanto em RAM quanto na reconstrução fria do journal. `port` pinado apenas em RAM é mitigação de laboratório, não solução para reload/autenticação.

**Segurança:** armazenar identificadores de referência e vínculo NÃO autoriza persistir bearer token real em localStorage. Exigir restrição de contexto, recusa fail-closed de troca de origem, CSP restrita, filtragem por destinatário server-side e regressões do Codex existente; não criar segundo motor, servidor ou outbox.

## Próxima coordenação recomendada

- **DEV**: correção RED→GREEN de ambos canários sobre TEST40 original, incluir contexto original no HUD e no fluxo de recuperação, recusar receipt fora de room/principal, manter a mesma ID e o journal único. Sem alterar o backend Codex original. Reexecutar 14 HTTP, 30 UI mock, 39 offline, 10 canários revalidados e regressões que mudaram. Entregar launcher TEST40 funcional sem Playwright como transporte, para ensaio numa bancada autorizada.
- **PESQ**: testar a fonte TEST40/TEST41 (não voltar ao TEST39) com os 2 canários e negativos de troca de cena/room, cold reopen, receipt errado/duplicado, autorização dos bytes. Não clonar backend nem fornecer patches prontos nas fontes DEV.
- **CODEX**: QUOTA-HOLD conforme relato do Mestre, não promover writer. Reusar binário 0.4.0 original congelado para TEST. Caso seja indispensável mudança Python do backend, preservar HOLD para sucessão estritamente autorizada.
- **Integração final**: numa bancada que permita Chrome→origem local autorizada, comprovar `ATACAR` por clique de tela → HTTP navegador → Authority Codex 0.4.0 → SQLite → `REJECTED/MECHANICS_UNAVAILABLE` → HUD e cold recovery com commandId única. **Só então** solicitar ABI REAL do VLAB competente e sua decisão mecânica oficial. Celular/notebook/ambos aceitos. Nada de implantação pública ou Party real sem gates.

## NAC-PASS-02 e continuidade

**PASS:** integridade original das fontes, 14 asset HTTP, Node→Authority SQLite (1 receipt), 30 UI mocked, 39 offline, 10 PESQ-020 baseline e 10 revalidadas contra TEST40. **RED reproduzidos:** associação cena e sala/porta no frontend TEST40 em harness científico. **HOLD:** POST Chromium→Authority nativo, autenticação/Party real, VLAB mecânico, multiplayer entre dispositivos, deploy. O resultado `ERR_BLOCKED_BY_ADMINISTRATOR` é barreira instrumental, não defeito de aplicação comprovado.

**LAST-VERIFIED:** RUN-017/TEST40 physically retrieved e testado nos limites descritos; PESQ-020 canários transferidos para teste sobre TEST40; Codex0.4 read-only. **FIRST-PENDING:** corrigir vínculo de recibo à cena/sala/identidade e homologar fluxo HTTP nativo Chromium em ambiente permitido. **NEXT:** DEV corrige duas falhas e prova nativo, PESQ audita, depois gate ABI VLAB. **NO-REPEAT:** versões anteriores, recibos backend/SQLite, outbox, engine paralela, regressões sem hipótese, projetos novos.
