# Integração dos motores originais — VLAB R237 e LEVEL-UP R216-P12

**Status: preparada, mas execução GitHub do VLAB/LEVEL-UP ainda depende de transferir os dois ZIPs originais.** Não confundir a aprovação dos testes preparatórios com a execução dos motores.

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

## Último passo para executar **no GitHub**

A ferramenta conectada ao ChatGPT atualmente publica **arquivos de texto**, mas não transferiu os ZIPs binários diretamente para este repositório.

O Mestre pode adicionar **uma única vez** os ZIPs originais ao diretório `lab-inputs/` do repositório privado, preservando os nomes exatos. No Android, abrir GitHub pelo Chrome, repositório privado → **Add file → Upload files**, selecionar os ZIPs baixados da conversa e confirmar o commit. Não é necessário programar.

O workflow [Native Engines](../../.github/workflows/native-engines.yml) então testa automaticamente os arquivos adicionados; também pode ser iniciado pelo menu **Actions → VLAB & LEVEL-UP — Native Engines (TEST) → Run workflow** quando houver entradas. Se só existir um arquivo, testa apenas aquele e identifica o outro como **NOT PROVIDED / NOT TESTED**. Não concede PASS sem executar código.

## Integração contínua futura

Depois que a versão original estiver salva, o Comestre poderá propor **alterações de código em branches** e comparar a execução contra o baseline original. O GitHub preserva histórico de alterações, regressões, seeds, resultados e erros. Não constitui COMESTRE-ID ou atribuição de writer. O responsável da operação continua dono de seu laboratório.

## Hierarquia do RPG

- [Sistema de Combate](https://app.notion.com/p/3ebc2b324ede81f1be4be8804ac113c0), [Criação de Ficha](https://app.notion.com/p/3ebc2b324ede81449222f3c06b840613) e [Transformação Espiritual](https://app.notion.com/p/3f2c2b324ede81c0ae0ee4e66212edc9) prevalecem sobre fixtures; dados incertos permanecem UNKNOWN.
- [Laboratório VLAB](https://app.notion.com/p/3fbc2b324ede80e0b28cd227967a19ea), [Laboratório LEVEL-UP](https://app.notion.com/p/3fbc2b324ede804a95fafcb7b293c92c) e suas OPs continuam intocados.
- [Diário da integração](https://app.notion.com/p/400c2b324ede8102ad79e3c9d54a34ef) e [Diretriz GH-RP-01](https://app.notion.com/p/400c2b324ede8147bc9af2160e0b1a8e) controlam continuidade e limites.
- **Replit suspenso**, sem novos gastos, por decisão do Mestre.

**Estado:** TEST / produção HOLD / integração remota VLAB e LEVEL-UP ainda NÃO comprovada até obter os ZIPs no GitHub e observar os jobs.
