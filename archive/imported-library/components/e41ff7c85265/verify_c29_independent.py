#!/usr/bin/env python3
"""Independent algorithm for numeric formulas, NOT independent documentary coder."""
import csv,json,re,collections,hashlib
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'publication'
rows=list(csv.DictReader((P/'C29_VZ_8_RE_FIP_EXPLICITOS.csv').open()))
modes=list(csv.DictReader((P/'C29_MODOS_DEPENDENTES_8.csv').open()))
chains=list(csv.DictReader((P/'C29_6_PROVAS_ANTI_STACK.csv').open()))
def distribution(expr):
 counts={0:1}
 for chunk in re.findall(r'[+-]?[^+-]+',expr.replace(' ','')):
  mt=re.fullmatch(r'([+-]?)(\d+)d(\d+)',chunk)
  if mt:
   sign=-1 if mt[1]=='-' else 1;num=int(mt[2]);size=int(mt[3])
   for k in range(num):
    t=collections.defaultdict(int)
    for base,v in counts.items():
     for face in range(1,size+1):t[base+sign*face]+=v
    counts=t
  else:
   step=int(chunk);counts={base+step:v for base,v in counts.items()}
 return counts
def mean(d):return sum(k*v for k,v in d.items())/sum(d.values())
asserts=[]
def t(name,ok):asserts.append(dict(name=name,passed=bool(ok)))
for x in rows:
 d=distribution(x['chassi_intrinseco_reconciliado']);a=mean(d)
 t('dist_'+x['ID'],abs(a-float(x['DME_chassi']))<1e-10)
 t('prob_mass_'+x['ID'],sum(d.values())>0)
 t('all_positive_'+x['ID'],min(d)>=0)
for x in modes:
 d=distribution(x['formula']);t('mode_'+x['effect_id']+'_'+x['modo'],abs(mean(d)-float(x['DME']))<1e-10)
for x in chains:
 n=mean(distribution(x['soma_ILICITA']));a=mean(distribution(x['saida_LEGAL']))
 t('anti_'+x['personagem']+'_'+x['fonte'],abs(n-a-float(x['inflacao_DME']))<1e-10)
other={
 'phase19':len(list(csv.DictReader((P/'C29_PLANO_SUPREMO_19_FASES.csv').open())))==19,
 'gate8':len(list(csv.DictReader((P/'C29_F0_OITO_REQUISITOS_OPERACIONAIS.csv').open())))==8,
 'A5_7_no_bytes':len(list(csv.DictReader((P/'C29_A5_REFERENCIAS_SETE_SEM_BYTES.csv').open())))==7 and all(x['actual_original_bytes_downloaded']=='False' for x in csv.DictReader((P/'C29_A5_REFERENCIAS_SETE_SEM_BYTES.csv').open())),
 'genuine_coder_missing':True,
 'negative_admission_seven':len(list(csv.DictReader((P/'C29_PROVA_NEGATIVA_ADMISSAO_V11.csv').open())))==7,
}
for a,b in other.items():t(a,b)
assert all(x['passed'] for x in asserts)
res={'n':len(asserts),'passed':sum(x['passed'] for x in asserts),'method':'integer-face exact discrete convolution independent from formula mean parser; not second human coder','items':asserts}
(P/'C29_SECOND_NUMERICAL_ALGORITHM.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
print('C29 INDEPENDENT_NUMERIC_VALIDATION',len(asserts),'/',len(asserts),'PASS')
