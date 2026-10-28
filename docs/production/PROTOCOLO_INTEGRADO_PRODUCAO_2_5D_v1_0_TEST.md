# RPG ASSIMILAÇÃO — PROTOCOLO INTEGRADO DE PRODUÇÃO DO JOGO 2.5D

**Identificação:** Anexo técnico integrado ao `SPRITE-PIPELINE-TEST` do Laboratório do Inovador  
**Versão:** 1.0 — candidata / TEST / MESTRE-SIDE  
**Data-base:** 26 de outubro de 2026  
**Autoridade das decisões criativas:** Mestre  
**Guarda documental:** Notion do RPG Assimilação  
**Homologação sistêmica:** PENDENTE; não substitui NAC-CONT-03, NAC-NORM-01, NAC-PASS-02, VLAB, LEVEL-UP, DMG, CRAFT ou contratos oficiais.

> **Princípio executivo:** preservar o que já existe, produzir ativos verificáveis, manter consistência visual e física, separar apresentação artística de mecânicas canônicas e integrar ao jogo por interfaces autorizadas. Uma animação de vinte quadros continua sendo uma ação mecânica quando o VLAB assim a resolver.

## 0. Resumo executivo e limites

Este documento consolida o fluxo completo de produção de referências, monstros, NPCs, personagens, armas, equipamentos, terrenos, mapas, efeitos visuais, movimentos, sprite sheets, modelos 3D, interfaces e integrações do Tabletop do RPG Assimilação. **Não** institui uma nova operação, reescreve o sistema de combate, presume autorização de writer, altera fichas, substitui trabalho do Desenvolvedor ou concede acesso à Party. O documento é um protocolo operacional técnico subordinado às normas vigentes.

As **diretrizes criativas expressamente aprovadas** estão incorporadas; escolhas de engenharia e contratos ainda não demonstrados estão marcados **PROPOSTOS** ou **PENDENTES**. A promoção de algo a PROD depende de implementação física, testes, readback e aprovação competente.

### Estados obrigatórios

| Estado | Significado |
|---|---|
| VERIFICADO | Prova física no artefato, código, teste ou Notion reaberto |
| APROVADO PELO MESTRE | Decisão expressa de intenção visual/funcional, não homologação mecânica |
| INFERIDO | Parte oculta ou comportamento plausível, ainda não visto ou comprovado |
| PROPOSTO | Método, contrato ou solução de engenharia ainda não implantado |
| TEST | Protótipo isolado, sem efeito de verdade canônica |
| PENDENTE/HOLD | Falta prova, decisão, interface, acesso ou gate |
| PROD/APROVADO | Somente após implementação, testes e NAC-PASS aplicável |

## 1. Governança, fontes de verdade e responsabilidades

1. O **Notion canônico do RPG** preserva regras, fichas e decisões vigentes. O Mestre aprova intenção e direção. A governança aplicável inclui BOOTSTRAP-COMESTRE, NAC-CONT-03, NAC-NORM-01, NAC-PASS-02, LONG-RUN-01 e a distribuição de responsabilidades do Laboratório do Inovador.
2. O **VLAB é a autoridade de resolução mecânica** quando seu contrato cobre a ação: turnos, iniciativa, gasto de ações/PA, ataques, dano, defesa, alvos, interrupções e ordem causal. A interface não recalcula o RPG nem altera os resultados.
3. O **Tabletop existente** é a linha funcional a evoluir com o Desenvolvedor e o Codex conforme escopo e writer legítimos. O protótipo HTML/JS atual não deve ser descartado por entusiasmo com Godot. Uma rota Godot deve começar como estudo/protótipo de apresentação e receber decisão de integração própria.
4. O **Blender** é ferramenta de modelagem, rig, animação, renderização e exportação visual; o **Godot** pode importar recursos e validar cenas, sprites, câmera, animações e colisões, mas não assume autoridade mecânica sem contrato. **Codex/Work/Computer Use**, quando disponível e autorizado, são meios de execução, não provas de permissão ou execução realizada.
5. **MESTRE-SIDE**: ativos ainda secretos, metadados de produção e resultados de testes internos não seguem à Party nem a O Primeiro. Exposição pública requer triagem de direitos e segredos. Custo adicional alvo: **R$ 0**, sem compromissos pagos não aprovados.
6. Divisão funcional: Mestre — decisão e aceite; Coordenador Inovador — critérios, rastreabilidade e handoff; Pesquisador — evidências e opções; Desenvolvedor/Codex — implementação sob writer competente; Auditor — provas independentes quando cabível; VLAB e demais frentes — competência preservada.

## 2. Catálogo dos ativos e seu ciclo de vida

Famílias tratadas pelo pipeline: (A) personagens, NPCs e bestas; (B) armas, escudos, armaduras, roupas e acessórios; (C) habilidades, magias, projéteis, impactos e VFX; (D) terreno, arquitetura, cenário, props e mapas; (E) interfaces, ícones, menus e indicadores; (F) animações e sequências; (G) contratos de ligação aos dados canônicos.

Cada ativo recebe **identidade estável** (`asset_id`), referência original, responsável, contexto de uso, versão, data, status, público permitido, arquivos-fonte editáveis, exportações, hashes e histórico de mudanças. Não dar novos IDs a cópias redundantes de ativo existente. Arquivos gerados ou screenshots não substituem ficha canônica.

**Estados do ativo:** RECEBIDO → REFERÊNCIA AVALIADA → IDENTIDADE VISUAL APROVADA → TEST DE GEOMETRIA/ÂNGULOS → TEST DE ANIMAÇÃO → QA TÉCNICA → TEST EM CENA → ACEITE VISUAL DO MESTRE → INTEGRAÇÃO/GATE → PROD, se autorizada. Reprovação volta apenas à etapa defeituosa, preservando partes aprovadas.

## 3. Briefing e referência-mãe

Antes de gerar arte, registrar: espécie/identidade, quantidade e posição de membros, anatomia, silhueta, expressão, paleta, materiais, textura, adornos, armas, mão dominante, acessórios assimétricos, escala relativa a um humanoide e câmera de uso. Identificar o que é **observado**, **inferido** e **ainda não mostrado** (costas, lado oculto, interior do manto etc.).

A referência aprovada funciona como **modelo visual de identidade**, não como evidência de geometria 3D perfeita. Se não houver vista de costas, criar complementação anatômica coerente, sem transformar o monstro em outra espécie. Objetos e efeitos de obras externas são inspirações metodológicas; não reproduzir assets, personagens, pergaminhos, cenas nem sequências protegidas.

**Caso Orc:** cabeça do lobo no ombro **esquerdo anatômico**; machado grande, cabo reto, metal recortado e pesado; sua representação em perfil direito pode ocultar a cabeça de lobo, nunca transferi-la ao ombro direito. O tamanho da arma deve ser proporcional ao personagem, sem aparência de machadinha por excesso de miniaturização.

## 4. Direção visual e câmera 2.5D

A proposta estética do Mestre é **pixel art realista, detalhada e legível**, em câmera inclinada superior inspirada funcionalmente em Hades 1, League of Legends e Baldur’s Gate 3, sem copiar seus recursos visuais. Uma elevação visual aproximada de 30° a 40° é hipótese inicial de teste, **não configuração canônica automática**.

Travar por ativo/família: projeção ortográfica ou perspectiva adotada, elevação, distância/aparente escala, direção da luz, tom, plano do chão, posição do pivô e lado anatômico. Evitar mudança de câmera inadvertida entre vistas e frames. Medir tamanho de cada personagem e da arma com régua comparativa de humanoide, não pelo preenchimento da tela.

**Enquadramento:** margens geralmente de 10% a 20% dentro da célula; reservar mais onde arma, asas ou cauda excedem o corpo. Nunca comprimir, achatar ou cortar extremidades para preencher o quadro. Se quatro figuras por folha ficarem pequenas, passar para duas ou uma por folha. Zoom da câmera e escala física do objeto são variáveis distintas.

## 5. Turntable direcional de personagens — padrão quatro por prancha

**Diretriz do Mestre:** preferir **duas pranchas 2×2**, cada uma com quatro vistas legíveis, em vez de oito figuras pequenas na mesma imagem.

- **Prancha A — cardinais:** 01 Frente/S, 02 Direita/E, 03 Costas/N, 04 Esquerda/O.
- **Prancha B — diagonais:** 05 Frente-direita/SE, 06 Costas-direita/NE, 07 Costas-esquerda/NO, 08 Frente-esquerda/SO.
- **Prancha C — índice opcional:** as oito orientações em imagem de consulta menor, nunca substituindo os arquivos-mestres em escala grande.

Produzir primeiro A; auditar silhueta, proporções, assimetrias e volume; obter aceite; produzir B **derivada das mesmas referências e A**, sem reinvenção. Para criaturas enormes ou complexas, são permitidas **duas ou uma vista por folha**. Uma prancha de ângulos apresenta orientações; **não equivale** a quadros temporais de um ataque.

## 6. Turntable de armas e itens — 12 perspectivas

Para arma complexa, criar 12 vistas do **mesmo objeto rígido**: frente 0°, frente-direita 45°, direita 90°, trás-direita 135°, traseira 180°, trás-esquerda 225°, esquerda 270°, frente-esquerda 315°, axial superior, axial inferior, isométrica superior e isométrica inferior. Eixo do cabo fixo; cabeça e lâminas permanecem conectadas. Elementos assimétricos e manchas seguem suas superfícies.

**Erros já observados e proibidos:** diagonais que inventam outra lâmina; cabeça metálica inflada; duplicação de peças; cabo torto; espelhamento errado; lâminas encostando na borda; machado reduzido a machadinha; PNG com fundo pintado. Em falha recorrente, preferir **um único modelo 3D Blender e renderizações por rotação real** em vez de gerar perspectivas 2D desconexas. A prancha e o modelo requerem aprovação do Mestre, não aprovação automática.

## 7. Escala de monstros, grid, footprint e hitbox

Separar formalmente as seguintes coisas:

- **Escala corporal:** dimensões do monstro no mundo e relação visual com humanoides. Não presumir metros por tile sem ler contrato/código existente.
- **Sprite/silhueta:** pixels exibidos; partes visíveis podem ultrapassar células por perspectiva, VFX, arma, asas ou cauda.
- **Footprint:** máscara de células efetivamente ocupadas pela criatura, podendo ser 1×1, 1×6, T, L, cruz, retângulo ou formato orgânico; não precisa ocupar a caixa delimitadora inteira.
- **Hitbox atingível:** geometria de corpo elegível a ataque, vinculada à anatomia/pose e à ocupação declarada, sem se limitar ao pivô central. Hitbox fina da engine e máscara tática podem diferir.

Exemplo de footprint em T, cinco células ocupadas em 3×3:

```text
[X][X][X]
[ ][X][ ]
[ ][X][ ]
```

A máscara deve suportar pivô, rotação/orientação e colisão com paredes, personagens e terreno. Selecionar qualquer célula corporal ocupada pode resolver o mesmo `actor_id` como alvo quando regras oficiais permitirem. Atingir duas células pertencentes ao **mesmo ator não implica duplicar dano**. Linha de visão, alcance, adjacência, AoO, deslocamento e áreas aguardam semântica oficial do VLAB/contratos existentes; não improvisar.

**Casos TEST obrigatórios:** máscara 1×1; 1×6; T de cinco células; L assimétrico; rotação junto de obstáculo; seleção da extremidade; interseção de AoE com múltiplas células do mesmo ator; ausência de duplo dano; idempotência; replay/snapshot; transformação ou mudança real de porte quando e se autorizada. Nenhuma escala tile↔metros inventada pelo protocolo.

## 8. Coreografia de ataques, magias e habilidades

**Prancha temporal é diferente de turntable.** Aprovada a convenção de **cinco quadros por linha**, leitura 01–05, 06–10, 11–15, 16–20 e quantas linhas ou páginas forem necessárias. O número de quadros é escolhido pela complexidade e pela clareza, nunca por um teto arbitrário; dividir em várias folhas quando houver miniaturização.

Fases de uma ação: entrada/repouso → intenção/antecipação → carregamento → aceleração → execução → contato/liberação → seguimento → desaceleração → recuperação/retorno (ou transição explícita). Nem todas precisam ser um quadro isolado; pausa, velocidade e interpolação são temporais, não só contagem de poses.

Verificar arcos de cabeça/mãos/pés, centro de gravidade, transferência de peso, ponto de apoio, trajetória da arma, ângulo da câmera, impacto e estado final. Uma sequência que acaba no quadro de contato está **incompleta**, a menos que esse seja um estado de transição deliberadamente integrado. Quadros repetidos não servem para completar grade; somente quando pausa deliberada.

Estilos aprovados como possibilidade, sem classe fixa:

- **Cinético/impactante (inspiração Hades 1):** deslocamentos, ataques legíveis e fortes, mudanças de posição, efeitos direcionais, transições rápidas.
- **Marcial/elemental fluido (inspiração Avatar):** movimentos corporais elegantes, quase dança, artes marciais e elementos seguindo os gestos e o fluxo corporal.
- **Híbrido:** alta fluidez com impacto forte, fluidez baixa e impacto leve/forte, ou qualquer combinação coerente.

**Fluidez, peso visual, impacto, velocidade, amplitude, deslocamento e expressão elemental são eixos artísticos independentes.** Não definem automaticamente dano, PA, elemento disponível ou direito a mais ataques. Estilos de adagas/ladino e magias de outras obras continuam referências a pesquisar futuramente, sem escolha presumida.

## 9. VFX e semântica visual

Sempre que possível, separar **personagem, arma/equipamento, VFX, sombra e interface** em camadas exportáveis. A magia precisa de origem, gestual, formação, liberação, trajetória ou área, momento de consequência e dissipação. Um VFX cinematográfico não pode encobrir continuamente arma, personagem ou alvos; usar contraste/ordem de desenho para legibilidade.

Fazer variantes de impacto, erro, bloqueio, esquiva, interrupção e cancelamento somente se o contrato de eventos realmente distingui-las. Não mostrar como acerto oficial aquilo que o VLAB resolveu como erro. Nenhuma animação cria nova área, alvo, ação, reação, AoO, dano ou recurso por conta própria.

## 10. Ferramentas — competência, entradas e saídas

| Ferramenta | Usar para | Nunca presumir |
|---|---|---|
| Notion | Cânone, referência, aprovação, proveniência, registros e checkpoints | Arquivo carregado ou página alterada sem readback |
| Gerador de imagens | Estudos visuais, identidade, variações e conceito 2.5D | Geometria 3D perfeita ou transparência real sem inspeção |
| Blender | Modelo 3D, escala, rig, poses, render de ângulos, PNG RGBA | Integração automática com motor de combate |
| Vídeo/gerador de movimento | Estudos de timing e frames auxiliares | Persistência de anatomia/arma entre todos os quadros |
| Extrator e montador local | Quadros individuais, atlas, duração, pivô, manifesto | Fluidez/identidade artística por passar em teste de arquivo |
| Godot | Câmera, AnimatedSprite2D, AnimationPlayer, cena visual, TileMapLayer e inspeção | Autoridade sobre regras canônicas ou engine-alvo definitiva |
| Tabletop HTML/JS existente | Apresentação, mapa, UI, tokens, replay e cliente | Novo motor mecânico independente do VLAB |
| Codex/Work/Computer Use | Editar/testar ferramentas e projetos quando conectado e autorizado | Controle automático do PC sem capacidade e permissões verificadas |
| GitHub público | Versão demonstrativa sem segredos; documentação técnica permitida | Licença para redistribuir arte de terceiros ou dados MESTRE-ONLY |

**Fontes oficiais:** [Godot — AnimatedSprite2D e sprite sheet](https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html), [Godot — TileMaps/TileMapLayer](https://docs.godotengine.org/en/stable/tutorials/2d/using_tilemaps.html), [Blender — fundo transparente](https://docs.blender.org/manual/en/latest/render/cycles/render_settings/film.html). A seleção e versão exata das ferramentas devem ser verificadas no ambiente do executor.

## 11. Contratos mínimos dos arquivos (candidatos TEST)

**Organização sugerida** (não migra nem substitui a estrutura existente sem decisão):

```text
assets/<asset_id>/references/
assets/<asset_id>/source_3d/
assets/<asset_id>/views/S|SE|E|NE|N|NW|W|SW/
assets/<asset_id>/animations/<action_id>/<direction>/frame_001.png
assets/<asset_id>/vfx/<effect_id>/
assets/<asset_id>/atlases/
assets/<asset_id>/manifest.json
assets/<asset_id>/qa/
```

**Manifesto mínimo recomendado:** `asset_id`, `entity_ref_canonical` (quando houver), `scope`, `origin`, `source_license`, `reference_sha256`, `asset_version`, `author_tool`, `view`, `camera_config`, `pixels_per_unit` (se aprovado), `physical_scale_source`, `pivot`, `footprint_by_facing`, `collision_or_hit_region`, `animations[]` (ação, orientação, frames, duração por frame, loop/transição), `vfx[]`, `approved_by`, `approval_state`, `source_hashes`, `output_hashes` e `integration_contract_version` (se houver). Campos desconhecidos são `null`/PENDENTE, jamais valores estimados apresentados como canônicos.

**PNG RGBA:** existência de canal alfa e pixels realmente transparentes; verificar limites da silhueta/efeito; nomeação e ordem estáveis; dimensões de célula consistentes; nenhum quadro redimensionado independentemente sem critério aprovado; pivô padronizado. **Atlas:** coordenadas, quantidade de linhas, colunas, duração, animação e direção devem estar no manifesto. Uma imagem estática não comprova temporalidade; gerar prévia animada.

## 12. Separação visual ↔ mecânica e eventos

Contrato de responsabilidade:

```text
Pedido do Mestre
  -> validação e resultado pelo contrato VLAB competente
  -> eventos autorizados e ordenados (ator, ação, alvo, desfecho, interrupções)
  -> adaptador de apresentação, SOMENTE LEITURA do resultado
  -> animação corporal e VFX correspondentes
  -> recuperação visual / estado sincronizado
  -> liberação de próxima ação segundo scheduler oficial
```

O frame de contato deve estar **sincronizado visualmente** com o evento mecânico pertinente, sem criar novo evento oficial. Se eventos chegarem atrasados, forem repetidos ou invalidados, o cliente deve respeitar ordenação/idempotência do contrato e ter política de apresentação/replay testada. Animação por turnos pode ter 20, 50 ou 100 frames e representar **uma única ação**; quantidade de frames não multiplica dano nem autoriza combo mecânico não validado.

## 13. Processo de produção — dez gates executáveis

| Gate | Entrada | Saída exigida | Motivo de HOLD |
|---|---|---|---|
| G0 — Escopo | Pedido do Mestre e fonte vigente | Brief com identidade, destino e autoridade | Referência/escopo ambíguos e materialmente conflitantes |
| G1 — Referência | Imagens/descrições | Ficha-mãe com observado/inferido | Anatomia não reconhecível ou proveniência ausente |
| G2 — Escala | Ficha-mãe + parâmetros existentes | Tamanho comparado e pivô; footprint proposto se necessário | Tile/metragem inventados |
| G3 — Vistas | Modelo visual | Prancha A, B ou 12 vistas com margens | Duplicação, deformação, lado trocado, recorte |
| G4 — Rig/poses | Vistas aprovadas | Modelo fonte/poses-chave | Interpolação quebrada ou arma instável |
| G5 — Animação | Poses + ação | Sequência completa e preview temporal | Falta clímax, recuperação, orientação ou fluidez |
| G6 — Exportação | Fonte e quadros | PNG alfa, atlas e manifesto/hash | Transparência falsa, pivô ou arquivo corrupto |
| G7 — Cena | Assets + projeto autorizado | Import demonstrável em Godot/HTML conforme rota | Novo motor paralelo, conflito de API ou escala |
| G8 — Combate | Eventos oficiais do VLAB | Mapeamento visual validado a eventos/resultados | Alvo/dano/ordem de eventos reimplementados |
| G9 — Aceite | Testes e registro ANTES/DEPOIS | Readback, evidências, aprovação do Mestre e gate NAC | Sem prova real, distribuição inadequada ou regressão |

Corrigir apenas o gate falho quando tecnicamente possível, manter versões e não recomeçar ativos aprovados desnecessariamente. Um ciclo `TEST PASS` comprova somente os critérios efetivamente executados.

## 14. Matriz de ensaios mínimos

**QA artística:** oito orientações distintas; proporção corpo/arma; mesma cabeça do lobo no ombro esquerdo; nenhuma duplicata; continuidade frente→diagonal→perfil→costas; luz/câmera invariantes; margens; sem cortes; legibilidade a tamanho real no mapa.

**QA de animação:** início/contato/fim legíveis; peso e aceleração; cada frame acrescenta gesto ou pausa intencional; quadros temporais e preview; não há teleporte visual acidental; arma rígida; VFX acompanha o gesto; final encaixa com idle ou próxima pose.

**QA de engine:** atlas extrai exatamente N quadros; duração respeitada; pivô não salta; rotação troca direção certa; câmera e sorting corretos; zoom em Android/PC; não há borrões/cintilação indevidos.

**QA de footprint/hitbox:** caso 1×6 e T; rotação junto a obstáculos; tentativa de cruzar parede; várias células da mesma criatura em AoE; seleção em borda/extremidade; sem dano duplicado; alvo inválido; pathfinding; linha de visão e cobertura **conforme contrato**; replay e ordenação de eventos.

**QA sistêmica:** nenhum dado Mestre-only no repositório público; licenças; sem escrita em Party/O Primeiro; sem writer assumido; hashes de arquivos e log no lugar certo; readback de registro; regressão nas funções existentes do Tabletop e VLAB.

## 15. Operação entre ferramentas, segurança e custos

Aplicar cadeia: **LER → ESTADO ANTES → AUTORIDADE → EXECUTAR NO ESCOPO → TESTAR → REABRIR/RELÊ-LO → RECONCILIAR → ESTADO DEPOIS → NAC-PASS QUANDO APLICÁVEL**. Repositório público recebe só demo sintética, sem dados Mestre-only, segredos, credenciais ou recursos de terceiros sem licença. O Notion gratuito pode limitar anexos por arquivo; anexo acima do limite não bloqueia trabalho: registrar nome, versão, SHA, destino seguro e pendência de custódia, sem declarar upload que não ocorreu.

Preservar fontes 3D editáveis, quadros PNG individuais, atlas, manifesto, preview, roteiro de poses, imagem-mãe, licença e evidência de teste. Nunca usar um PNG achatado como único arquivo-mestre de um ativo difícil de reproduzir. Fazer backup/exportabilidade para migração entre contas e ferramentas.

## 16. Priorização de entregas e integração incremental

**Primeira demonstração vertical recomendada, sob writer competente:** um ator aprovado (Orc), escala e pivô, oito direções com vistas originais 4+4, um ataque pesado de machado com sequência completa, um alvo TEST, efeitos visuais legíveis, um caso de defesa/erro/acerto derivado dos eventos oficiais, um footprint irregular TEST separado e um replay inspecionável. Evitar multiplayer completo, cenários enormes ou inventário total antes de validar essa fatia end-to-end.

**Evolução:** (a) personagens pequenos, médios e colossais; (b) footprint irregular com orientação; (c) escola cinética/impactante, marcial-elemental e híbrida; (d) adagas/ladino e magia com futuras referências selecionadas; (e) efeitos de área; (f) mapas, tiles, cenários; (g) otimização e apresentação multiplayer conforme sequência do Desenvolvedor; (h) distribuição liberada e validação de dispositivos reais.

A rota Blender→renders 2D→Godot é sugestão de produção visual; não assumir migração imediata do HTML/JS existente. As metas devem ser executadas por lotes demonstráveis, com checkpoints recuperáveis, sem gerar outros laboratórios ou motores.

## 17. Critério de conclusão de uma entrega

Uma entrega completa precisa especificar: `LAST-VERIFIED`, `FIRST-PENDING`, `NEXT`, `NO-REPEAT`, versão, artefatos e hashes; imagens de comparação antes/depois; lista de testes com resultado e ambiente; aprovação do Mestre quando necessária; link/página canônica da fonte; riscos remanescentes; permissão de distribuição. **Não dizer “pronto” se apenas o prompt, conceito, prancha estática ou relatório estiverem prontos.**

Se falhar a integração mecânica, aprovar visualmente o ativo pode ser legítimo, mas informar `VISUAL APROVADO / INTEGRAÇÃO HOLD`. Se o asset foi renderizado mas não testado no jogo, informar `RENDER VERIFICADO / GAMEPLAY NÃO TESTADO`.

## 18. Ponto de retomada e responsabilidades imediatas

**LAST-VERIFIED documental prévio:** Laboratório do Inovador já reúne o SPRITE-PIPELINE-TEST, diretriz 5 colunas, identidade visual/turntable 4+4, hitbox-footprint irregular e estudos Hades × Avatar (leituras Notion de 26/10/2026). **PENDENTE:** implementação física de máscaras de footprint pelo Codex/VLAB, medida real do tile e contrato de alvo, turno completo animado, integração efetiva Blender/Godot/HTML, auditoria real de fluidez e release. **NEXT:** entregar documento ao Coordenador Inovador e Desenvolvedor legitimamente responsáveis, auditar interface atual antes de editar código e desenvolver vertical slice TEST. **NO-REPEAT:** não repetir pesquisa consolidada, não recriar regras/motores/áreas de trabalho nem duplicar entradas de ficha.

### Fontes internas

- [Laboratório do Inovador](https://app.notion.com/p/401c2b324ede809585d3d1907c194df9)
- [Kit Essencial de Integração — BOOTSTRAP-COMESTRE](https://app.notion.com/p/3edc2b324ede81d0b25ec2f3be128db6)
- [Painel do Mestre — governança](https://app.notion.com/p/3f0c2b324ede81628f43e2d61a0929e2)

**Observação:** referências públicas e tutoriais de ferramentas são material de apoio; o jogo é governado pelas fontes canônicas autorizadas, não pela documentação de terceiros.