from pathlib import Path
import base64
from playwright.sync_api import sync_playwright
P=Path(__file__).resolve().parent
html=(P/'visualizador_atlas_TEST.html').read_text()
for f in ['mestre_test_sprite_atlas.png','inimigo_test_sprite_atlas.png','base_grama.png','base_pedra.png','base_agua.png']:
 html=html.replace("'"+f+"'","'data:image/png;base64,"+base64.b64encode((P/f).read_bytes()).decode()+"'")
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1)
 page.set_content(html,wait_until='load')
 page.wait_for_function("document.querySelector('#status').textContent.includes('5/5 PNG carregados')",timeout=10000)
 status=page.locator('#status').inner_text()
 page.select_option('#dir','3')
 assert page.locator('#dir').input_value()=='3'
 pixel=page.evaluate("""() => {const d=document.querySelector('canvas').getContext('2d').getImageData(0,0,240,120).data; return d.some(x=>x!==0)}""")
 assert pixel
 page.screenshot(path=str(P/'screenshot_prova_assets_chromium_390x844.png'),full_page=True)
 print('PASS chromium 390x844 via set_content in-memory due localhost blocked; '+status+'; direction interaction PASS; canvas pixels PASS; screenshot PASS')
 browser.close()
