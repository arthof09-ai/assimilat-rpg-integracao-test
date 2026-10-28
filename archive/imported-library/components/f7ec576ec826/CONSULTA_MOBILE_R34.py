#!/usr/bin/env python3
"""R34 thin operational adapter: natural-language user input -> Mestre-side semantic
interpretation -> EXISTING R27/R26 engine. Does not invent a second tariff model.
No Notion API, no physical writes, no autonomous unattended service.

Usage in conversation: the Comestre reads the free-form text and authorized Notion
comparators, constructs one auditable wire, and calls consultar_chat() directly.
"""
from __future__ import annotations
from pathlib import Path
import hashlib,json,sys
from typing import Any
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'r28/provider_r27'))
from ponte_pa_craft_r27 import consultar_ficha_craft,ContractError

VERSION='PA-CHAT-QMC05-R34/1.0.0-TEST'
class ChatContractError(ValueError):pass

def consultar_chat(descricao_original:str, interpretacao:dict, *, fontes_reabertas: list[str]|None=None)->dict:
    if not isinstance(descricao_original,str) or len(descricao_original.strip())<20:
        raise ChatContractError('DESCRICAO_NATURAL_NAO_FORNECIDA')
    if not isinstance(interpretacao,dict) or 'item' not in interpretacao:
        raise ChatContractError('INTERPRETACAO_AUDITAVEL_REQUERIDA')
    if interpretacao.get('acao','CONSULTAR_PA_TEST')!='CONSULTAR_PA_TEST':
        raise ChatContractError('ACAO_FORA_DO_ESCOPO_PA_CONSULTA')
    if interpretacao.get('historico'):
        raise ChatContractError('R34_DESTINADO_NOVO_ITEM_TEST; HISTORICOS_USAR_R28_LEITURA')
    for a in interpretacao.get('habilidades',[]):
        if a.get('descricao','').strip() and len(a.get('descricao',''))>len(descricao_original)*3:
            raise ChatContractError('EFEITO_EXTENSO_NAO_COMPROVADO_NA_DESCRICAO')
    w=json.loads(json.dumps(interpretacao,ensure_ascii=False))
    w['acao']='CONSULTAR_PA_TEST';w['historico']=False
    real=consultar_ficha_craft(w)
    known={url.strip() for url in (fontes_reabertas or [])}
    cited={c.get('url') for q in w.get('pesquisa',{}).values() for c in (q.get('comparadores') or []) if isinstance(c,dict)}
    # If comparison is not independently re-opened by connector, mark the
    # apparent confidence as a report, not as independent E0 evidence.
    unverified=sorted(u for u in cited if u not in known)
    cost=real['custo_pa']
    completed=bool(cost.get('pa_por_dia') is not None and not unverified)
    status = ('CONSULTA_TEST_CENARIO_ESTIMADO_ALTO_RISCO_USO_MATERIAL_HOLD' if completed and real.get('risco_material')
              else 'CONSULTA_TEST_CENARIO_ENERGETICO_COMPLETO' if completed
              else 'CONSULTA_TEST_PARCIAL_EVIDENCIA_INSUFICIENTE')
    return {
      'versao':VERSION,'status':status,
      'descricao_livre_original':descricao_original,
      'descricao_sha256':hashlib.sha256(descricao_original.encode()).hexdigest(),
      'interpretacao_semantica_proposta':w,
      'comparadores_reabertos_nesta_sessao':sorted(known),
      'comparadores_sem_readback_confirmado':unverified,
      'rank_item':real['item']['classificacao_declarada'],
      'habilidades':real['habilidades'],
      'pa_por_dia':cost.get('pa_por_dia') if completed else None,
      'pa_ativacao_no_cenario':cost.get('pa_ativacoes_no_cenario') if completed else None,
      'pa_total_cenario':cost.get('pa_total_no_cenario') if completed else None,
      'subtotal_simulado_nao_aprovado':cost.get('pa_por_dia'),
      'pendencias':real['pendencias'],
      'gate_origem':real['gate'],
      'politica':'CLASSIFICACAO_MESTRE_SIDE_SEMICANONICA_REVOGAVEL; TESTE, NAO_PUBLICAR_P4',
      'uso_material_permitido':False,'notion_write':False,'party_write':False,'writer_lease_epoch':None,
      'motor_origem':'PA_R27→PA_R26; nenhuma formula local duplicada'
    }

def ficha_md(o:dict)->str:
    s=['# Ficha energética — parecer Mestre-side',
       f"**Item:** {o['interpretacao_semantica_proposta']['item']}",
       f"**Rank do item:** {o['rank_item'] or 'A INVESTIGAR'}",
       f"**Estado:** {o['status']}"]
    for a in o['habilidades']:
        s.extend(['',f"## {a['nome']} ({a['modalidade']})",
            f"Efeito: {a['efeito_literal']}",
            f"Rank de efeito: {a['rank_efeito_proposto'] or 'INDETERMINADO'}; confiança: {a['confianca']}; risco: {a['risco']}",
            f"PA/dia da habilidade: {a['pa_por_dia'] if a['pa_por_dia'] is not None else 'PENDENTE'}; PA/ativação: {a['pa_por_ativacao'] if a['pa_por_ativacao'] is not None else 'NÃO APLICÁVEL/PENDENTE'}",
            f"Duração: {a['duracao'] or 'NÃO DOCUMENTADA'}; frequência: {a['frequencia'] or 'NÃO DOCUMENTADA'}"])
    s.extend(['','## Orçamento energético',
            f"Manutenção: {o['pa_por_dia'] if o['pa_por_dia'] is not None else 'PENDENTE'} PA/dia",
            f"Ativações no cenário: {o['pa_ativacao_no_cenario'] if o['pa_ativacao_no_cenario'] is not None else 'PENDENTE'} PA",
            f"Total cenário: {o['pa_total_cenario'] if o['pa_total_cenario'] is not None else 'PENDENTE'} PA",
            f"Pendências: {'; '.join(o['pendencias']) or 'Nenhuma pendência numérica na simulação; revisão JIT/PS material independente.'}",
            '**Sem escrita Notion/Party; sem promoção P4.**'])
    return '\n'.join(s)+'\n'

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser(description='Consultor de PA: Comestre estrutura a fala e chama motor real; CLI TEST')
    ap.add_argument('--input-json',required=True,help='JSON de {descricao_original, interpretacao, fontes_reabertas}')
    ap.add_argument('--saida-json');ap.add_argument('--saida-md')
    x=ap.parse_args();v=json.loads(Path(x.input_json).read_text('utf8'))
    o=consultar_chat(v['descricao_original'],v['interpretacao'],fontes_reabertas=v.get('fontes_reabertas'))
    j=json.dumps(o,ensure_ascii=False,indent=2,sort_keys=True)+'\n'
    if x.saida_json:Path(x.saida_json).write_text(j,encoding='utf8')
    if x.saida_md:Path(x.saida_md).write_text(ficha_md(o),encoding='utf8')
    print(j)
