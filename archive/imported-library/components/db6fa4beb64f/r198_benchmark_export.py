"""R198 experiment benchmark FROM executed R18 events; extend preserved R197 HTML, no fictitious execute button."""
import json,sqlite3,pathlib,statistics,csv,collections,hashlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
RESULTS=json.loads((ROOT/'evidence/R198_FIGHT_RESULTS.json').read_text())
SRC=json.loads((ROOT.parent/'work/r197/source/R197_SOURCE_SNAPSHOTS.json').read_text())
EXT=json.loads((ROOT/'source/R198_ACTOR_EXTENSION.json').read_text())['actors'][0]
PRE=json.loads((ROOT/'source/R198_PRE_REG.json').read_text())
NAMES={x['id']:x['name'] for x in SRC['actors']};NAMES[EXT['id']]=EXT['name']

traces={};byactor={};csvrows=[]
for r in RESULTS:
 if not r.get('db'):continue
 path=ROOT/'evidence/db'/r['db'];c=sqlite3.connect(f'file:{path}?mode=ro',uri=True)
 try:rows=[json.loads(x[0]) for x in c.execute('SELECT row_json FROM events ORDER BY seq')]
 finally:c.close()
 trace=[];actors={x:dict(attempts=0,hits=0,raw=0,post_rd=0,hp_removed=0,overkill=0,crit_pos=0,crit_neg=0,pa_spent=0) for x in r['pair']}
 for x in rows:
  d=x['detail'];ev=d.get('attack')
  if not ev:continue
  a=actors[ev['from']];a['attempts']+=1;a['hits']+=int(ev['hit']);a['raw']+=ev['raw'];a['post_rd']+=ev['net'];a['hp_removed']+=ev['hp_loss_actual'];a['overkill']+=ev['overkill'];a['crit_pos']+=int(ev['critical']=='POSITIVE');a['crit_neg']+=int(ev['critical']=='NEGATIVE')
  rec={'seq':x['seq'],'actor':ev['from'],'target':ev['to'],'score':ev['roll_score'],'ca':int(ev['ca_exact']),'hit':ev['hit'],'crit':ev['critical'],'rd':ev['rd_applied'],'raw':ev['raw'],'post_rd':ev['net'],'hp_loss':ev['hp_loss_actual'],'overkill':ev['overkill'],'hp_before':ev['before_hp'],'hp_after':ev['after_hp']}
  trace.append(rec)
  csvrows.append({'run_id':r['run_id'],'seed':r['seed'],'group':r['group'],**rec})
 traces[r['run_id']]=trace;byactor[r['run_id']]=actors

groups=[]
for pair in PRE['pairs']:
 allr=[x for x in RESULTS if x['pair']==pair]
 done=[x for x in allr if x['status']=='FINISHED']
 hold=[x for x in allr if x['status']=='PRECOMMIT_TIE_HOLD']
 wins=collections.Counter(x['winner'] for x in done)
 k=tuple(pair);expected=len(PRE['seeds']['development'])+len(PRE['seeds']['holdout'])
 assert len(allr)==expected
 s={'pair':pair,'labels':[NAMES[x] for x in pair], 'attempted_seed_blocks':len(allr),
    'executed_fights':len(done),'initiative_precommit_holds':len(hold),
    'censored':sum(z['status']=='CENSORED_HORIZON' for z in allr),
    'wins':{x:wins[x] for x in pair},
    'observed_win_rate':{x:(wins[x]/len(done) if done else None) for x in pair},
    'mean_rounds':statistics.mean(x['rounds'] for x in done) if done else None,
    'round_min_max':[min(x['rounds'] for x in done),max(x['rounds'] for x in done)] if done else None,
    'by_actor':{},'runs':[x['run_id'] for x in allr],
    'holdout_fights':sum(z['group']=='holdout' and z['status']=='FINISHED' for z in allr),
    'note':'Conditional physical baseline; same species/actor identities repeated, no general population estimator.'}
 for actor in pair:
  ar=[byactor[x['run_id']][actor] for x in done]
  attempts=sum(t['attempts'] for t in ar);hits=sum(t['hits'] for t in ar)
  s['by_actor'][actor]={'attempts':attempts,'hits':hits,'hit_rate_observed':hits/attempts if attempts else None,
    'post_rd_total':sum(t['post_rd'] for t in ar),'hp_removed_total':sum(t['hp_removed'] for t in ar),
    'damage_per_round_observed':sum(t['hp_removed'] for t in ar)/sum(x['rounds'] for x in done) if done else None,
    'crit_positive':sum(t['crit_pos'] for t in ar),'crit_negative':sum(t['crit_neg'] for t in ar),
    'pa_spent':sum(t['pa_spent'] for t in ar)}
 groups.append(s)

new={'version':'R198-MICROBENCH-EXECUTED-RESULTS-1','as_of':'2026-10-19','from_core':'R18 v0.8.1, 40 planned scenarios, 38 actual SQLite fights, 2 precommit initiative holds',
 'baseline':'R197 frozen retained, no change to official records','pre_reg_sha256':hashlib.sha256((ROOT/'source/R198_PRE_REG.json').read_bytes()).hexdigest(),
 'source197_sha256':hashlib.sha256((ROOT.parent/'work/r197/source/R197_SOURCE_SNAPSHOTS.json').read_bytes()).hexdigest(),
 'runs':RESULTS,'groups':groups,'actor_names':NAMES,'battle_traces':traces,
 'status':'LAB_EXPERIMENTAL_CONDITIONAL_SOURCE_PARTIAL','unique_pairs':4,'unique_actors':4,
 'executed_fights':sum(x['status']=='FINISHED' for x in RESULTS),
 'initiatives_held_pre_commit':sum(x['status']=='PRECOMMIT_TIE_HOLD' for x in RESULTS),
 'censored_fights':sum(x['status']=='CENSORED_HORIZON' for x in RESULTS),
 'seeds_per_pair':10,'seed_blocks_unique':10,'commits':sum(x.get('commits',0) for x in RESULTS),
 'attacks':sum(x.get('metrics',{}).get('attempts',0) for x in RESULTS),
 'native_events':sum(x.get('events',0) for x in RESULTS),
 'official_benchmark_cells':0,'certified_contracts':0,
 'full_ability_profiles_evaluated':False,
 'uncertainties':['Named Beast Luta/Initiative unconfirmed => scenario untrained','Capanga physical RD not published => assumed 0 only for LAB',
 'Liu and Capanga aggregate attack damage tags not literal','Lobo +2 Force status and grab not exercised','Cabra charge/push not exercised, Duplo is one literal damage expression',
 'Geometric contact is TEST scenario, not campaign map','R42 critical-negative as legacy lab policy','No spells and no PA-activation in basic-attack microbenchmark'],
 'audit':'independent local semantic readback before benchmark creation, not external formal review'}
(ROOT/'evidence/R198_BENCHMARK_RESULTS.json').write_text(json.dumps(new,ensure_ascii=False,indent=2))
with (ROOT/'evidence/R198_OFFENSIVE_RECEIPTS_DMG.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(csvrows[0]));w.writeheader();w.writerows(csvrows)

# Single addition to R197 user-facing HTML: retain its original script, data and 3 tabs unchanged.
p=(ROOT.parent/'work/r197/ui/VLAB_R197_BANCADA_PODER_OFFLINE.html').read_text()
assert p.count('data-tab="detalhado"')==1 and p.count("'detalhado'")==1
p=p.replace('data-tab="detalhado">3 · Evidência detalhada</button>',
 'data-tab="detalhado">3 · Evidência detalhada</button><button class="tab" data-tab="combates">4 · Combates executados</button>')
newsection='''<section id="combates" class="hidden"><div class="panel"><h2>R198 · Microbenchmark de combates realmente executados</h2><p class="good">Lutas obtidas por R18/v0.8.1 e registradas em SQLite; esta página carrega recibos já processados. O HTML offline <strong>não executa Python ou novos combates</strong>.</p><div class="grid" id="r198-stats"></div><div class="cols"><div><label for="r198-fighter">Combatente</label><select id="r198-fighter"></select></div><div><label for="r198-pair">Confronto de referência</label><select id="r198-pair"></select></div></div><div id="r198-summary"></div><h3>Execuções e seeds</h3><div class="tablewrap"><table><thead><tr><th>Seed</th><th>Grupo</th><th>Desfecho</th><th>Rodadas</th><th>HP final</th></tr></thead><tbody id="r198-runrows"></tbody></table></div><div class="cols"><div><label for="r198-run">Recibo de uma luta</label><select id="r198-run"></select></div><div><label for="r198-scope">Escopo</label><input id="r198-scope" type="text" disabled value="Somente ataques normais · TEST"/></div></div><h3>Ataques reais do combate selecionado</h3><div class="tablewrap"><table><thead><tr><th>#</th><th>Atacante</th><th>Teste / CA</th><th>Crítico</th><th>Dano bruto → pós-RD</th><th>HP retirado</th></tr></thead><tbody id="r198-trace"></tbody></table></div><p class="warning">Proficiências não registradas foram tratadas como hipóteses sem treinamento; contato e tipagem não são fatos da campanha. O Capanga usa RD0 <strong>somente como hipótese explícita</strong>. Habilidades especiais omitidas tornam o piloto uma avaliação de ataques básicos, não do poder integral da ficha. Dois empates de iniciativa foram recusados antes do primeiro commit, sem vitória fictícia.</p></div></section>'''
p=p.replace('<footer>',newsection+'<footer>',1)
p=p.replace("['rapido','padrao','detalhado']","['rapido','padrao','detalhado','combates']",1)
json_data=json.dumps(new,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
addon=f'''<script id="r198-data" type="application/json">{json_data}</script>
<script>
const RB=JSON.parse(document.getElementById('r198-data').textContent), el=id=>document.getElementById(id), show=x=>Number(x).toLocaleString('pt-BR',{{maximumFractionDigits:1}});
function pop(id,items,label){{el(id).innerHTML='';items.forEach(x=>{{const opt=document.createElement('option');opt.value=x;opt.textContent=label(x);el(id).add(opt)}});}}
const allF=[...new Set(RB.groups.flatMap(x=>x.pair))];pop('r198-fighter',allF,id=>RB.actor_names[id]||id);
function reloadPairs(){{let who=el('r198-fighter').value,options=RB.groups.filter(x=>x.pair.includes(who));pop('r198-pair',options.map(x=>x.pair.join('|')),s=>s.split('|').map(x=>RB.actor_names[x]).join(' × '));renderPair();}}
function renderPair(){{const key=el('r198-pair').value;const g=RB.groups.find(x=>x.pair.join('|')===key);if(!g)return;
 el('r198-stats').innerHTML=[["Lutas executadas",RB.executed_fights],["Empates sem commit",RB.initiatives_held_pre_commit],["Pares de referência",RB.unique_pairs],["Benchmarks oficiais",RB.official_benchmark_cells]].map(([k,v])=>`<div class="stat"><strong>${{v}}</strong><small>${{k}}</small></div>`).join('');
 el('r198-summary').innerHTML=`<h3>${{g.labels.join(' × ')}}</h3><div class="grid">${{g.pair.map(id=>`<div class="stat"><strong>${{g.wins[id]}} / ${{g.executed_fights}}</strong><small>Vitórias observadas · ${{RB.actor_names[id]}}</small></div>`).join('')}}<div class="stat"><strong>${{g.mean_rounds===null?'—':show(g.mean_rounds)}}</strong><small>Média de rodadas terminadas</small></div><div class="stat"><strong>${{g.initiative_precommit_holds}}</strong><small>Empate inicial não resolvido</small></div></div><p class="mini muted">Taxa observada entre duelos que iniciaram; não é chance universal de vitória. Seeds compartilhadas entre pares, não espécies independentes.</p><div class="tablewrap"><table><thead><tr><th>Ator</th><th>Acertos</th><th>Pós-RD</th><th>Vida retirada</th><th>Críticos +/−</th><th>PA</th></tr></thead><tbody>${{g.pair.map(id=>{{const a=g.by_actor[id];return `<tr><td>${{RB.actor_names[id]}}</td><td>${{a.hits}}/${{a.attempts}}</td><td>${{a.post_rd_total}}</td><td>${{a.hp_removed_total}}</td><td>${{a.crit_positive}}/${{a.crit_negative}}</td><td>${{a.pa_spent}}</td></tr>`}}).join('')}}</tbody></table></div>`;
 const rows=RB.runs.filter(r=>r.pair.join('|')===key);el('r198-runrows').innerHTML=rows.map(r=>`<tr><td>${{r.seed}}</td><td>${{r.group}}</td><td>${{r.status==='FINISHED'?RB.actor_names[r.winner]+' vence':r.status}}</td><td>${{r.rounds??'—'}}</td><td>${{r.hp_final?Object.entries(r.hp_final).map(([k,v])=>RB.actor_names[k]+': '+v).join(' / '):'—'}}</td></tr>`).join('');
 pop('r198-run',rows.filter(r=>r.db).map(r=>r.run_id),id=>id.slice(-8)+' · '+(RB.runs.find(r=>r.run_id===id).group));renderTrace();}}
function renderTrace(){{const id=el('r198-run').value;el('r198-trace').innerHTML=(RB.battle_traces[id]||[]).map(e=>`<tr><td>${{e.seq}}</td><td>${{RB.actor_names[e.actor]}}</td><td>${{e.score}} / ${{e.ca}} ${{e.hit?'✓':'×'}}</td><td>${{e.crit==='NONE'?'—':e.crit}}</td><td>${{e.raw}} → ${{e.post_rd}}</td><td>${{e.hp_loss}}</td></tr>`).join('');}}
el('r198-fighter').onchange=reloadPairs;el('r198-pair').onchange=renderPair;el('r198-run').onchange=renderTrace;reloadPairs();
</script>'''
p=p.replace('</body></html>',addon+'</body></html>',1)
p=p.replace('R197 · Fichas reais do Notion Mestre · Sem alterar ranks', 'R197 + R198 · Perfis e combates TEST reais · Sem alterar ranks',1)
p=p.replace('9 snapshots · 5 referências Prata 1 · 0 benchmarks oficiais','9 snapshots R197 · 38 lutas R198 · 0 benchmarks oficiais',1)
(RootHtml:=ROOT/'ui/VLAB_R198_BANCADA_COMBATES_OFFLINE.html').write_text(p)
print(json.dumps({'groups':len(groups),'executed':new['executed_fights'],'held':new['initiatives_held_pre_commit'],'traces':sum(len(y)for y in traces.values()),'html_bytes':RootHtml.stat().st_size},ensure_ascii=False))
