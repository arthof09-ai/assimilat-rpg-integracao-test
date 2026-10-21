# AGENTS.md — Orientações do laboratório RPG Assimilação (TEST)

> Escopo: apenas este repositório. Este arquivo orienta colaboradores e assistentes que o consultarem; não é bloqueio técnico de permissão nem autorização de novo Comestre.

## Fontes autoritativas
- [Diretriz local GH-RP-01 do Notion](https://app.notion.com/p/400c2b324ede8147bc9af2160e0b1a8e) — reabrir antes de iniciar ações.
- [Diário Operacional em alternantes](https://app.notion.com/p/400c2b324ede8102ad79e3c9d54a34ef) — consultar o último marco e registrar novos resultados verificáveis.
- [Laboratório GitHub + Replit](https://app.notion.com/p/400c2b324ede816e8bccef35bd18f3da) — fonte de escopo TEST.

## Antes de trabalhar
1. Verifique a branch, o último commit, os arquivos existentes e o estado do CI. Não reimplemente VLAB, DMG, CRAFT ou LEVEL-UP só porque seus programas existem em outras fontes.
2. GitHub/Replit são ferramentas, **não** COMESTRES registrados. Não invente COMESTRE-ID, INSTANCE-ID, TRACE-ID, OP-ID, writer, lease, epoch ou aprovação do Mestre.
3. Mesmo com acesso técnico a todos os repositórios, **só escreva neste repositório dedicado**, salvo ordem específica posterior do Mestre e do dono da operação. Os laboratórios e códigos dos demais Comestres são fontes de leitura, não destinos de escrita.
4. Trabalhe sobre cópias de dados ou programas necessários, separadas do original; garanta que nenhuma fixture ou automação acione escrita no Notion, Party, O Primeiro, cânone ou em outro laboratório. Não use credenciais de produção em CI.
5. Planeje o teste, rode em TEST, preserve artefato/sha/seed, faça readback do status e regist­re limites. PASS de GitHub Actions não certifica regras do jogo.
6. Modificações por agentes: prefira branch/PR, revisão do diff e testes; evite force push e escrituras concorrentes. Diante de ação ambígua, confira o estado no servidor antes de repetir.
7. REG-ROUTE-03: mantenha código aqui e o registro ANTES/DEPOIS no Diário do laboratório. Nunca misture logs operacionais a fichas, cenas, itens ou regras de jogo.
8. **Decisão vigente do Mestre (21/10/2026): Replit SUSPENSO SEM PRAZO operacional.** A cota gratuita mensal inviabiliza a praticidade desejada. Não espere pelo reset de 20/11/2026 como requisito, não faça upgrade, não compre créditos, não chame o Agent nem crie outro app. A prioridade é ChatGPT + Notion + GitHub gratuito, com execução de testes locais quando mais simples; reabrir o tema Replit somente mediante nova decisão expressa do Mestre.
9. Regras globais do Comestre/NAC prevalecem sobre qualquer comentário deste repositório. Só o Mestre/fluxo apropriado pode autorizar publicação ao cânone.

## Estado comprovado, 21/10/2026
- Repositório privado conectado ao ChatGPT com leitura e escrita.
- Workflow `Test Integrity Auditor #1`: tela do GitHub Android apresentada pelo Mestre mostra **verde/sucesso, 10 segundos, branch main**. Confirma o workflow remoto; os oito testes foram antes verificados localmente e o workflow usa fixtures sintéticas, **não** os ZIPs reais dos motores.
- **Integração nativa DMG C29:** [PR #1](https://github.com/arthof09-ai/assimilat-rpg-integracao-test/pull/1) validada no CI (#10), dois scripts originais com SHA, 43 verificações e 10 saídas; [PR #2](https://github.com/arthof09-ai/assimilat-rpg-integracao-test/pull/2) validada no CI (#13), cinco regressões fail-closed. Ambas incorporadas em main. Isso não altera a OP DMG ou o cânone.
- Replit TEST permanece SUSPENSO por decisão do Mestre: não usá-lo como dependência de continuidade nem contratar plano.
- Qualquer novo marco deve iniciar com readback e terminar com um alternante numerado GH-RP-DNNN no Diário do Notion.

**Sem escrita nos sistemas oficiais e sem promoção automática de resultados.**
