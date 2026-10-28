"""R169 new cold validated cohort extraction and descriptive analysis. No modified historical ledgers."""
from pathlib import Path
import sys,sqlite3,json,csv,hashlib,collections,statistics
HERE=Path(__file__).parent;sys.path.insert(0,str(HERE))
from r162_receipt_producer_v1 import classify_committed_action
from r165_cold_temporal_independent import audit as cold165
from r166_cold_concurrent_independent import verify as cold166
from r168_cold_crocodile_independent import verify as cold168  # this import performs read-only independent audit; writes audit output only
R18='VLAB-R18-INTERACTIVE-CLI-0.1-EXPERIMENTAL'
canon=lambda o:json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'))
sha=lambda o:hashlib.sha256(canon(o).encode()).hexdigest()
sel=sorted([x for x in (HERE/'runs').glob('R168_ED_AUREN_VS_CROC_BASIC_*.sqlite') if '.checkpoint.' not in x.name]+[x for x in (HERE/'runs').glob('R166_V2_CASULO_AOO_*.sqlite') if '.checkpoint.' not in x.name]+[x for x in (HERE/'runs').glob('R165_FLECHA_TURN_EXPLICIT_V3_DEV_*.sqlite') if '.checkpoint.' not in x.name])
assert len(sel)==5,sel
allr=[];info={};peractors=collections.defaultdict(lambda:collections.Counter());bytype=collections.defaultdict(lambda:collections.Counter())
for db in sel:
 if db.stem.startswith('R165_'):aud=cold165(db);scope='EXPLICIT_TEMPORAL_FIXTURE';subjectmap={'I':'Iskiel','A':'Auren'}
 elif db.stem.startswith('R166_'):aud=cold166(db);scope='CONCURRENT_AOO_CAUSAL_FIXTURE';subjectmap={'F':'Feryn','V':'Varok','E':'Eristan','A':'Auren'}
 else:aud=cold168(db);scope='ED_CROC_PHYSICAL_EXOGENOUS_INITIATIVE';subjectmap={'E':'Auren','B':'Crocodilo de Lodo Astral Ancião'}
 with sqlite3.connect(f'file:{db.as_posix()}?mode=ro',uri=True) as c:
  assert c.execute('pragma integrity_check').fetchone()[0]=='ok';assert c.execute('select count(*) from pending').fetchone()[0]==0
  rows=list(c.execute('select seq,row_json,row_sha from events order by seq'))
  meta=dict(c.execute('select key,value from meta'))
 prev=meta['genesis'];nn=0;net=0;actual=0;overkill=0
 for i,rr,rhash in rows:
  row=json.loads(rr)
  assert i==row['seq'] and row['prev']==prev and sha(row)==rhash
  prev=rhash
  acts=row['detail'].get('native_actions') or ([row['detail']['native_action']] if row['detail'].get('native_action') else [])
  for j,a in enumerate(acts,1):
   if a.get('action') not in ('weapon_attack','spell'):continue
   receipt=classify_committed_action(a)
   who=a['from'] if a['action']=='weapon_attack' else a.get('by',row['detail'].get('actor'))
   target=a['to'] if a['action']=='weapon_attack' else a.get('target')
   who=subjectmap.get(who,who);target=subjectmap.get(target,target)
   r={'cohort':'R161_R170_NEW_NOT_MERGED_R160','run_id':db.stem,'seed':int(json.loads(db.with_suffix('.genesis.json').read_text())['seed']),
      'scenario_scope':scope,'seq_R18':i,'native_action_in_commit':j,'event_SHA256':rhash,'source_actor':who,'source_target':target,
      'attack_origin':a.get('attack_origin','SPELL'),'damage_type':a.get('type',''),
      'crit':a.get('critical','NONE'),'hit':a.get('hit','MAGIC_REQUIRES_SAVE'),'dice_attempts':json.dumps(a.get('attack_roll_attempts',[])),
      'save_or_reaction':json.dumps(a.get('defensive_reaction',None)),
      'raw_damage':receipt['raw_damage'],'rd_applied':receipt['rd_applied'],'net_post_RD':receipt['net_post_RD'],
      'hp_effectively_lost':receipt['hp_effectively_lost'],'overkill':receipt['overkill'],
      'hp_before':receipt['hp_before'],'hp_after':receipt['hp_after'],
      'PA_spent_allocated_to_event':55 if scope=='EXPLICIT_TEMPORAL_FIXTURE' and a['from']=='I' else 0,
      'position_conditioned':scope=='CONCURRENT_AOO_CAUSAL_FIXTURE',
      'independent_cold_status':'PASS','official_power_cell':False,'blinded_holdout':False,
      'limitations':{'EXPLICIT_TEMPORAL_FIXTURE':'directed critical, not combat',
       'CONCURRENT_AOO_CAUSAL_FIXTURE':'directed R42 crit, conditional Casulo expiry and synthetic initial wound',
       'ED_CROC_PHYSICAL_EXOGENOUS_INITIATIVE':'exogenous Beast initiative, physical-only repertoire, nonblind reserved seed'}[scope]}
   allr.append(r);nn+=1;net+=r['net_post_RD'];actual+=r['hp_effectively_lost'];overkill+=r['overkill'];peractors[who]['attacks']+=1
   peractors[who]['hits']+=int(a.get('hit',False) is True);peractors[who]['post_rd']+=r['net_post_RD'];peractors[who]['hp_effective']+=r['hp_effectively_lost']
   bytype[scope]['attacks']+=1;bytype[scope]['hp_effective']+=r['hp_effectively_lost'];bytype[scope]['overkill']+=r['overkill']
 assert prev==meta['head'] and len(rows)==int(meta['revision']) and net==actual+overkill,(db,net,actual,overkill)
 info[db.stem]={'scope':scope,'commits':len(rows),'native_attack_receipts':nn,'net_post_rd':net,'effective_hp_loss':actual,'overkill':overkill,'audit_status':'INDEPENDENT_COLD_PASS','sha256_sqlite':hashlib.sha256(db.read_bytes()).hexdigest(),'head':prev,'pending':0}
assert len(allr)==137 and sum(v['commits'] for v in info.values())==413,(len(allr),info)
assert sum(x['net_post_RD'] for x in allr)==sum(x['hp_effectively_lost']+x['overkill'] for x in allr)
output=HERE/'R169_NEW_NATIVE_RECEIPTS_137_SOURCE_SCOPED.csv'
with output.open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=list(allr[0]));w.writeheader();w.writerows(allr)
assert sum(int(r['hp_effectively_lost']) for r in allr if r['scenario_scope']=='ED_CROC_PHYSICAL_EXOGENOUS_INITIATIVE')==11160
actuals={'new_runs':len(info),'new_commits':sum(x['commits'] for x in info.values()),'new_offensive_receipts':len(allr),
         'damage_post_RD':sum(int(x['net_post_RD']) for x in allr),'hp_effective':sum(int(x['hp_effectively_lost']) for x in allr),'overkill':sum(int(x['overkill']) for x in allr),
         'actors':dict(peractors),'scope':dict(bytype),'per_run':info,'prior_R160':'154 receipts 466 commits historically separate; 3 receipt corrections made in newly exported file',
         'source_holds':['Beast natural Initiative unresolved','Casulo exact two turns expiry unresolved','Lightning RD Auren unknown','Grifo Descarga range short unquantified','Mixed damage split unknown','Second ED not admitted']}
(HERE/'R169_NEW_OBSERVATION_COUNTS.json').write_text(json.dumps(actuals,ensure_ascii=False,indent=2)+'\n')
science={'as_of':'2026-10-17','operation':'OP-VLAB-FUSION-SANDBOX-01','hypotheses_preregistered':[
 {'H':'CROC_PHYSICAL_BASE_ACCURACY_UNDER_CA','mechanical_max':'6d6+134 has maximum170 (6*6+134), Auren CA225','predicts':'Ordinary Crocodile bite misses; critical positive can auto-hit, if applicable','observed':'0/66 Crocodile bite hits across two physical-only source-conditional trials','limits':'One fixed policy, two seeds; NOT universal victory chance.'},
 {'H':'AUREN_BASE_PRECISION_OVER_CROC_CA','mechanical_min':'6d6+193 minimum199 versus Crocodile CA112','predicts':'Ordinary Auren attacks hit unless lab negative critical','observed':'66/66 physical attacks hit in these two observations','limits':'No reactive defense modeled in these Crocodile scenes, no creature specials.'},
 {'H':'RECEIPT_PHYSICAL_HP_CAP','mechanism':'actual HP lost=min(post-RD,HP before), overkill=post-RD-actual','observed':'R166 KO 114 post-RD,60 actual,54 overkill; R168 terminal blow overkill 152/62 respectively','limits':'Algebra and selected transaction events, not distributional damage model.'}],
 'new_Crocodile_bouts':2,'Crocodile_seed_families':['DEV','RESERVED_NONBLIND'],'seed_blind_independent_holdout':0,
 'actual_analytic_sample_size':'n=2 source-conditional Crocodile bouts, no independent policy comparison; 66 actor attacks/species observed but clustered by two duels',
 'RNG_causal_alignment':'Each source run cold audited within own command/RNG stream; cross-policy draws are not necessarily aligned. Do not pair events merely by ordinal index.',
 'stats':'Descriptive hit counts exact; no global win probability, no confidence interval claimed from n=2 selected seeds.',
 'progress_batteries':{'A':'Auren L3 normal ED conditional; 0 official new cells','B':'Grifo L2 derived no official cell, Initiative still gap','C':'second ED complete 0 newly admitted','D':'Crocodilo L3 distinct species Croc vs Grifo source-scoped evidence, official 0/27'},
 'original_power_benchmark':'0/1875 official cells','limitations':'R168 exogenous natural Beast initiative, basic-only attack, no full behavior. R165 and R166 technical fixtures not combat efficacy.'}
(HERE/'R169_CROCODILE_SCIENTIFIC_RESULT.json').write_text(json.dumps(science,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in actuals.items() if k not in ('per_run','actors','scope')},ensure_ascii=False,indent=2))
