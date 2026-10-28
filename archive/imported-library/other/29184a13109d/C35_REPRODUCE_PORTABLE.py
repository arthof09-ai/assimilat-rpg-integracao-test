#!/usr/bin/env python3
"""DMG C35 independent portable replay. No Notion API, no gameplay writer."""
from pathlib import Path
from fractions import Fraction as F
import csv,re,math
ROOT=Path(__file__).parent
dpath=ROOT/"C35_DOZE_SALVAGUARDA_DOT_150_CENARIOS.csv"
tpath=ROOT/"C35_TREIMOR_CONDICIONAL_VARIANCIAS.csv"
tables={}
with dpath.open(encoding="utf-8",newline="") as f:
    rows=list(csv.DictReader(f))
assert len(rows)==150
checks=0
for r in rows:
    key=(r["versao"],int(r["INT_hipotetica"]),F(r["P_sucesso_Fortitude_hipotetica"]),int(r["ticks_falha_hipoteticos"]))
    b,i,p,t=key
    mu=F(r["media_base_bruta"]);tick=F(r["media_tick_condicional"]);e=F(r["E_total_condicional_sem_RD"])
    expect=(1-p/2)*mu+(1-p)*tick*t
    assert e==expect and e>=0;checks+=1
    if t<4:
        assert e<=(1-p/2)*mu+(1-p)*tick*(t+1);checks+=1
    if p<1:
        q=p+F(1,4)
        assert e>=(1-q/2)*mu+(1-q)*tick*t;checks+=1
    tables[key]=e
assert checks==390
for I in [0,20]:
    for p4 in range(5):
        p=F(p4,4)
        for t in range(5):
            assert tables[("O5_O2_alternativa_d8",I,p,t)]-tables[("O5_O2_alternativa_d6",I,p,t)]==9*(1-p/2)
            checks+=1
assert checks==440
with tpath.open(encoding="utf-8",newline="") as f:
    rows=list(csv.DictReader(f))
assert len(rows)==8
moments={}
for r in rows:
    m=F(int(r["bonus_fixo"]));v=F(0)
    for part in r["dados"].split("+"):
        n,s=map(int,re.fullmatch(r"(\d+)d(\d+)",part).groups())
        m+=F(n*(s+1),2)
        v+=F(n*(s*s-1),12)
    assert m==F(r["media_condicional"]) and v==F(r["variancia_condicional"])
    moments[r["versao_documental"],r["habilidade"],r["anotacao"]]=(m,v)
    checks+=1
assert checks==448
assert moments["normal","Ataque","entre_parenteses"]==(F(142),F(87))
assert moments["transformado","Ataque","entre_parenteses"]==(F(355,2),F(249,4))
assert moments["normal","Pressao","entre_parenteses"][0]==193
assert moments["transformado","Pressao","entre_parenteses"][0]==245
print("C35 PORTABLE REPLAY: 150 scenarios / 8 expressions / 448 CHECKS PASS; no canonical effects asserted")
