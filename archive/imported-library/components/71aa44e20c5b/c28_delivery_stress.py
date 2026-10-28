"""Scenario demonstrations, never battle observations. Source: Selo and Manopla in Mestre Notion."""
from pathlib import Path
import csv,json
OUT=Path(__file__).resolve().parent.parent/'publication'
fixtures=[
('AREA_SAME_EVENT_3_TARGETS','one hostile area effect', [20,60,95], [0,1,2], [20,60,60], 'One same damage occurrence may protect all three if conditions fulfilled'),
('THREE_SEPARATE_HITS','three separate attack events',[20,60,95],[2],[0,0,60],'Seal protects only one identified occurrence, not all hits'),
('THREE_SEPARATE_EQUAL_HITS','three separate attack events',[80,80,80],[0],[60,0,0],'Choosing one hit does not reuse a consumable across others'),
('AREA_LOW_MED_HIGH','one hostile area effect',[0,5,150],[0,1,2],[0,5,60],'Protection does not create healing, leftover remains at high target'),
('TWO_DISTINCT_SOURCES','two distinct effects',[70,70],[0],[60,0],'Protection cannot span effects with distinct provenance'),
('ONE_EVENT_THREE_SMALL','one hostile area effect',[30,30,30],[0,1,2],[30,30,30],'The cap applies per target, not total for the three'),
('ONE_TARGET_HIGH','single hostile hit',[130],[0],[60],'Cap is 60 and remainder remains 70'),
('NON_DAMAGING_CONTROL','hostile control without damage',[0],[],[0],'No trigger for a damaging-effect protection'),
]
r=[]
for id,t,raw,eligible,manual_saved,why in fixtures:
 saved=[min(60,x) if i in eligible else 0 for i,x in enumerate(raw)]
 assert saved==manual_saved
 r.append([id,t,';'.join(map(str,raw)),';'.join(map(str,eligible)),';'.join(map(str,saved)),sum(saved),sum(raw)-sum(saved),why,'HYPOTHETICAL_AFTER_ALL_LEGITIMATE_RD; requires PA55, Reação, targets within 4m, consumable available'])
with (OUT/'C28_SELO_SCOPE_HYPOTHETICAL_EVENT_FIXTURES.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['fixture_id','hostile_event_structure','postRD_per_target','eligible_target_indices_0based','saved_per_target','total_saved','residual_total','contract','limitations']);w.writerows(r)
extra=[]
for good_hits in [1,2,3,4,5,6,8,10]:
 extra.append([good_hits,25.5,25.5/good_hits,22,1,'Assume one successful eligible discharge during a sequence of confirmed melee hits, not hit rate, crit, DPT, or free duplicate charges'])
with (OUT/'C28_MANOPLA_SINGLE_CHARGE_PER_CONFIRMED_HIT_COUNT.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['number_confirmed_eligible_hits_over_window','single_discharge_mean_bonus','mean_bonus_amortized_over_count','one_activation_PA','charges_per_8h','limitations']);w.writerows(extra)
(OUT/'C28_DELIVERY_STRESS_ASSERTIONS.json').write_text(json.dumps({'status':'PASS','count':len(r)+len(extra),'scope':'source-conditioned illustrative logical fixtures, not combat observations','events':len(r),'amortization_cases':len(extra)},ensure_ascii=False,indent=2))
print('Delivered',len(r),'Selo event fixtures and',len(extra),'Manopla resource cases.')
