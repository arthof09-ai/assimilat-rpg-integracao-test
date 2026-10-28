"""Fail-closed source entry gate for Liu's Furia; DOES NOT execute effect."""
import json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
SOURCE='https://app.notion.com/p/0b4c2b324ede837cb6be818dc8e36010'
def gate(hp,pa,action_economy=None,duration=None):
 if hp>117:return {'legal':False,'reason':'FURIA_REQUIRES_HP_HALF_OR_LESS','pa_debit':0}
 if pa<12:return {'legal':False,'reason':'PA_INSUFFICIENT','pa_debit':0}
 if action_economy is None:return {'legal':False,'reason':'SOURCE_ACTION_ECONOMY_UNDOCUMENTED','pa_debit':0}
 if duration is None:return {'legal':False,'reason':'SOURCE_DURATION_UNDOCUMENTED','pa_debit':0}
 return {'legal':False,'reason':'NO_AUTHORITY_TO_INSERT_ACTION_OR_DURATION','pa_debit':0}
record={'source':SOURCE,'literal':'Quando sua vida chega na metade pode entrar em Furia: +15 FOR e +80 Vida; 12 PA','tests':[{'hp':235,'pa':73,'out':gate(235,73)},{'hp':117,'pa':11,'out':gate(117,11)},{'hp':117,'pa':73,'out':gate(117,73)},{'hp':117,'pa':73,'proposed_action':'MOVEMENT','proposed_duration':3,'out':gate(117,73,'MOVEMENT',3)}],'executed_activations':0,'assertion':'SOURCE_COST_AND_THRESHOLD_KNOWN_BUT_ACTION_DURATION_AND_HP_SEMANTICS_NOT_ADMITTED','not_claimed':'FURIA_ACTIVATED'}
(ROOT/'evidence/R192_ENERGY_ADMISSION.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
assert all(not t['out']['legal'] and t['out']['pa_debit']==0 for t in record['tests'])
print('R192_FAIL_CLOSED_GATES_PASS_4_OF_4_NO_PA_CONSUMED')
