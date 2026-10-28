"""TEST-only stateful R142/R143 controller using prior R131 T6-B/T9-A rules.
No canonical actor, Spirit or beast created. No published campaign dice or scene asserted.
Form theoretical maxima are derived from Rule5/T6, not copied as living beast HP/PA.
"""
from __future__ import annotations
from copy import deepcopy
import json
from r149_150_spirit_runtime import tier, Hold as TierHold
class Gate(ValueError):pass
FORM_DATA={'rank':'Prata 1','level':6,'normal_dice_fixed':5,'transform_dice_fixed':6,'base_hp':12,'base_pa':16,'CON':2,'INT':16,'BAP_SYNTH':2,'TAP_SYNTH':1,'spirit_cap_synth':6,'overlay_synth':{'SAB':6},'actor_id':'SYNTH-R142-01','spirit_id':'SYNTH-SPIRIT-R142-01'}

def derive(d):
 lv=d['level'];normal_hp=d['base_hp']+lv*(d['normal_dice_fixed']+d['CON']);normal_pa=d['base_pa']+lv*(d['normal_dice_fixed']+d['INT']);theor_hp=d['base_hp']+lv*(d['transform_dice_fixed']+d['CON']);theor_pa=d['base_pa']+lv*(d['transform_dice_fixed']+d['INT']);budget=d['TAP_SYNTH']*min(lv,d['spirit_cap_synth']);assert sum(d['overlay_synth'].values())==budget
 return {'normal_hp_max':normal_hp,'normal_pa_max':normal_pa,'theoretical_form_hp':theor_hp,'theoretical_form_pa':theor_pa,'spirit_hp_max':max(0,theor_hp-normal_hp),'spirit_pa_max':max(0,theor_pa-normal_pa),'budget':budget}

def initial():
 vals=derive(FORM_DATA)
 return {'identity':FORM_DATA,'derived':vals,'normal_hp':20,'normal_pa':110,'normal_pa_committed':20,'pa_gastavel_test_receipt':110,'item_temp_hp':10,'spirit_temp_hp':0,'spirit_pa':0,'form_active':False,'active_scene':None,'duration_remaining':0,'used_scenes':[],'last_used_scene':None,'rest_after_last_use':False,'activation_events':[],'history':[]}

def validate(s):
 if s['form_active'] and (s['spirit_temp_hp']<0 or s['spirit_pa']<0):raise Gate('NEGATIVE_RESERVE')
 if s['normal_pa']<0 or s['normal_hp']<0 or s['normal_pa_committed']<0:raise Gate('NEGATIVE_NORMAL')
 if s['pa_gastavel_test_receipt']>s['normal_pa']:raise Gate('SPENDABLE_ABOVE_CURRENT')
 return s

def activate(s,*,event,scene,duration_d6,action,actor_id,spirit_id,scene_test_authorized,source_mode):
 validate(s)
 if event in s['activation_events']:return deepcopy(s),'NOOP_ALREADY_ACTIVATED'
 if source_mode!='SYNTH_TEST_ONLY' or not scene_test_authorized:raise Gate('MISSING_SOURCE_SCENE_TEST_GATE')
 if actor_id!=s['identity']['actor_id'] or spirit_id!=s['identity']['spirit_id']:raise Gate('WRONG_ACTOR_OR_SPIRIT')
 try:spec=tier(s['identity']['level'])
 except TierHold:raise Gate('BRONZE_UNAVAILABLE')
 if s['identity']['rank'].rsplit(' ',1)[0]!=spec['category']:raise Gate('RANK_LEVEL_MISMATCH')
 action_table={'COMPLETA':'ACAO_COMPLETA','PADRAO':'ACAO_PADRAO','MOVIMENTO':'ACAO_MOVIMENTO','LIVRE':'ACAO_LIVRE'}
 if action!=action_table[spec['action']]:raise Gate('WRONG_ACTION')
 if type(duration_d6)!=int or not 1<=duration_d6<=spec['die']:raise Gate('DURATION_RECEIPT_MISSING')
 if s['form_active'] or scene in s['used_scenes']:raise Gate('USED_SCENE_OR_ACTIVE')
 if s['last_used_scene'] and not s['rest_after_last_use']:raise Gate('REST_REQUIRED')
 if not scene:raise Gate('SCENE_ID_REQUIRED')
 if s['normal_pa']-s['normal_pa_committed']<spec['cost']:raise Gate('COST_NOT_PAYABLE_TEST_CURRENT_MINUS_COMMITTED')
 a=deepcopy(s);a['normal_pa']-=spec['cost'];a['pa_gastavel_test_receipt']=min(a['pa_gastavel_test_receipt'],a['normal_pa']);a['spirit_temp_hp']=a['derived']['spirit_hp_max'];a['spirit_pa']=a['derived']['spirit_pa_max'];a['form_active']=True;a['active_scene']=scene;a['duration_remaining']=duration_d6+spec['offset'];a['used_scenes'].append(scene);a['last_used_scene']=scene;a['rest_after_last_use']=False;a['activation_events'].append(event);a['history'].append({'event':event,'kind':'ACTIVATE','scene':scene,'test_d6':duration_d6,'normal_pa_cost':spec['cost'],'spirit_hp_new':a['spirit_temp_hp'],'spirit_pa_new':a['spirit_pa']});return validate(a),'COMMITTED_CANDIDATE'

def synthetic_damage(s,points):
 if not s['form_active']:raise Gate('FORM_NOT_ACTIVE')
 if points<0:raise Gate('NEGATIVE_DAMAGE')
 a=deepcopy(s);remaining=points;sp=min(a['spirit_temp_hp'],remaining);a['spirit_temp_hp']-=sp;remaining-=sp;it=min(a['item_temp_hp'],remaining);a['item_temp_hp']-=it;remaining-=it;hp=min(a['normal_hp'],remaining);a['normal_hp']-=hp;remaining-=hp;a['history'].append({'kind':'SYNTHETIC_DAMAGE','input':points,'absorbed':{'spirit':sp,'item':it,'normal':hp,'overkill':remaining}});return validate(a)

def deactivate(s,*,event):
 if not s['form_active']:raise Gate('NOT_ACTIVE')
 a=deepcopy(s);a['form_active']=False;a['duration_remaining']=0;a['active_scene']=None;a['spirit_temp_hp']=0;a['spirit_pa']=0;a['history'].append({'event':event,'kind':'DEACTIVATE','normal_hp_persist':a['normal_hp'],'normal_pa_persist':a['normal_pa']});return validate(a)

def complete_rest(s,*,event,new_scene,rest_type,recorded_test_duration_h,independent_scene_test_authority):
 if s['form_active']:raise Gate('CANNOT_REST_ACTIVE')
 if not independent_scene_test_authority or rest_type not in ('SHORT','LONG') or (rest_type=='SHORT' and not (isinstance(recorded_test_duration_h,(int,float)) and 4<=recorded_test_duration_h<=6)):raise Gate('TEST_REST_NOT_CERTIFIED')
 if new_scene in s['used_scenes'] or not new_scene:raise Gate('MISSING_NEW_SCENE')
 a=deepcopy(s);a['rest_after_last_use']=True;a['history'].append({'event':event,'kind':'SYNTHETIC_REST_COMPLETED','hours_test':recorded_test_duration_h,'new_scene':new_scene,'normal_hp_unchanged':a['normal_hp'],'normal_pa_unchanged':a['normal_pa']});return validate(a)

def scenario():
 x=initial();a,gate=activate(x,event='R142-ACTIVATE-1',scene='SCENE-TEST-A',duration_d6=3,action='ACAO_COMPLETA',actor_id=x['identity']['actor_id'],spirit_id=x['identity']['spirit_id'],scene_test_authorized=True,source_mode='SYNTH_TEST_ONLY');assert gate=='COMMITTED_CANDIDATE'
 assert a['derived']=={'normal_hp_max':54,'normal_pa_max':142,'theoretical_form_hp':60,'theoretical_form_pa':148,'spirit_hp_max':6,'spirit_pa_max':6,'budget':6}
 assert a['normal_pa']==70 and a['spirit_temp_hp']==6
 try:activate(a,event='X',scene='SCENE-TEST-A',duration_d6=3,action='ACAO_COMPLETA',actor_id=x['identity']['actor_id'],spirit_id=x['identity']['spirit_id'],scene_test_authorized=True,source_mode='SYNTH_TEST_ONLY')
 except Gate:pass
 else:raise AssertionError('same scene reactivated')
 assert activate(a,event='R142-ACTIVATE-1',scene='SCENE-TEST-A',duration_d6=3,action='ACAO_COMPLETA',actor_id=x['identity']['actor_id'],spirit_id=x['identity']['spirit_id'],scene_test_authorized=True,source_mode='SYNTH_TEST_ONLY')[1]=='NOOP_ALREADY_ACTIVATED'
 b=synthetic_damage(a,12);assert b['spirit_temp_hp']==0 and b['item_temp_hp']==4 and b['normal_hp']==20
 c=deactivate(b,event='R143-END-A');assert c['normal_pa']==70
 try:activate(c,event='R143-ACTIVATE-2',scene='SCENE-TEST-B',duration_d6=2,action='ACAO_COMPLETA',actor_id=x['identity']['actor_id'],spirit_id=x['identity']['spirit_id'],scene_test_authorized=True,source_mode='SYNTH_TEST_ONLY')
 except Gate:pass
 else:raise AssertionError('no-rest scene allowed')
 d=complete_rest(c,event='R143-REST-TEST',new_scene='SCENE-TEST-B',rest_type='SHORT',recorded_test_duration_h=5,independent_scene_test_authority=True)
 e,gate=activate(d,event='R143-ACTIVATE-2',scene='SCENE-TEST-B',duration_d6=2,action='ACAO_COMPLETA',actor_id=x['identity']['actor_id'],spirit_id=x['identity']['spirit_id'],scene_test_authorized=True,source_mode='SYNTH_TEST_ONLY');assert e['normal_pa']==30 and e['spirit_temp_hp']==6 and e['spirit_pa']==6
 f=deactivate(e,event='R143-END-B');assert f['normal_pa']==30 and f['normal_hp']==20
 return [{'label':label,'state':obj} for label,obj in [('PRE',x),('A_ACTIVATE_TEST',a),('B_SYNTH_DAMAGE',b),('C_DEACTIVATE',c),('D_REST_TEST',d),('E_SECOND_SCENE_ACTIVATE',e),('F_DEACTIVATE_SECOND',f)]]
if __name__=='__main__':
 seq=scenario();print(json.dumps({'status':'PASS_TEST_ONLY','steps':[(r['label'],r['state']['normal_pa'],r['state']['spirit_temp_hp'],r['state']['spirit_pa']) for r in seq],'not_campaign':True},ensure_ascii=False))
