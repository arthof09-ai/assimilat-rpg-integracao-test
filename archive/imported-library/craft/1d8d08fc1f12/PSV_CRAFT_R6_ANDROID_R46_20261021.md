# PSV — CRAFT R6 · Continuidade Mestre-side e pré-dossiê R46 no Android

**Data-base:** 21/10/2026 · **Operação original:** `OP-ARQ-RIN-REC-01` · **Workstream:** `CM-000002-WS0001` · **Identidade:** CM-000002 lógica, sem `INSTANCE-ID` ou writer assumidos. 

## 1. Ponto ANTES recuperado

O Notion Mestre e a Biblioteca pessoal foram reabertos. Checkpoint anterior R5: `CRAFT-R5-MOBILE-GATE-20261021-001`, com bancada offline v1.2 e revisor JavaScript/Node no mesmo núcleo `logic.js`. O arquivo PSV do R5 estava desatualizado na Biblioteca; foi substituído **no mesmo ID**, recuperado byte a byte e validado:

- `/Comestre/PSV_CRAFT_R5_ANDROID_20261021.md`
- `libfile_0a9b187e2f6c81918be468afca5711cc` · **7.494 B** · SHA-256 `47c6286637b4567f2eb8e22a31930cbb71317fe36f7746d1cae3f80a598689da` · readback PASS.

Bancada R5 original permaneceu imutável: ZIP SHA-256 `29b4bfb61a726bd4e12bffa8e245552831003ca5f3e1b7e4f5edcbd7f65eb6e8`; núcleo `logic.js` SHA-256 `a346889dd1cc59826d7d0ce24a16a9444d7587d316f63eccd1034dfc8be6e484`. Regressões 63/63 e 26/26 foram reexecutadas PASS antes da evolução.

## 2. R6 realmente implementado

**Lacuna funcional identificada:** o R46 existente requer amostras/lotes, `reading_id`, unidade e incerteza, identificação instrumental e calibração, fuso horário, cadeia de custódia, quatro conjuntos de anexos com bytes/sha e revisão independente. O R5 captura medidas, mas não emitia um pré-dossiê que explicite lacunas para o especialista. Não havia razão para criar outro motor científico.

**Delta R6:** o mesmo HTML offline agora exibe **v1.3** com o botão **Exportar pré-dossiê R46**, usando adaptador JS pequeno e único (`r46_predossier.js`). O avaliador QA R5 permanece byte-idêntico. O botão reaproveita os registros da sessão e gera documento `CRAFT-R46-PREDOSSIER/1.0-TEST-NONNATIVE`, exclusivamente preparatório e Mestre-only.

- **Inclui:** B30-01 Tábua Lamelar (fonte PS Ardósia, CRN `CRAFT-F5-R01-MIN-01`) e B30-03 Mica (CRN `CRAFT-F5-R01-MIN-02`). Leituras mm/count/bool recebem IDs de rascunho e preservam dados *declarados*, não atestados.
- **Exclui com motivo:** B30-02 Cordão de Casca Boreal, porque o R46 recebido cobre apenas Tábua/Mica, sem adaptar silenciosamente o contrato nativo.
- **Controles comuns:** não herdam falsamente `source_page_id`/`source_crn_id` dos materiais PS; sua procedência continua pendente.
- **Limites rígidos:** `report_id=null`, `recipe_key=null`, `observed_at=null` quando só há hora local sem fuso, `artifacts=[]`, `custody=[]`, `r46_import_ready=false`, `physical_measurement_verified=false`, `execution_authorized=false`, `official_rec_ids_created=0`, `stock_effect=0`, `notion_write=false` e `party_write=false`. A classificação permanece `QUARANTINE_INCOMPLETE_NO_AUTOCANON`.
- **Comprovantes ainda necessários:** fonte/lote real, identidade e competência do operador, série e calibração rastreável do instrumento, fuso e tempo, método/condições, custódia, quatro anexos primários e revisão independente. Nenhuma dessas provas foi inventada.

O usuário Android não precisa de Node, Python ou internet para operar o novo botão em navegador compatível. O CLI facultativo usa o mesmo código de transformação para revisão posterior.

## 3. Testes e evidências de integridade

| Categoria | Resultado |
| --- | --- |
| Testes novos R6 do adaptador | **35/35 PASS** |
| Regressão QA original R5 | **63/63 PASS** |
| Regressão revisor Node R5 | **26/26 PASS** |
| Vetores metrológicos sintéticos R5 | **2.000 PASS** (não são novos testes unitários) |
| Chromium móvel 390x844 | **2 E2E PASS** (fluxo R5 e export R46 R6) |
| Pré-dossiê produzido pelo navegador versus CLI Node | **Identidade semântica PASS** |
| ZIP vR6 | **21 membros, CRC PASS, manifesto 20/20 SHA PASS** |
| Replay frio da extração ZIP local | **PASS** |
| Replay frio da cópia baixada da Biblioteca | **PASS** |

Os resultados foram obtidos com **amostras sintéticas**; nenhuma medição física externa foi submetida. O campo de controle exige origem não autenticada e nenhum dado foi enviado à Party/O Primeiro.

## 4. Biblioteca Mestre — arquivos finais, readback

| Artefato | ID da Biblioteca | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `/Comestre/CRAFT_R6_ANDROID_R46_PREDOSSIER_20261021.zip` | `libfile_2ab2ea33eb248191b586d079f8f42c62` | 399.393 | `a3d28127fee7a4fae43be7b9356832318e359e5ccb560e394324f732f247698f` |
| `/Comestre/CRAFT_BANCADA_ANDROID_R6_OFFLINE.html` | `libfile_802988569364819191fb0c45ceb7444d` | 36.806 | `6607aa235196629f5cee6242458787ef2ee4a2056db22cbb3b04f24e4624420c` |

Ambos foram publicados, materializados em diretório separado, comparados byte a byte e aceitos. O ZIP contém baseline R5 completa PINNED, código vR6, 35 testes novos, regressões R5, exemplos sintéticos, manual Mestre Android e protocolo de continuidade interna. Os arquivos R5 originais na Biblioteca não foram substituídos por R6.

## 5. Persistência Notion e governança

- **LAB ANTES/DEPOIS:** `CRAFT-R6-R46-MOBILE-PREDOSSIER-20261021-001` — https://app.notion.com/p/3fbc2b324ede811db848d35d4739eb00, com hashes/replay/verificação e readback.
- **Diário OP:** seção com mesmo TRACE registrada no corpo do objeto original https://app.notion.com/p/3f1c2b324ede81d7aa79c83106240516 e relida. O comentário também foi solicitado, mas seu readback individual não foi confirmado pelo leitor de comentários; a seção da OP é a prova persistente confirmada.
- **IBX-116 existente:** devolutiva no objeto https://app.notion.com/p/3ffc2b324ede817aa3abea3cb7ba8c08, sem ticket novo, `Estado=NOVA`, `Exige ACK=YES`. Leitura posterior confirmou o texto e checksum.

**R51, read-only:** buscado destino físico Receitas & Fórmulas sob raiz Mestre Itens e por sinônimos, também em busca global. O resultado de busca de conteúdo foi limitado a 50 por chamada e retornou frequentemente itens cujos *corpos* mencionam receitas, não pasta com parent validado. Em conjunto com a inspeção anterior de 17 filhos diretos da raiz, nenhuma área física REC-LIB única foi verificada. **Isto não comprova inexistência global.** Nenhuma pasta movida/criada, nenhum UUID de parent inventado.

**IBX-117:** já triada anteriormente como metodologia VLAB/DMG TEST (20 testes), sem nova tarefa. **IBX-115/PA:** errata Mestre da tarifa já havia corrigido interpretação CRAFT, sem defeito no motor PA R26/R27; não foi recriado fornecedor PA.

## 6. NAC-PASS proporcional e ponto exato de retomada

**PASS:** evolução documental/software R6; regressões, cobertura adversarial, navegador Chromium móvel, integridade ZIP/manifest, publicação e readback Biblioteca, sincronização de registro LAB/OP/IBX.

**HOLD:** abertura de arquivo `file://` em Android físico específico não foi verificada; nenhuma identidade de operador, instrumento, certificado, anexo, hash de byte primário real, cadeia de custódia ou assinatura foi fornecida; nenhum laudo R46 **nativo** foi produzido; nenhum desempenho material/mágico do item foi demonstrado.

**Gates globais:** F5 P0 RED; C19-021 UNKNOWN-EFFECT; IBX-38 sem prova de fencing técnico; R51 sem parent REC-LIB único certificado; P2-SALT-01, P2-ENERGY-02, Óleo de Vedação e ensaio H2-3A/B pendentes; RC5/P4/PRODUÇÃO HOLD. `Party` e `O Primeiro`: 0 writes; estoque, itens, ficha, receita, PA e R48: 0 writes. Sem `INSTANCE-ID`, `ACK`, `writer`, `epoch`, `lease`, `fence` ou GREEN autodeclarado.

**Retomada em ordem:** (1) quando houver operadores e evidência primária, usar a bancada Android para coletar e gerar o pré-dossiê, sem chamar isso laudo nativo; (2) submeter as leituras, anexos e cadeia de custódia reais ao motor R46 e revisor independente conforme norma; (3) só com ato técnico de fencing e reconciliação C19 + parent REC-LIB/autorização, considerar um microbloco RC5, com NAC-PASS próprio; (4) antes disso, trabalhar em frente funcional segura verdadeiramente não realizada, nunca inventar RC5 ou refazer R48/QMC/R5/R6.

**Estado final deste checkpoint:** CRAFT-R6 software concluído e persistido. Operação CRAFT global continua aberta e em HOLD material.
