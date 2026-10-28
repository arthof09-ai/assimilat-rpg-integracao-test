"""Reproducible synthetic stress; does not authorize any real sheet modifications."""
import copy
import random
from levelup_engine import RACE, FIXED_60, die_for, fingerprint, plan_level_up


def run(samples=500, seed=1708):
    rng=random.Random(seed)
    for i in range(samples):
        race=list(RACE)[i % len(RACE)]
        base={'FOR':rng.randint(4,12),'DES':4,'CON':rng.randint(4,12),'INT':rng.randint(3,12),'SAB':4,'CAR':3}
        before_ff=(base['FOR']+base['DES']+base['CON'])*10
        s={'character_id':f'STRESS-{i:04d}','revision':1,'layout':'synthetic','race':race,'level':1,
           'base':base,'permanent':{k:0 for k in base},'equipment':{k:0 for k in base},
           'temporary':{k:0 for k in base},
           'vital':{'vida_inicial':10+base['CON'],'alma_inicial':10+base['INT'],
                    'vida_growth':[],'alma_growth':[]},
           'extras':{'armor':0,'ca_bonus':0,'cd_bonus':0,'proficiency_bonus':2,
                     'vida_extra':0,'alma_extra':0,'pa_comprometido':0},
           'unspent_points':0,'ff_high_watermark':before_ff,
           'ff_locks':{str(k):{'type':'Dano','faces':[1]} for k in range(100,before_ff+1,100)}}
        gain=RACE[race]['points']
        for_inc=rng.randint(0,gain)
        new_ff=before_ff+10*gain
        new_locks={str(k):{'type':'Dano','faces':[1]} for k in range(100,new_ff+1,100) if k>before_ff}
        r={'expected_revision':1,'expected_snapshot_hash':fingerprint(s),'target_level':2,
           'growth_stat_scope':'intrinsic','spirit_id':None,
           'allocations':{'2':{'FOR':for_inc,'CON':gain-for_inc}},
           'policies':{'vida':'fixed','alma':'fixed'},'new_ff_locks':new_locks}
        old=copy.deepcopy(s)
        output=plan_level_up(s,r)
        assert s==old
        assert output['normal']['FF']==new_ff
        assert output['normal']['Alma_PA_Total']==10+base['INT']+FIXED_60[die_for(2,RACE[race]['alma_shift'])]+base['INT']
        assert output['normal']['Vida']==10+base['CON']+FIXED_60[die_for(2,RACE[race]['vida_shift'])]+base['CON']+(gain-for_inc)
        assert output['unspent_points']==0
        assert not output['write_allowed']
    return samples

if __name__=='__main__':
    print(f'STRESS SYNTHETIC PASS {run()}/500, failures=0')
