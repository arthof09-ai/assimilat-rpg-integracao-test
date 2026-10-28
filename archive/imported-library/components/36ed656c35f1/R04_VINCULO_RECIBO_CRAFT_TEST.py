"""R04: finite fail-closed receipt-to-recipe binding check, TEST ONLY.

This is NOT a PA pricing engine and NOT a replacement for the existing CRAFT
preflight. It consumes an already-generated native R27 receipt, verifies it
against the original request and recipe anchor, then delegates to the original
CRAFT v1.2 gate. No official write, E0 inference, magical fabrication or PROD.
"""
from __future__ import annotations
import hashlib
import json
from typing import Any, Callable

CONTRACT = 'R04_BIND_CRAFT_PA_READONLY_TEST/1.0'
MAX_RECEIPT_BYTES = 250_000


def _reject(reason: str, *, detail: str | None=None) -> dict:
    return {
        'contract': CONTRACT, 'state': 'HOLD_'+reason,
        'scenario_pa': None, 'receipt_bound': False,
        'pa_tariff_compatible': None,
        'original_craft_gate': None,
        'official_pa': None, 'authoritative_RE_E0': None,
        'production': 'DENY', 'writer': None, 'lease': None,
        'notion_write': False, 'party_write': False,
        'detail':detail,
    }


def _unique_object(pairs):
    obj={}
    for key,value in pairs:
        if key in obj:
            raise ValueError('DUPLICATE_JSON_KEY:'+key)
        obj[key]=value
    return obj


def _load_receipt(raw:bytes) -> dict:
    if not isinstance(raw,bytes) or len(raw)>MAX_RECEIPT_BYTES:
        raise ValueError('BYTES_INVALID_OR_TOO_LARGE')
    obj=json.loads(raw.decode('utf8'),object_pairs_hook=_unique_object,
                   parse_constant=lambda s: (_ for _ in ()).throw(ValueError('NONFINITE_JSON')))
    if not isinstance(obj,dict):raise ValueError('NOT_JSON_OBJECT')
    return obj


def _identity_equal(recipe_identity: Any, receipt_identity: Any) -> bool:
    # Deliberate, narrow compatibility with the ONE existing LAB fixture naming
    # convention. Do not treat this as an authority or official identity UUID.
    if not isinstance(recipe_identity,str) or not isinstance(receipt_identity,str):
        return False
    if recipe_identity == receipt_identity: return True
    if recipe_identity.endswith(' — TEST E3'):
        return receipt_identity == recipe_identity.removesuffix(' E3')
    return False


def bind_and_run(recipe: dict, request: dict, receipt_bytes: bytes, *,
                 native_r27: Callable[[dict],dict], native_craft_gate:Callable[...,dict],
                 r48_executable: bool=False, r48_recipe_executed: bool=False) -> dict:
    """Validate provider and recipe association; never calculate PA locally."""
    if not isinstance(recipe,dict) or not isinstance(request,dict):
        return _reject('REQUEST_OR_RECIPE_NOT_OBJECT')
    try:
        receipt=_load_receipt(receipt_bytes)
    except (ValueError,UnicodeError,TypeError) as exc:
        return _reject('RECIBO_JSON_INVALIDO',detail=str(exc)[:160])
    source_digest=hashlib.sha256(receipt_bytes).hexdigest()
    pa=recipe.get('pa')
    if not isinstance(pa,dict) or pa.get('source_receipt_sha256')!=source_digest:
        return _reject('RECEIPT_SHA_NOT_BOUND_TO_RECIPE')
    try:
        generated=native_r27(request)
    except Exception as exc:
        # Errors at the existing R27 boundary are never interpreted as zero PA.
        return _reject('ORIGINAL_PROVIDER_REJECTED_REQUEST',detail=type(exc).__name__)
    if receipt != generated:
        return _reject('ORIGINAL_PROVIDER_RESULT_MISMATCH')
    request_canonical=json.dumps(request,sort_keys=True,ensure_ascii=False,separators=(',',':'))
    if receipt.get('id_entrada_sha256') != hashlib.sha256(request_canonical.encode('utf8')).hexdigest():
        return _reject('PROVIDER_REQUEST_HASH_MISMATCH')
    if not _identity_equal((recipe.get('target') or {}).get('identity'), (receipt.get('item') or {}).get('nome')):
        return _reject('RECIPE_ITEM_IDENTITY_MISMATCH')
    if receipt.get('contrato')!='PA-CRAFT-QMC05-COMPAT-R27/1.0.0-TEST':
        return _reject('UNEXPECTED_PROVIDER_CONTRACT')
    cost=receipt.get('custo_pa') or {}
    if receipt.get('gate')!='CONSULTA_TEST_COMPLETA_COM_REVISAO_JIT' or request.get('historico'):
        return _reject('RECEIPT_NOT_QUALIFIED_FOR_TEST_BINDING')
    if not all(type(cost.get(k)) is int and cost[k]>=0 for k in ('pa_por_dia','pa_ativacoes_no_cenario','pa_total_no_cenario')):
        return _reject('PROVIDER_COST_NOT_CLOSED')
    # Check only correspondence of *declared fields* against the provider;
    # do not replicate tariff computation or apply any rank/percentage locally.
    days=(pa.get('daily') or {}).get('amount')
    uses=(pa.get('scenario_uses'))
    total=pa.get('scenario_total')
    if type(days) is not int or type(uses) is not int or type(total) is not int:
        return _reject('RECIPE_PA_FIELDS_INVALID')
    if days!=cost['pa_por_dia'] or total!=cost['pa_total_no_cenario']:
        return _reject('RECIPE_PA_TOTALS_NOT_PROVIDER')
    abilities=receipt.get('habilidades') or []
    active=[a for a in abilities if a.get('modalidade')=='ATIVA']
    use_count=sum(a.get('usos_no_dia',0) for a in active)
    if uses!=use_count:return _reject('RECIPE_USES_NOT_PROVIDER')
    # The recipe's existing single "per_activation" field can only represent one
    # active ability. A new multi-active contract must use itemized receipts.
    if len(active)!=1:
        return _reject('PER_ACTIVATION_FIELD_NEEDS_ITEMIZATION')
    per_activation=(pa.get('per_activation') or {}).get('amount')
    if type(per_activation) is not int or per_activation!=active[0].get('pa_por_ativacao'):
        return _reject('RECIPE_PER_ACTIVATION_NOT_PROVIDER')
    try:
        consumed=native_craft_gate(recipe,receipt,r48_executable=r48_executable,
                                   r48_recipe_executed=r48_recipe_executed)
    except Exception as exc:
        return _reject('EXISTING_CRAFT_GATE_REJECTED_INPUT',detail=type(exc).__name__)
    if not isinstance(consumed,dict) or consumed.get('production')!='DENY' or consumed.get('party_write') is not False:
        return _reject('CRAFT_PRODUCTION_OR_BOUNDARY_INVALID')
    return {
        'contract':CONTRACT, 'state':'BOUND_TEST_RECEIPT_R27_TO_CRAFT_V12',
        'receipt_bound':True,
        'receipt_sha256':source_digest,
        'request_sha256':receipt['id_entrada_sha256'],
        'scenario_pa':{'daily':cost['pa_por_dia'],
                       'activations':cost['pa_ativacoes_no_cenario'],
                       'scenario_total':cost['pa_total_no_cenario']},
        'pa_tariff_compatible':consumed.get('pa_version_compatible'),
        'original_craft_gate':consumed,
        'official_pa':None,'authoritative_RE_E0':None,
        'production':'DENY','writer':None,'lease':None,
        'notion_write':False,'party_write':False,
        'scope':'MESTRE_ONLY_TEST',
    }
