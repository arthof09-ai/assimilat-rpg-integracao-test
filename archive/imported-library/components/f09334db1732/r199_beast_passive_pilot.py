"""One source-listed Beast passive connected to existing R198 combat+native v0.8.1.
No alternative damage resolver. One conditional +2 STR interpretation, no other cumulative bonuses.
"""
from __future__ import annotations
import json,pathlib,hashlib,sys,copy
from collections import Counter
ROOT=pathlib.Path(__file__).resolve().parents[3];R199=ROOT/'new/r199'
sys.path.insert(0,str(ROOT/'new/code'))
import r198_microbenchmark as base
from vlab_effects_v08 import EffectBlocked
P=R199/'source/R199_BEAST_PREREG.json';PRE=json.loads(P.read_text());PRE_SHA=hashlib.sha256(P.read_bytes()).hexdigest()
PAIR=tuple(PRE['pair']);r18=base.r18

def setup(db,seed,policy):
 base.setup(db,seed,PAIR)
 c=r18.connect(str(db))
 try:
  st=json.loads(c.execute('SELECT value FROM meta WHERE key="state"').fetchone()[0]);st.update({'r199_beast_pre_sha':PRE_SHA,'r199_beast_policy':policy,
      'scope':'R199_BASIC_PLUS_LOBO_FORCA_ANCESTRAL_CONDITIONAL','r199_beast_bonus_applied_attacks':0})
  with c:c.execute('UPDATE meta SET value=? WHERE key="state"',(r18.canonical(st),))
 finally:c.close()

def start(st,p,seq):
 if p.get('r199_beast_pre_sha')!=PRE_SHA or p.get('r199_beast_policy')!=st['r199_beast_policy']:raise EffectBlocked('PREREG_DRIFT')
 return base.start(st,{k:v for k,v in p.items() if k not in ('r199_beast_pre_sha','r199_beast_policy')},seq)

def attack(st,p,seq):
 who=st['active'];power=who=='LOBO_P1' and st['r199_beast_policy']=='ANCESTRAL_PLUS2_IF_NOT_INCLUDED'
 if not power:return base.attack(st,p,seq)
 wolf=base.ACTORS['LOBO_P1'];orig_score=wolf['attack_bonus'];orig_damage=wolf['damage_flat']
 try:
  wolf['attack_bonus']=orig_score+2;wolf['damage_flat']=orig_damage+2
  receipt=base.attack(st,p,seq)
  st['r199_beast_bonus_applied_attacks']+=1
  receipt['source_passive_overlay']={'source':PRE['source'],'literal':PRE['literal_ability'],
    'rank':'PRATA_1','FOR_plus':2,'attack_bonus_before':orig_score,'attack_bonus_with_passive':orig_score+2,
    'damage_flat_before':orig_damage,'damage_flat_with_passive':orig_damage+2,
    'status':'TEST_CONDITIONAL_ALREADY_INCLUDED_NOT_RESOLVED','native_attack_seq':receipt['attack']['seq']}
  return receipt
 finally:
  wolf['attack_bonus']=orig_score;wolf['damage_flat']=orig_damage

def run_one(root,seed,policy):
 ident=f'R199_LOBO_ANCESTRAL_VS_CAPANGA_{seed}_{policy}';db=pathlib.Path(root)/(ident+'.sqlite')
 if db.exists():raise RuntimeError('NO_RUN_ID_REUSE')
 init,order=base.roll_initiative(seed,PAIR)
 if order is None:return {'id':ident,'seed':seed,'policy':policy,'status':'PRECOMMIT_TIE_HOLD'}
 setup(db,seed,policy)
 payload={'initiative':init,'order':order,'pre_reg_sha':base.PRE_SHA,'source_snap_sha':base.SOURCE_SHA,'r199_beast_pre_sha':PRE_SHA,'r199_beast_policy':policy}
 r18.event_commit(str(db),'LAB-CMD-'+ident+'-INIT','R199_BEAST_INIT',payload,start)
 for i in range(PRE['horizon_attacks']):
  st,_,_=r18.load(str(db))
  if st['phase']=='FINISHED':break
  who=st['active'];target=next(x for x in PAIR if x!=who)
  own_turn=1+sum(x['actor']==who for x in st['history']);f=st['actors'][who]['resource']
  weak=f['hp']>0 and 10*f['hp']<f['maximum_hp']
  p={'actor':who,'target':target,'own_turn':own_turn,'roll_tape':base.tape(seed,PAIR,who,own_turn,weak)}
  r18.event_commit(str(db),'LAB-CMD-'+ident+f'-ATK{i+1:03d}','R199_SOURCE_SCOPED_PHYSICAL_ATTACK',p,attack)
 st,head,rev=r18.load(str(db));base.write_checkpoint(str(db))
 return {'id':ident,'seed':seed,'policy':policy,'status':st['phase'] if st['phase']=='FINISHED' else 'CENSORED_HORIZON',
  'winner':st['winner'] if st['phase']=='FINISHED' else None,'rounds':st['round'],'commits':rev,'events':len(st['native_events']),
  'hp':{k:v['resource']['hp'] for k,v in st['actors'].items()},'pa':{k:v['resource']['pa'] for k,v in st['actors'].items()},
  'passive_attack_events':st['r199_beast_bonus_applied_attacks'],'metrics':st['metrics'],'db':db.name,'head':head}

def main():
 dest=R199/'evidence/db';dest.mkdir(exist_ok=True)
 rec=[run_one(dest,seed,policy) for seed in PRE['seeds'] for policy in PRE['policies']]
 (R199/'evidence/R199_BEAST_SPECIAL_RESULTS.json').write_text(json.dumps(rec,indent=2,ensure_ascii=False))
 print(json.dumps({'runs':len(rec),'status':dict(Counter(x['status'] for x in rec)),
  'winner':dict(Counter(x.get('winner') for x in rec)),
  'bonus_attack_receipts':sum(x.get('passive_attack_events',0) for x in rec)}))
if __name__=='__main__':main()
