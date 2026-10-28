"""Extend existing six-tab R200 offline viewer without touching prior tabs.
Read only the R204 V2 and boundary-selected V2B receipts (not a browser runner).
"""
from __future__ import annotations
import json,pathlib,sqlite3,html
root=pathlib.Path(__file__).resolve().parents[1]
source=pathlib.Path('/mnt/data/VLAB_R200_BANCADA_COMBATES_E_EQUIPAMENTOS_OFFLINE.html')
out=pathlib.Path('/mnt/data/VLAB_R204_BANCADA_MAGIA_DISTANCIA_CORRIGIDA_OFFLINE.html')
s=source.read_text()
assert 'data-tab="r200"' in s and 'r204' not in s[:12000]
runs=[];traces={}
for ver,data,dirn in [('V2','R204_V2_LIVE_MAGIC_RESULTS.json','v2_db'),('V2B','R204_V2B_LIVE_MAGIC_RESULTS.json','v2b_db')]:
 records=json.loads((root/'evidence'/data).read_text())
 for rec in records:
  rid=rec['run_id'];runs.append(dict(rec,cohort=ver))
  c=sqlite3.connect(f'file:{(root/"evidence"/dirn/rec["db"]).as_posix()}?mode=ro',uri=True)
  rows=[json.loads(x[0]) for x in c.execute('select row_json from events order by seq')];c.close()
  trace=[]
  for x in rows:
   if x['kind']=='R204_ACTUAL_SOURCE_MAGIC_NO_CRIT':
    d=x['detail'];e=d['effect'];
    trace.append({'seq':x['seq'],'kind':'CHICOTE DE ÁGUA','action':{'distance_m':d['distance_before_m'],'attack_dice':e['attack_roll'],'attack_score':e['attack_score'],'target_CA':e['target_ca'],'hit':e['hit'],'damage_roll':e['rolls'] if e['hit'] else None,'damage_after_RD':e['net'],'HP_removed':d['HP_removed'],'PA_before':e['PA_before'],'PA_after':e['PA_after'],'cost':d['PA_paid'],'critical':e['critical']}})
   elif x['kind']=='R204_SPATIAL_SPELL_REJECT_OR_DECLINE':
    trace.append({'seq':x['seq'],'kind':'RECUSA / DECLÍNIO','action':x['payload']})
   elif x['kind']=='R204_BEAST_SPATIAL_MOVE_AND_ATTACK':
    d=x['detail'];a=d['attack'];trace.append({'seq':x['seq'],'kind':'LOBO — PATADA','action':{'hit':a['hit'],'raw':a['raw'],'hp_removed':a['hp_loss_actual'],'roll_score':a['roll_score'],'ca_exact':a['ca_exact'],'critical':a['critical'],'move':d.get('spatial_movement') is not None}})
  traces[rid]=trace
s=s.replace('data-tab="r200">6 · ED de referência &amp; equipamentos</button>','data-tab="r200">6 · ED de referência &amp; equipamentos</button><button class="tab" data-tab="r204">7 · Magia real &amp; distância</button>',1)
s=s.replace("'r199','r200']","'r199','r200','r204']",1)
frag='''<section id="r204" class="hidden"><div class="panel">
<h2>R204 · Chicote de Água — magia real, distância e PA</h2>
<p class="good">40 combates TEST novos com leitura do teste específico 4d6+INT antes do dano 8d6+28. Sem crítico mágico. Ação e alcance físico 9m validados antes do débito de 8 PA. Logs SQLite nativos R18; o HTML é VISUALIZADOR, não executor.</p>
<div class="grid" id="r204-kpis"></div>
<p class="warning">V1: outras 24 batalhas físicas preservadas em dossiê, mas com interpretação de acerto direto <strong>incompatível com o teste específico publicado</strong>. EXCLUÍDAS desta comparação V2. A coorte V2B usa seeds selecionadas para demonstrar a fronteira de alcance e não é uma amostra aleatória de vitórias.</p>
<div class="cols"><div><label for="r204-cohort">Coorte</label><select id="r204-cohort"><option value="V2">R204-V2 · Confrontos pareados</option><option value="V2B">R204-V2B · Validação da fronteira 9 / 9,5 m</option></select></div><div><label for="r204-run">Luta e seed</label><select id="r204-run"></select></div></div>
<div class="tablewrap"><table><thead><tr><th>Seed</th><th>Distância</th><th>Política</th><th>Resultado</th><th>Chicotes</th><th>PA</th><th>HP retirado</th><th>Recusas fora do alcance</th></tr></thead><tbody id="r204-rows"></tbody></table></div>
<div class="panel"><h3>Recibo causal da execução selecionada</h3><div class="tablewrap"><table><thead><tr><th>Commit</th><th>Evento</th><th>Teste / estado / consequência</th></tr></thead><tbody id="r204-trace"></tbody></table></div></div>
<p class="mini muted">Fonte: Ong Mefita Prata2, Lobo Prata1, Sistema de Magia, Criação de Besta, decisão do Mestre alcance padrão 9m. Encontro com deslocamento adjacente TEST; reação, cobertura e AOO não generalizados. 0/17 contratos terminais; 0/1.875 células oficiais.</p>
</div></section>
'''
pos=s.index('<script id="r200-data"')
s=s[:pos]+frag+s[pos:]
data={'runs':runs,'traces':traces}
js='''<script id="r204-data" type="application/json">'''+json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+'''</script>
<script>(()=>{const D=JSON.parse(document.getElementById('r204-data').textContent),$=i=>document.getElementById(i),esc=x=>String(x??'—').replace(/[&<>"']/g,s=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[s]));
const records=D.runs, n=(a,k)=>a.reduce((v,x)=>v+(Number(x[k])||0),0);
$('r204-kpis').innerHTML=[['Combates corrigidos',records.length],['Conjurações',n(records,'spell_casts')],['PA debitados',n(records,'PA_spell_spent')],['Recusas por alcance',n(records,'range_refusals')]].map(([label,v])=>`<div class="stat"><strong>${v}</strong><small>${label}</small></div>`).join('');
function draw(){let c=$('r204-cohort').value,a=records.filter(r=>r.cohort===c);$('r204-run').innerHTML=a.map(r=>`<option value="${esc(r.run_id)}">${r.seed} · ${r.initial_distance_m}m · ${r.policy==='CAST_WHEN_IN_RANGE'?'Lança':'Declina'}</option>`).join('');$('r204-rows').innerHTML=a.map(r=>`<tr><td>${r.seed}</td><td>${r.initial_distance_m}m</td><td>${r.policy==='CAST_WHEN_IN_RANGE'?'Conjurar':'Sem conjuração'}</td><td>${esc(r.winner)} (${r.round}rod.)</td><td>${r.spell_casts}</td><td>${r.PA_spell_spent}</td><td>${r.HP_removed_by_spell}</td><td>${r.range_refusals}</td></tr>`).join('');trace();}
function trace(){let id=$('r204-run').value;let t=D.traces[id]||[];$('r204-trace').innerHTML=t.map(r=>`<tr><td>${r.seq}</td><td>${esc(r.kind)}</td><td><code class="mini">${esc(JSON.stringify(r.action))}</code></td></tr>`).join('');}
$('r204-cohort').onchange=draw;$('r204-run').onchange=trace;draw();})();</script>
'''
s=s.replace('</body></html>',js+'</body></html>',1)
s=s.replace('R197 + R198 + R199 + R200 · R200 acrescenta ensaios físicos prospectivos', 'R197 + R198 + R199 + R200 + R204 · R204 acrescenta lutas reais com magia e alcance')
out.write_text(s)
(root/'ui').mkdir(exist_ok=True);(root/'ui'/out.name).write_bytes(out.read_bytes())
print(json.dumps({'html':str(out),'size':out.stat().st_size,'cohorts':{'V2':32,'V2B':8},'old_tab_count_preserved':6,'new_tab_count':7},indent=2))
