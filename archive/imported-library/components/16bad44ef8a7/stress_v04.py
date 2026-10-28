"""Deterministic offline conservation and activation invariants; not an E2E Notion test."""
import random
from transform_contract_v04 import activate_verified,new_ledger,deactivate,damage,level_up_maxima
from levelup_engine import InvalidPlan

rng=random.Random(20261009)
checks=0
for i in range(5000):
    n=rng.randrange(1,10000)
    it=rng.randrange(0,5000)
    sp=rng.randrange(0,5000)
    pac=rng.randrange(0,3000)
    pap=rng.randrange(0,1000)
    st=dict(normal_current=n,normal_max=n+rng.randrange(0,10000),
       item_current=it,item_max=it+rng.randrange(0,400),
       spirit_current=0,spirit_max=sp,transformed=False,
       pa_normal_current=pac,pa_normal_max=pac+rng.randrange(0,4000),
       pa_spirit_current=0,pa_spirit_max=pap)
    act=activate_verified(st,new_ledger(f'A{i}'),actor_id=f'A{i}',scene_id=f'S{i}-1',
         event_id=f'E{i}-1',spirit_id='SPIRIT',new_spirit_hp_max=sp,
         new_spirit_pa_max=pap,activation_cost_paid_evidence='SYNTHETIC-VALIDATED',provenance='SYNTHETIC')
    checks+=1
    d=rng.randrange(0,20000)
    attacked=damage(act['after'],d)
    assert sum(attacked['debit'].values())+attacked['unabsorbed_damage']==d
    assert attacked['after']['pa_normal_current']==pac
    checks+=2
    over=deactivate(attacked['after'])
    assert over['after']['normal_current']==attacked['after']['normal_current']
    assert over['after']['pa_normal_current']==pac
    assert over['after']['spirit_current']==0 and over['after']['pa_spirit_current']==0
    checks+=3
    # Reuse same scene cannot mint a second full reserve.
    try:
        activate_verified(over['after'],act['ledger'],actor_id=f'A{i}',scene_id=f'S{i}-1',event_id=f'E{i}-2',
           spirit_id='SPIRIT',new_spirit_hp_max=sp,new_spirit_pa_max=pap,
           verified_rest={'rest_id':f'R{i}', 'kind':'SHORT','completed':True,'verified':True,
                          'after_activation_seq':1,'duration_hours':5},
           activation_cost_paid_evidence='SYNTHETIC',provenance='SYNTHETIC')
    except InvalidPlan:
        checks+=1
    else:raise AssertionError('illegal same-scene refill')
    # Genuine different scene after proven rest refreshes both additional pools ONLY.
    new=activate_verified(over['after'],act['ledger'],actor_id=f'A{i}',scene_id=f'S{i}-2',event_id=f'E{i}-2',
       spirit_id='SPIRIT',new_spirit_hp_max=sp,new_spirit_pa_max=pap,
       verified_rest={'rest_id':f'R{i}','kind':'SHORT','completed':True,'verified':True,
                      'after_activation_seq':1,'duration_hours':4.5},
       activation_cost_paid_evidence='SYNTHETIC',provenance='SYNTHETIC')
    assert new['after']['spirit_current']==sp and new['after']['pa_spirit_current']==pap
    assert new['after']['normal_current']==attacked['after']['normal_current']
    assert new['after']['pa_normal_current']==pac
    checks+=4
    up=level_up_maxima(new['after'],new_normal_vida_max=st['normal_max']+100,
                       new_normal_pa_max=st['pa_normal_max']+100,
                       new_spirit_vida_max=sp+100,new_spirit_pa_max=pap+100)
    assert up['after']['spirit_current']==sp and up['after']['pa_spirit_current']==pap
    assert up['after']['normal_current']==attacked['after']['normal_current']
    checks+=2
print('STRESS V04: cases=5000, invariant_assertions=',checks,'status=PASS')
