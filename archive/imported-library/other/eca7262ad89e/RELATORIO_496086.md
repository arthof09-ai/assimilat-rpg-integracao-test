# Relatório individual — 496086
## RPG visual, animação de personagens, sprites e transferência de recursos para a interface

**Projeto-alvo:** Tabletop Assimilação · **Destinatário:** Coordenador e Desenvolvedor (MESTRE-SIDE) · **Data da análise:** 24/10/2026 · **Duração da fonte:** 27min57s · **Arquivo:** `496086.mp4` · **SHA-256:** `8be501727611630c4b0106cce8fd3a26f11f76e51c294c13e5042149ef8152f1`.

**Classificação:** estudo visual verificável e especificação proposta. Não constitui verificação do código, licença de arte, dispositivo Android ou narração integral. MP4 com H.264/AAC, 640×360, sem faixa de legendas. Foram amostrados 30 quadros temporais mais sete ampliações; a narração não foi transcrita.

## Síntese executiva e impacto

O criador alterna entre **o jogo executado** e o **processo de produção de personagem e animação**. Mostra campos, ruínas e interiores com aparência consistente, depois um documento de instruções de animação, sprite sheets, uma imagem de rosto isolada e, por fim, cenas de apresentação com retrato no canto. Para Assimilação, o ganho não é importar a arte desse autor, mas estabelecer um **contrato de recursos visuais verificáveis** para cada token da arena: PNG com transparência, atlas coerente, direção, quadros, âncora, tamanho em casas e estados de animação. O desenho dos tokens deverá continuar separado de posição, permissões, iniciativa e efeitos do VLAB.

## Cronologia de observações auditáveis

| Faixa aproximada | Evidência visual | Interpretação com cautela |
|---|---|---|
| 00:00–02:55 | Personagem armado em estrada campestre, ruínas e interior de pedra, com HUD pequeno e minimapa | O vídeo compara cenários com aparência consistente; não prova multiplayer ou regras completas |
| 03:00–05:40 | Documento no navegador, título visível sobre animações de personagens para games e várias folhas de sprites | Há um processo explícito de decomposição de movimentos; detalhes textuais não foram todos recuperados |
| 06:00–08:20 | Variações de pose, movimento e folhas com recortes de sprite | Evidência de preparação de assets e de problema de padronização entre poses |
| 08:40–11:00 | Retorno ao jogo com personagem no mapa, árvores e caminho | Ciclo de integração visual no protótipo do autor, não evidência de receita automática sem ajustes |
| 11:20–17:50 | Aplicação de IA, escolha/importação de imagem de retrato com fundo verde e instruções textuais | O recorte de fundo e a consistência de estilo exigem verificação; não presumir licença da imagem |
| 18:00–23:55 | Textos de correção e métricas num ambiente de trabalho; retrato estilizado é ajustado | Mostra iteração e inspeção de resultados; métricas são do ambiente do autor, não do nosso jogo |
| 24:00–25:55 | Detalhes de sprites/retrato e cena verde com personagem e painel de retrato à esquerda | A UI de identificação do personagem é uma referência útil para seleção tática |
| 26:00–27:57 | Cenas de ruína/floresta/caverna com HUD de Vida e personagem | A apresentação varia por mapa e ambiente; alcance, colisão e Turnos não são demonstrados |

## O que pode e o que não pode ser afirmado

**VERIFICADO NA IMAGEM:** personagem visível, atlas/sprite sheets, retrato, mapas variados, UI de recursos e interação visual com navegador/editor. **INFERIDO:** foi necessário organizar assets em atlas com direções e estados; a captura não mostra o pipeline completo. **PROPOSTO:** usar atlas e retrato em nossa Arena. **PENDENTE:** transcrição da narração, projeto fonte, direitos dos assets, integração em Android, medição de FPS e exame de colisões/oclusão.

## Engenharia aplicável ao Tabletop Assimilação

**Contrato visual mínimo de token** (proposta, não cânone): `token_visual_id`, `atlas_url`, `frame_w`, `frame_h`, `directions`, `states`, `frames_per_state`, `fps`, `pivot_foot_x/y`, `grid_occupancy_w/h`, `alt_label`. O arquivo não identifica identidade canônica do personagem, nem inclui valores de Vida/PA. A renderização segue a projeção autorizada da sala e não interpreta regras.

**Camadas e escala:** solo/água/obstáculos baixos → tokens → copas/portais/camadas oclusivas → marcadores de seleção/alcance. O jogador deve sempre enxergar quais casas a mecânica considera ocupadas, mesmo com árvore artística sobreposta. Uma camada opcional de grade acessível e contorno de token evita que a bela arte torne o tabuleiro ilegível.

**Feedback de ação:** um evento visual `ATTACK_PRESENTATION_CONFIRMED` recebido do backend pode disparar quadros de golpe, mas nunca assumir resultado por previsão local. Se recibo `UNKNOWN`, mostrar recuperação/reconciliação, sem animação de dano irreversível.

## Alternativas gratuitas e executáveis

- **Prioridade agora:** HTML/JS Canvas e arquivos PNG locais com sprite sheets autorais/licenciadas. Já temos o Tabletop em HTML; migrar de engine produziria risco sem provar benefício.
- **Assets gratuitos:** [Kenney Roguelike/RPG CC0](https://kenney.nl/assets/roguelike-rpg-pack) fornece tiles simples, mas não oferece por si só todos os ciclos de animação; validá-los numa cópia TEST. As artes do vídeo não são automaticamente reutilizáveis.
- **Sprite pipeline sem assinatura:** Python/Pillow para recortar/validar dimensões/alpha e gerar manifesto; ou edição manual num aplicativo de desenho realmente utilizável no Android. Não reintroduzir PixelLab.
- **Alternativa 3D de avatar:** Mixamo é irrelevante para sprites 2D neste marco, a menos que o Desenvolvedor aprove um pipeline render-to-sprite com origem e direitos demonstrados.

## Experimento proposto ao Desenvolvedor (executável, testável, não realizado neste vídeo)

**Nome:** `TOKEN-ATLAS-VISUAL-TEST`. Inserir no TEST36 atual, apenas sob writer autorizado, um token com atlas próprio ou CC0, pelo menos 4 direções e 2 quadros por direção; preservar 49 casas, FOV, régua, zoom, áreas de efeito e o cliente de sala. Gerar hash de PNG e do arquivo original; recortar frame no Canvas; testar primeira tela Android 390×844 e três posições sobrepostas a objetos.

**Critérios de aceite:** 4/4 direções, 8/8 índices válidos, nenhum frame fora do atlas, 0 alterações de posição/custos via código de animação, grade e hover legíveis, screenshot real e tempo de quadro medido. Não aceitar apenas uma foto bonita como demonstração de sprites animados.

## Contribuição material deste lote

Produzi o relatório com evidências temporais, quadros ampliados e o contrato visual de atlas. O experimento executado neste lote está focado em apresentação de recibos sintéticos na cópia do TEST36, não em animação final de sprite. Portanto, **o contrato de animação está PROPOSTO, não implementado**.

## Riscos e dependências

Fonte artística de terceiros; consistência entre oito ou mais direções; custo de memória no Android; animações e oclusão que escondam unidades; divergência de cor/contraste; dados Mestre-only nos rótulos. Decisões de arte pertencem ao Mestre/Desenvolvedor; VLAB não muda por escolha visual.

**LAST-VERIFIED:** frames do arquivo original e SHA256. **FIRST-PENDING:** atlas original/CC0 em TEST36 com testes de posição e FPS. **NEXT:** integração visual com tokens existentes. **NO-REPEAT:** não criar um explorador genérico nem engine novo; não inferir sistema de combate do vídeo. **NAC-PASS:** estudo visual PASS; integração atlas/Android HOLD.
