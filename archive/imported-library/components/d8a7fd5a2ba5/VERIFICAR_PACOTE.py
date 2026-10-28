import json,hashlib,pathlib,sys
root=pathlib.Path(__file__).resolve().parent
mf=json.loads((root/'MANIFESTO_SHA256.json').read_text(encoding='utf-8'))
problems=[]
for name,expected in mf['entries'].items():
    p=root/name
    if not p.is_file():problems.append((name,'MISSING'));continue
    got=hashlib.sha256(p.read_bytes()).hexdigest()
    if got!=expected:problems.append((name,'BAD_SHA'))
print(json.dumps({'checked':len(mf['entries']),'passed':len(mf['entries'])-len(problems),'errors':problems,'status':'PASS' if not problems else 'FAIL'},ensure_ascii=False))
raise SystemExit(0 if not problems else 1)
