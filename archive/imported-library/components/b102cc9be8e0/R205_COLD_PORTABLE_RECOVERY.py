#!/usr/bin/env python3
"""ONLY read-only archive+SQLite validation. NEVER dispatches combat runners.
Run: python R205_COLD_PORTABLE_RECOVERY.py /path/to/VLAB_R205_...zip
Requires stdlib Python3. Returns nonzero on manifest/causal failure.
"""
import json,hashlib,zipfile,sys,pathlib,tempfile,subprocess,shutil,sqlite3

def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    p=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else next(pathlib.Path('.').glob('VLAB_R205_*.zip'))
    with zipfile.ZipFile(p) as z:
        bad=z.testzip();assert bad is None,bad
        m=json.loads(z.read('MANIFEST_SHA256.json'))
        expected=m['files']; names=set(z.namelist())
        assert names-set(expected)=={'MANIFEST_SHA256.json'}, names-set(expected)
        assert len(expected)==len(names)-1
        for name,digest in expected.items():
            assert sha(z.read(name))==digest,name
        past='baseline/R204/VLAB_R201_R204_MAGIA_REAL_EDREF_MESTRE_ONLY.zip'
        assert sha(z.read(past))=='80a513dfc5f1c182597a576f416a752ca25a8b2aa8ba2634f9195fcc9c1cace2'
        dbs=[n for n in names if n.startswith('new/r205/evidence/db/') and n.endswith('.sqlite')]
        assert len(dbs)==20,len(dbs)
        runs=[]
        for name in dbs:
            with tempfile.NamedTemporaryFile(suffix='.sqlite') as temp:
                temp.write(z.read(name));temp.flush()
                db=sqlite3.connect(f'file:{temp.name}?mode=ro',uri=True)
                try:
                    r=dict(db.execute('select key,value from meta'));assert r['mode']=='EXPERIMENTAL_LAB_ONLY'
                    assert not db.execute('select 1 from pending limit 1').fetchall()
                    assert int(r['revision'])==db.execute('select count(*) from events').fetchone()[0]>0
                    runs.append(pathlib.Path(name).name)
                finally:db.close()
        assert len(set(runs))==20
        with tempfile.TemporaryDirectory() as t:
            # Extract ONLY proof and independent auditors, NEVER combat runners.
            target=pathlib.Path(t)
            allow=('new/r205/source/','new/r205/evidence/','new/r205/code/r205_wind_independent_readonly_audit.py','new/r205/code/r205_ring_independent_readonly_audit.py')
            for n in names:
                if n.startswith(allow) and not n.endswith('/'):
                    out=target/n;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(z.read(n))
            verified=[]
            for script in ('r205_wind_independent_readonly_audit.py','r205_ring_independent_readonly_audit.py'):
                sp=target/'new/r205/code'/script
                process=subprocess.run([sys.executable,str(sp)],capture_output=True,text=True,check=True)
                verified.append(json.loads(process.stdout))
            assert verified[0]['files']==12 and verified[0]['combat_reexecutions']==0
            assert verified[1]['dbs']==8 and verified[1]['combat_reexecutions']==0
            assert verified[0]['commits']+verified[1]['commits']==945
            assert verified[0]['events']+verified[1]['events']==2812
            assert verified[0]['attacks']+verified[1]['attacks']==462
    o={'result':'PASS_R205_COLD_PORTABLE_RECOVERY','zip_sha256':sha(p.read_bytes()),
       'files_hashed':len(expected),'sqlite_audited':20,'commits':945,'events':2812,'attacks':462,
       'old_runs_reexecuted':0,'new_runs_reexecuted':0,
       'wind_audit':verified[0]['audit'],'ring_audit':verified[1]['audit']}
    print(json.dumps(o,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
