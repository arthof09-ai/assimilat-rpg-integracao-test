from playwright.sync_api import sync_playwright
import pathlib,json
p=pathlib.Path(__file__).resolve().parents[1]/'ui/VLAB_R205_BANCADA_MAGIA_DEFESA_ITEM_CLASSIFICADO_OFFLINE.html'
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path="/usr/bin/chromium",args=["--no-sandbox"])
 page=b.new_page(viewport={'width':390,'height':844})
 errors=[]
 page.on('pageerror',lambda err:errors.append(str(err)))
 page.set_content(p.read_text(),wait_until='domcontentloaded')
 tabs=page.locator('button.tab').count()
 page.locator('button[data-tab="r205"]').click()
 assert page.locator('#r205').is_visible()
 assert '20' in page.locator('#r205-kpis').inner_text()
 assert page.locator('#r205-rows tr').count()==12
 page.locator('#r205-cohort').select_option('RING')
 assert page.locator('#r205-rows tr').count()==8
 assert page.locator('#r205-trace tr').count()>1
 page.locator('#r205-run').select_option(index=1)
 assert 'ANEL' in page.locator('#r205-trace').inner_text()
 page.locator('button[data-tab="r204"]').click()
 assert page.locator('#r204').is_visible() and page.locator('#r204-rows tr').count()==32
 page.locator('button[data-tab="r200"]').click()
 assert page.locator('#r200').is_visible() and page.locator('#r200-rows tr').count()>0
 page.locator('button[data-tab="r205"]').click()
 shot=pathlib.Path('/mnt/data/vlab_r205_work/new/r205/evidence/R205_MOBILE_SCREENSHOT.png')
 page.screenshot(path=str(shot),full_page=True)
 assert not errors,errors
 print(json.dumps({'result':'PASS_MOBILE_EIGHT_TABS','tabs':tabs,'wind_rows':12,'ring_rows':8,'R204_R200_preserved':True,'js_errors':errors,'screenshot':str(shot)},ensure_ascii=False))
 b.close()
