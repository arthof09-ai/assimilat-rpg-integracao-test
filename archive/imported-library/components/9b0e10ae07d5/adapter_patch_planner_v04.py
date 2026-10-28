"""Strict READ-ONLY patch planning. No Notion writes, no implicit reformatting.

Apply material changes only AFTER native full-toggle save verified and Party writer
approved. The diff planner merely verifies unique original fragment + revision.
"""
from __future__ import annotations
from hashlib import sha256
from dataclasses import dataclass
from levelup_engine import InvalidPlan


def _sha(s:str)->str:return sha256(s.encode('utf-8')).hexdigest()


def plan_minimal_field_patch(*,source_markup:str,source_sha256:str,
                             original_exact:str,replacement_exact:str,
                             notion_page_id:str,field_id:str,save_readback_verified:bool=False):
    for v,k in [(source_markup,'source_markup'),(source_sha256,'source_sha256'),
                (original_exact,'original_exact'),(replacement_exact,'replacement_exact'),
                (notion_page_id,'notion_page_id'),(field_id,'field_id')]:
        if not isinstance(v,str) or not v.strip():raise InvalidPlan(k+' inválido')
    if not (len(notion_page_id)==36 and notion_page_id.count('-')==4):
        raise InvalidPlan('Identificador de página precisa ser completo e explícito')
    if _sha(source_markup)!=source_sha256:
        raise InvalidPlan('Snapshot da página mudou: reabrir antes da atualização')
    if source_markup.count(original_exact)!=1:
        raise InvalidPlan('Trecho original ausente ou duplicado: nunca substituição global')
    if original_exact==replacement_exact:
        raise InvalidPlan('Sem alteração; não planejar escrita')
    if not original_exact.startswith('### ') or not replacement_exact.startswith('### '):
        raise InvalidPlan('Atualizações locais devem substituir exatamente uma linha/campo do Notion')
    if original_exact.split(':',1)[0].strip()!=replacement_exact.split(':',1)[0].strip():
        raise InvalidPlan('Alterou identidade do campo: preservar layout da player')
    if '\n' in original_exact or '\n' in replacement_exact:
        raise InvalidPlan('Patch restrito ao mesmo bloco/linha, sem reorganizar outras seções')
    proposal=source_markup.replace(original_exact,replacement_exact,1)
    if len(proposal)-len(source_markup)!=len(replacement_exact)-len(original_exact):
        raise InvalidPlan('Alteração além do touch-set')
    return {'status':'READ_ONLY_PATCH_CANDIDATE',
            'page_id':notion_page_id,'field_id':field_id,
            'preimage_sha256':source_sha256,'proposed_sha256':_sha(proposal),
            'old':original_exact,'new':replacement_exact,
            'save_preverified':save_readback_verified is True,
            'write_allowed':False,
            'stop_reason':None if save_readback_verified else 'SAVE nativo não verificado',
            'note':'NUNCA usar a string gerada como autorização: writer/claim/NAC-PASS separados'}
