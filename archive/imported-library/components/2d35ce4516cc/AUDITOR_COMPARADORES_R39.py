#!/usr/bin/env python3
"""R39 — deterministic quality control of readback-linked source excerpts.
Does not decide ranks, compute PA, reach Notion, create items, or claim E0 RE.
It consumes the Comestre's semantic interpretation and then calls unmodified R34.
"""
from __future__ import annotations
from pathlib import Path
import copy,hashlib,json,re,unicodedata
from CONSULTA_MOBILE_R34 import consultar_chat

ROOT=Path(__file__).resolve().parent
REG=json.loads((ROOT/'EVIDENCIAS_MECANICAS_READBACK_R39.json').read_text(encoding='utf8'))['fontes']
VERSION='PA-QUALIDADE-EVIDENCIA-R39/1.0-TEST'

def norm(s:str)->str:
    return ' '.join(''.join(x for x in unicodedata.normalize('NFKD',s.lower()) if not unicodedata.combining(x)).split())

def fingerprints():
    return {key:{**rec,'excerpt_sha256':hashlib.sha256(rec['trecho_mecanico'].encode('utf8')).hexdigest()} for key,rec in REG.items()}

def auditoria(input_wire:dict,*,strict:bool=True)->dict:
    """Source excerpts must literally match a recovered Notion snapshot, and claims
    of independent canonical RE are never inferred from known RI alone.
    A mechanism matched by string is NOT semantic proof or independent RE gold.
    """
    if not isinstance(input_wire,dict):raise ValueError('WIRE_REQUER_OBJETO')
    wire=copy.deepcopy(input_wire)
    queries=wire.get('pesquisa',{})
    if not isinstance(queries,dict):raise ValueError('PESQUISA_REQUER_OBJETO')
    report=[]; blockers=[];warnings=[];covered=set()
    for hab in wire.get('habilidades',[]):
        name=hab.get('nome')
        if not isinstance(name,str):raise ValueError('NOME_DE_HABILIDADE_INVALIDO')
        q=queries.get(name,{})
        if not isinstance(q,dict):q={}
        comps=q.get('comparadores',[])
        if not isinstance(comps,list):raise ValueError('COMPARADORES_REQUER_LISTA')
        if not comps:
            warnings.append('SEM_COMPARADORES_HABILIDADE:'+name)
        kinds=set()
        for c in comps:
            key=c.get('fonte_readback_id') if isinstance(c,dict) else None
            if not key or key not in REG:
                blockers.append('FONTE_SEM_ID_READBACK_AUTORIZADO:'+name)
                continue
            source=REG[key];quoted=c.get('trecho_literal','')
            if not quoted or norm(quoted)!=norm(source['trecho_mecanico']):
                blockers.append('TRECHO_MECANICO_NAO_CONFIRMADO:'+name+':'+str(key))
                continue
            if c.get('url')!=source['url']:
                blockers.append('URL_FONTE_DIVERGENTE:'+name+':'+str(key))
                continue
            if c.get('alega_RE_E0') is True and source['tipo_rank_rotulado']!='RE_E0':
                blockers.append('RI_OU_METODO_NAO_COMPROVA_RE:'+name+':'+str(key))
                continue
            if source['tipo_rank_rotulado'].startswith('RIN_'):
                warnings.append('RIN_NAO_COMPROVA_TRANSFERENCIA_MAGICA:'+name+':'+str(key))
            kinds.add(c.get('tipo'))
            covered.add(key)
            report.append({'habilidade':name,'fonte_readback_id':key,'url':source['url'],
                           'titulo':source['title'],'versao_fonte':source['last_edited_at_readback'],
                           'trecho_sha256':hashlib.sha256(source['trecho_mecanico'].encode('utf8')).hexdigest(),
                           'confronto_lit':'MATCH_EXCERTO_READBACK',
                           'tipo_rotulo_original':source['tipo_rank_rotulado'],
                           'rank_efeito_e0_comprovado':False,
                           'limite':'Parecer mecanico precisa de julgamento Comestre; trecho literal nao e prova automatica de RE.'})
        if kinds and len(kinds)<2:
            warnings.append('COMPARADORES_MESMA_FAMILIA_SOMENTE:'+name)
        body=norm(hab.get('descricao',''))
        if hab.get('modalidade','').upper()=='ATIVA':
            duration=norm(str(hab.get('duracao') or ''))
            if (re.search(r'invisivel|invisibilidade|camuflagem|copia magia|copiar magia',body)
                and not re.search(r'\b\d+\s*(?:turno|turnos|segundo|segundos|minuto|minutos|rodada|rodadas)\b',body+duration)):
                warnings.append('DURACAO_EFEITO_ATIVO_NAO_DELIMITADA:'+name)
        if re.search(r'\bcontrole total\b|\bdomina\b|\bressuscita\b|\bimortal\b|\bqualquer magia\b',body):
            warnings.append('RISCOS_ESTRATEGICOS_DEMANDA_JIT:'+name)
    return {'versao':VERSION,'fontes_cotejadas':len(report),'fontes_unicas':len(covered),
            'evidencias':report,'bloqueios':sorted(set(blockers)),'ressalvas':sorted(set(warnings)),
            'precisao_re_medida':None,'motivo_sem_acuracia':'Nenhuma dessas âncoras fornece gabarito INDEPENDENTE RE E0 da habilidade, mesmo quando ha RI explicito.',
            'nao_reequilibra_historico':True,'nao_altera_codigo_r26_r27':True,
            'escopo':'TEST; TRECHO VERIFICADO CONTRA ARQUIVO RECUPERADO, NAO CONTRA NOTION ONLINE POR PYTHON'}

def consultar_fundamentado(descricao_original:str, interpretacao:dict)->dict:
    """Thin gate. Calculations performed ONLY by the authentic R34/R27/R26.
    Falsely attested Notion citations are never accepted as closed contractual cost.
    """
    q=auditoria(interpretacao)
    urls=sorted({x['url'] for x in q['evidencias']})
    res=consultar_chat(descricao_original,interpretacao,fontes_reabertas=urls)
    res['qualidade_r39']=q
    res['versao_gate_evidencia']=VERSION
    if q['bloqueios'] or any(s.startswith('DURACAO_EFEITO_ATIVO_NAO_DELIMITADA:') for s in q['ressalvas']):
        res['estimativa_parcial_nao_aprovada']={'pa_por_dia':res['pa_por_dia'],'pa_uso':res['pa_ativacao_no_cenario'],
                                               'pa_total':res['pa_total_cenario']}
        res['pa_por_dia']=None;res['pa_ativacao_no_cenario']=None;res['pa_total_cenario']=None
        res['status']='CONSULTA_R39_PARECER_RANK_MANTIDO_PA_TOTAL_NAO_HOMOLOGAVEL'
        res['pendencias']=list(res['pendencias'])+q['bloqueios']+q['ressalvas']
    elif q['ressalvas']:
        res['estado_evidencia']='PARECER_ENERGETICO_COMPLETO_COM_RESSALVAS_COMPARATIVAS'
    else:res['estado_evidencia']='TRECHOS_MECANICOS_VERIFICADOS; RE_INDEPENDENTE_E0_NAO_PROVADO'
    res['gate_nac_prod']='HOLD; nao e instalacao no runtime CRAFT'
    return res

def envelope_craft_qualificado(descricao_original:str,interpretacao:dict)->dict:
    """Read-only CRAFT handoff: real R27 response + independently qualified evidence.
    Does not alter or install QMC05; avoids a second tariff calculation.
    """
    from r28.provider_r27.ponte_pa_craft_r27 import consultar_ficha_craft
    evala=consultar_fundamentado(descricao_original,interpretacao)
    original=consultar_ficha_craft(interpretacao)
    c=original['custo_pa']
    if evala['pa_por_dia'] is not None:
        if (evala['pa_por_dia'],evala['pa_ativacao_no_cenario'],evala['pa_total_cenario']) != (c['pa_por_dia'],c['pa_ativacoes_no_cenario'],c['pa_total_no_cenario']):
            raise ValueError('DIVERGENCIA_CONTRATO_E_FORNECEDOR_ORIGINAL')
    return {'contrato_craft_original':original['contrato'],
        'id_entrada_sha256':original['id_entrada_sha256'],
        'motor_pa':original['custo_pa']['origem_calculo'],
        'gate_r39':evala['status'],
        'custo_pa_qualificado':{'pa_por_dia':evala['pa_por_dia'],
             'pa_ativacoes_no_cenario':evala['pa_ativacao_no_cenario'],
             'pa_total_no_cenario':evala['pa_total_cenario']},
        'proveniencia_fontes':evala['qualidade_r39'],
        'efeitos':evala['habilidades'],
        'historico_reprecificado':False, 'escrita_producao':False,
        'tee_runtime_prod':'PENDENTE; este envelope NAO instala adaptador nem muda QMC05',
        'nac_pass_fabricacao':'HOLD'}

def main():
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--input-json',required=True);ap.add_argument('--output')
    args=ap.parse_args()
    payload=json.loads(Path(args.input_json).read_text(encoding='utf8'))
    result=consultar_fundamentado(payload['descricao_original'],payload['interpretacao'])
    txt=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    if args.output:Path(args.output).write_text(txt,encoding='utf8')
    else:print(txt,end='')
if __name__=='__main__':main()
