"""IBX-114 continuation: fail-closed, transport-free transaction recovery.

Extends writer V2 *checks*, not its host writer or authorization. No calls to
Notion, Party, O Primeiro. A local test observation MUST NOT be represented
as an independently verified physical Notion PASS.

The actual Notion host has demonstrated successful HTTP reporting for a partial
multi-target mutation. Hence: request success and version increment have zero
weight for data integrity without independent full-body readback.
"""
from __future__ import annotations
from dataclasses import dataclass
import hashlib
import json
from typing import Literal
from ibx114_writer_v2_scope import (
 PatchPreview, ScopedChange,ScopedWriteHold,preflight,signature,
 reconcile_partial,verify_host_after)

SCHEMA='IBX114_RECOVERY_INTENT_V1'

class RecoveryHold(ScopedWriteHold): pass

@dataclass(frozen=True)
class Intent:
    operation_id:str
    plan:PatchPreview
    declared_test_only:bool=True

@dataclass(frozen=True)
class Observation:
    page_id:str
    version:str
    body:str|None
    provenance:Literal['LOCAL_SIMULATION','PHYSICAL_NOTION_FETCH','UNVERIFIED']='UNVERIFIED'
    # An explicit host-fetch label must be backed by a tool receipt outside
    # this local module; it is NOT independent proof of host transport.


def make_intent(plan:PatchPreview)->Intent:
    if plan.gate != 'LAB_TEST_PREPARED_NO_COMMIT':
        raise RecoveryHold('NOT_A_LAB_PREVIEW')
    content={'schema':SCHEMA,'page':plan.page_id,'source_version':plan.version,
             'source_sha256':plan.source_sha256,'after_sha256':plan.after_sha256,
             'fields':plan.fields,
             'changes':[(p.field,p.old,p.new) for p in plan.changes]}
    oid=hashlib.sha256(json.dumps(content,ensure_ascii=False,sort_keys=True,
                                  separators=(',',':')).encode()).hexdigest()
    return Intent(oid,plan)


def classify_observation(intent:Intent, observed:Observation,*,tool_report:str='UNKNOWN')->dict:
    """Classify effects; no host write or rollback is performed here.

    No route in this function produces a Notion PASS or a production COMMIT.
    Even with provenance='PHYSICAL_NOTION_FETCH', the physical receipt must be
    externally validated. A correct after state is not evidence of atomic CAS.
    """
    p=intent.plan
    out={'operation_id':intent.operation_id,'target':p.page_id,'tool_report':tool_report,
         'provenance_claim':observed.provenance,'physical_provenance_independently_verified':False,
         'production_write_authorized':False,'cas_atomicity_proven':False,
         'host_write_performed_by_this_module':False,'automatic_retry':False,
         'automatic_compensation':False,'transaction_status':'HOLD'}
    if observed.page_id!=p.page_id:
        return dict(out,classification='DIFFERENT_TARGET_HOLD',reason='PAGE_ID_DRIFT')
    if not observed.version or observed.body is None:
        return dict(out,classification='OBSERVATION_MISSING_HOLD',reason='INCOMPLETE_FETCH')
    before_hash=signature(observed.body)['sha256']
    out['observed_sha256']=before_hash
    out['observed_version']=observed.version
    if before_hash==p.source_sha256 and observed.body!=p.expected_after:
        # Version can change due to an unrelated edit: never call it stable.
        return dict(out,classification=('NOOP_BODY_VERSION_DRIFT_HOLD' if
                    observed.version!=p.version else 'NOOP_BODY_CONFIRMED'),
                    applied_fields=[],compensation_candidate=[])
    if observed.body==p.expected_after and before_hash==p.after_sha256:
        if observed.version==p.version:
            return dict(out,classification='AFTER_BODY_VERSION_UNCHANGED_HOLD',
                        applied_fields=list(p.fields),compensation_candidate=[])
        local=verify_host_after(p,observed.body,after_version=observed.version)
        return dict(out,classification='FULL_BODY_MATCH_NOT_HOST_ATOMICITY',
                    local_readback_status=local['status'],applied_fields=list(p.fields),
                    compensation_candidate=[],integrity_comparison='PASS_LOCAL')
    # Detection is safe only for a matched subset, no unrelated mutations.
    baseline=p.expected_after
    if observed.body != baseline:
        reference_body=baseline
        # Reverse all replacements from the predicted body, then validate
        # reconstructed prefix and expected SHA before calling reconciler.
        for change in reversed(p.changes):
            if reference_body.count(change.new)!=1:
                return dict(out,classification='AMBIGUOUS_PREIMAGE_HOLD',reason='INCONSISTENT_PATCH_PLAN')
            reference_body=reference_body.replace(change.new,change.old,1)
        if signature(reference_body)['sha256'] != p.source_sha256:
            return dict(out,classification='AMBIGUOUS_PREIMAGE_HOLD',reason='PREIMAGE_HASH_MISMATCH')
        state=reconcile_partial(reference_body,observed.body,list(p.changes))
        if state['status']=='PARTIAL_APPLY_DETECTED':
            return dict(out,classification='PARTIAL_APPLY_DETECTED_HOLD',
                        applied_fields=state['applied_fields'],
                        compensation_candidate=state['compensating_patches'],
                        compensation_requires_independent_preflight=True)
        return dict(out,classification='FOREIGN_OR_AMBIGUOUS_MUTATION_HOLD',
                    reason=state['status'])
    return dict(out,classification='INCONCLUSIVE_HOLD')


def recovery_gate(intent:Intent, observed:Observation,*,tool_report:str,
                  previously_dispatched:set[str]|frozenset[str]|None=None)->dict:
    """No automatic replay, including if a timeout reports no success.

    previously_dispatched is a local test fixture, NOT a distributed lock or
    durable shared idempotency store; no writer authorization is conferred.
    """
    prior=previously_dispatched or set()
    report=classify_observation(intent,observed,tool_report=tool_report)
    seen=intent.operation_id in prior
    return {'report':report,'replay_gate':'REFUSE_DUPLICATE_OR_UNKNOWN_RESULT' if seen
            else 'REFUSE_HOST_REPLAY_PENDING_AUTHORITY','duplicate_seen_locally':seen,
            'same_page_proven':observed.page_id==intent.plan.page_id,
            'safe_to_auto_execute':False,'safe_to_auto_rollback':False}


def prepare_local_compensation(intent:Intent,obs:Observation,*,
                  lab_parent_verified:bool,expected_current_version:str,
                  expected_current_sha256:str)->dict:
    """Prepare an independently revalidated rollback preview; no execution.

    Works only for exactly recognized partial/full effects in allowed TEST
    clone, and only with a fresh content hash/version from the caller.
    Version match here is optimistic preflight, not CAS/fencing.
    """
    report=classify_observation(intent,obs)
    if report['classification'] not in ('PARTIAL_APPLY_DETECTED_HOLD',
                                        'FULL_BODY_MATCH_NOT_HOST_ATOMICITY'):
        raise RecoveryHold('NO_UNAMBIGUOUS_PATCH_SET_TO_REVERSE')
    if obs.provenance!='PHYSICAL_NOTION_FETCH':
        raise RecoveryHold('FRESH_PHYSICAL_HOST_READBACK_REQUIRED')
    if obs.version != expected_current_version or not expected_current_version:
        raise RecoveryHold('STALE_RECOVERY_VERSION')
    if not obs.body or signature(obs.body)['sha256']!=expected_current_sha256:
        raise RecoveryHold('STALE_RECOVERY_CONTENT_HASH')
    selected=set(report['applied_fields'])
    reverse=[ScopedChange(c.field,c.new,c.old) for c in intent.plan.changes if c.field in selected]
    # A precise plan is necessary but NOT sufficient for a safe host write:
    # host atomicity and writer authority remain unproven.
    rollback=preflight(page_id=intent.plan.page_id,version=obs.version,
                       expected_version=expected_current_version,body=obs.body,
                       changes=reverse,lab_parent_verified=lab_parent_verified,
                       expected_sha256=expected_current_sha256)
    return {'operation_id':intent.operation_id,'recovery_preview':rollback,
            'expected_reverted_body_sha256':rollback.after_sha256,
            'compensated_fields':tuple(c.field for c in reverse),
            'automatic_dispatch_allowed':False,'host_compensation_executed':False,
            'requires_new_permission':True,'requires_fresh_preflight_at_commit':True}
