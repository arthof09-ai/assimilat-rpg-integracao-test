"""In-memory source errors + hash-rebuilt SQLite clones; never touches accepted DBs."""
import json,sqlite3,shutil,copy,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'code'),str(ROOT/'runtime/native'),str(ROOT/'runtime/fusion_stage12')]
import r225_confirmed_rounding_native as sim
import r215_integrated_native as old
from vlab_effects_v08 import Scene,ActorActionState,cast_source_specified_spell,Resistances,EffectBlocked
from r225_independent_readonly_audit import audit_file,sha
PRE=json.loads((ROOT/'sources/R225_PREREG_BEFORE_EXEC.json').read_text());PH=hashlib.sha256((ROOT/'sources/R225_PREREG_BEFORE_EXEC.json').read_bytes()).hexdigest();DEC=json.loads((ROOT/'sources/R225_MASTER_DECISION_SOURCE.json').read_text())

def sc(provenance='R225-TEST'):
    a=old.actor('E');b=old.actor('R');a.standard=1
    return Scene({'E':a,'R':b},provenance=provenance)
def attempt(s,pol,auth,dice):
    source=old.SPORES
    return cast_source_specified_spell(s,'E','R',source=source,
      state=ActorActionState('E',20,s.actors['E'].pa,(source.action_id,),standard_available=True,range_confirmed=True,enemy_ids_visible=('R',)),
      proofs=(old.PROOFS['E'],),damage=61,damage_tag='planta',rd=Resistances(general=0,provenance='R225-LAB'),explicit_save_effect='SAVE-HALF',target_save_exceeds_cd=True,
      odd_half_rounding_test_policy=pol,rounding_decision_source=auth,damage_rolls=dice,damage_faces=10,documented_flat_bonus=10)

def in_memory_controls():
    good=(5,)*9+(6,);cases=[('NO_POLICY',None,None,good,'R225-TEST'),('WRONG_AUTH',sim.POL,'FOREIGN',good,'R225-TEST'),('UNVERIFIED_DICE',sim.POL,sim.AUTH,(1,)*10,'R225-TEST'),('NON_TEST_PROVENANCE',sim.POL,sim.AUTH,good,'R225-PRODUCTION')]
    ret=[]
    for name,pol,auth,dice,prov in cases:
        s=sc(prov);before=(s.actors['E'].pa,s.actors['R'].hp,s.actors['E'].standard,len(s.events))
        try:attempt(s,pol,auth,dice);raise AssertionError('ILLEGAL_ACCEPT:'+name)
        except EffectBlocked as exc:
            assert (s.actors['E'].pa,s.actors['R'].hp,s.actors['E'].standard,len(s.events))==before
            ret.append({'case':name,'blocked':True,'unmodified':True,'reason':str(exc)})
    return ret

def forge(clone,field,value):
    c=sqlite3.connect(clone);meta=dict(c.execute('select key,value from meta'));st=json.loads(meta['state']);rec=json.loads(c.execute('select row_json from events').fetchone()[0]);
    if field=='DECISION':st['r225']['decision']=value
    elif field=='ROUND':rec['detail']['events_added'][0]['raw']=value;st['native_events'][0]['raw']=value
    elif field=='PA':st['actors']['E']['pa']=value
    else:raise AssertionError('BAD_FORGE')
    # rebuild all relevant receipts to defeat hash-only verification
    rec['after_sha']=sha(st);c.execute('update events set row_json=?,row_sha=?,after_sha=?',(json.dumps(rec,sort_keys=True,separators=(',',':'),ensure_ascii=False),sha(rec),rec['after_sha']))
    c.execute('update meta set value=? where key="state"',(json.dumps(st,sort_keys=True,separators=(',',':'),ensure_ascii=False),))
    c.execute('update meta set value=? where key="head"',(sha(rec),))
    c.commit();c.close()

def adversarial():
    base=ROOT/'evidence/db/R225_SOURCE_GATED_ODD_61_S22560004.sqlite';case=next(r for r in PRE['new_runs'] if r['seed']==22560004)
    tmp=ROOT/'evidence/adversarial';tmp.mkdir(exist_ok=True);out=[]
    for name,field,value in [('FORGED_DECISION','DECISION','FALSE_AUTH'),('FORGED_ROUNDING','ROUND',31),('FORGED_PA','PA',804)]:
        p=tmp/f'R225_ADVERSARIAL_{name}.sqlite'
        if p.exists():raise FileExistsError('NO_REUSE_ADVERSARIAL')
        shutil.copy2(base,p);forge(p,field,value)
        try:audit_file(p,case,PH,DEC['decision_id']);raise AssertionError('AUDITOR_ACCEPTED_TAMPERING')
        except AssertionError as e:
            if str(e)=='AUDITOR_ACCEPTED_TAMPERING':raise
            out.append({'name':name,'rejected':True,'reason':str(e)})
    return out
if __name__=='__main__':
    o={'negative_controls':in_memory_controls(),'tamper_cases':adversarial(),'accepted_primary':3,'quarantine_preliminary':3}
    p=ROOT/'evidence/reports/R225_ADVERSARIAL_AND_PREFLIGHT.json';p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'PASS_R225_NEGATIVE_AND_FORGED_HASHES','negative':len(o['negative_controls']),'hash_rebuilt_attacks_rejected':len(o['tamper_cases'])},indent=2))
