# VLAB — Código-Mãe R325: backup histórico recuperável

**Origem:** [Drive original](https://drive.google.com/file/d/1ZDtKo3BtyxLwHpSEOU9lhzSUtw6EVKDV/view) · **data:** 28/10/2026 · **status:** HISTÓRICO / MESTRE-SIDE / NÃO CANONIZADO.

Esta pasta contém os **15.836.459 bytes originais** do arquivo `VLAB_CODIGO_MAE_R325_COMPLETO.zip` distribuídos em 11 blobs Git comuns (dez partes de 1.572.864 bytes, última de 107.819 bytes). Os nomes, posições, hashes SHA-256, hashes Git e a origem estão no [manifesto](manifest.json). O ZIP original contém 99 entradas e teve CRC PASS; 18 ZIPs internos também passaram CRC. Nenhuma nova funcionalidade foi implementada, e não houve publicação na Party nem mudança de produção.

**SHA-256 original:** `a322ff311199643e1230b7e1cd3ea31445e1c3155615235df047a928ca58f502`.

Recrie na pasta do checkout da branch:

```sh
python reassemble.py --output ./VLAB_CODIGO_MAE_R325_COMPLETO.zip
```

A ferramenta é uma adaptação mínima do reassemblador R326 já versionado, apenas para o nome original R325. Valida tamanho e SHA-256 de cada parte, SHA-256 total, quantidade de entradas e CRC. **Não sobrescreve** arquivo existente e remove saída inválida.

**Limites:** este é um backup TEST histórico. Importação e CRC não comprovam funcionamento no VLAB oficial, CI ou homologação NAC-PASS. O Drive novo lista cópia de mesmo nome/tamanho; equivalência binária com a cópia nova ainda não foi testada.

## TESTE DE REMONTAGEM LOCAL — 28/10/2026

**VERIFICADO:** uma cópia local do script de remontagem foi comparada pelo hash Git blob SHA1 com a versão publicada (`1bfafa154a1c860edd9f1a3ba48c21907e468303`): igualdade **PASS**. O arquivo original do Drive foi dividido em partes idênticas aos offsets e hashes especificados no manifesto publicado, executou-se `python reassemble.py --output reconstructed-r325.zip` com **exit 0**, CRC e 99 membros PASS, SHA-256 `a322ff311199643e1230b7e1cd3ea31445e1c3155615235df047a928ca58f502`, 15.836.459 bytes. A comparação completa entre ZIP original e reconstruído foi **byte-for-byte igual**. Este é um ensaio local da remontagem e identidade, **não** execução de 18 scripts nativos nem teste de conformidade com VLAB canônico/CI.

**Readback GitHub:** árvore recursiva da branch, 11/11 blobs em `archive/vlab-source/R325/` com SHA1 e tamanho exatamente iguais aos do manifesto, 14 objetos esperados e `truncated=false`. Evidência de conteúdo completo por identidade de objeto Git; ZIP original não armazenado diretamente como single blob.
