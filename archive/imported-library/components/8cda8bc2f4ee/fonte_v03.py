"""Proveniência por campo, sem elevar autodeclaração a autenticidade.

Preserva integralmente o envelope/JSON v02; nunca converte fichas reais em
engine_state e nunca recalcula bônus de equipamentos/habilidades.
"""
from __future__ import annotations
import copy
from iniciar_levelup import APP_ROOT  # inicializa compat Windows, sem alterar motor
from adaptador_copia_local import import_local, ImportHold, RealSourceHold, canonical_sha

FIELD_PATHS={
    'identidade.id':'NORMAL.id',
    'progressao.ordinal':'NORMAL.level',
    'raca.nome':'NORMAL.race',
    'atributos.intrinsecos':'NORMAL.attrs',
    'recursos.vida_atual':'NORMAL.hp_current',
    'recursos.vida_max':'NORMAL.hp_max',
    'recursos.alma_atual':'NORMAL.pa_current',
    'recursos.alma_max':'NORMAL.pa_max',
    'espirito.estado_ativacao':'TRANSFORM.activation_state'
}
UNMAPPED=['identidade','progressao.historico_niveis','raca.fonte',
          'atributos.equipamento','atributos.magia','atributos.espirito_overlay',
          'equipamentos','habilidades','titulos','espirito','historico','listas','blocos_originais']

def lookup(o,path):
    for key in path.split('.'):
        if not isinstance(o,dict) or key not in o:
            return None,False
        o=o[key]
    return o,True

def ledger(record,evidence):
    snapshot=evidence['snapshot']
    state=record['engine_state']
    manifest=[]
    for k, engine_path in FIELD_PATHS.items():
        v,ok=lookup(snapshot,k);dst,present=lookup(state,engine_path)
        manifest.append({'snapshot_field':k,'engine_field':engine_path,
                         'snapshot_value_sha256':canonical_sha(v) if ok else None,
                         'field_present':ok,'local_value_matches':bool(ok and present and v==dst),
                         'mechanical_equivalence':'MATCHED_SYNTHETIC_ONLY' if ok and present and v==dst else 'HOLD_NO_EQUIVALENCE',
                         'authenticity':'NOT_INDEPENDENTLY_AUTHENTICATED',
                         'claim_origin':record.get('proveniencia',{}).get('origem','AUSENTE')})
    for k in UNMAPPED:
        v,ok=lookup(snapshot,k)
        manifest.append({'snapshot_field':k,'engine_field':None,'field_present':ok,
                         'snapshot_value_sha256':canonical_sha(v) if ok else None,
                         'mechanical_equivalence':'NOT_MAPPED_PRESERVED_EXACTLY',
                         'authenticity':'NOT_INDEPENDENTLY_AUTHENTICATED',
                         'claim_origin':record.get('proveniencia',{}).get('origem','AUSENTE')})
    return {'schema':'LEVELUP-FIELD-PROVENANCE-V03','file_sha256':evidence['original_bytes_sha256'],
            'snapshot_sha256':evidence['snapshot_sha256'],
            'original_bytes_kept':True,'all_unknown_fields_kept_in_original':True,
            'inferred_from_declaration_only':True,'rest_authenticated':False,
            'field_manifest':manifest}

def import_v03(path,root):
    state,evidence=import_local(path,root)
    import json
    record=json.loads(evidence['original_raw_bytes'])
    # V02 verifica alguns espelhos; a tela V03 exige também máximos exatos.
    for source,target in [('recursos.vida_max','NORMAL.hp_max'),
                          ('recursos.alma_max','NORMAL.pa_max')]:
        x,ok=lookup(evidence['snapshot'],source);y,_=lookup(state,target)
        if not ok or x!=y:
            raise ImportHold(f'HOLD: máximo de recurso divergente em {source}')
    evidence['field_provenance']=ledger(record,evidence)
    return copy.deepcopy(state), evidence
