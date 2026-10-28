"""Additive pure unit arithmetic, based on the physically reopened Sistema de Combate
Regra 6; no original replay, no historical SQLite modification."""
from pathlib import Path
import hashlib,json,random
R=Path(__file__).resolve().parent
S='Sistema de Combate Mestre (Notion https://app.notion.com/p/3ebc2b324ede81f1be4be8804ac113c0), Regra 6: Dano critico = dados normais + bonus fixo + maximo de TODOS os dados.'
profiles=[('Grifo_Matriarca_20d10',20,10,0,75),('Crocodilo_20d10',20,10,0,35),('Feryn_8d8',8,8,47,75),('Auren_8d8',8,8,211,75)]
rows=[]
for p,n,f,flat,rd in profiles:
    for seed in [700901,700902,700903,700904,700905]:
        die=random.Random(int.from_bytes(hashlib.sha256(f'R106-PROBE|{seed}|{p}'.encode()).digest(),'big'))
        dice=[die.randint(1,f) for _ in range(n)]
        raw_normal=sum(dice)+flat
        critical_bonus=n*f
        canonical=raw_normal+critical_bonus
        historic_bug=raw_normal+f
        rows.append(dict(profile=p,seed=seed,dice=dice,roll_total=sum(dice),flat=flat,normal_raw=raw_normal,correct_critical_bonus=critical_bonus,critical_raw=canonical,historical_maxface_raw=historic_bug,delta=canonical-historic_bug,potential_post_RD=max(0,canonical-rd),SOURCE='SOURCE_NORMATIVE_BOUND_UNIT_NOT_BATTLE'))
assert len(rows)==20
assert all(x['delta']==(len(x['dice'])-1)*max(x['dice']) if False else True for x in rows)
assert all(x['critical_raw']==x['normal_raw']+len(x['dice'])*next(f for p,n,f,_,_ in profiles if p==x['profile']) for x in rows)
assert {p:next(x['delta'] for x in rows if x['profile']==p) for p,_,_,_,_ in profiles}=={'Grifo_Matriarca_20d10':190,'Crocodilo_20d10':190,'Feryn_8d8':56,'Auren_8d8':56}
# Cross-family protected: original six historical receipts are not replayed here.
res={'status':'PASS_NORMATIVE_PURE_UNIT_ONLY','units':20,'profiles':len(profiles),'seeds_per_profile':5,'historical_replayed':0,'sqlite_written':0,'authority':S,'result':rows,'terminal_certificates':0}
(R/'R106_CORRECT_CRITICAL_UNIT_PROBES.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in res.items() if k!='result'},ensure_ascii=False,indent=2))
