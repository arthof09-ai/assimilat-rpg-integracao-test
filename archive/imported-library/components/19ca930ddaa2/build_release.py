from pathlib import Path
import hashlib,base64,re,zipfile,json,shutil,os
ROOT=Path('/mnt/data/tabletop_run008');PUBLIC=ROOT/'public';DIST=ROOT/'dist';DIST.mkdir(exist_ok=True)
index=(PUBLIC/'index.html').read_text();js=(PUBLIC/'app.js').read_text();css=(PUBLIC/'styles.css').read_text()
def sri(text):return 'sha256-'+base64.b64encode(hashlib.sha256(text.encode()).digest()).decode()
index_public=index.replace('TEST 25 · DEMONSTRAÇÃO SINTÉTICA','TEST 26 · DEMONSTRAÇÃO SINTÉTICA')
(PUBLIC/'index.html').write_text(index_public)
# Independent no-network standalone CSP using only the exact inline code hashes.
standalone=index_public.replace('<link rel="stylesheet" href="styles.css">','<style>'+css+'</style>').replace('<script src="app.js" defer></script>','<script>'+js+'</script>')
standalone=standalone.replace("default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'",f"default-src 'none'; script-src '{sri(js)}'; style-src '{sri(css)}'; img-src 'self' data:; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'")
(DIST/'TABLETOP_ASSIMILACAO_TEST26_OFFLINE.html').write_text(standalone)
# public site = exact 3 files; the index must not contain inline private content.
pub=Path('/mnt/data/TABLETOP_SITE_SINTETICO_TEST26.zip')
with zipfile.ZipFile(pub,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for name in ['index.html','styles.css','app.js']:z.write(PUBLIC/name,name)
shutil.copy2(DIST/'TABLETOP_ASSIMILACAO_TEST26_OFFLINE.html','/mnt/data/TABLETOP_ASSIMILACAO_TEST26_OFFLINE.html')
print('built static',pub.stat().st_size,'offline',len(standalone))
