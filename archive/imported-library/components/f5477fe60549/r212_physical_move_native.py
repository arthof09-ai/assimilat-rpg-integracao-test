"""R212 source-labelled physical ranged post-move case, no AoO claim.

Native module source is read from recovered R211; R18 event_commit and v081
move_via_verified_path/apply_weapon_attack do all mechanical state mutations.
"""
from __future__ import annotations
import sys,hashlib,json,random,copy,math
from pathlib import Path
from dataclasses import asdict
from fractions import Fraction
R=Path(__file__).resolve().parents[1]
BASE=R.parents[1]/'preflight'/'new'/'r211'/'code'
sys.path.insert(0,str(BASE))
import r211_dynamic_center_native as r211
from vlab_effects_v08 import (Combatant,AbilitySource,ActorActionState,FrozenRuleEvidence,EffectBlocked,
  move_via_verified_path,apply_weapon_attack,end_source_turn,Resistances)
core=r211.core;R18=r211.R18
PRE_B=(R/'source/R212_PHYSICAL_AFTER_MOVE_PREREG.json').read_bytes();PRE=json.loads(PRE_B)
PHASH=hashlib.sha256(PRE_B).hexdigest();VERSION='R212-ADD-NATIVE-PHYSICAL-AFTER-MOVE-1'
A='RAYA_REPLICA_R212';D='ERISTAN_REPLICA_R212';PAIR=(A,D)
SRC_COMBAT=PRE['sources']['combat'];SRC_RAYA=PRE['sources']['raya']
PROOF_MOVE=FrozenRuleEvidence(SRC_COMBAT,'R212-COMBAT-MOVEMENT',hashlib.sha256(SRC_COMBAT.encode()).hexdigest(),'2026-10-20','NOTION_SOURCE_REOPENED_R212')
PROOF_ATTACK=FrozenRuleEvidence(SRC_RAYA,'R212-RAYA-PRINTED-ATTACK',hashlib.sha256(SRC_RAYA.encode()).hexdigest(),'2026-10-20','NOTION_SOURCE_REOPENED_R212')
MOVE=AbilitySource('R212-RAYA-STEP','move','MOVEMENT',SRC_COMBAT,PROOF_MOVE.rule_id,'RULE-DERIVED',target_scope='POSITION',effect_adapter_ready=True,effect_adapter_id='NATIVE-V081-PATH-MOVE')
ATTACK=AbilitySource('R212-RAYA-PRINTED-H-ATTACK','attack','STANDARD',SRC_RAYA,PROOF_ATTACK.rule_id,'RULE-DERIVED',target_scope='ENEMY',requires_range_check=True,requires_line_of_sight=True,effect_adapter_ready=True,effect_adapter_id='NATIVE-V081-WEAPON')
# Only a TEST replica: no writes to Raya nor Eristan, no implicit writer authority.
core.ACTORS[A]={'id':A,'kind':'ED','name':'Raya Vhassar TEST REPLICA','url':SRC_RAYA,'edited':'2026-10-20_READONLY','rank':'Lendário','star':1,'level':21,'hp':1392,'maximum_hp':1392,'pa':632,'ca':221,
 'dex':172,'init_dice':(6,6),'initiative_bonus':188,'attack_dice':(6,6),'attack_bonus':245,'damage_dice':((16,8),(12,6),(4,12)),'damage_flat':294,'damage_tag':'perfurante','rd':14,'rd_status':'SOURCE_SNAPSHOT_PHYSICAL_ONLY',
 'attack_name':'H-ATAQUE-PRINTED-SOURCE-COMBINATION','damage_tag_status':'LAB-HYPOTHESIS-PHYSICAL_VS_MAGIC_SPLIT_PENDING'}
# Eristan is preloaded by R210 as a PROPOSED ON5; create isolated keyed replica.
e=copy.deepcopy(core.ACTORS[r211.E]);e.update(id=D,name='Sikong Eristan PROPOSTO replica');core.ACTORS[D]=e

def dice(seed,code,n,faces):
    h=hashlib.sha256(f'{VERSION}|{seed}|{code}|{n}d{faces}'.encode()).digest()
    rng=random.Random(int.from_bytes(h,'big'));return [rng.randint(1,faces) for _ in range(n)]
def roll_tape(seed):
    return {'hit':dice(seed,'HIT',6,6),'crit':dice(seed,'CRIT',3,6),'damage':[dice(seed,f'DMG{i}',n,f) for i,(n,f) in enumerate(core.ACTORS[A]['damage_dice'])]}

def init_state(db,seed):
    R18.init_db(str(db),'A',seed)
    st=core.state_genesis(seed,PAIR)
    st['r212']={'version':VERSION,'prereg_sha':PHASH,'positions_m':copy.deepcopy(PRE['scene']['positions_m']),'path':[], 'shots':[],'aoo_state':'BLOCKED-SOURCE-ADJACENCY-NOT_EXERCISED'}
    st['position']={'contact':False,'same_layer':True,'line_of_effect':True,'movement':True,'campaign_location':False}
    for actor in PAIR:
        a=st['actors'][actor]['resource'];a['position']=str(tuple(st['r212']['positions_m'][actor]));a['movement']=0
        if actor==A:a['base_speed']=Fraction(137,2).__str__() # encoded as JSON string; Combatant accepts in Fraction()
        # the source's HP maximum remains as supplied
    c=R18.connect(str(db))
    try:
        with c:c.execute('UPDATE meta SET value=? WHERE key="state"',(R18.canonical(st),))
    finally:c.close()

def init(st,p,seq):
    if st['phase']!='INIT' or st['r212']['prereg_sha']!=PHASH or p!={'prereg_sha':PHASH,'actor':A,'seed':st['seed']}:
        raise EffectBlocked('R212_INIT_PREFLIGHT')
    st['phase']='ACTIVE';st['round']=1;st['order']=[A,D];st['turn']=0;st['active']=A
    scene=core.scene(st);scene.actors[A].standard=0
    from vlab_effects_v08 import begin_source_turn
    begin_source_turn(scene,A);core.sync(st,scene)
    return {'kind':'R212_INIT_TEST_ONLY','source_status':'PROPOSED/REPLICA','actor':A,'events_added':copy.deepcopy(scene.events)}

def native_move_shoot(st,p,seq):
    if st['phase']!='ACTIVE' or st['active']!=A or st['r212']['prereg_sha']!=PHASH:
        raise EffectBlocked('R212_ACTIVE_SCOPE')
    seed=st['seed'];t=roll_tape(seed)
    if p!={'actor':A,'target':D,'tape':t,'prereg_sha':PHASH}:
        raise EffectBlocked('R212_PAYLOAD_NOT_PREREGISTERED')
    # Critical failure outcome is not source-resolved: reject before any intent/commit.
    if t['crit'][:2]==[1,1] and t['crit'][2]<=2:raise EffectBlocked('UNRESOLVED_NEGATIVE_CRITICAL')
    s=core.scene(st);a=s.actors[A];d=s.actors[D];before=len(s.events)
    pos=st['r212']['positions_m'];source=pos[A];dest=PRE['scene']['raya_move_destination_m'];target=pos[D]
    if source!=[0,0] or target!=[40,0] or dest!=[5,0]:raise EffectBlocked('COORDINATE_DRIFT')
    speed=Fraction(137,2);travel=Fraction(5)
    mv=move_via_verified_path(s,A,source=MOVE,state=ActorActionState(A,21,a.pa,(MOVE.action_id,),standard_available=True,movement_available=True,
      geometry_confirmed=True,environment_contract=True),proofs=(PROOF_MOVE,),destination=str(tuple(dest)),
      path_evidence='R212_STRAIGHT_5M_OPEN_ROUTE_NO_ADJACENT_ENEMIES_START_DIST40_END_DIST35',travel_cost=travel,speed=speed)
    pos[A]=list(dest);st['r212']['path'].append({'move_seq':mv['seq'],'from':source,'to':dest,'travel_m':5})
    distance=math.dist(dest,target)
    if distance>50 or distance<=0:raise EffectBlocked('OUT_OF_DOCUMENTED_SHORT_RANGE')
    if a.standard!=1 or a.movement!=0 or d.hp<=0:raise EffectBlocked('ACTION_BUDGET_OR_TARGET')
    rolls=tuple(tuple(v) for v in t['damage']);normal=sum(map(sum,rolls))+294;score=sum(t['hit'])+245
    ev=apply_weapon_attack(s,A,D,source=ATTACK,state=ActorActionState(A,21,a.pa,(ATTACK.action_id,),standard_available=True,
       movement_available=False,range_confirmed=True,los_confirmed=True,enemy_ids_visible=(D,)),proofs=(PROOF_ATTACK,),
       roll_score=score,damage=normal,damage_tag='perfurante',rd=Resistances(general=25,provenance='ERISTAN_RD25_PHYSICAL_SOURCE_CONDITIONAL_TOTAL_TAG'),
       damage_dice_groups=core.ACTORS[A]['damage_dice'],damage_roll_groups=rolls,damage_fixed_bonus=294,critical_sequence=tuple(t['crit']),
       attack_roll_attempts=(tuple(t['hit']),),attack_bonus=245,attack_origin='NORMAL',advantage_levels=0,disadvantage_levels=0)
    if a.reaction!=1 or d.reaction!=1:raise EffectBlocked('UNEXPECTED_REACTION_MUTATION')
    end_source_turn(s,A);st['phase']='CENSORED_TEST_WINDOW';st['active']=None;st['finish_reason']='ONE_TURN_HORIZON_NOT_VICTORY'
    core.sync(st,s);st['r212']['shots'].append({'attack_seq':ev['seq'],'after_m':distance,'roll':t,'range_m':50,'hit':ev['hit'],'loss':ev['hp_loss_actual']})
    st['history'].append({'actor':A,'move':True,'attack':True,'censored':True})
    return {'kind':'R212_NATIVE_MOVE_AND_WEAPON_ATTACK','native_events_added':copy.deepcopy(s.events[before:]),'move_seq':mv['seq'],'attack_seq':ev['seq'],
      'attack_result':ev,'pos_before':source,'pos_after':dest,'range_after_m':distance,'status':'CENSORED_WINDOW_NOT_KO_WIN'}

def prevalidate(seed):
    t=roll_tape(seed)
    return not(t['crit'][:2]==[1,1] and t['crit'][2]<=2)

def main():
    results=[];(R/'evidence/db').mkdir(parents=True,exist_ok=True)
    for seed in PRE['seeds']:
        rid=f'R212_PHYSMOVE_S{seed}_ONE_TURN';db=R/'evidence/db'/f'{rid}.sqlite'
        if db.exists():raise RuntimeError('NO_REUSE_RUN_ID '+rid)
        if not prevalidate(seed):
            results.append({'run_id':rid,'seed':seed,'status':'BLOCKED_PREFLIGHT_NEG_CRIT','combats':0});continue
        init_state(db,seed)
        R18.event_commit(str(db),f'LAB-CMD-{rid}-INIT','R212_INIT',{'prereg_sha':PHASH,'actor':A,'seed':seed},init)
        row=R18.event_commit(str(db),f'LAB-CMD-{rid}-MOVE_ATTACK','R212_NATIVE_MOVE_AND_ATTACK',{'actor':A,'target':D,'tape':roll_tape(seed),'prereg_sha':PHASH},native_move_shoot)
        st,head,rev=R18.load(str(db));core.write_checkpoint(str(db))
        ev=row['detail']['attack_result']
        results.append({'run_id':rid,'seed':seed,'status':'CENSORED_ONE_TURN','db':db.name,'commits':rev,'head':head,
          'native_events':len(st['native_events']),'native_moves':1,'physical_attack_attempts':1,'hits':int(ev['hit']),'hp_loss':ev['hp_loss_actual'],
          'rd_applied':ev['rd_applied'],'damage_raw':ev['raw'],'net':ev['net'],'overkill':ev['overkill'],'critical':ev['critical'],
          'raya_movement_spent':1-st['actors'][A]['resource']['movement'],'raya_standard_spent':1-st['actors'][A]['resource']['standard'],
          'raya_reaction_remains':st['actors'][A]['resource']['reaction'],'eristan_hp_final':st['actors'][D]['resource']['hp'],
          'official_winner':None})
    (R/'evidence/R212_RESULTS.json').write_text(json.dumps(results,indent=2,ensure_ascii=False))
    print(json.dumps({'runs':len(results),'complete':sum(bool(x.get('db')) for x in results),'move':sum(x.get('native_moves',0) for x in results),
      'attack':sum(x.get('physical_attack_attempts',0) for x in results),'hits':sum(x.get('hits',0) for x in results),'damage':sum(x.get('hp_loss',0) for x in results)},indent=2))
if __name__=='__main__':main()
