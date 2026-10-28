# VLAB R323 — recuperacao de bytes originais

Backup historico MESTRE-SIDE **TEST / nao canonico**, preservado como 10 objetos Git binarios. Não representa novo motor nem habilita publicacao à Party ou implantação em campanha.

Origem binaria: [Google Drive RPG (novo)](https://drive.google.com/file/d/1s5Zo0jNU2doiPghvNdNcWhF_T99SorIS/view).

ZIP original: `VLAB_CODIGO_MAE_R323_COMPLETO.zip`. Tamanho **15634470** bytes, SHA256 **`0ecf4897aa6d05cda373c4bd1a0f8f3d6f83d34add8725b8c44cd2ca2ad15fd8`**, membros **82**, CRC PASS, manifesto interno 81/81 e 17/17 ZIPs internos CRC PASS, via auditoria local anterior.

Para reconstruir sem sobrescrever arquivos:

```sh
python archive/vlab-source/R323/reassemble.py --output /diretorio/novo/VLAB_CODIGO_MAE_R323_COMPLETO.zip
```

Cada `partXX.bin` tem SHA de Git e tamanho documentados no `manifest.json`; programa confere partes, tamanho e SHA256 do ZIP final, CRC e caminhos internos. Os IDs das partes foram cruzados contra os bytes de origem antes do commit.

Gates: backup/arquivo TEST; não aprova CI, Android físico, regras canônicas nem NAC-PASS global.
