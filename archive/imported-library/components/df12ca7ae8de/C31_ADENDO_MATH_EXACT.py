"""C31 READ-ONLY TEST: exact conditional damage after hypothetical flat reduction.
No assumptions about defender, elemental eligibility, action, attack hit, or canon.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import json,re

FORMULAS = {
 "Ravin_front":"2d6+37",
 "Ravin_parenthetical":"7d6+20",
 "Onopio_text":"1d8+4d6+16"
}
FLAT_RD=(0,35,40,45,50,55)
DICE=re.compile(r'(?P<n>[1-9][0-9]*)d(?P<f>[2-9][0-9]*)$')

def parse(text):
 terms=text.split('+');out=[];fixed=0
 for term in terms:
  if re.fullmatch('[0-9]+',term):fixed+=int(term)
  elif (m:=DICE.fullmatch(term)):
   count,faces=int(m['n']),int(m['f']);
   if count>12 or faces>100: raise ValueError('input bound')
   out.extend([faces]*count)
  else: raise ValueError('unsupported expression')
 return out,fixed

def convolution(text):
 dice,fixed=parse(text);counts=Counter({fixed:1})
 for face in dice:
  nxt=Counter()
  for subtotal,c in counts.items():
   for d in range(1,face+1):nxt[subtotal+d]+=c
  counts=nxt
 return counts

def enumeration(text):
 dice,fixed=parse(text)
 return Counter(sum(faces)+fixed for faces in product(*(range(1,face+1) for face in dice)))

def stats(dist,rd):
 n=sum(dist.values());mean=Fraction(sum(value*cnt for value,cnt in dist.items()),n)
 net=Fraction(sum(max(0,value-rd)*cnt for value,cnt in dist.items()),n)
 positive=Fraction(sum(cnt for value,cnt in dist.items() if value>rd),n)
 return {'rd_assumed':rd,'total_outcomes':n,'raw_expected':str(mean),'expected_post_rd':str(net),'expected_post_rd_decimal':round(float(net),7),'probability_post_rd_positive':str(positive),'probability_post_rd_positive_decimal':round(float(positive),7),'distribution_support_min':min(dist),'distribution_support_max':max(dist)}

def generate():
 result={'classification':'TEST_MATH_ONLY','purpose':'Show equal-ish raw averages can conceal different distribution and defensive sensitivity','sources':{'Ravin':'https://app.notion.com/p/14bc2b324ede834daba501e769feda9d','Onopio':'https://app.notion.com/p/2ebc2b324ede82cfbd1c81b7a2107bb9'},'no_permission_to_pair_specific_defender':True,'damage_type_action_hit_probability_control_FIP_RE':'UNKNOWN_NOT_ASSUMED','scenarios':[]}
 for k,formula in FORMULAS.items():
  conv=convolution(formula)
  en=enumeration(formula)
  if conv!=en:raise AssertionError(f'INDEPENDENT_METHODS_FAIL_{k}')
  assert sum(conv.values())==sum(en.values())
  result['scenarios'].append({'key':k,'source_expression_literal':formula,'exact_enumeration_equals_convolution':True,'conditionals':[stats(conv,rd) for rd in FLAT_RD]})
 result['scenarios_count']=len(FORMULAS)*len(FLAT_RD)
 result['source_interpretation']='Ravin text includes parenthetical alternative; only one formula per scenario. Onopio has own separate recorded attack; not combining characters. No actual target with proven RD was paired.'
 return result

if __name__=='__main__':
 p=Path(__file__).parent/'C31_ADENDO_DISTRIBUTION_18_HYPOTHETICAL_RD.json'
 r=generate();p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 for item in r['scenarios']:
  print(item['key'],item['source_expression_literal'], [(x['rd_assumed'],x['expected_post_rd_decimal'],x['probability_post_rd_positive_decimal']) for x in item['conditionals']])
 print('PASS',r['scenarios_count'],'SCENARIOS',len(r['scenarios']),'FORMULAS','INDEPENDENT CONVOLUTION ENUMERATION')
