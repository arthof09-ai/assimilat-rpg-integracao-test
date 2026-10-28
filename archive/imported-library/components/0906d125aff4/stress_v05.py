"""Deterministic property/stress suite R05, no Notion API, no writes."""
from __future__ import annotations
import sys,random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from tests.test_adapters_v05 import envelope,NORMAL,TRANS
from save_snapshot_v05 import build_archive,save_append_only_preflight,verify_archived_readback,SaveHold
from adapters_family_v05 import identify
from nfm_structure_v05 import digest
from tx_workflow_v05 import Tx,TxHold
from progression_gate_v05 import RateComponent,prepare_rate_contract
from transform_contract_v04 import fixed_die_value

rng=random.Random(20261009)
M=10000
assert fixed_die_value(12)==7
checks=0
for idx in range(M):
    level=rng.randint(1,25)
    amount=rng.randint(0,100000)
    anchor=f'Vida: {amount}'
    raw=NORMAL.strip('\n').replace('Vida: 450',anchor)
    event=f'LVL-STRESS-{idx:07d}'
    c=build_archive(event_id=event,profile_key='ningning',preimage=raw,
        scope='active-root-toggle',source_page_id='648c2b32-4ede-8352-9233-014d8fef25a6',
        candidate_level=f'NIVEL-{level}')
    page=envelope(raw)
    plan=save_append_only_preflight(page_export_before=page,candidate=c)
    assert plan['content_to_append']==c['archive_markup'];checks+=1
    after=envelope(raw+'\n'+c['archive_markup'])
    ver=verify_archived_readback(exported_after_save=after,candidate=c)
    assert ver['source_sha256']==digest(raw) and not ver['allow_mutation'];checks+=1
    assert identify('ningning',envelope(raw+'\n'+TRANS))['candidate_current']['rank_from_title']['level']==15;checks+=1
    with_dup=False
    try:save_append_only_preflight(page_export_before=after,candidate=c)
    except SaveHold:with_dup=True
    assert with_dup;checks+=1
    # Tampering must fail, even if only a single health token was modified.
    corrupted=c['archive_markup'].replace(anchor,anchor+'9')
    with_tamper=False
    try:verify_archived_readback(exported_after_save=envelope(raw+'\n'+corrupted),candidate=c)
    except SaveHold:with_tamper=True
    assert with_tamper;checks+=1
    # Unknown-effect cannot advance until a targeted readback is recorded.
    t=Tx(event,'a'*36);t.ambiguous('OP1')
    with_unknown=False
    try:t.advance('CONFIRM_PLAYER_RATE',proof='player-response-ref-1')
    except TxHold:with_unknown=True
    assert with_unknown;checks+=1
    t.reopen_reconcile(observed_state='operation_applied',proof='verified-physical-reopen')
    assert not t.unknown_effect;checks+=1
    # Player confirmation cannot be inferred from race even if the total is known.
    rc=RateComponent('racial',2,'Criação de Ficha')
    z=prepare_rate_contract(character_id='PLAYER-1',player_character=True,components=[rc],current_level=level)
    assert z['status']=='HOLD_AWAITING_DIRECT_PLAYER_CONFIRMATION';checks+=1
    assert fixed_die_value(12)==7;checks+=1
    assert c['real_notional_write_allowed'] is False;checks+=1
print(f'R05_STRESS PASS {M}/{M} scenarios; {checks}/{checks} invariants; deterministic_seed=20261009; NO_NOTION_WRITES=True')
