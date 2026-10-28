#!/usr/bin/env python3
"""ZIP integrity + independent read-only R206B SQLite auditor, NEVER runs historical combat."""
import pathlib,sys,hashlib,json,zipfile,tempfile,subprocess

def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    p=pathlib.Path(sys.argv[1])
    with zipfile.ZipFile(p) as z:
        assert z.testzip() is None
        m=json.loads(z.read('MANIFEST_SHA256.json'))
        assert set(z.namelist())==set(m['files'])|{'MANIFEST_SHA256.json'}
        for n,h in m['files'].items():assert sha(z.read(n))==h,n
        assert sha(z.read('baseline/R205/VLAB_R205_DEFESA_DE_VENTO_ANEL_CLASSIFICADO_MESTRE_ONLY.zip'))=='62a9851b3a5ae7919b9225d9379a3d32c8736448e76bfcea4729dcbfe933cead'
        with tempfile.TemporaryDirectory() as td:
            root=pathlib.Path(td)
            for n in m['files']:
                if n.startswith('new/r206b/') and not n.endswith('/'):
                    fp=root/n;fp.parent.mkdir(parents=True,exist_ok=True);fp.write_bytes(z.read(n))
            audit=root/'new/r206b/code/r206b_independent_readonly_audit.py'
            proc=subprocess.run([sys.executable,str(audit)],capture_output=True,text=True,check=True)
            data=json.loads(proc.stdout)
            assert data['audit']=='PASS_R206B_TACTICAL_SQLITE_READONLY_INDEPENDENT'
            assert (data['dbs'],data['seeds'],data['commits'],data['events'],data['attacks'],data['censures'])==(8,4,392,1160,192,8)
            assert data['combat_reexecutions']==0
    print(json.dumps({'audit':'PASS_R206B_COLD_PORTABLE_RECOVERY','files_hashed':len(m['files']),
        'baseline':'R205_INTACT','R206_V1':'QUARANTINE_AUDIT_FAIL_NOT_REPLAYED',
        'R206B':data['audit'],'dbs':data['dbs'],'seeds':data['seeds'],
        'commits':data['commits'],'events':data['events'],'attacks':data['attacks'],
        'combat_reexecutions':0},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
