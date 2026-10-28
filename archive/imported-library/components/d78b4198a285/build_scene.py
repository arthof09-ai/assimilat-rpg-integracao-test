from pathlib import Path
import re,base64,hashlib,json
src=Path('/mnt/data/video_lote_20261024/TABLETOP_TEST36_ARENA_PRIMEIRO_OFFLINE_TEST_20261024.html')
out=Path('/mnt/data/playlist_20261024/ARENA_TEST36_CAMADAS_AMBIENTAIS_OFFLINE.html')
s=src.read_text()
assert 'id="viewport"' in s and 'connect-src \'none\'' in s
style=r'''/* Extensão independente: apresentação ambiental TEST, sem ações mecânicas */
#scene-test-panel{border:1px solid #4c825c;background:linear-gradient(120deg,#183a36,#14273c);border-radius:12px;padding:12px;margin:8px 0 12px;color:#f0f7ed}
#scene-test-panel .head{display:flex;justify-content:space-between;gap:8px;align-items:center;flex-wrap:wrap}
#scene-test-panel .scene-buttons{display:flex;gap:6px;flex-wrap:wrap;margin:8px 0}
#scene-test-panel button{background:#244453;color:#fff;border:1px solid #5f8d80;border-radius:8px;padding:9px 12px;font-weight:650}
#scene-test-panel button[aria-pressed="true"]{background:#c9a766;color:#142a32}
#scene-test-panel p{margin:6px 0;color:#c9ddd5;font-size:12px}
#viewport{position:relative;isolation:isolate}
#viewport::after{content:"";position:absolute;inset:0;pointer-events:none;z-index:9;opacity:0;transition:opacity .3s;background:transparent}
#viewport.scene-rain::after{opacity:.6;background:repeating-linear-gradient(105deg,transparent 0 8px,rgba(133,211,255,.2) 8px 9px,transparent 9px 18px);animation:rainfallTest 1s linear infinite}
#viewport.scene-night::after{opacity:1;background:linear-gradient(115deg,rgba(5,20,49,.7),rgba(16,25,65,.54));}
#viewport.scene-night .tile{filter:brightness(.77) saturate(.92)}
#viewport.scene-rain .tile.ground-grass{filter:saturate(1.17) brightness(.85)}
#viewport.scene-day .tile.ground-grass{background-image:radial-gradient(circle at 16% 15%,#347e5a 0 2px,transparent 3px),radial-gradient(circle at 64% 56%,#499963 0 2px,transparent 3px)}
#viewport.scene-day .tile.ground-water{background-image:repeating-linear-gradient(-20deg,transparent 0 8px,rgba(148,239,247,.23) 8px 11px,transparent 11px 20px)}
@keyframes rainfallTest{from{background-position:0 0}to{background-position:-22px 38px}}
@media (max-width:600px){#scene-test-panel{padding:9px}#scene-test-panel button{min-height:38px;padding:7px 9px}}
@media (prefers-reduced-motion: reduce){#viewport.scene-rain::after{animation:none}}
'''
script=r'''(()=>{'use strict';
const panel=document.getElementById('scene-test-panel'),viewport=document.getElementById('viewport');
if(!panel||!viewport)return;
const modes=Object.freeze(['day','rain','night']);
const state={schema_version:'assim.tabletop.scene.presentation.test.v1',mode:'day',source:'MESTRE_ONLY_SYNTHETIC_PRESENTATION',mechanics:'NO_RULES_NO_RESOURCE_WRITES',network:'DISABLED'};
const info=panel.querySelector('#scene-test-info');
function setMode(mode){if(!modes.includes(mode))return false;for(const m of modes)viewport.classList.remove('scene-'+m);viewport.classList.add('scene-'+mode);state.mode=mode;panel.querySelectorAll('[data-scene]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.scene===mode)));info.textContent=({day:'Dia: iluminação ilustrativa',rain:'Chuva: animação ilustrativa, sem efeitos nas regras',night:'Noite: filtro visual, sem modificar FOV ou permissões'})[mode];const output=panel.querySelector('#scene-export-output');if(!output.hidden){const old=JSON.parse(output.value||'{}');output.value=JSON.stringify({...old,...state},null,2);}return true;}
panel.querySelectorAll('[data-scene]').forEach(btn=>btn.addEventListener('click',()=>setMode(btn.dataset.scene)));
panel.querySelector('#scene-export').addEventListener('click',()=>{
const dto={...state,cell_count:document.querySelectorAll('#board .tile').length,sent_to_server:false,apply_mechanics:false};
const dest=panel.querySelector('#scene-export-output');dest.value=JSON.stringify(dto,null,2);dest.hidden=false;
});
setMode('day');
})();'''
markup='''<section id="scene-test-panel" aria-label="Apresentação ambiental TEST" role="group"><div class="head"><strong>🌿 Ambiente da Arena — TEST visual</strong><small>NÃO altera movimento, FOV, PA, dano ou regras</small></div><div class="scene-buttons"><button type="button" data-scene="day">☀️ Dia</button><button type="button" data-scene="rain">🌧️ Chuva</button><button type="button" data-scene="night">🌙 Noite</button><button type="button" id="scene-export">Ver contrato JSON</button></div><p id="scene-test-info" aria-live="polite"></p><textarea id="scene-export-output" hidden readonly rows="6" style="width:100%;font:11px monospace;background:#0b1720;color:#d3eddc"></textarea></section>'''
s=s.replace('<div id="viewport"',markup+'<div id="viewport"') if '<div id="viewport"' in s else s.replace('<div class="viewport" id="viewport"',markup+'<div class="viewport" id="viewport"')
assert 'id="scene-test-panel"' in s
s=s.replace('</head>',f'<style>{style}</style></head>',1)
s=s.replace('</body>',f'<script>{script}</script></body>',1)
def sha(x):return base64.b64encode(hashlib.sha256(x.encode()).digest()).decode()
# Add hash to original CSP directives, retaining every old hash.
s=s.replace("style-src ","style-src 'sha256-"+sha(style)+"' ",1)
s=s.replace("script-src ","script-src 'sha256-"+sha(script)+"' ",1)
out.write_text(s)
Path('/mnt/data/playlist_20261024/SCENE_PRESENTATION_TEST.contract.json').write_text(json.dumps({'schema_version':'assim.tabletop.scene.presentation.test.v1','mode':['day','rain','night'],'contract':'VIEW_LAYER_ONLY','source':'SYNTHETIC','mechanical_effect':'NONE','server_action':'NONE','permissions':'PRESENTATION_ONLY','requires_official_VLAB_for_mechanics':True,'preserve_grid':True},indent=2))
print('created',out.stat().st_size,'orig',src.stat().st_size)
