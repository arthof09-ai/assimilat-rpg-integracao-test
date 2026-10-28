"""Immutable pre-evolution archive *plan*, for native Notion toggles.

Constructs enhanced Markdown without silently claiming that native images/subpages
have been duplicated. Actual production needs a verified legitimate writer and
native resource-copy proof; this module has no network/write permissions.
"""
from __future__ import annotations
import re
from dataclasses import dataclass
from nfm_structure_v05 import digest, archive_risk, root_toggles, page_body, StructuralError

class SaveHold(StructuralError):pass
EVENT=re.compile(r'^[A-Z0-9][A-Z0-9_-]{7,95}$')


def _indent_once(text: str)->str:
    return '\n'.join('\t'+line if line else '\t' for line in text.split('\n'))

def _dedent_once(text:str)->str:
    lines=text.split('\n')
    if any(not v.startswith('\t') for v in lines):
        raise SaveHold('Archive perdeu nível de indentação: sem readback de fidelidade')
    return '\n'.join(v[1:] for v in lines)


def _validate_event(event_id:str,profile_key:str):
    if not isinstance(event_id,str) or not EVENT.fullmatch(event_id):
        raise SaveHold('EVENT-ID estável obrigatório (A-Z,0-9,-,_)')
    if not re.fullmatch(r'[a-z0-9-]{2,45}', profile_key):
        raise SaveHold('profile_key inválido')


def build_archive(*,event_id:str,profile_key:str,preimage:str,scope:str,source_page_id:str,
                  candidate_level:str, native_clone_evidence:bool=False)->dict:
    """Save of *pre-edit* body or root toggle, not post-edit values.

    Output is a CANDIDATE requiring Notion readback and separate verification of
    media/file/child pages. Never automatically permits patching.
    """
    _validate_event(event_id,profile_key)
    if scope not in ('full-page','active-root-toggle','paired-root-toggles'):raise SaveHold('Invalid archive scope')
    if not isinstance(preimage,str) or not preimage.strip():raise SaveHold('Preimage vazia')
    if not isinstance(source_page_id,str) or len(source_page_id)!=36:raise SaveHold('page-id ausente')
    if not isinstance(candidate_level,str) or not candidate_level.strip() or '<' in candidate_level:
        raise SaveHold('Level de origem inválido')
    if scope=='active-root-toggle':
        roots=root_toggles(preimage)
        if len(roots)!=1 or roots[0].start>3 or preimage[roots[0].end:].strip():
            raise SaveHold('Escopo ativo exige exato um toggle raiz completo')
    if scope=='paired-root-toggles':
        roots=root_toggles(preimage)
        if len(roots)!=2 or roots[0].start>3 or preimage[roots[-1].end:].strip():
            raise SaveHold('Save pareado exige NORMAL + TRANSFORMAÇÃO, dois toggles raiz completos')
        if 'Transforma' in roots[0].summary or 'Transforma' not in roots[1].summary:
            raise SaveHold('Par de saves deve ser normal seguido da transformação correspondente')
    inv=archive_risk(preimage)
    marker=f'SAVE-{event_id}-{profile_key}'
    meta=f'{marker} · ORIGEM {candidate_level} · SHA256 {digest(preimage)}'
    if len(meta)>180:raise SaveHold('Identificador de toggle muito extenso')
    # The inner content is not normalized; a synthetic roundtrip proves its bytes.
    archive='\n<details color="gray_bg">\n<summary>'+meta+'</summary>\n'+_indent_once(preimage)+'\n</details>\n'
    native_risks=inv['risks']
    return {'type':'ARCHIVE_PREIMAGE_CANDIDATE','event_id':event_id,'profile_key':profile_key,
            'source_page_id':source_page_id,'scope':scope,'source_sha256':digest(preimage),
            'raw_bytes':len(preimage.encode('utf-8')),'archive_markup':archive,
            'marker':marker,'risk_inventory':inv['inventory'],'native_risks':native_risks,
            'can_certify_native_without_copy_evidence':not native_risks,
            'native_clone_evidence_declared':native_clone_evidence,
            'real_notional_write_allowed':False,'state':'PREPARED_READ_ONLY'}


def _find_archive_body(exported:str,marker:str)->str:
    body=page_body(exported)
    roots=root_toggles(body)
    found=[x for x in roots if marker in x.summary]
    if len(found)!=1:raise SaveHold(f'Arquivo não encontrado exatamente 1 vez ({len(found)})')
    t=found[0]
    raw=t.raw(body)
    ix=raw.index('</summary>')+len('</summary>')
    iy=raw.rfind('</details>')
    inside=raw[ix:iy]
    if inside.startswith('\n'):inside=inside[1:]
    if inside.endswith('\n'):inside=inside[:-1]
    return _dedent_once(inside)


def verify_archived_readback(*,exported_after_save:str,candidate:dict,
                             witnessed_native_ref_copy:bool=False)->dict:
    """A text-equivalent readback is not media independence proof."""
    if candidate.get('type')!='ARCHIVE_PREIMAGE_CANDIDATE':raise SaveHold('Plano inválido')
    recovered=_find_archive_body(exported_after_save,candidate['marker'])
    ok=digest(recovered)==candidate['source_sha256']
    if not ok:raise SaveHold('SAVE não coincide com preimage (byte/hash); STOP antes de editar')
    native_risks=candidate['native_risks']
    if native_risks and not witnessed_native_ref_copy:
        return {'state':'READBACK_TEXT_ONLY_NATIVE_ASSETS_HOLD', 'source_sha256':digest(recovered),
                'saved_marker':candidate['marker'],'native_risks':native_risks,
                'allow_mutation':False}
    return {'state':'READBACK_FULL_EVIDENCE_CANDIDATE', 'source_sha256':digest(recovered),
            'saved_marker':candidate['marker'],'native_risks':native_risks,
            'allow_mutation':False,'reason':'Writer, field mapping, authorized Party gate and NAC-PASS are independently required'}


def save_append_only_preflight(*,page_export_before:str, candidate:dict)->dict:
    """Check event duplication and source identity immediately before append."""
    body=page_body(page_export_before)
    if candidate['marker'] in body:raise SaveHold('Save já existe: reabrir/verificar em vez de anexar novamente')
    if candidate['scope']=='full-page' and digest(body)!=candidate['source_sha256']:
        raise SaveHold('Página mudou desde a captura; cancelar save antigo')
    if candidate['scope']=='active-root-toggle' and candidate['source_sha256'] not in [t.source_sha256 for t in root_toggles(body)]:
        raise SaveHold('Toggle ativo mudou desde a captura; cancelar save antigo')
    if candidate['scope']=='paired-root-toggles':
        # Preimage must be an unmodified, contiguous slice of both native root toggles.
        # Check against exact current source: an archived copy cannot satisfy preflight.
        archive_start=body.find('<summary>SAVE-')
        current_body=body if archive_start<0 else body[:archive_start]
        if candidate['source_sha256'] not in [digest(current_body[a.start:b.end]) for i,a in enumerate(root_toggles(current_body)) for b in root_toggles(current_body)[i+1:i+2] if a.start<b.start]:
            raise SaveHold('Dupla normal+espírito não é mais uma preimage contígua verificada')
    return {'status':'APPEND_CANDIDATE_NOT_AUTHORIZATION','marker':candidate['marker'],
            'content_to_append':candidate['archive_markup'],'operation':'insert_content at end',
            'required_next':'REOPEN + READBACK BEFORE FIELD PATCH','real_write_allowed':False}
