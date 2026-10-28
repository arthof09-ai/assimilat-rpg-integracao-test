"""R151 normal progression + spiritual TAP/carry + max cap, TEST only.
Upgrade normal first, mirror normal deltas into form, then independent TAP overlay.
No activation implied by eligibility; rank-cross modeled read-only until R129 gate.
"""
from copy import deepcopy
from fractions import Fraction
from r148_evidence_binding import fractional_budget
class Hold(ValueError):pass
ATTRS=('FOR','DES','CON','INT','SAB','CAR')
FIXED={'Bronze':4,'Prata':5,'Ouro':6,'Ouro Negro':7,'Lendário':12}
RANKS=('Bronze','Prata','Ouro','Ouro Negro','Lendário')
def rank_at(level):
 if not 1<=level<=25:raise Hold('INVALID_LEVEL')
 return RANKS[(level-1)//5]

def preview(state,*,event,allocation,mode='FIXED60_EXPLICIT'):
 if event in state.get('consumed_events',[]):return {'decision':'NOOP_ALREADY_CONSUMED','writes':0}
 if mode!='FIXED60_EXPLICIT' or set(allocation)!=set(ATTRS) or any(type(x)!=int or x<0 for x in allocation.values()) or sum(allocation.values())!=2:raise Hold('HUMAN_TEST_EXPLICIT_2_POINTS_REQUIRED')
 s=deepcopy(state);lv=s['normal']['level'];newlv=lv+1
 if newlv>25:raise Hold('MAX_LEVEL')
 oldrank=rank_at(lv);newrank=rank_at(newlv)
 if oldrank!=newrank:return {'decision':'HOLD_RANK_NATIVE_SEPARATE_GATE','preview_only':True,'from_level':lv,'to_level':newlv,'would_unlock_transform':newlv>=6}
 oldnormal=s['normal'];n=deepcopy(oldnormal)
 n['level']=newlv;n['rank']=newrank
 for k,v in allocation.items():n['natural_attrs'][k]+=v
 fixed=FIXED[newrank]
 n['hp_max']+=fixed+n['natural_attrs']['CON'];n['pa_max']+=fixed+n['natural_attrs']['INT']
 effective={k:n['natural_attrs'][k]+sum(layer.get(k,0) for layer in s.get('layers',{}).values()) for k in ATTRS}
 recomputed_ff=10*(effective['FOR']+effective['DES']+effective['CON'])
 if recomputed_ff!=oldnormal['ff']:raise Hold('FF_LAYER_DECOMPOSITION_CONFLICT')
 n['ff']=recomputed_ff
 # physical current resources unchanged; equipment remains a separate layer.
 if n['hp_current']>n['hp_max'] or n['pa_current']>n['pa_max']:raise Hold('RESOURCE_CURRENT_ABOVE_NEW_MAX')
 overlay=deepcopy(s['spirit_overlay']);bap=overlay['bap_synthetic'];cap=overlay['cap_ordinal']
 budget=fractional_budget(bap=bap,level=newlv,cap=cap,previous_distributed=overlay['allocation'])
 previous_total=sum(overlay['allocation'].values());increment=budget['distributable']-previous_total
 if increment<0:raise Hold('SPIRIT_DISTRIBUTION_CONFLICT')
 # Pure preview refuses to invent allocation; staged candidate explicitly proposes a single target from TEST plan.
 target=overlay.get('proposed_attribute_for_next_gain')
 if increment>0:
  if target not in ATTRS:raise Hold('SPIRIT_DISTRIBUTION_CHOICE_MISSING')
  overlay['allocation'][target]=overlay['allocation'].get(target,0)+increment
 overlay['distributed_total']=sum(overlay['allocation'].values());overlay['carry_numerator']=budget['carry_numerator'];overlay['carry_denominator']=budget['carry_denominator'];overlay['effective_level']=budget['effective_level'];overlay['checksum']=budget['checksum'];overlay['active']=False
 # shared normal delta mirrored before independent spirit overlay; no double-count.
 overlay['normal_mirrored_attrs']=deepcopy(n['natural_attrs'])
 s['normal']=n;s['spirit_overlay']=overlay;s['consumed_events']=s.get('consumed_events',[])+[event]
 s.setdefault('history',[]).append({'event':event,'normal_allocation':allocation,'normal_fixed_die':fixed,'spirit_increment':increment,'carry':str(Fraction(budget['carry_numerator'],budget['carry_denominator'])),'form_auto_activated':False})
 s['status']='PREVIEW_TEST_NOT_APPLIED';return {'decision':'PREVIEW_READY_TEST_ONLY','before':state,'after':s,'level_delta':1,'normal_allocated':sum(allocation.values()),'spirit_increment':increment,'rank_cross':False,'form_remained_inactive':True}

def selftest():
 attr={'FOR':6,'DES':10,'CON':10,'INT':8,'SAB':7,'CAR':4}
 base={'normal':{'level':17,'rank':'Ouro Negro','natural_attrs':attr,'hp_max':309,'hp_current':240,'pa_max':273,'pa_current':150,'ff':290},'layers':{'title':{'SAB':2},'equipment':{'DES':3}},'spirit_overlay':{'bap_synthetic':11,'cap_ordinal':20,'allocation':{'SAB':93},'distributed_total':93,'carry_numerator':1,'carry_denominator':2,'effective_level':17,'proposed_attribute_for_next_gain':'SAB','active':False},'permanent_milestones':{'100':{'choice':'VIDA','rolls':[2,3],'source':'R111_TEST_CLONE_NOT_ACTOR_HISTORY'}},'consumed_events':[]}
 # valid budget at lv17 is floor(5.5*17)=93 and carry 0.5.
 d={'FOR':0,'DES':0,'CON':0,'INT':2,'SAB':0,'CAR':0}
 r=preview(base,event='TEST-LEVEL18',allocation=d);assert r['decision']=='PREVIEW_READY_TEST_ONLY';n=r['after']['normal'];sp=r['after']['spirit_overlay']
 assert n['level']==18 and n['natural_attrs']['INT']==10 and n['hp_max']==326 and n['pa_max']==290
 assert sp['distributed_total']==99 and sp['carry_numerator']==0 and r['spirit_increment']==6
 assert r['after']['normal']['hp_current']==240 and r['after']['normal']['pa_current']==150 and not sp['active']
 assert preview(r['after'],event='TEST-LEVEL18',allocation=d)['decision']=='NOOP_ALREADY_CONSUMED'
 capped=deepcopy(base);capped['spirit_overlay']['cap_ordinal']=17
 assert preview(capped,event='CAPPED',allocation=d)['spirit_increment']==0
 near=deepcopy(base);near['normal']['level']=5;near['normal']['rank']='Bronze'
 assert preview(near,event='CROSS',allocation=d)['decision']=='HOLD_RANK_NATIVE_SEPARATE_GATE'
 return r
if __name__=='__main__':print(selftest()['decision'])
