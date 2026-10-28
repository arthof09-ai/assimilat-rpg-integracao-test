# Prompt mestre — pesquisa e brainstorm de um NOVO jogo de RPG Assimilação

Copie o conteúdo entre “INÍCIO DO PROMPT” e “FIM DO PROMPT”. Em outra conversa, anexe as cinco imagens de referência nomeadas na seção 5, **os quatro MP4s originais de Dunloc** e, quando possível, a síntese expandida com timestamps fornecida pelo Mestre. Há outras imagens de referência no histórico; preserve-as como material complementar somente quando efetivamente anexadas e identificadas. O prompt deve permanecer executável mesmo se vídeos ou imagens não puderem ser acessados, declarando as lacunas. Os links do Notion dependem do acesso da conta conectada.

**Versão ampliada:** conserva o prompt Codex como base e acrescenta a investigação orientada dos quatro devlogs Dunloc, Canvas 2D procedural, animação articulada/IK, estratégia de produção com IA, desempenho e multiplayer. As inserções mantêm a etapa de pré-produção e não autorizam escrever código do jogo.

## INÍCIO DO PROMPT

Atue como uma equipe de pré-produção de jogos com competências em direção criativa, game design tático, adaptação de RPG de mesa, direção de arte, animação, level design, UX, áudio, engenharia de jogos para navegador e multiplayer. Integre as decisões em uma proposta coerente; não apresente pareceres desconectados de especialistas.

Sua missão é pesquisar, explorar alternativas e produzir um brainstorm profissional, aprofundado e acionável para o campo de batalha digital do meu **RPG Assimilação**. Quero descobrir como este jogo deve funcionar, parecer e ser produzido, preservando a identidade do meu sistema.

**Este é um projeto novo e independente. O caráter visual da tentativa anterior foi insatisfatório e deve ser abandonado. Quero uma nova concepção visual e de experiência; o código anterior e o VLAB podem servir como referências técnicas para criar o código do novo jogo.**

Não trate esta tarefa como reforma visual ou continuação do jogo anterior. Não herde sua aparência, composição de telas, interface, mapas, assets visuais ou direção artística. Capturas e protótipos antigos não são referências estéticas para o novo produto. É permitido consultar o código anterior para compreender soluções técnicas úteis e orientar a criação de código próprio, sem transportar junto a apresentação visual antiga ou sua arquitetura por padrão. Nesta etapa, faça apenas leitura e análise das fontes técnicas acessíveis; preserve os projetos originais.

As bases deste novo projeto são os requisitos expressos neste prompt, as regras e o universo do RPG Assimilação no Notion, as fichas autorizadas, as cinco imagens principais anexadas, os quatro vídeos originais de Dunloc, o resumo expandido desses vídeos e as referências externas indicadas. Manter o mesmo sistema de RPG não implica herdar o jogo anterior. Se encontrar no Notion propostas, telas ou especificações daquela tentativa, não as trate como requisitos atuais. Informações e soluções técnicas úteis podem ser estudadas criticamente, mantendo a nova direção visual e as decisões de produto independentes.

O VLAB tem código e experiências que podem orientar a criação do motor do novo jogo, mas ainda não está 100% pronto. Use-o como referência técnica e mecânica, sem presumir completude, correção integral ou adequação automática ao produto. Não copie simplesmente seu código nem o do jogo anterior. Estude a intenção de cada solução, seus pressupostos, dependências, testes e limitações; então proponha uma implementação adequada ao novo projeto. Decisões históricas de implementação e planos antigos de integração não são requisitos obrigatórios.

Explore soluções novas para identidade visual, composição dos mapas, interface, apresentação do combate e experiência de uso. Justifique as escolhas por sua adequação ao projeto atual, sem organizar o resultado como comparação “antes/depois”. O diagnóstico fornecido é a insatisfação com o caráter visual anterior; não conclua que todo o código é ruim, nem que todo o código funciona corretamente, sem examiná-lo.

**A entrega desta etapa é a pré-produção: pesquisa, conceitos, comparações, recomendações e plano de validação. Não implemente nem publique o jogo agora.** Prepare uma proposta independente para o Codex desenvolver posteriormente. Na futura implementação, planeje uma base de código e um espaço de projeto próprios; não é necessário apagar ou alterar o trabalho anterior.

### 1. Visão e prioridades do produto

Quero um RPG de mesa digital com apresentação de videogame: um campo de batalha tático por turnos no qual o mestre prepara encontros e as jogadoras controlam suas personagens, usando as regras reais do Assimilação.

A experiência combina a liberdade de preparar encontros de uma mesa virtual como Roll20, a clareza e o envolvimento das batalhas de Baldur’s Gate 3 e uma direção visual cuja principal referência é Hades 1 e Hades 2.

O ciclo central precisa permitir: escolher mapa → preparar encontro → colocar personagens, monstros e NPCs → distribuir controle → iniciar combate → mover → escolher ações, habilidades e magias → selecionar alvos → resolver regras → visualizar consequências → acompanhar recursos e condições → encerrar ou salvar a batalha.

Preserve estes requisitos:

- Combate por turnos baseado no meu sistema próprio, com fichas, equipamentos, habilidades, magias, criaturas e transformações integrados.
- Mestre livre para escolher adversários e montar encontros, com controle manual e automação configurável das criaturas.
- Apresentação 2.5D coesa, estilizada, adulta e ilustrada; profundidade, volume, ambientação e leitura tática.
- Pelo menos dez mapas diversos no produto planejado, com continuidade ambiental e identidade própria.
- Jogo de navegador em PC e celular, com interação por mouse e toque considerada desde o planejamento. A ordem de implantação entre dispositivos é uma decisão de produção a propor e validar.
- Multiplayer como requisito estrutural e Supabase como serviço previsto para dados e comunicação, definindo seus limites e as demais responsabilidades.
- Blender e Godot como ferramentas prováveis, sujeitas a uma avaliação fundamentada.
- Campo de batalha como área principal da tela. Fichas, preparação do encontro e ferramentas avançadas devem abrir sob demanda.
- Três ritmos de apresentação: animações completas, apresentação intermediária mais rápida e apresentação instantânea/sem animações ornamentais.

Missões, masmorras, labirintos e exploração controlada são possibilidades futuras. Registre pontos de expansão sem deslocar o foco atual para campanha narrativa, diálogos, mundo aberto ou progressão de roguelike.

Separe os requisitos fixos, as preferências negociáveis e as decisões ainda abertas. Não trate cada exemplo de referência como uma funcionalidade obrigatória.

**Nova prioridade de pesquisa tecnológica (não decisão de engine):** além de Godot/Blender e renderização híbrida, inclua como candidato sério o pipeline de **Canvas 2D com arte desenhada proceduralmente por código e rig/esqueleto matemático**, demonstrado pelo criador de Dunloc segundo os vídeos disponibilizados. Teste sua capacidade de alcançar a linguagem artística escolhida sem converter a preferência do autor por não usar engine em obrigação para nós. **Dunloc é referência técnica/processual prioritária; Hades 1 continua referência artística principal.**

### 2. Método de pesquisa e qualidade das evidências

Pesquise antes de recomendar. Consulte o Notion e as fontes originais do Assimilação; depois use documentação oficial, materiais dos desenvolvedores e gameplay para estudar as referências externas.

Para cada achado relevante, informe fonte, trecho/seção ou timestamp observado, interpretação e consequência prática para este projeto. Diferencie:

1. requisito expresso por mim;
2. regra oficial localizada;
3. capacidade implementada e efetivamente demonstrada;
4. observação de uma referência;
5. proposta de design;
6. hipótese ou lacuna a validar.

Não invente pesquisas, resultados de testes, números, custos, acesso a páginas, análises de vídeos ou validações técnicas. Se uma fonte não abrir, identifique a limitação e continue nas frentes independentes. Data de edição recente, isoladamente, não prova autoridade nem substituição de regra.

**Hierarquia específica de prova audiovisual:** mantenha camadas distintas para (A) descrição expandida/paráfrase fornecida pelo Mestre; (B) alegação verbal atribuída ao criador, com timestamp; (C) cena realmente observada no MP4, com timestamp, aparelho/contexto e comportamento visível; (D) arquivo de código, build, documentação ou infraestrutura realmente inspecionados; e (E) experimento independente. A descrição expandida não é transcrição literal e não equivale, por si, a auditoria do código. Não promova C a D nem D a teste de produção. Ao encontrar contradição entre resumo e vídeo, registre a diferença; não corrija silenciosamente a fonte. Aponte lacunas de legenda: no vídeo 2 há uma ausência aproximada de texto entre 22 e 46 minutos, a ser confrontada com o MP4.

Faça escolhas proporcionais: pesquise o suficiente para sustentar decisões materiais, compare alternativas e explicite o que permanece incerto. Evite uma lista interminável de jogos sem análise e evite transformar o brainstorm em um questionário inicial. Procure no material disponível as respostas antes de me perguntar.

### 3. Investigação do Assimilação, Notion e VLAB

Use estes pontos de partida e siga os links pertinentes:

- [Sistema de Combate](https://app.notion.com/p/3ebc2b324ede81f1be4be8804ac113c0).
- [Criação de Ficha](https://app.notion.com/p/3ebc2b324ede81449222f3c06b840613).
- [Sistema de Transformação Espiritual](https://app.notion.com/p/3f2c2b324ede81c0ae0ee4e66212edc9).
- [Bíblia da Assimilação — Party](https://app.notion.com/p/a109c16dd49582a4a38b81cd3e0872e8).
- [Laboratório Virtual de Combate — VLAB](https://app.notion.com/p/3fbc2b324ede80e0b28cd227967a19ea).
- [Coordenação e integração do VLAB](https://app.notion.com/p/404c2b324ede81bbaf2afb58ebd54acc).

**PA significa Pontos de Alma.** Modele separadamente a economia de ações: Ação Padrão, Movimento, Reação, Ações Livres e Ação Completa, conforme as fontes vigentes. Não transforme PA em pontos de ação nem presuma uma barra adicional de mana.

Investigue Vida, Alma, PA total/livre/comprometido, atributos, classificações, dados, iniciativa, acerto, CA, defesas, reações, dano, críticos, vantagens/desvantagens, condições, deslocamento, magias, equipamentos, Força Física e transformação. Confirme a relação entre os recursos e seus nomes antes de propor barras ou fórmulas.

A transformação deve ser pesquisada como mudança de estado completa: atributos, recursos, reservas temporárias, habilidades, alcance, tamanho, duração, custo e retorno à forma anterior. Preserve as reservas e a ordem de consumo que a regra determinar; não suponha cura ao destransformar nem una reservas distintas por conveniência da interface.

**Limite de arquitetura e governança:** este prompt exige uma proposta de código próprio para o novo produto, mas isso NÃO autoriza iniciar um segundo motor normativo, abrir operação concorrente ou contrariar titularidade do VLAB. Antes de qualquer implementação futura, confronte a opção de resolver combate com serviço/ABI existente, componente reaproveitado, adaptação ou reimplementação independente com a governança vigente e o Mestre. Registre o conflito, a competência para decidir, o critério de paridade de regras e os gates; não presuma autorização para criar autoridade mecânica paralela. Na pré-produção, compare possibilidades sem tocar sistemas existentes.

O VLAB é um laboratório experimental de implementação e testes ainda incompleto. Consulte seu código, casos de referência e evidências pertinentes à compreensão das mecânicas, distinguindo regra oficial, interpretação, capacidade implementada, comportamento efetivamente testado e lacuna. Uma implementação experimental não se torna regra oficial por estar funcionando. Consulte as autoridades mecânicas para resolver o que é canônico.

Defina os requisitos de um motor de combate adequado ao novo jogo a partir das regras confirmadas. Consulte o código anterior e o VLAB como fontes de aprendizado para soluções como turnos, recursos, validação, eventos, cálculos e recuperação, quando houver código pertinente. Para cada solução técnica que influenciar a proposta, registre: origem e versão quando disponíveis; problema resolvido; evidência de funcionamento; lacunas e dependências; princípio aproveitável; adaptação ou reescrita necessária; verificação prevista no novo jogo. Não imponha porte integral, integração obrigatória ou cópia de módulos por conveniência. Qualquer implementação baseada nessas referências precisará ser verificada contra as fontes oficiais e casos de referência rastreáveis; testes antigos são evidência a examinar, não garantia automática da nova implementação.

Produza uma matriz: mecânica → regra/fórmula → fonte e autoridade → evidência disponível → necessidade do novo jogo → lacuna/decisão pendente. Destaque casos como empate de iniciativa, renovação de reações, interrupções simultâneas, duração de efeitos e medidas do tabuleiro quando não houver resposta normativa.

Não preencha lacunas usando D&D, BG3 ou regras comuns de outros RPGs. Proponha alternativas claramente identificadas e mantenha separadas as partes já definidas. Os estudos e futuros protótipos devem usar cópias e estados de partida, sem atualizar fichas oficiais ou resultados de campanha automaticamente.

### 4. Referências: o que estudar e o que adaptar

Estabeleça esta hierarquia:

- **Hades 1:** referência principal de arte e animação; composição, formas, personagens, materiais, pintura, iluminação, poses, ritmo, impacto e feedback audiovisual. Hades 2 permanece como referência complementar, sem substituir o estudo específico do primeiro jogo.
- **League of Legends:** referência principal de jogabilidade na interação com unidades e habilidades, direção de arte e animação; estudar seleção, movimento, alcance, posicionamento, identidade dos kits, silhuetas, orientação, ataques, habilidades, transformações, indicadores e legibilidade de VFX/SFX e equipamentos.
- **Baldur’s Gate 3:** referência principal de jogabilidade tática, organização das mecânicas e construção de mundo/ambientes; estudar decisões de turno, interação com o terreno, verticalidade, preparação de encontros, leitura de consequências e continuidade entre espaço de batalha e mundo.
- **Dunloc Online (nome apresentado na síntese fornecida):** referência prioritária de **metodologia de produção assistida por IA, arte/animação procedural em Canvas 2D e protótipos multiplayer em navegador**, estudada em quatro vídeos originais. O vídeo inicial é [Estou criando um jogo MMORPG inteiro com IA! Veja a evolução | Devlog #001](https://www.youtube.com/watch?v=txHj8LftGL4). O resumo expandido atribui o projeto ao criador Rafael; confirme canais, grafia oficial, data, site, builds e a relação dos quatro MP4s com os devlogs antes de apresentar isso como verificação pública independente. Não substitua esta referência por um homônimo.
- **Enigma do Medo:** integração entre personagens e cenários, iluminação, profundidade, oclusão e ambientação.
- **Threads of Time:** composição 2.5D, integração de camadas, personagens e profundidade de cenário.
- **Roll20:** preparação e operação de encontros, biblioteca, controle de unidades, fichas e permissões. Use como ponto de partida o [guia oficial de preparação da mesa](https://pages.roll20.net/set-up-roll20-virtual-tabletop-as-dm).

Amplie com outras referências apenas quando resolverem um problema concreto. Para cada referência adicional, mostre a contribuição, a adaptação e o custo; não dilua a direção principal.

Não importe o combate em tempo real de Hades/LoL, as regras D&D de BG3 nem a estética pixel art de Enigma/Threads automaticamente. Separe intenção visual, técnica de produção e regra de jogo.

Hades I e II não devem ser presumidos como um mesmo pipeline: há documentação de [personagens pré-renderizados no primeiro](https://steamcommunity.com/app/1145360/discussions/0/1738883810796606862/) e de [personagens 3D em tempo real no segundo](https://www.nintendo.com/us/whatsnew/battle-beyond-the-underworld-in-hades-ii/). Verifique essas diferenças e compare caminhos capazes de produzir a aparência desejada.

Comece também pela [apresentação oficial do combate de BG3](https://baldursgate3.game/about/) e pelos [princípios de clareza publicados pela Riot](https://www.leagueoflegends.com/en-us/news/dev/clarity-in-league/). Para animações, procure gameplay representativo nos canais oficiais; uma página textual não substitui observação de movimento.

Entregue uma matriz de referências com exemplos visuais consultáveis e comentários sobre o que vale absorver, adaptar ou deixar de fora. Preserve identidade original para o Assimilação.

**Estudo aprofundado de League of Legends — jogabilidade, arte e animação.** Analise como o jogo comunica a intenção do jogador e a identidade de cada unidade: selecionar, apontar, mover, reconhecer alcance, atacar, escolher alvo, lançar projétil, usar área de efeito e distinguir habilidades direcionadas de habilidades de área. Estude posicionamento, distância, combinação de habilidades e resposta aos adversários como problemas de decisão. Separe princípios transferíveis para turnos de exigências de reflexo, precisão em tempo real e estrutura de MOBA. Não adote rotas, farm, economia, recargas ou kits de campeão automaticamente como regras do Assimilação.

Selecione uma amostra justificada de pelo menos seis campeões, abrangendo combate leve e pesado corpo a corpo, ataque à distância, conjuração, criatura de anatomia distinta e transformação ou mudança de postura quando houver exemplos acessíveis. Use páginas e vídeos de habilidades para identificar ações e gameplay real para estudar transições. Registre campeão, aparência/skin, versão ou data e fonte observada; mudanças cosméticas podem alterar a amostra. Nomes de campeões são referências de estudo, não personagens a reproduzir.

Para cada perfil, decomponha repouso, início/parada de movimento, mudança de direção, ciclo de ataque, habilidade característica, reação a impacto e morte, conforme o que for observável. Examine pose de antecipação, transferência de peso, trajetória, ponto de contato/disparo, recuperação, movimento secundário de cabelo/tecido/arma, transições e sincronização sonora. Diferencie deslocamento da unidade, movimento do corpo, projétil e efeito visual. Quando houver cancelamento de animação, investigue sua relação com o comando e o instante de efeito; não transfira esse comportamento para uma ação por turnos sem uma decisão explícita de design e compatibilidade com a regra.

Estude também o acabamento visual de personagens e terreno: proporções, silhueta, formas de armas, materiais estilizados, tratamento de valores, cor e contraste na câmera de jogo. Diferencie ilustração promocional, cinemática e asset em partida. A análise deve explicar como obter personagens expressivos e habilidades reconhecíveis sem poluir a batalha.

**Estudo aprofundado de Hades 1 — arte e animação.** Analise separadamente retratos, personagens em combate, criaturas, cenários, objetos e VFX. Observe desenho de formas, anatomia estilizada, planos de luz e sombra, contornos, acabamento de materiais, paletas e composição. Explique como o personagem permanece legível sobre um cenário detalhado e como a unidade parece pertencer ao mesmo espaço. Não reduza o estudo a “arte bonita, escura e isométrica”.

Observe pelo menos três perfis de arma/ação com ritmos distintos e três perfis de inimigo, quando o material acessível permitir. Compare deslocamento, ataque leve/pesado ou equivalente observado, ação à distância, conjuração, impacto e morte. Estude poses principais, arcos de movimento, antecipação, contato, recuperação, trilhas, partículas e som. Verifique recursos como pausas de impacto ou deformações somente quando efetivamente observáveis. Converta os achados em orientações para animação por turnos, sem importar invulnerabilidade, esquiva em tempo real ou regras de Hades. Use o [site oficial de Hades 1](https://www.supergiantgames.com/games/hades/) como ponto de partida para mídia e gameplay.

**Estudo aprofundado de Baldur’s Gate 3 — jogabilidade, mecânicas e construção de mundo.** Examine a sequência de decisões da batalha: preparação, iniciativa, seleção de ator, movimento, custo, alvo, reação, resolução e leitura das consequências. Investigue interações ambientais, superfícies, objetos, desníveis, salto, obstáculos, acessos alternativos e combinação de efeitos, quando sustentados por exemplos observados. Separe a função de design de cada interação da fórmula/regra D&D que a implementa. Para o Assimilação, classifique cada adaptação como regra já existente, apresentação visual ou proposta mecânica pendente.

Estude pelo menos três espaços contrastantes, por exemplo um exterior natural, uma área urbana e um interior ou ambiente subterrâneo. Analise percurso, ponto de vista, marcos reconhecíveis, arquitetura, materiais, vestígios de uso, escala, iluminação, som, profundidade e vistas para áreas além do combate. Explique como o local sugere atividades e acontecimentos e como suas estruturas geram escolhas táticas. Diferencie cenário decorativo de objeto interativo e avalie como o jogador reconhece essa diferença. Investigue a continuidade entre áreas de circulação e locais de encontro para evitar arenas que pareçam tabuleiros isolados no vazio.

“Construção de mundo” aqui significa lugares coerentes, variados, habitáveis e ambientalmente expressivos, com possibilidades de interação. Não exige copiar Forgotten Realms, criar campanha narrativa agora, nem reproduzir o tamanho ou a densidade de produção de BG3. Aplique os princípios aos dez mapas do novo jogo, mantendo o universo do Assimilação.

**Estudo abrangente de Dunloc Online — produto e criação com IA.** Esta é uma grande inspiração pessoal do usuário e deve receber um estudo próprio, com profundidade proporcional às informações disponíveis. Comece pelo vídeo exato indicado: [Devlog #001 — Estou criando um jogo MMORPG inteiro com IA! Veja a evolução](https://www.youtube.com/watch?v=txHj8LftGL4). **Agora existem quatro arquivos MP4 encaminhados pelo Mestre**, relacionados a quatro vídeos de desenvolvimento, e um resumo expandido em paráfrase com recortes temporais. Identifique a origem de cada vídeo, assista aos momentos decisivos e use esses materiais como fontes primárias de audiovisual e como índice de assuntos; não confunda resumo com fala literal nem com verificação de runtime. A grafia e autoria apresentadas na síntese são informações atribuídas a ela até confirmação independente nos créditos e metadados. Não dependa de uma busca pelo nome “Dunloc” para escolher outro jogo.

Analise o que o criador explica e o que efetivamente aparece nas cenas separadamente. Registre timestamps para afirmações, ferramentas e demonstrações observadas. Na descrição, nos links do canal e nos devlogs relacionados, procure o site jogável, documentação, repositório e continuidade do desenvolvimento, quando públicos e acessíveis. O episódio #001 pode mostrar uma etapa inicial; não o trate automaticamente como retrato da versão atual. Se só conseguir metadados ou transcrição, indique essa cobertura: o título não prova funcionalidades, e a transcrição não equivale à inspeção visual de animações ou jogabilidade. Se alguma identificação continuar incerta, registre a pendência e prossiga com as demais referências.

Uma vez identificado, reúna as informações públicas relevantes: site/jogo, páginas do criador, documentação, devlogs, demonstrações, entrevistas, atualizações, gameplay e repositório público quando houver. Distingua versão atual, versões antigas, protótipos e funcionalidades anunciadas. Organize as fontes por tema, evitando repetir alegações de diferentes matérias como se fossem comprovações independentes.

Cubra estas frentes:

1. **Experiência de jogo:** proposta, ciclo central, câmera, controles, movimentação, combate, habilidades, inimigos, equipamentos, feedback, interface e facilidade para começar a jogar. Registre o que realmente está disponível e observado.
2. **Arte e animação:** personagens, cenários, coerência de estilo, integração 2D/3D quando aplicável, escala, luz, materiais, transições, efeitos e áudio. Diferencie assets vistos em gameplay de peças promocionais e de recursos cujo processo de criação não foi documentado.
3. **Mundo e mapas:** composição, profundidade, continuidade ambiental, diversidade, marcos, vida no cenário e interações. Identifique princípios que ajudem nossos dez mapas a parecer lugares de um mundo.
4. **Online e desempenho:** navegador ou instalação, dispositivos suportados, multiplayer efetivamente demonstrado, persistência e reconexão quando documentadas. Não deduza servidor autoritativo, stack, capacidade simultânea, latência ou custo apenas pelo aspecto do jogo ou por um vídeo.
5. **Engenharia e produção:** ferramentas, engine, linguagens, organização do código, geração/importação de assets, animação, hospedagem, backend e processo de atualização, somente na medida em que existam fontes acessíveis. Código público pode ser estudado como referência técnica, com origem e limitações registradas; sua disponibilidade não exige copiá-lo.
6. **Uso de IA:** investigue separadamente assistência em programação, geração de arte, animação, áudio, design, testes e operação, além de eventual IA durante as partidas. O usuário o descreve como feito por IA; registre isso como informação fornecida pelo usuário até encontrar documentação. Diferencie declarações do criador de verificações independentes e não transforme “feito com IA” em “100% autônomo”, “sem trabalho humano” ou “NPCs generativos”.
7. **Método que podemos aprender:** como o criador especificou o projeto, dividiu tarefas, iterou, verificou resultados e corrigiu problemas, quando isso estiver documentado. Prazos ou custos divulgados devem indicar fonte e escopo; não são promessas de que nosso jogo terá o mesmo esforço ou resultado.

**Dossiê obrigatório dos quatro vídeos — escopo, ordem e pontos de checagem.** Os nomes locais dos MP4s são identificadores de anexo, não nomes oficiais da série. A associação abaixo deriva da ordem e das durações verificadas dos arquivos fornecidos; confira título e origem na abertura de cada vídeo. Os tempos de temas derivam da **síntese expandida do Mestre**, devendo ser confrontados com as imagens/falas do material original:

| Fonte recebida | Duração aproximada | Roteiro de verificação no vídeo | Aprendizado a extrair | Risco de leitura equivocada |
|---|---|---|---|---|
| **Vídeo 1 — `498995.mp4`** | **39m25s** | 00:01–04:12 contexto e experiências; 04:13–07:42 objetivos visuais/browser; 12:27–16:49 duas sessões multiplayer e Supabase; 16:50–24:41 falhas de sprites; 24:42–31:14 Godot/Blender; 31:15–38:10 personagens procedurais | Primeiro validar compartilhamento de cena; depois testar estilos e ergonomia. Entender a escolha pelo desenho programático e personalização de armas/armaduras | Aparição de dois personagens não prova servidor autoritativo, segurança ou compatibilidade com muitos clientes |
| **Vídeo 2 — `499005.mp4`** | **1h08m44s** | 00:01–04:01 custos relatados; 04:02–09:59 pipeline e engine; 13:02–21:20 agente, planos, revisão e referência; **22–46 min: lacuna do resumo textual**; 46:29–1:06:44 evolução visual | Método iterativo com checkpoints, agentes especializados, Git, critérios de qualidade e gestão de custos | R$ 1.200 aproximados são relato histórico do autor, NÃO nosso orçamento nem previsão de gasto; duração/token de seus ensaios não prevê esforço do Codex |
| **Vídeo 3 — `499245.mp4`** | **27m57s** | 00:00–02:25 arte por código; 02:26–08:30 escolha Canvas 2D; 08:31–10:27 cabeça e referências; 10:28–17:42 demonstração; 14:35–16:14 IK; 17:43–25:49 primeira versão e refinamento de rosto | Construção de personagem por camadas e rig matemático, movimento multidirecional, animações sem depender de sprites completos, refinamento por elemento | IK não produz estilo artístico automaticamente; resultados relatados de 1h59 e 2h28 são uma experiência específica, não promessas de produtividade |
| **Vídeo 4 — `499255.mp4`** | **25m28s** | 00:00–04:52 ambientes de desenvolvimento/teste/produção; 04:53–09:39 cidade, mapa, transparência da vegetação; 09:40–11:56 desempenho e deploy; 15:37–18:24 inventário/morte; 19:16–21:14 controles/ataque; 21:15–25:22 preparação do beta | Mundo aparentemente contínuo, oclusão de cenário, mapa orgânico, menus e controles; maturidade de publicação e teste de usuário | Recursos planejados para MMORPG (história, nível 10, loot, PvP e mapa de 3 km²) não são requisitos para nossa arena tática |

**Técnicas a investigar com profundidade — não copiadas por presunção:**

1. **Geometria e estilo procedural:** como são construídos rosto, cabelo, olhos, roupa, volume, materiais, contornos, sombra e luz em tamanho real de gameplay; distinção entre arte gerada em tempo de desenvolvimento e desenho recalculado em tempo de execução. Comparar dois ou mais estilos com a **mesma personagem e o mesmo enquadramento**. Uma bela imagem estática não prova animação consistente.
2. **Rig matemático e IK:** quais articulações, limites, transformações e coordenadas são usadas; como pés fixam ao solo, como mãos acompanham arma/cajado, como a camada de armadura evita interseção, como ataque e descanso fazem transição sem deformar rostos, cabelo ou tecidos. Testar ao menos quatro orientações e diagonais, diferentes alturas/tamanhos, espelhamento e mudança de equipamento.
3. **Separação estático/dinâmico:** o que pode ser pré-renderizado e cacheado (terreno, arquitetura, vegetação sem movimento, elementos repetidos); o que precisa de atualização por quadro (personagem, projétil, partículas, sombras móveis); invalidação quando muda clima, luz, câmera, oclusão ou estado. Investigar o custo de pré-renderizar, o uso de memória e a nitidez em zoom diferente.
4. **Sprite versus Canvas versus rig 3D:** comparar custo de autoria e revisão, consistência em direções, reutilização de animações/equipamentos, qualidade de pele/rosto, efeito de profundidade, iluminação, performance e manutenção. A preferência do Rafael por dispensar engine é motivação pessoal, não demonstra inferioridade de Godot/Blender.
5. **Personalização de equipamento:** separar dados de item/efeito, aparência (formas e camadas) e raridade visual. Uma armadura Lendária pode ganhar tratamento visual especial sem inventar bônus, valores ou propriedade em fichas oficiais. Comparar predefinições com geração procedural controlada por dados.
6. **Mapa e oclusão:** mostrar árvores/edificações encobrindo parcialmente unidades, com transparência seletiva e opção de realce somente quando legítimo. A ocultação visual não pode revelar inimigos não percebidos; câmera/renderização são independentes do estado de percepção oficial.
7. **UX e controle:** comparar movimento por clique, cursor/alvo selecionado, aproximação automática e modo livre exibidos nos vídeos, convertendo-os para o paradigma de **intenção confirmada por turno**. Ataque automático permanente no MMORPG não deve consumir ações ou escolher resultados sem autorização/regra.
8. **IA como ferramenta de produção:** mapear pesquisa → plano pequeno → execução por agente → screenshot/teste → crítica objetiva → correção → Git/revert → checkpoint. Exigir um avaliador que compare a imagem real no zoom de jogo com a referência; revisão puramente textual é insuficiente. Auditar custo/benefício de gerações repetidas de rosto e animações.
9. **Online real versus demo:** discriminar contas/sessões distintas, sincronização de posição, autorização por sala, idempotência, reconexão, servidor autoritativo, persistência, testes simultâneos e implantação. Nos vídeos, somente atribua cada capacidade ao que tiver sido demonstrado, relatado ou verificado.
10. **Evolução de produto:** comparar o que o vídeo 1 chama de protótipo com o que o vídeo 4 mostra como beta planejado. Mapear o risco de gastar esforços em MMO, lore, inventário amplo, comércio, loot, tutorial de progressão, social e mapa enorme, todos fora do núcleo atual do Assimilação.

**Entregas próprias do estudo Dunloc:**

- Índice temático de quatro vídeos, com *timestamp real conferido* e quadro/cena representativa quando o vídeo for acessível; não alegar inspeção integral se apenas trechos forem vistos.
- Cinco ou mais decisões extraídas do **processo de desenvolvimento** e cinco ou mais princípios extraídos do **resultado visual/interativo**, todos com origem e limite.
- Quadro de defeitos/tentativas abandonadas (sprites inconsistentes, material 3D não convincente, transição corporal, custo de tokens, gargalo de renderização) e maneiras de evitá-los com teste controlado e critérios de parada.
- Uma análise original de transferência para **arena de combate por turnos com duas players e Mestre**, removendo serviços de MMO que não trazem valor.
- Comparação das alternativas gráficas com experimento mínimo de mesmo personagem/mesmo mapa/mesma ação, a planejar, não executar agora.

Entregue uma ficha de identificação e fontes, uma análise dos pontos fortes e limites observáveis e uma matriz: achado → evidência → princípio útil → aplicação ao Assimilação → dependência/custo → validação. Destaque o que inspira a experiência final e o que inspira nosso processo de criação com o Codex. Recomende ações concretas para o novo jogo sem substituir a direção artística de Hades 1/LoL, as referências táticas de BG3 ou as regras próprias por características de Dunloc Online automaticamente. “Toda informação” significa cobertura ampla das dimensões relevantes e das fontes acessíveis, com lacunas explícitas, sem alegar exaustividade absoluta.

**Síntese obrigatória dos estudos.** Para cada achado relevante, entregue: fonte e evidência observada → princípio identificado → contribuição para o novo jogo → exemplo concreto de aplicação → custo/limite → regra do Assimilação envolvida → teste ou validação necessária. Inclua uma situação de combate original mostrando a interação entre a apresentação de ações inspirada em LoL, a direção de arte/animação inspirada em Hades 1 e a organização espacial/tática inspirada em BG3. Integre os aprendizados comprovados de Dunloc Online onde forem pertinentes, inclusive no plano de produção com IA. Isso é uma proposta original, não prova de implementação.

Esses estudos são parte central do brainstorm. Se o ambiente não permitir assistir ou inspecionar vídeos, avance com as evidências disponíveis e marque a análise temporal como pendente; não preencha a matriz com timestamps inventados ou afirme ter realizado análise quadro a quadro.

### 5. Direção artística e análise das imagens anexadas

Analise individualmente as cinco imagens, pelo nome do arquivo:

- **499007.jpg:** referência de ambiente com câmera elevada, caminhos, arquitetura, vegetação, água e iluminação em tons frios; considere somente a área do jogo, desconsiderando navegador e sobreposições.
- **498980.jpg:** terreno com caminhos, vegetação, rochas, água e desníveis; estudar organização espacial, materiais e continuidade do ambiente.
- **498977.jpg:** ambiente de batalha com arquitetura, estátua, diferenças de altura e iluminação; estudar composição e hierarquia entre unidades e cenário.
- **462746.jpg:** referência de personagem com cabelo escuro, tecidos claros, armadura e ornamentos dourados, com silhueta e presença marcantes.
- **462806.jpg:** referência de personagem com vestimenta longa e ornamentada e um cajado de leitura característica.

As duas últimas imagens são inspirações de personagem. Não deduza nomes, identidade, classe, poderes, valores de ficha ou qual jogadora representam apenas pela aparência. Confronte detalhes com as fichas disponíveis e mantenha as correspondências não confirmadas em aberto.

Traduza o pedido de “cartoon estilizado adulto, desenhado e com certo realismo” em decisões observáveis: anatomia e proporção, formas principais/secundárias, linha e contorno, pincelada, textura, materiais, paletas, valores, luz e simplificação para o zoom de jogo.

Explique como adaptar o detalhamento das ilustrações para personagens legíveis no campo: cabelo, capa, arma, ornamentos e postura devem continuar reconhecíveis em tamanho reduzido. Diferencie retrato de ficha, concept art e asset jogável.

Defina como harmonizar personagens e ambiente por escala, perspectiva, direção de luz, sombra de contato, tratamento de bordas e saturação. A integração deve preservar o contraste necessário para selecionar unidades e entender ações.

O universo é amplo: proponha exemplos diurnos, abertos, luminosos e coloridos, além de locais sombrios. A referência Hades não obriga mitologia grega, submundo ou interiores escuros.

### 6. Câmera e soluções para o 2.5D

Compare, no mínimo:

1. ambientes pintados em 2D com personagens em sprites, inclusive pré-renderizados;
2. cenários 3D estilizados com personagens 2D e retratos ilustrados;
3. cenários e personagens 3D com acabamento ilustrado e interface/retratos 2D.

Avalie câmera fixa/isométrica/ortográfica, liberdade de rotação, altura, oclusão, seleção, sombras, iluminação, equipamentos intercambiáveis, direções de animação, memória, download, custo de produção e desempenho no navegador.

**Quarta abordagem de produção a considerar:** Canvas 2D procedural, com rig matemático/IK e cenários em camadas cacheadas. Pode estar associado à opção 1, mas deve ter avaliação técnica **separada**, pois desenhar a cada frame é diferente de reproduzir sprites pré-renderizados. Acrescente ao quadro: (a) 4–8 direções de leitura, (b) tamanho real dos personagens quando o mapa inteiro é mostrado, (c) personagem atrás de obstáculos, (d) impacto de zoom e densidade de NPCs, (e) performance em smartphone, (f) estratégia de fallback para dispositivos fracos e (g) horas humanas/de IA de refinamento artístico. Não imponha rotação livre se o pipeline escolhido for orientado a ângulos finitos.

Mostre as consequências da câmera sobre os assets: um personagem feito para poucos ângulos não adquire rotação livre sem trabalho adicional. Recomende uma solução inicial e uma alternativa de contingência, com critérios de validação. Não escolha tecnologia apenas pelo rótulo “2.5D”.

### 7. Design do combate e experiência das jogadoras

Descreva uma rodada completa pela experiência de uso: reconhecer de quem é o turno → selecionar unidade → examinar movimento → escolher ação → entender custo e legalidade → selecionar alvo/área → abrir reação quando cabível → resolver → apresentar efeitos → atualizar estado e log.

Investigue grid quadrado, hexagonal ou movimentação livre com medição. Faça a recomendação respeitar as unidades e adjacências oficiais; uma grade discreta/oculta pode preservar a aparência de mundo. Não substitua a regra espacial para combinar com uma imagem.

Explore caminho previsto, alcance, linha de visão, obstáculos, cobertura, alturas, salto, voo, áreas de efeito e terreno. Indique o que já existe no sistema, o que é somente visual e o que exigiria regra nova. Uma escada ou pedra decorativa não pode prometer interação que o motor não oferece.

Planeje seleção clara, cancelamento antes da confirmação, aviso de alvo inválido, explicação de custos e feedback de erro. Não exiba chances, danos previstos ou modificadores sem base no cálculo e nas informações disponíveis àquela pessoa.

Descreva as janelas de reação: quem decide, quando recebe a informação, como a partida aguarda a escolha e como uma política de tempo limite poderia ser configurada. Não invente prioridade ou resposta automática para lacunas normativas.

### 8. Mestre, fichas e ferramentas de desenvolvimento

O mapa deve dominar a tela. Proponha uma HUD com informação necessária ao momento: turno, unidade selecionada, recursos pertinentes, ações e condições. Detalhes ficam em painéis acessíveis por botão, seleção ou atalho.

Separe três contextos:

- **Jogadoras:** suas unidades, fichas, ações, inventário relevante e informações permitidas.
- **Mestre:** escolha de mapa, biblioteca de criaturas/NPCs, colocação e remoção de unidades, equipes, controle, preparação de encontros e gestão da partida.
- **Desenvolvimento:** inspeção técnica, depuração, conteúdo experimental e diagnóstico, acessível por botão e protegido por permissões reais.

Um botão escondido não é uma política de acesso. Defina o que cada papel pode ler e alterar, inclusive informações secretas de criaturas. Use a conveniência de uma mesa virtual mantendo a experiência principal centrada na batalha.

Proponha wireframes descritivos para PC e celular: seleção por toque, zoom, deslocamento da câmera, confirmação, painéis e prevenção de gestos ambíguos. Celular pode ter implantação posterior, mas não deve exigir refazer toda a interação.

### 9. Animação, VFX, áudio e três ritmos de combate

Estude uma amostra representativa de gameplay real. Para cada exemplo efetivamente observado, registre jogo, URL, intervalo, ação, antecipação, contato/disparo, recuperação, orientação, deslocamento, VFX, som e aplicação proposta. Só informe frames ou duração se medidos. Liste o que não foi possível observar; não alegue ter estudado todas as animações com base em trailers ou imagens estáticas.

**Aporte de Dunloc ao sistema de animação:** proponha uma biblioteca de poses e articulações reusáveis, com hierarquia corpo → membros → mãos/pés → equipamento → ornamentos, sem pressupor que Canvas procedural será vencedor. Documente contraexemplos de IK: pés deslizando, braços que atravessam torso, espada sem peso, expressões faciais mudando ao virar, capas e armaduras sobrepondo o corpo e efeitos que apagam a silhueta. Priorize consistência do personagem em todas as direções sobre polimento de uma pose única; planeje validação com sequências curtas repetidas, reversão, troca de arma e comparação com as imagens de referência.

Consolide aqui os estudos específicos de League of Legends e Hades 1 da seção 4. Entregue fichas de animação para o novo jogo com poses principais, transições, evento mecânico representado, VFX/SFX, variantes por equipamento/corpo, prioridade de produção e comportamento nos modos Completo, Dinâmico e Instantâneo. O instante visual de contato representa um evento resolvido pelo motor; não deve determinar sozinho dano, consumo de recurso ou oportunidade de reação.

Monte uma matriz de estados: repouso, deslocamento, parada, mudança de direção, ataque, conjuração, habilidade, projétil, dano recebido, defesa/esquiva, salto, morte e transformação, conforme aplicabilidade às criaturas e regras. Inclua identificação de ações por equipamento e reaproveitamento entre criaturas sem apagar suas personalidades.

Planeje sons de passos e superfícies, armas, impactos, conjuração, habilidades, criaturas, transformação, morte e ambiência. Ofereça controles de volume e redução de efeitos intensos.

Defina três modos:

- **Completo:** apresentação integral, movimento, ataques, impactos, efeitos e sons.
- **Dinâmico:** durações e transições reduzidas, mantendo os momentos necessários à leitura.
- **Instantâneo:** atualização direta do resultado com feedback essencial e log; sem espera ornamental.

Todos devem representar a mesma sequência mecânica, com os mesmos recursos, rolagens, reações e resultado. Desligar animação não pula decisão nem altera regra. Em multiplayer, separe o relógio lógico da partida das preferências locais de apresentação e explique como impedir dessincronização e filas excessivas de animação.

### 10. Dez mapas distintos e integrados ao mundo

Apresente pelo menos dez conceitos de mapa, suficientemente diferentes em composição, materiais, iluminação e possibilidades táticas. O planejamento completo deve manter os dez; a primeira validação pode produzir uma arena representativa antes das demais.

Use como sementes, adaptando ao universo comprovado ou rotulando como propostas: floresta monumental, cidade/porto, montanhas e pontes, ruínas em deserto, região nevada, mangue ou pântano, cavernas luminosas, fortaleza ou pátio cerimonial, cidade em árvore e domínio espiritual. Não declare esses lugares parte oficial do lore sem fonte.

Para cada mapa, entregue: nome provisório; conceito; vínculo com o mundo; paleta e luz; escala; ponto de interesse; caminhos e zonas táticas; relevos e oclusores; oportunidades de encontro; som/vida ambiental; cenário além da área jogável; regras necessárias; dificuldade e reaproveitamento de assets.

Aplique explicitamente o estudo de construção de ambientes de BG3: para cada mapa, descreva o que torna o lugar parte de um mundo, quais detalhes sugerem seu uso/história, quais escolhas espaciais enriquecem o encontro e como a área continua visualmente além do campo de batalha. Preserve a linguagem artística escolhida a partir de Hades 1 e LoL, sem importar automaticamente o acabamento visual de BG3.

“Sem bordas ou limbo” significa continuidade visual além do espaço de combate: paisagem, arquitetura, vegetação, profundidade, parallax ou extensão de cenário conforme o pipeline. A área jogável pode ser limitada por elementos naturais e legíveis. Não é uma exigência de mundo infinito nem de céu visível em toda câmera.

Os mapas precisam parecer lugares habitáveis de um mundo, com história ambiental, transições de materiais e elementos vivos. Avalie onde a decoração poderia prejudicar seleção, visibilidade e percepção do terreno.

### 11. Inteligência artificial tática

Proponha controle manual, sugestões ao mestre e controle automático por criatura ou grupo. O mestre deve poder intervir entre decisões, e a IA deve usar o mesmo conjunto de comandos legais das demais unidades.

Compare regras de comportamento, árvores de comportamento, utility AI e busca limitada. Explique qual combinação inicial oferece decisões boas, custo previsível e facilidade de depuração. “IA experiente” é um objetivo de qualidade; não afirme que será treinada por machine learning sem dados, método, orçamento e avaliação.

Considere objetivos, alcance, posicionamento, ameaças, recursos, reações, sinergias e comportamento de espécie. Criaturas diferentes precisam ter maneiras de lutar diferentes; uma besta e um conjurador não devem se tornar o mesmo otimizador com aparências diferentes.

Defina acesso à informação: sem conhecimento de fichas secretas, posições não percebidas ou resultados futuros de rolagem, salvo capacidade específica. Dificuldade pode mudar planejamento e tolerância a risco sem adulterar fórmulas silenciosamente.

Proponha avaliação com cenários de referência: legalidade das ações, objetivos cumpridos, uso de recursos, tempo de decisão, coerência e situações de impasse. Não use apenas taxa de vitória como prova de inteligência.

### 12. Navegador, Godot, Blender e arquitetura do novo jogo

Trate “rodar em HTML” como acesso por página web. Compare a exportação web do Godot com uma alternativa web nativa proporcional ao projeto, sem iniciar dois projetos paralelos.

**Agora compare explicitamente quatro famílias de pipeline, sem declarar vencedora antes de pesquisa e prova:** (1) Canvas 2D vetorial/procedural + esqueleto/IK + cache; (2) arte pintada/pré-renderizada + sprites animados em renderizador web; (3) Godot 4 + Blender com renderização ilustrada, exportando para Web; (4) híbrido web com Canvas/WebGL e recursos 2D/3D gerados offline. Diferencie o custo de produzir *arte desejada* do custo de apenas desenhar quadros. Teste conceitualmente a mesma cena: protagonista detalhada, monstro grande, floresta diurna, ataque com VFX e câmera de três quartos. Compare quatro ângulos, três ritmos de animação e presença de múltiplas unidades. Avalie ainda acessibilidade de depuração, proteção de segredos no código servido e interoperabilidade com a autoridade mecânica. A direção visual aprovada pelo Mestre deverá determinar o pipeline, não o contrário.

Verifique na versão escolhida do Godot: linguagem exportável, WebAssembly/WebGL, renderizador, suporte a threads, exigências da hospedagem, áudio, entrada, memória, download e limitações de Safari/iOS/Android. Use a [documentação oficial de exportação web](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html). Não prometa que um projeto nativo funcionará no browser sem adaptações.

**Documentação de desempenho Canvas (exigir verificação na versão aplicável):** comece pelas recomendações da [MDN sobre otimização Canvas](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Optimizing_canvas), como pré-render de objetos repetidos, camadas estáticas, evitar redesenho desnecessário e animação sincronizada por `requestAnimationFrame`. Avalie se o navegador suporta as APIs escolhidas; `OffscreenCanvas`, workers e cache não devem ser presumidos como solução mágica para partículas, sombras, ordenação isométrica ou desenhos complexos. Inclua critérios para **não usar** desenho procedural em peças específicas, escolhendo sprites/3D quando fizerem melhor trabalho.

Para Blender, descreva o caminho de autoria, rig, animação, materiais, exportação/importação e otimização. Compare assets 3D com renderização para sprites quando pertinente. As ferramentas de autoria não devem virar instalação exigida do jogador.

Proponha uma arquitetura própria para o novo jogo, com separação entre conteúdo/regras versionados, motor de combate, autoridade multiplayer, apresentação audiovisual e ferramentas do mestre. Compare onde cada responsabilidade deve ser executada e como comandos, eventos e estados devem circular. As soluções do código anterior e do VLAB podem orientar esse desenho quando forem úteis e compreendidas, sem impor dependência do executor Python existente ou transplantar a arquitetura antiga. Separe lógica de regras e apresentação para que uma referência técnica não determine a nova estética.

Defina interfaces conceituais, formatos e responsabilidades; não escreva agora uma base de código extensa. Se faltarem definições de regra ou provas de viabilidade, trate isso como dependência verificável e mantenha o design visual e de interface avançando.

### 13. Supabase, multiplayer e persistência

Defina o papel de Supabase Auth, Postgres, Storage e Realtime e o componente responsável por validar e resolver as ações. Consulte a [documentação Realtime](https://supabase.com/docs/guides/realtime) e as [políticas de acesso/RLS](https://supabase.com/docs/guides/database/postgres/row-level-security). Não confunda atualização de banco ou Broadcast com um árbitro de combate pronto.

Descreva o fluxo: cliente envia intenção → autoridade confere jogador, unidade, turno, reação, alvo e recursos → executor resolve → estado/evento é persistido de forma consistente → participantes recebem o resultado → clientes o apresentam.

**Aprendizado delimitado do Dunloc:** o resumo do vídeo 1 relata um teste em dois navegadores no qual os personagens veem o movimento um do outro com servidor e Supabase/PostgreSQL. Isso comprova apenas o objetivo **descrito** do protótipo inicial; para o Assimilação, planeje teste próprio de Mestre + duas jogadoras em sessões independentes, ação concorrente e reconexão. Diferencie posição visual em tempo real da ação tática por turnos; nossas intenções devem ser autorizadas e serializadas pela autoridade antes de broadcast. Supabase é infraestrutura de dados/comunicação, não substituto automático de servidor de decisões. Na [autorização Realtime](https://supabase.com/docs/guides/realtime/authorization), canais privados dependem de RLS e associação de papéis; além disso, examine a atualização de acesso durante conexões duradouras e a revogação de participantes. Não infira segurança por exibir login na tela.

Planeje salas privadas, convite, papéis, propriedade de unidades, visibilidade de fichas, reconexão, salvamento, saída do mestre e recuperação. Compare quem pode exercer autoridade e os riscos de depender do navegador do anfitrião.

Inclua identificador de comando, prevenção de duplicação, versão de estado e ordem de eventos. Reconexão deve recuperar o estado canônico e reconciliar eventos; mensagens visuais recebidas não bastam como única fonte de verdade.

Explique permissões/RLS e autorização dos canais privados; segredos de serviço ficam fora do cliente. Compare opções para o backend próprio do novo jogo, incluindo serviço de aplicação e funções/RPCs quando adequadas, respeitando as necessidades do motor e os limites atuais dos serviços. Não prometa IA pesada e permanente dentro de uma função curta.

Proponha um modelo conceitual para usuários, salas, participantes, atores, snapshots de ficha, conteúdo, mapas, encontros, comandos, eventos e estado da partida. Diferencie conteúdo-base, versão de regra e estado transitório de batalha.

### 14. Alternativas criativas e recomendação

Apresente três direções originais para o novo produto, variando escolhas reais: composição de câmera, integração 2D/3D, profundidade de interação e custo de produção. Todas devem preservar turnos, regras próprias, multiplayer e preparação de encontros. Desenvolva-as a partir deste briefing e da pesquisa atual, sem adaptar propostas do jogo anterior.

Para cada direção, descreva como seria uma partida, vantagens, concessões, risco principal e prova necessária. Recomende uma combinação final fundamentada. Evite uma colagem em que cada referência manda em uma parte incompatível com as demais.

Inclua ideias ousadas opcionais, associadas ao ganho para a experiência, à regra necessária e ao custo. Classifique as sugestões em núcleo inicial, evolução posterior e experimental.

### 15. Escopo, produção e validação

Proponha etapas com entregas verificáveis: pesquisa e inventário de regras; concepção independente e arquitetura do novo jogo; especificação do motor e seus contratos; protótipo funcional próprio; arena representativa com arte e animação; multiplayer real; biblioteca e automação; expansão até os dez mapas. Não use migração ou reforma do jogo anterior como marco de produção.

Multiplayer deve ser considerado desde a arquitetura e testado cedo, ainda que a primeira interação local seja pequena. A expansão visual não pode esconder uma batalha que só funciona em uma aba ou com resultados simulados.

Defina o menor encontro capaz de validar as decisões centrais com fichas/fixtures rastreáveis: movimento, ataque, dano, recursos, reação, condição, magia e transformação conforme as regras confirmadas e o escopo proposto para o novo motor. Lacunas de regra devem ficar identificadas, sem inventar certificação de compatibilidade completa.

Inclua critérios de aceite: resultados coerentes com as fontes; igualdade do estado entre clientes; comando duplicado sem efeito duplo; reconexão; permissões; leitura no zoom de jogo; equivalência entre os três modos de animação; desempenho nos aparelhos-alvo; mapas com continuidade visual.

**Controle de custo/experimento:** o resumo fornecido atribui ao criador gasto aproximado de **R$ 1.200 em três meses** de testes, incluindo uso compartilhado de assinatura Claude e ferramentas artísticas. Trate-o como **relato com atribuição, de escopo diferente do nosso**. Nosso teto desejado de gasto adicional é R$ 0; proponha abordagem local/gratuita e explicite limites de contas, armazenamento, tráfego, funções, filas de render, IA, hospedagem e licenças. Evite políticas de “tentar gerar até ficar bonito” sem orçamento e teto de iterações. Produza um plano de *experimentos com critérios de falha e reversão* antes de recomendar um pipeline caro.

Estime esforço por disciplina e dependências, em intervalos condicionados à equipe e ao pipeline. Proponha orçamentos de assets e performance como hipóteses a medir; não apresente números arbitrários ou prazos como compromissos.

### 16. Formato obrigatório da resposta

Entregue, nesta ordem:

1. **Síntese do novo conceito:** experiência desejada, pilares, independência da tentativa anterior e limites desta etapa.
2. **Preferências e decisões:** requisitos fixos, escolhas abertas e hipóteses.
3. **Pesquisa do sistema e referências técnicas:** fontes consultadas, matriz de regras, código pertinente do jogo anterior e do VLAB efetivamente examinado, princípios úteis, limitações e plano de adaptação/validação para código próprio. Não herdar o caráter visual antigo nem apresentar código não consultado como analisado.
4. **Estudo aprofundado das referências e anexos:** LoL em jogabilidade/arte/animação; Hades 1 em arte/animação; BG3 em jogabilidade/mecânicas/construção de mundo; **Dunloc Online com análise específica dos quatro MP4s**, de sua arte procedural/Canvas 2D, rig/IK, cache, multiplayer, evolução do produto e processo de criação com IA. Confirmar títulos, origem e cenas; distinguir a síntese do Mestre da observação audiovisual e do código efetivamente auditado. Incluir matriz timestamp → técnica → evidência → transferência → teste.
5. **Três direções de produto:** comparação e recomendação.
6. **Direção artística:** linguagem visual, câmera, pipeline e critérios de coesão.
7. **Experiência de combate:** ciclo, interações, reações, fichas, mestre e wireframes.
8. **Animações, VFX e áudio:** matriz de estados e três ritmos de apresentação.
9. **Catálogo dos dez mapas:** fichas completas e matriz comparativa.
10. **IA tática:** arquitetura proposta, comportamentos e avaliação.
11. **Viabilidade técnica:** arquitetura própria, navegador, **Canvas 2D procedural/IK/cache versus sprites, Godot/Blender e híbrido WebGL**, governança do novo motor, Supabase e multiplayer; demonstrar uma escolha fundamentada com contingência e critérios de falsificação.
12. **Plano para o Codex:** marcos, dependências, riscos, critérios de aceite e próximo pacote de implementação.

Use tabelas para comparações e exemplos concretos para explicar como seria jogar. Dê profundidade proporcional aos problemas; não substitua decisões por adjetivos como “imersivo”, “fluido” ou “profissional”.

Finalize com recomendações priorizadas e somente as perguntas que ainda mudem uma decisão importante ou bloqueiem uma etapa. Continue o trabalho independente enquanto uma resposta estiver pendente. Ao terminar, deve ser possível revisar uma proposta concreta e preparar a implementação seguinte, sem confundir ideias novas com regras já oficiais.

## FIM DO PROMPT

## Notas da pesquisa que embasou este prompt

Consulta original em 25/10/2026; **ampliação com os quatro vídeos recebidos e com pesquisa técnica específica de Canvas e multiplayer**. Prompt revisado conforme a orientação do usuário: criar um jogo novo com direção visual independente, permitindo consultar o código anterior e o VLAB como referências técnicas para criar código próprio. O VLAB é incompleto; não há exigência de cópia ou integração automática de seu executor. Esta revisão do prompt não constitui auditoria dos códigos antigos. Foram consultadas páginas do Notion, documentação técnica e materiais oficiais/de produção. As imagens anexadas permitem análise visual estática. Não foi realizada análise quadro a quadro dos vídeos; o prompt pede esse estudo na execução do brainstorm, com evidências observadas.

- **Regras e laboratório:** o [Sistema de Combate](https://app.notion.com/p/3ebc2b324ede81f1be4be8804ac113c0) documenta uma economia de ações própria. A [Criação de Ficha](https://app.notion.com/p/3ebc2b324ede81449222f3c06b840613) distingue PA — Pontos de Alma — e suas reservas. O [VLAB](https://app.notion.com/p/3fbc2b324ede80e0b28cd227967a19ea) se apresenta como ambiente experimental; não é, por si, fonte canônica de regras.
- **Hades:** um [desenvolvedor de Hades I](https://steamcommunity.com/app/1145360/discussions/0/1738883810796606862/) descreve personagens animados em 3D e convertidos para frames, com a maior parte dos ambientes pintada em 2D. A [comunicação oficial de Hades II na Nintendo](https://www.nintendo.com/us/whatsnew/battle-beyond-the-underworld-in-hades-ii/) descreve ambientes pintados e personagens 3D em tempo real. A comparação dos pipelines no prompt decorre dessa diferença.
- **Combate e clareza:** a [página oficial de BG3](https://baldursgate3.game/about/) descreve combate por turnos baseado em D&D 5e e interações ambientais. A [Riot explica a clareza de LoL](https://www.leagueoflegends.com/en-us/news/dev/clarity-in-league/) por comunicação do jogo, hierarquia visual, redução de ruído e silhuetas reconhecíveis. São referências de experiência e apresentação; não definem regras do Assimilação.
- **Referências auxiliares:** o [press kit de Enigma do Medo](https://sites.google.com/dumativa.com.br/enigmaoffear/pt-br) descreve pixel art integrada a ambientes 3D e iluminação dinâmica. O [site oficial de Threads of Time](https://threadsoftimegame.com/) apresenta sua direção 2.5D. O prompt usa essas referências sem impor pixel art.
- **Browser:** a [documentação de exportação web do Godot](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html) explica WebAssembly/WebGL 2, Compatibility e limitações de exportação. A [documentação de importação 3D](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html) orienta a integração com Blender/glTF. A versão escolhida deve ser verificada antes da implementação.
- **Multiplayer:** [Realtime](https://supabase.com/docs/guides/realtime), [RLS](https://supabase.com/docs/guides/database/postgres/row-level-security) e [autorização Realtime](https://supabase.com/docs/guides/realtime/authorization) documentam comunicação e acesso. A resolução autoritativa de comandos é uma recomendação de arquitetura para este projeto, não uma funcionalidade de RPG pronta no Supabase.
- **Mesa virtual:** o [guia oficial do Roll20](https://pages.roll20.net/set-up-roll20-virtual-tabletop-as-dm) documenta a preparação de mapas, tokens vinculados a fichas e acompanhamento dos turnos. Essas funções embasam a referência operacional do mestre.


### Adendo de pesquisa e custódia — quatro devlogs (25/10/2026)

- **Fontes privadas fornecidas pelo Mestre:** `498995.mp4` (39m25s), `499005.mp4` (1h08m44s), `499245.mp4` (27m57s), `499255.mp4` (25m28s). Durações confirmadas por leitura de metadados locais (`ffprobe`). Foram examinados alguns fotogramas amostrais: o primeiro mostra ferramenta de sprite e arena/cidade isométrica; o segundo, prompts e mundo verde no navegador; o terceiro, telas de desenvolvimento e referências de pose; o quarto, campo arborizado e mapa da região. **Amostras não equivalem à visualização integral** nem verificam áudio ou código-fonte.
- **Resumo expandido entregue pelo Mestre:** índice em paráfrase de quatro episódios com timestamps aproximados; serve para localizar os capítulos, mas não é transcrição verbatim. Há uma lacuna textual no episódio 2, cerca de 22–46 min. As observações técnicas narradas devem ser comparadas diretamente às cenas/falas quando a pré-produção for executada.
- **Hipótese técnica central surgida dos vídeos:** Canvas 2D com gráficos procedurais, esqueleto matemático, IK e separação de renderizações estáticas/dinâmicas. É candidato para testes comparativos, **não decisão aprovada de renderizador**.
- **Canvas:** [MDN — Optimizing Canvas](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Optimizing_canvas), que documenta camadas, pré-renderização e redução de custo por quadro.
- **Exportação web:** [Godot — Exporting for the Web](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html), cuja compatibilidade exige atenção a WebAssembly, WebGL 2, renderizador Compatibility e limites de aparelhos móveis.
- **Multiplayer e segurança:** [Supabase Realtime Authorization](https://supabase.com/docs/guides/realtime/authorization) e [Realtime Limits](https://supabase.com/docs/guides/realtime/limits), para desenho de salas autorizadas e avaliação objetiva do plano gratuito; dados e mensagens de terceiros exigem segregação por papéis e RLS.
- **Custos mencionados nos vídeos:** aproximadamente R$ 1.200 em experimento histórico do autor, segundo resumo do Mestre; não foram auditadas cobranças e **não representam custo necessário ou orçamento aprovado do Assimilação**.
- **Preservação do original:** esta revisão só amplia o prompt de pré-produção. Não houve edição do Notion, GitHub, VLAB ou jogo anterior; nenhuma API/jogo foi implementada nesta rodada.
