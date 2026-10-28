#!/usr/bin/env python3
"""Audit existing R08 Atlas and R09 gates without rank promotion or fake holdout."""
import zipfile,csv,io,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
z08=ROOT/'PA_P0_R08_ORIGINAIS_ATLAS_CORRECOES_TEST_20261018.zip'
z09=ROOT/'PA_P0_R09_CORRIGENDA_TEST_20261018.zip'
assert hashlib.sha256(z08.read_bytes()).hexdigest()=='e7957fb016c3ce04343620a7e1a2b155a5e317afc5eb22ef753f96f1aa9b6499'
assert hashlib.sha256(z09.read_bytes()).hexdigest()=='90ceedc8513b09fe6b6938d0c747a4eba77feb854f8834b791791de9fd320d90'
with zipfile.ZipFile(z08) as z:
    rows=list(csv.DictReader(io.StringIO(z.read('ATLAS_9x14_EIXOS_R08.csv').decode('utf-8-sig')),delimiter=';'))
with zipfile.ZipFile(z09) as z:
    gates=json.loads(z.read('GATES_RANKS_R09.json'))
ids=set(r['uuid'] for r in rows)
assert len(ids)==9 and len(rows)==126
assert all({int(x['eixo_numero']) for x in rows if x['uuid']==k}==set(range(1,15)) for k in ids)
assert len(gates['atlas_nove'])==9 and all(x['rank_canonicamente_homologado'] is False for x in gates['atlas_nove'])
assert len(gates['tres_sem_classificacao'])==3
out={'R14':{'atlas_uuid':9,'eixos_por_item':14,'atlas_rows':126,'all_E3_unapproved':True,
             'independent_comparators_sufficient':False,'veste_imperial_not_independent':True,
             'new_ranks_canonized':0},
     'R15':{'without_rank':3,'status':'SEM_CLASSIFICACAO_DE_PODER/MECANICA_INSUFICIENTE','mechanics_resolved':0},
     'R16':{'new_empirical_rates_validated':0,'master_independent_holdout_costed':0,
        'why':'R05 reports zero genuinely independent priced holdout Mestre; Party mirror and twin variants are not independent samples',
        'preregistration':'define E0 independent source identities; effects fully typed, pure isolate with PA/dia explicit; lock holdout before searching and reject text ancestry clones; preserve PA/activation and cost modality; no regression rates on composite-only observations',
        'no_price_from_MED_or_rank':True},'notion_writes':0,'source_zip_hashes_verified':True}
print(json.dumps(out,ensure_ascii=False,indent=2))
