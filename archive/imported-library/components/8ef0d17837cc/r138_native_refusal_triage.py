"""R138 actual response classification and policy respecting blocker. No Notion caller.
Never repeat security refusals with alternate syntax, target, or account.
"""
from __future__ import annotations
from dataclasses import dataclass
import json
class Hold(ValueError): pass
SECURITY_TEXT='Esta ferramenta foi bloqueada pelas configurações de segurança da OpenAI. Verifique novamente o que está enviando.'
@dataclass(frozen=True)
class NativeAttempt:
    tx:str;stage:str;target:str;operation:str;before_version:str;requested_change:str
    original_error:str|None; response_payload:str|None; readback_before:bool; readback_after:bool; readback_other:bool

def diagnose(a:NativeAttempt):
    if a.readback_other or sum((a.readback_before,a.readback_after,a.readback_other))!=1:
        return {'class':'UNKNOWN_EFFECT','policy':'STOP_AND_QUARANTINE','retry':False}
    if a.original_error and 'bloqueada pelas configurações de segurança da OpenAI' in a.original_error:
        return {'class':'SAFETY_POLICY_REFUSAL_OBSERVED','technical_inner_cause':'NOT_DISCLOSED_BY_TOOL',
                'observed_effect':'BEFORE' if a.readback_before else 'AFTER',
                'policy':'NO_RETRY_NO_ALTERNATE_FORMAT_NO_TARGET_SWITCH_FOR_REFUSED_EFFECT',
                'retry':False}
    if a.original_error:
        return {'class':'UNDETERMINED_TOOL_ERROR','effect':'BEFORE' if a.readback_before else 'AFTER','retry':False}
    if a.response_payload and a.readback_after:
        return {'class':'WRITE_RESPONSE_AND_AFTER_OBSERVED','policy':'PROCEED_JOURNAL_WITH_CAUSAL_RECEIPT','retry':False}
    return {'class':'MISSING_CAUSAL_EVIDENCE','retry':False}

def safe_plan(a:NativeAttempt):
    d=diagnose(a)
    if d.get('class')=='SAFETY_POLICY_REFUSAL_OBSERVED':
        return {'decision':'HOLD_SECURITY_REFUSAL','actor_page':a.target,'write_set':[],
                'future_action':'ONLY_WITH_NEW_EXPLICIT_TOOL_AUTHORIZATION_OR_DIAGNOSABLE_NON_SECURITY_VALIDATION_FAILURE',
                'difference_from_accepted_precedents':'NOT_CAUSALLY_IDENTIFIED'}
    if d.get('class')=='WRITE_RESPONSE_AND_AFTER_OBSERVED':return {'decision':'READBACK_JOURNAL_CANDIDATE','write_set':['JOURNAL_ONLY']}
    return {'decision':'HOLD','write_set':[]}

def main():
    x=NativeAttempt('R129','NORMAL','R129','notion_update_page','v0','PHASE_NORMAL: INTENT_PREPARED -> WRITE_DISPATCHED',SECURITY_TEXT,None,True,False,False)
    y=NativeAttempt('R130','D','R130','notion_update_page','v2','JSON stage C->D',SECURITY_TEXT,None,True,False,False)
    pos=NativeAttempt('R135','STRUCT_FIELDS','R135','notion_update_page','v1','4 targeted fields',None,'{"page_id":"..."}',False,True,False)
    a,b,c=diagnose(x),diagnose(y),diagnose(pos)
    assert a['class']=='SAFETY_POLICY_REFUSAL_OBSERVED' and a['observed_effect']=='BEFORE'
    assert b['class']=='SAFETY_POLICY_REFUSAL_OBSERVED' and b['retry'] is False
    assert c['class']=='WRITE_RESPONSE_AND_AFTER_OBSERVED'
    assert safe_plan(x)['write_set']==[] and safe_plan(y)['decision']=='HOLD_SECURITY_REFUSAL'
    assert diagnose(NativeAttempt('OTHER','N','X','U','v','s',None,None,False,False,True))['class']=='UNKNOWN_EFFECT'
    assert diagnose(NativeAttempt('OTHER','N','X','U','v','s',None,None,False,False,False))['class']=='UNKNOWN_EFFECT'
    return {'R129':a,'R130':b,'R135':c,'security_compliance':'NO_RETRY_WITHOUT_NEW_EVIDENCE',
            'technical_root_cause':'NOT_VISIBLE_FROM_POLICY_REFUSAL_TEXT'}
if __name__=='__main__':print(json.dumps(main(),ensure_ascii=False,indent=2))
