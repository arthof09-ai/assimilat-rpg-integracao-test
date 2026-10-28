"""R242 semantic adversarial clones of report; never write test evidence or canonical files."""
import copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'code'))
import r242_independent_readonly_audit as a
raw=json.loads((ROOT/'reports/R242_RUN_RAW.json').read_text())
mutations=[]
def add(label,fn):
 clone=copy.deepcopy(raw);fn(clone)
 try:a.audit(ROOT,write=False,mod=clone)
 except AssertionError as e:mutations.append({'name':label,'rejected':True,'reason':str(e)});return
 raise AssertionError('ADVERSARIAL_NOT_DETECTED '+label)
# Locate canonical corresponding cases; compare to source rule states.
find=lambda d,t,r:next(x for x in d['details'] if x['tape']==t and x['rd']==r)
add('negative_crit_forced_admission',lambda d:find(d,[1,1,1],75).__setitem__('status','ADMITTED'))
add('positive_crit_ignored',lambda d:find(d,[6,6,6],75).__setitem__('hit',False))
add('reordered_positive_false',lambda d:find(d,[6,5,6],75).__setitem__('critical','POSITIVE'))
add('negative_pre_effect_modified',lambda d:find(d,[1,1,2],1000).__setitem__('pre_effect_unchanged',False))
add('RD_1000_bypass',lambda d:find(d,[6,6,5],1000).__setitem__('hp_loss_actual',220))
add('RD_nominal_as_actual_forgery',lambda d:find(d,[6,6,5],1000).__setitem__('rd_applied',220))
add('source_sha_replace',lambda d:d.__setitem__('source_beast_sha','0'*64))
add('duplicate_crit_tape',lambda d:d['details'].__setitem__(1,copy.deepcopy(d['details'][0])))
add('fake_official_cells',lambda d:d.__setitem__('official_cells',1))
add('source_critical_outcome_promotion',lambda d:d.__setitem__('source_status','P4'))
add('damage_amount_forgery',lambda d:find(d,[6,6,5],75).__setitem__('raw',999))
add('missing_one_critical_tape',lambda d:d['details'].pop())
report={'gate':'PASS_12_OF_12_SEMANTIC_REPORT_TAMPERS_REJECTED','tests':len(mutations),'details':mutations,'original_report_modified':False}
(ROOT/'reports/R242_ADVERSARIAL_AUDIT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
