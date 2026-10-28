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

VERSION='COMBAT-EFFECT-ADAPTER-PARTIAL-v0.8+R126-POSITION-PA-REACTION-CONTROLLED'
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
    timed_source_speed_penalty_m:int=0  # R165 Flecha de Trava, source-scoped until end of target next turn
    cocoon_source_speed_penalty_m:int=0  # R166 Casulo 4m, expiry still HOLD
    def __post_init__(self):
        if self.hp<0 or (self.pa is not None and self.pa<0):raise EffectBlocked('invalid resources')
        if self.maximum_hp is not None and (self.maximum_hp<=0 or self.hp>self.maximum_hp):raise EffectBlocked('invalid maximum hp')
        if self.immobile_next_own_turns<0:raise EffectBlocked('invalid immobilization')
        if self.timed_source_speed_penalty_m<0 or self.cocoon_source_speed_penalty_m<0:raise EffectBlocked('invalid temporary speed penalty')
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
    speed=Fraction(actor.base_speed,2) if weak_status(actor) else Fraction(actor.base_speed)
    if actor.timed_source_speed_penalty_m:
        # Interplay with Fraco has not been normatively adjudicated: fail closed.
        if weak_status(actor):raise EffectBlocked('timed movement penalty combined with Fraco unresolved')
        speed-=actor.timed_source_speed_penalty_m
    if actor.cocoon_source_speed_penalty_m:
        if weak_status(actor):raise EffectBlocked('Casulo plus Fraco movement precedence unresolved')
        speed-=actor.cocoon_source_speed_penalty_m
    if speed<0:raise EffectBlocked('temporary penalty exceeds source speed')
    return speed


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
                        final_effort:bool=False,advantage_levels:int=0,disadvantage_levels:int=0,
                        attack_origin:str='NORMAL',lab_negative_critical_policy:bool=False,opportunity_intent_seq:int|None=None):
    """Historical v0.8.1 source-gated attack resolver with additive source-verified
    critical, weak and final-effort paths.  Legacy scalar calls remain supported
    solely for noncritical/non-weak historical regression; no official promotion.
    No new standalone damage engine is used; vlab_rd_v08.mitigate remains authority.
    """
    a=scene.actors[attacker_id];d=scene.actors[defender_id]
    if attack_origin not in ('NORMAL','OPPORTUNITY'):raise EffectBlocked('unverified attack origin')
    if attack_origin=='NORMAL':
        if a.standard!=1 or source.economy!='STANDARD':raise EffectBlocked('standard or source unavailable')
        phase='TURN'
    else:
        if source.economy!='REACTION' or source.reaction_trigger!='EXIT_ADJACENT':
            raise EffectBlocked('opportunity wrong source trigger')
        if opportunity_intent_seq is None:
            if a.reaction!=1:raise EffectBlocked('opportunity reaction unavailable')
        else:
            if a.reaction!=0:raise EffectBlocked('intent-reserved reaction must be zero')
            preceding=[v for v in scene.events if v.get('seq')==opportunity_intent_seq]
            if len(preceding)!=1:raise EffectBlocked('missing reaction intent evidence')
            intent=preceding[0]
            if (intent.get('action')!='opportunity_reaction_reserved' or intent.get('by')!=attacker_id
                or intent.get('to')!=defender_id or intent.get('source_id')!=source.action_id):
                raise EffectBlocked('reaction intent mismatch')
            if any(v.get('action')=='weapon_attack' and v.get('opportunity_intent_seq')==opportunity_intent_seq for v in scene.events):
                raise EffectBlocked('reaction intent already resolved')
            if any(v.get('action')=='turn_start' and v.get('by')==attacker_id for v in scene.events[opportunity_intent_seq:]):
                raise EffectBlocked('reaction intent expired at turn renewal')
        phase='REACTION'
    if source.kind!='attack':raise EffectBlocked('wrong attack adapter')
    if any(type(x)!=int or not 0<=x<=4 for x in (advantage_levels,disadvantage_levels)):
        raise EffectBlocked('advantage levels out of limits')
    if attack_origin=='OPPORTUNITY' and advantage_levels<1:raise EffectBlocked('AoO requires advantage')
    if not isinstance(roll_score,int) or isinstance(roll_score,bool) or roll_score<0:raise EffectBlocked('invalid roll')
    _require_option(scene,attacker_id,source,state,proofs,phase=phase,strict=strict,target=defender_id)
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
        if critical=='NEGATIVE' and not lab_negative_critical_policy:raise EffectBlocked('critical failure consequence unresolved; pre-intent rejection')
        if not attack_roll_attempts or any(len(t)==0 or any(type(x)!=int or not 1<=x<=6 for x in t) for t in attack_roll_attempts):
            raise EffectBlocked('invalid hit tape')
        net_adv=max(-4,min(4,advantage_levels-disadvantage_levels-(1 if weak else 0)))
        expected_attempts=1+abs(net_adv)
        if len(attack_roll_attempts)!=expected_attempts:raise EffectBlocked('advantage/weak tape count mismatch')
        scores=[sum(t)+attack_bonus for t in attack_roll_attempts]
        effective_score=(max(scores)+2*net_adv if net_adv>0 else
                         min(scores)+2*net_adv if net_adv<0 else scores[0])
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
        if defense_event.get('action') not in ('DEFENDER','ESQUIVAR','CAPA_POEIRA'):
            raise EffectBlocked('unresolved defense')
    negated=bool(defense_event.get('damage_negated')) if defense_event else False
    hit=(effective_score>d.ca or (advanced and critical=='POSITIVE')) and critical!='NEGATIVE'
    applied_raw=damage+(critical_maximum if advanced and (critical=='POSITIVE' or final_effort) and hit else 0)
    # This is the existing v0.8.1 RD module; no local alternative formula.
    outcome=mitigate((DamageComponent(applied_raw,damage_tag,source.action_id),),rd) if hit and not negated else None
    before=d.hp;before_weak=weak_status(d) if d.maximum_hp is not None else None
    if attack_origin=='NORMAL':a.standard=0
    elif opportunity_intent_seq is None:a.reaction=0
    else:
        # Already reserved by declare_opportunity_reaction; never debit twice.
        if a.reaction!=0:raise EffectBlocked('reserved reaction drift')
    if outcome:d.hp=max(0,d.hp-outcome.effective)
    if final_effort:
        a.final_effort_used=True
        a.immobile_next_own_turns=2
    after_weak=weak_status(d) if d.maximum_hp is not None else None
    return scene.record({'action':'weapon_attack','from':attacker_id,'to':defender_id,
        'roll_score':effective_score,'ca_exact':str(d.ca),'hit':hit,
        'attack_origin':attack_origin,'opportunity_intent_seq':opportunity_intent_seq,'advantage_levels':advantage_levels,
        'disadvantage_levels':disadvantage_levels,'net_levels':(max(-4,min(4,advantage_levels-disadvantage_levels-(1 if weak else 0))) if advanced else 0),
        'defensive_reaction':defense_event.get('action') if defense_event else None,
        'defense_negated':negated,'raw':applied_raw if outcome else 0,
        'type':damage_tag,'rd_applied':outcome.applicable_rd if outcome else 0,
        'net':outcome.effective if outcome else 0,'before_hp':before,'after_hp':d.hp,
        'hp_loss_actual':before-d.hp,'overkill':max(0,(outcome.effective if outcome else 0)-before),
        'critical':critical,'critical_failure_policy':('CRITICAL_FAILURE / VLAB-LAB-POLICY' if critical=='NEGATIVE' else None),'critical_max_bonus':critical_maximum if advanced and (critical=='POSITIVE' or final_effort) else 0,
        'critical_sequence':list(critical_sequence) if critical_sequence else None,
        'damage_roll_groups':damage_roll_groups,'normal_damage':damage if advanced else None,
        'attack_roll_attempts':attack_roll_attempts,'weak_attacker':weak,
        'weak_target_before':before_weak,'weak_target_after':after_weak,
        'final_effort':final_effort,'immobile_next_turns':a.immobile_next_own_turns,
        'official_death_derived':False,'status':'LAB-STOP-HP0-NOT-CANON'})



def declare_opportunity_reaction(scene:Scene,attacker_id:str,defender_id:str,*,source:AbilitySource,
       state:ActorActionState,proofs:tuple[FrozenRuleEvidence,...],fixture_adjacency_id:str):
    """R214 lab-only native extension: reserve a verified AoO before ANY offensive draw.
    No external SQLite side effect; the R18 event_commit publishes scene atomically.
    Not a counterattack, and not a campaign-level adjacency rule.
    """
    if (not fixture_adjacency_id or source.kind!='attack' or source.economy!='REACTION'
        or source.reaction_trigger!='EXIT_ADJACENT'):
        raise EffectBlocked('source-gated opportunity missing')
    if attacker_id==defender_id or attacker_id not in scene.actors or defender_id not in scene.actors:
        raise EffectBlocked('invalid AoO actors')
    attacker=scene.actors[attacker_id];target=scene.actors[defender_id]
    if attacker.hp<=0 or target.hp<=0 or attacker.reaction!=1:
        raise EffectBlocked('reaction or living target unavailable')
    _require_option(scene,attacker_id,source,state,proofs,phase='REACTION',strict=True,target=defender_id)
    # First logical change occurs in the same clone and precedes attack RNG generation.
    attacker.reaction=0
    return scene.record({'action':'opportunity_reaction_reserved','by':attacker_id,'to':defender_id,
          'source_id':source.action_id,'fixture_adjacency_id':fixture_adjacency_id,
          'reaction_before':1,'reaction_after':0,'before_offensive_rng':True})

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
                                damage_rolls:tuple[int,...]|None=None,damage_faces:int|None=None,documented_flat_bonus:int=0):
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
        if damage_faces is None or any(type(x)!=int or x<1 or x>damage_faces for x in damage_rolls) or type(documented_flat_bonus)!=int or documented_flat_bonus<0 or sum(damage_rolls)+documented_flat_bonus!=damage:
            raise EffectBlocked('rolled damage does not match supplied dice')
    raw=0 if explicit_save_effect=='SAVE-FULL-NEGATE' and target_save_exceeds_cd else (damage//2 if explicit_save_effect=='SAVE-HALF' and target_save_exceeds_cd else damage)
    outcome=mitigate((DamageComponent(raw,damage_tag,source.action_id),),rd)
    before=target.hp
    caster.pa-=source.required_pa;caster.standard=0;target.hp=max(0,target.hp-outcome.effective)
    return scene.record({'action':'spell','by':caster_id,'target':target_id,'source_rule':source.rule_id,
      'save_effect':explicit_save_effect,'save_exceeds_cd':target_save_exceeds_cd,'damage_rolls':damage_rolls,'damage_faces':damage_faces,'documented_flat_bonus':documented_flat_bonus,
      'critical':'NOT-APPLICABLE-BY-SISTEMA-DE-MAGIA','raw':raw,'damage_type':damage_tag,
      'rd_applied':outcome.applicable_rd,'effective':outcome.effective,
      'hp_before':before,'hp_after':target.hp,'PA_spent':source.required_pa,
      'death':'NOT-ADJUDICATED'})


# R118-R125 additive paths inside the historical v0.8.1 source module.
# R50: counter response ONLY on actual miss, not on zero-net critical hit.
# R51: counter response has origin COUNTER and never opens another counter window.
def declare_counterattack(scene:Scene,defender_id:str,attacker_id:str,*,source:AbilitySource,
                          state:ActorActionState,proofs:tuple[FrozenRuleEvidence,...],
                          declared_before:bool,attack_origin:str='NORMAL'):
    if attack_origin!='NORMAL':raise EffectBlocked('R51 counter-on-counter forbidden')
    if not declared_before:raise EffectBlocked('R50 declaration must precede attack resolution')
    if defender_id==attacker_id or defender_id not in scene.actors or attacker_id not in scene.actors:
        raise EffectBlocked('invalid counter actors')
    d=scene.actors[defender_id]
    if d.hp<=0 or d.reaction!=1:raise EffectBlocked('counter reaction slot unavailable')
    if source.kind!='reaction' or source.economy!='REACTION' or source.reaction_trigger!='ATTACK_DECLARED':
        raise EffectBlocked('counter source trigger mismatched')
    _require_option(scene,defender_id,source,state,proofs,phase='REACTION',strict=True,target=defender_id)
    d.reaction=0
    return scene.record({'action':'COUNTER_DECLARE','by':defender_id,'against':attacker_id,
         'consumes_reaction':True,'before_attack_resolution':True,'source':'MESTRE_R50_R51',
         'attack_origin':'NORMAL'})


def execute_declared_counterattack(scene:Scene,defender_id:str,attacker_id:str,*,
                                  declaration:dict,incoming:dict,attack_attempts:tuple[tuple[int,...],tuple[int,...]],
                                  attack_bonus:int,critical_sequence:tuple[int,int,int],
                                  damage_groups:tuple[tuple[int,int],...],
                                  damage_roll_groups:tuple[tuple[int,...],...],flat:int,
                                  damage_tag:str,rd:Resistances):
    """Only after R50 actual miss; R51 terminal reaction, no normal standard consumed.
    All dice and the source-gated declaration must be in SAME R18 transaction.
    """
    if declaration.get('action')!='COUNTER_DECLARE' or declaration.get('by')!=defender_id or declaration.get('against')!=attacker_id:
        raise EffectBlocked('counter lacks prior source-gated declaration')
    if incoming.get('action')!='weapon_attack' or incoming.get('from')!=attacker_id or incoming.get('to')!=defender_id:
        raise EffectBlocked('counter is not linked to incoming normal attack')
    if scene.actors[defender_id].reaction!=0:raise EffectBlocked('counter not consumed')
    if incoming.get('hit') is True:
        return scene.record({'action':'COUNTER_NO_RESPONSE','by':defender_id,'incoming_hit':True,
                'incoming_critical':incoming.get('critical'),'incoming_net':incoming.get('net'),
                'reaction_already_consumed':True,'R50':'HIT_MEANS_NO_RESPONSE'})
    if incoming.get('hit') is not False:raise EffectBlocked('unknown incoming hit')
    d=scene.actors[defender_id];a=scene.actors[attacker_id]
    if d.hp<=0 or a.hp<=0:raise EffectBlocked('counter requires living attacker/defender')
    if d.maximum_hp is None or weak_status(d):raise EffectBlocked('weak counter advantage/disadvantage interaction requires authority')
    if len(attack_attempts)!=2 or any(len(t)==0 or any(type(v)!=int or not 1<=v<=6 for v in t) for t in attack_attempts):
        raise EffectBlocked('advantage needs two authorized attack rolls')
    if len(critical_sequence)!=3 or any(type(v)!=int or not 1<=v<=6 for v in critical_sequence):
        raise EffectBlocked('invalid sequential critical tape')
    if critical_sequence[:2]==(1,1) and critical_sequence[2]<=2:
        raise EffectBlocked('negative critical consequence unresolved')
    if len(damage_groups)!=len(damage_roll_groups) or len(damage_groups)==0:
        raise EffectBlocked('counter damage groups unavailable')
    if any(type(n)!=int or type(f)!=int or n<=0 or f<2 or len(rolls)!=n or
           any(type(v)!=int or not 1<=v<=f for v in rolls)
           for (n,f),rolls in zip(damage_groups,damage_roll_groups)):
        raise EffectBlocked('counter damage dice invalid')
    critical=(critical_sequence[:2]==(6,6) and critical_sequence[2]>=5)
    score=max(map(sum,attack_attempts))+attack_bonus+2
    hit=score>a.ca or critical
    original=sum(sum(t) for t in damage_roll_groups)+flat
    bonus=sum(n*f for n,f in damage_groups) if critical else 0
    out=mitigate((DamageComponent(original+bonus,damage_tag,'R50-R51-SOURCE-COUNTER'),),rd) if hit else None
    before=a.hp
    if out:a.hp=max(0,a.hp-out.effective)
    return scene.record({'action':'COUNTER_RESPONSE','from':defender_id,'to':attacker_id,
         'attack_origin':'COUNTER','R51_nested_counter_enabled':False,
         'advantage_rolls':attack_attempts,'advantage_bonus':2,'attack_bonus':attack_bonus,
         'roll_score':score,'target_ca':str(a.ca),'hit':hit,'critical':'POSITIVE' if critical else 'NONE',
         'critical_sequence':critical_sequence,'normal_damage':original,'critical_bonus':bonus,
         'raw':original+bonus if hit else 0,'rd_applied':out.applicable_rd if out else 0,
         'net':out.effective if out else 0,'before_hp':before,'after_hp':a.hp,
         'overkill':max(0,(out.effective if out else 0)-before),
         'reaction_spent':True,'normal_standard_spent':False})


# R126 controlled extensions of source-gated existing v0.8.1 effects.
def apply_capa_poeira(scene:Scene,defender_id:str,attacker_id:str,*,source:AbilitySource,
                     state:ActorActionState,proofs:tuple[FrozenRuleEvidence,...],
                     attack_score:int,attack_kind:str='PHYSICAL'):
    d=scene.actors[defender_id]
    if attack_kind!='PHYSICAL':raise EffectBlocked('Capa applies only to physical attack')
    if d.hp<=0 or d.reaction!=1 or d.pa is None or d.pa<35:raise EffectBlocked('Capa PA or reaction unavailable')
    if source.kind!='reaction' or source.economy!='REACTION' or source.required_pa!=35 or source.reaction_trigger!='ATTACK_DECLARED':
        raise EffectBlocked('Capa source mismatch')
    _require_option(scene,defender_id,source,state,proofs,phase='REACTION',strict=True,target=defender_id)
    d.pa-=35;d.reaction=0
    return scene.record({'action':'CAPA_POEIRA','by':defender_id,'against':attacker_id,
        'source_page':source.source_page_id,'PA_spent':35,'consumes_reaction':True,
        'attack_score':attack_score,'adds_disadvantage':1,'damage_negated':False,
        'attack_kind':'PHYSICAL'})

def apply_marca_passos(scene:Scene,actor_id:str,target_id:str,*,source:AbilitySource,
                       state:ActorActionState,proofs:tuple[FrozenRuleEvidence,...],
                       range_met:bool,los_met:bool):
    a=scene.actors[actor_id]; t=scene.actors[target_id]
    if a.hp<=0 or t.hp<=0 or a.standard!=1 or a.pa is None or a.pa<25:
        raise EffectBlocked('Marca action/PA unavailable')
    if not range_met or not los_met:raise EffectBlocked('Marca must have visible target <=30m')
    if source.kind!='control' or source.economy!='STANDARD' or source.required_pa!=25:
        raise EffectBlocked('Marca source mismatch')
    _require_option(scene,actor_id,source,state,proofs,strict=True,target=target_id)
    a.pa-=25;a.standard=0
    return scene.record({'action':'MARCA_PASSOS_PERDIDOS','by':actor_id,'to':target_id,
        'source_page':source.source_page_id,'PA_spent':25,'duration_own_turns':3,
        'bonus_only':'PERCEPCAO_E_SOBREVIVENCIA_+10','attack_bonus_granted':0,
        'target_visible_within_30m':True})

def apply_reconstituicao_seiva(scene:Scene,actor_id:str,target_id:str,*,source:AbilitySource,
        state:ActorActionState,proofs:tuple[FrozenRuleEvidence,...],
        dice_rolls:tuple[int,...],range_met:bool,gloves_equipped:bool,heal_blocked:bool=False):
    """R130 Eristan documented direct heal. Native v0.8.1 source/action/resolver extension.
    8d10+25 direct healing; equipped Gloves +20 ONCE per successful direct cast.
    Does not erase wounds, revive dead, or import any rule for bleeding status.
    """
    caster=scene.actors[actor_id];target=scene.actors[target_id]
    if source.kind!='heal' or source.economy!='STANDARD' or source.required_pa!=75 or source.target_scope!='ALLY':
        raise EffectBlocked('Eristan heal source mismatch')
    if not range_met:raise EffectBlocked('Eristan healing range >5m or unverifiable')
    if heal_blocked:raise EffectBlocked('source wound prohibits magical healing')
    if caster.hp<=0 or target.hp<=0 or target.maximum_hp is None or target.hp>=target.maximum_hp:
        raise EffectBlocked('target dead/full or maximum HP unknown')
    if caster.standard!=1 or caster.pa is None or caster.pa<75:raise EffectBlocked('insufficient healing action or PA')
    if len(dice_rolls)!=8 or any(type(x)!=int or not 1<=x<=10 for x in dice_rolls):
        raise EffectBlocked('8d10 heal dice required')
    _require_option(scene,actor_id,source,state,proofs,strict=True,target=target_id)
    value=sum(dice_rolls)+25;item_extra=20 if gloves_equipped else 0
    before=target.hp;actual=min(target.maximum_hp-before,value+item_extra)
    target.hp+=actual;caster.pa-=75;caster.standard=0
    return scene.record({'action':'RECONSTITUICAO_SEIVA','by':actor_id,'to':target_id,
       'healing_rolls':list(dice_rolls),'healing_source':source.source_page_id,
       'base_heal':value,'equipped_gloves_bonus':item_extra,'gross_heal':value+item_extra,
       'hp_before':before,'hp_after':target.hp,'hp_max':target.maximum_hp,
       'actual_healed':actual,'excess_heal':value+item_extra-actual,'PA_spent':75,
       'standard_consumed':1,'target_resurrected':False,'bleeding_removed':False})

# R138 controlled additive source-bound extension: existing v0.8.1 catalog / Scene.
def apply_passo_fuligem(scene:Scene,actor_id:str,*,source:AbilitySource,
                      state:ActorActionState,proofs:tuple[FrozenRuleEvidence,...]):
    a=scene.actors[actor_id]
    if (source.kind!='move' or source.economy!='MOVEMENT' or source.required_pa!=25
        or source.target_scope!='SELF'):raise EffectBlocked('Passo source shape')
    if a.hp<=0 or a.movement!=1 or a.pa is None or a.pa<25:raise EffectBlocked('Passo unavailable')
    _require_option(scene,actor_id,source,state,proofs,strict=True,target=actor_id)
    a.pa-=25;a.movement=0
    return scene.record({'action':'PASSO_FULIGEM','by':actor_id,'PA_spent':25,
       'movement_action_consumed':1,'speed_bonus_m':12,'duration':'ESTE_TURNO',
       'source_page':source.source_page_id})


def apply_pulso_estabilizacao(scene:Scene,caster_id:str,target_id:str,*,source:AbilitySource,
                   state:ActorActionState,proofs:tuple[FrozenRuleEvidence,...],
                   dice_rolls:tuple[int,...],range_met:bool,damage_just_resolved:bool,
                   gloves_equipped:bool):
    c=scene.actors[caster_id];t=scene.actors[target_id]
    if (source.kind!='heal' or source.economy!='REACTION' or source.required_pa!=45
        or source.target_scope!='ALLY' or source.reaction_trigger!='ALLY_AFTER_DAMAGE'):
        raise EffectBlocked('Pulso source shape')
    if not range_met or not damage_just_resolved:raise EffectBlocked('Pulso missing trigger or range')
    if (c.hp<=0 or t.hp<=0 or t.maximum_hp is None or t.hp>=t.maximum_hp
        or c.reaction!=1 or c.pa is None or c.pa<45):raise EffectBlocked('Pulso resources or target')
    if len(dice_rolls)!=3 or any(type(x)!=int or not 1<=x<=10 for x in dice_rolls):
        raise EffectBlocked('Pulso 3d10 evidence')
    _require_option(scene,caster_id,source,state,proofs,phase='REACTION',strict=True,target=target_id)
    gross=sum(dice_rolls)+10+(20 if gloves_equipped else 0)
    before=t.hp;healed=min(t.maximum_hp-before,gross)
    t.hp+=healed;c.pa-=45;c.reaction=0
    return scene.record({'action':'PULSO_ESTABILIZACAO','by':caster_id,'to':target_id,
       'PA_spent':45,'reaction_consumed':1,'healing_rolls':list(dice_rolls),
       'source_base':sum(dice_rolls)+10,'gloves_bonus':20 if gloves_equipped else 0,
       'gross_heal':gross,'actual_heal':healed,'excess_heal':gross-healed,
       'before_hp':before,'after_hp':t.hp,'target_resurrected':False,
       'bleeding_removed':False,'source_page':source.source_page_id})

# R153 additive source-bound native support. Two-turn exact expiry is NOT assigned.
def apply_casulo_brotos(scene:Scene,caster_id:str,target_id:str,*,source:AbilitySource,
      state:ActorActionState,proofs:tuple[FrozenRuleEvidence,...],range_m:int,
      same_caster_effect_active:bool=False):
    a=scene.actors[caster_id];t=scene.actors[target_id]
    if source.kind!='control' or source.economy!='STANDARD' or source.required_pa!=60 or source.target_scope!='ALLY':
        raise EffectBlocked('Casulo source type and action mismatch')
    if a.hp<=0 or t.hp<=0 or a.standard!=1 or a.pa is None or a.pa<60:
        raise EffectBlocked('Casulo action or PA unavailable')
    if same_caster_effect_active:raise EffectBlocked('same caster Casulo cannot stack')
    if type(range_m)!=int or not 0<=range_m<=15:raise EffectBlocked('Casulo 15m range')
    _require_option(scene,caster_id,source,state,proofs,target=target_id)
    before_ca=t.ca
    t.ca+=22;t.cocoon_source_speed_penalty_m+=4;a.standard=0;a.pa-=60
    return scene.record({'action':'CASULO_BROTOS','by':caster_id,'to':target_id,'PA_spent':60,
        'standard_spent':1,'range_m':range_m,'ca_before':str(before_ca),'ca_after':str(t.ca),
        'CA_delta':22,'movement_delta_m':-4,'duration_literal':'2 TURNOS',
        'expiration_boundary':'HOLD_SOURCE_NOT_DEFINED','same_caster_nonstack':True,
        'source_page':source.source_page_id})


# R165 additive time-bounded source effect: Iskiel Flecha de Trava (end of target NEXT turn).
def apply_flecha_trava_post_hit(scene:Scene,attacker_id:str,target_id:str,attack_receipt:dict,*,source_page:str,cost_pa:int=55):
    """Call inside the SAME R18 reducer as a legitimately resolved, source-gated physical attack.
    Standard already consumed by apply_weapon_attack. Only this verified technique can apply -6m.
    """
    a=scene.actors[attacker_id];t=scene.actors[target_id]
    if source_page!='3f6c2b324ede81a78a59d3d81fd5e966' or cost_pa!=55:
        raise EffectBlocked('not Iskiel Flecha de Trava 55PA source')
    if attack_receipt.get('action')!='weapon_attack' or attack_receipt.get('from')!=attacker_id or attack_receipt.get('to')!=target_id:
        raise EffectBlocked('receipt and actor mismatch')
    if a.pa is None or a.pa<55:raise EffectBlocked('PA unavailable')
    if a.standard!=0:raise EffectBlocked('physical attack standard not already consumed')
    if t.timed_source_speed_penalty_m:raise EffectBlocked('duplicate/stack precedence not documented')
    a.pa-=55
    applied=bool(attack_receipt['hit'] and attack_receipt['after_hp']>0)
    if applied:t.timed_source_speed_penalty_m=6
    return scene.record({'action':'FLECHA_TRAVA_SOURCE_POST_HIT','by':attacker_id,'to':target_id,
      'pa_spent':55,'slow_applied':applied,'speed_delta_m':-6 if applied else 0,
      'duration_until':'END_OF_TARGET_NEXT_OWN_TURN','source_page':source_page,
      'same_caster_stack':'HOLD_REJECT'})

def expire_flecha_trava_next_turn(scene:Scene,target_id:str):
    t=scene.actors[target_id]
    if t.timed_source_speed_penalty_m!=6:raise EffectBlocked('no matching source-gated temporal status')
    before=str(effective_movement_speed(t));t.timed_source_speed_penalty_m=0
    after=str(effective_movement_speed(t))
    return scene.record({'action':'FLECHA_TRAVA_EXPIRES','by':target_id,
        'source':'Iskiel Flecha de Trava','boundary':'END_OF_TARGET_NEXT_OWN_TURN',
        'speed_before':before,'speed_after':after,'modifiers_removed':-6})
