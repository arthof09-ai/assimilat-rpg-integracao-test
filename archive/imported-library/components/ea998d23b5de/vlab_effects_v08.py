"""Source-gated event adapters for Combat / Magic / Transform / RD.

No random unverified RPG rule is introduced. A catalog menu proves option
availability; an effect resolver uses source-specific payloads. SourceProof
is an EVIDENCE POINTER only; it must be joined to a physically re-opened Notion
record by the external authoritative gate. Fixtures are LAB_ONLY until then.
"""
from __future__ import annotations
from dataclasses import dataclass,field,asdict
from fractions import Fraction
from copy import deepcopy
from hashlib import sha256
import json
from typing import Literal
from vlab_action_catalog_v01 import ActorActionState,AbilitySource,FrozenRuleEvidence,action_menu
from vlab_rd_v08 import DamageComponent,Resistances,mitigate,RDUnresolved

VERSION='COMBAT-EFFECT-ADAPTER-PARTIAL-v0.8+R108-R117-CONTROLLED'
COMBAT_PAGE='3ebc2b32-4ede-81f1-be4b-e8804ac113c0'
MAGIC_PAGE='3ebc2b32-4ede-81f7-b343-f7270ff91373'
TRANSFORM_PAGE='3f2c2b32-4ede-81c0-ae0e-e4e66212edc9'
class EffectBlocked(ValueError):pass

@dataclass
class Combatant:
    actor_id:str
    hp:int
    pa:int|None
    ca:Fraction
    constitution:int
    armor:int
    fortitude:int
    reflex:int
    position:str
    rank:str='Bronze'
    standard:int=1
    movement:int=1
    reaction:int=1
    mode:str='NORMAL'
    spirit_id:str|None=None
    form_overlay:dict|None=None
    transformation_remaining:int|None=None
    maximum_hp:int|None=None
    base_speed:Fraction|None=None
    beast_rank_index:int|None=None
    final_effort_used:bool=False
    immobile_next_own_turns:int=0
    def __post_init__(self):
        if self.hp<0 or (self.pa is not None and self.pa<0):raise EffectBlocked('invalid resources')
        if self.maximum_hp is not None and (self.maximum_hp<=0 or self.hp>self.maximum_hp):raise EffectBlocked('invalid maximum hp')
        if self.immobile_next_own_turns<0:raise EffectBlocked('invalid immobilization')
        if self.standard not in (0,1) or self.movement not in (0,1) or self.reaction not in (0,1):raise EffectBlocked('invalid action budget')

@dataclass
class Scene:
    actors:dict[str,Combatant]
    events:list[dict]=field(default_factory=list)
    seed:int=0
    provenance:str='LAB-TEST-SYNTHETIC-NONCANON'
    def __post_init__(self):
        if any(i!=x.actor_id for i,x in self.actors.items()):raise EffectBlocked('actor map/ID mismatch')
    def record(self,entry):
        row={'seq':len(self.events)+1,'engine':VERSION,'provenance':self.provenance,**entry}
        self.events.append(row)
        return row
    def checksum(self):return sha256(json.dumps(self.events,sort_keys=True,ensure_ascii=False,default=str).encode()).hexdigest()


def _require_option(scene:Scene,actor_id:str,source:AbilitySource,state:ActorActionState,proofs:tuple[FrozenRuleEvidence,...], *, phase='TURN',strict=True,target=None):
    if actor_id not in scene.actors:raise EffectBlocked('actor not present')
    if state.actor_id!=actor_id:raise EffectBlocked('actor/ability context mismatch')
    compile=action_menu(state,(source,),phase=phase,strict=strict,source_evidence=proofs)
    matches=[o for o in compile.legal_options if o.target_id==target]
    if not matches:raise EffectBlocked('not source/legal/action-ready: '+str(compile.rejected))
    return matches[0]


def weak_status(actor:Combatant)->bool:
    """Strict <10% from Combat Regra 7. Unknown HP cap fails closed."""
    if actor.maximum_hp is None:raise EffectBlocked('HP maximum required for weak status')
    return actor.hp>0 and 10*actor.hp<actor.maximum_hp


def effective_movement_speed(actor:Combatant):
    if actor.base_speed is None:raise EffectBlocked('source speed unknown')
    if actor.immobile_next_own_turns:return Fraction(0)
    return Fraction(actor.base_speed,2) if weak_status(actor) else Fraction(actor.base_speed)


def apply_weapon_attack(scene:Scene,attacker_id:str,defender_id:str,*, source:AbilitySource,
                        state:ActorActionState, proofs:tuple[FrozenRuleEvidence,...],
                        roll_score:int,damage:int,damage_tag:str,rd:Resistances,
                        strict:bool=True,defense_event:dict|None=None,
                        damage_dice_groups:tuple[tuple[int,int],...]|None=None,
                        damage_roll_groups:tuple[tuple[int,...],...]|None=None,
                        damage_fixed_bonus:int|None=None,
                        critical_sequence:tuple[int,int,int]|None=None,
                        attack_roll_attempts:tuple[tuple[int,...],...]|None=None,
                        attack_bonus:int|None=None,
                        final_effort:bool=False):
    """Historical v0.8.1 source-gated attack resolver with additive source-verified
    critical, weak and final-effort paths.  Legacy scalar calls remain supported
    solely for noncritical/non-weak historical regression; no official promotion.
    No new standalone damage engine is used; vlab_rd_v08.mitigate remains authority.
    """
    a=scene.actors[attacker_id];d=scene.actors[defender_id]
    if a.standard!=1:raise EffectBlocked('standard already spent')
    if source.kind!='attack' or source.economy!='STANDARD':raise EffectBlocked('wrong attack adapter')
    if not isinstance(roll_score,int) or isinstance(roll_score,bool) or roll_score<0:raise EffectBlocked('invalid roll')
    _require_option(scene,attacker_id,source,state,proofs,strict=strict,target=defender_id)
    if d.hp<=0 or a.hp<=0:raise EffectBlocked('not a current legal actor/target')
    advanced=any(x is not None for x in (damage_dice_groups,damage_roll_groups,damage_fixed_bonus,critical_sequence,attack_roll_attempts,attack_bonus)) or final_effort
    if advanced and (damage_dice_groups is None or damage_roll_groups is None or damage_fixed_bonus is None
                     or critical_sequence is None or attack_roll_attempts is None or attack_bonus is None):
        raise EffectBlocked('full atomic critical/weak proof requires dice, crit and scored attack tape')
    weak=False; critical='NONE';critical_maximum=0;effective_score=roll_score
    if advanced:
        weak=weak_status(a)
        if len(critical_sequence)!=3 or any(type(x)!=int or not 1<=x<=6 for x in critical_sequence):raise EffectBlocked('invalid sequential critical evidence')
        if critical_sequence[:2]==(6,6) and critical_sequence[2]>=5:critical='POSITIVE'
        elif critical_sequence[:2]==(1,1) and critical_sequence[2]<=2:critical='NEGATIVE'
        if critical=='NEGATIVE':raise EffectBlocked('critical failure consequence unresolved; pre-intent rejection')
        if not attack_roll_attempts or any(len(t)==0 or any(type(x)!=int or not 1<=x<=6 for x in t) for t in attack_roll_attempts):
            raise EffectBlocked('invalid hit tape')
        expected_attempts=2 if weak else 1
        if len(attack_roll_attempts)!=expected_attempts:raise EffectBlocked('weak disadvantage requires two attack rolls')
        scores=[sum(t)+attack_bonus for t in attack_roll_attempts]
        effective_score=min(scores)-2 if weak else scores[0]
        if roll_score!=effective_score:raise EffectBlocked('attack score does not match authoritative roll/disadvantage')
        if len(damage_dice_groups)!=len(damage_roll_groups) or not damage_dice_groups:raise EffectBlocked('dice groups mismatch')
        if any(type(n)!=int or type(f)!=int or n<=0 or f<2 or len(rolls)!=n or any(type(v)!=int or not 1<=v<=f for v in rolls)
               for (n,f),rolls in zip(damage_dice_groups,damage_roll_groups)):
            raise EffectBlocked('invalid damage dice tape')
        if type(damage_fixed_bonus)!=int:raise EffectBlocked('invalid damage flat bonus')
        critical_maximum=sum(n*f for n,f in damage_dice_groups)
        base=sum(sum(rolls) for rolls in damage_roll_groups)+damage_fixed_bonus
        if damage!=base:raise EffectBlocked('scalar damage not equal to dice evidence')
        if final_effort:
            if a.beast_rank_index is None or a.beast_rank_index<11 or a.final_effort_used or not weak:
                raise EffectBlocked('final effort not source eligible or already used')
            if critical=='POSITIVE':raise EffectBlocked('final effort overlaps natural critical; precedence unresolved')
            if effective_score<=d.ca:raise EffectBlocked('final effort forced hit on miss unresolved; safe rejection')
        # Never grant a critical's outcome based only on a synthetic score without tape.
    elif a.maximum_hp is not None and weak_status(a):
        raise EffectBlocked('legacy scalar attack cannot omit weak disadvantage')
    if defense_event is not None:
        if not scene.events or scene.events[-1]!=defense_event or defense_event.get('seq')!=len(scene.events):
            raise EffectBlocked('defense event must be immediate and unconsumed')
        if defense_event.get('by')!=defender_id or defense_event.get('attack_score')!=effective_score:
            raise EffectBlocked('defense event does not match incoming attack')
        if defense_event.get('action') not in ('DEFENDER','ESQUIVAR'):
            raise EffectBlocked('unresolved defense')
    negated=bool(defense_event.get('damage_negated')) if defense_event else False
    hit=effective_score>d.ca or (advanced and critical=='POSITIVE')
    applied_raw=damage+(critical_maximum if advanced and (critical=='POSITIVE' or final_effort) and hit else 0)
    # This is the existing v0.8.1 RD module; no local alternative formula.
    outcome=mitigate((DamageComponent(applied_raw,damage_tag,source.action_id),),rd) if hit and not negated else None
    before=d.hp;before_weak=weak_status(d) if d.maximum_hp is not None else None
    a.standard=0
    if outcome:d.hp=max(0,d.hp-outcome.effective)
    if final_effort:
        a.final_effort_used=True
        a.immobile_next_own_turns=2
    after_weak=weak_status(d) if d.maximum_hp is not None else None
    return scene.record({'action':'weapon_attack','from':attacker_id,'to':defender_id,
        'roll_score':effective_score,'ca_exact':str(d.ca),'hit':hit,
        'defensive_reaction':defense_event.get('action') if defense_event else None,
        'defense_negated':negated,'raw':applied_raw if outcome else 0,
        'type':damage_tag,'rd_applied':outcome.applicable_rd if outcome else 0,
        'net':outcome.effective if outcome else 0,'before_hp':before,'after_hp':d.hp,
        'hp_loss_actual':before-d.hp,'overkill':max(0,(outcome.effective if outcome else 0)-before),
        'critical':critical,'critical_max_bonus':critical_maximum if advanced and (critical=='POSITIVE' or final_effort) else 0,
        'critical_sequence':list(critical_sequence) if critical_sequence else None,
        'damage_roll_groups':damage_roll_groups,'normal_damage':damage if advanced else None,
        'attack_roll_attempts':attack_roll_attempts,'weak_attacker':weak,
        'weak_target_before':before_weak,'weak_target_after':after_weak,
        'final_effort':final_effort,'immobile_next_turns':a.immobile_next_own_turns,
        'official_death_derived':False,'status':'LAB-STOP-HP0-NOT-CANON'})


def begin_source_turn(scene:Scene,actor_id:str):
    a=scene.actors[actor_id]
    if a.hp<=0:raise EffectBlocked('KO actor cannot take a turn')
    if a.standard==1:raise EffectBlocked('turn already available')
    a.standard=1;a.movement=1;a.reaction=1
    return scene.record({'action':'turn_start','by':actor_id,'weak':weak_status(a) if a.maximum_hp else 'UNKNOWN',
      'speed':str(effective_movement_speed(a)) if a.base_speed is not None and a.maximum_hp else 'UNKNOWN',
      'immobile':a.immobile_next_own_turns>0})


def end_source_turn(scene:Scene,actor_id:str):
    a=scene.actors[actor_id]
    if a.standard!=0:raise EffectBlocked('standard not spent; explicit pass required')
    pre=a.immobile_next_own_turns
    if pre:a.immobile_next_own_turns-=1
    return scene.record({'action':'turn_end','by':actor_id,'immobilization_before':pre,'immobilization_after':a.immobile_next_own_turns})

def react_defensively(scene:Scene,defender_id:str,*,kind:Literal['DEFENDER','ESQUIVAR'],
                       attack_score:int,announced_before:bool,trigger_source:str,
                       source:AbilitySource,state:ActorActionState,
                       proofs:tuple[FrozenRuleEvidence,...],strict:bool=True):
    defender=scene.actors[defender_id]
    if not announced_before:raise EffectBlocked('reaction must be declared BEFORE an attack')
    if defender.reaction!=1:raise EffectBlocked('reaction not available')
    if not trigger_source or source.reaction_trigger!=trigger_source:raise EffectBlocked('source trigger mismatch')
    if source.economy!='REACTION' or source.kind!='reaction':raise EffectBlocked('wrong reaction adapter')
    # Same ActionCatalog source proof and window gate as other actions.
    _require_option(scene,defender_id,source,state,proofs,phase='REACTION',strict=strict,target=defender_id)
    form=defender.form_overlay if defender.mode=='TRANSFORMED' else None
    if form is not None:
        # Do not silently use base defenses if the activated form did not publish them.
        if 'CA' not in form or 'CON' not in form or 'Fortitude' not in form or 'Reflexo' not in form or 'Armadura' not in form:
            raise EffectBlocked('transformed defense snapshot incomplete')
    ca=Fraction(form['CA']) if form is not None else defender.ca
    con=form['CON'] if form is not None else defender.constitution
    armor=form['Armadura'] if form is not None else defender.armor
    fort=form['Fortitude'] if form is not None else defender.fortitude
    reflex=form['Reflexo'] if form is not None else defender.reflex
    if kind=='DEFENDER':defense=6+con+armor+fort
    elif kind=='ESQUIVAR':defense=ca+reflex
    else:raise EffectBlocked('unresolved reaction kind')
    defender.reaction=0
    return scene.record({'action':kind,'by':defender_id,'attack_score':attack_score,
        'defense_exact':str(defense),'damage_negated':attack_score<=defense,
        'consumes_reaction':True,'source':trigger_source,
        'qualification':'DEFENDER: on success no damage; ESQUIVAR: evade hit on success'})


def move_via_verified_path(scene:Scene,actor_id:str,*,source:AbilitySource,state:ActorActionState,
                           proofs:tuple[FrozenRuleEvidence,...],destination:str,
                           path_evidence:str,travel_cost:Fraction,speed:Fraction,
                           strict:bool=True):
    a=scene.actors[actor_id]
    if a.movement!=1:raise EffectBlocked('movement spent')
    if source.kind!='move' or source.economy!='MOVEMENT':raise EffectBlocked('wrong move adapter')
    if not path_evidence or not destination:raise EffectBlocked('verified path and destination needed')
    if travel_cost<0 or speed<0 or travel_cost>speed:raise EffectBlocked('path beyond verified speed')
    if a.immobile_next_own_turns:raise EffectBlocked('final effort immobilized next turn')
    if a.maximum_hp is not None and a.base_speed is not None and speed>effective_movement_speed(a):raise EffectBlocked('speed exceeds weak/source speed')
    # Scenario must already have reviewed legal adjacency/terrain/line-of-sight;
    # do not invent a 5ft square or metric conversion.
    _require_option(scene,actor_id,source,state,proofs,strict=strict,target=None)
    before=a.position;a.position=destination;a.movement=0
    return scene.record({'action':'move','by':actor_id,'from':before,'to':destination,
        'path_proof':path_evidence,'travel_cost':str(travel_cost),'speed':str(speed)})

TRANS_COST={'Bronze':(20,'FULL','1d4',1),'Prata':(40,'FULL','1d6',1),
            'Ouro':(80,'STANDARD','1d8',1),'Ouro Negro':(160,'MOVEMENT','1d10',1),
            'Lendário':(320,'FREE','1d12',2)}

@dataclass(frozen=True)
class AssimilatedSpirit:
    spirit_source_id:str
    maximum_level:int
    bap_per_level:Fraction
    overlay_delta:dict[str,int]
    overlay_precomputed:dict
    provenance:str
    def __post_init__(self):
        if not self.spirit_source_id or self.provenance=='':raise EffectBlocked('source spirit missing')
        if not 1<=self.maximum_level<=25:raise EffectBlocked('invalid spirit cap')
        if self.bap_per_level<0:raise EffectBlocked('invalid BAP')
        if any(type(n)!=int or n<0 for n in self.overlay_delta.values()):raise EffectBlocked('invalid overlay')
        if set(self.overlay_delta)!={'FOR','DES','CON','INT','SAB','CAR'}:raise EffectBlocked('missing six attribute overlay')
        if not self.overlay_precomputed:raise EffectBlocked('transformation stats not precomputed')


def transformed_budget(ordinal_level:int,spirit:AssimilatedSpirit):
    lv=min(ordinal_level,spirit.maximum_level)
    raw=spirit.bap_per_level*lv/2
    return lv,raw.numerator//raw.denominator,raw-(raw.numerator//raw.denominator)


def activate_transformation(scene:Scene,actor_id:str,*,source:AbilitySource,
        state:ActorActionState,proofs:tuple[FrozenRuleEvidence,...],spirit:AssimilatedSpirit,
        ordinal_level:int,duration_die_roll:int,compatible:bool,strict:bool=True,
        full_reaction_policy:Literal['PENDING','LAB-CONSUME','LAB-PRESERVE']='PENDING'):
    actor=scene.actors[actor_id]
    if actor.spirit_id is None or actor.spirit_id!=spirit.spirit_source_id:raise EffectBlocked('spirit must actually be assimilated')
    if actor.mode!='NORMAL':raise EffectBlocked('already transformed')
    if actor.rank not in TRANS_COST:raise EffectBlocked('unknown rank')
    cost,economy,die,plus=TRANS_COST[actor.rank]
    if (source.kind,source.economy,source.required_pa)!=('transform',economy,cost):
        raise EffectBlocked('source ability/rank activation mismatch')
    if actor.pa is None or actor.pa<cost:raise EffectBlocked('not enough verified PA')
    from re import fullmatch
    face=int(die.partition('d')[2]);
    if type(duration_die_roll)!=int or not 1<=duration_die_roll<=face:raise EffectBlocked('duration die out of bounds')
    lv,points,carry=transformed_budget(ordinal_level,spirit)
    if sum(spirit.overlay_delta.values())!=points:raise EffectBlocked('TAP accumulated checksum violated')
    if economy=='FULL' and full_reaction_policy=='PENDING':
        raise EffectBlocked('FULL normally consumes reaction: specify approved policy or explicit LAB overlay')
    _require_option(scene,actor_id,source,state,proofs,strict=strict,target=actor_id)
    if economy=='FULL':
        if actor.standard!=1 or actor.movement!=1:raise EffectBlocked('full action not available')
    elif economy=='STANDARD' and actor.standard!=1:raise EffectBlocked('standard action spent')
    elif economy=='MOVEMENT' and actor.movement!=1:raise EffectBlocked('movement spent')
    elif economy=='FREE' and not state.free_action_contract_ready:raise EffectBlocked('free action not certified')
    # Commit everything only after all gates have passed.
    if economy=='FULL':
        actor.standard=0;actor.movement=0
        if full_reaction_policy=='LAB-CONSUME':actor.reaction=0
    elif economy=='STANDARD':actor.standard=0
    elif economy=='MOVEMENT':actor.movement=0
    actor.pa-=cost;actor.mode='TRANSFORMED';actor.form_overlay=deepcopy(spirit.overlay_precomputed)
    actor.transformation_remaining=duration_die_roll+plus+(1 if compatible else 0)
    return scene.record({'action':'transform','by':actor_id,'spirit_id':spirit.spirit_source_id,
      'effective_level':lv,'TAP':str(spirit.bap_per_level/2),'overlay_points':points,
      'carry':str(carry),'PA_spent':cost,'duration_roll':duration_die_roll,
      'duration_total':actor.transformation_remaining,'duration_unit':'turns',
      'rank':actor.rank,'mode':actor.mode,'full_reaction_policy':full_reaction_policy,
      'expiration_timing_resolver':'PENDING-CANON-SOURCE',
      'ff_marks_preserved':True,'state':'TRANSFORMED-FORM-SNAPSHOT-LOADED'})


def cast_source_specified_spell(scene:Scene,caster_id:str,target_id:str,*,source:AbilitySource,
                                state:ActorActionState,proofs:tuple[FrozenRuleEvidence,...],
                                damage:int,damage_tag:str,rd:Resistances,
                                explicit_save_effect:Literal['NO-SAVE','SAVE-FULL-NEGATE','SAVE-HALF']='NO-SAVE',
                                target_save_exceeds_cd:bool|None=None,strict:bool=True,
                                damage_rolls:tuple[int,...]|None=None,damage_faces:int|None=None):
    caster=scene.actors[caster_id];target=scene.actors[target_id]
    if source.kind!='spell':raise EffectBlocked('not a spell')
    if source.economy!='STANDARD':raise EffectBlocked('only default standard spell adapter supported')
    if source.required_pa<=0:raise EffectBlocked('spell PA cost source required for this adapter')
    if caster.pa is None or caster.pa<source.required_pa:raise EffectBlocked('PA unknown or low')
    if caster.standard!=1:raise EffectBlocked('action not available')
    _require_option(scene,caster_id,source,state,proofs,strict=strict,target=target_id)
    if explicit_save_effect!='NO-SAVE':
        if target_save_exceeds_cd is None:raise EffectBlocked('save outcome required')
        if explicit_save_effect=='SAVE-HALF' and target_save_exceeds_cd and damage%2:
            raise EffectBlocked('odd half damage rounding unresolved; no intent')
        if explicit_save_effect not in ('SAVE-FULL-NEGATE','SAVE-HALF'):raise EffectBlocked('unknown save effect')
    elif target_save_exceeds_cd is not None:raise EffectBlocked('cannot invent save')
    if damage_rolls is not None:
        if damage_faces is None or any(type(x)!=int or x<1 or x>damage_faces for x in damage_rolls) or sum(damage_rolls)!=damage:
            raise EffectBlocked('rolled damage does not match supplied dice')
    raw=0 if explicit_save_effect=='SAVE-FULL-NEGATE' and target_save_exceeds_cd else (damage//2 if explicit_save_effect=='SAVE-HALF' and target_save_exceeds_cd else damage)
    outcome=mitigate((DamageComponent(raw,damage_tag,source.action_id),),rd)
    before=target.hp
    caster.pa-=source.required_pa;caster.standard=0;target.hp=max(0,target.hp-outcome.effective)
    return scene.record({'action':'spell','by':caster_id,'target':target_id,'source_rule':source.rule_id,
      'save_effect':explicit_save_effect,'save_exceeds_cd':target_save_exceeds_cd,'damage_rolls':damage_rolls,'damage_faces':damage_faces,
      'critical':'NOT-APPLICABLE-BY-SISTEMA-DE-MAGIA','raw':raw,'damage_type':damage_tag,
      'rd_applied':outcome.applicable_rd,'effective':outcome.effective,
      'hp_before':before,'hp_after':target.hp,'PA_spent':source.required_pa,
      'death':'NOT-ADJUDICATED'})
