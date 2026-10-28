"""Search locally for the exact historical AI09 v0.9 ZIP; never extract or execute code."""
from pathlib import Path
from hashlib import sha256
from zipfile import ZipFile, BadZipFile
import argparse, json, sys
EXPECTED_SHA='80683c8d75c464ada2ad34e8ff3b188193d2dcb9308eea58af5af2b035f5c894'
EXPECTED_BYTES=201898
EXPECTED_ENTRIES=84
EXPECTED_NAME='SIM-DMG-VLAB-AI09-SCENE-TRANSFORM-INTEGRATED-v0.9.zip'

def evaluate(data, label):
    result={'source':label,'size_bytes':len(data),'sha256':sha256(data).hexdigest(),'authenticated':False,'reason':None}
    if len(data)!=EXPECTED_BYTES:
        result['reason']='SIZE_MISMATCH'
    elif result['sha256']!=EXPECTED_SHA:
        result['reason']='HASH_MISMATCH'
    else:
        from io import BytesIO
        try:
            with ZipFile(BytesIO(data)) as z:
                infos=z.infolist()
                if len(infos)!=EXPECTED_ENTRIES: result['reason']='MEMBER_COUNT_MISMATCH'
                elif len({i.filename for i in infos})!=len(infos):result['reason']='DUPLICATE_MEMBER'
                elif any(i.filename.startswith('/') or '..' in i.filename.replace('\\','/').split('/') for i in infos):result['reason']='UNSAFE_MEMBER'
                elif z.testzip():result['reason']='CRC_FAILURE'
                else:result['authenticated']=True;result['reason']='VERIFIED'
        except (BadZipFile, OSError) as e:result['reason']=type(e).__name__
    return result

def scan(roots, max_member_bytes=20_000_000):
    results={'expected_name':EXPECTED_NAME,'expected_sha256':EXPECTED_SHA,'expected_bytes':EXPECTED_BYTES,'expected_members':EXPECTED_ENTRIES,
             'searched_roots':[str(p) for p in roots], 'regular_files_scanned':0,'outer_zips_opened':0,'nested_zip_candidates':0,
             'direct_candidates':[],'nested_candidates':[],'authenticated':False,'errors':[]}
    seen=set()
    for root in roots:
        if not root.exists():continue
        paths=([root] if root.is_file() else root.rglob('*'))
        for path in paths:
            if not path.is_file() or path.is_symlink():continue
            try:
                key=(path.stat().st_dev,path.stat().st_ino)
                if key in seen:continue
                seen.add(key)
                results['regular_files_scanned']+=1
                size=path.stat().st_size
                # Size-first and name-first exact-check (no accidental execution).
                if size==EXPECTED_BYTES or path.name.lower()==EXPECTED_NAME.lower():
                    item=evaluate(path.read_bytes(),str(path))
                    results['direct_candidates'].append(item)
                    results['authenticated'] |= item['authenticated']
                if path.suffix.lower()=='.zip':
                    try:
                        with ZipFile(path) as z:
                            results['outer_zips_opened']+=1
                            for zi in z.infolist():
                                if zi.is_dir():continue
                                # Only decompress tiny candidate members, not all archived data
                                if zi.file_size==EXPECTED_BYTES or Path(zi.filename).name.lower()==EXPECTED_NAME.lower():
                                    results['nested_zip_candidates']+=1
                                    if zi.file_size > max_member_bytes:
                                        results['nested_candidates'].append({'source':str(path)+'::'+zi.filename,'reason':'TOO_LARGE','authenticated':False})
                                        continue
                                    try:
                                        candidate=z.read(zi)
                                        item=evaluate(candidate,str(path)+'::'+zi.filename)
                                        results['nested_candidates'].append(item)
                                        results['authenticated'] |= item['authenticated']
                                    except Exception as e:
                                        results['errors'].append({'zip':str(path),'member':zi.filename,'error':str(e)[:200]})
                    except (BadZipFile, OSError, RuntimeError) as e:
                        results['errors'].append({'zip':str(path),'error':str(e)[:200]})
            except (OSError, PermissionError) as e:results['errors'].append({'path':str(path),'error':str(e)[:200]})
    results['status']='FOUND_VERIFIED' if results['authenticated'] else 'BLOCKED_NO_AUTHENTIC_BYTES'
    return results

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('roots',nargs='*',default=['/mnt/data']);ap.add_argument('--output');a=ap.parse_args()
    r=scan([Path(p) for p in a.roots]);s=json.dumps(r,ensure_ascii=False,indent=2,sort_keys=True)
    if a.output:Path(a.output).write_text(s+'\n')
    print(s)
    sys.exit(0 if r['authenticated'] else 3)
