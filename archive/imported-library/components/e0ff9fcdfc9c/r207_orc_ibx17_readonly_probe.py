"""VLAB R207: diagnostic of IBX-17's ACTUAL read-only MobileSession on a labeled
synthetic Orc snapshot. No Notion source attestation, write, or LEVEL-UP parity claim.
"""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
NATIVE=ROOT/'reference/ibx17_readonly'
sys.path.insert(0,str(NATIVE))
from r198_dynamic_source import SourceSnapshot,sha,ATTRS
from r199_r200_live_mobile import MobileSession
src=json.loads((ROOT/'source/R207_ORC_HISTORICAL_SNAPSHOTS_READONLY.json').read_text())

def make(level):
 o=src[str(level)];a=o['natural_current']
 normal={'level':level,'rank':('Bronze' if level<=5 else 'Prata'),
 'natural_attrs':a.copy(),'hp_current':o['natural_hp_max'],'hp_max':o['natural_hp_max'],
 'pa_current':o['natural_pa_max'],'pa_max':o['natural_pa_max'],
 'pa_committed':0,'pa_free':o['natural_pa_max'],'ff':o['ff'],
 'ca':o['ca_physical_exact'],'magic_cd':None,'normal_rate':5,'magic_prof':None}
 return SourceSnapshot(page_id=f'LOCAL_SYNTH_ORC_{level}',
   parent_id='3fbc2b324ede804a95fafcb7b293c92c',
   version='LOCAL_READONLY_20261020',layout='LOCAL_ORC_SOURCE_MAP_NOT_NOTION_NATIVE',
   source_hash=sha(o),source_length=len(json.dumps(o)),normal=normal,
   layers={},structural={'media_binary_certified':False},
   provenance='SYNTHETIC_CONSTRUCTED_FROM_HISTORICAL_VLAB_SNAPSHOTS_NOT_NATIVE_NOTION_OBSERVATION',
   status='READONLY_DIAGNOSTIC_NOT_COMMIT_ELIGIBLE')

def case(before,after):
 a=make(before);delta={k:src[str(after)]['natural_current'][k]-src[str(before)]['natural_current'][k] for k in ATTRS}
 assert sum(delta.values())==5 and all(x>=0 for x in delta.values())
 m=MobileSession(source=a,event=f'IBX17-R207-ORC-SYNTHETIC-DIAG-{before}-{after}',levels=1)
 p=m.revise([delta]);step=p['steps'][0];pred=p['after'];target=src[str(after)]
 out={'transition':f'{before}->{after}','actual_code':'r199_r200_live_mobile.MobileSession.revise',
      'fixture':'SYNTHETIC_NOT_NATIVE_ATTESTED','mode':'FIXED60_EXPLICIT','writes':p['writes'],
      'allocation':delta,'source_snapshot_historical':{'hp':src[str(before)]['natural_hp_max'],'pa':src[str(before)]['natural_pa_max'],'ff':src[str(before)]['ff']},
      'target_historical':{'hp':target['natural_hp_max'],'pa':target['natural_pa_max'],'ff':target['ff']},
      'holds':p['holds'],'source_hash':a.source_hash,'preview_hash':p['preview_hash']}
 if pred is None:
  out['preview_after']=None;out['native_rank_gate']=step['hold'];out['decision']='NO_NATIVE_LEVELUP_PARITY__RANK_CROSS_REBASE_PENDING'
 else:
  out['preview_after']={'hp':pred['hp_max'],'pa':pred['pa_max'],'ff':pred['ff']}
  out['differences']={k:{'IBX17_generic':pred[n],'Orc_VLAB_historical':target[t]} for k,n,t in [('hp','hp_max','natural_hp_max'),('pa','pa_max','natural_pa_max'),('ff','ff','ff')] if pred[n]!=target[t]}
  out['decision']='NO_NATIVE_LEVELUP_PARITY__ORC_RACIAL_GROWTH_NOT_IN_GENERIC_PREVIEW' if out['differences'] else 'LOCAL_VALUE_MATCH_ONLY_NOT_NATIVE_ATTESTATION'
 return out

if __name__=='__main__':
 results=[case(1,2),case(5,6)]
 for r in results:assert r['writes']==0
 assert results[0]['preview_after']=={'hp':37,'pa':31,'ff':320}
 assert results[0]['differences']['hp']=={'IBX17_generic':37,'Orc_VLAB_historical':39}
 assert 'RANK_CROSS_REBASE_REQUIRES_SEPARATE_SOURCE_BOUND_RULE' in results[1]['holds']
 report={'audit':'PASS_R207_ORC_NATIVE_CODE_OFFLINE_DIAGNOSTIC_NOT_NATIVE_PARITY',
 'native_code_unmodified':True,'transport':'LOCAL_SYNTHETIC_SOURCE_SNAPSHOT_NO_NOTION_ATTESTATION',
 'comparison_count':2,'results':results,'writer_claim':False,'writes':0,
 'corrective_interface':'RACIAL_DICE_SHIFT_2_BRO_NATURAL_HP_AND_RANK_REBASE_ORC_SOURCE_BOUND',
 'next_owner':'LEVEL-UP ENGINE IBX-17 existing executor, no protected lab modifications'}
 (ROOT/'evidence/R207_ORC_IBX17_NATIVE_PREVIEW_DIAGNOSTIC.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
 print(json.dumps(report,ensure_ascii=False,indent=2))
