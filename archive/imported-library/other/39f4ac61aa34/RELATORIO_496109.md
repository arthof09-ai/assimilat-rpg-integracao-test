# Relatório individual — 496109
## Contexto-mãe de projeto, geração de ativos 3D e riscos de reconstrução de um RPG assistido por IA

**Projeto:** Tabletop Assimilação · **Arquivo:** `496109.mp4` · **Duração:** 20min05s · **SHA-256:** `80e9f896286507808658c5dec00ac8b8816c6b544edb43eda97debdbccdaee` · **Data:** 24/10/2026.

**Método:** análise de 30 quadros selecionados ao longo do MP4 e seis detalhes ampliados; reprodução de textos legíveis em tela sem inferir transcrição do áudio. Arquivo com H.264/AAC e nenhuma faixa de legendas. A fala integral e o código completo do autor não foram verificados.

## Achado central

É o vídeo **metodologicamente mais próximo da necessidade de continuidade do Assimilação**. O criador demonstra um RPG 3D chamado *Frosthold*, usa um grande arquivo de contexto do projeto com seções de visão, estilo, mecânicas e requisitos, discute decisões de geração de cenário/Blender, apresenta edições e acaba testando um mundo 3D que inclui floresta, vila, inventário, interação com portas, loja, ruínas e um inimigo. O contexto comum evita que cada conversa de IA reinvente as mesmas premissas — um problema que o Mestre já enfrentou com vários Comestres.

**Ponto de atenção:** o exemplo usa editor/arquivos e cenário 3D, o que não comprova que essa é a melhor infraestrutura para nosso Tabletop Android em HTML/JS. Importar o gênero FPS, a progressão e a história do vídeo seria um erro de escopo.

## Linha do tempo observável

| Momento aproximado | Evidência | Utilidade/risco |
|---|---|---|
| 00:00–02:40 | Exibição de personagem de referência conhecido, documento com lista de inimigos e progressão de atributos | A lista de escopo existe, mas não autoriza copiar IP ou regras do outro jogo |
| 02:40–05:20 | Preparação de instrução à IA com arquivo de contexto e pedidos de modelagem para projeto 3D | **Metodologia reutilizável:** artefato único de verdade recuperável entre conversas |
| 05:20–08:25 | Documento “FROSTHOLD — CONTEXTO MESTRE DO PROJETO”, visão geral, metas e imagens de mapa low poly | Demonstra arquivo de visão/escopo, não substitui fonte canônica do RPG |
| 08:25–10:10 | Conversa longa com arquivos e referências de povoado/cenário e solicitações de implementação | Risco de pedidos enormes sem gates, necessidade de checkpoints menores |
| 10:10–11:50 | Edição de scripts (Blender/Python visíveis) e nova cena de vila | A automação de assets exige pipeline determinístico e hashes |
| 12:20–14:15 | Telas de título, vila, jogo 3D em terceira pessoa e caminhos com árvores | Produto visual demonstrado, teste do autor; hardware e qualidade técnica não auditados |
| 14:15–16:20 | Mundo de floresta e painel de loja/armas, estado de missão na tela | HUD conecta dados à cena, mas não demonstra regras ou inventário homologados |
| 16:20–18:25 | Loja, porta com tecla de interação, ruínas e NPC/inimigo em área interna | Evidência de interações jogáveis no exemplo; sem garantias sobre persistência ou redes |
| 18:25–20:05 | Enfrentamento de criatura e trechos finais de cena | A ação final parece jogável, mas não informa backend, número de bugs ou consistência canônica |

## Aplicação diretamente relevante ao Assimilação

Já possuímos BOOTSTRAP-COMESTRE, NAC-CONT-03, Diário e um handoff Mestre-only. Portanto **não precisamos criar um segundo “Contexto Mestre” paralelo** como o do vídeo. Precisamos derivar uma **cápsula operacional de desenvolvimento**, sempre apontando para os documentos canônicos existentes. Ao abrir uma tarefa, o executor recebe referência ao LAB atual, último RUN/TEST, source hash, writer/lease, meta funcional, dependência mecânica, teste de aceite e proibição de Party/produção. Isso é uma implementação de método — não outra governança.

**Contrato sugerido de entrada de tarefa (test-only):**

```json
{
  "operation": "Tabletop Assimilacao",
  "source": "Notion canonico - Lab Inovador",
  "role": "Desenvolvedor|Pesquisador|Codex",
  "last_verified_run": "RUN-013/TEST36 (revalidar)",
  "branch_or_file_owner": "verificar antes de editar",
  "target_player_action": "selecionar unidade, acao, alvo e obter recibo",
  "mechanical_authority": "VLAB aprovado ou HOLD",
  "privacy": "A+C, server side before Party transmission",
  "acceptance": "acao real na arena, evidencias, recursos intactos sem recibo",
  "forbidden": ["novo motor", "Party write", "main/gh-pages sem gate"]
}
```

Esse contrato é um **modelo de briefing**, não atualização da norma canônica, e seu RUN precisa ser revalidado no momento do uso.

## Ferramentas e alternativas gratuitas

- **Blender:** aplicativo gratuito de modelagem/automação Python em desktop; não pressupor que o Mestre possa trabalhar nele pelo Android. Caso se queira um asset 3D isométrico, Pesquisador/Codex num ambiente Linux autorizado podem exportar sprites/PNG, com direitos e processo reproduzível.
- **HTML/JS existentes:** melhor alternativa pragmática para manter o Tabletop com Android/R$0 adicional, não exigir reimplementar Godot.
- **Godot Android:** o editor é experimental e não fornece C# no Android; o Mestre já baixou o aplicativo, porém o vídeo não prova sua integração com as regras. [Fonte oficial](https://godotengine.org/download/android/).
- **Documentação estruturada:** Notion e Biblioteca Mestre já usados são o substituto real para arquivos de projeto sem ligação com o cânone. Evitar copiar o documento Frosthold e substituir a visão do Mestre.

## Experimento de método executável recomendado

Criar um **verificador de prontidão de tarefa TEST** que rejeite falta de `source`, `last_verified_run`, `target_player_action`, `privacy`, `mechanical_authority` e `acceptance` antes de acionar qualquer executor. Não deve escrever Notion nem mudar motor; apenas validar se a ordem de trabalho ajuda a entregar jogabilidade visível.

**Aceite:** (a) contrato completo PASS; (b) remove `mechanical_authority` ⇒ FAIL; (c) tentativas de escrever Party/main sem autoridade ⇒ FAIL; (d) o executor entrega um ANTES→DEPOIS de ação tocável, não só novas páginas; (e) LAST/FIRST/NEXT/NO-REPEAT presentes.

## Experimento efetivamente realizado neste lote

A prova Chromium em uma cópia do TEST36 usou estados artificiais `ACCEPTED/REJECTED/UNKNOWN` e mostrador de recibos sem alterar recursos. Ela valida um elemento do objetivo de interface, não a metodologia completa de documentação nem integração 3D. O modelo de briefing fica **PROPOSTO**, com critérios verificáveis.

## Riscos e fidelidade

O foco em um arquivo “contexto-mãe” pode virar duplicata normativa se não apontar para o Notion. Importar storylines/itens/atributos alheios criaria violações canônicas. Servidor sala único + VLAB mecânico competente continuam separados. A apresentação 2D/2.5D da nossa arena pode ganhar qualidade visual sem migrar a engine.

**LAST-VERIFIED:** observações do vídeo e artefatos existentes. **FIRST-PENDING:** validar contrato de entrada de tarefas contra governança vigente e testar reutilização no próximo RUN funcional. **NEXT:** usar a cápsula para integrar recibo autorizado à Arena; **NO-REPEAT:** não clonar Frosthold, documentos canônicos ou criar motor paralelo. **NAC-PASS:** estudo/documentação PASS; integração de método e gameplay 3D HOLD.
