"""Adds sixth R200 data-only tab to genuine R199 dashboard; no Python run control."""
from __future__ import annotations
import json,pathlib,sqlite3,html,statistics,collections
BASE=pathlib.Path(__file__).resolve().parents[1]
OLD=BASE.parent/'previous/new/r199/ui/VLAB_R199_COMBATES_MAGIA_TRANSFORMACAO_OFFLINE.html'
NEW=BASE/'ui/VLAB_R200_BANCADA_COMBATES_E_EQUIPAMENTOS_OFFLINE.html'
records=json.loads((BASE/'evidence/R200_EXECUTED_FIGHTS.json').read_text())
profiles=json.loads((BASE/'evidence/R200_ED_REF_01_B1_P1_PROFILES.json').read_text())
traces={}
for r in records:
    if not r['db']:continue
    c=sqlite3.connect(f"file:{(BASE/'evidence/db'/r['db']).as_posix()}?mode=ro",uri=True)
    try:
        trace=[]
        for (v,) in c.execute('SELECT row_json FROM events ORDER BY seq'):
            v=json.loads(v)
            if 'attack' in v['detail']:
                e=v['detail']['attack']
                trace.append({'seq':v['seq'],'from':e['from'],'to':e['to'],'score':e['roll_score'],
                'CA':e['ca_exact'],'hit':e['hit'],'crit':e['critical'],'rolls':e['damage_roll_groups'],
                'raw':e['raw'],'rd':e['rd_applied'],'post_rd':e['net'],'hp_removed':e['hp_loss_actual'],
                'hp_after':e['after_hp'],'overkill':e['overkill']})
        traces[r['id']]=trace
    finally:c.close()
data={'header':{'completed':sum(bool(r['db']) for r in records),'attempts':len(records),'seeds':8,'precommit_ties':sum(r['status']=='PRECOMMIT_TIE_HOLD' for r in records),'source_status':'FIRST_R200_TEST_PROXY_UNRANKED_NOT_BATTERY_E_CERTIFIED'},'records':records,'profiles':profiles,'traces':traces}
payload=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
orig=OLD.read_text()
assert len(orig)>200_000 and '5 · Poderes e transformação' in orig and "'r199'])$(tab)" in orig
orig=orig.replace('R197 + R198 + R199 · Combates, magia e transformação','R197 + R198 + R199 + R200 · R200 acrescenta ensaios físicos prospectivos e fontes TEST sem alterar os históricos')
orig=orig.replace('5 · Poderes e transformação</button>','5 · Poderes e transformação</button><button class="tab" data-tab="r200">6 · ED de referência &amp; equipamentos</button>',1)
orig=orig.replace("'combates','r199'])$(tab)","'combates','r199','r200'])$(tab)",1)
start='''
<section id="r200" class="hidden"><div class="panel">
<h2>R200 · Referência Orc B1/P1 &amp; equipamentos físicos</h2>
<p class="good">Estes são combates reais de laboratório com bancos R18/v0.8.1. A página consulta recibos já executados; não executa Python. R197–R199 permanecem acessíveis.</p>
<div id="r200-kpis" class="grid"></div>
<div class="cols"><div><label for="r200-level">Referência e adversário</label><select id="r200-level"><option value="1">Orc Bronze 1 × Galinha Demoníaca Bronze 1</option><option value="6">Orc Prata 1 × Lobo da Caverna Prata 1</option></select></div>
<div><label for="r200-run">Recibo por seed e política</label><select id="r200-run"></select></div></div>
<div class="panel"><h3>Ficha e componentes da proteção</h3><div id="r200-profile" class="grid"></div>
<p class="warning">O anel TEST tem +2 CA e 13 PA/dia publicados; sua classificação NÃO está publicada na fonte consultada. A cobrança na entrada da cena é CONVENÇÃO TEST. O par NÃO representa Bateria E homologada nem equipamento Bronze legalmente demonstrado.</p></div>
<h3>Resultados reais por seed e política</h3><div class="tablewrap"><table><thead><tr><th>Seed</th><th>Política</th><th>Estado</th><th>Rodadas</th><th>HP final</th><th>PA restante</th><th>HP efetivo por ator</th></tr></thead><tbody id="r200-rows"></tbody></table></div>
<p class="mini muted">Os ramos da mesma seed são pareados, não observações independentes. Empates recusados não são combates executados. Impasses/censuras são excluídos do denominador de vitórias.</p>
<div class="panel"><h3>Recibo causal R18 — execução selecionada</h3><div class="tablewrap"><table><thead><tr><th>Seq</th><th>Atacante → alvo</th><th>Teste/CA</th><th>Crítico</th><th>Bruto / RD / pós-RD</th><th>HP retirado</th><th>Vida após golpe</th></tr></thead><tbody id="r200-trace"></tbody></table></div></div>
<div class="panel"><h3>Geometria e próximos gates</h3><p>Alvo único: 9 m inclusivo; AoE circular: raio 6 m e centro a até 9 m do conjurador. Cone: extensão 4,5 m, mas abertura não documentada — a única cunha ilustrada é explicitamente TEST, não uma adjudicação canônica. O módulo de validação espacial ainda não foi exercitado em um combate mágico completo novo.</p><p class="warning">ED-REF-01 P1 deriva de escolhas documentadas e matemática TEST; ainda falta paridade com o LEVEL-UP ENGINE. A referência Bronze não pode transformar. Sem magia própria atribuída sem fonte, sem Bateria A–E terminal; produção HOLD.</p></div>
</div></section>
<script id="r200-data" type="application/json">'''+payload+'''</script>
<script>
(function(){
const D=JSON.parse(document.getElementById('r200-data').textContent),$=id=>document.getElementById(id);
const actor=id=>({'ED-REF-01-B1':'Orc ref B1','ED-REF-01-P1':'Orc ref P1','GALINHA_B1':'Galinha B1','LOBO_P1':'Lobo P1'})[id]||id;
const label=p=>p==='SEM_MAGIA_ITEM'?'Proteção mágica OFF':'Proteção mágica ON — proxy TEST';
const esc=x=>String(x===null||x===undefined?'—':x).replace(/[&<>\"']/g,s=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}[s]));
$('r200-kpis').innerHTML=[['Bancos executados',D.header.completed],['Seeds distintas',D.header.seeds],['Empates sem commit',D.header.precommit_ties],['Contratos oficiais',0]].map(([label,v])=>`<div class="stat"><strong>${v}</strong><small>${label}</small></div>`).join('');
function redraw(){let level=Number($('r200-level').value),p=level===1?D.profiles.actor:D.profiles.prata_1;
const rows=D.records.filter(r=>r.level===level),done=rows.filter(r=>r.db);
$('r200-profile').innerHTML=[['Vida natural',p.natural_hp_max],['PA natural',p.natural_pa_max],['FF',p.ff],['Arma física',p.weapon.physical_dice.join('d')],['CA física',p.ca_physical_exact],['CA + anel TEST',Number(evalFraction(p.ca_physical_exact))+2],['FF dano',p.ff_damage_bonus],['Nível',level]].map(([l,v])=>`<div class="stat"><strong>${esc(v)}</strong><small>${esc(l)}</small></div>`).join('');
$('r200-rows').innerHTML=rows.map(r=>`<tr><td>${r.seed}</td><td>${label(r.policy)}</td><td>${r.status==='FINISHED'?actor(r.winner)+' vence':r.status==='PRECOMMIT_TIE_HOLD'?'Empate pré-commit':'CENSURA'}</td><td>${esc(r.rounds)}</td><td>${esc(r.final_hp?Object.entries(r.final_hp).map(([k,v])=>actor(k)+': '+v).join(' / '):null)}</td><td>${esc(r.final_pa?Object.entries(r.final_pa).map(([k,v])=>actor(k)+': '+v).join(' / '):null)}</td><td>${esc(r.damage_effective_by_actor?Object.entries(r.damage_effective_by_actor).map(([k,v])=>actor(k)+': '+v).join(' / '):null)}</td></tr>`).join('');
$('r200-run').innerHTML=done.map(r=>`<option value="${r.id}">${r.seed} · ${label(r.policy)}</option>`).join('');redrawTrace();}
function evalFraction(s){let p=s.split('/');return p.length===2?Number(p[0])/Number(p[1]):Number(s)}
function redrawTrace(){let id=$('r200-run').value;let tr=D.traces[id]||[];if(tr.length>300)tr=tr.slice(0,300);
$('r200-trace').innerHTML=tr.map(e=>`<tr><td>${e.seq}</td><td>${actor(e.from)} → ${actor(e.to)}</td><td>${e.score} / ${e.CA} ${e.hit?'✓':'×'}</td><td>${e.crit==='NONE'?'—':esc(e.crit)}</td><td>${e.raw} / ${e.rd} / ${e.post_rd}</td><td>${e.hp_removed}</td><td>${e.hp_after}</td></tr>`).join('');}
$('r200-level').onchange=redraw;$('r200-run').onchange=redrawTrace;redraw();
})();
</script>
'''
assert orig.count('</body></html>')==1
orig=orig.replace('</body></html>',start+'</body></html>')
NEW.parent.mkdir(parents=True,exist_ok=True)
NEW.write_text(orig)
print(json.dumps({'file':str(NEW),'bytes':NEW.stat().st_size,'embedded_fights':len(records),'traces':len(traces),'legacy_tabs':5,'new_tab':'r200'},ensure_ascii=False))
