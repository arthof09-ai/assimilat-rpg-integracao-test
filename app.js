/* Tabletop Assimilação — TEST 07–15, FRONT-END AUTORAL / SINTÉTICO.
 * Não contém motores de combate, contas, rede, credenciais ou dados canônicos.
 * TEST 06 original preservado separadamente; esta é evolução do modelo visual.
 */
(()=>{'use strict';
const $=id=>document.getElementById(id), clone=x=>JSON.parse(JSON.stringify(x));
const MAX_SCENES=8, MAX_UNITS=30, MAX_EVENTS=100, MAX_LOGS=80, MAX_FILE=750000;
const KEY='assim.tabletop.synthetic.workspace.v1', WORKSCHEMA='assim.tabletop.synthetic.workspace.v1', REPLAYSCHEMA='assim.lab.vlab.readonly.v1';
const validId=x=>typeof x==='string'&&/^[a-z0-9_-]{1,32}$/.test(x)&&!['__proto__','constructor','prototype'].includes(x);
const textOK=(x,max=80)=>typeof x==='string'&&x.length>0&&x.length<=max&&!/[<>\u0000-\u001f]/.test(x);
const plain=x=>x!==null&&typeof x==='object'&&!Array.isArray(x)&&Object.getPrototypeOf(x)===Object.prototype;
const safeKeys=(x)=>plain(x)&&Object.keys(x).every(k=>!['__proto__','constructor','prototype'].includes(k));
const allowedSize=[5,7,10,20], xy=(x,y)=>`${x},${y}`, inside=(x,y,n)=>Number.isInteger(x)&&Number.isInteger(y)&&x>=0&&y>=0&&x<n&&y<n;
const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const stamp=()=>new Date().toISOString().slice(0,19);
const unit=(id,name,mark,team,x,y)=>({id,name,mark,team,x,y,range:1,hp:100,soul:50,pa:60});
function newScene(id='c1',name='Cena de exploração TEST',n=7){return {id,name,n,walls:[],danger:[],terrain:{},units:[unit('u1','Exploradora TEST','E','ally',1,1),unit('u2','Conjurador TEST','C','ally',1,3),unit('u3','Criatura TEST','X','enemy',n-2,2)],selected:'u1',mode:'play',round:1,stepsUsed:0,acted:false,logs:['Cena sintética criada; nenhuma fonte oficial.'],notes:'',frames:[],frameTopology:null,explored:[],fovEnabled:false,fovRadius:8};}
const defaultWorkspace=()=>({schema:WORKSCHEMA,version:1,active:'c1',scenes:[newScene()]});
let workspace=defaultWorkspace(),history=[],future=[],zoom=44,playTimer=null,viewReplay=null,frameIndex=0,renderLast=0;
let editingNew=false,editingId=null,lastCell=null,gesture={pointers:new Map(),start:null,suppress:false,dragged:false};
const scene=()=>workspace.scenes.find(s=>s.id===workspace.active), selected=()=>scene().units.find(u=>u.id===scene().selected);
const note=t=>{$('message').textContent=t;};
function pushLog(s,t){s.logs.unshift(`[${stamp()}] ${t}`);s.logs=s.logs.slice(0,MAX_LOGS);}
function migrateWorkspace(w){
 // Migration limited to TEST15 v1 fields; do not rewrite unknown schema versions.
 if(!safeKeys(w)||w.schema!==WORKSCHEMA||w.version!==1||!Array.isArray(w.scenes))return w;
 for(const sc of w.scenes){if(safeKeys(sc)){
   if(!Object.hasOwn(sc,'explored'))sc.explored=[];
   if(!Object.hasOwn(sc,'fovEnabled'))sc.fovEnabled=false;
   if(!Object.hasOwn(sc,'fovRadius'))sc.fovRadius=8;
 }}return w;
}
function validateScene(s){
 if(!safeKeys(s)||!validId(s.id)||!textOK(s.name,70)||!allowedSize.includes(s.n)||!Array.isArray(s.units)||s.units.length>MAX_UNITS||!Array.isArray(s.walls)||!Array.isArray(s.danger)||!safeKeys(s.terrain)||!Array.isArray(s.logs)||s.logs.length>MAX_LOGS||!textOK(s.mode,20)||!['play','pan','wall','danger','terrain','erase','place'].includes(s.mode)||!Number.isSafeInteger(s.round)||s.round<1||s.round>999999||!Number.isSafeInteger(s.stepsUsed)||s.stepsUsed<0||s.stepsUsed>4||typeof s.acted!=='boolean'||typeof s.notes!=='string'||s.notes.length>800||!Array.isArray(s.frames)||s.frames.length>MAX_EVENTS)return false;
 const ids=new Set(),where=new Set();for(const u of s.units){if(!safeKeys(u)||!validId(u.id)||ids.has(u.id)||!textOK(u.name,48)||!textOK(u.mark,2)||!['ally','enemy','neutral'].includes(u.team)||!inside(u.x,u.y,s.n)||where.has(xy(u.x,u.y))||!Number.isInteger(u.range)||u.range<1||u.range>20||![u.hp,u.soul,u.pa].every(v=>Number.isInteger(v)&&v>=0&&v<=99999))return false;ids.add(u.id);where.add(xy(u.x,u.y));}
 if(s.selected!==null&&!ids.has(s.selected))return false;
 for(const list of [s.walls,s.danger]){if(list.length>s.n*s.n||new Set(list).size!==list.length)return false;for(const key of list){if(typeof key!=='string'||!/^\d+,\d+$/.test(key))return false;const [x,y]=key.split(',').map(Number);if(!inside(x,y,s.n)||where.has(key))return false;}}
 if(s.walls.some(x=>s.danger.includes(x)||Object.hasOwn(s.terrain,x)))return false;
 for(const [k,v] of Object.entries(s.terrain)){if(!/^\d+,\d+$/.test(k)||!['grass','sand','water'].includes(v))return false;const [x,y]=k.split(',').map(Number);if(!inside(x,y,s.n))return false;}
 if(s.logs.some(x=>typeof x!=='string'||x.length>400||/[<>]/.test(x)))return false;
 if(s.frameTopology!==null&&s.frameTopology!==topology(s))return false;
 if(s.frames.length>0&&s.frameTopology===null)return false;
 if(!Array.isArray(s.explored)||s.explored.length>s.n*s.n||new Set(s.explored).size!==s.explored.length||typeof s.fovEnabled!=='boolean'||!Number.isSafeInteger(s.fovRadius)||s.fovRadius<2||s.fovRadius>20)return false;
 for(const k of s.explored){if(typeof k!=='string'||!/^\d+,\d+$/.test(k))return false;const [x,y]=k.split(',').map(Number);if(!inside(x,y,s.n))return false;}
 for(const f of s.frames){if(!safeKeys(f)||!textOK(f.title,100)||!safeKeys(f.positions)||Object.keys(f.positions).length!==ids.size)return false;const occupied=new Set();for(const id of ids){const p=f.positions[id];if(!Array.isArray(p)||p.length!==2||!inside(p[0],p[1],s.n)||s.walls.includes(xy(...p))||occupied.has(xy(...p)))return false;occupied.add(xy(...p));}if(Object.keys(f.positions).some(k=>!ids.has(k)||!validId(k)))return false;}
 return true;
}
function validateWorkspace(w){if(!safeKeys(w)||w.schema!==WORKSCHEMA||w.version!==1||!Array.isArray(w.scenes)||w.scenes.length<1||w.scenes.length>MAX_SCENES||!validId(w.active))return false;const ids=new Set();for(const s of w.scenes){if(!validateScene(s)||ids.has(s.id))return false;ids.add(s.id);}return ids.has(w.active);}
function persistChecked(candidate){
 if(!validateWorkspace(candidate))throw Error('Estado TEST inválido');
 const serialized=JSON.stringify(candidate);
 if(serialized.length>MAX_FILE)throw Error('Salvamento acima de 750 KB; exporte um backup menor.');
 const previous=localStorage.getItem(KEY);
 try{
  localStorage.setItem(KEY,serialized);
  if(localStorage.getItem(KEY)!==serialized)throw Error('Verificação de leitura local divergente');
 }catch(error){
  // If write took place but readback failed, attempt rollback; fail closed either way.
  try{const now=localStorage.getItem(KEY);if(now!==previous){if(previous===null)localStorage.removeItem(KEY);else localStorage.setItem(KEY,previous);}}catch(_){}
  throw error;
 }
 return true;
}
function saveLocal(quiet=true){try{persistChecked(workspace);$('storageStatus').textContent='Salvo e relido neste navegador · '+stamp();if(!quiet)note('Cenas salvas e conferidas. Exporte backup para não perder dados ao limpar o Chrome.');return true;}catch(e){$('storageStatus').textContent='NÃO SALVO: '+e.message+' • exporte backup';if(!quiet)note('FALHA ao salvar: '+e.message+'. As alterações atuais podem se perder ao reabrir.');return false;}}
function restoreCandidate(raw){
 const candidate=migrateWorkspace(clone(raw));
 // CRITICAL: write candidate first, then swap active workspace and render.
 persistChecked(candidate);
 stopReplay();workspace=candidate;history=[];future=[];clearReplay();closeTokenForm();render();center();
 $('storageStatus').textContent='Backup restaurado, gravado e relido · '+stamp();
 return true;
}
function loadLocal(){try{const raw=localStorage.getItem(KEY);if(!raw)return; if(raw.length>MAX_FILE)throw Error('salvamento acima do limite');const val=JSON.parse(raw);migrateWorkspace(val);if(!validateWorkspace(val))throw Error('estado armazenado inválido');workspace=val;}catch(e){$('storageStatus').textContent='Salvamento anterior rejeitado: '+e.message+'; cena inicial segura.';}}
function download(obj,name){const blob=new Blob([JSON.stringify(obj)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);}
async function readJSON(file){if(!file||file.size>MAX_FILE)throw Error('Arquivo acima do limite de 750 KB');return JSON.parse(await file.text());}
function positions(s){return Object.fromEntries(s.units.map(u=>[u.id,[u.x,u.y]]));}
function topology(s){return JSON.stringify({n:s.n,walls:[...s.walls].sort(),ids:s.units.map(x=>x.id).sort()});}
function captureFrame(s,title){const top=topology(s);if(s.frameTopology!==top){s.frames=[];s.frameTopology=top;}s.frames.push({title,positions:positions(s)});if(s.frames.length>MAX_EVENTS)s.frames.shift();}
function snap(){history.push(clone(workspace));if(history.length>40)history.shift();future=[];}
function commit(s,msg,record=false){pushLog(s,msg);if(record)captureFrame(s,msg);render();saveLocal();}
function undo(){if(!history.length)return note('Nada para desfazer.');stopReplay();future.push(clone(workspace));workspace=history.pop();render();saveLocal();note('Alteração desfeita.');}
function redo(){if(!future.length)return note('Nada para refazer.');stopReplay();history.push(clone(workspace));workspace=future.pop();render();saveLocal();note('Alteração refeita.');}
function nextId(prefix,existing){let i=1;while(existing.has(`${prefix}${i}`))i++;return `${prefix}${i}`;}
function neighbors(s,x,y){return [[1,0],[-1,0],[0,1],[0,-1]].map(([dx,dy])=>[x+dx,y+dy]).filter(([nx,ny])=>inside(nx,ny,s.n));}
function allRoutes(s,active){const dist=new Map([[xy(active.x,active.y),0]]),prev=new Map(),queue=[[active.x,active.y]],blocked=new Set([...s.walls,...s.units.filter(u=>u.id!==active.id).map(u=>xy(u.x,u.y))]);for(let i=0;i<queue.length;i++){const [x,y]=queue[i],d=dist.get(xy(x,y));for(const [nx,ny] of neighbors(s,x,y)){const k=xy(nx,ny);if(blocked.has(k)||dist.has(k))continue;dist.set(k,d+1);prev.set(k,xy(x,y));queue.push([nx,ny]);}}return {dist,prev};}
function routeTo(routes,from,to){const dest=xy(to.x,to.y),start=xy(from.x,from.y);if(!routes.dist.has(dest))return null;const path=[];let p=dest;while(p!==start){const [x,y]=p.split(',').map(Number);path.unshift({x,y});p=routes.prev.get(p);if(!p)return null;}return path;}
function dangerWarning(s,path){return path.filter(p=>s.danger.includes(xy(p.x,p.y))).length;}
function aooWarning(s,u,path){let prev={x:u.x,y:u.y},count=0;for(const p of path){if(s.units.some(v=>v.team!==u.team&&v.team!=='neutral'&&Math.abs(v.x-prev.x)+Math.abs(v.y-prev.y)===1))count++;prev=p;}return count;}
function clickCell(x,y){if(gesture.suppress)return;const s=scene(),key=xy(x,y),at=s.units.find(u=>u.x===x&&u.y===y),u=selected();lastCell={x,y};
 if(s.mode==='pan')return;
 if(s.mode==='play'){
   if(at){s.selected=at.id;invalidateFov();render();saveLocal();return note('Selecionado: '+at.name);}
   if(!u||u.team!=='ally')return note('Selecione um aliado TEST para mover.');
   const routes=allRoutes(s,u),path=routeTo(routes,u,{x,y});if(!path||!path.length)return note('Casa bloqueada ou inalcançável.');if(path.length>4-s.stepsUsed)return note('Movimento TEST: passos restantes '+(4-s.stepsUsed)+'.');
   const warn=aooWarning(s,u,path),danger=dangerWarning(s,path);snap();if(!s.frames.length)captureFrame(s,"Início da movimentação TEST");u.x=x;u.y=y;s.stepsUsed+=path.length;commit(s,`${u.name} moveu ${path.length} casa(s).${warn?' Alerta de oportunidade não resolvido.':''}${danger?' Terreno perigoso não resolvido.':''}`,true);note('Movimento visual TEST executado; sem dano ou resultado oficial.');return;
 }
 if(s.mode==='place'){
   if(!u)return note('Selecione o token a posicionar.');if(at&&at.id!==u.id)return note('Casa ocupada.');if(s.walls.includes(key))return note('Parede bloqueia token.');if(u.x===x&&u.y===y)return;
   snap();if(!s.frames.length)captureFrame(s,"Início do posicionamento TEST");u.x=x;u.y=y;s.stepsUsed=0;commit(s,`Token ${u.name} reposicionado na cena TEST.`,true);return;
 }
 if(at)return note('Não edite terreno sob unidades.');
 const old=JSON.stringify({walls:s.walls,danger:s.danger,terrain:s.terrain});
 snap();
 if(s.mode==='wall'){
   const had=s.walls.includes(key);
   s.walls=s.walls.filter(z=>z!==key);
   if(!had){s.walls.push(key);s.danger=s.danger.filter(z=>z!==key);delete s.terrain[key];}
 }else if(s.mode==='danger'){
   const had=s.danger.includes(key);
   s.danger=s.danger.filter(z=>z!==key);
   if(!had){s.danger.push(key);s.walls=s.walls.filter(z=>z!==key);delete s.terrain[key];}
 }else if(s.mode==='terrain'){
   const steps=[undefined,'grass','sand','water'],cur=s.terrain[key],next=steps[(steps.indexOf(cur)+1)%steps.length];
   if(next)s.terrain[key]=next;else delete s.terrain[key];s.danger=s.danger.filter(z=>z!==key);s.walls=s.walls.filter(z=>z!==key);
 }else if(s.mode==='erase'){
   s.walls=s.walls.filter(z=>z!==key);s.danger=s.danger.filter(z=>z!==key);delete s.terrain[key];
 }
 if(old===JSON.stringify({walls:s.walls,danger:s.danger,terrain:s.terrain})){history.pop();return;}
 if(s.mode==='wall'){s.frames=[];s.frameTopology=null;}
 commit(s,'Terreno TEST editado em '+(x+1)+','+(y+1)+'.');
}
// Edição por toque, com snapshots isolados e sem efeitos em motores oficiais.
function changeMode(mode){const s=scene();if(!['play','pan','wall','danger','terrain','erase','place'].includes(mode))return;s.mode=mode;gesture.suppress=false;render();}
function resize(n){const s=scene();if(!allowedSize.includes(n)||n===s.n)return; if(s.units.some(u=>u.x>=n||u.y>=n)){return note('Não é possível reduzir: existem unidades fora da nova grade.');}snap();s.n=n;s.walls=s.walls.filter(key=>key.split(',').every(v=>Number(v)<n));s.danger=s.danger.filter(key=>key.split(',').every(v=>Number(v)<n));for(const key of Object.keys(s.terrain))if(key.split(',').some(v=>Number(v)>=n))delete s.terrain[key];s.frames=[];s.frameTopology=null;s.explored=s.explored.filter(key=>key.split(',').every(v=>Number(v)<n));invalidateFov();commit(s,'Grade alterada para '+n+'×'+n+'.');if(s.fovEnabled&&selected())centerAt(selected().x,selected().y);else center();}
const board=$('board'),vp=$('viewport');let cachedN=0,tiles=[];
function ensureBoard(n){if(cachedN===n)return;cachedN=n;tiles=[];const frag=document.createDocumentFragment();for(let y=0;y<n;y++)for(let x=0;x<n;x++){const b=document.createElement('button');b.type='button';b.className='tile';b.dataset.xy=xy(x,y);b.setAttribute('role','gridcell');b.innerHTML='<span class="coord"></span><span class="token" hidden></span>';frag.append(b);tiles.push(b);}board.replaceChildren(frag);board.style.setProperty('--n',n);}
// TEST18 VISUAL FOV: author-written symmetric shadowcasting implementation for synthetic maps.
// This is neither a canonical light/perception rule nor a client-side security filter.
let fovCacheKey='',fovCache=null;
function invalidateFov(){fovCacheKey='';fovCache=null;}
function symmetricShadowcast(s,origin,radius){
 const walls=new Set(s.walls),visible=new Set([xy(origin.x,origin.y)]),rad2=radius*radius;
 const blocked=(x,y)=>!inside(x,y,s.n)||walls.has(xy(x,y));
 // Four quadrants, depths progressing outwards, slope bounds -1 .. 1.
 const orient=[(d,c)=>[origin.x+c,origin.y-d],(d,c)=>[origin.x+c,origin.y+d],(d,c)=>[origin.x+d,origin.y+c],(d,c)=>[origin.x-d,origin.y+c]];
 const roundUp=v=>Math.floor(v+0.5),roundDown=v=>Math.ceil(v-0.5);
 for(const project of orient){
  const scan=(depth,start,end)=>{
   if(depth>radius||start>end)return;
   let prevWall=null,low=start;
   for(let col=roundUp(depth*start);col<=roundDown(depth*end);col++){
    const [x,y]=project(depth,col),wall=blocked(x,y);
    if(inside(x,y,s.n)&&((col>=depth*start&&col<=depth*end)||wall)&&((x-origin.x)**2+(y-origin.y)**2<=rad2))visible.add(xy(x,y));
    const boundary=(2*col-1)/(2*depth);
    if(prevWall===true&&!wall)low=boundary;
    if(prevWall===false&&wall)scan(depth+1,low,boundary);
    prevWall=wall;
   }
   if(prevWall===false)scan(depth+1,low,end);
  };
  scan(1,-1,1);
 }
 return visible;
}
function currentFov(s){
 if(!s.fovEnabled)return null;
 const u=selected();if(!u)return null;
 const key=JSON.stringify([s.id,s.n,u.id,u.x,u.y,s.fovRadius,[...s.walls].sort()]);
 if(key!==fovCacheKey){fovCacheKey=key;fovCache=symmetricShadowcast(s,u,s.fovRadius);}
 const old=new Set(s.explored);for(const k of fovCache)old.add(k);
 if(old.size!==s.explored.length)s.explored=[...old].sort();
 return fovCache;
}
function reachable(s){const u=selected();if(!u||u.team!=='ally'||s.mode!=='play')return new Set();const r=allRoutes(s,u),remaining=4-s.stepsUsed;return new Set([...r.dist].filter(([k,d])=>d>0&&d<=remaining).map(([k])=>k));}
function renderBoard(s){
 ensureBoard(s.n);
 const occupied=new Map(s.units.map(u=>[xy(u.x,u.y),u]));
 const walls=new Set(s.walls),danger=new Set(s.danger);
 const reach=$('layerReach').checked?reachable(s):new Set();
 const showCoords=$('layerCoords').checked,showDanger=$('layerDanger').checked,fov=currentFov(s),explored=fov?new Set(s.explored):null;if($('fovStatus'))$('fovStatus').textContent=fov?`${fov.size} visíveis · ${s.explored.length} exploradas`:'FOV desligado';
 for(let i=0;i<tiles.length;i++){
  const b=tiles[i],x=i%s.n,y=Math.floor(i/s.n),key=xy(x,y),u=occupied.get(key);
  let cls='tile'+((x+y)%2?' alt':'');
  if(s.terrain[key])cls+=' ground-'+s.terrain[key];
  if(walls.has(key))cls+=' wall';
  if(danger.has(key)&&showDanger)cls+=' danger';
  if(reach.has(key))cls+=' reachable';
  if(u?.id===s.selected)cls+=' chosen';if(fov&&!fov.has(key))cls+=explored.has(key)?' fov-explored':' fov-hidden';
  // TEST07: atualiza somente casas cujo conteúdo visual realmente mudou.
  const sig=cls+'|'+showCoords+'|'+(u?u.id+':'+u.mark+':'+u.team+':'+u.name:'');
  if(b.dataset.sig===sig)continue;
  b.dataset.sig=sig;b.className=cls;
  b.setAttribute('aria-label',`Coluna ${x+1}, linha ${y+1}${u?', '+u.name:''}${walls.has(key)?', parede':''}`);
  const coord=b.firstElementChild;coord.hidden=!showCoords;
  if(showCoords)coord.textContent=`${x+1}.${y+1}`;
  const p=b.lastElementChild;p.hidden=!u;
  if(u){p.className='token '+u.team;p.textContent=u.mark;p.title=u.name;}
 }
}
function renderUnits(s){const root=$('unitList');root.replaceChildren();for(const u of s.units){const b=document.createElement('button');b.type='button';b.className='unitBtn'+(u.id===s.selected?' sel':'');const bubble=document.createElement('span');bubble.className='bubble '+u.team;bubble.textContent=u.mark;const label=document.createElement('span'),strong=document.createElement('strong'),small=document.createElement('small');strong.textContent=u.name;small.textContent=`${u.team==='ally'?'Aliado':u.team==='enemy'?'Adversário':'Neutro'} • ${u.x+1},${u.y+1} • Vida ${u.hp} • Alma ${u.soul} • PA ${u.pa}`;label.append(strong,small);b.append(bubble,label);b.addEventListener('click',()=>{s.selected=u.id;invalidateFov();render();saveLocal();note('Selecionado '+u.name);});root.append(b);}}
function renderSceneSelector(){const root=$('scenes'),s=scene();root.replaceChildren();for(const sc of workspace.scenes){const opt=document.createElement('option');opt.value=sc.id;opt.textContent=sc.name;root.append(opt);}root.value=s.id;}
function renderLog(s){const root=$('log');root.replaceChildren();for(const msg of s.logs.slice(0,12)){const p=document.createElement('p');p.textContent=msg;root.append(p);}}
function render(){const t0=performance.now(),s=scene();renderSceneSelector();$('gridSize').value=String(s.n);$('sceneHeading').textContent=s.name;$('sceneMeta').textContent=' · '+s.n+'×'+s.n;$('unitCount').textContent=s.units.length+' unidades';$('roundCount').textContent='Rodada TEST '+s.round;$('activeSceneCount').textContent=workspace.scenes.length+' cena(s)';$('sceneNotes').value=s.notes;$('layerFov').checked=s.fovEnabled;$('fovRadius').value=String(s.fovRadius);renderBoard(s);renderUnits(s);renderLog(s);for(const b of document.querySelectorAll('[data-mode]')){const active=b.dataset.mode===s.mode;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));}drawMinimap();renderReplay();renderLast=performance.now()-t0;$('perf').textContent=`Render ${renderLast.toFixed(1)} ms (medição local)`;}
function cameraScale(next,anchor){const prior=zoom,after=Math.min(84,Math.max(28,Math.round(Number(next)/4)*4));if(!Number.isFinite(after))return;const x=anchor?.x??vp.clientWidth/2,y=anchor?.y??vp.clientHeight/2;const worldX=(vp.scrollLeft+x)/prior,worldY=(vp.scrollTop+y)/prior;zoom=after;document.documentElement.style.setProperty('--cell',after+'px');$('zoom').value=String(after);$('zoomLabel').textContent=after+' px';vp.scrollLeft=worldX*after-x;vp.scrollTop=worldY*after-y;drawMinimap();}
function center(){vp.scrollLeft=Math.max(0,(board.scrollWidth-vp.clientWidth)/2);vp.scrollTop=Math.max(0,(board.scrollHeight-vp.clientHeight)/2);drawMinimap();}
function centerAt(x,y){const s=scene();vp.scrollLeft=Math.max(0,(x+.5)*(zoom+2)-vp.clientWidth/2);vp.scrollTop=Math.max(0,(y+.5)*(zoom+2)-vp.clientHeight/2);drawMinimap();}
function drawMinimap(){const s=scene(),canvas=$('minimap'),ctx=canvas.getContext('2d'),W=canvas.width,step=W/s.n,walls=new Set(s.walls),danger=new Set(s.danger);ctx.clearRect(0,0,W,W);for(let y=0;y<s.n;y++)for(let x=0;x<s.n;x++){const key=xy(x,y);ctx.fillStyle=walls.has(key)?'#8b94a1':danger.has(key)?'#aa634d':s.terrain[key]==='grass'?'#327963':s.terrain[key]==='water'?'#316a9b':s.terrain[key]==='sand'?'#9c8254':'#324e69';ctx.fillRect(x*step,y*step,step-.5,step-.5);}for(const u of s.units){ctx.beginPath();ctx.arc((u.x+.5)*step,(u.y+.5)*step,Math.max(2.5,step*.3),0,Math.PI*2);ctx.fillStyle=u.id===s.selected?'#fbe08a':u.team==='enemy'?'#d7757a':'#67bdf1';ctx.fill();}const rect=vp.getBoundingClientRect(),br=board.getBoundingClientRect();if(br.width&&br.height){const x=Math.max(0,(rect.left-br.left)/br.width*W),y=Math.max(0,(rect.top-br.top)/br.height*W);ctx.strokeStyle='#ffffb5';ctx.lineWidth=2;ctx.strokeRect(x,y,Math.min(W-x,rect.width/br.width*W),Math.min(W-y,rect.height/br.height*W));}}
function cameraGesture(){const points=gesture.pointers,xyList=[...points.values()];if(xyList.length!==2)return null;const a=xyList[0],b=xyList[1];return {mid:{x:(a.x+b.x)/2,y:(a.y+b.y)/2},distance:Math.max(1,Math.hypot(a.x-b.x,a.y-b.y))};}
vp.addEventListener('pointerdown',e=>{if(e.pointerType==='mouse'&&e.button!==0)return;if(gesture.pointers.size===0)gesture.suppress=false;gesture.pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});gesture.dragged=false;const g=cameraGesture();if(g){const r=vp.getBoundingClientRect();gesture.start={zoom,distance:g.distance,worldX:(vp.scrollLeft+g.mid.x-r.left)/zoom,worldY:(vp.scrollTop+g.mid.y-r.top)/zoom};gesture.suppress=true;}if(scene().mode==='pan'||gesture.pointers.size>1)try{vp.setPointerCapture(e.pointerId);}catch{}});
vp.addEventListener('pointermove',e=>{const previous=gesture.pointers.get(e.pointerId);if(!previous)return;gesture.pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});const g=cameraGesture();if(g&&gesture.start){const rect=vp.getBoundingClientRect();cameraScale(gesture.start.zoom*g.distance/gesture.start.distance,{x:g.mid.x-rect.left,y:g.mid.y-rect.top});vp.scrollLeft=gesture.start.worldX*zoom-(g.mid.x-rect.left);vp.scrollTop=gesture.start.worldY*zoom-(g.mid.y-rect.top);gesture.suppress=true;gesture.dragged=true;drawMinimap();e.preventDefault();}else if(scene().mode==='pan'&&gesture.pointers.size===1){const dx=e.clientX-previous.x,dy=e.clientY-previous.y;if(dx||dy){vp.scrollLeft-=dx;vp.scrollTop-=dy;gesture.suppress=true;gesture.dragged=true;drawMinimap();e.preventDefault();}}});
function endPointer(e){if(!gesture.pointers.has(e.pointerId))return;gesture.pointers.delete(e.pointerId);if(gesture.pointers.size<2)gesture.start=null;if(gesture.pointers.size===0&&gesture.dragged){gesture.suppress=true;}else if(gesture.pointers.size===0&&scene().mode!=='pan'){gesture.suppress=false;}}
for(const type of ['pointerup','pointercancel','lostpointercapture'])vp.addEventListener(type,endPointer);
vp.addEventListener('click',e=>{if(gesture.suppress||scene().mode==='pan'){e.preventDefault();e.stopPropagation();gesture.suppress=false;}},true);
board.addEventListener('click',e=>{const b=e.target.closest('[data-xy]');if(!b)return;const [x,y]=b.dataset.xy.split(',').map(Number);clickCell(x,y);});
$('minimap').addEventListener('click',e=>{const r=e.currentTarget.getBoundingClientRect(),s=scene(),x=Math.min(s.n-1,Math.max(0,Math.floor((e.clientX-r.left)/r.width*s.n))),y=Math.min(s.n-1,Math.max(0,Math.floor((e.clientY-r.top)/r.height*s.n)));centerAt(x,y);});vp.addEventListener('scroll',drawMinimap,{passive:true});
function editToken(create=false){const s=scene(),u=selected();if(!create&&!u)return note('Selecione uma unidade para editar.');if(create&&s.units.length>=MAX_UNITS)return note('Limite de 30 unidades por cena.');editingNew=create;editingId=create?null:u.id;const t=create?unit('','Token TEST','T','neutral',0,0):u;$('tokName').value=t.name;$('tokMark').value=t.mark;$('tokTeam').value=t.team;$('tokHp').value=t.hp;$('tokSoul').value=t.soul;$('tokPa').value=t.pa;$('tokRange').value=t.range;$('tokenForm').classList.remove('hidden');}
function commitToken(){const s=scene(),name=$('tokName').value.trim(),mark=$('tokMark').value.trim(),team=$('tokTeam').value,range=Number($('tokRange').value),values=[$('tokHp'),$('tokSoul'),$('tokPa')].map(el=>Number(el.value));if(!textOK(name,48)||!textOK(mark,2)||!['ally','enemy','neutral'].includes(team)||!Number.isInteger(range)||range<1||range>20||values.some(v=>!Number.isInteger(v)||v<0||v>99999))return note('Dados TEST inválidos. Confira nome, marca e valores.');if(editingNew){const occupied=new Set(s.units.map(u=>xy(u.x,u.y))),walls=new Set(s.walls);let pos=null;for(let y=0;y<s.n&&!pos;y++)for(let x=0;x<s.n;x++)if(!occupied.has(xy(x,y))&&!walls.has(xy(x,y))){pos={x,y};break;}if(!pos)return note('Mapa sem casa livre para token.');snap();const id=nextId('u',new Set(s.units.map(u=>u.id)));s.units.push({...unit(id,name,mark,team,pos.x,pos.y),range,hp:values[0],soul:values[1],pa:values[2]});s.selected=id;s.frames=[];s.frameTopology=null;commit(s,'Novo token TEST criado: '+name);}else{const u=selected();if(!u||u.id!==editingId)return note('Seleção alterada; reabra o editor.');snap();Object.assign(u,{name,mark,team,range,hp:values[0],soul:values[1],pa:values[2]});commit(s,'Token TEST editado: '+name);}closeTokenForm();}
function closeTokenForm(){$('tokenForm').classList.add('hidden');editingNew=false;editingId=null;}
function removeToken(){const s=scene(),u=selected();if(!u)return; if(!confirm(`Remover ${u.name} desta cena TEST?`))return;snap();s.units=s.units.filter(x=>x.id!==u.id);s.selected=s.units[0]?.id||null;s.frames=[];s.frameTopology=null;commit(s,'Token TEST removido: '+u.name);}
function createScene(){if(workspace.scenes.length>=MAX_SCENES)return note('Limite de oito cenas.');snap();const id=nextId('c',new Set(workspace.scenes.map(s=>s.id)));const sc=newScene(id,'Nova cena TEST '+id);workspace.scenes.push(sc);workspace.active=id;history=[];future=[];clearReplay();render();saveLocal();note('Cena independente criada.');}
function copyScene(){if(workspace.scenes.length>=MAX_SCENES)return note('Limite de oito cenas.');const id=nextId('c',new Set(workspace.scenes.map(s=>s.id))),sc=clone(scene());sc.id=id;sc.name=(sc.name.slice(0,52)+' (cópia)');snap();workspace.scenes.push(sc);workspace.active=id;clearReplay();render();saveLocal();note('Cena duplicada sem modificar a original.');}
function deleteScene(){if(workspace.scenes.length<=1)return note('Mantenha ao menos uma cena TEST.');const s=scene();if(!confirm(`Excluir a cena TEST “${s.name}”?`))return;snap();workspace.scenes=workspace.scenes.filter(x=>x.id!==s.id);workspace.active=workspace.scenes[0].id;clearReplay();render();saveLocal();note('Cena experimental excluída.');}
function switchScene(id){if(!workspace.scenes.some(s=>s.id===id))return;workspace.active=id;invalidateFov();clearReplay();history=[];future=[];closeTokenForm();render();saveLocal();center();}
function renameScene(){const s=scene(),name=prompt('Nome da cena TEST (máximo 70 caracteres):',s.name);if(name===null)return;const value=name.trim();if(!textOK(value,70))return note('Nome TEST inválido.');snap();s.name=value;commit(s,'Cena renomeada.');}
function resetScene(){const s=scene();if(!confirm(`Limpar o mapa, tokens e histórico de “${s.name}” nesta cena TEST?`))return;snap();const restored=newScene(s.id,s.name,s.n);restored.notes=s.notes;workspace.scenes=workspace.scenes.map(x=>x.id===s.id?restored:x);history=[];future=[];clearReplay();render();saveLocal();note('Cena reiniciada.');}
function nextRound(){const s=scene();snap();s.round++;s.stepsUsed=0;s.acted=false;commit(s,'Nova rodada TEST; não executa iniciativa oficial.');}
function addEventFrame(){const s=scene();snap();captureFrame(s,'Quadro TEST '+(s.frames.length+1));commit(s,'Quadro de replay TEST capturado.');loadCurrentReplay();}
function makeReplay(s){const frames=s.frames.length?s.frames:[{title:'Posições atuais TEST',positions:positions(s)}];return {schema:REPLAYSCHEMA,source:{kind:'SYNTHETIC_FIXTURE',scope:'MESTRE_ONLY',isolatedCopy:true,reference:'TABLETOP-PUBLIC-TEST18',exportedAt:stamp()},grid:{width:s.n,height:s.n,walls:s.walls.map(v=>v.split(',').map(Number))},units:s.units.map(u=>({id:u.id,label:u.name,mark:u.mark,team:u.team})),events:frames.map((f,i)=>({id:'frame-'+String(i+1).padStart(3,'0'),type:i?'POSITION':'ROUND_NOTE',title:f.title,description:'Snapshot visual sintético; sem cálculo do RPG.',frame:{positions:f.positions}}))};}
function validateReplay(d){if(!safeKeys(d)||d.schema!==REPLAYSCHEMA||!safeKeys(d.source)||d.source.kind!=='SYNTHETIC_FIXTURE'||d.source.scope!=='MESTRE_ONLY'||d.source.isolatedCopy!==true||!textOK(d.source.reference,100)||!textOK(d.source.exportedAt,40)||!safeKeys(d.grid)||!allowedSize.includes(d.grid.width)||d.grid.width!==d.grid.height||!Array.isArray(d.grid.walls)||d.grid.walls.length>200||!Array.isArray(d.units)||d.units.length<1||d.units.length>MAX_UNITS||!Array.isArray(d.events)||d.events.length<1||d.events.length>MAX_EVENTS)return false;
 const walls=new Set();for(const w of d.grid.walls){if(!Array.isArray(w)||w.length!==2||!inside(w[0],w[1],d.grid.width)||walls.has(xy(...w)))return false;walls.add(xy(...w));}
 const ids=new Set();for(const u of d.units){if(!safeKeys(u)||!validId(u.id)||ids.has(u.id)||!textOK(u.label,70)||!textOK(u.mark,2)||!['ally','enemy','neutral'].includes(u.team))return false;ids.add(u.id);}const eventIds=new Set();let previousNumeric=null,previousPrefix=null,hadSequence=null,prevSequence=null;
 const numericIds=d.events.every(e=>typeof e.id==='string'&&/^(frame|ev)-\d+$/.test(e.id));
 for(const e of d.events){
  if(Object.hasOwn(e,'sequence')){if(!Number.isSafeInteger(e.sequence)||e.sequence<0||hadSequence===false||(prevSequence!==null&&e.sequence<=prevSequence))return false;prevSequence=e.sequence;hadSequence=true;}
  else if(hadSequence===true)return false;else hadSequence=false;
  if(numericIds){const m=/^(frame|ev)-(\d+)$/.exec(e.id);const num=Number(m[2]);if(!Number.isSafeInteger(num)||num<0||(previousPrefix!==null&&m[1]!==previousPrefix)||(previousNumeric!==null&&num<=previousNumeric))return false;previousNumeric=num;previousPrefix=m[1];}
if(!safeKeys(e)||!textOK(e.id,55)||eventIds.has(e.id)||!['POSITION','ATTACK_DECLARED','AO0_ALERT','DAMAGE_RECORDED','ROUND_NOTE','EFFECT_DECLARED'].includes(e.type)||!textOK(e.title,120)||!textOK(e.description,500)||!safeKeys(e.frame)||!safeKeys(e.frame.positions))return false;eventIds.add(e.id);if(Object.keys(e.frame.positions).length!==ids.size)return false;const occupied=new Set();for(const id of ids){const p=e.frame.positions[id];if(!Array.isArray(p)||p.length!==2||!inside(p[0],p[1],d.grid.width)||walls.has(xy(...p))||occupied.has(xy(...p)))return false;occupied.add(xy(...p));}if(Object.keys(e.frame.positions).some(k=>!ids.has(k)||!validId(k)))return false;}return true;}
function stopReplay(){if(playTimer!==null){clearInterval(playTimer);playTimer=null;}$('replayPlay').textContent='▶ Reproduzir';}
function clearReplay(){stopReplay();viewReplay=null;frameIndex=0;drawnTopology='';}
let drawnTopology='';
function loadCurrentReplay(){const d=makeReplay(scene());if(!validateReplay(d))return note('Não foi possível gerar replay TEST: snapshots incompatíveis.');loadReplay(d);}
function loadReplay(d){if(!validateReplay(d))throw Error('Replay inválido ou não sintético; dados VLAB reais permanecem HOLD.');stopReplay();viewReplay=clone(d);frameIndex=0;drawnTopology='';renderReplay();}
function renderReplay(){const d=viewReplay,root=$('replayGrid'),overlay=$('replayPieces'),list=$('eventList');if(!d){$('replayCounter').textContent='0/0';$('replayInfo').textContent='Capture um quadro ou importe replay sintético.';root.replaceChildren();overlay.replaceChildren();list.replaceChildren();return;}
 const n=d.grid.width,event=d.events[frameIndex],prev=frameIndex?d.events[frameIndex-1]:null,size=n===20?20:28,gap=2;const signature=n+':'+d.grid.walls.map(w=>w.join(',')).join('|');if(signature!==drawnTopology){drawnTopology=signature;root.replaceChildren();overlay.replaceChildren();root.style.setProperty('--n',n);root.style.setProperty('--t',size+'px');overlay.style.setProperty('--t',size+'px');const walls=new Set(d.grid.walls.map(w=>xy(...w)));for(let y=0;y<n;y++)for(let x=0;x<n;x++){const tile=document.createElement('div');tile.className='replayCell'+(walls.has(xy(x,y))?' wall':'');root.append(tile);}for(const u of d.units){const piece=document.createElement('div');piece.className='replayPiece '+u.team;piece.dataset.id=u.id;piece.style.width=size+'px';piece.style.height=size+'px';const inner=document.createElement('span');inner.textContent=u.mark;piece.append(inner);overlay.append(piece);}}
 for(const piece of overlay.children){const p=event.frame.positions[piece.dataset.id];piece.style.transform=`translate(${p[0]*(size+gap)}px,${p[1]*(size+gap)}px)`;}
 let delta='Quadro inicial.';if(prev){const changes=d.units.filter(u=>!equal(prev.frame.positions[u.id],event.frame.positions[u.id])).map(u=>`${u.label}: ${prev.frame.positions[u.id].join(',')} → ${event.frame.positions[u.id].join(',')}`);delta=changes.join('\n')||'Nenhuma posição mudou.';}
 $('replayCounter').textContent=`${frameIndex+1}/${d.events.length}`;$('replayInfo').textContent=event.title+'\n'+event.description+'\n'+delta;$('replaySeek').max=d.events.length-1;$('replaySeek').value=frameIndex;list.replaceChildren();for(let i=0;i<d.events.length;i++){const b=document.createElement('button');b.type='button';b.className=i===frameIndex?'current':'';b.textContent=`${i+1}. ${d.events[i].title}`;b.onclick=()=>seek(i);list.append(b);}}
function seek(i){if(!viewReplay)return;frameIndex=Math.max(0,Math.min(viewReplay.events.length-1,i));renderReplay();}
function togglePlayback(){if(playTimer!==null){stopReplay();return;}if(!viewReplay)return note('Capture ou importe replay TEST primeiro.');if(frameIndex>=viewReplay.events.length-1)seek(0);$('replayPlay').textContent='⏸ Pausar';playTimer=setInterval(()=>{if(!viewReplay||frameIndex>=viewReplay.events.length-1){stopReplay();return;}seek(frameIndex+1);},Number($('replaySpeed').value));}
function exportReplay(){if(!viewReplay)loadCurrentReplay();if(viewReplay)download(viewReplay,'TABLETOP_TEST15_REPLAY_SINTETICO.json');}
function initialize(){loadLocal();document.documentElement.style.setProperty('--cell',zoom+'px');render();center();}
// CONTROLES DE CENA, EDITOR, TOKEN, PERSISTÊNCIA.
$('scenes').onchange=e=>switchScene(e.target.value);$('newScene').onclick=createScene;$('copyScene').onclick=copyScene;$('deleteScene').onclick=deleteScene;$('renameScene').onclick=renameScene;$('resetScene').onclick=resetScene;$('gridSize').onchange=e=>resize(Number(e.target.value));$('nextRound').onclick=nextRound;
for(const b of document.querySelectorAll('[data-mode]'))b.onclick=()=>changeMode(b.dataset.mode);$('undo').onclick=undo;$('redo').onclick=redo;$('zoomOut').onclick=()=>cameraScale(zoom-4);$('zoomIn').onclick=()=>cameraScale(zoom+4);$('zoom').oninput=e=>cameraScale(Number(e.target.value));$('center').onclick=center;$('focus').onclick=()=>{const u=selected();if(u)centerAt(u.x,u.y);};
for(const id of ['layerCoords','layerReach','layerDanger'])$(id).onchange=()=>{renderBoard(scene());drawMinimap();};$('layerFov').onchange=e=>{scene().fovEnabled=e.target.checked;invalidateFov();render();saveLocal();if(e.target.checked){const u=selected();if(u)centerAt(u.x,u.y);}note(e.target.checked?'Campo de visão EXPERIMENTAL: não aplica regras oficiais.':'FOV visual desligado.');};$('fovRadius').onchange=e=>{scene().fovRadius=Number(e.target.value);invalidateFov();render();saveLocal();};$('newToken').onclick=()=>editToken(true);$('editToken').onclick=()=>editToken(false);$('removeToken').onclick=removeToken;$('commitToken').onclick=commitToken;$('cancelToken').onclick=closeTokenForm;
$('sceneNotes').addEventListener('change',e=>{const s=scene();const value=e.target.value;if(value.length>800)return note('Nota muito longa.');snap();s.notes=value;saveLocal();});
$('save').onclick=()=>saveLocal(false);$('backup').onclick=()=>{if(validateWorkspace(workspace))download(workspace,'TABLETOP_ASSIMILACAO_BACKUP_TEST15.json');};
$('restore').onchange=async e=>{const f=e.target.files?.[0];if(!f)return;try{const w=await readJSON(f);if(!validateWorkspace(migrateWorkspace(clone(w))))throw Error('Schema, topologia, cena ou conteúdo inválido');if(!confirm('Substituir suas cenas locais pelas cenas deste backup TEST?'))return;restoreCandidate(w);note('Backup sintético restaurado e persistência local conferida.');}catch(err){note('Backup rejeitado: '+err.message);}finally{e.target.value='';}};
$('record').onclick=addEventFrame;$('replayExport').onclick=exportReplay;$('replayPlay').onclick=togglePlayback;$('replaySpeed').onchange=()=>{if(playTimer!==null){stopReplay();togglePlayback();}};$('replayPrev').onclick=()=>{stopReplay();seek(frameIndex-1);};$('replayNext').onclick=()=>{stopReplay();seek(frameIndex+1);};$('replayFirst').onclick=()=>{stopReplay();seek(0);};$('replaySeek').oninput=e=>{stopReplay();seek(Number(e.target.value));};
$('replayImport').onchange=async e=>{const f=e.target.files?.[0];if(!f)return;try{const v=await readJSON(f);loadReplay(v);note('Replay TEST importado; nenhuma cena foi modificada.');}catch(err){note('Replay rejeitado: '+err.message);}finally{e.target.value='';}};
// API ESTRITAMENTE TEST para ensaios externos; nenhuma escrita remota.
window.__tabletopTEST={state:()=>clone(workspace),scene:()=>clone(scene()),validateWorkspace,validateReplay,restoreCandidate,shadowcast:({x,y,radius})=>[...symmetricShadowcast(scene(),{x,y},radius)].sort(),fovNow:()=>currentFov(scene())?[...currentFov(scene())].sort():null,mode:changeMode,cell:clickCell,undo,redo,save:saveLocal,createScene,copyScene,switchScene,resize,addToken:()=>editToken(true),capture:addEventFrame,replay:()=>viewReplay?clone(viewReplay):null,seek,makeReplay:()=>makeReplay(scene()),zoom:v=>cameraScale(v),lastRenderMs:()=>renderLast,render,center};
initialize();
})();
