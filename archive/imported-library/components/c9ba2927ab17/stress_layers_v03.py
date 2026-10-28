"""Deterministic stress of layer conservation and no passive refill; synthetic only."""
from random import Random
from layered_vital_v03 import damage_three_layers,project_after_level,project_form_change
R=Random(20261009)
for i in range(7500):
    s={'normal_max':R.randint(0,20000),'item_max':R.randint(0,20000),
       'spirit_max':R.randint(0,20000),'transformed':bool(R.randint(0,1))}
    for k in ('normal','item','spirit'):s[k+'_current']=R.randint(0,s[k+'_max'])
    damage=R.randint(0,60000)
    d=damage_three_layers(s,damage)
    assert sum(d['debit'].values())+d['damage_unabsorbed_after_zero']==damage
    assert all(d['after'][name+'_current']<=s[name+'_current'] for name in ('normal','item','spirit'))
    if not s['transformed']: assert d['debit']['spirit']==0
    else:
        if d['debit']['item']>0:assert d['after']['spirit_current']==0
        if d['debit']['normal']>0:assert d['after']['spirit_current']==d['after']['item_current']==0
    upd=project_after_level(s,new_normal_max=s['normal_max']+R.randint(0,500),
             new_item_max=s['item_max']+R.randint(0,500),new_spirit_max=s['spirit_max']+R.randint(0,500))['after']
    assert all(upd[name+'_current']==s[name+'_current'] for name in ('normal','item','spirit'))
    flip=project_form_change(s,transformed=not s['transformed'],external_gate_checked=True)['after']
    assert all(flip[name+'_current']==s[name+'_current'] for name in ('normal','item','spirit'))
print('STRESS v0.3: 7500/7500 casos sintéticos aprovados (escudos 3 camadas, dano conservado, sem refresh)')
