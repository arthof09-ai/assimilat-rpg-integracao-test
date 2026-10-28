"""Independent read-only causal decomposer of R95 attack receipts, no combat replay.
Only standard library; does not alter signed R95 ledgers.
"""
import csv,json,collections,hashlib,math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OLD=ROOT.parent/'r92_r101'
rows=list(csv.DictReader((OLD/'R97_ATTACK_RECEIPTS_1344_FOR_DMG.csv').open()))
r95=[r for r in rows if r['cohort']=='R95_BASIC_FIXED_OPENING']
assert len(r95)==892
runs=collections.defaultdict(list)
for r in r95:
    runs[r['run_id']].append(r)
assert len(runs)==16 and len(set((r['matchup'],r['seed']) for r in r95))==8
summary=[]
crit=[]
for rid,arr in sorted(runs.items()):
    B=[x for x in arr if x['actor']=='B'];E=[x for x in arr if x['actor']=='E']
    assert all(x['hit']=='1' for x in E)
    assert all(x['hit']==x['crit_plus'] for x in B)
    for x in arr:
        assert int(x['raw']) >= 0
        assert int(x['net_potential']) == max(0,int(x['raw'])-int(x['rd'])) if x['hit']=='1' else int(x['net_potential'])==0
        assert int(x['hp_loss_actual'])==min(int(x['hp_before']),int(x['net_potential']))
        assert int(x['hp_before'])-int(x['hp_loss_actual'])==int(x['hp_after'])
        if x['crit_plus']=='1':
            groups=json.loads(x['dice'])
            max_of_all=sum(n*f for n,f in groups)
            max_face=max(f for n,f in groups)
            assert x['actor']=='B' and x['matchup'].startswith('R95-GRIFO')
            normalized_raw=int(x['raw'])-max_face+max_of_all
            normalized_net=max(0,normalized_raw-int(x['rd']))
            normalized_actual=min(int(x['hp_before']),normalized_net)
            crit.append({'run_id':rid,'seed':int(x['seed']),'opening':x['matchup'],'side':x['side'],
                         'historic_raw':int(x['raw']),'historic_net':int(x['net_potential']),
                         'historic_hp_loss':int(x['hp_loss_actual']),
                         'current_combat_rule_critical_bonus':max_of_all,
                         'r95_adapter_critical_bonus':max_face,'delta_raw':max_of_all-max_face,
                         'counterfactual_single_event_raw':normalized_raw,
                         'counterfactual_single_event_net':normalized_net,
                         'counterfactual_single_event_hp_loss':normalized_actual,
                         'counterfactual_hp_after_event':int(x['hp_before'])-normalized_actual})
    summary.append({'run_id':rid,'species':'GRIFO' if 'GRIFO' in arr[0]['matchup'] else 'CROCO',
                    'opening':arr[0]['matchup'].rsplit('-',1)[1], 'seed':int(arr[0]['seed']),
                    'side':arr[0]['side'], 'attacks_B':len(B),'hits_B':sum(x['hit']=='1' for x in B),
                    'attacks_E':len(E),'hits_E':len(E),
                    'hp_E_end_from_attack_trace':B[-1]['hp_after'] if B else None,
                    'hp_B_end_from_attack_trace':E[-1]['hp_after'] if E else None,
                    'raw_by_E':sum(int(x['raw']) for x in E),
                    'rd_applied_E':sum(int(x['rd']) for x in E if x['hit']=='1'),
                    'actual_hp_loss_E':sum(int(x['hp_loss_actual']) for x in E),
                    'actual_hp_loss_B':sum(int(x['hp_loss_actual']) for x in B)})
assert len(crit)==4 and len({x['seed'] for x in crit})==1
assert all(c['historic_raw']==104 and c['counterfactual_single_event_raw']==294 for c in crit)
assert all(c['historic_hp_loss']==69 and c['counterfactual_single_event_hp_loss']==259 for c in crit)
res={'source_sha256':hashlib.sha256((OLD/'R97_ATTACK_RECEIPTS_1344_FOR_DMG.csv').read_bytes()).hexdigest(),
     'scope':'R95 READ_ONLY; NOT A COUNTERFACTUAL COMBAT EXECUTION',
     'denominator':{'r95_runs':len(runs),'mirrored_matchup_seed_pairs':8,'distinct_seed_values':2,'distinct_species':2,
                    'independent_random_families':2,'attacks':len(r95),'attacks_auren':448,'attacks_beasts':444},
     'hits':{'auren':448,'beasts':4,'beast_hits_positive_crit_only':4,'crit_unique_seed_values':1},
     'original':{'auren_min_numeric_attack':199,'grifo_max_numeric_attack':174,'croco_max_numeric_attack':170,
                 'auren_ca':225,'grifo_ca':153,'croco_ca':112,
                 'auren_physical_rd':35,'beasts_physical_rd':75,'auren_mean_normal_raw':247,
                 'auren_mean_on_hit_after_beast_rd':172,'grifo_hp':4315,'croco_hp':5580,
                 'grifo_extra_hp_to_croco':1265,'extra_hits_at_auren_mean_damage':1265/172},
     'critical_normative_delta':{'current_rule':'NORMAL_DAMAGE_DICE + FIXED_BONUS + SUM_OF_MAXIMA_FOR_ALL_DICE',
                                 'r95_adapter_used':'NORMAL_DAMAGE_DICE + FIXED_BONUS + MAX_FACE',
                                 'unreconciled_r95_source_legality':'HOLD',
                                 'observed_critical_events':crit},
     'additional_normative_gaps':['FRACO below10percent not applied to attacks or movement in R95',
                                  'Gold+ Besta final effort when below10percent not represented',
                                  'Natural initiative training not evidenced, opening exogenous',
                                  'Static contact, no declared reactions, no special abilities'],
     'descriptive_run_table':summary,
     'conclusion':'R95 full-state audit proved faithful replay of restricted adapter, not full parity with current Combat critical or low HP mechanics; original ledgers MUST remain unmodified.'}
(ROOT/'R102_CAUSAL_R95_READONLY.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in res.items() if k not in ('descriptive_run_table','critical_normative_delta')},ensure_ascii=False,indent=2)[:4600])
print('GRIFO B end', sorted(set(v['hp_B_end_from_attack_trace'] for v in summary if v['species']=='GRIFO')))
print('CROCO B end', sorted(set(v['hp_B_end_from_attack_trace'] for v in summary if v['species']=='CROCO')))
print('B total actual',sum(v['actual_hp_loss_B'] for v in summary))
