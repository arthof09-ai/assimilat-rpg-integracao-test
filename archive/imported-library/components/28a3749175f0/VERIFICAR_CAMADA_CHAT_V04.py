#!/usr/bin/env python3
"""Verificação offline do pacote. Sem rede/Notion e sem autorizações implícitas."""
from __future__ import annotations
import hashlib,json,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SHA_V03='89f584753801c59ce9c555ea12c9a4f6e49d9a5a3f9cfff075f96fe59a136a6b'

def check():
 m=json.loads((ROOT/'MANIFEST_CHAT_V04_SHA256.json').read_text(encoding='utf-8'))
 bad=[]
 for rel,expected in m['files'].items():
  target=ROOT/rel
  if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest()!=expected:
   bad.append(rel)
 engine=json.loads((ROOT/'SHA256_MOTOR_R27_SEM_MODIFICACOES.json').read_text(encoding='utf8'))
 e_bad=[]
 for rel,expected in engine.items():
  f=ROOT/rel
  if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest()!=expected:
   e_bad.append(rel)
 old=ROOT/'historico_autenticado'/'V03_ORIGINAL_NAO_MODIFICADA.zip'
 ancestor=hashlib.sha256(old.read_bytes()).hexdigest() if old.is_file() else None
 with zipfile.ZipFile(old) as original_archive:
  exact_entries=[x for x in original_archive.namelist() if x.startswith('LEVELUP_MESTRE_UAT_V03/engine_r17_existing_r27/') and not x.endswith('/')]
  exact_mismatches=[]
  for entry in exact_entries:
   target=ROOT/entry.removeprefix('LEVELUP_MESTRE_UAT_V03/')
   if not target.is_file() or target.read_bytes()!=original_archive.read(entry):
    exact_mismatches.append(entry)
 summary={'schema':'LEVELUP-CHAT-V04-VERIFY','file_manifest_ok':len(bad)==0,
          'files_verified':len(m['files'])-len(bad),'files_expected':len(m['files']),
          'motor_original_ok':len(e_bad)==0,'motor_original_verified':len(engine)-len(e_bad),
          'motor_original_expected':len(engine),'ancestor_v03_ok':ancestor==SHA_V03,
          'ancestor_v03_sha256':ancestor,
          'engine_exact_file_comparison':f'{len(exact_entries)-len(exact_mismatches)}/{len(exact_entries)}',
          'engine_exact_equal_to_original_v03':not exact_mismatches,
          'bad_files':bad,'bad_engine':e_bad,'bad_exact_engine_files':exact_mismatches,
          'notion_writes':0,'production_certified':False}
 print(json.dumps(summary,ensure_ascii=False,indent=2));return int(bool(bad or e_bad or ancestor!=SHA_V03 or bool(exact_mismatches)))
if __name__=='__main__':sys.exit(check())
