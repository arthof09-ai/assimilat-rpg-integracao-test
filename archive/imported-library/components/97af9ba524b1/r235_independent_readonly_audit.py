"""R235 independent source/math auditor for native R18, no runner or engine imports."""
import sqlite3,json,hashlib,random,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def check(test,msg):
 if not test:raise AssertionError(msg)
def can(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def sha(x):return hashlib.sha256(can(x).encode()).hexdigest()
def roll_r234(seed,who,own,tag,n,f):
 v=int.from_bytes(hashlib.sha256(f'R234|{seed}|{who}|OWN{own}|{tag}|{n}d{f}'.encode()).digest(),'big');r=random.Random(v);return [r.randint(1,f) for _ in range(n)]
def roll_r235(seed,who,own,tag,n,f):
 v=int.from_bytes(hashlib.sha256(f'R235|{seed}|{who}|{own}|{tag}|{n}d{f}'.encode()).digest(),'big');r=random.Random(v);return [r.randint(1,f) for _ in range(n)]
def get(path):
 c=sqlite3.connect(f'file:{path}?mode=ro&immutable=1',uri=True)
 try:
  m=dict(c.execute('select key,value from meta'));st=json.loads(m['state']);rows=[]
  for seq,cmd,prev,text,h,before,after in c.execute('select seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha from events order by seq'):
   x=json.loads(text);check(sha(x)==h and x['seq']==seq and x['cmd_id']==cmd and x['prev']==prev and x['before_sha']==before and x['after_sha']==after,'SQL_ROW_SHA')
   rows.append((x,h))
  pending=c.execute('select count(*) from pending').fetchone()[0]
  return m,st,rows,pending
 finally:c.close()
def audit(root=ROOT,write=True):
 root=Path(root)
 pb=(root/'sources/R235_PREREG_BEFORE_COMMIT.json').read_bytes();p=json.loads(pb);ph=hashlib.sha256(pb).hexdigest()
 sb=(root/'sources/R235_GRIFFON_SPELL_SOURCE_EXCERPT.json').read_bytes();s=json.loads(sb);sh=hashlib.sha256(sb).hexdigest()
 bb=(root/'sources/R234_BEAST_FROZEN_EXCERPTS.json').read_bytes();b=json.loads(bb);bh=hashlib.sha256(bb).hexdigest();be=b['beasts']
 check(p['seeds']==[23571001,23571002,23571003,23571004] and p['save_focus_seeds']==[23578001,23578002,23578003,23578004],'PREFROZEN_FIXED')
 check(p['horizon_rounds']==6 and len(p['arms'])==4 and p['actors']==['G','C'] and s['cost_pa']==55 and s['save_cd']==94 and s['damage']=='14d10','SOURCE_MAGIC_COST_DC')
 check(b['source_status']=='PRECREATE_VZ_MASTER_SIDE_NON_P4' and s['parent_status']=='PRECREATE_VZ_NON_P4','NO_CANON_PROMOTION')
 dbs=list((root/'evidence/db').glob('*.sqlite'));check(len(dbs)==20,'TWENTY_REGISTERED_SQLITE')
 totals={'valid_battles':0,'focused_single_casts':0,'commits':0,'events':0,'physical_attacks':0,'hit':0,'spells':0,'saves':0,'odd_halves':0,'move':0,'PA_spent':0,'effective_spell_hp_loss':0,'physical_hp_loss':0}
 results=[];streams={};derived_events=[]
 for seed in p['seeds']+p['save_focus_seeds']:
  arms=p['arms'] if seed in p['seeds'] else ['SAVE_FOCUS']
  for arm in arms:
   file=root/'evidence/db'/f'R235_{arm}_S{seed}.sqlite';check(file.exists(),'EXPECTED_DB_MISSING')
   m,st,rows,pending=get(file);focus=arm=='SAVE_FOCUS';order=['G','R'] if focus else ['G','C']
   check(pending==0 and len(rows)==int(m['revision'])==(1 if focus else 12),'R18_FULL_COMMIT_CHAIN')
   check(st['synthetic'] is True and st['winner'] is None and st['phase']==('CENSORED_ONE_SPELL' if focus else 'CENSORED_HORIZON'),'CENSOR_NO_WINNER')
   rr=st['r235'];check(rr['source_sha']==sh and rr['beast_source_sha']==bh and rr['prereg_sha']==ph and rr['source_status']=='VZ_PRECREATE_NONP4','SOURCE_HASH_AND_LABEL')
   rd=0 if arm.endswith('_RD0_TEST') else 75;check(rr['rd_target']==rd,'COUNTERFACTUAL_RD_EXPLICIT')
   hp={a:be[a]['hp'] for a in order};pa={a:be[a]['pa'] for a in order};pos={a:'(0,0)' if a=='G' else '(14,0)' if a=='C' else '(1,0)' for a in order}
   moves=0;attacks=0;hits=0;spells=0;saves=0;odd=0;paid=0;physloss=0;spellloss=0;allevents=[];prev=m['genesis'];last_after=None
   for idx,(row,digest) in enumerate(rows):
    check(row['prev']==prev and (last_after is None or row['before_sha']==last_after),'R18_PRIOR_AND_CHAIN')
    prev=digest;last_after=row['after_sha'];totals['commits']+=1
    who='G' if focus else order[idx%2];own=1 if focus else idx//2+1
    if not focus:check(row['payload']=={'prereg_sha':ph,'spell_sha':sh,'seed':seed,'arm':arm,'who':who,'turn':idx+1},'ACTION_PAYLOAD_PREREG')
    native_full=(st['native_events'] if focus else None)
    events=row['detail']['events_new'];
    # Save-focus runner includes turn_start in state but excludes it from R18 detail.
    ev=(st['native_events'] if focus else events)
    actions=[e['action'] for e in ev]
    spell_action=who=='G' and (focus or (arm.startswith('MIXED') and own%2==0))
    expected=['turn_start']+(['move'] if own==1 and not focus else [])+(['R235_FROZEN_MAGIC_TAPE','spell'] if spell_action else ['R235_PER_ACTOR_PHYSICAL_TAPE','weapon_attack'])+['turn_end']
    check(actions==expected,'SOURCE_ACTION_ORDER_NO_EXTRA_ACTION')
    if focus:check(events==ev[1:],'FOCUS_INTENT_DETAIL_SET')
    tape=ev[-3];act=ev[-2];check(ev[0]['by']==who and ev[-1]['by']==who,'ACTOR_OWNS_TURN')
    check(ev[0]['speed']==str(be[who]['speed']) and ev[0]['weak'] is False,'SOURCE_SPEED')
    if own==1 and not focus:
     mov=ev[1];exdest='(12.5,0)' if who=='G' else '(14,1)';excost='25/2' if who=='G' else '1'
     check(mov['action']=='move' and mov['by']==who and mov['from']==pos[who] and mov['to']==exdest and mov['travel_cost']==excost and mov['speed']==str(be[who]['speed']),'MOVE_SOURCE_BOUND')
     pos[who]=exdest;moves+=1
    target='R' if focus else 'C' if who=='G' else 'G'
    check(tape.get('target')==target,'TARGET_POLICY')
    if spell_action:
     check(tape['action']=='R235_FROZEN_MAGIC_TAPE' and act['action']=='spell','SPELL_NO_EXTRA_ATTACK')
     droll=roll_r235(seed,'G',own,'LIGHTNING_DAMAGE',14,10);save_roll=roll_r235(seed,target,own,'REFLEX_SAVE',6,6)
     check(tape['damage_dice']==droll and tape['save_dice']==save_roll and tape['source_sha']==sh and tape['cost_pa']==55,'RNG_SPELL_SOURCE_PA')
     score=sum(save_roll)+be[target]['stats']['DES'];success=score>94;gross=sum(droll);after_save=gross//2 if success else gross
     eff=max(0,after_save-rd);loss=min(eff,hp[target])
     check(tape['save_score']==score and tape['source_cd']==94 and tape['save_success']==success,'SOURCE_REFLEX_GATE')
     check(act['source_rule']=='R235-GRIFFON-SHORT-LINE-CD94' and act['damage_type']=='raio' and act['damage_faces']==10 and act['damage_rolls']==droll and act['save_effect']=='SAVE-HALF','SPELL_SOURCE_RNG')
     check(act['save_exceeds_cd']==success and act['r223_damage_before_half']==gross and act['raw']==after_save,'MASTER_FLOOR_AFTER_SAVE')
     check(act['rd_applied']==rd and act['effective']==eff and act['hp_before']==hp[target] and act['hp_after']==hp[target]-loss,'RD_AFTER_FLOOR_AND_HP')
     check(act['PA_spent']==55 and act['critical']=='NOT-APPLICABLE-BY-SISTEMA-DE-MAGIA','NO_SPELL_CRIT_EXTRA_COST')
     if success and gross%2:check(act['r223_odd_half_policy']=='FLOOR_MASTER_CONFIRMED_TEST' and act['r225_rounding_authority']=='MASTER_EXPRESS_CONFIRMATION_CANONIZATION_PENDING','CONFIRMED_HALF_POLICY')
     hp[target]-=loss;pa[who]-=55;spells+=1;saves+=int(success);odd+=int(success and gross%2);paid+=55;spellloss+=loss
    else:
     z=be[who];a=roll_r234(seed,who,own,'ATTACK',6,6);dr=roll_r234(seed,who,own,'DAMAGE',20,10);cr=roll_r234(seed,who,own,'CRITICAL',3,6)
     check(tape['action']=='R235_PER_ACTOR_PHYSICAL_TAPE' and act['action']=='weapon_attack' and tape['dice_attack']==a and tape['dice_damage']==dr and tape['critical']==cr,'PHYSICAL_SOURCE_RNG')
     score=sum(a)+z['attack_bonus'];positive=cr[:2]==[6,6] and cr[2]>=5;negative=cr[:2]==[1,1] and cr[2]<=2;hit=(score>be[target]['ca'] or positive) and not negative
     raw=(sum(dr)+(200 if positive else 0)) if hit else 0
     chosenrd=rd if target=='C' else 75
     net=max(0,raw-chosenrd);loss=min(net,hp[target]);attacks+=1;hits+=int(hit);physloss+=loss
     check(act['roll_score']==score and act['critical']==('POSITIVE' if positive else 'NEGATIVE' if negative else 'NONE') and act['hit']==hit and act['raw']==raw,'BASIC_ATTACK_CRITICAL')
     check(act['normal_damage']==sum(dr) and act['rd_applied']==(min(raw,chosenrd) if hit else 0) and act['net']==net and act['hp_loss_actual']==loss,'BASIC_RD_HP')
     check(act['after_hp']==hp[target]-loss and act['before_hp']==hp[target],'HP_DAMAGE_CONSERVATION')
     hp[target]-=loss
     streams.setdefault((seed,who,own),{})[arm]=(a,dr,cr)
    if not focus:
     allevents.extend(events)
     check([e['seq'] for e in events]==list(range(len(allevents)-len(events)+1,len(allevents)+1)),'EVENT_SEQ')
    check(row['official_effects']==0 and row['synthetic'] is True,'NO_CANON_EFFECT')
   check(m['head']==prev and row['after_sha']==sha(st),'R18_FINAL_HEAD_AFTER')
   if not focus:check(st['native_events']==allevents,'FULL_TRACE_REPRODUCIBLE')
   check({k:v['hp'] for k,v in st['actors'].items()}==hp and {k:v['pa'] for k,v in st['actors'].items()}==pa,'FINAL_HP_PA_RECON')
   stats=rr['stats'];check(stats['attacks']==attacks and stats['hits']==hits and stats['spells']==spells and stats['save_success']==saves and stats['odd_saved']==odd and stats['pa_spent']==paid and stats['movements']==moves and stats['physical_hp_loss']==physloss and stats['spell_hp_loss']==spellloss,'STATS_DENOM')
   check(rr['outcome']['official_cells']==0,'OFFICIAL_BATTERIES_ZERO')
   if focus:totals['focused_single_casts']+=1
   else:totals['valid_battles']+=1
   totals['physical_attacks']+=attacks;totals['hit']+=hits;totals['spells']+=spells;totals['saves']+=saves;totals['odd_halves']+=odd;totals['move']+=moves;totals['PA_spent']+=paid;totals['physical_hp_loss']+=physloss;totals['effective_spell_hp_loss']+=spellloss;totals['events']+=len(st['native_events'])
   results.append({'seed':seed,'arm':arm,'hpC':hp.get('C'),'hpG':hp['G'],'hpR':hp.get('R'),'PA_G':pa['G'],'spell_hp_loss':spellloss,'physical_hp_loss':physloss,'saves':saves,'odd_halves':odd})
 # Corresponding source RNG identical across all four arms, irrespective of RD or Grifo's substitution of spell.
 for seed in p['seeds']:
  for own in range(1,7):
   croc=streams[(seed,'C',own)];check(set(croc)==set(p['arms']) and len(set(tuple(map(tuple,v)) for v in croc.values()))==1,'CROC_SHARED_RNG_4_ARMS')
   if own%2:
    grif=streams[(seed,'G',own)];check(set(grif)==set(p['arms']) and len(set(tuple(map(tuple,v)) for v in grif.values()))==1,'G_SHARED_RNG_COMMON_ACTIONS')
   else:
    grif=streams[(seed,'G',own)];check(set(grif)=={'PHYSICAL_SOURCE_RD75','PHYSICAL_RD0_TEST'} and len(set(tuple(map(tuple,v)) for v in grif.values()))==1,'G_PHYS_ODD_SHOULD_DIVERGE_ACTIONS')
 out={'status':'PASS_R235_FACTORIAL_SOURCE_GRIFFON_SPELL_NATIVE_CONDITIONAL','counts':totals,'seed_clusters':4,'counterfactual_RD0_is_not_canon':True,'named_beasts_source':'VZ-PRECREATE-ONLY','official_battery_cells':0,'historical_replays':0,'outcomes':results}
 if write:(root/'evidence/reports/R235_INDEPENDENT_SQL_AUDIT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(out,ensure_ascii=False,indent=2));return out
if __name__=='__main__':audit()
