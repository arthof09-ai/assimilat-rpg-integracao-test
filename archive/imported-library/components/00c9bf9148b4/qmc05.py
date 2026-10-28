#!/usr/bin/env python3
"""QMC-05: extensão semântica/read-only do QMC-04. NÃO cria itens, receitas ou PA.

Somente evidência literal de fetch autoritativo verificada na conversa é admissível.
Um arquivo local, inclusive acompanhado de hash, não atesta a origem no Notion.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys, zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'QMC-04'))
import qmc04

VERSION='QMC-05.0-LAB'
EFFECT_SCHEMA='EFFECT-STRUCTURED-CANDIDATE-1'
PA_INTERCHANGE='CRAFT-PA-INTERCHANGE-05-CANDIDATE'


def _literal_lines(content:str)->list[str]:
    lines=qmc04.lines_with_offsets(content)
    return [x['literal'] for x in lines]


def _magnitude_spans(sentence:str)->list[dict]:
    """Extrai apenas intervalos literais; nunca precifica ou aplica bônus."""
    rules=(
        ('CA',r'(?<!\w)([+\-]\s*\d+)\s*CA\b'),
        ('DESLOCAMENTO_M',r'(?<!\w)([+\-]\s*\d+)\s*m\s*(?:de\s+)?deslocamento\b'),
        ('DESTREZA',r'(?<!\w)([+\-]\s*\d+)\s*(?:de\s+)?destreza\b'),
        ('CARISMA',r'\bperde\s+(\d+)\s+pontos?\s+de\s+carisma\b'),
        ('FURTIVIDADE',r'(?<!\w)([+\-]\s*\d+)\s*(?:de\s+)?furtividade\b'),
        ('VELOCIDADE_MULTIPLICADOR',r'\bduplica\s+(?:sua\s+)?velocidade\b'),
        ('DANO_DADOS',r'\b\d+d\d+(?:\s*\+\s*(?:\d+|int|for|des))?'),
    )
    found=[];seen=set()
    for kind,pat in rules:
        for m in re.finditer(pat,sentence,flags=re.I):
            span=m.group(0)
            sig=(kind,m.start(),m.end())
            if sig in seen:continue
            seen.add(sig)
            num=None
            if kind=='VELOCIDADE_MULTIPLICADOR':
                num=2
            elif kind!='DANO_DADOS':
                a=re.search(r'[+\-]?\s*\d+',m.group(1));num=int(a.group(0).replace(' ','')) if a else None
                if kind=='CARISMA' and num is not None:num=-abs(num)
            found.append({'property':kind,'value':num,'unit':'fator' if kind=='VELOCIDADE_MULTIPLICADOR' else ('metros' if kind=='DESLOCAMENTO_M' else ('dados literais' if kind=='DANO_DADOS' else 'pontos')),
                          'literal':span, 'documented':True})
    return sorted(found,key=lambda x:sentence.find(x['literal']))


def _explicit_mode(sentence:str)->str:
    if re.search(r'\(Atv\)',sentence,re.I):return 'ATIVO_EXPLICITO'
    if re.search(r'\(Pass\)',sentence,re.I):return 'PASSIVO_EXPLICITO'
    if re.search(r'\bquando ativad[ao]\b',sentence,re.I):return 'ATIVACAO_DESCRITA_MAS_ACAO_NAO_DEFINIDA'
    if re.search(r'\buma vez\s+por\s+(?:noite|dia|turno)\b',sentence,re.I):return 'USO_CONDICIONAL_SEM_TIPO_DE_ACAO'
    return 'MODALIDADE_NAO_DETERMINADA'


def _is_negated_benefit(sentence:str)->bool:
    """Negação explícita impede transformar a menção de bônus em bônus concedido."""
    return bool(re.search(r'\b(?:não|nunca)\s+(?:concede|aumenta|adiciona|causa|duplica|atribui|fornece|garante|dá|da)\b|\bsem\s+(?:b[oô]nus|custo|aumento)\b',sentence,re.I))


def _duration(sentence:str)->dict:
    for p in (r'\bpor\s+\d+\s+(?:minutos?|horas?|turnos?|rodadas?)\b',r'\bat[eé]\s+o\s+final\s+do\s+turno\b'):
        m=re.search(p,sentence,re.I)
        if m:return {'status':'DURACAO_EXPLICITA','literal':m.group(0),'exact_seconds':None}
    if re.search(r'\btemporariamente\b|\btempor[aá]ri[ao]\b',sentence,re.I):
        return {'status':'TEMPORARIA_SEM_DURACAO_EXATA','literal':'temporariamente','exact_seconds':None}
    return {'status':'NAO_DOCUMENTADA','literal':None,'exact_seconds':None}


def _condition(sentence:str)->list[str]:
    patterns=(r'\bao\s+amanhecer\b',r'\ba\s+cada\s+novo\s+amanhecer\b',
              r'\bao\s+ficar\s+(?:na\s+frente|diante)\s+(?:desse|do)\s+espelho\b',r'\bquem\s+ficar\s+na\s+frente\s+(?:desse|do)\s+espelho\b',
              r'\bprimeiro\s+golpe\b',r'\bem\s+climas\s+frios\b',r'\bem\s+lugares\s+escuros\b',
              r'\buma\s+vez\s+por\s+(?:noite|dia|turno)\b',r'\bquando\s+ativad[ao]\b')
    return [m.group(0) for pat in patterns for m in re.finditer(pat,sentence,re.I)]


def structured_effects(qualified:dict)->dict:
    """Grounding: todos os efeitos derivam de citações já presentes em QMC-04.

    Não considerar título de poder prova de consumo, reação, carga ou duração.
    """
    if qualified.get('status')!='ATENDIDO_PARECER_COM_LIMITE_DE_ATESTACAO':
        return {'status':'QUALIFICACAO_INADMISSIVEL','effects':[]}
    source=qualified['baseline_qmc03']['item']['identity']['url']
    effects=[]
    for idx,e in enumerate(qualified['additional_effects']['effects']):
        s=e['literal']
        if any(x in s.lower() for x in ('conserva informações','arquivo histórico','fonte protegida','recalculado','referência legada','função, propriedades')):
            continue
        negative=_is_negated_benefit(s)
        mentioned_mags=_magnitude_spans(s)
        mag=[] if negative else mentioned_mags
        conditions=_condition(s)
        mode=_explicit_mode(s)
        cost=[{'value':int(m.group(1)),'unit':'PA sem inferir modalidade', 'literal':m.group(0)} for m in re.finditer(r'(?<!\d)(\d+)\s*PA\b',s,re.I)]
        for c in cost:
            if re.search(r'\bpor\s+dia\b',s,re.I):c['unit']='PA/dia explícito'
            elif re.search(r'\b(?:ativar|ativação|\(Atv\))\b',s,re.I):c['unit']='PA por ativação descrita'
        if re.search(r'\b(?:portador|usu[aá]ri[ao]|sua velocidade|destreza)\b',s,re.I):target='PORTADOR_DESCRITO'
        elif re.search(r'\bquem\s+ficar\b',s,re.I):target='PESSOA_DIANTE_DO_OBJETO'
        elif re.search(r'\b(?:inimigo|alvo)\b',s,re.I):target='ALVO_DESCRITO'
        else:target='NAO_EXPLICITO'
        effects.append({'effect_id':f'E{len(effects)+1:02}', 'literal':s, 'source_url':source,
            'semantic_kind':['RESTRICAO_NEGATIVA_EXPLICITA'] if negative else ([m['property'] for m in mag] or ['EFEITO_TEXTUAL_NAO_QUANTIFICADO']),
            'negated_benefit':negative,'negated_magnitude_mentions':mentioned_mags if negative else [],
            'target':target,'magnitudes':mag,'mode':mode,'conditions':conditions,
            'duration':_duration(s), 'frequency':next((x for x in conditions if 'uma vez por' in x.lower()),None),
            'pa_linked_to_same_sentence':cost,
            'unknowns':(['TIPO_DE_ACAO'] if mode not in ('ATIVO_EXPLICITO','PASSIVO_EXPLICITO') else [])+
                (['DURACAO_EXATA'] if _duration(s)['status']=='TEMPORARIA_SEM_DURACAO_EXATA' else []),
            'evidence_status':'LITERAL_NO_PARECER_QMC04', 'rule_inference':False})
    # Verify every extracted span is actually a substring of literal evidence.
    bad=[(e['effect_id'],m['literal']) for e in effects for m in e['magnitudes'] if m['literal'] not in e['literal']]
    return {'status':'GROUNDING_APROVADO' if not bad else 'GROUNDING_DIVERGENTE',
       'schema':EFFECT_SCHEMA,'item_uuid':qualified['identity']['uuid'],'source_as_of':qualified['readback']['source_as_of'],
       'effects':effects, 'count':len(effects),'grounding_errors':bad,
       'decision':'TEXTO_DOCUMENTADO; APLICAÇÃO_MECÂNICA_NÃO_EXECUTADA'}


def energy_contract(qualified:dict,struct:dict)->dict:
    """Intercâmbio de dados, nunca cálculo de custo PA."""
    core=qualified['baseline_qmc03']['item']
    costs=core['costs']
    return {'kind':'CRAFT_ENERGY_INPUT_READONLY','contract':PA_INTERCHANGE,'provider_contract':None,
      'interface_state':'CANDIDATE_SEM_API_FORNECEDOR_VALIDADA','item':{'uuid':qualified['identity']['uuid'],
       'url':qualified['identity']['url'],'source_as_of':qualified['readback']['source_as_of'],
       'rank':qualified['identity']['rank'],'family':qualified['identity']['family']},
      'source_sha256':qualified['readback']['complete_content_sha256'],
      'costs_documented':{'daily':costs['daily'],'activation':costs['activation'],'ambiguous':costs['ambiguous']},
      'effects':struct.get('effects',[]),'rules':{'R-PA-DIA':'SOMENTE_NO_ESCOPO_PREVISTO'},
      'unresolved':['VALIDAR_FORNECEDOR_PA','HOMOLOGACAO_DO_CONTRATO_PA',
       'NAO_CALCULAR_AUSENCIAS'], 'return_official_cost':None,'activation_authorized':False}


def verify_energy_response(reply:dict,official_provider:dict|None=None)->dict:
    """Sem cadastro oficial autenticado não aceitar resposta, ainda que `kind=PROD`."""
    if not isinstance(reply,dict) or reply.get('kind') in ('FIXTURE_SIMULADA','MOCK','TEST'):
        return {'state':'FIXTURE_REJEITADA','official':False}
    if official_provider is None or not official_provider.get('authority_readback_verified'):
        return {'state':'FORNECEDOR_NAO_ATESTADO','official':False}
    if (reply.get('provider_id')!=official_provider.get('provider_id') or
            reply.get('contract_version')!=official_provider.get('contract_version')):
        return {'state':'FORNECEDOR_OU_VERSAO_DIVERGENTE','official':False}
    return {'state':'CONTRATO_COMPATIVEL_SEM_HOMOLOGACAO_AUTOMATICA','official':False,
            'pending':'Validação independente e release do motor competente'}


def version_semantic(before_raw:str,after_raw:str,uid:str,anchor_before:dict,anchor_after:dict)->dict:
    x=qmc04.compare_lab_revisions(before_raw,after_raw,uid,anchor_before,anchor_after)
    if x.get('status')!='DELTA_LAB_DOCUMENTAL_CONFERIDO' and x.get('status')!='MESMO_READBACK':
        return {'state':'VERSAO_BLOQUEADA','raw':x}
    mapped=[]
    for d in x.get('diff',[]):
        domain={'title':'IDENTIDADE_EDITORIAL','cost':'CUSTO_ENERGETICO_DOCUMENTAL_TEST',
                'effect':'EFEITO_MECANICO_TEXTUAL_TEST','editorial':'APENAS_EDITORIAL','other_content':'NAO_CLASSIFICADO'}.get(d['field'],'NAO_CLASSIFICADO')
        mapped.append({'domain':domain,**d})
    return {'state':'DELTA_LAB_INTERPRETADO' if mapped else 'SEM_DELTA', 'uuid':uid,
       'as_of_before':x.get('readback_before'),'as_of_after':x.get('readback_after'),
       'changes':mapped, 'mechanical_change':any(y['domain'] in ('CUSTO_ENERGETICO_DOCUMENTAL_TEST','EFEITO_MECANICO_TEXTUAL_TEST') for y in mapped),
       'physical_lab_only':True,'canonical_item_revision':False}


def compatibility(qa:dict,qb:dict,request:str)->dict:
    """Separa engenharia/documentação, mecânica, armazenagem, energia.
    Parecer nunca prova uso simultâneo concreto sem evidência de instalação/equipamento.
    """
    if any(x.get('status')!='ATENDIDO_PARECER_COM_LIMITE_DE_ATESTACAO' for x in (qa,qb)):
        return {'state':'PARECER_BLOQUEADO','domains':{}}
    base=qmc04.compatible_pair(qa,qb,request)
    q=request.casefold()
    domain={'physical':'INDETERMINADO','mechanical':'INDETERMINADO',
            'energy':'INDETERMINADO','documentary':'AMBOS_IDENTIFICADOS'}
    if 'anel dimensional' in q or 'empilhar' in q:
        domain['physical']=base['status']
    elif 'alimentar' in q or 'energia' in q:
        domain['energy']=base['status']
    elif 'matriz' in q or 'inscri' in q:
        domain['mechanical']=base['status']
    sources=[qa['identity']['url'],qb['identity']['url']]
    return {'state':base['status'],'question':request,'domains':domain,'sources':sources,
      'competent_rule_or_literal':base.get('reason'),'missing':base.get('missing',[]),
      'no_application_or_activation':True,'no_universal_combination_rule':True}


def media_receipt(qualified:dict,files:list[dict]|None=None)->dict:
    """Não transforma URL assinada em imagem inspecionada."""
    matches=[]
    for ref in qualified.get('media',[]):
        rel=(next((x for x in (files or []) if x.get('reference')==ref['reference']),None))
        if not rel or not rel.get('local_path'):
            matches.append({'reference':ref['reference'],'state':'URL_RESOLVIDA_BYTES_NAO_ADQUIRIDOS'
             if rel and rel.get('signed_url_obtained') else 'IMAGEM_REFERENCIADA_PENDENTE','bytes':None,'sha256':None,
             'inspection':'NÃO_REALIZADA'});continue
        path=Path(rel['local_path'])
        if not path.is_file():
            matches.append({'reference':ref['reference'],'state':'CAMINHO_INEXISTENTE','bytes':None,'sha256':None,'inspection':'NÃO_REALIZADA'});continue
        content=path.read_bytes()
        signature=content[:8]
        valid=(signature[:3]==b'\xff\xd8\xff' or signature==b'\x89PNG\r\n\x1a\n')
        matches.append({'reference':ref['reference'],'state':'BYTES_RECUPERADOS' if valid else 'FORMATO_NÃO_VALIDADO',
                        'bytes':len(content),'sha256':hashlib.sha256(content).hexdigest(),
                        'inspection':'PENDENTE_INSPECAO_VISUAL_AUTENTICA','mime_type':'image/jpeg' if signature[:3]==b'\xff\xd8\xff' else ('image/png' if valid else None)})
    return {'uuid':qualified['identity']['uuid'],'media':matches,'inspected':0,
        'rule_R_IMG':'INCOMPLETA_ATE_INSPECAO_VISUAL_REAL'}


def analyze(raw:str,url:str,anchor:dict|None=None)->dict:
    base=qmc04.qualified_chat(raw,url,anchor)
    if base.get('status')!='ATENDIDO_PARECER_COM_LIMITE_DE_ATESTACAO':
        return {'state':'BLOQUEADO','previous':base,'no_recipes':True}
    fx=structured_effects(base)
    if fx['status']!='GROUNDING_APROVADO':return {'state':'GROUNDING_BLOQUEADO','details':fx}
    return {'state':'QMC05_PARECER_DOCUMENTAL_TEST','version':VERSION,'qmc04':base,
      'structured_effects':fx,'energy_exchange':energy_contract(base,fx),
      'visual_evidence':media_receipt(base), 'production':'HOLD', 'new_recipes':0}


def conversational(x:dict)->str:
    if x.get('state')!='QMC05_PARECER_DOCUMENTAL_TEST':return 'PARECER BLOQUEADO: '+x.get('state','')
    q=x['qmc04'];i=q['identity'];costs=x['energy_exchange']['costs_documented'];fx=x['structured_effects']['effects']
    n=lambda arr:', '.join(str(v.get('value'))+' '+v.get('unit','') for v in arr) if arr else 'PENDENTE'
    s=[f"**{i['title']}** — {i['family']}; rank: {i['rank']}.",
       f"**Fonte Mestre:** {i['url']} (estado fornecido pela ferramenta: {q['readback']['source_as_of']}; atualização de hoje não comprovada).",
       '**Efeitos com evidência literal:**']
    for e in fx[:12]:
        mag='; '.join(m['literal'] for m in e['magnitudes']) or 'sem magnitude numérica documentada'
        cond=' / '.join(e['conditions']) or 'sem gatilho específico demonstrado'
        s.append(f"- {e['literal']} | magnitude: {mag}; modalidade: {e['mode']}; condição: {cond}; duração: {e['duration']['status']}.")
    s.extend([f"**PA/dia:** {n(costs['daily'])}. **PA/ativação:** {n(costs['activation'])}. **PA ambíguo:** {n(costs['ambiguous'])}.",
         f"**Imagem:** {x['visual_evidence']['rule_R_IMG']}; não inspecionada visualmente.",
         '**Interoperabilidade PA:** dados estruturados prontos; fornecedor e contrato real ainda não validados.',
         '**Uso/fabricação oficiais:** NÃO AUTORIZADOS. Receitas novas PROIBIDAS; produção HOLD.'])
    return '\n\n'.join(s)


def main():
    ap=argparse.ArgumentParser(description='CRAFT QMC05 qualificação read-only')
    ap.add_argument('--url',required=True);ap.add_argument('--readback',required=True);ap.add_argument('--anchor');ap.add_argument('--output')
    ap.add_argument('--pa-r28',action='store_true',help='TEST only: call external PA R27/R26')
    ap.add_argument('--pa-projeto-json',help='Optional proposed new item, TEST only')
    ns=ap.parse_args();raw=Path(ns.readback).read_text().rstrip('\n');anchor=json.loads(Path(ns.anchor).read_text()) if ns.anchor else None
    result=analyze(raw,ns.url,anchor)
    if ns.pa_r28:
        from pa_r28_native import output_json
        hypothesis=json.loads(Path(ns.pa_projeto_json).read_text(encoding='utf8')) if ns.pa_projeto_json else None
        s=output_json(result,hypothesis)
    else:s=conversational(result)
    if ns.output:Path(ns.output).write_text(s+'\n',encoding='utf8')
    else:print(s)
    if result['state']!='QMC05_PARECER_DOCUMENTAL_TEST':raise SystemExit(2)
if __name__=='__main__':main()
