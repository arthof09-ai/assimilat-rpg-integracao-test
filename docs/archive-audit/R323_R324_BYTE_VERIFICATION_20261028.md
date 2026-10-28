# VLAB R323 e R324 — prova de bytes recuperados (28/10/2026)

Classificação: MESTRE-SIDE HISTORICAL_TEST_NONCANONICAL. Conectores Notion/Drive: conta Mestre ou RPG como depósito, nunca envio para jogadoras. Esta página é recibo de evidência e **NÃO substitui o backup original**.

| Arquivo original | Tamanho | SHA256 real | CRC ZIP | Manifesto interno | ZIPs aninhados | GitHub |
|---|---:|---|---|---|---|---|
| `VLAB_CODIGO_MAE_R323_COMPLETO.zip` | 15.634.470 B | `0ecf4897aa6d05cda373c4bd1a0f8f3d6f83d34add8725b8c44cd2ca2ad15fd8` | PASS (82 membros) | 81/81 SHA PASS | 17/17 CRC PASS | VERIFICADO NA PR #21; reconstrução byte-idêntica ao Drive |
| `VLAB_CODIGO_MAE_R324_COMPLETO.zip` | 15.698.603 B | `2a52c00d2199e40c5635def308349d1dce21ca061212666595e5742dce5d68f0` | PASS (87 membros) | 86/86 SHA PASS | 18/18 CRC PASS | VERIFICADO NA PR #21; reconstrução byte-idêntica ao Drive |

Dados coletados com download autenticado e cálculo SHA256 do original e cópia no Drive novo, iguais por versão. As cópias binárias ORIGINAIS encontram-se no Drive RPG:
- R323: https://drive.google.com/file/d/1s5Zo0jNU2doiPghvNdNcWhF_T99SorIS/view
- R324: https://drive.google.com/file/d/1_qqhVE6gNVe1wU-uVey0e1vktW3GEyiK/view

Manifestos de proveniência com análise de membros, recuperados e publicados no novo Drive:
- R323: https://drive.google.com/file/d/1foFC2Kw0wHo1vHZYDdAICZbUxF9Q6jYe/view
- R324: https://drive.google.com/file/d/1xhF_l9Hlroz9PyY9hLL4hkJXbWd9oGVV/view

**Readback em 28/10/2026 pelo Codex:** os ZIPs já estavam na PR #21 no head `29e819da054fafb2d87f912009432214132f8852`, em 10 partes por versão. Novo download autenticado do Drive correto, reconstrução pelos scripts publicados e comparação byte a byte PASS. Não foram duplicados. Gate de publicação de bytes GitHub é separado: revisar segredos/licença/arquivos e confirmar Git blob + reconstrução SHA256. Os R325/R326 já estão em GitHub, portanto não duplicar.

Esta prova documental respeita a ordem expressa do Mestre de publicar códigos Mestre-side no GitHub, sem promover cânone nem enviar à Party.

Revalidação estendida: R325 tem 98 hashes internos conferidos e 19 ZIPs internos CRC PASS. R326 preserva o SHA-256 original `420fa4c9f084df449e68075e30fec50ad392bfe041070433b9a4feaf4daf17d5` e CRC dos 20 ZIPs internos, mas seu manifesto interno histórico possui 3 divergências (`README_MESTRE_ONLY.md`, `index.html`, `manifest.json`): 95 PASS de 98 entradas. Nenhum byte original foi corrigido.

Correção de ferramenta de reconstrução R323/R324: em caso de destino já existente, a falha de abertura exclusiva agora preserva esse arquivo; antes o tratamento genérico de erro podia removê-lo. Verificação de regressão com arquivo sentinela existente PASS nas duas versões.


**SECURITY-HOLD atual:** integridade dos originais comprovada, mas há membros com dados derivados de fichas Party no pacote histórico incorporado. Publicação/merge integrais não estão aprovados. Ver `RECOVERY_EXECUTION_20261028.md` para cadeia e hash da evidência; arquivos oficiais no Drive preservados.
