#!/usr/bin/env python3
"""CRAFT Oficina do Mestre v02: thin, local-only batch UI over unmodified R48.

All fabrication, stages, evidence, reservations, QA, outputs, ledger, commit,
rollback and idempotence belong to the ORIGINAL R44/R47/R48 engines. The only
new responsibilities are collecting human input, preparing R48 orders, running
read-only projected R48 simulation, and presenting committed receipts.
"""
from __future__ import annotations
import argparse
import copy
import html
import json
import secrets
import uuid
import webbrowser
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, urlsplit
from http.server import ThreadingHTTPServer

import app as old
from app import (esc, canon, write_json, Studio, Handler, RECIPES, NAMES, LOT_NAMES,
                 BATCH_RE, values_from_default, layout, rows_stock)
from r48_factory import IntegratedFactory, SandboxEngine, FactoryError
from r48_store import DurableFactory
from r47_fixtures import REVIEW

V02_TITLE='Oficina CRAFT v02 — Planejar e fabricar lotes'
OLD_NAV=old.nav

def extended_nav():
    return OLD_NAV().replace('</nav>','<a href="/lotes"><strong>Planejar lote</strong></a><a href="/sessoes">Sessões salvas</a></nav>')
old.nav=extended_nav
old.CSS+='''
.totals{font-weight:bold;background:#f0f4fb}.pass{color:#166443}.fail{color:#a32424}
.compact{font-size:.88rem}.highlight{background:#f2f5fc;padding:12px;border-radius:8px}
input[type=number].qty{width:92px}.warning-text{color:#a33c21}
'''

class BatchStudio(Studio):
    """Adds no mechanical engine; delegates all projection/commit to R48."""
    def catalog_lots(self,code):
        _,f,_=self.active_store()
        if f is None:raise ValueError('CRIAR_SESSAO_PRIMEIRO')
        recipe=self.recipe(code)
        choices=[]
        for rule in recipe['inputs']:
            candidates=[v for v in f.core.state['lots'].values()
                if v['source_page_id']==rule['source_page_id'] and v['unit']==rule['unit']]
            choices.append(candidates)
        return choices

    @staticmethod
    def _qa_fixture(recipe,mode):
        qa=copy.deepcopy(values_from_default(recipe))
        if mode=='pass':return qa
        if mode!='invalid':raise ValueError('MODO_QA_INVALIDO')
        # The engine/R46 rejects the altered reading. This is NOT a real test.
        field=next((r for r in recipe['qa_rules'] if r['kind']=='bool_eq'),None)
        if field:qa[field['field']]=not field['value']
        else:
            rule=recipe['qa_rules'][0]
            qa[rule['field']]=rule.get('max',rule.get('min',0))+10000
        return qa

    def _make_order(self,raw,batch_id,ordinal):
        # Reuse the existing R47 fixture constructor and R48 order adapter.
        stem=int(batch_id[-16:],16)
        derived='SBX-R48-BATCH-UI-'+f'{(stem+ordinal+1)%(1<<64):016x}'
        return self.request_from(raw,derived)['orders'][0]

    def _parse_batch(self,fields):
        counts={}
        for code in RECIPES:
            try:qty=int(fields.get('count_'+code,'0'))
            except (ValueError,TypeError):raise ValueError('QUANTIDADE_DE_PRODUTOS_INVALIDA')
            if not 0<=qty<=16:raise ValueError('LIMITE_POR_RECEITA_0_A_16')
            counts[code]=qty
        total=sum(counts.values())
        if not 1<=total<=16:raise ValueError('LIMITE_R48_DE_1_A_16_TENTATIVAS')
        choices={}
        for code in RECIPES:
            rec=self.recipe(code)
            choices[code]=[fields.get(f'batch_lot_{code}_{i}','') for i in range(len(rec['inputs']))]
            if counts[code] and (any(not v for v in choices[code]) or len(set(choices[code]))!=len(choices[code])):
                raise ValueError('ESCOLHA_LOTES_DISTINTOS_POR_TENTATIVA:'+code)
        mode=fields.get('batch_qa','pass')
        if mode not in ('pass','invalid'):raise ValueError('QA_DESCONHECIDO')
        target=fields.get('batch_qa_recipe','B30-01')
        if target not in RECIPES:raise ValueError('RECEITA_QA_DESCONHECIDA')
        return counts,choices,mode,target

    def plan(self,fields):
        with self.lock:
            store,f,pointer=self.active_store()
            if store is None:raise ValueError('CRIAR_SESSAO_PRIMEIRO')
            counts,choices,mode,target=self._parse_batch(fields)
            batch_id='SBX-R48-BATCH-UI-'+secrets.token_hex(8)
            orders=[];demand={lot_id:0 for lot_id in f.quantities}
            input_summary=[]
            for code in RECIPES:
                rec=self.recipe(code)
                for attempt in range(counts[code]):
                    qa_mode='invalid' if mode=='invalid' and target==code and attempt==0 else 'pass'
                    raw={'recipe':code,'lot_ids':choices[code],
                         'tools':list(rec['tools']),'skills':list(rec['skills']),
                         'qa':self._qa_fixture(rec,qa_mode)}
                    order=self._make_order(raw,batch_id,len(orders))
                    orders.append(order)
                    for rule,lot in zip(rec['inputs'],raw['lot_ids']):
                        demand[lot]=demand.get(lot,0)+rule['quantity']
                    input_summary.append({'code':code,'ordinal':attempt+1,
                            'output_units_proposed':rec['output']['quantity'],
                            'lot_ids':raw['lot_ids'],'qa_fixture':qa_mode})
            request={'batch_id':batch_id,'orders':orders,'reviewed_at':REVIEW}
            snap=f.snapshot()
            # TRUE R48 process_batch on an isolated copy, no parallel mechanic.
            projection=IntegratedFactory.restore(snap,f.head,snap['snapshot_sha256'])
            receipt=projection.process_batch(**request)
            deny=[{'ordinal':i+1,'status':o['status'],'reasons':o['reasons']}
                  for i,o in enumerate(receipt['orders']) if o['status']=='REJECTED_PRECHECK']
            quarantine=[{'ordinal':i+1,'status':o['status'],'reasons':o['reasons']}
                  for i,o in enumerate(receipt['orders']) if o['status']!='EXPERIMENTAL_QA_PASS']
            # Allow deliberate invalid QA demonstration, but no stock shortfall.
            can_confirm=not deny and (not quarantine or mode=='invalid')
            if any(q<0 for q in f.quantities.values()):raise FactoryError('STOCK_NEGATIVE')
            plan={'version':'CRAFT-UI-BATCH-v02','kind':'ONLY_SYNTHETIC',
                  'session_id':self.session_id(),'expected_head':pointer['r48_head'],
                  'plan_status':'DRAFT',
                  'created_utc':datetime.now(timezone.utc).isoformat(),
                  'counts':counts,'selected_lots':choices,'qa_mode':mode,'qa_target':target,
                  'order_summary':input_summary,'demand':demand,
                  'before':f.quantities,'receipt_preview':receipt,
                  'can_confirm':can_confirm,'preflight_blockers':deny,
                  'expected_non_pass':quarantine,'request':request,
                  'official_product_effect':0,'official_stock_effect':0}
            write_json(self.path(self.session_id())/'plans'/f'{batch_id}.json',plan)
            return plan

    def get_plan(self,batch_id):
        if not BATCH_RE.fullmatch(batch_id):raise ValueError('ID_PLANO_INVALIDO')
        sid=self.session_id()
        if sid is None:raise ValueError('CRIAR_SESSAO_PRIMEIRO')
        target=self.path(sid)/'plans'/f'{batch_id}.json'
        if not target.is_file():raise ValueError('PLANO_NAO_ENCONTRADO_NESTA_SESSAO')
        plan=json.loads(target.read_text('utf8'))
        if plan.get('version')!='CRAFT-UI-BATCH-v02' or plan.get('kind')!='ONLY_SYNTHETIC' or plan.get('session_id')!=sid:
            raise ValueError('PLANO_INVALIDO_OU_DE_OUTRA_SESSAO')
        if plan['request']['batch_id']!=batch_id or len(plan['request']['orders'])!=sum(plan['counts'].values()):
            raise ValueError('INTEGRIDADE_PLANO_INVALIDA')
        return plan

    def cancel_plan(self,batch_id):
        """Explicit user cancellation of DRAFT only. No R48 write or stock effect."""
        with self.lock:
            plan=self.get_plan(batch_id)
            if plan.get('plan_status')=='CANCELLED_BY_USER':return plan
            _,f,_=self.active_store()
            if batch_id in f.seen_batches:
                raise ValueError('LOTE_JA_CONFIRMADO_USE_REVERTER_CHECKPOINT')
            plan['plan_status']='CANCELLED_BY_USER'
            plan['can_confirm']=False
            plan['cancelled_utc']=datetime.now(timezone.utc).isoformat()
            write_json(self.path(self.session_id())/'plans'/f'{batch_id}.json',plan)
            return plan

    def confirm_plan(self,batch_id):
        with self.lock:
            plan=self.get_plan(batch_id)
            if plan.get('plan_status')=='CANCELLED_BY_USER':
                raise ValueError('PLANO_CANCELADO_PELO_MESTRE_NAO_EXECUTAR')
            if not plan['can_confirm']:
                raise ValueError('CONFIRMACAO_BLOQUEADA_POR_PRECHECK')
            store,f,pointer=self.active_store()
            existing=batch_id in f.seen_batches
            if not existing and pointer['r48_head']!=plan['expected_head']:
                raise ValueError('PLANO_DESATUALIZADO_ESTOQUE_MODIFICADO_REFAZER_PREVIA')
            req=plan['request']
            # Save exact request BEFORE motor commit; replay after ACK loss is safe.
            path=self.path(self.session_id())/'requests'/f'{batch_id}.json'
            if path.exists():
                if old.digest(json.loads(path.read_text('utf8')))!=old.digest(req):
                    raise ValueError('IDENTIDADE_PEDIDO_CONFLITANTE')
            else:write_json(path,req)
            result=store.commit_batch(**req,expected_head=None if existing else plan['expected_head'])
            if result['receipt']['request_sha256']!=plan['receipt_preview']['request_sha256']:
                raise FactoryError('PREVIEW_COMMIT_MISMATCH')
            if not result['idempotent_replay']:
                # No other writer in the same local store can interleave with CAS.
                for key in ('status','stock_before','stock_after','orders'):
                    if result['receipt'][key]!=plan['receipt_preview'][key]:
                        raise FactoryError('R48_DETERMINISM_DIVERGENCE:'+key)
            return result

    def new_lot_scenario(self,lot_id,quantity):
        """Adds a synthetic lot ONLY to a brand-new independent scenario.

        The R48 engine has no deposit event, so never mutate its historic ledger.
        A new test state is seeded from *current balances* with the new fixture;
        the original session and its products remain readable separately.
        """
        with self.lock:
            _,f,_=self.active_store()
            if f is None:raise ValueError('CRIAR_SESSAO_PRIMEIRO')
            if lot_id not in f.core.state['lots']:raise ValueError('LOTE_MODELO_DESCONHECIDO')
            if type(quantity) is not int or not 1<=quantity<=100000:
                raise ValueError('QUANTIDADE_LOTE_INVALIDA')
            base=copy.deepcopy(list(f.core.state['lots'].values()))
            extra=copy.deepcopy(f.core.state['lots'][lot_id])
            extra['lot_id']='SBX-UI-LOT-'+secrets.token_hex(6).upper()
            extra['quantity']=quantity
            extra['fixture_kind']='SYNTHETIC'
            base.append(extra)
            sid='sim-'+uuid.uuid4().hex[:12]
            root=self.path(sid)
            root.mkdir(parents=True,exist_ok=False)
            DurableFactory(root/'store').initialize(IntegratedFactory.fixture_factory(base))
            write_json(root/'session.json',{'id':sid,'type':'SYNTHETIC_ONLY',
                'origin':self.session_id(),'reason':'NEW_INDEPENDENT_SYNTHETIC_STOCK_SCENARIO',
                'new_lot_id':extra['lot_id'],'model_lot_id':lot_id,'new_lot_quantity':quantity,
                'does_not_inherit_products_or_prior_commits':True,
                'started_utc':datetime.now(timezone.utc).isoformat()})
            self.activate(sid)
            return {'session_id':sid,'lot_id':extra['lot_id'],'quantity':quantity,'origin_preserved':True}


def source_lot_options(studio,code,index):
    pool=studio.catalog_lots(code)[index]
    defaults={'B30-01':['SBX-SLATE-GOOD-01'],
              'B30-03':['SBX-MICA-GOOD-A','SBX-MICA-GOOD-B']}
    ideal=defaults[code][index]
    return ''.join(f'<option value="{esc(r["lot_id"])}" {"selected" if r["lot_id"]==ideal else ""}>'
                   f'{esc(LOT_NAMES.get(r["lot_id"],"Lote adicional de teste"))} '
                   f'· {esc(r["lot_id"])} · saldo {r["quantity"]}</option>' for r in pool)


def format_preflight(plan):
    before=plan['before'];need=plan['demand'];preview=plan['receipt_preview']
    projected=preview['stock_after']
    stockrows=[]
    for lot_id,available in before.items():
        request=need.get(lot_id,0)
        if not available and not request:continue
        shortage=max(0,request-available)
        cls=' class="fail"' if shortage else ''
        stockrows.append(f'<tr{cls}><td>{esc(LOT_NAMES.get(lot_id,"Adicional de teste"))}<br><small>{esc(lot_id)}</small></td>'
                         f'<td>{available}</td><td>{request}</td><td>{shortage}</td><td>{projected[lot_id]}</td></tr>')
    statusrows=[]
    for n,o in enumerate(preview['orders'],1):
        statusrows.append(f'<tr><td>{n}</td><td>{esc(o["recipe_key"])}</td>'
                          f'<td>{esc(o["status"])}</td><td>{esc(o["reasons"] or "PASS")}</td>'
                          f'<td>{sum(p["units"] for p in o["products"])}</td></tr>')
    counts=plan['counts']
    prods=sum(sum(p['units'] for p in o['products']) for o in preview['orders'])
    tools=[]
    for code,n in counts.items():
        if n:
            tools.append(f'{n} × {esc(NAMES[code])} ({esc(code)})')
    title='<h2>Prévia do lote · ainda NÃO confirmado</h2><p><strong>Tentativas:</strong> '+', '.join(tools)+f'. <strong>Peças sintéticas previstas pelo R48:</strong> {prods}. '
    title+='Reservas permanentes: <strong>0</strong> (a prévia não bloqueia estoque).</p>'
    top='<div class="info"><strong>Executor real da prévia: R48 em cópia isolada.</strong> A confirmação só aceita o mesmo HEAD local; mudanças posteriores exigem novo planejamento. Custo econômico: <strong>INDISPONÍVEL</strong> (sem MED verificado). Fórmulas simbólicas originais disponíveis nas páginas das receitas. Tempos, geometria e QA são propostos/simulados.</div>'
    inventory='<section class="panel"><h3>Consumo por lote fictício · disponibilidade × demanda</h3><table><thead><tr><th>Lote</th><th>Disponível</th><th>Necessário</th><th>Falta</th><th>Após motor R48</th></tr></thead><tbody>'+''.join(stockrows)+'</tbody></table></section>'
    result='<section class="panel"><h3>Decisões por tentativa · motor R44/R47/R48</h3><table><thead><tr><th>#</th><th>Receita</th><th>QA/estoque</th><th>Razão</th><th>Peças</th></tr></thead><tbody>'+''.join(statusrows)+'</tbody></table></section>'
    warn=''
    if plan.get('plan_status')=='CANCELLED_BY_USER':
        warn='<div class="info"><strong>Plano CANCELADO pelo Mestre.</strong> Não houve tentativa de fabricação; nenhuma reserva ou consumo foi realizado. Crie uma nova prévia se desejar.</div>'
    elif plan['preflight_blockers']:
        warn='<div class="error"><strong>Confirmação bloqueada:</strong> há falta de recursos ou requisito não atendido. Nenhum estoque foi modificado na prévia. Ajuste quantidades ou crie um novo cenário fictício.</div>'
    elif plan['expected_non_pass']:
        warn='<div class="warn"><strong>Falha intencional em QA de TESTE:</strong> o motor projetou quarentena/reprovação. A confirmação registra o lote misto como previsto. Recurso consumido ou preservado obedece exclusivamente ao R48.</div>'
    else:warn='<div class="info"><span class="good">Lote elegível à confirmação experimental.</span> Nada foi consumido nesta prévia.</div>'
    return title+top+inventory+result+warn


def batch_form(studio):
    _,f,_=studio.active_store()
    if f is None:return f'<section class="panel"><h2>Planejador de lotes</h2><p>Crie primeiro um estoque fictício. Para o exemplo 3 Tábuas + 2 pares de Mica, você pode usar o cenário de teste pronto com 8 lâminas e 8 folhas de cada tipo.</p><form action="/cenario-pronto" method="post"><input type="hidden" name="csrf" value="{esc(studio.token)}"><button type="submit">Criar cenário fictício 3+2 pronto</button></form><p><a href="/">Personalizar estoque manualmente</a></p></section>'
    token=studio.token
    entries=[]
    for code in RECIPES:
        recipe=studio.recipe(code)
        components=''.join(f'<li>{i["quantity"]} {esc(i["unit"])} · origem PS {esc(i["source_page_id"])} · requisito {esc(i.get("minimum_dimensions_mm","conforme receita"))}</li>' for i in recipe['inputs'])
        select=''.join(f'<label>Ingrediente {i+1} · selecionar lote fictício <select name="batch_lot_{code}_{i}" required>{source_lot_options(studio,code,i)}</select></label>' for i in range(len(recipe['inputs'])))
        entries.append(f'<section class="panel"><h3>{esc(code)} — {esc(NAMES[code])}</h3>'
                       f'<label><strong>Quantidade de tentativas</strong> (B30-03: cada tentativa produz um PAR de 2 peças): <input type="number" class="qty" name="count_{code}" min="0" max="16" value="{3 if code=="B30-01" else 2}" required></label>'
                       f'<details open><summary>Ingredientes, lotes e requisitos</summary><ul>{components}</ul>{select}'
                       f'<p><small>Ferramentas: {esc(", ".join(recipe["tools"]))}; competências: {esc(", ".join(recipe["skills"]))}; duração {recipe["proposed_active_minutes"]} min PROPOSTA por tentativa; QA experimental conforme contrato original. <a href="/receita?code={code}">Ver etapas e critérios completos</a>.</small></p></details></section>')
    form=f'''<section class="panel"><h2>Planejar fabricações em lote</h2><p>Informe quantas vezes executar cada receita. O motor R48 aceita até <strong>16 tentativas numa transação</strong>. A prévia fará um ensaio do lote inteiro sem consumir estoque real ou fictício.</p>
      <form method="post" action="/lotes-planejar"><input type="hidden" name="csrf" value="{esc(token)}">
      <div class="grid">{''.join(entries)}</div>
      <fieldset><legend>Qualidade de TESTE</legend><label>Modo QA <select name="batch_qa"><option value="pass">Fixture sintética aprovada (padrão)</option><option value="invalid">Simular 1 laudo reprovado/quarentenado</option></select></label><label>Se simular falha, qual receita? <select name="batch_qa_recipe"><option value="B30-01">B30-01</option><option value="B30-03">B30-03</option></select></label><small>Nunca constitui medição física. O QA é decidido por R44/R46/R47/R48.</small></fieldset>
      <button type="submit">Conferir necessidade, custo e estoque (SEM consumir)</button></form></section>'''
    stock='<section class="panel"><h3>Saldo fictício na sessão</h3>'+rows_stock(f)+'<p><small>Reserva atual permanente: zero. A reserva da fabricação é transacional e pertence ao R48; a previsão não reserva recursos.</small></p></section>'
    choices=''.join(f'<option value="{esc(v)}">{esc(LOT_NAMES.get(v,"Lote adicional de teste"))}: {esc(v)}</option>' for v in f.quantities)
    add=f'''<section class="panel"><h3>Adicionar um lote fictício para TESTES</h3><p>O motor R48 não possui evento de entrada de estoque: para preservar o ledger, esta ação cria <strong>nova sessão independente</strong> a partir do saldo atual + 1 lote clonado. Sessão e recibos anteriores ficam preservados, mas seus produtos não são importados na nova sessão.</p><form action="/lote-adicional" method="post"><input type="hidden" name="csrf" value="{esc(token)}"><label>Copiar parâmetros do lote-modelo <select name="lot_template">{choices}</select></label><label>Quantidade fictícia <input type="number" name="quantity" min="1" max="100000" value="5" required></label><button type="submit" class="subtle">Criar nova sessão com lote adicional</button></form></section>'''
    return form+stock+add


class BatchHandler(Handler):
    server_version='CRAFT-SBX-UI/2.0'
    def do_GET(self):
        path=urlsplit(self.path).path
        try:
            if path=='/lotes':
                return self._send(layout(batch_form(self.studio),V02_TITLE,self.studio.session_id()))
            if path=='/lote-previa':
                bid=self._query().get('id','')
                p=self.studio.get_plan(bid)
                rendered=format_preflight(p)
                if p['can_confirm'] and p.get('plan_status')!='CANCELLED_BY_USER':
                    rendered+=f'<section class="panel"><form action="/lotes-confirmar" method="post"><input type="hidden" name="csrf" value="{esc(self.studio.token)}"><input type="hidden" name="id" value="{esc(bid)}"><button type="submit">Confirmar lote e registrar no R48</button></form></section>'
                if p.get('plan_status')=='DRAFT':
                    rendered+=f'<section class="panel"><form action="/lotes-cancelar" method="post"><input type="hidden" name="csrf" value="{esc(self.studio.token)}"><input type="hidden" name="id" value="{esc(bid)}"><button class="danger" type="submit">Cancelar plano SEM consumir</button></form></section>'
                rendered+='<p><a href="/lotes">Voltar e editar novo planejamento</a></p>'
                return self._send(layout(rendered,V02_TITLE,self.studio.session_id()))
            if path=='/lote-resumo':return self.batch_summary()
            if path=='/lote-recibo-individual':return self.download_individual()
            return super().do_GET()
        except Exception as e:self.fail(e)

    def do_POST(self):
        path=urlsplit(self.path).path
        if path not in ('/lotes-planejar','/lotes-confirmar','/lotes-cancelar','/lote-adicional','/cenario-pronto'):
            return super().do_POST()
        try:
            fields=self._post()
            if path=='/cenario-pronto':
                q={k:(8 if ('SLATE-GOOD-01' in k or 'MICA-GOOD-' in k) else v) for k,v in old.DEFAULT_QTY.items()}
                self.studio.init(q)
                return self._redirect('/lotes')
            if path=='/lotes-planejar':
                plan=self.studio.plan(fields)
                return self._redirect('/lote-previa?id='+quote(plan['request']['batch_id']))
            if path=='/lotes-cancelar':
                bid=fields.get('id','')
                self.studio.cancel_plan(bid)
                return self._redirect('/lote-previa?id='+quote(bid))
            if path=='/lotes-confirmar':
                if fields.get('confirm') not in (None,'on'):
                    raise ValueError('CONFIRMACAO_INVALIDA')
                result=self.studio.confirm_plan(fields.get('id',''))
                return self._redirect('/lote-resumo?batch='+quote(result['receipt']['batch_id']))
            if path=='/lote-adicional':
                try:qty=int(fields.get('quantity','0'))
                except ValueError:raise ValueError('QUANTIDADE_NAO_NUMERICA')
                self.studio.new_lot_scenario(fields.get('lot_template',''),qty)
                return self._redirect('/lotes')
        except Exception as e:self.fail(e)

    def _receipt(self):
        bid=self._query().get('batch','')
        return bid,self._receipt_for(bid)

    def batch_summary(self):
        bid,receipt=self._receipt()
        rows=[];units=0;consumption={}
        for ix,o in enumerate(receipt['orders'],1):
            q=sum(p['units'] for p in o['products']);units+=q
            for item in o['consumed']:
                lid=item['lot_id'];consumption[lid]=consumption.get(lid,0)+item['quantity']
            rows.append(f'<tr><td>{ix}</td><td>{esc(o["recipe_key"])}</td><td>{esc(o["status"])}</td>'
                        f'<td>{q}</td><td><a href="/lote-recibo-individual?batch={quote(bid)}&index={ix}">Recibo {ix} (JSON)</a></td></tr>')
        before=receipt['stock_before'];after=receipt['stock_after']
        balance=''.join(f'<tr><td>{esc(LOT_NAMES.get(k,k))}<br><small>{esc(k)}</small></td><td>{before[k]}</td><td>{before[k]-after[k]}</td><td>{after[k]}</td></tr>' for k in sorted(before))
        content=f'<section class="panel"><h2>Resumo do lote confirmado · {esc(receipt["status"])}</h2><p>Identificador <code>{esc(bid)}</code>. <strong>{len(receipt["orders"])} tentativas individuais</strong>, <strong>{units} peças sintéticas</strong>. Publicação única no ledger local R48; status individuais podem conter rejeições. Sem produção física ou RC5.</p>'
        content+='<table><tr><th>#</th><th>Receita</th><th>Resultado QA/R48</th><th>Peças</th><th>Recibo</th></tr>'+''.join(rows)+'</table></section>'
        content+='<section class="panel"><h3>Estoque ANTES → DEPOIS (consumo R48)</h3><table><tr><th>Lote</th><th>Antes</th><th>Consumido</th><th>Depois</th></tr>'+balance+'</table><p><strong>Custo:</strong> MED indisponível; fórmulas experimentais preservadas. <strong>Perdas:</strong> consulte cada recibo do motor.</p></section>'
        content+=f'<section class="panel"><div class="buttons"><a class="button subtle" href="/recibo?batch={quote(bid)}">Ver traço completo e QA</a><a class="button subtle" href="/baixar?batch={quote(bid)}">Baixar recibo completo JSON</a><form action="/repetir" method="post"><input type="hidden" name="csrf" value="{esc(self.studio.token)}"><input type="hidden" name="batch_id" value="{esc(bid)}"><button type="submit">Repetir mesma operação (idempotente)</button></form><a class="button" href="/lotes">Novo lote</a></div></section>'
        return self._send(layout(content,V02_TITLE,self.studio.session_id()))

    def download_individual(self):
        bid,receipt=self._receipt()
        ix=int(self._query().get('index','0'))
        if not 1<=ix<=len(receipt['orders']):raise ValueError('INDICE_RECIBO_INVALIDO')
        order=receipt['orders'][ix-1]
        individual={'schema':'CRAFT-UI-INDIVIDUAL-RECEIPT-v02','synthetic_only':True,
                    'batch_id':bid,'order_number':ix,'batch_request_sha256':receipt['request_sha256'],
                    'batch_stock_before':receipt['stock_before'],
                    'batch_stock_after':receipt['stock_after'],
                    'order':order,'official_materialization':False,'not_an_independent_R48_commit':True}
        return self._send(canon(individual),ctype='application/json; charset=utf-8',
                          filename=f'{bid}-pedido-{ix}.json')

    def home(self):
        # Reuse ALL existing home behavior; insert a clear direct batch entry.
        return super().home()

    def help(self):
        return self._send(layout('''<section class="panel"><h2>Guia em 7 passos</h2><ol>
          <li>Abra <strong>INICIAR_CRAFT.bat</strong> no Windows ou <strong>INICIAR_CRAFT.sh</strong> em Linux/Mac.</li>
          <li>Clique <strong>Criar estoque e começar</strong> e escolha quantidades inteiramente fictícias.</li>
          <li>Use Tábua B30-01 ou Mica B30-03 para fabricar uma tentativa individual.</li>
          <li>Abra <a href="/lotes">Planejar lote</a>, informe 3 Tábuas e 2 pares de Mica.</li>
          <li>Clique <strong>Conferir necessidade</strong>. Compare saldo, falta, QA e custo (MED indisponível).</li>
          <li><strong>Confirme</strong> a prévia se elegível. Veja <strong>Resumo</strong>, recibos individuais e histórico.</li>
          <li>Feche a janela e inicie novamente: o aplicativo reabre a mesma sessão. Em <a href="/sessoes">Sessões</a>, abra versões anteriores. Para reverter o último lote, utilize <strong>Reverter</strong> na página Início — cria uma nova sessão preservando o histórico original.</li>
          </ol><p><strong>QA e materiais são simulados:</strong> todas as assinaturas R47 são de TESTE e nenhum custo MED, dimensão física ou estoque real é declarado. O R48 é quem consome, rejeita, produz e mantém idempotência.</p>
          <p><strong>Lote novo adicional:</strong> abre cenário independente a partir dos saldos atuais, nunca reabastece silenciosamente o ledger original. A prévia não reserva estoque permanentemente.</p>
          <p><strong>Limite:</strong> 16 tentativas numa transação R48. Estado oficial F5 RED, 0/26 gaps, 0/30 RC5, C19 UNKNOWN, NAC-PASS material HOLD.</p></section>''',V02_TITLE,self.studio.session_id()))


def serve(data,host,port,open_browser=True):
    if host not in ('127.0.0.1','localhost'):
        raise ValueError('SOMENTE_SERVIDOR_LOCAL_127_0_0_1')
    studio=BatchStudio(Path(data))
    server=ThreadingHTTPServer((host,port),BatchHandler)
    server.studio=studio
    if open_browser:
        import threading
        threading.Timer(.6,lambda:webbrowser.open(f'http://{host}:{port}')).start()
    print(f'Oficina CRAFT v02 local: http://{host}:{port} | fictício, sem Notion')
    try:server.serve_forever()
    finally:server.server_close()

if __name__=='__main__':
    p=argparse.ArgumentParser(description='Oficina CRAFT v02 local: motor R48 original')
    p.add_argument('--data',default=str(Path(__file__).resolve().parent/'SESSOES-FICTICIAS'))
    p.add_argument('--host',default='127.0.0.1')
    p.add_argument('--port',type=int,default=8765)
    p.add_argument('--no-browser',action='store_true')
    a=p.parse_args();serve(a.data,a.host,a.port,not a.no_browser)
