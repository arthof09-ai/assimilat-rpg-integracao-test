# PESQUISA INOVADOR — VÍDEO 496132

**Projeto:** RPG Assimilação / Tabletop Assimilação  
**Data da análise:** 24/10/2026  
**Função:** Coordenação Inovador, MESTRE-SIDE  
**Objeto:** método de produção de personagens em múltiplas vistas e folhas de sprites, com apoio de IA e demonstração de Blender  
**Duração examinada:** 05:01,81  
**Arquivo:** `496132.mp4`, H.264, 640×360 a 30 fps, áudio AAC, 10.974.515 bytes  
**SHA-256:** `1c0b4e4332b4bc961137a62979474052a0a63be4002f7daa0bb33e600c3f29c4`  
**Evidência:** 24 quadros amostrados ao longo do arquivo + 16 quadros para inspeção ampliada, folhas de contato e teste próprio reproduzível.  
**Estado da narração:** áudio existe, mas não há faixa textual de legendas. Não foi feita transcrição confiável das falas; textos visíveis na tela não equivalem a narração completa.

## 1. Parecer executivo

O vídeo é **relevante para a produção visual do Tabletop**, não para as regras de combate. A principal contribuição é a demonstração de um processo iterativo para manter um personagem reconhecível em vistas distintas e convertê-lo em quadros organizados de animação. Aparecem ferramentas de geração e revisão de imagens, uma interface do Blender e conjuntos de quadros de personagens. Contudo, o vídeo sozinho **não comprova** que as vistas tenham sido criadas automaticamente do mesmo modelo 3D ou que o material final seja compatível com nosso código sem transformação.

Nossa aplicação prática recomendada é **um contrato único de sprite sheet** para tokens, NPCs e bestas: tamanho de quadro, direções, quadros por animação, origem do pé, transparência, identidade visual, proveniência e licença. O contrato fica na camada de **apresentação**, separado do VLAB. A animação não escolhe ataques, não altera iniciativa nem modifica Vida, Alma, PA, defesa ou dano.

Foi construída uma ferramenta offline — `OFICINA_SPRITES_ASSIMILACAO_TEST_ANDROID_OFFLINE.html` — e uma folha PNG autoral sintética 4×4. O verificador abre o atlas, anima os quadros, mede problemas estruturais e exporta JSON. Em Chromium Linux: **45/45 verificações aprovadas em três viewports de celular**. Não houve integração ao TEST 36 nem teste em aparelho Android físico.

## 2. Evidência cronológica do vídeo

**00:00–00:39 — problema de consistência entre quadros.** Uma ferramenta em tema escuro exibe texto instrucional em inglês e exemplos de personagem em folhas horizontais; a apresentação compara quadros, ângulos e movimentos. O conteúdo visual sugere que o criador está especificando perspectivas e estados para uma mesma figura. Sem ler todo o texto em alta resolução, não é possível recuperar uma especificação completa nem afirmar qual modelo de IA forneceu cada imagem.

**00:40–01:42 — geração e revisão de variantes.** Aparecem imagens organizadas em conjuntos, incluindo um personagem estilizado em múltiplas vistas. O criador volta entre instruções e saídas, inspecionando resultados. O ponto transferível é iterar sobre **um personagem-base com restrições de identidade** — não gerar um rosto e uma roupa diferentes para cada direção.

**01:43–02:25 — ajuste da estrutura da folha.** A interface mostra strips e arranjos de personagens em diferentes orientações e poses. Problemas típicos a verificar no nosso pipeline: escala variável, pés em alturas diferentes, mãos ou armas cortadas, orientação invertida e espaçamento irregular. O vídeo sugere preocupação com esses pontos, mas não demonstra que todos foram corrigidos.

**02:26–03:09 — referência 3D/Blender.** Observa-se um personagem humanoide dentro do Blender, com cenas de inspeção de câmera e postura. Isto prova a **presença do editor 3D no fluxo exibido**, não prova ligação automatizada entre Blender, as imagens geradas e um atlas final. Qualquer pipeline 3D→sprites para o Assimilação exigiria exportação por direção, câmera fixa, iluminação estável e validação dos quadros.

**03:10–04:09 — retorno às instruções e exemplos.** Surgem strips direcionais e um cenário de RPG com vegetação/casa. A referência de cenário ajuda a avaliar escala e estilo, mas o objeto principal permanece o personagem e as vistas. Não há prova de uma batalha entre Mestre e players nessa gravação.

**04:10–05:02 — variações e organização final.** Vê-se uma matriz com variantes de um soldado, diferentes paletas/roupas, direções e poses, ao lado de nova especificação de texto. É o trecho mais útil como referência de um possível catálogo de variantes: cada linha/coluna deve ter significado explícito; *variante cosmética* não pode ser confundida com *estado mecânico ou transformação demoníaca*.

**Limite de escopo audiovisual:** estes intervalos descrevem momentos observados em amostragem temporal e quadros adicionais. Não substituem uma auditoria de todos os 9.054 quadros, transcrição das falas, leitura integral dos prompts ou inspeção do projeto do autor.

## 3. Análise técnica do método

### 3.1. O problema central: consistência

Para um mesmo personagem, identidade exige manter proporções da cabeça, mochila/armadura, cores, posição do equipamento e ponto de apoio. Geração independente de cada direção tende a introduzir diferenças perceptíveis. A solução não é aceitar imagens bonitas isoladas, mas estabelecer uma **folha de referência e critérios mensuráveis**. Um modelo 3D pode ajudar a fixar proporções e ângulos, mas é opcional e não foi comprovado como obrigatório no vídeo.

### 3.2. Contrato mínimo recomendado

- **Fonte:** PNG com canal alfa e licença/proveniência verificáveis.
- **Grade:** colunas = quadros da sequência; linhas = direções/estados, versionadas em JSON.
- **Vistas:** frente/baixo, esquerda, direita, costas/cima (no protótipo: 4 direções × 4 quadros).
- **Âncora:** `bottom-center` na célula, associada à posição da unidade na grade tática.
- **FPS:** parâmetro de apresentação; independente da economia de ações.
- **Eventos:** idle, walk, hit, cast, transform somente quando disponíveis e autorizados; sem inferir eventos mecânicos a partir dos pixels.
- **Verificações:** divisibilidade, transparência, células vazias, deriva vertical, área de corte, consistência de nome/versão.
- **Governança:** assets TEST separados de fichas canônicas, validação de licenças e revisão pelo escritor competente antes da integração.

### 3.3. O que não se deve assumir

O vídeo não demonstra o formato exato do atlas final, o algoritmo de recorte, exportação por API, tempo real de produção, compatibilidade com celular, copyright/licença do personagem nem uso comercial permitido. Tampouco prova que o Blender é necessário. Qualquer recomendação que dependa dessas premissas permanecerá **INFERIDA/PROPOSTA**, até teste independente.

## 4. Ferramentas, custo e alternativas funcionais

**Blender.** É gratuito e de código aberto, confirmado pela fonte oficial `https://www.blender.org/`. Relevante se decidirmos produzir imagens 2D a partir de modelos 3D; entretanto, o editor completo não foi homologado para o Android do Mestre e não deve se tornar dependência obrigatória agora.

**Ferramentas generativas presentes no vídeo.** A interface sugere criação de imagens por IA, mas o nome exato do serviço e as condições da conta não foram estabelecidos por esta auditoria. Não contratar nem copiar a arte do criador. Preferir recursos já disponíveis e geradores de uso autorizado, seguidos de inspeção da folha resultante.

**Substituto comprovado R$0 neste lote.** Pillow gera um atlas de TEST PNG e o navegador HTML/Canvas o valida e anima, sem API, conexão, assinatura ou instalação pelo Mestre. É uma alternativa real para **testar o pipeline técnico**; não substitui a habilidade de um artista e não promete equivalência estética a personagens 3D gerados por IA.

**Assets de base:** o pacote Kenney Roguelike/RPG publica licença CC0 em `https://kenney.nl/assets/roguelike-rpg-pack`; é candidato a cenários, mas não foi necessário baixar ou utilizar esse pacote neste experimento. Prova de licença e adequação artística sempre separadas.

## 5. Comparação com o Tabletop Assimilação

**Já existente, sob outros executores:** Arena TEST 36 com tabuleiro, tokens, edição e sala experimental; contrato de ações em PESQ-015; visualização TEST de seleção de ação, áreas e recibos em cópias anteriores. Não alterar ou reimplementar esses componentes.

**Lacuna que o vídeo ajuda a fechar:** a Arena ainda necessita de um catálogo de personagens e monstros com sprites coerentes e animados, que possam ocupar células sem perder legibilidade de alcance, terreno, seleção e oclusão. O plano é desenvolver um **adaptador visual** e um catálogo de sprites auditados; não expandir o escopo para mapa de exploração ou motor gráfico paralelo.

**O que permanece fora do escopo:** ataques, defesas, magias e transformações oficiais continuam dependentes da autoridade mecânica VLAB. Uma animação de golpe é apenas apresentação posterior ou provisória, nunca a fonte do resultado. Mestre-only não deve ser embarcado em pacotes destinados às players.

## 6. Entrega concreta: Oficina de Sprites offline

**Arquivo:** `OFICINA_SPRITES_ASSIMILACAO_TEST_ANDROID_OFFLINE.html`. Inclui uma folha de exemplo autoral 192×192 PNG (16 quadros, células 48×48), interações para carregar PNG/WEBP, definir linhas/colunas, selecionar direção, alterar FPS, iniciar/parar, auditar transparência/células, verificar variação aproximada da linha de base e exportar JSON.

**Teste independente:** Playwright + Chromium local (Linux) em 360×740, 390×844 e 412×915; **15 verificações por resolução, 45/45 PASS**, sem solicitações de rede e sem erro JavaScript. A suíte exercitou tamanho/células, direção, pausa, retomada, exportação JSON, erro de grade e restauro. A primeira execução encontrou erro de reset (o exemplo não readitava o estado ao carregar a mesma imagem); foi corrigido e a bateria inteira reexecutada. Portanto, há evidência de falha identificada e correção, não somente de renderização bonita.

**Demonstração restrita:** o arquivo foi carregado no Chromium; não houve teste no Android físico nem integração no TEST 36. O PNG gerado é sintético e simples, **não é arte final do Assimilação**, nem foi extraído do vídeo. Nenhuma ação foi transmitida, nenhum cálculo de VLAB foi executado.

## 7. Plano de integração para o Desenvolvedor, sem writer concorrente

**PASSO 1 — revisar contrato:** aprovar ou ajustar `ASSIMILACAO_SPRITE_PRESENTATION_TEST.v1`, adaptando o visualizador ao renderizador da Arena existente. A ordem das linhas e dos frames deve ser descrita explicitamente; nunca deduzir o significado de uma linha só pela cor.

**PASSO 2 — piloto sobre tokens sintéticos:** carregar um sprite do catálogo em um token TEST, mantendo posições, seleção, escala, colisões e grid já existentes. Verificar 3 viewports de celular e fallback quando imagem faltar.

**PASSO 3 — vincular eventos:** após recibo confirmado da sala/VLAB, reproduzir o estado visual adequado; em UNKNOWN preservar visibilidade de reconciliação, sem representar dano concluído ou executar o comando novamente.

**PASSO 4 — controle de segurança:** assets e campos para Party devem conter somente dados autorizados. Não incluir fichas Mestre-only, estatísticas privadas nem prompts canônicos em arquivos públicos.

**PASSO 5 — gate:** teste físico Android, tamanho de download, tempo de renderização, oclusão, legibilidade em tela pequena, export/import de cenas e rollback. Mudar versão oficial somente após escritor competente e autorização pertinente.

## 8. Critérios objetivos de aceite

1. Folha PNG do personagem TEST possui frames com dimensões divisíveis e alpha: PASS na prova autoral.
2. Todas as 16 células apresentam conteúdo e grade correta: PASS.
3. Animações direcionais mudam somente apresentação: PASS no HTML isolado.
4. Configuração inválida é sinalizada: PASS.
5. Contrato JSON pode ser baixado: PASS nos testes Chromium.
6. Funciona sem rede em modo demonstrado: PASS em carregamento de conteúdo Chromium, mas execução real `file://` Android continua PENDENTE.
7. Integrado a token TEST 36 real: PENDENTE.
8. Animação refletindo evento mecânico homologado: HOLD até recibo/ABI VLAB.
9. Uso físico no Android e performance: PENDENTE.
10. Recursos artísticos finais e direitos comprovados: PENDENTE.

## 9. Proveniência, continuidade e NAC-PASS

**VERIFICADO:** o MP4 e sua duração/hash; presença visual de editor com prompts, imagens direcionais e Blender; PNG autoral; código HTML e execução de 45/45 testes Chromium; ausência de faixa de legendas embutida.  
**INFERIDO:** a intenção do criador de garantir consistência entre ângulos; pipeline híbrido IA/Blender.  
**PROPOSTO:** contrato de sprites, teste de piloto no renderer do Desenvolvedor, eventual revisão de pipeline 3D quando necessária.  
**PENDENTE:** reconhecimento confiável das falas, ferramentas generativas exatas e licenças do autor, execução Android físico, integração ao TEST 36.  
**HOLD:** promoção de recursos visuais não autorizados, mecânica VLAB, multiplayer oficial, publicação Party.  

**LAST-VERIFIED-UNIT:** estudo do vídeo 496132 e Oficina de Sprites TEST com 45/45 PASS; sem mudança ao Tabletop oficial.  
**FIRST-PENDING:** teste real no aparelho Android e revisão do contrato pelo Desenvolvedor; alinhamento aos eventos oficiais apenas após gate VLAB.  
**NEXT:** entregar esta prova ao escritor do frontend para avaliar integração mínima em TEST, sem criar outro renderer, jogo ou operação.  
**NO-REPEAT:** não refazer PESQ-012–015, TEST 32–36, Codex POC ou os cinco lotes anteriores; não retomar áudio reprovado; não presumir que sprite bonito equivale a batalha jogável.

**Classificação NAC-PASS proporcional:** **PASS** para estudo visual, proveniência técnica local e Oficina de Sprites/Chromium. **HOLD** para análise integral da narração, integração na Arena, uso Android físico e mecânica oficial.
