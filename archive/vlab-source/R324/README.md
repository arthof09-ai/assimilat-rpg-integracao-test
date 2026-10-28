# VLAB R324 — recuperacao de bytes originais

Backup historico MESTRE-SIDE **TEST / nao canonico**, preservado como 10 objetos Git binarios. Não representa novo motor nem habilita publicação à Party ou implantação em campanha.

Origem: [Google Drive RPG (novo)](https://drive.google.com/file/d/1_qqhVE6gNVe1wU-uVey0e1vktW3GEyiK/view).

ZIP original: `VLAB_CODIGO_MAE_R324_COMPLETO.zip`. Tamanho **15698603** bytes, SHA256 **`2a52c00d2199e40c5635def308349d1dce21ca061212666595e5742dce5d68f0`**, 87 membros, CRC PASS, manifesto interno 86/86 e 18/18 ZIPs internos CRC PASS por auditoria local anterior.

Para reconstruir sem sobrescrever arquivos:
```sh
python archive/vlab-source/R324/reassemble.py --output /diretorio/novo/VLAB_CODIGO_MAE_R324_COMPLETO.zip
```

O programa verifica cada SHA do blob Git, tamanho final, SHA256 do ZIP, CRC dos membros e paths seguros. Sem aprovação CI, Android físico, NAC-PASS de produção ou canonização. R325 e R326 já coexistem na árvore: preservar todas as versões.
