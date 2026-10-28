# Dossiê científico operacional — Lote 03 de vídeos do Mestre

**Projeto:** RPG Assimilação / Tabletop Assimilação · MESTRE-SIDE · 23/10/2026 (horário do Mestre)  
**Escopo:** triagem de 3 MP4 locais + contraste com TEST36 candidato em cópia somente leitura.  
**Foco imutável:** Arena de COMBATE TÁTICO MULTIPLAYER do RPG Assimilação, Mestre+players em Android, VLAB autoridade mecânica, A+C server-side, orçamento R$0, sem jogos paralelos.  
**Limitação de método:** FFprobe e inspeção distribuída de **88 quadros em oito folhas de contato**, mais 10 detalhes ampliados. **Não** houve transcrição integral da fala, inspeção de repositórios dos criadores nem reprodução completa cronológica do vídeo quadro por quadro. Alegações de narradores não são execução verificada. 

## Custódia dos arquivos enviados

| MP4 | Duração | Tamanho | SHA-256 |
|---|---:|---:|---|
| `496003.mp4` | 47:38 | 135.158.768 bytes | `5b2cb496cc84e504f7eb7a76d5d4f069f80f6aba1bbd71c1c20ece652df06494` |
| `496008.mp4` | 17:42 | 31.345.526 bytes | `ef4c047b3b391a6ffcb9f5c49938f847f84798a94063a241041a14e707193139` |
| `496016.mp4` | 19:52 | 36.032.167 bytes | `0c5d172ce002c3adaf3124986e409a288bee2cea56e7d7408f8f0e99cfab824c` |

**Soma de duração:** 5.112 segundos aprox. = 85min12s. MP4 originais permanecem uploads desta conversa; este pacote **não** copia/republica os vídeos brutos. Na análise apenas quadros de referência de custódia mestre.

## Evidências por vídeo e relevância

### 496003 — Processo de produção de assets e prototipagem técnica (47m38)

- ~00:35–06:32: discussão e navegação por referências e aplicativos, Steam/cartas com interface de RPG.
- ~08:55–14:53: geração/seleção de personagens, imagens de sprites em diferentes poses, cenários, cartas/recursos visuais e prompts.
- **~16:04:** interface Mixamo com modelos de personagens/visualização 3D. O vídeo *exibe* essa ferramenta, sem demonstrar no Assimilação um pipeline pronto.
- ~17:16–19:38: personagem 3D, tentativas de animação/sprite sheet a partir de poses, erros visuais e refinamentos.
- ~27:59–30:22: editor de engine 3D com modelos colocados na cena, organização e testes.
- ~31:33: protótipo de tabuleiro com peças coloridas, UI e ações, mais relevante para a forma incremental de testar fluxo do que para adotar a mesma engine.
- ~36:19–44:39: código, correções e validações; há problemas visíveis e iterações, não um sistema de combate completamente demonstrado.

**Aplicação concreta sugerida:** pipeline de personagem → animação/quadros → atlas → renderização em unidade da Arena, com license gate e performance Android. Para nosso jogo HTML/JS atual, o pipeline 3D→2D da referência NÃO é prioridade; sprites 2D autorais/CC0 e ferramentas já presentes são mais simples. Referência adicional: provar um microfluxo de ação na interface antes de ampliar produção artística.

**Ferramentas detectadas:** Adobe Mixamo (visível), editor 3D (plataforma exata não homologada), ferramentas de geração de imagens IA (provedor não necessariamente demonstrado em todos os trechos). A documentação oficial Adobe confirma Mixamo gratuito com Adobe ID sem assinatura e uso royalty-free de personagens/animações; não confundir uso das animações com direitos sobre modelos próprios/de terceiros.

### 496008 — RPG 2D incremental com Codex (17m42)

- ~01:06–03:19: planejamento de jogo de estilo Pokémon em conversa/prompts e uso de interface Codex com tarefas e alterações; *não* migrar a propriedade intelectual Pokémon para o Assimilação.
- ~04:47–06:16: cenário de tiles com vegetação; personagem e diálogo tipo RPG.
- ~08:28–13:38: exemplos/iterações de spritesheets, edifícios, vegetação, mapas e estruturas top-down; consistente com processo de produzir o visual em lotes incrementais.
- **~15:07:** quadro de batalha por turnos com o monstro “Bramblet” e atributos “VIG”; o importante é a CLAREZA VISUAL: identificação de ator, oposição, recurso e mensagem de resultado, não as regras do jogo do autor.
- ~15:51–16:35: cena e interação com NPC/mapa.

**Aplicação direta e priorizada:** o TEST36 precisa expor no mesmo tabuleiro seleção de unidade/ação/alvo e uma **resposta de procedência mecânica** sob autoridade VLAB. O layout de batalha do vídeo é referência de hierarquia informacional, NÃO para substituir o combate tático em mapa por uma cena de combate separada ou sistema idle/automático. Nada de novas fórmulas improvisadas.

**Ferramentas:** Codex aparece no vídeo e JÁ está configurado pelo Mestre para o projeto; não criar outra instância de motor ou gastar nova assinatura. Editor HTML/CSS/JS e spritesheets são mais compatíveis com o stack vigente que migrar automaticamente para Godot.

### 496016 — *Velmora*: implementação incremental, mecânica e apresentação (19m52)

- ~00:24–06:12: planejamento e instruções para projetos no Codex, arquivos e documentação; risco de acumular prompts longos sem provar jogabilidade.
- ~07:02–09:31: editor de engine com cena e versão do jogo com HUD de Vida/energia/objetivos.
- ~10:20–12:00: diário de fauna, exploração e mudanças de ambiente. Isso é referência secundária: não iniciar campanha/worldbuild no Assimilação.
- **~14:29–18:37:** comparação temporal muito clara: cena simples inicialmente; depois chão com tiles, caminhos orgânicos, árvores, sombra/iluminação, HUD contínuo e ciclo dia/noite.

**Aplicação:** manter uma camada artística intercambiável no MESMO tabuleiro, com camadas e obstáculos/casas de jogo preservados; não é necessário esperar concluir cada detalhe de backend para mostrar evolução visual. O projeto do vídeo é exemplo de UX/art, não de homologação do VLAB nem de três aparelhos conectados.

**Ferramentas:** ambiente/editor semelhante ao Godot visível, mas sem inferir que todos os assets/códigos rodam Android nativo. O Mestre já baixou Godot, porém o editor Android tem limitações relevantes e não é justificativa para abandonar HTML/JS atual.

## Confronto com o TEST 36 — resultado FÍSICO

**Fonte do código:** ZIP de distribuição candidato TEST36 da Biblioteca Mestre, SHA256 `5a7cb0bd9f7b239f7441c843d5df831a0bd16be92a46386241f0072907561bf1`; cinco arquivos HTML/CSS/JS, ZIP sem modificação.

O arquivo `verificador_aceite_combate_test36.py` auditou **11 premissas estáticas** do código, gerando `ACEITE_COMBATE_TEST36_BASELINE.json`. Resultado: **11/11 premissas sustentadas por código**, subdivididas em **5 capacidades TEST já identificadas** e **6 lacunas/pendências**. Não é 11/11 de jogabilidade — as lacunas são evidência negativa! Ver o JSON para as expressões usadas e limitações.

**Já presente:** grade/viewport; token e edição de recursos TEST; perfis Mestre/P1/P2 DEMO; recibos v2 em bancada; botão de rodada TEST. 

**Ainda não demonstrado/ausente no bundle de distribuição:** botão/fluxo mecânico Ataque/Magia; iniciativa oficial; interface motor VLAB para resolver dano/PA; autenticação real; filtro de dados Mestre-only ANTES da transmissão em servidor; três Android reais conectados.

## Decisão operacional que muda produto

**O que NÃO fazer:** mais vídeos como substituto de produto, áudio descartado pelo Mestre, clone de Pokémon/Minecraft, nova engine, nova backend, novos cálculos TEST enganadores. Não criar/PUBLICAR TEST37 automaticamente, nem alterar código do Desenvolvedor, VLAB, Party ou gh-pages.

**Primeiro incremento que deve contar como avanço de jogabilidade:** dentro da **Arena existente**, Mestre toca numa unidade e numa ação; seleciona alvo; emite intenção formal versionada; backend competente valida ACL, turno, revisão e deduplicação; interface VLAB autorizada calcula ou retorna HOLD explícito; servidor persiste recibo/projeta dados role-safe; UI apresenta resultado e custos com origem. Enquanto VLAB ABI estiver HOLD, aceitar implementação de UI/intent + feedback `MECANICA_INDISPONIVEL`, sem alterar Vida/PA ou inventar resultado. Nenhum segundo jogo.

**Critérios de aceite mínimos (para futuro desenvolvedor):** 1) primeira tela Android mostra mapa e unidades; 2) seletor ação + alvo no mesmo tabuleiro; 3) intenção possui ID/revision/actor; 4) perda de ACK preserva UNKNOWN e consulta ID estável; 5) nenhum número de dano/PA é calculado fora VLAB; 6) players não recebem dados Mestre-only (servidor, bytes); 7) smoke de dois perfis/3 Android somente com WSS de verdade; 8) captura antes/depois e teste que Mestre pode tocar. TEST36 não satisfaz itens 2, 5-mechanics-active, 6-server ou 7.

## Substituições de ferramentas e custo

| Ferramenta/abordagem vista | Condição/alternativa | Estado honesto |
|---|---|---|
| Mixamo (animação/rig 3D) | Gratuito com Adobe ID segundo Adobe; se fluxo online ou 3D for trabalhoso no Android, spritesheets autorais/CC0 2D e render atual HTML Canvas reduzem dependência | Disponibilidade documental; NÃO usado nos assets do Assimilação |
| Godot/engine editor para cena | Mestre já tem Godot; Android editor oficial existe, mas tem UX limitada em celular, C# ausente; alternativa para jogo atual é conservar HTML/JS + Canvas, Phaser se realmente preciso | Documentado; migração NÃO AUTORIZADA |
| Codex em vídeos | Codex Cloud já configurado/missionado no projeto. Direcionar para artefatos e testes pontuais sob autorização; não executar outro backend | Relatado ativo, fonte POC ainda depende de recuperação |
| Bancos de sprites/asset gerado por IA | PNG autorial ou assets Kenney CC0 previamente pesquisados; checar cada licença/versão/consistência de quadros | Pipeline Pillow/Canvas Lote01 já foi testado; NÃO repetir como prova nova |
| Templates de jogo Pokémon / narrativas | Tomar só fluxo de HUD/tilemap e teste; mecânicas e personagens do Assimilação originais | Referência, não código reaproveitado |

**Fontes externas consultadas em 23/10/2026:** https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html ; https://docs.godotengine.org/en/4.5/tutorials/editor/using_the_android_editor.html ; https://phaser.io/download/license . Consulta não equivale a teste da ferramenta.

## Governança, novidade real e próxima retomada

**NOVO nesta rodada:** oito folhas de contato com 88 timestamps, quadros-chave, proveniência SHA dos vídeos; auditoria de aceitação dirigida ao TEST36 com seis pendências distintas; preservação em arquivo físico. **NÃO novo:** a falta da mecânica foi diagnosticada anteriormente e PESQ015 já contém boundary Arena-Sala-VLAB. O ganho atual é confrontar lacunas com vídeos recentes e entregar o verificador reproduzível sem tocar o código do Desenvolvedor.

**Último pesquisador:** PESQ-INOV-20261023-015 já foi localizada no Notion: 15/15 dirigidas, 256/256 mutações, 35/35 estruturais relatados; não refazer a pesquisa, não presumir writer/lease. **TEST36** último development correlato visto nesta auditoria; site publicado TEST32 no último checkpoint. **Codex:** bridge local relatada e pacote inacessível no último recorte. **VLAB:** autoridades não migradas e homologação mecânica HOLD.

**LAST-VERIFIED:** vídeos MP4 presentes/FFprobe/SHA; auditoria estática TEST36 11/11 premissas; PESQ015/RUN013 no Notion; fontes externas de ferramentas. 
**FIRST-PENDING:** primeiro incremento COMBATE funcional no próprio TEST36; suporte de motor VLAB autorizado ou recibo HOLD explícito; prova física Android. 
**NEXT:** Desenvolvedor competente implemente fluxo de intenção de ação+alvo em cópia TEST, Coordenação compare com contrato PESQ015 e resultado Codex, Pesquisador audite fluxo de integração sem criar motores paralelos. 
**NO-REPEAT:** PESQ012–015, TEST33–36, áudio rejeitado, sprite dummy como produto final, novas operações. 
**NAC-PASS proporcional:** PASS custódia, matriz de evidências e teste ESTÁTICO; HOLD RPG mecânico, servidor, rede, Android real e produção.
