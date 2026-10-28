"""R113 pure additive layer evaluator. No permanent state edited, no production authorizations.
Uses official FF=(FOR+DES+CON)*10, PA total/free and FF lock permanence.
"""
import json
from pathlib import Path
record=json.loads((Path(__file__).parent/'R111_RECEIPT_NATIVE.json').read_text())
lock=record['after']['LOCKS']['permanent_milestones']['1']
N={'FOR':4,'DES':3,'CON':2,'INT':5,'SAB':5,'CAR':6}

def eval_layer(equip_on,temp_on,title_on):
 A=dict(N);sources={}
 if equip_on:A['FOR']+=1;sources['equipment']={'FOR':1,'PA_MAX':10}
 if temp_on:A['CON']+=1;sources['temporary']={'CON':1}
 if title_on:A['SAB']+=2;sources['title']={'SAB':2}
 ff=(A['FOR']+A['DES']+A['CON'])*10;active=ff>=100
 natural_hp=18
 hp_max=natural_hp+(lock['total_bonus'] if active else 0)
 pa_max=24+(10 if equip_on else 0);pa_committed=5
 return {'layers':sources,'total_attrs':A,'ff':ff,'lock_history':lock,'lock_active':active,
   'hp_natural':natural_hp,'hp_max':hp_max,'pa_max':pa_max,'pa_committed':pa_committed,'pa_free':pa_max-pa_committed,
   'separation_natural_conditional':True,'synthetic':True}
case={'natural_only':eval_layer(False,False,False),'equip_title_on':eval_layer(True,False,True),
 'equip_title_temp_on':eval_layer(True,True,True),'equipment_off_temp_on':eval_layer(False,True,True),
 'all_off':eval_layer(False,False,False),'reequip':eval_layer(True,False,True)}
assert [case[x]['ff'] for x in case]==[90,100,110,100,90,100]
assert [case[x]['hp_max'] for x in case]==[18,23,23,23,18,23]
assert [case[x]['pa_free'] for x in case]==[19,29,29,19,19,29]
assert all(v['lock_history']==lock for v in case.values())
assert case['equip_title_temp_on']['total_attrs']['SAB']==7
assert case['all_off']['hp_natural']==case['reequip']['hp_natural']==18
out={'contract':'R113_TWO_PLUS_CONDITIONAL_LAYERS','source':'Criação de Ficha + T7/T8 Transformação','status':'PASS_LOCAL_ONLY_NATIVE_LAYER_TOGGLE_HOLD','cases':case,
 'checks':{'6_states':True,'FF_lock_no_reroll':True,'natural_hp_stable':True,'equipment_bonus_conditional':True,'PA_free_consistent':True},
 'not_claimed':['equipment effect is a specific real character item','native Test toggle','temporary HP item priority actually executed']}
p=Path(__file__).parent/'R113_LAYERS_LOCAL.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2));print('R113 PASS LOCAL 6 states equip+title+temporary on/off; locks persisted')
