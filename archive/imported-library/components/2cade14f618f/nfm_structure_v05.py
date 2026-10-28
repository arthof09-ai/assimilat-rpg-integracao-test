"""Structural inspection of Notion enhanced Markdown; NO external calls or writes.

Immutable char offsets are against the exact fetched page body. We do not parse
markdown by splitting on subtitles: nested details, columns and images survive.
"""
from __future__ import annotations
from dataclasses import dataclass
import hashlib, re

class StructuralError(ValueError): pass

DETAIL_TAG = re.compile(r'<details(?:\s+[^<>]*?)?>|</details>')
SUMMARY = re.compile(r'<summary>(.*?)</summary>', re.DOTALL)
PAGE = re.compile(r'<page\s+url="([^"]+)"[^>]*>')
IMAGE = re.compile(r'notion-file-block://[^\s\)\"]+')
MENTION = re.compile(r'<mention-page\s+url="([^"]+)"')


def digest(x: str) -> str:
    return hashlib.sha256(x.encode('utf-8')).hexdigest()


def page_body(exported: str) -> str:
    if not isinstance(exported, str) or not exported.startswith('Here is the result of "fetch"'):
        raise StructuralError('Requer exportação íntegra de fetch Notion, não cópia livre')
    start=exported.find('<content>')
    end=exported.rfind('</content>')
    if start<0 or end<start:
        raise StructuralError('Envelope <content> ausente ou incompleto')
    return exported[start+len('<content>'):end]


@dataclass(frozen=True)
class Toggle:
    start: int
    end: int
    open_end: int
    close_start: int
    depth: int
    summary: str
    summary_start: int
    summary_end: int
    source_sha256: str

    def raw(self, body: str) -> str:
        return body[self.start:self.end]


def parse_toggles(body: str) -> tuple[Toggle, ...]:
    """Parse full spans and depth; fail closed on unbalanced or absent summaries."""
    stack=[]
    out=[]
    for m in DETAIL_TAG.finditer(body):
        is_close=m.group(0).startswith('</')
        if not is_close:
            stack.append((m.start(), m.end(), len(stack)))
            continue
        if not stack:
            raise StructuralError('Fechamento de toggle sem abertura')
        st, op_end, dep=stack.pop()
        # The first summary must precede any nested child toggle.
        next_child=DETAIL_TAG.search(body,op_end,m.start())
        search_end=next_child.start() if next_child else m.start()
        sr=SUMMARY.search(body,op_end,search_end)
        if sr is None:
            raise StructuralError('Toggle sem summary direto detectável')
        fragment=body[st:m.end()]
        out.append(Toggle(st,m.end(),op_end,m.start(),dep,sr.group(1),sr.start(),sr.end(),digest(fragment)))
    if stack:
        raise StructuralError('Aberturas de toggle sem fechamento')
    ordered=sorted(out,key=lambda n:n.start)
    if any(n.end>len(body) for n in ordered):
        raise StructuralError('Span além do corpo')
    return tuple(ordered)


def root_toggles(body: str) -> tuple[Toggle,...]:
    return tuple(n for n in parse_toggles(body) if n.depth==0)


def protected_inventory(source: str) -> dict:
    """Inventory immutable references; copying markup does NOT clone referenced files."""
    return {
        'sha256':digest(source),
        'characters':len(source),
        'byte_length':len(source.encode('utf-8')),
        'native_page_refs':tuple(PAGE.findall(source)),
        'native_file_refs':tuple(IMAGE.findall(source)),
        'mention_refs':tuple(MENTION.findall(source)),
        'tables':len(re.findall(r'<table(?:\s|>)',source)),
        'columns':len(re.findall(r'<columns(?:\s|>)',source)),
        'details':len(re.findall(r'<details(?:\s|>)',source)),
    }


def archive_risk(source: str) -> dict:
    i=protected_inventory(source)
    risks=[]
    if i['native_file_refs']:
        risks.append('MÍDIA BLOCO-NATIVO: referências não comprovam duplicação de bytes/arquivo')
    if i['native_page_refs']:
        risks.append('SUBPÁGINAS: link preservado, conteúdo futuro não congela automaticamente')
    return {'write_safe_without_native_clone':not bool(risks),'risks':risks,'inventory':i}
