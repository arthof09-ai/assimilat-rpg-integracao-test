"""TEST06 functional & security checks: mobile Chromium, read-only synthetic fixture."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import json,copy
DIR=Path(__file__).resolve().parent
HTML=(DIR/'TABLETOP_ASSIMILACAO_INOVADOR_TEST_06.html').read_text(encoding='utf-8')
FIXTURE=json.loads((DIR/'VLAB_TEST03_FIXTURE_SINTETICA.json').read_text())
checks=[]
def check(name, cond):
 try:
  assert cond,name
  checks.append(name)
  print('PASS | '+name)
 except Exception:
  print('FAIL | '+name)
  raise
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for vw,vh in [(390,844),(360,740)]:
  page=browser.new_page(viewport={'width':vw,'height':vh},is_mobile=True,has_touch=True,accept_downloads=True)
  errors=[]; requests=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('request',lambda r:requests.append(r.url))
  page.set_content(HTML)
  state=lambda:page.evaluate('window.__arenaTest.get()')
  camera=lambda:page.evaluate('window.__inovadorTest05.camera()')
  layers=lambda:page.evaluate('window.__inovadorTest06.layers()')
  check(f'{vw}: identidade TEST06',page.locator('.badge').first.inner_text().find('TEST 06')>=0)
  check(f'{vw}: minimapa disponível',page.locator('#miniMap').count()==1 and page.evaluate('window.__inovadorTest06.miniSize()')==200)
  check(f'{vw}: canvas minimapa renderizado',page.locator('#miniMap').evaluate('(e)=>e.getContext("2d").getImageData(0,0,1,1).data[3]')>0)
  check(f'{vw}: camadas iniciais on',all(layers().values()))
  initial=json.dumps(state(),sort_keys=True)
  page.locator('[data-layer="coords"]').click()
  check(f'{vw}: coordenadas invisíveis',layers()['coords'] is False and page.locator('.board').evaluate('(e)=>e.classList.contains("hide-coords")'))
  check(f'{vw}: seletor reflete estado',page.locator('[data-layer="coords"]').get_attribute('aria-pressed')=='false')
  page.locator('[data-layer="threat"]').click()
  check(f'{vw}: ameaça visual off',layers()['threat'] is False)
  page.locator('[data-layer="reach"]').click()
  check(f'{vw}: alcance visual off',layers()['reach'] is False)
  check(f'{vw}: camadas não alteram motor',json.dumps(state(),sort_keys=True)==initial)
  page.locator('[data-layer="coords"]').click()
  check(f'{vw}: coordenadas restauradas',layers()['coords'] is True)
  page.locator('#size').select_option('20')
  page.evaluate('window.__inovadorTest05.zoom(96)')
  page.locator('#centerMap').click()
  before=camera()
  check(f'{vw}: mapa 20x20 navegável',before['x']>0 and before['y']>0)
  page.locator('#miniMap').click(position={'x':15,'y':17})
  after=camera()
  check(f'{vw}: minimapa desloca camera',after['x']<before['x'] and after['y']<before['y'])
  check(f'{vw}: minimapa não altera estado',state()['n']==20 and state()['units'][0]['x']==1)
  page.locator('#focusToken').click()
  check(f'{vw}: foco não altera token',state()['units'][0]['x']==1 and state()['units'][0]['y']==2)
  # cancel event after gesture must not leave pending gesture for next tap.
  page.evaluate('''() => { const w=document.getElementById('boardWrap');
    w.dispatchEvent(new PointerEvent('pointerdown',{pointerId:201,pointerType:'touch',clientX:100,clientY:150,bubbles:true}));
    w.dispatchEvent(new PointerEvent('pointercancel',{pointerId:201,pointerType:'touch',clientX:100,clientY:150,bubbles:true}));
  }''')
  page.wait_for_timeout(20)
  check(f'{vw}: pointercancel limpa ponteiros',page.evaluate('window.__inovadorTest06.gesture().count')==0)
  check(f'{vw}: pointercancel sem estado preso',page.evaluate('window.__inovadorTest06.gesture().active') is False)
  # two-touch synthetic pointer pinch with moving midpoint
  page.evaluate("window.__inovadorTest05.zoom(44)")
  startzoom=camera()['zoom']
  page.evaluate('''() => {const w=document.getElementById('boardWrap'); const E=(type,id,x,y)=>w.dispatchEvent(new PointerEvent(type,{pointerId:id,pointerType:'touch',clientX:x,clientY:y,bubbles:true}));
    E('pointerdown',311,90,180);E('pointerdown',312,180,180);E('pointermove',311,75,180);E('pointermove',312,220,180);E('pointerup',311,75,180);E('pointerup',312,220,180);
  }''')
  check(f'{vw}: pinça altera zoom',camera()['zoom']!=startzoom)
  check(f'{vw}: pinça não altera personagens',state()['units'][0]['x']==1 and state()['units'][1]['x']==0)
  page.wait_for_timeout(20)
  check(f'{vw}: dois toques liberados',page.evaluate('window.__inovadorTest06.gesture().count')==0)
  page.locator('#panToggle').click();page.locator('#panToggle').click()
  page.locator('#size').select_option('7')
  page.locator('#reset').click()
  page.locator('[data-xy="2,2"]').click()
  check(f'{vw}: toque após gestos move unidade',state()['units'][0]['x']==2)
  page.locator('#captureReplay').click()
  check(f'{vw}: replay gerado',page.evaluate('window.__inovadorTest05.replay()') is not None)
  page.locator('#replayNext').click()
  check(f'{vw}: delta exibe antes/depois', '→' in page.locator('#replayDelta').inner_text())
  beforeReplay=json.dumps(state(),sort_keys=True)
  page.locator('#replayFirst').click()
  check(f'{vw}: navegar replay sem mutação',json.dumps(state(),sort_keys=True)==beforeReplay)
  malicious=copy.deepcopy(FIXTURE)
  first_id=malicious['units'][0]['id']
  malicious['units'][0]['id']='__proto__'
  for ev in malicious['events']:
   ev['frame']['positions']['__proto__']=ev['frame']['positions'].pop(first_id)
  rejection=page.evaluate('(d)=>window.__inovadorTest05.validateReplay(d)',malicious)
  check(f'{vw}: rejeita chave __proto__',isinstance(rejection,str) and 'inválida' in rejection)
  check(f'{vw}: não houve erro JS',len(errors)==0)
  check(f'{vw}: nenhuma requisição externa',len(requests)==0)
  check(f'{vw}: documento mobile sem overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
  page.screenshot(path=str(DIR/f'TABLETOP_TEST06_{vw}x{vh}.png'),full_page=True)
  page.close()
 browser.close()
print('RESULTADO NOVOS',len(checks),'/',len(checks))
