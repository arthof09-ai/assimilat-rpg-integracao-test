"""IBX-113 additive repair of existing LEVEL-UP-ENGINE / IBX-17.

R202 rolls are replayed exactly once as DIE VALUES, but old +CON/INT
modifiers (bound to invalid R201 base) are superseded. No Notion writes.
The source must come from a fresh physical R201 fetch and be parsed using
r198_dynamic_source.parse_notion after fenced PRE snapshots are ignored
for structural counts. A production HOST signature is NOT fabricated.
"""
from __future__ import annotations
from copy import deepcopy
import hashlib, json
from r198_dynamic_source import sha,SourceSnapshot,ATTRS
from r199_r200_live_mobile import GateHold
from r202_roll_ff_integrated import check_receipt,ALLOC,TARGET,EVENT
FF_SEED = "3baca309f8ef498c1f94d7359adeaa225ab9d6aeb3fab71b57f686274336ed2a"

def value(seed,label,sides):
    d=hashlib.sha256(f"{seed}|{label}|0".encode()).digest()
    return 1+d[0]%sides

BASE_REPAIR_TX='IBX17-IBX113-R201-BASE-REPAIR-20261019-01'
LEDGER_SHA='9f060ced38f421f58d2d51ce3bf56e7f5bc22a25be33a5bac1876fb3ada08c94'
CORRECTED_VERSION='2026-10-20T00:38:56.784Z' # observed physical after repair journal
EXPECTED_NAT={'FOR':6,'DES':13,'CON':14,'INT':13,'SAB':9,'CAR':4}
FF_COMMIT='e2979cdc4c1052db520a20535760998a04720035e6b81c8ff18f16eef6d9ac8e'
BASE_LIMITS=(372,354,360,28)

def check_ff300_retro_synthetic():
    if hashlib.sha256(bytes.fromhex(FF_SEED)).hexdigest()!=FF_COMMIT:raise GateHold('FF_COMMIT_MISMATCH')
    v=value(FF_SEED,'FF300_CA_1D4',4)
    if v!=2:raise GateHold('FF300_DIE_REPLAY_FAILED')
    return {'milestone':300,'first_reach_synthetic_level':9,'choice':'CA','die':'1d4','raw_die':v,
        'provenance':'R202_REAL_HUMAN_CHOICE_AND_COMMITTED_DIE_APPLIED_RETROACTIVELY_TO_SYNTHETIC_TEST_HISTORY',
        'first_reach_historical_campaign_attested':False,'commit_sha256':FF_COMMIT}

def source_gate(source:SourceSnapshot):
    if source.page_id!=TARGET or source.parent_id!='3fbc2b324ede804a95fafcb7b293c92c':raise GateHold('NOT_R201_IN_LAB')
    if source.layout!='COLUMN_TABLE_R144' or source.normal['level']!=17 or source.normal['rank']!='Ouro Negro':raise GateHold('R201_WRONG_LAYOUT_LEVEL')
    if source.normal['natural_attrs']!=EXPECTED_NAT or sum(source.normal['natural_attrs'].values())!=59:raise GateHold('BASE_14_NOT_REPAIRED')
    n=source.normal
    if tuple(n[k] for k in ('hp_max','pa_max','ff','ca'))!=BASE_LIMITS:raise GateHold('BASE_NUMBERS_NOT_REPAIRED')
    if (n['hp_current'],n['pa_current'],n['pa_committed'],n['pa_free'])!=(240,150,30,324):raise GateHold('RESOURCES_NOT_RECONCILED')
    if source.layers!={'equipment':{'DES':3},'title':{'SAB':2}}:raise GateHold('EXTERNAL_LAYER_CHANGED')
    if source.structural['<columns>']!=1 or source.structural['<table']!=1 or source.structural['<page url=']!=1 or source.structural['<details']!=3:raise GateHold('R201_STRUCTURE_FAILED')
    if source.version!=CORRECTED_VERSION:raise GateHold('STALE_SOURCE_REFETCH_REQUIRED')
    return True

def build_corrected_r202_preview(source:SourceSnapshot,roll_receipt:dict):
    source_gate(source)
    rollcheck=check_receipt(roll_receipt) # checks exact immutable seed/digest/old historical receipt, no reroll
    if roll_receipt['source_version']!='2026-10-19T19:47:50.723Z':raise GateHold('DIE_RECEIPT_UNEXPECTED_PRE_REPAIR_VERSION')
    ff=check_ff300_retro_synthetic()
    before=deepcopy(source.normal);n=deepcopy(before); steps=[]
    for i,a in enumerate(ALLOC):
        lvl=18+i; old=deepcopy(n); n['level']=lvl
        for attr,points in a.items():n['natural_attrs'][attr]+=points
        if sum(n['natural_attrs'].values())!=25+2*lvl:raise GateHold('POINT_BUDGET_VIOLATED')
        rv1=roll_receipt['rolls'][2*i]['value'];rv2=roll_receipt['rolls'][2*i+1]['value']
        plus_hp=n['natural_attrs']['CON'];plus_pa=n['natural_attrs']['INT']
        increment_hp=rv1+plus_hp;increment_pa=rv2+plus_pa
        n['hp_max']+=increment_hp;n['pa_max']+=increment_pa;n['pa_free']=n['pa_max']-n['pa_committed']
        effective={k:n['natural_attrs'][k]+sum(l.get(k,0) for l in source.layers.values()) for k in ATTRS}
        n['ff']=10*(effective['FOR']+effective['DES']+effective['CON'])
        # Level 17 already includes FF300 +2. No new milestone is acquired.
        n['ca']=6+effective['DES']+4+ff['raw_die']
        if n['ff']>=400:raise GateHold('UNEXPECTED_NEW_FF400')
        steps.append({'from':old['level'],'to':lvl,'rank':f'Ouro Negro {lvl-15}',
                      'allocation':{k:v for k,v in a.items() if v},'rolled_hp_d12':rv1,'hp_CON':plus_hp,'gain_hp':increment_hp,
                      'rolled_pa_d12':rv2,'pa_INT':plus_pa,'gain_pa':increment_pa,
                      'hp_max':n['hp_max'],'pa_max':n['pa_max'],'pa_free':n['pa_free'],
                      'ff':n['ff'],'ca':n['ca'],'natural_total':sum(n['natural_attrs'].values()),
                      'effective_attrs':effective,'ff_new_locks':[]})
    if (n['hp_max'],n['pa_max'],n['ff'],n['ca'])!=(414,402,390,30):raise GateHold('R202_NEW_BASE_MATH_MISMATCH')
    after={**deepcopy(n),'rank':'Ouro Negro','hp_current':240,'pa_current':150}
    result={'event':EVENT,'status':'PREVIEW_ONLY_AWAITING_EXPRESS_HUMAN_APPROVAL',
       'source':{'id':source.page_id,'version':source.version,'hash':source.source_hash,'fingerprint':source.fingerprint()},
       'base_repair_event':BASE_REPAIR_TX,'base_ledger_sha256':LEDGER_SHA,'roll_receipt_sha256':rollcheck['sha256'],
       'roll_numbers_reused':[r['value'] for r in roll_receipt['rolls']],
       'invalidated_old_modifiers':[r['attribute_modifier'] for r in roll_receipt['rolls']],
       'new_modifiers':[14,13,15,14],
       'human_allocations':[{'DES':2},{'CON':1,'INT':1}],
       'ff300':ff,'ff100_and_200':'DANO +2, +3 SYNTH_FIXTURE_NOT_RANDOM_ATTESTED',
       'ca_test_offset':4,'before':before,'steps':steps,'after':after,
       'hp_pa_current_preserved':True,'r202_mechanical_write_count':0,
       'r202_write_authorized':False,'party_write_authorized':False,
       'rank_cross':False,'unknowns':['CD_MAGIA_ABSOLUTE_NO_PROF_BONUS','PROFICIENCY_LIST_NOT_DEFINED_IN_R201'],
       'no_automatic_rerolls':True,'no_ff_double_count':True,'no_claim_of_historical_campaign':True,
       'holds':[]}
    result['preview_hash']=sha(result)
    return result

def build_safe_structural_writeset(source:SourceSnapshot,body:str,preview:dict):
    """No dispatch. Edit active section only; snapshots/children are immutable."""
    source_gate(source)
    if preview['source']['fingerprint']!=source.fingerprint() or sha(body)!=source.source_hash:
        raise GateHold('SOURCE_VERSION_OR_BODY_MISMATCH')
    active,tail=body.split('## Regras TEST — estrutura',1)
    new=active
    pairs=[('**Nível:** 17','**Nível:** 19'),
      ('### Vida: 240/372','### Vida: 240/414'),
      ('### Alma: 150/354 (30 comprometidos)','### Alma: 150/402 (30 comprometidos)'),
      ('**FF:** 360','**FF:** 390'),
      ('**Destreza:** 16 (inclui +3 equipamento da fixture; natural 13 IBX113)','**Destreza:** 18 (inclui +3 equipamento da fixture; natural 15 R202)'),
      ('**Constituição:** 14','**Constituição:** 15'),
      ('**Inteligência:** 13','**Inteligência:** 14'),
      ('**CA:** 28 (inclui +2 lock FF300 reconciliado IBX113 TEST)','**CA:** 30 (inclui +2 FF300 preexistente na baseline corrigida)')]
    for before,after in pairs:
        if new.count(before)!=1:raise GateHold('NOT_UNIQUE_ACTIVE_EDIT_'+before)
        new=new.replace(before,after,1)
    newtable=tail.split('</table>',1)[0]
    if newtable.count('<td>DES</td>\n<td>16</td>')!=1 or newtable.count('<td>CON</td>\n<td>14</td>')!=1:raise GateHold('TABLE_FIELDS_NOT_PRESENT')
    # preserve table and archival native toggles, produce only preview of edit specs
    return {'ready_for_dispatch':False,'source_version':source.version,'event':EVENT,'edits_active':pairs,
            'edits_table':[('DES',16,18),('CON',14,15)],
            'needs_new_bottom_history_toggle':True,'original_tail_untouched':True,
            'expected_active_after':new,'revalidate_before_write':True}
