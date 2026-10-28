"""IBX-17 R51–R60: additive TEST-only experimental adapter to recovered R30/R42.

NOT an authoritative engine or Notion writer.  Runs normal-only subset of
Criação de Ficha Regras 2, 4, 5, 6 on synthetic actor without Spiritual Form,
actual equipment, advanced class transitions or FF milestone choices. R30
historical after-state is replayed from a previous receipt, NOT recomputed.

The guard intentionally refuses unspecified or official-source effects.
"""
from __future__ import annotations
from dataclasses import dataclass
from copy import deepcopy
from pathlib import Path
import hashlib, json, os, tempfile

ATTRS=('FOR','DES','CON','INT','SAB','CAR')
FIXED={6:4,8:5,10:6,12:7,20:12}
class LabHold(ValueError):pass

def raw(obj):return json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
def digest(obj):return hashlib.sha256(raw(obj)).hexdigest()
def deep(obj):return deepcopy(obj)

def validate_actor(a):
    if a.get('fixture')!='SYNTHETIC_HUMAN_NORMAL_ONLY':raise LabHold('REAL_ACTOR_NOT_ADMITTED')
    if a.get('race')!='Humano':raise LabHold('RACE_OUTSIDE_SUBSET')
    if a.get('transform') is not False:raise LabHold('TRANSFORMATION_UNCERTIFIED')
    if a.get('equipment') or a.get('titles') or a.get('temporary'):
        raise LabHold('EXTERNAL_MODIFIERS_REQUIRE_ORIGINAL_ENGINE')
    if not isinstance(a.get('level'),int) or not 1<=a['level']<=5:raise LabHold('RANK_OUTSIDE_BRONZE')
    if set(a.get('initial',{}))!=set(ATTRS) or sum(a['initial'].values())!=25:
        raise LabHold('INITIAL_25_INVALID')
    if any(not isinstance(v,int) or not 2<=v<=6 for v in a['initial'].values()):
        raise LabHold('HUMAN_INITIAL_RANGE_INVALID')
    if set(a.get('natural',{}))!=set(ATTRS):raise LabHold('MISSING_ATTRIBUTES')
    if any(type(x)!=int or x<2 for x in a['natural'].values()):raise LabHold('INVALID_NATURAL')
    if a['ff']!=(a['natural']['FOR']+a['natural']['DES']+a['natural']['CON'])*10:
        raise LabHold('FF_NOT_ALIGNED')
    if a['ff']>=100:raise LabHold('FF_REQUIRES_HISTORICAL_LOCKS')
    if a['hp_current']>a['hp_max'] or a['pa_current']>a['pa_max']:
        raise LabHold('RESOURCES_INCONSISTENT')
    if not a.get('dice_ledger') or len(a['dice_ledger'])!=a['level']:
        raise LabHold('DICE_HISTORY_MISSING')
    if a['hp_initial']!=10+a['initial']['CON'] or a['pa_initial']!=10+a['initial']['INT']:
        raise LabHold('INITIAL_RESOURCES_INVALID')
    if a['ca']!=6+a['natural']['DES']:raise LabHold('HUMAN_CA_INVALID')
    if sum(a['natural'].values())!=25+2*a['level']:raise LabHold('HUMAN_POINTS_HISTORY_MISMATCH')
    return True

def seed_human_level_one():
    # Exactly 25 initial, each 2..6.  At Bronze 1 fixed d6=4, allocation +2 INT.
    initial={'FOR':2,'DES':3,'CON':2,'INT':6,'SAB':6,'CAR':6}
    natural={**initial,'INT':8}
    return {'fixture':'SYNTHETIC_HUMAN_NORMAL_ONLY','race':'Humano',
       'level':1,'rank':'Bronze','initial':initial,'natural':natural,
       'equipment':{},'titles':{},'temporary':{},'transform':False,
       'hp_initial':12,'pa_initial':16,'hp_max':18,'pa_max':28,
       'hp_current':14,'pa_current':20,'ff':70,'ca':9,
       'dice_ledger':[{'level':1,'die':'d6','option':'FIXO_60','result':4,
          'allocation':{'INT':2},'origin':'SYNTHETIC_TEST_INPUT'}],
       'history':[{'event':'LEVEL_1_SYNTHETIC','status':'SETUP'}],
       'ref':'Criação de Ficha Regras 2,4,5,6 / 2026-10-16'}

def preview_up(before,allocation,*,dice=4):
    validate_actor(before)
    if before['level']>=5:raise LabHold('CROSS_RANK_REBASE_NOT_IN_SUBSET')
    if set(allocation)-set(ATTRS) or any(type(v)!=int or v<0 for v in allocation.values()) or sum(allocation.values())!=2:
        raise LabHold('ALLOCATION_INVALID')
    if dice!=4:raise LabHold('ONLY_DOCUMENTED_FIXED_D6')
    after=deep(before); after['level']+=1
    for k,val in allocation.items():after['natural'][k]+=val
    after['ff']=(after['natural']['FOR']+after['natural']['DES']+after['natural']['CON'])*10
    if after['ff']>=100:raise LabHold('FF_MILESTONE_CHOICE_REQUIRED')
    after['ca']=6+after['natural']['DES']
    after['hp_max']+=dice+after['natural']['CON']
    after['pa_max']+=dice+after['natural']['INT']
    # Actual life/soul not automatically healed by a level-up.
    after['dice_ledger'].append({'level':after['level'],'die':'d6','option':'FIXO_60','result':dice,
            'allocation':deep(allocation),'origin':'SYNTHETIC_TEST_INPUT'})
    after['history'].append({'event':'LEVEL_UP_PREVIEW','from':before['level'],'to':after['level']})
    validate_actor(after)
    return {'operation':'UP','status':'PREVIEW_ONLY','before':deep(before),'after':after,
            'before_sha256':digest(before),'after_sha256':digest(after),
            'scope':'LOCAL_SYNTHETIC_NORMAL_ONLY','official_writes':0,'notion_writes':0}

def historical_down_reference(reference_json):
    """Replays an authenticated *reported* before/after snapshot; not R17 computation."""
    snap=json.loads(Path(reference_json).read_text())['preview']; b=snap['antes']; a=snap['depois']
    if b['level']!=a['level'] or b['level']!=16:raise LabHold('LEVEL_LOSS_DETECTED')
    if b['natural']['DES']-a['natural']['DES']!=10:raise LabHold('DES_UNEXPECTED')
    if b['natural']['CON']-a['natural']['CON']!=5:raise LabHold('CON_UNEXPECTED')
    if a['normal']['hp_current']!=b['normal']['hp_current']:raise LabHold('WRONG_AUTOHEAL')
    if a['normal']['pa_current']!=b['normal']['pa_current']:raise LabHold('WRONG_AUTORECHARGE')
    if a['locks_total']!=b['locks_total'] or a['spirit_tap']!=b['spirit_tap']:
        raise LabHold('LOCK_OR_SPIRIT_DRIFT')
    if a['normal']['ff']!=290 or a['normal']['hp_natural']!=287 or a['normal']['hp_max']!=292:
        raise LabHold('HISTORICAL_RECEIPT_CONFLICT')
    return {'operation':'DOWN_REPLAY_R30_RECORDED_OUTPUT','status':'REFERENCE_REPLAY_ONLY',
            'before':deep(b),'after':deep(a),
            'before_sha256':digest(b),'after_sha256':digest(a),
            'source_file_sha256':hashlib.sha256(Path(reference_json).read_bytes()).hexdigest(),
            'notion_writes':0,'official_writes':0}

class ExperimentalStore:
    """Strictly local writable sandbox; verified atomic content, preview, idempotency."""
    def __init__(self,root,actor,*,allow_new=True):
        self.root=Path(root).resolve(); self.root.mkdir(parents=True,exist_ok=True)
        self.file=self.root/'state.json';self.events=self.root/'events.json'
        if self.file.exists():
            self.state=json.loads(self.file.read_text());self.journal=json.loads(self.events.read_text())
        elif allow_new:
            self.state=deep(actor);self.journal=[];self._write(self.file,self.state);self._write(self.events,self.journal)
        else:raise LabHold('MISSING_FIXTURE')
        self.origin=digest(self.state)
    def _write(self,p,obj):
        p=Path(p)
        if p.is_symlink() or p.parent.resolve()!=self.root:raise LabHold('PATH_ESCAPE_OR_SYMLINK')
        fd,name=tempfile.mkstemp(prefix='.tx-',dir=self.root)
        try:
            with os.fdopen(fd,'wb') as f:
                f.write(raw(obj));f.flush();os.fsync(f.fileno())
            os.replace(name,p)
        finally:
            if os.path.exists(name):os.unlink(name)
    def commit(self,plan,transaction_id,*,approved=True,inject_failure=False):
        if not isinstance(transaction_id,str) or not transaction_id.startswith('SIM-'):
            raise LabHold('ONLY_SIMULATED_TRANSACTION')
        for j in self.journal:
            if j['tx']==transaction_id:
                if j['after']==digest(self.state):return {'status':'NOOP_ALREADY_APPLIED','receipt':j}
                raise LabHold('REPLAY_UNMATCHED_STATE')
        if not approved:return {'status':'REFUSED_NO_WRITE'}
        if plan['before_sha256']!=digest(self.state):raise LabHold('SOURCE_DRIFT')
        if plan['after_sha256']!=digest(plan['after']):raise LabHold('AFTER_HASH_INTEGRITY')
        if inject_failure:raise LabHold('INJECTED_BEFORE_COMMIT')
        old=deep(self.state); self._write(self.root/f'archive-{transaction_id}.json',old)
        try:
            self._write(self.file,plan['after'])
            observed=json.loads(self.file.read_text())
            if digest(observed)!=plan['after_sha256']:raise LabHold('READBACK_FAILED')
            receipt={'tx':transaction_id,'before':digest(old),'after':digest(observed),'status':'TEST_COMMITTED'}
            self._write(self.events,self.journal+[receipt]);self.state=observed;self.journal.append(receipt)
            return {'status':'TEST_COMMITTED','receipt':receipt}
        except Exception:
            self._write(self.file,old);self.state=old
            raise
    def new_fork(self,folder):
        folder=Path(folder)
        if folder.resolve()==self.root:raise LabHold('FORK_SAME_FOLDER')
        return ExperimentalStore(folder,deep(self.state))
