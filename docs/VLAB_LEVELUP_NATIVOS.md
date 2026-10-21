# Integração dos motores originais — VLAB R237 e LEVEL-UP R216-P12

**Status em 21/10/2026: dois motores originais executados e aprovados no GitHub Actions.** O ZIP combinado foi enviado pelo Mestre pelo Android, conferido por SHA-256 e Git blob. A versão inicial do workflow detectou diferença binária entre SQLite gerado em máquinas distintas; PR #6 adicionou verificação de integridade e igualdade semântica integral (schema + linhas) e passou no GitHub.

## Por que estes dois motores são os prioritários

**VLAB:** o pacote R237 possui 241 programas Python e oito bancos de confrontos. Reexecutar os mesmos scripts e sementes produz oito bancos SQLite idênticos, com 155 commits, 640 eventos e oito passagens da condição normal para Fraco. Não é outro motor de combate: são os programas originais, sem modificações.

**LEVEL-UP:** o pacote atual é **R216-P12** (substitui P11). Possui 116 programas Python e a correção do Mestre para **dois Anéis da Alma = +100 PA livres, zero gasto diário**. Nosso gate rápido executa **184 testes nativos dirigidos do P12**; a bateria histórica completa de **2.026 testes** é outro gate, não executado remotamente aqui.

## Fontes pinadas

| Sistema | Fonte da Biblioteca do Mestre | SHA-256 original |
|---|---|---|
| VLAB R237 | `VLAB_R237_LIVE_FRACO_TRANSITION_NATIVE_COLD_AUDITED_MESTRE_ONLY.zip` | `49c2db6ebf8fdae8e378355c3f017e95afe879c7e29ba72086044afdd190d4de` |
| LEVEL-UP P12 | `IBX114_SUCESSOR_R216P12_MESTRE_CORRIGIDO_20261021_MESTRE_ONLY.zip` | `619fe210a2e8469df59f7db001220c97309cae79054b7574284a5047c633e4de` |

O runner [native_engine_ci.py](../../scripts/native_engine_ci.py) rejeita qualquer ZIP ou membro alterado, caminhos inseguros e manifestos incompletos. Todos os efeitos ficam dentro de um diretório temporário do runner GitHub. Não fornece token Notion; não altera fichas, Party, O Primeiro, outros laboratórios, regras ou o cânone.

## Testes locais já realizados

- VLAB: **PASS** — motor R237 original reexecutou oito combates, o auditor original reproduziu 155 commits / 640 eventos e os oito SQLite gerados tiveram o mesmo SHA-256 dos originais. Também passou a auditoria fria dos 299 arquivos.
- LEVEL-UP: **PASS** — pacote P12 autenticado, 370 hashes, suíte nativa específica `test_ibx114_r216p12_master_correction` executou **184/184** testes. A verificação histórica completa de 2.026 testes está documentada no recibo original, não é uma conclusão do presente CI GitHub.
- Ambos: execução em cópias locais, com ambiente sem credenciais de produção e sem mutações do Notion.

## Upload pelo Android — etapa concluída (sem novo envio)

O Mestre já enviou pelo Chrome um único arquivo, sem código, assinatura ou computador:

**`ASSIMILACAO_NATIVE_INPUTS_R237_P12_20261021.zip`** (3.140.244 bytes), SHA-256 `6d28bb0412be08e7b54d5725d73fc4918566e9415bfcaa66f033101cfd57ac84`. Ele contém os dois ZIPs originais intactos e um manifesto verificável, evitando dois uploads manuais.

O arquivo está em [lab-inputs](../lab-inputs/README.md). A identidade binária coincide com o pacote original: Git blob `98af6c8b7b12cc06140686f74220716704384741`; commit de upload `dca4e3c755da4effbb01104965da6e71c6135b7d`.

O [workflow Native Engines](../.github/workflows/native-engines.yml) verificou o pacote combinado e os manifestos de ambos os ZIPs e executou código original do VLAB e do LEVEL-UP. [Execução remota de aprovação](https://github.com/arthof09-ai/assimilat-rpg-integracao-test/actions/runs/39675022018) e [PR #6 da correção](https://github.com/arthof09-ai/assimilat-rpg-integracao-test/pull/6) com quatro testes de portabilidade aprovados.

**Importante:** a execução remota está **PASS no escopo TEST**, não certificada como implementação canônica. O primeiro job remoto #1 falhou estritamente na exigência de igualdade física de bancos SQLite, antes da correção: [registro da falha](https://github.com/arthof09-ai/assimilat-rpg-integracao-test/actions/runs/39674136110). Em máquinas diferentes, os 8 bancos regenerados têm **0/8 SHA de arquivo coincidente, mas 8/8 fingerprints semânticos coincidentes**, incluindo esquema e todas as linhas, além do resultado PASS do auditor mecânico original (8 lutas, 155 commits, 640 eventos). Se qualquer linha/esquema mudar, o teste falha. No ambiente local original, os oito bancos foram byte-idênticos.

O workflow preserva compatibilidade com ZIPs separados eventualmente disponíveis, mas o plano preferido e mais simples para Android é **um único upload** do pacote combinado.

## Integração contínua futura

A versão original já está salva. O Comestre poderá propor **alterações de código em branches** e comparar a execução contra o baseline original. O GitHub preserva histórico de alterações, regressões, seeds, resultados e erros. Não constitui COMESTRE-ID ou atribuição de writer. O responsável da operação continua dono de seu laboratório.

## Hierarquia do RPG

- [Sistema de Combate](https://app.notion.com/p/3ebc2b324ede81f1be4be8804ac113c0), [Criação de Ficha](https://app.notion.com/p/3ebc2b324ede81449222f3c06b840613) e [Transformação Espiritual](https://app.notion.com/p/3f2c2b324ede81c0ae0ee4e66212edc9) prevalecem sobre fixtures; dados incertos permanecem UNKNOWN.
- [Laboratório VLAB](https://app.notion.com/p/3fbc2b324ede80e0b28cd227967a19ea), [Laboratório LEVEL-UP](https://app.notion.com/p/3fbc2b324ede804a95fafcb7b293c92c) e suas OPs continuam intocados.
- [Diário da integração](https://app.notion.com/p/400c2b324ede8102ad79e3c9d54a34ef) e [Diretriz GH-RP-01](https://app.notion.com/p/400c2b324ede8147bc9af2160e0b1a8e) controlam continuidade e limites.
- **Replit suspenso**, sem novos gastos, por decisão do Mestre.

**Estado:** GitHub CI original VLAB R237 **PASS (8 combates, 8/8 bancos semanticamente idênticos)**; LEVEL-UP R216-P12 **PASS 184/184 casos direcionados**; 2.026 testes históricos **não reproduzidos neste CI**. TEST / produção, Party, O Primeiro e cânone **HOLD/NO-WRITE**. Replit suspenso.
