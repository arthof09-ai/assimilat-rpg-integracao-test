"""Read-only orchestrator: three supported Notion sheet families, one engine.

Boundary intentionally stops before material Notion operations. It outputs a
concrete manifest which an approved worker can use after all legal/native gates.
"""
from __future__ import annotations
from typing import Any
from adapters_family_v05 import REGISTRY,identify,AdapterHold
from nfm_structure_v05 import page_body,root_toggles,archive_risk,digest
from save_snapshot_v05 import build_archive,save_append_only_preflight,SaveHold
from paired_plan_v05 import form_plan

class ServiceHold(ValueError): pass


def discover_all(page_by_profile:dict[str,str])->dict:
    expected=set(REGISTRY)
    unknown=set(page_by_profile)-expected
    if unknown:raise ServiceHold('Perfis desconhecidos: '+','.join(sorted(unknown)))
    results={}
    for name in sorted(page_by_profile):
        try:
            data=identify(name,page_by_profile[name])
            body=page_body(page_by_profile[name])
            risk=archive_risk(body)
            results[name]={'analysis':data,'native_assets':risk,'raw_page_sha256':digest(body)}
        except Exception as e:
            results[name]={'analysis':{'readiness':'HOLD','hold_reasons':[str(e)]}}
    return {'status':'READ_ONLY_DISCOVERY','profile_count':len(results),'profiles':results,
            'material_write_allowed':False}


def _pair_legacy(exported:str,profile_key:str,verified_current_heading:str|None):
    d=identify(profile_key,exported,verified_current_heading=verified_current_heading)
    if d['readiness']=='HOLD':raise ServiceHold('Identificação bloqueada: '+'; '.join(d['hold_reasons']))
    chosen=d['candidate_current']
    body=page_body(exported)
    matches=[x for x in d['versions'] if x['transformed'] and x['rank_from_title'] and
             x['rank_from_title']['code']==chosen['rank_from_title']['code']]
    if len(matches)!=1:raise ServiceHold(f'Par de transformação correspondente não é único: {len(matches)}')
    t=matches[0]
    if chosen['root_start']>=t['root_start']:
        raise ServiceHold('O par histórico não está ordenado Normal → Transformado')
    chunk=body[chosen['root_start']:t['root_end']]
    # Safeguard against a third root toggle in between.
    if len(root_toggles(chunk))!=2:raise ServiceHold('Há toggles extras entre estados normal/transformado')
    return d,chunk


def plan_before_edit(*,profile_key:str,normal_export:str,event_id:str,
                     verified_current_heading:str|None=None,spirit_export:str|None=None):
    if profile_key not in REGISTRY:raise ServiceHold('Perfil não encontrado')
    p=REGISTRY[profile_key]
    if p.family=='legacy':
        d,pre=_pair_legacy(normal_export,profile_key,verified_current_heading)
        a=build_archive(event_id=event_id,profile_key=profile_key,preimage=pre,
                        scope='paired-root-toggles',source_page_id=p.page_id,
                        candidate_level=d['candidate_current']['summary'])
        append=save_append_only_preflight(page_export_before=normal_export,candidate=a)
        risk=a['native_risks']
        return {'profile':profile_key,'form_mode':'LEGACY_PAIRED_TOGGLES','archives':[a],
                'append_preflights':[append],'risks':risk,'ready_for_real_edit':False,
                'next':'Verify native assets + permission then physical append and readback before edits'}
    normal=identify(profile_key,normal_export)
    body=page_body(normal_export)
    a=build_archive(event_id=event_id,profile_key=profile_key,preimage=body,
                    scope='full-page',source_page_id=p.page_id,
                    candidate_level=(normal['active_normal_rank'] or {}).get('code','RANK_UNVERIFIED'))
    candidates=[a]
    if spirit_export is None:
        return {'profile':profile_key,'form_mode':'CROSS_PAGE','archives':candidates,
                'risks':a['native_risks'],'ready_for_real_edit':False,
                'hold':'Espírito precisa da própria página snapshot/save antes de ambos edits'}
    sk=f'{p.family}-spirit'
    if sk not in REGISTRY:raise ServiceHold('Perfil do Espírito não cadastrado')
    target=REGISTRY[sk]
    sd=identify(sk,spirit_export)
    sp=page_body(spirit_export)
    b=build_archive(event_id=event_id,profile_key=sk,preimage=sp,scope='full-page',
                    source_page_id=target.page_id,candidate_level='FORM_SOURCE_VERIFIED_LATER')
    candidates.append(b)
    return {'profile':profile_key,'form_mode':'CROSS_PAGE','archives':candidates,
            'append_preflights':[save_append_only_preflight(page_export_before=normal_export,candidate=a),
                                 save_append_only_preflight(page_export_before=spirit_export,candidate=b)],
            'risks':a['native_risks']+b['native_risks'],
            'pair':form_plan(profile_key=p.family,normal_page=p.page_id,spirit_page=target.page_id),
            'ready_for_real_edit':False,'next':'Verify TWO native saves and policy gates before normal+spirit edits'}
