"""Experimental v0.9+ manual-turn runtime, reconstructed on authentic v0.8.1.

NOT a reproduction of the unavailable v0.9 binary, an automatic scheduler, or
an approved battle engine. Every action is a closed LAB fixture; STRICT denies.
All source/effect mutations are staged on copies and committed together only
when catalog, effect and ledger all pass. Log hashes detect accidental changes,
not a cryptographic proof of canonical authenticity.
"""
from __future__ import annotations
from copy import deepcopy
from dataclasses import asdict
from hashlib import sha256
import json
from fractions import Fraction
from vlab_action_catalog_v01 import AbilitySource,ActorActionState,FrozenRuleEvidence,action_menu
from vlab_action_catalog_v09plus_rebuilt import compile_legal_actions,transformation_readiness
from vlab_effects_v08 import (Scene,EffectBlocked,apply_weapon_attack,
                              cast_source_specified_spell,move_via_verified_path,react_defensively)
from vlab_effects_v09_rebuilt import activate_transformation_v09_rebuilt,expire_transformation_v09_rebuilt
from vlab_transformation_limit_v09_rebuilt import TransformationUseLedger,SceneLockError
from independent_resource_gate_v09plus import ResourceEvidence,ResourceDenied,reserve_item_or_pa

VERSION='DOCUMENTARY-V09PLUS-MANUAL-SOURCE-EFFECT-ATOMIC-LAB'
class RuntimeBlocked(ValueError):pass


def _json(x):
    return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'),default=str)


def _sha(payload):
    return sha256(_json(payload).encode('utf-8')).hexdigest()


class RebuiltManualRuntime:
    def __init__(self,*,scene:Scene,ledger:TransformationUseLedger|None,scene_id:str,
                 test_fixture_authorized:bool=False,item_charges:dict[str,int]|None=None):
        if test_fixture_authorized is not True:raise RuntimeBlocked('LAB_FIXTURE_AUTHORIZATION_REQUIRED')
        if not isinstance(scene,Scene) or not isinstance(ledger,TransformationUseLedger):
            raise RuntimeBlocked('SCENE_AND_PERSISTED_LEDGER_REQUIRED')
        if not isinstance(scene_id,str) or not scene_id.strip():raise RuntimeBlocked('SCENE_ID_REQUIRED')
        if scene.provenance!='LAB-TEST-SYNTHETIC-NONCANON':
            raise RuntimeBlocked('NONCANONICAL_SCENE_ONLY')
        self.scene=scene;self.ledger=ledger;self.scene_id=scene_id;self.trace=[]
        self.catalogue_version=VERSION
        self.item_charges=deepcopy(item_charges if item_charges is not None else {})
        if not isinstance(self.item_charges,dict) or any(
                not isinstance(k,str) or not k or type(v)!=int or v<0 for k,v in self.item_charges.items()):
            raise RuntimeBlocked('BAD_FIXTURE_ITEM_CHARGES')
        self._charges_anchor=_sha(self.item_charges)

    def _preflight(self,actor_id:str,state:ActorActionState):
        if actor_id not in self.scene.actors or state.actor_id!=actor_id:
            raise RuntimeBlocked('ACTOR_BINDING_MISMATCH')
        actor=self.scene.actors[actor_id]
        # A stale AI-provided state must not bypass actual PA or spent budgets.
        if (state.available_pa!=actor.pa or state.standard_available!=(actor.standard==1)
            or state.movement_available!=(actor.movement==1) or state.reaction_available!=(actor.reaction==1)):
            raise RuntimeBlocked('CATALOG_ACTOR_STATE_STALE')
        if actor_id not in self.ledger.actors:raise RuntimeBlocked('ACTOR_LEDGER_NOT_PERSISTED')
        return actor

    def _append_trace_on_clone(self,kind,actor_id,_,candidate,ledger_clone,*,extra,staged_charges=None):
        before=self.trace[-1]['chain_hash'] if self.trace else None
        ev={'index':len(self.trace)+1,'kind':kind,'actor_id':actor_id,'scene_id':self.scene_id,
            'previous_chain_hash':before,'effect_event':deepcopy(_),'scene_events_sha256':candidate.checksum(),
            'actor_state_sha256':_sha({a:asdict(x) for a,x in sorted(candidate.actors.items())}),
            'ledger_snapshot_sha256':ledger_clone.snapshot()['sha256'],
            'item_charges_sha256':_sha(self.item_charges if staged_charges is None else staged_charges),
            'qualification':VERSION,'source_mode':'LAB-ASSUMPTION-ONLY',**extra}
        ev['chain_hash']=_sha(ev)
        return ev

    def _commit(self,candidate:Scene,staged_ledger:TransformationUseLedger,event:dict,staged_charges=None):
        if set(candidate.actors)!=set(self.scene.actors):raise RuntimeBlocked('ACTOR_SET_CHANGED')
        if not self.validate_trace():raise RuntimeBlocked('TRACE_TAMPERED_OR_MALFORMED')
        # No side effects until all checks have succeeded. Keep actor references.
        # The state is a LAB fixture and never injected into official RPG records.
        for actor_id in self.scene.actors:
            self.scene.actors[actor_id].__dict__.update(deepcopy(candidate.actors[actor_id].__dict__))
        self.scene.events[:]=deepcopy(candidate.events)
        self.ledger.actors=deepcopy(staged_ledger.actors)
        self.ledger.used_rests=set(staged_ledger.used_rests)
        self.ledger.events=deepcopy(staged_ledger.events)
        if staged_charges is not None:
            self.item_charges=deepcopy(staged_charges)
        self._charges_anchor=_sha(self.item_charges)
        self.trace.append(event)

    def validate_trace(self):
        if _sha(self.item_charges)!=self._charges_anchor:return False
        previous=None
        for seq,row in enumerate(self.trace,1):
            if row.get('index')!=seq or row.get('previous_chain_hash')!=previous:return False
            if not isinstance(row.get('chain_hash'),str) or row['chain_hash']!=_sha({k:v for k,v in row.items() if k!='chain_hash'}):return False
            previous=row['chain_hash']
        if self.trace:
            tail=self.trace[-1]
            if tail.get('scene_events_sha256')!=self.scene.checksum():return False
            if tail.get('actor_state_sha256')!=_sha({a:asdict(x) for a,x in sorted(self.scene.actors.items())}):return False
            if tail.get('ledger_snapshot_sha256')!=self.ledger.snapshot()['sha256']:return False
            if tail.get('item_charges_sha256')!=_sha(self.item_charges):return False
        return True

    def compile(self,*,actor_id:str,state:ActorActionState,sources:tuple[AbilitySource,...],
                proofs:tuple[FrozenRuleEvidence,...]=(),strict=False):
        if strict:raise RuntimeBlocked('STRICT_AUDITED_SOURCES_AND_NAC_PASS_NOT_AVAILABLE')
        self._preflight(actor_id,state)
        if any(s.source_status!='LAB-ASSUMPTION' for s in sources):
            raise RuntimeBlocked('REQUIRE_EXPLICIT_LAB_SOURCE_QUALIFICATION')
        return compile_legal_actions(actor=state,sources=sources,ledger=self.ledger,scene_id=self.scene_id,
                                     strict=False,source_evidence=proofs)

    def execute_turn(self,*,actor_id:str,action_id:str,sources:tuple[AbilitySource,...],
                     state:ActorActionState,proofs:tuple[FrozenRuleEvidence,...]=(),
                     payload:dict|None=None,manual_turn_start=False,strict=True,
                     resource_evidence:ResourceEvidence|None=None):
        if strict:raise RuntimeBlocked('STRICT_SOURCE_FROZEN_BATTLE_ENGINE_NOT_APPROVED')
        if manual_turn_start is not True:raise RuntimeBlocked('EXTERNAL_TURN_START_REQUIRED')
        if not isinstance(payload,dict):raise RuntimeBlocked('EXACT_EFFECT_PAYLOAD_REQUIRED')
        if not self.validate_trace():raise RuntimeBlocked('TRACE_TAMPERED')
        catalog,readiness=self.compile(actor_id=actor_id,state=state,sources=sources,proofs=proofs,strict=False)
        options=[o for o in catalog.legal_options if o.action_id==action_id]
        if len(options)!=1:raise RuntimeBlocked('ACTION_NOT_IN_SOURCE_GATED_OPTIONS:'+str(catalog.rejected))
        spec=next((s for s in sources if o_key(s,options[0])==action_id),None)
        if spec is None:raise RuntimeBlocked('SOURCE_OPTION_BINDING_FAILED')
        if not spec.effect_adapter_ready:raise RuntimeBlocked('EFFECT_ADAPTER_NOT_READY')
        if not any(p.source_page_id==spec.source_page_id and p.rule_id==spec.rule_id
                   and p.audit_record_id.startswith(('MOCK-','LAB-')) for p in proofs):
            raise RuntimeBlocked('LAB_SOURCE_PROOF_POINTER_REQUIRED')
        if not isinstance(spec.effect_adapter_id,str) or not spec.effect_adapter_id.startswith('LAB-'):
            raise RuntimeBlocked('UNTRUSTED_EFFECT_ADAPTER_ID')
        reservation=None
        if resource_evidence is None and spec.effect_adapter_id=='LAB-ITEM-GRANTED':
            raise RuntimeBlocked('ITEM_RESOURCE_LINK_MANDATORY')
        if resource_evidence is not None:
            try:
                reservation=reserve_item_or_pa(evidence=resource_evidence,
                    actor_id=actor_id,action_id=spec.action_id,
                    source_page_id=spec.source_page_id,
                    source_cost=spec.required_pa,source_slot=spec.economy,
                    actor_pa=self.scene.actors[actor_id].pa,
                    reaction_available=self.scene.actors[actor_id].reaction==1,
                    charges=self.item_charges,strict=False)
            except ResourceDenied as exc:
                raise RuntimeBlocked('INDEPENDENT_RESOURCE_GATE_DENIED:'+str(exc)) from exc
        staged_scene=deepcopy(self.scene)
        staged_ledger=TransformationUseLedger.restore(self.ledger.snapshot())
        staged_charges=(deepcopy(self.item_charges) if reservation is None
                        else deepcopy(reservation['charges_after']))
        pa_before=self.scene.actors[actor_id].pa
        try:
            if spec.kind=='transform':
                require_keys(payload,{'spirit','ordinal_level','duration_die_roll','compatible','full_reaction_policy'})
                event=activate_transformation_v09_rebuilt(staged_scene,actor_id,scene_id=self.scene_id,
                      ledger=staged_ledger,strict=False,source=spec,state=state,proofs=proofs,**payload)
            elif spec.kind=='attack':
                require_keys(payload,{'roll_score','damage','damage_tag','rd'})
                if spec.economy!='STANDARD':raise RuntimeBlocked('ATTACK_ADAPTER_ECONOMY_UNSUPPORTED')
                target=options[0].target_id
                if target is None:raise RuntimeBlocked('ATTACK_TARGET_REQUIRED')
                event=apply_weapon_attack(staged_scene,actor_id,target,source=spec,state=state,
                    proofs=proofs,strict=False,defense_event=None,**payload)
            elif spec.kind=='spell':
                require_keys(payload,{'damage','damage_tag','rd','explicit_save_effect','target_save_exceeds_cd','mock_spell_fixture'})
                if payload['mock_spell_fixture'] is not True:raise RuntimeBlocked('NO_REAL_SPELL_SOURCE_FROZEN')
                target=options[0].target_id
                if target is None:raise RuntimeBlocked('SPELL_TARGET_REQUIRED')
                spell_kw={k:v for k,v in payload.items() if k!='mock_spell_fixture'}
                event=cast_source_specified_spell(staged_scene,actor_id,target,source=spec,state=state,
                    proofs=proofs,strict=False,**spell_kw)
                event['mock_spell_fixture']=True
            elif spec.kind=='move':
                require_keys(payload,{'destination','path_evidence','travel_cost','speed'})
                if options[0].target_id is not None:raise RuntimeBlocked('POSITION_ONLY')
                event=move_via_verified_path(staged_scene,actor_id,source=spec,state=state,
                    proofs=proofs,strict=False,**payload)
            else:raise RuntimeBlocked('EFFECT_KIND_UNSUPPORTED_AND_NOT_RECONSTRUCTED')
        except (EffectBlocked,SceneLockError,KeyError,TypeError,ValueError) as ex:
            raise RuntimeBlocked('SOURCE_EFFECT_REJECTED:'+str(ex)) from ex
        if reservation is not None and (pa_before is None or
                pa_before-staged_scene.actors[actor_id].pa!=reservation['known_pa_cost_sum']):
            raise RuntimeBlocked('RESOURCE_PA_SPEND_MISMATCH_WITH_HISTORIC_EXECUTOR')
        event2=self._append_trace_on_clone(spec.kind.upper(),actor_id,event,staged_scene,staged_ledger,
                   extra={'source_rule':spec.rule_id,'action_id':action_id,'transform_readiness':readiness.status,
                          'mock_effect':spec.kind=='spell','canonical_credit':0,
                          'resource_mode':'EXPLICIT_UNIT_FIXTURE' if reservation is not None else 'NO_ITEM_RESERVATION',
                          'reservation_sha256':reservation['plan_sha256'] if reservation else None,
                          'item_fixture_id':resource_evidence.item_id if resource_evidence else None},
                   staged_charges=staged_charges)
        self._commit(staged_scene,staged_ledger,event2,staged_charges=staged_charges)
        return deepcopy(event2)


    def execute_attack_with_defense(self,*,attacker_id:str,defender_id:str,
            attack_source:AbilitySource,defense_source:AbilitySource,
            attack_state:ActorActionState,defense_state:ActorActionState,
            attack_proofs:tuple[FrozenRuleEvidence,...],defense_proofs:tuple[FrozenRuleEvidence,...],
            attack_payload:dict,defense_kind:str,announced_before:bool,
            trigger_source:str,strict=True,
            attack_resource_evidence:ResourceEvidence|None=None,
            defense_resource_evidence:ResourceEvidence|None=None):
        """Cycle 1: two original v0.8.1 effect resolvers, ONE atomic transaction.

        Defender/Esquivar execute in BEFORE_ATTACK window, then immediately
        resolve the specific incoming attack in the SAME scene clone. Any gate
        failure discards both provisional effects. No reaction scheduler is
        inferred; this is an explicitly ordered single LAB fixture.
        """
        if strict:raise RuntimeBlocked('STRICT_REACTION_SOURCE_NAC_PASS_HOLD')
        if not self.validate_trace():raise RuntimeBlocked('TRACE_TAMPERED')
        if attacker_id==defender_id or defender_id not in self.scene.actors:
            raise RuntimeBlocked('DISTINCT_KNOWN_DEFENDER_REQUIRED')
        if not isinstance(attack_payload,dict):raise RuntimeBlocked('ATTACK_PAYLOAD_REQUIRED')
        require_keys(attack_payload,{'roll_score','damage','damage_tag','rd'})
        if announced_before is not True or trigger_source!='BEFORE-ATTACK':
            raise RuntimeBlocked('BEFORE_ATTACK_DECLARATION_REQUIRED')
        if defense_kind not in ('DEFENDER','ESQUIVAR'):
            raise RuntimeBlocked('DEFENDER_OR_ESQUIVAR_ONLY')
        if attack_source.kind!='attack' or attack_source.economy!='STANDARD':
            raise RuntimeBlocked('SOURCE_ATTACK_ADAPTER_REQUIRED')
        if (defense_source.kind!='reaction' or defense_source.economy!='REACTION'
                or defense_source.reaction_trigger!='BEFORE-ATTACK'
                or defense_source.target_scope!='SELF'):
            raise RuntimeBlocked('SOURCE_DEFENSIVE_REACTION_REQUIRED')
        if (attack_source.source_status!='LAB-ASSUMPTION' or
                defense_source.source_status!='LAB-ASSUMPTION'):
            raise RuntimeBlocked('LAB_ONLY_SOURCE_STATUS')
        for spec,proofs in ((attack_source,attack_proofs),(defense_source,defense_proofs)):
            if not spec.effect_adapter_ready or not isinstance(spec.effect_adapter_id,str) or not spec.effect_adapter_id.startswith('LAB-'):
                raise RuntimeBlocked('SOURCE_EFFECT_ADAPTER_NOT_AUTHORIZED')
            if not any(p.source_page_id==spec.source_page_id and p.rule_id==spec.rule_id
                       and p.audit_record_id.startswith(('MOCK-','LAB-')) for p in proofs):
                raise RuntimeBlocked('LAB_RULE_SOURCE_PROOF_REQUIRED')
        self._preflight(attacker_id,attack_state)
        self._preflight(defender_id,defense_state)
        if defense_state.reaction_trigger_observed!='BEFORE-ATTACK':
            raise RuntimeBlocked('OBSERVED_REACTION_TRIGGER_REQUIRED')
        if attacker_id not in defense_state.enemy_ids_visible:
            raise RuntimeBlocked('DEFENDER_INCOMING_ATTACKER_NOT_VISIBLE')
        if defender_id not in attack_state.enemy_ids_visible:
            raise RuntimeBlocked('ATTACK_TARGET_NOT_VISIBLE')
        catalog,_=self.compile(actor_id=attacker_id,state=attack_state,
                  sources=(attack_source,),proofs=attack_proofs,strict=False)
        if len([o for o in catalog.legal_options if o.action_id==attack_source.action_id+':'+defender_id])!=1:
            raise RuntimeBlocked('ATTACK_SOURCE_MENU_DENIED')
        dc=action_menu(defense_state,(defense_source,),phase='REACTION',strict=False,
                       source_evidence=defense_proofs)
        if len([o for o in dc.legal_options if o.action_id==defense_source.action_id+':'+defender_id])!=1:
            raise RuntimeBlocked('REACTION_SOURCE_MENU_DENIED:'+str(dc.rejected))
        # Cycle 3: link BOTH action reservations to this very same clone.
        # Independent turn_planner must approve PA/equip/charges before either
        # historic effect resolver is called. STRICT is always unavailable.
        stage_charges=deepcopy(self.item_charges)
        reservations=[]
        for spec,actor,evidence,slot_window in (
            (attack_source,attacker_id,attack_resource_evidence,None),
            (defense_source,defender_id,defense_resource_evidence,'BEFORE-ATTACK')):
            if evidence is None and spec.effect_adapter_id=='LAB-ITEM-GRANTED':
                raise RuntimeBlocked('ITEM_RESOURCE_LINK_MANDATORY:'+spec.action_id)
            if evidence is not None:
                try:
                    reservation=reserve_item_or_pa(evidence=evidence,actor_id=actor,
                        action_id=spec.action_id,source_page_id=spec.source_page_id,
                        source_cost=spec.required_pa,source_slot=spec.economy,
                        actor_pa=self.scene.actors[actor].pa,
                        reaction_available=self.scene.actors[actor].reaction==1,
                        charges=stage_charges,strict=False,reaction_window=slot_window)
                except ResourceDenied as exc:
                    raise RuntimeBlocked('ATOMIC_INDEPENDENT_RESOURCE_DENIED:'+str(exc)) from exc
                stage_charges=deepcopy(reservation['charges_after'])
                reservations.append((actor,reservation))
        staged_scene=deepcopy(self.scene)
        staged_ledger=TransformationUseLedger.restore(self.ledger.snapshot())
        try:
            reaction_event=react_defensively(staged_scene,defender_id,kind=defense_kind,
                attack_score=attack_payload['roll_score'],announced_before=True,
                trigger_source=trigger_source,source=defense_source,
                state=defense_state,proofs=defense_proofs,strict=False)
            attack_event=apply_weapon_attack(staged_scene,attacker_id,defender_id,
                source=attack_source,state=attack_state,proofs=attack_proofs,
                defense_event=reaction_event,strict=False,**attack_payload)
        except (EffectBlocked,SceneLockError,KeyError,TypeError,ValueError) as exc:
            raise RuntimeBlocked('ATOMIC_DEFENSE_AND_ATTACK_DENIED:'+str(exc)) from exc
        for actor,reservation in reservations:
            before_pa=self.scene.actors[actor].pa
            after_pa=staged_scene.actors[actor].pa
            if before_pa is None or after_pa is None or before_pa-after_pa!=reservation['known_pa_cost_sum']:
                raise RuntimeBlocked('RESOURCE_PA_SPEND_MISMATCH_WITH_HISTORIC_REACTION_ATTACK')
        event={'reaction':reaction_event,'attack':attack_event,
               'reaction_declared':'BEFORE-ATTACK','reaction_slot_spent_once':True,
               'resource_reservations':[r['plan_sha256'] for _,r in reservations],
               'first_attack_after_reaction':True}
        row=self._append_trace_on_clone('ATOMIC_REACTION_ATTACK',attacker_id,event,staged_scene,staged_ledger,
                extra={'defender_id':defender_id,'defense_kind':defense_kind,
                       'attack_action_id':attack_source.action_id,'defense_action_id':defense_source.action_id,
                       'canonical_credit':0,'mock_effect':False,
                       'resource_mode':'EXPLICIT_UNIT_FIXTURE' if reservations else 'NO_ITEM_RESERVATION',
                       'item_fixture_ids':[e.item_id for e in (attack_resource_evidence,defense_resource_evidence) if e is not None]},
                staged_charges=stage_charges)
        self._commit(staged_scene,staged_ledger,row,staged_charges=stage_charges)
        return deepcopy(row)

    def manual_turn_budget_reset(self,*,actor_id:str,turn_id:str,external_authority_ref:str,
                                 standard:int,movement:int,reaction:int,strict=True):
        """Manual external turn boundary, not an initiative calculation.

        All budgets must be supplied by the external LAB fixture. No PA or HP
        refill and no inferred duration ticks. The trace records the declaration.
        """
        if strict:raise RuntimeBlocked('STRICT_SCHEDULER_AUTHORITY_NOT_AVAILABLE')
        if not self.validate_trace():raise RuntimeBlocked('TRACE_TAMPERED')
        if actor_id not in self.scene.actors or actor_id not in self.ledger.actors:
            raise RuntimeBlocked('PERSISTENT_ACTOR_REQUIRED')
        if not isinstance(turn_id,str) or not turn_id.strip():raise RuntimeBlocked('EXTERNAL_TURN_ID_REQUIRED')
        if not isinstance(external_authority_ref,str) or not external_authority_ref.startswith('LAB-'):
            raise RuntimeBlocked('LAB_EXTERNAL_TURN_AUTHORITY_REQUIRED')
        if any(row.get('turn_id')==turn_id for row in self.trace):
            raise RuntimeBlocked('DUPLICATE_EXTERNAL_TURN_ID')
        budgets={'standard':standard,'movement':movement,'reaction':reaction}
        if any(type(v)!=int or v not in (0,1) for v in budgets.values()):
            raise RuntimeBlocked('EXTERNAL_ACTION_BUDGET_MUST_BE_DECLARED_0_OR_1')
        if self.scene.actors[actor_id].hp<=0:
            raise RuntimeBlocked('ACTOR_WITH_HP0_REQUIRES_CANONICAL_RULING')
        candidate=deepcopy(self.scene)
        for key,value in budgets.items():setattr(candidate.actors[actor_id],key,value)
        event=candidate.record({'action':'TURN-START-LAB','by':actor_id,
                                'scene_id':self.scene_id,'turn_id':turn_id,
                                'scheduler':'MANUAL_EXTERNAL_DECLARATION_ONLY',
                                'authority_ref':external_authority_ref,
                                'budgets':budgets,'PA_refunded':0,'HP_refunded':0,
                                'duration_tick':'NOT_EXECUTED_NO_AUTHORITY'})
        led=TransformationUseLedger.restore(self.ledger.snapshot())
        trace=self._append_trace_on_clone('TURN_START_MANUAL',actor_id,event,candidate,led,
                              extra={'canonical_credit':0,'turn_id':turn_id})
        self._commit(candidate,led,trace)
        return deepcopy(trace)

    def expire_manual(self,*,actor_id,termination_reference,strict=True):
        if strict:raise RuntimeBlocked('STRICT_SOURCE_FROZEN_BATTLE_ENGINE_NOT_APPROVED')
        if not self.validate_trace():raise RuntimeBlocked('TRACE_TAMPERED')
        candidate=deepcopy(self.scene);ledger=TransformationUseLedger.restore(self.ledger.snapshot())
        try:event=expire_transformation_v09_rebuilt(candidate,actor_id,scene_id=self.scene_id,
                    ledger=ledger,termination_reference=termination_reference,strict=False)
        except (EffectBlocked,SceneLockError,ValueError) as ex:raise RuntimeBlocked('EXPIRATION_REJECTED:'+str(ex)) from ex
        wrapper=self._append_trace_on_clone('EXPIRY_MANUAL',actor_id,event,candidate,ledger,
                        extra={'canonical_credit':0,'termination_authority':'MANUAL_FIXTURE'})
        self._commit(candidate,ledger,wrapper)
        return deepcopy(wrapper)

    def completed_rest_manual(self,*,actor_id,rest_id,rest_kind,evidence_id,completed,strict=True):
        if strict:raise RuntimeBlocked('STRICT_SOURCE_FROZEN_BATTLE_ENGINE_NOT_APPROVED')
        if not self.validate_trace():raise RuntimeBlocked('TRACE_TAMPERED')
        candidate=deepcopy(self.scene);ledger=TransformationUseLedger.restore(self.ledger.snapshot())
        try:event=ledger.conclude_rest(actor_id,rest_id=rest_id,rest_kind=rest_kind,
                                      evidence_id=evidence_id,completed=completed)
        except (SceneLockError,ValueError) as ex:raise RuntimeBlocked('REST_REJECTED:'+str(ex)) from ex
        wrapper=self._append_trace_on_clone('REST_COMPLETED_FIXTURE',actor_id,event,candidate,ledger,
                    extra={'canonical_credit':0,'PA_recovered':0})
        self._commit(candidate,ledger,wrapper)
        return deepcopy(wrapper)


def o_key(source:AbilitySource,option)->str:
    # Source IDs may contain ':'; use the exact prefix constructed by v0.8.1.
    return source.action_id+':'+(option.target_id or 'none')


def require_keys(payload,keys):
    if set(payload)!=keys:raise RuntimeBlocked('EXACT_ADAPTER_PAYLOAD_REQUIRED:'+str(sorted(keys)))
