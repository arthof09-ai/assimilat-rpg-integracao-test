from playwright.sync_api import sync_playwright
from pathlib import Path
import json, tempfile
DIR=Path(__file__).resolve().parent
HTML=(DIR/'TABLETOP_ASSIMILACAO_INOVADOR_TEST_06.html').read_text()
FIXTURE=json.loads((DIR/'VLAB_TEST03_FIXTURE_SINTETICA.json').read_text())
results=[]
def check(name, fn):
    try:
        assert fn(),name
        results.append((name,True))
        print('PASS |',name)
    except Exception as ex:
        results.append((name,False))
        print('FAIL |',name,repr(ex))
        raise
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,accept_downloads=True)
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content(HTML)
    cam=lambda:page.evaluate('window.__inovadorTest05.camera()')
    state=lambda:page.evaluate('window.__arenaTest.get()')
    check('TEST05 presente',lambda:'TEST 06' in page.locator('.badge').first.inner_text())
    check('controle de zoom presente',lambda:page.locator('#zoom').count()==1)
    check('zoom inicial 44',lambda:cam()['zoom']==44)
    page.locator('#zoomIn').click()
    check('zoom + altera tamanho célula',lambda:cam()['zoom']==48 and page.locator('.cell').first.evaluate('(e)=>e.getBoundingClientRect().width')==48)
    page.locator('#zoomOut').click()
    check('zoom - restaura',lambda:cam()['zoom']==44)
    page.evaluate('window.__inovadorTest05.zoom(96)')
    check('zoom máximo 96',lambda:cam()['zoom']==96)
    page.evaluate('window.__inovadorTest05.zoom(400)')
    check('limite superior impede extrapolação',lambda:cam()['zoom']==96)
    page.evaluate('window.__inovadorTest05.zoom(0)')
    check('limite inferior 28',lambda:cam()['zoom']==28)
    page.locator('#zoom').fill('60')
    page.locator('#zoom').dispatch_event('input')
    check('slider altera zoom',lambda:cam()['zoom']==60)
    page.locator('#panToggle').click()
    check('pan liga',lambda:cam()['pan'] and page.locator('#panToggle').get_attribute('aria-pressed')=='true')
    page.locator('#size').select_option('20')
    page.evaluate('window.__inovadorTest05.zoom(96)')
    page.locator('#centerMap').click()
    check('mapa grande permite scroll',lambda:page.locator('#boardWrap').evaluate('(e)=>e.scrollWidth>e.clientWidth && e.scrollHeight>e.clientHeight'))
    check('centralizar ajusta câmera',lambda:cam()['x']>0 and cam()['y']>0)
    before=cam()
    # Pointer mouse drag on boardWrap with pan enabled
    page.evaluate('''() => {const w=document.getElementById('boardWrap');
      w.dispatchEvent(new PointerEvent('pointerdown',{pointerId:77,pointerType:'touch',clientX:180,clientY:210,bubbles:true}));
      w.dispatchEvent(new PointerEvent('pointermove',{pointerId:77,pointerType:'touch',clientX:110,clientY:130,bubbles:true}));
      w.dispatchEvent(new PointerEvent('pointerup',{pointerId:77,pointerType:'touch',clientX:110,clientY:130,bubbles:true}));}''')
    check('arraste move viewport',lambda:cam()['x']>before['x'] and cam()['y']>before['y'])
    check('arrastar nao move unidades',lambda:state()['units'][0]['x']==1 and state()['units'][0]['y']==2)
    page.locator('#panToggle').click()
    check('pan desliga',lambda:not cam()['pan'])
    page.evaluate('window.__inovadorTest05.zoom(44)')
    page.locator('#reset').click()
    page.locator('#size').select_option('7')
    cell=lambda x,y:page.locator(f'[data-xy="{x},{y}"]')
    start=state()['units'][0]['x']
    cell(2,2).click()
    check('movimento segue ativo com pan desligado',lambda:state()['units'][0]['x']==2)
    page.locator('#undo').click()
    check('undo restaurou unidade',lambda:state()['units'][0]['x']==start)
    check('redo foi habilitado',lambda:page.locator('#redo').is_enabled() and page.evaluate('window.__arenaTest.redoLength()')==1)
    page.locator('#redo').click()
    check('redo reaplica movimento',lambda:state()['units'][0]['x']==2)
    page.locator('#undo').click(); cell(1,1).click()
    check('nova ação invalida redo',lambda:page.locator('#redo').is_disabled())
    page.locator('#reset').click()
    check('reset limpa replay temporário e redo',lambda:page.locator('#redo').is_disabled() and len(page.evaluate('window.__arenaTest.history()'))==0)
    cell(2,2).click();cell(3,2).click()
    page.locator('#captureReplay').click()
    replay=lambda:page.evaluate('window.__inovadorTest05.replay()')
    check('captura contém 3 quadros',lambda:replay() is not None and len(replay()['events'])==3)
    check('schema TEST03 compatível',lambda:replay()['schema']=='assim.lab.vlab.readonly.v1')
    check('origem sintética obrigatória',lambda:replay()['source']['kind']=='SYNTHETIC_FIXTURE' and replay()['source']['scope']=='MESTRE_ONLY')
    check('posições de replay corretas',lambda:replay()['events'][2]['frame']['positions']['b']==[3,2])
    check('replay começa no quadro zero',lambda:page.evaluate('window.__inovadorTest05.replayIndex()')==0)
    page.locator('#replayNext').click()
    check('replay avança',lambda:page.evaluate('window.__inovadorTest05.replayIndex()')==1)
    page.locator('#replayLast').click()
    check('replay último quadro',lambda:page.evaluate('window.__inovadorTest05.replayIndex()')==2)
    page.locator('#replayPrev').click()
    check('replay retrocede',lambda:page.evaluate('window.__inovadorTest05.replayIndex()')==1)
    page.locator('#replayFirst').click()
    check('replay reinicia',lambda:page.evaluate('window.__inovadorTest05.replayIndex()')==0)
    page.evaluate('window.__inovadorTest05.seek(10000)')
    check('seek fora do intervalo é limitado',lambda:page.evaluate('window.__inovadorTest05.replayIndex()')==2)
    check('replay não altera estado de arena',lambda:state()['units'][0]['x']==3)
    page.locator('#replayClear').click()
    check('replay limpar preserva arena',lambda:replay() is None and state()['units'][0]['x']==3)
    page.locator('#captureReplay').click()
    with page.expect_download() as dl:
        page.locator('#replayExport').click()
    d=dl.value
    check('JSON exportado',lambda:d.suggested_filename=='INOVADOR_TEST06_REPLAY_SINTETICO.json')
    with tempfile.TemporaryDirectory() as temp:
        saved=Path(temp)/'r.json';d.save_as(saved)
        exported=json.loads(saved.read_text())
        check('export JSON idêntico replay',lambda:exported==replay())
        check('validator aceita própria exportação',lambda:page.evaluate('(d)=>window.__inovadorTest05.validateReplay(d)',exported) is None)
        page.locator('#replayClear').click()
        page.locator('#replayImport').set_input_files(str(saved))
        page.wait_for_function('window.__inovadorTest05.replay() !== null')
        check('reimport JSON restaura replay',lambda:replay() is not None and len(replay()['events'])==3)
    check('aceita fixture TEST03 independente',lambda:page.evaluate('(d)=>window.__inovadorTest05.validateReplay(d)',FIXTURE) is None)
    page.evaluate('(d)=>window.__inovadorTest05.loadReplay(d)',FIXTURE)
    check('fixture TEST03 carregada na interface',lambda:len(replay()['events'])==4)
    check('fixture externa não altera arena',lambda:state()['units'][0]['x']==3)
    bad=json.loads(json.dumps(FIXTURE));bad['source']['kind']='VLAB_TEST_EXPORT'
    check('bloqueia VLAB real não verificado',lambda:'HOLD' in page.evaluate('(d)=>window.__inovadorTest05.validateReplay(d)',bad))
    bad=json.loads(json.dumps(FIXTURE));bad['events'][0]['id']=bad['events'][1]['id']
    check('rejeita IDs repetidos',lambda:page.evaluate('(d)=>window.__inovadorTest05.validateReplay(d)',bad) is not None)
    bad=json.loads(json.dumps(FIXTURE));bad['events'][0]['frame']['positions']['u1']=[7,7]
    check('rejeita coordenadas fora',lambda:page.evaluate('(d)=>window.__inovadorTest05.validateReplay(d)',bad) is not None)
    bad=json.loads(json.dumps(FIXTURE));bad['events'][0]['frame']['positions']['u1']=bad['events'][0]['frame']['positions']['u2']
    check('rejeita sobreposição',lambda:page.evaluate('(d)=>window.__inovadorTest05.validateReplay(d)',bad) is not None)
    bad=json.loads(json.dumps(FIXTURE));bad['units'][0]['label']='<img src=x onerror=alert(1)>'
    check('rejeita HTML malicioso',lambda:page.evaluate('(d)=>window.__inovadorTest05.validateReplay(d)',bad) is not None)
    bad=json.loads(json.dumps(FIXTURE));bad['grid']['walls'].append(bad['grid']['walls'][0])
    check('rejeita parede duplicada',lambda:page.evaluate('(d)=>window.__inovadorTest05.validateReplay(d)',bad) is not None)
    bad=json.loads(json.dumps(FIXTURE));bad['source']['scope']='PARTY'
    check('não aceita Party',lambda:page.evaluate('(d)=>window.__inovadorTest05.validateReplay(d)',bad) is not None)
    bad=json.loads(json.dumps(FIXTURE));bad['events']=bad['events']*26
    check('rejeita replay acima de 100 eventos',lambda:page.evaluate('(d)=>window.__inovadorTest05.validateReplay(d)',bad) is not None)
    check('ausência erros JS',lambda:not errors)
    check('viewport sem overflow 390',lambda:page.evaluate('document.documentElement.scrollWidth<=window.innerWidth+1'))
    page.screenshot(path=str(DIR/'TABLETOP_ASSIMILACAO_TEST05_390x844.png'),full_page=True)
    browser.close()
print('RESULTADO TEST05 NOVOS',sum(x[1] for x in results),'/',len(results))
