"""Audits R176 SQLite without importing the producer, v0.8.1 or R18 modules.
Local independent-code audit, NOT an external human adjudication/NAC-PASS certification.
"""
import sqlite3,json,pathlib,hashlib,random,collections,sys
VERSION='VLAB-R176-GRIFFIN-BOUNDED-INIT-CONTACT-v1'
SEED=1760101
SOURCES={
 'AUREN':{'url':'https://app.notion.com/p/3ebc2b324ede814bb730d47dd7bd5f02','hp':523,'pa':719,'ca':225,'rd':35,'des':164,'bonus':193,'n':8,'faces':8,'flat':211,'status':'FICHA_MESTRE','type':'perfurante'},
 'GRIFFIN':{'url':'https://app.notion.com/p/3f3c2b324ede813987deda0b382e83c7','hp':4315,'pa':4016,'ca':153,'rd':75,'des':116,'bonus':138,'n':20,'faces':10,'flat':0,'status':'PRECREATE_BLUEPRINT','type':'cortante'}}

def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def sha(x):return hashlib.sha256(canon(x).encode()).hexdigest()
def dice(seed,key,n,faces):
 rng=random.Random(int.from_bytes(hashlib.sha256(f'{VERSION}|{seed}|{key}|{n}d{faces}'.encode()).digest(),'big'))
 return [rng.randint(1,faces) for _ in range(n)]
def tape(seed,who,turn):
 f=SOURCES[who]
 return {'critical':dice(seed,f'{who}-TURN{turn}-CRIT',3,6),
 'hit':dice(seed,f'{who}-TURN{turn}-HIT',6,6),
 'hit_weak':dice(seed,f'{who}-TURN{turn}-HIT-WEAK',6,6),
 'damage':dice(seed,f'{who}-TURN{turn}-DAMAGE',f['n'],f['faces'])}

def source_init(seed):
 a=dice(seed,'AUREN-INIT',6,6);g=dice(seed,'GRIFFIN-INIT',6,6)
 scored=sum(a)+166;gmin=sum(g)+116;gmax=gmin+22
 assert scored>gmax,(scored,gmax)
 return {'AUREN':{'dice':a,'score':scored,'source_bonus':2},
         'GRIFFIN':{'dice':g,'min':gmin,'max':gmax,'ordinary_proficiency_cap':22,'unresolved_specific_prof':True},
         'order':['AUREN','GRIFFIN'],'verdict':'UNAMBIGUOUS_UNDER_BOUNDED_HYPOTHESES',
         'hypothesis':'INIT_BONUS_IN_[0,22]_NO_EXTRA_EXTERNAL_MODIFIERS','NOT':'CERTIFIED_GRIFFIN_INIT_BONUS'}

def audit(db):
 db=pathlib.Path(db);c=sqlite3.connect(db)
 try:
  meta=dict(c.execute('SELECT key,value FROM meta'))
  rows=list(c.execute('SELECT seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha FROM events ORDER BY seq'))
  pending=list(c.execute('SELECT cmd_id FROM pending'))
 finally:c.close()
 assert not pending and int(meta['revision'])==len(rows) and len(rows)>1 and meta['mode']=='EXPERIMENTAL_LAB_ONLY'
 st=json.loads(meta['state']); assert st['seed']==SEED and st['r176_version']==VERSION and st['synthetic'] is True
 assert st['source_status']=='PRECREATE_SOURCE_SCOPED_PHYSICAL_ONLY_NOT_BENCHMARK' and st['phase']=='FINISHED'
 assert st['r176_unknown']==['GRIFFIN_INIT_SKILL_SPECIFIC','GRIFFIN_NOT_PHYSICALLY_PROMOTED','NATURAL_ENCOUNTER_GEOMETRY','COMPLETE_BEHAVIOR_AND_ABILITIES_NOT_EXERCISED']
 geo=st['r176_geometry'];assert geo['scenario_frozen'] is True and geo['relation']=='HITBOX_CONTACT' and geo['moving'] is False
 assert geo['same_vertical_contact_layer'] is True and geo['range_policy']=='CONTACT_ONLY_NO_METRIC_REACH_INFERRED'
 assert geo['canonical_reach_metres'] is None and geo['no_flying_bonus'] is True
 init=source_init(SEED);assert st['r176_initiative']==init
 for who,f in SOURCES.items():
  s=st['actors'][who]['stats'];assert s['source']==f['url'] and s['status']==f['status'] and s['attack_bonus']==f['bonus'] and s['physical_rd']==f['rd'] and s['des']==f['des']
 assert st['actors']['GRIFFIN']['stats']['initiative_named_prof'] is None
 hp={w:f['hp'] for w,f in SOURCES.items()};pa={w:f['pa'] for w,f in SOURCES.items()};reaction={w:1 for w in SOURCES};standard={w:0 for w in SOURCES}
 cnt=collections.Counter();turn=collections.Counter();natives=[];lastsha=meta['genesis'];lastafter=None;active=None
 attacker_hits=collections.Counter();effective=collections.Counter();attacks=collections.Counter();bonuses=[]
 for i,cmd,prev,rowjson,rowhash,before,after in rows:
  r=json.loads(rowjson)
  assert i==r['seq'] and cmd==r['cmd_id'] and prev==r['prev']==lastsha and r['kind'] in ('R176_INITIATIVE_AND_CONTACT','R176_PHYSICAL_CONTACT_ATTACK')
  assert sha(r)==rowhash and r['before_sha']==before and r['after_sha']==after
  if lastafter is not None:assert before==lastafter
  detail=r['detail'];incoming=[]
  if r['kind']=='R176_INITIATIVE_AND_CONTACT':
   assert i==1 and detail['initiative']==init and r['payload']['initiative']==init and r['payload']['seed']==SEED
   assert detail['order']==['AUREN','GRIFFIN'] and detail['geometry']==geo
   active='AUREN';incoming=detail['native_events']
  else:
   a=detail['actor'];d=detail['target'];assert a==active and d!=a and a in SOURCES and d in SOURCES
   assert detail['geometry_preflight']=='HITBOX_CONTACT' and r['payload']['actor']==a and r['payload']['target']==d
   assert r['payload']['seed']==SEED and detail['source_page']==SOURCES[a]['url'] and detail['target_page']==SOURCES[d]['url']
   turn[a]+=1;f=SOURCES[a];fd=SOURCES[d];t=tape(SEED,a,turn[a]);assert r['payload']['tape']==t==detail['tape']
   assert detail['actor_turn']==turn[a] and r['payload']['turn_number']==turn[a]
   expected_bonus=8 if a=='AUREN' and turn[a]>=3 else 0
   assert detail['mechanical_title_bonus']==expected_bonus
   bonuses.append(expected_bonus)
   e=detail['attack'];assert e['action']=='weapon_attack' and e['from']==a and e['to']==d and e['attack_origin']=='NORMAL'
   assert e['type']==f['type'] and e['ca_exact']==str(fd['ca']) and e['advantage_levels']==0 and e['disadvantage_levels']==0
   weak=hp[a]*10<f['hp'];attempts=[t['hit'],t['hit_weak']] if weak else [t['hit']]
   score=(min(map(sum,attempts))+f['bonus']+expected_bonus-2 if weak else sum(t['hit'])+f['bonus']+expected_bonus)
   assert e['weak_attacker']==weak and e['roll_score']==score and e['attack_roll_attempts']==attempts and e['critical_sequence']==t['critical']
   crit='POSITIVE' if t['critical'][:2]==[6,6] and t['critical'][2]>=5 else 'NEGATIVE' if t['critical'][:2]==[1,1] and t['critical'][2]<=2 else 'NONE'
   assert e['critical']==crit
   hit=(score>fd['ca'] or crit=='POSITIVE') and crit!='NEGATIVE'
   assert e['hit']==hit
   damage_normal=sum(t['damage'])+f['flat'];assert e['normal_damage']==damage_normal and e['damage_roll_groups']==[t['damage']]
   raw=(damage_normal+(f['n']*f['faces'] if crit=='POSITIVE' else 0)) if hit else 0
   post=max(0,raw-fd['rd']) if hit else 0;loss=min(hp[d],post);over=max(0,post-hp[d]); assert (e['raw'],e['rd_applied'],e['net'])==(raw,fd['rd'] if hit else 0,post)
   assert (e['before_hp'],e['after_hp'],e['hp_loss_actual'],e['overkill'])==(hp[d],hp[d]-loss,loss,over)
   assert standard[a]==1;standard[a]=0;hp[d]-=loss
   assert detail['HP_after']==hp and detail['PA_after']==pa and detail['reactions_after']==reaction
   cnt['attempts']+=1;cnt['hits']+=int(hit);cnt['post_rd']+=post;cnt['hp_loss']+=loss;cnt['overkill']+=over;cnt['crit_positive']+=int(crit=='POSITIVE');cnt['crit_negative']+=int(crit=='NEGATIVE')
   attacks[a]+=1;attacker_hits[a]+=int(hit);effective[a]+=loss;incoming=detail['new_native_events']
   if hp[d]==0:
    assert detail['scheduler']['ko']==d and detail['scheduler']['next_turn'] is None;active=None
   else:
    active=['AUREN','GRIFFIN'][(['AUREN','GRIFFIN'].index(a)+1)%2];assert detail['scheduler']['next_turn']==active
  for evt in incoming:
   assert evt['seq']==len(natives)+1 and evt['provenance']=='R176_CONTACT_INIT_BOUNDED_SOURCE_SCOPE_TEST';natives.append(evt)
   if evt['action']=='turn_start':
    who=evt['by'];assert standard[who]==0 and hp[who]>0;standard[who]=1;reaction[who]=1
   elif evt['action']=='turn_end':assert standard[evt['by']]==0
   elif evt['action']=='weapon_attack':assert evt['from'] in SOURCES and evt['to'] in SOURCES
   else:raise AssertionError(('unmodeled native event',evt['action']))
  lastsha=rowhash;lastafter=after
 assert st['winner']=='AUREN' and st['active'] is None and active is None
 assert lastsha==meta['head'] and lastafter==sha(st) and len(rows)==cnt['attempts']+1
 assert st['r176_events']==natives and len(st['r176_history'])==cnt['attempts']
 assert hp=={w:st['actors'][w]['resource']['hp'] for w in SOURCES}
 assert pa=={w:st['actors'][w]['resource']['pa'] for w in SOURCES}
 for k,v in cnt.items():assert st['r176_counts'][k]==v
 assert st['r176_counts']['pa_spent']==st['r176_counts']['reactions_spent']==0
 assert any(x==8 for x in bonuses),'No title activation, source completeness not proven'
 cp=pathlib.Path(str(db)+'.checkpoint.json');d=json.loads(cp.read_text());assert sha(d['body'])==d['sha256']
 assert d['body']['state']==st and d['body']['head']==lastsha and d['body']['revision']==len(rows)
 return {'result':'PASS_R176_SOURCE_BOUNDED_CAUSAL_REPLAY','db':db.name,'source_status':st['source_status'],'rounds':st['round'],'winner_conditional':st['winner'],
 'commits':len(rows),'native_events':len(natives),'attempts':dict(attacks),'hits':dict(attacker_hits),'hp_removed':dict(effective),
 'hp_final':hp,'pa_final':pa,'metric':st['r176_counts'],'auren_title_applied_attacks':sum(x==8 for x in bonuses),'initiative':init,'head':lastsha}
if __name__=='__main__':
 print(json.dumps(audit(sys.argv[1]),indent=2,ensure_ascii=False))
