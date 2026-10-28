from playwright.sync_api import sync_playwright
from pathlib import Path
import json
html=Path('/mnt/data/playlist_20261024/ARENA_TEST36_CAMADAS_AMBIENTAIS_OFFLINE.html').read_text()
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for width,height in [(360,740),(390,844),(412,915)]:
  page=browser.new_page(viewport={'width':width,'height':height})
  errors=[];net=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('request',lambda r:net.append(r.url))
  page.set_content(html,wait_until='load')
  page.wait_for_timeout(350)
  tiles=page.locator('#board .tile').count()
  exist=page.locator('#scene-test-panel').count()==1
  for scene in ['rain','night','day']:
   page.locator(f'[data-scene={scene}]').click()
   active=page.locator('#viewport').get_attribute('class')
   button=page.locator(f'[data-scene={scene}]').get_attribute('aria-pressed')
   results.append({'viewport':f'{width}x{height}','test':f'{scene}_activated','passed':('scene-'+scene) in active and button=='true'})
  page.locator('#scene-export').click()
  text=page.locator('#scene-export-output').input_value()
  d=json.loads(text)
  for name,val in [('49_tiles',tiles==49),('panel_exists',exist),('contract_version',d['schema_version']=='assim.tabletop.scene.presentation.test.v1'),('no_mechanics',d['apply_mechanics']==False),('no_server_send',d['sent_to_server']==False),('zero_requests',len(net)==0),('zero_js_errors',len(errors)==0)]:results.append({'viewport':f'{width}x{height}','test':name,'passed':val})
  if width==390:
   page.locator('[data-scene=rain]').click();results.append({'viewport':f'{width}x{height}','test':'export_refreshes_on_mode_change','passed':json.loads(page.locator('#scene-export-output').input_value())['mode']=='rain'});page.locator('#scene-test-panel').scroll_into_view_if_needed();page.screenshot(path='/mnt/data/playlist_20261024/PROVA_CENARIO_CHUVA_390x844.png')
  page.close()
 browser.close()
path='/mnt/data/playlist_20261024/test_scene_results.json';Path(path).write_text(json.dumps(results,indent=2))
print('PASS',sum(x['passed'] for x in results),'/',len(results));print([x for x in results if not x['passed']]);
