from playwright.sync_api import sync_playwright
from pathlib import Path
import json
out=Path('/mnt/data/relatorio_496132_20261024'); html=(out/'OFICINA_SPRITES_ASSIMILACAO_TEST_ANDROID_OFFLINE.html').read_text()
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for w,h in [(360,740),(390,844),(412,915)]:
  page=browser.new_page(viewport={'width':w,'height':h},accept_downloads=True)
  errors=[];requests=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append(r.url))
  page.set_content(html,wait_until='load');page.wait_for_timeout(750)
  checks={}
  checks['title']='Oficina de Sprites' in page.title()
  checks['stage_has_alpha']=page.locator('#stage').evaluate('(e)=>e.getContext("2d").getImageData(20,20,1,1).data[3]')>0
  checks['sheet_is_192']=page.locator('#sheet').evaluate('(e)=>e.width===192&&e.height===192')
  checks['default_grid']=page.locator('#cols').input_value()=='4' and page.locator('#rows').input_value()=='4'
  checks['16_nonempty']=page.locator('#status').inner_text().find('nenhuma célula vazia')!=-1
  checks['audit_pass']=page.locator('#status').inner_text().find('ESTRUTURA TEST ADEQUADA')!=-1
  page.locator('#dir').select_option('2'); checks['direction']=page.locator('#dir').input_value()=='2'
  page.locator('#pause').click();checks['pause']=page.locator('#pause').inner_text().startswith('Reproduzir')
  page.locator('#pause').click();checks['resume']=page.locator('#pause').inner_text().startswith('Pausar')
  with page.expect_download(timeout=3000) as down:page.locator('#export').click()
  artifact=down.value
  checks['export']=artifact.suggested_filename=='ASSIMILACAO_SPRITES_TEST.json'
  page.locator('#cols').fill('7');page.locator('#cols').dispatch_event('change');checks['invalid_grid']='não divisível' in page.locator('#status').inner_text()
  page.locator('#reset').click();page.wait_for_function("document.getElementById('status').textContent.includes('ESTRUTURA TEST ADEQUADA')");checks['reset']=page.locator('#cols').input_value()=='4' and 'ESTRUTURA TEST ADEQUADA' in page.locator('#status').inner_text()
  checks['no_errors']=not errors;checks['offline_no_requests']=not requests
  checks['mobile_width_fit']=page.evaluate('document.documentElement.scrollWidth<=window.innerWidth+2')
  if (w,h)==(390,844):page.screenshot(path=str(out/'OFICINA_SPRITES_TEST_390x844.png'),full_page=True)
  result={'viewport':f'{w}x{h}','passed':sum(checks.values()),'total':len(checks),'checks':checks,'errors':errors,'requests':requests};results.append(result)
  print(result['viewport'],result['passed'],'/',result['total'],'failed',[k for k,v in checks.items() if not v]);page.close()
 browser.close()
(out/'RESULTADOS_TESTE_OFICINA.json').write_text(json.dumps(results,indent=2,ensure_ascii=False))
assert all(r['passed']==r['total'] for r in results)
