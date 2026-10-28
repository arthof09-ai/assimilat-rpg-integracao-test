from pathlib import Path
import hashlib,base64,re,json
root=Path('/mnt/data/lote04_20261024/experimento');src=Path('/mnt/data/RELATORIOS_11_VIDEOS_ASSIMILACAO_20261023/prova_test36/TABLETOP_TEST36_PREVIA_ACAO_NAO_ENVIA.html');dst=root/'ARENA_TEST36_PREVIA_GEOMETRIA_VISUAL_OFFLINE.html'
s=src.read_text()
assert 'aria-label="Preparar ação de combate TEST"' in s and 'connect-src \'none\'' in s
html='''<div class="visual-preview" id="geometricPreview"><h3>◈ Geometria de área — SOMENTE VISUAL</h3><p class="note-test">Mostra casas ilustrativas, sem distância, alcance, linha de visão, alvo legal ou qualquer regra oficial do Assimilação. Sem envio de comando.</p><label>Forma de visualização <select id="previewShape" aria-label="Geometria visual"><option value="POINT">Ponto</option><option value="LINE">Linha ilustrativa</option><option value="CONE">Cone ilustrativo</option><option value="CIRCLE">Área ilustrativa</option></select></label><div class="actions"><button type="button" id="previewPaint">Visualizar na Arena</button><button type="button" id="previewClear">Limpar área</button></div><p id="previewGeometryStatus" role="status">Selecione duas unidades e uma forma. Não envia comandos.</p></div>'''
s=s.replace('<div class="actions"><button type="button" id="previewBuild"',html+'<div class="actions"><button type="button" id="previewBuild"',1)
style=r'''
.visual-preview{margin:10px 0;padding:12px;border:1px solid #4e7193;border-radius:12px;background:#0d2038}.visual-preview h3{margin:0 0 6px;color:#e9cd8a;font-size:15px}.visual-preview label{display:block;margin:8px 0}.visual-preview select{width:100%;max-width:100%;min-height:38px;background:#183451;color:#fff;border:1px solid #6389a9;border-radius:6px}.visual-preview .actions{display:flex;gap:8px;flex-wrap:wrap}.visual-preview button{background:#294e67;color:#fff;border:1px solid #8ab3bc;border-radius:7px;padding:9px}.tile.preview-area-visual{outline:3px solid #eec678;outline-offset:-4px;background-image:linear-gradient(0deg,#ecbb5e42,#ecbb5e42)!important}.tile.preview-actor-visual{outline:3px solid #72efbf;outline-offset:-4px}.tile.preview-target-visual{box-shadow:inset 0 0 0 3px #ff7586}
'''
script=r'''/* LAB MESTRE TEST: prévia de geometria artística, nunca legalidade mecânica. */
(()=>{'use strict';
const $=id=>document.getElementById(id),board=$('board'),actor=$('previewActor'),target=$('previewTarget'),shape=$('previewShape');
const status=$('previewGeometryStatus'); const classes=['preview-area-visual','preview-actor-visual','preview-target-visual'];
function clear(){for(const tile of board.querySelectorAll('.tile')) for(const c of classes)tile.classList.remove(c);}
function getUnits(){const arr=[];for(const btn of document.querySelectorAll('#unitList .unitBtn')){
 const name=btn.querySelector('strong')?.textContent?.trim();const tx=btn.querySelector('small')?.textContent||'';
 const m=tx.match(/(?:^|[•\s])(\d+)\s*,\s*(\d+)\b/);
 if(name&&m) arr.push({name,x:Number(m[1])-1,y:Number(m[2])-1});
}return arr;}
function render(){clear();const a=getUnits().find(x=>x.name===actor.value),t=getUnits().find(x=>x.name===target.value);if(!a||!t||a.name===t.name){status.textContent='Selecione uma unidade e um alvo distintos. Nenhuma ação enviada.';return;}
 const tileMap=new Map([...board.querySelectorAll('.tile')].map(x=>[x.dataset.xy,x]));
 if(tileMap.size===0){status.textContent='Arena vazia; nada enviado.';return;}
 const size=Math.round(Math.sqrt(tileMap.size)),mode=shape.value;
 const vx=t.x-a.x,vy=t.y-a.y,len=Math.hypot(vx,vy)||1;
 const ux=vx/len,uy=vy/len;let count=0;
 for(let y=0;y<size;y++)for(let x=0;x<size;x++){
  const dx=x-a.x,dy=y-a.y,dist=Math.hypot(dx,dy);const forward=dx*ux+dy*uy;
  let matches=false;
  if(mode==='POINT')matches=(x===t.x&&y===t.y);
  else if(mode==='LINE')matches=dist<=3.1&&forward>=0&&Math.abs(dx*uy-dy*ux)<=.40;
  else if(mode==='CONE')matches=dist<=3.1&&dist>0&&forward>=0&&Math.abs(dx*uy-dy*ux)<=forward*.85;
  else if(mode==='CIRCLE')matches=Math.hypot(x-t.x,y-t.y)<=2.05;
  const tile=tileMap.get(x+','+y); if(matches&&tile){tile.classList.add('preview-area-visual');count++;}
 }
 tileMap.get(a.x+','+a.y)?.classList.add('preview-actor-visual');tileMap.get(t.x+','+t.y)?.classList.add('preview-target-visual');
 status.textContent='GEOMETRIA ILUSTRATIVA TEST — '+count+' casa(s) realçada(s) na grade. SEM validação de alcance/PA/VLAB, sem envio ou modificação de estado.';
}
$('previewPaint').addEventListener('click',render);$('previewClear').addEventListener('click',()=>{clear();status.textContent='Área removida; nenhum comando enviado.';});
for(const el of [actor,target,shape])el.addEventListener('change',()=>{if(!document.querySelector('.tile.preview-area-visual'))return;render();});
$('previewClose').addEventListener('click',clear);
})();'''
# Append inline style and script immediately before close body
s=s.replace('</body>',f'<style>{style}</style>\n<script>{script}</script>\n</body>',1)
csshash=base64.b64encode(hashlib.sha256(style.encode()).digest()).decode();jshash=base64.b64encode(hashlib.sha256(script.encode()).digest()).decode();
# Insert hashes into existing CSP
s=s.replace("; img-src data:",f" 'sha256-{csshash}'; img-src data:",1)
s=s.replace("; style-src ",f" 'sha256-{jshash}'; style-src ",1)
assert f"'sha256-{csshash}'" in s and f"'sha256-{jshash}'" in s
assert s.count('connect-src \'none\'')==1
assert s.count('actionPreviewToggle')>=2 and s.count('previewPaint')>=2
dst.write_text(s,encoding='utf8')
(root/'geometria_aceite.json').write_text(json.dumps({'classification':'EXPERIMENTO_TEST_VISUAL_SEM_MECANICA','geometry_shapes':['POINT','LINE','CONE','CIRCLE'],'no_game_rules':True,'source_html_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'output_html_sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'server_not_contacted':True,'mechanics_hold':['dano','pa','alcance','linha_de_visao','alvo_legal','iniciativa'],'acceptance':['49 tiles preserved','actions preview controls survive','no mutations of HP/soul/PA','no network','3 Android-like viewports smoke']},ensure_ascii=False,indent=2))
print(dst, dst.stat().st_size)
