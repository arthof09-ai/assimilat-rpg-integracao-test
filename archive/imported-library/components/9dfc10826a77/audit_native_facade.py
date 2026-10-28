#!/usr/bin/env python3
"""Auditor aditivo, SEM WRITER, para exportações Markdown de R75/R76 e de fachadas TEST.

Uso: python audit_native_facade.py --engine R76.md --face R88.md
Não executa motores nem consulta Notion; requer exportações reais feitas por um operador autorizado.
"""
import argparse
import json
import re
from pathlib import Path

ATTRS = ('FOR','DES','CON','INT','SAB','CAR')


def state_from_engine(markdown: str) -> dict:
    match = re.search(r'## ESTADO ATIVO INTEGRAL DO MOTOR[^\n]*', markdown)
    if not match:
        raise ValueError('Motor: seção de estado integral ausente')
    section = markdown[match.end():].split('<details', 1)[0]
    chunks = re.findall(r'^STATE_\d{3}: (.*)$', section, re.M)
    if not chunks:
        raise ValueError('Motor: chunks STATE_000 ausentes')
    state = json.loads(''.join(chunks))
    if set(state) != {'NORMAL','TRANSFORM','LOCKS'}:
        raise ValueError('Contrato integral NORMAL/TRANSFORM/LOCKS incompleto')
    return state


def active_fields(markdown: str) -> dict:
    # Apenas a fachada antes do separador do conteúdo legado; nunca busca no histórico!
    active = markdown.split('\n---\n',1)[0]
    pairs = re.findall(r'^\*\*([^*]+?):\*\*\s*(.*)$',active,re.M)
    keys = [k.strip() for k,_ in pairs]
    if len(keys) != len(set(keys)):
        raise ValueError('Fachada com campos ativos duplicados, rejeitada sem efeitos')
    return {k.strip():v.strip() for k,v in pairs}


def attr_value(field: str | None, attr: str) -> str | None:
    if field is None:
        return None
    found = re.search(r'(?<!\w)' + re.escape(attr) + r':\s*(\d+)',field)
    return found.group(1) if found else None


def audit(engine: str, facade: str) -> dict:
    st=state_from_engine(engine)
    f=active_fields(facade)
    n=st['NORMAL']; tr=st['TRANSFORM']; locks=st['LOCKS']
    verdict=[]
    def ck(key,want,got):
        verdict.append({'field':key,'expected':str(want),'observed':got,'pass':got==str(want)})
    for key in ATTRS:
        ck('NORMAL.'+key,n['attrs'][key],attr_value(f.get('ATRIBUTOS ATIVOS'),key))
        ck('INITIAL.'+key,n['initial_attrs'][key],attr_value(f.get('ATRIBUTOS INICIAIS TEST'),key))
        ck('OVERLAY.'+key,tr['overlay'][key],attr_value(f.get('OVERLAY'),key))
        ck('FORM.'+key,tr['attrs'][key],attr_value(f.get('ATRIBUTOS DA FORMA'),key))
    if 'attribute_layers' in n:
        for source,dest in [('equipment','CAMADA EQUIPADA'),('permanent_title','CAMADA TÍTULO PERMANENTE'),('temporary','CAMADA TEMPORÁRIA')]:
            for key in ATTRS:
                ck(source+'.'+key,n['attribute_layers'][source][key],attr_value(f.get(dest),key))
    ck('LEVEL',n['level'],re.match(r'\d+',f.get('NÍVEL','')).group(0) if re.match(r'\d+',f.get('NÍVEL','')) else None)
    ck('RACE',n['race'],f.get('RAÇA'))
    ck('POINTS_PER_LEVEL',n['normal_rate'],f.get('PONTOS POR NÍVEL'))
    for label,want in [('FF',n['derived']['ff']),('VIDA MÁXIMA',n['hp_max']),('VIDA ATUAL',n['hp_current']),('PA MÁXIMO',n['pa_max']),('PA ATUAL',n['pa_current']),('PA COMPROMETIDO',n['pa_committed']),('PA LIVRE',n['pa_free']),('CA',n['derived']['ca']),('CD MAGIA',n['derived']['magic_cd']),('ATAQUE LUTA FOR',n['derived']['attack_bonus_luta_for']),('DADOS ATAQUE POR RANK',n['derived']['attack_dice_by_rank']),('MARCOS FF LOCKED',len(locks['milestones']))]:
        ck(label,want,f.get(label))
    for label,want in [
        ('VIDA BASE/NATURAL/PERMANENTE',f"{n['hp_initial']} / {n['hp_natural']} / {n['hp_permanent']}"),
        ('PROFICIÊNCIA LUTA/MAGIA',f"{n['luta_prof']} / {n['magic_prof']}"),
        ('DANO ARMA BASE/FORÇA FF TEST',f"{n['derived']['weapon_damage_base_fixture']} / {n['derived']['weapon_damage_plus_ff_fixture']}"),
        ('BÔNUS FF DANO/VIDA',f"{n['derived']['ff_bonus_damage']} / {n['derived']['ff_bonus_life']}"),
        ('CAP / NÍVEL EFETIVO',f"{tr['spirit']['cap']} / {tr['effective_level']}"),
        ('BAP/TAP CARRY',f"{tr['spirit']['bap']} / {tr['tap_carry_half_units']}"),
        ('FF/CA/CD DA FORMA',f"{tr['derived']['ff']} / {tr['derived']['ca']} / {tr['derived']['magic_cd']}"),
        ('DANO BONUS FF/VIDA FF FORMA',f"{tr['derived']['ff_bonus_damage']} / {tr['derived']['ff_bonus_life']}"),
        ('VIDA FORMA BONUS MÁXIMO/ATUAL',f"{tr['hp_bonus_max']} / {tr['hp_bonus_current']}"),
        ('PA FORMA BONUS MÁXIMO/ATUAL',f"{tr['pa_bonus_max']} / {tr['pa_bonus_current']}"),
    ]: ck(label,want,f.get(label))
    ck('ACTIVATION',tr['activation_state'],f.get('ESTADO DE ATIVAÇÃO'))
    if 'attribute_layers' in n:
        ck('LOCK_HISTORY',locks['history'][0],f.get('HISTÓRICO MARCOS'))
    return {'verified':sum(x['pass'] for x in verdict),'total':len(verdict),'all_pass':all(x['pass'] for x in verdict),'failures':[x for x in verdict if not x['pass']],'checks':verdict,'scope':'only fields represented in active facade; no media, history or Party certification'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--engine',type=Path,required=True)
    p.add_argument('--face',type=Path,required=True)
    p.add_argument('--out',type=Path)
    a=p.parse_args()
    result=audit(a.engine.read_text(encoding='utf8'),a.face.read_text(encoding='utf8'))
    text=json.dumps(result,ensure_ascii=False,indent=2)
    if a.out: a.out.write_text(text,encoding='utf8')
    else: print(text)
    raise SystemExit(0 if result['all_pass'] else 1)
