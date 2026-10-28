"""Fail-closed PRE/AFTER comparison for the *existing* IBX-17 writer.

This is a guard/validator, NOT another writer or transport implementation.
Current physical evidence: TEST clone V2, not Party or original R213.
The Notion connector has no proven atomic CAS: even an HTTP-successful
multi-field update can apply only a subset. Never commit without a readback.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
import hashlib
import re

LAB_TEST_CLONE = '3ffc2b324ede81439826e9b50ce9de89'
R213_ORIGINAL = '3ffc2b324ede81d383e4df1d5a4633ed'
PARTY_PAGES = {'bc49c16dd495824ea26f0186c4101d48', '3779c16dd4958237a312817eab2cf85a'}

class ScopedWriteHold(ValueError):
    pass

@dataclass(frozen=True)
class ScopedChange:
    field: str
    old: str
    new: str

@dataclass(frozen=True)
class PatchPreview:
    page_id: str
    version: str
    source_sha256: str
    after_sha256: str
    expected_after: str
    fields: tuple[str, ...]
    changes: tuple[ScopedChange, ...]
    child_ids: tuple[str, ...]
    toggle_count: int
    gate: str = 'LAB_TEST_PREPARED_NO_COMMIT'


def child_ids(body: str) -> tuple[str, ...]:
    return tuple(dict.fromkeys(re.findall(r'<page url="https://app.notion.com/p/([a-f0-9]{32})"', body)))


def signature(body: str) -> dict:
    """Root fingerprint, including references that are easy to lose in patches.

    Reference tokens are exact serialized strings, not binary file hashes.
    A stable signed media reference is NOT evidence of unchanged file bytes.
    """
    native_refs=tuple(re.findall(r'<(?:mention|image|file|audio|video|embed|bookmark)\b[^>]*>',body,re.I))
    structural_tags=tuple(re.findall(r'</?(?:toggle|details|page|callout|columns|column|table|tr|td)\b[^>]*>',body,re.I))
    return {'toggle_count':len(re.findall(r'<toggle(?:\s|>)', body)),
            'details_count':len(re.findall(r'<details(?:\s|>)',body)),
            'escaped_legacy':len(re.findall(r'\\</(?:details|toggle)\\>', body)),
            'child_ids':child_ids(body),
            'media_reference_tokens':tuple(re.findall(r'notion-file-block://[^"\s<>]+',body)),
            'native_reference_tokens':native_refs,
            'structural_tags':structural_tags,
            'sha256':hashlib.sha256(body.encode('utf-8')).hexdigest()}


def preflight(*, page_id: str, version: str, expected_version: str,
              body: str, changes: list[ScopedChange], lab_parent_verified: bool,
              expected_sha256: str | None = None) -> PatchPreview:
    """Demonstrated clone and operation ONLY; no authority to call Notion.

    Pre-check every field independently; reject duplicated names, overlapping
    strings and already-present markers. This specifically prevents the
    host's observed valid-first/invalid-second partial apply from being sent.
    """
    if page_id != LAB_TEST_CLONE or page_id in PARTY_PAGES or page_id == R213_ORIGINAL:
        raise ScopedWriteHold('PAGE_NOT_WHITELISTED_TEST_CLONE')
    if not lab_parent_verified:
        raise ScopedWriteHold('LAB_PARENT_NOT_VERIFIED')
    if not version or version != expected_version:
        raise ScopedWriteHold('VERSION_STALE_OR_MISSING')
    fingerprint = signature(body)
    if fingerprint['details_count'] or fingerprint['escaped_legacy']:
        raise ScopedWriteHold('LEGACY_ESCAPED_OR_MIXED_SERIALIZER')
    if fingerprint['toggle_count'] != 103 or len(fingerprint['child_ids']) != 20:
        raise ScopedWriteHold('STRUCTURAL_SIGNATURE_NOT_TESTED')
    if not expected_sha256 or fingerprint['sha256'] != expected_sha256:
        raise ScopedWriteHold('BODY_CHANGED_OR_MISSING_PREVIEW_HASH')
    if not 1 <= len(changes) <= 5:
        raise ScopedWriteHold('CHANGE_DENOMINATOR_UNSUPPORTED')
    seen, spans = set(), []
    for p in changes:
        if not p.field or p.field in seen:
            raise ScopedWriteHold('DUPLICATE_OR_MISSING_FIELD_ID')
        seen.add(p.field)
        if not p.old or not p.new or p.old == p.new:
            raise ScopedWriteHold('EMPTY_OR_NOOP_CHANGE')
        if body.count(p.old) != 1:
            raise ScopedWriteHold('ORIGINAL_LITERAL_NOT_EXACTLY_ONCE')
        if p.new in body:
            raise ScopedWriteHold('ALREADY_APPLIED_IDEMPOTENCE')
        if p.old.count('<toggle') != p.new.count('<toggle') or p.old.count('</toggle>') != p.new.count('</toggle>'):
            raise ScopedWriteHold('ALTERED_TOGGLE_MARKUP')
        if p.old.count('<page url=') != p.new.count('<page url='):
            raise ScopedWriteHold('CHILD_REFERENCE_CHANGE')
        at = body.index(p.old)
        spans.append((at, at+len(p.old)))
    spans.sort()
    if any(right > next_left for (_,right),(next_left,_) in zip(spans,spans[1:])):
        raise ScopedWriteHold('OVERLAPPING_PATCHES')
    predicted = body
    for p in changes:
        if predicted.count(p.old) != 1:
            raise ScopedWriteHold('COMPOUND_CONTEXT_COLLISION')
        predicted = predicted.replace(p.old,p.new,1)
    a = signature(predicted)
    if a['toggle_count'] != fingerprint['toggle_count'] or a['child_ids'] != fingerprint['child_ids']:
        raise ScopedWriteHold('PLANNED_STRUCTURE_CHANGE')
    for protected in ('media_reference_tokens','native_reference_tokens','structural_tags'):
        if a[protected] != fingerprint[protected]:
            raise ScopedWriteHold('PLANNED_PROTECTED_STRUCTURE_OR_REFERENCE_CHANGE:'+protected)
    return PatchPreview(page_id, version, fingerprint['sha256'], a['sha256'], predicted,
                        tuple(p.field for p in changes),tuple(changes),fingerprint['child_ids'],fingerprint['toggle_count'])


def verify_host_after(plan: PatchPreview, after_body: str, *, after_version: str) -> dict:
    """Exact text and tree comparison. Does not silently ignore serialization."""
    s=signature(after_body)
    applied={p.field: after_body.count(p.new)==1 for p in plan.changes}
    exp=signature(plan.expected_after)
    clean = (after_body == plan.expected_after and s['child_ids'] == plan.child_ids
             and s['toggle_count'] == plan.toggle_count and s['details_count']==0
             and s['media_reference_tokens']==exp['media_reference_tokens']
             and s['native_reference_tokens']==exp['native_reference_tokens']
             and s['structural_tags']==exp['structural_tags'])
    # A local string comparison cannot attest that its caller actually fetched
    # bytes from the Notion host. Never emit PASS_TEST_NOTION from this pure
    # comparison routine, including when the caller supplies synthetic version.
    return {'status':'PASS_LOCAL_CONTENT_EQUALITY_NO_HOST_ATTESTATION' if clean and after_version != plan.version else 'FAIL_OR_HOLD','host_physical_attested':False,
            'all_target_markers_present':all(applied.values()),'individual_targets':applied,
            'exact_body':after_body==plan.expected_after, 'children_unchanged':s['child_ids']==plan.child_ids,
            'toggles_unchanged':s['toggle_count']==plan.toggle_count,
            'version_changed':after_version != plan.version,'atomic_CAS_proven':False,
            'production_write_authorized':False}


def reconcile_partial(before_body: str, observed_body: str,
                      changes: list[ScopedChange]) -> dict:
    """If a host operation was partial, identify the exact applied subset.

    This does not automatically roll back; the caller must re-fetch and verify
    version and authorization before separately executing compensating writes.
    If any unrelated byte changed, stop without a guessed rollback.
    """
    if len(changes)>5: raise ScopedWriteHold('RECONCILE_TOO_MANY_PATCHES')
    candidates=[]
    for mask in product((False,True),repeat=len(changes)):
        trial=before_body
        for active,p in zip(mask,changes):
            if active:
                if trial.count(p.old)!=1:
                    break
                trial=trial.replace(p.old,p.new,1)
        else:
            if trial==observed_body:
                candidates.append(mask)
    if len(candidates)!=1:
        return {'status':'AMBIGUOUS_OR_FOREIGN_MUTATION_HOLD','rollback_prepared':False}
    mask=candidates[0]
    return {'status':'ALL_APPLIED' if all(mask) else 'NONE_APPLIED' if not any(mask) else 'PARTIAL_APPLY_DETECTED',
            'applied_fields':[p.field for p,applied in zip(changes,mask) if applied],
            'missing_fields':[p.field for p,applied in zip(changes,mask) if not applied],
            'compensating_patches':[{'field':p.field,'old':p.new,'new':p.old} for p,applied in zip(changes,mask) if applied],
            'rollback_prepared':True,'host_rollback_executed':False}
