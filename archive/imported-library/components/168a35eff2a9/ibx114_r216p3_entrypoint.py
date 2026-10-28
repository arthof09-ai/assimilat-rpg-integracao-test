"""Experimental entrypoint integrated with IBX-17 conversation engine.

Explicit-form selector → source version gate → existing calculation engine →
provisional preview / cancel / submit. No new engine, writer, or Notion action.
A transformed form's represented projection is accessible without pretending
it can be activated or that its spirit TAP is free.
"""
from __future__ import annotations
from ibx114_conversation_v2 import select_actor,actor_preview,make_id,ConversationGate
from ibx114_r216p3_provenance import compare_physical_readback


def run_exact_form_preview(*,actor:str,form_exact:str,natural_delta:dict,
                           action:str='PREVIEW',historical_test:bool=True,
                           page_version:str|None=None,visibility:str='MESTRE-SIDE')->dict:
    if visibility!='MESTRE-SIDE':raise ConversationGate('MASTER_ONLY_ROUTE_REQUIRED')
    if action not in ('PREVIEW','CANCEL','SUBMIT_FOR_APPROVAL'):
        raise ConversationGate('WRITE_OR_UNKNOWN_ACTION_NOT_SUPPORTED')
    selection=select_actor(actor,visibility=visibility)
    if form_exact not in selection['forms']:
        raise ConversationGate('EXACT_FORM_EXPLICIT_SELECTION_REQUIRED')
    if page_version is None or page_version!=selection['version']:
        raise ConversationGate('EXPECTED_SOURCE_VERSION_MISSING_OR_STALE')
    provenance=compare_physical_readback(actor,visibility=visibility)
    if not historical_test:
        # A same version without full current body revalidation is still not
        # approval to represent a LIVE authoritative final preview.
        raise ConversationGate('CURRENT_SOURCE_FULL_READBACK_AND_AUTHORITY_REQUIRED')
    selected_pair=None
    projection_class='STANDALONE'
    normal_cohort=form_exact
    for pair in selection['paired_forms']:
        if form_exact==pair['normal_form']:
            selected_pair=pair;projection_class='PAIRED_NORMAL';break
        if form_exact==pair['transformed_form']:
            selected_pair=pair;normal_cohort=pair['normal_form']
            projection_class='PAIRED_TRANSFORMED_REPRESENTED_NOT_ACTIVATED';break
    base=actor_preview(actor,normal_cohort,natural_delta,
      expected_page_version=page_version,action='PREVIEW')
    if projection_class=='STANDALONE':
        projection=base['result']
    else:
        key='transformed' if projection_class.startswith('PAIRED_TRANSFORMED') else 'normal'
        projection=base['result']['projections'][key]
        if projection['form_exact']!=form_exact:
            raise ConversationGate('PAIR_PROJECTION_FORM_ID_DRIFT')
    fingerprint=make_id({'operation':'IBX-17','actor':actor,'form_exact':form_exact,
     'source_version':page_version,'natural_delta':natural_delta,
     'projection_class':projection_class,'base_preview_sha256':base['preview_sha256']})
    status={'PREVIEW':'PREVIEW_FOR_HUMAN_REVIEW','CANCEL':'CANCELED',
            'SUBMIT_FOR_APPROVAL':'SUBMITTED_FOR_APPROVAL_NO_WRITE'}[action]
    answer={'operation':'IBX-17','order':'IBX-114','preview_mode':'SYNTHETIC_HISTORICAL_TEST',
      'actor':actor,'form_exact':form_exact,'source_version':page_version,
      'source_freshness':provenance['status'],
      'source_version_drift':provenance['source_drift'],
      'projection_class':projection_class,'status':status,
      'preview_sha256':fingerprint,'writes':0,'transaction_authorized':False,
      'personnel_approved_preview':False,'production':'HOLD',
      'alternate_forms_preserved':True,'rank_derived_change':'NOT_COMPUTED',
      'transform_activation':'NOT_INFERRED',
      'tap_budget_change':'UNTOUCHED',
      'source_authority':'SNAPSHOT_READONLY_WITH_CURRENT_VERSION_DISCLAIMER'}
    if selected_pair:
        answer['pair_context']={'normal':selected_pair['normal_form'],
          'transformed':selected_pair['transformed_form'],
          'availability':selected_pair['transform_availability'],
          'rank_status':selected_pair['rank_status']}
    if action!='CANCEL':
        answer['selected_form_projection']=projection
    return answer


def showcase()->dict:
    actor='NIEL';s=select_actor(actor);form=s['paired_forms'][0]['transformed_form']
    x=run_exact_form_preview(actor=actor,form_exact=form,natural_delta={'DES':1},
       page_version=s['version'],action='PREVIEW')
    y=run_exact_form_preview(actor=actor,form_exact=form,natural_delta={'DES':1},
       page_version=s['version'],action='CANCEL')
    z=run_exact_form_preview(actor=actor,form_exact=form,natural_delta={'DES':1},
       page_version=s['version'],action='SUBMIT_FOR_APPROVAL')
    if not(x['preview_sha256']==y['preview_sha256']==z['preview_sha256']):
        raise ConversationGate('TOKEN_DRIFT_FOR_SAME_REQUEST')
    return {'preview':x,'cancel':y,'submit':{'status':z['status'],'writes':z['writes']},
            'no_host_writer':True}
