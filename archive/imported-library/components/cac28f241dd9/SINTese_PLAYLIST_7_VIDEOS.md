# Síntese de coordenação — método e prioridades da playlist

# Playlist VibeCode — 7 vídeos, 5 episódios inéditos e 2 duplicatas

**Projeto:** RPG Assimilação / Tabletop; **papel:** Coordenador Inovador MESTRE-SIDE; **data da análise:** 24/10/2026.

**Método:** sete MP4 lidos fisicamente; durações/codec/SHA256 via ffprobe/hashlib; 28 quadros por arquivo (196 quadros amostrados) em 14 folhas de contato, cada uma com timestamp. As legendas e letreiros são gravados no próprio vídeo em muitos trechos. Não há faixa separada de legendas, nem transcrição integral feita por ASR. Apenas textos visíveis nos quadros inspecionados foram tratados como observáveis; explicações sobre funcionamento interno só são inferências quando o vídeo não expõe fonte/teste.

**Deduplicação importante:** `496150` tem SHA256 já registrado como vídeo anterior `495862`; `496210` coincide com `495907`. Contam como 7 arquivos recebidos, 5 vídeos de conteúdo novo neste conjunto, 2 obras repetidas. Não criar duplicações normativas nem tratar revisão como descoberta inédita.

**Critério de utilidade:** ganho observável na própria Arena tática com Mestre+Party, ações mecânicas do VLAB e servidor único; melhorias gráficas/cenográficas são subordinadas a esse objetivo. Nunca transferir condições ambientais dos vídeos para cálculos de Vida, Alma, PA, alcance, dano ou FOV.

## Avanço cronológico observado

- **Prólogo (496210, duplicata):** mecânica simples primeiro, testes e sprites depois, exportação com custo/cotas em mente.
- **Dia 1 (496150, duplicata):** animar personagem, tirar fundo de atlas, corrigir recortes, compor cenário de rio.
- **Dia 2 (496165):** atlas de fauna, estados rastrear/espreitar, cadeia alimentar ilustrativa; há bugs assumidos.
- **Dia 3 (496174):** seed, água, rios com entrada, confluências, chunks e emendas; mapa precisa ser determinístico.
- **Interlúdio (496183):** consulta à audiência para priorizar animais, não implementação.
- **Dia 4 (496192):** clima, temperatura, sol e chuva; o vídeo admite sistemas incompletos.
- **Dia 5 (496201):** nutrientes e ciclos de solo; demonstra como cresce a complexidade e aparecem variáveis não calibradas.

## Transferência prioritária AO COMBATE do Assimilação

**P0 — Não adiar:** Arena existente deve mostrar comando autorizado e resultado mecânico VLAB com Mestre+players, ação legal, alvo e recibo. A playlist não ensina essa integração, logo não declarar que resolve o bloqueio.

**P1 — Apresentação:** sprite atlas direcional no token e estado visual do campo (chuva/noite/rios) APENAS se não afetar cálculo/FOV/visibilidade.

**P2 — Terreno reproduzível:** seeds/salvamentos e validação entre bordas de cenas; não gerar mundo aberto.

**P3 — Criaturas inteligentes:** testar seleção entre ações LEGALMENTE fornecidas pelo VLAB, sem motor de combate paralelo; VLAB já tem pesquisa de tática adaptativa, portanto evitar duplicar.

**P4 — Recusar escopo:** fotossíntese, nutrientes, reprodução animal, cadeia alimentar completa e voto público para cânone.

## Ferramentas e substitutos

Claude Code aparece no vídeo; não é requisito. Já existem HTML/JS, a Arena TEST36, codificação por Codex quando autorizada, Pillow e arquivos CSV/JSON, além de sprites originais/CC0 candidatos. **A prova TEST da playlist usa somente CSS/JS do Tabletop existente** sem assinar serviços. Não usar imagem de vídeo alheio no produto público.

## Prova executada nesta análise

`ARENA_TEST36_CAMADAS_AMBIENTAIS_OFFLINE.html`: addon opcional em cópia do TEST36 original, três modos *Dia/Chuva/Noite*, contrato `assim.tabletop.scene.presentation.test.v1`; 31/31 checks Playwright em Chromium Linux, 360×740 / 390×844 / 412×915, 49 células, zero chamadas de rede e nenhum resultado mecânico alterado. **Não é combate, não é Android real e não foi integrado à branch oficial.**

## Checklist da próxima passagem

1. Verificar novo RUN/TEST e ABI VLAB/estado Codex, impedindo regressão/repetição.
2. Entregar ao Desenvolvedor relatório de prioridades e POC isolado, sem atribuir escrita de outro executor.
3. Somente adotar clima visual após validação FOV/ACL e UX Android; não redirecionar Dev de combate P0.
4. Reavaliar tempo canônico de RS/CG antes de eventuais sistemas de calendário; não adotar o calendário fictício da playlist.
