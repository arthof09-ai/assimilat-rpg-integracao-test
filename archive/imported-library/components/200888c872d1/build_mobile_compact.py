from pathlib import Path
import zipfile,hashlib,json,re,io
base=Path('/mnt/data/video_lote_20261024');source=base/'test36_ref/TABLETOP_SITE_SINTETICO_TEST36_CANDIDATE.zip'
output=base/'TEST36_MOBILE_ARENA_VISIVEL_TEST'
output.mkdir(exist_ok=True)
with zipfile.ZipFile(source) as z:
 for n in z.namelist():
  (output/n).write_bytes(z.read(n))
p=output/'index.html';s=p.read_text()
assert '<section class="workspace">' in s
s=s.replace('<link rel="stylesheet" href="styles.css">','<link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="arena-primeiro.css">')
s=s.replace('<section class="workspace">','''<section class="workspace">
<div class="arena-primeiro-botoes" role="group" aria-label="Controles compactos para Android">
<button class="btn primary" id="arenaFocusToggle" type="button" aria-expanded="false" aria-controls="arenaTools">⚙ Ferramentas</button>
<button class="btn" id="arenaUnitsJump" type="button">◉ Unidades</button>
<span class="arena-primeiro-indicador">Modo Arena • TEST</span>
</div>''')
s=s.replace('<div class="card toolbar">','<div class="card toolbar" id="arenaTools">',1)
s=s.replace('<script src="room-client.js" defer></script>','<script src="room-client.js" defer></script><script src="arena-primeiro.js" defer></script>')
p.write_text(s)
css='''/* PROVA TEST de ergonomia; NÃO altera regras, tokens, roteamento ou estados oficiais. */
.arena-primeiro-botoes{display:none}
@media(max-width:700px){
  body.arena-primeiro .shell{padding:7px 7px 24px}
  body.arena-primeiro .header{padding:3px 4px 5px;gap:4px}
  body.arena-primeiro .header .eyebrow,body.arena-primeiro .header .sub{display:none}
  body.arena-primeiro .header h1{font-size:21px;margin:0}
  body.arena-primeiro .header .tag{font-size:9px;padding:4px 8px}
  .arena-primeiro-botoes{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:5px 0 8px}
  .arena-primeiro-botoes .btn{min-height:40px;padding:5px 9px}
  .arena-primeiro-indicador{font-size:11px;color:#f8d98a}
  body.arena-primeiro:not(.arena-tools-open) .workspace .card.toolbar,
  body.arena-primeiro:not(.arena-tools-open) .workspace .battle-map-primary .toolbar2,
  body.arena-primeiro:not(.arena-tools-open) .workspace .battle-map-primary .layers,
  body.arena-primeiro:not(.arena-tools-open) .workspace .battle-map-primary .mini,
  body.arena-primeiro:not(.arena-tools-open) .workspace .battle-map-primary > .flex.split > .flex{display:none}
  body.arena-primeiro:not(.arena-tools-open) .battle-map-primary{padding:8px;margin-bottom:8px}
  body.arena-primeiro:not(.arena-tools-open) .battle-map-primary > .flex.split{margin-bottom:5px}
  body.arena-primeiro:not(.arena-tools-open) .battle-map-primary .arenaWrap{grid-template-columns:minmax(0,1fr)}
  body.arena-primeiro:not(.arena-tools-open) .battle-map-primary .viewport{height:min(64dvh,570px);min-height:370px;max-height:none}
  body.arena-primeiro:not(.arena-tools-open) .battle-map-primary .message{margin-top:6px}
}
'''
(output/'arena-primeiro.css').write_text(css)
js='''/* Aditivo TEST; apenas apresentação. NUNCA simula ataque/PA/turno ou altera storage. */
(()=>{'use strict';
 const btn=document.getElementById('arenaFocusToggle');const units=document.getElementById('arenaUnitsJump');
 const viewport=document.getElementById('viewport');const map=viewport?.closest('.card');
 if(!btn||!units||!map)return;
 map.classList.add('battle-map-primary');
 document.body.classList.add('arena-primeiro');
 btn.setAttribute('aria-expanded','false');
 btn.addEventListener('click',()=>{
  const open=document.body.classList.toggle('arena-tools-open');
  btn.textContent=open?'🗺 Priorizar Arena':'⚙ Ferramentas';
  btn.setAttribute('aria-expanded',String(open));
  if(!open)map.scrollIntoView({block:'nearest',behavior:'auto'});
 });
 units.addEventListener('click',()=>document.getElementById('unitList')?.scrollIntoView({block:'start',behavior:'auto'}));
})();
'''
(output/'arena-primeiro.js').write_text(js)
# Do not alter scripts/styles original (only HTML insertion and two additive files).
with zipfile.ZipFile(source) as z:
 for n in ['styles.css','app.js','room-client.js','room-v2-adapter.js']:
  assert z.read(n)==(output/n).read_bytes(), n
# zip candidate
out_zip=base/'TEST36_PROVA_MOBILE_ARENA_VISIVEL_20261024.zip'
with zipfile.ZipFile(out_zip,'w',zipfile.ZIP_DEFLATED) as zz:
 for file in sorted(output.iterdir()):
  info=zipfile.ZipInfo(file.name,(2026,10,24,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
  zz.writestr(info,file.read_bytes())
print('ZIP',out_zip,out_zip.stat().st_size,hashlib.sha256(out_zip.read_bytes()).hexdigest())
