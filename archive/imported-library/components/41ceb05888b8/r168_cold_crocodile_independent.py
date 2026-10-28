"""R168 independent stdlib-only causal cold evaluator; imports ONLY historical cold auditor, never combat resolver.
The frozen R159 cold auditor recomputes RNG/event chain/turns, and the additional checks enforce new Crocodile source provenance.
"""
from pathlib import Path
import sys,json,sqlite3,hashlib
HERE=Path(__file__).parent
import os
OLD=Path(os.environ.get('R160_BASE_DIRECTORY','/mnt/data/vlab_r161_work/baseline_r160'))/'r151_r160'
sys.path.insert(0,str(OLD))
from r159_cold_ed_besta_independent import verify
selected=sorted(p for p in (HERE/'runs').glob('R168_ED_AUREN_VS_CROC_BASIC_*.sqlite') if '.checkpoint.' not in p.name)
assert len(selected)==2,'not a paired experimental sample'
reports=[]
for path in selected:
 src=json.loads(path.with_suffix('.genesis.json').read_text())
 assert src['actors']['B']['stats']['att']==[6,6,134] and src['actors']['B']['stats']['damage']==[[20,10]]
 assert src['actors']['B']['resource']['maximum_hp']==5580 and src['actors']['B']['resource']['ca']==112
 assert src['actors']['B']['source']=='3f3c2b324ede813987deda0b382e83c7'
 assert src['actors']['E']['source']=='3ebc2b324ede814bb730d47dd7bd5f02'
 out=verify(path)
 assert out['phase']=='FINISHED' and out['winner']=='E' and out['events']==198 and out['counts']['native_attacks']==66
 assert out['counts'].get('native_specials',0)==0
 # Scientific counters only; no RNG stream redirection or conditional damage assumptions.
 out['source_frozen']='CROC_P3_FULLSPEC_SOURCE_ACTOR_GENESIS_NOT_CANON_PROMOTED';out['natural_Besta_initiative']='UNRESOLVED';out['holdout']='RESERVED_NONBLIND'
 reports.append(out)
total_events=sum(x['events'] for x in reports)
R={'status':'INDEPENDENT_COLD_PASS_TWO_PHYSICAL_CONDITIONAL_DUELS','runs':reports,'runs_checked':len(reports),'commits':total_events,'native_attacks':sum(x['counts']['native_attacks'] for x in reports),'official_benchmark':0,
 'holdout_independence':'NOT PROVED; seed reservation is not blind holdout','new_mechanical_insight':'Crocodile physical base attack ceiling 170 below Auren CA225; only positive critical auto-hit can connect. Auren min physical score 199 > Croc CA112 except R42 negative crit.'}
(HERE/'R168_COLD_ED_CROCODILE_AUDIT.json').write_text(json.dumps(R,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in R.items() if k!='runs'},indent=2,ensure_ascii=False))
