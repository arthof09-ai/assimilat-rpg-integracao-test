from pathlib import Path
root=Path(__file__).parents[1]
src=(root/'originais/PACOTE_ARENA_INOVADOR_TEST_02/ARENA_INOVADOR_TEST_02.html').read_text()
style='''<style>
.bridgecols{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:14px}.bridgegrid{display:grid;grid-template-columns:repeat(var(--n),minmax(0,1fr));gap:2px;margin-top:10px;max-width:540px}.bridgecell{aspect-ratio:1;border:1px solid #51647b;background:#273852;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:12px}.bridgecell.blocked{background:#666b78}.bridgecell .mark{background:#3378ac;color:white;border-radius:50%;min-width:17px;text-align:center;font-weight:bold}.bridgecell .enemy{background:#b84d64}.bridgewarning{padding:8px;border:1px solid #806f51;border-radius:8px;margin:8px 0;color:#f7ddb5}.bridgebtn{min-height:44px;min-width:48px}.bridgecontrols{display:flex;flex-wrap:wrap;gap:8px;align-items:center}.bridgecontrols input{flex:1;min-width:110px}.bridgeoutput{font-size:12px;overflow-wrap:anywhere;color:#bfd5f0}.bridgehelp{font-size:12px;color:#d2e1f7}@media(max-width:700px){.bridgecols{grid-template-columns:1fr}.bridgecell{font-size:9px}}
</style>'''
src=src.replace('</head>',style+'</head>')
panel='''<section class="panel" id="bridgePanel" aria-label="Ponte sintética de leitura TEST 04">
<h2>🔬 Ponte e replay TEST 04 — somente leitura</h2>
<p class="bridgewarning">MESTRE-SIDE • TEST • NÃO CANÔNICO. O replay mostra snapshots sintéticos da Arena, sem cálculo oficial de combate. Arquivo gerado serve para importar no Observatório TEST 03. Não compartilhar com a Party.</p>
<div class="bridgecontrols"><button id="bridgeCapture" class="tool bridgebtn">Capturar sequência TEST</button><button id="bridgeDownload" class="tool bridgebtn" disabled>↓ JSON para Observatório</button><button id="bridgePrev" class="tool bridgebtn" disabled>←</button><input id="bridgeSeek" type="range" min="0" max="0" value="0" disabled aria-label="Percorrer snapshots da ponte"><button id="bridgeNext" class="tool bridgebtn" disabled>→</button></div>
<p id="bridgeStatus" role="status" aria-live="polite" class="bridgeoutput">Ainda não capturado. Execute movimentos na Arena e toque em Capturar sequência TEST.</p>
<div class="bridgecols"><div><strong>Mapa de replay congelado</strong><div id="bridgeGrid" class="bridgegrid" role="img" aria-label="Nenhum snapshot"></div></div><div><strong id="bridgeStep">Sem replay</strong><p id="bridgeDetails" class="bridgehelp">O conteúdo é visual. Não modifica a Arena.</p></div></div>
</section>'''
src=src.replace('<div class="foot">',panel+'<div class="foot">',1)
bridge_js=r'''
// TEST04: o ledger é derivado exclusivamente de snapshots locais TEST02. NÃO consome VLAB real.
let bridgeDoc=null,bridgeIndex=0;
const unitAliases={b:'Exploradora TEST',w:'Conjurador TEST',e:'Criatura TEST',f:'Guardião TEST'};
function sameWalls(a,b){return JSON.stringify([...a].sort())===JSON.stringify([...b].sort());}
function bridgeMake(){
  // Apenas o sufixo que usa a malha atual. Alterações de parede rompem o contrato de grade estática do Observatório.
  const states=[...history,s];let start=states.length-1;
  while(start>0 && states[start-1].n===s.n && sameWalls(states[start-1].walls,s.walls))start--;
  const compatible=states.slice(start);const aliases=['b','w','e','f'];
  const units=aliases.map(id=>{const u=s.units.find(x=>x.id===id);return {id,label:unitAliases[id],mark:u.mark,team:u.team};});
  const events=compatible.map((st,i)=>{
    const positions={};for(const id of aliases){const u=st.units.find(x=>x.id===id);positions[id]=[u.x,u.y];}
    const prior=i>0?compatible[i-1]:null;
    const moved=prior&&aliases.some(id=>{const a=prior.units.find(x=>x.id===id),b=st.units.find(x=>x.id===id);return a.x!==b.x||a.y!==b.y;});
    return {id:'test04-'+String(i+1).padStart(3,'0'),type:moved?'POSITION':'ROUND_NOTE',title:'Snapshot sintético '+String(i+1),description:'Arena TEST 02 / cópia isolada. Frame declarado, sem cálculo ou autenticação VLAB.',frame:{positions}};
  });
  const walls=s.walls.map(key=>key.split(',').map(Number));
  return {doc:{schema:'assim.lab.vlab.readonly.v1',source:{kind:'SYNTHETIC_FIXTURE',scope:'MESTRE_ONLY',isolatedCopy:true,reference:'INOVADOR-TEST04-ARENA-LOCAL',exportedAt:'2026-10-22'},grid:{width:s.n,height:s.n,walls},units,events},discarded:start};
}
function bridgeRender(){const d=bridgeDoc;if(!d)return;const n=d.grid.width,ev=d.events[bridgeIndex];
  $('bridgeSeek').max=String(d.events.length-1);$('bridgeSeek').value=String(bridgeIndex);$('bridgeSeek').disabled=d.events.length<2;
  $('bridgePrev').disabled=bridgeIndex===0;$('bridgeNext').disabled=bridgeIndex>=d.events.length-1;
  $('bridgeStep').textContent=`Quadro ${bridgeIndex+1}/${d.events.length} • ${ev.type}`;
  $('bridgeDetails').textContent='Somente a posição dos quatro tokens e paredes fixas foi exportada. Intenções, PA, dano e alertas não são inferidos.';
  const board=$('bridgeGrid');board.style.setProperty('--n',String(n));board.replaceChildren();
  const walls=new Set(d.grid.walls.map(x=>x.join(',')));
  const places=new Map(Object.entries(ev.frame.positions).map(([id,xy])=>[xy.join(','),id]));
  for(let y=0;y<n;y++)for(let x=0;x<n;x++){const key=x+','+y,cell=document.createElement('span');cell.className='bridgecell'+(walls.has(key)?' blocked':'');
    if(places.has(key)){const u=d.units.find(z=>z.id===places.get(key)),mark=document.createElement('span');mark.className='mark'+(u.team==='enemy'?' enemy':'');mark.textContent=u.mark;mark.title=u.label;cell.appendChild(mark);}board.appendChild(cell);}
}
function bridgeCapture(){const result=bridgeMake();bridgeDoc=structuredClone(result.doc);bridgeIndex=0;
  $('bridgeDownload').disabled=false;
  $('bridgeStatus').textContent=`Snapshot TEST: ${bridgeDoc.events.length} quadro(s); ${result.discarded} histórico(s) anterior(es) excluídos por edição de paredes. Export compatível com schema sintético do Observatório TEST 03; nenhuma fonte oficial foi consultada.`;
  bridgeRender();return structuredClone(result);}
$('bridgeCapture').addEventListener('click',bridgeCapture);
$('bridgePrev').addEventListener('click',()=>{if(bridgeDoc){bridgeIndex=Math.max(0,bridgeIndex-1);bridgeRender();}});
$('bridgeNext').addEventListener('click',()=>{if(bridgeDoc){bridgeIndex=Math.min(bridgeDoc.events.length-1,bridgeIndex+1);bridgeRender();}});
$('bridgeSeek').addEventListener('input',ev=>{if(bridgeDoc){bridgeIndex=Number(ev.target.value);bridgeRender();}});
$('bridgeDownload').addEventListener('click',()=>{if(!bridgeDoc)return;const blob=new Blob([JSON.stringify(bridgeDoc,null,2)],{type:'application/json'});const uri=URL.createObjectURL(blob),link=document.createElement('a');link.href=uri;link.download='INOVADOR_TEST04_PONTE_OBSERVATORIO_SINTETICA.json';document.body.appendChild(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(uri),1000);});
window.__inovadorBridgeTest={capture:bridgeCapture,get:()=>bridgeDoc?structuredClone(bridgeDoc):null,index:()=>bridgeIndex};
'''
src=src.replace('window.__arenaTest={',bridge_js+'\nwindow.__arenaTest={',1)
src=src.replace('TEST 02 · NÃO CANÔNICO','TEST 04 (Arena 02 + ponte) · NÃO CANÔNICO')
src=src.replace('<title>','<title>TEST 04 • ',1)
out=root/'work/ARENA_PONTE_REPLAY_INOVADOR_TEST_04.html'
out.write_text(src)
print(out, out.stat().st_size)
