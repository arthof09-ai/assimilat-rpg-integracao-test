"""Preserves R197 interface and R198 microbench HTML, adds actual PA-spell fight receipts."""
import json,pathlib,sqlite3
ROOT=pathlib.Path(__file__).resolve().parents[1]
res=json.loads((ROOT/'evidence/R198_MAGIC_RESULTS.json').read_text())
records=[]
for r in res:
 if not r.get('db'):continue
 db=ROOT/'evidence/magic_db'/r['db'];c=sqlite3.connect(f'file:{db}?mode=ro',uri=True)
 try:rows=[json.loads(q[0]) for q in c.execute('SELECT row_json FROM events ORDER BY seq')]
 finally:c.close()
 spells=[{'seq':x['seq'],'attack':x['detail']['attack'],'debit':x['detail']['PA_debit_event']} for x in rows if x['kind']=='SOURCE_SPELL_WHIP_WITH_PA']
 records.append({**r,'spell_receipts':[{'seq':z['seq'],'attack_score':z['attack']['roll_score'],'hit':z['attack']['hit'],
 'critical':z['attack']['critical'],'raw':z['attack']['raw'],'rd':z['attack']['rd_applied'],'net':z['attack']['net'],
 'hp_loss_actual':z['attack']['hp_loss_actual'],'PA_before':z['debit']['PA_before'],'PA_after':z['debit']['PA_after']}
 for z in spells]})

magic={'version':'R198-WATER-WHIP-REAL-FIGHTS-v1','records':records,
       'no_spell_in_decline_policy':all(x['spell_count']==0 for x in res if x['policy']=='DECLINE_WHIP'),
       'total_pa_spent':sum(x['metrics']['pa_spent'] for x in res),
       'casts':sum(x['spell_count'] for x in res),
       'distinct_seeds':len(set(x['seed'] for x in res)),
       'metadata':{'canonical_status':'LAB_TEST_WITH_ATTACK_SPELL_CRITICAL_AND_RANGE_HYPOTHESES','source':'https://app.notion.com/p/2b6c2b324ede82a2b415019eae21eaf5',
          'source_spell':'M - Chicote de Água — Ataque 4d6+INT; 8 PA; 8d6+28; alvos corpo a corpo TEST','no_canonical_rank_change':True}}
(ROOT/'evidence/R198_MAGIC_BENCHMARK.json').write_text(json.dumps(magic,ensure_ascii=False,indent=2))
p=(ROOT/'ui/VLAB_R198_BANCADA_COMBATES_OFFLINE.html').read_text()
insert='''<div class="panel"><h2>R198 · Habilidade com PA executada (piloto separado)</h2><p><strong>Ong Mefita Prata 2 × Lobo da Caverna Prata 1.</strong> Compare Chicote de Água (8 PA, ataque de Água) com declinar a magia, nas mesmas quatro seeds. São oito lutas adicionais, sem misturá-las com as 38 lutas da matriz básica.</p><div class="grid" id="magic-kpis"></div><div class="tablewrap"><table><thead><tr><th>Seed</th><th>Política</th><th>Vitória</th><th>Rodadas</th><th>Lançamentos</th><th>PA</th><th>HP do Lobo</th></tr></thead><tbody id="magic-rows"></tbody></table></div><div class="cols"><div><label for="magic-seed">Recibos do Chicote</label><select id="magic-seed"></select></div><div><p class="mini muted">Cada lançamento associa o ataque e o débito de 8 PA na mesma transação SQLite R18. Consulta, não simulação local do navegador.</p></div></div><div class="tablewrap"><table><thead><tr><th>Commit</th><th>Ataque</th><th>Acerto</th><th>Dano pós-RD</th><th>PA antes → depois</th></tr></thead><tbody id="magic-trace"></tbody></table></div><p class="warning">Ponte de ataque mágico em TEST: alcance e economia de ação assumidos para contato, crítico de ataque mágico submetido condicionalmente ao v0.8.1, desconto de Evocação e bônus de itens não aplicados sem fonte específica. Nenhuma homologação oficial.</p></div>'''
needle='</p></div></section><footer>'
assert p.count(needle)==1
p=p.replace(needle,'</p></div>'+insert+'</section><footer>',1)
inline=json.dumps(magic,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
script=f'''<script type="application/json" id="r198-magic-data">{inline}</script>
<script>
const Mg=JSON.parse(document.getElementById('r198-magic-data').textContent), mid=id=>document.getElementById(id);
mid('magic-kpis').innerHTML=[["Lutas com/sem magia",Mg.records.length],["Seeds pareadas",Mg.distinct_seeds],["Magias lançadas",Mg.casts],["PA gasto",Mg.total_pa_spent]].map(([l,v])=>`<div class="stat"><strong>${{v}}</strong><small>${{l}}</small></div>`).join('');
mid('magic-rows').innerHTML=Mg.records.map(r=>`<tr><td>${{r.seed}}</td><td>${{r.policy==='CAST_WHIP'?'Chicote':'Sem Chicote'}}</td><td>${{r.winner==='LOBO_P1'?'Lobo':'Ong'}}</td><td>${{r.rounds}}</td><td>${{r.spell_count}}</td><td>${{r.metrics.pa_spent}}</td><td>${{r.hp_final.LOBO_P1}}</td></tr>`).join('');
for(const r of Mg.records.filter(x=>x.policy==='CAST_WHIP')){{let o=document.createElement('option');o.value=r.run_id;o.textContent=String(r.seed);mid('magic-seed').add(o)}}
function magicReceipt(){{const r=Mg.records.find(x=>x.run_id===mid('magic-seed').value);mid('magic-trace').innerHTML=(r?.spell_receipts||[]).map(e=>`<tr><td>${{e.seq}}</td><td>${{e.attack_score}}</td><td>${{e.hit?'✓':'×'}}</td><td>${{e.net}}</td><td>${{e.PA_before}} → ${{e.PA_after}}</td></tr>`).join('');}}
mid('magic-seed').onchange=magicReceipt;magicReceipt();
</script>'''
p=p.replace('</body></html>',script+'</body></html>',1)
q=ROOT/'ui/VLAB_R198_COMBATES_E_MAGIA_OFFLINE.html';q.write_text(p)
print('HTML',q,q.stat().st_size,'magic',magic['casts'],'PA',magic['total_pa_spent'])
