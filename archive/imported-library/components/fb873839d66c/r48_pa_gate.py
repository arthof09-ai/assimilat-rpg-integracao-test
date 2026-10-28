"""Consumer-side CRAFT TEST guard: reads the UNMODIFIED R39/R27/R26 result.
No rank classifier, PA arithmetic, or economic pricing is implemented here.
Cannot authorize magic or material fabrication. Fail-closed on changed evidence.
"""
from pathlib import Path
import json,hashlib
R39_SHA='1d4e43e1f8b21106e0c8fee25bab53a81528e4a903f3184852b768dade48c4ea'
EXPECTED_INPUT_SHA='5d0cd90a50eaca679680b83bffc90ebac1eeda713852263bcc6c7c1fc8306613'
BASE=Path(__file__).resolve().parent

def validate_envelope(candidate_hash):
    p=BASE/'R39_PINGENTE_ENVELOPE_NATIVE.json'
    if not p.is_file():raise ValueError('PA_R39_ENVELOPE_NOT_AVAILABLE')
    raw=p.read_bytes();actual=hashlib.sha256(raw).hexdigest()
    if candidate_hash!=actual or actual!=R39_SHA:
        raise ValueError('PA_R39_ENVELOPE_SHA_OR_SOURCE_VERSION_CHANGED')
    env=json.loads(raw)
    if env.get('contrato_craft_original')!='PA-CRAFT-QMC05-COMPAT-R27/1.0.0-TEST' or env.get('id_entrada_sha256')!=EXPECTED_INPUT_SHA:
        raise ValueError('PA_R27_CONTRACT_OR_INPUT_MISMATCH')
    if env.get('motor_pa')!='PARECER_R26_TEST_SEMICANONICO' or env.get('gate_r39')!='CONSULTA_TEST_CENARIO_ENERGETICO_COMPLETO':
        raise ValueError('PA_R39_PROVIDER_GATE_INVALID')
    # These values merely match the authenticated supplier's scoped receipt;
    # there is NO internal tariff calculation.
    if env.get('custo_pa_qualificado')!={'pa_por_dia':12,'pa_ativacoes_no_cenario':14,'pa_total_no_cenario':26}:
        raise ValueError('PA_R39_RECEIPT_CHANGED')
    q=env.get('proveniencia_fontes',{})
    if q.get('bloqueios') or q.get('versao')!='PA-QUALIDADE-EVIDENCIA-R39/1.0-TEST' or q.get('fontes_cotejadas')!=5:
        raise ValueError('PA_R39_PROVENANCE_REJECTED')
    effects=env.get('efeitos',[])
    if len(effects)!=2 or {(e.get('nome'),e.get('modalidade'),e.get('rank_efeito_proposto'),e.get('duracao'),e.get('usos_no_dia')) for e in effects}!={
      ('Luminescência de Vigília','PASSIVA','Bronze','enquanto equipado',0),
      ('Abertura de Contrassombra','ATIVA','Prata','1 turno',2)}:
        raise ValueError('PA_R39_EFFECT_CONDITION_CHANGED')
    if any(e.get('estado')!='PARECER_SEMICANONICO_COMPARATIVO' for e in effects):
        raise ValueError('PA_R39_FALSE_E0_STATUS')
    if env.get('escrita_producao') is not False or env.get('nac_pass_fabricacao')!='HOLD':
        raise ValueError('PA_R39_SCOPE_ESCALATION')
    return {'status':'PA_R39_R27_R26_RECEIPT_CONSUMED','sha256':actual,
       'classification':'RI_PRATA_E3,RE_BRONZE_E3_PASSIVA,RE_PRATA_E3_ATIVA',
       'pa_por_ativacao':next(e['pa_por_ativacao'] for e in effects if e['modalidade']=='ATIVA'),
       'authority':'TEST_ONLY,NO_REAL_MAGIC_MEASURED'}
