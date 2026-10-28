"""R183 scientific replay. No import of the source producer nor native damage/turn resolver.
Uses pinned source literal snapshots and an independently written state/event reduction.
Local independent-code audit is NOT an independent external approval.
"""
import pathlib,sqlite3,json,hashlib,random,collections,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
VERSION='R177-R186-NATIVE-R18-V081-VAROK-LEVIATHAN-1'
PRE_SHA='c6d979740af07874201ee12463eed97b5a778c06a6e4eed624780f8a21b49651'
S={'VAROK':{'name':'Sikong Varok','page':'https://app.notion.com/p/3f6c2b324ede81f49ea9efbe1a811091','role':'NPC_ENCOUNTER_PROPOSAL_NOT_ED','rank':'Ouro Negro 5','hp':734,'pa':324,'ca':83,'rd':35,'des':27,'atk_n':4,'atk_bonus':100,'n':10,'faces':10,'flat':48,'tag':'impacto'},
'LEVIATHAN':{'name':'Leviata de Ferro Mnemonico','page':'https://app.notion.com/p/3f3c2b324ede813987deda0b382e83c7','role':'BEAST_PRECREATE_NOT_PHYSICALLY_PROMOTED','rank':'Lendario 4','hp':6060,'pa':4260,'ca':110,'rd':75,'des':60,'atk_n':6,'atk_bonus':142,'n':20,'faces':10,'flat':0,'tag':'impacto'}}
CAN=lambda x:json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'))
SHA=lambda x:hashlib.sha256(CAN(x).encode()).hexdigest()
def roll(seed,who,turn,label,n,faces):
 e=hashlib.sha256(f'{VERSION}|{seed}|{who}|{turn}|{label}|{n}d{faces}'.encode()).digest()
 rng=random.Random(int.from_bytes(e,'big'));return [rng.randint(1,faces) for _ in range(n)]
def expected_tape(seed,who,turn):
 f=S[who];return{'crit':roll(seed,who,turn,'CRIT',3,6),'hit':roll(seed,who,turn,'HIT',f['atk_n'],6),'hit_weak':roll(seed,who,turn,'WEAK',f['atk_n'],6),'damage':roll(seed,who,turn,'DAMAGE',f['n'],f['faces'])}
def audit(db):
 db=pathlib.Path(db);c=sqlite3.connect(str(db))
 try:
  meta=dict(c.execute('SELECT key,value FROM meta'))
  rows=[(x[0],x[1],x[2],json.loads(x[3]),x[4],x[5],x[6]) for x in c.execute('SELECT seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha FROM events ORDER BY seq')]
  pending=list(c.execute('SELECT cmd_id FROM pending'))
 finally:c.close()
 assert meta['mode']=='EXPERIMENTAL_LAB_ONLY' and not pending
 assert len(rows)==int(meta['revision']) and len(rows)>=2
 st=json.loads(meta['state']);assert st['experiment_version']==VERSION and st['pre_registration_sha']==PRE_SHA
 pre=ROOT/'R184_PRE_REGISTRATION_BEFORE_EXECUTION.json';assert hashlib.sha256(pre.read_bytes()).hexdigest()==PRE_SHA
 assert st['scene_category']=='MESTRE_SIDE_TEST_SOURCE_SCOPED_NPC_VS_PRECREATE_BEAST_NOT_ED_VS_BE'
 assert st['unknowns']==['LEVIATHAN_NAMED_INITIATIVE_SKILL','LEVIATHAN_PHYSICAL_PAGE_PROMOTION','BEAST_NATURAL_ENGAGEMENT_GEOMETRY','NPC_PROPOSAL_NOT_OFFICIAL_CAMPAIGN','OTHER_BEAST_ABILITIES_NOT_EXERCISED']
 policy=st['policy'];assert policy in ('ARMOR_ON_FIRST_SOURCE_ATTACK','ARMOR_OFF')
 seed=st['seed'];assert seed in (17718001,17718002,17718011,17718012,17718013)
 g=st['geometry'];assert g=={'frozen':True,'surface_contact':True,'same_layer':True,'motion':False,'reach_m':None,'policy':'PHYSICAL_CONTACT_WITHOUT_METRIC_REACH','vertical':'CONTACT_TEST_ONLY','natural_encounter':False}
 for who,f in S.items():
  o=st['actors'][who]['stats'];assert o['source_url']==f['page'] and o['role']==f['role'] and o['rank']==f['rank'] and o['attack_fixed']==f['atk_bonus'] and o['rd']==f['rd']
 binit=roll(seed,'LEVIATHAN',0,'INIT',6,6);vinit=roll(seed,'VAROK',0,'INIT',4,6)
 init={'VAROK':{'dice':vinit,'exact':sum(vinit)+29,'named_prof_from_sheet':True},'LEVIATHAN':{'dice':binit,'floor_without_skill':sum(binit)+60,'named_prof':None},'order':['LEVIATHAN','VAROK'],'proof':'66 > 53 FOR ALL ORDINARY DICE AND ANY NONNEGATIVE BEAST SKILL BONUS','not':'CERTIFIED_BEAST_INITIATIVE_VALUE','external_modifiers':'NONE_SCENARIO_SCOPE'}
 assert st['init_record']==init and st['order']==['LEVIATHAN','VAROK'] and sum(vinit)+29 < sum(binit)+60
 hp={x:y['hp'] for x,y in S.items()};pa={x:y['pa'] for x,y in S.items()};standard={x:0 for x in S};reaction={x:1 for x in S};counts=collections.Counter();turns=collections.Counter();hist=[];natives=[];active=None;used=False;lastsha=meta['genesis'];lastafter=None;laststate=None
 for seq,cmd,prev,r,rowsha,before,after in rows:
  assert r['seq']==seq and r['cmd_id']==cmd and prev==r['prev']==lastsha
  assert SHA(r)==rowsha and r['before_sha']==before and r['after_sha']==after
  if lastafter is not None:assert before==lastafter
  assert r['synthetic']==True and r['official_effects']==0
  p=r['payload'];d=r['detail'];incoming=[]
  if seq==1:
   assert r['kind']=='SOURCE_ORDER_CONTACT_START';assert p['seed']==seed and p['geometry']==g and p['initiative']==init
   assert d['proof']==init and d['geometry']==g
   active='LEVIATHAN';incoming=d['native_events']
  else:
   assert r['kind']=='SOURCE_PHYSICAL_ATTACK_WITH_OPTIONAL_ARMOR'
   who=active;assert who is not None
   other='VAROK' if who=='LEVIATHAN' else 'LEVIATHAN'
   turns[who]+=1;tn=turns[who];f=S[who];ft=S[other]
   assert p['actor']==who and p['target']==other and p['seed']==seed and p['turn_number']==tn and p['policy']==policy
   assert d['actor']==who and d['target']==other and d['actor_turn']==tn and d['source_page']==f['page'] and d['target_page']==ft['page'] and d['seed']==seed and d['policy']==policy
   t=expected_tape(seed,who,tn);assert p['tape']==t==d['tape'];e=d['attack']
   weak=hp[who]>0 and hp[who]*10<f['hp'];att=[t['hit'],t['hit_weak']] if weak else [t['hit']]
   score=(min(map(sum,att))+f['atk_bonus']-2) if weak else sum(t['hit'])+f['atk_bonus']
   critical='POSITIVE' if t['crit'][:2]==[6,6] and t['crit'][2]>=5 else 'NEGATIVE' if t['crit'][:2]==[1,1] and t['crit'][2]<=2 else 'NONE'
   hit=(score>ft['ca'] or critical=='POSITIVE') and critical!='NEGATIVE'
   basic=sum(t['damage'])+f['flat'];gross=basic+(f['n']*f['faces'] if critical=='POSITIVE' and hit else 0) if hit else 0
   post=max(0,gross-ft['rd']) if hit else 0
   assert e['action']=='weapon_attack' and e['from']==who and e['to']==other and e['attack_origin']=='NORMAL' and e['ca_exact']==str(ft['ca']) and e['roll_score']==score
   assert e['critical_sequence']==t['crit'] and e['attack_roll_attempts']==att and e['normal_damage']==basic and e['damage_roll_groups']==[t['damage']]
   assert e['critical']==critical and e['hit']==hit and e['type']==f['tag']
   assert e['raw']==gross and e['net']==post and e['rd_applied']==(ft['rd'] if hit else 0)
   assert e['before_hp']==hp[other] and e['after_hp']==max(0,hp[other]-post) and e['hp_loss_actual']==min(hp[other],post) and e['overkill']==max(0,post-hp[other])
   armor=who=='LEVIATHAN' and policy=='ARMOR_ON_FIRST_SOURCE_ATTACK' and not used
   assert d['item_active']==armor and standard[who]==1
   if armor:
    assert reaction['VAROK']==1 and pa['VAROK']>=50;used=True;pa['VAROK']-=50;reaction['VAROK']=0;counts['pa_activation']+=50;counts['reactions']+=1
   prevented=min(70,post) if armor else 0
   eventual=max(0,post-prevented);loss=min(hp[other],eventual);over=max(0,eventual-hp[other])
   assert d['item_prevented']==prevented and d['item_after_hp']==hp[other]-loss and d['final_hp_loss']==loss and d['final_overkill']==over
   hp[other]-=loss;standard[who]=0
   counts['attack_attempts']+=1;counts['hits']+=int(hit);counts['gross_hit']+=gross;counts['post_rd_before_item']+=post;counts['item_prevention']+=prevented;counts['hp_lost']+=loss;counts['overkill']+=over;counts['crit_positive']+=int(critical=='POSITIVE');counts['crit_negative']+=int(critical=='NEGATIVE')
   hist.append({'seq':seq,'actor':who,'target':other,'hp_loss':loss,'item':armor,'item_prevented':prevented})
   incoming=d['native_events']
   if hp[other]==0:
    assert d['scheduler']=={'ko':other,'next_turn':None};active=None
   else:
    active=other;assert d['scheduler']['next_turn']==other
  for evt in incoming:
   assert evt['seq']==len(natives)+1 and evt['provenance']=='R177-R186-SOURCE-SCOPED-PURE-MEMORY-R18'
   if evt['action']=='turn_start':
    target=evt['by'];assert hp[target]>0 and standard[target]==0;standard[target]=1;reaction[target]=1
   elif evt['action']=='turn_end':assert standard[evt['by']]==0
   elif evt['action']=='SOURCE_ARMOR_DECLARE':
    assert used and evt['by']=='VAROK' and evt['incoming_from']=='LEVIATHAN' and evt['before_attack_roll'] and evt['pa_debit']==50 and evt['reaction_spent']==1 and evt['once_per_scene']
   elif evt['action']=='SOURCE_ARMOR_POST_RD_PREVENTION':
    assert evt['by']=='VAROK' and evt['source_page']==S['VAROK']['page'] and evt['incoming_attack_seq']==evt['seq']-1 and evt['declaration_seq']==evt['seq']-2
    assert evt['prevented']==prevented and evt['hp_final']==hp['VAROK'] and evt['hp_loss_actual_final']==loss and evt['overkill_final']==over and evt['PA_spent_in_declaration']==50
   elif evt['action']=='weapon_attack':assert evt==e
   else:raise AssertionError(('UNKNOWN_NATIVE_EVENT',evt['action']))
   natives.append(evt)
  if seq>1:
   assert d['HP_after']==hp and d['PA_after']==pa and d['Reaction_after']==reaction, (seq,d['Reaction_after'],reaction)
  lastsha=rowsha;lastafter=after
 assert len(rows)==len(hist)+1 and lastsha==meta['head'] and lastafter==SHA(st)
 assert st['history']==hist and st['native_events']==natives and st['armor_used']==used
 assert st['metrics']=={x:counts.get(x,0) for x in st['metrics']}
 assert {x:st['actors'][x]['resource']['hp'] for x in S}==hp and {x:st['actors'][x]['resource']['pa'] for x in S}==pa and {x:st['actors'][x]['resource']['reaction'] for x in S}==reaction
 assert st['phase'] in ('FINISHED','ACTIVE')
 if st['phase']=='FINISHED':assert active is None and st['winner']==('VAROK' if hp['LEVIATHAN']==0 else 'LEVIATHAN')
 cp=pathlib.Path(str(db)+'.checkpoint.json');packet=json.loads(cp.read_text());assert SHA(packet['body'])==packet['sha256'] and packet['body']['state']==st and packet['body']['head']==meta['head'] and packet['body']['revision']==len(rows)
 return {'result':'PASS_SOURCE_SCOPED_R18_NATIVE_REPLAY','db':db.name,'seed':seed,'policy':policy,'commits':len(rows),'native_events':len(natives),'attacks':len(hist),'winner':st['winner'],'rounds':st['round'],'HP_final':hp,'PA_final':pa,'metrics':dict(counts),'source_class':st['scene_category'],'admission':'CONDITIONAL_NOT_TERMINAL'}
if __name__=='__main__':print(json.dumps(audit(sys.argv[1]),ensure_ascii=False,indent=2))
