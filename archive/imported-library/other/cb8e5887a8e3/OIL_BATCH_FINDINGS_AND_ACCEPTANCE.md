# Busca dirigida de Óleo de Vedação acabado — resultado e teste de custódia

## Fontes efetivamente verificadas

| Fonte | Referência | Que prova | Que não prova |
|---|---|---|---|
| Página oficial de Poções | https://app.notion.com/p/3edc2b324ede81f1a88ec69980ab6cfd | Existe receita/função descrita; item está catalogado | Lote, quantidade, fabricação realizada, validade ou detentor |
| Receita histórica | https://app.notion.com/p/75fc2b324ede83d492f881e556dc03f8 | Variante textual preservada | Lote disponível ou superioridade à fonte vigente |
| Registro histórico de produto | https://app.notion.com/p/803c2b324ede83fc8f0f0132ffd6a199 | Valor histórico **1.270.000 MED** e descrição funcional | Estoque, reserva, compra, preço atual ou certificação |
| Índice Poções oficial | https://app.notion.com/p/3edc2b324ede817f867efa0dc8cac5e0 | **7 fichas** cadastradas, incluindo óleo | **7 frascos** ou disponibilidade |
| Manifesto MAN-CRAFT-F1-001 | https://app.notion.com/p/3f1c2b324ede81b393fbe1a235524796 | 212 UCO são páginas de recursos | Estoque real de poções ou lotes de óleo |
| Catálogo Party (Mestre — Espelho), somente leitura | data source `collection://d8bc2b32-4ede-82b2-8dc4-87f0dac72a9e` | SQL conferiu **10 linhas**; 0 nomes com “Óleo” ou “Vedação” | Ausência noutros catálogos, contas e armazéns; espelho pode estar defasado |
| Loja Chamas Divinas Mestre-side | https://app.notion.com/p/3f5c2b324ede81ae848ff4da661c6707 | Texto consultado sem oferta identificável de Óleo de Vedação | Não há nenhum vendedor em toda a campanha |
| Google Drive conectado | 3 buscas de metadados (Óleo de Vedação; CRAFT estoque; Inventário recursos Assimilação) | Nenhum arquivo encontrado nesse recorte | Arquivos sem indexação, páginas de Notion e estoques in-game |

**Resultado real nesta execução:** `0/3 referências de óleo qualificadas como lote`, `0/10 nomes no banco de inventário do espelho`, `0/3 buscas Drive com resultados`; **não inferir quantidade global zero**. Nenhum frasco foi criado, adquirido, reservado ou consumido. Não houve certificação de qualidade.

## Contrato de aceitação de um possível lote futuro

Lote só é candidato para H2-3 com: identidade exata do Óleo, `lot_id`, documento de produção ou origem/acervo, quantidade e unidade verificáveis, titular/custódia, integridade, condições de conservação, disponibilidade atual, autorização de uso exclusivamente TEST, compatibilidade com a P2, readback da fonte e método reversível de registro de consumo. **Uma ficha de produto ou preço histórico não contém esses dados.** A ausência de um deles mantém HOLD.

A ferramenta `code/lot_and_ticket.py` executa hoje a **negativa de admissão baseada nas fontes**. Mesmo um lote simulado com todos os campos fica marcado `LAB_FIXTURE_IS_NOT_MATERIAL_LOT`. Uma linha documental aparentemente completa sem fetch de verificação recebe `REQUIRES_INDEPENDENT_AUTHORITY_SOURCE_READBACK`, não PASS. O código **não reserva estoque real**.

## Decisão prática

Rota curta: fornecedor legítimo já acabado **se** surgir lote autenticado e apropriado. Enquanto não houver, o procedimento de fabricar o Óleo permanece dependente da reconciliação própria da receita, inclusive Orvalho Amanhecer/Dragão, Essência Lua Minguante/Vórtice, passo 2 truncado e 3× vs 2× Ferro Celestial da versão vigente e histórica. A P2 ainda exige sanar sal e energização independentemente do óleo.
