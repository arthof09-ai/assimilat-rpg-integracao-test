from pathlib import Path
import sys,json,hashlib,math,re,unicodedata
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
ROOT=Path(__file__).resolve().parent
from benchmark_data_r42 import CASES
RANKS=['Bronze','Prata','Ouro','Ouro Negro','Lendário']
def normalize(s):
 s=unicodedata.normalize('NFKD',s.lower())
 return ''.join(c for c in s if not unicodedata.combining(c))
def dataset():
 gold=[{'id':id,'rank_pattern_e0':rank,'url':'https://app.notion.com/p/'+id} for id,rank,_ in CASES]
 mechanics=[{'opaque_id':hashlib.sha256(id.encode()).hexdigest()[:16],
             'mechanics_text':txt,'mechanics_sha256':hashlib.sha256(txt.encode()).hexdigest()} for id,_,txt in CASES]
 # No pattern title, its rank, item rank, names, costs/prices used as predictors.
 return mechanics,gold

def compare_leave_one_out(mechanics,gold):
 texts=[normalize(x['mechanics_text']) for x in mechanics]
 v=TfidfVectorizer(ngram_range=(1,2),analyzer='word',min_df=1,sublinear_tf=True)
 X=v.fit_transform(texts)
 sims=cosine_similarity(X)
 predictions=[]
 for i,row in enumerate(mechanics):
  j=max((k for k in range(len(texts)) if k!=i),key=lambda k:sims[i,k])
  predictions.append({'opaque_id':row['opaque_id'],'mechanics_sha256':row['mechanics_sha256'],
        'rank_predicted_by_nearest_other':gold[j]['rank_pattern_e0'],
        'nearest_other_opaque_id':mechanics[j]['opaque_id'],
        'similarity':round(float(sims[i,j]),5),
        'confidence':'BAIXA' if sims[i,j]<.2 else 'MEDIA' if sims[i,j]<.5 else 'ALTA',
        'training_self_case_excluded':True})
 return predictions

def run():
 mechanics,gold=dataset()
 assert len(mechanics)==len(gold)==12
 assert len(set(x['opaque_id'] for x in mechanics))==12
 # Mechanic-only prediction file cannot contain labels of its OWN case, own title, RI or price.
 predictions=compare_leave_one_out(mechanics,gold)
 (ROOT/'MECHANICS_ONLY_R42.json').write_text(json.dumps(mechanics,ensure_ascii=False,indent=2)+'\n')
 (ROOT/'GOLD_R42_SEPARATE.json').write_text(json.dumps(gold,ensure_ascii=False,indent=2)+'\n')
 frozen={'kind':'R42_TEXTUAL_PATTERN_LOO_TEST','not_26_technique_images':True,
         'caveat':'Label of each evaluated case excluded from its own training row; small nonrandom curated corpus, not independent prospective blind adjudication.',
         'predictions':predictions}
 frozen_body=json.dumps(frozen,sort_keys=True,ensure_ascii=False,separators=(',',':'))
 freeze=hashlib.sha256(frozen_body.encode()).hexdigest()
 (ROOT/'PREDICTIONS_FROZEN_R42.json').write_text(json.dumps({**frozen,'sha256_prediction_freeze':freeze},ensure_ascii=False,indent=2)+'\n')
 correct=sum(p['rank_predicted_by_nearest_other']==g['rank_pattern_e0'] for p,g in zip(predictions,gold))
 low=sum(p['confidence']=='BAIXA' for p in predictions)
 out={'n_cases':12,'n_text_mechanics':12,'n_technique_images_read':0,'n_valid_inscription_pattern_labels':12,
      'scope':'RANK DO PADRÃO/INSCRIÇÃO COMPLETA; NÃO RANK DE CADA SUBEFEITO OU RI',
      'prediction_protocol':'TF-IDF 1+2grams normalized, leave-one-out, nearest-other (no own label); report per-case provisional',
      'n_predictions':12,'n_correct':correct,'accuracy':round(correct/12,4),'low_confidence':low,
      'predictions_sha256':freeze,'n_unscored_techniques_from_R40':26,
      'limitations':['Corpus oportunístico de fontes canônicas; não generalizar precisão a itens.',
       'A transcrição das mecânicas foi feita manualmente a partir dos textos Notion, sem reabertura binária dos anexos.',
       'Predição computacional não usa a própria etiqueta do caso, mas o desenho da metodologia não é avaliação independente de desenvolvimento.',
       'R26 calcula o PA corretamente; esta LOO é prova de classificação complementar, não substitui fornecedor nem autoriza canonização.'],
      'individual':[{'opaque_id':p['opaque_id'],'gold_rank':g['rank_pattern_e0'], 'predicted':p['rank_predicted_by_nearest_other'], 'correct':p['rank_predicted_by_nearest_other']==g['rank_pattern_e0'], 'confidence':p['confidence'],'similarity':p['similarity']} for p,g in zip(predictions,gold)]}
 (ROOT/'SCORE_R42.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:out[k] for k in ['n_cases','n_predictions','n_correct','accuracy','low_confidence','predictions_sha256']},indent=2))
 return out
if __name__=='__main__':run()
