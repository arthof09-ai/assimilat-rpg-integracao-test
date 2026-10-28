"""Rank rebase R129 additive fixed60 synthetic test math; no player or canonical edit."""
import json
from r127_receipt_protocol import sha
EVENT='IBX17-R129-RANK-20261017-01'
BEFORE={
 'NORMAL':{'actor_id':'SYNTH-IBX17-R129-01','race':'Humano','level':5,'rank':'Bronze 5','attrs':{'FOR':4,'DES':3,'CON':2,'INT':14,'SAB':6,'CAR':6},'ca':9,'synthetic':True},
 'TRANSFORM':{'natural_hp':42,'hp_max':42,'hp_current':20,'natural_pa':86,'pa_max':86,'pa_current':45,'pa_committed':0,'pa_free':86,'external_hp_bonus':0,'external_pa_bonus':0,'form_active':False},
 'LOCKS':{'ff':90,'permanent_milestones':{},'rank_ledger':[{'stage':'PRE_BRONZE5_R105','documentation_only':True}]}}
AFTER={
 'NORMAL':{**BEFORE['NORMAL'],'level':6,'rank':'Prata 1','attrs':{**BEFORE['NORMAL']['attrs'],'INT':16}},
 'TRANSFORM':{**BEFORE['TRANSFORM'],'natural_hp':54,'hp_max':54,'natural_pa':142,'pa_max':142,'pa_free':142},
 'LOCKS':{**BEFORE['LOCKS'],'rank_ledger':BEFORE['LOCKS']['rank_ledger']+[{'event_id':EVENT,'from_level':5,'to_level':6,'rank_rebase':'REPLACE_NATURAL_NOT_ADD','fixed60':'d8=5','validated_test_only':True}]}}

def validate(b,a):
 assert b['NORMAL']['level']==5 and a['NORMAL']['level']==6
 assert b['NORMAL']['rank']=='Bronze 5' and a['NORMAL']['rank']=='Prata 1'
 assert a['NORMAL']['attrs']['INT']==16 and a['NORMAL']['attrs']['CON']==2
 assert a['TRANSFORM']['hp_max']==54 and a['TRANSFORM']['pa_max']==142
 assert a['TRANSFORM']['hp_max']!=42+54 and a['TRANSFORM']['pa_max']!=86+142
 assert a['TRANSFORM']['hp_current']==b['TRANSFORM']['hp_current']==20
 assert a['TRANSFORM']['pa_current']==b['TRANSFORM']['pa_current']==45
 assert a['LOCKS']['ff']==b['LOCKS']['ff']==90
 assert len(a['LOCKS']['rank_ledger'])==len(b['LOCKS']['rank_ledger'])+1
 assert sum(x['event_id']==EVENT for x in a['LOCKS']['rank_ledger'] if 'event_id' in x)==1
 return True
if __name__=='__main__':
 print('R129 VALIDATED',validate(BEFORE,AFTER),'stages',[(k,sha(BEFORE[k]),sha(AFTER[k])) for k in BEFORE]);print(json.dumps({'event':EVENT,'before':BEFORE,'after':AFTER},ensure_ascii=False))
