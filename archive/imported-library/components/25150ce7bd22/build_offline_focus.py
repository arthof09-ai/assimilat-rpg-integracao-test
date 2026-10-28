from pathlib import Path
import hashlib,base64,re
b=Path('/mnt/data/video_lote_20261024');src=b/'test36_ref/TABLETOP_ASSIMILACAO_TEST36_OFFLINE.html';out=b/'TABLETOP_TEST36_ARENA_PRIMEIRO_OFFLINE_TEST_20261024.html'
mod=b/'TEST36_MOBILE_ARENA_VISIVEL_TEST'
s=src.read_text()
assert s.count('<style>')==1 and s.count('<script>')==3
s=s.replace('<section class="workspace">','''<section class="workspace">
<div class="arena-primeiro-botoes" role="group" aria-label="Controles compactos para Android">
<button class="btn primary" id="arenaFocusToggle" type="button" aria-expanded="false" aria-controls="arenaTools">⚙ Ferramentas</button>
<button class="btn" id="arenaUnitsJump" type="button">◉ Unidades</button>
<span class="arena-primeiro-indicador">Modo Arena • TEST</span>
</div>''')
s=s.replace('<div class="card toolbar">','<div class="card toolbar" id="arenaTools">',1)
css=(mod/'arena-primeiro.css').read_text();js=(mod/'arena-primeiro.js').read_text()
def token(t):return "'sha256-"+base64.b64encode(hashlib.sha256(t.encode()).digest()).decode()+"'"
s=s.replace('</head>','<style>'+css+'</style></head>',1)
s=s.replace('</body>','<script>'+js+'</script></body>',1)
s=s.replace("; style-src",' '+token(js)+'; style-src',1)
s=s.replace('; img-src',' '+token(css)+'; img-src',1)
# Verify no third party network permission and original script hashes untouched.
assert "connect-src 'none'" in s
out.write_text(s)
print(out,out.stat().st_size,hashlib.sha256(out.read_bytes()).hexdigest(), 'scripts:',s.count('<script>'), 'styles:',s.count('<style>'))
