# PARECER DE AUDITORIA DA ENTREGA CODEX — Tabletop Assimilação

**Data de auditoria:** 24/10/2026. **Escopo:** Coordenação do Inovador, MESTRE-SIDE; TEST exclusivamente. **Operação:** Tabletop Assimilação EXISTENTE. **Fonte de entrega:** pasta Drive `RPG ASSIMILAÇÃO`, ID `1RPl9yOjGrhO73vfRU0jmmGHZkvkKHG1B`; ZIP ID `1sA1QvBqorW5iBLmdWmo5u_QpSxsBf-O6`, arquivo `.sha256` ID `1IPnHerDiSA80vXjISHHKI5H9ObcryBKg`. **Não contém autorização para publicar ou colocar em produção.**

## Evidências independentes verificadas

- ZIP original baixado por conector Google Drive com acesso à pasta enviada pelo Mestre. `ponte-vlab-tabletop-test.zip`, **367.597 bytes**.
- SHA-256 calculado: `80aa408adabcd3c8e9fb2267d7efeb5ee4b9a3ef5e22c618a9d814bb98b751a3`, idêntico ao `.sha256` e ao hash mencionado pelo Codex.
- ZIP: **44 entradas**, sem caminhos de extração relativos que escapem o diretório, nomes sem colisão, **CRC PASS** para todas as entradas.
- Manifesto interno: **42/42 payloads** com tamanho e SHA-256 conferidos. SHA256SUMS.txt: **43/43 hashes** conferidos (inclui manifesto). Não há auto-hash circular.
- Extração realizada em diretório de auditoria isolado, SEM modificar o original. Código, patches, relatórios e recibos lidos.
- Suite entregue executada INDEPENDENTEMENTE: **34/34 testes Python PASS**, dos quais um orquestra **15/15 testes Node PASS**; não somar como testes Python adicionais. `tsc -p tsconfig.json`: **PASS**. `run_checks.py`: **LOCAL-TEST-PASS**, inclusive demonstração HTTP local de 3 clientes/test fixtures PASS. Sem WSS real, três Android físicos ou VLAB.
- Ambiente de execução: Python3 do container e Node `v22.16.0`, que não atende à exigência declarada `>=24.12.0` do projeto. Sem opção Node especial a suite falha 1/34 por `ERR_UNKNOWN_FILE_EXTENSION .ts`; com `NODE_OPTIONS=--experimental-strip-types` passou 34/34 e 15/15. **Nenhum byte do código original foi alterado**; registrar como incompatibilidade de ambiente, não passar silêncio por falha de aplicação.
- Auditoria estática: `authority.py` restringe projeção a chaves allowlist, exige escalares, resiste a objetos aninhados inesperados nos casos sintéticos, reverte transação quando projeção da resposta falha. Sua auth usa tokens públicos `FAKE_TEST_*`, portanto **NÃO autenticação/ACL reais**. Scanner/inspeção pontual não é certificação universal de ausência de segredos, nem libera repositório público.

## Confronto com fontes institucionais

- Pacote PESQ-INOV-20261023-015 da Biblioteca Mestre lido; matriz de 25 requisitos e contrato `BOUNDARY_ARENA_SALA_VLAB_015.json` marcado PROPOSTO_TEST_MESTRE_ONLY. TEST36 original (pacote técnico RUN013) inspecionado: `room-client.js` e `room-v2-adapter.js` contêm `RECEIPT_QUERY`, `JOIN` e `MOVE_VISUAL_TEST`, mas não `ATTACK_REQUEST`, `DEFENSE_REQUEST` ou `TURN_START_REQUEST`. TEST36 não é sala real.
- Codex: seis operações `create/view/submit/history/checkpoint/restore` sob schema v1 HTTP local, efeito `FAKE_SET_LABEL` sem dano nem PA; idempotência evita segundo COMMIT, mas **não dispõe de RECEIPT_QUERY**, armazenamento do recibo consultável por ID, outbox de intenção pendente no servidor, WSS/join real, credenciais permanentes ou integração VLAB. Igualar `create` a `JOIN` é erro; `client_action_id`/`commandId`/`intentId` e `expected_revision`/`baseRevision` são relações semânticas candidatas, requerem negociação da ABI.
- **Risco de identidade de commit:** a mensagem do Codex afirma o commit de entrega `7fd03324209ee44d2314ac86609b17293542bef1`. O pacote `receipt.json` e `RELATORIO.md` identificam o **source_commit** `bad50082621f5ddebb157088949dccac8e6aa8ca`; nenhuma referência a `7fd0332` existe nos bytes inspecionados. Hipótese: commit posterior de embalagem; **não comprovado** sem Git remoto ou recibo complementar. Os bytes ZIP estão auditados por hash independente, mesmo sem equivalência Git demonstrada.
- Runtime Cloudflare DO, 3 Android, segurança Mestre/Party em servidor, VLAB ABI e Python↔TS com motor real seguem **HOLD**. Uma suíte 34/34 local não é homologação produtiva.

## Decisão de coordenação

**GO:** preservar a POC sintética como evidência consultiva (estabilidade de revisão, atomicidade SQLite local, deduplicação, rollback, projeções por papel) e usar a matriz de divergências na direção do backend único. Desbloqueio de entrega ZIP por Drive: **PASS**.

**NO-GO:** publicação em GitHub público, integração mecânica nativa, simular ataque/defesa oficial, afirmar cliente TEST36 compatível com seis envelopes, declarar segurança de Party em produção ou fazer deploy. Dependem de autorização expressa do Mestre, owner de contrato e testes efetivos. A cópia Drive foi listada pelo conector como **não compartilhada publicamente**.

**Desenvolvedor:** seguir M0 da direção já aprovada: Arena mobile-first com unidade→ação→alvo/área, estados e prévias, sem alterar Vida/PA. Preservar `room-client.js`, `room-v2-adapter.js` e journal corrigido TEST36; codex POC não deve forçar troca de protocolo cliente.

**Pesquisador:** agora NÃO precisa tratar o arquivo Codex como ausente; transformar matriz requisito 24 de `PENDENTE DE CODEX` para **BYTES_RECEBIDOS_E_AUDITADOS / ABI_AINDA_INCOMPATÍVEL**, revisar matriz diferencial e os casos de recibo após perda de ACK e projeção pré-SEND, sem replicar código ou insistir em npm indisponível.

**Codex:** a entrega foi resolvida via Drive; NÃO refazer/exportar outra vez. Próxima missão legítima é explicar vínculo `bad5008 ↔ 7fd0332` e propor camada de compatibilidade TEST conservadora (especialmente `RECEIPT_QUERY` e recuperação estável de id) sem criar backend alternativo ou reescrever o VLAB. O próprio Codex deve tratar o ZIP do Drive como baseline confirmado por SHA.

**VLAB:** só executor competente poderá autorizar ABI real e decidir uma ação de combate. Nenhuma alteração à Party/O Primeiro.

## PSV e ponto exato de retomada

**ANTES:** Codex ZIP local sem link de exportação acessível; `CODEX_BYTES_HOLD`.

**DEPOIS:** acesso Drive confirmado; SHA/CRC/42+43 entradas de manifesto confirmados; fonte/PESQ015/TEST36 confrontados; 34 Python + 15 Node aninhados + TypeScript + demonstração local reexecutados. `CODEX_DELIVERY_PASS`, `CODEX_POC_LOCAL_TEST_PASS`, `CODEX_ABI_NOT_INTEGRATED/HOLD`.

**LAST-VERIFIED:** arquivo exato de 367.597 bytes SHA acima, pacote PESQ015 lido, TEST36 adaptador v2 lido, testes locais reproduzidos. **FIRST-PENDING:** vínculo Git do commit final, seleção de autoridade única de sala e contrato conciliado com VLAB e TEST36, autenticação real; paralelamente desenvolver M0. **NEXT:** preparar despachos individualizados com LONG-RUN-01 §15.2 integral uma vez cada, após este checkpoint, sem repetição de PESQ015/RUN013/POC. **NO-REPEAT:** relatórios de vídeo já preservados, reexportação do mesmo ZIP, código paralelo, publish/merge/deploy, garantias de Android não demonstradas.
