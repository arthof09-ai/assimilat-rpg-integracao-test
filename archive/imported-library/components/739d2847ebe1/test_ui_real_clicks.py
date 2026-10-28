import asyncio,json,pathlib
from playwright.async_api import async_playwright
from test_integrated import mount,ROOT
async def suite(browser,w,h):
 page=await browser.new_page(viewport={'width':w,'height':h})
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 await mount(page);results=[]
 async def check(name,ok):
  if not ok:raise AssertionError(f'{w}x{h} {name}')
  results.append(name)
 state=lambda:page.evaluate('window.__tabletopTEST.scene()')
 await page.locator('.tile[data-xy="1,1"]').click()
 await check('seleciona via grid click',(await state())['selected']=='u1')
 await page.locator('.tile[data-xy="2,1"]').click()
 await check('move via click da tela',(await state())['units'][0]['x']==2)
 await check('historico registrado',(await state())['frames'][-1]['positions']['u1']==[2,1])
 await page.locator('[data-mode="wall"]').click()
 await page.locator('.tile[data-xy="2,2"]').click()
 await check('edita parede via toque','2,2' in (await state())['walls'])
 await page.locator('[data-mode="erase"]').click()
 await page.locator('.tile[data-xy="2,2"]').click()
 await check('apaga parede via toque','2,2' not in (await state())['walls'])
 await page.locator('[data-mode="pan"]').click()
 old=await state()
 await page.locator('.tile[data-xy="3,1"]').click()
 await check('modo pan bloqueia movimento',(await state())['units']==old['units'])
 await page.locator('[data-mode="play"]').click()
 await page.locator('.tile[data-xy="3,1"]').click()
 await page.locator('#record').click()
 await check('captura por botão cria replay',int((await page.locator('#replayCounter').inner_text()).split('/')[1])>=2)
 await page.locator('#replayNext').click()
 await check('avança replay por botão',(await page.locator('#replayCounter').inner_text()).startswith('2/'))
 await check('erros JS ausentes',not errors)
 await page.close();return results
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  a=await suite(browser,390,844);b=await suite(browser,360,740)
  await browser.close()
 print('UI REAL CLICKS:',len(a),'+',len(b),'=',len(a)+len(b),'PASS')
 (ROOT.parent/'evidence'/'ui_click_results.json').write_text(json.dumps({'390':a,'360':b,'total':len(a)+len(b)},ensure_ascii=False,indent=2))
if __name__=='__main__':asyncio.run(main())
