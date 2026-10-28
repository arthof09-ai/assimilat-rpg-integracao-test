"""Research-side checks against unmodified recovered TEST15 sources. Never mutates originals."""
import json, threading, socketserver, http.server, contextlib, os, random, re
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path('/mnt/data/inovador_pesq_pos15/audit/public')
OUT=Path('/mnt/data/inovador_pesq_pos15/evidence'); OUT.mkdir(exist_ok=True)
class Quiet(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
 def log_message(self,*a):pass
class Server(socketserver.ThreadingTCPServer):allow_reuse_address=True
s=Server(('127.0.0.1',0),Quiet); port=s.server_address[1]
th=threading.Thread(target=s.serve_forever,daemon=True);th.start()
results=[]
def check(name, cond, details=None):
 results.append(dict(name=name,passed=bool(cond),details=details)); print(('PASS' if cond else 'FAIL'),name,details if details is not None else '')
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 context=browser.new_context(viewport={'width':390,'height':844},accept_downloads=True)
 page=context.new_page(); errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(re.sub(r'<meta http-equiv="Content-Security-Policy"[^>]+>', '', (ROOT/'index.html').read_text(encoding='utf-8')))
 page.add_style_tag(content=(ROOT/'styles.css').read_text(encoding='utf-8'))
 page.evaluate("""() => {window.__storageTEST={};Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem(k){return Object.hasOwn(window.__storageTEST,k)?window.__storageTEST[k]:null;},setItem(k,v){window.__storageTEST[k]=String(v);},removeItem(k){delete window.__storageTEST[k];}}});}""")
 page.add_script_tag(content=(ROOT/'app.js').read_text(encoding='utf-8'))
 page.wait_for_function('window.__tabletopTEST !== undefined')
 base=page.evaluate('window.__tabletopTEST.state()');check('public-three-assets-loaded',len(base['scenes'])==1 and base['schema']=='assim.tabletop.synthetic.workspace.v1');check('initial-no-js-errors',not errors,errors)
 # Inject benign-but-inconsistent frame topology: source function validateScene accepts mismatched frameTopology
 injected=page.evaluate('''() => {const s=__tabletopTEST.scene(),w=__tabletopTEST.state();w.scenes[0].frames=[{title:'Corrompido TEST',positions:Object.fromEntries(s.units.map(u=>[u.id,[u.x,u.y]]))}];w.scenes[0].frameTopology='tampered';return {accepted:__tabletopTEST.validateWorkspace(w),frameTopology:w.scenes[0].frameTopology}}''')
 check('replay-topology-not-validated-finding',injected['accepted'] is True,injected)
 # Invalid replay semantic order accepted if both ids unique; this validator doesn't prescribe order intentionally.
 sem=page.evaluate('''() => {let r=__tabletopTEST.makeReplay();let ev=structuredClone(r.events[0]);ev.id='frame-000';ev.type='POSITION';r.events.unshift(ev);return {accepted:__tabletopTEST.validateReplay(r),events:r.events.map(e=>e.id)};}''')
 check('replay-sequence-not-enforced-finding',sem['accepted'] is True,sem)
 # Browser storage failure after valid restore: no destructive mutation expected. Test actual event import without touching original app source.
 before=page.evaluate('window.__tabletopTEST.state()')
 backup=json.loads(json.dumps(before));backup['scenes'][0]['name']='CENA IMPORTADA SEM SALVAMENTO'
 f=OUT/'fixture_restore_simulada.json';f.write_text(json.dumps(backup,ensure_ascii=False),encoding='utf-8')
 page.on('dialog',lambda d:d.accept());
 page.evaluate("""() => {localStorage.setItem=function(){throw new DOMException('Quota','QuotaExceededError');};}""")
 page.locator('#restore').set_input_files(str(f));page.wait_for_function("window.__tabletopTEST.state().scenes[0].name === 'CENA IMPORTADA SEM SALVAMENTO'")
 state=page.evaluate('''() => ({name:__tabletopTEST.state().scenes[0].name,status:document.querySelector('#storageStatus').textContent,saved:localStorage.getItem('assim.tabletop.synthetic.workspace.v1'),message:document.querySelector('#message').textContent})''')
 check('storage-failure-import-mutates-memory',state['saved']!=json.dumps(backup) and state['name']=='CENA IMPORTADA SEM SALVAMENTO',{'status':state['status'],'message':state['message'],'saved_character_count':len(state['saved'] or '')})
 check('storage-failure-disclosed-but-not-rolled-back', 'Falha' in state['status'],{'status':state['status']})
 # Side effects of failed store: after reload original storage data or default (not imported); verify no persistent imported scene.
 previous_saved=page.evaluate('window.__storageTEST')
 page2=context.new_page();page2.set_content(re.sub(r'<meta http-equiv="Content-Security-Policy"[^>]+>', '', (ROOT/'index.html').read_text(encoding='utf-8')));page2.add_style_tag(content=(ROOT/'styles.css').read_text(encoding='utf-8'))
 page2.evaluate("""state => {window.__storageTEST=state;Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem(k){return Object.hasOwn(window.__storageTEST,k)?window.__storageTEST[k]:null;},setItem(k,v){window.__storageTEST[k]=String(v);},removeItem(k){delete window.__storageTEST[k];}}});}""",previous_saved)
 page2.add_script_tag(content=(ROOT/'app.js').read_text(encoding='utf-8'));page2.wait_for_function('window.__tabletopTEST !== undefined')
 reloaded=page2.evaluate('window.__tabletopTEST.state().scenes[0].name')
 check('failed-save-does-not-survive-reload',reloaded!='CENA IMPORTADA SEM SALVAMENTO',{'reloaded':reloaded})
 # Patch local storage failure guard not in original; recommendation only
 check('no-js-errors-audit',not errors,errors)
 browser.close()
s.shutdown();s.server_close()
(OUT/'AUDITORIA_TEST15_ADVERSARIAL.json').write_text(json.dumps({'source':'sha256 e6f8eda189af26f94518ddbf1afcb1a8333bacfe94bb83419aca084a4563e613','environment':'Chromium set_content with injected JS/CSS and simulated localStorage 390x844, NOT Android','tests':results},indent=2,ensure_ascii=False),encoding='utf-8')
print('SUMMARY',sum(x['passed'] for x in results),'/',len(results))
