"""LEVEL-UP-ENGINE IBX-17 / R188-R189 integrated vertical slice.
Reuses canonical R151 integrated progression and R185 chat parser; never authorizes native writes.
One fixture layout sourced from existing R99 TEST, not an official player sheet.
"""
from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass
import hashlib,json,re,sys,unicodedata
from pathlib import Path
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'core'/'runtime'))
sys.path.insert(0,str(root/'compat_runtime'))

import r151_integrated_progression as old
from r185_mobile_preview import rank_label

LAB='3fbc2b324ede804a95fafcb7b293c92c'
SOURCE_R99='3fbc2b324ede8191a5cdc34c720f2c29'
SOURCE_R99_VERSION='2026-10-16T21:42:47.998Z'
ATTRS=old.ATTRS
class VerticalHold(ValueError):pass

def canonical_hash(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def initial_test_state(*,fixture_id,fixture_parent=LAB,source_version=SOURCE_R99_VERSION):
    if fixture_parent!=LAB:raise VerticalHold('OUTSIDE_LAB')
    if not fixture_id:raise VerticalHold('MISSING_TARGET')
    return {
      'identity':{'fixture_id':fixture_id,'parent_id':LAB,'source_fixture':SOURCE_R99,'source_version':source_version,'scope':'LAB_TEST','provenance':'R99_ACTIVE_SYNTHETIC_FIELDS'},
      'normal':{'level':17,'rank':'Ouro Negro','natural_attrs':{'FOR':13,'DES':9,'CON':8,'INT':11,'SAB':6,'CAR':6},'hp_max':277,'hp_current':180,'pa_max':320,'pa_current':200,'pa_committed':20,'pa_free':300,'ff':300,'ca':18,'magic_cd':13,'luta':15,'attack_base_test':4,'attack_plus_ff_test':5,'ff_bonus_life':7,'ff_bonus_damage':1,'magic_prof':2,'armor':2,'normal_rate':2},
      'layers':{},
      'spirit_overlay':{'bap_synthetic':0,'cap_ordinal':16,'allocation':{},'distributed_total':0,'carry_numerator':0,'carry_denominator':1,'effective_level':16,'proposed_attribute_for_next_gain':None,'active':False,'abilities_active':[], 'hp_bonus_current':0,'hp_bonus_max':105,'pa_bonus_current':0,'pa_bonus_max':102},
      'permanent_milestones':{'1':{'type':'CA','rolls':[1]},'2':{'type':'DANO','rolls':[1]},'3':{'type':'VIDA','rolls':[4,3]}},
      'consumed_events':[], 'history':[],'status':'SOURCE_TEST_READ_ONLY'}

def validate_source(state):
    n=state['normal'];sp=state['spirit_overlay'];i=state['identity']
    if i['parent_id']!=LAB or i['source_fixture']!=SOURCE_R99:raise VerticalHold('SOURCE_SCOPE_MISMATCH')
    if n['rank']!=rank_label(n['level']).rsplit(' ',1)[0]:raise VerticalHold('RANK_LEVEL_MISMATCH')
    if n['ff']!=10*(n['natural_attrs']['FOR']+n['natural_attrs']['DES']+n['natural_attrs']['CON']):raise VerticalHold('FF_COMPOSITION_MISMATCH')
    if n['pa_free']!=n['pa_max']-n['pa_committed']:raise VerticalHold('PA_FREE_MISMATCH')
    if n['magic_cd']!=n['natural_attrs']['INT']+n['magic_prof']:raise VerticalHold('CD_COMPOSITION_MISMATCH')
    if sp['active']:raise VerticalHold('INACTIVE_FIXTURE_EXPECTED')
    return True

def parse_mobile(text):
    if not isinstance(text,str):raise VerticalHold('INPUT_MISSING')
    n=''.join(c for c in unicodedata.normalize('NFKD',text.lower()) if not unicodedata.combining(c))
    if re.search(r'\b(cancelar|cancela|desistir)\b',n):return {'intent':'CANCEL'}
    if re.search(r'\b(confirmo|pode aplicar|autorize|execute)\b',n):return {'intent':'CONFIRM_NO_HOST_ATTESTATION'}
    if re.search(r'\b(subir|subo|subi|passei|evoluir|upar)\b.*?\b(dois|duas|2)\b.*?\b(niveis|levels|level|nivel)\b',n):return {'intent':'LEVEL_UP','levels':2}
    if re.search(r'\b(subir|subo|subi|passei|evoluir|upar)\b.*?\b(um|1)\b.*?\b(niveis|levels|level|nivel)\b',n):return {'intent':'LEVEL_UP','levels':1}
    return {'intent':'UNKNOWN'}

def calculate(state,*,tx,per_level_allocations,mode='FIXED60_EXPLICIT'):
    validate_source(state)
    if len(per_level_allocations) not in (1,2):raise VerticalHold('LEVEL_COUNT_UNSUPPORTED_TEST')
    if len(set(f'{tx}-L{i}' for i in range(1,len(per_level_allocations)+1)))!=len(per_level_allocations):raise VerticalHold('DUPLICATE_TX')
    if state.get('consumed_events'):raise VerticalHold('NOT_FRESH_FIXTURE_EVENT')
    initial=deepcopy(state);work=deepcopy(state);steps=[]
    for idx,alloc in enumerate(per_level_allocations,1):
        if set(alloc)!=set(ATTRS) or any(type(v)!=int or v<0 for v in alloc.values()) or sum(alloc.values())!=work['normal']['normal_rate']:raise VerticalHold('ALLOCATION_INVALID')
        event=f'{tx}-L{idx}'
        oldlevel=work['normal']['level'];before=deepcopy(work['normal'])
        result=old.preview(work,event=event,allocation=alloc,mode=mode)
        if result.get('decision')!='PREVIEW_READY_TEST_ONLY':raise VerticalHold(result.get('decision','UNEXPECTED'))
        work=result['after'];n=work['normal'];n['pa_free']=n['pa_max']-n['pa_committed'];n['magic_cd']=n['natural_attrs']['INT']+n['magic_prof']
        # CA, Luta, attack etc remain unchanged only if relevant underlying inputs remain unchanged.
        if n['natural_attrs']['DES']!=before['natural_attrs']['DES']:raise VerticalHold('CA_RECALC_NOT_SOURCE_PROVEN_FOR_THIS_FIXTURE')
        if n['natural_attrs']['FOR']!=before['natural_attrs']['FOR']:raise VerticalHold('LUTA_RECALC_NOT_SOURCE_PROVEN_FOR_THIS_FIXTURE')
        if n['ff']!=before['ff']:raise VerticalHold('FF_LOCK_NEW_MILESTONE_REQUIRES_CHOICE')
        if work['spirit_overlay']['active']:raise VerticalHold('UNEXPECTED_SPIRIT_ACTIVATION')
        steps.append({'step':idx,'from':rank_label(oldlevel),'to':rank_label(n['level']),'allocation':alloc,'fixed60':old.FIXED[n['rank']],'changes':{key:{'before':before[key],'after':n[key]} for key in ('level','hp_max','hp_current','pa_max','pa_current','pa_free','ff','ca','magic_cd','luta')},'attributes_before':before['natural_attrs'],'attributes_after':deepcopy(n['natural_attrs']),'spirit_delta':result['spirit_increment']})
    changes={}
    for k in ('level','rank','natural_attrs','hp_max','hp_current','pa_max','pa_current','pa_committed','pa_free','ff','ca','magic_cd','luta','attack_base_test','attack_plus_ff_test','ff_bonus_life','ff_bonus_damage'):
        b=initial['normal'][k];a=work['normal'][k]
        changes[k]={'antes':b,'depois':a,'alterado':b!=a}
    return {'status':'COMPLETE_PREVIEW_TEST_NOT_APPLIED','tx':tx,'target':state['identity']['fixture_id'],'before_hash':canonical_hash(initial),'after_hash':canonical_hash(work),'source':state['identity'],'before':initial,'after':work,'steps':steps,'changes':changes,'permanent_milestones_unchanged':work['permanent_milestones']==initial['permanent_milestones'],'active_spirit_unchanged':False==work['spirit_overlay']['active'],'native_effects':0,'host_attestation':False,'party_safe':False,'authorization':'MESTRE_LAB_TEST_SCOPE_ONLY'}

def test_demo():
    s=initial_test_state(fixture_id='PLACEHOLDER_NEVER_FOR_NATIVE_WRITE')
    allocations=[{'FOR':0,'DES':0,'CON':0,'INT':2,'SAB':0,'CAR':0},{'FOR':0,'DES':0,'CON':0,'INT':0,'SAB':2,'CAR':0}]
    p=calculate(s,tx='IBX17-R190-VERTICAL-SANDBOX-EXAMPLE',per_level_allocations=allocations)
    assert p['after']['normal']['level']==19
    assert p['after']['normal']['hp_max']==307
    assert p['after']['normal']['pa_max']==360
    assert p['after']['normal']['pa_free']==340
    assert p['after']['normal']['magic_cd']==15
    assert p['after']['normal']['hp_current']==180 and p['after']['normal']['pa_current']==200
    assert p['after']['normal']['natural_attrs']['INT']==13 and p['after']['normal']['natural_attrs']['SAB']==8
    assert p['after']['normal']['ff']==300 and p['after']['normal']['ca']==18
    assert p['after']['spirit_overlay']['active'] is False
    assert parse_mobile('Quero subir dois níveis com este personagem')['levels']==2
    assert parse_mobile('cancelar')['intent']=='CANCEL'
    return p
if __name__=='__main__':
    p=test_demo()
    print(json.dumps({'status':p['status'],'target_levels':[s['to'] for s in p['steps']],'attributes':p['changes']['natural_attrs'],'Vida':p['changes']['hp_max'],'Alma':p['changes']['pa_max'],'CD':p['changes']['magic_cd'],'FF':p['changes']['ff'],'CA':p['changes']['ca'],'current_hp':p['changes']['hp_current'],'current_pa':p['changes']['pa_current'],'hash':p['after_hash']},ensure_ascii=False,indent=2))
