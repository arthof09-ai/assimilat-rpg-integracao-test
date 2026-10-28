#!/usr/bin/env python3
"""Verificador offline da entrega V03 — não concede certificado Notion."""
from __future__ import annotations
import hashlib
import zipfile
import json
import sys
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST_V03_SHA256.json').read_text(encoding='utf-8'))
bad=[]
for f in manifest['arquivos']:
    p=root/f['arquivo']
    if not p.is_file() or p.stat().st_size!=f['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=f['sha256']:
        bad.append(f['arquivo'])
print(f"MANIFEST V03: {len(manifest['arquivos'])-len(bad)}/{len(manifest['arquivos'])} arquivos íntegros")
expected_v02='f5ea4adce4ce587c36d5ada43ab1145c4fc2a5a3a4a4adf6b364e3221f732f77'
p=root/'historico_autenticado/UAT_V02_ORIGINAL_NAO_MODIFICADA.zip'
legacy=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else 'AUSENTE'
print('UAT V02 HISTÓRICA:', 'PASS' if legacy==expected_v02 else 'FAIL')
expected_engine=json.loads((root/'SHA256_MOTOR_R27_SEM_MODIFICACOES.json').read_text(encoding='utf-8'))
engine_bad=[k for k,v in expected_engine.items() if not (root/k).is_file() or hashlib.sha256((root/k).read_bytes()).hexdigest()!=v]
print(f'MOTOR R27 PYTHON / MANIFESTO: {len(expected_engine)-len(engine_bad)}/{len(expected_engine)} hashes iguais')
# Dez arquivos adicionais (ZIPs e textos) também estão dentro da pasta original.
with zipfile.ZipFile(root/'historico_autenticado/UAT_V02_ORIGINAL_NAO_MODIFICADA.zip') as oldzip:
    original_engine=[n for n in oldzip.namelist() if '/engine_r17_existing_r27/' in n and not n.endswith('/')]
    complete_bad=[]
    for fullname in original_engine:
        relative=fullname.split('/engine_r17_existing_r27/',1)[1]
        current=root/'engine_r17_existing_r27'/relative
        if not current.is_file() or current.read_bytes()!=oldzip.read(fullname):
            complete_bad.append(relative)
print(f'PASTA MOTOR R27 INTEIRA: {len(original_engine)-len(complete_bad)}/{len(original_engine)} byte-exatos versus V02')
expected_r29='47bf4cb79d410f0e5d507386b47dac8287285fbfdcefa940474c118ad294cb7c'
p29=root/'historico_autenticado/R29_ORIGINAL_NAO_MODIFICADO.zip'
r29=hashlib.sha256(p29.read_bytes()).hexdigest() if p29.exists() else 'AUSENTE'
print('R29 HISTÓRICO:', 'PASS' if r29==expected_r29 else 'FAIL')
if bad: print('ERROS NO MANIFESTO:',bad[:20])
if engine_bad: print('ERROS MOTOR:',engine_bad[:20])
if complete_bad: print('ERROS PASTA MOTOR:',complete_bad[:20])
if bad or legacy!=expected_v02 or engine_bad or complete_bad or r29!=expected_r29:sys.exit(2)
print('INTEGRIDADE DA ENTREGA EXPERIMENTAL: PASS. Windows físico/UAT/Notion produção: NÃO CERTIFICADOS.')
