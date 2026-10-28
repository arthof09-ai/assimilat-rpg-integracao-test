from pathlib import Path
p=Path('/mnt/data/tabletop_run008/public/app.js')
s=p.read_text()
s=s.replace('Tabletop Assimilação — TEST20–23','Tabletop Assimilação — TEST24–26')
s=s.replace("let storageState='COMMITTED_VERIFIED',storageUncertain=null,pendingRestore=null,restoreDialogOpen=false;","let storageState='COMMITTED_VERIFIED',storageUncertain=null,pendingRestore=null,restoreDialogOpen=false;\n// Régua visual, não persistida e sem regras oficiais: um par de células da cena ativa.\nlet rulerA=null,rulerB=null,rulerSceneId=null;")
s=s.replace("function clickCell(x,y){if(gesture.suppress)return;const s=scene(),key=xy(x,y),at=s.units.find(u=>u.x===x&&u.y===y),u=selected();lastCell={x,y};\n if(s.mode==='pan')return;", """function clickCell(x,y){if(gesture.suppress)return;const s=scene(),key=xy(x,y),at=s.units.find(u=>u.x===x&&u.y===y),u=selected();lastCell={x,y};
 if(s.mode==='pan')return;
 if(s.mode==='measure'){
  if(rulerSceneId!==s.id||rulerA===null||rulerB!==null){rulerA={x,y};rulerB=null;rulerSceneId=s.id;}
  else rulerB={x,y};
  renderBoard(s);renderRuler();
  return;
 }""")
s=s.replace(" const old=JSON.stringify({walls:s.walls,danger:s.danger,terrain:s.terrain});\n snap();", " const old=JSON.stringify({walls:s.walls,danger:s.danger,terrain:s.terrain});\n const previousTopology=topology(s);\n snap();")
s=s.replace(" if(s.mode==='wall'){s.frames=[];s.frameTopology=null;}\n commit(s,'Terreno TEST editado em '+(x+1)+','+(y+1)+'.');", """ // Topologia é propriedade do mapa, não do botão escolhido: qualquer modo
 // pode remover paredes. Alteração cosmética/perigo preserva replay válido.
 if(topology(s)!==previousTopology){s.frames=[];s.frameTopology=null;}
 commit(s,'Terreno TEST editado em '+(x+1)+','+(y+1)+'.');""")
s=s.replace("if(!['play','pan','wall','danger','terrain','erase','place'].includes(mode))return;s.mode=mode;gesture.suppress=false;render();", "if(!['play','pan','wall','danger','terrain','erase','place','measure'].includes(mode))return;\n if(mode!==s.mode){rulerA=null;rulerB=null;rulerSceneId=null;}\n s.mode=mode;gesture.suppress=false;render();")
s=s.replace("!['play','pan','wall','danger','terrain','erase','place'].includes(s.mode)","!['play','pan','wall','danger','terrain','erase','place','measure'].includes(s.mode)")
s=s.replace(" if(reach.has(key))cls+=' reachable';", " if(reach.has(key))cls+=' reachable';\n  if(rulerSceneId===s.id&&rulerA&&xy(rulerA.x,rulerA.y)===key)cls+=' ruler-point ruler-start';\n  if(rulerSceneId===s.id&&rulerB&&xy(rulerB.x,rulerB.y)===key)cls+=' ruler-point ruler-end';")
s=s.replace("function render(){const t0=performance.now(),s=scene();", "function render(){const t0=performance.now(),s=scene();")
s=s.replace("drawMinimap();renderReplay();renderLast=", "drawMinimap();renderRuler();renderReplay();renderLast=")
s=s.replace("vp.scrollTop=worldY*after-y;drawMinimap();}","vp.scrollTop=worldY*after-y;drawMinimap();renderRuler();}")
# Add ruler in DOM after board; attach SVG layer as child of board, inserted as final DOM child after tiles to preserve tiles.
s=s.replace("board.replaceChildren(frag);board.style.setProperty('--n',n);", "board.replaceChildren(frag);board.append($('rulerOverlay'));board.style.setProperty('--n',n);")
# But moving rulerOverlay element into board will be removed on second board resize by replaceChildren; hold external reference const below fix
s=s.replace("const board=$('board'),vp=$('viewport');let cachedN=0,tiles=[];", "const board=$('board'),vp=$('viewport'),rulerSvg=$('rulerOverlay');let cachedN=0,tiles=[];")
s=s.replace("board.append($('rulerOverlay'));", "board.append(rulerSvg);")
# Insert renderRuler after renderLog and before render()
needle="function render(){const t0=performance.now(),s=scene();"
insert="""function renderRuler(){
 const s=scene(),root=$('rulerOverlay'),line=$('rulerSegment'),status=$('rulerStatus');
 const show=s.mode==='measure'&&rulerSceneId===s.id&&rulerA;
 root.hidden=!show;const cell=zoom+2;root.setAttribute('width',String(s.n*cell));root.setAttribute('height',String(s.n*cell));
 if(!show){status.textContent='Régua: dois toques no mapa · nenhuma regra de alcance.';return;}
 if(!rulerB){line.setAttribute('x1',String((rulerA.x+.5)*cell));line.setAttribute('y1',String((rulerA.y+.5)*cell));line.setAttribute('x2',String((rulerA.x+.5)*cell));line.setAttribute('y2',String((rulerA.y+.5)*cell));status.textContent=`Régua: início ${rulerA.x+1},${rulerA.y+1} · toque a segunda casa.`;return;}
 line.setAttribute('x1',String((rulerA.x+.5)*cell));line.setAttribute('y1',String((rulerA.y+.5)*cell));line.setAttribute('x2',String((rulerB.x+.5)*cell));line.setAttribute('y2',String((rulerB.y+.5)*cell));
 const dx=Math.abs(rulerA.x-rulerB.x),dy=Math.abs(rulerA.y-rulerB.y);
 status.textContent=`Régua TEST: ${rulerA.x+1},${rulerA.y+1} → ${rulerB.x+1},${rulerB.y+1} · Manhattan ${dx+dy} casas · reta ${Math.hypot(dx,dy).toFixed(2)} casas (geométrico, não canônico).`;
}
"""
assert needle in s
s=s.replace(needle,insert+needle)
# fix tile loop currently loops tiles which doesn't include svg; fine
s=s.replace("function switchScene(id){", "function switchScene(id){")
# Reset visually on scene switch via render resets because rulerSceneId other scene => hidden. When switch back same id old ruler reappears; noncanonical fine but no influence scene data.
s=s.replace("function togglePlayback(){", "function togglePlayback(){")
needle="$('replayImport').onchange=async e=>{"
assert needle in s
s=s.replace(needle,"document.addEventListener('visibilitychange',()=>{if(document.hidden&&playTimer!==null){stopReplay();note('Replay pausado: a aba ficou em segundo plano.');}});\n"+needle)
s=s.replace("zoom:v=>cameraScale(v),lastRenderMs", "zoom:v=>cameraScale(v),ruler:()=>({scene:rulerSceneId,start:rulerA?clone(rulerA):null,end:rulerB?clone(rulerB):null,text:$('rulerStatus').textContent}),lastRenderMs")
p.write_text(s)
idx=Path('/mnt/data/tabletop_run008/public/index.html')
h=idx.read_text()
h=h.replace('TEST 22 · DEMONSTRAÇÃO SINTÉTICA','TEST 25 · DEMONSTRAÇÃO SINTÉTICA')
h=h.replace('<button class="btn" data-mode="place">◉ Posicionar</button>', '<button class="btn" data-mode="place">◉ Posicionar</button><button class="btn" data-mode="measure" title="Dois toques: somente medida geométrica TEST" aria-label="Ativar régua geométrica experimental">📏 Régua</button>')
h=h.replace('<span id="fovStatus" class="small">FOV desligado</span>', '<span id="fovStatus" class="small">FOV desligado</span><span id="rulerStatus" class="small" role="status" aria-live="polite">Régua: dois toques no mapa · nenhuma regra de alcance.</span>')
h=h.replace('<div id="board" class="board" role="grid" aria-label="Tabuleiro de combate experimental"></div>', '<div id="board" class="board" role="grid" aria-label="Tabuleiro de combate experimental"><svg id="rulerOverlay" class="rulerOverlay" aria-hidden="true" hidden><line id="rulerSegment" x1="0" y1="0" x2="0" y2="0" /></svg></div>')
idx.write_text(h)
css=Path('/mnt/data/tabletop_run008/public/styles.css')
c=css.read_text()+"""
/* TEST25: régua semântica puramente visual, sem bloquear toques ou calcular combate. */
.board{position:relative}
.rulerOverlay{position:absolute;left:0;top:0;pointer-events:none;overflow:visible;z-index:9}
.rulerOverlay[hidden]{display:none}
.rulerOverlay line{stroke:#ffd66b;stroke-width:4;stroke-linecap:round;stroke-dasharray:6 5;filter:drop-shadow(0 1px 3px #000)}
.tile.ruler-start{outline:3px solid #5ce8dd;outline-offset:-3px}
.tile.ruler-end{outline:3px solid #ffcd64;outline-offset:-3px}
#rulerStatus{display:inline-block;max-width:100%;white-space:normal;color:#dceca4}
@media(max-width:560px){#rulerStatus{width:100%}}
"""
css.write_text(c)
print('patched',len(s),len(h),len(c))
