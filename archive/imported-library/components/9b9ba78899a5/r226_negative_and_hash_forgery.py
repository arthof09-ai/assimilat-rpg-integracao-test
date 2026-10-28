"""Post-run R226 in-memory safety probes plus hash-rebuilt SQLite copies. No original state changed."""
import copy,json,sqlite3,shutil,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'code'),str(ROOT/'runtime/native'),str(ROOT/'runtime/fusion_stage12')]
import r226_manopla_pair_native as sim
from r226_independent_sqlite_pair_audit import audit_one,dig
from vlab_effects_v08 import DamageComponent,Resistances,mitigate

def source_probes():
    orig=ROOT/'evidence/db/R226_MANOPLA_SAME_PHYSICAL_WITH_MAGIC_S22681001.sqlite'
    c=sqlite3.connect(f'file:{orig}?mode=ro&immutable=1',uri=True)
    st=json.loads(dict(c.execute('select key,value from meta'))['state']);c.close()
    out=[]
    for name,patch in [('DUPLICATE_USE',{'item_used':True}),('LOW_PA',{'item_used':False,'pa':21}),('NO_EQUIPPED',{'item_used':False,'equipped':False})]:
        ss=copy.deepcopy(st);ss['active']='R';ss['turn']=0;ss['phase']='ACTIVE';ss['actors']['R']['standard']=0;ss['native_events']=[]
        ss['r226']['item_used']=patch['item_used'];ss['r226']['item_equipped_both']=patch.get('equipped',True)
        if 'pa' in patch:ss['actors']['R']['pa']=patch['pa']
        before=json.dumps(ss,sort_keys=True,ensure_ascii=False)
        try:sim.attack(ss,{'seed':22681001,'pre':sim.PH,'item':sim.IH},1);raise AssertionError('ILLEGAL_ITEM_ACTIVATION:'+name)
        except sim.SourceHold as ex:
            if json.dumps(ss,sort_keys=True,ensure_ascii=False)!=before:raise AssertionError('PREFLIGHT_MUTATED_DURABLE_CANDIDATE')
            out.append({'name':name,'blocked':str(ex),'no_candidate_mutation':True})
    e=mitigate((DamageComponent(30,'raio','R226-LAB-IMMUNITY-FIXTURE'),),Resistances(general=100,provenance='R226-HYPOTHETICAL-NOT_VAROK')).effective
    assert e==0
    out.append({'name':'ZERO_LIGHTNING_AFTER_RD_HYPOTHETICAL','magic_raw':30,'hypothetical_rd':100,'magic_effective':0,'no_slow_when_zero_by_source':True,'not_a_fight':True})
    return out

def forge(path,kind):
    con=sqlite3.connect(path);m=dict(con.execute('select key,value from meta'));st=json.loads(m['state']);last=json.loads(con.execute('select row_json from events where seq=2').fetchone()[0])
    if kind=='PA_FORGED':st['actors']['R']['pa']=333
    elif kind=='SLOW_EXPIRY_FORGED':st['native_events'][-1]['boundary']='END_OF_THE_CURRENT_TURN';last['detail']['events_added'][-1]['boundary']='END_OF_THE_CURRENT_TURN'
    elif kind=='ITEM_ACTIVATION_FORGED':st['r226']['item_used']=False
    elif kind=='HP_FORGED':st['actors']['V']['hp']+=1
    else:raise AssertionError('BAD_TAMPER_KIND')
    last['after_sha']=dig(st);j=json.dumps(last,sort_keys=True,separators=(',',':'),ensure_ascii=False)
    con.execute('update events set row_json=?,row_sha=?,after_sha=? where seq=2',(j,dig(last),last['after_sha']))
    con.execute('update meta set value=? where key="state"',(json.dumps(st,sort_keys=True,separators=(',',':'),ensure_ascii=False),))
    con.execute('update meta set value=? where key="head"',(dig(last),))
    con.commit();con.close()

def adversarial():
    origin=ROOT/'evidence/db/R226_MANOPLA_SAME_PHYSICAL_WITH_MAGIC_S22681001.sqlite';folder=ROOT/'evidence/adversarial';folder.mkdir(exist_ok=True)
    res=[]
    for kind in ['PA_FORGED','SLOW_EXPIRY_FORGED','ITEM_ACTIVATION_FORGED','HP_FORGED']:
        p=folder/f'R226_ADVERSARIAL_{kind}.sqlite'
        if p.exists():raise FileExistsError('ATTACK_COPY_COLLISION')
        shutil.copy2(origin,p);forge(p,kind)
        try: audit_one(p,sim.P,sim.IH,sim.PH,'SAME_PHYSICAL_WITH_MAGIC',22681001);raise AssertionError('AUDITOR_ACCEPTED_FORGERY')
        except AssertionError as ex:
            if str(ex)=='AUDITOR_ACCEPTED_FORGERY':raise
            res.append({'attack':kind,'rejected':True,'reason':str(ex)})
    return res
if __name__=='__main__':
    o={'in_memory_negative_tests':source_probes(),'hash_rebuilt_adversarial':adversarial(),'source':'R226 source-admitted TEST only'}
    (ROOT/'evidence/reports/R226_NEGATIVE_AND_ADVERSARIAL.json').write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'PASS_R226_INDEPENDENT_ADVERSARIAL_GATE','preflight_cases':len(o['in_memory_negative_tests']),'forgeries_rejected':len(o['hash_rebuilt_adversarial'])},indent=2))
