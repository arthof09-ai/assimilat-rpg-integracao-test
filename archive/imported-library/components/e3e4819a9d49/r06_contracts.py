"""R06 contracts for evidence-based, no-write Notion profile adaptation.

No network, keys, remote mutations, or hidden Party data.  All operations
produce *plans*.  Physical Notion execution is outside this module and requires
separate role/writer/permission/asset and NAC checks.
"""
from __future__ import annotations
import hashlib
import json
import re
from dataclasses import dataclass, field
from typing import Mapping


class R06Hold(ValueError):
    pass


def sha(text: str) -> str:
    if not isinstance(text, str):
        raise R06Hold('source must be text')
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def nfm_content(fetched: str) -> str:
    a = fetched.find('<content>')
    z = fetched.rfind('</content>')
    if a < 0 or z < a:
        raise R06Hold('fetch has no complete editable content; possible async/blank/truncated')
    return fetched[a + len('<content>'):z]


PAGE_TAG = re.compile(r'<page url="https://app\.notion\.com/p/([0-9a-f]{32})"[^>]*>([^<]+)</page>')
NOTION_URL = re.compile(r'https://app\.notion\.com/p/[0-9a-f]{32}')
FILE_TAG = re.compile(r'notion-file-block://([0-9a-f-]{36})/([0-9a-f-]{36})(\?[^)\s"<>]+)?')
MEDIA_TAG = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')


def canonical_duplicate_body(body: str) -> str:
    """Normalize ONLY IDs that native Notion duplication is expected to remap."""
    return NOTION_URL.sub('https://app.notion.com/p/COPIED',
        FILE_TAG.sub(lambda m: 'notion-file-block://COPIED/' + m.group(2) + (m.group(3) or ''), body))


def media_manifest(body: str) -> list[dict]:
    return [{'block_id': m.group(1), 'file_id': m.group(2),
             'query': m.group(3) or '', 'filename': re.search(r'(?:^|&)name=([^&]+)', m.group(3) or '').group(1)
             if re.search(r'(?:^|&)name=([^&]+)', m.group(3) or '') else None}
            for m in FILE_TAG.finditer(body)]


def native_duplicate_parity(source: str, copy: str, *, original_id: str, clone_id: str,
                            source_title: str, clone_title: str) -> dict:
    if original_id == clone_id:
        raise R06Hold('duplicate cannot reuse original page ID')
    if not source_title.strip() or not clone_title.strip():
        raise R06Hold('page must be populated after asynchronous duplication')
    if '(1)' not in clone_title and '(TESTE' not in clone_title:
        raise R06Hold('page title does not indicate duplication; inspect')
    x, y = nfm_content(source), nfm_content(copy)
    if not x.strip() or not y.strip():
        raise R06Hold('blank clone still asynchronous: hold')
    norm_eq = canonical_duplicate_body(x) == canonical_duplicate_body(y)
    a, b = media_manifest(x), media_manifest(y)
    p, q = list(PAGE_TAG.finditer(x)), list(PAGE_TAG.finditer(y))
    same_img_data = [(v['file_id'], v['filename']) for v in a] == [(v['file_id'], v['filename']) for v in b]
    img_remapped = len(a) == len(b) and all(i['block_id'] != j['block_id'] for i,j in zip(a,b))
    page_remapped = len(p)==len(q) and all(i.group(1)!=j.group(1) and i.group(2)==j.group(2)
                                                   for i,j in zip(p,q))
    return {
      'state': 'SEMANTIC_PARITY' if norm_eq and same_img_data and img_remapped and page_remapped
                      else 'DIVERGENCE_HOLD',
      'original':original_id,'clone':clone_id, 'source_sha256':sha(x), 'clone_sha256':sha(y),
      'normalized_source_sha256':sha(canonical_duplicate_body(x)),
      'normalized_clone_sha256':sha(canonical_duplicate_body(y)),
      'image_references': len(a), 'child_page_blocks':len(p),
      'image_block_ids_new':img_remapped, 'file_upload_ids_retained':same_img_data,
      'child_page_ids_new':page_remapped, 'only_remappable_fields_changed':norm_eq,
      'title_is_test': '(TESTE' in clone_title,
      'allowed_to_mutate':False,
      'reason':'Cloned binary retention, writer, test title and native restore not all proven'
    }


def must_be_test_page(page_export: str, *,expected_id:str) -> dict:
    if not re.fullmatch(r'[0-9a-f-]{36}',expected_id):raise R06Hold('invalid test page ID')
    if f'/p/{expected_id.replace("-", "")}' not in page_export:
        raise R06Hold('fetched another page; source fence violation')
    title = re.search(r'"title":"([^"]+)"',page_export)
    if not title or '(TESTE' not in title.group(1):
        raise R06Hold('Never write unmarked duplicate or original')
    parent = re.search(r'<parent-page [^>]*title="([^"]+)"',page_export)
    if not parent or parent.group(1) != 'Teste':
        raise R06Hold('Test page outside isolated Teste parent')
    if 'TESTE ISOLADO' not in nfm_content(page_export):
        raise R06Hold('Synthetic test fixture disclaimer missing')
    return {'id':expected_id,'title':title.group(1),'parent':'Teste','fence':'PASS','writes_allowed':False}


@dataclass(frozen=True)
class FieldEdit:
    old:str
    new:str
    context:str=''


def plan_unique_edit(*,body:str, edit:FieldEdit, preimage_sha256:str) -> dict:
    if sha(body)!=preimage_sha256:raise R06Hold('stale preimage')
    if not edit.old.strip() or edit.old==edit.new:
        raise R06Hold('empty/no-op edit')
    n=body.count(edit.old)
    if n!=1:raise R06Hold(f'ambiguous field has {n} matches')
    if 'SAVE-' in edit.old or '</details>' in edit.old or '<page' in edit.old:
        raise R06Hold('Never edit saved historical toggle, file or child page references')
    updated=body.replace(edit.old,edit.new,1)
    return {'state':'PLAN_ONLY','expected_before_sha256':sha(body),'planned_after_sha256':sha(updated),
            'old_str':edit.old,'new_str':edit.new,'preserve_other_bytes':True,
            'write_allowed':False,'context':edit.context}


def verify_edit(*,before:str, after:str, edit:dict) -> dict:
    if sha(before)!=edit['expected_before_sha256']:raise R06Hold('wrong source before')
    if sha(after)!=edit['planned_after_sha256']:raise R06Hold('patch drift or unrelated change')
    expected=before.replace(edit['old_str'],edit['new_str'],1)
    if after!=expected:raise R06Hold('unintended differences')
    return {'state':'BYTE_EXACT_PATCH','after_sha256':sha(after),'only_one_change':True}


def verify_preimage_archive(*,before_body:str,after_save_body:str,archive_marker:str,
                            archive_text:str, assets_recreated:bool=False)->dict:
    if archive_marker in before_body:raise R06Hold('archive event already exists')
    if after_save_body.count(archive_marker)!=1:raise R06Hold('archive missing/duplicated')
    if not after_save_body.startswith(before_body):raise R06Hold('non-append-only save')
    if archive_text not in after_save_body:raise R06Hold('archive not exact bytes')
    inventory={'files':len(media_manifest(before_body)), 'pages':len(PAGE_TAG.findall(before_body)),
               'mentions':before_body.count('<mention-page ')}
    risks=sum(inventory.values())
    return {'state':'READBACK_NATIVE_EVIDENCE_HOLD' if risks and not assets_recreated else 'READBACK_TEXT_EQUAL',
            'original_sha256':sha(before_body),'inventory':inventory,
            'native_assets_fully_proven': bool(not risks or assets_recreated),
            'write_allowed':False}


@dataclass
class EventJournal:
    actor_id:str
    event_id:str
    initial_sources:dict[str,str]
    state:str='DISCOVERED'
    evidence:list[dict]=field(default_factory=list)
    saved_sources:dict[str,str]=field(default_factory=dict)
    current_sources:dict[str,str]=field(default_factory=dict)
    uncertain:bool=False

    def _gate(self):
        if self.uncertain:raise R06Hold('UNKNOWN_EFFECT: must reopen and reconcile')
        if not self.event_id or not self.actor_id:raise R06Hold('event and actor identity required')
    def prepare(self):
        self._gate()
        if self.state!='DISCOVERED':raise R06Hold('bad transaction state')
        if len(self.initial_sources)!=len(set(self.initial_sources)) or not self.initial_sources:
            raise R06Hold('empty or ambiguous source set')
        if any(len(v)!=64 for v in self.initial_sources.values()):
            raise R06Hold('full SHA256 for every source required')
        self.state='PREPARED';self.evidence.append({'phase':'PREPARED','sources':len(self.initial_sources)})
    def witnessed_save(self,page_id:str,observed_source_sha:str):
        self._gate()
        if self.state not in ('PREPARED','SAVING'):raise R06Hold('save out of order')
        if self.initial_sources.get(page_id)!=observed_source_sha:
            raise R06Hold('save does not match the source snapshot')
        if page_id in self.saved_sources:raise R06Hold('duplicate save event')
        self.saved_sources[page_id]=observed_source_sha
        self.state='SAVING';self.evidence.append({'phase':'SAVED','page_id':page_id})
    def authorize_patch_candidate(self):
        self._gate()
        if self.state!='SAVING' or self.saved_sources!=self.initial_sources:
            raise R06Hold('all pages in paired operation require verified saves')
        self.state='READY_TO_PROPOSE';self.evidence.append({'phase':'PAIR_SAVED'})
        return {'candidate_only':True,'writer_authorized':False}
    def report_unknown(self,what:str):
        self.uncertain=True;self.evidence.append({'phase':'UNKNOWN_EFFECT','what':what})
    def reconcile(self,*,observed:str,proof:str):
        if not self.uncertain or observed not in ('PRESENT','ABSENT') or len(proof)<8:
            raise R06Hold('insufficient proof of unknown-effect reconciliation')
        self.uncertain=False
        if observed=='PRESENT':
            self.state='RECONCILED_PRESENT_HOLD'
            # A positive readback is not permission to reapply the operation.
        self.evidence.append({'phase':'RECONCILED','observed':observed,'proof':proof})


def confirmation_gate(*,player_reply:str|None,charted_rate:float|None,
                      attributed_components:Mapping[str,float],reconciled:bool=False)->dict:
    if player_reply is None or not str(player_reply).strip():
        return {'state':'PLAYER_CONFIRMATION_HOLD','safe_to_allocate':False}
    if charted_rate is None:
        return {'state':'CANON_RATE_MISSING_HOLD','safe_to_allocate':False}
    try:actual=float(player_reply.replace(',','.'))
    except (ValueError,TypeError):return {'state':'PLAYER_REPLY_AMBIGUOUS_HOLD','safe_to_allocate':False}
    if actual<0 or not float(actual).is_integer() and actual*2%1:
        return {'state':'RATE_FORMAT_HOLD','safe_to_allocate':False}
    total=sum(attributed_components.values())
    if abs(total-charted_rate)>0.00001:
        return {'state':'SOURCE_COMPONENT_MISMATCH_HOLD','safe_to_allocate':False}
    if abs(actual-charted_rate)>0.00001:
        return {'state':'PLAYER_CANON_DIVERGENCE_HOLD','safe_to_allocate':False}
    if not reconciled:
        return {'state':'PENDING_PLAYER_AND_MASTER_RECONCILIATION','safe_to_allocate':False}
    return {'state':'RATE_CONFIRMED','rate_per_level':actual,'safe_to_allocate':False,
            'note':'writer and full transaction gate independent'}


def validate_transform_vitals(normal_hp:int, normal_pa:int, transformed_hp:int, transformed_pa:int,
                              normal_hp_current:int, normal_pa_current:int)->dict:
    values=[normal_hp,normal_pa,transformed_hp,transformed_pa,normal_hp_current,normal_pa_current]
    if any(not isinstance(v,int) or v<0 for v in values):raise R06Hold('negative/noninteger vital')
    if normal_hp_current>normal_hp or normal_pa_current>normal_pa:
        raise R06Hold('actual resources higher than their normal maxima')
    return {'spirit_hp_shield':max(0,transformed_hp-normal_hp),'spirit_pa_bonus':max(0,transformed_pa-normal_pa),
            'normal_hp_current_preserved':normal_hp_current,'normal_pa_current_preserved':normal_pa_current,
            'fixed_d12':7,'requires_valid_activation_event':True}


def audit_player_safe_report(report:dict)->dict:
    forbidden = {'BAP','TAP_SECRET','SOURCE_BESTA','GM_NOTES','MESTRE_ONLY','hidden_formula',
                 'writer','lease','epoch','fencing','notion_page_id'}
    def walk(obj,path=''):
        if isinstance(obj,dict):
            for key,val in obj.items():
                if str(key) in forbidden or str(key).upper().startswith('BAP_'):
                    raise R06Hold('unsafe field in player report: '+path+'/'+str(key))
                walk(val,path+'/'+str(key))
        elif isinstance(obj,list):
            for i,val in enumerate(obj):walk(val,path+'/'+str(i))
        elif isinstance(obj,str) and re.search(r'\b(?:BAP|MESTRE.ONLY|WRITER.EPOCH)\b',obj,re.I):
            raise R06Hold('unsafe content in player report: '+path)
    walk(report)
    required={'personagem','nivel_antes','nivel_depois','ganhos_atributos','vida','alma'}
    missing=required-set(report)
    if missing:raise R06Hold('missing report fields '+','.join(sorted(missing)))
    return {'state':'PLAYER_SAFE_SCHEMA_CANDIDATE','write_or_send_allowed':False,'fields':len(report)}


def invariant_gate(event:dict)->dict:
    if event.get('attempts',0)<1 or not event.get('synthetic_fixture',False):
        raise R06Hold('Only finite synthetic reproducible scenarios')
    if event.get('source_original_modified') or event.get('party_modified'):
        raise R06Hold('Original/Party mutation detected')
    return {'state':'SYNTHETIC_ONLY','reproducible':bool(event.get('seed') is not None)}



def native_duplicate_strict(source: str, copy: str, *,
                            verified_extra_remaps: Mapping[str,str]|None=None)->dict:
    """Only normalize remaps with known ownership: native child blocks and
    independently verified extra mentions. Different external links are a HOLD.
    This is stronger than the permissive early-discovery comparison.
    """
    old=nfm_content(source).strip();new=nfm_content(copy).strip()
    children_a=list(PAGE_TAG.finditer(old));children_b=list(PAGE_TAG.finditer(new))
    if len(children_a)!=len(children_b):raise R06Hold('child count changed')
    mapping={}
    for a,b in zip(children_a,children_b):
        if a.group(2)!=b.group(2):raise R06Hold('child title changed')
        if a.group(1)==b.group(1):raise R06Hold('child page has not been independently duplicated')
        if a.group(1) in mapping and mapping[a.group(1)]!=b.group(1):
            raise R06Hold('inconsistent child remap')
        mapping[a.group(1)]=b.group(1)
    images_a=media_manifest(old);images_b=media_manifest(new)
    if len(images_a)!=len(images_b):raise R06Hold('media count changed')
    asset_mapping={}
    for a,b in zip(images_a,images_b):
        if a['file_id']!=b['file_id'] or a['query']!=b['query']:
            raise R06Hold('file identity or metadata changed')
        if a['block_id']==b['block_id']:
            raise R06Hold('media block ID was not duplicated')
        asset_mapping[a['block_id']]=b['block_id']
    unknown=verified_extra_remaps or {}
    if not all(re.fullmatch(r'[0-9a-f]{32}',k) and re.fullmatch(r'[0-9a-f]{32}',v)
               for k,v in unknown.items()):raise R06Hold('extra map must contain validated IDs')
    if set(unknown)&set(mapping):raise R06Hold('extra remap duplicates known native child')
    page_map={**mapping,**unknown}
    # Replace only known source page IDs, never an unrelated reference.
    rewritten=NOTION_URL.sub(lambda m:'https://app.notion.com/p/'+
          page_map.get(m.group(0).rsplit('/',1)[1],m.group(0).rsplit('/',1)[1]),old)
    rewritten=FILE_TAG.sub(lambda m:'notion-file-block://'+asset_mapping.get(m.group(1),m.group(1))+'/'+m.group(2)+(m.group(3) or ''),rewritten)
    eq=rewritten==new
    idx=next((i for i,(a,b) in enumerate(zip(rewritten,new)) if a!=b),min(len(rewritten),len(new))) if not eq else None
    return {'state':'STRICT_SEMANTIC_PARITY' if eq else 'UNVERIFIED_REMAP_HOLD',
            'native_child_mapping_count':len(mapping),'witnessed_extra_mappings':len(unknown),
            'remapped_media_blocks':len(asset_mapping), 'only_expected_remaps':eq,
            'first_unexplained_diff_offset':idx,'native_binary_independence_proven':False,
            'write_allowed':False}
