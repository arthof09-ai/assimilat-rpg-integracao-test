# RPG Assimilação — Auditoria do Código-Mãe VLAB R315 para o Tabletop Interativo

**Data:** 23/10/2026  
**Classificação:** MESTRE-SIDE / MESTRE-ONLY / análise TEST.  
**Papel:** Coordenação funcional do Inovador — análise de arquitetura, NÃO execução do motor VLAB nem novo writer.  
**Fonte física:** `VLAB_CODIGO_MAE_R315_FONTES_E_TESTES.zip`, entregue novamente pelo Mestre.  
**Operações afetadas:** OP-VLAB-FUSION-SANDBOX-01, Laboratório do Inovador e Tabletop Assimilação. Nenhuma escrita em Party/O Primeiro nem publicação de código interno.

## 1. Verificação e escopo

**VERIFICADO NO ZIP ENVIADO:** 14.869.981 bytes; SHA-256 `ab6862e2fbbe9caf7057c624530d248e8c137c30afa4d0c7307d8ca476318a9f`; 24 entradas externas; CRC externo válido. Conferidos `README_MESTRE_ONLY.md`, `manifest.json`, documentos de pré-gate R316, relatório documental de instalação fria R315 e fontes Python dos overlays históricos. Foi realizada leitura estática de assinaturas e fluxos das versões selecionadas R18/R21/R22 e overlays R289–R315. **Não foi reexecutado, neste exame, o conjunto de 19 testes da reconstrução fria, a execução de combate real, a implantação cloud ou teste físico Android.** O relatório do pacote declara cold-gate 19/19 PASS como evidência arquivada, não repetida nesta instância. Uma análise anterior do mesmo ZIP verificou separadamente os 4/4 testes do atlas.

**MANIFESTO (afirmação do artefato, não estado live mais recente):** último marco R315, primeiro pendente R316; 315 posições históricas, 62 marcos recuperados e 253 NÃO REAUDITADOS; 0/17 contratos terminais homologados; 0/1.875 células R91; produção HOLD. O atlas `index.html` não é um simulador de combate.

## 2. Matriz de reaproveitamento — evidência → utilidade → limite

| Recurso do VLAB observado | Evidência primária | Valor para Tabletop | Situação |
|---|---|---|---|
| Comandos `create/state/actions/decision` | `vlab_r22_chat_adapter.py`, funções `run`, `create`, `decide`, `view` | Modelo de interface entre cliente e motor autoritativo | REFERÊNCIA TEST; ainda não API de rede nem sessão multiplayer |
| `revision`, `head`, `intent_id` | `decide`, `validated_step`, `intent_cmd_id` | Deduplicação, concorrência otimista e detecção de conflito | APROVEITAR PADRÃO; adaptar identidade e autenticação em servidor, não expor journal bruto |
| Journal SQLite com recibos/hashes | `vlab_r18_interactive.py`, `event_commit`; R21 `checked_history` | Replay determinístico, rastreabilidade, suporte a auditoria e recuperação | TÉCNICA TEST; não certificação de regras nem de sincronização remota |
| Checkpoint, restauração e suspeita de efeito parcial | R22 `checkpoint`, `restore`, `inspect_pending` | Reconexão, retomada, resolução de operações incertas | ÚTIL como design, mas ZIP SQLite bruto jamais para a Party |
| Agenda de turnos | R21 `A1ExternalScheduler`, controle `TURN_*` | Ciclo de fase/rodada/turno e eventos para animação | TEST com dois atores; disputas multiator e desempates HOLD |
| Ataque, defesa e esquiva | R18 `do_attack`; overlay R308/R309 | Futuro contrato autoritativo de resultados de combate | FIXTURES fictícias; integração canônica depende de homologação |
| Contra-atacar | R312 classificador; R315 guarda no R22 | Interface pode mostrar indisponibilidade, nunca executar por simulação | HOLD: falta ataque nativo consumindo REACTION em transação única |
| Resumos e exportação HTML | `vlab_r304_summary.py`, `vlab_r310_export_html.py` | Tela de auditoria Mestre e replay de leitura | MESTRE-ONLY; não transferir saída bruta para clientes |
| Magias, PA, transformação, equipamentos, bestas e IA | 17 contratos do manifesto; rubricas do VLAB | Definem futuros cenários de teste mecânico e IA | HOLD TERMINAL; não assumir sistema completo |

**LIMITAÇÃO MATERIAL CONCRETA:** o R21 `_runner` usa `R21_TWO_ACTORS_ONLY`, e seu `checked_load` exige ordem de dois atores. O R22 oferece `START`, `ATTACK`, `PASS`, `HEAL` no laboratório, com `HEAL` 1d6 fictício e custo zero, recusando custo/magia real. Não usar como evidência de grupo 2×1, 20×20 ou técnicas reais da campanha.

## 3. Contrato candidato para o multiplayer (PROPOSTO, SEM EXECUÇÃO)

**Client Android (web/PWA, Godot futuro opcional)** → **serviço de sala autenticado** → **interface do VLAB oficialmente versionada e homologada** → **journal/estado autoritativo** → **projeções separadas por papel ANTES do envio** → clientes. A sala de transporte não adjudica ataque, dano, Vida, Alma, PA, RD, rolagens, magia ou transformação. O VLAB não assume autenticação e autorização dos participantes por existir o R22 `chat.run`.

**Envelope mínimo de intenção sintética para o Desenvolvedor testar:** `room_id`, `client_action_id`, `expected_public_revision`, `actor_token_id`, `action_type`, `target_token_id` e `arguments_public`; o servidor vincula a identidade real da conexão, rejeita comandos fora do papel, converte somente após contrato formal competente, grava no máximo uma decisão e retorna revisão + recibo público projetado. `head`, hashes internos, sementes, bancos, snapshots completos, fontes e condições ocultas permanecem Mestre-side. Não confundir o envelope de transporte PROPOSTO com ABI VLAB já homologada.

**Três visões distintas:** painel do Mestre (capacidade administrativa e segredos), visão Party 1 e visão Party 2 (somente informações compartilháveis e autorizadas). Projeção por whitelist a partir de estado Mestre, nunca ocultação de CSS/JS: dado secreto não deve chegar ao navegador, nem mesmo como campo invisível. Tokens efêmeros/sessões e ACL devem ser testados; armazenamento de credenciais em cliente estático é vedado.

**Sequência de aceitação inicial sem mecânica:** (1) Mestre cria sala sintética; (2) duas players entram em dispositivos/navegadores distintos; (3) três visões recebem estado revisionado; (4) comando duplicado aplica no máximo uma vez; (5) corrida de revision gera um aceite e um conflito; (6) reload/reconexão recupera snapshot e gap de eventos sem reaplicar intenção; (7) payload das players falha no teste se contiver qualquer campo secreto; (8) cliente adulterado não controla token alheio; (9) perda/timeout diferencia `UNKNOWN` de `NO_EFFECT`; (10) sem VLAB oficial, nenhuma mecânica real habilitada; (11) quotas Free, HTTPS/WSS, Android físico e custo R$0 são comprovados antes de deploy real.

## 4. Lacuna crítica: Python VLAB versus backend Cloudflare

**CONFIRMADO PELAS FONTES ATUAIS:** Cloudflare Workers oferece Python via Pyodide, mas o filesystem é efêmero, `threading` e `multiprocessing` não funcionam normalmente; Durable Objects têm API de armazenamento SQLite própria e garantias de persistência separadas. Fontes: https://developers.cloudflare.com/workers/languages/python/ ; https://developers.cloudflare.com/workers/languages/python/stdlib/ ; https://developers.cloudflare.com/durable-objects/api/sqlite-storage-api/ ; https://developers.cloudflare.com/durable-objects/platform/pricing/ .

**INFERÊNCIA ARQUITETURAL RELEVANTE:** o código R21/R22 usa conexão SQLite local por path, manipulação de arquivos e subprocessos/cold snapshot; o simples suporte de Python no Cloudflare **não comprova execução direta desse VLAB sem alterações**. Não presumir que o Durable Object atual seja host do executor Python ou que converter a regra para JavaScript seja uma adaptação sem motor paralelo. Tratar como um gate técnico independente: preservar Python executor onde houver runtime compatível e criar transporte autenticado; ou comprovar por teste de contrato uma adaptação oficialmente autorizada, preservando fonte única e paridade. Infraestrutura gratuita para hospedar Python autoritativo em produção segue PENDENTE — não prometer custo zero real antes de prova.

A primeira sala sintética em Cloudflare pode ser valiosa **como laboratório de transporte e ACL**, sem alegar integração ao motor. A pesquisa PESQ-INOV-20261023-012 produziu ensaios WebSocket locais, NÃO implantação Cloudflare no Android.

## 5. Dossiê para divisão de trabalho

**Coordenador (esta frente):** custodiar decisões, comparar requisitos com R315 e PESQ012, controlar `LAST-VERIFIED`/`FIRST-PENDING`, apontar integrações ilegítimas e manter documentação incremental sem writer herdado.  
**Pesquisador:** provar limite de compatibilidade Python/Cloudflare, estratégia de transporte viável em R$0, identidade e segregação de payloads, alternativas servidor Python host compatível e riscos Android. Não editar código do Desenvolvedor.  
**Desenvolvedor:** implementar, em sua própria branch/test bench existente, **apenas sala multiplayer de dados sintéticos** com ACL/deduplicação/reconexão e testes. Não escrever mecânica nem VLAB nem lançar deploy sem gate.  
**Executor VLAB:** único responsável pela correção nativa R316, source-freeze e ABI homologada, sob suas próprias permissões.  
**Codex/Work:** somente mediante autorização específica do Mestre e missão delimitada; Codex como executor de código com teste, Work para investigação executável ou validação pontual de infraestrutura. Não iniciar ambos com tarefas sobrepostas.

## 6. Estado de continuidade

- **VERIFICADO:** integridade do ZIP remetido; API e restrições de fontes Python selecionadas; R315 guarda Contra-atacar; R21 limita dois atores; HTML é atlas Mestre.
- **DOCUMENTADO EM FONTES:** cold 19/19, 128 recibos nativos R314 distribuídos 52 misses, 64 hits RD100 com net=0 e 12 críticos positivos em HOLD; zero Contra-atacar efetivado. Não reexecutados neste exame.
- **PROPOSTO:** contrato de sala sintética, revisões públicas, ACL, teste de duplicatas, renderização separada de autoridade mecânica.
- **PENDENTE/HOLD:** R316; 17 contratos; R91; transformações, equipamentos, IA e magias reais; ABI de grupo; Python Cloudflare; autenticação real; app Android; 3 players físicos; custo e hospedagem reais.
- **LAST-VERIFIED:** exame estático e hash do R315 com fonte Mestre-only; recuperação documental do Laboratório/Notion e da pesquisa PESQ012.
- **FIRST-PENDING:** confrontar entrega mais recente do Desenvolvedor e D-INOV-033 com o contrato sintético; ensaiar autenticação/transporte com payloads artificiais; abrir negociação de ABI atual do VLAB apenas com executor competente.
- **NO-REPEAT:** não publicar o ZIP R315 ou dados Mestre; não criar motor, operação, laboratório, Diário nem identidade paralelos; não prometer o R316 como concluído; não converter pesquisa em certificação de produto.

**NAC-PASS proporcional:** PASS documental/estático e integridade; integração VLAB→Tabletop e produção HOLD. Sucessão institucional ainda requer governança própria.
