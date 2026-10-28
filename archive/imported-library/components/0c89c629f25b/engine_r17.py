"""R17 additive local-only planner, with real dice receipt consumption.

R13/R14/R16 untouched. Supports verified synthetic Human contract, Prata 1+
and a conditional Bronze5->Prata1 sample, NOT a ruling on TAP accounting in Bronze.
Unknown race, title, spirit-cap, PA spend ordering, class-specific grants => HOLD.
"""
from __future__ import annotations
import copy
from engine_r13 import (ATTRS,RANKS,NORMAL_DICE,FIXED,RulePending,rank,ff,addattrs,
                        bump_die,_derived_normal,_derived_transform,lock_value)
from r10_recovery import digest
from r16_gate import prata_fixture,plan_prata,access,FIRST_TRANSFORM_LEVEL
from roll_ledger_r17 import RollLedger

class R17Hold(RulePending):pass
MODES=('FIXO','ROLAR')
RESOURCES=('NORMAL_HP','NORMAL_PA','TRANSFORM_HP','TRANSFORM_PA')


def bronze5_fixture():
    """Conditional purely synthetic fixture; no Bronze form activation or FF ghost grant.

    Historical pre-Silver TAP distribution is a TEST assumption, not a new
    official ruling. The ledger must carry a validated contract before real use.
    """
    state=prata_fixture();n,t,l=state['NORMAL'],state['TRANSFORM'],state['LOCKS']
    for p in (n,t,l):p['id']='SYNTH-R17-BRONZE5-ONLY'
    n['level']=5;n['attrs']['FOR']-=2
    n['hp_natural']=n['hp_initial']+5*(FIXED[6]+n['attrs']['CON'])
    n['pa_natural']=n['pa_initial']+5*(FIXED[6]+n['attrs']['INT'])
    n['hp_current']=39;n['pa_current']=32
    n['history']=['R17 conditional synthetic Bronze 5 baseline; no activation legal']
    t['effective_level']=5
    t['overlay']=dict(zip(ATTRS,[15,0,15,0,0,0]))
    t['attrs']=addattrs(n['attrs'],t['overlay'])
    t['tap_carry_half_units']=0
    t['hp_theoretical_natural']=n['hp_initial']+5*(FIXED[8]+t['attrs']['CON'])
    t['pa_theoretical_natural']=n['pa_initial']+5*(FIXED[8]+t['attrs']['INT'])
    t['hp_bonus_current']=0;t['pa_bonus_current']=0
    t['abilities_active']=['Rugido inventado (TESTE)']
    t['activation_state']='INACTIVE_NEVER_LEGAL_BRONZE'
    t['bronze_accounting']='SYNTHETIC_HYPOTHESIS_NOT_CANON'
    t['history']=['Pre-Silver spiritual budget mathematically staged; NEVER playable while Bronze']
    l['milestones']={k:v for k,v in l['milestones'].items() if int(k)<=2}
    l['history']=['Only NORMAL Bronze FF milestones genuinely reached in synthetic history']
    _derived_normal(n,l['milestones']);_derived_transform(n,t,l['milestones'])
    validate_r17(state)
    return state


def bronze1_fixture():
    """Synthetic Bronze 1 normal-only fixture, NEVER a player record.

    Pre-Silver Spirit accounting is a *hypothesis* staged for continuity with
    the R17 Bronze5 fixture.  It must not be construed as permission to
    activate the Spirit or grant player-visible spiritual benefits in Bronze.
    """
    state=prata_fixture();n,t,l=(state[k] for k in ('NORMAL','TRANSFORM','LOCKS'))
    for p in (n,t,l):p['id']='SYNTH-R25-BRONZE1-STAGED-ONLY'
    n['level']=1;n['attrs']=copy.deepcopy(n['initial_attrs'])
    n['hp_natural']=n['hp_initial']+FIXED[6]+n['attrs']['CON']
    n['pa_natural']=n['pa_initial']+FIXED[6]+n['attrs']['INT']
    n['hp_current']=20;n['pa_current']=20;n['pa_committed']=1
    n['history']=['R25 synthetic Bronze 1 normal baseline, NEVER Party']
    t['effective_level']=1
    t['overlay']=dict(zip(ATTRS,[3,0,3,0,0,0]))
    t['attrs']=addattrs(n['attrs'],t['overlay'])
    t['tap_carry_half_units']=0
    t['hp_theoretical_natural']=n['hp_initial']+FIXED[8]+t['attrs']['CON']
    t['pa_theoretical_natural']=n['pa_initial']+FIXED[8]+t['attrs']['INT']
    t['hp_bonus_current']=0;t['pa_bonus_current']=0
    t['abilities_active']=[]
    t['activation_state']='INACTIVE_NEVER_LEGAL_BRONZE'
    t['bronze_accounting']='SYNTHETIC_HYPOTHESIS_NOT_CANON'
    t['history']=['PRE_SILVER_SPIRIT_PROJECTION_ONLY; NO ACTIVATION OR REWARD']
    l['milestones']={'1':copy.deepcopy(l['milestones']['1'])}
    l['history']=['Only genuine normal FF100 synthetic lock is recorded']
    _derived_normal(n,l['milestones']);_derived_transform(n,t,l['milestones'])
    validate_r17(state)
    return state


def lendario_ff_fixture():
    """Synthetic normal FF580 -> FF600 pilot for unique 1d4/2d6 lock receipts."""
    state=prata_fixture();n,t,l=state['NORMAL'],state['TRANSFORM'],state['LOCKS']
    for p in (n,t,l):p['id']='SYNTH-R17-LENDARIO-FF-ONLY'
    n['level']=21
    n['initial_attrs']=dict(zip(ATTRS,[6,6,6,2,2,3]))
    n['attrs']=dict(zip(ATTRS,[24,17,17,2,2,3]))
    n['hp_initial']=16;n['pa_initial']=12
    n['hp_natural']=16+21*(FIXED[20]+17)
    n['pa_natural']=12+21*(FIXED[20]+2)
    n['hp_current']=400;n['pa_current']=100;n['pa_committed']=10
    n['history']=['R17 synthetic Lendario1 580FF; no official item']
    t['spirit']['cap']=25;t['spirit']['bap']=0
    t['effective_level']=21
    t['overlay']={k:0 for k in ATTRS}
    t['attrs']=copy.deepcopy(n['attrs']);t['tap_carry_half_units']=0
    t['hp_theoretical_natural']=16+21*(FIXED[30]+17)
    t['pa_theoretical_natural']=12+21*(FIXED[30]+2)
    t['hp_bonus_current']=0;t['pa_bonus_current']=0
    t['history']=['Synthetic theoretical spirit state inactive']
    _derived_normal(n,l['milestones']);_derived_transform(n,t,l['milestones'])
    validate_r17(state)
    return state


def validate_r17(state):
    if set(state)!={'NORMAL','TRANSFORM','LOCKS'}:raise R17Hold('invalid synthetic page contract')
    n,t,l=(state[k] for k in ('NORMAL','TRANSFORM','LOCKS'))
    if any(p.get('fixture_only') is not True for p in (n,t,l)) or not n['id'].startswith('SYNTH-'):
        raise R17Hold('non-synthetic actor denied')
    if n['id']!=t['id'] or n['id']!=l['id']:raise R17Hold('three-document identity mismatch')
    if n['race']!='Humano' or n['normal_rate']!=2 or n['titles'] or n['title_credits']:
        raise R17Hold('race/title contract not admitted; canonical specific source required')
    lv=n['level'];rank(lv)
    if t['effective_level']!=min(lv,t['spirit']['cap']):raise R17Hold('effective level mismatch')
    if t['spirit']['bap']<0 or type(t['spirit']['bap']) is not int:raise R17Hold('invalid spiritual budget source')
    if t['tap_carry_half_units']!=(t['spirit']['bap']*t['effective_level'])%2:
        raise R17Hold('fractional carry mismatch')
    if sum(t['overlay'].values())!=(t['spirit']['bap']*t['effective_level'])//2:
        raise R17Hold('spirit budget checksum')
    if set(n['attrs'])!=set(ATTRS) or set(t['attrs'])!=set(ATTRS) or t['attrs']!=addattrs(n['attrs'],t['overlay']):
        raise R17Hold('attribute/overlay mismatch')
    # R25 ingress validation: negative reserves and stale spendable PA used to
    # survive preflight. An injured/debt state with an unsupported negative
    # value is HOLD for explicit adjudication, not silently repaired by levelling.
    for key in ('hp_current','pa_current','pa_committed','hp_max','pa_max',
                'hp_natural','pa_natural'):
        if type(n.get(key)) is not int or n[key]<0:
            raise R17Hold('negative or invalid normal reserve: '+key)
    for key in ('hp_bonus_current','pa_bonus_current','hp_bonus_max','pa_bonus_max',
                'hp_theoretical_natural','pa_theoretical_natural'):
        if type(t.get(key)) is not int or t[key]<0:
            raise R17Hold('negative or invalid transform reserve: '+key)
    if n['hp_current']>n['hp_max'] or n['pa_current']>n['pa_max'] or n['pa_committed']>n['pa_current']:
        raise R17Hold('normal reserve exceeds maximum/spendable')
    if t['hp_bonus_current']>t['hp_bonus_max'] or t['pa_bonus_current']>t['pa_bonus_max']:
        raise R17Hold('transform reserve exceeds maximum')
    if n['pa_free']!=n['pa_max']-n['pa_committed'] or n.get('pa_spendable_now')!=n['pa_current']-n['pa_committed']:
        raise R17Hold('PA free/spendable mismatch')
    if any(int(k)<=0 or lock_value(v)<1 for k,v in l['milestones'].items()):
        raise R17Hold('invalid permanent FF milestone')
    if set(range(1,ff(n['attrs'])//100+1))-{int(k) for k in l['milestones']}:
        raise R17Hold('genuine NORMAL FF milestone lacking lock')
    if lv<FIRST_TRANSFORM_LEVEL and t.get('activation_state')!='INACTIVE_NEVER_LEGAL_BRONZE':
        raise R17Hold('Bronze cannot have active form')
    if lv>=FIRST_TRANSFORM_LEVEL and t.get('activation_state')!='INACTIVE_NO_T6B_REFRESH':
        raise R17Hold('real activation handling not certified')
    return True


def dice_contracts(state,choices):
    """List every resource roll needed, including full new-rank rebases."""
    validate_r17(state)
    lv0=state['NORMAL']['level'];target=choices['target_level'];rank(target)
    if target<=lv0:raise R17Hold('invalid target')
    cap=state['TRANSFORM']['spirit']['cap']
    # T2/T3 canon: the NORMAL actor keeps levelling after the Spirit's ceiling.
    # Only the effective Spirit level controls spiritual rolls and TAP.  This
    # is a synthetic-only engine; external character activation stays gated.
    specs=[];old_eff=min(lv0,cap)
    for lv in range(lv0+1,target+1):
        ni=rank(lv)[0];nprev=rank(lv-1)[0]
        ti=rank(min(lv,cap))[0];tprev=rank(old_eff)[0]
        count=lv if ni!=nprev else 1
        tc=min(lv,cap) if ti!=tprev else 1
        vals={
            'NORMAL_HP':(NORMAL_DICE[ni],count),
            'NORMAL_PA':(NORMAL_DICE[ni],count)}
        # T2: no effective Spiritual level change = NO spiritual growth dice,
        # not even when the NORMAL character crosses a higher rank.
        if min(lv,cap)>old_eff:
            vals.update({'TRANSFORM_HP':(bump_die(NORMAL_DICE[ti],1),tc),
                         'TRANSFORM_PA':(bump_die(NORMAL_DICE[ti],1),tc)})
        for component,(sides,num) in vals.items():
            purpose=f'LV{lv:02d}_{component}'
            specs.append({'level':lv,'component':component,'purpose':purpose,'sides':sides,'count':num})
        old_eff=min(lv,cap)
    return specs


def _alloc(raw,expected,allowed):
    if not isinstance(raw,dict) or set(raw)-set(allowed) or any(type(v) is not int or v<0 for v in raw.values()):
        raise R17Hold('allocation must be explicit, numeric, within source-approved attributes')
    if sum(raw.values())!=expected:raise R17Hold('allocation budget mismatch')
    return raw


def _values(spec,modes,receipts,event_id):
    mode=modes[spec['component']]
    if mode=='FIXO':return [FIXED[spec['sides']]]*spec['count'], None
    if mode!='ROLAR':raise R17Hold('missing explicit resource choice')
    rid=f'{event_id}_{spec["purpose"]}'
    r=receipts.get(rid)
    if r is None:raise R17Hold('rolled resources require verified durable receipt: '+rid)
    RollLedger.verify(r)
    x=r['spec']
    if (x['event_id'],x['roll_id'],x['purpose'],x['sides'],x['count'])!=(event_id,rid,spec['purpose'],spec['sides'],spec['count']):
        raise R17Hold('misbound/duplicated roll receipt')
    return list(r['rolls']),r['receipt_sha256']


def plan_r17(state,choices,event_id):
    """Pure preview: consume already revealed receipts, never draw implicitly."""
    validate_r17(state)
    if not event_id.startswith('SIM-') or choices.get('actor')!='SIMULATED_TEST_AGENT' or choices.get('approval')!='OFFLINE_SYNTHETIC_ONLY':
        raise R17Hold('real identity/authority denied')
    n0=state['NORMAL'];lv0=n0['level'];target=choices.get('target_level')
    if type(target) is not int or target<=lv0 or target>25:raise R17Hold('invalid destination')
    modes=choices.get('resource_modes')
    if not isinstance(modes,dict) or set(modes)!=set(RESOURCES) or any(v not in MODES for v in modes.values()):
        raise R17Hold('explicit choices required for all resource growth components')
    if n0['titles'] or n0['title_credits'] or choices.get('title_events'):
        raise R17Hold('title bonus/reroll requires separate verified authority')
    if choices.get('conditional_unverified') or choices.get('extra_race_rules'):
        raise R17Hold('unsourced conditional class/race choice')
    # Race/class/skill prompts require a separately verified conditional contract.
    # Only inert synthetic selection is supported; no stat/ability is fabricated.
    contracts=state['NORMAL'].get('choice_contracts',[])
    choice_ids={c['id'] for c in contracts}
    selected=choices.get('conditionals',{})
    if set(selected)!=choice_ids:
        raise R17Hold('missing/surplus conditional choice')
    for c in contracts:
        if (c.get('source')!='SIMULATED_VERIFIED_CONTRACT' or
            c.get('impact')!='RECORD_ONLY_TEST' or
            c.get('level') not in range(lv0+1,target+1) or
            selected[c['id']] not in c.get('options',[])):
            raise R17Hold('conditional cannot be applied without verified rule source')
    # R25 normal Bronze progression: only allow an explicit STAGED synthetic
    # Spirit hypothesis; never promote it into active spiritual benefits.
    # Real Bronze historical accounting remains separately unverified.
    if lv0<6 and state['TRANSFORM'].get('bronze_accounting')!='SYNTHETIC_HYPOTHESIS_NOT_CANON':
        raise R17Hold('unverified pre-Silver Spirit accounting; HOLD')
    # Above the Spirit cap, normal levels are still legal under T2/T3; the
    # capped Spirit may not receive another TAP point, unlock or growth roll.
    if any(k not in choices for k in ('normal_allocations','spirit_allocations','milestones')):
        raise R17Hold('human choices absent')
    specs=dice_contracts(state,choices)
    recmap=choices.get('roll_receipts',{})
    expected_rolls={f'{event_id}_{s["purpose"]}' for s in specs if modes[s['component']]=='ROLAR'}
    rec_usage=set()
    if set(recmap)!=expected_rolls | {f'{event_id}_FF_{k}' for k in choices['milestones']}:
        raise R17Hold('missing, surplus or wrong-context roll receipt')
    p=copy.deepcopy(state);n,t,l=(p[k] for k in ('NORMAL','TRANSFORM','LOCKS'))
    steps=[];consumed=[];old_effective=t['effective_level']
    for level in range(lv0+1,target+1):
        previous_rank=rank(n['level'])[0];index,star,rname=rank(level)
        normal_alloc=_alloc(choices['normal_allocations'].get(str(level)),n['normal_rate'],ATTRS)
        n['attrs']=addattrs(n['attrs'],normal_alloc);n['level']=level
        previous_effective=t['effective_level']
        effective=min(level,t['spirit']['cap']);bap=t['spirit']['bap']
        spirit_budget=(bap*effective)//2-(bap*previous_effective)//2
        spirit_alloc=_alloc(choices['spirit_allocations'].get(str(level)),spirit_budget,t['spirit']['allowed_attrs'])
        t['overlay']=addattrs(t['overlay'],spirit_alloc)
        t['effective_level']=effective;t['tap_carry_half_units']=(bap*effective)%2
        t['attrs']=addattrs(n['attrs'],t['overlay'])
        level_specs=[s for s in specs if s['level']==level]
        growth={}
        for s in level_specs:
            vv,h=_values(s,modes,recmap,event_id)
            growth[s['component']]={'dice':f'{s["count"]}d{s["sides"]}', 'sum':sum(vv),
                                   'receipt_sha256':h,'method':modes[s['component']]}
            if h:rec_usage.add(f'{event_id}_{s["purpose"]}');consumed.append({'purpose':s['purpose'],'receipt_sha256':h})
        if index!=previous_rank:
            n['hp_natural']=n['hp_initial']+growth['NORMAL_HP']['sum']+level*n['attrs']['CON']
            n['pa_natural']=n['pa_initial']+growth['NORMAL_PA']['sum']+level*n['attrs']['INT']
        else:
            n['hp_natural']+=growth['NORMAL_HP']['sum']+n['attrs']['CON']
            n['pa_natural']+=growth['NORMAL_PA']['sum']+n['attrs']['INT']
        oldti=rank(previous_effective)[0];newti=rank(effective)[0]
        if effective==previous_effective:
            # T2 cap: no new Spiritual level means no intrinsic natural HP/PA
            # growth or new dice. Preserve the already accrued hypothetical
            # component; T6-B still recomputes its nonnegative difference
            # against the *new normal maximum* below. Any reduction below a
            # previously spent reserve remains a HARD HOLD, not a free reset.
            for component in ('TRANSFORM_HP','TRANSFORM_PA'):
                growth[component]={'dice':'NONE_SPIRIT_CAPPED','sum':0,
                    'receipt_sha256':None,'method':'NO_EFFECTIVE_LEVEL_GAIN'}
        elif newti!=oldti:
            t['hp_theoretical_natural']=n['hp_initial']+growth['TRANSFORM_HP']['sum']+effective*t['attrs']['CON']
            t['pa_theoretical_natural']=n['pa_initial']+growth['TRANSFORM_PA']['sum']+effective*t['attrs']['INT']
        else:
            t['hp_theoretical_natural']+=growth['TRANSFORM_HP']['sum']+t['attrs']['CON']
            t['pa_theoretical_natural']+=growth['TRANSFORM_PA']['sum']+t['attrs']['INT']
        for i in range(1,ff(n['attrs'])//100+1):
            k=str(i)
            if k not in l['milestones']:
                ch=choices['milestones'].get(k)
                if ch is None or ch.get('type') not in ('DANO','CA','VIDA'):
                    raise R17Hold(f'new FF milestone {k} requires player choice')
                sides=6 if ch['type']=='VIDA' else 4;count=2 if sides==6 else 1
                rid=f'{event_id}_FF_{k}';r=recmap.get(rid)
                if r is None:raise R17Hold('FF requires durable roll receipt')
                RollLedger.verify(r)
                spec=r['spec'];purpose=f'FF_MILESTONE_{int(k):03d}_{ch["type"]}'
                if (spec['event_id'],spec['roll_id'],spec['purpose'],spec['sides'],spec['count'])!=(event_id,rid,purpose,sides,count):
                    raise R17Hold('FF receipt misbound')
                l['milestones'][k]={'type':ch['type'],'rolls':list(r['rolls']),
                                      'first_source':f'SIM-R17-LEVEL-{level}',
                                      'receipt_sha256':r['receipt_sha256']}
                consumed.append({'purpose':purpose,'receipt_sha256':r['receipt_sha256']})
                rec_usage.add(rid)
        _derived_normal(n,l['milestones']);_derived_transform(n,t,l['milestones'])
        if n['hp_current']>n['hp_max'] or n['pa_current']>n['pa_max'] or t['hp_bonus_current']>t['hp_bonus_max'] or t['pa_bonus_current']>t['pa_bonus_max']:
            raise R17Hold('current resources cannot be silently clamped or refilled')
        t['activation_state']='INACTIVE_NO_T6B_REFRESH' if level>=6 else 'INACTIVE_NEVER_LEGAL_BRONZE'
        # The Mestre explicitly DENIED transformation in Bronze. The early
        # level budget is bookkeeping only; no power is granted as active.
        t['abilities_active']=(t['spirit']['abilities'][:min(newti+1,len(t['spirit']['abilities']))]
                              if level>=FIRST_TRANSFORM_LEVEL else [])
        n['history'].append(f'SIM-R17-{event_id}: level {level}; normal distribution {normal_alloc}')
        t['history'].append(f'SIM-R17-{event_id}: effective level {effective}; own distribution {spirit_alloc}')
        steps.append({'level':level,'rank':rname,'star':star,
                      'spirit_capped':effective==previous_effective,
                      'spirit_effective_level_before':previous_effective,
                      'spirit_effective_level_after':effective,
                      'normal_budget':n['normal_rate'],
                      'normal_allocation':normal_alloc,'spirit_budget':spirit_budget,'spirit_allocation':spirit_alloc,
                      'growth':growth,'rank_rebase':previous_rank!=index,
                      'legal_transform_activation':False,
                      'activation_eligible_after_level':level>=FIRST_TRANSFORM_LEVEL,
                      'normal_hp_max':n['hp_max'],'normal_pa_max':n['pa_max'],
                      'normal_ff':ff(n['attrs']),'spirit_ff_theoretical':ff(t['attrs'])})
    if rec_usage!=set(recmap):raise R17Hold('unconsumed/unproven receipt detected')
    if contracts:
        n.setdefault('synthetic_choice_history',[]).extend(
            {'contract':c['id'],'level':c['level'],'choice':selected[c['id']],
             'effect':'RECORDED_ONLY_NOT_APPLIED'} for c in contracts)
    validate_r17(p)
    # Verify NO new FF locks from hypothetical spiritual state.
    actual_ff_cap=max(ff(n0['attrs']),max(step['normal_ff'] for step in steps))//100
    new={int(k) for k in l['milestones']}-{int(k) for k in state['LOCKS']['milestones']}
    if any(k>actual_ff_cap for k in new):raise R17Hold('ghost FF milestone was granted')
    diff={k:{'before_sha256':digest(state[k]),'after_sha256':digest(p[k])} for k in p}
    return {'event_id':event_id,'before':copy.deepcopy(state),'before_digest':digest(state),
            'updates':p,'diff':diff,'steps':steps,'choices':copy.deepcopy(choices),
            'roll_receipt_hashes':consumed,'activation_eligibility':access(target),
            'transition_label':('BRONZE_STAGED_NORMAL_ONLY_SANDBOX' if target<6 else
                'BRONZE5_PRATA1_CONDITIONAL_SANDBOX' if lv0==5 else
                'BRONZE_TO_PRATA_CONDITIONAL_SANDBOX' if lv0<6 else 'SILVER_PLUS_SANDBOX'),
            'writer_authorized':False,'notion_writes':0,
            'deferred_spirit_milestones':[str(k) for k in range(1,ff(t['attrs'])//100+1) if str(k) not in l['milestones']]}
