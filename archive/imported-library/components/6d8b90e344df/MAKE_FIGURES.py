#!/usr/bin/env python3
"""Original mathematical illustrations of reproducible empirical diagnostic."""
from pathlib import Path
import json
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
r=json.loads((ROOT/'results/DIAGNOSTIC_RESULTS.json').read_text())
V=r['mechanism_experiments'];D=ROOT/'figures';D.mkdir(exist_ok=True)
# Separate chart: post-RD expectations; no palette/style override.
fig,ax=plt.subplots(figsize=(9,5.5))
labels={'SOURCE_LUPUS_P1_2d6_plus25':'Fonte Prata 1: 2d6+25','LAB_EQUAL_MEAN_4d6_plus18':'TEST: 4d6+18 (mesma média)','LAB_ATTR_PLUS5_2d6_plus30':'TEST: 2d6+30 (atributo +5)','LAB_EXTRA_D6_3d6_plus25':'TEST: 3d6+25 (dado +1d6)'}
for key in labels:
 m=V[key]['metrics_by_rd'];xs=[int(k) for k in m];ys=[m[k]['after_rd'] for k in m]
 ax.plot(xs,ys,marker='o',linewidth=1.9,label=labels[key])
ax.set_title('Dano líquido condicional a efeito realizado, por RD (cenários)')
ax.set_xlabel('RD hipotética, aplicável à mesma parcela de dano')
ax.set_ylabel('E[max(0, dano − RD)]')
ax.legend(fontsize=8)
ax.grid(alpha=.25)
fig.tight_layout();fig.savefig(D/'CURVAS_RD_CONTROLADAS.png',dpi=170);plt.close(fig)
fig,ax=plt.subplots(figsize=(8.6,5.3))
names=['Bronze 5 · R02 (9 ações)','Prata 1/5 + Ouro 1 · R03 (6 ações)']
co=r['sample_15_actions']['aggregation'];pairs=[co['R02_Bronze5_candidate'],co['R03_rank_strict']]
attrs=[i['weighted_attribute_fraction']*100 for i in pairs];dice=[100-a for a in attrs]
ax.bar(names,dice,label='DME intrínseco dos dados')
ax.bar(names,attrs,bottom=dice,label='Atributo impresso na fórmula')
ax.set_ylim(0,103);ax.set_ylabel('% da soma das médias brutas no recorte')
ax.set_title('Composição das médias condicionais, amostras selecionadas')
for i,a in enumerate(attrs):ax.annotate(f'{a:.1f}% atributo',xy=(i,dice[i]+a/2),ha='center',va='center',fontsize=9)
ax.legend(loc='lower right');ax.tick_params(axis='x',labelsize=8)
fig.tight_layout();fig.savefig(D/'PESO_DOS_ATRIBUTOS.png',dpi=170);plt.close(fig)
print('figs',*[p.name for p in D.glob('*.png')])
