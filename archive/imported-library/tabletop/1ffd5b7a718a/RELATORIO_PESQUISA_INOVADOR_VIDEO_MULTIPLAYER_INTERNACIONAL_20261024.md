# RPG Assimilação — Pesquisa aplicada: três vídeos internacionais sobre jogos com IA e multiplayer

**Data:** 24/10/2026  
**Responsável:** Comestre Coordenador dos Inovadores — MESTRE-SIDE  
**Tipo:** pesquisa/curadoria sobre fontes externas; NÃO nova operação, nova engine, novo backend ou autorização de migração.  
**Questão do Mestre:** extrair práticas técnicas dos vídeos estrangeiros que acelerem a primeira batalha funcional do Tabletop, em **celular OU notebook/PC OU ambos**, sem R$ adicionais, preservando VLAB único motor mecânico, governança e segredos Mestre-only.

## 1. Escopo e metodologia de prova

Três MP4 originais enviados pelo Mestre foram lidos fisicamente via ffprobe/ffmpeg, frames amostrados sistematicamente a 20 posições por vídeo, folhas de contato e análise visual. Links YouTube originais fornecidos pelo Mestre foram cruzados com documentação pública dos autores (incluindo Google Codelab, How I AI, Nick Saraev). Áudio dos vídeos **não foi transcrito integralmente**: o plugin conectado vidIQ recusou a operação por saldo insuficiente de créditos, sem cobrança; não repetir chamada até os créditos voltarem e somente se o Mestre desejar. As sínteses textuais externas não substituem transcrição integral nem execução dos códigos de terceiros. Nenhuma instalação, implantação, serviço pago, uso de credencial externa ou escrita no laboratório alheio nesta pesquisa.

| Fonte enviada | Arquivo | Duração medida | Bytes | SHA-256 calculado |
|---|---|---:|---:|---|
| Google Cloud Tech — `t4LOHNHv-r8` | `497523.mp4` | 11m38s | 28.043.571 | `5a9b881979e501282920b622f3de467e95c2f50fffef820242828ea3b4a07d43` |
| How I AI — `xW5y2Yv_E2Y` | `497532.mp4` | 31m43s | 49.411.774 | `1cb5ac833dac78dfa872703002f10451b5efb12e4213cd366a9f05237fb5711b` |
| Nick Saraev — `LD0NxqDcDiY` | `497544.mp4` | 23m26s | 73.460.499 | `6e606df4bdfd5d373628e684bc10aff419ebfc9fc710fcc00bf895444580a293` |

Links originais:
- https://www.youtube.com/watch?v=t4LOHNHv-r8
- https://www.youtube.com/watch?v=xW5y2Yv_E2Y
- https://www.youtube.com/watch?v=LD0NxqDcDiY

### Classes de evidência
- **VERIFICADO-VÍDEO:** cena, tela, palavra/interface legível ou sequência visual no MP4 efetivamente inspecionado.
- **VERIFICADO-DOC-EXTERNA:** recurso ou recomendação declarado na documentação externa consultada, não significa prova própria de funcionamento.
- **RELATADO-TERCEIRO:** funcionalidades, custos, número de usuários, hospedagem e sucesso alegados pelo criador/resumidor, não reproduzidos independentemente.
- **PROPOSTO:** adaptação ao Assimilação; depende de implementação e gate.
- **HOLD:** algo que exige motor VLAB real, autenticação/rede, custo/limites, ambiente compatível e validação própria.

## 2. Vídeo 1 — Google Cloud Tech: jogo web de turnos com histórico de eventos

**Identidade:** «Launch your web-based video game with AI»; vídeo enviado 11m38s; codelab oficial atualizado em setembro/2026: https://codelabs.developers.google.com/codelabs/cloud-run/launch-your-web-based-video-game-with-ai

**VERIFICADO-VÍDEO (amostras visuais):** ~00:17 página do tutorial; ~02:37 Google AI Studio com prompt extenso; ~03:12 opção Firebase; ~03:46–05:31 jogo da velha em navegador em iteração, início de partida e visualização de tabuleiro; ~06:41–09:36 duas interfaces/partidas em navegador; ~10:10 tutorial Deploy to Cloud Run; ~10:45 console Firestore e registros, ~11:20 limpeza.

**VERIFICADO-DOC-EXTERNA:** Codelab demonstra partida por turnos, código curto/convite, Firebase Authentication, Firestore, gravação de jogadas sequenciais/event sourcing, histórico/replay/rollback e deploy Cloud Run. O guia atual aponta Starter Tier (2 apps em região selecionada sob condições) e Standard Deployment com billing; portanto **não se presume R$0 irrestrito**. A abstração de event sourcing pode reconstruir um estado a partir de eventos, mas regressão/undo de partida exige governança própria para evitar apagar ou invalidar decisões canônicas.

**Ganhos diretamente transferíveis SEM trocar infraestrutura:**
1. Esquema mínimo comando recebido → decisão VLAB competente → recibo/evento oficial imutável → projeção por destinatário → replay de visualização, usando a autoridade existente.
2. Identidade de partida/sala e ID estável de intenção, o que TEST37/Codex já iniciaram.
3. Teste de autorização NEGATIVO e histórico/revisão; não confundir botão de login com segurança real.
4. Inspeção do registro persistido após ação, com evidência de estado ANTES/DEPOIS.

**NÃO transferir automaticamente:** recriar event store em Firestore, habilitar Google Sign-In, exigir Firebase/Cloud Run, copiar lógica Tic-Tac-Toe/Minimax, autorizar rollback físico de combate oficial sem VLAB/NAC. Não há prova do código real do RPG funcionando nessa stack.

## 3. Vídeo 2 — How I AI: protótipo 3D, trabalho paralelo e integração

**Identidade:** vídeo enviado 31m43s; «How I AI: Speedrun a 3D Multiplayer Game in 15 Minutes with Cody De Arkland»; documentação do episódio: https://www.chatprd.ai/how-i-ai/vibe-code-3d-multiplayer-game-in-15-minutes e runbook https://www.chatprd.ai/how-i-ai/workflows/how-to-speedrun-a-3d-multiplayer-game-prototype-in-15-minutes-with-claude-code-cli

**VERIFICADO-VÍDEO:** ~03:57 ambiente de desenvolvimento; ~05:33 tela SPACEFLIGHT; ~10:18–13:28 comandos/código em terminal; ~18:14–21:24 implementação/telas; ~22:59 cena de voo 3D simples com avião; ~24:35 interface de entrada/sala. Demonstração narrada e entrevistas são intercaladas, vídeo completo dura 31m43; a marca dos «15 minutos» corresponde à parte do experimento, não ao tempo de entrega de um produto robusto.

**VERIFICADO-DOC-EXTERNA:** autor descreve primeiro controlar corretamente o jogo local (orientação do modelo, câmera, controles, limites), depois iniciar um workstream separado para Express/Socket.IO/WebSocket; testar múltiplos clientes, join/movement, desconexão, reconexão e mensagens malformadas. A documentação deixa claro que é demo local, sem autenticação, limites, persistência, segurança ou deploy de produção homologados.

**Aplicações ao Assimilação:**
1. **Corte vertical mínimo de jogabilidade** antes de otimizar toda infraestrutura. No nosso caso: personagem→ação→alvo→decisão oficial VLAB→registro→exibição.
2. **Paralelismo com fronteiras explícitas**: Desenvolvedor frontend, Codex ponte, Pesquisador auditor — estrutura já existente, não nova equipe. Um contrato único e uma prova de integração impedem divergência de nomenclatura.
3. **Testes de experiência em cliente real** (browser efetivo) e de servidor realmente conectado, não resultado de screenshot.
4. **Iteração guiada por bug observado**: controlar um loop, testar, reproduzir, corrigir, avançar; não geração gigante sem checkpoints.
5. **Separar «jogável» de «multiplayer de produção»**; o segundo exige auth, rate limits, roles, recuperação, observabilidade e dispositivos independentes.

**Não transferir:** React/Three.js, avião, coord. 3D, chat ou novo Express/Socket.IO se já existe autoridade prevista; isso seria reconstrução onerosa e engine paralela sem benefício real.

## 4. Vídeo 3 — Nick Saraev: jogo base, playtest e multiplayer posterior

**Identidade:** enviado 23m26s; guia externo com indexação por capítulos derivado das legendas disponível em https://aihow.tv/en/use-cases/build-a-multiplayer-browser-game-and-put-it-online/ .

**VERIFICADO-VÍDEO:** ~00:35 jogabilidade fantasia Minecraft/Attack on Titan em navegador; ~01:45 comparação em cartões Haiku/Sonnet/Opus; ~02:55–05:16 IDE/prompt; ~06:26–13:28 teste de caminhada, ataques e deslocamento em mundo; ~14:38 mais alterações por prompt; ~16:59 personagem 3D/HUD; ~18:09 tela de Practice; ~20:30 e ~21:40 combate demonstrado; ~22:51 autor fala. O vídeo inclui vários ciclos de jogar/testar/corrigir.

**RELATADO-TERCEIRO:** síntese externa informa versões de benchmark entre modelos, relatado ~$5 para uma variante e $24–25 para outras, jogo posteriormente publicado em URL Netlify, uso de Twilio relay e partida com colegas, total narrado ~$31 em tokens. Essa alegação não é auditoria independente de contas, custos totais/hospedagem, escalabilidade nem privacidade.

**Ganhos aplicáveis:**
1. Modelo primeiro testado com controle/jogabilidade em uma pessoa, depois sala compartilhada;
2. Jornada «jogar→notar defeito→especificar correção→jogar de novo», reduzindo abstração e relatórios excessivos;
3. Escopo mínimo de primeiro uso local mesmo se futuro multiplayer online;
4. Teste separado de custo e dependência, evitando copiar Twilio relay/planos pagos;
5. Valor de um link simples para abrir jogo no navegador, mas sem alterar automaticamente produção.

**Não transferir:** 3D, bots, missões, estética de outra propriedade intelectual, pagamento Anthropic/Twilio/Netlify, game engine nova, movimentação tempo real quando o Assimilação é RPG tático com autoridade de turno.

## 5. Conclusão comparativa e decisão técnica PROPOSTA

| Critério | Google (turnos) | How I AI (protótipo 3D) | Nick Saraev (jogabilidade primeiro) | Decisão Assimilação |
|---|---|---|---|---|
| Loop local antes da rede | Parcial, jogo da velha | Explícito | Explícito | **Prioridade 1** |
| Fonte mecânica autoritativa | Lógica do app | Server/posições experimental | Não homologada aqui | **VLAB Python único** |
| Histórico/recuperação | Firestore event sourcing | Demo/rede, faltas produção | Não demonstrado independentemente | Reutilizar jornal/recibos e logs oficiais; não event store paralela |
| Segurança Mestre vs player | Firebase auth/regras exemplo | Não homologada | Não homologada | Gateway role-safe ANTES envio obrigatório quando compartilhar |
| Android/notebook | Web navegável | Browser/3D | Browser/3D | **Qualquer um ou ambos**, conforme provas mais rápidas |
| Hospedagem R$0 | Starter condicionado/Standard billing | Hosting fora escopo | Relatado custos e relay | Não impor nova plataforma nem custos |

**Decisão do Coordenador (PROPOSTA, dependente do próximo gate):** confirmar no TEST38 ou última versão validada a melhor interface prática para 1 batalha local do Mestre, conectar UMA ação real ao executor competente do VLAB sem motor paralelo e obter efeito/recibo/visualização corretamente classificados. Investir no multiplayer como contrato mínimo em paralelo, mas adiar polimento de lobby/contas/escalabilidade/distribuição antes de prova do combate. Plataforma livre: notebook, celular ou ambos, conforme menor obstáculo REAL. Depois testar segundo cliente autorizado, primeiro no mesmo ambiente e, quando possível, em dois dispositivos; internet real só após auth/ACL/projeção antes do envio e competência de host. Sem decidir Stack Firebase, Colyseus, Cloudflare, React/Three.js, Twilio ou qualquer serviço ainda.

### Gates de implementação sugeridos
- **G0 — interface utilizável:** TEST38/RUN015 ou sucessor lido/testado; ator→ação→alvo, preview visual e bloqueio honesto; sem VLAB real ainda.
- **G1 — primeira ação VLAB real local:** entrada autenticada/competente ou ambiente Mestre-only, motor VLAB oficial decide ataque/defesa/PA/vida quando cabível, event/receipt ligado à mesma intenção, frontend apresenta sem inventar regras. Não permitir duas fontes de combate.
- **G2 — dois clientes TEST e uma autoridade:** revisão, receipt idempotente, sequência e projeção por role em servidor TEST; navegador/tab distinto não é dispositivo real.
- **G3 — duas pessoas/dispositivos reais:** identidade, permissões, reconexão, rede autêntica (LAN ou internet conforme autorizado), sem vazamentos.
- **G4 — publicação robusta/escala:** WSS/hosting/habitação/fila/backup/R$0 comprovado e 3+ dispositivos quando de interesse.

### Direção concreta para os 3 Comestres (NÃO nova ordem a executores já despachados)
- **Desenvolvedor:** manter interface original e apresentação fiel, especialmente TEST38; melhorar somente bloqueio de interação real e erro observável, não cosmética/3D.
- **Codex:** adequar wire geométrico/snapshot sem reconstruir backend e garantir recibos persistentes idempotentes. Validar contrato contra versões físicas atuais, não TEST36 isolado.
- **Pesquisador:** testar adversarialmente a integração REAL client/server/roles e ABI VLAB (sem assumi-la disponível); não criar novo receipt overlay nem outro servidor.
- **Coordenador:** receber PSV atuais, revalidar baseline (há registros RUN015/TEST38, PESQ017 e menção Codex 0.3 no Notion), reconciliação NAC-PASS, decidir o próximo P0 com evidência. Isto é leitura DOCUMENTAL de estado, não auditoria independente dessas novas rodadas.

## 6. Referências secundárias e limitações

- Google tutorial primário: https://codelabs.developers.google.com/codelabs/cloud-run/launch-your-web-based-video-game-with-ai (last updated 09/2026)
- How I AI workflow: https://www.chatprd.ai/how-i-ai/workflows/how-to-speedrun-a-3d-multiplayer-game-prototype-in-15-minutes-with-claude-code-cli
- How I AI episode: https://www.chatprd.ai/how-i-ai/vibe-code-3d-multiplayer-game-in-15-minutes
- Nick Saraev summary captions-derived: https://aihow.tv/en/use-cases/build-a-multiplayer-browser-game-and-put-it-online/
- Signaling/P2P and STUN/TURN (não supor «sem infraestrutura»): https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Signaling_and_video_calling , https://webrtc.org/getting-started/peer-connections
- Colyseus server authority — conceitual, não adoção: https://docs.colyseus.io/

**Status global:** VERIFICADO contato visual e hash dos 3 arquivos; VERIFICADO-DOC técnicas oficiais e contexto; RELATADO-TERCEIRO custos, limites e demos online; PENDENTE transcrição integral (vidIQ sem créditos), execução dos códigos externos, custos das plataformas no projeto; PROPOSTO priorizar batalha local VLAB e gate rede mínimo; HOLD VLAB físico, auth de produção, WSS/internet, Android físico e notebook físico não ensaiados nesta pesquisa.

**NAC-PASS-02 proporcional:** PASS curadoria de referências e prova documental/visual; nenhuma promoção de produção.  
**LAST-VERIFIED:** hash+contato dos 3 vídeos originais e fontes documentais conferidas; Notion atual consultado.  
**FIRST-PENDING:** auditar PSV físicos mais recentes dos 3 Comestres e comprovar G1 primeira ação VLAB real na Arena.  
**NEXT:** registrar no Lab/Coordenador, guardar originais com hash na Biblioteca Mestre, entregar resumo ao Mestre; só alterar direção dos executores depois de ler novos PSV.  
**NO-REPEAT:** vídeos 496248/496257 anteriores, vídeos 497523/497532/497544 desta rodada, tutoriais como prompts de novo projeto, recreação de motores/servidores ou migração compulsória.
