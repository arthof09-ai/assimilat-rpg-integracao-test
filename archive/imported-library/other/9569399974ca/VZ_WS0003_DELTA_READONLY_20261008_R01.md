# DELTA READ-ONLY R01 — CM-000005 / WS0003 / 2026-10-08

**Tipo:** Adendo de evidência independente ao pacote congelado. **Não substitui nem modifica** os arquivos executivos prévios. **NÃO É REGISTRO CANÔNICO NOTION**.

**Controle:** `NOTION-PERSISTENCE=PENDING`; `INSTANCE-I0011=UNCLAIMED`; `ARCHITECTURAL-ABSORPTION=HOLD`; `MATERIAL-ABSORPTION=DENY`; `R07=HOLD`; `MATERIAL-WRITER=NONE`; `PARTY-WRITE=0`.

## D1. Integridade e fronteira de materialização — observado no CSV congelado

- 200 linhas, 200 `SLOT_ID` diferentes e 40 `BEAST_ID` diferentes; exatamente cinco posições por Besta.
- 50 linhas com `ORIGIN=LEGACY-B / E2` e 150 com `ORIGIN=PROPOSTA DE DESIGN / SEM ID UAT`.
- 200/200 `SOURCE_ID=NÃO ATRIBUÍDO`; 200/200 `OFFER_ID=NÃO ATRIBUÍDO`; 200/200 `CREDIT=0`.
- 165/200 posições possuem `CONFLICT` textual preenchido; engloba 150 propostas não canonizadas e 15 posições históricas vinculadas a B04/B09/B10. Isto é anotação de risco, NÃO 165 conflitos independentes comprovados.
- Duas propostas contêm resíduos de ninho (`B-VZ-FAL-04` e `B-VZ-BOS-10`). Até demonstração de origem animal e obtenção, não contar automaticamente como drops verdadeiros de espécie. Propostas com pólen aderido também exigem demonstrar que não são simples recurso vegetal externo. Não remover/alterar as posições congeladas; exigir validação de ecologia no gate posterior.

## D2. Reconciliação B04, B09, B10 — disposição de design proposta

**B04 → `B-VZ-PAN-02` Crocodilo de Lodo Astral**: `LEGACY-B/UAT-B-B04` registra Terra/Espectral, Ouro 1★ e Pântano; `BEAST-VZ-CORPUS-40` registra Água/Espectral, L2, Pântano. **Disposição:** `ALIAS-TO-FINAL + CONFLICT-HOLD` para elementos/patamar. Preservar cinco drops legados `UAT-B-D04A..E` como históricos `BLOCKED-BEAST`. A afinidade Água/Espectral do blueprint E3 é referência vigente de design, não licença para reinterpretar retrospectivamente os cinco drops. Verificar anatomia e funções contra a espécie final, eventual variação ecológica/estelar por fonte, com autoridade canônica competente; não criar crocodilo alternativo.

**B09 → `B-VZ-BOS-03` Lobo de Bruma Nula**: `LEGACY-B/UAT-B-B09` registra Espectral/Vento e transição Pântano/Falésias; E3 registra Espectral/Gelo e Bosque (transições frias). **Disposição:** `ALIAS-TO-FINAL + HABITAT-HISTORICAL-PENDING + ELEMENT-CONFLICT-HOLD`. Bioma primário de design E3 = Bosque; biomas históricos Pântano/Falésias **não** autorizam quota CORE regional sem `REGION-BINDING` independente e comprovado. Drops `D09B` (Falésias) e `D09D` (Pântano) perdem elegibilidade presumida de CORE até prova; IDs históricos continuam íntegros. Não duplicar espécie por bioma.

**B10 → `B-VZ-FEN-03` Besouro do Horizonte Fendido**: `LEGACY-B/UAT-B-B10` registra Bosque/Fenda, Luz/Terra; E3 registra Fenda primária e Terra/Luz. **Disposição:** `ALIAS-TO-FINAL + PRIMARY-BIOME=FEN + SECONDARY-HABITAT=HISTORICAL-PENDING`. `D10D` (CORE Bosque) exige prova de ocorrência natural no Bosque e elegibilidade regional; não recontar como Bosque só porque o histórico o menciona. Não duplicar espécie.

**Observação transversal:** as três disposições são *propostas de reconciliação*, não correções efetivas no Notion. Só há uma identidade `B-VZ-*` corrente para cada espécie. Preservar o `UAT-B-Bxx` como alias de origem com suas diferenças documentadas; diferenças anatômicas, elementais e geográficas continuam `NAC-NORM-HOLD` até decisão competente.

## D3. Economia — prova faltante, sem alteração de denominador

- Cadeia obrigatória: `BEAST-ID → DROP-LEGACY-ID/DESIGN-SLOT → SOURCE-ID (ou alias / noncommercial) → PRODUCT/REC-ID (se aplicável) → OFFER-ID/STORE-ID/CITY-ID → ROUTE-ID[] (se importado)`.
- O corpus atual de 200 posições comprova somente o primeiro vínculo nominal (Besta→posição/drop histórico). Não comprova vinculação a SOURCE ou OFFER.
- `SHOP-VZ-EXEC-01` define quatro lojas, `252` ofertas por loja, total `1008`, mínimo `420` fontes únicas, `≥60` assinaturas exclusivas por cidade e `≥84` staples comuns; nenhum desses critérios pode ser considerado atendido por uma posição de drop. `OFFER≠SOURCE`.
- `RECIPE-VZ-CORPUS-48`: 48 blueprints, 143 ingredientes RV documentais, 7 receitas com dependência cross-bioma; nenhuma ligação direta nominal dos 50 IDs legados de drops como ingrediente dessas 48 receitas. Outros consumidores não foram completamente descartados nem comprovados.
- Fórmula-base: `1008 + 420 + 96 + 40 + 1 + 32 + 48 + 4 = 1649` (MATERIAL=0). Cenário aritmético hipotético `420+150 = 570` e `1649+150 = 1799` requer **prova de 150 SOURCE-UAT independentes**, manutenção dos outros componentes e revisão de quotas/lojas/fanout. Não promover.
- A lacuna de adjudicação é **nominal e econômica**, não uma falha de somar 200 posições: SOURCE/alias/consumidor e classificação por drop seguem PENDENTES. É proibido atribuir SOURCE-ID ou criar OFFER-ID sem gate material e validação de identidade.

## D4. Incidente, escritor e retomada

- `SCI-WS0003-I0011-ALLOC-20261008`: readback do Diário consultado nesta execução não localizou marcador. `NEXT-INSTANCE-SEQ=I0011` no Perfil. Nenhum claim novo foi observado no Control. O erro histórico de `notion_update_page/insert_content` foi explícito: `Esta ferramenta foi bloqueada pelas configurações de segurança da OpenAI. Verifique novamente o que está enviando.`
- **Não** foi feita uma nova operação de escrita; logo, disponibilidade de escrita posterior NÃO foi testada nem afirmada. Restauro depende da via legítima indicada no relato de suporte congelado.
- Primeiro microbloco após liberação verificada: `REOPEN Diário/Perfil/Control → REGISTRO ANTES → REOPEN → alocação I0011 válida → CLAIM/GATE do domínio PROMO → PATCH-01 HO02→HO03 → REOPEN/VERIFY → REGISTRO DEPOIS → RELEASE/REPA/NAC-PASS proporcional`.
- Enquanto bloqueada: `PATCHES-APPLIED=0/6`, `REGRESSION=11/16 histórico`, `ABS-A..K=HOLD`, `ABS-L=DENY`, scheduler não armado, Party zero write.

## D5. Fontes Notion consultadas por leitura

- BEAST-VZ-CORPUS-40: https://app.notion.com/p/3f2c2b324ede81f4857edfd583fb58f9
- LEGACY-B: https://app.notion.com/p/3f1c2b324ede81b39225fc1a7733c602
- NORM-BEAST-DROP-ECO-01: https://app.notion.com/p/3f2c2b324ede8167b225ca27ea5784b0
- Matriz 09: https://app.notion.com/p/3f1c2b324ede8145be13d394780e6d2c
- SHOP-VZ-EXEC-01: https://app.notion.com/p/3f2c2b324ede8141b3beecc19564305a
- REC48: https://app.notion.com/p/3f2c2b324ede818ab73edfd8e5ffc525
- Manifesto: https://app.notion.com/p/3f2c2b324ede81fc9a31e1b6472a0418
- Diário: https://app.notion.com/p/3f1c2b324ede81e5a480ef85fb003b8e
- Perfil: https://app.notion.com/p/3f1c2b324ede818ba68be8179405fca7
- Control: https://app.notion.com/p/3f1c2b324ede81ed832becc1845029cf

**No changes were made to frozen baseline XLSX/CSV/MD/support note/QA image.**
