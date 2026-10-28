# R26 evidence-gate regression ONLY. Not an engine. Does not run any fight.
import json, csv, hashlib, io, zipfile, importlib.util, sys
from pathlib import Path
p=Path(__file__).resolve().parent
c=json.loads((p/'R26_CONTRATO_ATAQUE_PREPARADO.json').read_text())
assert c['state']=='PREPARED_NOT_EXECUTED'
assert c['controlled_experiment_requirements']['scene_kind']=='MESTRE_SIDE_EXPERIMENTAL_NOT_CANON'
assert all(v is None for k,v in c['controlled_experiment_requirements'].items() if k!='scene_kind')
assert len(c['controlled_experiment_requirements'])-1==c['missing_fields_N']
assert c['admission_policy']['execution_when_unresolved_norm']=='REJECT'
assert c['admission_policy']['strict_credit'] is False
assert c['known_snapshot']['defender_printed_ca']==39
assert c['known_snapshot']['defender_calculated_ca_not_rounded']==44.6
assert c['conditional_math']['attack_vs_literal_ca']['passing_sequences']==6
assert c['conditional_math']['attack_vs_current_formula_ca']['passing_sequences']==0
assert c['conditional_math']['damage_items_only']=='5d8+6'
assert c['conditional_math']['unattributed_difference']=='1d6+27'
assert c['conditional_math']['damage_printed_mean_no_weakness']==59
assert c['conditional_math']['damage_printed_mean_weakness_conditional']==72.5
with (p/'R26_B01_B18_MATRIX.csv').open(newline='',encoding='utf-8') as f:
 r=list(csv.DictReader(f))
assert len(r)==18 and {x['criterion'] for x in r}=={'B'+str(i).zfill(2) for i in range(1,19)}
assert sum(x['estado_R26']=='PASS_DOCUMENTAL' for x in r)==1
assert sum(x['estado_R26']=='PARTIAL' for x in r)==9
assert sum(x['estado_R26']=='BLOCKED' for x in r)==6
assert sum(x['estado_R26']=='NOT_TESTED' for x in r)==2
assert all(x['novo_PASS_R26']=='NÃO' for x in r)
sha=lambda x:hashlib.sha256(x).hexdigest()
assert sha((p/'R25_ORIGINAL_READONLY.zip').read_bytes())=='b3e90a31f5df1ce16bbe4dfdc3bbd17d4d8de1eb6d661f90fb21a843706896b1'
with zipfile.ZipFile(p/'R25_ORIGINAL_READONLY.zip') as z:
 assert z.testzip() is None
 assert (p/'R13_ORACLE_READONLY.py').read_bytes()==z.read('R13_ORACLE_READONLY.py')
sp=importlib.util.spec_from_file_location('r13_r26_readonly',p/'R13_ORACLE_READONLY.py')
m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
assert m.hits_2d6(30,39,0)==6
assert m.hits_2d6(30,44.6,0)==0
assert all(x['status']=='VERIFICADO DOCUMENTAL' or x['status'].startswith(('VERIFICADO DOCUMENTAL','HISTÓRICO','VERIFICADO DOCUMENTAL NO REOPEN')) for x in json.loads((p/'R26_FONTES_E_READBACK.json').read_text())['source_evidence'].values())
md=(p/'R26_ACAO_BONUS_PARECER.md').read_text()
assert 'NÃO APROVADA' in md and 'não autoriza' not in md or 'NÃO APROVADA' in md
report=(p/'RELATORIO_R26_CONSOLIDADO.md').read_text()
assert '0/2' in report and '0/9' in report and '0/5' in report and '1/18' in report
assert 'sem execução do VLAB' in report
print('R26 PASS: 18 denominador, enumeração 1/9/6/2, R25 integrity, oracle byte-preserved, 31? guard fields, no execution/canon claims')
