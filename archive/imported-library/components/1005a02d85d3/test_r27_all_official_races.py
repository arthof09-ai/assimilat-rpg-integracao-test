"""F18: official R2 race contracts, independent hard-coded source golden values.
Synthetic legal initial attributes, NEVER a historical/Party character.
"""
import copy, tempfile, unittest, unicodedata
from engine_r17 import (race_official_fixture_r27,plan_r17,dice_contracts,validate_r17,
                        R17Hold,RACE_R2,RESOURCES)
from dialogue_r17 import DialogueR17
from roll_ledger_r17 import RollLedger
from durable_r14 import DurableStore
from safe_runner_r17 import SafeLocalR17Runner
from r10_recovery import digest

# Independently hand-calculated from the Notion canonical Criação de Ficha R2/R4/R5.
# Values include invented ARMOR=2, and NO CA from synthetic FF locks (the
# synthetic historic FF locks grant damage only, leaving official race CA isolated).
GOLDEN_BRONZE = {
  'Humano':       dict(rate=2, creation=25,initial_hp=24,initial_pa=22,initial_ca=13,
                       final_hp=33,final_pa=30,final_ca=15, hp_die=6,pa_die=6, alloc={'DES':2}),
  'Orc':          dict(rate=5, creation=37,initial_hp=32,initial_pa=24,initial_ca=24,
                       final_hp=46,final_pa=34,final_ca=25, hp_die=10,pa_die=6,alloc={'DES':4,'INT':1}),
  'Abissiano':    dict(rate=5, creation=37,initial_hp=22,initial_pa=34,initial_ca=15,
                       final_hp=30,final_pa=49,final_ca=20,hp_die=6,pa_die=10,alloc={'DES':5}),
  'Asa Prateada': dict(rate=4, creation=30,initial_hp=20,initial_pa=27,initial_ca=19,
                       final_hp=27,final_pa=38,final_ca=23,hp_die=6,pa_die=8,alloc={'DES':4}),
  'Raça Superior':dict(rate=8, creation=45,initial_hp=32,initial_pa=30,initial_ca=11,
                       final_hp=46,final_pa=47,final_ca=11,hp_die=10,pa_die=10,alloc={'DES':4,'INT':4}),
}
GOLDEN_PRATA = {
  'Humano':       dict(initial_hp=60,initial_pa=74,final_hp=75,final_pa=116,final_ca=15, hp_die=8,pa_die=8,alloc={'DES':2}),
  'Orc':          dict(initial_hp=88,initial_pa=110,final_hp=108,final_pa=225,final_ca=24,hp_die=12,pa_die=8,alloc={'INT':5}),
  'Abissiano':    dict(initial_hp=54,initial_pa=144,final_hp=68,final_pa=235,final_ca=20,hp_die=8,pa_die=12,alloc={'DES':5}),
  'Asa Prateada': dict(initial_hp=48,initial_pa=111,final_hp=61,final_pa=184,final_ca=23,hp_die=8,pa_die=10,alloc={'DES':4}),
  'Raça Superior':dict(initial_hp=88,initial_pa=162,final_hp=108,final_pa=341,final_ca=11,hp_die=12,pa_die=12,alloc={'INT':8}),
}

def options(level,allocation):
 return {'target_level':level,'normal_allocations':{str(level):allocation},
         'spirit_allocations':{str(level):{}},'milestones':{},'conditionals':{},
         'resource_modes':{k:'FIXO' for k in RESOURCES},'roll_receipts':{},
         'actor':'SIMULATED_TEST_AGENT','approval':'OFFLINE_SYNTHETIC_ONLY'}

class OfficialFiveRaceContractF18(unittest.TestCase):
 def test_five_races_are_exactly_the_canonical_list(self):
  self.assertEqual(set(GOLDEN_BRONZE),set(RACE_R2))
  self.assertEqual(len(RACE_R2),5)
 def test_all_five_races_bronze_growth_and_derivatives(self):
  for race,g in GOLDEN_BRONZE.items():
   with self.subTest(race=race):
    b=race_official_fixture_r27(race,1);n=b['NORMAL'];self.assertEqual(sum(n['initial_attrs'].values()),g['creation'])
    self.assertEqual(n['normal_rate'],g['rate']);self.assertEqual(n['hp_max'],g['initial_hp'])
    self.assertEqual(n['derived']['proficiencies_initial_count'],2+n['initial_attrs']['INT'])
    self.assertEqual(n['pa_max'],g['initial_pa']);self.assertEqual(n['derived']['ca'],g['initial_ca'])
    p=plan_r17(b,options(2,g['alloc']),'SIM-R27-BRONZE-'+race.replace(' ','_'))
    a=p['updates'];n1=a['NORMAL'];self.assertEqual(n1['level'],2)
    self.assertEqual(n1['hp_max'],g['final_hp']);self.assertEqual(n1['pa_max'],g['final_pa'])
    self.assertEqual(n1['derived']['ca'],g['final_ca']);self.assertEqual(n1['normal_rate'],g['rate'])
    self.assertEqual(p['steps'][0]['growth']['NORMAL_HP']['dice'],f"1d{g['hp_die']}")
    self.assertEqual(p['steps'][0]['growth']['NORMAL_PA']['dice'],f"1d{g['pa_die']}")
    self.assertEqual(a['TRANSFORM']['effective_level'],1)
    self.assertEqual(a['TRANSFORM']['overlay'],b['TRANSFORM']['overlay'])
    self.assertEqual(a['NORMAL']['hp_current'],b['NORMAL']['hp_current'])
    self.assertEqual(a['NORMAL']['pa_current'],b['NORMAL']['pa_current'])
    self.assertEqual(digest(b),p['before_digest'])
 def test_all_five_bronze5_prata1_rebase_is_source_exact(self):
  for race,g in GOLDEN_PRATA.items():
   with self.subTest(race=race):
    b=race_official_fixture_r27(race,5)
    self.assertEqual(b['NORMAL']['hp_max'],g['initial_hp'])
    self.assertEqual(b['NORMAL']['pa_max'],g['initial_pa'])
    p=plan_r17(b,options(6,g['alloc']),'SIM-R27-PRATA-'+race.replace(' ','_'))
    n=p['updates']['NORMAL'];self.assertEqual(n['level'],6)
    self.assertEqual(n['hp_max'],g['final_hp']);self.assertEqual(n['pa_max'],g['final_pa'])
    self.assertEqual(n['derived']['ca'],g['final_ca'])
    self.assertTrue(p['steps'][0]['rank_rebase'])
    self.assertEqual(p['steps'][0]['growth']['NORMAL_HP']['dice'],f"6d{g['hp_die']}")
    self.assertEqual(p['steps'][0]['growth']['NORMAL_PA']['dice'],f"6d{g['pa_die']}")
    self.assertEqual(p['steps'][0]['growth']['TRANSFORM_HP']['sum'],0)
 def test_each_race_end_to_end_atomic_local_commit_rollback_idempotency(self):
  for race,g in GOLDEN_BRONZE.items():
   with self.subTest(race=race),tempfile.TemporaryDirectory() as tmp:
    b=race_official_fixture_r27(race)
    event='SIM-R27-COMMIT-'+unicodedata.normalize('NFKD',race).encode('ascii','ignore').decode().replace(' ','_')
    dialog=DialogueR17(copy.deepcopy(b),2,event,RollLedger(tmp+'/roll'))
    for answer in ('CONFIRMO_NIVEIS',g['rate'],'FIXO',g['alloc'],'CONFIRMO'):
     dialog.respond(answer)
    self.assertEqual(dialog.phase,'READY')
    store=DurableStore(tmp+'/store',b);runner=SafeLocalR17Runner(store)
    receipt=runner.execute(dialog);self.assertEqual(receipt['status'],'COMMITTED_LOCAL_VERIFIED')
    self.assertEqual(store.get_all()['NORMAL']['hp_max'],g['final_hp'])
    self.assertEqual(runner.execute(dialog)['status'],'NOOP_VERIFIED_IDEMPOTENT')
    rollback=runner.rollback(dialog);self.assertEqual(rollback['status'],'ROLLED_BACK_VERIFIED_LOCAL')
    self.assertEqual(digest(store.get_all()),digest(b))
 def test_each_race_silver_rank_transition_commits_and_recovers(self):
  for race,g in GOLDEN_PRATA.items():
   with self.subTest(race=race),tempfile.TemporaryDirectory() as tmp:
    b=race_official_fixture_r27(race,5)
    slug=unicodedata.normalize('NFKD',race).encode('ascii','ignore').decode().replace(' ','_')
    dialog=DialogueR17(copy.deepcopy(b),6,'SIM-R27-SILVER-'+slug,RollLedger(tmp+'/roll'))
    for answer in ('CONFIRMO_NIVEIS',b['NORMAL']['normal_rate'],'FIXO',g['alloc'],'CONFIRMO'):
     dialog.respond(answer)
    store=DurableStore(tmp+'/store',b);runner=SafeLocalR17Runner(store)
    self.assertEqual(runner.execute(dialog)['status'],'COMMITTED_LOCAL_VERIFIED')
    self.assertEqual(store.get_all()['NORMAL']['hp_max'],g['final_hp'])
    self.assertEqual(store.get_all()['NORMAL']['pa_max'],g['final_pa'])
    self.assertEqual(store.get_all()['NORMAL']['derived']['ca'],g['final_ca'])
    self.assertEqual(runner.execute(dialog)['status'],'NOOP_VERIFIED_IDEMPOTENT')
    self.assertEqual(runner.rollback(dialog)['status'],'ROLLED_BACK_VERIFIED_LOCAL')
    self.assertEqual(digest(store.get_all()),digest(b))
 def test_unauthorized_or_unknown_races_fails_closed(self):
  s=race_official_fixture_r27('Orc')
  for bad in ('Elfo','Humano','Raça Superior'):
   x=copy.deepcopy(s);x['NORMAL']['race']=bad
   with self.assertRaises(R17Hold):validate_r17(x)
 def test_racial_extra_distribution_is_rejected_when_wrong(self):
  for race,wrong in [('Orc','INT'),('Abissiano','DES'),('Asa Prateada','FOR')]:
   s=race_official_fixture_r27(race);c=s['NORMAL']['racial_creation_contract'];bonus=c['racial_bonus']
   if race=='Asa Prateada':bonus['FOR']=1;bonus['DES']-=1
   else:
    src='FOR' if race=='Orc' else 'INT';bonus[src]-=1;bonus[wrong]+=1
   s['NORMAL']['initial_attrs']= {k:c['base'][k]+bonus[k] for k in c['base']}
   with self.assertRaises(R17Hold):validate_r17(s)
 def test_bad_creation_caps_fail_closed(self):
  for race in ('Humano','Orc','Abissiano','Asa Prateada','Raça Superior'):
   s=race_official_fixture_r27(race);n=s['NORMAL']
   n['initial_attrs']['FOR']+=100
   with self.assertRaises(R17Hold):validate_r17(s)
 def test_superior_speed_and_orc_exact_quarter_no_rounding(self):
  s=race_official_fixture_r27('Raça Superior');self.assertEqual(s['NORMAL']['derived']['speed'],10)
  p=plan_r17(s,options(2,{'DES':4,'INT':4}),'SIM-R27-SUPERIOR-SPEED')
  self.assertEqual(p['updates']['NORMAL']['derived']['speed'],11)
  o=race_official_fixture_r27('Orc');self.assertEqual(o['NORMAL']['derived']['ca'],24)
  # Synthetic +1 DES produces a quarter-point, not an invented integer rounding rule.
  p=plan_r17(o,options(2,{'DES':1,'INT':4}),'SIM-R27-ORC-FRACTIONAL-CA')
  self.assertEqual(p['updates']['NORMAL']['derived']['ca'],24.25)

if __name__=='__main__':unittest.main()
