#!/usr/bin/env python3
"""MESTRE-SIDE R10 controlled synthetic fixture against byte-preserved v0.8.1 module.
NO legitimate native real-source scene: synthetic mock proofs borrowed from ORIGINAL
unit test module, not physical Notion proofs. Detects version compatibility gap.
"""
import json,sys,hashlib,inspect
from pathlib import Path
root=Path(__file__).parent/'source_readonly'/'v081_runtime_readonly'
sys.path.insert(0,str(root))
from fractions import Fraction
from vlab_effects_v08 import Scene,Combatant,apply_weapon_attack,react_defensively,COMBAT_PAGE,VERSION
from vlab_action_catalog_v01 import ActorActionState
from vlab_rd_v08 import Resistances
from test_vlab_effects_v08 import source,evidence,state

def scene():
 s=Scene({'a':Combatant('a',38,22,Fraction(20),10,0,0,6,'A'),
          'b':Combatant('b',38,22,Fraction(20),10,0,0,6,'B')},seed=110,provenance='R10-CONTROLLED-SYNTHETIC-CRIT-NONCANON')
 return s

def example(reaction):
 s=scene(); ev=None
 if reaction:
  sr=source('reaction','REACTION',COMBAT_PAGE,'reaction',0,'SELF',trigger='BEFORE-ATTACK')
  st=ActorActionState('b',1,22,('test-reaction',),reaction_trigger_observed='BEFORE-ATTACK')
  ev=react_defensively(s,'b',kind='ESQUIVAR',attack_score=20,announced_before=True,trigger_source='BEFORE-ATTACK',source=sr,state=st,proofs=(evidence(COMBAT_PAGE,'reaction'),))
  assert ev['damage_negated'] is True and ev['consumes_reaction'] is True
 src=source(); st=state(actor='a',pa=22,known=('test-attack',),enemies=('b',))
 res=apply_weapon_attack(s,'a','b',source=src,state=st,proofs=(evidence(COMBAT_PAGE,'attack'),),roll_score=20,
                         damage=22,damage_tag='impacto',rd=Resistances(general=5),strict=True,defense_event=ev)
 # Controlled 6->6->5 gives critical, and the ordinary hit d6=1 => attack20.
 # Crit damage d6=3 +FOR13+maxdie6 =22 gross, RD5=>17 net.
 assert res['hit'] is False and res['net']==0 and s.actors['b'].hp==38
 return {'synthetic_input':{'hit_d6':1,'raw_attack':20,'crit_3d6':[6,6,5],'damage_d6':3,'crit_gross':22,'rd':5,'defense':26 if reaction else 20,'reaction_predeclared':reaction},
         'master_expected':{'hit':True,'net':17,'after_hp':21},
         'original_native_v081_observed':{'hit':res['hit'],'net':res['net'],'after_hp':s.actors['b'].hp,'defense_negated':res['defense_negated']},
         'discrepancy':'CRITICAL_AUTO_HIT_NOT_PROPAGATED_IN_NATIVE_ADAPTER'}

f=inspect.signature(apply_weapon_attack)
assert 'critical' not in f.parameters and 'critical_hit' not in f.parameters and 'is_critical' not in f.parameters
src=(root/'vlab_effects_v08.py').read_bytes()
out={'status':'CONTROLLED_NATIVE_MODULE_COMPATIBILITY_DEFECT_REPRODUCED','original_engine':VERSION,
     'original_module_sha256':hashlib.sha256(src).hexdigest(),
     'provenance':'R27 historical_v081_verified_original; strict synthetic example with pre-existing fixture proof; no event in R40 files written or replayed',
     'case_no_reaction':example(False),'case_with_predeclared_evasion':example(True),
     'R40_adapter_evidence':{'R40_tape_positive_critical':True,'R40_native_call_lacks_critical_flag':True,
           'R40_auditor_uses': 'hit_bool = score > 20; net = 0 if (not hit_bool or re is not None) else max(0,raw-5)',
           'R40_actual_crit_events':0,
           'R40_replay_affected_by_the_new_decision':'NOT DEMONSTRATED / no positive critical event in 42 original attacks'},
     'integration_gate':'BLOCKED_CRITICAL_AUTO_HIT until official VLAB patch+controlled native source-specific receipt+independent replay/NAC-PASS',
     'canonical_writes':0}
p=Path(__file__).parent/'R10_NATIVE_CRITICAL_GAP.json'
p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'result':out['status'],'sha':out['original_module_sha256'],'reaction_disabled':out['case_no_reaction']['original_native_v081_observed'],
                  'reaction_enabled':out['case_with_predeclared_evasion']['original_native_v081_observed']},ensure_ascii=False))
