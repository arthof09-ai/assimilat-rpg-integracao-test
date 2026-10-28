from pathlib import Path
import sys,json,os
HERE=Path(__file__).resolve().parent
sys.path.insert(0,os.environ.get('R42_R26_ENGINE',str(HERE/'parents'/'engine_r26')))
from parecer_semicanonico_r26 import avaliar
from benchmark_data_r42 import CASES
ROWS=[]
for uid,gold,mechanics in CASES:
    # Direct call to unchanged R26 without providing gold/RI or pre-chosen RE.
    raw='Item: Item proposto anônimo\nHabilidade ativa: Efeito: '+mechanics
    response=avaliar(raw,origem='NOVO_TEST',pesquisa={})
    a=response.get('r26',{}).get('pareceres',[])
    candidate=a[0].get('rank_efeito_recomendado') if len(a)==1 else None
    ROWS.append({'id':uid,'rank_source_inscription_pattern_e0':gold,'r26_candidate_without_gold':candidate,
        'r26_confidence':a[0]['confianca'] if a else None,
        'agree':candidate==gold if candidate else None,
        'status':response.get('r26',{}).get('veredito')})
n=sum(x['r26_candidate_without_gold'] is not None for x in ROWS)
correct=sum(x['agree'] is True for x in ROWS)
out={'n':len(ROWS),'n_auto_re_candidates':n,'candidate_coverage':n/len(ROWS),'n_correct_if_candidate':correct,
     'accuracy_conditional_on_candidate':correct/n if n else None,
     'accuracy_all_cases_treat_unranked_as_abstention':correct/len(ROWS),
     'interpretation':'R26 was used exactly as written, no supplied rank or comparative research. Not a measure of expert consultant guided by E3 research. Rank of full pattern only.',
     'rows':ROWS}
(HERE/'R26_DIRECT_R42.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='rows'},ensure_ascii=False,indent=2))
