from pathlib import Path
from playwright.sync_api import sync_playwright
SRC=Path(__file__).parent/'TABLETOP_ASSIMILACAO_INOVADOR_TEST_05.html'
checks=[]
def ok(title,value):
 assert value,title
 print('PASS |',title);checks.append(title)
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 pg=b.new_page(viewport={'width':360,'height':740},is_mobile=True,has_touch=True)
 errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
 pg.set_content(SRC.read_text())
 pg.locator('#size').select_option('20')
 ok('400 casas no viewport 360',pg.locator('.cell').count()==400)
 ok('touch-action permite pinch customizado',pg.locator('#boardWrap').evaluate('(e)=>getComputedStyle(e).touchAction')=='none')
 before=pg.evaluate('window.__inovadorTest05.camera()')
 pg.evaluate('''() => {const w=document.getElementById('boardWrap');
 for(const [type,id,x] of [['pointerdown',1,90],['pointerdown',2,230],['pointermove',2,340],['pointerup',1,90],['pointerup',2,340]])
  w.dispatchEvent(new PointerEvent(type,{pointerId:id,pointerType:'touch',clientX:x,clientY:180,bubbles:true}));}''')
 after=pg.evaluate('window.__inovadorTest05.camera()')
 ok('pinça amplia o mapa',after['zoom']>before['zoom'])
 ok('pinça não movimenta personagem',pg.evaluate('window.__arenaTest.get().units[0].x')==1)
 pg.locator('#panToggle').click();pg.locator('#panToggle').click()
 ok('modo pan reversível após pinça',pg.evaluate('window.__inovadorTest05.camera().pan')==False)
 ok('nenhum erro JavaScript',not errs)
 ok('documento sem overflow horizontal 360',pg.evaluate('document.documentElement.scrollWidth<=window.innerWidth+1'))
 pg.screenshot(path=str(Path(__file__).parent/'TABLETOP_ASSIMILACAO_TEST05_360x740.png'),full_page=True)
 b.close()
print('RESULT',len(checks),'/',len(checks))
