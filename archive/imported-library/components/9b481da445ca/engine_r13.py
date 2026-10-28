"""LEVEL-UP-ENGINE R13/R14 additive, OFFLINE synthetic evolution harness.
Preserves R10 module; has NO Notion write path or player authority.
Rules read 2026-10-09: Criação de Ficha Regra 2/4/5/6/7/10, Transformação T1-T8,
Sistema de Magia CD. Synthetic input choices are explicitly supplied, never inferred.
"""
from __future__ import annotations
import copy
from dataclasses import dataclass
from typing import Any
from r10_recovery import FakeStore, RecoveryController, digest, Crash, Conflict, export_journal

ATTRS=('FOR','DES','CON','INT','SAB','CAR')
RANKS=('Bronze','Prata','Ouro','Ouro Negro','Lendário')
NORMAL_DICE=(6,8,10,12,20)
FIXED={6:4,8:5,10:6,12:7,20:12,30:18,40:24,50:30,60:36}
DICE_CATEGORIES=(6,8,10,12,20,30,40,50,60)

class RulePending(ValueError):pass


def rank(level:int)->tuple[int,int,str]:
    if type(level) is not int or not 1<=level<=25:raise RulePending('level outside official 1..25')
    i=(level-1)//5
    return i,(level-1)%5+1,RANKS[i]


def bump_die(die:int,steps:int)->int:
    i=DICE_CATEGORIES.index(die)+steps
    if not 0<=i<len(DICE_CATEGORIES):raise RulePending('dice category outside normative table')
    return DICE_CATEGORIES[i]


def validate_attrs(a):
    if set(a)!=set(ATTRS) or any(type(v) is not int or v<0 for v in a.values()):
        raise RulePending('invalid attribute map')


def sumattrs(a):return sum(a.values())


def addattrs(a,b):return {k:a[k]+b.get(k,0) for k in ATTRS}


def ff(attrs):return (attrs['FOR']+attrs['DES']+attrs['CON'])*10


def lock_value(choice):
    kind=choice.get('type'); rolls=choice.get('rolls',[])
    if kind not in ('CA','DANO','VIDA'):raise RulePending('milestone choice missing')
    if not isinstance(rolls,list) or len(rolls)!=(2 if kind=='VIDA' else 1):
        raise RulePending('wrong FF dice count')
    sides=6 if kind=='VIDA' else 4
    if any(type(r) is not int or not 1<=r<=sides for r in rolls):
        raise RulePending('FF rolls outside dice bounds')
    return sum(rolls)


def milestone_stats(locks, ff_value):
    result={'CA':0,'DANO':0,'VIDA':0}
    for level,choice in locks.items():
        if int(level)*100<=ff_value:result[choice['type']]+=lock_value(choice)
    return result


def validate_state(pages):
    if set(pages)!= {'NORMAL','TRANSFORM','LOCKS'}:raise RulePending('must have three isolated synthetic pages')
    n,t,lk=pages['NORMAL'],pages['TRANSFORM'],pages['LOCKS']
    if n['fixture_only'] is not True or t['fixture_only'] is not True or lk['fixture_only'] is not True:
        raise RulePending('not marked synthetic fixture')
    if n['id'] != t['id'] or n['id']!=lk['id']:raise RulePending('identity mismatch')
    if n['race']!='Humano' or n['normal_rate']!=2 or n['progression_confirmed']!='SYNTHETIC_EXPLICIT':
        raise RulePending('unsupported race or unconfirmed progression')
    lv=n['level'];rank(lv)
    if t['effective_level']!=min(lv,t['spirit']['cap']):raise RulePending('effective level mismatch')
    if t['spirit']['bap']<0 or type(t['spirit']['bap']) is not int:raise RulePending('invalid synthetic BAP')
    if t.get('tap_carry_half_units',0) != (t['spirit']['bap']*t['effective_level'])%2:
        raise RulePending('TAP fractional carry mismatch')
    validate_attrs(n['attrs']);validate_attrs(t['overlay']);validate_attrs(t['attrs'])
    if sumattrs(t['overlay'])!=(t['spirit']['bap']*t['effective_level'])//2:
        raise RulePending('TAP checksum mismatch')
    if t['attrs']!=addattrs(n['attrs'],t['overlay']):raise RulePending('overlay mismatch')
    if n['hp_current']>n['hp_max'] or n['pa_current']>n['pa_max']:
        raise RulePending('invalid current normal resources')
    if n['pa_current']-n['pa_committed']<0:raise RulePending('negative spendable PA')
    if n['pa_free']!=n['pa_max']-n['pa_committed'] or n['pa_spendable_now']!=n['pa_current']-n['pa_committed']:
        raise RulePending('PA Livre = PA Total - comprometido; spendable separately')
    if t['hp_bonus_current']>t['hp_bonus_max'] or t['pa_bonus_current']>t['pa_bonus_max']:
        raise RulePending('bonus reserve over maximum')
    for k,choice in lk['milestones'].items():
        if int(k)<=0:raise RulePending('invalid milestone index')
        lock_value(choice)
    if set(range(1,ff(t['attrs'])//100+1)) - {int(k) for k in lk['milestones']}:
        raise RulePending('historical FF lock missing')
    return True


def _derived_normal(n, locks):
    bonus=milestone_stats(locks,ff(n['attrs']))
    n['hp_max']=n['hp_natural']+n['hp_permanent']+bonus['VIDA']
    n['pa_max']=n['pa_natural']+n['pa_permanent']
    n['pa_free']=n['pa_max']-n['pa_committed']
    n['pa_spendable_now']=n['pa_current']-n['pa_committed']
    n['derived']={'ff':ff(n['attrs']),'ca':6+n['attrs']['DES']+n['armor']+bonus['CA'],
                  'magic_cd':n['magic_prof']+n['attrs']['INT']+n['magic_cd_other'],
                  'ff_bonus_damage':bonus['DANO'],'ff_bonus_life':bonus['VIDA'],
                  'attack_dice_by_rank':rank(n['level'])[0]+1 if n['level']<=20 else 6,
                  'attack_bonus_luta_for':n['attrs']['FOR']+n['luta_prof'],
                  'weapon_damage_base_fixture':n['weapon_damage_base_fixture'],
                  'weapon_damage_plus_ff_fixture':n['weapon_damage_base_fixture']+bonus['DANO']}


def _derived_transform(n,t,locks):
    bonus=milestone_stats(locks,ff(t['attrs']))
    nb=milestone_stats(locks,ff(n['attrs']))
    normal_total=n['hp_natural']+n['hp_permanent']+nb['VIDA']
    transform_total=t['hp_theoretical_natural']+n['hp_permanent']+bonus['VIDA']
    t['hp_bonus_max']=max(0,transform_total-normal_total)
    t['pa_bonus_max']=max(0,t['pa_theoretical_natural']+n['pa_permanent']-n['pa_max'])
    t['derived']={'ff':ff(t['attrs']), 'ca':6+t['attrs']['DES']+n['armor']+bonus['CA'],
                  'magic_cd':n['magic_prof']+t['attrs']['INT']+n['magic_cd_other'],
                  'ff_bonus_damage':bonus['DANO'],'ff_bonus_life':bonus['VIDA'],
                  'weapon_damage_base_fixture':n['weapon_damage_base_fixture'],
                  'weapon_damage_plus_ff_fixture':n['weapon_damage_base_fixture']+bonus['DANO']}


def _touch_locks(locks,normal_attrs,trans_attrs,choices,source):
    ceiling=max(ff(normal_attrs),ff(trans_attrs))//100
    for i in range(1,ceiling+1):
        k=str(i)
        if k not in locks:
            if k not in choices:raise RulePending('new FF milestone lacks player choice: '+k)
            new=copy.deepcopy(choices[k]);lock_value(new)
            new['first_source']=source
            locks[k]=new


def make_fixture():
    """Explicitly invented test character. Not a character, NPC or Party record."""
    initial=dict(zip(ATTRS,[5,5,4,4,4,3]))
    current=dict(zip(ATTRS,[6,5,5,4,4,3]))
    normal={'id':'SYNTH-R13-ONLY','fixture_only':True,'race':'Humano','level':2,
            'normal_rate':2,'progression_confirmed':'SYNTHETIC_EXPLICIT',
            'initial_attrs':initial,'attrs':current,'hp_initial':14,'pa_initial':14,
            'hp_natural':23,'pa_natural':22,'hp_permanent':0,'pa_permanent':0,
            'hp_current':17,'pa_current':16,'pa_committed':3,'hp_max':23,'pa_max':22,
            'pa_free':19,'pa_spendable_now':13,'armor':2,'magic_prof':2,'luta_prof':2,'magic_cd_other':0,
            'weapon_damage_base_fixture':4,
            'hp_growth_mode':'60_PERCENT_FIXED','pa_growth_mode':'60_PERCENT_FIXED',
            'titles':[],'title_credits':{},'history':['R13 synthetic baseline Bronze 2'],
            'untouched':{'inventario':['marcador ficticio'], 'links':['synthetic://only'],
                         'historico_sintetico':['nenhuma sessao real']}}
    overlay=dict(zip(ATTRS,[6,0,6,0,0,0]))
    transformed={'id':'SYNTH-R13-ONLY','fixture_only':True,'effective_level':2,
                 'spirit':{'id':'SPIRIT-FICTIONAL-ONLY','bap':12,'cap':5,
                           'allowed_attrs':['FOR','CON'],
                           'abilities':['Rugido Sintético (não usado em campanha)','Couraça Sintética (não usada em campanha)']},
                 'overlay':overlay,'attrs':addattrs(current,overlay),'tap_carry_half_units':0,
                 'hp_theoretical_natural':46,'pa_theoretical_natural':32,
                 'hp_bonus_max':23,'pa_bonus_max':10,
                 'hp_bonus_current':12,'pa_bonus_current':8,
                 'abilities_active':['Rugido Sintético (não usado em campanha)'],
                 'history':['R13 synthetic baseline Bronze 2'],
                 'untouched':{'images':[{'media_state':'PENDING','src':'synthetic://not-real'}]}}
    locks={'id':'SYNTH-R13-ONLY','fixture_only':True,
           'milestones':{'1':{'type':'CA','rolls':[2],'first_source':'SYNTH-BEFORE'},
                         '2':{'type':'DANO','rolls':[3],'first_source':'SYNTH-BEFORE'}},
           'history':['FF milestones synthetic before R13']}
    _derived_normal(normal,locks['milestones']);_derived_transform(normal,transformed,locks['milestones'])
    out={'NORMAL':normal,'TRANSFORM':transformed,'LOCKS':locks}
    validate_state(out)
    return out


def make_choices_single():
    return {'target_level':3, 'normal_allocations':{'3':{'FOR':2}},
            'spirit_allocations':{'3':{'FOR':2,'CON':4}},
            'milestones':{'3':{'type':'DANO','rolls':[2]}},
            'resource_choice':'60_PERCENT_FIXED','actor':'SIMULATED_TEST_AGENT',
            'approval':'OFFLINE_SYNTHETIC_ONLY'}


def _validate_alloc(raw,expected,allowed=ATTRS):
    if not isinstance(raw,dict) or any(k not in allowed or type(v) is not int or v<0 for k,v in raw.items()):
        raise RulePending('allocation requires exact nonnegative explicit choices')
    if sum(raw.values())!=expected:raise RulePending(f'allocation sum != budget {expected}')
    return raw


def plan(pages,choices,event_id):
    """Pure PREVIEW: raises on missing decisions; nothing is mutated."""
    validate_state(pages)
    if choices.get('approval')!='OFFLINE_SYNTHETIC_ONLY' or choices.get('actor')!='SIMULATED_TEST_AGENT':
        raise RulePending('real player/master approval missing')
    if choices.get('resource_choice')!='60_PERCENT_FIXED':raise RulePending('dice roll choice unverified')
    if not event_id.startswith('SIM-'):raise RulePending('non-synthetic event id')
    updates=copy.deepcopy(pages)
    n,t,l=updates['NORMAL'],updates['TRANSFORM'],updates['LOCKS']
    oldlevel=n['level'];target=choices['target_level'];rank(target)
    if target<=oldlevel:raise RulePending('target must be above current level')
    old_hash=digest(pages)
    steps=[]
    for level in range(oldlevel+1,target+1):
        before_n=copy.deepcopy(n);before_t=copy.deepcopy(t)
        ai,star,rank_name=rank(level)
        prev_rank=rank(n['level'])[0]
        # Explicit, synthetic verified retroactive titles; never invent title authority.
        prior_title_rate=sum(x['per_level'] for x in n['titles'])
        new_title_bonus=0
        for title in choices.get('title_events',{}).get(str(level),[]):
            if title.get('id') in n['title_credits'] or title.get('source')!='SYNTHETIC_TITLE_EVENT' or title.get('approved')!='SYNTHETIC_EXPLICIT' or title.get('retroactive') is not True or type(title.get('per_level')) is not int or title['per_level']<=0:
                raise RulePending('title lacks unique verified synthetic causal source')
            n['titles'].append(copy.deepcopy(title))
            n['title_credits'][title['id']]=level
            new_title_bonus+=title['per_level']*level
        budget=n['normal_rate']+prior_title_rate+new_title_bonus
        raw=choices.get('normal_allocations',{}).get(str(level))
        allocation=_validate_alloc(raw,budget)
        n['attrs']=addattrs(n['attrs'],allocation)
        for title in n['titles']:n['title_credits'][title['id']]=level
        n['level']=level
        # Same category: incremental growth, not retroactively reopening old CON/INT.
        # Rank transition: canonical rebase under new category using current stats and total levels.
        if ai==prev_rank:
            n['hp_natural']+=FIXED[NORMAL_DICE[ai]]+n['attrs']['CON']
            n['pa_natural']+=FIXED[NORMAL_DICE[ai]]+n['attrs']['INT']
        else:
            n['hp_natural']=n['hp_initial']+level*(FIXED[NORMAL_DICE[ai]]+n['attrs']['CON'])
            n['pa_natural']=n['pa_initial']+level*(FIXED[NORMAL_DICE[ai]]+n['attrs']['INT'])
        # Current normal HP and PA are intentionally never healed by levelup.
        new_effective=min(level,t['spirit']['cap'])
        old_effective=t['effective_level']
        bap=t['spirit']['bap']
        allocated=(bap*new_effective)//2-(bap*old_effective)//2
        rawsp=choices.get('spirit_allocations',{}).get(str(level),{})
        spirit_delta=_validate_alloc(rawsp,allocated,t['spirit']['allowed_attrs'])
        t['overlay']=addattrs(t['overlay'],spirit_delta)
        t['effective_level']=new_effective
        t['tap_carry_half_units']=(bap*new_effective)%2
        t['attrs']=addattrs(n['attrs'],t['overlay'])
        ti=rank(new_effective)[0]
        prev_ti=rank(old_effective)[0]
        if ti==prev_ti:
            if new_effective>old_effective:
                die=bump_die(NORMAL_DICE[ti],1)
                t['hp_theoretical_natural']+=FIXED[die]+t['attrs']['CON']
                t['pa_theoretical_natural']+=FIXED[die]+t['attrs']['INT']
        else:
            die=bump_die(NORMAL_DICE[ti],1)
            t['hp_theoretical_natural']=n['hp_initial']+new_effective*(FIXED[die]+t['attrs']['CON'])
            t['pa_theoretical_natural']=n['pa_initial']+new_effective*(FIXED[die]+t['attrs']['INT'])
        _touch_locks(l['milestones'],n['attrs'],t['attrs'],choices.get('milestones',{}),f'SIM-R13-level-{level}')
        _derived_normal(n,l['milestones']);_derived_transform(n,t,l['milestones'])
        # Changing maximums never replenishes spent normal or transformed reserves.
        if n['hp_current']>n['hp_max'] or n['pa_current']>n['pa_max']:
            raise RulePending('resource exceeds new maximum; manual reconciliation')
        if t['hp_bonus_current']>t['hp_bonus_max'] or t['pa_bonus_current']>t['pa_bonus_max']:
            raise RulePending('form reserve exceeds new maximum; manual reconciliation')
        unlocked=min(ti+1,len(t['spirit']['abilities']))
        t['abilities_active']=t['spirit']['abilities'][:unlocked]
        n['history'].append(f'SIM-{event_id}: level {level} {rank_name} {star}, allocation {allocation}')
        t['history'].append(f'SIM-{event_id}: effective {new_effective}, TAP {spirit_delta}')
        steps.append({'level':level,'rank':rank_name,'star':star,'normal_budget':budget,
                      'normal_alloc':allocation,'tap_budget':allocated,'spirit_alloc':spirit_delta,
                      'rank_rebase':ai!=prev_rank,'effective_level':new_effective,
                      'normal_hp_max':n['hp_max'],'normal_pa_max':n['pa_max'],
                      'transform_hp_bonus_max':t['hp_bonus_max'], 'transform_pa_bonus_max':t['pa_bonus_max'],
                      'normal_ff':n['derived']['ff'],'transform_ff':t['derived']['ff'],
                      'skills':copy.deepcopy(t['abilities_active'])})
    validate_state(updates)
    diff={}
    for key in updates:
        diff[key]={'before_sha256':digest(pages[key]),'after_sha256':digest(updates[key])}
    return {'event_id':event_id,'before_digest':old_hash,'before':copy.deepcopy(pages),
            'updates':updates,'steps':steps,'diff':diff,'choices':copy.deepcopy(choices)}


def execute(prepared, store, crash_at=None):
    current={k:store.read(k)[0] for k in ('NORMAL','TRANSFORM','LOCKS')}
    if digest(current)!=prepared['before_digest'] and prepared['event_id'] not in store.journals:
        raise Conflict('stale PLAN; reread before retry')
    return RecoveryController(store).run(prepared['event_id'],prepared['updates'],crash_at=crash_at)


def make_store(pages=None):return FakeStore(make_fixture() if pages is None else pages)


def rollback(store,journal):
    """Explicit compensation request, using R10's conservative version checks."""
    if journal.state=='COMMITTED':
        # R10 auto-reconcile intentionally refuses to rollback committed events, so
        # do NOT invent a second undo transaction here. A new local safe reversal
        # is made with CAS and full expected-version preflight.
        snapshots=journal.snapshots
        for k,data in snapshots.items():
            value,version=store.read(k)
            if value!=journal.intended[k] or version!=data['version']+1:
                raise Conflict('rollback refused due concurrent change')
        for k in reversed(list(snapshots)):
            current,version=store.read(k)
            store.cas(k,version,snapshots[k]['value'])
        if all(store.read(k)[0]==snapshots[k]['value'] for k in snapshots):
            journal.state='ROLLED_BACK_VERIFIED'
            journal.log('EXPLICIT_ROLLBACK_READBACK_ALL_PASS')
            return journal
        raise Conflict('rollback readback failed')
    return RecoveryController(store).reconcile(journal)


def preview_summary(prepared):
    a=prepared['before'];b=prepared['updates'];
    n0,n1=a['NORMAL'],b['NORMAL'];t0,t1=a['TRANSFORM'],b['TRANSFORM']
    return {'event_id':prepared['event_id'],'level':[n0['level'],n1['level']],
       'rank':[rank(n0['level'])[2],rank(n1['level'])[2]],
       'attributes_before':n0['attrs'],'attributes_after':n1['attrs'],
       'normal_hp_max':[n0['hp_max'],n1['hp_max']], 'normal_hp_current':[n0['hp_current'],n1['hp_current']],
       'normal_pa_max':[n0['pa_max'],n1['pa_max']], 'normal_pa_current':[n0['pa_current'],n1['pa_current']],
       'pa_free':[n0['pa_free'],n1['pa_free']],
       'pa_spendable_now':[n0['pa_spendable_now'],n1['pa_spendable_now']],
       'normal_ca':[n0['derived']['ca'],n1['derived']['ca']],
       'normal_magic_cd':[n0['derived']['magic_cd'],n1['derived']['magic_cd']],
       'normal_ff':[n0['derived']['ff'],n1['derived']['ff']],
       'transform_ff':[t0['derived']['ff'],t1['derived']['ff']],
       'transform_ca':[t0['derived']['ca'],t1['derived']['ca']],
       'transform_life_bonus_max':[t0['hp_bonus_max'],t1['hp_bonus_max']],
       'transform_life_bonus_current':[t0['hp_bonus_current'],t1['hp_bonus_current']],
       'transform_pa_bonus_max':[t0['pa_bonus_max'],t1['pa_bonus_max']],
       'transform_pa_bonus_current':[t0['pa_bonus_current'],t1['pa_bonus_current']],
       'abilities':[t0['abilities_active'],t1['abilities_active']],
       'ff_lock_keys':[sorted(a['LOCKS']['milestones'],key=int),sorted(b['LOCKS']['milestones'],key=int)],
       'steps':prepared['steps'],'sha256':prepared['diff']}
