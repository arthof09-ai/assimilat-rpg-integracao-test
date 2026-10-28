from playwright.sync_api import sync_playwright
import json, pathlib
html=pathlib.Path('/mnt/data/lote04_20261024/experimento/ARENA_TEST36_PREVIA_GEOMETRIA_VISUAL_OFFLINE.html').read_text()
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for w,h in [(360,740),(390,844),(412,915)]:
  page=browser.new_page(viewport={'width':w,'height':h});errs=[];net=[]
  page.on('pageerror',lambda e:errs.append(str(e)))
  page.on('request',lambda q:net.append(q.url))
  page.set_content(html,wait_until='domcontentloaded');page.wait_for_timeout(180)
  count=page.locator('#board .tile').count();assert count==49,(w,count)
  page.locator('#actionPreviewToggle').click()
  assert page.locator('#actionPreviewDrawer').is_visible()
  assert page.locator('#previewActor option').count()>=2
  units_before=page.locator('#unitList .unitBtn strong').all_text_contents()
  assert units_before
  for mode in ['POINT','LINE','CONE','CIRCLE']:
   page.locator('#previewShape').select_option(mode)
   page.locator('#previewPaint').click()
   highlighted=page.locator('.tile.preview-area-visual').count();assert highlighted>=1,(w,mode,highlighted,page.locator('#previewGeometryStatus').inner_text())
   results.append(dict(viewport=f'{w}x{h}',shape=mode,highlighted=highlighted,status='PASS'))
  text=page.locator('#previewGeometryStatus').inner_text();assert 'SEM validação' in text
  page.locator('#previewClear').click();assert page.locator('.tile.preview-area-visual').count()==0
  page.locator('#previewBuild').click();payload=page.locator('#previewJSON').inner_text();assert 'PREVIEW_ONLY_NOT_DISPATCHABLE' in payload and 'NOT_SENT' in payload and 'MECANICA_INDISPONIVEL' in payload
  assert page.locator('#board .tile').count()==49
  assert page.locator('#unitList .unitBtn strong').all_text_contents()==units_before
  assert not errs,errs
  assert not net,net
  page.screenshot(path=f'/mnt/data/lote04_20261024/experimento/captura_{w}x{h}.png',full_page=True)
  print(w,h,'PASS','shapes 4','tiles',count,'errors',len(errs),'network',len(net),flush=True)
  results.append(dict(viewport=f'{w}x{h}',check='legacy preview retained; all 49 tiles; no network; no JS errors',status='PASS'))
  page.close()
 browser.close()
pathlib.Path('/mnt/data/lote04_20261024/experimento/resultados_test_geom.json').write_text(json.dumps({'directed_checks':len(results),'pass':sum(x['status']=='PASS' for x in results),'cases':results},indent=2,ensure_ascii=False))
