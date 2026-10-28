"""Source-scoped R125 synthesis, no player event and no Notion writes.
Existing R113 conditional evaluator and R105 human Bronze 60% source rule.
No FF milestone is rolled: the certified synthetic R111 value is reused.
"""
from copy import deepcopy
import hashlib,json
LOCK={'source':'NORMAL_FIRST_HIT','choice':'VIDA','rolls':[2,3],'total_bonus':5,'synthetic_only':True,'event':'IBX17-R111-FF100-20261016-01'}
BASE={'FOR':4,'DES':3,'CON':2,'INT':5,'SAB':5,'CAR':6}

def derive(level,attrib_delta,equipment=True,temporary=True,title=False):
 a=deepcopy(BASE)
 for k,n in attrib_delta.items():a[k]+=n
 if level not in (1,2):raise ValueError('only test levels 1/2')
 if sum(attrib_delta.values())!=(level-1)*2:raise ValueError('human per-level points invalid')
 t=deepcopy(a)
 if equipment:t['FOR']+=1
 if temporary:t['CON']+=1
 if title:t['SAB']+=2
 ff=(t['FOR']+t['DES']+t['CON'])*10
 hp_nat=18+(6 if level==2 else 0)
 pa_nat=24+(9 if level==2 else 0)
 return {'normal':{'actor':'SYNTH-R125-COMPOSITE', 'race':'Humano','level':level,'rank':f'Bronze {level}','natural_attrs':a,'growth':'FIXED60_EXPLICIT','growth_receipt':{'die':6,'fixed':4},'choice_source':'LAB_TEST_PLAN_NOT_PLAYER'},
  'layers':{'equipment':{'id':'R125-SYNTH-EQUIP','active':equipment,'FOR':1,'PA_MAX':10},'temporary':{'id':'R125-SYNTH-TEMP','active':temporary,'CON':1},'title':{'id':'R125-SYNTH-TITLE','active':title,'SAB':2}},
  'effective_attrs':t,'resources':{'hp_natural_max':hp_nat,'hp_max':hp_nat+(5 if ff>=100 else 0),'hp_current':12,'pa_natural_max':pa_nat,'pa_max':pa_nat+(10 if equipment else 0),'pa_current':15,'pa_committed':5,'pa_free':pa_nat+(10 if equipment else 0)-5},
  'locks':{'ff':ff,'FF100_LOCK':LOCK,'FF100_ACTIVE':ff>=100,'new_rolls':0},'spirit_active':False,'spirit_eligibility':'BRONZE_FORBIDDEN','fixture_only':True}

STEPS=[derive(1,{},True,True,False),derive(2,{'SAB':2},True,True,False),derive(2,{'SAB':2},False,True,False),derive(2,{'SAB':2},False,False,True)]
assert [(s['normal']['level'],s['locks']['ff'],s['resources']['hp_max'],s['resources']['pa_max']) for s in STEPS]==[(1,110,23,34),(2,110,29,43),(2,100,29,33),(2,90,24,33)]
assert all(s['locks']['FF100_LOCK']==LOCK and s['locks']['new_rolls']==0 for s in STEPS)
assert all(s['resources']['hp_current']==12 and s['resources']['pa_current']==15 for s in STEPS)
assert STEPS[3]['effective_attrs']['SAB']==9 and STEPS[3]['locks']['FF100_ACTIVE'] is False
assert all(s['spirit_active'] is False for s in STEPS)
assert STEPS[3]['resources']['pa_free']==28
print('R125: 6 directed integrated invariants PASS')
if __name__=='__main__':
 from pathlib import Path
 Path(__file__).with_name('R125_COMPOSITE_RECEIPTS.json').write_text(json.dumps({'before':STEPS[0],'after':STEPS[-1],'steps':[{'step':i,'event':f'IBX17-R125-S{i}-20261016-01','before':STEPS[i-1],'after':STEPS[i]} for i in range(1,4)]},ensure_ascii=False,indent=2))
