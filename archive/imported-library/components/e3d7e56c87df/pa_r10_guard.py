#!/usr/bin/env python3
"""Overlay aditivo, TEST/READ-ONLY, para sucessão PA pós-R09.

NÃO escreve no Notion, não altera ficheiros históricos, não aprova receitas,
não substitui o motor PA R05 nem o validador nativo CRAFT QMC-02.
Autoridade: cinco tarifas expressas pelo Mestre; status de fontes R09.
"""
from __future__ import annotations
import argparse
import csv
from decimal import Decimal, InvalidOperation
from io import StringIO
import json
from pathlib import Path
from typing import Any
import zipfile

R09_NAME = 'PA_P0_R09_CORRIGENDA_TEST_20261018.zip'
R09_SHA = '90ceedc8513b09fe6b6938d0c747a4eba77feb854f8834b791791de9fd320d90'
RATES = {
    'ATRIBUTO_PERMANENTE': Decimal(5),
    'DANO_FIXO_ADICIONAL': Decimal(1),
    'DESLOCAMENTO_PERMANENTE_M': Decimal(1),
    'BONUS_TESTE_ATAQUE': Decimal(1),
    'CA_MAGICA': Decimal(1),
}
UNKNOWN_KINDS = {'RD', 'RDM', 'CURA', 'CONTROLE', 'DADOS_DANO', 'CA_ESTRUTURAL',
                 'DESLOCAMENTO_ATIVO', 'ATIVACAO', 'EFEITO_COMPOSTO', 'ALCANCE',
                 'FREQUENCIA', 'SALVAGUARDA'}


def _positive_number(v: Any) -> Decimal:
    if isinstance(v, bool) or v is None:
        raise ValueError('magnitude numérica positiva exigida; booleanos não são números')
    try:
        d = Decimal(str(v))
    except InvalidOperation as e:
        raise ValueError('magnitude inválida') from e
    if not d.is_finite() or d <= 0:
        raise ValueError('magnitude deve ser finita e positiva')
    return d


def _fmt(v: Decimal | None) -> str | None:
    return None if v is None else format(v.normalize(), 'f')


def quote_effects(effects: list[dict[str, Any]], *, assertion_no_other_effects: bool = False) -> dict[str, Any]:
    """Calcula somente tarifas explicitamente autorizadas, nunca completa lacunas.

    Campos de efeito: kind, magnitude, mode (PASSIVO_DIARIO),
    magical_origin_confirmed (apenas CA_MAGICA), conditional, unit.
    """
    if not isinstance(effects, list):
        raise ValueError('effects deve ser lista')
    components = []
    subtotal = Decimal(0)
    unresolved = []
    seen = set()
    for i, e in enumerate(effects):
        if not isinstance(e, dict):
            raise ValueError('efeito deve ser objeto')
        effect_id = e.get('id', f'e{i}')
        if effect_id in seen:
            raise ValueError('efeito duplicado')
        seen.add(effect_id)
        kind = e.get('kind')
        if kind not in RATES and kind not in UNKNOWN_KINDS:
            raise ValueError(f'tipo {kind!r} desconhecido; não inferir tarifa')
        magnitude = _positive_number(e.get('magnitude'))
        mode = e.get('mode', 'DESCONHECIDO')
        value = None
        reason = None
        if kind not in RATES:
            reason = 'SEM_TARIFA_MESTRE_APROVADA_PARA_ESTE_EFEITO'
        elif mode != 'PASSIVO_DIARIO':
            reason = 'TARIFA_DIARIA_NAO_PROVA_PA_POR_ATIVACAO_OU_TURNO'
        elif kind == 'CA_MAGICA' and e.get('magical_origin_confirmed') is not True:
            reason = 'ORIGEM_MAGICA_DA_CA_NAO_COMPROVADA'
        elif kind == 'DESLOCAMENTO_PERMANENTE_M' and e.get('permanent_confirmed') is not True:
            reason = 'DESLOCAMENTO_PERMANENTE_NAO_COMPROVADO'
        elif kind == 'DANO_FIXO_ADICIONAL' and e.get('damage_is_fixed') is not True:
            reason = 'NAO_COMPROVADO_DANO_FIXO_ADICIONAL'
        elif kind == 'BONUS_TESTE_ATAQUE' and e.get('is_attack_test') is not True:
            reason = 'NAO_COMPROVADO_SER_TESTE_DE_ATAQUE'
        elif kind == 'ATRIBUTO_PERMANENTE' and e.get('permanent_confirmed') is not True:
            reason = 'PERMANENCIA_ATRIBUTO_NAO_COMPROVADA'
        elif bool(e.get('conditional', False)) and kind == 'DANO_FIXO_ADICIONAL':
            reason = 'FREQUENCIA_CONDICIONAL_DE_DANO_SEM_TARIFA_DEFINIDA'
        else:
            value = magnitude * RATES[kind]
            subtotal += value
        if reason:
            unresolved.append({'id': effect_id, 'reason': reason})
        components.append({'id': effect_id, 'kind': kind, 'magnitude': _fmt(magnitude),
                           'mode': mode, 'daily_pa_component': _fmt(value),
                           'reason_if_unresolved': reason})
    total = (subtotal if effects and not unresolved and assertion_no_other_effects is True else None)
    return {
        'status': 'CUSTO_TOTAL_TEST_ISOLADO' if total is not None else 'TOTAL_INDETERMINADO',
        'identified_daily_subtotal_pa': _fmt(subtotal),
        'daily_total_pa': _fmt(total), 'activation_pa': None,
        'components': components, 'unresolved': unresolved,
        'assertion_no_other_effects': assertion_no_other_effects,
        'basis': 'DECISOES_EXPRESSAS_MESTRE_PA_R09_NAO_CANONIZADAS_NESTE_PACOTE',
        'notion_write_authorized': False,
        'craft_native_accepted': False,
        'new_recipe_permitted': False,
        'production_hold': True,
    }


def load_r09(path: str | Path) -> tuple[list[dict[str, str]], list[dict[str, Any]], dict[str, Any]]:
    path = Path(path)
    import hashlib
    if hashlib.sha256(path.read_bytes()).hexdigest() != R09_SHA:
        raise ValueError('pacote R09 não é o original conhecido')
    with zipfile.ZipFile(path) as z:
        if z.testzip() is not None:
            raise ValueError('CRC ZIP inválido')
        rows = list(csv.DictReader(StringIO(z.read('AUDITORIA_94_RECONCILIADA_R09.csv').decode('utf-8-sig')), delimiter=';'))
        gates = json.loads(z.read('GATES_CORRECOES_R09.json'))
        manifest = json.loads(z.read('MANIFEST_R09.json'))
        for name, digest in manifest['created_files'].items():
            if hashlib.sha256(z.read(name)).hexdigest() != digest:
                raise ValueError(f'manifest R09 não confere: {name}')
        if len(rows) != 94 or len({row['uuid'] for row in rows}) != 94:
            raise ValueError('censo de 94 linhas violado')
        if sum(r['origem']=='PARTY_MESTRE_ESPELHO' for r in rows)!=80:
            raise ValueError('80 Espelho não conferem')
        if sum(r['origem']=='CATALOGO_MESTRE_INDEXADO' for r in rows)!=14:
            raise ValueError('14 Mestre não conferem')
        if any(r['writer_apto']!='False' or r['aplicado_notion']!='False' for r in rows):
            raise ValueError('mutação indevida ou estado declarado suspeito')
        if len(gates)!=3:
            raise ValueError('esperados 3 gates, não planos de escrita')
        return rows,gates,manifest


def correction_preview(item: str, r09_zip: str | Path) -> dict[str, Any]:
    rows,gates,_=load_r09(r09_zip)
    def norm(s): return s.strip().casefold()
    match=[x for x in gates if norm(x['item'])==norm(item)]
    if len(match)!=1:
        raise KeyError(f'item {item!r} não encontrado nos 3 gates R09')
    gate=match[0]
    originals=[x for x in rows if norm(x['item'])==norm(item)]
    if len(originals)!=1 or originals[0]['url_original']!=gate['original_party']:
        raise ValueError('identidade original/espelho não reconciliada')
    historical = int(originals[0]['historico_pa_dia'])
    if historical != gate['historico_PA_dia']:
        raise ValueError('custo histórico não confere')
    proposed = gate.get('new_cost')
    if gate['item']=='Mobilidade':
        proposed=None
    if gate['item']=='Manto de Proteção':
        proposed=None  # nunca sem prova física de magia, independentemente do campo R08 test
    return {
        'item': gate['item'], 'historical_daily_pa': historical,
        'proposed_daily_pa_test': proposed,
        'hypothetical_daily_if_magical_ca_confirmed': gate.get('new_cost_if_magical'),
        'gate': gate['estado'], 'party_original_url': gate['original_party'],
        'historical_master_mirror_url': originals[0]['url_fonte'],
        'physical_current_party_readback': False,
        'can_write_original': False, 'can_write_mirror': False,
        'can_use_as_canonical_pa': False,
        'sync_performed': False, 'production_hold': True,
    }


def main():
    p=argparse.ArgumentParser(description='Gate PA pós-R09, TEST e NO-WRITE')
    p.add_argument('--r09', default=str(Path(__file__).resolve().parent.parent/'PA_P0_R09_CORRIGENDA_TEST_20261018.zip'))
    p.add_argument('--item',choices=['Mira Apurada','Manto de Proteção','Mobilidade'])
    p.add_argument('--effects',help='arquivo JSON contendo lista de efeitos')
    p.add_argument('--all-effects-documented',action='store_true')
    a=p.parse_args()
    output = correction_preview(a.item,a.r09) if a.item else quote_effects(json.loads(Path(a.effects).read_text('utf8')) if a.effects else [],assertion_no_other_effects=a.all_effects_documented)
    print(json.dumps(output,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
