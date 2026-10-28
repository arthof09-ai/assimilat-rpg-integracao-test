from __future__ import annotations
import hashlib,json,zipfile
from pathlib import Path
BASE=Path(__file__).resolve().parent
OUT=BASE.parent/'PA_R29_R38_CONSULTOR_OPERACIONAL_TEST_20261020.zip'
FILES=[
'PA_R28_QMC05_NATIVO_INTEGRADO_TEST_20261020.zip',
'RUN_R29_R38.py','test_r29_r38.py','test_mobile_r34.py',
'CONSULTA_MOBILE_R34.py','CONSULTA_MOBILE_DEMO_INPUT.json',
'RECIBO_R34_CONSULTA_REAL.json','FICHA_R34_MESTRE.md',
'CORPUS_12_FONTE_NOTION.json','BENCHMARK_R35_12_PARECERES.json','build_research_r35.py',
'PROTOCOLO_OPERACIONAL_CHAT_R34.md','R31_R32_MATRIZ_AUTORIDADE.json','STATUS_R29_R38.json',
'CANARIO_R36_HISTORICO_READONLY.json','CANARIO_R36_NOVO_PROJETO_READONLY.json',
'PRE_R36_HASHES.txt','POS_R36_HASHES.txt','BENCHMARK_R35_RESULTADO.log',
'R30_R35_TESTES.log','NOVOS_R29_R38_TESTES.log','RUN_R29_R38_RESULT.json',
'RUN_R29_R38_MAIN.log','RELATORIO_R29_R38.md','PSV_R29_R38_FINAL.md',
'BUILD_PACOTE_R29_R38.py'
]
if len(FILES)!=len(set(FILES)):raise SystemExit('duplicate inputs')
manifest={'archive':'PA_R29_R38_CONSULTOR_OPERACIONAL_TEST_20261020.zip',
          'version':'PA R29–R38 TEST 1.0','files':{}}
for f in sorted(FILES):
    p=BASE/f
    if not p.is_file():raise SystemExit('MISSING:'+f)
    raw=p.read_bytes()
    manifest['files'][f]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
(BASE/'MANIFEST_R29_R38.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for f in sorted(FILES+['MANIFEST_R29_R38.json']):
        p=BASE/f;zi=zipfile.ZipInfo(f,date_time=(2026,10,20,12,0,0));zi.compress_type=zipfile.ZIP_DEFLATED;zi.external_attr=(0o644<<16)
        z.writestr(zi,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=6)
with zipfile.ZipFile(OUT) as z:
    bad=z.testzip()
    for f,rec in manifest['files'].items():
        a=z.read(f);assert len(a)==rec['bytes'] and hashlib.sha256(a).hexdigest()==rec['sha256']
assert bad is None
print('ZIP',OUT,'BYTES',OUT.stat().st_size,'SHA256',hashlib.sha256(OUT.read_bytes()).hexdigest(),'FILES',len(FILES)+1,'CRC',bad or 'PASS')
