# Integração dos motores originais — VLAB R237 e LEVEL-UP R216-P12

**Status: preparada, mas execução GitHub do VLAB/LEVEL-UP ainda depende de enviar um único pacote ZIP combinado com os dois originais.** Não confundir a aprovação dos testes preparatórios com a execução dos motores.

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

## Último passo para executar **no GitHub** — uma única transferência pelo Android

Preparei **um só arquivo** para enviar, sem código, sem assinatura e sem computador:

**`ASSIMILACAO_NATIVE_INPUTS_R237_P12_20261021.zip`** (3.140.244 bytes), SHA-256 `6d28bb0412be08e7b54d5725d73fc4918566e9415bfcaa66f033101cfd57ac84`. Ele contém os dois ZIPs originais intactos e um manifesto verificável, evitando dois uploads manuais.

1. Baixar esse arquivo diretamente na conversa do ChatGPT, para o armazenamento local do Android. **Não extraia** o arquivo.
2. Pelo **Chrome**, acessar [lab-inputs](../lab-inputs/README.md) no repositório privado do Mestre.
3. Selecionar **Add file → Upload files**, localizar o arquivo ZIP único, fazer upload e tocar em **Commit changes**.
4. O [workflow Native Engines](../.github/workflows/native-engines.yml) verifica primeiro SHA-256 do arquivo combinado, extrai só os dois ZIPs pinados, valida os dois manifestos individuais e roda os programas originais VLAB R237 e LEVEL-UP P12. A página **Actions** mostrará se passou ou falhou.

**Importante:** a execução VLAB/LEVELUP no GitHub permanece **PENDENTE** até a presença real do pacote e prova do status do job remoto. O check verde no PR #5 aprovou apenas os testes preparatórios + ferramentas já integradas (DMG e CRAFT).

O workflow preserva compatibilidade com ZIPs separados eventualmente disponíveis, mas o plano preferido e mais simples para Android é **um único upload** do pacote combinado.

## Integração contínua futura

Depois que a versão original estiver salva, o Comestre poderá propor **alterações de código em branches** e comparar a execução contra o baseline original. O GitHub preserva histórico de alterações, regressões, seeds, resultados e erros. Não constitui COMESTRE-ID ou atribuição de writer. O responsável da operação continua dono de seu laboratório.

## Hierarquia do RPG

- [Sistema de Combate](https://app.notion.com/p/3ebc2b324ede81f1be4be8804ac113c0), [Criação de Ficha](https://app.notion.com/p/3ebc2b324ede81449222f3c06b840613) e [Transformação Espiritual](https://app.notion.com/p/3f2c2b324ede81c0ae0ee4e66212edc9) prevalecem sobre fixtures; dados incertos permanecem UNKNOWN.
- [Laboratório VLAB](https://app.notion.com/p/3fbc2b324ede80e0b28cd227967a19ea), [Laboratório LEVEL-UP](https://app.notion.com/p/3fbc2b324ede804a95fafcb7b293c92c) e suas OPs continuam intocados.
- [Diário da integração](https://app.notion.com/p/400c2b324ede8102ad79e3c9d54a34ef) e [Diretriz GH-RP-01](https://app.notion.com/p/400c2b324ede8147bc9af2160e0b1a8e) controlam continuidade e limites.
- **Replit suspenso**, sem novos gastos, por decisão do Mestre.

**Estado:** TEST / produção HOLD / integração remota VLAB e LEVEL-UP ainda NÃO comprovada até obter os ZIPs no GitHub e observar os jobs.
