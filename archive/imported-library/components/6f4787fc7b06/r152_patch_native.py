"""Additive controlled continuation R151. Strictly defaults to old hold; R42 only explicit lab flag."""
from pathlib import Path
p=Path(__file__).resolve().parent/'native_v081_controlled/vlab_effects_v08.py'
s=p.read_text()
a="attack_origin:str='NORMAL'):"
b="attack_origin:str='NORMAL',lab_negative_critical_policy:bool=False):"
assert s.count(a)>=1;s=s.replace(a,b,1)
a="if critical=='NEGATIVE':raise EffectBlocked('critical failure consequence unresolved; pre-intent rejection')"
b="if critical=='NEGATIVE' and not lab_negative_critical_policy:raise EffectBlocked('critical failure consequence unresolved; pre-intent rejection')"
assert s.count(a)>=1;s=s.replace(a,b,1)
a="hit=effective_score>d.ca or (advanced and critical=='POSITIVE')"
b="hit=(effective_score>d.ca or (advanced and critical=='POSITIVE')) and critical!='NEGATIVE'"
assert s.count(a)>=1;s=s.replace(a,b,1)
a="'critical':critical,'critical_max_bonus':critical_maximum if advanced and (critical=='POSITIVE' or final_effort) else 0,"
b="'critical':critical,'critical_failure_policy':('CRITICAL_FAILURE / VLAB-LAB-POLICY' if critical=='NEGATIVE' else None),'critical_max_bonus':critical_maximum if advanced and (critical=='POSITIVE' or final_effort) else 0,"
assert s.count(a)>=1;s=s.replace(a,b,1)
p.write_text(s)
print('R42 additive patch written',p)
