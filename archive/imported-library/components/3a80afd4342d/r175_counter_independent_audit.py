"""Counter variation independent auditor. No import from engine or producer; verifies
R18 chain, causal R50/R51 linkage, per-attack RNG/damage/HP/reaction and checkpoint.
"""
import json,sqlite3,pathlib,hashlib,random,collections,sys
VERSION='VLAB-R175-ED-BE-SOURCE-PHYSICAL-TEST-v1'
F={'AUREN':dict(hp=523,pa=719,ca=225,rd=35,bonus=193,n=8,faces=8,flat=211),
 'ROC':dict(hp=4200,pa=3740,ca=164,rd=75,bonus=150,n=20,faces=10,flat=0)}
def canon(o):return json.dumps(o,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def sha(o):return hashlib.sha256(canon(o).encode()).hexdigest()
def roll(seed,label,n,f):return [random.Random(int.from_bytes(hashlib.sha256(f'{VERSION}|{seed}|{label}|{n}d{f}'.encode()).digest(),'big')).randint(1,f)] if False else _roll(seed,label,n,f)
def _roll(seed,label,n,f):
 r=random.Random(int.from_bytes(hashlib.sha256(f'{VERSION}|{seed}|{label}|{n}d{f}'.encode()).digest(),'big'));return [r.randint(1,f) for _ in range(n)]
def tape(seed,who,n):
 f=F[who];return {'critical':roll(seed,f'{who}-TURN{n}-CRIT',3,6),'hit':roll(seed,f'{who}-TURN{n}-HIT',6,6),'hit_weak':roll(seed,f'{who}-TURN{n}-HIT-WEAK',6,6),'damage':roll(seed,f'{who}-TURN{n}-DAMAGE',f['n'],f['faces'])}
def counter_tape(seed,n):return {'rolls':[roll(seed,f'AUREN-COUNTER-ROC-TURN{n}-TRY{i}',6,6) for i in (1,2)],'critical':roll(seed,f'AUREN-COUNTER-ROC-TURN{n}-CRIT',3,6),'damage':roll(seed,f'AUREN-COUNTER-ROC-TURN{n}-DAMAGE',8,8)}
def crit(seq):return 'POSITIVE' if seq[:2]==[6,6] and seq[2]>=5 else 'NEGATIVE' if seq[:2]==[1,1] and seq[2]<=2 else 'NONE'
def audit(path):
 path=pathlib.Path(path);c=sqlite3.connect(str(path));m=dict(c.execute('SELECT key,value FROM meta'));rows=list(c.execute('select seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha from events order by seq'));p=list(c.execute('select cmd_id from pending'));c.close();assert not p
 st=json.loads(m['state']);seed=st['seed'];assert seed==1750101 and st['r175_counter_policy'].startswith('AUREN_R50_R51')
 assert st['r175_order_branch']=='AUREN_FIRST' and st['source_status']=='SOURCE_DOCUMENTED_ED_AND_PRECREATE_BE_SCOPE_CONDITIONAL'
 hp={x:f['hp'] for x,f in F.items()};pa={x:f['pa'] for x,f in F.items()};react={x:1 for x in F};std={x:0 for x in F}
 count=collections.Counter();turns=collections.Counter();prev=m['genesis'];after=None;active=None;native=[];counter_decl=0;counter_response=0;hit_by=collections.Counter();loss_by=collections.Counter()
 for seq,cmd,p0,row_json,row_sha,before_sha,after_sha in rows:
  r=json.loads(row_json);assert seq==r['seq'] and cmd==r['cmd_id'] and p0==prev==r['prev'] and sha(r)==row_sha
  assert r['before_sha']==before_sha and r['after_sha']==after_sha
  if after is not None:assert before_sha==after
  after=after_sha;prev=row_sha
  d=r['detail'];new=[]
  if r['kind']=='R175_SOURCE_START':
   assert seq==1 and d['order']==['AUREN','ROC'];active='AUREN';new=d['native_events']
  else:
   a=d['actor'];other='ROC' if a=='AUREN' else 'AUREN';assert active==a and d['target']==other
   turns[a]+=1;tt=tape(seed,a,turns[a]);assert d['tape']==r['payload']['tape']==tt
   assert d['source_page'].endswith('3ebc2b324ede814bb730d47dd7bd5f02') if a=='AUREN' else d['source_page'].endswith('3f3c2b324ede813987deda0b382e83c7')
   normal=d['attack'];f=F[a];fo=F[other]
   assert normal['from']==a and normal['to']==other and normal['attack_origin']=='NORMAL'
   is_weak=10*hp[a]<f['hp'];attempts=[sum(tt['hit']),sum(tt['hit_weak'])] if is_weak else [sum(tt['hit'])]
   score=min(attempts)+f['bonus']-2 if is_weak else attempts[0]+f['bonus'];assert normal['roll_score']==score
   cstate=crit(tt['critical']);hit=(score>fo['ca'] or cstate=='POSITIVE') and cstate!='NEGATIVE'
   assert normal['hit']==hit and normal['critical']==cstate
   raw=sum(tt['damage'])+f['flat']+(f['n']*f['faces'] if cstate=='POSITIVE' else 0) if hit else 0
   post=max(0,raw-fo['rd']) if hit else 0
   loss=min(hp[other],post);over=max(0,post-hp[other]);assert (normal['raw'],normal['rd_applied'],normal['net'])==(raw,fo['rd'] if hit else 0,post)
   assert (normal['before_hp'],normal['after_hp'],normal['hp_loss_actual'],normal['overkill'])==(hp[other],hp[other]-loss,loss,over)
   assert std[a]==1;std[a]=0;hp[other]-=loss
   count['attempts']+=1;count['hits']+=int(hit);count['post_rd']+=post;count['hp_loss']+=loss;count['overkill']+=over;count['crit_positive']+=int(cstate=='POSITIVE');count['crit_negative']+=int(cstate=='NEGATIVE');hit_by[a]+=int(hit);loss_by[a]+=loss
   if a=='ROC':
    ct=counter_tape(seed,turns[a]);assert d['counter_tape']==r['payload']['counter_tape']==ct
    dec=d['declaration'];cou=d['counter'];assert dec and cou
    assert dec['action']=='COUNTER_DECLARE' and dec['by']=='AUREN' and dec['against']=='ROC' and dec['consumes_reaction'] is True and dec['before_attack_resolution'] is True
    assert react['AUREN']==1;react['AUREN']=0;counter_decl+=1;count['reactions_spent']+=1
    assert cou['declaration_seq']==dec['seq'] and cou['original_attack_seq']==normal['seq']==dec['seq']+1 and cou['seq']==normal['seq']+1
    if hit:
     assert cou['action']=='COUNTER_NO_RESPONSE';assert cou['incoming_hit'] is True
    else:
     assert cou['action']=='COUNTER_RESPONSE' and cou['attack_origin']=='COUNTER' and cou['R51_nested_counter_enabled'] is False
     assert cou['advantage_rolls']==[ct['rolls'][0],ct['rolls'][1]] or tuple(map(tuple,cou['advantage_rolls']))==tuple(map(tuple,ct['rolls']))
     assert cou['attack_bonus']==193 and cou['advantage_bonus']==2
     cs=max(sum(x) for x in ct['rolls'])+193+2;ccrit=crit(ct['critical']);assert ccrit!='NEGATIVE';counterhit=(cs>F['ROC']['ca'] or ccrit=='POSITIVE')
     assert cou['roll_score']==cs and cou['hit']==counterhit and cou['critical']==ccrit
     rawc=sum(ct['damage'])+211+(8*8 if ccrit=='POSITIVE' else 0) if counterhit else 0
     netc=max(0,rawc-75) if counterhit else 0;lossc=min(hp['ROC'],netc);overc=max(0,netc-hp['ROC'])
     assert (cou['raw'],cou['rd_applied'],cou['net'])==(rawc,75 if counterhit else 0,netc)
     assert (cou['before_hp'],cou['after_hp'],cou['overkill'])==(hp['ROC'],hp['ROC']-lossc,overc)
     hp['ROC']-=lossc;counter_response+=1
     count['attempts']+=1;count['hits']+=int(counterhit);count['post_rd']+=netc;count['hp_loss']+=lossc;count['overkill']+=overc;count['crit_positive']+=int(ccrit=='POSITIVE');hit_by['AUREN']+=int(counterhit);loss_by['AUREN']+=lossc
   new=d['new_native_events']
   assert d['HP_after']==hp and d['PA_after']==pa
   if hp['ROC']==0:
    assert d['scheduler']['ko']=='ROC';active=None
   elif hp['AUREN']==0:
    assert d['scheduler']['ko']=='AUREN';active=None
   else:
    active=other;assert d['scheduler']['next_turn']==active
  for x in new:
   assert x['seq']==len(native)+1;native.append(x);kind=x['action']
   if kind=='turn_start':
    actor=x['by'];assert std[actor]==0 and hp[actor]>0;std[actor]=1;react[actor]=1
   elif kind=='turn_end':assert std[x['by']]==0
   elif kind=='weapon_attack':assert x['from'] in F and x['to'] in F
   elif kind=='COUNTER_DECLARE':pass
   elif kind in ('COUNTER_RESPONSE','COUNTER_NO_RESPONSE'):pass
   else:raise AssertionError(('unexpected_native',kind))
 assert prev==m['head'] and after==sha(st) and int(m['revision'])==len(rows)
 assert st['phase']=='FINISHED' and st['winner']=='AUREN' and hp=={k:v['resource']['hp'] for k,v in st['actors'].items()}
 assert pa=={k:v['resource']['pa'] for k,v in st['actors'].items()}
 assert react=={k:v['resource']['reaction'] for k,v in st['actors'].items()}
 assert len(st['r175_native_events'])==len(native) and st['r175_native_events']==native
 assert len(st['r175_history'])==len(rows)-1
 for key in st['r175_counts']:assert st['r175_counts'][key]==count[key],(key,st['r175_counts'][key],count[key])
 doc=json.loads(pathlib.Path(str(path)+'.checkpoint.json').read_text());assert sha(doc['body'])==doc['sha256'] and doc['body']['state']==st and doc['body']['head']==prev
 return {'audit':'PASS_R175_COUNTER_INDEPENDENT','db':path.name,'commits':len(rows),'native_events':len(native),'counter_declarations':counter_decl,'counter_responses':counter_response,'rounds':st['round'],'winner':st['winner'],'metrics':dict(count),'hits_by_actor':dict(hit_by),'actual_hp_removed_by_actor':dict(loss_by),'hp_after':hp,'pa_after':pa,'head':prev}
if __name__=='__main__':print(json.dumps(audit(sys.argv[1]),indent=2,ensure_ascii=False))
