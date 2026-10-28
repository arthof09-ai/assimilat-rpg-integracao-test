# Relatório técnico individual — Vídeo 496036

**Tema:** Comparação de agentes de IA e construção do jogo Véu de Brasas

**Duração real:** 25:44 · 640×360 (H.264) · áudio AAC disponível · 32 quadros amostrados · 2 folhas de contato

**MP4 SHA-256:** `3402d0aeb330b58dd116e39933f4853af2c20721dcb0b7df8693fcc18188dacf`

**Ambiente:** Coordenação do Inovador / Mestre-only / referência científica não-canônica

> **Rigor de evidência:** este relatório examina quadros reais amostrados e quadros-chave dos MP4 enviados pelo Mestre. NÃO contém transcrição integral das falas (os arquivos têm AAC, mas não têm stream de legendas; nesta rodada não havia pesos ASR locais disponíveis). A observação visual de uma demonstração não comprova código, estabilidade, servidor, licenças ou funcionamento no Android. Toda inferência está identificada.

**Missão preservada:** Tabletop Assimilação é a ARENA DE COMBATE TÁTICO MULTIPLAYER do RPG existente, Mestre e players em aparelhos separados. VLAB é a autoridade mecânica; sem motor paralelo, sem divulgar dados Mestre-only, Android-first e R$0 adicional.


## 1. Escopo e evidência observável

Comparação visual entre AI Studio, Antigravity, ChatGPT e Claude sob um pedido semelhante; versões de um jogo de ação com hordas, habilidades em área, feedback, tela de resultados e refinamento gráfico.

O conteúdo foi observado em amostras distribuídas ao longo de TODO o arquivo, com prioridade a transições relevantes. As faixas horárias abaixo identificam blocos da gravação; não significam reprodução/escuta integral de cada segundo.

## 2. Cronologia visual com classificação de confiança

### 00:00–02:30

**OBSERVADO VISUALMENTE:** A abertura mostra quatro candidatos de geração por IA rotulados AI Studio, Antigravity, ChatGPT e Claude. Aparece um texto extenso de especificação e orientações de produção.

**LIMITE / NÃO INFERIR:** Os quatro nomes e as telas são visíveis. Não podemos concluir que receberam *exatamente* os mesmos tokens, limites ou tempo de execução sem examinar prompt e logs completos.

### 02:30–06:30

**OBSERVADO VISUALMENTE:** Uma implementação chamada AI STUDIO aparece com tela de escolha de melhoria, ondas de monstros, hordas e quadrículas. Barras, contadores e foco do personagem aparecem sobre a ação.

**LIMITE / NÃO INFERIR:** UI em execução demonstrada; não há prova do motor, da fórmula de dano ou de testes reproduzíveis.

### 06:30–11:00

**OBSERVADO VISUALMENTE:** Planos e trechos de texto precedem outra visualização de combate em arena escura com projéteis e adversários; a tela alterna do jogo para especificações.

**LIMITE / NÃO INFERIR:** É possível observar iterações de aparência e fluxo, mas os textos miúdos e as falas não foram recuperados integralmente.

### 11:00–15:25

**OBSERVADO VISUALMENTE:** Tela de morte/reinício, mapa de pedras e vegetação, menu de título “Véu de Brasas” e sprites de monstros dispostos em grade.

**LIMITE / NÃO INFERIR:** Há recursos visuais e HUD; os sprites expostos não estão licenciados para o Assimilação.

### 15:25–19:15

**OBSERVADO VISUALMENTE:** Outra interface de Véu de Brasas exibe mapas de calabouço e movimento de um personagem cercado por inimigos. Uma prévia em cone aparece projetada diante do personagem.

**LIMITE / NÃO INFERIR:** O formato visual de um cone na arena é o recurso mais aproveitável para interface de habilidades; NÃO prova alcance correto ou linha de visão.

### 19:15–22:50

**OBSERVADO VISUALMENTE:** O cone e outras zonas de efeito passam a aparecer durante o jogo; números e efeitos luminosos são visíveis. O cenário varia para terrenos esverdeados e zonas de ruínas.

**LIMITE / NÃO INFERIR:** O feedback comunica intenção e resultado de ações; como isso é um jogo de ação, seus cálculos não devem ser adaptados ao RPG tático sem VLAB.

### 22:50–25:45

**OBSERVADO VISUALMENTE:** O jogo mostra chefes, golpes projetados e área de ação, encerrando com inimigos no cenário.

**LIMITE / NÃO INFERIR:** A variação de inimigos e cenários é uma vitrine do autor; duração de desenvolvimento e qualidade de código não foram medidas.

## 3. Achados úteis para o RPG Assimilação

| Prioridade | Técnica e risco | Aplicação real / restrição |
|---|---|---|
| Alto | Área de efeito ANTES de confirmar | Cone, linha, ponto e círculo são convenções visuais úteis. Nosso TEST36 não deve presumir que tais shapes correspondam a uma magia canônica. |
| Alto | HUD sobre o jogo | Transformar o tabuleiro na interface principal e mover controles secundários para gaveta — já existe cópia TEST “Arena Primeiro”. |
| Médio | Comparar agentes pela mesma tarefa | Critério de aceitação deve ser funcional: compatibilidade, custo e código recuperável; não ganhar por arte mais bonita. |
| Baixo | Hordas automáticas | Não copiar geração de hordas, dano ou progressão automática: o Assimilação tem turnos, PA, reações e regras próprias. |

## 4. Ferramentas, viabilidade e substitutas reais

| Ferramenta | O que está verificado e o que falta | Substituta preferível no projeto |
|---|---|---|
| Google AI Studio | Pode criar/codificar protótipos; uso no vídeo observável, mas cota/modelo exatos não estabelecidos. | O Codex Cloud já configurado no projeto ou programação de TEST local sob writer competente. |
| Google Antigravity | Plano individual anunciado a R$0 com limites semanais; seu aplicativo de desenvolvimento é direcionado a desktop/terminal, não equivale a editor Android testado. | Codex Cloud acessado pelo aplicativo ChatGPT Android, com exportação verificável; não instalar IDE desktop só por causa do vídeo. |
| Claude | Comparação visual, sem garantia de plano gratuito adequado à execução prolongada. | Modelo já disponível no fluxo existente, mantendo autoria, logs, checks e R$0 adicional. |
| ChatGPT | Ferramenta do projeto; vídeos não provam que uma simples resposta seja produto testado. | Separar geração de código, execução de testes e readback de pacote. |

**Fontes públicas verificáveis quando pertinentes:** [Google/Unity Playground, 07/10/2026](https://unity.com/news/google-and-unity-partner-on-new-ai-gaming-platform-for-the-next-era-of-interactive-entertainment); [Google Antigravity pricing](https://antigravity.google/pricing); [Google Antigravity overview](https://www.antigravity.google/docs/overview); [Kenney CC0](https://kenney.nl/assets/roguelike-rpg-pack). Material de fontes externas foi consultado para critérios de custo/compatibilidade, NÃO para validar código dos autores.

## 5. Comparação explícita com o TEST36 existente

**JÁ IMPLEMENTADO NA ARENA:** grade tática com 49 casas na demonstração padrão, unidades TEST, edição de mapa, seleção de unidades, rodadas visuais TEST, preview de intenção NÃO ENVIÁVEL no add-on de estudos do Lote 03. TEST35–36 documentam recuperação UNKNOWN/RECEIPT_QUERY e journal fail-closed em fixtures, não servidor mecânico oficial.

**NÃO DEMONSTRADO NO TEST36:** ciclo oficial de iniciativa/ataque/defesa/magia resolvido pelo VLAB, autenticação real Mestre/Party pelo servidor, garantia de sigilo recursivo em WSS, três Android e qualidade visual dos vídeos. Não converter lacunas em PASS por descrição.

## 6. Entrega física ou especificação implementável

**EXPERIMENTO NOVO EXECUTADO:** `experimento/ARENA_TEST36_PREVIA_GEOMETRIA_VISUAL_OFFLINE.html`, uma cópia offline da Arena TEST36 com quatro formas visuais sobre as casas reais. Scripts de teste: `experimento/test_geom.py`, `build_geom.py`, e resultados `resultados_test_geom.json`. Quatro formas × três tamanhos de viewport com 15/15 checks dirigidos em Chromium Linux; 49/49 casas; nenhuma requisição de rede; o JSON anterior de prévia continua `NOT_SENT`/`MECANICA_INDISPONIVEL`. Nenhum alcance, alvo legal, dano, turno, PA ou regra foi alterado. Não foi testado em Android físico. 

### Condições de aceitação

- O Mestre abre uma cópia TEST sem perder tabuleiro/tokens

- Escolhe duas unidades e visualiza um dos quatro formatos

- O contorno não modifica Vida/Alma/PA/iniciativa

- Ao fechar e limpar, a interface volta ao estado de antes

- Antes de execução mecânica, o VLAB competente informa o formato e o alcance reais; caso contrário HOLD.

## 7. Plano de execução sem invadir o Desenvolvedor

1. Comparar a fonte do TEST36 real com o contrato deste relatório e com a fronteira PESQ015; não deduzir compatibilidade por nomes de mensagem.

2. Reproduzir a menor prova relevante em cópia TEST, mantendo original/hash, com aceites ANTES→DEPOIS e sem envio à Party.

3. Se o passo exigir resultado mecânico, consultar a interface VLAB competente e registrar HOLD quando não houver ABI autorizada.

4. Entregar patch ou especificação ao Desenvolvedor competente. Só promover depois dos gates NAC-PASS e testes físicos Android quando necessários.

5. Registrar falhas separando visual, transporte, mecânica e segurança.

## 8. Narração/áudio — estado real

- **VERIFICADO:** existe trilha AAC no MP4 e imagens/textos parcialmente legíveis nas telas.

- **NÃO RECUPERADO:** transcrição integral confiável em português, preços/promessas falados e ordens exatas do narrador. Não foram inventadas frases nem falas.

- **MÉTODO EM ABERTO:** ASR com pesos disponíveis e autorização de processamento local; áudio separado não é exigência do Mestre.

## 9. Parecer executivo do Coordenador

**ALTA PRIORIDADE** para apresentação das áreas de ação do combate tático. Aplicar, mediante writer do Desenvolvedor, apenas como **prévia visual** até haver contrato mecânico homologado. Não usar hordas automáticas como regra.

**PSV:** LAST-VERIFIED = arquivo MP4 e folhas de contato, ferramentas consultadas e artefato/contrato deste relatório; FIRST-PENDING = validação das falas e resultados mecânicos da Arena com ABI autorizada; NEXT = apresentar a prova ao writer competente e testar em Android real; NO-REPEAT = vídeo/regras/sprites de terceiros não copiados, sem motor paralelo nem trabalho em Party/O Primeiro.
