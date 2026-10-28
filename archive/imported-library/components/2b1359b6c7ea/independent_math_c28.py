#!/usr/bin/env python3
"""Second arithmetic technique: numpy polynomial convolution, crosscheck all C28 source tables.
Not an independent researcher or documentary recoding.
"""
import numpy as np,csv,json,re
from pathlib import Path
from fractions import Fraction
out=Path(__file__).resolve().parent.parent/'publication'

def polynomial(expr):
  txt=expr.replace(' ','')
  parts=re.findall(r'(\d+)d(\d+)',txt,re.I)
  replaced=re.sub(r'\d+d\d+','',txt,flags=re.I)
  constant=sum(map(int,re.findall(r'\d+',replaced))) if replaced else 0
  p=np.array([1],dtype=object)
  for cnt,faces in parts:
    die=np.r_[0,np.ones(int(faces),dtype=object)]
    for _ in range(int(cnt)): p=np.convolve(p,die)
  p=np.r_[np.zeros(constant,dtype=object),p]
  return p
checks=[]
def check(name,a,b):
 if a!=b:raise AssertionError(f'{name}: {a!r} vs {b!r}')
 checks.append(name)
# Read builder outputs as values, while applying wholly separate convolution code.
for line in csv.DictReader((out/'C28_PHYSICAL_RDF_SELO_10_CONDITIONAL_FIXTURES.csv').open()):
 p=polynomial(line['attack_expr']);n=np.arange(len(p),dtype=object);rd=int(line['RDF']);total=int(sum(p))
 before=Fraction(sum(int(c)*max(0,int(i)-rd) for i,c in enumerate(p) if c),total)
 after=Fraction(sum(int(c)*max(0,int(i)-rd-60) for i,c in enumerate(p) if c),total)
 probability=Fraction(sum(int(c) for i,c in enumerate(p) if int(i)-rd>60),total)
 check(line['effect_id']+':'+str(rd)+':before',str(before),line['before_fraction'])
 check(line['effect_id']+':'+str(rd)+':after',str(after),line['after_fraction'])
 check(line['effect_id']+':'+str(rd)+':saved',str(before-after),line['prevented_fraction'])
 check(line['effect_id']+':'+str(rd)+':probability',str(probability),line['residual_prob_fraction'])
for line in csv.DictReader((out/'C28_MANOPLA_ELECTRIC_RESISTANCE_THRESHOLDS.csv').open()):
 p=polynomial('5d8+3');r=int(line['hypothetical_Raio_resistance']);total=int(sum(p))
 avg=Fraction(sum(int(c)*max(0,int(i)-r) for i,c in enumerate(p) if c),total)
 chance=Fraction(sum(int(c) for i,c in enumerate(p) if i>r),total)
 check('Electric:'+str(r)+':expectation',str(avg),line['exact_mean_fraction'])
 check('Electric:'+str(r)+':chance',str(chance),line['exact_probability_fraction'])
for line in csv.DictReader((out/'C28_LEGACY_MULTIEFFECT_DECOMPOSITION.csv').open()):
 p=polynomial(line['formula']);total=int(sum(p));avg=Fraction(sum(i*int(c) for i,c in enumerate(p)),total)
 check('legacy:'+line['effect_id']+':min',next(i for i,c in enumerate(p) if c>0),int(line['min']))
 check('legacy:'+line['effect_id']+':max',len(p)-1-next(i for i,c in enumerate(p[::-1]) if c>0),int(line['max']))
 check('legacy:'+line['effect_id']+':mean',float(avg),float(line['mean']))
result={'check_count':len(checks),'passed':len(checks),'backend':'numpy integer polynomial convolution (independent math implementation), corroborates tables not Notion transcription','checks':checks}
(out/'C28_SECOND_ALGORITHM_AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(result['check_count'],'second algorithm checks PASS')
