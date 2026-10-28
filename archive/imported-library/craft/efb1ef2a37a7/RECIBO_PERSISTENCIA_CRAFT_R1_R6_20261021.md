# RECIBO DE PERSISTÊNCIA — REGISTRO CRAFT R1–R6

**TRACE:** CRAFT-CONT-REG-R1R6-20261021-001  
**Objeto de referência:** `REGISTRO_CONSOLIDADO_CRAFT_R1_R6_20261021.md` · Biblioteca Mestre `/Comestre/` · `libfile_81245740e448819183f99b9fd664f584` · **21.390 bytes** · SHA256 `90f6800421adc317b704621a3fdcc86d4f48fedb4c7c9cf71be90ea66f54d24e`.

## Checkpoints físicos verificados nesta retomada

1. **Biblioteca Mestre:** upload retornou sucesso e `libfile_81245740e448819183f99b9fd664f584`. Materialização em pasta independente retornou 21.390 bytes; comparação `cmp` PASS e ambos SHA iguais ao acima. Arquivo fonte e cópia da Biblioteca são byte a byte idênticos.
2. **LAB CRAFT, Notion Mestre:** foram acrescentadas três seções no mesmo LAB existente sob o mesmo TRACE: `REGISTRO CONSOLIDADO / ANTES`, `DEPOIS / ENTREGAS E DENOMINADORES` e `PENDÊNCIAS / GATES / PONTO DE RETOMADA`. Fetch posterior encontrou **3 ocorrências do TRACE**, as três seções e o SHA completo do arquivo. URL: https://app.notion.com/p/3fbc2b324ede811db848d35d4739eb00 . Isso também registra o patch R6 de custódia CLI que antes não tinha readback na LAB.
3. **Diário da OP-ARQ-RIN-REC-01:** uma seção de índice foi acrescida ao corpo existente, seguida de fetch positivo para TRACE, SHA do relatório e SHA do patch R6. URL: https://app.notion.com/p/3f1c2b324ede81d7aa79c83106240516 . Houve também um comentário com retorno de sucesso (`401c2b32-4ede-81df-957e-001d7da61d64`), mas a ferramenta de leitura dos comentários mostrou apenas a primeira parte da discussão e não permitiu readback individual desse comentário. Portanto a **prova de persistência do Diário é a seção no corpo reaberta**, não a alegação sobre comentário.
4. **IBX-116 existente:** seção `DEVOLUTIVA CONSOLIDADA / SEM AUTO-ACK` gravada e readback com TRACE e SHA completos. As propriedades continuam `Estado=NOVA` e `Exige ACK=__YES__`; nenhum ACK, writer, lease, epoch, fencing ou instância foi reivindicado. URL: https://app.notion.com/p/3ffc2b324ede817aa3abea3cb7ba8c08 .
5. **IBX-38 e R51:** fetch nesta retomada confirmou ambos `Estado=NOVA`; nenhuma prova de fencing técnico (IBX-38) ou parent físico universal REC-LIB (R51) foi recuperada. URLs: https://app.notion.com/p/3f3c2b324ede817fb888ca32aacaf2de e https://app.notion.com/p/3f4c2b324ede812a9153d39281b488f8 .

## Gate NAC-PASS proporcional

**PASS DOCUMENTAL:** arquivo + Biblioteca + LAB + seção no corpo do Diário + mesma IBX-116; readback verificável, sem substituição de objetos existentes. **PASS DIGITAL HISTÓRICO:** hashes/CRC de 17 ZIPs conferidos localmente; os testes históricos permanecem atribuídos às respectivas rodadas, não reexecutados cumulativamente nesta consolidação.

**HOLD MATERIAL/NORMATIVO:** IBX-38 / C19, R51, P2-SALT-01, P2-ENERGY-02, Óleo de Vedação, H2-3A/B, calibração/lotes/observação, RC5/P4/F5/PROD. Nenhuma escrita em Party, O Primeiro, fichas de jogo, inventário, PA ou R48; nenhum REC-ID oficial novo.

**Retomada:** abrir o registro consolidado na Biblioteca ou as três seções no LAB; verificar novas decisões externas. Se nada mudou, prosseguir apenas por testes digitais úteis e integrar o patch R6 de custódia com o ramo R6/R46 **após comparação**, sem presumir que isso já ocorreu.
