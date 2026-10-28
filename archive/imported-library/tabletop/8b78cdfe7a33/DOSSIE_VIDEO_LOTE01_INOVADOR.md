# RPG Assimilação — Dossiê de vídeos do Mestre, lote 01

**Ambiente:** MESTRE-SIDE / Laboratório do Inovador existente / R$ 0 / Android prioritário  
**Fonte:** vídeos MP4 originais enviados pelo Mestre nesta conversa; arquivos 495923, 495933, 495943, 495950, 495957  
**Metodologia:** metadados FFprobe, quadros amostrados com FFmpeg ao longo de cada gravação e exame de quadros-chave em resolução ampliada. **Não foi realizada transcrição integral das falas**; por isso são verificadas as demonstrações visuais e inscrições legíveis, mas não a totalidade de afirmações feitas por narradores. Não houve acesso a repositórios privados/código-fonte dos autores. Descrições do tipo “feito em cinco horas” são alegações dos criadores, não benchmarks auditados.

## Denominador e integridade

| Arquivo | Duração | SHA-256 completo | Amostras com timestamps | Foco |
|---|---:|---|---:|---|
| 495923.mp4 | 33m56,67s | `d311aec0fc1247dbdefa146253e3e444c49e77c37334550323f0c27ad37ce35c` | 26 | Game loop / processo de desenvolvimento com IA |
| 495933.mp4 | 2m27,49s | `2e16baf7d9d2d74a7d4f06e1850fdf392ccb393db416501a64cb363711a1d443` | 15 | Sistema de clima, dia/noite e eventos ambientais |
| 495943.mp4 | 6m55,61s | `965de34c2f3ba973baa2dc96d3073d57e5db6e3a0b97b44b6938a50ca5e27b67` | 20 | “Cinzas de Véspera”: sala de RPG visual, HUD, recursos e habilidades |
| 495950.mp4 | 1m34,97s | `2d510796bc1ac2d26fdba745c820414dd4d4a3c07cb432e0c6913c092e68fdd5` | 14 | Iteração de mapas, biomas, interiores, NPCs, arte |
| 495957.mp4 | 34,67s | `b5433fa08f0c62b3a61ccbe35ef11ed85af3a413e72ec4ef99b53ef9015f8ec8` | 12 | Vídeo promocional “RPG em 5 horas”, cena 3D |

**Duração total ~45m29,41s**. Os thumbnails ampliados e cinco folhas de contato fazem parte do pacote de evidências. Vídeos brutos permanecem vinculados a esta conversa; não foram republicados dentro do ZIP para evitar 100 MB de duplicação e redistribuição indevida de material de terceiros.

## 495923.mp4 — desenvolvimento de game com IA (prioridade ALTA para método)

- **00:00–02:30:** demonstra o jogo “Pest Must Die”, com menu, criaturas e HUD/loop em cena escura, arena jogável em demonstração e retorno a estatísticas/área de progresso.
- **~03:00:** examina recursos de arte de terceiros, incluindo “Bountiful Bits” (página de pacote de tiles), cujo regime de licença deve ser conferido antes de importar qualquer arquivo. Não usar a imagem do criador sem permissão.
- **~04:00–14:30:** telas de prompts, editor, geração de código, organização do projeto e solução de problemas. Não basta copiar o prompt sem entender o projeto.
- **~16:00–23:00:** apresenta rascunhos de interface e, mais adiante, um mapa de nós/seleção de melhorias. Esse é um **loop de decisões** que gera progresso visível, não simplesmente infraestrutura.
- **~24:00–30:00:** volta a cenas de jogo e telas de habilidades, progresso e combate; há demonstração e iteração.
- **~32:10–33:40:** retorna a notas, ferramentas e vídeos relacionados.

**Aproveitamento para Assimilação:** priorizar uma vertical de combate com *ordem de turnos → seleção de ação/ator/alvo → recibo autorizado → feedback com Vida/Alma/PA/status*, e só depois polimento visual. Aproveitar abordagem de mudanças pequenas que passam teste de interface e teste mecânico. **NÃO adotar automaticamente** upgrades roguelite, XP por segundos ou combate automático do vídeo; não comprovado compatível com VLAB. Importante: nenhuma prova observada de multiplayer seguro ou de regra de RPG Assimilação.

## 495933.mp4 — clima e eventos ambientais (prioridade MÉDIA)

- **00:00–00:20:** terreno florestal top-down e apresentação do sistema climático; afirmação visual “100% vibe coded” é relato de autoria, não auditoria de código.
- **00:25–00:45:** ícones e parâmetros **CALOR, UMIDADE, EMPURRÃO**, vento, frente fria, serra, chão quente, e chuva visível sobre água e vegetação.
- **~00:50–01:20:** UI temporal; demonstra mudança de horário, nascer/pôr do sol e trajetória solar, densidade da chuva e diferenças de luminosidade.
- **~01:30–02:00:** exibe árvores e efeitos ambientais como frente fria/vento afetando a aparência e a vegetação.
- **~02:00–02:27:** interações de fogueira e cards adicionais de eventos e limitações do sistema.

**Aproveitamento correto:** atributos ambientais de cena (chuva, vento, visibilidade, calor) separados em **CAMADA VISUAL** e **EFEITO MECÂNICO HOMOLOGADO**. A camada visual pode alterar gotas/cor/iluminação; testes de campo e turnos podem usar metadados. Não aplicar dano, empurrão, penalidade, velocidade ou FOV mecânicos sem norma/cálculo autorizado pelo VLAB. Clima não deve bloquear o marco atual de combate.

## 495943.mp4 — “Cinzas de Véspera” (prioridade MUITO ALTA para HUD e ações)

- **00:15–00:45:** arena tipo masmorra no browser, personagem central, inimigos, barra de ações/ícones, Vida, XP, equipamento e diário de eventos; outra cena “Vigília de Pedra”.
- **00:45:** tela lista Claude, ChatGPT e DeepSeek como IAs que o autor usou. Isso não demonstra que as três são necessárias ou que ele as usou simultaneamente.
- **~01:00–01:50:** alternância entre arena e sprites/arte; há referência a “pixellab.ai — sprites e animações”; PixelLab é EXCLUÍDO pelo Mestre e não deve ser reintroduzido como condição.
- **~02:00:** aparece o site de download do **Godot para Windows**; não demonstra que a implementação do jogo exibido depende exatamente desse binário ou que funciona no Android do Mestre.
- **~02:20–05:20:** interface mostra progressão em sala, Vida, XP, Essência, ataque, runas/equipamento, diário, memórias de inimigos, compras/decisões. Em uma tela lê-se “Fagulha automática — a cada 3s” e “Tudo acontece sozinho”; **parte da jogabilidade é automática/idle**, portanto NÃO copiar a lógica mecânica para nosso combate tático por turnos.
- **~05:50:** apelo explícito a feedback de jogadores.

**Aproveitamento central:** o que falta na Arena Assimilação é tornar **visíveis as decisões e seus resultados**: HUD de personagem/monstro, botões de ação, alvo e status, log que explique quem agiu/por que acertou/custo PA, antes/depois. Inspiração para PRESENTAÇÃO, **não** regras, não motor concorrente, nem IA autônoma com efeitos fora do VLAB.

## 495950.mp4 — mapa/criação visual (prioridade MÉDIA)

- **00:05–00:30:** jogo top-down com personagem placeholder, blocos/terrenos e menus de cena/mapa; parece produto em evolução, não código disponibilizado.
- **~00:32–00:55:** cena de interiores/NPCs, caminhos e objetos, depois câmera em área exterior.
- **~01:00–01:30:** substituição de sprites provisórios por terreno com vegetação/árvores e composição mais rica, mantendo estrutura espacial anterior. Mostra incrementalidade, não demonstra física de combate.

**Aproveitamento:** desenhar tiles que mantenham a geometria de grid, alcance, obstáculos/oclusão e hitboxes do TEST36; nunca converter tabuleiro oficial em mini-jogo de caminhada. Melhorias visuais devem seguir comandos de ação autoritativos e testes de toque Android.

## 495957.mp4 — “fiz um RPG em 5 horas” (prioridade BAIXA para arquitetura)

- **00:00–00:10:** vídeo vertical de perfil “Uniday Studio” com texto promocional sobre construir RPG em cinco horas.
- **00:12–00:34:** demonstra menu e cenário 3D com gramado, árvores e personagens, sem código detalhado, contratos, licença, testes, multiplayer, segurança ou comprovação do tempo de produção.

**Aproveitamento:** referência de ritmo de prototipagem e comparação visual, não motivo para migrar HTML/JS para engine 3D ou abandonar regras. **Velocidade declarada não equivale a projeto completo.**

## Ferramentas reconhecidas e alternativas com evidência

| Requisito | Ferramenta mostrada/pressuposta | Alternativa gratuita/pragmática | Evidência/limitação |
|---|---|---|---|
| Programar com IA | Claude, ChatGPT e DeepSeek citados | **Usar ChatGPT/Codex conectado ao GitHub**, já configurado pelo Mestre | Sem novo plano pago ou três agentes simultâneos; a implementação real continua precisando de testes e integração |
| Gerar sprites por IA | PixelLab foi citado em 495943 | **Pacotes Kenney CC0** (tiles 16×16 e personagens) e **Pillow para atlas PNG**; Piskel apenas quando dispositivo compatível | Kenney fonte oficial CC0; PNG+atlas Pillow+Canvas foram TESTADOS em laboratório. **A arte gerada neste teste não tem qualidade de produto final e não foi integrada ao Tabletop**. Pacote Kenney ainda não baixado/integrado e sua compatibilidade artística deve ser avaliada |
| Editar pixel art | Não comprovada ferramenta única em todos os vídeos | Piskel editor web gratuito e open source, preferencialmente desktop; no Android, usar exportação de PNG/edição leve automatizada quando permitido | Página do Piskel recomenda desktop e README oficial diz sem suporte mobile: **NÃO homologado Android** |
| Mapas/terreno | Biomas e tiles top-down nos vídeos | HTML/CSS/JS já existente no TEST36 + sprites/tilemap e exportação PNG | **Sem novo motor**; a preservação de geometria, FOV e toque exigirá testes de integração pelo Desenvolvedor |
| Engine completa | Godot Windows mostrado em 495943 | **Preservar HTML/JS**. Godot Android como laboratório opcional, não migração | Documentação Godot Android reporta limitação em celulares, sem C#/Mono; Mestre já baixou Godot, teste físico pendente |
| Clima | Efeitos e UI do 495933 | Parâmetros de apresentação/eventos de cena controlados pelo servidor competente, aplicação dos efeitos mecânicos somente após VLAB | Proposta, não implementada nem homologada. Não criar sistema meteorológico novo antes do combate |
| Arte de terceiros | Bountiful Bits e assets de vídeos | Recursos CC0 com fonte/licença clara, sprites autorais | Não importar assets do vídeo sem verificar licença e autoria |

**Fontes primárias externas verificadas:**
- Kenney Roguelike/RPG Pack: https://kenney.nl/assets/roguelike-rpg-pack (CC0, 1700 tiles 16×16)
- Kenney Roguelike Characters: https://kenney.nl/assets/roguelike-characters (CC0, 450 assets)
- Piskel: https://www.piskelapp.com/ ; https://github.com/piskelapp/piskel (editor web gratuito; *mobile não suportado oficialmente*)
- Godot Android: https://docs.godotengine.org/en/4.5/tutorials/editor/using_the_android_editor.html (limitações Android)

## Experimento executado na mesma rodada: alternativa R$0 ao pipeline de sprites

**Prova técnica limitada (não produto):** `build_assets.py` gera sprite sheets PNG para duas unidades SINTÉTICAS, cada uma com quatro direções e dois frames por direção (8 frames; atlas PNG 48×96), além de três tiles 24×24. `MANIFESTO_ASSETS_TEST.json` registra dimensões, SHA-256 e tamanho. `visualizador_atlas_TEST.html` usa Canvas/JavaScript para exibir PNGs e mudar a direção sem motor de jogo paralelo. 5/5 arquivos PNG decodificam, atlas/frame/tiles têm dimensões previstas; Chromium Linux com viewport simulada 390×844 carrega 5/5 PNG, desenha pixels e aceita mudança de direção. Screenshot anexada. **Limitação:** navegação direta a `localhost` bloqueada por ERR_BLOCKED_BY_ADMINISTRATOR; conteúdo foi injetado com PNG em data URIs por `page.set_content` para testar o renderizador. Não demonstra teste no Android físico, importação no TEST36, regras ou qualidade visual final. O sprite não pretende reproduzir nem licenciar assets de terceiros.

**Valor real do experimento:** prova que o caminho `gerar/obter PNG com licença → atlas versionado → renderizar via Canvas no navegador` não exige PixelLab ou software pago. Isso é somente uma **peça do pipeline**, não substitui design profissional/curadoria artística e não converte o TEST36 em combate pronto.

## Restrições canônicas e rota material

**Últimos marcos recuperados:** PESQ014, RUN013/TEST36 (candidato em Library), gh-pages TEST32 publicado, Codex bridge ainda HOLD até código entregue, D-INOV-032 A+C aprovada, D-INOV-033 proposta. Aplicativo ChatGPT Android é interface principal do Mestre; Tabletop é app web mobile. Não duplicar codex, VLAB, operação de pesquisa, backend, fichas ou arquivos Party.

**Primeira pendência que importa para o Mestre:** transformar uma arena existente em um CICLO DE COMBATE TÁTICO visível e verificável (selecionar unidade/alvo; ação; turno; resultado de motor competente ou fixture TEST sinalizada; atualização da interface e trilha de eventos), numa única base. **Isso pertence ao Desenvolvedor, integrando VLAB e servidor conforme sua autoridade**, não a este laboratório de evidência. Pesquisador deve somente definir/verificar limites de contrato/permissões, não entregar outra aplicação independente.

### Aplicações prioritárias, sem abrir nova OP

1. **P0 (visível e mecânico):** tomar o HUD/diário do 495943 como referência para UMA ação selecionada e recebida na Arena TEST36, com resultado e origem/sinalização de fixture. Aceite: antes não havia ato de combate acionável; depois o Mestre consegue tocar ação e observar resultado, origem e recurso correspondente sem motor paralelo. Ação com mecânica oficial fica HOLD até VLAB competente.
2. **P1 (arte própria e grátis):** manter grid e testar substituição de apresentação de tokens por PNG/atlas CC0/autoral no MESMO tabuleiro; realizar avaliação qualitativa antes de promoção. Não incorporar nosso asset sintético de laboratório como arte final.
3. **P2 (clima posterior):** só após combate e multiplayer reais, acrescentar metadados ambientais visuais do 495933, efeitos mecânicos exclusivamente por VLAB. Não converter clima em minigame autônomo.
4. **NO-REPEAT:** não criar mais um motor, outro jogo genérico/idle ou RPG 3D, não migrar para Godot automaticamente, não exigir PixelLab/Piskel mobile, não publicar asset de vídeo, não usar áudio agora, não tratar contagem de testes como substituta da experiência jogável.

## PSV

- **ANTES:** 5 vídeos sem triagem física; substituição gratuita do pipeline de sprites não demonstrada nesta conversa.
- **DEPOIS:** 5 vídeos catalogados com metadados, hashes e amostras; testes de sprite atlas+Canvas executados em TEST isolado; quadro de alternativas com limites reais; prioridades referidas diretamente à Arena.
- **VERIFICADO:** integridade de vídeos, quadros amostrados, documentação oficial Kenney/Piskel/Godot, 5/5 PNGs e visualização Chromium via `set_content`.
- **INFERIDO/PROPOSTO:** adaptações específicas de UI tática, clima, artes CC0 e eventual interface com VLAB/servidor.
- **HOLD:** narração integral sem ASR; aquisição de pacotes Kenney, licença concreta de cada asset externo, navegador Android físico, presença de CodeX source, interface VLAB mecânica e multiplayer real.
- **LAST-VERIFIED:** lote 5/5 catalogado e teste local de pipeline sem custo.
- **FIRST-PENDING:** autorização/capacidade do Desenvolvedor para vincular primeira ação de combate ao frontend existente e acesso à ABI VLAB homologada, junto da revisão de testes já concluídos; avaliação artística de packs CC0 quando o wire/outbox estiver estabilizado.
- **NEXT:** auditar entrega de nova versão que permita TOCAR uma ação de batalha, não somente protocolar novos testes; preservar referências para materiais de vídeo posteriores.
- **NO-REPEAT:** PESQ012–014, RUN010–013, onboarding Codex, vídeos antigos, áudio rejeitado, não duplicar provas dos cinco vídeos como pesquisa nova.
- **NAC-PASS:** PASS recuperação/custódia e teste de asset pipeline; HOLD integração funcional Android/Party/VLAB.
