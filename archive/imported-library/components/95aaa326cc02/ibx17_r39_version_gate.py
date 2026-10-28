"""IBX-17/R39 — delta local de governança de prévia, aprovação e preservação.

NO Notion writer. All returned candidates are dry-run trees; no Party, Master or
O Primeiro updates. Intent is to make required archival/approval checks executable
and testable, NOT to claim native Notion transaction or template fidelity.
"""
from __future__ import annotations
import copy
import json
import re
import sys
from pathlib import Path
from typing import Any

_reference_r38 = Path(__file__).resolve().parents[1] / 'r38'
if not (_reference_r38 / 'ibx17_r38_bridge.py').exists():
    _reference_r38 = Path(__file__).resolve().parent / 'r38_reference'
sys.path.insert(0, str(_reference_r38))
from ibx17_r38_bridge import BridgeHold, stable_hash, verify_record, structural_inventory

DOMAINS = (
    'nivel_rank', 'atributos_naturais', 'equipamentos_bonus', 'titulos',
    'vida', 'alma_PA', 'FF_marcos', 'CA_defesas', 'ataques_dano',
    'pericias_acerto', 'magias', 'transformacao', 'rolagens_historico',
    'blocos_midias', 'sincronizacao_master_party',
)
# These are treated as projected, not authenticated effects; field coverage must
# be sourced to the historical rule engine and character-specific receipts.
VALID_COVERAGE = {'ALTERA', 'NAO_ALTERA_VERIFICADO', 'PENDENTE'}
USER_EDIT_ENDINGS = {'content', 'value', 'number', 'checkbox', 'url', 'name'}
RESERVED_KEYS = {'id', 'type', 'has_children', 'last_edited_time', 'created_time', 'archived',
                 'in_trash', 'object', 'parent', 'children', 'results', 'blocks'}


def _g(obj: Any, path: list[Any]):
    if not isinstance(path, list) or not path:
        raise BridgeHold('PATH_REQUIRED')
    now = obj
    for key in path:
        if type(key) is int and isinstance(now, list) and 0 <= key < len(now):
            now = now[key]
        elif isinstance(key, str) and isinstance(now, dict) and key in now:
            now = now[key]
        else:
            raise BridgeHold('PATH_NOT_PRESENT')
    return now


def _set_existing(obj: Any, path: list[Any], new: Any):
    node = _g(obj, path[:-1])
    key = path[-1]
    if type(key) is int and isinstance(node, list) and 0 <= key < len(node):
        node[key] = copy.deepcopy(new)
    elif isinstance(key, str) and isinstance(node, dict) and key in node:
        node[key] = copy.deepcopy(new)
    else:
        raise BridgeHold('PATH_NOT_PRESENT')


def _text(block: dict):
    typ = block.get('type')
    val = block.get(typ) if isinstance(typ, str) else None
    if not isinstance(val, dict):
        return ''
    out = []
    for run in val.get('rich_text', []):
        if isinstance(run, dict):
            out.append(run.get('plain_text') or (run.get('text') or {}).get('content') or '')
    return ''.join(out)


def _archive_split(blocks: list[dict]):
    """New archives are a trailing contiguous run; never infer a legacy layout."""
    for i, b in enumerate(blocks):
        if not isinstance(b, dict):
            raise BridgeHold('UNSUPPORTED_TOP_LEVEL_BLOCK')
        known = b.get('_ibx17_archive') is True
        heading = _text(b).casefold()
        legacy_hint = b.get('type') == 'toggle' and bool(re.search(
            r'vers[aã]o\s+anteri|vers[oõ]es\s+anteri|hist[oó]rico\s+de\s+ficha', heading))
        if legacy_hint and not known:
            raise BridgeHold('LEGACY_TOGGLE_LAYOUT_UNMAPPED')
        if known and b.get('type') != 'toggle':
            raise BridgeHold('INVALID_ARCHIVE_MARKER')
    cut = len(blocks)
    while cut > 0 and blocks[cut-1].get('_ibx17_archive') is True:
        cut -= 1
    if any(b.get('_ibx17_archive') is True for b in blocks[:cut]):
        raise BridgeHold('ARCHIVE_NOT_TRAILING')
    return copy.deepcopy(blocks[:cut]), copy.deepcopy(blocks[cut:])


def _property_snapshots(raw: dict) -> list[dict]:
    """Serialize ALL page-level metadata, not merely the properties database object.

    A separate native writer must reconstruct the visible archived representation.
    """
    header = {k:v for k,v in raw.items() if k != "children"}
    payload = json.dumps(header, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    chunks = [payload[i:i+1700] for i in range(0, len(payload), 1700)] or ['{}']
    return [{'type': 'paragraph', 'paragraph': {
        'rich_text': [{'type': 'text', 'text': {'content': ('Propriedades originais e metadados da página (JSON) — ' if i == 0 else '') + chunk}}]}}
        for i, chunk in enumerate(chunks)]


def _media_assets(raw: dict):
    missing = []
    def visit(node, path='$'):
        if isinstance(node, list):
            for idx, x in enumerate(node):visit(x,f'{path}[{idx}]')
        elif isinstance(node, dict):
            typ = node.get('type')
            if typ in ('image','file','video','audio','pdf','embed','bookmark','link_preview','child_page','child_database','link_to_page','synced_block'):
                proof = node.get('_ibx17_durable_media_proof')
                if not (isinstance(proof, dict) and proof.get('sha256') and proof.get('persisted_location')):
                    missing.append({'path':path, 'type':typ,'reason':'DURABLE_ASSET_COPY_UNPROVEN'})
            for key in ('children','blocks','results'):
                if isinstance(node.get(key), list):visit(node[key],path+'.'+key)
            payload=node.get(typ) if isinstance(typ,str) else None
            if isinstance(payload,dict):
                for key in ('children','blocks','results'):
                    if isinstance(payload.get(key),list):visit(payload[key],path+'.'+typ+'.'+key)
    visit(raw)
    # Cover and icon may be outside the block tree and still part of the sheet.
    for key in ('icon','cover'):
        val=raw.get(key)
        if isinstance(val,dict) and val.get('type') in ('file','external','custom_emoji'):
            proof=val.get('_ibx17_durable_media_proof')
            if not (isinstance(proof,dict) and proof.get('sha256') and proof.get('persisted_location')):
                missing.append({'path':'$.'+key,'type':val.get('type'),'reason':'PAGE_MEDIA_BACKUP_UNPROVEN'})
    return missing


def _impacts(coverage: dict):
    if set(coverage) != set(DOMAINS):
        raise BridgeHold('IMPACT_MATRIX_INCOMPLETE')
    for d, ent in coverage.items():
        if not isinstance(ent, dict) or ent.get('status') not in VALID_COVERAGE:
            raise BridgeHold('IMPACT_NOT_EVALUATED_'+d)
        if not ent.get('explanation') or not ent.get('source_ref'):
            raise BridgeHold('IMPACT_EXPLANATION_OR_SOURCE_MISSING_'+d)
    return [d for d,x in coverage.items() if x['status']=='PENDENTE']


def preview_versioned_change(record: dict, edits: list[dict], coverage: dict, *,
                             label: str, user_summary: str, page_ownership: dict) -> dict:
    """Propose the entire preimage, exact patch, and native toggle architecture.

    All authenticating claims must be checked against the independent Notion
    connector by a future writer; R39 itself performs NO network operation.
    """
    verify_record(record)
    if record['kind'] != 'NOTION_NATIVE_READ_ONLY':
        raise BridgeHold('NO_NATIVE_SHEET_PREVIEW_FOR_REAL_APPLICATION')
    inv=structural_inventory(record)
    if not inv['native_complete_verified']:
        raise BridgeHold('UNEXPANDED_NATIVE_TREE')
    if not isinstance(record['raw'],dict) or not isinstance(record['raw'].get('children'),list):
        raise BridgeHold('UNKNOWN_NATIVE_SHEET_STRUCTURE')
    if not page_ownership or page_ownership.get('character_key')!=record['character_key'] or \
        page_ownership.get('page_id')!=record['page_id'] or \
        page_ownership.get('surface')!=record['surface'] or \
        page_ownership.get('binding_receipt') is None:
        raise BridgeHold('SHEET_OWNERSHIP_UNPROVEN')
    if not isinstance(edits,list) or not edits:
        raise BridgeHold('NO_CONCRETE_EDITS')
    if not isinstance(user_summary,str) or not user_summary.strip() or not label.strip():
        raise BridgeHold('REVIEW_DESCRIPTION_REQUIRED')
    pending = _impacts(coverage)
    raw0 = copy.deepcopy(record['raw'])
    active, history = _archive_split(raw0['children'])
    # Only one effect per exact targeted leaf; values cannot contain undeclared subtree changes.
    working=copy.deepcopy(raw0)
    before_after=[]; targets=set()
    for patch in edits:
        path=patch.get('path')
        if not isinstance(path,list) or len(path)<2 or path[0] not in ('children','properties'):
            raise BridgeHold('EDIT_TARGET_UNSUPPORTED')
        if any(isinstance(x,str) and x in RESERVED_KEYS for x in path[1:]):
            raise BridgeHold('STRUCTURAL_MUTATION_UNSUPPORTED')
        if path[-1] not in USER_EDIT_ENDINGS and type(path[-1]) is not int:
            raise BridgeHold('TARGET_NOT_A_USER_VALUE')
        if path[0]=='children' and (type(path[1]) is not int or path[1]>=len(active)):
            raise BridgeHold('ATTEMPT_TO_EDIT_HISTORY')
        key=json.dumps(path,ensure_ascii=False)
        if key in targets:raise BridgeHold('DUPLICATE_TARGET')
        targets.add(key)
        before=_g(working,path)
        if before!=patch.get('before'):
            raise BridgeHold('EXPECTED_OLD_VALUE_MISMATCH')
        if type(before)!=type(patch.get('after')) or isinstance(before,(dict,list)):
            raise BridgeHold('SCALAR_ONLY_PATCH')
        if before==patch['after']:
            raise BridgeHold('NO_OP_CHANGE')
        if not patch.get('explanation') or not patch.get('rule_ref'):
            raise BridgeHold('CHANGE_WITHOUT_EXPLANATION')
        _set_existing(working,path,patch['after'])
        before_after.append({'path':copy.deepcopy(path),'before':copy.deepcopy(before),
                             'after':copy.deepcopy(patch['after']),
                             'explanation':patch['explanation'],'rule_ref':patch['rule_ref']})
    if stable_hash(raw0)==stable_hash(working):raise BridgeHold('NO_EFFECT')
    if len(working['children']) != len(active)+len(history):
        raise BridgeHold('STRUCTURAL_DRIFT_AFTER_PATCH')
    # Guard against unintended changes in old archives and all untouched content.
    if stable_hash(working['children'][len(active):]) != stable_hash(history):
        raise BridgeHold('HISTORY_MUTATED')
    media_unknown=_media_assets({**{k:v for k,v in raw0.items() if k!='children'},'children':active})
    complete_archive = not media_unknown
    preimage_hash=stable_hash(raw0)
    preview_body={'operation':'IBX-17','phase':'PREVIEW_ONLY',
                  'character_key':record['character_key'],'surface':record['surface'],
                  'page_id':record['page_id'],'preimage_sha256':preimage_hash,
                  'proposed_edited_content_sha256':stable_hash(working),
                  'summary':user_summary,'changes':before_after,
                  'impact_matrix':copy.deepcopy(coverage), 'impact_pending':pending,
                  'existing_history_toggles':len(history),
                  'archive_source_active_blocks_sha256':stable_hash(active),
                  'archive_full_preimage_sha256':preimage_hash,
                  'archive_props_sha256':stable_hash(raw0.get('properties',{})),
                  'archive_media_missing_proofs':media_unknown,
                  'media_backup_complete':complete_archive,
                  'page_ownership_receipt':page_ownership['binding_receipt'],
                  'legacy_parity_verified':False,
                  'permission_to_write':False,
                  'native_archive_physically_written':False,
                  'approval_received':False}
    preview_digest=stable_hash(preview_body)
    return {'status':'PREVIEW_REVIEW_REQUIRED', 'preview_sha256':preview_digest,
            'review':preview_body, 'source_record':copy.deepcopy(record),
            'preimage_raw':raw0,'changed_raw':working,'label':label,
            'archive_eligible_locally':complete_archive and not pending,
            'writes':0}


def approval_gate(plan: dict, approval: dict, *, actor_authority: dict) -> dict:
    review=plan['review'];
    if plan.get('status')!='PREVIEW_REVIEW_REQUIRED':
        raise BridgeHold('APPROVAL_NOT_FOR_PREVIEW')
    if not isinstance(approval,dict) or approval.get('decision') != 'APROVO':
        raise BridgeHold('APPROVAL_ABSENT_OR_REJECTED')
    if approval.get('preview_sha256')!=plan['preview_sha256'] or \
       stable_hash(review)!=plan['preview_sha256']:
        raise BridgeHold('PREVIEW_CHANGED_AFTER_REVIEW')
    if not approval.get('all_changes_displayed'):
        raise BridgeHold('INCOMPLETE_USER_PREVIEW')
    if not approval.get('archive_full_previous_version_explicit'):
        raise BridgeHold('PREVIOUS_VERSION_NOT_AUTHORIZED')
    if approval.get('role') not in ('MESTRE','PLAYER') or not approval.get('actor_id'):
        raise BridgeHold('APPROVER_IDENTITY_MISSING')
    if actor_authority.get('verified_actor_id')!=approval['actor_id'] or not actor_authority.get('authenticated'):
        raise BridgeHold('APPROVAL_AUTHENTICATION_UNPROVEN')
    if actor_authority.get('surface')!=review['surface'] or \
       actor_authority.get('character_key')!=review['character_key'] or \
       actor_authority.get('page_id')!=review['page_id']:
        raise BridgeHold('APPROVAL_TARGET_OR_SURFACE_MISMATCH')
    if approval['role']=='PLAYER' and not actor_authority.get('character_owner_verified'):
        raise BridgeHold('PLAYER_NOT_OWNER')
    if not actor_authority.get('explicit_sheet_write_authority'):
        raise BridgeHold('SHEET_WRITE_AUTHORITY_ABSENT')
    # Party requires its own physically authenticated connection and authority;
    # an approval for the Master's mirror is not authorization to write Party.
    if review['surface']=='PARTY' and not actor_authority.get('independent_party_connector_verified'):
        raise BridgeHold('PARTY_WRITER_NOT_AUTHORIZED')
    if review['impact_pending']:
        raise BridgeHold('UNRESOLVED_SECONDARY_EFFECTS')
    if not review['media_backup_complete']:
        raise BridgeHold('FULL_MEDIA_BACKUP_NOT_VERIFIED')
    if not approval.get('explicit_approval_receipt'):
        raise BridgeHold('APPROVAL_RECEIPT_UNVERIFIED')
    return {'status':'LOCAL_APPROVAL_CONTRACT_VALID',
            'preview_sha256':plan['preview_sha256'],
            'approved_by':approval['actor_id'],'scope':review['surface'],
            'authorizing_receipt':approval['explicit_approval_receipt'],
            'no_notion_write':True}


def archive_dry_run(plan: dict, local_approval: dict, reread_record: dict) -> dict:
    """Return a candidate page containing the previous active sheet in a toggle.

    This is not the Notion writer. Child ID rewriting, unsupported types, remote
    media durability, and template parity are **unverified native dependencies**.
    """
    if local_approval.get('status')!='LOCAL_APPROVAL_CONTRACT_VALID' or \
       local_approval.get('preview_sha256')!=plan['preview_sha256']:
        raise BridgeHold('APPROVAL_RECEIPT_MISMATCH')
    verify_record(reread_record)
    review=plan['review']
    if reread_record['page_id']!=review['page_id'] or reread_record['surface']!=review['surface'] or \
       reread_record['character_key']!=review['character_key']:
        raise BridgeHold('PREWRITE_WRONG_SHEET')
    if stable_hash(reread_record['raw'])!=review['preimage_sha256']:
        raise BridgeHold('CONCURRENT_CHANGE_REAPPROVAL_REQUIRED')
    original=plan['preimage_raw']
    active, history=_archive_split(original['children'])
    # Notion API will generate new IDs for historical clones; local tree keeps
    # old IDs to measure full fidelity. This MUST NOT be written directly.
    archive_children=_property_snapshots(original)+copy.deepcopy(active)
    toggle={'type':'toggle', '_ibx17_archive':True,
        '_ibx17_archive_meta':{
            'review_sha256':plan['preview_sha256'],
            'full_page_snapshot_sha256':review['archive_full_preimage_sha256'],
            'original_active_children_sha256':stable_hash(active),
            'original_properties_sha256':stable_hash(original.get('properties',{})),
            'previous_archives_count':len(history),
            'native_ids_remapped':False,'native_api_verified':False},
        'toggle':{'rich_text':[{'type':'text','text':{'content':f"Versão anterior — {plan['label']}"}}],
                  'children':archive_children}}
    candidate=copy.deepcopy(plan['changed_raw'])
    candidate['children']=copy.deepcopy(candidate['children'])+[toggle]
    if stable_hash(candidate['children'][:len(active)])!=stable_hash(plan['changed_raw']['children'][:len(active)]):
        raise BridgeHold('NEW_ACTIVE_CONTENT_CHANGED_DURING_ARCHIVE')
    if stable_hash(candidate['children'][len(active):len(active)+len(history)])!=stable_hash(history):
        raise BridgeHold('OLD_ARCHIVES_CHANGED')
    if stable_hash(candidate['children'][-1]['toggle']['children'][len(_property_snapshots(original)):]) != stable_hash(active):
        raise BridgeHold('ARCHIVE_NOT_COMPLETE')
    if stable_hash(original)!=review['archive_full_preimage_sha256']:
        raise BridgeHold('PREIMAGE_HASH_DRIFT')
    return {'status':'LOCAL_BLUEPRINT_NOT_APPLIED',
            'candidate_raw':candidate,'candidate_sha256':stable_hash(candidate),
            'previous_active_blocks_sha256':stable_hash(active),
            'previous_full_page_sha256':stable_hash(original),
            'old_history_count':len(history),'new_version_toggles_added':1,
            'archival_location':'END_OF_ORIGINAL_PAGE',
            'archived_previous_fully_in_local_blueprint':True,
            'native_replayable':False, 'native_writer_admitted':False,
            'next_physical_steps':[
                'read fresh original Party or Master page and all descendants, verifying snapshot and media',
                'verify permission and record authenticated approval bound to exact preview',
                'derive Notion-native clone with remapped block IDs and preserved rich text/media',
                'append archived full prior version to tail as native toggle and reopen/verify archival completeness',
                'only after archive proof, apply authorized edits to currently active sheet',
                'reopen, verify all fields/blocks/history/media and reconcile source hashes',
                'record before-after receipts, rollback if safe, finalize NAC-PASS',
            ],
            'writes':0}


def checkup_for_chat(plan: dict) -> str:
    """Friendly player-safe *structural* check-up; caller must restrict info to
    authorized surface and never add Master-only evidence to Party delivery."""
    if plan.get('status') != 'PREVIEW_REVIEW_REQUIRED' or \
       stable_hash(plan['review']) != plan.get('preview_sha256'):
        raise BridgeHold('CHECKUP_SOURCE_UNVERIFIED')
    r=plan['review']; lines=[
        'PRÉVIA DE ALTERAÇÃO — NÃO APLICADA',
        f"Ficha: {r['character_key']} | Área: {r['surface']}",
        f"Objetivo: {r['summary']}",
        'ANTES → DEPOIS (alterações propostas):',
    ]
    for i, ch in enumerate(r['changes'],1):
        where='/'.join(str(x) for x in ch['path'])
        lines.append(f"{i}. {where}: {ch['before']!r} → {ch['after']!r}; "+
                     f"motivo: {ch['explanation']}; regra: {ch['rule_ref']}")
    lines.append('CHECK-UP DOS EFEITOS INDIRETOS:')
    for domain in DOMAINS:
        ent=r['impact_matrix'][domain]
        lines.append(f"- {domain}: {ent['status']} — {ent['explanation']} (fonte: {ent['source_ref']})")
    lines.append('HISTÓRICO: a versão anterior completa será preservada no final '+
                 'da ficha em alternante, sem apagar versões mais antigas.')
    if r['archive_media_missing_proofs']:
        lines.append('PENDÊNCIA: mídias ou referências sem cópia durável comprovada.')
    if r['impact_pending']:
        lines.append('PENDÊNCIA: impactos não resolvidos — '+', '.join(r['impact_pending']))
    lines += ['Autorização: NENHUMA. Aprovação somente após leitura deste conteúdo inteiro.',
              'A aplicação física exige reabertura da ficha, arquivo anterior verificado, '+
              'escrita autorizada, releitura e NAC-PASS.',
              f"Identificador desta prévia: {plan['preview_sha256']}"]
    return '\n'.join(lines)
