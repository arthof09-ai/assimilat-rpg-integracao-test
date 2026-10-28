"""Deliberate crash only in isolated NEW R115 SQLite, never historical ledgers."""
import sys,hashlib,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import r112_native_battle as bridge
from vlab_effects_v08 import apply_weapon_attack
from vlab_rd_v08 import Resistances
core=bridge.core
p=Path(sys.argv[1]);mode=sys.argv[2]
s,head,rev=core.load(p)
assert rev==1 and s['active']=='B' and s['actors']['B']['resource']['standard']==1
cmd='LAB-CMD-R115-'+hashlib.sha256((str(p)+'|FAULT_NATIVE_CRIT').encode()).hexdigest()[:24]
payload={'actor':'B','target':'E','crits':[6,6,5],'attack_tape':[4]*6,'damage_tape':[5]*20,
         'reason':'R115 INJECTED CRASH, NOT CAMPAIGN RNG; SOURCE-NATIVE-DIRECTED PROBE'}
def resolver(candidate,request,seq):
    sc=bridge.scene_from(candidate);src,st,proof=bridge.source_and_state(candidate,'B','E','BASIC')
    assert seq==2
    hit=apply_weapon_attack(sc,'B','E',source=src,state=st,proofs=proof,roll_score=162,damage=100,
      damage_tag='perfurante',rd=Resistances(general=35),
      damage_dice_groups=((20,10),),damage_roll_groups=((5,)*20,),damage_fixed_bonus=0,
      critical_sequence=(6,6,5),attack_roll_attempts=((4,4,4,4,4,4),),attack_bonus=138)
    for a,c in sc.actors.items():
        obj=bridge.asdict(c)
        for k in ('ca','base_speed'):obj[k]=int(obj[k]) if obj[k] is not None else None
        candidate['actors'][a]['resource']=obj
    candidate['action_indexes']['B']+=1
    return {'kind':'NATIVE_CRIT_SOURCE_GATED','native_action':hit,'no_synthetic_damage_resolver':True}
core.event_commit(p,cmd,'FAULT_NATIVE_CRITICAL_TEST',payload,resolver,failpoint=mode)
