"""Read-only all 1344 R97 attack receipts, current System-of-Combat critical gate."""
import csv,hashlib,json,collections
from pathlib import Path
R=Path(__file__).resolve().parent
P=R.parent/'r92_r101'/'R97_ATTACK_RECEIPTS_1344_FOR_DMG.csv'
rows=list(csv.DictReader(P.open()))
assert len(rows)==1344
crits=[]
for r in rows:
 if r['crit_plus']!='1':continue
 dice=json.loads(r['dice']);old=max(f for n,f in dice);expected=sum(n*f for n,f in dice)
 assert expected>old
 oldraw=int(r['raw']);current=oldraw-old+expected
 rd=int(r['rd']);potential=max(0,current-rd);actual=min(int(r['hp_before']),potential)
 crits.append({'run_id':r['run_id'],'cohort':r['cohort'],'seed':int(r['seed']),'side':r['side'],'attacker':r['actor'],
               'history_raw':oldraw,'required_max_all_dice':expected,'adapter_added_max_face':old,
               'missing_bonus':expected-old,'single_event_corrected_raw':current,'single_event_corrected_potential':potential,
               'single_event_corrected_actual':actual,'single_event_corrected_hp_after':int(r['hp_before'])-actual,
               'NOTE':'COUNTERFACTUAL_SINGLE_EVENT_ONLY; no fight outcomes reexecuted or modified'})
assert len(crits)==6
assert collections.Counter(x['cohort'] for x in crits)=={'R95_BASIC_FIXED_OPENING':4,'R93_TEAM_2X1_BASIC':2}
out={'source_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),
     'normative_source':'Sistema de Combate Mestre, Regra 6: dano normal + fixo + valor MAXIMO DE TODOS OS DADOS NORMAIS, e nao somente uma face',
     'historical_replay':'PASS 24/24 for restricted adapter, but SOURCE_NORMATIVE_CRITICAL_PARITY FAIL in six receipts',
     'number_critical_receipts':6,'distinct_positive_critical_seed_families':2,
     'old_files_untouched':True,'R93_AND_R95_scientific_admission':'HOLD for full normative replay',
     'critical_receipts':crits}
(R/'R102_R93_R95_CRITICAL_PARITY_ERRATA.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('crit receipts',len(crits),'missing total',sum(x['missing_bonus'] for x in crits))
for x in crits:print(x['cohort'],x['seed'],x['side'],x['history_raw'],x['single_event_corrected_raw'],x['single_event_corrected_actual'])
