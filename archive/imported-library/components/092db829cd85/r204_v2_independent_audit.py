"""Read-only code-separated R204 ledger & semantic audit.
No import from the combat producer, R18 runner, or v0.8.1 damage adapter.
Expected RNG, HP, PA, moves, phases independently recomputed from stored prereg.
"""
from __future__ import annotations
import json,hashlib,pathlib,sqlite3,random,re,collections
from fractions import Fraction
ROOT=pathlib.Path(__file__).resolve().parents[1]
PREPATH=ROOT/'source/R204_V2_MAGIC_PREREG.json'
PRE=json.loads(PREPATH.read_text());PRE_SHA=hashlib.sha256(PREPATH.read_bytes()).hexdigest()
V='R204V2-SOURCE-EXPLICIT-4D6-ATTACK-NO-MAGIC-CRIT-1'
VER198='R198-R18-SOURCE-SCOPED-MICROBENCH-1'
PAIR=['ONG_P2','LOBO_P1']

def check(test,error):
 if not test:raise AssertionError(error)
def canon(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def sha(x):return hashlib.sha256(canon(x).encode()).hexdigest()
def magic_roll(seed,turn):
 def roll(label,n):
  tape=f'{V}|{seed}|ONG_P2-LOBO_P1|ONG_P2|{turn}|{label}'
  rng=random.Random(int.from_bytes(hashlib.sha256(tape.encode()).digest(),'big'))
  return [rng.randint(1,6)for _ in range(n)]
 return {'hit':roll('4d6-ATTACK-SOURCE-EXPLICIT',4),'damage':roll('8d6-DAMAGE-SOURCE-EXPLICIT',8)}
def base_dice(seed,who,turn,label,n,faces):
 e=f'{VER198}|{seed}|ONG_P2-LOBO_P1|{who}|{turn}|{label}|{n}d{faces}'
 r=random.Random(int.from_bytes(hashlib.sha256(e.encode()).digest(),'big'))
 return [r.randint(1,faces)for _ in range(n)]
def audit(path):
 path=pathlib.Path(path)
 m=re.fullmatch(r'R204V2_ONG_LOBO_S(\d+)_DIST(9|9p5)_(CAST_WHEN_IN_RANGE|NEVER_CAST_CONTROL)\.sqlite',path.name)
 check(m,'BAD_RUN_NAME')
 seed=int(m.group(1));dist=Fraction(m.group(2).replace('p','.'));policy=m.group(3)
 check(seed in PRE['seeds'] and dist in [Fraction(x) for x in PRE['positions_m']] and policy in PRE['policies'],'NOT_PREREGISTERED')
 c=sqlite3.connect(f'file:{path.as_posix()}?mode=ro',uri=True)
 try:
  meta=dict(c.execute('SELECT key,value FROM meta'))
  dbrows=list(c.execute('SELECT seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha FROM events ORDER BY seq'));rows=[json.loads(x[3]) for x in dbrows]
  pending=c.execute('SELECT count(*) FROM pending').fetchone()[0]
 finally:c.close()
 check(pending==0,'PENDING_UNKNOWN_EFFECT')
 st=json.loads(meta['state']);check(st['r204_pre_sha']==PRE_SHA and st['r204_version']==V and st['r204_policy']==policy,'STATE_PRE_REG_DRIFT')
 check(st['seed']==seed and st['pair']==PAIR and Fraction(st['geo']['initial_m'])==dist,'STATE_ACTOR_POS_DRIFT')
 check(st['position']=={'contact':True,'same_layer':True,'line_of_effect':True,'movement':False,'campaign_location':False},'UNEXPECTED_R198_POSITION_BRIDGE')
 check(st['scope']=='LAB_R204_CAUSAL_DISTANCE_CAST_WITH_SOURCE_ACTOR_AND_NATIVE_RD','BAD_LAB_SCOPE')
 check(len(rows)==int(meta['revision']) and len(rows)>2,'MISSING_COMMIT')
 head=meta['genesis'];lastafter=None;hp={'ONG_P2':99,'LOBO_P1':240};pa={'ONG_P2':91,'LOBO_P1':180}
 initiative={x:sum(base_dice(seed,x,0,'INIT',2,6))+(15 if x=='ONG_P2' else 20)for x in PAIR}
 check(initiative['ONG_P2']!=initiative['LOBO_P1'],'INIT_TIE_SHOULD_HAVE_BEEN_HELD')
 order=sorted(PAIR,key=lambda x:initiative[x],reverse=True);active=order[0]
 turns=collections.Counter();magic_count=0;magic_hp=0;magic_pa=0;declines=collections.Counter();move_count=0;attack_count=0
 native=[];prev=None;geo=dist;roundno=1
 for i,row in enumerate(rows,1):
  check(row['seq']==i and row['prev']==head and row['cmd_id'].startswith('LAB-CMD-R204V2_'),'ROW_LINK_DRIFT')
  check(dbrows[i-1][0]==i and dbrows[i-1][1]==row['cmd_id'] and dbrows[i-1][2]==row['prev'] and dbrows[i-1][4]==sha(row) and dbrows[i-1][5]==row['before_sha'] and dbrows[i-1][6]==row['after_sha'],'ROW_SHA_OR_PROVENANCE_TAMPER')
  check(row['synthetic'] is True and row['official_effects']==0,'OFFICIAL_EFFECTS_PRESENT')
  check(lastafter is None or row['before_sha']==lastafter,'BEFORE_AFTER_BREAK')
  d=row['detail'];p=row['payload'];kind=row['kind']
  if i==1:
   check(kind=='R204_SPATIAL_INIT' and d['order']==order and p['r204_version']==V,'BAD_INIT')
   check(d['results']['ONG_P2']['result']==initiative['ONG_P2'] and d['results']['LOBO_P1']['result']==initiative['LOBO_P1'],'INIT_DICE_DRIFT')
   fresh=d['new_native_events']
   check(len(fresh)==1 and fresh[0]['action']=='turn_start' and fresh[0]['by']==active,'INIT_NATIVE')
  else:
   actor=active;turns[actor]+=1;turn=turns[actor]
   if actor=='ONG_P2':
    if kind=='R204_ACTUAL_SOURCE_MAGIC_NO_CRIT':
     check(policy=='CAST_WHEN_IN_RANGE' and geo<=9 and pa[actor]>=8,'CAST_WHEN_NOT_ALLOWED')
     check(d['kind']=='NATIVE_RD_SPATIAL_MAGIC_CAST' and p['own_turn']==turn,'MAGIC_BRANCH_DRIFT')
     ev=d['effect'];paid=d['paid'];rng=magic_roll(seed,turn)
     check(ev['rolls']==rng['damage'] and p['source_rolls']==rng,'MAGIC_RNG_DRIFT')
     score=sum(rng['hit'])+19;hit=score>34
     raw=sum(rng['damage'])+28 if hit else 0;rd=15 if hit else 0
     net=max(0,raw-rd);lost=min(hp['LOBO_P1'],net)
     check(ev['attack_roll']==rng['hit'] and ev['attack_score']==score and ev['attack_bonus']==19 and ev['target_ca']==34 and ev['hit']==hit,'SPELL_HIT_TEST_DRIFT')
     check(ev['spell_attack_test_literal']=='4d6+INT19','NOT_EXPLICIT_SPELL_TEST')
     check(ev['raw']==raw and ev['net']==net and ev['rd_applied']==rd and ev['hp_loss_actual']==lost,'MAGIC_DAMAGE_DRIFT')
     check(ev['hp_before']==hp['LOBO_P1'] and ev['hp_after']==hp['LOBO_P1']-lost,'MAGIC_HP_DRIFT')
     check(ev['distance_m']==str(geo) and Fraction(ev['distance_m'])<=9 and ev['limit_m']=='9' and ev['range_source']== 'https://app.notion.com/p/3ffc2b324ede81c5a5c3d56cc6a29f84','MAGIC_GEOMETRY_DRIFT')
     check(ev['critical']=='NONE' and ev['critical_tape'] is None and ev['attack_roll']==rng['hit'] and ev['save_roll'] is None,'MAGIC_ILLEGAL_CRIT_OR_ROLL')
     check(ev['PA_before']==pa[actor] and ev['PA_after']==pa[actor]-8 and paid['PA_before']==pa[actor] and paid['PA_after']==pa[actor]-8 and paid['PA_spent']==8,'MAGIC_PA_DRIFT')
     check(paid['spell_effect_seq']==ev['seq'] and d['PA_paid']==8,'PA_CROSS_REF_MISSING')
     check(ev['action_cost']=='STANDARD' and ev['dice_expression']=='8d6+28' and ev['evocation_discount']=='NOT_APPLIED_NO_EXPLICIT_SPELL_TAG','SOURCE_MAGIC_CONTRACT_DRIFT')
     hp['LOBO_P1']-=lost;pa[actor]-=8;magic_count+=1;magic_pa+=8;magic_hp+=lost
     fresh=d['new_native_events'];check(fresh[0]==ev and fresh[1]==paid,'MAGIC_NATIVE_MISMATCH')
    elif kind=='R204_SPATIAL_SPELL_REJECT_OR_DECLINE':
     reason='NEVER_CAST_POLICY' if policy=='NEVER_CAST_CONTROL' else 'OUTSIDE_9M' if geo>9 else 'INSUFFICIENT_PA' if pa[actor]<8 else 'NOT_ALLOWED'
     check(reason!='NOT_ALLOWED' and p['reason']==reason and d['reason']==reason,'PASS_FALSE')
     check(p['PA_spent']==0 and p['distance_m']==str(geo),'RANGE_INVALID_PA_CHARGED')
     fresh=d['new_native_events'];check(fresh[0]['action']=='spatial_spell_declined' and fresh[0]['reason']==reason and fresh[0]['PA_spent']==0,'INVALID_SPELL_EFFECT_APPLIED')
     declines[reason]+=1
    else:check(False,'UNKNOWN_ONG_ACTION')
    check(p['actor']=='ONG_P2','WRONG_ONG_ACTOR')
   else:
    check(kind=='R204_BEAST_SPATIAL_MOVE_AND_ATTACK' and d['kind']=='SOURCE_SCOPED_BASIC_ATTACK','BEAST_HANDLER_DRIFT')
    move=d.get('spatial_movement');fresh=d['events_added']
    if geo:
     check(geo<=15 and move is not None and move['action']=='spatial_move' and Fraction(move['movement_spent_m'])==geo and move['end_distance_m']=='0','MOVEMENT_TELEPORT_OR_SPEED_DRIFT')
     check(fresh[0]==move and move['speed_m']=='15' and move['move_budget_used']==1,'MOVE_NATIVE_DRIFT')
     geo=Fraction(0);move_count+=1
    else:check(move is None,'DOUBLE_MOVE')
    roll=d['tape'];expect={'crit':base_dice(seed,'LOBO_P1',turn,'CRIT',3,6),
      'hit':[base_dice(seed,'LOBO_P1',turn,'HIT0',2,6)],
      'damage':[base_dice(seed,'LOBO_P1',turn,'DMG0',1,6)]}
    # Weak player requires second hit tape and -2; source adapter already validates it; audit independently.
    weak=10*hp['LOBO_P1']<240 and hp['LOBO_P1']>0
    if weak:expect['hit'].append(base_dice(seed,'LOBO_P1',turn,'HIT1',2,6))
    check(roll==expect and p['roll_tape']==expect,'WOLF_RANDOM_TAPE_DRIFT')
    hitroll=(min(map(sum,expect['hit']))-2 if weak else sum(expect['hit'][0]))+24
    crit=expect['crit'];ctype='POSITIVE' if crit[:2]==[6,6] and crit[2]>=5 else 'NEGATIVE' if crit[:2]==[1,1] and crit[2]<=2 else 'NONE'
    hit=(hitroll>30 or ctype=='POSITIVE') and ctype!='NEGATIVE'
    base_val=sum(expect['damage'][0])+24;raw=base_val+(6 if ctype=='POSITIVE' else 0) if hit else 0
    loss=min(hp['ONG_P2'],raw);ev=d['attack']
    check(ev['roll_score']==hitroll and ev['critical']==ctype and ev['hit']==hit,'WOLF_HIT_DRIFT')
    check(ev['raw']==raw and ev['net']==raw and ev['hp_loss_actual']==loss and ev['before_hp']==hp['ONG_P2'] and ev['after_hp']==hp['ONG_P2']-loss,'WOLF_DAMAGE_DRIFT')
    check(any(x==ev for x in fresh),'ATTACK_NOT_IN_NATIVE')
    hp['ONG_P2']-=loss;attack_count+=1
   # Check sequential event order and causal turn progress.
   if 0 in hp.values():
    check(fresh[-1]['action']=='turn_end','NO_TURN_END_ON_KO')
    check(i==len(rows),'POST_MORTEM_ATTACK')
    active=None
   else:
    check(fresh[-1]['action']=='turn_start' and fresh[-1]['by']==('LOBO_P1' if actor=='ONG_P2' else 'ONG_P2'),'TURN_NOT_ADVANCED')
    active='LOBO_P1' if actor=='ONG_P2' else 'ONG_P2'
   if actor==order[-1] and active is not None:roundno+=1
  for ev in fresh:
   check(ev['seq']==len(native)+1,'EVENT_SEQ_DRIFT')
   native.append(ev)
  lastafter=row['after_sha'];head=sha(row)
 check(head==meta['head'] and sha(st)==lastafter,'LEDGER_HEAD_OR_STATE_DRIFT')
 check(st['native_events']==native,'NATIVE_EVENT_TAMPER')
 check(st['actors']['ONG_P2']['resource']['hp']==hp['ONG_P2'] and st['actors']['LOBO_P1']['resource']['hp']==hp['LOBO_P1'],'HP_FINAL_INCONSISTENT')
 check(st['actors']['ONG_P2']['resource']['pa']==pa['ONG_P2'] and st['actors']['LOBO_P1']['resource']['pa']==pa['LOBO_P1'],'PA_FINAL_INCONSISTENT')
 check(Fraction(st['geo']['distance_m'])==geo,'FINAL_GEOMETRY_DRIFT')
 check(st['magic_live']['spell_count']==magic_count and st['magic_live']['PA_spent']==magic_pa and st['magic_live']['spell_hp_removed']==magic_hp,'SPELL_METRICS_DRIFT')
 check(st['magic_live']['range_refusals']==declines['OUTSIDE_9M'] and st['magic_live']['never_cast_passes']==declines['NEVER_CAST_POLICY'],'DECLINE_METRICS_DRIFT')
 check(st['magic_live']['movement_events']==move_count and st['magic_live']['no_critical_guarantee'] is True,'BEAST_MOVE_OR_CRIT_DRIFT')
 check(st['metrics']['pa_spent']==magic_pa,'OVERCHARGED_PA')
 check(st['phase']=='FINISHED' and st['winner']==next(x for x in PAIR if hp[x]>0) and active is None,'KO_STATE_DRIFT')
 ck=json.loads((path.parent/(path.name+'.checkpoint.json')).read_text());check(sha(ck['body'])==ck['sha256'],'CHECKPOINT_DRIFT')
 return{'id':path.stem,'seed':seed,'distance':str(float(dist)) if dist.denominator!=1 else str(dist),'policy':policy,'winner':st['winner'],'commits':len(rows),
   'native_events':len(native),'magic_casts':magic_count,'PA_spent':magic_pa,'magic_actual_HP_removed':magic_hp,
   'distance_rejections':declines['OUTSIDE_9M'],'beast_moves':move_count,'physical_attacks':attack_count,
   'SHA256_DB':hashlib.sha256(path.read_bytes()).hexdigest()}

def main():
 records=[audit(p)for p in sorted((ROOT/'evidence/v2_db').glob('*.sqlite'))]
 src=json.loads((ROOT/'evidence/R204_V2_LIVE_MAGIC_RESULTS.json').read_text())
 check(len(records)==len(src)==32 and {r['id'] for r in records}=={x['run_id'] for x in src},'AUDIT_MISSING_RECORDS')
 out={'status':'PASS_R204V2_CODE_SEPARATE_SEMANTIC_AUDIT','battles':len(records),'KO':len(records),'commits':sum(x['commits']for x in records),
      'native_events':sum(x['native_events']for x in records),'magic_casts':sum(x['magic_casts']for x in records),
      'PA_magic_spent':sum(x['PA_spent']for x in records),'magic_actual_HP_removed':sum(x['magic_actual_HP_removed']for x in records),
      'distance_refusals':sum(x['distance_rejections']for x in records),'wolf_movement_events':sum(x['beast_moves']for x in records),
      'wolf_physical_attacks':sum(x['physical_attacks']for x in records),'independent_external_auditor':False,
      'official_benchmark_credits':0,'native_magic_core_complete':False,'records':records}
 (ROOT/'evidence/R204_V2_INDEPENDENT_AUDIT.json').write_text(json.dumps(out,indent=2,ensure_ascii=False))
 print(json.dumps({k:v for k,v in out.items()if k!='records'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
