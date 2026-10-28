# PSV — PROMPT DE HANDOFF / CRAFT QMC-02 RECEBER O PA R05 EM TEST

**MESTRE-SIDE / CONFIDENCIAL.** Para encaminhar ao CM-000002 — Executor CRAFT, atribuição por confirmar no Notion, sem herdar escritor/lease/epoch/instance. Operação `OP-ARQ-RIN-REC-01`. QMC-02 original SHA-256 `2763d96ba3624741a89d0d2159000826584ed932e11fbf6ef8e637ab3858d92a`. PA R04 baseline SHA-256 `2c64788b33b6e486f3edc45334b462f88fce8fb2db02fc742aa6b0b2e954cc46`.

**ORDEM DIRIGIDA:** Receba o pacote PA_R05 da Biblioteca/arquivo do Mestre e faça pré-verificação de integridade. **Não crie receitas, recursos, fichas, produto, REC-ID, nova QMC ou operação.** Primeiro reabra `qmc02.py`, `source_readbacks.json`, `bancada.py`, `test_qmc02.py`, o contrato `QMC-PA-INTERCHANGE-CANDIDATE-1` e o `R05_CODE/qmc_pa_r05_wire.py` em laboratório isolado. Preserve o código original e documente o delta mínimo proposto. Somente após autoridade competente pode adaptar o **entrypoint QMC-02** para que `QMC qualifica → PA informa historico ou estimativa/indeterminação → QMC valida resposta` efetivamente ocorra na execução Nativa TEST, não só em sidecar.

## O defeito concreto a corrigir

Na QMC-02 original, `validate_external_pa` NÃO tem ramo de aceite externo: mock → SIMULAÇÃO, outros → `INTERFACE_EXTERNA_NAO_CONTRATADA`. A R05 provou rejeição original em teste. Qualificação original da **Bota Caminho Veloz** (`3edc2b324ede8135b199fd0cdbb5463c`) foi executada via QMC CLI, e o motor PA reconciliou o custo histórico: 18 PA/dia + 5 PA/uso. O R05 já possui modelo de envelope com `QMC-PA-RESPONSE-R05-TEST-1`; não inventar validador paralelo produtor. **O delta nativo deverá pertencer ao Executor CRAFT depois de gate, sem substituição da QMC02.**

## Aceite mínimo falsificável

1. Qualifique Bota via CLI QMC original; anexe readback/identidade/versão do extrato; PA reconcilia 18 diário e 5/uso; validador NATIVO atualizado em cópia autorizada retorna aceite **HISTÓRICO TEST**, nunca REC-ID/produção.
2. Candidato experimental espada **+5 DES permanente e +20 dano por acerto**: 25 PA/dia são apenas parcela de DES pela determinação expressa do Mestre de 17/10; custo total e dano permanecem `null`; validador aceita o **parecer de indeterminação** em TEST, não inventa energia.
3. Rejeitar hash adulterado, hash recomposto com custo PA falso (comparação com baseline QMC e PA), UUID/URL divergentes, famílias/versões divergentes, unidade trocada, fonte Espelho promovida silenciosamente, payload sem componentes, mock, custo `null` trocado por zero e `new_recipe_permitted=true`.
4. Erros e conflitantes são expostos ao Mestre sem criar receita. Se houver concorrência/lease/unknown effect, manter HOLD sem tocar fonte canônica.
5. Verifique composição de `PA Total - PA comprometido = PA Livre`, separação PA/dia e PA/uso, ausência de regra de exaustão por item não documentada.
6. Reexecute somente regressão de impacto + suites QMC relevantes. Produza SHA do componente modificado em cópia isolada, linha exata de mudança, recibo nativo, rejeições negativas, PSV, gates NAC-NORM/NAC-PASS. Envie ACK pela Inbox única na identidade correta.

**SE A ESCRITA NO CÓDIGO NATIVO NÃO FOR AUTORIZADA:** preparar PR/diff isolado, não aplicar no original e marcar `NATIVE=HOLD`. Não reportar sidecar como integração nativa. **PRODUÇÃO HOLD, RECEITAS 0.**
