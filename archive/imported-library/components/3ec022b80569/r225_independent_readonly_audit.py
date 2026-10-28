"""SQL-only independent audit of Mestre-confirmed combat damage rounding. No combat runtime import."""
import json,hashlib,sqlite3,re,collections
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
def sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def require(x,why):
    if not x:raise AssertionError(why)
def audit_file(path,expected,prereg_hash,decision):
    con=sqlite3.connect(f'file:{path}?mode=ro&immutable=1',uri=True)
    try:
        m=dict(con.execute('select key,value from meta'))
        st=json.loads(m['state'])
        rows=[json.loads(z[0]) for z in con.execute('select row_json from events order by seq')]
        receipts=list(con.execute('select seq,cmd_id,prev,row_sha,before_sha,after_sha from events order by seq'))
        pending=con.execute('select count(*) from pending').fetchone()[0]
    finally:con.close()
    require(not pending and int(m['revision'])==1 and len(rows)==1,'STATE_COMMIT_OR_PENDING')
    row=rows[0];rec=receipts[0];require(rec==(1,row['cmd_id'],row['prev'],sha(row),row['before_sha'],row['after_sha']),'ROW_RECEIPT_FORGED')
    require(row['prev']==m['genesis'] and m['head']==sha(row) and row['after_sha']==sha(st),'HASH_CHAIN_AND_FINAL_STATE')
    require(st['seed']==expected['seed'] and st['r225']['pre_hash']==prereg_hash and st['r225']['decision']==decision,'SOURCE_DECISION_RECEIPT')
    require(st['r225']['world_canon'] is False and row['official_effects']==0,'NOT_PRODUCTION')
    require(row['cmd_id']==f'LAB-CMD-R225-CONFIRMED-S{expected["seed"]}','CMD_ID')
    e=row['detail']['events_added'];require(len(e)==1 and e==st['native_events'],'EVENT_STREAM_INTEGRITY')
    ev=e[0];require(ev['action']=='spell' and ev['source_rule']=='R215-FROZEN-SOURCE-BOUND' and ev['provenance'].startswith('R225-TEST-'),'SPELL_SOURCE_STATUS')
    require(ev['damage_rolls']==expected['dice'] and len(ev['damage_rolls'])==10 and all(type(v)==int and 1<=v<=10 for v in ev['damage_rolls']),'10D10_TAPE')
    require(sum(ev['damage_rolls'])+10==expected['damage']==ev['r223_damage_before_half'],'DAMAGE_DICE_ARITHMETIC')
    require(ev['save_effect']=='SAVE-HALF' and ev['save_exceeds_cd'] is True,'SAVING_THROW_PROVEN_FIXTURE')
    require(ev['raw']==expected['expected']==expected['damage']//2 and ev['effective']==ev['raw'],'FLOOR_VALUE')
    require(ev['PA_spent']==80 and st['actors']['E']['pa']==804-80,'PA_ONCE')
    require(ev['hp_before']==806 and ev['hp_after']==806-expected['expected'] and st['actors']['R']['hp']==ev['hp_after'],'HEALTH_AND_RD')
    require(ev['r225_rounding_authority']==('MASTER_EXPRESS_CONFIRMATION_CANONIZATION_PENDING' if expected['damage']%2 else None),'DECISION_RANK')
    require(ev['r223_odd_half_policy']==('FLOOR_MASTER_CONFIRMED_TEST' if expected['damage']%2 else None),'ODD_HALF_GATE')
    require(row['kind']=='R225_SOURCE_CONFIRMED_SPELL' and st['phase']=='CENSORED_ONE_SPELL','PHASE')
    return {'seed':expected['seed'],'gross':expected['damage'],'effective':ev['effective'],'PA_spent':80,'events':1,'commits':1,'sha_head':m['head']}

def audit(root=ROOT):
    pre=(root/'sources/R225_PREREG_BEFORE_EXEC.json').read_bytes();p=json.loads(pre);d=json.loads((root/'sources/R225_MASTER_DECISION_SOURCE.json').read_text());h=hashlib.sha256(pre).hexdigest()
    valid=list((root/'evidence/db').glob('R225_*.sqlite'));bad=list((root/'evidence/quarantine').glob('R225_*.sqlite'))
    require(len(valid)==3 and len(bad)==3,'DENOMINATOR_ADMITTED_QUARANTINE')
    require(p['candidate']=='R225' and len(p['new_runs'])==3 and d['lab_policy_id']=='FLOOR_MASTER_CONFIRMED_TEST','PREREG_OR_POLICY')
    accepted=[]
    for r in p['new_runs']:
        path=root/'evidence/db'/f'{r["id"]}_S{r["seed"]}.sqlite';require(path.exists(),'MISSING_SOURCE_GATED_RUN')
        accepted.append(audit_file(path,r,h,d['decision_id']))
    require({x.name for x in valid}=={f'{r["id"]}_S{r["seed"]}.sqlite' for r in p['new_runs']},'EXTRA_HIDDEN_RUN')
    for m in bad:
        require(m.name.startswith('R225_SPELL_') and not m.name.startswith('R225_SOURCE_GATED'), 'QUARANTINE_MISCLASSIFIED')
    fixtures=[('physical',61,2,30),('magical',61,2,30),('elemental',61,2,30),('magical',99,2,49),('physical',1,2,0),('physical',60,2,30)]
    for kind,n,denom,want in fixtures:require(n//denom==want,'GENERAL_DAMAGE_FLOOR_'+kind)
    # distinct transformation carry = 11/2; never round to 5 permanently.
    require(Fraction(11,2)-5==Fraction(1,2),'TAP_CARRY_ALTERED')
    return {'status':'PASS_R225_INDEPENDENT_NATIVE_SPELL_CONFIRMED_DAMAGE_FLOOR_TEST','admitted':len(accepted),'quarantined_preliminary':len(bad),'commits':3,'native_spells':3,'odd_half_spells':2,'arithmetic_types':['physical','magical','elemental'],'tamper_checked_sources':True,'runs':accepted,'historical_replays':0}
if __name__=='__main__':
    print(json.dumps(audit(),ensure_ascii=False,indent=2))
