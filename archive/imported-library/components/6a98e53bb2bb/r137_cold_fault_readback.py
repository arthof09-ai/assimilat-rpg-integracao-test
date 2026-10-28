"""Cold standard-library readback of paid-reaction crash fault banks; no native import.
Never invokes a runner on the UNKNOWN_EFFECT bank.
"""
from pathlib import Path
import json,sqlite3,hashlib
ROOT=Path(__file__).resolve().parent
D=[('R134_AFTER_INTENT_973213','INTENT'),('R134_AFTER_COMMIT_973214','COMMIT')]
report=[]
for name,kind in D:
 p=ROOT/'runs'/f'{name}.sqlite'
 with sqlite3.connect(p) as c:
  meta=dict(c.execute('SELECT key,value FROM meta'))
  evs=[json.loads(x[0]) for x in c.execute('SELECT row_json FROM events ORDER BY seq')]
  pend=[dict(zip(('cmd_id','base_head','kind','payload_json'),x)) for x in c.execute('SELECT cmd_id,base_head,kind,payload_json FROM pending')]
 st=json.loads(meta['state']);r=st['actors']['F1']['resource']
 if kind=='INTENT':
  assert int(meta['revision'])==2 and len(evs)==2 and len(pend)==1
  assert pend[0]['kind']=='STRIKE' and r['hp']==479 and r['pa']==424 and r['reaction']==1
 else:
  assert int(meta['revision'])==3 and len(evs)==3 and len(pend)==0
  action=evs[-1]['detail']['native_actions'];assert action[0]['action']=='CAPA_POEIRA' and action[0]['PA_spent']==35
  assert action[1]['action']=='weapon_attack' and r['hp']==245 and r['pa']==389 and r['reaction']==0
  assert action[1]['before_hp']==479 and action[1]['after_hp']==245 and action[1]['hp_loss_actual']==234
 report.append({'run_id':name,'status':'UNKNOWN_EFFECT_HOLD_DO_NOT_REPLAY' if kind=='INTENT' else 'EXACT_ONE_COMMIT',
                'ledger_events':len(evs),'pending':len(pend),'HP_F1':r['hp'],'PA_F1':r['pa'],
                'reaction_slot':r['reaction'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
                'auditor_imports_native':False})
(ROOT/'R137_COLD_FAULT_READBACK.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
