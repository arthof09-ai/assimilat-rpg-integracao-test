# VLAB — Código-Mãe R326: cópia integral recuperável

**Origem:** [Google Drive original](https://drive.google.com/file/d/10m9vPsOfEp5uNs0iuMjINStEYv7nmG2K/view) · **Data da auditoria:** 28/10/2026.

**Finalidade:** backup histórico da fonte original do VLAB R326, **não** é nova versão do motor, integração operacional, upgrade de CI ou homologação NAC-PASS. A publicação no GitHub não substitui Notion nem autoriza comunicação Mestre-only à Party.

O ZIP original não coube em uma única chamada de transmissão pelo conector. Para **não perder os bytes**, preservamos o objeto exato em **11 partes binárias ordenadas** de 1.572.864 bytes (última: 222.921 bytes). Não comprimir nem editar os arquivos `partNN.bin` separadamente.

- Nome original: `VLAB_CODIGO_MAE_R326_COMPLETO.zip`
- Tamanho exato: **15.951.561 bytes**
- SHA-256 do ZIP: `420fa4c9f084df449e68075e30fec50ad392bfe041070433b9a4feaf4daf17d5`
- CRC do ZIP original: **PASS**
- Entradas no ZIP original: **109**
- Proveniência e SHA-256 de cada parte: [manifest.json](manifest.json)
- Teste original de hash: conferido com a mídia baixada do Drive, antes de copiar.

## Reconstrução (Python 3, sem dependências)
Abra esta pasta numa cópia clonada da branch de arquivamento e execute:

```sh
python reassemble.py --output ./VLAB_CODIGO_MAE_R326_COMPLETO.zip
```

O script verifica **cada SHA-256 individual, tamanho e ordem**, concatena os bytes, verifica SHA-256 final, número de entradas e CRC. Se falhar, marca erro e não deixa ZIP adulterado como arquivo válido. Não sobrescreve ZIP existente.

**Estado de gestão:** origem VERIFICADA, pacote binário de backup; passar pelo gate do VLAB antes de executar/implantar qualquer código. No GitHub, o ZIP está distribuído em Git blobs normais para superar o limite de transmissão do conector; não são ponteiros Git LFS.
