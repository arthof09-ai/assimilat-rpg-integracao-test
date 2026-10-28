"""R176 TEST gates and SQL semantically forged clones. Never touches old R175 banks."""
import pathlib,sys,sqlite3,json,hashlib,shutil,copy
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'code'))
import r176_bounded_initiative_combat as producer
import r176_independent_scientific_audit as audit
from vlab_effects_v08 import EffectBlocked

DB=ROOT/'evidence'/f'R176_AUREN_GRIFFIN_INIT_BOUNDED_DEV{producer.SEED}.sqlite'
CAN=lambda o:json.dumps(o,sort_keys=True,ensure_ascii=False,separators=(',',':'))
SHA=lambda o:hashlib.sha256(CAN(o).encode()).hexdigest()

def clone_and_rechain(label,edit):
 dst=ROOT/'evidence'/'negative_cases'/f'R176_TAMPER_{label}.sqlite'
 dst.parent.mkdir(parents=True,exist_ok=True)
 shutil.copy2(DB,dst)
 c=sqlite3.connect(dst)
 rows=[json.loads(x[0]) for x in c.execute('SELECT row_json FROM events ORDER BY seq')]
 st=json.loads(c.execute('SELECT value FROM meta WHERE key="state"').fetchone()[0])
 edit(rows,st)
 prev=c.execute('SELECT value FROM meta WHERE key="genesis"').fetchone()[0]
 for i,r in enumerate(rows):
  r['prev']=prev
  if i: r['before_sha']=rows[i-1]['after_sha']
  if i==len(rows)-1:r['after_sha']=SHA(st)
  rowsha=SHA(r)
  c.execute('UPDATE events SET prev=?,row_json=?,row_sha=?,before_sha=?,after_sha=? WHERE seq=?',
             (prev,CAN(r),rowsha,r['before_sha'],r['after_sha'],r['seq']))
  prev=rowsha
 c.execute('UPDATE meta SET value=? WHERE key="head"',(prev,));c.execute('UPDATE meta SET value=? WHERE key="state"',(CAN(st),));c.commit();c.close()
 # Rebuild checkpoint to avoid failures that are only due to stale metadata.
 cp=json.loads((pathlib.Path(str(DB)+'.checkpoint.json')).read_text())
 cp['body']['state']=st;cp['body']['head']=prev;cp['sha256']=SHA(cp['body'])
 pathlib.Path(str(dst)+'.checkpoint.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2))
 try:audit.audit(dst)
 except (AssertionError,ValueError,KeyError,TypeError) as exc:
  return {'clone':dst.name,'reason':'REJECTED_SEMANTICALLY','detail':str(exc)[:130],'structural_hashes_recomputed':True,'checkpoint_recomputed':True}
 raise AssertionError('FORGED_CLONE_PASSED:'+label)

def suite():
 good=audit.audit(DB); assert good['result']=='PASS_R176_SOURCE_BOUNDED_CAUSAL_REPLAY'
 # Certified only within bounded ordinary-proficiency hypotheses, never assign named initiative.
 init=producer.proof_of_order(producer.SEED)
 assert init['AUREN']['score']==193 and init['GRIFFIN']['max']==157 and init['order']==['AUREN','GRIFFIN']
 # Independent Roc universal max, using L3 6d6 + DES128 + ordinary proficiency up to +22.
 roc_ceiling=6*6+128+22
 assert roc_ceiling==186 and init['AUREN']['score']>roc_ceiling
 # General roll bands still overlap: NEVER generalize the order to every future seed.
 assert 166+6 <= 128+22+36
 st=producer.init_state(producer.SEED,contact=False);orig=copy.deepcopy(st)
 try:producer.start(st,{'seed':producer.SEED,'initiative':init},1)
 except EffectBlocked as exc:assert 'SPATIAL_PREFLIGHT_HOLD' in str(exc)
 else:raise AssertionError('disjoint preflight permitted')
 assert st==orig
 st=producer.init_state(producer.SEED);orig=copy.deepcopy(st);p=copy.deepcopy(init);p['GRIFFIN']['max']+=5
 try:producer.start(st,{'seed':producer.SEED,'initiative':p},1)
 except EffectBlocked as exc:assert 'INIT_PROVENANCE' in str(exc)
 else:raise AssertionError('forged initiative permitted')
 assert st==orig
 assert producer.geometry_gate(producer.init_state(producer.SEED)['r176_geometry'])
 # semantic forgeries with SQL chains + checkpoint deliberately rehashed
 bad=[]
 bad.append(clone_and_rechain('INITIATIVE',lambda rows,st: (rows[0]['detail']['initiative']['AUREN'].update({'score':202}),st['r176_initiative']['AUREN'].update({'score':202}))))
 bad.append(clone_and_rechain('GEOMETRY',lambda rows,st: (rows[0]['detail']['geometry'].update({'relation':'DISJOINT'}),st['r176_geometry'].update({'relation':'DISJOINT'}))))
 bad.append(clone_and_rechain('IDENTITY',lambda rows,st: rows[1]['detail'].update({'source_page':audit.SOURCES['GRIFFIN']['url']})))
 bad.append(clone_and_rechain('RD',lambda rows,st: rows[1]['detail']['attack'].update({'rd_applied':76})))
 def title_forge(rows,st):
  for r in rows:
   if r['kind']=='R176_PHYSICAL_CONTACT_ATTACK' and r['detail']['actor']=='AUREN' and r['detail']['actor_turn']==3:
    r['detail']['mechanical_title_bonus']=0;return
  raise AssertionError('turn3 not found')
 bad.append(clone_and_rechain('TITLE',title_forge))
 result={'suite':'R176_INDEPENDENT_TESTS_AND_SQL_ADVERSARIAL','passes':{'math_replay':True,'grifo_order_bounded':True,'roc_upper_bound_for_frozen_Auren_roll':True,'no_universal_order_assumption':True,'contact_preflight_fail_closed':True,'initiative_payload_forgery_fail_closed':True,'legal_contact_gate':True,'rehashed_sql_semantic_clones_rejected':len(bad)==5},'adversarial':bad,'source_scope':'NO_EXACT_GRIFFIN_OR_ROC_INIT_PROF_CERTIFICATION',
         'initiative':init,'roc_new_seed_conditional_ceiling':roc_ceiling,'full_source_admission':'HOLD','contracts_terminal':0,'benchmarks_official':0}
 (ROOT/'evidence'/'R176_INDEPENDENT_SUITE.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 return result
if __name__=='__main__':print(json.dumps(suite(),ensure_ascii=False,indent=2))
