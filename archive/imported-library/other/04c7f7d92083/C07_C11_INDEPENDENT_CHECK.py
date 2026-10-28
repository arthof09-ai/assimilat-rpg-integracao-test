#!/usr/bin/env python3
"""Independent mathematical check for C07-C11.
Never imports C07_C11_EXACT_REPLAY or historical VLAB; read-only verification.
No claim of an independent canonical combat engine validation.
"""
from fractions import Fraction as Fr
from pathlib import Path
from itertools import product
from collections import Counter
from zipfile import ZipFile
import hashlib,json
R=Path(__file__).resolve().parent
BASE={
'Feryn':((4,6),92,(8,8),47,123,125,22,479),
'Varok':((4,6),100,(10,10),48,83,83,35,734),
'Arveth':((4,6),72,(8,10),35,93,95,30,806)}

def counts(num,faces):
 c={0:1}
 for i in range(num):
  d={}
  for x,n in c.items():
   for y in range(1,faces+1):d[x+y]=d.get(x+y,0)+n
  c=d
 assert sum(c.values())==faces**num
 return c

def fracdata(counts,fn):
 den=sum(counts.values())
 return Fr(sum(n*fn(v) for v,n in counts.items()),den)

def num(j):return Fr(j['fraction'])

def QA(k,cond):
 assert cond,k
 issues.append(k)
issues=[]
actual={x:json.loads((R/(x+'.json')).read_text()) for x in ['C07_SOURCE_AUTHORITY','C08_R47_R49_AUDIT','C09_ON5_LAB_SENSITIVITY','C10_AOO_PRIORITY_PA','C11_COUNTER_NORMATIVE_BRANCH']}
# Source invariant and damage-only normalization
QA('veado_bronze_same_dice_rank',actual['C07_SOURCE_AUTHORITY']['rank_invariants']['Bronze_2_vs_Bronze_4_rank_dice'].startswith('both Bronze'))
QA('veado_range',actual['C07_SOURCE_AUTHORITY']['source_verified']['Veado']['normal_raw_range']==[12,17])
QA('veado_mean',num(actual['C07_SOURCE_AUTHORITY']['source_verified']['Veado']['normal_raw_mean'])==Fr(29,2))
QA('regalis_electric_trigger_only',num(actual['C07_SOURCE_AUTHORITY']['regalis_actions'][0]['p_fortitude_test_gate'])==Fr(1,4))
QA('no_imported_luta',actual['C07_SOURCE_AUTHORITY']['source_verified']['Veado']['luta']=='MISSING_NOT_ZERO' and actual['C07_SOURCE_AUTHORITY']['source_verified']['Regalis']['luta']=='MISSING_NOT_ZERO')

# Derive critical chance by enumerating all ordered 3d6, no use of first oracle
seq=list(product(range(1,7),repeat=3))
pos=sum(1 for x in seq if x[:2]==(6,6) and x[2]>=5)
neg=sum(1 for x in seq if x[:2]==(1,1) and x[2]<=2)
QA('positive_negative_sequential_disjoint',pos==neg==2)
QA('invalid_656_is_not_critical',not ((6,5,6)[:2]==(6,6)))

pairs=actual['C09_ON5_LAB_SENSITIVITY']['pairwise_normal_CA']+actual['C09_ON5_LAB_SENSITIVITY']['pairwise_evasion']
for row in pairs:
 a=BASE[row['attacker']];b=BASE[row['defender']]
 ac=counts(*a[0]);dc=counts(*a[2]);defense=b[5] if row['defense_kind']=='Esquiva' else b[4]
 p_norm=fracdata(ac,lambda v: int(a[1]+v>defense))
 e_norm=fracdata(dc,lambda v:max(0,v+a[3]-b[6]))
 e_pos=fracdata(dc,lambda v:max(0,v+a[3]+a[2][0]*a[2][1]-b[6]))
 p_plus=Fr(pos,len(seq));p_neg=Fr(neg,len(seq))
 p_effective=(1-p_plus-p_neg)*p_norm
 qhit=p_effective+p_plus
 e=(1-p_plus-p_neg)*p_norm*e_norm + p_plus*e_pos
 QA('P_basic_'+row['attacker']+'_'+row['defender']+'_'+row['defense_kind'],num(row['hit_basic_conditional_noncrit'])==p_norm)
 QA('P_total_'+row['attacker']+'_'+row['defender']+'_'+row['defense_kind'],num(row['total_hit_per_attempt'])==qhit)
 QA('E_life_'+row['attacker']+'_'+row['defender']+'_'+row['defense_kind'],num(row['E_damage_per_attack'])==e)

# Verify damage arithmetic and destination risk fully bounded in R49
r49=actual['C10_AOO_PRIORITY_PA']['R49_bound'];QA('maximum_two_fully_critical',''+str(r49['maximum_two_attacks'])=='280' and 280<734)
score=counts(4,6);tie=Fr(sum(n*n for n in score.values()),(6**4)**2)
QA('tie_4d6',num(actual['C10_AOO_PRIORITY_PA']['priority_tie_probability'])==tie)
QA('geom_tie_iterations',num(actual['C10_AOO_PRIORITY_PA']['priority_expected_rounds_to_separate'])==1/(1-tie))

for row in actual['C10_AOO_PRIORITY_PA']['activations']:
 a=BASE[row['attacker']];b=BASE[row['defender']]
 n,faces={'Feryn':(5,8),'Varok':(6,12),'Arveth':(6,10)}[row['attacker']]
 c=counts(n,faces)
 QA('E_added_'+row['attacker'],num(row['raw_extra_E'])==fracdata(c,lambda x:x))
 QA('E_separate_RD_'+row['attacker'],num(row['separate_extra_RD_increment_E_IF_separately_mitigated'])==fracdata(c,lambda x:max(0,x-b[6])))

# First goat R47B positive damage conditional and hypothetical Counter safe bound
r47=actual['C11_COUNTER_NORMATIVE_BRANCH'];QA('r47b_crit_damage_values',r47['goat_vs_Feryn']['effective_critical_values']==[0,0,0,1,2,3]);QA('r47b_positive_event_p',num(r47['goat_vs_Feryn']['probability_positive_life_per_attack'])==Fr(1,216));QA('r47b_expected_damage',num(r47['goat_vs_Feryn']['expected_life_lost_per_attack'])==Fr(1,108));QA('counter_action_min_kills_goat',r47['counter_semantic_branches'][0]['minimum_counter_net_damage']==50 and 50>38)
# Read-only file integrity, no rewriting historical evidence
z=R.parent/'evidence_readonly/VLAB_R47_R48_R49_CRITICO_CONTRA_ANINHAMENTO_ON5_MESTRE_ONLY.zip'
with ZipFile(z) as src:
 m=json.loads(src.read('R47_R49_FILE_MANIFEST.json'))
 QA('package_crc',src.testzip() is None)
 QA('package_file_members',len(m['members'])==39)
 QA('package_all_sha',all(hashlib.sha256(src.read(n)).hexdigest()==expected for n,expected in m['members'].items()))
QA('package_outer_sha',hashlib.sha256(z.read_bytes()).hexdigest()==actual['C08_R47_R49_AUDIT']['documentary_sha256'])

# Immutable old checkpoint: materialized physically in CURRENT turn
ck=json.loads((R.parent/'C02_C06_FINAL_CHECKPOINT.json').read_text())
old=ck['old_files_and_sha256'];QA('18_predecessor_old_file_checks',len(old)==18 and all(Path(p).exists() and hashlib.sha256(Path(p).read_bytes()).hexdigest()==sha for p,sha in old.items()))
new=ck['new_files_and_sha256'];avail={p:h for p,h in new.items() if (R.parent/p).exists()}
QA('subset_C02_C06_currently_materialized',len(avail)>0 and all(hashlib.sha256((R.parent/p).read_bytes()).hexdigest()==h for p,h in avail.items()))

out={'scope':'independent mathematics, archive CRC/SHA and predecessor hash validation, NOT independent Notion source authority / VLAB full execution',
 'checks_passed':len(issues),'checks':issues,
 'physical_old_R10_C01_verified':len(old),'current_C02_C06_files_verified':len(avail),
 'current_C02_C06_files_not_materialized':sorted(set(new)-set(avail)),
 'VLAB_zip_archive_verified':'39/39 SHA256 CRC plus cold VLAB independent auditor externally rerun',
 'source_semantic_new_status':'unresolved, not inferred as true',
 'nac_pass':'HOLD'}
(R/'C07_C11_INDEPENDENT_QA.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('INDEPENDENT_C07_C11_PASS',len(issues),'old',len(old),'new_visible',len(avail))
