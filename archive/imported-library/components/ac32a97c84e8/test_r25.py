from pathlib import Path
from hashlib import sha256
import importlib.util,csv,json,zipfile
from R25_PREFLIGHT_ONLY import blockers,gate
R=Path(__file__).resolve().parent
c=json.loads((R/'R25_CONTRATO_PREFLIGHT.json').read_text(encoding='utf8'))
s=json.loads((R/'FONTES_R25_READBACK.json').read_text(encoding='utf8'))
assert c['synthetic_arithmetic_only']['real_events']==0
assert c['status_B15']=='PARTIAL' and c['strict_full_fight']=='0/2'
assert len(blockers(c))>=20 and not gate(c)['admissible_for_operator_review']
assert set(['jaku','ong','ong_morto','gloves','dragon','combat','beast','dmg_rank']).issubset(s)
assert sha256((R/'R24_ORIGINAL_READONLY.zip').read_bytes()).hexdigest()=='13151e4ab2914261d3e8cc97a85925590bffb1a68eb10c238de2d57f7a5048b5'
with zipfile.ZipFile(R/'R24_ORIGINAL_READONLY.zip') as z:
 assert z.testzip() is None
 with zipfile.ZipFile(__import__('io').BytesIO(z.read('DMG_R24_DECISIVE_ADDENDUM/R24_V01_ORIGINAL_READONLY.zip'))) as z1:
  assert (R/'R13_ORACLE_READONLY.py').read_bytes()==z1.read('DMG_R24_INDEPENDENT_SANDBOX/r13_oracle.py')
spec=importlib.util.spec_from_file_location('r13_external_readonly',R/'R13_ORACLE_READONLY.py')
module=importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name]=module;spec.loader.exec_module(module)
assert module.hits_2d6(30,39,0)==6 and module.chance_hits(30,39,0)==1/6
assert module.hits_2d6(30,38,0)==10 # lower CA improves
assert module.hits_2d6(30,44,0)==0 # higher CA prevents all 2d6 rolls (max 42)
assert (5*4.5+3.5+33)==59.0 and (59+3*4.5)==72.5
assert (2*4.5+2)+(2*4.5+2)+(1*4.5+2)==28.5 # NOT printed total; residual is UNKNOWN
assert (5*4.5+3.5+33)-28.5==30.5 # leftover is a mixed 1d6+27, not settled by 5d8 matching
assert (1*4.5+2)+3*4.5==20.0 # fire gloves only, weakness bonus
assert abs(10+28+33/5-44.6)<1e-10
with (R/'R25_MATRIX_18.csv').open(encoding='utf8',newline='') as f: rows=list(csv.DictReader(f))
assert len(rows)==18 and len(set(r['criterion'] for r in rows))==18
states=[r['estado_R25'] for r in rows]
assert states.count('PASS_DOCUMENTAL')==1 and states.count('PARTIAL')==9 and states.count('BLOCKED')==6 and states.count('NOT_TESTED')==2
assert all(r['certificado_adicional_R25']=='NO' for r in rows)
with (R/'R25_MATRIZ_LEGALIDADE_13.csv').open(encoding='utf8',newline='') as f: gates=list(csv.DictReader(f))
assert len(gates)==13
assert any(r['id']=='Q04' and r['veredito']=='BLOCKED_NORM' for r in gates)
assert any(r['id']=='Q06' and '5d8' in r['evidencia'] for r in gates)
assert '0/5' in (R/'RELATORIO_R25_CONSOLIDADO.md').read_text(encoding='utf8')
assert 'NÃO ENVIADO' in (R/'PEDIDO_OPERACIONAL_CM000006_NAO_ENVIADO.md').read_text(encoding='utf8')
print('R25 PRIMARY TEST SUITE PASS: continuity/oracle, attack source consistency, fail-closed preflight, statuses, governance')
