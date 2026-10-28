"""R42 fail-closed CRAFT writer adapter. Prototype only; cannot fence OTHER sessions
with direct Notion shared credentials. This guards only a compliant caller.
"""
from dataclasses import dataclass
class Blocked(RuntimeError): pass
@dataclass(frozen=True)
class Authority:
    write_domain:str='CRAFT_F5'
    permit:str='RED'
    owner:str|None=None
    epoch:int|None=None
    predecessor_fenced:bool=False
    c19_reconciled:bool=False
    stop_ack_or_external_enforcement:bool=False
    candidate_hash:str|None=None

def can_commit(a:Authority, request:dict)->bool:
    if a.write_domain!='CRAFT_F5' or a.permit!='GREEN':raise Blocked('PERMIT_RED_OR_WRONG_DOMAIN')
    if not (a.predecessor_fenced and a.c19_reconciled and a.stop_ack_or_external_enforcement):raise Blocked('FENCE_OR_C19_UNVERIFIED')
    if a.epoch is None or a.epoch<=19 or not a.owner:raise Blocked('OWNER_EPOCH_UNVERIFIED')
    if request.get('expected_epoch')!=a.epoch or request.get('owner')!=a.owner:raise Blocked('STALE_OR_MISMATCHED_EPOCH')
    if request.get('contract_sha256')!=a.candidate_hash:raise Blocked('CONTRACT_HASH_MISMATCH')
    return True

def request_production(a:Authority, req:dict, write_fn):
    can_commit(a,req)
    # Native platform must recheck fencing atomically at commit, which the shared
    # Notion MCP connector currently does NOT expose. Therefore always DENY.
    raise Blocked('UNENFORCED_EXTERNAL_NOTION_FENCE_AT_WRITE')
