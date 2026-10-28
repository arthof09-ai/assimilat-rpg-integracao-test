"""Alter only fresh R175 test clones; rebuild SQL chain after semantic tampering.
Independent R175 auditor must still reject them. Never touch originals/historical.
"""
import json,hashlib,sqlite3,shutil,pathlib,sys,subprocess

def canon(o):return json.dumps(o,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def sha(o):return hashlib.sha256(canon(o).encode()).hexdigest()
def clone_rehash(original,out,kind):
 original=pathlib.Path(original);out=pathlib.Path(out);out.parent.mkdir(parents=True,exist_ok=True)
 shutil.copy2(original,out)
 shutil.copy2(str(original)+'.checkpoint.json',str(out)+'.checkpoint.json')
 with sqlite3.connect(str(out)) as c:
  meta=dict(c.execute('select key,value from meta'));prev=meta['genesis']
  data=list(c.execute('select seq,cmd_id,row_json from events order by seq'))
  changed=False;patched=[]
  for seq,cmd,blob in data:
   row=json.loads(blob)
   if not changed and row['kind']=='R175_SOURCE_PHYSICAL_ATTACK' and row['detail']['actor']=='AUREN':
    if kind=='RD':row['detail']['attack']['rd_applied']=0
    elif kind=='SOURCE':row['detail']['source_page']='https://app.notion.com/p/3f2c2b324ede81f09c48f6e11874cd81'
    else:raise ValueError(kind)
    changed=True
   row['prev']=prev;rowsha=sha(row)
   c.execute('update events set prev=?,row_json=?,row_sha=? where seq=?',(prev,canon(row),rowsha,seq))
   prev=rowsha
  assert changed
  c.execute('update meta set value=? where key="head"',(prev,))
 with open(str(out)+'.checkpoint.json') as f:ck=json.load(f)
 ck['body']['head']=prev;ck['body']['events']=[json.loads(x[0]) for x in sqlite3.connect(str(out)).execute('select row_json from events order by seq')]
 ck['sha256']=sha(ck['body'])
 pathlib.Path(str(out)+'.checkpoint.json').write_text(json.dumps(ck,sort_keys=True,indent=2,ensure_ascii=False))
 return out
if __name__=='__main__':
 base=pathlib.Path(sys.argv[1]);folder=pathlib.Path(sys.argv[2]);auditor=pathlib.Path(__file__).with_name('r175_independent_audit.py')
 results=[]
 for kind in ('RD','SOURCE'):
  out=clone_rehash(base,folder/f'R175_ADVERSARIAL_{kind}_REHASH.sqlite',kind)
  cmd=[sys.executable,str(auditor),str(out.parent)]
  # Auditing each isolated clone in own directory avoids incidental group errors.
  isolated=folder/kind;isolated.mkdir(exist_ok=True,parents=True)
  target=isolated/out.name;shutil.copy2(out,target);shutil.copy2(str(out)+'.checkpoint.json',str(target)+'.checkpoint.json')
  p=subprocess.run(cmd[:-1]+[str(isolated)],capture_output=True,text=True)
  results.append({'kind':kind,'clone':target.name,'structural_rehash':True,'independent_auditor_rejected':p.returncode!=0,'error_tail':(p.stderr.strip().splitlines()[-1] if p.stderr.strip() else '')})
 assert all(x['independent_auditor_rejected'] for x in results)
 print(json.dumps({'audit':'R175_ADVERSARIAL_REHASH_SEMANTIC','results':results,'pass':True},indent=2))
