"""Read-only experimental metrics derived from independently checked SQLite fight banks."""
from __future__ import annotations
import json,collections,statistics,pathlib
from r200_read_only_audit import audit_one
ROOT=pathlib.Path(__file__).resolve().parents[1]
res=json.loads((ROOT/'evidence/R200_EXECUTED_FIGHTS.json').read_text())
verified={x['id']:audit_one(ROOT/'evidence/db'/x['db']) for x in res if x['db']}
assert len(verified)==30
summ={}
for level in (1,6):
    for policy in ('SEM_MAGIA_ITEM','COM_MAGIA_ITEM_PROXY_UNRANKED_TEST'):
        g=[r for r in res if r['level']==level and r['policy']==policy]
        completed=[r for r in g if r['db']]
        actor=f'ED-REF-01-{"B1" if level==1 else "P1"}'
        enemy='GALINHA_B1' if level==1 else 'LOBO_P1'
        o={'attempts':len(g),'physical_fights':len(completed),'terminal_KO':sum(r['status']=='FINISHED' for r in completed),
           'precommit_ties':sum(r['status']=='PRECOMMIT_TIE_HOLD' for r in g),
           'censored':sum(r['status']=='CENSORED_HORIZON' for r in completed),
           'ed_wins':sum(r.get('winner')==actor for r in completed),'enemy_wins':sum(r.get('winner')==enemy for r in completed),
           'mean_rounds_all_executed':round(statistics.mean(r['rounds'] for r in completed),2),
           'attacks':sum(verified[r['id']]['attacks'] for r in completed),
           'hp_removed_by_ed':sum(verified[r['id']]['damage_by_actor'].get(actor,0) for r in completed),
           'hp_removed_by_enemy':sum(verified[r['id']]['damage_by_actor'].get(enemy,0) for r in completed),
           'ed_hits':sum(verified[r['id']]['hits_by_actor'].get(actor,0) for r in completed),
           'enemy_hits':sum(verified[r['id']]['hits_by_actor'].get(enemy,0) for r in completed),
           'ring_proxy_pa_at_entry_total':13*len(completed) if policy!='SEM_MAGIA_ITEM' else 0,
           'ring_proxy_source_grade':'UNPUBLISHED_NOT_RANK_CERTIFIED'}
        summ[f'{level}|{policy}']=o
paired={}
for level in (1,6):
    actor=f'ED-REF-01-{"B1" if level==1 else "P1"}'
    data=[]
    for seed in range(20021001,20021009):
        a=next(r for r in res if r['seed']==seed and r['level']==level and r['policy']=='SEM_MAGIA_ITEM')
        b=next(r for r in res if r['seed']==seed and r['level']==level and r['policy']!='SEM_MAGIA_ITEM')
        data.append({'seed':seed,'sem':a['status'],'com':b['status'],'winner_sem':a.get('winner'),'winner_com':b.get('winner'),
                     'ed_win_improved':a.get('winner')!=actor and b.get('winner')==actor,
                     'ed_hp_end_diff':(b['final_hp'][actor]-a['final_hp'][actor]) if a.get('db') and b.get('db') else None})
    paired[str(level)]={'seed_blocks':len(data),'both_executed':sum(x['ed_hp_end_diff'] is not None for x in data),
                         'observable_ed_win_flips':sum(x['ed_win_improved'] for x in data),'by_seed':data}
out={'scope':'R200_ED_REF_01_TEST_NEW_GEAR_PHYSICAL_MAGIC_PROXY_UNRANKED','sources':['https://app.notion.com/p/3ebc2b324ede81449222f3c06b840613','https://app.notion.com/p/eddc2b324ede829f8a75011e8acbf429','https://app.notion.com/p/be5c2b324ede832e8b7a81c5460571c1','https://app.notion.com/p/168c2b324ede82d6b8ce013ec82217ad'],
     'group_metrics':summ,'paired':paired,'unit_distinction':'8 seeds per rank, 2 policies per seed; 30 physical fights with 2 precommit ties. Never 32 independent seeds.',
     'scientific_diagnosis':{'bronze':'+2 CA proxy improved observed ED B1 wins in 3/7 completed pairs; cast status not evidence of legal Bronze item rank; winner comparisons seed-conditional',
       'prata':'2/8 Lobo KOs without proxy, 0/8 with proxy but all proxy fights censored: NOT a win improvement claim',
       'prata_offense':'REF P1 2d6+22 <= CA34 Lobo on all ordinary rolls; only conditional critical can hit. Low offense/scope issue, not universal weakness or rank certification'},
     'official_cells_certified':0,'contracts_terminal':0}
(ROOT/'evidence/R200_BENCHMARK_FROM_RECEIPTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps({'levels':list(summ.keys()),'paired_improvements':{k:v['observable_ed_win_flips'] for k,v in paired.items()},'phys_fights':sum(v['physical_fights'] for v in summ.values())},ensure_ascii=False))
