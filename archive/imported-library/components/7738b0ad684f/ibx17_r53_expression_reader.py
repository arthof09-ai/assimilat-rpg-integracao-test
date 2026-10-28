"""Aditivo source-bound experimental: validate annotated equations without editing.
Handles 19+3(aprimoramento)+15 (armadura)=50, which earlier simple regex missed.
No rule creation, writes, data inference or unconditional item application.
"""
import re
from dataclasses import dataclass,asdict

@dataclass(frozen=True)
class Equation:
    attr:str
    terms:tuple
    published:int
    computed:int
    delta:int
    evidence:str
    kind:str='ANNOTATED_SOURCE_EQUATION'

PAT=re.compile(r'(?P<attr>Força|Destreza|Constituição|Inteligência|Sabedoria|Carisma)\s*:\s*'
   r'(?P<expr>\d+(?:\s*\+\s*\d+\s*(?:\([^)]*\))?)*\s*=\s*\d+)',re.I)

def parse_annotated_equations(markdown:str):
    if not isinstance(markdown,str):raise ValueError('INVALID_SOURCE')
    r=[]
    clean=markdown.replace('<br>','\n').replace('<br/>','\n')
    # Case of Destreza annotated equation. Some multiline Notion renderers split.
    for line in markdown.splitlines():
        for m in PAT.finditer(line):
            e=m.group('expr')
            parts=re.split(r'=',e)
            lhs,rhs=parts[0],parts[1]
            vals=tuple(map(int,re.findall(r'(?:^|\+)\s*(\d+)',lhs)))
            if len(vals)<2:continue
            shown=int(rhs.strip());actual=sum(vals)
            r.append(asdict(Equation(m.group('attr'),vals,shown,actual,shown-actual,m.group(0))))
    return r

def separate_item_bonus(natural,mentioned_bonus,*,equipped,already_in_total):
    if not isinstance(natural,int) or not isinstance(mentioned_bonus,int):raise ValueError('NOT_NUMERIC')
    if equipped is None or already_in_total is None:return {'status':'HOLD_APPLICABILITY_UNKNOWN'}
    if not equipped:return {'status':'NOT_APPLICABLE','natural':natural,'applied':0}
    return {'status':'APPLICABLE_ALREADY_COUNTED' if already_in_total else 'APPLICABLE_NOT_COUNTED',
            'natural':natural,'applied':mentioned_bonus,
            'computed_total':natural+mentioned_bonus,
            'should_add_again':False if already_in_total else True}
