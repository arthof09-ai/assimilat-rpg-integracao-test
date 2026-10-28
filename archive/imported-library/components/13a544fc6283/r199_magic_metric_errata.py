"""R199 derivative correction for R198 metric; READ ONLY historical SQLite.
Uses R198 separate auditor for all structural and semantic validation, but never adopts
its asymmetric magic_hp_removed. Derives source-separated loss from native events.
"""
import json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'new/code'))
import r198_magic_independent_audit as old

def corrected(db):
    r=old.audit(db)
    import sqlite3
    conn=sqlite3.connect(f'file:{pathlib.Path(db)}?mode=ro',uri=True)
    try: st=json.loads(conn.execute("SELECT value FROM meta WHERE key='state'").fetchone()[0])
    finally:conn.close()
    loss_by={'ONG_P2':0,'LOBO_P1':0};received_by={'ONG_P2':0,'LOBO_P1':0}
    magical=0;gross_magic=0;postrd_magic=0;casts=0;pa=0
    spell_attack_seqs={e['attack_event_seq'] for e in st['native_events'] if e['action']=='spell_pa_cost'}
    for e in st['native_events']:
        if e['action']=='spell_pa_cost':casts+=1;pa+=e['PA_spent']
        if e['action']!='weapon_attack':continue
        fr,to=e['from'],e['to'];h=e['hp_loss_actual']
        loss_by[fr]+=h;received_by[to]+=h
        if e['seq'] in spell_attack_seqs:
            assert fr=='ONG_P2' and to=='LOBO_P1' and e['type']=='agua'
            magical+=h;gross_magic+=e['raw'];postrd_magic+=e['net']
    assert len(spell_attack_seqs)==casts
    assert casts==r['casts'] and pa==r['pa_spent']
    assert magical==loss_by['ONG_P2'] and received_by['LOBO_P1']==magical
    if r['policy']=='DECLINE_WHIP':assert casts==0 and magical==0
    r.pop('magic_hp_removed')
    r.update({'damage_caused_by_actor_hp':loss_by,'damage_received_by_actor_hp':received_by,
       'water_spell_hp_removed':magical,'water_spell_raw':gross_magic,'water_spell_post_rd':postrd_magic,
       'healing_by_actor':{'ONG_P2':0,'LOBO_P1':0},'metric_version':'R199_ERRATA_ASYMMETRIC_MAGIC_HP_REMOVED'})
    return r

def main():
    paths=sorted((ROOT/'new/evidence/magic_db').glob('*.sqlite'))
    assert len(paths)==8
    records=[corrected(p) for p in paths]
    dest=ROOT/'new/r199/evidence/R199_R198_MAGIC_METRICS_CORRECTED.json'
    output={'status':'PASS_R199_R198_DERIVED_METRIC_ERRATA','historical_sqlite_modified':False,
      'defect':'R198 old auditor recorded Ong HP loss under DECLINE_WHIP as magic HP removed',
      'fix':'Only source-correlated weapon_attack events with paired spell_pa_cost and type agua count as water spell HP removal',
      'records':records}
    dest.write_text(json.dumps(output,ensure_ascii=False,indent=2))
    assert sum(r['water_spell_hp_removed'] for r in records if r['policy']=='DECLINE_WHIP')==0
    assert sum(r['casts'] for r in records)==20 and sum(r['pa_spent'] for r in records)==160
    print(json.dumps({'status':output['status'],'runs':len(records),'decline_spell_hp':0,'casts':20,'PA':160,
        'total_spell_hp':sum(x['water_spell_hp_removed'] for x in records)}))
if __name__=='__main__':main()
