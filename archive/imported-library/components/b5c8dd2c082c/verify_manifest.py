"""Verify static baseline/code/docs against manifest; outputs are derived replay files.
Never writes to source artifacts or Notion.
"""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SKIP={'MANIFEST_SHA256.json'}
def file_set():
 return sorted((p for p in ROOT.rglob('*') if p.is_file() and not any(x in ('outputs','__pycache__') for x in p.relative_to(ROOT).parts) and p.name not in SKIP and p.suffix!='.pyc'), key=lambda x:str(x.relative_to(ROOT)))
def main():
 m=json.loads((ROOT/'MANIFEST_SHA256.json').read_text());actual={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in file_set()};expected=m['sha256']
 fail={'missing':sorted(set(expected)-set(actual)),'unexpected':sorted(set(actual)-set(expected)),'hash_drift':sorted(x for x in set(actual)&set(expected) if actual[x]!=expected[x])}
 ok=all(not x for x in fail.values())
 print(json.dumps({'ok':ok,'manifest_expected':len(expected),'scanned':len(actual),'findings':fail},indent=2))
 if not ok:sys.exit(1)
if __name__=='__main__':main()
