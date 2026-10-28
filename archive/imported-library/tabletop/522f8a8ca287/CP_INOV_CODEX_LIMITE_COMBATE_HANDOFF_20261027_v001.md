# RPG ASSIMILAÇÃO — CHECKPOINT DE RETOMADA CODEX (MESTRE-SIDE)

**Identificador:** CP-INOV-CODEX-LIMITE-20261027-001  
**Data:** 27/10/2026  
**Natureza:** checkpoint de continuidade e preservação de transferências, sem execução do Codex nesta rodada.  
**Autoridade:** decisões expressas do Mestre; a página canônica no Notion continua sendo a fonte de governança.  
**Separação:** MESTRE-SIDE; Party / O Primeiro NO-WRITE; não publicar assets privados no GitHub público.

## 1. MOTIVO DA PAUSA

O Mestre informou esgotamento temporário de limite do Codex. **NÃO** relançar, migrar ou repetir o trabalho do Codex por conta própria. Retomar somente em nova interação autorizada, a partir do checkpoint real mais recente que o próprio Codex confirmar.

### Último relato do Codex (status RELATADO, não retestado pelo Comestre)

- Protótipo de batalha jogável: andar, atacar, defender, perder Vida, gastar Alma, salvar partida.
- Informou **25 testes do motor** e **28 verificações de interface** aprovados.
- Entregáveis citados: contexto Mestre, manual Blender/props/tiles/sprites, regras de exemplo, instruções de protótipo e pacote de ~59 MB.
- Usou dados sintéticos TEST; arte como estudo inicial; projeto legado preservado.
- Próximo marco anunciado pelo próprio Codex: testar batalha no navegador, refinar rigs/animações no Blender, integrar no Godot sem perder a versão browser.

### Último estado visível (captura enviada pelo Mestre)

- Codex trabalhando em ambiente **Linux Cloud**, checkpoint anterior encontrado, Blender/Godot relatados disponíveis neste ambiente.
- **Acesso à pasta Windows do notebook não comprovado** nesta execução. Antes houve microteste local por comandos: Blender 5.2.3 (editar/salvar/reabrir) e Godot 4.7.2 (projeto Node2D) com PASS históricos; Computer Use visual parcial (timeouts). Não assumir que tal acesso persiste entre sessões.
- Caminho alvo Windows conhecido: `C:\Users\Antônio Tiburtino\OneDrive\Área de Trabalho\RPG Assimilação`. Apenas buscar/verificar em ambiente realmente acessível. Evitar repetir microteste sem causa.
- O ZIP unificado ~92 MB não entrou na ferramenta, que informou **limite de transferência 32 MiB**. Logo, NÃO afirmar que o Codex já analisou os 37 PNGs.
- Atividades que surgiram como INICIADAS, não concluídas: `Governança v002`, `Assets audit v002`, `Baseline qa v002`; preparação de diretório Godot isolado. O estado final, commits e testes posteriores a essa captura **NÃO SÃO CONHECIDOS**.

## 2. QUATRO PARTES MENORES PREPARADAS PARA ENVIO QUANDO O LIMITE VOLTAR

Pasta privada na Library pessoal:
`/RPG-Assimilacao/Tabletop-Inovador/PRIVADO-MESTRE-ONLY/BIBLIOTECAS-VISUAIS/TRANSFERENCIA-CODEX-20261027/`

| Ordem | Arquivo | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| 1 | `RPG_ASSIMILACAO_CODEX_PARTE_01_BESTA_CRISTALINA_v009.zip` | 28177343 | `b7b47607b4370bdc84ae77c36cd595047b8d254b8bf0b0ec2ef247948cc804f6` |
| 2 | `RPG_ASSIMILACAO_CODEX_PARTE_02_CAPRILEO_v001.zip` | 21315322 | `2230c6799c3b12b14302b8897f1482f131cbc4e89ad52d3c50289d6a361ff5f6` |
| 3 | `RPG_ASSIMILACAO_CODEX_PARTE_03_ORC_CARDINAIS.zip` | 17045062 | `a11e1307e9d9f5a51c3ed130c14b1383acc1c7afc8fad43e2f4d2ef5aeb1858e` |
| 4 | `RPG_ASSIMILACAO_CODEX_PARTE_04_ORC_DIAGONAIS_ATAQUES.zip` | 25815712 | `205d648bde877a45540d2ecfdb76ca3f98a3206dfd019f0063ea58d206f065a1` |

Todos os quatro ZIPs foram verificados localmente com CRC PASS em 27/10/2026, e todos são menores que 32 MiB. **Isso prova integridade local, não chegada ao Cloud do Codex.** Repassar cada parte ao Codex e solicitar confirmação de recebimento, extração, hashes e contagem dos originais. Não ultrapassar limite e não reenviar o ZIP gigante enquanto a limitação permanecer.

Conteúdos: **Besta Cristalina (16 PNGs)**, **Capríleo Escamoso (8 PNGs + JPEG mãe)** e **Orc (13 PNGs)**; imagens, metadados e documentos. Os recortes auxiliares NÃO substituem a auditoria independente do Codex sobre pranchas completas. Preservar bibliotecas originais como fontes únicas; divisão de transporte não substitui versões canônicas.

## 3. DIREÇÃO CRIATIVA DE COMBATE A TRANSMITIR AO CODEX

**Aprovado como direção artística pelo Mestre:** arena tática de combate **2.5D**, estilizada, browser, câmera oblíqua/superior; pixel art realista altamente detalhada nas artes aprovadas; qualidade nativa máxima útil, respeitando as silhuetas, animações e legibilidade.

**Referências complementares (inspiração; não assets copiáveis):**
- **Hades 1:** ritmo e impacto cinético, antecipações curtas ou pesadas, deslocamentos, arcos de ataque, esquivas, VFX direcionais, silhueta clara, sincronização entre hit e reação. Inspiração no método 3D→quadros 2D renderizados quando for útil, sem impor essa solução a todo o projeto.
- **Avatar: A Lenda de Aang:** gestos corporais contínuos, postura/respiração, movimentos de artes marciais e condução/liberação de magias elementais acompanhando corpo e trajetórias (fogo/água/terra/ar). Magia pode fluir como uma dança sem perder força de impacto.
- **League of Legends:** leitura de área, estados e efeitos na câmera de jogo; clareza da unidade e resposta visual.
- **Baldur's Gate 3:** profundidade e legibilidade do combate tático por turnos. Referência de apresentação, não reprodução mecânica.
- **Diversidade artística:** um Orc com machado pode ser pesado, uma conjuração pode ser fluida, uma criatura pode fazer investida brutal; estilos mistos são válidos. Não impor que todo ataque seja rápido/igual ou que magia pareça ataque físico.

**Gramática de animação audiovisual:** intenção/postura inicial → antecipação → aceleração/condução → contato, liberação ou erro → impacto e reação quando realmente houver acerto → seguimento → recuperação → repouso. Em um erro, não representar efeito mecânico de impacto bem-sucedido. Valorizar *timing*, pose-chave, deformação controlada, peso, transferência de massa, atrasos de cabelo/juba/cauda/capa, emissão luminosa, impacto no ambiente quando autorizado, som e legibilidade sem poluição excessiva.

**Alerta estrutural:** um ataque mecânico pode ter 3, 9, 12, 20 ou N quadros de animação sem virar N ataques. VLAB rege ações, resultados, tempo/turnos, PA, alcance, acerto, erro, dano e evento. Godot/HTML/Blender exibem visualmente eventos autorizados. No protótipo TEST usar fixtures sintéticas separadas e indicar a ausência de contrato VLAB. Não inventar bônus, dano ou novas regras a partir de aparência gráfica.

**Animação modular:** rigs humanoides reusáveis (identidade corporal/cosméticos/equipamento/arma como camadas), animações genéricas de caminhar, correr, defender, cair, levantar, golpes com espada/machado, arco, conjuração; retargeting quando compatível; animação procedural para ajustes secundários e IK, caso validada. Orc como prova humanoide; Capríleo e Besta Cristalina precisam de famílias de rig apropriadas, NÃO um esqueleto humano. Sprite sheets de caminhada TEST do bestiário são referência de movimento, não loop certificado.

**Níveis de apresentação:** estudar modos de animação completa, reduzida e desligada, com mesmas decisões mecânicas e eventos, para favorecer desempenho e preferências do jogador; ainda precisam de especificação de UX/teste antes de serem implementados.

## 4. BESTAS MAIORES QUE HUMANOS — FOOTPRINT/HITBOX (DIREÇÃO EXPRESSA)

Fonte: Laboratório do Inovador, **HITBOX-FOOTPRINT-IRREGULAR** (26/10/2026). Status de design autorizado, **não implementação mecânica homologada**.

Três geometrias distintas:
1. **Sprite/projeção artística:** corpo renderizado, cabeça, chifres, asas, cauda, arma, juba ou VFX podem extrapolar sua base visualmente.
2. **Footprint de ocupação no tabuleiro:** conjunto de células realmente ocupadas, possivelmente formatos 1×1, 1×6, T, L, faixa ou outras máscaras irregulares; acompanha orientação, escala e rotação validada, podendo conter múltiplas células por ator.
3. **Hitbox/área atingível:** regiões elegíveis para atingir uma única criatura, mapeadas à anatomia, pose e ocupação válidas; não se limita automaticamente à célula central, nem equivale a qualquer pixel do efeito visual.

É proibido **miniaturizar** uma grande Besta Demoníaca para caber num tile humano ou criar footprint só porque a cauda passou por ali. Testar seleção/alvo por células de extremidade, rotação e colisão em paredes/obstáculos, persistência/replay, formas T/L/1×6, vários tiles abrangidos por mesma magia e **ausência de dano multiplicado por célula** salvo determinação do VLAB. Verificar medidas reais do tile no código antes de supor metros por célula. Nenhuma nova regra de alcance/AoO por iniciativa do renderizador.

## 5. AMBIENTE E CRITÉRIO DE RETOMADA

- Continuar o projeto existente, não criar substituto. Primeiro reabrir o estado do Codex no ambiente que estiver realmente disponível; checar últimos arquivos, diffs/branch, scripts e testes; recuperar progresso interrompido na execução e identificar FIRST-PENDING físico.
- Depois testar o protótipo já criado no navegador; analisar quatro ZIPs confirmados; inventariar rigs, meshes e referências de animação na pasta local, **somente se disponível**; executar protótipo Blender→Godot (Compatibility/web quando aplicável) e produzir demo funcional com floresta 2.5D sem borda visual abrupta, personagem com animação modular e bestas em escala coerente.
- Não impor Godot como substituição imediata do HTML funcional; validar exportação browser em protótipo isolado e comparar desempenho/limitações. Evitar dependências pagas; custo adicional R$ 0.
- Preservar PNGs byte a byte, hashes e IDs; os manifestos explicam fluxo da prancha (caminhada por linha/direção, ataques esquerda→direita continuando na linha seguinte), SEM textos nas artes. Codex audita independentemente a extração/alpha/poses/pivôs.
- Governança: BOOTSTRAP-COMESTRE, NAC-CONT-03, NAC-NORM-01 quando mudança normativa, NAC-PASS-02 antes de certificar; diário e checkpoints; separar VERIFICADO / RELATADO / INFERIDO / PROPOSTO / PENDENTE.
- Sem acesso ao Windows, não afirmar edição no notebook. Sem teste browser executado, não afirmar build jogável atual. Sem verificação dos quatro ZIPs pelo Codex, não afirmar análise concluída.

## 6. FONTES CANÔNICAS

- Laboratório do Inovador (documentação completa de Hades × Avatar e hitbox): https://app.notion.com/p/401c2b324ede809585d3d1907c194df9
- Portal visual 2.5D (roteador dos protocolos): https://app.notion.com/p/405c2b324ede81eb80cfecc4ba47abdb
- Besta Cristalina: https://app.notion.com/p/406c2b324ede81859909cf00a5031609
- Capríleo: https://app.notion.com/p/406c2b324ede81f38af7f3f620baf05c
- Orc: https://app.notion.com/p/405c2b324ede816ca88af5f66f103a2a
- Kit Essencial de Integração: https://app.notion.com/p/3edc2b324ede81d0b25ec2f3be128db6

## 7. PONTO EXATO DE RETOMADA / FIRST-PENDING

**Estado no momento da pausa:** Codex sem limite de execução disponível para o Mestre; visualizou-se trabalho em Cloud Linux, operações de auditoria v002 iniciadas, mas sem confirmação final; arquivo unificado rejeitado pelo limite de 32 MiB; quatro pacotes menores preparados localmente. **Não reenviar nem reiniciar ainda.**

**Na próxima interação com Codex:** (1) ler estado real da execução interrompida; (2) receber e conferir as quatro partes menores; (3) ler este checkpoint e as fontes de direção artística/combat/hitbox; (4) continuar o projeto real, não iniciar reconstrução em paralelo; (5) entregar testes, demos, hashes e checkpoint pós-execução. Sem publicação Party/GitHub de conteúdo Mestre-only.

**Critério de sucesso do registro:** os quatro arquivos e este checkpoint recuperáveis pela Library privada e por índice Notion, sem depender de memória informal.
