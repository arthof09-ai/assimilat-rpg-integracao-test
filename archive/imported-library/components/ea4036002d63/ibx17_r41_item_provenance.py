"""IBX-17 R41-R50 / additive read-only item provenance and preview layer.

NO Notion writer. NO normative rules. NO claim of current equipment use based on
item presence. Designed to coexist with R36 reader, R39A native archive review,
and R40 native TEST readback. The historical motor remains authoritative.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, asdict
from decimal import Decimal
from typing import Any

class EvidenceHold(ValueError):
    pass

PAGE_REF = re.compile(r'<(mention-page|page)\s+url="(https://app\.notion\.com/p/[0-9a-f]{32})"[^>]*?(?:/>|>(.*?)</page>)', re.I)
UUID = re.compile(r'/p/([0-9a-f]{32})', re.I)
SUPPORTED = {'FOR','DES','CON','INT','SAB','CAR','PA','CA','CD','REF','VIDA','DANO','ALCANCE','CATEGORIA_DANO'}
EQUIP_STATUS = {'ATIVO_COMPROVADO', 'ARMAZENADO', 'INATIVO', 'DESCONHECIDO'}

@dataclass(frozen=True)
class Reference:
    page_id: str
    url: str
    kind: str
    title_literal: str | None
    line: int

@dataclass(frozen=True)
class Effect:
    source_id: str
    source_url: str
    source_sha256: str
    line: int
    literal: str
    value: str
    domain: str
    mode: str
    condition: str
    applied_to_total: str


def content_of_fetch(markdown: str) -> str:
    if not isinstance(markdown,str) or markdown.count('<content>')!=1 or markdown.count('</content>')!=1:
        raise EvidenceHold('NOTION_CONTENT_BOUNDARY_AMBIGUOUS')
    return markdown.split('<content>',1)[1].split('</content>',1)[0].strip('\n')


def sha256(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def parse_references(body: str) -> list[Reference]:
    """Preserves repeated occurrences and distinguishes mention from child page.

    An actual child page is NOT safe to archive as a new page or as a copied link.
    """
    if not isinstance(body,str): raise EvidenceHold('NON_TEXT_SHEET')
    found=[]
    for m in PAGE_REF.finditer(body):
        kind,url,title=m.groups()
        found.append(Reference(UUID.search(url).group(1),url,kind, title,body.count('\n',0,m.start())+1))
    return found


def unique_references(refs: list[Reference]) -> list[dict]:
    groups={}
    for r in refs:
        k=(r.page_id,r.kind)
        if k not in groups:
            groups[k]={'page_id':r.page_id,'url':r.url,'kind':r.kind,'title_literal':r.title_literal,'lines':[r.line]}
        else:groups[k]['lines'].append(r.line)
    return list(groups.values())


def _visible_text(line: str) -> str:
    return re.sub(r'<[^>]*>', '', line).replace('**','').replace('*','').strip()


def _domain(line: str, context: str, *, position: int|None=None) -> str:
    if position is not None:
        tail=line[position:]
        aft=re.search(r'^\+?\s*\d+(?:d\d+)?\s+(?:de\s+)?(PA|intelig[eê]ncia|destreza|sabedoria|CD|CA|vida|REF)\b',tail,re.I)
        if aft:
            target=aft.group(1).lower()
            return {'pa':'PA','inteligência':'INT','inteligencia':'INT','destreza':'DES','sabedoria':'SAB','cd':'CD','ca':'CA','vida':'VIDA','ref':'REF'}[target]
        prefix=line[max(0,position-40):position].lower()
        if 'cd ' in prefix or 'cd do usuário' in prefix:return 'CD'
    s=(line+' '+context).lower()
    if 'inteligência' in s or 'inteligencia' in s: return 'INT'
    if 'destreza' in s: return 'DES'
    if 'reflex' in s: return 'REF'
    if 'sabedoria' in s: return 'SAB'
    if 'carisma' in s: return 'CAR'
    if 'constituição' in s or 'constituicao' in s: return 'CON'
    if 'força física' in s: return 'FOR'
    if 'de vida' in s: return 'VIDA'
    if 'cd ' in s or ' cd' in s or 'cd:' in s: return 'CD'
    if 'alcance' in s: return 'ALCANCE'
    if 'categoria de dano' in s: return 'CATEGORIA_DANO'
    if 'pa' in s and ('de pa' in s or ' pa ' in ' '+s+' '): return 'PA'
    if 'dano' in s or re.search(r'\d+d\d+',s): return 'DANO'
    return 'UNCLASSIFIED'


def extract_effects(item_markdown: str, *, source_url: str, status: str='DESCONHECIDO') -> dict:
    """Conservative documentary effect extraction; does not infer activation.

    Complex rules, dice and unknown numeric fields are preserved literally and
    not added to integer character totals. Returns a source-specific inventory.
    """
    if status not in EQUIP_STATUS: raise EvidenceHold('ITEM_STATUS_INVALID')
    match=UUID.search(source_url)
    if not match:raise EvidenceHold('ITEM_SOURCE_URL_INVALID')
    source_id=match.group(1)
    body=content_of_fetch(item_markdown) if '<content>' in item_markdown else item_markdown
    source_hash=sha256(body)
    lines=body.splitlines()
    effects=[]
    scope='CONDITION_NOT_ESTABLISHED'
    for i,raw in enumerate(lines,1):
        literal=_visible_text(raw)
        if not literal:continue
        # Heading fields are not themselves effects.
        if re.search(r'\b(passiv[oa])\b',literal,re.I): scope='PASSIVE_DESCRIBED'
        if re.search(r'\b(ativ[oa])\b',literal,re.I): scope='ACTIVE_REQUIRES_ACTION'
        if re.search(r'\b(1x/dia|1x/semana)\b',literal,re.I): scope='LIMITED_USE'
        candidates=[]
        # Dice: preserve exact notations; never collapse into unconditional integer.
        for m in re.finditer(r'(?<!\w)(\+\s*\d+d\d+(?:\s*\+\s*\d+)?)(?!\w)',literal,re.I):
            candidates.append((m.group(1).replace(' ',''),'DICE',m.start()))
        # Signed integers with documentary context.
        for m in re.finditer(r'(?<![\w\d])(\+\s*\d+)(?![\dd])',literal,re.I):
            val=m.group(1).replace(' ','')
            # Don't duplicate +2 in +2d6+2: match starting at dice end? avoid dice notation members.
            pre=literal[max(0,m.start()-5):m.start()]
            aft=literal[m.end():m.end()+3]
            if re.match(r'[dD]\d',aft) or (pre and re.search(r'\d[dD]\d+$',pre)):continue
            candidates.append((val,'NUMBER',m.start()))
        # Explicit prose 'concede 130 de PA' (not signed).
        for m in re.finditer(r'\b(?:concede|ganha|adiciona|aumenta(?:\s+a\s+CD\s+do\s+usuário\s+em)?)\s*\+?(\d+)\s+de\s+(PA|intelig[eê]ncia|CA|CD)\b',literal,re.I):
            val='+'+m.group(1)
            candidates.append((val,'NUMBER',m.start()))
        for m in re.finditer(r'\b(gasto|custo)\s*:\s*(\d+)\s*PA\b',literal,re.I):
            candidates.append((m.group(2),'COST',m.start(2)))
        # PA specifically as an effect when source says concede +130 de PA;
        # costs are separate, not character PA bonuses.
        if not candidates: continue
        seen=set()
        for val,typ,pos in candidates:
            if (val,typ,pos) in seen:continue
            seen.add((val,typ,pos))
            contextual=literal
            d=_domain(contextual,scope,position=pos)
            is_cost=bool(re.search(r'\b(gasto|gastar|custo|sofre)\b', literal, re.I))
            mode='COST' if is_cost or typ=='COST' else ('DICE_OR_FORMULA' if typ=='DICE' else 'LITERAL_MODIFIER')
            if d=='UNCLASSIFIED':mode='UNCLASSIFIED_NUMBER'
            condition=('EQUIPAMENTO_ATIVO_COMPROVADO' if status=='ATIVO_COMPROVADO' else
                       'EQUIPAMENTO_ARMAZENADO' if status=='ARMAZENADO' else
                       'EQUIPAMENTO_INATIVO' if status=='INATIVO' else 'EQUIPAMENTO_SEM_ESTADO_COMPROVADO')
            if scope in ('ACTIVE_REQUIRES_ACTION','LIMITED_USE'):
                condition += ';'+scope
            if 'sombra' in literal.lower():condition+=';SOMENTE_SOMBRA_SE_APLICAVEL'
            effects.append(asdict(Effect(source_id,source_url,source_hash,i,literal,val,d,mode,condition,'NAO_COMPROVADO')))
    return {'item_id':source_id,'item_url':source_url,'source_excerpt_sha256':source_hash,
            'status':status,'effects':effects,'count':len(effects),'interpretation':'READ_ONLY_DOCUMENTARY_NO_APPLY'}


def make_mention_summary(label: str, item: dict, *, item_ref: str, applicability: str='PENDENTE') -> dict:
    if not item_ref or item['item_id'] not in item_ref:raise EvidenceHold('SOURCE_MENTION_MISMATCH')
    if applicability not in {'INCLUIDO_COMPROVADO','CONDICIONAL','NAO_INCLUIDO','PENDENTE'}:
        raise EvidenceHold('APPLICABILITY_INVALID')
    distinct=[]
    seen=set()
    for e in item['effects']:
        # preserve same value with different conditions/lines
        key=(e['literal'],e['value'],e['domain'],e['mode'])
        if key not in seen:
            seen.add(key);distinct.append({'literal':e['literal'],'dominio':e['domain'],
                                           'valor_literal':e['value'],'natureza':e['mode'],
                                           'condicao':e['condition'],'linha_fonte':e['line']})
    return {'item_id':item['item_id'],'item_label':label,'mention_original':item_ref,
            'fonte_sha256':item['source_excerpt_sha256'],'bonus_objetivos':distinct,
            'aplicabilidade_na_ficha':applicability,'equip_state':item['status'],
            'snapshot_state':'EXTRATO_CONGELADO_NESTA_VERSAO','new_item_page_created':False}


def reconcile_numeric(total: int, natural: int|None, items: list[dict], domain: str) -> dict:
    if domain not in SUPPORTED:raise EvidenceHold('DOMAIN_NOT_ADMITTED')
    if natural is None:return {'domain':domain,'status':'HOLD_NATURAL_UNKNOWN', 'total':total}
    if not isinstance(total,int) or not isinstance(natural,int):raise EvidenceHold('NON_INTEGER_STAT')
    amount=0;ids=set();evidence=[]
    for item in items:
        k=item['item_id']
        if k in ids:raise EvidenceHold('DUPLICATED_ITEM_EFFECT:'+k)
        ids.add(k)
        if item['equip_state']=='DESCONHECIDO' and any(e['dominio']==domain for e in item['bonus_objetivos']):
            raise EvidenceHold('UNKNOWN_EQUIP_EFFECT:'+k)
        if item['equip_state']!='ATIVO_COMPROVADO':continue
        if item['aplicabilidade_na_ficha']!='INCLUIDO_COMPROVADO':
            raise EvidenceHold('BONUS_INCIDENCE_UNVERIFIED:'+k)
        for e in item['bonus_objetivos']:
            if e['dominio']!=domain or e['natureza']!='LITERAL_MODIFIER':continue
            if not re.fullmatch(r'\+\d+',e['valor_literal']):continue
            if ';ACTIVE_REQUIRES_ACTION' in e['condicao'] or ';LIMITED_USE' in e['condicao']:continue
            amount+=int(e['valor_literal']);evidence.append((k,e['linha_fonte'],e['valor_literal']))
    computed=natural+amount
    return {'domain':domain,'published':total,'natural':natural,'bonus':amount,
            'computed':computed,'difference':total-computed,'consistent':total==computed,
            'evidence':evidence,'status':'MATCH' if total==computed else 'CONFLICT'}


def arithmetic_mismatches(body: str) -> list[dict]:
    """Checks explicit simple non-dice expressions. Does not change source."""
    out=[]
    for n,line in enumerate(body.splitlines(),1):
        for match in re.finditer(r'(?<![\d])((?:\d+\s*\+\s*)+\d+)\s*=\s*(\d+)',line):
            terms=[int(k) for k in re.findall(r'\d+',match.group(1))]
            shown=int(match.group(2));computed=sum(terms)
            if computed!=shown:out.append({'line':n,'expression':match.group(0),
                                            'computed':computed,'published':shown,'diff':shown-computed})
    return out


def freeze_archive_snapshot(sheet_id: str, active_body: str, summaries: list[dict],
                            *, original_reference_ids: list[str]) -> dict:
    """A local proposal for a version snapshot, not a Notion write or restorable block tree."""
    if not UUID.search('https://app.notion.com/p/'+sheet_id.replace('-','')):raise EvidenceHold('SHEET_ID_INVALID')
    if not isinstance(active_body,str) or not active_body:raise EvidenceHold('ACTIVE_BODY_MISSING')
    if '<page url=' in active_body:raise EvidenceHold('CHILD_PAGES_NEED_NATIVE_INTEGRITY_GATE')
    extracted={x.page_id for x in parse_references(active_body) if x.kind=='mention-page'}
    if set(original_reference_ids)-extracted:raise EvidenceHold('MISSING_ORIGINAL_MENTION')
    if any(s['item_id'] not in extracted for s in summaries):raise EvidenceHold('SUMMARY_WITHOUT_MENTION')
    by_id=[s['item_id'] for s in summaries]
    if len(by_id)!=len(set(by_id)):raise EvidenceHold('DUPLICATE_SUMMARY')
    return {'sheet_id':sheet_id,'active_sha256':sha256(active_body),
            'immutable_extratos_sha256':sha256(json.dumps(summaries,sort_keys=True,ensure_ascii=False)),
            'summaries':summaries,'native_write':False,'ready_for_native_writer':False,
            'reason':'REQUIRES_R39A_NATIVE_FIDELITY_AND_APPROVAL'}


def request_gate(*, surface:str, approved:bool, synthetic:bool,
                 source_stable:bool, history_preserved:bool) -> str:
    if surface=='PARTY' or surface=='O_PRIMEIRO':return 'HOLD_PARTY_OR_PRIMEIRO_NO_WRITE'
    if not synthetic:return 'HOLD_OFFICIAL_SHEET_REQUIRES_SPECIFIC_APPROVAL_AND_NAC_PASS'
    if not source_stable:return 'HOLD_SOURCE_DRIFT'
    if not history_preserved:return 'HOLD_HISTORY_INTEGRITY'
    return 'TEST_MUTATION_ELIGIBLE_ONLY' if approved else 'NO_WRITE_REFUSAL'
