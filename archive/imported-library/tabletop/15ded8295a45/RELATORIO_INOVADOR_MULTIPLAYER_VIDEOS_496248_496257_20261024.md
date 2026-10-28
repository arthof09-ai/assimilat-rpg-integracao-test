# Tabletop Assimilação — PESQUISA COMPLEMENTAR MULTIPLAYER E DOIS VÍDEOS (24/10/2026)

**Classificação:** MESTRE-SIDE / pesquisa consultiva. **Status:** PROPOSTO e documental; NÃO é nova operação, norma, produto, autorização de deploy, ou teste de infraestrutura do RPG. **Pergunta do Mestre:** multiplayer antes/depois da base jogável? Analise os dois vídeos e referências internacionais, sem custo adicional, Android e VLAB oficial.

## Fontes físicas recebidas e limites da observação

- `496248.mp4`: MP4, 49,203 s, 360×640, 2.928.837 bytes; SHA-256 `6542e81b22183a565ff8ad2d53985b0bd18ea877561639416caa611591868b5f`. Inspeção por amostragem de ~17 quadros ao longo do vídeo + quadros pontuais. Captura com legendas EM INGLÊS.
- `496257.mp4`: MP4, 534,686 s (~8m55s), 640×360, 20.806.595 bytes; SHA-256 `1c32c481eb75cdbc646f6e447264618ac8751ff1b505303127ee10fee5b6ac71`. Inspeção por amostragem de ~36 quadros + quadros pontuais. Interface principalmente EM PORTUGUÊS.
- Arquivos de evidência local: `video_multiplayer_inspecao/496248_contact.png`, `.../496257_contact.png`. **LIMITAÇÃO:** sem transcrição técnica do áudio neste ambiente. Não foram inspecionados códigos-fonte, logs, tráfego, servidores ou telefones de terceiros associados aos vídeos; as conclusões sobre funcionalidades são VISUAIS/RELATADAS PELA TELA, não demonstração de arquitetura ou segurança.

## Vídeo 496248 — mundo social / minijogos, baixa a média utilidade

Quadros: 00:03 painel Arcade; 00:06–00:12 ambiente isométrico/social e indicação `CLUBGLUBO.COM`; 00:15 avatar/personalização de um pato; 00:18 navegação/avatar e botões de direção; 00:21 pesca; 00:24 indicadores de atividade/achievements; 00:27 leaderboard; 00:30–00:33 praça/avatares e fala visual sobre cinco pessoas; 00:42 jogo de garra; 00:48 página central. **Aproveitável:** feedback de presença, separação identidade/avatar, microinteração tocável, painel leve/visibilidade de atividade e convite. **Não comprovado:** mesmo estado em dispositivos diferentes, rede real, autenticação, servidor, escala, rollback/causalidade, regras de combate. **Decisão:** não copiar temática de patos, não implantar minijogos paralelos; usar apenas inspiração de ergonomia social para pós-MVP.

## Vídeo 496257 — Fábrica de Jogos IA / jogos HTML em arquivo único; utilidade média, NÃO prova segurança multiplayer

Quadros: 00:00–00:45 demo de condução/obstáculos em navegador; 01:05–01:15 página “Fábrica de Jogos IA”, texto “Crie jogos online com IA. Num arquivo só”, “até 8 jogadores online”, “R$0 de servidor”, “PC e celular”; 01:45–02:45 jogo de percurso com avatares coloridos; 03:00–03:45 demos de cartas; 05:00–05:45 interface semelhante a Ludo; 07:00–07:30 guia local “Você descreve. O Claude programa. Todo mundo joga” e orientações para gerar HTML; 07:45–08:40 listagem de oito jogos para baixar `.html`, incluindo “Fúria no Asfalto”, “Turma da Bomba”, “Tombo Turbo”, “Turbo Kart Rally”, “A Tocha”, “Pit Pat”, “Ludo Alto Merda” (texto pequeno de baixa resolução; nomes secundários sujeitos a erro), “Neon Dash”. A página é exibida como caminho de arquivo LOCAL no navegador.

**Aproveitável:** distribuição HTML simples com uma interface usável, exemplos pequenos por jogo, prompts orientados a resultados, convite via código de sala e compatibilidade aspirada a PC/celular; isso reforça o objetivo já existente de manter um **HTML offline funcional** para o Tabletop TEST. **Risco:** “sem servidor” pode significar sem servidor PRÓPRIO/PAGO, P2P ou dependências externas (sinalização, STUN/TURN, trackers etc.) e NÃO prova ausência de infraestrutura. Exibição de avatares na tela não prova três celulares em redes distintas. O vídeo não demonstra auditoria de autenticação/ACL, isolamento de informação Mestre-only, durabilidade de combate, persistência/recibos ou resolução VLAB. **Decisão:** não trocar a arquitetura autorizada por “jogo em arquivo só” nem importar código de terceiros não auditado; estudar apenas custo/UX, condicionando multiplayer a testes físicos e servidor competente.

## Pesquisa externa verificada em 24/10/2026 (idiomas independentes)

1. **Google Codelab oficial — jogo web de turnos com IA + Firebase + event sourcing**. Atualizado em 09/09/2026. Ensina lobby/código de partida, autenticação Firebase, registro imutável de ações, replay e recuperação do estado. Tecnologias NÃO são adotadas; valor é o protocolo/event ledger, alinhado ao VLAB e journal existente. https://codelabs.developers.google.com/codelabs/cloud-run/launch-your-web-based-video-game-with-ai — vídeo Google Cloud Tech https://www.youtube.com/watch?v=t4LOHNHv-r8 (11 minutos, indexado por página de recursos, conteúdo NÃO inspecionado diretamente nesta pesquisa).
2. **How I AI — Speedrun a 3D Multiplayer Game** (fluxo técnico: primeiro loop local jogável, depois servidor WebSocket paralelo com contrato JOIN/input/state/disconnect, testes de falhas). https://www.chatprd.ai/how-i-ai/workflows/how-to-speedrun-a-3d-multiplayer-game-prototype-in-15-minutes-with-claude-code-cli ; vídeo https://www.youtube.com/watch?v=xW5y2Yv_E2Y (episódio ~10 min, vídeo não inspecionado diretamente).
3. **Nick Saraev — game multiplayer browser com IA (09/10/2026)**. Após protótipo jogável, desenvolver online, testar com pessoas, detectar latência; relata custo ~US$31 de tokens e relay Twilio, incompatível com assumir R$0 adicional. https://aihow.tv/en/use-cases/build-a-multiplayer-browser-game-and-put-it-online/ ; vídeo https://www.youtube.com/watch?v=LD0NxqDcDiY (relatório secundário de captions, vídeo não inspecionado diretamente).
4. **SpacetimeDB — experimento jogável construído com Claude Code**. Fonte do fornecedor, demonstra modelo de estado autoritativo e assinaturas de atualização. Ferramenta NÃO adotada: https://spacetimedb.com/blog/building-with-claude-code.
5. **Colyseus — state synchronization**: cliente envia intenções, servidor altera estado; reforça um único estado autoritativo. NÃO criar servidor paralelo Colyseus. https://docs.colyseus.io/state.
6. **Godot — secure multiplayer design**: não aceitar inputs client-side como resultados oficiais; servidor autoridade sobre combate/inventários. NÃO migrar engine. https://docs.godotengine.org/en/latest/tutorials/networking/high_level_multiplayer.html.
7. **MDN WebRTC**: P2P requer sinalização e pode exigir STUN/TURN; “sem servidor” deve ser entendido no máximo como ausência de um servidor de gameplay tradicional/próprio, dependendo da implementação. https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Connectivity.
8. **Cloudflare DO SQLite + WebSocket hibernation**: solução candidata para sala persistente em Free com limites, não VLAB portado; verificar conta, runtimes, disponibilidade, custos antes de arquitetura definitiva. https://developers.cloudflare.com/durable-objects/examples/websocket-hibernation-server/ ; https://developers.cloudflare.com/durable-objects/platform/pricing/.

## Decisão estratégica PROPOSTA — multiplayer na hora certa

**FALSO DILEMA:** não é “construir todo o multiplayer AGORA” versus “ignorar completamente até jogo estar pronto”. Ordem ótima para Assimilação (jogo tático de turnos, Android, R$0 adicional, VLAB Python único):

1. **M0 ALREADY DELIVERED (TEST37)**: arena de toque, unidade→ação→alvo, prévias VISUAIS com rollback; excelente, mas não combate verdadeiro.
2. **P0 PRÓXIMO: uma batalha vertical funcional de 1 ator contra 1 alvo no MESMO aparelho com decisão oficial VLAB**: ataque + defesa e recursos reais, log/recibo íntegro, mesmo contrato como base futura de sala. Deve ser priorizado pelo responsável competente do VLAB e DEV sob governança, não por engine paralelo.
3. **P0 PARALELO LEVE:** preservar protocolo JOIN/INTENT/ACK/RECEIPT_QUERY, identidade/owner, revisão, eventos separados, projeção por papel e rollback/recuperação, e TESTar um caminho cliente→servidor→recibo; não aumentar escopo para lobby generalizado ou contas reais agora. Código existente Codex 0.2 e PESQ016 são base, não refazer.
4. **DEPOIS de batalha vertical PASS:** provar Mestre + 1 player em sala real TEST, só então +1 player e autenticação, WSS, isolamento dos campos Mestres e reconexão. Android físico e VLAB mecânico devem ter gates independentes. Não autorizar segredo Mestre-only em ambiente público.
5. **P2+**: múltiplas salas, matchmaking, otimizações de escala, mundos persistentes, minijogos sociais, arte/polimento, hospedagem permanente e integrações “serverless” da moda.

**Proporção de prioridade para próxima coordenação, NÃO nova norma:** ~70% da capacidade voltada à batalha VLAB jogável, ~20% na ponte mínima receipt e ~10% em pesquisa de bugs/segurança, ajustando conforme dependências reais. Não descartar já concluídas as ordens enviadas pelo Mestre aos três executores. Próxima intervenção apenas após seus PSV ou evidência urgente.

## Resultado e continuidade

- **VERIFICADO visual/documental:** duração, frames acima, hash do arquivo, texto capturado da tela, documentação citada, baseline Codex0.2 e TEST37 previamente auditados.
- **INFERIDO:** arquitetura real dos criadores dos vídeos, se realmente funcionam dois/três celulares, se usam P2P/terceiros. Não canonizar.
- **PROPOSTO:** estratégia “vertical slice mecânico primeiro com protocolo multiplayer mínimo em paralelo”; não altera assignments ou decisões antigas.
- **PENDENTE:** qualquer áudio técnico sem transcrição, validação de network stacks dos vídeos, código original e handshake real; a ABI VLAB do RPG; real auth/WSS e 3 celulares.
- **LAST-VERIFIED:** vídeos locais/quadros e documentação; **FIRST-PENDING:** observar PSV de TEST38/Codex/PESQ após ordens já entregues e reavaliar priorização com evidência; **NO-REPEAT:** cinco lotes anteriores, PESQ015/016, Codex 0.1/0.2, TEST36/37, reimplementar motores ou seguir promessa de “sem servidor” sem teste.
- **NAC-PASS proporcional:** PASS consulta/registro/pesquisa; HOLD para fonte de vídeo, multiplayer real, produção ou adoção de infraestrutura.
