# Relatório individual — 496097
## Plataforma de geração de jogos por IA, monetização e limites de transferência para um RPG canônico

**Projeto:** RPG Assimilação / Tabletop · **Data:** 24/10/2026 · **Arquivo:** `496097.mp4` · **Duração:** 15min10s · **SHA-256:** `3b9a49698aa94147d0ad212533dc229b21bd19faa3e5b49c21fb4332501d92a3`.

**Método:** 24 quadros amostrados e seis ampliados, leitura visual. MP4 com AAC, sem stream de legendas. A narração não foi transcrita integralmente, e números exibidos na interface do vídeo podem variar por plano/região/data.

## Diagnóstico

Este vídeo não é simplesmente “IA faz um RPG”. Ele demonstra uma plataforma de geração de jogos e assets, seleção de classes, telas de início, controles mobile, jogo de arena tipo sobrevivência e, perto de 09:09, **uma oferta de plano pago na própria interface**, com valor visível de cerca de US$19,99 mensais. Isso é incompatível com exigir novos gastos do Mestre sem autorização; além disso, não há comprovação no vídeo de exportação livre do projeto, revisão de fonte ou integração com VLAB.

## Cronologia dos trechos observados

| Momento | O que aparece | Implicação |
|---|---|---|
| 00:00–01:35 | “Combos — plataforma de criação de jogos utilizando IA”, chat em inglês e parâmetros de game | Ferramenta especializada; serviço não é automaticamente substituto para a infraestrutura canônica |
| 01:35–03:10 | Tela “Hero Dungeon”, escolha de classe e área de geração de recursos | UI de classe e habilidades, não uma ficha de personagem do Assimilação |
| 03:10–04:55 | Joystick, HUD de Vida/XP, escolha de Cavaleiro, Mago, Patrulheiro, Bárbaro e outras classes | Boa referência de organização visual compacta, mas classes são do protótipo do vídeo |
| 05:05–08:45 | Upload/geração de sprite, galeria de assets, planejamento de múltiplos heróis | Geração de artes dentro do serviço; fluxo de direitos/exportação precisa ser verificado |
| 09:00–09:30 | Tela “Choose a plan”, preço de plano Pró US$19,99/mês visualmente | Evidência de barreira econômica na etapa mostrada, não parecer financeiro de todas as ofertas futuras |
| 09:30–12:30 | Jogo Hero Dungeon com piso em tiles, inimigos, upgrade de nível e escolha de melhorias | É um protótipo jogável do autor; progressão é sintética e não equivale ao LEVEL-UP |
| 12:30–14:40 | Salas com monstros, sistema automático/survivor e telas de mapas | Combate automático não substitui decisão tática de um turno real |
| 14:40–fim | Encerramento/promocional da plataforma | Não é contrato de performance, licenciamento ou manutenção do serviço |

## Classificação das ferramentas e substituição real

**Plataforma Combos vista no vídeo — CONDICIONADA/BLOQUEADA:** o vídeo mostra valor pago e não comprova exportação de projeto completo em formato que possamos auditar. NÃO recomendar assinatura. Confirmação de preço atual da conta depende do site e do perfil do usuário, não apenas do vídeo.

**Alternativa funcional existente — APROVEITAR:** Tabletop HTML/CSS/JS já preservado no GitHub/Biblioteca, com Codex conectado ao repositório e testes independentes. Essa alternativa é real no nosso projeto e evita contratar outra plataforma, mas ainda não executa combate VLAB homologado.

**Sprites e tiles gratuitos — CANDIDATOS:** recursos Kenney CC0 e atlas PNG original, reusando o renderizador existente. Não há licença para copiar heróis do vídeo.

**IA de código sem plano extra — VIÁVEL COM GATES:** Codex e ChatGPT que o Mestre já utiliza, testando branches isoladas, mantendo autoria/receipts; sem depender de exportação fechada de outra plataforma.

## O que aproveitar para a Arena

O melhor conteúdo não é o gênero survivor. É a **hierarquia visual**: cenário central, HUD pequeno, botão de ação, lista de escolhas e retorno visual de uma decisão. No Assimilação, essa hierarquia deve ter unidade ativa, alvo, habilidade, PA livre, Vida/Alma, fase do turno e histórico, sempre a partir de projeção autorizada. A UI não pode selecionar efeitos ou custos a partir das regras de Hero Dungeon.

A progressão visível de “subir de nível e escolher bônus” também inspira um menu futuro, porém qualquer ganho deve ser controlado pelo LEVEL-UP canônico e não pelo código de UI.

## Contrato de aceite recomendado ao Desenvolvedor

`ARENA-FIRST-ACTION-HUD-TEST`: no TEST36 ou posterior legítimo, abrir Arena em 390×844 com mapa visível na primeira tela; selecionar unidade/ação/alvo; distinguir ação `READY`, `PENDING`, `ACCEPTED`, `REJECTED` e `UNKNOWN`; usar apenas recibos TEST marcados até existir backend e VLAB autorizados. O envio real será controlado pelo cliente v2 competente e replay persistente, nunca por onclick que altere Vida local.

**Aceite:** 49 casas preservadas; 3 perfis de teste; nenhum campo Mestre-only aparece no payload das players; nenhuma ação duplicada após ACK perdido; 0 cálculos de ataque ou PA inventados. O requisito de multiplayer permanece HOLD até 3 dispositivos reais e WSS confiável.

## Experimento realizado neste lote

O protótipo `ARENA_TEST36_RECIBOS_VISUAIS_SINTETICOS_OFFLINE.html` foi construído em cópia TEST do HTML existente com um painel de estados visuais. **42/42 checks Chromium em 3 resoluções** validaram abertura, ACCEPTED/REJECTED/UNKNOWN, guardas de schema, 49 casas, recursos mecânicos intocados, 0 rede e 0 erros JS. Esses são recibos artificiais de UI: não equivalem a uma sala publicada ou batalha funcional.

## Riscos, conclusão e sucessão

**VERIFICADO:** a tela de plano pago e a demonstração visual. **INFERIDO:** a plataforma pode dificultar recuperação de projetos fora de seu ecossistema; é risco a auditar, não prova de lock-in definitivo. **PROPOSTO:** aproveitar a hierarquia UX. **PENDENTE:** documentação/licença de exportação atual e testes no próprio serviço, que não são necessários para o P0 do nosso Tabletop.

**LAST-VERIFIED:** quadros do MP4, artefato HTML e testes locais. **FIRST-PENDING:** integração à UI oficial TEST36 por writer competente. **NEXT:** ação/autorização/recibo VLAB no próprio tabuleiro. **NO-REPEAT:** não contratar Combos, não criar survivor paralelo ou copiar classes. **NAC-PASS:** laboratório UI PASS, plataforma externa não homologada.
