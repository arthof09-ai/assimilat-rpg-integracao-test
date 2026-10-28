"""Independent R151 cold auditor: standard library only. Does NOT import runtime/engine.
Replays event ordering, RNG, full resource state and hash chain, not just final state.
"""
import json,hashlib,sqlite3,random,copy,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
VERSION='VLAB-R18-INTERACTIVE-CLI-0.1-EXPERIMENTAL'
def can(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def sha(x):return hashlib.sha256(can(x).encode()).hexdigest()
def draw(seed,nonce,who,kind,n,f):
 h=hashlib.sha256(f'{seed}|{nonce}|R151-{who}-{kind}|{n}d{f}|{VERSION}'.encode()).digest()
 return [random.Random(int.from_bytes(h,'big')).randint(1,f)] if n==1 else [random.Random(int.from_bytes(h,'big')).randint(1,f) for _ in []] # replaced below

def rng(seed,nonce,who,kind,n,f):
 entropy=hashlib.sha256(f'{seed}|{nonce}|R151-{who}-{kind}|{n}d{f}|{VERSION}'.encode()).digest()
 r=random.Random(int.from_bytes(entropy,'big'));return [r.randint(1,f) for _ in range(n)]
def check(cond,msg):
 if not cond:raise AssertionError(msg)

def replay(path):
 path=Path(path)
 st=json.loads(path.with_suffix('.genesis.json').read_text())
 with sqlite3.connect(path) as con:
  meta=dict(con.execute('select key,value from meta'))
  rows=[json.loads(x[0]) for x in con.execute('select row_json from events order by seq')]
  pending=con.execute('select count(*) from pending').fetchone()[0]
 check(not pending,'UNKNOWN EFFECT pending')
 check(meta['mode']=='EXPERIMENTAL_LAB_ONLY','mode');check(len(rows)==int(meta['revision']),'rev count')
 prev=meta['genesis'];normal=0;spells=0;neg=0;damage=0;PA=0;turns=0;action_log=[]
 for i,row in enumerate(rows,1):
  check(row['seq']==i and row['prev']==prev,'event head');check(row['before_sha']==sha(st),'source before state')
  check(row['synthetic'] and row['official_effects']==0,'canon write')
  actor=st['active'];kind=row['kind'];p=row['payload'];natives=row['detail']['native_actions'];extra=row['detail']['extra'];seed=st['seed']
  if kind=='INIT':
   check(st['phase']=='INIT' and p=={'seed':seed},'initiative phase')
   computed=[]
   for who,act in st['actors'].items():
    pr=act['source_profile'];roll=rng(seed,0,who,'INIT',pr['init_dice'],6)
    computed.append({'id':who,'dice':roll,'des':pr['dex'],'total':sum(roll)+pr['init_bonus'],'source':pr['source']})
   check(sorted(computed,key=lambda x:x['id'])==sorted(extra['rows'],key=lambda x:x['id']),'initiative dice source')
   check(len({x['total'] for x in computed})==len(computed),'tie not evaluated by this fixture')
   order=[r['id'] for r in sorted(computed,key=lambda x:(x['total'],x['des']),reverse=True)]
   check(order==extra['tie']['order'] and not natives,'initiative order')
   st.update({'order':order,'active':order[0],'phase':'ACTIVE','round':1})
  elif kind=='START':
   r=st['actors'][actor]['resource'];check(p=={'actor':actor} and r['standard']==0 and r['hp']>0,'start gate')
   check(len(natives)==1 and natives[0]['action']=='turn_start','start native')
   r['standard']=r['movement']=r['reaction']=1;turns+=1
  elif kind=='END':
   r=st['actors'][actor]['resource'];check(p=={'actor':actor} and r['standard']==0,'end gate')
   check(natives[0]['action']=='turn_end','end native');st['turn_index']+=1
   living={who:st['teams'][who] for who,v in st['actors'].items() if v['resource']['hp']>0}
   if len(set(living.values()))<=1:
    st['phase']='FINISHED_HP0';st['winner']=next(iter(living),None);st['active']=None
   else:
    idx=st['order'].index(actor)
    for k in range(1,len(st['order'])+1):
     j=(idx+k)%len(st['order']);who=st['order'][j]
     if st['actors'][who]['resource']['hp']>0:
      st['active']=who
      if j<=idx:st['round']+=1
      break
    if st['round']>st['horizon']:st.update({'phase':'CENSORED_HORIZON','active':None,'winner':None})
  elif kind=='STRIKE':
   normal+=1;t=p['tape'];who=t['who'];target=t['target'];pr=st['actors'][who]['source_profile'];tar=st['actors'][target]['source_profile'];ra=st['actors'][who]['resource'];rt=st['actors'][target]['resource']
   check(who==actor and ra['standard']==1,'physical action availability')
   nonce=st['action_nonce'][who]+1;check(nonce==t['nonce'],'physical nonce')
   weak=ra['hp']*10<pr['hp'];net=max(-4,min(4,t['adv']-t['dis']-int(weak)))
   hit=[rng(seed,nonce,who,'NORMAL-HIT-'+str(j),pr['attack_dice'],6) for j in range(1+abs(net))]
   score=(max(map(sum,hit))+2*net if net>0 else min(map(sum,hit))+2*net if net<0 else sum(hit[0]))+pr['attack_flat']
   crit=[rng(seed,nonce,who,'NORMAL-CRIT-'+str(j),1,6)[0] for j in range(3)]
   d=[rng(seed,nonce,who,'NORMAL-DMG-'+str(j),n,f) for j,(n,f) in enumerate(pr['damage_dice'])]
   check(t['hit']==hit and t['score']==score and t['crit']==crit and t['damage_rolls']==d,'physical RNG mismatched')
   check(t['damage']==sum(map(sum,d))+pr['damage_flat'],'damage tape base')
   positive=crit[:2]==[6,6] and crit[2]>=5
   negative=crit[:2]==[1,1] and crit[2]<=2
   hit_flag=(score>rt['ca'] or positive) and not negative
   raw=(t['damage']+sum(n*f for n,f in pr['damage_dice']) if positive else t['damage']) if hit_flag else 0
   eff=max(0,raw-tar['rd']) if hit_flag else 0
   actual=min(rt['hp'],eff)
   rec=natives[0]
   check(rec['action']=='weapon_attack' and rec['hit']==hit_flag and rec['roll_score']==score,'native physical hit')
   check(rec['critical']==('POSITIVE' if positive else 'NEGATIVE' if negative else 'NONE'),'native critical')
   check(rec['raw']==raw and rec['net']==eff and rec['rd_applied']==(tar['rd'] if hit_flag else 0),'native physical damage/RD')
   check(rec['before_hp']==rt['hp'] and rec['after_hp']==rt['hp']-actual and rec['hp_loss_actual']==actual,'native HP')
   check(rec['overkill']==max(0,eff-rt['hp']),'overkill')
   if negative:
    neg+=1;check(rec['critical_failure_policy']=='CRITICAL_FAILURE / VLAB-LAB-POLICY' and rec['hit'] is False and rec['net']==0,'lab negative policy')
   rt['hp']-=actual;ra['standard']=0;st['action_nonce'][who]+=1;damage+=actual
   action_log.append([who,'BASIC',hit_flag,actual])
  elif kind=='SPELL':
   spells+=1;t=p['tape'];who=t['who'];target=t['target'];pr=st['actors'][who]['source_profile'];ra=st['actors'][who]['resource'];rt=st['actors'][target]['resource'];nonce=st['action_nonce'][who]+1
   check(who==actor and ra['standard']==1 and ra['pa']>=t['cost'],'spell PA or turn')
   typ=t['which']
   if typ=='SPORES':
    dl=rng(seed,nonce,who,'SPORES-DAMAGE',10,10);save=rng(seed,nonce,target,'SPORES-FORTITUDE',4,6);sc=sum(save)+24;cd=76;flat=10;cost=80
   else:
    check(typ=='TURB','unknown spell');dl=rng(seed,nonce,who,'TURB-DAMAGE',9,10);save=rng(seed,nonce,target,'TURB-REFLEX',4,6)
    sc=sum(save)+28;attack=rng(seed,nonce,who,'TURB-OFFENSE',4,6);cd=sum(attack)+92;flat=8;cost=60
    check(t['attack_roll']==attack,'Turb attack stream')
   raw=sum(dl)+flat;success=sc>cd
   check(t['dmg']==dl and t['save']==save and t['save_score']==sc and t['cd']==cd,'save RNG')
   check(raw==t['raw'] and success==t['save_success'] and cost==t['cost'],'spell inputs')
   check(not(success and raw%2),'odd-half must hold')
   afterraw=raw//2 if success else raw
   check(len(natives)==1 and natives[0]['action']=='spell','native spell')
   native=natives[0];check(native['damage_rolls']==dl and native['documented_flat_bonus']==flat,'flat proof')
   check(native['raw']==afterraw and native['rd_applied']==0 and native['effective']==afterraw,'conditional lab elemental damage')
   before=rt['hp'];rt['hp']=max(0,before-afterraw);ra['pa']-=cost;ra['standard']=0;st['action_nonce'][who]+=1
   check(native['hp_before']==before and native['hp_after']==rt['hp'] and native['PA_spent']==cost,'native spell HP/PA')
   check(extra['not_official_RD0'] is True,'RD0 assumption must stay labeled')
   damage+=before-rt['hp'];PA+=cost;action_log.append([who,typ,True,before-rt['hp']])
  else:raise AssertionError('unknown kind '+kind)
  check(sha(st)==row['after_sha'],'post state after '+str(i))
  check(sha(row)==sqlite_row_sha(path,i),'row SHA row'+str(i))
  prev=sha(row)
 check(prev==meta['head'] and sha(st)==sha(json.loads(meta['state'])),'terminal head/state')
 check(st['phase'] in ('FINISHED_HP0','CENSORED_HORIZON'),'terminal status')
 with sqlite3.connect(path) as con:integrity=con.execute('PRAGMA integrity_check').fetchone()[0]
 check(integrity=='ok','sqlite integrity')
 return {'run_id':st['run_id'],'verified':True,'events':len(rows),'rounds':st['round'],'status':st['phase'],'winner':st['winner'],
 'physical_attacks':normal,'spells':spells,'negative_critical_lab':neg,'PA':PA,'HP_effective':damage,'turn_starts':turns,
 'end_HP':{w:z['resource']['hp'] for w,z in st['actors'].items()},'final_hash':meta['head'],'replay':'FULL_STATE_REPLAY_WITH_INDEPENDENT_RNG_AND_SQLITE'}
def sqlite_row_sha(path,index):
 with sqlite3.connect(path) as con:return con.execute('select row_sha from events where seq=?',(index,)).fetchone()[0]
if __name__=='__main__':
 items=[]
 for p in sorted((HERE/'runs').glob('R15[78]*.sqlite')):
  if 'checkpoint' in p.name:continue
  items.append(replay(p))
 (HERE/'R159_COLD_TACTICAL_AUDIT.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(items,ensure_ascii=False,indent=2))
