from pathlib import Path
import json,copy,hashlib
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).parent
ARENA=ROOT/'ARENA_PONTE_REPLAY_INOVADOR_TEST_04.html'
OBSERVER=ROOT.parent/'originais/PACOTE_INTERCAMBIO_INOVADOR_TEST_03_20261022/ADAPTADOR_VLAB_READONLY_TEST_03.html'
checks=[]
def check(label,result):
 if not result:raise AssertionError(label)
 checks.append(label)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 arena=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1,is_mobile=True,has_touch=True)
 observer=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1,is_mobile=True,has_touch=True)
 errors=[]
 for page in (arena,observer):page.on('pageerror',lambda exc:errors.append(str(exc)))
 arena.set_content(ARENA.read_text());observer.set_content(OBSERVER.read_text())
 get=lambda:arena.evaluate('window.__inovadorBridgeTest.get()')
 capture=lambda:arena.evaluate('window.__inovadorBridgeTest.capture()')
 valid=lambda doc:observer.evaluate('(x)=>window.__vlabObserverTest.validate(x)',doc)
 first=capture();doc=first['doc']
 check('contrato export é versão do Observatório',doc['schema']=='assim.lab.vlab.readonly.v1')
 check('origem explicitamente sintética',doc['source']['kind']=='SYNTHETIC_FIXTURE')
 check('não é Party',doc['source']['scope']=='MESTRE_ONLY')
 check('cópia isolada declarada',doc['source']['isolatedCopy'] is True)
 check('versão TEST explícita',doc['source']['reference'].startswith('INOVADOR-TEST04'))
 check('validação pelo Observatório real',valid(doc) is None)
 check('unidades genéricas sem ficha real', all('TEST' in u['label'] for u in doc['units']))
 check('4 unidades mapeadas',len(doc['units'])==4)
 check('snapshot inicial único',len(doc['events'])==1)
 check('49 células preview',arena.locator('#bridgeGrid .bridgecell').count()==49)
 check('4 peças no preview',arena.locator('#bridgeGrid .mark').count()==4)
 check('download ativado após capture',arena.locator('#bridgeDownload').is_enabled())
 check('captura não altera estado arena',arena.evaluate('window.__arenaTest.get().stepsUsed')==0)
 stateBefore=arena.evaluate('window.__arenaTest.get()');capture();check('captura totalmente side-effect-free',stateBefore==arena.evaluate('window.__arenaTest.get()'))
 arena.locator('[data-xy="2,2"]').click()
 afterMove=capture();doc=afterMove['doc']
 check('timeline cresceu após movimento',len(doc['events'])==2)
 check('evento classificado como POSIÇÃO declarada',doc['events'][-1]['type']=='POSITION')
 check('posição final coincide com Arena',doc['events'][-1]['frame']['positions']['b']==[2,2])
 check('contrato após movimento válido',valid(doc) is None)
 check('navegar anterior e posterior',arena.locator('#bridgePrev').is_disabled() and arena.locator('#bridgeNext').is_enabled())
 arena.locator('#bridgeNext').click()
 check('próximo navegou',arena.locator('#bridgeStep').inner_text().startswith('Quadro 2/2'))
 arena.locator('#bridgePrev').click()
 check('anterior navegou',arena.locator('#bridgeStep').inner_text().startswith('Quadro 1/2'))
 check('replay não muda arena',arena.evaluate('window.__arenaTest.get().units[0].x')==2)
 observer.evaluate('(x)=>window.__vlabObserverTest.load(x)',doc)
 check('observatório carrega export TEST04',observer.locator('#stepLabel').inner_text()=='Evento 1/2')
 observer.locator('#next').click()
 check('observatório reproduz segundo frame',observer.locator('#stepLabel').inner_text()=='Evento 2/2')
 check('token posição final no Observatório',observer.evaluate('window.__vlabObserverTest.get().events[1].frame.positions.b[0]')==2)
 check('serialização export determinística',json.dumps(doc,sort_keys=True)==json.dumps(capture()['doc'],sort_keys=True))
 with arena.expect_download() as dl:arena.locator('#bridgeDownload').click()
 download=dl.value
 destination=ROOT/'INOVADOR_TEST04_PONTE_OBSERVATORIO_SINTETICA.json'
 download.save_as(destination)
 exported=json.loads(destination.read_text())
 check('download JSON browser funciona',exported==doc)
 check('JSON baixado aceito pelo observatório',valid(exported) is None)
 # mudança topológica: descarta snapshots incompatíveis, preserva atuais
 arena.locator('[data-mode="wall"]').click();arena.locator('[data-xy="3,1"]').click()
 wall=capture()
 check('alteração do mapa foi capturada',wall['doc']['grid']['walls']==[[3,1]])
 check('frames anteriores removidos após troca topológica',wall['discarded']>=1)
 check('mapa após modificação válido',valid(wall['doc']) is None)
 # não executar HTML injetado via JSON importado
 injected=copy.deepcopy(doc);injected['units'][0]['label']='<img src=x onerror=alert(1)>'
 check('observatório rejeita markup externo',isinstance(valid(injected),str))
 injected=copy.deepcopy(doc);injected['source']['scope']='PARTY'
 check('observatório rejeita escopo Party',isinstance(valid(injected),str))
 injected=copy.deepcopy(doc);injected['events'][0]['frame']['positions']['b']=[999,999]
 check('observatório rejeita coordenada inválida',isinstance(valid(injected),str))
 injected=copy.deepcopy(doc);injected['events'][1]['id']=injected['events'][0]['id']
 check('observatório rejeita IDs repetidos',isinstance(valid(injected),str))
 injected=copy.deepcopy(doc);injected['events'][0]['frame']['positions'].pop('w')
 check('observatório rejeita snapshot parcial',isinstance(valid(injected),str))
 # reset e 20x20
 arena.locator('#size').select_option('20')
 big=capture()['doc']
 check('20x20 schema validado',valid(big) is None)
 check('400 células no replay',arena.locator('#bridgeGrid .bridgecell').count()==400)
 check('sem requisições externas definidas',all('fetch(' not in ARENA.read_text() for _ in [1]))
 check('sem erros JS',not errors)
 check('viewport móvel sem overflow da página',arena.evaluate('document.documentElement.scrollWidth<=innerWidth+2'))
 # file:// não testável aqui: Chromium do sandbox bloqueia pelo administrador (HOLD separado).
 # volta 7 para captura
 arena.locator('#size').select_option('7');capture()
 arena.screenshot(path=str(ROOT/'INOVADOR_TEST04_CHROMIUM_MOBILE.png'),full_page=True)
 browser.close()
print(f'BRIDGE TEST04 {len(checks)}/{len(checks)} PASS')
for i,x in enumerate(checks,1):print(f'{i:02d} PASS {x}')
