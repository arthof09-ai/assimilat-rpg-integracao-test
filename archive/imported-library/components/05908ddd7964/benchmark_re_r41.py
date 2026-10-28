#!/usr/bin/env python3
"""Controlled RE E0 holdout. Label-only pages do NOT qualify as scored tests.
Text of skills must have independently certified mechanical source; names, prices, rank tags
are stripped before prediction. No training/relabeling by the target rank.
"""
from pathlib import Path
import json,hashlib,copy
RANKS=('Bronze','Prata','Ouro','Ouro Negro','Lendário')

def sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

def mask_gold(gold:dict,mechanics:list)->dict:
    assert 'techniques' in gold
    lookup={r['notion_page_id']:r for r in gold['techniques']}
    numbered=[];pending=[]
    for rec in mechanics:
        uid=rec['notion_page_id'];mech=(rec.get('mechanics_verified_text') or '').strip()
        source=rec.get('source_mechanics_sha256')
        if uid not in lookup:raise ValueError('NO_GOLD_SOURCE')
        if not mech or not source or hashlib.sha256(mech.encode()).hexdigest()!=source:
            pending.append({'opaque_id':hashlib.sha256(uid.encode()).hexdigest()[:12],
                            'status':'NO_VALIDATED_MECHANICS'});continue
        for r in RANKS:
            if f'({r})' in mech or f'Classificação: {r}' in mech:
                raise ValueError('RANK_LEAK_IN_MECHANICS')
        numbered.append({'opaque_id':hashlib.sha256(uid.encode()).hexdigest()[:12],
                         'mechanics_verified_text':mech,'mechanics_sha256':source})
    return {'schema':'RE-E0-BLIND-R41/1.0-TEST','cases':numbered,'unscorable':pending,
            'gold_labels_exposed_to_predictor':False,'score_must_be_null_until_frozen':True}

def score_predictions(gold:dict,mechanics:list,preds:list)->dict:
    masked=mask_gold(gold,mechanics)
    index={hashlib.sha256(r['notion_page_id'].encode()).hexdigest()[:12]:r for r in gold['techniques']}
    pred_idx={r['opaque_id']:r for r in preds}
    if len(pred_idx)!=len(preds):raise ValueError('DUPLICATE_PREDICTION')
    correct=0;total=0;rows=[]
    for rec in masked['cases']:
        entry=pred_idx.get(rec['opaque_id'])
        if not entry or entry.get('prediction_locked') is not True or entry.get('mechanics_sha256')!=rec['mechanics_sha256']:
            continue
        p=entry.get('predicted_re');gold_rank=index[rec['opaque_id']]['rank_de_efeito_documentado']
        if p not in RANKS:raise ValueError('INVALID_PREDICTION')
        ok=p==gold_rank;correct+=ok;total+=1
        rows.append({'opaque_id':rec['opaque_id'],'predicted_rank':p,'gold_rank':gold_rank,'correct':ok})
    return {'n_gold_labels':len(index),'n_mechanical_proofs':len(masked['cases']),
            'n_valid_blind_predictions':total,'n_correct':correct,
            'accuracy':correct/total if total else None,
            'missing_mechanics':len(masked['unscorable']), 'rows':rows}

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--gold',required=True);ap.add_argument('--mechanics');ap.add_argument('--predictions');args=ap.parse_args()
    g=json.loads(Path(args.gold).read_text());m=json.loads(Path(args.mechanics).read_text()) if args.mechanics else []
    p=json.loads(Path(args.predictions).read_text()) if args.predictions else []
    print(json.dumps(score_predictions(g,m,p),ensure_ascii=False,indent=2))
