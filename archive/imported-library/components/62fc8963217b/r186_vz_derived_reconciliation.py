"""IBX-17 R186: source-bound VZ sandbox HP/PA & FF table reconciliation.

A parser for the existing NORMAL-STATS-VZ-08 native Notion enhanced Markdown;
no mutation, no BAP exposure, no campaign write or actual assimilation.
"""
from __future__ import annotations
import html
import re

SOURCE_ID='3f2c2b324ede8168b50ee4254134d821'
SOURCE_VERSION='2026-10-07T21:52:35.997Z'
ACTORS=('Serah','Darek','Nym','Urosh','Sel-Myr','Kael','Rhovan','Asha')
LIFE_HEADER='## FECHAMENTO VIDA/ALMA TRANSFORMADAS — v1.1'
FF_HEADER='## APLICAÇÃO FF-LOCK — v1.2'

class SourceBoundHold(ValueError): pass


def _table_between(text: str, start: str, end: str | None):
    if text.count(start)!=1 or (end is not None and text.count(end)!=1):
        raise SourceBoundHold('MISSING_OR_DUPLICATE_SECTION')
    seg=text.split(start,1)[1]
    if end:seg=seg.split(end,1)[0]
    matches=re.findall(r'<table\b[^>]*>(.*?)</table>',seg,re.DOTALL)
    if len(matches)!=1:raise SourceBoundHold('NOT_EXACTLY_ONE_TABLE')
    rows=[]
    for match in re.findall(r'<tr\b[^>]*>(.*?)</tr>',matches[0],re.DOTALL):
        cells=re.findall(r'<t[dh]\b[^>]*>(.*?)</t[dh]>',match,re.DOTALL)
        vals=[html.unescape(re.sub('<[^>]+>','',v)).strip() for v in cells]
        if not vals or any(not v for v in vals):raise SourceBoundHold('EMPTY_CELL')
        rows.append(vals)
    if len(rows)!=9:raise SourceBoundHold('ACTOR_DENOMINATOR_NOT_8')
    return rows


def reconcile_source(*,native_markdown: str,source_id: str,source_version: str):
    if (source_id,source_version)!=(SOURCE_ID,SOURCE_VERSION):
        raise SourceBoundHold('SOURCE_ID_OR_VERSION_NOT_PINNED')
    if not isinstance(native_markdown,str):raise SourceBoundHold('MALFORMED_SOURCE')
    life=_table_between(native_markdown,LIFE_HEADER,FF_HEADER)
    ff=_table_between(native_markdown,FF_HEADER,None)
    if life[0]!=['Personagem','Vida transformada','Alma/PA transformada','Regime']:
        raise SourceBoundHold('LIFE_HEADER_CHANGED')
    if ff[0]!=['Personagem','Vida normal + FF','CA normal + FF','Dano FF normal',
                'Vida transformada + FF','CA transformada + FF','Dano FF transformado']:
        raise SourceBoundHold('FF_HEADER_CHANGED')
    life_data={}; ff_data={}
    for row in life[1:]:
        if len(row)!=4 or row[0] in life_data:raise SourceBoundHold('DUPLICATE_LIFE_ROW')
        if not all(x.isdecimal() for x in row[1:3]):raise SourceBoundHold('INVALID_LIFE_VALUE')
        life_data[row[0]]={'hp':int(row[1]),'pa':int(row[2]),'regime':row[3]}
    for row in ff[1:]:
        if len(row)!=7 or row[0] in ff_data:raise SourceBoundHold('DUPLICATE_FF_ROW')
        if not all(re.fullmatch(r'\+?\d+',x) for x in row[1:]):raise SourceBoundHold('INVALID_FF_VALUE')
        ff_data[row[0]]=dict(zip(('hp_normal_plus_ff','ca_normal_plus_ff','damage_ff_normal',
                                   'hp_transform_plus_ff','ca_transform_plus_ff','damage_ff_transform'),
                                   map(lambda n:int(n.lstrip('+')),row[1:])))
    if set(life_data)!=set(ACTORS) or set(ff_data)!=set(ACTORS):
        raise SourceBoundHold('ACTOR_SET_MISMATCH')
    if 'Espírito ON5' not in life_data['Darek']['regime'] or 'd20 conservador' not in life_data['Darek']['regime']:
        raise SourceBoundHold('DAREK_CONSERVATIVE_TIER_ABSENT')
    for a in ACTORS:
        if ff_data[a]['hp_transform_plus_ff']<life_data[a]['hp']:
            raise SourceBoundHold('FF_TRANSFORM_HP_BELOW_SOURCE_BASE')
    return {'scope':'VZ_SANDBOX_SOURCE_RECONCILED_NOT_CAMPAIGN','source_id':source_id,
            'source_version':source_version,'source_only_self_review':True,
            'native_writes':0,'host_confirmation':False,'actor_count':8,
            'actors':{a:{'transform_base':life_data[a],'ff_integrated':ff_data[a]} for a in ACTORS},
            'remaining':'equipment/title/condition, source version and campaign not certified'}
