from pathlib import Path
import hashlib
source=Path('/mnt/data/TABLETOP_ASSIMILACAO_INOVADOR_TEST_05.html')
out=Path(__file__).resolve().parent/'TABLETOP_ASSIMILACAO_INOVADOR_TEST_06.html'
s=source.read_text(encoding='utf-8')
def rep(old,new,amount=1):
 global s
 assert s.count(old)==amount,(old[:60],s.count(old),amount)
 s=s.replace(old,new)
rep('Tabletop Assimilação • Inovador TEST 05','Tabletop Assimilação • Inovador TEST 06')
rep('TEST 05 · MESTRE-ONLY · NÃO CANÔNICO','TEST 06 · MESTRE-ONLY · NÃO CANÔNICO')
rep('🎞 Replay do laboratório — TEST 05','🎞 Replay do laboratório — TEST 06')
rep("'INOVADOR-TEST05-LOCAL'","'INOVADOR-TEST06-LOCAL'")
rep("'INOVADOR_TEST05_REPLAY_SINTETICO.json'","'INOVADOR_TEST06_REPLAY_SINTETICO.json'")
rep("'TEST 05: toque, zoom, arraste, redo e replay somente leitura.'","'TEST 06: mapa por camadas, minimapa e replay sintético somente leitura.'")
rep('.board-wrap{touch-action:none}.board-wrap.panMode', '.board-wrap{touch-action:none;position:relative}.board-wrap.panMode')
newcss='''
/* TEST06: camadas estritamente VISUAIS: não alteram estado de jogo nem replay. */
.board.hide-coords .coord{display:none}.board.hide-threat .cell.threat:after{display:none}.board.hide-reach .cell.reach{box-shadow:none}
.layerBar{display:flex;gap:7px;flex-wrap:wrap;align-items:center;margin:8px 0}.layerBar .tool{min-height:44px;font-size:12px}.layerBar button[aria-pressed="false"]{opacity:.65}
.navArea{display:grid;grid-template-columns:minmax(0,1fr) 164px;gap:12px;align-items:start;margin-top:8px}.miniBox{border:1px solid var(--edge);border-radius:12px;background:#0d1628;padding:8px}.miniBox canvas{width:100%;height:auto;aspect-ratio:1;touch-action:manipulation;display:block;cursor:crosshair;border-radius:6px;image-rendering:pixelated}.miniBox p{margin:6px 0 0;font-size:11px;color:var(--soft)}
#replayDelta{font-size:12px;padding:8px;border-left:2px solid #e4c36d;background:#1d2840;border-radius:4px;white-space:pre-line}
@media(max-width:510px){.navArea{grid-template-columns:minmax(0,1fr)}.miniBox{display:flex;align-items:center;gap:9px}.miniBox canvas{width:106px;flex:none}.miniBox p{flex:1}.layerBar .tool{flex:1;min-width:95px}}
'''
rep('@media(max-width:720px){.replayLayout',newcss+'\n@media(max-width:720px){.replayLayout')
old='''<div class="board-wrap" id="boardWrap"><div id="board" class="board" role="grid" aria-label="Arena tática interativa"></div></div><p class="hint">Toque numa peça'''
new='''<div class="layerBar" aria-label="Camadas de visualização"><span class="hint">Camadas:</span><button class="tool" type="button" data-layer="coords" aria-pressed="true">Coordenadas</button><button class="tool" type="button" data-layer="threat" aria-pressed="true">Ameaças TEST</button><button class="tool" type="button" data-layer="reach" aria-pressed="true">Casas alcançáveis TEST</button><button class="tool" id="focusToken" type="button">⌖ Focar selecionado</button></div><div class="navArea"><div class="board-wrap" id="boardWrap"><div id="board" class="board" role="grid" aria-label="Arena tática interativa"></div></div><div class="miniBox"><canvas id="miniMap" width="200" height="200" aria-label="Minimapa tático sintético, toque para navegar" role="img"></canvas><p>Minimapa: toque para navegar. A moldura mostra o recorte visível; não move personagens.</p></div></div><p class="hint">Toque numa peça'''
rep(old,new)
rep('''<p id="replayDescription" class="hint">Capture o histórico ou importe um JSON sintético.</p><div id="replayEvents"''','''<p id="replayDescription" class="hint">Capture o histórico ou importe um JSON sintético.</p><p id="replayDelta" aria-live="polite">Nenhuma comparação de posições.</p><div id="replayEvents"''')
# render() update the minimap when map rebuilt
rep("$('size').value=String(s.n);}","$('size').value=String(s.n);drawMini();}")
# pointer handlers replace
start=s.index('// Um dedo arrasta apenas em modo pan; dois dedos fazem pinça.')
end=s.index('// TEST05: ledger de snapshots.',start)
newjs='''// TEST06: gestos nativos. Clique e camera são independentes do estado de combate.
const pointers=new Map();let pinchStart=null,gestureUsed=false,clearGestureTimer=null;
const midPoints=()=>{const [a,b]=[...pointers.values()];return {x:(a.x+b.x)/2,y:(a.y+b.y)/2,d:Math.hypot(a.x-b.x,a.y-b.y)};};
function beginPinch(){if(pointers.size!==2)return;const m=midPoints(),r=wrap.getBoundingClientRect();pinchStart={zoom:zoomValue,d:Math.max(1,m.d),x:wrap.scrollLeft+m.x-r.left,y:wrap.scrollTop+m.y-r.top};gestureUsed=true;}
wrap.addEventListener('pointerdown',e=>{
 if(e.pointerType==='mouse'&&e.button!==0)return;
 if(clearGestureTimer!==null){clearTimeout(clearGestureTimer);clearGestureTimer=null;}
 pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});
 if(pointers.size===2)beginPinch();
 if(panMode||pointers.size>1){try{wrap.setPointerCapture(e.pointerId);}catch{}}
});
wrap.addEventListener('pointermove',e=>{
 const prev=pointers.get(e.pointerId);if(!prev)return;
 pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});
 if(pointers.size===2&&pinchStart){
  const m=midPoints(),r=wrap.getBoundingClientRect();
  const z=pinchStart.zoom*m.d/pinchStart.d;
  setZoom(z,m.x-r.left,m.y-r.top);
  const f=zoomValue/pinchStart.zoom;
  wrap.scrollLeft=pinchStart.x*f-(m.x-r.left);
  wrap.scrollTop=pinchStart.y*f-(m.y-r.top);
  gestureUsed=true;e.preventDefault();drawMini();
 }else if(panMode&&pointers.size===1){
  if(Math.hypot(e.clientX-prev.x,e.clientY-prev.y)>0){wrap.scrollLeft-=e.clientX-prev.x;wrap.scrollTop-=e.clientY-prev.y;gestureUsed=true;e.preventDefault();drawMini();}
 }
});
function endPointer(e){
 if(!pointers.has(e.pointerId))return;
 pointers.delete(e.pointerId);
 if(pointers.size<2)pinchStart=null;
 if(pointers.size===0){
  if(clearGestureTimer!==null)clearTimeout(clearGestureTimer);
  clearGestureTimer=setTimeout(()=>{gestureUsed=false;clearGestureTimer=null;},0);
 }
}
for(const name of ['pointerup','pointercancel','lostpointercapture'])wrap.addEventListener(name,endPointer);
wrap.addEventListener('click',e=>{if(gestureUsed||panMode){e.preventDefault();e.stopPropagation();gestureUsed=false;}},true);
wrap.addEventListener('dragstart',e=>e.preventDefault());

// TEST06: camadas e minimapa visuais; nenhum caminho novo ou resultado calculado.
const layers={coords:true,threat:true,reach:true};
function applyLayers(){for(const [name,show] of Object.entries(layers)){board.classList.toggle('hide-'+name,!show);const b=document.querySelector('[data-layer="'+name+'"]');b?.setAttribute('aria-pressed',String(show));}}
for(const button of document.querySelectorAll('[data-layer]'))button.addEventListener('click',()=>{const n=button.dataset.layer;layers[n]=!layers[n];applyLayers();});
function centerWorld(nx,ny){
 const wr=wrap.getBoundingClientRect(),br=board.getBoundingClientRect();
 const left=br.left-wr.left+wrap.scrollLeft,top=br.top-wr.top+wrap.scrollTop;
 wrap.scrollLeft=left+nx*board.scrollWidth-wrap.clientWidth/2;
 wrap.scrollTop=top+ny*board.scrollHeight-wrap.clientHeight/2;
 drawMini();
}
$('focusToken').addEventListener('click',()=>{const u=where(s.selected);if(u)centerWorld((u.x+.5)/s.n,(u.y+.5)/s.n);});
function drawMini(){
 const cvs=$('miniMap');if(!cvs)return;const ctx=cvs.getContext('2d');if(!ctx)return;
 const W=cvs.width,n=s.n,t=W/n;ctx.clearRect(0,0,W,W);ctx.fillStyle='#121d31';ctx.fillRect(0,0,W,W);
 const walls=new Set(s.walls),danger=new Set(s.danger);
 for(let y=0;y<n;y++)for(let x=0;x<n;x++){
  const kxy=x+','+y;ctx.fillStyle=walls.has(kxy)?'#8992a6':danger.has(kxy)?'#a65c3b':(x+y)%2===0?'#243d58':'#2a4763';ctx.fillRect(x*t+.4,y*t+.4,Math.max(.5,t-1),Math.max(.5,t-1));
 }
 for(const u of s.units){ctx.beginPath();ctx.arc((u.x+.5)*t,(u.y+.5)*t,Math.max(2.4,t*.32),0,Math.PI*2);ctx.fillStyle=u.id===s.selected?'#ffe18a':u.team==='enemy'?'#e26f74':'#68c7ff';ctx.fill();}
 const wr=wrap.getBoundingClientRect(),br=board.getBoundingClientRect();
 if(br.width&&br.height){
  const x=(wr.left-br.left)/br.width*W,y=(wr.top-br.top)/br.height*W;
  const w=wrap.clientWidth/br.width*W,h=wrap.clientHeight/br.height*W;
  ctx.strokeStyle='#fff5b1';ctx.lineWidth=2;ctx.strokeRect(Math.max(0,x),Math.max(0,y),Math.min(W-Math.max(0,x),w),Math.min(W-Math.max(0,y),h));
 }
}
$('miniMap').addEventListener('click',e=>{const rect=e.currentTarget.getBoundingClientRect();centerWorld(Math.max(0,Math.min(1,(e.clientX-rect.left)/rect.width)),Math.max(0,Math.min(1,(e.clientY-rect.top)/rect.height)));});
wrap.addEventListener('scroll',()=>drawMini(),{passive:true});
$('zoomIn').addEventListener('click',drawMini);$('zoomOut').addEventListener('click',drawMini);$('zoom').addEventListener('input',drawMini);$('centerMap').addEventListener('click',drawMini);

'''
s=s[:start]+newjs+s[end:]
# add prototypes, bound labels and timestamp:
rep("const clean=(str,max)=>typeof str==='string'&&str.length>0&&str.length<=max&&!/[<>\\u0000-\\u001f]/.test(str);", "const clean=(str,max)=>typeof str==='string'&&str.length>0&&str.length<=max&&!/[<>\\u0000-\\u001f]/.test(str);\nconst safeKey=k=>!['__proto__','prototype','constructor'].includes(k);")
rep("||ids.has(u.id))return 'unidade duplicada ou inválida'","||ids.has(u.id)||!safeKey(u.id))return 'unidade duplicada ou inválida'")
rep("if(Object.keys(p).length!==ids.size||Object.keys(p).some(id=>!ids.has(id)))","if(Object.keys(p).length!==ids.size||Object.keys(p).some(id=>!ids.has(id)||!safeKey(id)))")
rep("$('replayDescription').textContent='Capture o histórico ou importe um JSON sintético.';", "$('replayDescription').textContent='Capture o histórico ou importe um JSON sintético.';$('replayDelta').textContent='Nenhuma comparação de posições.';")
rep("$('replayDescription').textContent=ev.title+' — '+ev.description;", "$('replayDescription').textContent=ev.title+' — '+ev.description;\n $('replayDelta').textContent=prev?Object.entries(ev.frame.positions).map(([id,pos])=>({id,pos,before:prev.frame.positions[id]})).filter(x=>x.pos[0]!==x.before[0]||x.pos[1]!==x.before[1]).map(x=>{const name=d.units.find(u=>u.id===x.id).label;return name+': ('+(x.before[0]+1)+','+(x.before[1]+1)+') → ('+(x.pos[0]+1)+','+(x.pos[1]+1)+')';}).join('\\n')||'Nenhuma unidade mudou de posição neste quadro.':'Quadro inicial: posições declaradas na fixture TEST.';")
rep("window.__inovadorTest05={", "window.__inovadorTest05={")  # no-op for reference
rep("setZoom(44);drawReplay();", "window.__inovadorTest06={layers:()=>({...layers}),centerWorld,drawMini,gesture:()=>({active:gestureUsed,count:pointers.size}),miniSize:()=>$('miniMap').width};\napplyLayers();setZoom(44);drawReplay();")
assert 'TEST06' in s and 'miniMap' in s
out.write_text(s,encoding='utf-8')
print(out, len(s.encode()), hashlib.sha256(s.encode()).hexdigest())
