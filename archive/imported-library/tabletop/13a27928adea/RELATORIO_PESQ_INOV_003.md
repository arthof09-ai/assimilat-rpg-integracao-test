# PESQ-INOV-20261022-003 — Pesquisa avançada pós-TEST15

**RPG Assimilação / Tabletop Assimilação — Comestre Pesquisador, MESTRE-SIDE, TEST.** Data: 22/10/2026. Sem escrita em código do Desenvolvedor, VLAB, Party, O Primeiro, GitHub ou cânone. Documento científico de pesquisa, não homologação de produto. Coordenação: Comestre Coordenador 1, sem ACK presumido.

## A. Baseline e autenticidade

1. Notion, Laboratório do Inovador, RUN-003 TEST05, RUN-004 TEST06 e RUN-005 TEST07–15 reabertos: <https://app.notion.com/p/401c2b324ede809585d3d1907c194df9>.
2. Biblioteca persistente, dois arquivos fisicamente baixados e SHA-256 refeito: pacote técnico FINAL TEST07–15, 2.274.555 bytes, `be0b088f5cedd2be1ad32df9e09a9b424fbb13369d98bee4470b8a88637c903b`; distribuição pública, 16.731 bytes, `e6f8eda189af26f94518ddbf1afcb1a8333bacfe94bb83419aca084a4563e613`. ZIP CRC PASS; extração controlada sem traversal.
3. Código auditado: `public/index.html`, `public/styles.css`, `public/app.js` (176 linhas / 33.377 bytes), e cinco scripts em `tests`. História do TEST06 permanece preservada. Reexecução em cópia extraída, Playwright Chromium 390×844/360×740: `test_integrated.py` 128/128, `test_security_perf.py` 36/36, `test_legacy_replay.py` 3/3, `test_ui_real_clicks.py` 18/18. **Total reexecutado 185/185, testes escritos originalmente pelo Desenvolvedor**. Não significa 185 testes novos criados por este Pesquisador, nem teste Android físico.
4. Já implementado: render diferencial, BFS por origem, Pointer Events, zoom, minimapa, editor, tokens dinâmicos, até oito cenas, undo/redo, localStorage, JSON backup, replay sintético. **Não recomendar como novidades.**

## B. Auditoria real: defeitos reproduzidos, oportunidades e patch isolado

| Local observado | Evidência nesta execução | Impacto | Correção sugerida ao Desenvolvedor | Aceite |
|---|---|---|---|---|
| `app.js` `#restore` handler (linha 170), `saveLocal` (linha 37) | Importação validada troca `workspace` antes de `saveLocal()`. Ao lançar `QuotaExceededError` simulado, a aplicação afirma “Backup sintético validado e restaurado”, mas o estado não fica persistido; nova sessão volta à cena anterior/default. Reprodução adversarial no Chromium com storage substituto: PASS de observação. | **P0: perda de alteração após recarga e falsa confirmação visual.** Não comprovado em Android físico. | Persistir backup validado antes de publicar a mudança em memória; verificar retorno da gravação, falhar sem trocar workspace; preservar backup antigo/exportação explícita. Exemplo `patch_restauracao_sugerido.js`, 4/4 verificações Node independentes. | Quota/falha de escrita rejeita restauração sem alterar cena nem exibir sucesso; reload mantém estado anterior; caso normal persiste novo estado. |
| `validateScene`, linhas 32–34 | `frameTopology` é aceito se for qualquer string: valor adulterado `tampered` passou. | P1 integridade de replay; pode desassociar histórico da topologia. Não provado dano em cena. | Recalcular assinatura topológica dos frames/grade; versionar e rejeitar divergências. | Fixture adulterada recusada; fixture válida preservada. |
| `validateReplay`, linhas 147–149 | IDs únicos aceitos em ordem arbitrária; evento inserido `frame-000` antes de `frame-001` sem contrato de causalidade. | P1, inconsistência se futuro adaptador depender de IDs ordenados. Não prova falha do replay visual sintético atual. | Adicionar `sequence` numérico ordenado no schema futuro ou esclarecer que ordem é o índice do array e ignorar ordenação lexical de IDs; validar sem inventar eventos VLAB. | Contrato explícito rejeita sequência duplicada/regressiva; replay legítimo TEST03 ainda passa. |

Testador adicional `audit_test15.py` (com CSP removida **somente na montagem da bancada**, semelhante ao harness original) executou **8/8 verificações de comportamento observado**. Esse PASS é observação de cenários, **não sinal de ausência de bugs**. O site distribuído conserva sua CSP original; não removê-la em produção.

## C. FOV — três algoritmos, dez cenários, 4 escalas

**Não implementado no TEST15.** Fontes examinadas: <https://www.albertford.com/shadowcasting/> (algoritmo Symmetric Shadowcasting publicado CC0), <https://roguebasin.com/index.php/Shadow_casting> e <https://chizaruu.github.io/roguebasin/fov_using_recursive_shadowcasting>. Módulo independente `fov_research.py` implementa Bresenham/LOS por célula, Recursive Shadowcasting octantes e Symmetric Shadowcasting racional em quatro quadrantes. Entrada `(width,height,walls,origin,radius)`, saída `visible_now: set[tuple[int,int]]`; helper `explored_update(old,current)` preserva descobertas anteriores. Não transmite dados da Party.

Cenários determinísticos: sala retangular, corredor, parede isolada, corredor em L, porta, obstáculos diagonais, canto interno, canto externo, origem junto à parede e campo aberto. Grades 20,30,50,70; raios 8,12,18,24; 55 execuções temporizadas por combinação; mediana e p95 completos em `BENCH_FOV_PESQUISA.json`. 912/912 invariantes de origem, alcance, limites, amostras de simetria de piso e separação explorado/visível PASS. Não são 912 cenas independentes.

**Medianas de medianas Python, em ms (menor melhor; não Chrome Android):**

| Grade | Bresenham | Recursive | Symmetric racional |
|---|---:|---:|---:|
| 20×20 | 0,275 | 0,158 | 1,120 |
| 30×30 | 0,828 | 0,330 | 2,240 |
| 50×50 | 2,555 | 0,696 | 4,367 |
| 70×70 | 5,553 | 1,246 | 7,794 |

**Escolha recomendada — P0:** prototipar **Symmetric Shadowcasting** para semântica previsível e simetria entre casas livres; comparar com Recursive como referência de desempenho no Chromium Android. Não importar a implementação Python racional como módulo produtivo JS nem decidir regras de visão, portas, iluminação, raio, furtividade ou LOS canônico. Diferenças de visibilidade ao redor de cantos/colunas são **políticas geométricas**, não defeitos automaticamente. Experimento de aceitação: posição A vê B se e somente se B vê A (ambas casas livres e mesmo raio suficiente); obstáculo bloqueia além da parede; 7×7/20×20 e 50×50; `visible_now` vs `explored`; testes após girar câmeras e mover unidade; nunca enviar estado Mestre ao cliente Party.

## D. Escalabilidade e caminhos

Benchmark Python sintético (não motor TEST15): 75 buscas por tamanho, cenário conectado fixo, BFS por origem para **todos** destinos contra A* Manhattan para **um** destino. Mesmo comprimento nos 300 pares e invalidação de parede no caso adicional: **301/301 verificações PASS**. Medianas Python (ms):

| Grade | BFS todas as casas | A* um alvo |
|---|---:|---:|
| 20×20 | 0,241 | 0,099 |
| 30×30 | 0,594 | 0,242 |
| 50×50 | 1,846 | 0,652 |
| 70×70 | 3,514 | 1,272 |

A* explora menos nós porque executa tarefa menor; não interpretar como ganho garantido de 2–3× sobre a implementação real. **BFS existente continua recomendado para camada visual de todas casas alcançáveis.** A* por destino só depois de medir gargalos em mapas grandes. Invalidação de cache sempre que mapa/obstáculo/token/fonte do custo mudar; vincular chave a versão topológica. Custos heterogêneos exigem Dijkstra/A* admissível, não BFS sem peso.

Bancada isolada Chromium 390×844 (não TEST15 ampliado): 35 amostras de atualização DOM completa (atributos), patch de seis células e Canvas 2D `fillRect` em 20²,30²,50²,70². Medianas DOM completa 0,2 / 0,4 / 1,2 / 2,2 ms; Canvas 0,1 / 0,1 / 0,4 / 0,7 ms. Patch de seis células frequentemente abaixo da resolução do cronômetro (mediana registrada 0,0 ms, não tempo nulo). Ver `BENCH_ESCALA_CAMINHOS_VISUAL.json` para p95. Canvas demonstra potencial de rasterização, **mas não inclui hit-test, acessibilidade, tokens, editor e UX**; não autoriza migração. TEST15 rejeita grades acima de 20 pelo schema atual: cenários maiores foram **bancadas independentes**.

## E. GitHub Pages — recomendação de publicação sem deployment nesta pesquisa

Conexão GitHub consultada: <https://github.com/arthof09-ai/assimilat-rpg-integracao-test> **repositório PUBLIC real**, branch padrão `main`, acesso de leitura e permissões de admin vistas na conta conectada, mas **sem autorização desta frente para publicar**; busca por `gh-pages` e `pages` retornou zero branches. README ainda descreve GitHub “privado”: documentação histórica desatualizada em relação ao estado real. Nenhum workflow alterado.

Procedimento sugerido para o Desenvolvedor/proprietário (fonte [GitHub Pages — publishing branch](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)):

1. Pré-publicação: validar o ZIP público de 3 assets pelos hashes e varrer URLs/segredos; é demo *somente sintética*. Preservar `main`, workflows, PRs e propostas existentes.
2. Criar branch `gh-pages` dedicada, sem mexer na `main`. Para manter somente três arquivos servidos, usar diretório `docs/` na branch `gh-pages`, contendo **apenas** `index.html`, `app.js`, `styles.css` do ZIP público. Arquivos do repositório fora da pasta de publicação não são parte do site; ainda assim revisar a exposição do repositório como um todo, que é público. Alternativa para publicador com Git: branch órfã só com os três arquivos no root.
3. Proprietário com permissão de Settings acessa `Settings > Pages > Build and deployment > Source: Deploy from a branch > Branch: gh-pages > Folder: /docs > Save`. Publicação por branch usa Pages com workflow gerenciado pelo GitHub; não criar workflow próprio desnecessário. Arquivos não precisam de servidor.
4. Conferir execução Pages Actions e URL fornecida por GitHub em Settings Pages; testar HTTPS, CSS, JS, criação de cena, backup e restauração depois de recarga no Chrome Android. URL previsível da modalidade projeto seria `https://arthof09-ai.github.io/assimilat-rpg-integracao-test/`, **não verificada como ativa** nesta pesquisa; tentativa de abertura via web falhou, sem afirmar status 404 ou deployment.
5. Atualização/reversão: cada release troca SOMENTE a pasta `/docs` nessa branch mediante diff/hash + smoke test; rollback pelo commit anterior da branch. Não alterar workflows VLAB/LEVEL-UP, nem configurar deploy de outra operação. Se precisar impedir transformações Jekyll, avaliar `.nojekyll` como exceção mínima ao requisito de 3 arquivos; não adicionado agora.

GitHub Pages é adequado ao estático e gratuito para repositório público conforme [Docs](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site); não fornece backend autoritativo nem sessão multiplayer. Passos em Chrome Android podem exigir modo site para computador para localizar os controles. Mudanças remotas não realizadas por esta pesquisa.

## F. VLAB — R205 materialmente recuperado

Biblioteca `/Comestre/OP-VLAB-FUSION-SANDBOX-01/` listada integralmente, 405 itens/entradas examinados; ZIP R205 encontrado e copiado. **SHA256 físico PASS:** `62a9851b3a5ae7919b9225d9379a3d32c8736448e76bfcea4729dcbfe933cead`, 20.800.905 bytes, 59 entradas ZIP, CRC PASS. Não executar runners históricos. Em SQLite aberto modo `ro&immutable=1`: **20/20 DBs**, tabelas `events`,`meta`,`pending`; `events` colunas `seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha`; 945 linhas reais, 120 meta, zero pendências de tabela. Todos DBs tiveram seq contínuo, cmd_id único por DB e cadeia `prev`→`row_sha` anterior. JSON interno `detail.new_native_events` 1.425 eventos e `detail.events_added` 1.387 eventos — **2.812 eventos físicos internos recontados**. `detail.attack` apareceu em 462 commits; ações internas incluem `turn_start`, `turn_end`, `weapon_attack`, cura/controle conforme pacote, marca de anel e reação; tipos exatos em `VLAB_R205_ROWJSON_FIELD_CENSUS.json`.

**Campos físicos observados:** `row_json.kind`, `payload.actor`, `payload.target`, `detail.attack`, `detail.next_turn`, `detail.resources`, `detail.new_native_events[].action`, `detail.new_native_events[].seq`, `detail.position_experiment`, `detail.new_native_events[].position_m`, `detail.intercepted.distance_m`. A posição `position_m=0` representa posição escalar da marca experimental; `distance_m=10.5` representa distância de reação, **não ponto [x,y]**. Nenhum objeto espacial completo `grid:{width,height,walls}` ou frames com quatro tokens foi identificado no censo R205. Não converter distância escalar em coordenada 2D. Contrato mínimo seguro ao Tabletop: somente leitura de sequência/ID/ação/ator/alvo e valores físicos já registrados, renderização textual sem movimento automático; validação de SHA/cadeia/readback, rejeição de evento desconhecido. Integrador de VLAB deve fornecer mapa ou coordenadas autênticas futuramente, em contrato adicional e com autorização do Mestre.

## G. Multiplayer preliminar — P2 somente pesquisa

**Mais simples futuramente:** servidor autoritativo com WebSocket em serviço apropriado, fatos/ações validados no servidor, projeções separadas para Mestre e Party e replay idempotente. **GitHub Pages não executa servidor.** Wi-Fi local dependeria de um host acessível e manutenção no aparelho/rede, mais difícil sem PC; servidor remoto facilita links mas implica hospedagem, autenticação e custos/uptime a avaliar; WebRTC DataChannel pode trocar dados diretamente após sinalização e NAT traversal/STUN/TURN, mas **não elimina autoridade do Mestre, sinalização ou eventual relé** ([WebRTC](https://webrtc.org/getting-started/peer-connections)). Web Bluetooth tem disponibilidade limitada e foca serviços GATT de periféricos, **não é alternativa preferida para salas browser-browser Android** ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/Bluetooth)). Nenhum servidor criado/implantado, nenhuma senha/autorização real testada.

## H. Encaminhamentos e próximo checkpoint

- **D-INOV-20261022-005 — P0/TEST15 persistência:** corrigir restore fail-closed + confirmar gravado antes de trocar workspace; executar regressões 185 e adversariais quota/reload.
- **D-INOV-20261022-006 — P0/FOV:** laboratório Symmetric Shadowcasting primeiro para simetria e quinas, contra Recursive como baseline de velocidade, explorar `visible_now`/`explored` na origem, sem Party.
- **D-INOV-20261022-007 — P1/performance/caminhos:** manter BFS e render diferencial; adicionar benchmark do código real a 30×30/50×50 numa cópia somente se mudança de schema for proposta pelo Desenvolvedor; estudar A* alvo único e cache invalidation.
- **D-INOV-20261022-008 — P1/Pages:** branch isolada `gh-pages` `/docs`, três arquivos públicos, publicar só com autoridade do Desenvolvedor/proprietário; testar URL real e rollback sem `main`.
- **D-INOV-20261022-009 — P1/VLAB:** schema R205 físico comprovado, preparar adaptador timeline de eventos reais sem quadro espacial e sem recomputar combate; acesso Mestre-only e autorização adicional para integração futura.

**NEXT:** Desenvolvedor decide integrar correção P0 de persistência e FOV numa cópia TEST16+, sem tocar originais por esta pesquisa. Pesquisador deve portar FOV demonstrativo para JS e testar Chromium com mapa 20×20/50×50 após decisão de semântica de cantos; seguir VLAB timeline read-only como proposta, sem publicar para Party; GitHub Pages só após preparação/autorização competente e verificação do site efetivo. **NAC-PASS:** integridade, pesquisa e testes delimitados PASS; PROD/Android real/Party/multiplayer/integração de motores = HOLD.
