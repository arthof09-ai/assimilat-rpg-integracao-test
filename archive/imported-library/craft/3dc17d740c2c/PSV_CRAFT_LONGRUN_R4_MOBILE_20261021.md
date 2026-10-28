# PSV de Sucessão — CRAFT R4 / Bancada Mobile + Auditor de Exportação

**Data operacional:** 21/10/2026. **Identidade lógica:** Comestre Executor CRAFT / CM-000002 / WS0001. **OP existente:** `OP-ARQ-RIN-REC-01`. **Superfície:** MESTRE-SIDE / LAB-TEST; Party e O Primeiro NO-WRITE. **Trace:** `CRAFT-LONGRUN-MOBILE-20261021-001`.

## 1. Reposição do estado canônico / não repetir

- Recuperados no Notion: LAB CRAFT https://app.notion.com/p/3fbc2b324ede811db848d35d4739eb00 ; Diário da OP https://app.notion.com/p/3f1c2b324ede81d7aa79c83106240516 ; Inbox destinatário CM000002, em especial IBX-116 https://app.notion.com/p/3ffc2b324ede817aa3abea3cb7ba8c08 ; IBX-38 https://app.notion.com/p/3f3c2b324ede817fb888ca32aacaf2de ; pedido R51 https://app.notion.com/p/3f4c2b324ede812a9153d39281b488f8 .
- Precedentes reais já executados: CRAFT R44/R45/R46 tinha QA metrológica em Python; QMC-01/QMC-02 possuíam bancada multicategoria e envelopes de fichas; R50_PLAN_B30-01 e B30-03_PRONTIDAO_RC5 foram recuperados da Biblioteca Mestre; a fábrica experimental R48 **já existe** e foi preservada. Não recriar nenhum desses motores.
- Recursos-fonte PS reabertos em Mestre: Ardósia de Geada Lamelar https://app.notion.com/p/3f3c2b324ede81acaf28c66a6b46e0b2 ; Mica de Bruma Boreal https://app.notion.com/p/3f3c2b324ede81e1b179e194e2838c84 ; Fibra de Casca Boreal https://app.notion.com/p/3f3c2b324ede815ab04ace5bd1074e79 . Não confundir disponibilidade documental de página com estoque/lote físico.
- Normas operacionais consultadas: PR-ITEM-02, REC-MOD-EQA-01, REC-LIB-01, AUD-CRAFT-F5-REMAP-01 e governança NAC. O escopo F5 R01/R02 é de backfill condicionado; F5 P0/RED, C19-021 UNKNOWN-SIDE-EFFECT e falta de fencing externo impedem novas RC5 oficiais. R51 ainda sem parent de receitas certificado.

## 2. Entregas desta retomada / estado ANTES → DEPOIS

### E4.1 — Bancada Android offline v1.0 (registro histórico mantido)

**ANTES:** limiares QA estavam em R50 e validadores em scripts Python, sem interface Android offline de preenchimento/exportação especificamente demonstrada nesta linha.

**DEPOIS:** HTML autocontido para B30-01 Tábua Lamelar e B30-03 Mica; identifica lote/amostra, instrumento, operador, calibração declarada, incerteza, dados geométricos e inspeção, pré-validando só limiares PROPOSTOS. Exporta JSON/CSV, sem rede e sem persistência oculta. 31/31 testes JS e navegação Chromium mobile PASS. ZIP histórico **não sobrescrito** `/Comestre/CRAFT_BANCADA_ANDROID_B30_01_03_20261021.zip` Library `libfile_4d186ea70a4081919c8709b34248debf` SHA256 `5df67b41eb29aee687c6ed01dbd23cb404fd830582b836defa29df81fbdd0fdb`.

### E4.2 — Evolução da mesma bancada para B30-02 v1.1

**ANTES:** B30-02 Cordão de Casca Boreal tinha design PRE-Q2: fibras entrada 2m→corda alvo 1m ±5cm, resistência mecânica a comparar com fibra vegetal comum, mas **sem carga de serviço homologada**.

**DEPOIS:** a mesma HTML do Mestre adicionou B30-02 com entrada de comprimento, fibra consumida, carga de ensaio/ruptura, alongamento e condições. Resultado sem erros geométricos é `NO_HOMOLOGATED_LOAD_THRESHOLD`; não existe caminho de aprovação automática de resistência por um número alto. Incerteza informada em mm convertida para cm no comprimento e propagada conservadoramente na Mica. Importação JSON v1.0 aceita com novo cálculo, sem confiar no parecer antigo. 40/40 testes Node e E2E Chromium mobile PASS; 5 larguras 320/360/390/412/768 px sem overflow, importação legada v1.0 e recálculo demonstrados.

**ZIP de código/auditoria:** `/Comestre/CRAFT_BANCADA_ANDROID_B30_01_02_03_V11_20261021.zip` Library `libfile_cf9aec52e4a0819186eb0103f4cf6dcc` SHA256 `021ce37de171e4ebb04c1a1b777d6f4e56191d0746e9d2ccb00e0e49145b8282` 483208 bytes; 11 ZIP/10 manifesto, CRC PASS e readback byte-idêntico, replay frio 40/40+E2E PASS.

**HTML standalone atual** `/Comestre/CRAFT_BANCADA_MESTRE_ANDROID_OFFLINE.html`, mesmo Library ID `libfile_3c8c676ea0f081918c5f6234eacc08de` (atualização em mesmo objeto; histórico v1.0 conservado no ZIP anterior), SHA256 `fc3be2a7000d9ac08dd5f3520c82f32d63b390b84db3a4a27858fd9edae9e867` 23005 bytes; readback Library byte-idêntico.

**Hotfix de aceite (versão atual, sem nova linha de produto):** a auditoria da UI detectou que os campos de inspeção visual partiam de estados favoráveis. Agora todas as verificações de trincas, delaminação, lamelas, encaixe e magia exigem resposta explícita **Sim / Não / Não observado**. Qualquer resposta não observada mantém a pré-validação como **INCOMPLETE_OR_INVALID**, jamais como ausência de defeito ou aprovação. Foi reexecutada a suíte de 40/40 e o fluxo Chromium 390px, incluindo esse caso negativo, após a atualização. A lógica pura JS do revisor permaneceu byte-idêntica. O ZIP e o HTML usam **os hashes atuais exibidos acima**; os SHA anteriores de v1.1 (42f733... e c5a111...) ficam SUPERADOS como distribuição corrente. Sem observação material real e sem homologação de inspeção.

### E4.3 — Revisor independente de JSON (read-only; mesmo QA JS)

**ANTES:** parecer pré-calculado no JSON exportado podia ser alterado sem recálculo, duplicatas entre lotes poderiam inflar unidades experimentais aparentes.

**DEPOIS:** script Node `review_capture.js` reutiliza **literalmente** o `logic.js` da bancada v1.1 (SHA256 `1067deec34d5b48667b62ac48a1aad1b6fb172e44178854a259cebbf64d15421`), aceita exportações 1.0/1.1, recalcula avaliações, registra SHA256 do arquivo recebido, rejeita divergências, falso writer, origem alterada, duplicatas tipo+lote+amostra e sinaliza possível pseudorreplicação entre lotes pelo mesmo sample_id. Não faz cliente Notion nem atesta origem física; `independence_verified=false` sempre.

**Resultado:** 18/18 testes Node regressivos/adversariais PASS; CLI de demonstração de 3 amostras **sintéticas** produz `REVIEW_REQUIRED_NO_AUTOCANON` e nenhum RC5; `REVIEW_QUARANTINE` se houver conflito. Revisão final substituiu apenas a mesma cópia de Biblioteca do revisor: `/Comestre/CRAFT_ANDROID_EXPORT_REVIEWER_20261021.zip` Library `libfile_57f0ba3599108191947acaf9ca5b435d`, SHA256 **atual** `456ba432343d5d70ce9dfac49b7180bd7de212b10722143b079d4985c5063b2e` 12565 bytes, ZIP7 CRC PASS, manifesto 6/6, readback byte-idêntico, cold replay 18/18 PASS. SHA anterior `db7e6290...` superado, não distribuir como versão atual.

**Denominador correto:** duas suítes atuais independentes **40 testes na bancada + 18 no revisor = 58 testes de regras**, além de ensaios E2E/mobile; não somar 31 antigos aos 40 atuais como novos. Zero lotes/material físico observados pela ferramenta; em nenhum caso foi validada identidade de operador/instrumento.

## 3. Rastreabilidade da sessão

- No Notion LAB existe ANTES e DEPOIS para `CRAFT-MOBILE-CAPTURE-20261021-001`, `CRAFT-MOBILE-FIBER-B30-02-20261021-001` e `CRAFT-MOBILE-REVIEW-20261021-001`, incluindo adendo do revisor. Não editar fichas de itens com checkpoints administrativos (IBX-82).
- A OP recebeu comentário `CRAFT-LONGRUN-MOBILE-20261021-001` na discussão existente e foi relido; histórico no corpo OP preservado.
- A IBX-116 recebeu uma devolutiva no mesmo objeto, sem AUTO-ACK e mantendo estado `NOVA`, `Exige ACK=YES` no readback. Sua missão principal de Pingente continua aberta.
- Biblioteca dos dois ZIP atuais e HTML foi materializada em diretórios independentes e verificada por igualdade byte a byte, SHA256 e replay frio.

## 4. Gate NAC-PASS proporcional

**PASS:** código local, UX simulada Android, QA de formato, cálculos preliminares, export/import, integridade de pacote, reprodutibilidade e documentação. **HOLD:** materiais reais, calibração/autenticação, independência de réplica, efeito/força de serviço, lotes, consumos MED/PA, QA mágico, insumos Pingente H2, RC5, REC-LIB, P4, produção e qualquer operação Party/O Primeiro.

Sem writer/lease/epoch/INSTANCE-ID/ACK/fencing/GREEN válido recuperado. Nenhuma escrita em R48, fontes PS, receitas, estoque, PA, fichas Mestre de jogo, Party ou O Primeiro.

## 5. Retomada exata — sem reiniciar

1. Quando houver **medições realmente adjudicadas** por operador competente, abrir a HTML offline, preencher IDs/lotes/instrumentos, exportar JSON e submetê-lo ao revisor. Este deve sinalizar erros e deixar `REVIEW_REQUIRED_NO_AUTOCANON` mesmo com zero conflitos. Não fingir medições para fechar pilotos.
2. Ao existir material qualificado, usar R45/R46 e NAC-PASS para inspeção independente da qualidade, comparação com materiais comuns, tempo e rendimento, custo CTE/MED e segurança; B30-02 depende sobretudo de limite de carga formal.
3. Continuar acompanhando **na mesma IBX-38** o fencing técnico de I0014, **na mesma R51/IBX-78** o parent único de receitas, **na IBX-116** sal/energia P2, Óleo de Vedação e testemunha H2. Não criar pedidos duplicados. Somente depois desses gates considerar microblocos RC5 com escritor competente.
4. Outras frentes possíveis: novos ensaios de qualidade realmente independentes, com recurso existente e contrato já canônico, sem inventar receita, engine ou bônus. Evitar repetir dados QA sintéticos de B30-01/B30-03/B30-06/B30-13 e recuperar resultados existentes antes de qualquer esforço.

**Estado terminal desta janela:** COMPLETA EM TEST para interface/validador de exportação; **CRAFT GLOBAL ABERTO / HOLD FÍSICO**. Estado da Party e de O Primeiro intacto.
