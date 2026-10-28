#!/usr/bin/env python3
"""Validador puramente local da cadeia física PA R05/R06/R07/R08/R09.
Verifica SHA256 do ZIP e os arquivos cobertos por cada manifesto; não reexecuta
fichas, Notion, CRAFT ou os motores antigos e não escreve no acervo.
"""
from pathlib import Path
import hashlib, json, zipfile

ROOT=Path(__file__).resolve().parent.parent
FILES={
  'R05':('PA_UNIVERSAL_R05_TEST_20261017.zip','6f69fd1ef197851e128c2fc7becbad1f2a14a1438e7bf9ac71742b835f99078e'),
  'P0_R06':('PA_P0_AUDITORIA_94_RANKS_CORRECOES_TEST_20261017.zip','6d00306079ac4578d0191d424742a3c746c2a9f73327b9d8563e9267b4f25eb6'),
  'P0_R07':('PA_P0_R07_READBACK_ORIGEM_20261017.zip','6fccc0eb0c3f2aa6c9cc6297f3882d83f03ae13ee10969902f78be623ffcf71a'),
  'P0_R08':('PA_P0_R08_ORIGINAIS_ATLAS_CORRECOES_TEST_20261018.zip','e7957fb016c3ce04343620a7e1a2b155a5e317afc5eb22ef753f96f1aa9b6499'),
  'P0_R09':('PA_P0_R09_CORRIGENDA_TEST_20261018.zip','90ceedc8513b09fe6b6938d0c747a4eba77feb854f8834b791791de9fd320d90'),
}

def sha(data):return hashlib.sha256(data).hexdigest()

def audit():
  rows=[]
  for stage,(name,expected_zip_sha) in FILES.items():
    path=ROOT/name
    actual_zip_sha=sha(path.read_bytes())
    manifest_found=0; manifest_pass=0;crc_bad=None;bad=[]
    with zipfile.ZipFile(path) as z:
      crc_bad=z.testzip()
      entry=next(x for x in z.namelist() if x.rsplit('/',1)[-1].startswith('MANIFEST') and x.endswith('.json') and x.count('/')<=1)
      m=json.loads(z.read(entry))
      if stage=='R05': sources=[(entry.rsplit('/',1)[0]+'/'+x['path'],x['sha256']) for x in m['files']]
      elif stage=='P0_R06': sources=[('PA_P0_AUDITORIA_20261017/'+x['path'],x['sha256']) for x in m['files']]
      elif stage=='P0_R07': sources=[(x['name'],x['sha256']) for x in m['files']]
      elif stage=='P0_R08': sources=list(m['files'].items())
      else:
        sources=list(m['created_files'].items())
        if m.get('baseline_r08_zip_sha256')!=FILES['P0_R08'][1]:bad.append('R09 parent R08 SHA mismatch')
      manifest_found=len(sources)
      for filename,expected in sources:
        try:actual=sha(z.read(filename))
        except KeyError:actual='MISSING'
        if actual==expected:manifest_pass+=1
        else:bad.append(filename)
      n_entry=len(z.namelist())
    ok=(expected_zip_sha==actual_zip_sha and crc_bad is None and manifest_found==manifest_pass and not bad)
    rows.append({'stage':stage,'filename':name,'size_bytes':path.stat().st_size,
                 'zip_sha256':actual_zip_sha,'sha_matches_persisted_baseline':actual_zip_sha==expected_zip_sha,
                 'zip_entries':n_entry,'crc_pass':crc_bad is None,
                 'manifest_pass':manifest_pass,'manifest_total':manifest_found,'errors':bad,'pass':ok})
  return {'scope':'RECOVERY_AND_INTEGRITY_ONLY_NO_CANONICAL_ATTESTATION',
          'pass':all(r['pass'] for r in rows),'stages':rows,'notion_writes':0,
          'craft_native_acceptance_proven':False,'version': 'PA-R10-SUCCESSION-READONLY'}

if __name__=='__main__':print(json.dumps(audit(),ensure_ascii=False,indent=2))
