"""R06 archive and two-surface evolution planning; creates ONLY local plans.

Notion native assets must be independently witnessed before a real patch.  No
credentials or Notion API methods are embedded.  Edit order is immutable.
"""
from __future__ import annotations
import re
from dataclasses import dataclass
from r06_contracts import (R06Hold, sha, nfm_content, plan_unique_edit,
                           verify_preimage_archive, EventJournal, FieldEdit,
                           media_manifest, PAGE_TAG)
from nfm_structure_v05 import root_toggles


@dataclass(frozen=True)
class ArchivePlan:
    page_id:str
    event_id:str
    scope:str
    preimage_sha256:str
    archive_markup:str
    marker:str
    native_risks:dict


def indent_nfm(src:str)->str:
    if not src or '\0' in src:raise R06Hold('invalid source body')
    return '\n'.join('\t'+row for row in src.split('\n'))


def archive_full_body(*,page_id:str,event_id:str,page_export:str)->ArchivePlan:
    if not re.fullmatch(r'R06-[A-Z0-9-]{8,90}',event_id):raise R06Hold('unrecognizable event ID')
    body=nfm_content(page_export).strip('\n')
    if not body:raise R06Hold('blank source page')
    marker=f'SAVE-{event_id}'
    if marker in body:raise R06Hold('save already exists: reopen before any retry')
    risk={'file_refs':len(media_manifest(body)),'child_pages':len(PAGE_TAG.findall(body)),
          'mentions':body.count('<mention-page ')}
    # Documentation provenance is part of the archive, not a fabricated Notion block UUID.
    mk=f'{marker} · pré-evolução · SHA256 {sha(body)}'
    nfm='<details color="gray_bg">\n<summary>'+mk+'</summary>\n'+indent_nfm(body)+'\n</details>'
    return ArchivePlan(page_id,event_id,'FULL_PAGE',sha(body),nfm,marker,risk)


def verify_body_plus_archive(*,before_export:str,after_export:str,plan:ArchivePlan,
                             independent_binary_proof:bool=False)->dict:
    a=nfm_content(before_export).strip('\n')
    b=nfm_content(after_export).strip('\n')
    if sha(a)!=plan.preimage_sha256:raise R06Hold('source drift before save')
    if not b.startswith(a):raise R06Hold('nonappend change during save')
    # NFM serialization typically joins block boundaries with a newline.
    expected=a+'\n'+plan.archive_markup
    if b!=expected:raise R06Hold('archive readback is not byte-for-byte equal')
    return verify_preimage_archive(before_body=a,after_save_body=b,archive_marker=plan.marker,
                                    archive_text=plan.archive_markup,assets_recreated=independent_binary_proof)


def final_state_unchanged_archive(*,after_patch_export:str,preimage:ArchivePlan,
                                  expected_replacement:str,expected_base_after:str)->dict:
    body=nfm_content(after_patch_export).strip('\n')
    if body.count(preimage.marker)!=1:raise R06Hold('archive duplicate/missing postpatch')
    if body!=expected_base_after+'\n'+preimage.archive_markup:
        raise R06Hold('unrelated change, archive changed or source overwritten')
    if expected_replacement not in expected_base_after:
        raise R06Hold('field did not update')
    return {'state':'POSTPATCH_EXACT_ARCHIVE_PRESERVED','original_sha256':preimage.preimage_sha256,
            'post_sha256':sha(body),'native_restore_proven':False,'writer_allowed':False}


def plan_multi_page_event(*,event_id:str,actor_id:str,preimages:dict[str,str],
                          confirmation_token:str|None=None)->dict:
    if not confirmation_token:
        return {'state':'PLAYER_CONFIRMATION_HOLD','write_allowed':False}
    if not 1<=len(preimages)<=2:
        raise R06Hold('supported pair is one historical page or two independent page layouts')
    j=EventJournal(actor_id,event_id,{k:sha(v) for k,v in preimages.items()})
    j.prepare()
    for pg in preimages:
        j.witnessed_save(pg,sha(preimages[pg]))
    candidate=j.authorize_patch_candidate()
    return {'state':'BOTH_BACKUPS_VERIFIED_CANDIDATE' if len(preimages)==2 else 'ONE_BACKUP_VERIFIED_CANDIDATE',
            'candidate':candidate,'journal':j,'write_allowed':False,
            'next':'Require native readback + authority before real mutation'}


def safe_field_plan(*,source_text:str,source_sha256:str,old:str,new:str)->dict:
    if not re.fullmatch(r'.{1,400}',old,re.S) or not re.fullmatch(r'.{1,400}',new,re.S):
        raise R06Hold('unbounded old/new substrings')
    return plan_unique_edit(body=source_text,edit=FieldEdit(old,new),preimage_sha256=source_sha256)


def restore_checkpoint(*,original_body:str,archived_body:str,restored_body:str)->dict:
    if sha(original_body)!=sha(archived_body):raise R06Hold('archive and original mismatch')
    if restored_body!=original_body:
        raise R06Hold('rollback not byte-equivalent')
    return {'state':'ROLLBACK_TEXT_EXACT','asset_independence':'NOT_PROVEN','write_allowed':False,
            'sha256':sha(original_body)}
