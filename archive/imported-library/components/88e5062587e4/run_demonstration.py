from pathlib import Path
import json,sys,hashlib
from ibx17_r51_r60_lab_driver import *
R=Path(__file__).resolve().parent
OUT=R/'reports';OUT.mkdir(parents=True,exist_ok=True)
# Repeated test copies independent, no forced rollback: user-authorized behavior.
src=seed_human_level_one();a=ExperimentalStore(R/'tests'/'human_normal_up_a',src)
p1=preview_up(a.state,{'SAB':2});ok=a.commit(p1,'SIM-R55-HUMAN-UP-L2')
p2=preview_up(a.state,{'CAR':2});ok2=a.commit(p2,'SIM-R55-HUMAN-UP-L3')
b=ExperimentalStore(R/'tests'/'human_normal_up_b',src)
bp=preview_up(b.state,{'INT':2});bok=b.commit(bp,'SIM-R55-HUMAN-UP-B-L2')
assert a.state['level']==3 and b.state['level']==2
assert a.state['hp_max']==30 and a.state['pa_max']==52 and a.state['ff']==70
assert b.state['pa_max']==42 and b.state['hp_max']==24
out={'status':'LOCAL_SYNTHETIC_EXECUTED','source':'Criação de Ficha regras 2,4,5,6',
    'fixture':'Humano sintético normal, sem equipamento/título/transformação',
    'initial_state':src,'fork_A':{'level1_to2':p1,'receipt1':ok,'level2_to3':p2,'receipt2':ok2,'final':a.state,'event_count':len(a.journal)},
    'fork_B':{'level1_to2':bp,'receipt':bok,'final':b.state,'event_count':len(b.journal)},
    'isolated':True,'notion_writes':0,'official_writes':0,'notion_native_validation':'NOT_RUN'}
(OUT/'DEMO_LEVEL_UP_NORMATIVE_SUBSET.json').write_text(json.dumps(out,indent=2,ensure_ascii=False))
# Replaying a historical R30 recorded before/after, NOT re-running the unavailable V05 engine.
source=R/'recovered'/'LEVELUP_IBX17_LEVELDOWN_CHAT_R30_20261015'/'LEVELUP_IBX17_LEVELDOWN_CHAT_R30_20261015'/'EVIDENCIAS'/'LEVELDOWN_DEMO'/'02_PREVIA.json'
ref=historical_down_reference(source)
d=ExperimentalStore(R/'tests'/'historical_down_replay_copy',ref['before']);receipt=d.commit(ref,'SIM-R56-HISTORICAL-R30-REPLAY')
noop=d.commit(ref,'SIM-R56-HISTORICAL-R30-REPLAY');assert noop['status']=='NOOP_ALREADY_APPLIED'
assert d.state['level']==16 and d.state['natural']['DES']==10 and d.state['natural']['CON']==10
rpt={'status':'HISTORICAL_OUTPUT_REPLAY_EXECUTED_LOCAL_COPY','computation_reexecuted':False,
     'replayed_reference':str(source),'reference_sha256':ref['source_file_sha256'],
     'level':16,'before':{'natural':ref['before']['natural'],'hp_max':ref['before']['normal']['hp_max'],'ff':ref['before']['normal']['ff']},
     'after':{'natural':d.state['natural'],'hp_max':d.state['normal']['hp_max'],'ff':d.state['normal']['ff']},
     'receipt':receipt,'duplicate':noop,'notion_writes':0,'official_writes':0,
     'note':'Historical R30 previous output applied to isolated local copy for transactional replay; original V05 engine not recovered'}
(OUT/'DEMO_LEVEL_DOWN_REPLAY_R30.json').write_text(json.dumps(rpt,indent=2,ensure_ascii=False))
print(json.dumps({'UP':{'A':{'level':a.state['level'],'hp':a.state['hp_max'],'pa':a.state['pa_max'],'ff':a.state['ff'],'events':len(a.journal)},
                             'B':{'level':b.state['level'],'hp':b.state['hp_max'],'pa':b.state['pa_max'],'events':len(b.journal)}},
                  'DOWN_REPLAY':{'level':d.state['level'],'natural_DES':d.state['natural']['DES'],'natural_CON':d.state['natural']['CON'],
                                 'hp':d.state['normal']['hp_max'],'ff':d.state['normal']['ff'],'status':receipt['status']},
                  'Notion_writes':0},indent=2))
