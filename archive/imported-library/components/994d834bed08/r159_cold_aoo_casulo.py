"""Independent pure stdlib semantic readback for R153/R154. Never import runtime modules."""
import json,hashlib,sqlite3,random
from pathlib import Path
ROOT=Path(__file__).resolve().parent
V='VLAB-R18-INTERACTIVE-CLI-0.1-EXPERIMENTAL'
def can(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def sha(x):return hashlib.sha256(can(x).encode()).hexdigest()
def dice(seed,ix,label,n,faces):
 h=hashlib.sha256(f'{seed}|{ix}|{label}|{n}d{faces}|{V}'.encode()).digest();r=random.Random(int.from_bytes(h,'big'));return [r.randint(1,faces) for _ in range(n)]
def check(cond,m):
 if not cond:raise AssertionError(m)

def load(path):
 st=json.loads(path.with_suffix('.genesis.json').read_text());con=sqlite3.connect(path)
 meta=dict(con.execute('select key,value from meta'))
 rows=[(seq,json.loads(row),rowsha) for seq,row,rowsha in con.execute('select seq,row_json,row_sha from events order by seq')]
 p=con.execute('select count(*) from pending').fetchone()[0];integrity=con.execute('pragma integrity_check').fetchone()[0];con.close()
 check(p==0 and integrity=='ok' and len(rows)==int(meta['revision']),'db integrity/pending')
 prev=meta['genesis']
 for i,row,rowsha in rows:
  check(i==row['seq'] and row['prev']==prev and rowsha==sha(row),'row integrity')
  prev=rowsha
 check(prev==meta['head'],'head')
 return st,rows,meta

def casulo():
 p=next(x for x in (ROOT/'runs').glob('R153_CASULO_CA_SOURCE_*.sqlite') if '.checkpoint.' not in x.name)
 st,rows,meta=load(p);check(len(rows)==9,'casulo txn9')
 events=[x for _,r,_ in rows for x in r['detail']['native_actions']]
 check([r['kind'] for _,r,_ in rows]==['START','COCOON','END','START','STRIKE','END','START','PASS','END'],'order')
 buff=next(x for x in events if x['action']=='CASULO_BROTOS')
 check(buff['PA_spent']==60 and buff['ca_before']=='76' and buff['ca_after']=='98' and buff['movement_delta_m']==-4,'Casulo source')
 attack=next(x for x in events if x['action']=='weapon_attack')
 row=next(r for _,r,_ in rows if r['kind']=='STRIKE');t=row['payload']['tape'];seed=st['seed'];score=sum(dice(seed,1,'R151-F-NORMAL-HIT-0',4,6))+92
 check(t['score']==score and attack['roll_score']==score and 76<score<=98,'Casulo opposed roll')
 check(attack['hit']==False and attack['after_hp']==630 and attack['before_hp']==630 and attack['ca_exact']=='98','Casulo protects target')
 with sqlite3.connect(p) as c:final=json.loads(dict(c.execute('select key,value from meta'))['state'])
 check(final['casulos']['E1/E2']['active'] and final['actors']['E2']['resource']['ca']==98,'Casulo persistent')
 check(final['actors']['E1']['resource']['pa']==744,'Casulo PA')
 return {'run':p.stem,'verified':'SOURCE_EVENT_AND_RNG_PASS','commits':9,'attack_score':score,'protected_CA':98,
  'unprotected_CA':76,'damage_prevented_by_defense_comparison':True,'source_expiration':'HOLD','movement_absolute_speed':'HOLD'}

def aoo(path):
 st,rows,meta=load(path);seed=st['seed'];full=st['actors']['F2']['resource']['hp']==479
 check(len(rows)==(4 if full else 2),'AOOs exact commits');check(rows[0][1]['kind']=='START' and rows[1][1]['kind']=='AOO_CHAIN','events')
 ao=rows[1][1];p=ao['payload'];ev=ao['detail']['native_actions'];n=[x for x in ev if x['action']=='weapon_attack']
 check(p['order']==['A','F1'] and p['path_distance_m']==1.5 and p['voluntary'] is True,'R43 order and source path')
 check(len(n)==(2 if full else 1),'number of consecutive AoO')
 hp=st['actors']['F2']['resource']['hp'];ca=st['actors']['F2']['resource']['ca']
 for i,(a,event) in enumerate(zip(['A','F1'],n)):
  pr=st['actors'][a]['source_profile'];nonce=1
  h=[dice(seed,nonce,f'R154-{a}-AOO-HIT-{j}',pr['attack_dice'],6) for j in range(2)]
  score=max(map(sum,h))+pr['attack_flat']+2
  cr=[dice(seed,nonce,f'R154-{a}-AOO-CRIT-{j}',1,6)[0] for j in range(3)]
  die=[dice(seed,nonce,f'R154-{a}-AOO-DMG-{j}',N,F) for j,(N,F) in enumerate(pr['damage_dice'])]
  base=sum(map(sum,die))+pr['damage_flat'];pos=cr[:2]==[6,6] and cr[2]>=5;neg=cr[:2]==[1,1] and cr[2]<=2
  hit=(score>ca or pos) and not neg;raw=base+sum(N*F for N,F in pr['damage_dice']) if hit and pos else base if hit else 0
  net=max(0,raw-22) if hit else 0;eff=min(hp,net)
  check(event['from']==a and event['to']=='F2' and event['attack_origin']=='OPPORTUNITY' and event['roll_score']==score,'attack source')
  check(event['critical']==('NEGATIVE' if neg else 'POSITIVE' if pos else 'NONE'),'R42 critical')
  check(event['raw']==raw and event['net']==net and event['before_hp']==hp and event['after_hp']==hp-eff,'damage/HP')
  hp-=eff
 check([x['from'] for x in n]==(['A','F1'] if full else ['A']),'actual action priority')
 if full:
  move=next(x for x in ev if x['action']=='move');check(move['from']=='CENTER' and move['to']=='OUT','move after AoO')
 else:
  check(hp==0 and all(x['action']!='move' for x in ev),'KO no movement')
  skip=ao['detail']['skip_reason'];check(len(skip)==1 and skip[0]['reaction_preserved']==1,'KO preserves second reaction')
 with sqlite3.connect(path) as c:final=json.loads(dict(c.execute('select key,value from meta'))['state'])
 check(final['actors']['F2']['resource']['hp']==hp,'terminal target HP')
 check(final['actors']['F1']['resource']['reaction']==(0 if full else 1),'slot single use')
 return {'run':path.stem,'verified':'SOURCE_R43_CAUSAL_RNG_PASS','commits':len(rows),'ordered_AOO':len(n),'target_HP':hp,
 'moved':full,'second_reaction_consumed':full}

if __name__=='__main__':
 out={'casulo':casulo(),'concurrent_aoo':[aoo(p) for p in sorted((ROOT/'runs').glob('R154_TWO_AOO_*.sqlite')) if '.checkpoint.' not in p.name]}
 (ROOT/'R159_COLD_CASULO_AOO_AUDIT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(out,ensure_ascii=False,indent=2))
