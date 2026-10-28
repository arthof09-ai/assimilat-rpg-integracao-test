#!/usr/bin/env python3
import hashlib,json,sys
from pathlib import Path
root=Path(__file__).resolve().parent
m=json.loads((root/'MANIFEST_V02_SHA256.json').read_text())
bad=[]
for a in m['arquivos']:
 p=root/a['arquivo']
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=a['sha256'] or p.stat().st_size!=a['bytes']:
  bad.append(a['arquivo'])
print(f"MANIFEST V02: {len(m['arquivos'])-len(bad)}/{len(m['arquivos'])} arquivos OK")
if bad: print('DIVERGENCIAS:',bad);sys.exit(2)
print('Histórico original V01 conservado dentro do pacote v02.')
