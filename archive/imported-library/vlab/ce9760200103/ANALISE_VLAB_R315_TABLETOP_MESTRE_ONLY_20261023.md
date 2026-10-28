# RPG ASSIMILAÇÃO — SUCESSÃO: VLAB R315 E SUA APLICAÇÃO AO TABLETOP

**Classificação:** MESTRE-ONLY · Registro incremental de continuidade, não uma nova operação, norma, engine nem homologação. 23/10/2026.

## Origem e documento autorizado
O Mestre entregou `VLAB_CODIGO_MAE_R315_FONTES_E_TESTES.zip` e pediu avaliação de reaproveitamento para o projeto Tabletop, preservando o contexto histórico e as ideias entre chats. Fonte primária desta análise = os bytes do arquivo anexado; confirmação cruzada com a seção existente `REF-INOV-VLAB-CODIGO-MAE-R315-INTEGRACAO-20261023-001` no Notion e o relatório PESQ-INOV-20261023-012. Não sobrescrever a análise anterior, os resultados do VLAB nem qualquer código oficial.

## Inspeção física nesta conversa
- ZIP externo: **SHA-256 `ab6862e2fbbe9caf7057c624530d248e8c137c30afa4d0c7307d8ca476318a9f`**, 24 entradas, CRC ZIP PASS.
- Conteúdo: `index.html` 180.740 bytes; `manifest.json` 181.761; `README_MESTRE_ONLY.md`; `reports/R315_COLD_INSTALL_LOCAL_RESULT.json`; `reports/R316_SOURCE_PREFLIGHT_AND_NEXT.md`; nove ZIPs em `source_archives/`; `tools/update_html.py`; `tests/test_sucessao.py`; fontes e registros históricos.
- Nove ZIPs de fonte embutidos: **9/9 CRC PASS**; a fonte `VLAB_STAGE12_A1A2A3_CHAT_R22_SANDBOX.zip` contém 2.286 entradas. Preservar todos os originais sem descompactar em repositório público.
- `manifest.json` declarou `last_verified=315`, `first_pending=316`, `production=HOLD`, `0/17` contratos terminais e `0/1875` células R91. Existem 315 posições históricas, mas **apenas 62 possuem marcos recuperados** e **253 estão `NAO_REAUDITADO`**: não equivalem a trabalhos inexistentes. As 17 categorias originais incluem AI tática A/B, transformação, agendamento/turnos, PA, ações/reação, replay/RNG, equipamentos e combate de grupos.
- Testes do painel executados nesta sessão com o pacote e suas nove dependências locais: **4/4 PASS**. Abrangência: manifesto=HTML, originais byte-preservados, rejeição SHA falso e atualização fictícia R316 em diretório temporário; **não executam batalhas nem homologam o VLAB**. Houve primeiro 3/4 PASS+1 erro de arquivo ausente porque a extração inicial omitira deliberadamente ZIPs de dependência; após extração correta, reexecução 4/4 PASS. Não confundir erro de preparação com falha do pacote.
- `index.html` é **autônomo**, sem `script src` ou CSS remoto. Pode ser aberto localmente em navegador Android, mas **não houve execução física no celular**. É atlas/painel, não o simulador browser.
- Relatório incorporado registra cold gate **19/19**, mas **não foi reexecutado nesta conversa**; o relatório de sucessão avisa que outros smoke/replay excederam timeout. Não declarar R316 PASS.

## Fontes mecânicas efetivas — alvos de estudo, não de cópia livre ao cliente
No ZIP histórico R22 há as fontes Python reais `fusion_stage12/vlab_r18_interactive.py` (funções `do_start`, `do_attack`, `do_pass`, `event_commit`, SQLite), `vlab_r21_dynamic_a1.py` (`create`, `validated_step`, `checked_history`, `intent_cmd_id`), `vlab_r22_chat_adapter.py` (`create`, `decide`, `view`, `checkpoint`, `restore`, `history`) e `vlab_r21_web.py` (interface HTTP para **127.0.0.1**; não publicar na internet sem segurança específica). Overlays posteriores alteram essas fontes: **não presumir que a versão R22 isolada seja o core mais recente**, nem misturar APIs sem instalar overlays em sequência e comparar proveniência. `source_archives` incluem extensões R289–R315, Esquivar nativo, sumários read-only, HTML Android e o gate de contra-ataque.

## Bloqueios mecânicos declarados pela fonte
O pacote R315 registra 128 recibos nativos R314 (64 acertos absorvidos em fixture RD100, 52 misses e 12 críticos positivos em HOLD para contrato específico), **0 contra-ataques executados**, 0/17 terminais e 0/1875 células. A proposta R316 é implementar, com validação de fonte e escritor VLAB, contra-atacar como REACTION sem consumir ação STANDARD extra, respeitando R50/R51, crítico positivo, Vantagem, idempotência, crash e replay. **Não tentar corrigir isso dentro do Tabletop** nem alegar mecanismo pronto. R315 pode não ser o estado live mais recente do VLAB; só fonte canônica atual e escritor competente podem declarar avanço.

## Valor para a arena Assimilação 2.5D multiplayer gratuita
1. **Autoridade mecânica**: o VLAB Python e seu journal poderão fornecer decisões oficiais e recibos para um backend confiável. A renderização 2.5D, Godot ou frontend web não recalcula vida, PA, dano, defesa e turnos fora do contrato homologado.
2. **Continuidade de rede**: estudar identificadores de intenção, `revision`, `head`, transações e SQLite para rejeitar comandos repetidos, usar snapshots, reconectar aparelhos e reproduzir ações sem duplicar resultados. A adaptação precisa de gate de interface e autoria; técnicas históricas não são prova de API de serviço multiplayer.
3. **Segurança Mestre/Party A+C**: Master administra marcadores; clientes Party recebem somente projeções permitidas **antes do transporte**; NUNCA expor este ZIP, painel Mestre-only, recibos completos, bancos, fontes internas ou dados ocultos em GitHub Pages/clients.
4. **Experiência Android**: atlas HTML Mestre-only demonstra possibilidade de consulta offline, não gameplay compartilhado nem APK. UI PWA e Godot são escolhas de apresentação independentes do motor canônico.
5. **IA tática**: os contratos `TACTICAL_AI_AB_FAIRNESS`, `TURN_SCHEDULER_EVENT_SOURCING`, `BATTLE_1X1_2X1_20X20` dão alvo de conformidade; produção ainda HOLD. IA de NPC precisa consultar ações legais do core competente, não criar novo motor de regras.

## Sincronização com pesquisa recente
O Laboratório do Inovador já possui `REF-INOV-VLAB-CODIGO-MAE-R315-INTEGRACAO-20261023-001` e `PESQ-INOV-20261023-012`. Esta última propõe como candidato P0 Cloudflare Workers + Durable Object e testes sintéticos de sala (43 WS localhost + 8 DOM estáticos, mais corrida e scoring artificial); **não representa multiplayer Android físico**, não publicou servidor real nem integram VLAB. Não duplicar a triagem ou repetir PESQ012 sem fato novo. O futuro Desenvolvedor receberá a implementação competente e separada.

## Ideias do Mestre que continuam vigentes
RPG recreativo não comercial, custo **R$0 adicional**, multiplayer presencial por aparelho na mesma batalha, Android prioritário, notebook da noiva eventual, estética **2D estilizada + profundidade 3D (2.5D)**, sem narrativa fixa na V1, mapas, NPCs, monstros, fichas, Vida/Alma/PA, magia e transformação demoníaca, IA tática forte, animações e áudio com modos cinemático/equilibrado/objetivo, exploração e missões só depois. FOV **A+C aprovado**. Godot já BAIXADO pelo Mestre, execução no Android ainda não verificada. Suno/ElevenLabs Free autorizados como possibilidades sob licenças não comerciais; PixelLab excluído. Codex e Work autorizáveis individualmente para MISSÃO CONCRETA apenas após briefing perfeito e pedido ao Mestre; executar/validar código, não gastar recursos com planejamento difuso.

## Critério de integração e sucessão
**VERIFICADO LOCALMENTE:** arquivo R315 original 24/24 entradas, ZIP CRC, 9/9 ZIPs internos íntegros, 4/4 testes de atlas PASS, funções Python históricas e dados do manifesto.
**RECUPERADO DO NOTION:** existência da triagem R315 e PESQ012 mais recente; não repetir.
**DOCUMENTADO PELA FONTE, NÃO REEXECUTADO AQUI:** cold gate R315 19/19 e testes históricos R314.
**PROPOSTO:** contrato de adaptador de backend sala→VLAB competente, com `create/decide/view/checkpoint/restore/history`, intenção única, estado revisionado e projeção segura. Exige autorização do escritor VLAB, assinatura do contrato de versão, segurança e testes.
**HOLD:** VLAB live atual, R316, terminal 17/17, R91, serviço cloud R$0 real, autenticação/WSS, integração mecânica, Android multiplayer físico e dados Party.
**LAST-VERIFIED:** atlas R315 4/4+9/9, fonte R315 hash físico, triagem Notion e PESQ012 lidas; gh-pages TEST32 SHA `0aa9bc817844fa4ce0e16a2103a3a89988df577c` quando verificada nesta conversa.
**FIRST-PENDING:** receber entrega do Desenvolvedor anunciada pelo Mestre e confrontar interfaces atuais com PESQ012 e R315, consultando o VLAB canônico atual quando necessário.
**NEXT:** definir a primeira tarefa pontual de Codex/Work (somente após anuência Mestre) e testar sala 1 Mestre+2 players sintéticos com dados públicos/privados segregados e backend confiável. Não integrar combate sem fonte homologada.
**NO-REPEAT:** não criar motor, AGENTS ou laboratório paralelos; não copiar VLAB Mestre-only para Party ou GitHub Pages; não proclamar R316 PASS; não pedir novo download Godot; não assinar ferramentas pagas.
