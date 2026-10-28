"""Ingresso read-only de snapshots locais. Não lê nem modifica Notion.

IMPORTANTE: snapshots reais são preservados/quarentenados e nunca executados
no R17, cujo contrato aceita SOMENTE entidades SYNTH- fictícias.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

REQUIRED = ('identidade','progressao','raca','atributos','recursos','equipamentos',
            'habilidades','titulos','espirito','historico','listas','blocos_originais')
MAX_BYTES = 15_000_000

class ImportHold(ValueError):
    pass

class RealSourceHold(ImportHold):
    def __init__(self, evidence):
        super().__init__('HOLD REAL: original integral acolhido apenas em quarentena. R17 não evolui fichas reais.')
        self.evidence = evidence

def quarantine_real(evidence, root):
    """Acervo local bruto do snapshot já verificado; jamais um commit de engine."""
    import secrets
    from datetime import datetime, timezone
    from durable_r14 import _atomic_json
    folder=Path(root)/'importacoes_quarentena'/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_'+secrets.token_hex(5))
    folder.mkdir(parents=True,exist_ok=False)
    target=folder/'COPIA_BRUTA_SEM_EVOLUCAO.json'
    target.write_bytes(evidence['original_raw_bytes'])
    if hashlib.sha256(target.read_bytes()).hexdigest()!=evidence['original_bytes_sha256']:
        raise ImportHold('HOLD: falha readback do snapshot arquivado; não reutilizar')
    _atomic_json(folder/'RECIBO_HOLD.json',{'status':'QUARENTENA_REAL_HOLD_SEM_MOTOR',
         'input_sha256':evidence['original_bytes_sha256'],
         'readback_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
         'snapshot_sha256':evidence['snapshot_sha256'],
         'origin':evidence['proveniencia'],'notion_writes':0,'canonical_commit':False})
    return folder

def canonical_sha(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,
                       separators=(',',':')).encode('utf-8')).hexdigest()

def import_local(path, root):
    """Returns (state, evidence). Never opens anything outside fichas_locais."""
    base=(Path(root)/'fichas_locais').resolve()
    if not base.is_dir():
        raise ImportHold('Crie fichas_locais e coloque a exportação JSON nessa pasta.')
    path=(base/path).resolve()
    if not path.is_relative_to(base) or path.suffix.lower()!='.json' or not path.is_file():
        raise ImportHold('Somente arquivos JSON dentro de fichas_locais.')
    if path.stat().st_size > MAX_BYTES:
        raise ImportHold('Arquivo maior que limite local de 15 MB.')
    raw=path.read_bytes()
    try:
        record=json.loads(raw)
    except (UnicodeDecodeError,ValueError) as exc:
        raise ImportHold('JSON inválido: '+str(exc)) from exc
    if not isinstance(record,dict) or record.get('schema')!='LEVELUP-COPIA-LOCAL-V1':
        raise ImportHold('Formato desconhecido. Consulte MODELO_IMPORTACAO.md.')
    snap=record.get('snapshot')
    if not isinstance(snap,dict) or any(k not in snap for k in REQUIRED):
        raise ImportHold('HOLD: snapshot incompleto: exigidas seções e blocos originais.')
    if not isinstance(snap['blocos_originais'],list) or not isinstance(snap['historico'],list):
        raise ImportHold('HOLD: blocos originais e histórico precisam ser listas completas.')
    if not snap['blocos_originais']:
        raise ImportHold('HOLD: snapshot sem blocos originais; não é prova de ficha integral.')
    expected=record.get('snapshot_sha256')
    if not isinstance(expected,str) or expected!=canonical_sha(snap):
        raise ImportHold('HOLD: SHA-256 do snapshot divergente ou ausente.')
    if not isinstance(record.get('proveniencia'),dict) or not all(record['proveniencia'].get(k) for k in ('origem','capturado_em','versao')):
        raise ImportHold('HOLD: origem, data e versão da captura ausentes.')
    evidence={'source_file':path.name,'original_bytes_sha256':hashlib.sha256(raw).hexdigest(),
              'snapshot_sha256':expected,'original_raw_bytes':raw,'snapshot':snap,
              'proveniencia':record['proveniencia'],'kind':record.get('kind')}
    if record.get('kind')!='FICTICIO_EXPERIMENTAL':
        raise RealSourceHold(evidence)
    state=record.get('engine_state')
    if not isinstance(state,dict):
        raise ImportHold('HOLD: estado R17 experimental não fornecido.')
    # A estrutura livre nunca vira fonte de regras por dedução; exigimos
    # consistência estrita com as informações representadas no motor.
    try:
        from engine_r17 import validate_r17
        validate_r17(state)
        n=state['NORMAL']; t=state['TRANSFORM']
        if snap['identidade'].get('id')!=n['id'] or snap['progressao'].get('ordinal')!=n['level']:
            raise ImportHold('HOLD: identidade/nível divergem do estado projetado.')
        if snap['raca'].get('nome')!=n['race'] or snap['atributos'].get('intrinsecos')!=n['attrs']:
            raise ImportHold('HOLD: raça/atributos divergem. Não somar equipamento e buffs.')
        if snap['espirito'].get('estado_ativacao')!=t['activation_state']:
            raise ImportHold('HOLD: Espírito divergente ou ativação desconhecida.')
        if snap['recursos'].get('vida_atual')!=n['hp_current'] or snap['recursos'].get('alma_atual')!=n['pa_current']:
            raise ImportHold('HOLD: reservas atuais divergentes.')
    except ImportHold:
        raise
    except (KeyError,TypeError,ValueError) as exc:
        raise ImportHold('HOLD: estado motor/espelho inconsistente: '+str(exc)) from exc
    evidence['engine_state_sha256']=canonical_sha(state)
    return state,evidence
