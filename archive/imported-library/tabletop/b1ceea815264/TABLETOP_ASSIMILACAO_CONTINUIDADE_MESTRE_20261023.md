# TABLETOP ASSIMILAÇÃO — CONTINUIDADE DO MESTRE

**Checkpoint preservado:** 23/10/2026 (Brasil)  
**Identificador documental:** `CP-TABLETOP-SUCESSAO-20261023-001`  
**Responsabilidade:** MESTRE-SIDE / Comestre Coordenador, desenvolvimento pelo Segundo Comestre Inovador, pesquisa pelo Terceiro Comestre Inovador.  
**Natureza:** espelho portátil de continuidade. **Não substitui** o Notion, as regras canônicas nem os pacotes físicos do GitHub/Library.  
**Critério:** VERIFICADO / DECISÃO DO MESTRE / PROPOSTO / PENDENTE sempre separados.

## 1. Objetivo permanente e visão de produto — DECISÃO DO MESTRE

Criar **RPG Assimilação Interativo**, um tabletop tático de combate com visual **2D estilizado + recursos 3D harmônicos (2,5D)**, ambiente rico, boa iluminação, camadas, animações e som, inspirado qualitativamente em *Baldur's Gate 3*, *Enigma do Medo/Ordem Paranormal* e na proposta funcional de *Roll20*, **sem copiar** IP, personagens, sprites, assets, código protegido ou mecânicas de terceiros. Deseja interface significativamente mais bonita, clara e eficiente do que a experiência simples do Roll20 e adaptada a Android.

**V1, primordial:** arena de batalha, **sem história nem campanhas narrativas inicialmente**. Múltiplos mapas de combate, colocação de monstros e NPCs pelo Mestre, fichas originais, unidades, movimentação, turnos, ataques, ações, habilidades, magias, equipamentos e efeitos integrados ao **sistema canônico do RPG Assimilação**, não a regras inventadas. Os NPCs/monstros devem poder ser controlados manualmente ou por **IA tática competente**, capaz de escolher alvos, posicionamento, gasto de PA, defesa, suporte e decisões sob as regras oficiais. “IA experiente/treinada” é objetivo de qualidade; não existe certificação de tal motor no Tabletop hoje.

**MULTIPLAYER É CRITÉRIO BLOQUEANTE:** sessões presenciais, cada pessoa em seu dispositivo acompanhando e agindo na **mesma partida simultaneamente**. Preferencialmente funciona em Android + notebook pelo navegador; o Mestre aceita uma plataforma única se inevitável, mas prefere inclusão dos dois. A sala deve suportar Mestre, players, reconexão, ações autoritativas, sincronização por turnos, prevenção de disputa/double-submit e estado/permissões separados. Jogar presencialmente não elimina a necessidade de transporte de rede e autoridade compartilhada.

**Animações:** deslocamento, correr/pular, atacar/ser atingido, defesa, morte, gritos, efeitos mágicos, conjuração, transformação demoníaca e outras da campanha. Três controles de apresentação: CINEMÁTICO (completo), EQUILIBRADO (curto) e OBJETIVO (animações mínimas). A lógica e o resultado mecânico DEVEM ser idênticos entre esses modos. Não atrasar a prova multiplayer para produzir animações.

**Futuro, NÃO V1:** missões/quests controladas, explorações, labirintos, masmorras, eventos e campanhas; sem roteiro fixo predefinido nesta fase.

**Orçamento:** R$ 0 de despesa nova. Usar planos e equipamentos já disponíveis, ferramentas gratuitas/open source/recursos CC0 e limites gratuitos comprovados. O Mestre usa **celular Android** como principal e eventualmente acessa o notebook da noiva; não pode depender do notebook constantemente. Não solicitar assinatura extra, créditos, servidores pagos nem migrar para ferramenta proprietária por moda. PixelLab explicitamente EXCLUÍDO das opções de interesse do Mestre.

## 2. Decisões e regras de autoridade — VERIFICADO EM NOTION

- **A+C do FOV — APROVADA:** `DIR-MESTRE-D-INOV-032-FOV-AC-20261022-001`. A: marcadores administrativos continuam visíveis ao Mestre inclusive em áreas escondidas pelo campo de visão simulado. C: numa futura interface para players, enviar **somente projeções de dados autorizados**, antes de chegar ao cliente. Ocultação CSS nunca substitui autorização/filtragem. B, ocultar marcadores do próprio Mestre, NÃO é padrão. Decisão de aparência não altera regra canônica de combate/percepção.
- **Visão 2,5D e multiplayer** registrada em `DIR-MESTRE-TABLETOP-VISAO-ARENA-2P5D-MULTIPLAYER-20261023-001`.
- **Delegação técnica de publicação limitada:** `DIR-MESTRE-TABLETOP-PAGES-DELEGACAO-20261022-001`, somente branch pública sintética TEST no GitHub Pages; **não autoriza** publicar dados reais Mestre-only, Party, alterar `main`, outros motores ou sites.
- **Governança aplicável:** BOOTSTRAP-COMESTRE, NAC-CONT-03, NAC-NORM-01, NAC-PASS-02, LONG-RUN-01, REG-ROUTE-03, Diário Operacional e atribuições de Comestres. Nenhum motor, laboratório ou governança paralelos; NO-WRITE em Party, O Primeiro, VLAB, LEVEL-UP, DMG, CRAFT, PA e áreas alheias sem autorização competente. Distinguir fato, inferência, proposta, pendência. Notion e provas físicas acima de chat.
- **Fontes essenciais:** Laboratório do Inovador https://app.notion.com/p/401c2b324ede809585d3d1907c194df9 ; repositório https://github.com/arthof09-ai/assimilat-rpg-integracao-test ; site TEST https://arthof09-ai.github.io/assimilat-rpg-integracao-test/ .

## 3. Baseline física / software — VERIFICADO em 23/10/2026

- **RUN-010 último desenvolvimento publicado localizado:** GitHub Pages TEST32 na branch `gh-pages`, HEAD `0aa9bc817844fa4ce0e16a2103a3a89988df577c`; fluxo Actions `39845848140` completed/success verificado previamente; 3 arquivos públicos `index.html`, `styles.css`, `app.js`, dados sintéticos. Anterior rollback `c4b28b3d22170ac9e8a68bc5e64e5a7b70a9dc27`. O site HTTP direto em Chrome Android físico permanece **HOLD**, não extrapolar sucesso de deploy como usabilidade testada. GitHub Pages é **hospedagem estática, não é por si só um servidor de sala multiplayer**.
- **TEST33:** candidato separado ainda **NÃO PUBLICADO** na consulta atual. ZIP público `TABLETOP_SITE_SINTETICO_TEST33_CANDIDATE.zip` (28.752 bytes), SHA256 `25160fc798916d660d94b58e16bd43596c0f38ea2b4dcd55cd1d0f0c519d8c8d`; pacote técnico `PACOTE_TECNICO_TABLETOP_TEST33_20261022.zip` (72.801 bytes), SHA256 `aa85ba2647073d3707646e13dc4099d57b60d89fdc9da0b839d782af354768bc`. Código JavaScript TEST33 dentro do pacote SHA `7b1cce98bfcfc4e86ea5978472bfe5ce5e24b2d6827b284e342c2992e82faba4` segundo PESQ011.
- **PESQ009:** pesquisa independente identificou problemas de Refazer em operações sem efeito de marcadores/notas no TEST32.
- **RUN-010 TEST33:** Desenvolvedor relatou 6/6 RED→GREEN, 30/30 novos testes, 719/719 regressões e 1.500 entradas geradas e 12 mutações; números relatados pelo próprio executor, sem confundir com auditoria independente.
- **PESQ010:** auditoria independente de TEST33 **22/22 PASS** nos contratos examinados vs TEST32 **14/22 PASS** (8 falhas históricas esperadas); FOV 8/8 observações; aprovação CIENTÍFICA PROPORCIONAL do D-INOV-030, não homologação global. Pacote `PACOTE_PESQ_INOV_20261022_010.zip`, 20.572 bytes, SHA256 `f62565e34237b1bb4afd22f3c8ec99b868767aabf03c0a3c4e8a5ea16a4cc4c6`.
- **PESQ011:** 5/5 metadados/transcrições portuguesas próprias dos vídeos selecionados; 11 vídeos adicionais identificados em radar; benchmark científico de código, controle de handoff e testes sintéticos, sem alteração de produto. Pacote `PACOTE_PESQ_INOV_20261022_011.zip`, 26.514 bytes, SHA256 `c0dcd9e992b3259535abb055456c921583a0982f56c6919fada619a2cf918ead` em Library `/RPG-Assimilacao/Tabletop-Inovador/PESQUISAS-INOVADOR/`. Já existe `AGENTS.md` na branch `main`; **NÃO DUPLICAR**.
- **RUN011+ e multiplayer**: nenhum RUN novo encontrado no Lab na leitura de preflight desta consolidação; **0 prova de sala multiplayer real**, 0 integração canônica autorizada, 0 IA tática validada dentro do Tabletop, 0 APK do Assimilação produzido. Reabrir Notion/GitHub a cada nova sessão para checar mudanças.
- **Mecânica canônica do combate:** VLAB/LEVEL-UP e outras fontes oficiais detêm contratos; NÃO levar resultados ainda não homologados como regras do jogo. Integração progressiva somente por componentes aprovados e com verificações.

## 4. Direção de arquitetura — PROPOSTA, não decisão definitiva de engine

**Caminho preferencial:** evoluir o frontend **HTML/CSS/JavaScript/SVG já existente** para web responsiva que rode em navegadores Android e notebook, com opção PWA instalável; manter Godot como alternativa experimental e só justificar migração mediante benefícios medidos. Web/PWA não garante multiplayer por si só; a arquitetura requer uma sala de sessão com estado autoritativo, conexão bidirecional (WebSocket/WSS, ou protocolo adequado), autenticação/permissões, isolamento Mestre↔Party, replay/log, versão e reconexão. Proibir cálculo arbitrário do dano/PA pelo cliente não confiável. Ações chegam ao servidor, que consulta motor oficial validado, confirma evento e emite projeções separadas. Eventuais testes com estado sintético, sem acesso a fichas reais.

**Infraestrutura R$0 candidatos — ainda sem implantação/aprovação:** (1) Cloudflare Workers + Durable Objects SQLite Free, WebSockets com hibernação, limites gratuitos publicados; serviço sujeito a quotas/termos, não garantia de hospedagem ilimitada. (2) Supabase Realtime Free, limitado a 200 conexões simultâneas e 2 milhões de mensagens/mês declaradas em documentação, também sujeito a limites, pausas, segurança e comportamento real. Pesquisador/Desenvolvedor deve comparar autenticação, autoridade de sala, custo máximo zero e possibilidade de perder conectividade. Alternativa de LAN local sem internet exige host ligado e segurança; notebook eventual da noiva NÃO deve ser dependência permanente. GitHub Pages pode continuar distribuindo frontend, mas não sincroniza clientes sozinho.

**Primeiro gate demonstrável de multiplayer:** uma sala TEST com 1 Mestre + 2 players sintéticos em aparelhos diferentes, criados com contas/dados TEST, mapa simples, turnos, movimento de tokens e mensagem de ação; reconexão; 100% de coincidência de eventos autorizados entre aparelhos; informação secreta ausente dos pacotes da Party **antes** da transmissão; nenhum gasto extra. Registrar vídeo/capturas/testes reais sem expor dados. Depois substituir ações sintéticas por mecânica oficial homologada. Sem querer fazer simultaneamente animações, exploração, multiplayer e todos os motores.

**Visuais 2,5D:** tiles/sprites com profundidade, sombras, camadas, luz, efeitos, idle/movimento/golpes, eventualmente shaders leves; harmonia 2D/3D sem contraste visual ruim, e controles de intensidade de animação. A apresentação não altera os resultados mecânicos. Para imagens, personagens, gritos, sons e músicas, usar recursos próprios/CC0/adequadamente licenciados; identificar origem/licença.

## 5. Godot e notebook — ESTUDADO, NÃO MIGRADO

Vídeo https://youtu.be/4Y3XZquie_4 (Sonecarox, “Seu primeiro jogo com Godot e ChatGPT: tutorial para iniciantes”), analisado por transcrição e breakdown visual: demonstra **Godot no Windows**, ChatGPT/Codex, mockup versus assets, projeto scene+GDScript, screenshot para prompts, importação e execução F6, movimento/interação e bug regressivo de personagem/animação. NÃO demonstra exportação APK/mobile/Web nem fluxo no Android. Fontes oficiais confirmam editor Android Godot e exportação Android em versões atuais, com UX experimental e mais limitações que desktop; licença MIT, sem custo do motor. Em notebook desenvolvimento mais confortável, mas o Mestre não tem acesso frequente. Godot poderia criar aplicativos móveis ou jogos web, porém não converte automaticamente o Tabletop HTML/JS existente. Não torná-lo dependência V1. https://godotengine.org/download/android/ ; https://docs.godotengine.org/pt-br/4.x/tutorials/export/exporting_for_android.html .

## 6. Vídeos e pesquisa IA aplicada — FONTES E STATUS

Cinco vídeos originais do Mestre, títulos/canais/transcrições confirmados por vidIQ pela Coordenação e posteriormente pelo Pesquisador (PESQ011). **Transcrições não são visualização integral nem código executado.**

1. https://youtu.be/jF53ziwjOX4 — Maurii IA: mesmo prompt usado para comparar ChatGPT/Codex, Gemini, Claude em roguelite. O criador indica prompt em https://rentry.co/63onyse5, cujo texto integral ainda NÃO foi recuperado. Método: contratos/teste de jogabilidade, evitar tomar opinião do criador como benchmark.
2. https://youtu.be/d4xETb1aoCo — Andrezitos: IA criando jogos/experimentos com GDD, riscos de cópia de IP, balanceamento e dependência de serviço.
3. https://youtu.be/uIAF73TlS18 — GQ Games: Combos, prototipação incremental por prompts, cenas, obstáculos, poderes, som; promoção/patrocínio e custos/portabilidade ainda não certificados.
4. https://youtu.be/CZ1IU-SkgTE — MagmaDev: GDD enxuto, documentação curta, AGENTS.md/handoff/journal, documentação oficial, anti-overengineering, não criar abstrações prematuras; integrar a governança EXISTENTE, não recriá-la.
5. https://youtu.be/0TvVgPdgQ6s — Sonecarox, **“Pedi um jogo à IA com um único prompt… e fui jogar”**, 14min58s, **transcrição integral em português recuperada novamente nesta consolidação**; análise detalhada na seção 7.

Radar PESQ011 inclui 11 outros vídeos sobre OpenAI Codex/ChatGPT criação de jogos, engines e repositórios. A maioria tinha apenas metadados; sem alegar transcrições ou prova de executabilidade. Pesquisador deve estudar sob escopo e orçamento existentes, sem gastar créditos extras. Registro prévio no Lab: `REF-INOV-VIDEOS05-TRANSCRICOES-RECUPERADAS-20261022-001`, `REF-INOV-RADAR-CHATGPT-CODEX-VIDEO-20261022-001`, PESQ011.

## 7. Análise solicitada especificamente: vídeo 0TvVgPdgQ6s — FONTE/transcrição versus verificação externa

**Fonte:** Sonecarox, demonstração de criação do protótipo **Horta Sitiada**, um tower defense inspirado na lógica de Plants vs. Zombies. O vídeo apresenta ferramentas, imagens de referências comerciais e demonstra o jogo depois de deixar um agente programador trabalhar. **Não é tutorial de multiplayer, nem prova de exportação Android ou processo de desenvolvimento pelo celular.**

**Ferramentas declaradas no começo da fala (segundo transcrição):**
- **Godot** (voz transcrita como “Gold Dot”): engine/estrutura do projeto; gratuita e open source MIT.
- **Claude Code** (transcrito como “Cloud Code”): agente principal de programação e integração local das ferramentas; criador menciona uso de modelo de maior capacidade para planejamento e outro para execução. **Não é obrigatório para o Assimilação**: preferir aproveitar ChatGPT/Codex já contratado, sujeito a limites do plano.
- **PixelLab:** geração/organização de sprites/imagens; **excluído por decisão do Mestre**. Substituir por assets CC0 próprios/disponíveis ou arte já autorizada, sem serviço extra.
- **Suno:** música de fundo; plano gratuito pode servir somente para uso não comercial conforme termos atuais; jamais presumir licença comercial gratuita.
- **ElevenLabs:** efeitos sonoros/áudio; plano grátis oferece geração, mas **licença comercial está em plano pago** segundo preços oficiais atuais; não é indispensável, não contratar.
- **Steam / screenshots de jogo conhecido:** referência de gênero/aparência, nunca licença para copiar assets/arte/personagens.

**Fluxo mostrado/relatado:** 1) Pesquisa jogos de referência tipo tower defense e captura frames de trailer, 2) dita um pedido natural e suficientemente específico: inimigos à direita, defesas à esquerda, várias fases, evolução de torres, progressão e poderes, 3) fornece screenshots ao agente, 4) informa e prepara conexões locais Godot e integração com serviços, 5) agente verifica o ambiente e créditos, gera código/assets, 6) criador deixa processo rodando e relata cerca de **duas horas** e **~3.600 linhas** geradas, 7) abre a build no computador e testa menu, música, história, plantas/towers, inimigos, ondas, recompensa de estrelas, upgrades e fases, 8) encontra falhas/limitações de animação e polimento, explica que protótipo demanda revisões.

**CUSTOS RELATADOS, NÃO GENERALIZÁVEIS:** o autor fala de assinatura e de cerca de **17% de sua cota semanal**, além de cálculo aproximado de dezenas de reais; isso depende de plano, modelo, ferramentas e metodologia dele, sem estabelecer custo do nosso projeto. O próprio vídeo indica que algumas integrações e créditos estavam previamente configurados; não é prova de construção totalmente gratuita/sem instalação/sem hardware. A versão apresentada é single-player e não prova fichas canônicas, sistema multiplayer, IA tática validada, exportação APK ou funcionamento no Android.

**Ganhos aproveitáveis R$0:** especificar em linguagem natural um MVP pequeno e testável; criar arquivos de código com agente; fornecer **referências de imagem legais** e verificadas; executar/testar o projeto; usar sons CC0; preservar versionamento, rollback e repositório; avaliar iterativamente mecânicas e UX; evitar dependência proprietária e manutenção impossível. A principal lição é integrar **programação + assets + áudio + testes** em uma cadeia incremental de desenvolvimento, sem copiar a stack paga e sem necessariamente adotar Godot.

**Alternativas legais gratuitas verificadas externamente:**
- Kenney RPG Base CC0: https://kenney.nl/assets/rpg-base
- Kenney 50 RPG sound effects CC0: https://opengameart.org/content/50-rpg-sound-effects
- Kenney Tiny Town CC0: https://kenney.nl/assets/tiny-town
- Gerar efeitos sonoros simples por código/Web Audio API; gravar áudio autoral do próprio grupo com consentimento (se útil) e arquivar licença/atribuição; música opcional na V1.
- Godot MIT: https://godotengine.org/license/
- Suno uso grátis não comercial: https://help.suno.com/en/articles/9601601
- ElevenLabs preços/licença comercial fora do grátis: https://elevenlabs.io/pt/pricing
- Infraestrutura experimental sem contratação: https://developers.cloudflare.com/durable-objects/platform/pricing/ ; https://supabase.com/docs/guides/realtime/pricing

**Risco de engenharia:** não reescrever o motor web JS/SVG atual para Godot sem comparar custo/benefício; o próprio vídeo adota um jogo local single-player, incompatível como prova direta do V1 multiplayer. Não importar sprites de Plants vs. Zombies ou copiar animações originais de terceiros. Não criar diálogo, história, missões ou áudio antes de demonstrar a sala de multiplayer básica.

## 8. Ordem de continuidade operacional — PRIORIDADES

**P0 — Proteção do estado:** conservar hashes e links; Notion+Library; readback; atualizações mínimas ao próprio Laboratório. Reabrir RUN e repositório para checar novos fatos; não duplicar fichas/labs/scripts/códigos.

**P0 — Prova de multiplayer R$0:** análise de viabilidade Cloudflare Durable Objects Free versus Supabase Realtime Free, ou equivalente gratuito; desenho de sessão autoritativa e protocolo de permissão; cópia TEST sintética com 1 Mestre + 2 players, movimento, sincronização, mensagem e reconnect. Antes de executar escrever no repositório, confirmar quem detém writer/lease/branch e autorização. Provar custo com quotas e configuração que impeça cobrança automática. Party original NO-WRITE, identidade sintética dos jogadores.

**P1 — Base de combate:** integrar VLAB/atributos/PA/fichas/skills quando contratos oficiais forem aprovados; reusar os motores canônicos; testes de dano/turnos/RD/condições/recurso; logs segregados. Sem anunciar engine/IA competente até IA tática ser medida em cenas adversariais.

**P1 — 2,5D e modo visual:** estilização harmonizada, assets próprios/CC0, UI Android, grids/tokens sem contraste 2D/3D; três níveis de animação independentes do cálculo; som como melhoria opcional.

**P2 — Godot:** prova mínima opcional sem depender de notebook; engine aberta e gratuita, mas não obrigatória. Comparar com manter navegador + eventual PWA. Sem introduzir novo motor se arquitetura JS atual for suficiente.

**P2 — Exploração/quest:** somente depois de combate multiplayer funcional e estabilizado.

## 9. Checkpoint e instrução para qualquer Comestre sucessor

**VERIFICADO:** visão do Mestre e A+C registradas no Notion, Lab e GitHub consultados; RUN010 último RUN, gh-pages TEST32 no commit `0aa9bc...`, TEST33 candidato e auditoria científica PESQ010; PESQ011 depositada; cinco vídeos transcritos; vídeo Sonecarox transcrito e stack identificada; Godot open source; planos gratuitos com LIMITES publicados.

**PROPOSTO:** Web/PWA com servidor de sala e tela 2,5D como direção preferencial; Cloudflare DO e Supabase como opções gratuitas condicionadas a gate; uso de sprites/sons CC0. Não alegar escolha formal de arquitetura, deploy de backend, conteúdo real sincronizado, custo zero para qualquer escala, editor Godot instalado ou APK pronto.

**FIRST-PENDING:** provar multiplayer real entre aparelhos, sem vazamento Mestre-only e sem despesa adicional; antes consultar autoridade de escrita e última versão do Desenvolvedor. Vínculos VLAB/LEVEL-UP quando aprovados, não antes. Android físico/HTTP/duas abas ainda em HOLD.

**NEXT:** coordenar Desenvolvedor para plano mínimo e teste sintético de sala multiplayer sob writer autorizado; Pesquisador audita custo/licença/protocolo, visual 2,5D e técnicas vídeo aplicáveis; usar decisões A+C e níveis de animação como contratos; Notion com readback por etapa.

**NO-REPEAT:** não reconstruir TEST32, não repetir PESQ009/010/011, não alterar branch main ou páginas Party, não criar AGENTS.md duplicado, não migrar para Godot precipitadamente, não investir em PixelLab, Claude Code pago, Suno/ElevenLabs pagos, servidores pagos ou novos motores. Não adiar multiplayer para desenvolver história/arte premium. Todo teste funcional exige prova física, não promessa.

**PERGUNTAS OPERACIONAIS PENDENTES (não exigem suspender pesquisa):** quantidade exata de players por sessão; se internet estável disponível na casa; capacidade média dos celulares; tolerância a latência/offline; regras canônicas concretas já prontas para integrar. Usar 1 Mestre + 2 clientes sintéticos como primeiro gate, sem presumir que esse é limite definitivo.

### Links de referência operacional

- Laboratório canônico do Inovador: https://app.notion.com/p/401c2b324ede809585d3d1907c194df9
- Site TEST32: https://arthof09-ai.github.io/assimilat-rpg-integracao-test/
- Repo: https://github.com/arthof09-ai/assimilat-rpg-integracao-test
- Workflow TEST32: https://github.com/arthof09-ai/assimilat-rpg-integracao-test/actions/runs/39845848140
- Vídeo solicitado: https://youtu.be/0TvVgPdgQ6s
- Vídeo Godot + ChatGPT adicional: https://youtu.be/4Y3XZquie_4

**Releia sempre fontes canônicas antes de agir. Este arquivo registra fatos observados e diretrizes, não concede autorização de publicação, gasto, migração ou alteração em motores externos.**
