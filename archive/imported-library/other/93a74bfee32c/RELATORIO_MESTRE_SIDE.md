# REG-ROUTE-03 — Auditoria estrutural do snapshot histórico Party (16/10/2026)

**Executor:** Comestre MESTRE-SIDE. **Natureza:** auditoria histórica sem qualquer escrita no workspace Party. **Escopo:** arquivo ZIP entregue pelo Mestre e árvore `Party` exportada, não todos os possíveis conteúdos do workspace independente. **NAC-PASS-02:** HOLD para fechamento semântico/global; PASS somente para preservação e inventário estrutural deste snapshot.

## Identidade e cadeia de custódia

- Arquivo ORIGINAL recebido: `ExportBlock-70f91013-f3b3-41f5-98bd-45f3bf8c0322.zip`.
- SHA-256 do ZIP original: `b44b97f68f983393c8f8fa91f0986513b6875af7bd89cd89bf1cf28fb3554769`; tamanho exato: 210,198,127 bytes.
- O mesmo ZIP bruto foi preservado na Biblioteca pessoal do projeto, em `/Comestre/REG-ROUTE-03/HISTORICO-PARTY-EXPORT-20261016-ORIGINAL.zip`; **re-materializado da Biblioteca e SHA-256 confrontado com o original, idêntico**.
- ID persistente Biblioteca: `libfile_23a23964c3d08191ba57263c280bf5cf` (arquivo de armazenamento, não UUID de página Notion).
- Integridade ZIP: `testzip()` PASS; 1688 entradas sem erro de leitura; 0 objetos tocados na Party.

## Inventário do arquivo recebido — fechado para este ZIP

| Unidade | Resultado |
|---|---:|
| Páginas HTML | **1.064** |
| UUIDs HTML únicos | **1.064** (sem colisão) |
| Páginas HTML alcançáveis por links locais desde a raiz Party | **1.064/1.064** |
| Links internos HTML ausentes | **0** |
| Mídias locais JPG/PNG/JPEG/JFIF | **623** |
| Referências internas de mídia local ausentes | **0** |
| Arquivos CSV | **1** |
| Referências a mídias remotas (não incluídas) | **512 ocorrências / 248 URLs únicas / 235 páginas** |
| Páginas HTML sem texto extraível | **130** |
| Páginas com menos de 100 caracteres de texto | **400** |
| Grupos de títulos repetidos entre UUIDs distintos | **188** |

Distribuição por ramo da árvore Party exportada (incluindo índices):

- **(ROOT PARTY):** 1 páginas.
- **ALQUIMIA:** 106 páginas.
- **ANOTAÇÕES:** 4 páginas.
- **Armadura Média (ON) (1):** 1 páginas.
- **Armadura leve (ON) (1):** 1 páginas.
- **Bíblia da Assimilação (Party):** 12 páginas.
- **FICHAS:** 149 páginas.
- **INVENTÁRIO:** 341 páginas.
- **ITENS BIOMAS:** 99 páginas.
- **OBJETIVOS:** 4 páginas.
- **PADRÕES DE INSCRIÇÕES:** 143 páginas.
- **Personagens Party:** 160 páginas.
- **Registro de Alterações da Party:** 21 páginas.
- **Sessões — Continuidade das Players:** 22 páginas.

**Atenção de denominador:** a exportação começa na página `Party` (`ce39c16dd49582288da2816aacd02201`). A raiz superior `RPG assimilação` do workspace oficial não está incluída. Não extrapolar a cobertura do ZIP para páginas privadas/compartilhadas que estejam fora desta árvore.

## Achados fundamentados

**PTY-001 — Master→Party:** a Bíblia da Assimilação (Party) exportada contém **97 hiperligações para 95 UUIDs de páginas Master**. Todos os 95 destinos foram reabertos pela conexão Master; tentativas dirigidas por conexão Party com dois desses UUIDs retornaram NOT_FOUND. O próprio conteúdo do texto da Bíblia da Party continua contendo essas referências no Notion vivo. **88/97 links possuem um candidato por nome entre as páginas locais Party; equivalência semântica, abrangência e permissão de divulgação ainda não estão homologadas.** O apontamento de um link Master não demonstra vazamento do conteúdo protegido, mas constitui dívida de referências cross-workspace e risco de rota inadequada.

**PTY-002 — referências externas históricas:** outras **79 ocorrências** na Bíblia apontam para **52 UUIDs externos não exportados** (78 ocorrências com formato `3b130166...`, mais uma de outro padrão). Dois alvos de `3b130166...` testados não foram encontrados por nenhuma das duas conexões; os demais não tiveram acesso individualmente validado. Não presumir que foram deletados.

**PTY-003 — links malformados no HTML:** páginas `Lu Pião` e `Porção de pó de osso` contêm a string `https://app.notion.comundefined` no export. Há outra URL no domínio Notion de proxy de imagem, **que não é uma URL quebrada de página**. As duas âncoras malformadas exigem revisão na UI/representação Notion, pois a leitura pelo conector não reproduziu literalmente a mesma URL.

**PTY-004 — duplicação nominal:** 188 grupos de títulos recorrentes, com 752 pares combinatórios. **545 pares têm texto extraído idêntico, mas 546 pares têm pelo menos um corpo quase vazio.** Outros **21 pares** possuem ≥100 caracteres em ambas as páginas e similaridade textual menor que 0,6; isso não demonstra incompatibilidade mecânica. Duplicatas por função, inventário, personagem/versão e catálogo não devem ser eliminadas sem governança.

**PTY-005 — dependências externas:** 512 referências a mídias remotas; o ZIP é estruturalmente íntegro mas não autocontido visualmente. Não houve teste de disponibilidade externa, e ausência de arquivo local não foi diagnosticada nessas URLs.

**PTY-006 — registros de operação na área apropriada:** O Primeiro, Diário Operacional do Primeiro, Registro de Alterações da Party, modelos e auditorias player-side contêm legitimamente termos administrativos. Essa presença não configura contaminação por si. Uma varredura semântica independente do Master é necessária para distinguir trechos realmente proibidos.

**PTY-007 — banco CSV exportado:** Catálogo de Itens contém duas referências Notion externas na coluna Name que não aparecem nas páginas HTML deste snapshot, além de linhas vazias. Revisar sem deduzir ausência de itens/estoque e sem inventar quantidades.

## Certificação e limites

- **100% DO SNAPSHOT / INVENTÁRIO E INTEGRIDADE ESTRUTURAL:** VERIFICADO para os 1.064 HTML + 623 mídias locais + CSV e seus enlaces locais.
- **100% DA CLASSIFICAÇÃO SEMÂNTICA E DA AUSÊNCIA DE MASTER-ONLY NA PARTY:** **NÃO CERTIFICADO.** Todas as 1.064 páginas tiveram texto lido por programa e padrões examinados, mas a inspeção semântica humana/mecânica não substitui comparação com o Master, análise das 130 páginas textualmente vazias, conteúdos de imagens, links externos e permissões.
- **100% WORKSPACE PARTY INDEPENDENTE:** **NÃO DETERMINÁVEL** apenas com esta árvore exportada.
- **100% GLOBAL MASTER+PARTY E REG-ROUTE-03:** **HOLD**, Master export ainda pendente.
- **SANEAMENTO:** zero páginas Party alteradas, zero correções aplicadas. Esta análise não autoriza criação silenciosa de versões ou links novos.

## Rota de retomada após chegada do Master

1. Preservar snapshot Master original com hash próprio e sem sobrepor Party histórica.
2. Fechar o inventário Master e confrontá-lo por UUID/raiz/link; preservar 1.064 como denominador **somente do ZIP Party**.
3. Reconciliar 95 UUIDs Master ligados pela Bíblia Party contra os candidatos player-safe, aprovando equivalência sem vazamento; tratar 52 links externos separadamente.
4. Comparar fichas atuais e históricas, imagens e 21 pares divergentes, aplicar taxonomia competente e registrar exceções.
5. Determinar o alcance canônico de saneamento sob CG0–CG5 e NAC-CONT-03, sem editar Party produtiva automaticamente.
6. Reconciliar 362 segmentos da matriz original do REG-ROUTE e validar NAC-PASS-02 antes de qualquer declaração de 100% global.

**Checkpoint:** 16/10/2026. **Próxima fronteira:** Master snapshot + cobertura do workspace independente fora da árvore Party exportada + classificação semântica cruzada. **Fonte física:** original em Biblioteca, índices CSV neste pacote, registro Mestre-side da operação.
