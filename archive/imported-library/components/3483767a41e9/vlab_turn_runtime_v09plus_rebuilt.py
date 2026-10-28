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
from vlab_action_catalog_v01 import AbilitySource,ActorActionState,FrozenRuleEvidence
from vlab_action_catalog_v09plus_rebuilt import compile_legal_actions,transformation_readiness
from vlab_effects_v08 import (Scene,EffectBlocked,apply_weapon_attack,
                              cast_source_specified_spell,move_via_verified_path)
from vlab_effects_v09_rebuilt import activate_transformation_v09_rebuilt,expire_transformation_v09_rebuilt
from vlab_transformation_limit_v09_rebuilt import TransformationUseLedger,SceneLockError

VERSION='DOCUMENTARY-V09PLUS-MANUAL-SOURCE-EFFECT-ATOMIC-LAB'
class RuntimeBlocked(ValueError):pass


def _json(x):
    return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'),default=str)


def _sha(payload):
    return sha256(_json(payload).encode('utf-8')).hexdigest()


class RebuiltManualRuntime:
    def __init__(self,*,scene:Scene,ledger:TransformationUseLedger|None,scene_id:str,
                 test_fixture_authorized:bool=False):
        if test_fixture_authorized is not True:raise RuntimeBlocked('LAB_FIXTURE_AUTHORIZATION_REQUIRED')
        if not isinstance(scene,Scene) or not isinstance(ledger,TransformationUseLedger):
            raise RuntimeBlocked('SCENE_AND_PERSISTED_LEDGER_REQUIRED')
        if not isinstance(scene_id,str) or not scene_id.strip():raise RuntimeBlocked('SCENE_ID_REQUIRED')
        if scene.provenance!='LAB-TEST-SYNTHETIC-NONCANON':
            raise RuntimeBlocked('NONCANONICAL_SCENE_ONLY')
        self.scene=scene;self.ledger=ledger;self.scene_id=scene_id;self.trace=[]
        self.catalogue_version=VERSION

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

    def _append_trace_on_clone(self,kind,actor_id,_,candidate,ledger_clone,*,extra):
        before=self.trace[-1]['chain_hash'] if self.trace else None
        ev={'index':len(self.trace)+1,'kind':kind,'actor_id':actor_id,'scene_id':self.scene_id,
            'previous_chain_hash':before,'effect_event':deepcopy(_),'scene_events_sha256':candidate.checksum(),
            'actor_state_sha256':_sha({a:asdict(x) for a,x in sorted(candidate.actors.items())}),
            'ledger_snapshot_sha256':ledger_clone.snapshot()['sha256'],
            'qualification':VERSION,'source_mode':'LAB-ASSUMPTION-ONLY',**extra}
        ev['chain_hash']=_sha(ev)
        return ev

    def _commit(self,candidate:Scene,staged_ledger:TransformationUseLedger,event:dict):
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
        self.trace.append(event)

    def validate_trace(self):
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
                     payload:dict|None=None,manual_turn_start=False,strict=True):
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
        staged_scene=deepcopy(self.scene)
        staged_ledger=TransformationUseLedger.restore(self.ledger.snapshot())
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
        event2=self._append_trace_on_clone(spec.kind.upper(),actor_id,event,staged_scene,staged_ledger,
                   extra={'source_rule':spec.rule_id,'action_id':action_id,'transform_readiness':readiness.status,
                          'mock_effect':spec.kind=='spell','canonical_credit':0})
        self._commit(staged_scene,staged_ledger,event2)
        return deepcopy(event2)

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
