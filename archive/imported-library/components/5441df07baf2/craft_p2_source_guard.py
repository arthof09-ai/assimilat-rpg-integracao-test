"""TEST-only complementary CRAFT source/lot reconciliation guard.

This is NOT an inscription runner, magic observer, recipe erratum, writer or canonical rule.
It applies conservative documentary constraints from the live P2/oil pages read on
2026-10-21; it never authorizes physical/in-game execution or stock/PA changes.
"""
from __future__ import annotations
import re
from typing import Any

P2_URL = 'https://app.notion.com/p/3edc2b324ede811783dfce62058ca6b8'
OIL_URL = 'https://app.notion.com/p/3edc2b324ede81f1a88ec69980ab6cfd'
OIL_HIST_URL = 'https://app.notion.com/p/75fc2b324ede83d492f881e556dc03f8'

P2_BOM = {
 'Argila de Elemental da Terra':3, 'Água Benta de Santuário':1,
 'Sal de Geodo Santo':2, 'Pó de Ferro de Meteoro':3,
 'Essência de Barreira Mística':1, 'Óleo de Vedação':1,
}
ENERGY_OPTIONS = {'Pedra da Luz':2, 'Pote de Essência Mágica':2}
# Official oil BOM as of 2026-10-21, not the old Party mirror version (2 iron).
OIL_OFFICIAL_BOM = {
 'Raiz de Mandrágora':1, 'Gota do Orvalho do Amanhecer':8,
 'Pó de Ferro Celestial':3, 'Essência de Lua Minguante':1,
}
OIL_HIST_IRON = 2


def _evidence(e:Any, fields:tuple[str,...])->bool:
    if not isinstance(e,dict):return False
    return all(isinstance(e.get(k),str) and e[k].strip() for k in fields)


def _lot(e:Any,minimum:int,finished:bool=False)->bool:
    req=('lot_id','custody','authenticity_sha256','provenance_ref') + (('quality_ref','product_identity') if finished else ())
    if not _evidence(e,req):return False
    if not isinstance(e.get('quantity'),(float,int)) or isinstance(e['quantity'],bool) or e['quantity']<minimum:return False
    return bool(re.fullmatch(r'[0-9a-fA-F]{64}',e['authenticity_sha256']))


def evaluate(data:dict)->dict:
    if not isinstance(data,dict):raise TypeError('Expected documentary-input dictionary')
    failures=[]
    salt=data.get('salt_decision')
    salt_value=salt.get('choice') if isinstance(salt,dict) else None
    if salt_value not in ('SANTO','ENCANTADO') or not _evidence(salt,('authority_decision_id','authority_ref')):
        failures.append('P2-SALT-01_NO_COMPETENT_DOCUMENTED_DECISION')
    energy=data.get('energy_decision')
    energy_choice=energy.get('choice') if isinstance(energy,dict) else None
    if energy_choice not in ENERGY_OPTIONS or not _evidence(energy,('authority_decision_id','authority_ref','process_step','activation_method')):
        failures.append('P2-ENERGY-02_NO_COMPETENT_PROCESS_DECISION')
    route=data.get('oil_route')
    if route not in ('FINISHED_LOT','MANUFACTURE'):
        failures.append('OIL_ROUTE_UNSET')
    elif route=='FINISHED_LOT':
        if not _lot(data.get('finished_oil_lot'),1,finished=True):
            failures.append('OIL_FINISHED_BATCH_WITH_TRACE_AND_QA_UNPROVEN')
    else:
        # Competing ingredient names, incomplete process and historical iron count
        # cannot be resolved by picking the convenient numeric variant.
        oil_dec=data.get('oil_manufacture_decision')
        if not _evidence(oil_dec,('authority_decision_id','authority_ref','complete_procedure_ref','bom_reconciliation_ref')):
            failures.append('OIL_RECIPE_CONFLICTS_UNRESOLVED')
        for item,quantity in OIL_OFFICIAL_BOM.items():
            if not _lot(data.get('oil_inputs',{}).get(item) if isinstance(data.get('oil_inputs'),dict) else None,quantity):
                failures.append('OIL_RAW_LOT_UNVERIFIED:'+item)
    source_lots=data.get('p2_inputs',{})
    if not isinstance(source_lots,dict):source_lots={}
    needed=dict(P2_BOM)
    # Oil is handled exclusively in its selected route to avoid double counting.
    needed.pop('Óleo de Vedação')
    if salt_value=='ENCANTADO':
        needed.pop('Sal de Geodo Santo');needed['Sal de Geodo Encantado']=2
    if energy_choice in ENERGY_OPTIONS:needed[energy_choice]=ENERGY_OPTIONS[energy_choice]
    for item,n in needed.items():
        if not _lot(source_lots.get(item),n):failures.append('P2_LOT_UNVERIFIED:'+item)
    coupon=data.get('parchment_coupon')
    if not _evidence(coupon,('specimen_id','origin_ref','qa_ref')):failures.append('PARCHMENT_PHYSICAL_SPECIMEN_UNVERIFIED')
    op=data.get('operator')
    if not _evidence(op,('operator_id','p2_competence_ref','appointment_ref')):failures.append('OPERATOR_P2_COMPETENCE_AND_ASSIGNMENT_UNVERIFIED')
    witnesses=data.get('witnesses',[])
    if not isinstance(witnesses,list) or len(witnesses)<2 or len(set(witnesses))<2 or any(not isinstance(x,str) or not x.strip() for x in witnesses):
        failures.append('TWO_DISTINCT_WITNESSES_NOT_ESTABLISHED')
    event=data.get('test_authority')
    if not _evidence(event,('decision_id','scope','evidence_ref')) or (isinstance(event,dict) and event.get('scope')!='H2-3A-PARCHMENT-TEST'):
        failures.append('TEST_EXECUTION_AUTHORITY_NOT_EVIDENCED')
    # Even complete input claims are not independently verified by a JSON dictionary.
    # A live qualified human/Notion readback is indispensable before any event.
    return {
        'source_set':{'p2':P2_URL,'oil_official':OIL_URL,'oil_historical_comparison_only':OIL_HIST_URL},
        'oil_official_iron':OIL_OFFICIAL_BOM['Pó de Ferro Celestial'],
        'oil_historical_iron_not_authority':OIL_HIST_IRON,
        'oil_route':route,
        'required_p2_lots':needed,
        'required_oil_raw_lots_if_manufacture':OIL_OFFICIAL_BOM if route=='MANUFACTURE' else {},
        'blocked_reasons':failures,
        'documentary_input_complete':not failures,
        'documentary_gate':'HOLD' if failures else 'CONDITIONAL_READBACK_REQUIRED',
        'authorization_to_apply':False,
        'magic_observed':False,
        'r48_action':'NONE',
        'pa_debit':'NONE',
        'note':'Completeness of asserted metadata is not verification of lot, competence, authority or magical effect.'
    }

if __name__=='__main__':
 import json,sys
 payload=json.load(sys.stdin)
 print(json.dumps(evaluate(payload),ensure_ascii=False,indent=2))
