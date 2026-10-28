# RPG Assimilação — Auditoria visual dos vídeos Lote 02 e prova mobile-first do TEST 36

**Ambiente:** MESTRE-SIDE / pesquisa e PROVA TEST isolada  
**Data local de recepção:** 23/10/2026 (America/Recife). **Objetivo permanente:** Arena de COMBATE TÁTICO MULTIPLAYER do RPG Assimilação, e não jogo de exploração, idle, minecraft, áudio ou motor concorrente.  
**Evidência:** três MP4 originais recebidos no chat, verificados por FFprobe/SHA-256; 132 amostras visuais distribuídas por toda a duração, ampliados pontos de interesse. **Não houve transcrição integral das falas, acesso ao código original dos criadores, nem prova do que não é visualmente demonstrado.**

## 1. Integridade e linha do tempo do lote

| Arquivo | Duração | Bytes | SHA-256 |
|---|---:|---:|---|
| 495967.mp4 | 39m50,6s | 102.428.489 | `b7fca59746b7dfeddbfc5fc7c5b2989836e7b5f09fd692fda5132cd5399dff7a` |
| 495980.mp4 | 39m25,0s | 77.349.797 | `c515556003432c8e3faa0b9e2c2a392324115708841d5091ff64beef93183f04` |
| 495988.mp4 | 10m55,1s | 29.941.179 | `5bca527219b90ee1abfbe2acbb19f683b69452c3acb29f36b81b4d0d31a87c7c` |

**Tempo total ~90m10,7s.** Todos têm vídeo H.264 640×360 e áudio AAC. Aproximações temporais nos capítulos são janelas observadas por frames, não transcrição.

## 2. Vídeo 495967 — Processo de construção com IA e validação

**Observado:**
- 0:00–2:00: o autor exibe como referência visual uma arena de ação com inimigos e barra de combate, em seguida discute a meta do experimento.
- ~2:40–10:00: tela de planejamento com cartões/especificações, conversa com ferramenta de IA e documentação de regras/tarefas; nenhuma dessas telas comprova código pronto.
- ~10:30–17:00: transição para criação de arquivos e teste de programa simples (janela THE CAVE / SALA DE TESTE, com WASD/setas e espaço para atacar). É um incremento funcional pequeno, não a apresentação final.
- ~18:00–26:00: reiterações no editor/código e análise de defeitos/regras.
- ~27:00–35:00: referências de interfaces de outros jogos (incluindo menus complexos), que ilustram como menus e ações são apresentados, sem comprovar o motor/serviço original do vídeo.
- ~35:00–39:50: mais código, versões e observações do criador.

**O que se pode reaproveitar:** roteiro em unidades FECHÁVEIS: especificar UMA ação tática do Assimilação → conectar ao código da Arena existente → executar em teste → corrigir até o Mestre conseguir tocar a ação e ver um recibo. Anexar a cada RUN evidência de tela e evento, não apenas aumento de contadores PASS.

**O que NÃO é prova:** multiplayer entre celulares, VLAB, regras do Assimilação, que todo jogo foi criado em 39 minutos, que uma IA serve como engine ou que é necessário contratar a ferramenta do autor.

## 3. Vídeo 495980 — Visual e interface de RPG 2.5D no navegador (prioridade máxima de apresentação)

**Observado:**
- ~1:40–6:00: navegação em ambiente exterior detalhado com perspectiva oblíqua, caminhos orgânicos, vegetação, personagem e HUD.
- ~6:30–12:00: interiores de masmorra isométricos, iluminação localizada, efeitos visuais, personagem e objetos em camadas.
- ~14:00–18:00: interface de login/seleção de personagem de um projeto denominado na tela **Dunloc Online**; presença de UI de login não prova autenticação ou backend produtivo.
- ~18:00–23:00: interface com ferramenta de sprites/quadros e personagem animado (observável visualmente) e navegação em cidade com inventário/barra de habilidades.
- ~25:00–31:00: diferentes cenas de masmorra e ações visíveis durante combate; sem acesso ao código/recibos não se pode homologar cálculo de dano ou segurança de multiplayer.
- ~31:00–39:25: personagem explorando campo com HUD de equipamento, minimapa, lista de ações e progressão. Cenário e menu aparecem simultaneamente; não é preciso procurar o jogo abaixo de grandes formulários.

**Aplicação CONCRETA ao Assimilação:** o MAPA deve ser o principal elemento da primeira tela Android; painel de unidades/turno/ações à vista ou a um toque, opções avançadas recolhidas; personagem e alvo claramente selecionados; dano/PA/efeito SOMENTE por recibo do VLAB competente. Camadas bonitas são prioridade visual posterior à interação de combate, sem usar sprites do autor.

**Limites:** não inferir que HTML simples (sem JS/Canvas/WebGL) produz essa renderização. Nem o vídeo comprova licença para reaproveitar seus tiles/personagens, autenticação séria, custo ou uso em três aparelhos Android.

## 4. Vídeo 495988 — Editor Unity, desenho de cenas e tiles

**Observado:** ~0–10:55 demonstrações de ambientes 2D tipo RPG, layouts de vilarejo, casas, caminhos, árvores, água, UI e mudanças do cenário, vistos num editor de desktop com hierarquia/inspector compatível com **Unity Editor**. O software exato aparece visualmente consistente com Unity; confirmação das funcionalidades internas/versão depende de projeto-fonte que não temos.

**Aplicação:** reutilizar o MÉTODO de mapas por camadas, tiles, objetos e cenas no sistema atual do Tabletop, sem converter a aplicação inteira. O módulo de editor e importação de tiles pode ser componente posterior do mesmo Tabletop, preservando grade/alcance/LOS/FOV reais.

**Bloqueio de ferramenta:** o Unity Editor oficial requer sistemas de desktop Windows/macOS/Linux para edição (fonte oficial Unity 6.3). **Não é a rota Android-first do Mestre.** Substituição apropriada NÃO é portar o código Unity à força: o Tabletop HTML/JS já possui mapa, tiles, editor e zoom. Evoluir esse código é a alternativa real de custo adicional zero. Godot instalado segundo relato do Mestre continua alternativa sob avaliação, não uma migração aprovada.

## 5. Alternativas gratuitas sob teste/prova

| Recurso do vídeo | Sem gastar mais | Estado honesto |
|---|---|---|
| Game editor pesado de desktop para montar mapas | Editor HTML/JS do Tabletop existente + tiles PNG próprios/CC0 | **Implementado parcialmente** no TEST36, sem acabamento da referência |
| Menus e HUD estilosos em browser | HTML/CSS nativo do projeto, com compactação mobile; Phaser (MIT) e PixiJS (MIT) como opções de bibliotecas somente se benchmark provar necessidade | **Prova TEST executada para HTML/CSS**; Phaser/PixiJS apenas verificados na documentação, NÃO instalados/testados |
| Geração de código e planejamento por IA | Codex/ChatGPT já disponíveis no projeto | **Uso anterior verificado/relatado**, não código dos autores dos vídeos |
| Arte e sprites originais | Criar manualmente/automatizar atlas próprios, aproveitar fontes CC0 verificadas | Pipeline original testado no Lote 01; direitos de sprites dos vídeos **NÃO demonstrados** |
| Combate e lógica do jogo | VLAB Python autorizado + UI/eventos da Arena existente | **HOLD** da integração real; não criar segundo motor |

Fontes oficiais: https://docs.phaser.io/ ; https://phaser.io/download/license ; https://github.com/pixijs/pixijs ; https://docs.unity.com/en-us/engine/6000.3/manual/get-started/install-and-upgrade/getting-started-installing-unity/system-requirements

## 6. Prova TEST que muda algo visível, feita sobre código REAL TEST36

**Problema reproduzido:** em Chromium Linux com viewport emulado **390×844**, renderizando os arquivos AUTÊNTICOS do pacote `TABLETOP_SITE_SINTETICO_TEST36_CANDIDATE.zip`, a primeira célula da Arena começa após barras de configuração. A janela `#viewport` começa em **y=864,8 px**, abaixo dos **844 px** disponíveis. O Mestre precisa rolar antes de ver o tabuleiro.

**Solução isolada TEST, não merge:** a partir da cópia byte exata do TEST36, adicionados `arena-primeiro.css` e `arena-primeiro.js` e uma barra de navegação simples em `index.html`. Em telas móveis, a vista inicia com configurações recolhidas; botões **Ferramentas** (abre/fecha) e **Unidades** (rola ao painel existente). Nenhum motor, mapa, token, regra, receptor websocket, journal ou armazenamento foi reescrito. `styles.css`, `app.js`, `room-v2-adapter.js` e `room-client.js` continuam byte a byte idênticos aos originais.

**TESTE FÍSICO EM CHROMIUM 390×844 (não Android físico):**
- Original: `viewport_y=864.8`, Arena fora da primeira tela.
- Cópia TEST: `viewport_y=157.8`, Arena VISÍVEL na primeira tela.
- 49/49 células do mesmo tabuleiro preservadas; SEM erros JavaScript no smoke.
- Botão abre → ferramentas aparecem; fecha → ferramentas somem; papel do Mestre e dados da Arena preservados no código.
- Documento offline único reconstruído mantendo CSP por hashes, `connect-src 'none'`, 49 células, controles testados via `page.set_content` no Chromium. Tentativa de abrir `file://` diretamente no ambiente de teste: `ERR_BLOCKED_BY_ADMINISTRATOR`; **Android real ainda não testado**.

**ARTEFATOS:** `TABLETOP_TEST36_ARENA_PRIMEIRO_OFFLINE_TEST_20261024.html` (abrível em Android quando o sistema permitir HTML local, ainda sem prova física), `TEST36_PROVA_MOBILE_ARENA_VISIVEL_20261024.zip` (cópia multifile com os scripts originais preservados), screenshots antes/depois, testes e relatório. Resultado é uma **correção de usabilidade da Arena** efetivamente executada em laboratório, **NÃO um combate mecânico, multiplayer real nem publicação**. Essa versão NÃO substitui o TEST36 canônico nem deve ser chamada TEST37.

## 7. Próximo resultado de jogo exigível ao Desenvolvedor (sem invadir writer)

1. Integrar **se adequado e autorizado** a barra compacta na árvore de código oficial do Desenvolvedor, com regressões seletivas e teste Android físico.
2. Mostrar unidades, iniciativa e seleção de ação/alvo no primeiro viewport mobile, mantendo a arena como principal espaço visual.
3. Acionar movimento / ataque apenas após autorização de identidade e turno; exigir recibo de decisão VLAB competente para dano, PA e reações. Sem ABI oficial, mostrar HOLD inequívoco; não criar regra substituta.
4. Uma atualização só recebe rótulo "melhoria de jogabilidade" quando o Mestre consegue tocar **ação de batalha** com origem de regra, feedback visual e continuidade real. Caso não, classificá-la como usabilidade/infraestrutura TEST.
5. A+C: payloads Party não contêm campos Mestre-only; o protótipo UX não é controle de segurança.

**LAST-VERIFIED:** três vídeos auditados visualmente e por metadados; TEST36 original e cópia TEST comparação y=864,8→157,8; quatro arquivos JS/CSS oficiais intactos; offline com CSP e botões em Chromium.  
**FIRST-PENDING:** integração da solução de UX sob writer competente; ação mecânica VLAB no tabuleiro; três aparelhos Android; evidência atualizada do Codex.  
**NEXT:** submeter diagnóstico UX e cenário de ação tática como proposta ao Desenvolvedor, sem escrita na branch dele.  
**NO-REPEAT:** não retomar análise dos vídeos do Lote 01, refazer RUN011–013 ou PESQ012–014, gerar game genérico, usar assets alheios, promover servidor ou mudar motor.  
**NAC-PASS proporcional:** PASS metadados/frames, provas Chromium e integridade local; HOLD áudio/transcrição integral, Android real, VLAB e produção.
