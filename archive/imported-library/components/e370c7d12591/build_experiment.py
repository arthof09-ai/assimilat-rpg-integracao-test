import base64, hashlib, json
from pathlib import Path
from PIL import Image, ImageDraw
out=Path('/mnt/data/relatorio_496132_20261024');out.mkdir(exist_ok=True,parents=True)
# Original TEST-only pixel-art. 4 rows of direction x 4 animation frames; 48px cells.
CW=48;CH=48;cols=4;rows=4
im=Image.new('RGBA',(CW*cols,CH*rows),(0,0,0,0))
colors={'coat':'#516854','shade':'#2d4444','skin':'#d1a277','hair':'#453b3b','pants':'#414c65','boot':'#302c35','pack':'#765744','glow':'#9bd7bf'}
for ry in range(rows):
 for fx in range(cols):
  tile=Image.new('RGBA',(CW,CH),(0,0,0,0));d=ImageDraw.Draw(tile);bounce=[0,1,0,-1][fx];step=[0,2,0,-2][fx]
  cx=24; y=6+bounce
  # boots and legs, anchored no larger than 1px drift
  d.ellipse((15,42,34,46),fill=(17,35,40,120))
  d.rectangle((18+step,y+29,23+step,y+39),fill=colors['pants']); d.rectangle((26-step,y+29,31-step,y+39),fill=colors['pants'])
  d.rectangle((17+step,y+38,24+step,y+42),fill=colors['boot']);d.rectangle((25-step,y+38,33-step,y+42),fill=colors['boot'])
  # pack behind side view
  if ry in (1,2):
   rx=31 if ry==1 else 13; d.rounded_rectangle((rx,y+13,rx+8,y+27),2,fill=colors['pack'])
  d.rounded_rectangle((17,y+13,31,y+31),3,fill=colors['shade']);d.rectangle((20,y+15,29,y+27),fill=colors['coat'])
  d.rectangle((15,y+18,19,y+28),fill=colors['skin']);d.rectangle((31,y+18,35,y+28),fill=colors['skin'])
  d.rounded_rectangle((17,y+1,32,y+16),4,fill=colors['skin'])
  d.rounded_rectangle((16,y,33,y+7),2,fill=colors['hair'])
  if ry==0:
   d.rectangle((20,y+9,22,y+10),fill=colors['shade']);d.rectangle((28,y+9,30,y+10),fill=colors['shade'])
  elif ry==3:
   d.rectangle((18,y+9,31,y+12),fill=colors['hair'])
  elif ry==1:
   d.rectangle((19,y+9,21,y+11),fill=colors['shade'])
  else:
   d.rectangle((29,y+9,31,y+11),fill=colors['shade'])
  # belt/clasp fixed anchor
  d.rectangle((19,y+26,30,y+28),fill=colors['pack']);d.point((25,y+27),fill=colors['glow'])
  im.alpha_composite(tile,(fx*CW,ry*CH))
asset=out/'PERSONAGEM_TEST_SPRITESHEET_4x4.png';im.save(asset)
assetsha=hashlib.sha256(asset.read_bytes()).hexdigest()
manifest={'contract':'ASSIMILACAO_VISUAL_SPRITESHEET_TEST.v1','status':'TEST_SYNTHETIC_NON_CANONICAL', 'name':'Viajante TEST (arte autoral sintética)', 'asset':asset.name,'asset_sha256':assetsha,'sheet_width':im.width,'sheet_height':im.height,'columns':4,'rows':4,'cell_width':48,'cell_height':48,'directions':['down','left','right','up'],'frames_per_direction':4,'fps':6,'origin':'bottom-center','copyright':'Original TEST illustration generated in this task','mechanics':'NONE'}
(out/'CONTRATO_SPRITESHEET_TEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf8')
b64=base64.b64encode(asset.read_bytes()).decode()
html=r'''<!doctype html>
<html lang="pt-BR"><head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"/>
<title>Oficina de Sprites | Assimilação TEST</title>
<style>
:root{color-scheme:dark;--bg:#0e1722;--card:#172635;--bord:#314759;--muted:#a4b9c6;--fg:#eff7f9;--accent:#7dd8ba}
*{box-sizing:border-box}body{margin:0;background:linear-gradient(160deg,#0a1520,#142637 65%,#0b161e);font-family:system-ui,-apple-system,sans-serif;color:var(--fg);padding:18px;min-height:100dvh}header{max-width:960px;margin:auto;padding:9px 0 16px}small,.sub,.hint{color:var(--muted)}.flag{font-size:11px;font-weight:800;letter-spacing:.14em;color:#9ae8d6}h1{font-size:clamp(25px,5vw,38px);margin:7px 0 5px}h2{font-size:16px;margin:0 0 14px}p{margin:8px 0 0;line-height:1.5}.grid{display:grid;grid-template-columns: minmax(0,1fr) minmax(0,1fr);max-width:960px;margin:auto;gap:14px}.card{border:1px solid var(--bord);background:var(--card);border-radius:16px;padding:16px;min-width:0}.preview{display:grid;place-items:center;min-height:270px;background:repeating-conic-gradient(#284354 0% 25%,#213646 0% 50%) 50% / 30px 30px;border-radius:14px;border:1px solid #3b5366}canvas{image-rendering:pixelated;max-width:100%}#stage{width:192px;height:192px;object-fit:contain}#sheet{width:100%;height:auto;max-height:250px;object-fit:contain;background:linear-gradient(45deg,#263746 25%,transparent 25%),linear-gradient(-45deg,#263746 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#263746 75%),linear-gradient(-45deg,transparent 75%,#263746 75%);background-size:20px 20px;background-position:0 0,0 10px,10px -10px,-10px 0}label{display:block;font-size:12px;color:var(--muted);margin-bottom:7px}.controls{display:grid;grid-template-columns:1fr 1fr;gap:12px}.field{min-width:0}input,select,button{font:inherit;max-width:100%;border-radius:9px}input[type=number],select,input[type=file]{width:100%;background:#101f2d;color:white;border:1px solid #385167;padding:10px}button{border:1px solid #4d7684;color:white;background:#244358;padding:11px 13px;cursor:pointer;font-weight:650}button.primary{background:#1d6c65;border-color:#70bcab}.actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}.log{white-space:pre-wrap;font:12px/1.55 ui-monospace,Consolas,monospace;background:#0a1926;padding:12px;border:1px solid #334a58;border-radius:10px;margin-top:12px;min-height:100px;color:#d7eeef}.span{grid-column:1/-1}footer{max-width:960px;margin:18px auto;font-size:12px;color:var(--muted)}.ok{color:#8de7c4}.warn{color:#ffce85}
@media(max-width:680px){body{padding:12px}.grid{grid-template-columns:1fr}.card{padding:14px}.preview{min-height:210px}#stage{width:160px;height:160px}}
</style></head><body>
<header><div class="flag">RPG ASSIMILAÇÃO / LABORATÓRIO TEST / NÃO CANÔNICO</div><h1>Oficina de Sprites</h1><p class="sub">Importe uma folha PNG, confira grade e transparência, anime por direção e exporte o contrato de apresentação. Tudo offline; nada é enviado.</p></header>
<main class="grid"><section class="card"><h2>Prévia animada</h2><div class="preview"><canvas id="stage" width="48" height="48"></canvas></div><div class="actions"><button id="pause">Pausar animação</button><button id="reset">Voltar ao exemplo</button></div><p class="hint" id="current">Exemplo sintético original. Não é NPC canônico.</p></section>
<section class="card"><h2>Carregar e configurar</h2><div class="field"><label for="upload">Sprite sheet PNG local (sem upload)</label><input id="upload" type="file" accept="image/png,image/webp"/></div><div class="controls" style="margin-top:14px"><div class="field"><label for="cols">Colunas</label><input id="cols" type="number" min="1" max="64" value="4"/></div><div class="field"><label for="rows">Linhas</label><input id="rows" type="number" min="1" max="64" value="4"/></div><div class="field"><label for="dir">Direção / linha</label><select id="dir"><option value="0">Frente (linha 1)</option><option value="1">Esquerda (linha 2)</option><option value="2">Direita (linha 3)</option><option value="3">Costas (linha 4)</option></select></div><div class="field"><label for="fps">Quadros por segundo</label><input id="fps" type="number" min="1" max="30" value="6"/></div></div><div class="actions"><button class="primary" id="audit">Auditar sprites</button><button id="export">Exportar contrato JSON</button></div><div class="log" id="status" role="status" aria-live="polite"></div></section>
<section class="card span"><h2>Folha de sprites</h2><canvas id="sheet" width="192" height="192"></canvas><p class="hint">Critérios: divisibilidade da grade, canal alfa, células vazias, dimensões, alinhamento aproximado dos pés. Aceite artístico e integração na Arena continuam decisões separadas.</p></section></main>
<footer>Test-only. Nenhuma regra de Vida, Alma, PA, dano, iniciativa ou VLAB foi executada. A animação não altera a posição de uma unidade.</footer>
<script>
const DEFAULT_IMAGE='data:image/png;base64,___BASE64___';
const $=id=>document.getElementById(id), stage=$('stage'), sheet=$('sheet'),ctx=stage.getContext('2d'),sx=sheet.getContext('2d');ctx.imageSmoothingEnabled=false;sx.imageSmoothingEnabled=false;
let image=new Image(),name='PERSONAGEM_TEST_SPRITESHEET_4x4.png',lastAudit=null,frame=0,playing=true,lastT=0,valid=false;
function cfg(){return {cols:Number($('cols').value),rows:Number($('rows').value),dir:Number($('dir').value),fps:Number($('fps').value)}}
function guard(){let {cols,rows,dir,fps}=cfg();return Number.isInteger(cols)&&Number.isInteger(rows)&&cols>0&&rows>0&&cols<=64&&rows<=64&&Number.isInteger(dir)&&dir>=0&&dir<rows&&Number.isFinite(fps)&&fps>=1&&fps<=30&&image.naturalWidth>0&&image.naturalHeight>0}
function drawSheet(){if(!image.complete||!image.naturalWidth)return;sheet.width=image.naturalWidth;sheet.height=image.naturalHeight;sx.imageSmoothingEnabled=false;sx.clearRect(0,0,sheet.width,sheet.height);sx.drawImage(image,0,0);let {cols,rows}=cfg();if(!(cols>0&&rows>0))return;sx.strokeStyle='rgba(126,216,186,.6)';sx.lineWidth=1;for(let x=0;x<=cols;x++){let p=x*sheet.width/cols;sx.beginPath();sx.moveTo(p,0);sx.lineTo(p,sheet.height);sx.stroke()}for(let y=0;y<=rows;y++){let p=y*sheet.height/rows;sx.beginPath();sx.moveTo(0,p);sx.lineTo(sheet.width,p);sx.stroke()}}
function render(t){requestAnimationFrame(render);if(!guard())return;let c=cfg();if(playing&&t-lastT>=1000/c.fps){frame=(frame+1)%c.cols;lastT=t;}let w=image.naturalWidth/c.cols,h=image.naturalHeight/c.rows;stage.width=Math.max(1,Math.round(w));stage.height=Math.max(1,Math.round(h));ctx.imageSmoothingEnabled=false;ctx.clearRect(0,0,stage.width,stage.height);ctx.drawImage(image,frame*w,c.dir*h,w,h,0,0,stage.width,stage.height)}
function audit(){let lines=[],c=cfg();if(!guard()){valid=false;$('status').textContent='ERRO: configuração inválida, imagem ainda indisponível ou direção fora da grade.';return false;}let w=image.naturalWidth,h=image.naturalHeight;
lines.push('Fonte: '+name+' | '+w+'×'+h+' px');
if(w%c.cols||h%c.rows){valid=false;lines.push('ERRO: tamanho não divisível pelo número de linhas/colunas.');$('status').textContent=lines.join('\n');return false;}
let cellW=w/c.cols,cellH=h/c.rows,tmp=document.createElement('canvas');tmp.width=w;tmp.height=h;let tc=tmp.getContext('2d',{willReadFrequently:true});tc.drawImage(image,0,0);
let data=tc.getImageData(0,0,w,h).data;let empty=[],opaque=0,pixels=0,feet=[];
for(let row=0;row<c.rows;row++){let arr=[];for(let col=0;col<c.cols;col++){let minX=cellW,minY=cellH,maxX=-1,maxY=-1,count=0;for(let yy=0;yy<cellH;yy++)for(let xx=0;xx<cellW;xx++){let a=data[((row*cellH+yy)*w+(col*cellW+xx))*4+3];pixels++;if(a===255)opaque++;if(a>16){count++;minX=Math.min(minX,xx);minY=Math.min(minY,yy);maxX=Math.max(maxX,xx);maxY=Math.max(maxY,yy)}}if(!count)empty.push((row+1)+'/'+(col+1));else arr.push(maxY);}feet.push(arr)}
let transparent=pixels-opaque; lines.push('Célula: '+cellW+'×'+cellH+' px, '+(c.cols*c.rows)+' quadros.');lines.push(transparent>0?'PASS: canal alfa presente (ao menos pixels translúcidos).':'ALERTA: não há transparência visível.');lines.push(empty.length?'ALERTA: células vazias: '+empty.join(', '):'PASS: nenhuma célula vazia.');let maxDrift=Math.max(0,...feet.map(a=>a.length?Math.max(...a)-Math.min(...a):0));lines.push(maxDrift>3?'ALERTA: variação de base da sprite dentro da mesma direção = '+maxDrift+'px.':'PASS: variação aproximada de base <=3px ('+maxDrift+'px).');valid=!empty.length&&transparent>0;lines.push(valid?'STATUS: ESTRUTURA TEST ADEQUADA (não certifica qualidade artística).':'STATUS: REVISÃO RECOMENDADA.');$('status').textContent=lines.join('\n');$('current').textContent=name+' · '+cellW+'×'+cellH+' px · '+c.cols+' frames por direção';lastAudit={structure_valid:valid,cell_width:cellW,cell_height:cellH,max_foot_drift:maxDrift,empty_cells:empty,transparent_pixel_count:transparent};return valid}
function exported(){audit();if(!lastAudit)return;let c=cfg();let ob={schema:'ASSIMILACAO_SPRITE_PRESENTATION_TEST.v1',status:'TEST_ONLY_NOT_CANONICAL',source_file:name,dimensions:{width:image.naturalWidth,height:image.naturalHeight,columns:c.cols,rows:c.rows,frame_width:lastAudit.cell_width,frame_height:lastAudit.cell_height},animation:{fps:c.fps,directions:['down','left','right','up'].slice(0,c.rows),frames_per_row:c.cols},origin:'bottom-center',audit:lastAudit,mechanics:'NONE',authorization:'REQUIRED_FOR_CANONICAL_INTEGRATION'};let blob=new Blob([JSON.stringify(ob,null,2)],{type:'application/json'});let a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='ASSIMILACAO_SPRITES_TEST.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),5000)}
$('audit').onclick=audit;$('export').onclick=exported;$('pause').onclick=()=>{playing=!playing;$('pause').textContent=playing?'Pausar animação':'Reproduzir animação'};
for(let id of ['cols','rows','dir','fps'])$(id).addEventListener('change',()=>{frame=0;drawSheet();audit()});
$('reset').onclick=()=>{name='PERSONAGEM_TEST_SPRITESHEET_4x4.png';$('cols').value=4;$('rows').value=4;$('dir').value=0;$('fps').value=6;image.src=DEFAULT_IMAGE};
$('upload').onchange=ev=>{let file=ev.target.files?.[0];if(!file)return;if(file.size>12_000_000){$('status').textContent='ERRO: imagem >12MB; escolha arquivo menor.';return;}let url=URL.createObjectURL(file),ni=new Image();ni.onload=()=>{if(ni.naturalWidth>4096||ni.naturalHeight>4096){$('status').textContent='ERRO: imagem excede 4096px por eixo.';URL.revokeObjectURL(url);return}image=ni;name=file.name;frame=0;drawSheet();audit();URL.revokeObjectURL(url)};ni.onerror=()=>{$('status').textContent='ERRO: imagem não decodificável';URL.revokeObjectURL(url)};ni.src=url};
image.onload=()=>{frame=0;drawSheet();audit()};image.src=DEFAULT_IMAGE;requestAnimationFrame(render);
</script></body></html>'''.replace('___BASE64___',b64)
(out/'OFICINA_SPRITES_ASSIMILACAO_TEST_ANDROID_OFFLINE.html').write_text(html,encoding='utf8')
print('ASSET SHA',assetsha,'HTML',len(html),'ASSET BYTES',asset.stat().st_size)
