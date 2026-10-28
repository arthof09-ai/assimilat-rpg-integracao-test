# PSV — VLAB | Continuidade R267–R271 | MESTRE-ONLY

**Fonte persistente:** OP-VLAB-FUSION-SANDBOX-01; Biblioteca `/Comestre/OP-VLAB-FUSION-SANDBOX-01/`. **Antes:** R266 verificado com patches do R18, 8 testes históricos e 54 novos, 0/17 terminais, 0/1875 oficiais. **Depois:** R271 TEST delimitado, sem alteração do canônico.

## Novas ações materialmente verificadas

- **R267:** detectada incompatibilidade real entre R265 `GENESIS_SCENE_SEED_INVALID` e R237 científico. Fonte-gate explícito reintroduziu compatibilidade sem liberar cenas desconhecidas. Registros R237 8 bancos, 155 commits, 640 eventos foram reexecutados em cópia e comparados byte a byte ao corpus congelado.
- **R268:** detectada aceitação do primeiro evento rehashado com `before_sha` falso. Fixado first-event anchor contra a gênese determinística. 8 regressões R18 + 54 herdadas R266 + 15 novos testes R267–268 PASS.
- **R269:** auditor independente R237 passou a verificar resumo de execução contra eventos nativos e rejeitar SQLite com WAL/SHM ativos em leitura `immutable=1`. Oito casos adulterados com hashes refeitos rejeitados; corpus original 155/640 mantém PASS.
- **R270:** extensão source-gated a R239/R240 no mesmo journal: R239 48/48 SQLite byte-identical e R240 256/256; 304 replays históricos, não combates científicos novos. Auditores próprios PASS após reexecução.
- **R271:** auditores R239/R240 passaram a recusar WAL/SHM ativos e verificar `detail.before`, `detail.after`, `detail.attack_detail`, `detail.phase` e fonte do HP/PA. Falha antiga de `detail.after.G.hp=987654` reproduzida; 12/12 adulterações rehashadas rejeitadas. Auditoria de fontes nos 304 replays PASS.

### Denominadores sem inflação

- Execuções históricas revalidadas: R237 **8**, R239 **48**, R240 **256**; **312** arquivos comparados, não 312 cenas inéditas ou células oficiais.
- Testes: R18 **8** históricos, R266 **54** herdados, R267–268 **15** novos; auditor adversarial R269 **8** e R271 **12** casos de rejeição. Não somar tipos de testes como se fossem contratos.
- Aceites terminais **0/17**; células oficiais **0/1875**; promoções canônicas **0**; escritas Party/O Primeiro/fichas/DMG/Notion protegido **0**.

### Inbox

Consulta da Inbox `CM-000006`: 17 mensagens com Estado NOVA, quatro P1 (IBX-40, 62, 70, 86), 14 exigindo ACK. Destaques mais recentes IBX-160 GitHub Free fallback local, IBX-152 uso proporcional opcional, IBX-138 encaminhamento integral sem duplicidade, IBX-120 interface consultiva DMG/LEVEL-UP. Nenhum ACK ou reivindicação de INSTANCE-ID criada por esta execução. `CM-000006-I0001` não consumida; writer, lease, epoch, fencing e GREEN HOLD.

### Integridade e ponto exato

Pacote único incremental `VLAB_R267_R271_COMPAT_AUDIT_MESTRE_ONLY.zip` com patches do módulo existente, adapters de fontes, auditores existentes, testes, relatórios e manifesto. Não duplicar motor nem atualizar R237/239/240 originais. **LAST VERIFIED R271; FIRST PENDING candidato R272**, conferir colisão na Biblioteca e último Inbox antes de agir. Prioridade real: continuar interoperabilidade do executor existente com fontes válidas, proteger auditorias contra inconsistências e trabalhar progressivamente rumo aos 17 contratos sem certificação presumida.
