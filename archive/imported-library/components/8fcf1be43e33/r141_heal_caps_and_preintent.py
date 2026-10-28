"""New isolated source-derived fixtures: precise cap and rejection no-intent.
Each test uses a new frozen genesis and its own SQLite database, no historical replay.
"""
from pathlib import Path
import json,hashlib,sqlite3,copy
import r138_multiround_native as m
ROOT=Path(__file__).resolve().parent
PREREG={'operation':'OP-VLAB-FUSION-SANDBOX-01','stage':'R141',
 'source':'Eristan Reconstituição 75 PA 8d10+25 plus gloves +20 once; max HP and no resurrection',
 'seed_base':993100,'run_ids':['R141_HEAL_CAP_S993101']+[f'R141_NEG_GATE_{k}_S{993110+i}' for i,k in enumerate(['FULL_HP','LOW_PA','NO_STANDARD','RANGE','KO','WRONG_DICE'])],
 'fixture':'Eristan acts in frozen fixture with Feryn 14 HP missing, not historical injury nor a full scene; no initiative proof',
 'holdout':'NONE; targeted laboratory checks only','no_repeat':'R138/R137 originals immutable'}

def prereg():
 p=ROOT/'R141_PREREG.json';data=m.can(PREREG)
 if p.exists():assert p.read_text()==data
 else:p.write_text(data)

def init_fixture(run,seed,mode):
 file=ROOT/'runs'/f'{run}.sqlite'
 if file.exists():raise ValueError('NO_RESTART_EXISTING_Fixture')
 m.core.init_db(file,'A',seed)
 st=m.genesis(run,seed);st['phase']='ACTIVE';st['active']='E';st['round']=1
 st['order']=['E','A','F1'];st['actors']['E']['resource']['standard']=1;st['actors']['E']['resource']['movement']=1
 st['actor_turns']['E']=1;st['actors']['F1']['resource']['hp']=465
 st['fixture_mode']='R141_SOURCE_DERIVED_WOUND_14_NOT_OFFICIAL';st['prereg_sha256']=hashlib.sha256((ROOT/'R141_PREREG.json').read_bytes()).hexdigest()
 if mode=='FULL_HP':st['actors']['F1']['resource']['hp']=479
 if mode=='LOW_PA':st['actors']['E']['resource']['pa']=74
 if mode=='NO_STANDARD':st['actors']['E']['resource']['standard']=0
 if mode=='KO':st['actors']['F1']['resource']['hp']=0
 head=m.core.sha({'genesis':st,'lineage':'R18_R26_V081_R141_HEAL_FROZEN_FIXTURE'})
 with m.core.connect(file) as c:
  for k,v in [('scene',st['scene']),('genesis',head),('head',head),('state',m.core.canonical(st))]:
   c.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
 file.with_suffix('.genesis.json').write_text(m.core.canonical(st)+'\n')
 return file

def inspect(file):
 with sqlite3.connect(file) as db:
  meta=dict(db.execute('select key,value from meta'))
  return {'head':meta['head'],'state':meta['state'],'revision':meta['revision'],
  'events':db.execute('select count(*) from events').fetchone()[0],
  'pending':db.execute('select count(*) from pending').fetchone()[0]}

def run():
 prereg();out=[]
 modes=['CAP','FULL_HP','LOW_PA','NO_STANDARD','RANGE','KO','WRONG_DICE']
 for i,mode in enumerate(modes):
  seed=993101 if mode=='CAP' else 993110+i-1
  runid='R141_HEAL_CAP_S993101' if mode=='CAP' else f'R141_NEG_GATE_{mode}_S{seed}'
  file=init_fixture(runid,seed,mode);before=inspect(file)
  st,_,_=m.core.load(file);d=m.dice(st,'E','HEAL',1,8,10)
  payload={'target':'F1','distance_m':6 if mode=='RANGE' else 3,
    'dice':[1]*8 if mode=='WRONG_DICE' else d}
  if mode=='CAP':
   event=m.command(file,'HEAL',payload)
   sc,_,n=m.core.load(file);after=inspect(file)
   heal=event['detail']['native_actions'][0]
   assert n==1 and heal['gross_heal']>=45 and heal['actual_healed']==14 and heal['hp_after']==479
   assert heal['excess_heal']==heal['gross_heal']-14
   assert sc['actors']['E']['resource']['pa']==729 and sc['actors']['F1']['resource']['hp']==479
   out.append({'mode':mode,'run_id':runid,'status':'NATIVE_PASS','gross':heal['gross_heal'],
     'effective':heal['actual_healed'],'overheal':heal['excess_heal'],
     'PA_spent':75,'events_after':after['events'],'source_restriction':'no resurrection; cap maximum HP'})
  else:
   try:m.command(file,'HEAL',payload)
   except Exception as exc:
    after=inspect(file)
    assert after==before and after['pending']==0 and after['events']==0
    assert m.core.load(file)[2]==0
    out.append({'mode':mode,'run_id':runid,'status':'REJECT_PRE_INTENT',
     'error':str(exc),'zero_pending':True,'zero_events':True,'state_unchanged':True})
   else:raise AssertionError('NEGATIVE_TEST_ACCEPTED_'+mode)
 report={'operation':'OP-VLAB-FUSION-SANDBOX-01','stage':'R141',
  'source_fixture':'MESTRE_ONLY_PRECREATE', 'native_cap_pass':sum(v['mode']=='CAP' and v['status']=='NATIVE_PASS' for v in out),
  'negative_pass':sum(v['status']=='REJECT_PRE_INTENT' for v in out),'cases':out}
 (ROOT/'R141_HEAL_CAP_NEGATIVES.json').write_text(m.can(report))
 return report
if __name__=='__main__':print(m.can(run()))
