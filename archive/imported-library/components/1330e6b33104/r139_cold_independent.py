"""Cold independent auditor: NO import of vlab_effects/vlab_r18/r126/r138.
Reconstructs EVERY state hash, physical PA/HP, attack and healing dice, statuses,
source-specific action constraints, scheduler order and expiration from genesis + SQLite.
"""
import json,hashlib,sqlite3,random,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parent
VERSION='VLAB-R18-INTERACTIVE-CLI-0.1-EXPERIMENTAL'
def can(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def sha(x):return hashlib.sha256(can(x).encode()).hexdigest()
def dice(seed,n,who,kind,count,faces):
 h=hashlib.sha256(f'{seed}|{n}|R138-{who}-{kind}|{count}d{faces}|{VERSION}'.encode()).digest()
 rng=random.Random(int.from_bytes(h,'big'))
 return [rng.randint(1,faces) for _ in range(count)]
def check(cond,message):
 if not cond:raise AssertionError(message)

def attack(st,tape,origin,record,reaction='NONE'):
 a=tape['actor'];target=tape['target'];pa=st['actors'][a]['source_profile'];tar=st['actors'][target]['source_profile']
 ra=st['actors'][a]['resource'];rt=st['actors'][target]['resource'];nonce=st['action_nonce'][a]+1
 check(tape['nonce']==nonce and a=='A' and target=='F1','attack identity')
 adv=1 if origin=='OPPORTUNITY' else 0;dis=1 if reaction=='CAPA' else 0
 weak=10*ra['hp']<pa['hp'];net=max(-4,min(4,adv-dis-int(weak)))
 hit_rolls=[dice(st['seed'],nonce,a,origin.replace('OPPORTUNITY','AOO')+'-HIT-'+str(i),pa['attack_dice'],6)
             for i in range(1+abs(net))]
 score=(max(map(sum,hit_rolls))+2*net if net>0 else min(map(sum,hit_rolls))+2*net if net<0 else sum(hit_rolls[0]))+pa['attack_flat']
 crit=[dice(st['seed'],nonce,a,origin.replace('OPPORTUNITY','AOO')+'-CRIT-'+str(i),1,6)[0] for i in range(3)]
 damage_rolls=[dice(st['seed'],nonce,a,origin.replace('OPPORTUNITY','AOO')+'-DMG-'+str(i),n,f)
               for i,(n,f) in enumerate(pa['damage_dice'])]
 # R138 `kind` in RNG is 'NORMAL' for standard and 'AOO' for opportunity.
 check(tape['hit_rolls']==hit_rolls and tape['crit']==crit and tape['dmg_rolls']==damage_rolls,'attack dice stream')
 check(score==tape['score'],'hit score')
 if crit[:2]==[1,1] and crit[2]<=2:raise AssertionError('unhandled critical failure')
 normal=sum(map(sum,damage_rolls))+pa['damage_flat'];check(tape['normal_damage']==normal,'normal damage')
 critical=crit[:2]==[6,6] and crit[2]>=5
 critical_extra=sum(n*f for n,f in pa['damage_dice']) if critical else 0
 hit=score>rt['ca'] or critical
 raw=normal+critical_extra if hit else 0;rd=tar['rd'];net_damage=max(0,raw-rd) if hit else 0
 before=rt['hp'];actual=min(before,net_damage);after=before-actual
 check(record['action']=='weapon_attack' and record['from']==a and record['to']==target,'native attack identity')
 for k,v in [('roll_score',score),('hit',hit),('critical','POSITIVE' if critical else 'NONE'),
  ('critical_max_bonus',critical_extra),('raw',raw),('rd_applied',rd if hit else 0),
  ('net',net_damage),('hp_loss_actual',actual),('overkill',max(0,net_damage-before)),
  ('before_hp',before),('after_hp',after),('attack_origin',origin),
  ('advantage_levels',adv),('disadvantage_levels',dis)]:
  check(record[k]==v,f'native attack {k} mismatch: {record[k]} != {v}')
 check(record['critical_sequence']==crit,'sequential critical roll')
 check(record['weak_attacker']==weak,'weak status')
 check(record['net_levels']==net,'adv/disadv causal')
 rt['hp']=after
 if origin=='NORMAL':check(ra['standard']==1,'standard unavailable');ra['standard']=0
 else:check(ra['reaction']==1,'reaction slot unavailable');ra['reaction']=0
 st['action_nonce'][a]+=1
 return actual

def cold(db,capture_at=None):
 path=Path(db);st=json.loads(path.with_suffix('.genesis.json').read_text())
 with sqlite3.connect(path) as con:
  meta=dict(con.execute('select key,value from meta'))
  rows=[json.loads(r[0]) for r in con.execute('select row_json from events order by seq')]
  pending=con.execute('select count(*) from pending').fetchone()[0]
 check(pending==0,'UNKNOWN_EFFECT pending')
 check(meta['mode']=='EXPERIMENTAL_LAB_ONLY','mode')
 check(len(rows)==int(meta['revision']) and len(rows)>=32,'event count')
 head=meta['genesis'];captured=None;metrics={'commits':0,'native_events':0,'normal_attacks':0,'opportunity_attacks':0,
  'heals':0,'reactive_heals':0,'PA_total':0,'healing_effective':0,'damage_effective':0,
  'start_count':{},'passo_expirations':0,'mark_boundary_holds':0,'reactions_paid':0}
 for i,row in enumerate(rows,1):
  check(row['seq']==i and row['prev']==head and row['before_sha']==sha(st),'pre-event chain')
  check(row['synthetic'] is True and row['official_effects']==0,'official status')
  k=row['kind'];p=row['payload'];events=row['detail']['native_actions'];a=st['active'];extra=row['detail'].get('extra') or {}
  metrics['native_events']+=len(events)
  if k=='INIT':
   check(st['phase']=='INIT' and p=={'seed':st['seed']} and len(events)==0,'init event')
   rr=[]
   for who in ('A','F1','E'):
    pr=st['actors'][who]['source_profile'];roll=dice(st['seed'],0,who,'INIT',pr['init_dice'],6)
    rr.append({'id':who,'dice':roll,'des':pr['dex'],'total':sum(roll)+pr['init_bonus'],'source':pr['source']})
   check(extra['initiative_rows']==rr,'initiative dice')
   check(len({r['total'] for r in rr})==3,'unexpected tie in this admitted scenario')
   ordered=[r['id'] for r in sorted(rr,key=lambda x:(x['total'],x['des']),reverse=True)]
   check(extra['tie']['order']==ordered,'initiative ordering')
   st['order']=ordered;st['active']=ordered[0];st['phase']='ACTIVE';st['round']=1
  elif k=='START':
   check(p=={'actor':a} and len(events)==1 and events[0]['action']=='turn_start','start mismatch')
   r=st['actors'][a]['resource'];check(r['hp']>0 and r['standard']==0,'start illegal')
   r['standard']=r['movement']=r['reaction']=1;st['actor_turns'][a]+=1
   metrics['start_count'][a]=metrics['start_count'].get(a,0)+1
   if a=='F1' and st['marks']:
    mark=st['marks']['F1'];mark['own_turn_started_since_cast']+=1
    if mark['own_turn_started_since_cast']>=3:mark['expiry_boundary']='HOLD_EXACT_3_TURNS'
  elif k=='FOREGO':
   check(events[0]['action']=='FOREGO_STANDARD' and events[0]['by']==a and p=={'actor':a},'forego identity')
   check(st['actors'][a]['resource']['standard']==1,'forego needs standard')
   st['actors'][a]['resource']['standard']=0
  elif k=='ATTACK':
   check(len(events)==(2 if p['reaction']=='CAPA' else 1),'attack reaction event count')
   if p['reaction']=='CAPA':
    rr=st['actors']['F1']['resource'];check(a=='A' and rr['reaction']==1 and rr['pa']>=35,'Capa gate')
    check(events[0]['action']=='CAPA_POEIRA' and events[0]['PA_spent']==35 and events[0]['attack_score']==p['attack']['score'],'Capa sourced')
    rr['reaction']=0;rr['pa']-=35;metrics['PA_total']+=35;metrics['reactions_paid']+=1
   metrics['damage_effective']+=attack(st,p['attack'],'NORMAL',events[-1],p['reaction'])
   metrics['normal_attacks']+=1
  elif k=='MARCA':
   check(a=='F1' and st['marks']=={} and events[0]['action']=='MARCA_PASSOS_PERDIDOS','mark')
   check(p=={'target':'A','distance_m':1.5,'line_of_sight':True},'Marca 30m and visible')
   r=st['actors'][a]['resource'];check(r['standard']==1 and r['pa']>=25,'Marca economy')
   r['standard']=0;r['pa']-=25;metrics['PA_total']+=25
   check(events[0]['attack_bonus_granted']==0 and events[0]['duration_own_turns']==3,'Marca not attack bonus')
   st['marks']['F1']={'target':'A','duration_literal':'3 TURNOS','activation_round':st['round'],
    'own_turn_started_since_cast':0,'source':st['actors'][a]['source'],
    'bonus':'PERCEPTION_SURVIVAL_ONLY_10','expiry_boundary':'HOLD_NO_UNIVERSAL_TURN_RULE',
    'no_attack_bonus':True}
  elif k=='PASSO':
   check(a=='F1' and events[0]['action']=='PASSO_FULIGEM' and p=={'actor':'F1','intent':'THIS_TURN_ONLY'},'Passo')
   r=st['actors'][a]['resource'];check(r['movement']==1 and r['pa']>=25,'Passo resource')
   check(events[0]['speed_bonus_m']==12 and events[0]['duration']=='ESTE_TURNO','Passo sourced')
   r['movement']=0;r['pa']-=25;metrics['PA_total']+=25
   st['temporary']['F1']={'source':st['actors'][a]['source'],'kind':'PASSO_FULIGEM',
    'bonus_speed_m':12,'expires_at':'END_CURRENT_F1_TURN',
    'activated_own_turn':st['actor_turns']['F1']}
  elif k=='HEAL':
   check(a=='E' and len(events)==1 and events[0]['action']=='RECONSTITUICAO_SEIVA','heal type')
   rr=st['actors']['E']['resource'];tar=st['actors']['F1']['resource']
   check(rr['standard']==1 and rr['pa']>=75 and 0<tar['hp']<tar['maximum_hp'],'heal resources')
   check(p['target']=='F1' and p['distance_m']<=5,'heal range')
   n=st['ability_nonce']['E_HEAL']+1;die=dice(st['seed'],n,'E','HEAL',8,10)
   check(p['dice']==die,'heal RNG')
   gross=sum(die)+25+20;actual=min(gross,tar['maximum_hp']-tar['hp'])
   rec=events[0]
   for key,val in [('healing_rolls',die),('base_heal',sum(die)+25),('equipped_gloves_bonus',20),
    ('gross_heal',gross),('actual_healed',actual),('hp_before',tar['hp']),('hp_after',tar['hp']+actual),
    ('PA_spent',75),('excess_heal',gross-actual),('bleeding_removed',False)]:
    check(rec[key]==val,f'heal {key}')
   tar['hp']+=actual;rr['pa']-=75;rr['standard']=0;st['ability_nonce']['E_HEAL']+=1
   metrics['heals']+=1;metrics['PA_total']+=75;metrics['healing_effective']+=actual
  elif k=='MOVE_F_AOO_PULSO':
   check(a=='F1' and len(events)==3,'multi reaction event sequence')
   check([e['action'] for e in events]==['weapon_attack','PULSO_ESTABILIZACAO','move'],'causal ordering')
   check(p['forced'] is False and p['path']==['B1','B2'] and p['pulse_distance_m']==2,'topology')
   check(st['actors']['F1']['resource']['position']=='B1' and st['actors']['A']['resource']['position']=='B0','adjacent pre')
   metrics['damage_effective']+=attack(st,p['attack'],'OPPORTUNITY',events[0]);metrics['opportunity_attacks']+=1
   pulse=events[1];rr=st['actors']['E']['resource'];tar=st['actors']['F1']['resource']
   check(rr['reaction']==1 and rr['pa']>=45 and tar['hp']>0,'postdamage Pulso preconditions')
   n=st['ability_nonce']['E_PULSO']+1;die=dice(st['seed'],n,'E','PULSO',3,10)
   check(p['pulse_dice']==die,'pulso dice')
   gross=sum(die)+10+20;actual=min(gross,tar['maximum_hp']-tar['hp'])
   for key,val in [('healing_rolls',die),('source_base',sum(die)+10),('gloves_bonus',20),
    ('gross_heal',gross),('actual_heal',actual),('before_hp',tar['hp']),('after_hp',tar['hp']+actual),
    ('PA_spent',45),('reaction_consumed',1),('target_resurrected',False)]:
    check(pulse[key]==val,f'pulso {key}')
   rr['reaction']=0;rr['pa']-=45;tar['hp']+=actual;st['ability_nonce']['E_PULSO']+=1
   metrics['PA_total']+=45;metrics['healing_effective']+=actual;metrics['reactive_heals']+=1;metrics['reactions_paid']+=1
   move=events[2];check(move['by']=='F1' and move['from']=='B1' and move['to']=='B2','move after reaction')
   check(tar['movement']==1,'move slot');tar['movement']=0;tar['position']='B2'
  elif k=='MOVE_A':
   check(a=='A' and len(events)==1 and events[0]['action']=='move','A move')
   check(p=={'from':'B0','to':'B1','path':['B0','B1']},'A path')
   r=st['actors'][a]['resource'];check(r['movement']==1 and r['position']=='B0','A move slot')
   r['movement']=0;r['position']='B1'
  elif k=='END':
   check(events[0]['action']=='turn_end' and p=={'actor':a},'end')
   check(st['actors'][a]['resource']['standard']==0,'end standard')
   if a in st['temporary']:
    check(len(events)==2 and events[1]['action']=='EXPIRE_TURN_EFFECT','expiration missing')
    check(events[1]['bonus_speed_removed_m']==12,'expiry scope')
    st['temporary'].pop(a);metrics['passo_expirations']+=1
   else:check(len(events)==1,'unexpected end events')
   j=st['order'].index(a);st['turn_index']+=1
   for off in range(1,len(st['order'])+1):
    k0=(j+off)%len(st['order']);who=st['order'][k0]
    if st['actors'][who]['resource']['hp']>0:
     st['active']=who
     if k0<=j:st['round']+=1
     break
   else:st['phase']='CENSORED_NO_LIVING';st['active']=None
   if st['round']>st['pre_registered_horizon']:
    st['phase']='CENSORED_HORIZON';st['active']=None;st['winner']=None
  else:raise AssertionError('UNKNOWN event '+k)
  check(row['after_sha']==sha(st),f'after state hash failed @ {i} {k}')
  if i==capture_at:captured=copy.deepcopy(st)
  head=sha(row);metrics['commits']+=1
 check(head==meta['head'] and sha(st)==sha(json.loads(meta['state'])),'final hash/head')
 check(st['phase']=='CENSORED_HORIZON' and st['winner'] is None,'censored no false victory')
 check(st['temporary']=={},'no transient Passo remains')
 check(st['marks']['F1']['expiry_boundary']=='HOLD_EXACT_3_TURNS','Marca boundary fail-closed')
 metrics['mark_boundary_holds']=1
 return {'run_id':st['run_id'],'seed':st['seed'],'metrics':metrics,'head':head,
 'state_sha256':sha(st),'phase':st['phase'],
 'end_hp':{k:x['resource']['hp'] for k,x in st['actors'].items()},
 'end_pa':{k:x['resource']['pa'] for k,x in st['actors'].items()},
 'independent_auditor_imports_engine':False,'terminal_certificates':0,
 'accepted_scope':'4-ROUND_SOURCE_CONDITIONAL_CENSORED_INTEGRATION_ONLY',
 'Marca_expiration':'HOLD_NOT_CERTIFIED', 'captured_prefix_state':captured if capture_at else None}
if __name__=='__main__':
 file=ROOT/'runs'/'R138_MULTI_SOURCE_FERYN_ERISTAN_DEV_S991402.sqlite'
 result=cold(file)
 (ROOT/'R139_INDEPENDENT_COLD_AUDIT.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(result,indent=2,ensure_ascii=False))
