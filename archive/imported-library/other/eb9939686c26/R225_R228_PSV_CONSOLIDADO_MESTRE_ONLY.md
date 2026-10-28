# PSV consolidado — VLAB R225–R228 / campanha de continuidade

**Data:** 21/10/2026. **Identidade lógica:** CM-000006 / MESTRE-SIDE. **Operação existente:** OP-VLAB-FUSION-SANDBOX-01. **Escopo:** TEST. **Produção:** HOLD. **Party, O Primeiro, fichas originais, Sistema de Combate e normas canônicas:** NO-WRITE.

## Decisão do Mestre e resultado de fonte

**DECISÃO EXPRESSA, VERIFICADA NO CHAT:** quando um ataque físico, mágico, elemental ou outro efeito de dano exige arredondamento fracionário, o resultado é arredondado **para baixo**. Isso define a direção da aproximação, não cria automaticamente uma regra de reduzir ataques à metade. O contrato especializado da Transformação Espiritual que conserva carry fracionário TAP/BAP permanece intacto. **NAC-NORM/edição das páginas canônicas não executados** por ausência de autoridade de writer e processo de promoção.

## Novidades demonstradas desde R224

**R225:** três conjurações nativas de Tempestade de Esporos de Eristan, com 10d10+10 full tape fonte-validada, três R18 commits independentes. Bruto 61→30 (salvaguarda), 60→30, 21→10, 80 PA por conjuração. Três quarentenas preliminares não admissíveis foram preservadas. Controles aritméticos físico/mágico/elemental e TAP carry. Nenhum combate integral.

**R226:** **oito pares, 16 bancos, 32 commits, 174 eventos**. Manopla do Trovão Cativo (Ouro, PS semicanônica) com golpe físico comum e descarga adicional +5d8+3 Raio por 22 PA após acerto; sete acertos, um erro; +187 PV efetivos condicionais na comparação COM/SEM, 154 PA consumidos em sete descargas, sete lentidões temporárias. Base do ataque e descarga foram separados; RD elétrica0 e velocidade4m explicitamente TEST. Janela de ataque, não duelo completo; nenhuma Bateria E oficial homologada.

**R227:** **seis pares, 12 bancos, 24 commits, 132 eventos**. Mesmo item PS sob hipóteses separadas RD elétrica0 versus RD elétrica100: quatro acertos, 100 PV extras versus zero e quatro lentidões versus zero. Em ambas as variantes dos quatro acertos houve débito 22 PA; dois erros não disparam item. Total 176 PA nos braços elegíveis. Auditoria externa e quatro clones adversariais rejeitados; relatório histórico apresentava um KeyError de chave impressa após as escritas, sem invalidar estados dos 12 SQLite. Foi produzida pós-auditoria específica de fontes para três candidatos da Bateria E (Manopla PS, Espada do Lendário, Adaga do Sussurro Mortal) e nenhum é elegível ao estrato oficial sem novas provas.

**R228:** **duas execuções dirigidas TEST, dois bancos, seis commits, 21 eventos**, quatro ataques físicos e quatro movimentos nativos. Flecha de Trava da proposta Iskiel ON5: 55 PA; acerto causa −6m até final do turno seguinte do alvo. Varok com velocidade12m explicitamente de fixture, não fonte canônica. No braço com acerto, sofreu 26 PV após RD físico35, andou 5m dentro do limite reduzido6m e, após expiração, 7m com velocidade12m restaurada. Uma tentativa de 7m ainda lento foi rejeitada antes de mutação. Braço crítico negativo teve política de erro **LAB-only**. Entre turnos observados de Varok não houve turno ofensivo de Iskiel; logo não é combate bilateral scheduler-completo. Ambos terminaram em censura, não KO. Quatro adulterações de evento/recurso/posição/status foram rejeitadas após reconstrução de hashes. Preliminar `R228_HIT_S22871001` recusada por ID de comando e preservada, sem retry do RUN-ID.

## Denominadores sem inflação

- R225: 3 cenários de conjuração dirigidos, 3 commits; zero duelos completos.
- R226: 8 seeds pareadas, 16 braços, 32 commits; sete acertos com descarga; janelas de um ataque + turno do alvo.
- R227: 6 seeds pareadas, 12 braços, 24 commits; RD elétrica é manipulação da fixture.
- R228: 2 seeds dirigidas, 2 braços, 6 commits; janelas de movimento e expiração, não duelos completos.
- Total das quatro coortes: **33 bancos admitidos, 65 commits e 330 eventos** (R225: 3; R226: 174; R227: 132; R228: 21). Os braços de políticas e ataques não são unidades estatísticas independentes.
- Zero reexecuções de seeds históricas, zero KO nas janelas e nenhum benchmark oficial.

## Fontes principais e classificação

- Sistema de Combate e Sistema de Magia: fontes canônicas de mecânica, sem edição nesta campanha.
- Eristan, Iskiel, Varok e Arveth: NPCs **propostos Mestre-side**. Não projetar para Party.
- Manopla: https://app.notion.com/p/3f5c2b324ede81f5ac62fb940204cdac — **PS/SEMICANÔNICA**. Estado P4 NÃO provado.
- Flecha de Trava: https://app.notion.com/p/3f6c2b324ede81a78a59d3d81fd5e966 — habilidade fonte-documentada de Iskiel, proposta.
- Espada do Lendário: https://app.notion.com/p/3edc2b324ede81ab9e22e168f6d939a9 — dano composto sem split físico/mágico certificado.
- Transformação Espiritual: T1 TAP=BAP/2 com carry; a ativação Bronze é proibida, apenas Prata1+.

## GOVERNANÇA — Gate por domínio

| Gate | Status |
| --- | --- |
| Direção de arredondamento do dano | DECISÃO DO MESTRE EXPRESSA; implementação TEST R225 PASS; propagação NAC-NORM PENDENTE |
| Separação de dano físico + item mágico PS | PASS TEST CONDICIONAL R226/R227 |
| RD mágica e lentidão da Manopla | PASS TEST condicional em RD0/100 hipotéticas |
| Flecha de Trava + movimento nativo e expiração | PASS TEST condicional R228 |
| Velocidade real de Varok e regra bloco↔metros | HOLD SOURCE/NORM |
| Consequência de erro crítico negativo | LAB-only; HOLD normativo |
| Controle de Besta integral e transformação Prata+ | PENDENTE source-complete |
| Bateria E de item canônico P4 | HOLD; 0 células oficiais |
| IBX-125 e IBX-126 | Publicadas anteriormente pela Coordenação; não reenviadas, nem ACK final presumido |
| Contratos terminais, matriz e produção | **0/17, 0/1.875, HOLD** |

## Persistência e continuidade

R225/R226/R227/R228: arquivos de evidência independentes, journals R18 e verificadores frios, todos publicados na pasta Biblioteca Mestre da operação. R227 tem suplemento de auditoria adversarial e pós-auditoria de elegibilidade Bateria E publicados separadamente. R228 possui ZIP CRC íntegro, 291 hashes válidos, dois SQLite aprovados e readback do artefato publicado. Não usar semicanônico como prova P4 nem adaptar a Party.

**LAST-VERIFIED-UNIT:** R228, retorno frio a partir da Biblioteca + suplementos R227 fonte-auditados.

**FIRST-PENDING:** R229 candidato, sujeito a namespace preflight: selecionar ator com movimento e alcance source-complete, integrar interposição real de turnos e prazo de lentidão; em paralelo encaminhar decisão universal de piso pelo gate normativo sem escritor autoatribuído.

**NEXT-5:** (1) localizar velocidade legal efetivamente documentada do alvo ou conservar TEST; (2) combate bilateral multiturmo com controle de movimento nos turnos intercalados, reação e iniciativa sem empate; (3) fonte P4 com físico/magia separados, antes da Bateria E; (4) Besta com controle completo ou ED Prata+ com Espírito real; (5) demanda de atualização NAC-NORM por rota autorizada e recibo incremental DMG por destinatário/assignment válidos, sem duplicar IBX-126.
