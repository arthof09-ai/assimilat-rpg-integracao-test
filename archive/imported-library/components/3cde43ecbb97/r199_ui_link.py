"""Preserve R197/R198 HTML and append fifth tab: direct real R199 SQLite receipts."""
import json,pathlib,sqlite3,collections
ROOT=pathlib.Path(__file__).resolve().parents[3];R199=ROOT/'new/r199'
old=(ROOT/'new/ui/VLAB_R198_COMBATES_E_MAGIA_OFFLINE.html').read_text()
b=json.loads((R199/'evidence/R199_BENCHMARK_FROM_REAL_FIGHTS.json').read_text())
err=json.loads((R199/'evidence/R199_R198_MAGIC_METRICS_CORRECTED.json').read_text())
traces={}
for x in b['records']:
 p=R199/'evidence/db'/(x['id']+'.sqlite');c=sqlite3.connect(f'file:{p}?mode=ro',uri=True)
 try:st=json.loads(c.execute('SELECT value FROM meta WHERE key="state"').fetchone()[0])
 finally:c.close()
 traced=[]
 for e in st['native_events']:
  if e['action']=='weapon_attack':traced.append({'seq':e['seq'],'type':'ATTACK','actor':e['from'],'defender':e['to'],
   'roll':e['roll_score'],'CA':e['ca_exact'],'crit':e['critical'],'hit':e['hit'],'raw':e['raw'],'RD':e['rd_applied'],'net':e['net'],'hp':e['hp_loss_actual'],'damage_type':e['type']})
  elif e['action'] in ('spell_pa_cost','transform_activate','transform_expire','transform_end_on_ko','transform_damage_split'):
   traced.append({'seq':e['seq'],'type':e['action'],'actor':e.get('by'),
      'pa_spent':e.get('PA_spent',e.get('cost',0)),'normal_pa_after':e.get('normal_pa_after'),
      'form_source':e.get('source_form'),'duration_total':e.get('duration_total'),
      'temporary_hp_removed':e.get('temporary_hp_removed'),'normal_hp_removed':e.get('normal_hp_removed')})
 traces[x['id']]=traced
UI={'summary':{'fights':b['actual_fights'],'seed_blocks':b['distinct_seed_blocks'],'policies':b['policy_summaries'],
  'status':b['status'],'official_benchmarks':0,'certified_contracts':0,'prior_r198_corrected':'DECLINE_WHIP_magic_damage_zero'},
 'records':b['records'],'traces':traces,'r198_errata':{'runs':len(err['records']),
 'CAST_WHIP_water_hp':sum(x['water_spell_hp_removed'] for x in err['records'] if x['policy']=='CAST_WHIP'),
 'DECLINE_WHIP_water_hp':sum(x['water_spell_hp_removed'] for x in err['records'] if x['policy']=='DECLINE_WHIP')}}
js_data=json.dumps(UI,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
# Preserve old 4-tab architecture, only expand selection list and append one section+controller.
old=old.replace('<title>VLAB • Bancada de Poder R197</title>','<title>VLAB R199 • Combates, Magias e Transformação TEST</title>')
old=old.replace('R197 + R198 · Perfis e combates TEST reais', 'R197 + R198 + R199 · Combates, magia e transformação em TEST')
old=old.replace('9 snapshots R197 · 38 lutas R198 · 0 benchmarks oficiais', 'R198 preservado · 32 novos combates TEST R199 · 0 benchmarks oficiais')
old=old.replace('<button class="tab" data-tab="combates">4 · Combates executados</button>', '<button class="tab" data-tab="combates">4 · Combates executados</button><button class="tab" data-tab="r199">5 · Poderes e transformação</button>')
old=old.replace("'rapido','padrao','detalhado','combates'", "'rapido','padrao','detalhado','combates','r199'")
section='''
<section id="r199" class="hidden"><div class="panel">
  <h2>R199 · Combates reais com magia, transformação e habilidade de Besta</h2>
  <p class="good">Os dados são extraídos de bancos SQLite R18 auditados. Esta aba <strong>consulta</strong> resultados; não finge executar um motor Python dentro do navegador.</p>
  <div class="grid" id="r199-kpis"></div>
  <div class="cols"><div><label for="r199-pair">Experimento executado</label><select id="r199-pair"><option value="magic">Ong Mefita × Lobo — magia e transformação</option><option value="beast">Capanga 1 × Lobo — Força Ancestral</option></select></div>
  <div><label for="r199-run">Recibo detalhado (seed/política)</label><select id="r199-run"></select></div></div>
  <div id="r199-summary"></div>
  <h3>Comparação pareada por seed</h3><div class="tablewrap"><table><thead><tr><th>Seed</th><th>Política</th><th>Resultado</th><th>Rodadas</th><th>HP final</th><th>PA gasto</th></tr></thead><tbody id="r199-rows"></tbody></table></div>
  <p class="warning">Duas políticas na mesma seed são ramos pareados, não duas amostras independentes. As duas censuras permanecem como censuras. Estado transformado de Ong depende de identidade do Espírito e reservas +54/+63 ainda incompletas. Força Ancestral +2 pode já estar incluída na ficha do Lobo.</p>
 </div><div class="panel"><h3>Eventos reais do combate selecionado</h3>
 <div class="tablewrap"><table><thead><tr><th>Evento</th><th>Ação</th><th>Teste/CA</th><th>Crítico</th><th>Dano / RD / HP retirado</th><th>PA</th></tr></thead><tbody id="r199-trace"></tbody></table></div>
 <p class="mini muted">Transformação: ativação/40 PA, duração, Vida adicional condicional e reversão; magia: ataque de Água e custo de 8 PA; Besta: Força Ancestral +2 em hipótese TEST. O dano de proteção temporária não é contado como Vida normal perdida.</p></div>
 <div class="panel"><h3>Errata métrica R198 — sem reescrever bancos históricos</h3><p id="r199-errata"></p><p class="warning">O laboratório preserva R198 e R197 integralmente. Não há aprovação de célula oficial, homologação da transformação nem sincronização da Party.</p></div>
</section>
<script type="application/json" id="r199-data">'''+js_data+'''</script>
<script>
(function(){
const D=JSON.parse(document.getElementById('r199-data').textContent), $=id=>document.getElementById(id);
const name=id=>({ONG_P2:'Ong',LOBO_P1:'Lobo',CAPANGA_P3:'Capanga 1'})[id]||id;
const groups={magic:['CAST_NORMAL','ACTIVATE_FORM_AND_CAST'],beast:['SOURCE_BASE_STAT_ONLY','ANCESTRAL_PLUS2_IF_NOT_INCLUDED']};
const polname={CAST_NORMAL:'Chicote (normal)',ACTIVATE_FORM_AND_CAST:'Transformação + Chicote',SOURCE_BASE_STAT_ONLY:'Força da ficha',ANCESTRAL_PLUS2_IF_NOT_INCLUDED:'Força Ancestral +2 TEST'};
const fmt=(x)=>x===null?'—':String(x);
$('r199-kpis').innerHTML=[['Lutas executadas',D.summary.fights],['Seeds distintas',D.summary.seed_blocks],['Ativações da forma',D.records.reduce((s,x)=>s+x.form_count,0)],['Magias lançadas',D.records.reduce((s,x)=>s+x.spell_count,0)]].map(([a,b])=>`<div class="stat"><strong>${b}</strong><small>${a}</small></div>`).join('');
function table(){
 const grp=$('r199-pair').value, policies=groups[grp], records=D.records.filter(x=>policies.includes(x.policy));
 $('r199-rows').innerHTML=records.map(r=>`<tr><td>${r.seed}</td><td>${polname[r.policy]}</td><td>${r.status==='FINISHED'?name(r.winner)+' vence':'CENSURADO'}</td><td>${r.rounds}</td><td>${Object.entries(r.hp_final).map(([k,v])=>name(k)+': '+v).join(' / ')}</td><td>${r.pa_total_spent}</td></tr>`).join('');
 $('r199-run').innerHTML=records.map(x=>`<option value="${x.id}">${x.seed} · ${polname[x.policy]}</option>`).join('');
 const count=Object.fromEntries(policies.map(p=>[p,records.filter(r=>r.policy===p)]));
 $('r199-summary').innerHTML='<div class="grid">'+policies.map(p=>{let rs=count[p];let x=rs.filter(r=>r.winner==='ONG_P2'||r.winner==='CAPANGA_P3').length;let y=rs.filter(r=>r.winner==='LOBO_P1').length;let n=rs.filter(r=>r.status!=='FINISHED').length;return `<div class="stat"><strong>${x} ED / ${y} Besta / ${n} cens.</strong><small>${polname[p]} · ${rs.length} ramos</small></div>`}).join('')+'</div>';
 trace();
}
function trace(){let id=$('r199-run').value;
 $('r199-trace').innerHTML=(D.traces[id]||[]).map(e=>e.type==='ATTACK'?`<tr><td>${e.seq}</td><td>${name(e.actor)} → ${name(e.defender)} (${e.damage_type})</td><td>${e.roll}/${e.CA} ${e.hit?'✓':'×'}</td><td>${e.crit==='NONE'?'—':e.crit}</td><td>${e.raw} / ${e.RD} / ${e.hp}</td><td>—</td></tr>`:`<tr><td>${e.seq}</td><td>${e.type} · ${name(e.actor)}</td><td>—</td><td>—</td><td>${e.temporary_hp_removed==null?'—':'Escudo '+e.temporary_hp_removed+' / Vida '+e.normal_hp_removed}</td><td>${e.pa_spent||0}</td></tr>`).join('')}
$('r199-pair').onchange=table;$('r199-run').onchange=trace;
$('r199-errata').textContent='R198 Chicote de Água: '+D.r198_errata.CAST_WHIP_water_hp+' HP efetivamente retirados; política sem Chicote: '+D.r198_errata.DECLINE_WHIP_water_hp+' HP mágicos. Dados derivados de 8 bancos originais, imutáveis.';
table();
})();
</script>
'''
assert old.endswith('</body></html>')
text=old.replace('</body></html>',section+'</body></html>')
dest=R199/'ui/VLAB_R199_COMBATES_MAGIA_TRANSFORMACAO_OFFLINE.html';dest.write_text(text)
pathlib.Path('/mnt/data/VLAB_R199_BANCADA_COMBATES_MAGIA_TRANSFORMACAO_OFFLINE.html').write_text(text)
print('PASS_R199_R198_PRESERVED_UI_ADDITIVE',len(text),'bytes',len(UI['records']),'runs',sum(len(x) for x in traces.values()),'events')
