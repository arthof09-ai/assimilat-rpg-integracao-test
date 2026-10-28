import asyncio,json,pathlib
from playwright.async_api import async_playwright
root=pathlib.Path(__file__).parent
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=await browser.new_page(viewport={'width':390,'height':844})
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  await page.set_content((root/'TIMELINE_VLAB_R205_MESTRE_ONLY_TEST19.html').read_text())
  data=root/'VLAB_R205_TIMELINE_REAL_MESTRE_ONLY.json';await page.locator('#file').set_input_files(str(data))
  await page.wait_for_function('window.__r205TEST.caseCount()===20');checks=[]
  def check(name,flag):
   assert flag,name;checks.append(name)
  e=await page.evaluate('window.__r205TEST.selected()')
  view=await page.locator('#detail').inner_text()
  check('composite stable identifier present','ID composto de apresentação:' in view and 'commit-001' in view)
  check('original command trace preserved',e['command'] in view)
  check('physical row hash shown',e['rowHash'] in view)
  sample=await page.evaluate('window.__r205TEST.eventIdentifier("CASE_TEST",{seq:4,command:"SYNTH_CMD"})')
  check('composite ID computed without numeric-only collision',sample=='CASE_TEST / commit-004 / SYNTH_CMD')
  check('source hash still visible', 'SHA fonte:' in await page.locator('#status').inner_text())
  check('no JS exceptions',not errors)
  print('PRIVATE TEST23 ENHANCEMENTS',len(checks),'/',len(checks),'PASS');
  (root/'test_private23_results.json').write_text(json.dumps({'count':len(checks),'tests':checks},ensure_ascii=False,indent=2))
  await browser.close()
asyncio.run(main())
