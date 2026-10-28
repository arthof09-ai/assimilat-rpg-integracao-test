"""Hardened PA R48 peer intake: preserves R47B, handles authentic full archive.
TEST / MASTER-ONLY. No canonical writes, no trust that attestations prove independence.
"""
from __future__ import annotations
import sys,json,zipfile,io,csv,hashlib
from pathlib import Path

R47B=(Path(__file__).resolve().parent/'r47b') if (Path(__file__).resolve().parent/'r47b'/'peer_intake_v2.py').exists() else Path('/mnt/data/PA_R47B_PEER_RECEBIMENTO_20261021')
sys.path.insert(0,str(R47B))
from peer_intake_v2 import (read_csv_checked,assess_rows,load_peer_template,verified_zip_entries,IntegrityError,sha)
ORIGINAL_NAME='FONTE_ORIGINAL_SEM_GABARITO.zip'
ORIGINAL_SHA='5c688a22908b0f55af792c826c20b22e43dd675a3b676a939268c40b9d55fe33'
TEMPLATE=R47B/'source/PEER_TEMPLATE_12_SEM_GABARITO.zip'

def audit(data:bytes,filename:str,template=TEMPLATE):
    expected=load_peer_template(template)
    provenance={'source_type':None,'input_files_verified':0,'original_images_verified':0,'peer_package_signatures_verified':False,'reviewer_independence_proven':False,'canonizations':0}
    if filename.lower().endswith('.csv'):
        csvbytes=data;provenance['source_type']='CSV'
    elif filename.lower().endswith('.zip'):
        if len(data)>60_000_000:raise IntegrityError('review ZIP too large')
        ent=verified_zip_entries(data)
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for n,h in ent.items():
                name=n.casefold()
                if n==ORIGINAL_NAME:
                    if h!=ORIGINAL_SHA:raise IntegrityError('trusted no-gabarito archive was modified')
                    with zipfile.ZipFile(io.BytesIO(z.read(n))) as inner:
                        if inner.testzip() is not None:raise IntegrityError('nested CRC failed')
                        manifest=json.loads(inner.read('MANIFEST_SHA256.json'))
                        if len(manifest)!=14:raise IntegrityError('nested manifest unexpected')
                        for p,q in manifest.items():
                            if sha(inner.read(p))!=q:raise IntegrityError('nested image/source mismatch')
                        assert set(expected)=={Path(p).stem for p in manifest if p.endswith('.jpg')}
                        assert all(expected[Path(p).stem]==v for p,v in manifest.items() if p.endswith('.jpg'))
                        provenance['original_images_verified']=12
                elif any(k in name for k in ('oraculo','gabarito','legacy_rank','r45','r46')):
                    raise IntegrityError('unexpected rank/oracle file name')
            csvs=[n for n in ent if n.casefold().endswith('.csv')]
            if len(csvs)!=1:raise IntegrityError('expected exactly 1 CSV')
            csvbytes=z.read(csvs[0]);provenance['source_type']='ZIP'
            if 'MANIFEST_SHA256_OUTPUT.json' in ent:
                mm=json.loads(z.read('MANIFEST_SHA256_OUTPUT.json'))['files']
                if set(mm)!=set(ent)-{'MANIFEST_SHA256_OUTPUT.json'}:raise IntegrityError('outer manifest does not describe exactly all files')
                for n,h in mm.items():
                    if h!=ent[n]:raise IntegrityError('outer manifest mismatch')
                provenance['input_files_verified']=len(mm)
            if 'FREEZE_RECORD.json' in ent:
                f=json.loads(z.read('FREEZE_RECORD.json'))
                if f.get('csv_sha256')!=sha(csvbytes):raise IntegrityError('frozen csv hash mismatch')
                if f.get('count_total')!=12:raise IntegrityError('frozen cases n!=12')
                if not f.get('pre_oracle'):raise IntegrityError('not a pre-oracle freeze')
                if 'RELATORIO_TECNICO_COMPLETO.md' in ent:
                    if f.get('report_sha256')!=ent['RELATORIO_TECNICO_COMPLETO.md']:
                        raise IntegrityError('frozen report hash mismatch')
                provenance['peer_package_signatures_verified']=True
    else:
        raise IntegrityError('only CSV/ZIP supported')
    rows=read_csv_checked(csvbytes)
    formal=assess_rows(rows,expected)
    if formal['batch_intake']!='FORM_COMPLETE_NOT_SCIENTIFICALLY_VALIDATED':
        raise IntegrityError('12-row peer form incomplete or invalid')
    return {'status':'FORM_COMPLETE_NOT_SCIENTIFICALLY_VALIDATED','formal':formal,'provenance':provenance,'scientific_accuracy':None,'REs_adjudicated':0,'canonical_changes':0}

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
    try:
        p=Path(a.input);x=audit(p.read_bytes(),p.name)
        Path(a.output).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
        print(x['status'], x['provenance'])
    except (IntegrityError,ValueError,KeyError,AssertionError,zipfile.BadZipFile) as e:
        Path(a.output).write_text(json.dumps({'status':'HOLD_OR_REJECT','reason':str(e),'canonical_changes':0},ensure_ascii=False),encoding='utf-8')
        print('HOLD_OR_REJECT',str(e));sys.exit(2)
