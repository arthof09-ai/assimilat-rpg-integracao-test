import json,hashlib,sys
from pathlib import Path
here=Path(__file__).resolve().parent
m=json.loads((here/'MANIFESTO_SHA256.json').read_text(encoding='utf-8'))
expected=set(m['files']);found={str(p.relative_to(here)) for p in here.rglob('*') if p.is_file() and p.name not in ('MANIFESTO_SHA256.json','VERIFICAR_INTEGRIDADE.py')}
assert expected==found, f'Files divergem: ausentes {expected-found}; extras {found-expected}'
for rel,val in m['files'].items():
 assert hashlib.sha256((here/rel).read_bytes()).hexdigest()==val,rel
print(f'PASS {len(expected)}/{len(expected)} arquivos, nenhum extra, hashes íntegros')
