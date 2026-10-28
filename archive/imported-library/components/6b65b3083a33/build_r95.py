from pathlib import Path
import json
R=Path(__file__).resolve().parent
src=json.loads((R/'R94_SOURCE_FREEZE.json').read_text())
src['source_note']='R95 corrected: 60-turn capped independent compare; fixed exogenous opening B/E means no invented Beast initiative proficiency. Basic physical documented values, no movement, no reactions, no positive PA; not full power.'
for p in src['profiles'].values():
 p['notes']=p.get('notes','').replace('R94','R95')
for m in src['matchups']:
 m['id']=m['id'].replace('R94','R95')
(R/'R95_SOURCE_FREEZE.json').write_text(json.dumps(src,ensure_ascii=False,indent=2)+'\n')
pr={'operation':'OP-VLAB-FUSION-SANDBOX-01','stage':'R95_FIXED_OPENING_HORIZON_AUDIT_CORRECTION','preregistered_before_first_R95_execution':True,'source_gate':'BASIC_PHYSICAL_SOURCE_EXPLICIT','seeds':{'development':[495101],'holdout':[495801]},'sides':['B_LEFT','E_LEFT'],'horizon':60,'opening_conditions':['B_FIRST','E_FIRST'],'matchups':4,'target_runs':16,'unit':'species x seed; sides & two fixed openings are within-block conditions, do not count 16 independent samples','corrections':['R92 R94 inherited default60 despite prereg120; both exploratory/QUARANTINE, do not promote','R94 resumed one scene toward prereg120 and generated a side mismatch','new seeds for R95, no revision to historical ledgers'],'assumptions':['No naturally rolled Beast initiative or unproven proficiency','No PA expenditure: documented basic 0PA only','No movement, active reactions, spellcast, transformation or abilities other than documented Auren +8 duelist title after 2 turns','60 completed individual actor turns cap; each NORMAL_ATTACK+TURN_END is one turn'],'scientific_scope':'Source-admissible basic attack conditional on exogenous opening, NOT full match under full rules.'}
(R/'R95_PREREG_STATIC_OPENING.json').write_text(json.dumps(pr,ensure_ascii=False,indent=2)+'\n')
a=(R/'r94_fixed_order_adapter.py').read_text().replace('R94_SOURCE_FREEZE.json','R95_SOURCE_FREEZE.json').replace('R94_PREREG_FIXED_OPENING.json','R95_PREREG_STATIC_OPENING.json').replace('r94_', 'r95_').replace('R94','R95').replace('r94','r95').replace('fixed_runs','r95_runs').replace('max_turns=60','max_turns=60')
a=a.replace('def run(seed,side,outdir,max_turns=60):\n',"def run(seed,side,outdir,max_turns=60):\n    if max_turns!=PREREG['horizon']:raise Deny('HORIZON_NOT_PREREG')\n")
a=a.replace("'reason':'60_TURNS_NO_SURVIVOR'","'reason':'60_ACTOR_TURNS_NO_KO'")
a=a.replace('folder)\n                    r[\'cohort\']','folder,PREREG[\'horizon\'])\n                    r[\'cohort\']')
(R/'r95_fixed_order_adapter.py').write_text(a)
b=(R/'r94_fixed_order_cold_auditor.py').read_text().replace('R94_SOURCE_FREEZE.json','R95_SOURCE_FREEZE.json').replace('R94_PREREG_FIXED_OPENING.json','R95_PREREG_STATIC_OPENING.json').replace('R94','R95').replace('r94','r95').replace('fixed_runs','r95_runs').replace("p=={'horizon':120}","p=={'horizon':60}")
(R/'r95_fixed_order_cold_auditor.py').write_text(b)
print('R95 built with prereg60, explicit runner gate, fresh seeds and IDs')
