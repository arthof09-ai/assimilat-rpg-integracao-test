"""Read-only layout discovery for exported Notion enhanced Markdown.

Never rewrites or corrects player text. Any compound attribute is an unresolved claim,
not a license to select one number. Not a live Notion adapter or authorized writer.
"""
from __future__ import annotations
import re
from typing import Any
from levelup_engine import ATTRS, RANKS

ALIAS = {"força":"FOR", "destreza":"DES", "constituição":"CON", "inteligência":"INT",
         "sabedoria":"SAB", "carisma":"CAR"}
ROMAN = {"I":1, "II":2, "III":3, "IV":4, "V":5}


def discover_exported_markdown(source: str) -> dict[str, Any]:
    """Return a candidate map only; never emit a write mapping."""
    if not isinstance(source, str) or not source.strip():
        raise ValueError("Exportação de ficha vazia")
    raw = source.replace('<br>', '\n').replace('<br/>', '\n').replace('<br />', '\n')
    # Readable plain-text scan; original source must remain unchanged by callers.
    raw = re.sub(r'<[^>]+>', '', raw)
    level_hits=[]
    for match in re.finditer(r"Espiritualista\s+Demoníaco\s+(Ouro\s+Negro|Lendário|Bronze|Prata|Ouro)\s+([IVX]+)\b", raw, re.I):
        rank = next((x for x in RANKS if x.casefold()==re.sub(r'\s+', ' ', match.group(1)).strip().casefold()),None)
        star = ROMAN.get(match.group(2).upper())
        if rank and star:
            level_hits.append({"rank":rank,"star":star,"ordinal":RANKS.index(rank)*5+star,
                               "text":match.group(0)})
    anchors=[]
    for term in ('ATRIBUTOS', 'BÔNUS', 'Títulos', 'CA', 'CD MAGIA', 'Vida', 'Alma', 'PROFICIÊNCIAS', 'Força física'):
        positions = [m.start() for m in re.finditer(r'\b'+re.escape(term)+r'\b',raw,re.I)]
        anchors.append({"section":term,"occurrences":len(positions)})
    # Distinguish a label claim from a proven attribute layer.
    lines=raw.splitlines()
    claims={x:[] for x in ATTRS}
    for index, line in enumerate(lines):
        match=re.search(r"\b(Força|Destreza|Constituição|Inteligência|Sabedoria|Carisma)\s*:\s*([^\n]+)",line,re.I)
        if match:
            key=ALIAS[match.group(1).casefold()]
            literal=match.group(2).strip('* \t')
            simple=re.fullmatch(r'\d+',literal)
            left=literal.split('=',1)[0]
            parts=[int(x) for x in re.findall(r'\d+', left)]
            right=re.match(r'\s*(\d+)\b',literal.split('=',1)[-1]) if '=' in literal else None
            computed=None
            if '=' in literal and len(parts)>1 and right and '+' in left and '-' not in left:
                computed={'sum_of_written_terms':sum(parts),'written_result':int(right.group(1)),
                          'matches':sum(parts)==int(right.group(1))}
            claims[key].append({'line':index+1, 'raw':literal, 'value_if_unambiguous':int(literal) if simple else None,
                                'requires_review':not bool(simple), 'arithmetic_note':computed})
    blockers=[]
    if len({x['ordinal'] for x in level_hits})>1:
        blockers.append('Múltiplas classificações na mesma exportação: identificar forma/página antes de converter')
    if any(len(v)>1 for v in claims.values()):
        blockers.append('Atributos aparecem múltiplas vezes: separar contextos antes de calcular')
    if any(x['arithmetic_note'] is not None and not x['arithmetic_note']['matches']
           for v in claims.values() for x in v):
        blockers.append('Ao menos uma expressão de atributos possui divergência aritmética literal')
    return {
        'status':'READ_ONLY_DISCOVERY_NOT_A_WRITE_ADAPTER',
        'level_claims':level_hits,
        'attribute_claims':claims,
        'anchor_counts':anchors,
        'review_reasons':blockers,
        'write_allowed':False,
    }
