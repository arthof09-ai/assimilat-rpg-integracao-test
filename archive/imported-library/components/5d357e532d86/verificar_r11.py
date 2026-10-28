#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,zipfile,sys
p=Path(sys.argv[1] if len(sys.argv)>1 else Path(__file__).with_name("DMG-F1-R11-B02-CERTIFICACAO-E-INTEGRACAO-VLAB-R03-v01.zip"))
with zipfile.ZipFile(p) as z:
 assert z.testzip() is None
 d=json.loads(z.read('MANIFEST_R11_SHA256.json'))
 assert sorted(d)==sorted(n for n in z.namelist() if n!='MANIFEST_R11_SHA256.json')
 for n,h in d.items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
 x=json.loads(z.read('DMG-F1-R11-MATRIZ-B01-B18-v01.json'))
 t=json.loads(z.read('DMG-F1-R11-TESTES-NOVOS-v01.json'))
 b=json.loads(z.read('DMG-F1-R11-B02-CERTIFICACAO-DOCUMENTAL-v01.json'))
 assert len(x['records'])==18 and x['certified_whole']==1 and x['pass_ids']==['B02']
 assert x['full_fight']==0 and x['lab_17_contracts_terminal']==0
 assert t['failed']==0 and t['passed']==t['total']
 assert b['verdict']=='PASS' and b['nac_pass02_terminal'].startswith('HOLD')
print('R11_PACKAGE_READBACK=PASS; MEMBERS=%d; R11_TESTS=%d/%d; SCIENTIFIC_B02_PASS=1/18; FULL_FIGHT=0/2; LAB_TERMINAL=0/17'%(len(d)+1,t['passed'],t['total']))
