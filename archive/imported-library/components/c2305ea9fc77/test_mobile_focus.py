import zipfile,re,asyncio,json,hashlib
from pathlib import Path
from playwright.async_api import async_playwright
base=Path('/mnt/data/video_lote_20261024')
source=base/'test36_ref/TABLETOP_SITE_SINTETICO_TEST36_CANDIDATE.zip'
modified=base/'TEST36_PROVA_MOBILE_ARENA_VISIVEL_20261024.zip'
async def load(page,z):
 html=z.read('index.html').decode();css=z.read('styles.css').decode();
 if 'arena-primeiro.css' in z.namelist(): css+='\n'+z.read('arena-primeiro.css').decode()
 html=re.sub(r'<meta http-equiv="Content-Security-Policy"[^>]*>','',html)
 html=html.replace('<link rel="stylesheet" href="styles.css">','<style>'+css+'</style>')
 html=html.replace('<link rel="stylesheet" href="arena-primeiro.css">','')
 html=re.sub(r'<script\b[^>]*\bsrc=["\'][^"\']+["\'][^>]*>\s*</script>','',html)
 await page.set_content(html,wait_until='load')
 for s in ['app.js','room-v2-adapter.js','room-client.js','arena-primeiro.js']:
  if s in z.namelist(): await page.add_script_tag(content=z.read(s).decode())
 await page.wait_for_timeout(500)
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  results={}
  for label,path in [('original',source),('compact',modified)]:
   page=await browser.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
   errors=[];page.on('pageerror',lambda e: errors.append(str(e)))
   with zipfile.ZipFile(path) as z:await load(page,z)
   pos=await page.locator('#viewport').bounding_box()
   board_count=await page.locator('#board .tile').count()
   await page.screenshot(path=str(base/f'test36_mobile_{label}_390x844.png'))
   info={'viewport_y':round(pos['y'],1) if pos else None,'viewport_h':round(pos['height'],1) if pos else None, 'above_fold':pos is not None and pos['y']<844,'board_cells':board_count,'errors':errors[:2]}
   if label=='compact':
    toggle=page.locator('#arenaFocusToggle')
    info['tools_closed_on_open']=not await page.locator('.toolbar').is_visible()
    await toggle.click()
    info['tools_visible_after_click']=await page.locator('.toolbar').is_visible()
    await toggle.click()
    info['tools_closed_again']=not await page.locator('.toolbar').is_visible()
    info['original_app_name']=await page.title()
   results[label]=info
   await page.close()
  await browser.close()
 print(json.dumps(results,indent=2,ensure_ascii=False))
 assert results['compact']['above_fold'] and not results['original']['above_fold']
 assert results['compact']['tools_closed_on_open'] and results['compact']['tools_visible_after_click'] and results['compact']['tools_closed_again']
 assert results['original']['board_cells']==results['compact']['board_cells']
 (base/'TESTE_ANDROID_390x844_RESULTADOS.json').write_text(json.dumps(results,indent=2,ensure_ascii=False))
asyncio.run(main())
