# CRAFT — Guia rápido do Revisor R16 (Android / MESTRE-SIDE TEST)

**Atenção:** este HTML contém dados do Mestre, inclusive fichas e observações internas. Não encaminhar o arquivo, o pacote, o relatório nem suas exportações à Party ou ao O Primeiro. Não é item pronto, receita RC5, laudo mágico ou publicador do Notion.

## Primeira utilização

1. Abra no seu Android o arquivo privado **`CRAFT_R16_REVISOR_ANDROID_OFFLINE_TEST.html`**. Abertura local em Android físico ainda não foi certificada; depende das permissões do navegador/gerenciador de arquivos. Se a abertura for bloqueada, não force permissões nem trate isso como homologação.
2. A tela inicial já contém **duas propostas TEST**. Toque em **Validar propostas** e confira `HOLD_TEST_DESIGN`, os links das fontes e os impedimentos. Nada será criado ou alterado no RPG.
3. Para revisar outro arquivo JSON de propostas, use **Carregar proposta** e escolha um `proposals.json` preparado dentro desta bancada Mestre. O importador rejeita arquivo inválido ou maior que 2 MiB, preservando o lote anterior.
4. Em lotes grandes, use **Página anterior / Próxima página**. Cada página exibe até **oito** projetos, mas o auditor processa todo o lote, sem alterar as regras do RPG.
5. **Salvar diagnóstico JSON** exporta todos os resultados QA, não apenas a página atual.
6. **Baixar roteiro de TODOS os projetos (Mestre TEST)** cria um pedido de evidências. Os campos instrumentais, de lote e observação permanecem `null/PENDENTE_NAO_OBSERVADO`; o arquivo não comprova medição, magia, custo nem autorização.

## O que este aplicativo NÃO faz

Não envia informações à rede por conta própria, não faz escrita no Notion, não altera o estoque, não transfere magia, não aprova PA e não produz receita RC5. A coleta de evidência física ou científica deve seguir o **R46 original** e operador competente, com instrumento/calibração, custódia, amostra, controles e laudo reais. Um relatório do navegador emulado não certifica funcionamento no seu telefone.

## Recuperação técnica

O pacote ZIP R16 contém `src/run.js`, `src/verify_outputs.js`, `data`, `tests`, manifesto de hashes e HTML. O recibo `OUTPUT_COMMIT.json` é do par de arquivos QA + prévia gerado via CLI TEST; verificar antes de tratá-los como consistentes. **Não é assinatura de autenticidade externa.**

Para retomar a operação CRAFT, consulte **`CRAFT_CHECKPOINT_SUCESSAO_R16_20261021.md`** na Biblioteca Mestre; ele discrimina os gates externos (IBX-38, C19-021, R51), os relatórios da R15 e o motivo da sincronização Notion posterior ao R13 ainda pendente.
