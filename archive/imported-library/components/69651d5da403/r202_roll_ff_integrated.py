"""R202 additive patch for existing IBX17 engine. TEST preview only.

Does NOT authenticate randomness, authorize writes, claim physical page mutation,
or resolve R201 FF300 provenance. SourceSnapshot must come from a Notion fetch.
"""
from __future__ import annotations
import copy,hashlib,json,re
from r198_dynamic_source import ATTRS,SourceSnapshot,rank_at,sha
from r199_r200_live_mobile import GateHold
EVENT='IBX17-R202-CONVERSATIONAL-TEST-20261019-01'
TARGET='3fec2b324ede8179a8d4f94886ff7510'
LABELS=('L18_VIDA_1D12_PLUS10','L18_ALMA_1D12_PLUS8','L19_VIDA_1D12_PLUS11','L19_ALMA_1D12_PLUS9')
MODIFIERS=(10,8,11,9)
ALLOC=({'FOR':0,'DES':2,'CON':0,'INT':0,'SAB':0,'CAR':0},
       {'FOR':0,'DES':0,'CON':1,'INT':1,'SAB':0,'CAR':0})

def check_receipt(receipt:dict):
    if receipt['event']!=EVENT or receipt['target']!=TARGET:raise GateHold('DICE_EVENT_TARGET_MISMATCH')
    if tuple(receipt['dice'])!=LABELS or len(receipt['rolls'])!=4:raise GateHold('DICE_LABELS_NOT_EXACT')
    seed=receipt['seed_revealed_hex']
    if not re.fullmatch('[0-9a-f]{64}',seed):raise GateHold('SEED_BAD_ENCODING')
    if hashlib.sha256(bytes.fromhex(seed)).hexdigest()!=receipt['seed_commitment_sha256']:raise GateHold('COMMIT_SEED_MISMATCH')
    for item,label,mod in zip(receipt['rolls'],LABELS,MODIFIERS):
        if item['label']!=label or item['attribute_modifier']!=mod or item['die']!='d12':raise GateHold('DICE_COMPONENT_MISMATCH')
        counter=0
        while True:
            digest=hashlib.sha256(f'{seed}|{label}|{counter}'.encode('ascii')).digest()
            if digest[0]<252:break
            counter+=1
            if counter>=1000:raise GateHold('DICE_COUNTER_OVERFLOW')
        if (item['value']!=1+digest[0]%12 or item['counter']!=counter or
            item['digest']!=digest.hex() or item['first_byte']!=digest[0] or item['increment']!=item['value']+mod):raise GateHold('DICE_REPLAY_MISMATCH')
    saved=receipt['receipt_sha256'];payload={k:v for k,v in receipt.items() if k!='receipt_sha256'}
    canonical=json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':'))
    if hashlib.sha256(canonical.encode()).hexdigest()!=saved:raise GateHold('RECEIPT_HASH_MISMATCH')
    return {'verified_replay':True,'sha256':saved,'commit':receipt['seed_commitment_sha256'],'randomness_host_attested':False}

def build_preliminary_preview(source:SourceSnapshot,receipt:dict):
    verification=check_receipt(receipt)
    if source.page_id!=TARGET or source.parent_id!='3fbc2b324ede804a95fafcb7b293c92c':raise GateHold('R202_WRONG_TARGET')
    if source.version!=receipt['source_version']:raise GateHold('R202_SOURCE_VERSION_DRIFT')
    if source.layout!='COLUMN_TABLE_R144':raise GateHold('R202_WRONG_LAYOUT')
    before=copy.deepcopy(source.normal)
    if before['level']!=17 or before['rank']!='Ouro Negro':raise GateHold('R202_NOT_LEVEL17_ON2')
    if before['ff']!=290 or before['hp_max']!=309 or before['pa_max']!=273:raise GateHold('R202_SOURCE_MECHANICS_DRIFT')
    n=copy.deepcopy(before);steps=[]
    for index,alloc in enumerate(ALLOC):
        old=copy.deepcopy(n);n['level']+=1
        for k,v in alloc.items():n['natural_attrs'][k]+=v
        if rank_at(n['level'])!='Ouro Negro':raise GateHold('R202_UNPLANNED_RANK_CROSS')
        roll_life,roll_pa=receipt['rolls'][2*index:2*index+2]
        if (n['natural_attrs']['CON']!=roll_life['attribute_modifier'] or
            n['natural_attrs']['INT']!=roll_pa['attribute_modifier']):raise GateHold('R202_DICE_MODIFIER_ATTRIBUTE_DIVERGENCE')
        n['hp_max']+=roll_life['increment'];n['pa_max']+=roll_pa['increment']
        n['pa_free']=n['pa_max']-n['pa_committed']
        effective={a:n['natural_attrs'][a]+sum(x.get(a,0) for x in source.layers.values()) for a in ATTRS}
        n['ff']=10*(effective['FOR']+effective['DES']+effective['CON'])
        # Humano 6+DES+armadura/bonuses; unchanged verified baseline offset.
        n['ca']=old['ca']+alloc['DES']
        steps.append(dict(level_from=old['level'],level_to=n['level'],rank=f'Ouro Negro {n["level"]-15}',allocation=alloc,rolls=[roll_life['value'],roll_pa['value']],delta_hp=roll_life['increment'],delta_pa=roll_pa['increment'],hp_max=n['hp_max'],pa_max=n['pa_max'],pa_free=n['pa_free'],ff=n['ff'],ca_before_ff300=n['ca'],effective_attrs=effective))
    budget_initial=25;budget_expected=budget_initial+17*2
    natural_points=sum(before['natural_attrs'].values());after_points=sum(n['natural_attrs'].values())
    if natural_points!=45 or after_points!=49:raise GateHold('R202_POINTS_BASELINE_CONFLICT')
    ff_new=[m for m in (100,200,300) if before['ff']<m<=n['ff']]
    if ff_new!=[300] or steps[0]['ff']!=310:raise GateHold('R202_FF_TIMELINE_INVALID')
    holds=['FF300_LOCK_MISSING_OR_UNPROVEN_IN_R201_SOURCE','HUMAN_NATURAL_POINTS_UNRECONCILED_14','CA_PRIOR_ARMOR_AND_BONUS_OFFSET_NOT_ATTRIBUTED','PROFICIENCY_LIST_NOT_IN_SOURCE','MAGIC_CD_NOT_IN_SOURCE']
    result={'event':EVENT,'status':'PREVIEW_PENDING_FF300_AND_HUMAN_APPROVAL','source':{'id':source.page_id,'version':source.version,'hash':source.source_hash,'fingerprint':source.fingerprint()},'mode':'SHA256_COMMIT_REPLAY_ROLLS_NOT_HOST_RANDOMNESS_ATTESTED','allocations':list(ALLOC),'before':before,'after_pre_ff300':n,'steps':steps,'dice_receipt_sha256':verification['sha256'],'dice_commit_sha256':verification['commit'],'ff300':{'trigger_level':18,'status':'NEEDS_MESTRE_CHOICE_AND_LOCK_PROVENANCE','choices':['DANO_1D4','CA_1D4','VIDA_2D6']},'attribute_budget':{'initial':budget_initial,'expected_level17':budget_expected,'observed_level17':natural_points,'gap_before':budget_expected-natural_points,'expected_level19':63,'observed_level19':after_points,'gap_after':63-after_points},'holds':holds,'mechanical_write_authorized':False,'party_write_authorized':False}
    result['preview_sha256']=sha(result)
    return result

def technical_dryrun_writeset(source:SourceSnapshot,body:str,preview:dict):
    """Build testable minimal edit-set for base values, NOT admissible for dispatch.
    FF300 is NOT resolved and therefore this plan cannot be sent to Notion.
    """
    if source.source_hash!=sha(body) or source.page_id!=preview['source']['id'] or source.fingerprint()!=preview['source']['fingerprint']:raise GateHold('SOURCE_FINGERPRINT_MISMATCH')
    if preview['mechanical_write_authorized']:raise GateHold('UNEXPECTED_PREVIEW_WRITE_AUTH')
    b=preview['before'];n=preview['after_pre_ff300']
    substitutions=[]
    def unique(old,new,label):
        if body.count(old)!=1:raise GateHold(f'{label}_NOT_UNIQUE_{body.count(old)}')
        substitutions.append({'field':label,'old':old,'new':new})
    active=body.split('## Regras TEST — estrutura')[0]
    def line(old,new,label):
        if active.count(old)!=1:raise GateHold(f'{label}_ACTIVE_AMBIGUOUS')
        unique(old,new,label)
    line('**Nível:** 17','**Nível:** 19','level')
    line('**Destreza:** 13 (inclui +3 equipamento da fixture)','**Destreza:** 15 (inclui +3 equipamento da fixture)','des_effective')
    line('**Constituição:** 10','**Constituição:** 11','con_effective')
    line('**Inteligência:** 8','**Inteligência:** 9','int_effective')
    line('### Vida: 240/309','### Vida: 240/'+str(n['hp_max']),'life_max_pre_ff')
    line('### Alma: 150/273 (30 comprometidos)','### Alma: 150/'+str(n['pa_max'])+' (30 comprometidos)','pa_max')
    line('**FF:** 290','**FF:** 320','ff')
    line('**CA:** 23','**CA:** 25','ca_without_ff_lock')
    table=body.split('## Regras TEST — estrutura',1)[1].split('</table>',1)[0]
    for x,y,label in [('<td>DES</td>\n<td>13</td>','<td>DES</td>\n<td>15</td>','des_table'),('<td>CON</td>\n<td>10</td>','<td>CON</td>\n<td>11</td>','con_table')]:
        if table.count(x)!=1:raise GateHold('TABLE_ROW_MISMATCH_'+label)
        unique(x,y,label)
    after=body
    for e in substitutions:
        if after.count(e['old'])!=1:raise GateHold('EDIT_CONFLICT_'+e['field'])
        after=after.replace(e['old'],e['new'],1)
    for token in ('<columns>','</columns>','<table','</table>','<details','</details>','<page url=','<mention-page','<image','notion-file-block://'):
        if body.count(token)!=after.count(token):raise GateHold('STRUCTURE_CHANGED_'+token)
    return {'status':'DRYRUN_ONLY_FF300_PENDING_DENY_DISPATCH','event':EVENT,'base_edits':substitutions,'preserved_children':source.structural['child_ids'],'expected_base_body_sha256':sha(after),'ff300_provenance':'PENDING','ready_to_dispatch':False}
