# RPG ASSIMILAÇÃO — ORDEM EXECUTIVA DO MESTRE PARA O CODEX
## CONTINUIDADE DO PROTÓTIPO JOGÁVEL · ARQUITETURA DE ANIMAÇÃO REUTILIZÁVEL · BLENDER → GODOT → NAVEGADOR

**Identidade operacional:** MESTRE-SIDE. **Natureza:** ordem de EXECUÇÃO, não apenas atualização de contexto. **Ambiente-alvo:** notebook Windows do Mestre, se fisicamente acessível nesta sessão. **Produto-alvo:** jogo RPG 2.5D jogável em navegador. **Prioridade imediata:** qualidade visual + locomoção/combate básicos + protótipo executável, sem antecipar a integração canônica completa do combate.

## A. ESTADO HERDADO E INÍCIO EXATO

Você informou como último checkpoint: um protótipo básico jogável com movimento, ataque, defesa, perda de Vida, consumo de Alma e salvamento; 25 testes do motor e 28 verificações da interface aprovados; pacote de entrega de aproximadamente 59 MB; contexto mestre, manual Blender/props/tiles/sprite sheets, regras exemplificadas e instruções de execução. Arte ainda em estudo e fichas com valores sintéticos TEST, separadas das regras oficiais. Projeto anterior preservado. Seu próximo passo anunciado foi testar a batalha no navegador, depois refinar rigs/animações no Blender e iniciar integração Godot no notebook.

**Faça isso agora.** Trate esses números e capacidades como relato do checkpoint anterior, NÃO como testes já reexecutados nesta sessão. Primeiro localize e abra o produto realmente existente, confira arquivos e ponto de retomada; execute um smoke test da batalha no navegador e regressões pertinentes. Não recrie o protótipo nem repita microtestes de instalação já aprovados sem indício de falha. Prossiga para uma entrega visual mais avançada no mesmo trabalho.

Receberá também o ZIP `RPG_ASSIMILACAO_ACERVO_VISUAL_UNIFICADO_CODEX_v001.zip` (ou sucessor fornecido pelo Mestre). Ele contém os acervos do **Orc**, do **Capríleo Escamoso Ouro 1★** e da **Besta Cristalina**. A biblioteca unificada é transferência de insumos; NÃO representa homologação de rig, animação, alpha, FPS, pivôs ou mecânica. Leia primeiramente `00_COMECE_AQUI`, índices, READMEs, manifestos e relatórios; confira nomes/hashes contra bytes reais, sem confiar apenas em nomes de arquivo.

## B. AUTORIDADE, SEGURANÇA E CONTINUIDADE

1. Você atua como executor técnico subordinado ao Mestre e à governança canônica. Recupere no Notion as fontes vigentes: `BOOTSTRAP-COMESTRE`, `NAC-CONT-03 v2`, `NAC-NORM-01` quando houver alteração de normas, `NAC-PASS-02` no fechamento, `NAC-EVOL`, registros/Diário aplicáveis e o ponto de retomada do Laboratório do Inovador. Não invente uma nova norma, operação, motor de combate, ID ou status de aprovação. Se houver conflito entre documentos, resolva conforme a hierarquia registrada, com evidência, e marque HOLD quando apropriado.
2. Referências Notion: Laboratório do Inovador `https://app.notion.com/p/401c2b324ede809585d3d1907c194df9`; Portal Visual 2.5D `https://app.notion.com/p/405c2b324ede81eb80cfecc4ba47abdb`; Orc `https://app.notion.com/p/405c2b324ede816ca88af5f66f103a2a`; Capríleo `https://app.notion.com/p/406c2b324ede81f38af7f3f620baf05c`; Besta Cristalina `https://app.notion.com/p/406c2b324ede81859909cf00a5031609`; Sistema de Combate `https://app.notion.com/p/3ebc2b324ede81f1be4be8804ac113c0`. Verifique vigência, páginas-filhas e checkpoints mais recentes; o pacote ZIP local pode conter versões binárias mais novas que descrições históricas do Notion.
3. **MESTRE ↔ PARTY separados.** Nenhum conteúdo MESTRE-ONLY em páginas das players, O Primeiro, GitHub público, sites ou serviços externos sem autorização específica. Evite envio de dados privados a terceiros. Testes são feitos com fixtures sintéticas TEST. Não altere o VLAB nem reivindique autoridade sobre dano, PA, turnos ou efeitos oficiais.
4. Use as convenções visuais existentes, em vez de recriá-las: `PV-2.5D-QUAL-03` (detalhamento/resolução nativa); `PV-2.5D-BIB-04` (custódia incremental após aprovação); `PV-2.5D-ANG-01` (vistas estáticas); `PV-2.5D-MOV-02 v1.1` (caminhada: **uma direção por linha, leitura temporal esquerda→direita**); `SEQ-ROW-MAJOR-SEM-RÓTULOS` (ataques podem continuar na linha abaixo); `CODEX-INDEPENDENT-SHEET-QA-01` (você audita pranchas integrais independentemente); e, quando relevante, `HITBOX-FOOTPRINT-IRREGULAR`.
5. **Não destrua o trabalho existente.** Inventarie ANTES; faça backup/checkpoint com hashes; trabalhe em subdiretório, cópia ou branch isolada; preserve projeto HTML anterior, saves existentes e fontes gráficas originais. Mudanças irreversíveis, publicação, credenciais, compras e sobrescrita canônica ficam fora deste mandato. Registre ANTES→MUDANÇAS→DEPOIS e readback. A autorização é ampla para implementação e testes locais seguros, não para apagar ou publicar.
6. A circular anterior dizia “não execute”; essa restrição era para o mero microteste de contextualização. **Esta mensagem nova substitui somente aquela espera e autoriza expressamente a execução do trabalho aqui descrito**, sem suspender as salvaguardas superiores.

## C. DESCOBERTA DO NOTEBOOK E DAS FERRAMENTAS — SEM SUPOSIÇÕES

O caminho informado por outro Comestre, ainda sujeito a confirmação física, é:
`C:\Users\Antônio Tiburtino\OneDrive\Área de Trabalho\RPG Assimilação`

- Verifique `Test-Path -LiteralPath` e liste subpastas antes de escrever. Se o caminho tiver sido redirecionado por OneDrive ou mudado, procure somente em locais plausíveis (Desktop/Área de Trabalho, Documents/Documentos, OneDrive, pastas já conhecidas) e confirme pela estrutura/arquivos de origem; não invente outro projeto nem faça varredura destrutiva no disco inteiro.
- Localize o protótipo entregue (~59 MB), READMEs e instruções, `index.html`, pacotes web, arquivos de teste, `project.godot`, `.blend`, `.gltf/.glb`, manifestos e relatórios; registre seus caminhos reais. Identifique projetos diferentes e o projeto-base antes de modificar algo.
- Localize Blender e Godot pelo PATH, atalhos e instalações usuais, sem deslocar executáveis. Confirme versões efetivas via `--version`; há um relato prévio de **Blender 5.2.3 PASS** e **Godot 4.7.2 PASS** (execução por comandos, salvamento/reabertura de cena Blender, criação/validação Node2D Godot). Isso é contexto histórico, não comprovação atual. O teste de controle visual por mouse/teclado foi **PARCIAL** por timeout; não dependa dele. Prefira CLI/scripting e use interface gráfica apenas se funcional.
- Exemplos de reconhecimento PowerShell **somente leitura**, adaptando ao ambiente: `Test-Path -LiteralPath $root`; `Get-ChildItem -LiteralPath $root -Force`; `Get-Command blender,godot -ErrorAction SilentlyContinue`; `where.exe blender`; `where.exe godot`. Utilize o caminho real para chamar `blender --background --python SCRIPT.py` e `godot --headless --path PASTA_DO_PROJETO --import`; verifique ajuda/flags na versão instalada antes de rodar.
- Encontre na pasta principal a subpasta chamada aproximadamente `ideia de referências de animações`, `ideias de referências de animação` ou variação próxima. Faça inventário com nomes, extensões, tamanhos, licenças e formatos, sem executar arquivos desconhecidos automaticamente. Diferencie projeto-fonte, vídeo, FBX/GLB/BLEND, animação, shader e código. Não importe assets externos cegamente nem tome material alheio como autorização de redistribuição.
- Se NÃO tiver acesso real ao notebook, à interface, aos comandos ou aos arquivos neste ambiente Codex, deixe isso explícito. Trabalhe sobre o repositório/arquivos realmente acessíveis, gere scripts reproduzíveis e um pacote executável possível; nunca invente comandos rodados, caminhos encontrados ou screenshots.

## D. REVISÃO INDEPENDENTE DOS TRÊS ACERVOS VISUAIS

**O ZIP é insumo técnico e artístico, não licença para aceitar todo frame como perfeito.** Descompacte em área privada de trabalho, preservando ZIP original e PNGs byte a byte. Leia o manifesto e confira hashes SHA-256, dimensões, RGBA verdadeiro, transparência (inclusive halos/quadriculado pintado), margens, separação de células, sequência, geometria, consistência de câmera e artefatos. Não edite originais. Produza somente derivativos identificados.

**ORC — PILOTO HUMANOIDE:** compare oito vistas, ataques com machado, referência das armas e cabeça de lobo sobre o ombro anatômico esquerdo. A arte aprovada representa um Orc já vestido/equipado; isso NÃO é um rig modular pronto e não revela automaticamente a anatomia sem armadura. Use como visual-alvo para construir um protótipo de corpo-base e equipamento separado. Não existe uma sprite sheet de caminhada do Orc aprovada neste acervo: ela foi deixada intencionalmente como desafio de produção. Gere o movimento por rig/animação se viável e compare com referências, sem alegar que houve animação oficial anterior.

**CAPRÍLEO ESCAMOSO OURO 1★ — QUADRÚPEDE:** preserve o corpo reptiliano de porte felino robusto, quatro patas, cauda espessa articulada, juba clara, fileira de espinhos e chifres gigantes espiralados com geometria original; nunca confunda com Ouro 4★ Titã. Examine as duas pranchas de ângulos, ataque de rabada, ataque de corrida curta/salto/cabeçada, quatro pranchas de caminhada (2×5, 2×5, 2×4, 2×4) e JPEG de referência. Biomecânica leonina: marcha quadrúpede com apoios alternados, transferência de peso, movimento de ombros/quadril, juba e cauda; evite patas desaparecendo e poses sem continuidade. Arte dos ataques/caminhadas aprovada artisticamente ≠ loop, impacto ou alfa tecnicamente homologado. A biblioteca já assinalava possível pendência no alfa de uma prancha — verificar de forma independente.

**BESTA CRISTALINA — ANATOMIA PRÓPRIA:** leia especialmente o manifesto e status da versão efetivamente enviada, que pode ser v009 ou posterior. Estude vistas, ataques, partes sequenciais e animações; identifique partes corporais, juntas reais, articulações não humanoides, deslocamento, ataques e VFX. Respeite a cronologia de efeitos, inclusive projétil/impacto quando existirem. Não transforme estudo gráfico em mecânica, e preserve alertas de QA (inclusive eventuais problemas em caminhada lateral). Não force a criatura ao esqueleto humanoide do Orc.

**RELATÓRIO OBRIGATÓRIO DE AUDITORIA:** para cada ativo, registrar fonte exata, hash, papel, status artístico, utilidade para modelagem/rig/ataque, limitações, direitos de uso quando conhecidos, e decisão `UTILIZAR / ADAPTAR / SOMENTE REFERÊNCIA / HOLD`, com motivo. Codex faz a extração definitiva, detecção de células, pivôs, hitboxes visuais, comparação de poses e preview; recortes auxiliares já existentes não substituem análise da prancha integral. Não coloque números, nomes, etiquetas ou linhas dentro dos pixels finais.

## E. PROPOSTA CENTRAL DO MESTRE — ESQUELETO REUTILIZÁVEL E CAMADAS

**Problema real:** haverá muitos humanos/NPCs, roupas e armas. Não é sustentável desenhar manualmente uma animação inteira por personagem e equipamento. Construa um sistema que compartilhe a lógica de animação, sem tornar todos os corpos artificialmente idênticos.

**Modelo lógico-alvo (não confundir com mero overlay de PNG):**
`ARQUÉTIPO / RIG BASE → CORPO/PERSONAGEM (malha e skinning) → EQUIPAMENTOS (malhas e sockets/bones) → ANIMAÇÃO (bibliotecas reutilizáveis) → COMPLEMENTO PROCEDURAL (IK/adaptações) → REPRESENTAÇÃO 2.5D (tempo real e/ou sprites prerenderizados)`.

**Prova de conceito prioritária: rig humanoide compartilhável.** Crie pelo menos uma armature de humanoide compatível com variações proporcionais, nomes estáveis de ossos, pose de descanso, root/hips, coluna, cabeça, braços, pernas, mãos e sockets de equipamento. Construa dois visuais distintos usando o MESMO esquema de animação: um manequim/base de desenvolvimento e uma versão Orc inspirada no acervo. Mostre a possibilidade de trocar corpo/roupa/armadura e arma sem refazer a caminhada. No Orc, respeite assimetria da pele de lobo, a arma volumosa e as limitações de sua vestimenta.

**Movimentos básicos compartilháveis (biblioteca incremental):** idle/respiração, caminhada, corrida curta, parar/virar, defesa, receber golpe, errar ataque (whiff), golpe genérico sem arma, espada, machado, arco (sacar/apontar/disparar/recuperar), conjuração genérica (antecipação/emissão/recuperação), esquiva se viável, cair, levantar e morte. Não prometa finalizar tudo se não houver qualidade; implemente um conjunto vertical demonstrável primeiro e liste o restante com prioridades. Cada animação precisa de antecipação, execução, follow-through e recuperação quando pertinente, sem slides nos pés ou clipping severo. Ataques específicos continuam podendo ter rigs/animações exclusivos.

**Armamentos e camadas:** mesh/material/corpo intercambiáveis; capacetes/peitorais/luvas/botas ligados ao rig ou ossos apropriados; armas com sockets por mão; hierarquia de renderização, oclusão, proporção e colisão preservadas. Roupa rígida pode acompanhar ossos; tecido/capa precisa de solução própria. Troca de item não deve deformar a arma, inverter ombros ou fazer o escudo entrar no corpo. Prove com pelo menos uma troca visual em runtime ou demonstração reproduzível.

**Procedural não significa “tudo gerado por código”:** compare keyframes + blending com ajustes procedurais como IK para pés, look-at, mira, apoio no solo, desaceleração, orientação, respiração e inércia secundária. Evite usar procedural para substituir indiscriminadamente coreografia de ataque. Use animações autorais no Blender como base e programação para adaptações contextuais; avalie retargeting real entre rigs compatíveis. Um esqueleto humanoide NÃO deve ser compartilhado automaticamente com quadrúpedes, criaturas cristalinas ou anatomias serpentinas. Crie **famílias de rigs** (humanoide, quadrúpede, especial) conforme necessário, com contrato comum de estados e eventos, mas ossaturas específicas.

**Arquiteturas a comparar antes de travar a escolha:**
1. 3D em tempo real no Godot, com modelos low-/mid-poly estilizados, animações retargetáveis, câmera 2.5D e exportação web.
2. Blender 3D para modelagem/animação e renderização de sprites 2D de oito direções (estilo Hades 1), importados no motor; maior controle sobre visual/pixel art, mas custo de quantidade de sprites/equipamentos.
3. Híbrida: cenário 3D/2.5D + atores 3D selecionados + sprites/efeitos prerenderizados; ou rig 3D como fonte autoritativa e exportação de 2D para NPCs/perfil de desempenho.
Compare qualidade, peso do download, CPU/GPU, compatibilidade navegador, velocidade de trabalho, extensibilidade dos equipamentos, retargeting, oclusão e custo de armazenamento. Decida pela alternativa que apresentar melhor prova no notebook, com justificativa e possibilidade de fallback. **Não há obrigação de transformar todas as PNGs existentes em malhas 3D automaticamente:** vistas estáticas não fornecem geometria 3D exata de áreas ocultas.

## F. BLENDER → GODOT → WEB: IMPLEMENTAÇÃO REAL

1. Abra o Blender efetivo; escreva scripts Python versionados para criar/alterar uma cena de teste, rig(s), meshes simples porém proporcionais, objetos separados, armaduras, skinning, sockets e animações. Salve `.blend` editável e exporte `.glb/.gltf` com animações, se escolhido; reabra os artefatos e valide no Blender em modo batch, não apenas pelo retorno do processo.
2. No Godot efetivo, crie ou aproveite o projeto de integração **em área isolada**, sem substituir às cegas o protótipo HTML. Importe o GLB, examine `Skeleton3D`, `AnimationPlayer`, `AnimationTree`, retargeting/BoneMap e bibliotecas de animação. Teste a mesma biblioteca em ao menos dois corpos humanoides compatíveis, e um objeto/arma anexada. Use GDScript e o renderer **Compatibility/WebGL 2.0** para compatibilidade com navegador em Godot 4; não assumir que C#/.NET pode ser exportado para HTML5 em Godot 4. Verifique suporte de templates de exportação instalados e particularidades da versão local.
3. Exporte uma **versão web real**, sirva por HTTP local, abra no navegador e teste cena, controles, animação e eventuais mensagens de console. Se exportação falhar, diagnostique e conserte; se houver bloqueio estrutural, conserve o HTML funcional anterior como entrega jogável e demonstre o protótipo Godot separadamente. Não invente URL pública.
4. Automatize testes CLI/CI e um smoke test visual onde houver ambiente/browser disponível. Capturas de tela, vídeo curto ou GIF são úteis como evidência auxiliar, mas NÃO substituem projeto executável nem arquivos-fonte. Forneça instrução de inicialização em PowerShell para o Mestre com o caminho encontrado. Evite depender de Computer Use visual se timeouts persistirem.

Documentação técnica oficial para consulta por versão instalada: Blender `https://docs.blender.org/manual/en/latest/animation/armatures/`; Godot AnimationTree `https://docs.godotengine.org/en/stable/tutorials/animation/animation_tree.html`; retargeting `https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/retargeting_3d_skeletons.html`; importação 3D `https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/import_configuration.html`; exportação Web `https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html`. Checar compatibilidade com versões exatas do notebook.

## G. REFERÊNCIAS ADICIONAIS DO MESTRE — PESQUISA CRÍTICA

- Analise o diretório local de **ideias/referências de animações**, documente uma matriz de utilidade e, somente quando houver licença/permissão, qualidade e compatibilidade, aproveite elementos como referência ou material adaptado. Não copie asset de terceiro para build distribuível sem direito adequado; não execute scripts desconhecidos sem auditoria.
- Localize o material do **MMORPG criado com IA pelo criador dos vídeos de referência** entre os links, notas e arquivos já fornecidos. Verifique a explicação exata usada por ele para rig, animação procedural, keyframes e movimentos; **não atribua ao autor detalhes técnicos que não foram efetivamente conferidos**. Se os vídeos não estiverem acessíveis, registre a lacuna, aproveitando o conceito técnico sem inventar transcrição.
- **Hades 1:** o desenvolvedor relatou uso de modelos/personagens 3D animados durante a produção e pré-renderização para quadros 2D em múltiplas direções, não renderização 3D dos atores em runtime. Use como inspiração de pipeline, não como promessa de repetir a produção comercial integral. Referência primária: `https://steamcommunity.com/app/1145360/discussions/0/1738883810796606862/`.
- Referências estéticas adicionais do Mestre: Enigma do Medo / Threads of Time (atmosfera e acabamento), Hades 1 (peso e fluidez), League of Legends e Baldur's Gate 3 (clareza de leitura, interação, enquadramento e impacto de combate). **Direção criativa, não instrução para copiar marcas ou assets nem exigência impossível de reproduzir jogos AAA integralmente nesta etapa.**

## H. PRIMEIRA CENA VISUAL DE JOGO — FLORESTA SEM BORDA VISÍVEL

Entregue uma pequena **arena florestal 2.5D jogável** como fatia vertical de qualidade. É uma cena/tilemap/ambiente delimitado LOGICAMENTE para gameplay; NÃO é mundo aberto. O jogador **não deve enxergar o fim abrupto do mapa** nem uma parede preta/quadrada/linha de corte da geometria.

- Use continuidade visual do mundo além do limite jogável: árvores de fundo, montanhas distantes, névoa atmosférica, colinas, múltiplos planos/parallax, vegetação e enquadramento da câmera. Escolha entre composição 2D, geometria 3D ou híbrida, favorecendo desempenho web.
- Mantenha limites reais de navegação e colisão seguros sem mostrar uma borda artificial; use desenho natural da cena (floresta densa, água, penhasco, trilha que dobra, transição para outra cena) e câmera que não revele o vazio. Não confunda “horizonte infinito” com tamanho físico infinito.
- Priorize visual: folhagem detalhada, troncos, sombras de contato, camadas de profundidade, oclusão de árvores diante do personagem, escala consistente, câmera cerca de 35° quando compatível com a proposta, leitura clara de passos e ataques e alvo de teste simples.
- Inclua ações mínimas visíveis: mover, virar, atacar, ataque que erra, bloqueio/defesa, receber dano, estados básicos e HUD TEST discreta. Dados de Vida/Alma são sintéticos, separados das regras canônicas. O jogo deve continuar utilizável mesmo com visual ainda em evolução.
- Meça tempo de carga, frame rate razoável no notebook, consumo de memória, tamanho exportado e comportamento no navegador; registre gargalos e otimizações de texturas, instancing, luzes, partículas e LOD apropriadas. Não sacrifique silenciosamente os originais para reduzir peso.

## I. CONTRATO DE EXECUÇÃO E PRIORIDADES — CONTINUE SEM RECOMEÇAR

**Etapa 0 — Baseline real:** localizar arquivo/protótipo do checkpoint informado, abrir no navegador e conferir a batalha; mapear estrutura e testes preexistentes; backup/branch; registrar ANTES, comandos, versões e caminhos; não repetir testes irrelevantes.

**Etapa 1 — Pesquisa aplicada e auditoria de assets:** abrir ZIP unificado, verificar hashes, examinar pranchas íntegras, identificar arte aprovada e riscos técnicos; inventariar materiais locais de animação e vídeo; fazer curta matriz de decisão das 3 arquiteturas. **Não pare após entregar a matriz:** ela informa implementação imediata.

**Etapa 2 — Prova reutilizável real:** criar rig humanoide editável, duas aparências, pelo menos caminhada/idle e uma ação de ataque, com troca de arma ou equipamento; fazer preview e export/import Blender↔Godot comprovados; documentar o experimento procedural/IK se viável. Não exigir que o Orc original ganhe um modelo final perfeito antes de testar o sistema.

**Etapa 3 — Fatia vertical web jogável:** inserir personagem/rig animado ou equivalente testado em floresta, câmera 2.5D e ações básicas; exportar/rodar Godot Web ou integrar de forma segura ao protótipo HTML se esta for a opção tecnicamente superior; executar regressões e registrar prova visual. Preferir produto funcional com escopo explícito a um protótipo grande que não abre.

**Etapa 4 — Encerramento rastreável:** README do Mestre para abrir/usar, arquivos fonte `.blend`, scripts e projeto Godot, pacote web/HTML jogável, README do Codex, inventário/hash, matriz de análise das três bibliotecas, resultados de testes, problemas e FIRST-PENDING. Se houver acesso/escrita autorizada no Notion, atualize **a página existente apropriada**, leia de volta e indique link. Não crie múltiplas páginas redundantes. Se não houver acesso, forneça checkpoint pronto para registro. Não publique Party nem GitHub público.

## J. GATES MÍNIMOS DE ACEITAÇÃO

- Produto anterior preservado, baseline localizado e testes relevantes sem regressões ocultas.
- Pelo menos uma demonstração **executável** de duas aparências/corpos humanoides usando movimento compartilhado, e equipamento trocável, ou bloqueio técnico honesto com evidência e alternativa concreta.
- Arquivo Blender recuperável + exportação de personagem/animação analisada; importação Godot testada onde acessível.
- Floresta demonstrável no navegador com movimento e ações básicas; sem bordas visíveis ou renderização terminando no vazio. Se indisponível, explicar precisamente qual pré-requisito falta e entregar o melhor build executável existente.
- Auditoria independente registrada para as 3 bibliotecas, com nenhum PNG original modificado.
- QA de sprites: transparência real, quadros na ordem correta, sem textos desenhados, chifres/armas/anatomia consistentes; não converter arte-estudo em asset final sem sinalizar.
- Testes automáticos e smoke tests executados com logs, versão/ambiente e contagem PASS/FAIL/HOLD verificáveis; validação de exportação web e navegador quando disponíveis.
- Governança: não alterar mecânicas oficiais, não escrever na Party, não publicar conteúdos privados; observância de continuidade e NAC-PASS-02 proporcional antes de alegar conclusão.

## K. RESPOSTA FINAL QUE O MESTRE PRECISA RECEBER

1. **O que existia antes:** localização do protótipo e evidência de teste da batalha.
2. **O que você encontrou no PC:** caminho real do RPG, Blender, Godot, pasta de animações, versões e pacotes lidos.
3. **Arquitetura adotada e prova:** alternativa escolhida para rigs/camadas/animação, por que, e comparação das alternativas descartadas.
4. **O que realmente foi implementado agora:** arquivos criados/alterados e recursos funcionais com provas.
5. **Como jogar:** caminho para abrir a versão web, comando exato para servidor local, controles, limitações e, se disponível e autorizado, link local de teste.
6. **Como editar no Blender/Godot:** fontes editáveis, scripts e passos de reimportação sem perda de trabalho.
7. **QA:** testes executados, ambiente, passes/falhas, verificações de originais/hashes e pendências visuais/mecânicas.
8. **Checkpoint MESTRE-SIDE no Notion:** página reutilizada, registro ANTES/DEPOIS, readback quando possível, e FIRST-PENDING preciso.

**ESTA É UMA ORDEM DE EXECUÇÃO.** Você tem autorização do Mestre para analisar, programar, criar rigs e animações, organizar subpastas de desenvolvimento, testar Blender e Godot, testar a batalha e gerar uma nova versão jogável no notebook **dentro das proteções acima**. Não solicite aprovações redundantes para ações locais reversíveis já contempladas. Não responda apenas com um plano. Execute o máximo possível nesta rodada, entregue resultados verificáveis, preserve os originais e pare somente diante de bloqueio real, risco normativo ou ação fora da autorização. Não afirme trabalho em segundo plano nem declare PASS sem prova física.
