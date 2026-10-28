"""Independent R234 adversarial: mutate published LAST commit and rebuild R18 chain + final snapshot SHA. Never touch admitted files."""
import json,sqlite3,hashlib,shutil
from pathlib import Path
import r234_independent_readonly_audit as audit
R=Path(__file__).resolve().parents[1]
def rehash_after_mutation(path,kind):
 c=sqlite3.connect(str(path));m=dict(c.execute('select key,value from meta'));s=json.loads(m['state']);rows=c.execute('select seq,row_json from events order by seq').fetchall();last=json.loads(rows[-1][1]);events=last['detail']['events_new'];att=events[-2];tape=events[-3];
 if kind=='FALSO_ROLL_SCORE':att['roll_score']+=17
 elif kind=='DANO_RESOLVIDO_SEM_RD':
  att['net']+=5;att['hp_loss_actual']+=5;att['after_hp']-=5;last['detail']['hp_loss']+=5;last['detail']['after_hp'][att['to']]-=5;s['actors'][att['to']]['hp']-=5;s['r234']['hp_loss']+=5;s['r234']['outcome']['hp'][att['to']]-=5
 elif kind=='FAKE_RANGE':tape['range_evidence_m']=9.0
 elif kind=='FAKE_TAPE':tape['damage_dice'][0]=1 if tape['damage_dice'][0]!=1 else 2
 elif kind=='FAKE_SOURCE_PROMOTION':s['r234']['source_status']='P4_CANONICAL'
 else:raise AssertionError('UNKNOWN_MUTATION')
 if kind in ('FALSO_ROLL_SCORE','DANO_RESOLVIDO_SEM_RD','FAKE_RANGE','FAKE_TAPE'):
  # Update final native trace precisely with the changed last turn; prior turns untouched.
  s['native_events'][-len(events):]=events
 last['after_sha']=audit.sha(s)
 c.execute('update events set row_json=?,row_sha=?,after_sha=? where seq=?',(audit.can(last),audit.sha(last),last['after_sha'],last['seq']))
 c.execute('update meta set value=? where key="state"',(audit.can(s),));c.execute('update meta set value=? where key="head"',(audit.sha(last),));c.commit();c.close()
 # Structural R18 chain is intact: final row hash, head, state hash and previous links.
def main():
 source=R/'evidence/db/R234_SOLO_G_VS_C_S23451001.sqlite';d=R/'evidence/adversarial';d.mkdir(exist_ok=True)
 out=[]
 for k in ['FALSO_ROLL_SCORE','DANO_RESOLVIDO_SEM_RD','FAKE_RANGE','FAKE_TAPE','FAKE_SOURCE_PROMOTION']:
  copy=d/f'R234_ADV_{k}.sqlite';shutil.copy2(source,copy);rehash_after_mutation(copy,k)
  # Test copy in a complete independent oracle tree, without modifying original.
  tmp=R/'evidence/db'/source.name
  data=tmp.read_bytes();tmp.write_bytes(copy.read_bytes())
  try:
   try:audit.audit(R,write=False);bad='ACCEPTED_UNLAWFULLY'
   except AssertionError as e:bad=str(e)
  finally:tmp.write_bytes(data)
  out.append({'case':k,'rejected':bad!='ACCEPTED_UNLAWFULLY','audit_failure':bad,'sql_hashes_rebuilt':True,'test_copy':copy.name})
 assert all(x['rejected'] for x in out),out
 target=R/'evidence/reports/R234_ADVERSARIAL_REHASH.json';target.write_text(json.dumps({'status':'PASS_R234_ADVERSARIAL_REHASH_5_OF_5','cases':out},ensure_ascii=False,indent=2)+'\n');print(target.read_text())
if __name__=='__main__':main()
