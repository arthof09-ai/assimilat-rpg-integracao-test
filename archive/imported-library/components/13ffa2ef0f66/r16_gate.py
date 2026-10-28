"""R16 additive canon correction: transformation is not usable before Prata 1.

The R13/R14 engine remains byte-identical to the historical ZIP. This module
wraps that engine, never writes Notion, and refuses unsupported real actors.
The Bronze pre-unlock accounting of TAP is NOT promoted to canon here; the
old R13 Bronze 2->3 receipt is archived as a mathematical-only fixture.
"""
from __future__ import annotations
import copy
from typing import Any
from engine_r13 import (ATTRS, RulePending, rank, addattrs, ff, plan as legacy_plan,
                        _derived_normal, _derived_transform, validate_state,lock_value)

FIRST_TRANSFORM_LEVEL = 6

class TransformationLocked(RulePending):
    pass


def access(level:int)->dict[str,Any]:
    _,star,tier=rank(level)
    enabled=level>=FIRST_TRANSFORM_LEVEL
    return {'level':level,'tier':tier,'star':star,
            'can_activate_transformation':enabled,
            'effective_bonus_access': 'REQUIRES_VALID_ACTIVATION' if enabled else 'DENIED_BRONZE',
            'rule_source':'DECISAO_DIRETA_MESTRE_2026-10-09',
            'interactions':'T9-A_SCENE_AND_REST_GATES' if enabled else 'NOT_APPLICABLE'}


def authorize_activation(level:int, *, scene_id:str|None, rested:bool|None,
                         used_scene:bool|None, prior_activation:bool=False):
    """Eligibility check only, never spends PA or activates anything."""
    if level < FIRST_TRANSFORM_LEVEL:
        raise TransformationLocked('Bronze 1-5: transforming is forbidden, even with an assimilated spirit')
    if not scene_id or used_scene is not False or (prior_activation and rested is not True):
        raise TransformationLocked('Prata+: T9-A scene/rest evidence incomplete; no activation')
    return {'eligible_to_begin_activation_check':True,'pa_payment':'PENDING_T6B_PRIORITY','not_activated':True}


def prata_fixture()->dict:
    """Entirely invented Prata 1 (ordinal 6) fixture, not a historical character.

    Normal baseline uses the official Human +2 rate and fixed 60% (d8=5).
    Spirit overlay is a synthetic hypothetical from 12 BAP per level; no
    disclosure of this number occurs in player messages. The form is INACTIVE.
    """
    init=dict(zip(ATTRS,[5,5,4,4,4,3]))
    attrs=dict(zip(ATTRS,[9,7,6,5,4,4]))  # 25 initial + (6-1)*2 = 35
    hp=14+6*(5+6)  # Prata d8 fixed 5, CON 6
    pa=14+6*(5+5)  # Prata d8 fixed 5, INT 5
    normal={'id':'SYNTH-R16-PRATA-ONLY','fixture_only':True,'race':'Humano','level':6,
            'normal_rate':2,'progression_confirmed':'SYNTHETIC_EXPLICIT',
            'initial_attrs':init,'attrs':attrs,'hp_initial':14,'pa_initial':14,
            'hp_natural':hp,'pa_natural':pa,'hp_permanent':0,'pa_permanent':0,
            'hp_current':49,'pa_current':42,'pa_committed':5,'hp_max':hp,'pa_max':pa,
            'pa_free':pa-5,'pa_spendable_now':37,'armor':2,'magic_prof':2,'luta_prof':2,
            'magic_cd_other':0,'weapon_damage_base_fixture':4,
            'hp_growth_mode':'60_PERCENT_FIXED','pa_growth_mode':'60_PERCENT_FIXED',
            'titles':[],'title_credits':{},'history':['R16 fictional baseline Prata 1; not historical'],
            'untouched':{'inventory':['ficcao'],'child_pages':['notion-independent:pending'],
                         'historical_session':None}}
    # 12 * 6 / 2 = 36 synthetic own Spirit points, restricted to FOR and CON.
    overlay=dict(zip(ATTRS,[18,0,18,0,0,0]))
    tattrs=addattrs(attrs,overlay)
    transform={'id':'SYNTH-R16-PRATA-ONLY','fixture_only':True,'effective_level':6,
             'spirit':{'id':'SPIRIT-SIMULATED-R16','bap':12,'cap':10,
                       'allowed_attrs':['FOR','CON'],
                       'abilities':['Rugido inventado (TESTE)','Couraca inventada (TESTE)']},
             'overlay':overlay,'attrs':tattrs,'tap_carry_half_units':0,
             'hp_theoretical_natural':14+6*(6+tattrs['CON']), # d10 60% 6
             'pa_theoretical_natural':14+6*(6+tattrs['INT']),
             'hp_bonus_max':0,'pa_bonus_max':0,
             'hp_bonus_current':0,'pa_bonus_current':0,
             'abilities_active':['Rugido inventado (TESTE)','Couraca inventada (TESTE)'],
             'activation_state':'INACTIVE_NO_T6B_REFRESH',
             'history':['R16 fictitious Prata 1; previous licensed activation occurred in simulated history; form now INACTIVE'],
             'untouched':{'media_independence':'PENDING'}}
    locks={'id':'SYNTH-R16-PRATA-ONLY','fixture_only':True,
           'milestones':{
                '1':{'type':'CA','rolls':[2],'first_source':'R16-SYNTH-PRIOR'},
                '2':{'type':'DANO','rolls':[3],'first_source':'R16-SYNTH-PRIOR'},
                '3':{'type':'VIDA','rolls':[2,3],'first_source':'R16-SYNTH-PRIOR'},
                '4':{'type':'CA','rolls':[4],'first_source':'R16-SYNTH-PRIOR'},
                '5':{'type':'DANO','rolls':[1],'first_source':'R16-SYNTH-PRIOR'}},
           'history':['FF locks 1..5 were achieved in earlier synthetic Prata1 activation; not automatically granted now']}
    _derived_normal(normal,locks['milestones'])
    _derived_transform(normal,transform,locks['milestones'])
    state={'NORMAL':normal,'TRANSFORM':transform,'LOCKS':locks}
    validate_state(state)
    return state


def choices_prata_single():
    return {'target_level':7,'normal_allocations':{'7':{'FOR':2}},
            'spirit_allocations':{'7':{'FOR':3,'CON':3}},
            'milestones':{},
            'resource_choice':'60_PERCENT_FIXED','actor':'SIMULATED_TEST_AGENT',
            'approval':'OFFLINE_SYNTHETIC_ONLY'}


def plan_prata(state:dict,choices:dict,event_id:str)->dict:
    """Reuses R13 growth, but defers milestone locks from INACTIVE hypothetical form.

    R13 expects a choice for *every* hypothetical transformed FF boundary. For
    an inactive form, staging-only dummy data is used internally to allow the
    historical pure planner to calculate the values. These synthetic dummies
    are NEVER granted, persisted or exposed as a human choice; new FF locks
    are retained only if physically reachable by an active verified state.
    """
    if state['NORMAL']['level']<FIRST_TRANSFORM_LEVEL:
        raise TransformationLocked('R13 Bronze overlay is not a playable transformation')
    if not access(choices['target_level'])['can_activate_transformation']:
        raise TransformationLocked('Prata1 required')
    if state['TRANSFORM'].get('activation_state')!='INACTIVE_NO_T6B_REFRESH':
        raise RulePending('R16 currently supports only inactive-form levelup; active proof integration pending')
    # Fail closed on absent or nonsynthetic decisions before staging.
    if choices.get('approval')!='OFFLINE_SYNTHETIC_ONLY' or choices.get('actor')!='SIMULATED_TEST_AGENT':
        raise RulePending('real-world approval is not available')
    old_level=state['NORMAL']['level'];target=choices['target_level']
    if target<=old_level:raise RulePending('target not ahead')
    for lv in range(old_level+1,target+1):
        if str(lv) not in choices.get('normal_allocations',{}):
            raise RulePending('normal allocation missing')
        if str(lv) not in choices.get('spirit_allocations',{}):
            raise RulePending('Spirit distribution missing or not explicitly empty')
    staged=copy.deepcopy(choices)
    staged.setdefault('milestones',{})
    existing=set(state['LOCKS']['milestones'])
    total_add=0
    for allocations in ('normal_allocations','spirit_allocations'):
        for a in choices.get(allocations,{}).values():
            if isinstance(a,dict):total_add+=sum(v for v in a.values() if type(v) is int and v>0)
    upper=(max(ff(state['NORMAL']['attrs']),ff(state['TRANSFORM']['attrs']))+10*total_add)//100
    internal_placeholders=[]
    for milestone in range(1,upper+1):
        k=str(milestone)
        if k not in existing and k not in staged['milestones']:
            staged['milestones'][k]={'type':'DANO','rolls':[1]}
            internal_placeholders.append(k)
    p=legacy_plan(state,staged,event_id)
    before=p['before'];after=p['updates']
    if after['TRANSFORM'].get('activation_state')!='INACTIVE_NO_T6B_REFRESH':
        raise RulePending('levelup tried to activate form')
    for key in ('hp_current','pa_current'):
        if before['NORMAL'][key]!=after['NORMAL'][key]:
            raise RulePending('normal HP/PA must not recover')
    for key in ('hp_bonus_current','pa_bonus_current'):
        if before['TRANSFORM'][key]!=after['TRANSFORM'][key]:
            raise RulePending('T6-B bonus refresh requires separate activation')
    normal_ceiling=ff(after['NORMAL']['attrs'])//100
    new_locks=set(after['LOCKS']['milestones'])-existing
    deferred=[]
    for k in sorted(new_locks,key=int):
        if int(k)>normal_ceiling:
            deferred.append(k)
            del after['LOCKS']['milestones'][k]
        elif k in internal_placeholders:
            raise RulePending('new actual FF milestone lacked a human choice; refuse staged placeholder')
    # Never keep or report the internally staged roll as historical evidence.
    _derived_normal(after['NORMAL'],after['LOCKS']['milestones'])
    _derived_transform(after['NORMAL'],after['TRANSFORM'],after['LOCKS']['milestones'])
    for k,choice in after['LOCKS']['milestones'].items():
        if int(k)<1:raise RulePending('invalid FF milestone')
        lock_value(choice)
    if after['TRANSFORM']['attrs']!=addattrs(after['NORMAL']['attrs'],after['TRANSFORM']['overlay']):
        raise RulePending('invalid spiritual overlay')
    if sum(after['TRANSFORM']['overlay'].values()) != (
        after['TRANSFORM']['spirit']['bap']*after['TRANSFORM']['effective_level'])//2:
        raise RulePending('TAP checksum mismatch')
    p['choices']=copy.deepcopy(choices)
    p['diff']={k:{'before_sha256':__import__('r10_recovery').digest(before[k]),
                   'after_sha256':__import__('r10_recovery').digest(after[k])} for k in after}
    p['r16_classification']='SILVER_E2E_INACTIVE_FORM_NO_GHOST_FF_AWARDS'
    p['activation_eligibility']=access(target)
    p['deferred_until_actual_activation_ff_milestones']=deferred
    p['technical_milestone_placeholders_not_persisted']=True
    return p


def historical_r13_audit():
    return {'R13_Bronze2_to_Bronze3':'HISTORICAL_MATH_ONLY_NOT_PLAYABLE_FORM',
            'R13_original_files':'PRESERVED_UNMODIFIED',
            'Bronze_activation':'DENIED',
            'TAP_before_silver':'PENDING_INTERPRETATION_DO_NOT_AUTOMATE_REAL'}
