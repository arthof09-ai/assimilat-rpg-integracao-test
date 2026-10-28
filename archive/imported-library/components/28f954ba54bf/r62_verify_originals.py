import json, zipfile, hashlib, pathlib
root=pathlib.Path('/mnt/data')
files=[('V05',root/'ibx17_followup/LEVELUP_CHAT_MESTRE_V05_20261014.zip','MANIFEST_V05_SHA256.json','bf62fb0eb77bfc29af8b3d0a476b034954275065472bbfccbce519b4f6dbd8d1',483),('R30',root/'ibx17_recovered/LEVELUP_IBX17_LEVELDOWN_CHAT_R30_20261015.zip','MANIFESTO_SHA256_LEVELDOWN_R30.json','989ecdb15822fe6d74cda5e17b87cd2843c96aa25216f10bb72811e604993e62',57),('POSTR60',root/'IBX17_POS_R60_V05_R17_R30_SUCESSAO_20261016.zip','MANIFESTO_SHA256_R61.json','647f09f13d6dee06166a5d06b1289be62fa093d4cf8adade5a83751a4678864a',10)]
out=[]
for name,p,m,expected,den in files:
 actual=hashlib.sha256(p.read_bytes()).hexdigest();assert actual==expected,(name,actual)
 with zipfile.ZipFile(p) as z:
  assert z.testzip() is None
  mp=next(n for n in z.namelist() if n.endswith(m));data=json.loads(z.read(mp));fs=data['files'];prefix=mp[:-len(m)];miss=[]
  for rel,h in fs.items():
   if prefix+rel not in z.namelist() or hashlib.sha256(z.read(prefix+rel)).hexdigest()!=h:miss.append(rel)
  print(name,'byte_size',p.stat().st_size,'nentry',len(z.namelist()),'manifest',len(fs),'mismatch',len(miss))
  out.append({'name':name,'file':p.name,'bytes':p.stat().st_size,'zip_entries':len(z.namelist()),'crc':'PASS','manifest_entries':len(fs),'manifest_matched':len(fs)-len(miss),'expected_denominator':den,'sha256':actual,'manifest_bad':miss})
json.dump(out,open(root/'IBX17_R62_R71_WORK/R62_AUTHENTICATED_FILES.json','w'),ensure_ascii=False,indent=2)
