#!/usr/bin/env python3
"""Consultor R05 com estado conversacional e interface wire TEST. Sem inferências de PA faltante."""
from __future__ import annotations
import json,re,unicodedata,sys,copy
from pathlib import Path
import pa_r05 as pa
from qmc_pa_r05_wire import wrap_candidate,strict_local_validation,native_qmc_probe

ATTR_ALIASES={'forca':'FOR','for':'FOR','destreza':'DES','des':'DES','constituicao':'CON','con':'CON',
             'inteligencia':'INT','int':'INT','sabedoria':'SAB','sab':'SAB','carisma':'CAR','car':'CAR'}

def norm(txt:str)->str:return ''.join(ch for ch in unicodedata.normalize('NFKD',txt.lower()) if not unicodedata.combining(ch))

def initial():return {'contract':'PA-CONSULTOR-STATE-R05-1','candidate_id':'MESTRE-R05-CANDIDATO-1',
                     'name':'Item proposto','family':'INDETERMINADA','effects':[],'pa_free_declared':None,
                     'historical_focus':None,'history':[],'only_test':True}

def _put(st,e):
    idx=next((i for i,x in enumerate(st['effects']) if x['id']==e['id']),None)
    if idx is None:st['effects'].append(e)
    else:st['effects'][idx].update(e)

def _historical_target(t:str):
    keys=[('bota caminho veloz','3edc2b324ede8135b199fd0cdbb5463c'),('amuleto tempo eterno','3edc2b324ede8132bbc8f857f4b276c4'),
          ('sabedoria ancestral','3edc2b324ede815699adc0412e96ea2b'),('colar cadente','3edc2b324ede810daba2cc509677856c'),
          ('amplificador de atributo','3c6c2b324ede82baa4a801de533a5975'),('adaga da serpente','3edc2b324ede811787a0de913622b14d')]
    return next((uid for alias,uid in keys if alias in t),None)

def interpret(st:dict,prompt:str)->tuple[dict,dict]:
    t=norm(prompt);st=copy.deepcopy(st);flags=[]
    hid=_historical_target(t)
    if hid:st['historical_focus']=hid;flags.append('HISTORICO')
    if 'espada' in t:st['family']='ARMA';st['name']='Espada mágica candidata'
    if 'armadura' in t:st['family']='ARMADURA';st['name']='Armadura mágica candidata'
    # +5 em Destreza, +10 SAB, +20 de dano, etc. Cuidado: +5 Reflexo não é +5 DES.
    for m in re.finditer(r'\+\s*(\d+(?:[.,]\d+)?)\s*(?:de\s*|em\s*)?(forca|destreza|constituicao|inteligencia|sabedoria|carisma|for|des|con|int|sab|car)\b',t):
        n=float(m.group(1).replace(',','.'));a=ATTR_ALIASES[m.group(2)]
        _put(st,{'id':'ATR_'+a,'kind':'ATRIBUTO','attribute':a,'magnitude':n,'mode':'PASSIVO_DIARIO','conditions':'enquanto equipado; bônus aditivo a validar'});flags.append('ATRIBUTO')
    # Permite também a forma natural: 'aumenta minha Destreza em +5'.
    for m in re.finditer(r'\b(forca|destreza|constituicao|inteligencia|sabedoria|carisma|for|des|con|int|sab|car)\s*(?:em\s*)?\+\s*(\d+(?:[.,]\d+)?)',t):
        a=ATTR_ALIASES[m.group(1)];n=float(m.group(2).replace(',','.'))
        _put(st,{'id':'ATR_'+a,'kind':'ATRIBUTO','attribute':a,'magnitude':n,
                 'mode':'PASSIVO_DIARIO','conditions':'enquanto equipado; bônus aditivo a validar'});flags.append('ATRIBUTO')
    m=re.search(r'\+\s*(\d+(?:[.,]\d+)?)\s*(?:de\s*)?dano',t)
    if m:
        _put(st,{'id':'DANO_BONUS','kind':'dano_passivo_por_acerto','magnitude':float(m.group(1).replace(',','.')),
                 'mode':'PASSIVO_DIARIO','frequency':'todos os ataques elegíveis','conditions':'acerto necessário'});flags.append('DANO')
    m=re.search(r'\brd\s*(\d+(?:[.,]\d+)?)',t)
    if m:
        cond='ataques elementais' if 'elemental' in t else 'não documentada'
        _put(st,{'id':'RD','kind':'rd_elemental' if 'elemental' in t else 'rd_universal',
                 'magnitude':float(m.group(1).replace(',','.')),'mode':'PASSIVO_DIARIO','conditions':cond});flags.append('RD')
    if ('movimenta' in t or 'desloca' in t or 'mobilidade' in t) and ('habilidade' in t or 'ativ' in t):
        # A magnitude representa apenas um marcador 1 efeito, nunca transformado em taxa por metro.
        _put(st,{'id':'MOBILIDADE_ATIVA','kind':'deslocamento_ativo','magnitude':1,'mode':'ATIVO_POR_USO',
                 'conditions':'alcance/duração devem ser informados','frequency':'não documentada'});flags.append('MOBILIDADE_ATIVA')
    once=('uma vez por dia' in t or '1x/dia' in t or '1 vez por dia' in t)
    if once:
        dmg=next((e for e in st['effects'] if e['id']=='DANO_BONUS'),None)
        if dmg:
            explicit=('ativ' in t or 'acion' in t or 'uso' in t)
            dmg['mode']='ATIVO_POR_USO' if explicit else 'CONDICIONAL_DIARIO'
            dmg['kind']='dano_ativo' if explicit else 'dano_passivo_por_acerto'
            dmg['frequency']='1x/dia';dmg['conditions']='gatilho e duração pendentes'
            flags.append('DANO_LIMITADO_1_DIA')
    if 'por turno' in t:
        dmg=next((e for e in st['effects'] if e['id']=='DANO_BONUS'),None)
        if dmg:dmg['frequency']='por turno';flags.append('FREQ_TURNO')
    if '10 minutos' in t:
        for e in st['effects']:
            if e['mode']=='ATIVO_POR_USO':e['duration']='10 minutos'
        flags.append('DURACAO')
    m=re.search(r'\b(\d+)\s*pa\s*livr',t)
    if m:st['pa_free_declared']=int(m.group(1));flags.append('PA_LIVRE')
    send='craft' in t and any(v in t for v in ['envi','mande','pass','encaminh','export'])
    if send:flags.append('CRAFT_EXPORT')
    result=pa.component_model(st['effects']);historico=pa.history(st['historical_focus']) if st['historical_focus'] else None
    lines=[]
    if 'ATRIBUTO' in flags:
        lines.append(f"Regra do Mestre: bônus permanentes de atributo custam {result['daily_pa_subtotal_identified']:g} PA/dia nesta composição, 5 PA/dia por ponto.")
    if 'DANO' in flags or 'DANO_LIMITADO_1_DIA' in flags:lines.append('Dano adicional identificado. Custo energético por acerto ou por ativação não possui coeficiente validado; frequência/duração não viram tarifa automaticamente.')
    if 'RD' in flags:lines.append('RD documentada como magnitude de efeito; PA/dia para RD específica ainda não identificável.')
    if 'MOBILIDADE_ATIVA' in flags:lines.append('Mobilidade ativável reconhecida. PA/uso ainda depende de fonte comparável adequada ou decisão do Mestre.')
    if historico:
        dl=historico['pa_daily']['value']
        lines.append('HISTÓRICO: '+historico['item']+', PA diário literal/interpretado: '+(str(dl)+' PA/dia' if dl is not None else 'indeterminado')+'. Fonte: '+historico['url'])
        historical_act=historico.get('pa_activation',{}).get('value')
        if historical_act is not None:lines.append(f'PA de ativação documentado: {historical_act} PA/uso; não adicionar automaticamente ao valor diário.')
        if historico.get('activation_abilities'):
            lines.append('Ativações específicas: '+', '.join(str(e['value'])+' PA/uso ('+e.get('name','habilidade')+')' for e in historico['activation_abilities']))
        anch=next((a for a in pa.ATTR_ANCHORS if a['uuid']==historico['id']),None)
        if anch and anch['surface']=='PARTY_MESTRE_ESPELHO':lines.append('PROVENIÊNCIA: Espelho da Party; não é amostra Mestre independente e não autoriza atualização de ficha Party.')
        audit=historico.get('audit_attribute_rule')
        if audit and audit['issues']:lines.append('CONFLITO COM REGRA DE ATRIBUTOS: '+', '.join(i['condition']+' (faltam no mínimo '+str(i['deficit_pa_day_at_least'])+' PA/dia)' for i in audit['issues']))
        if historico.get('R05_reconciliation'):lines.append('A unidade histórica de 35 de PA é ambígua; não homologar como PA/dia.')
    if st['pa_free_declared'] is not None:
        lines.append('PA Livre declarado: '+str(st['pa_free_declared'])+'. Sem custo completo e sem semântica diária competente, suficiência para uso global é indeterminada.')
    if not lines:lines.append('Consulte um item/efeito reconhecido, com magnitude, duração e frequência. Custos desconhecidos serão preservados como indeterminados.')
    if historico and not st['effects']:
        if historico.get('R05_reconciliation'):
            lines.append('Unidade de PA do item histórico NÃO IDENTIFICADA em R05; R03 permanece como registro, não tarifa diária aprovada.')
    elif result['daily_total_pa'] is None:
        lines.append('Custo diário TOTAL: INDETERMINADO; não usar o subtotal de atributos como preço integral do item.')
    else:lines.append('Custo diário TOTAL no escopo descrito: '+str(result['daily_total_pa'])+' PA/dia ('+result['daily_total_status']+').')
    payload=receipt=probe=None
    if send:
        candidate={'candidate_id':st['candidate_id'],'evidence_type':'USER_EXPERIMENTAL_SPEC','name':st['name'],
                   'qmc_family':st['family'],'effects':st['effects']}
        payload=wrap_candidate(candidate);receipt=strict_local_validation(payload);probe=native_qmc_probe(payload)
        lines.append('Parecer TEST exportado para QMC-02. Adaptador R05 aceitou envelope; VALIDADOR NATIVO ORIGINAL permanece NÃO CONTRATADO e não aprovou o custo.')
    st['history'].append({'user':prompt,'actions':flags})
    return st,{'answer':' '.join(lines),'flags':flags,'mode':'HISTORICO' if hid else 'PROPOSTA',
               'energy':result,'source_historical':historico,'historical_daily_pa_usable':(None if historico and historico.get('R05_reconciliation') else historico['pa_daily']['value'] if historico else None),'craft_test_payload':payload,'craft_test_receipt':receipt,
               'craft_native_probe':probe,'no_new_recipe':True,'production_hold':True,'state':st}

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--state',default=None);p.add_argument('queries',nargs='+');a=p.parse_args()
 state=json.loads(Path(a.state).read_text('utf8')) if a.state and Path(a.state).exists() else initial()
 for q in a.queries:
    state,res=interpret(state,q)
    print(json.dumps({'query':q,'answer':res['answer'],'mode':res['mode'],'PA_diario':res['energy']['daily_total_pa'],
       'craft_native_accepted':(res['craft_native_probe'] or {}).get('native_accepted',None)},ensure_ascii=False))
 if a.state:Path(a.state).write_text(json.dumps(state,indent=2,ensure_ascii=False)+'\n','utf8')
