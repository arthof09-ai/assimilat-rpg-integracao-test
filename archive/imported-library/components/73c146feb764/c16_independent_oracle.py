#!/usr/bin/env python3
"""Independent read-only audit, recomputes small set of C16 conclusions from original R205 SQLite."""
import sqlite3,glob,json,pathlib,collections,itertools,hashlib,csv
P=pathlib.Path(__file__).resolve().parent
folder=P/'src_r205/new/r205/evidence/db'
out=json.loads((P/'result/C16_R205_SCIENTIFIC_METRICS.json').read_text())
ledger=collections.Counter(); combat=[];atks=[];ring=[];crit=collections.Counter()
for path in sorted(folder.glob('*.sqlite')):
 name=path.name
 db=sqlite3.connect('file:'+str(path)+'?mode=ro',uri=True)
 commands=list(db.execute('SELECT row_json FROM events ORDER BY seq'))
 assert db.execute('SELECT count(*) FROM pending').fetchone()[0]==0
 seed=int(name.split('_S')[-1].split('_')[0]);cat='wind' if '_WIND_' in name else 'ring'
 pol=name.replace('.sqlite','').split(f'_S{seed}_')[-1]
 ordinary=[]
 for (j,) in commands:
  detail=json.loads(j)['detail'];attack=detail.get('attack')
  if attack:
   dice=attack['attack_roll_attempts'][0];rolled=sum(dice)+60;ca=float(attack['ca_exact']);critical=attack['critical']
   hit=critical=='POSITIVE' or (rolled>ca and critical!='NEGATIVE')
   assert int(hit)==int(attack['hit']) and rolled==attack['roll_score']
   ordinary.append(dict(score=rolled,roll=tuple(dice),ca=ca,hit=hit,turn=detail.get('own_turn'),loss=attack['hp_loss_actual']))
   crit[critical]+=1
  for event in detail.get('new_native_events',[]):
   action=event.get('action');ledger[action]+=event.get('pa_spent',0)
   if action=='r205_beast_attack_target_invalidated':
    assert event['attack_rolled']==False
    ring.append((seed,pol))
 combat.append(dict(seed=seed,cohort=cat,policy=pol,attacks=ordinary,commits=len(commands)))
 db.close()
assert len(combat)==20
assert sum(len(r['attacks']) for r in combat)==462
assert sum(x['commits'] for x in combat)==945
assert ledger['source_magic_defence_wind']==18 and ledger['source_magic_defence_wind_upkeep']==138
assert ledger['source_item_ring_mark']==32 and ledger['source_item_ring_return_reaction']==112
assert sum(ledger.values())==300
assert len(ring)==4
pairs=collections.defaultdict(dict)
for x in combat:pairs[(x['cohort'],x['seed'])][x['policy']]=x
same=0;prevented=0;ring_cf=0;ring_hit=0
for (co,seed),v in pairs.items():
 if co=='wind':
  a=v['NO_WIND']['attacks'];b=v['CAST_WIND_MAINTAIN']['attacks'];bm={x['turn']:x for x in b}
  for x in a:
   if x['turn'] not in bm:continue
   y=bm[x['turn']];assert x['roll']==y['roll'];same+=1
   if x['hit'] and not y['hit']:prevented+=1
 else:
  off=v['MAGIC_OFF']['attacks'];on=v['MAGIC_ON']['attacks']; a=[x for x in off if x['turn']==2]; assert len(a)==1
  assert not [x for x in on if x['turn']==2]
  ring_cf+=a[0]['loss'];ring_hit+=int(a[0]['hit'])
assert same==132 and prevented==28 and ring_cf==31 and ring_hit==1
assert out['cohort_wind']['matched_same_turn']['same_dice']==same
assert out['cohort_wind']['matched_same_turn']['threshold_crossings']==prevented
assert out['cohort_ring']['round2_off_actual_damage_sum']==ring_cf
assert out['cohort_ring']['round2_off_hits']==ring_hit
count71=sum(sum(d)+60>71 for d in itertools.product(range(1,7),repeat=3));count73=sum(sum(d)+60>73 for d in itertools.product(range(1,7),repeat=3))
assert count71==81 and count73==35
checks={'sqlite_originals_readonly':len(combat),'commits':sum(x['commits'] for x in combat),'native_attack_scores_verified':462,'critical_types':dict(crit),'pa_ledger':dict(ledger),'PA_total':sum(ledger.values()),'matched_identical_rolls':same,'matched_wind_prevented_hits':prevented,'ring_pre_roll_invalidations':len(ring),'ring_off_round2_hit':ring_hit,'ring_off_round2_loss':ring_cf,'ordinary_attack_p_ca71':f'{count71}/216','ordinary_attack_p_ca73':f'{count73}/216','simulation_executions':0,'sqlite_writes':0,'status':'PASS_C16_INDEPENDENT_READ_ONLY_ORACLE'}
(P/'result/C16_INDEPENDENT_QA.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(checks,ensure_ascii=False,indent=2))
