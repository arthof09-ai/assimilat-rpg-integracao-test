import sys,zipfile,hashlib,json
p=sys.argv[1]
with zipfile.ZipFile(p) as z:
 assert z.testzip() is None
 m=json.loads(z.read('MANIFEST_R12_SHA256.json'))
 assert sorted(m)==sorted(n for n in z.namelist() if n not in ['MANIFEST_R12_SHA256.json','verificar_r12.py'])
 for n,h in m.items(): assert hashlib.sha256(z.read(n)).hexdigest()==h,n
 d=json.loads(z.read('DMG-R12-MATRIZ-B01-B18-READONLY-v01.json'))
 t=json.loads(z.read('DMG-R12-TESTES-CONDICIONAIS-v01.json'))
 assert len(d['records'])==18 and d['pass_ids']==['B02'] and d['certified_whole']==1 and d['full_fight']==0
 assert t['passed']==t['test_count'] and t['failed']==0 and all(c['pass'] for c in t['tests'])
 print('R12_LOCAL_READBACK_PASS;TESTS=%d/%d;B02=DOC_PASS;FULL_FIGHT=0/2;GLOBAL_NAC_PASS=HOLD'%(t['passed'],t['test_count']))
