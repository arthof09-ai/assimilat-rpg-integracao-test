from pathlib import Path
p=Path(__file__).parent/'native_v081_controlled'/'vlab_effects_v08.py'
s=p.read_text()
s=s.replace("VERSION='COMBAT-EFFECT-ADAPTER-PARTIAL-v0.8'", "VERSION='COMBAT-EFFECT-ADAPTER-PARTIAL-v0.8+R108-R117-CONTROLLED'",1)
s=s.replace("    transformation_remaining:int|None=None\n", "    transformation_remaining:int|None=None\n    maximum_hp:int|None=None\n    base_speed:Fraction|None=None\n    beast_rank_index:int|None=None\n    final_effort_used:bool=False\n    immobile_next_own_turns:int=0\n",1)
s=s.replace("        if self.standard not in (0,1)","        if self.maximum_hp is not None and (self.maximum_hp<=0 or self.hp>self.maximum_hp):raise EffectBlocked('invalid maximum hp')\n        if self.immobile_next_own_turns<0:raise EffectBlocked('invalid immobilization')\n        if self.standard not in (0,1)",1)
start=s.index('def apply_weapon_attack(')
end=s.index('\ndef react_defensively(',start)
new='''def weak_status(actor:Combatant)->bool:
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
'''
s=s[:start]+new+s[end:]
needle="    if travel_cost<0 or speed<0 or travel_cost>speed:raise EffectBlocked('path beyond verified speed')"
s=s.replace(needle, needle+"\n    if a.immobile_next_own_turns:raise EffectBlocked('final effort immobilized next turn')\n    if a.maximum_hp is not None and a.base_speed is not None and speed>effective_movement_speed(a):raise EffectBlocked('speed exceeds weak/source speed')",1)
# Native SAVE-HALF documented rounding gate: even damage is mathematically integral.
s=s.replace("                                target_save_exceeds_cd:bool|None=None,strict:bool=True):", "                                target_save_exceeds_cd:bool|None=None,strict:bool=True,\n                                damage_rolls:tuple[int,...]|None=None,damage_faces:int|None=None):",1)
s=s.replace("        if explicit_save_effect=='SAVE-HALF':raise EffectBlocked('rounding of half damage needs source convention')", "        if explicit_save_effect=='SAVE-HALF' and target_save_exceeds_cd and damage%2:\n            raise EffectBlocked('odd half damage rounding unresolved; no intent')",1)
s=s.replace("        if explicit_save_effect!='SAVE-FULL-NEGATE':raise EffectBlocked('unknown save effect')", "        if explicit_save_effect not in ('SAVE-FULL-NEGATE','SAVE-HALF'):raise EffectBlocked('unknown save effect')",1)
s=s.replace("    raw=0 if explicit_save_effect=='SAVE-FULL-NEGATE' and target_save_exceeds_cd else damage", "    if damage_rolls is not None:\n        if damage_faces is None or any(type(x)!=int or x<1 or x>damage_faces for x in damage_rolls) or sum(damage_rolls)!=damage:\n            raise EffectBlocked('rolled damage does not match supplied dice')\n    raw=0 if explicit_save_effect=='SAVE-FULL-NEGATE' and target_save_exceeds_cd else (damage//2 if explicit_save_effect=='SAVE-HALF' and target_save_exceeds_cd else damage)",1)
s=s.replace("'save_exceeds_cd':target_save_exceeds_cd,", "'save_exceeds_cd':target_save_exceeds_cd,'damage_rolls':damage_rolls,'damage_faces':damage_faces,",1)
p.write_text(s)
print('patched',p, len(s))
