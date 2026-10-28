#!/usr/bin/env python3
"""DMG C05 exact damage distribution helper. NOT a combat engine, not DMG v2.
Input must be a documented literal formula and its documented attributes.
Unavailable hit probability, PA, crit and target resistances stay indeterminate.
Hypothetical RD is labeled TEST, not source-official.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction
from itertools import product
import re, json, argparse

FORMULA = re.compile(r'^\s*((?:\d+d\d+\s*\+\s*)*\d+d\d+)(?:\s*\+\s*(força|for|des|destreza|int|inteligência|inteligencia|\d+))?\s*$', re.I)
DIE = re.compile(r'(\d+)d(\d+)',re.I)
MAP = {'força':'FOR','for':'FOR','des':'DES','destreza':'DES','int':'INT','inteligência':'INT','inteligencia':'INT'}

def parse_literal(s: str, attributes: dict | None=None):
    match=FORMULA.fullmatch(s)
    if not match: raise ValueError('UNSUPPORTED_OR_INCOMPLETE_FORMULA: '+s)
    ds=[(int(a),int(b)) for a,b in DIE.findall(match.group(1))]
    if not ds or any(a<1 or b<2 or a>100 for a,b in ds):raise ValueError('INVALID_DICE')
    mod=match.group(2); attrs=attributes or {}; attr_code=None; fixed=0
    if mod:
        if mod.isdigit():fixed=int(mod)
        else:
            attr_code=MAP[mod.lower()]
            if attr_code not in attrs or attrs[attr_code] is None or attrs[attr_code]=='':raise ValueError('MISSING_SOURCE_ATTRIBUTE_'+attr_code)
            fixed=int(attrs[attr_code])
    return {'literal':s,'dice':ds,'attribute':attr_code,'fixed':fixed,'die_mean':sum(Fraction(n*(faces+1),2) for n,faces in ds)}

def pmf(literal,attributes=None):
    p=parse_literal(literal,attributes);c=Counter({p['fixed']:1})
    for count,faces in p['dice']:
        for _ in range(count):
            nxt=Counter()
            for x,w in c.items():
                for die in range(1,faces+1):nxt[x+die]+=w
            c=nxt
    total=sum(c.values());assert total==__import__('math').prod(f**n for n,f in p['dice'])
    return {k:Fraction(v,total) for k,v in sorted(c.items())},p

def median_from_dist(d):
    vs=sorted(d);c=Fraction(0)
    def q_at(q):
        cum=Fraction(0)
        for val in vs:
            cum+=d[val]
            if cum>=q:return val
    return (q_at(Fraction(1,2)),q_at(Fraction(1,4)),q_at(Fraction(3,4)))

def metrics(literal,attributes=None,rd=None,hit_probability=None,pa_cost=None,threshold=None):
    d,p=pmf(literal,attributes)
    m,lo,hi=median_from_dist(d)
    mean=sum(Fraction(x)*v for x,v in d.items());variance=sum(v*(x-mean)**2 for x,v in d.items())
    out={'formula':literal,'dice':p['dice'],'attribute_code':p['attribute'],'attribute_value':p['fixed'] if p['attribute'] else None,'fixed_bonus':p['fixed'] if not p['attribute'] else 0,'dice_expected':float(p['die_mean']),'gross_mean':float(mean),'gross_min':min(d),'gross_max':max(d),'gross_median':m,'gross_Q1':lo,'gross_Q3':hi,'gross_variance':float(variance),'dice_fraction_of_gross_mean':float(p['die_mean']/mean) if mean else None,'support_size':len(d),'gross_distribution_exact':[{'damage':x,'numerator':v.numerator,'denominator':v.denominator} for x,v in d.items()]}
    post=None
    if rd is not None:
        if not isinstance(rd,int) or rd<0:raise ValueError('RD_NONNEGATIVE_INTEGER_REQUIRED')
        post=Counter()
        for x,prob in d.items():post[max(0,x-rd)]+=prob
        exp=sum(x*q for x,q in post.items())
        out.update({'rd_input':rd,'rd_status':'DOCUMENTED_ONLY_IF_CALLER_PROVES_TYPE_AND_TARGET_OTHERWISE_TEST','post_rd_expected_on_hit':float(exp),'p_post_rd_positive':float(sum(v for k,v in post.items() if k>0)),'post_rd_exact':[{'damage':x,'numerator':prob.numerator,'denominator':prob.denominator} for x,prob in sorted(post.items())],'rd_prevented_expected':float(mean-exp)})
    else:out['post_rd_expected_on_hit']='INDETERMINATE_MISSING_RD'
    if threshold is not None:
        if not isinstance(threshold,int):raise ValueError('THRESHOLD_INTEGER_REQUIRED')
        out['P_gross_strictly_above_threshold']=float(sum(v for k,v in d.items() if k>threshold))
    if hit_probability is not None:
        if not isinstance(hit_probability,(float,int,Fraction)) or not 0<=hit_probability<=1:raise ValueError('HIT_PROBABILITY_OUTSIDE_0_1')
        out['p_hit_input']=float(hit_probability)
        out['per_attempt_expected']=float(Fraction(str(hit_probability))*(sum(k*v for k,v in post.items()) if post is not None else mean))
        out['precision_scope']='CONDITIONAL_INPUT_NOT_AUTOMATIC_SOURCE_PROOF'
    else:out['per_attempt_expected']='INDETERMINATE_NO_SOURCE_HIT_CHANCE'
    if pa_cost is not None:
        if not isinstance(pa_cost,int) or pa_cost<=0:raise ValueError('PA_POSITIVE_INTEGER_REQUIRED')
        out['pa_cost_input']=pa_cost
        out['per_pa_expected_conditional_on_hit']=float((sum(k*v for k,v in post.items()) if post is not None else mean)/pa_cost)
        out['per_pa_scope']='CONDITIONAL_INPUT_REQUIRES_SOURCE_PROOF'
    else:out['per_pa_expected_conditional_on_hit']='INDETERMINATE_NO_SOURCE_PA_COST'
    return out

def compare(first,second,attributes_a,attributes_b,rd=None):
    A,_=pmf(first,attributes_a);B,_=pmf(second,attributes_b)
    wins=sum(pa*pb for a,pa in A.items() for b,pb in B.items() if (max(0,a-rd) if rd is not None else a)>(max(0,b-rd) if rd is not None else b))
    return {'formula_a':first,'formula_b':second,'rd':rd,'P_A_strictly_greater_than_B':float(wins),'fraction':[wins.numerator,wins.denominator],'assumption':'INDEPENDENT_ROLLS_TEST; SAME_SCALAR_RD_CONDITIONAL; NO_ACCURACY'}

if __name__=='__main__':
 parser=argparse.ArgumentParser()
 parser.add_argument('formula');parser.add_argument('--FOR',type=int);parser.add_argument('--DES',type=int);parser.add_argument('--INT',type=int);parser.add_argument('--RD',type=int);parser.add_argument('--threshold',type=int);parser.add_argument('--PA',type=int);parser.add_argument('--hit-prob',type=float)
 a=parser.parse_args();attrs={k:getattr(a,k) for k in ('FOR','DES','INT')}
 print(json.dumps(metrics(a.formula,attrs,rd=a.RD,threshold=a.threshold,pa_cost=a.PA,hit_probability=a.hit_prob),ensure_ascii=False,indent=2))