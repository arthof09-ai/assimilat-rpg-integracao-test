"""Cold semantic validator (independently coded): reads R18 SQL only.
Does NOT import R199 producer, R198 producer, or combat mutators. Reconstructs
critical, attack dice, source-scoped RD, HP, transform reserves, magic PA,
initiative roll, native event order, commit hash-chain, and checkpoints.
R199 TEST certification, not external independent authority.
"""
from __future__ import annotations
import collections,hashlib,json,pathlib,random,re,sqlite3,sys
ROOT=pathlib.Path(__file__).resolve().parents[3];R199=ROOT/'new/r199';VER='R198-R18-SOURCE-SCOPED-MICROBENCH-1'
SRC1=R199/'source/R199_TRANSFORM_PREREG.json';SRC2=R199/'source/R199_BEAST_PREREG.json'
P1=json.loads(SRC1.read_text());P2=json.loads(SRC2.read_text())
H1=hashlib.sha256(SRC1.read_bytes()).hexdigest();H2=hashlib.sha256(SRC2.read_bytes()).hexdigest()
def canon(o):return json.dumps(o,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def sha(o):return hashlib.sha256(canon(o).encode()).hexdigest()
def ask(ok,label,**details):
 if not ok:raise AssertionError({'failed':label,'details':details})
def roll(seed,pair,who,own_turn,label,n,faces):
 entropy=hashlib.sha256(f'{VER}|{seed}|{pair[0]}-{pair[1]}|{who}|{own_turn}|{label}|{n}d{faces}'.encode()).digest()
 return [random.Random(int.from_bytes(entropy,'big')).randint(1,faces)] if n==1 else _rand_list(entropy,n,faces)
def _rand_list(entropy,n,faces):
 r=random.Random(int.from_bytes(entropy,'big'));return [r.randint(1,faces) for _ in range(n)]
def duration(seed):
 d=hashlib.sha256(f'R199|FORM_DURATION|{seed}|ONG_P2|1d6'.encode()).digest()
 return random.Random(int.from_bytes(d,'big')).randint(1,6)
def semantic(db):
 path=pathlib.Path(db);filename=path.name
 m=re.fullmatch(r'R199_ONG_LOBO_(\d+)_(CAST_NORMAL|ACTIVATE_FORM_AND_CAST)\.sqlite',filename)
 b=re.fullmatch(r'R199_LOBO_ANCESTRAL_VS_CAPANGA_(\d+)_(SOURCE_BASE_STAT_ONLY|ANCESTRAL_PLUS2_IF_NOT_INCLUDED)\.sqlite',filename)
 ask(bool(m or b),'RUN_NAME',db=filename)
 is_form=bool(m);seed=int((m or b).group(1));policy=(m or b).group(2)
 prereg=P1 if is_form else P2;h=H1 if is_form else H2
 ask(seed in prereg['seeds'] and policy in prereg['policies'],'PREREGISTRATION')
 pair=('ONG_P2','LOBO_P1') if is_form else ('CAPANGA_P3','LOBO_P1')
 specs={'ONG_P2':{'hp':99,'pa':91,'ca':30,'rd':0,'att':(4,6),'dmg':((8,6),),'bonus':19,'flat':28,'des':15,'init_bonus':15},
  'CAPANGA_P3':{'hp':196,'pa':128,'ca':25,'rd':0,'att':(2,6),'dmg':((2,10),(2,8)),'bonus':25,'flat':36,'des':16,'init_bonus':16},
  'LOBO_P1':{'hp':240,'pa':180,'ca':34,'rd':15,'att':(2,6),'dmg':((1,6),),'bonus':24,'flat':24,'des':20,'init_bonus':20}}
 conn=sqlite3.connect(f'file:{path}?mode=ro',uri=True)
 try:
  meta=dict(conn.execute('SELECT key,value FROM meta'))
  rows=conn.execute('SELECT seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha FROM events ORDER BY seq').fetchall()
  ask(conn.execute('SELECT count(*) FROM pending').fetchone()[0]==0,'PENDING_UNRESOLVED')
 finally:conn.close()
 ask(int(meta['revision'])==len(rows),'REVISION');st=json.loads(meta['state'])
 ask(st['seed']==seed and st['pair']==list(pair),'FINAL_IDENTITY')
 ask(st['r199_pre_reg_sha' if is_form else 'r199_beast_pre_sha']==h,'PREREG_HASH')
 ask(st['r199_policy' if is_form else 'r199_beast_policy']==policy,'POLICY_CHANGED')
 init={}
 for who in pair:
  s=specs[who];draw=roll(seed,pair,who,0,'INIT',2,6);init[who]=sum(draw)+s['init_bonus']
 ask(len(set(init.values()))==2,'INIT_TIE_COMMITTED')
 order=sorted(pair,key=lambda a:-init[a]);active=None;round_no=1;hp={k:specs[k]['hp'] for k in pair};pa={k:specs[k]['pa'] for k in pair}
 ca={k:specs[k]['ca'] for k in pair};nturn=collections.Counter();native=[];head=meta['genesis'];after_prev=None
 form_active=False;form_used=False;temp=0;normal_hp=99;normal_pa=91;extra_pa=0;remaining=0;transforms=0;expires=0
 casts=0;spell_hp=0;bonus_actions=0;attempts=0;hits=0;critpos=0;critneg=0;damage_gross=0;postrd=0;hp_loss=0;overkill=0;pa_spent=0
 for j,(seq,cmd,prev,row_json,row_sha,before_sha,after_sha) in enumerate(rows):
  x=json.loads(row_json);d=x['detail'];p=x['payload'];kind=x['kind']
  ask(seq==j+1 and prev==head and x['seq']==seq and x['prev']==prev and x['cmd_id']==cmd,'LEDGER_CHAIN',seq=seq)
  ask(x['before_sha']==before_sha and x['after_sha']==after_sha and sha(x)==row_sha and (after_prev is None or before_sha==after_prev),'LEDGER_INTEGRITY',seq=seq)
  ask(x.get('synthetic') is True and x.get('official_effects')==0,'UNAUTHORIZED_STATUS',seq=seq)
  fresh=d.get('new_native_events') or d.get('events_added') or d.get('added') or []
  if j==0:
   ask(kind in ('R199_INIT','R199_BEAST_INIT') and d['order']==order,'INIT_ORDER',seq=seq)
   ask(fresh and fresh[0]['action']=='turn_start' and fresh[0]['by']==order[0],'INIT_TURN',seq=seq)
   ask(all(d['results'][k]['result']==init[k] and d['results'][k]['roll']==roll(seed,pair,k,0,'INIT',2,6) for k in pair),'INIT_ROLL_SEMANTICS',seq=seq)
   active=order[0]
  else:
   who=active;other=next(x for x in pair if x!=who)
   ask(who in pair,'ACTION_AFTER_KO',seq=seq)
   nturn[who]+=1;own=nturn[who]
   if kind=='R199_TRANSFORM_ACTIVATE':
    ask(is_form and who=='ONG_P2' and policy=='ACTIVATE_FORM_AND_CAST' and not form_used and own==1,'TRANSFORM_ILLEGAL',seq=seq)
    ask(p['duration_roll']==duration(seed) and d['event']['duration_roll']==duration(seed),'DURATION_ROLL',seq=seq)
    ev=fresh[0];ask(d['event']==ev,'TRANSFORM_EVENT_DETAIL_INCONSISTENT',seq=seq);ask(ev['action']=='transform_activate' and ev['source']=='https://app.notion.com/p/3f2c2b324ede81c0ae0ee4e66212edc9','FORM_SOURCE')
    ask(ev['cost']==40 and ev['ca_after']==36 and ev['form_temporary_hp_conditional']==54 and ev['form_additional_pa_conditional']==63,'FORM_SOURCE_VAL')
    normal_pa-=40;extra_pa=63;pa['ONG_P2']=normal_pa+extra_pa;temp=54;hp['ONG_P2']=normal_hp+temp;ca['ONG_P2']=36
    transforms+=1;pa_spent+=40;form_active=True;form_used=True;remaining=duration(seed)+1
    ask(ev['duration_total']==remaining and len(fresh)==3,'FORM_TIMING')
    active=other
    if who==order[-1]:round_no+=1
   elif kind=='R199_SPELL_NO_PA_PASS':
    ask(is_form and who=='ONG_P2' and pa[who]<8 and not form_active,'PASS_WITH_PA_AVAILABLE',seq=seq)
    ask(fresh[0]['action']=='spell_declined' and fresh[0]['PA_spent']==0,'PASS_NONZERO_PA',seq=seq)
    active=other
    if who==order[-1]:round_no+=1
   elif kind in ('R199_BEAST_NORMAL_ATTACK','R199_WATER_WHIP','R199_SOURCE_SCOPED_PHYSICAL_ATTACK'):
    ask(p['actor']==who and p['target']==other and p['own_turn']==own,'ATTACK_IDENTITY',seq=seq,file=filename,expected_actor=who,actual_actor=p['actor'],expected_turn=own,actual_turn=p['own_turn'])
    ev=d['attack'];ask(fresh and ev==fresh[0] and ev['action']=='weapon_attack','ATTACK_NATIVE_CORRELATION')
    # Reconstruct frozen per-actor/per-turn original source RNG, conditional +2 FOR, transformed magic bonuses.
    s=specs[who];weak=hp[who]>0 and hp[who]*10<(153 if who=='ONG_P2' and form_active else s['hp'])
    ret={'crit':roll(seed,pair,who,own,'CRIT',3,6),
      'hit':[roll(seed,pair,who,own,'HIT'+str(k),*s['att']) for k in range(2 if weak else 1)],
      'damage':[roll(seed,pair,who,own,'DMG'+str(k),n,faces) for k,(n,faces) in enumerate(s['dmg'])]}
    ask(p['roll_tape']==ret,'RNG_TAPE',seq=seq)
    extra=2 if (not is_form and who=='LOBO_P1' and policy=='ANCESTRAL_PLUS2_IF_NOT_INCLUDED') else 0
    transformed_spell=is_form and who=='ONG_P2' and form_active
    bonus=(25 if transformed_spell else s['bonus'])+extra
    flat=(34 if transformed_spell else s['flat'])+extra
    score=(min(map(sum,ret['hit']))+bonus-2 if weak else sum(ret['hit'][0])+bonus)
    crit=('POSITIVE' if ret['crit'][:2]==[6,6] and ret['crit'][2]>=5 else 'NEGATIVE' if ret['crit'][:2]==[1,1] and ret['crit'][2]<=2 else 'NONE')
    hit=(score>ca[other] or crit=='POSITIVE') and crit!='NEGATIVE'
    nominal=sum(sum(x) for x in ret['damage'])+flat
    gross=nominal+(sum(n*faces for n,faces in s['dmg']) if crit=='POSITIVE' else 0) if hit else 0
    rd=specs[other]['rd'] if hit else 0
    net=max(0,gross-rd) if hit else 0
    prior=hp[other];taken=min(prior,net);hp[other]-=taken
    assert ev['critical_sequence']==ret['crit'] and ev['damage_roll_groups']==ret['damage']
    for k,v in {'from':who,'to':other,'roll_score':score,'ca_exact':str(ca[other]),'critical':crit,'hit':hit,
                'raw':gross,'rd_applied':rd,'net':net,'before_hp':prior,'after_hp':hp[other],
                'hp_loss_actual':taken,'overkill':max(0,net-prior),'normal_damage':nominal}.items():
     ask(ev[k]==v,'MATH_FIELD',seq=seq,field=k,got=ev[k],want=v)
    attempts+=1;hits+=int(hit);critpos+=int(crit=='POSITIVE');critneg+=int(crit=='NEGATIVE');damage_gross+=gross;postrd+=net;hp_loss+=taken;overkill+=max(0,net-prior)
    if transformed_spell or (is_form and who=='ONG_P2'):
     ask(kind=='R199_WATER_WHIP' and ev['type']=='agua','MAGIC_IDENTITY_AND_TYPE',seq=seq)
     ask(len(fresh)>=3 and fresh[1]['action']=='spell_pa_cost','MISSING_MAGIC_DEBIT',seq=seq)
     pe=fresh[1];ask(d['paid']==pe and pe['PA_spent']==8,'SPELL_PA_DETAIL_INCONSISTENT',seq=seq);ask(pe['attack_event_seq']==ev['seq'] and pe['source_bonus']==bonus and pe['source_flat_damage']==flat and pe['source']=='https://app.notion.com/p/2b6c2b324ede82a2b415019eae21eaf5','SPELL_SOURCE_OR_LINK',seq=seq)
     before=pa[who];pa[who]-=8;pa_spent+=8;casts+=1;spell_hp+=taken
     if form_active:
      normal_taken=min(8,normal_pa);normal_pa-=normal_taken;extra_pa-=8-normal_taken
     else:normal_pa-=8
     ask(before==pe['PA_before'] and pe['PA_after']==pa[who] and pe['normal_pa_after']==normal_pa and pe['additional_pa_after']==extra_pa,'SPELL_PA',seq=seq)
    else:
     ask(ev['type']=='impacto' and kind in ('R199_BEAST_NORMAL_ATTACK','R199_SOURCE_SCOPED_PHYSICAL_ATTACK'),'NORMAL_ATTACK_SOURCE',seq=seq)
     if extra:
      z=d.get('source_passive_overlay');ask(z is not None and z['FOR_plus']==2 and z['native_attack_seq']==ev['seq'] and z['source']==P2['source'],'BEAST_PASSIVE_PROOF',seq=seq)
      bonus_actions+=1
    if is_form and other=='ONG_P2':
     if form_active:
      reduction=min(temp,taken);temp-=reduction;normal_hp-=taken-reduction
      if kind=='R199_BEAST_NORMAL_ATTACK':
       z=d['resource_split'];ask(z['normal_hp_remaining']==normal_hp and z['temporary_hp_remaining']==temp and z['attack_native_seq']==ev['seq'],'FORM_HP_SPLIT',seq=seq)
     else:normal_hp=hp['ONG_P2']
    if is_form and who=='ONG_P2' and form_active and hp[other]>0:
     remaining-=1
     exp=[e for e in fresh if e['action']=='transform_expire']
     if remaining==0:
      ask(len(exp)==1 and d['expiration']==exp[0] and exp[0]['before']['additional_pa']==extra_pa and exp[0]['before']['temp_hp']==temp,'FORM_EXPIRE_MISSING')
      hp['ONG_P2']=normal_hp;pa['ONG_P2']=normal_pa;ca['ONG_P2']=30;temp=0;extra_pa=0;form_active=False;expires+=1
      ask(exp[0]['after']=={'hp':hp['ONG_P2'],'pa':normal_pa,'ca':'30'},'FORM_EXPIRE_POOLS')
     else:ask(not exp,'PREMATURE_FORM_EXPIRE')
    if hp[other]==0:
     active=None
     ask(seq==len(rows),'POST_KO_COMMIT')
     if is_form and other=='ONG_P2' and form_active:
      ask(fresh[-1]['action']=='transform_end_on_ko','KO_FORM_END_MISSING')
      form_active=False;expires+=1;remaining=0
     if is_form and who=='ONG_P2' and form_active:
      # On victory scene ends, active form duration does not reset without a rule.
      pass
    else:
     active=next(a for a in order if a!=who)
     if who==order[-1]:round_no+=1
   else:raise AssertionError(('UNEXPECTED_ROW',kind,seq))
   # Event group boundaries: each transaction publishes its entire native chain at once.
   ask(fresh and fresh[-1]['action'] in ('turn_start','transform_damage_split','transform_end_on_ko','turn_end') or kind=='R199_WATER_WHIP','TURN_END_EVENTS',seq=seq)
  for ev in fresh:
   ask(ev['seq']==len(native)+1 and ev['provenance']==VER+'-EXP-NOT-CAMPAIGN','NATIVE_SEQUENCE_ORIGIN',seq=seq)
   native.append(ev)
  head=row_sha;after_prev=after_sha
 ask(st['native_events']==native and st['actors'] and sha(st)==after_prev,'FINAL_SNAPSHOT')
 ask(head==meta['head'] and st['phase'] in ('FINISHED','ACTIVE'),'FINAL_LEDGER')
 finished=st['phase']=='FINISHED'
 if finished:ask(active is None and st['winner'] in pair,'WINNER_FALSE')
 else:ask(st['winner'] is None,'CENSORED_AS_WIN')
 ask(st['round']==round_no,'ROUND_REPLAY',round_actual=st['round'],want=round_no)
 for who in pair:
  ask(st['actors'][who]['resource']['hp']==hp[who] and st['actors'][who]['resource']['pa']==pa[who], 'RESOURCE_FINAL',actor=who)
  ask(str(st['actors'][who]['resource']['ca'])==str(ca[who]),'CA_FINAL',actor=who)
 for k,v in {'attempts':attempts,'hits':hits,'crit_positive':critpos,'crit_negative':critneg,'damage_gross':damage_gross,
             'post_rd':postrd,'hp_loss':hp_loss,'overkill':overkill,'pa_spent':pa_spent}.items():
  ask(st['metrics'][k]==v,'METRIC_REPLAY',metric=k)
 if is_form:
  ask(st['r199_events']=={'spell_count':casts,'spell_hp':spell_hp,'transform_activations':transforms,'transform_expirations':expires},'FORM_METRICS')
  ask(st['form']['active']==form_active and st['form']['normal_hp']==normal_hp and st['form']['normal_pa']==normal_pa,'FORM_FINAL_POOLS')
  ask(st['form']['used_scene']==form_used and st['form']['temp_hp']==temp and st['form']['additional_pa']==extra_pa,'FORM_RESERVE_FINAL')
  ask(st['form']['remaining']==remaining,'FORM_DURATION_FINAL')
 else:ask(st['r199_beast_bonus_applied_attacks']==bonus_actions,'BEAST_METRIC')
 cp=path.with_name(path.name+'.checkpoint.json');check=json.loads(cp.read_text());ask(sha(check['body'])==check['sha256'],'CHECKPOINT_SHA');ask(check['body']['head']==head,'CHECKPOINT_HEAD')
 return {'db':filename,'status':'PASS_SEMANTIC_COLD_REPLAY','seed':seed,'policy':policy,'winner':st['winner'],
         'fight_status':st['phase'] if finished else 'CENSORED_HORIZON','rounds':st['round'],
         'attacks':attempts,'hits':hits,'damage_hp_loss_total':hp_loss,'spells':casts,'spell_hp':spell_hp,
         'transform_activations':transforms,'transform_expirations':expires,'beast_power_uses':bonus_actions,
         'pa_spent':pa_spent,'commits':len(rows),'native_events':len(native),'hp_final':hp,
         'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

def main():
 all_dbs=sorted((R199/'evidence/db').glob('*.sqlite'))
 outputs=[semantic(p) for p in all_dbs]
 assert len(all_dbs)==32
 res={'status':'PASS_R199_COLD_SEMANTIC_AUDIT','sample_count':len(outputs),
      'commits':sum(x['commits']for x in outputs),'native_events':sum(x['native_events']for x in outputs),
      'attacks':sum(x['attacks']for x in outputs),'records':outputs,'independent_authority':False}
 (R199/'evidence/R199_INDEPENDENT_AUDIT.json').write_text(json.dumps(res,indent=2,ensure_ascii=False))
 print(json.dumps({k:v for k,v in res.items() if k!='records'}));return res
if __name__=='__main__':main()
