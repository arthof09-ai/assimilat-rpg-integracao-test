#!/usr/bin/env python3
"""Auditoria ESTÁTICA reproduzível TEST36. Não executa RPG/VLAB, não certifica Android.
Uso: python verificador_aceite_combate_test36.py caminho/TABLETOP_SITE_SINTETICO_TEST36_CANDIDATE.zip
"""
import sys, zipfile, re, json, hashlib
from pathlib import Path

path=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/mnt/data/video_lote_20261024/test36_ref/TABLETOP_SITE_SINTETICO_TEST36_CANDIDATE.zip')
with zipfile.ZipFile(path) as z:
    assert z.testzip() is None
    file_list=z.namelist()
    x={name:z.read(name).decode('utf8') for name in file_list if name.endswith(('.html','.js','.css'))}
html=x.get('index.html','')
js=x.get('app.js','')
rjs=x.get('room-client.js','')
vad=x.get('room-v2-adapter.js','')

checks=[
('UI mapa/grade presente', 'IMPLEMENTADO_TEST', 'id="viewport"' in html and 'id="board"' in html,'DOM do TEST36: #viewport e #board'),
('Painel de unidades e edição TEST', 'IMPLEMENTADO_TEST', 'id="unitList"' in html and 'id="tokHp"' in html,'DOM de editor token e recurso TEST'),
('Perfis Mestre/P1/P2 sintéticos', 'IMPLEMENTADO_TEST', all(t in html for t in ['Mestre DEMO','Player 1 DEMO','Player 2 DEMO']),'Perfis DEMO não autenticados'),
('Recuperação de intenção/recibo em fixture v2', 'IMPLEMENTADO_TEST', 'id="roomReceipt"' in html and 'RECEIPT_QUERY' in vad+rjs,'Consulta local não garante durabilidade servidor'),
('Rodada visual somente TEST', 'IMPLEMENTADO_TEST', 'id="nextRound"' in html and 'não executa iniciativa oficial' in js,'Botão rodada sintética não é iniciativa canônica'),
('Seleção de AÇÃO ataque/magia no DOM', 'PENDENTE', not bool(re.search(r'<button\b[^>]*\bid=["\'](?:attack|attackAction|castSpell|defendAction)["\']',html,re.I)),'Não há botão de ação mecânica com ids auditados; revisar nomenclaturas futuras'),
('Iniciativa oficial com fonte autorizada', 'PENDENTE', 'não executa iniciativa oficial' in js,'O código nega explicitamente iniciativa oficial'),
('Resolução de dano VLAB no TEST36', 'PENDENTE', 'sem motor oficial de combate' in html and not bool(re.search(r'vlab[_-]?(?:engine|execute|resolve)|mechanical[_-]?engine',js,re.I)),'Ausência de interface VLAB mecânica no bundle entregue'),
('Autenticação multiplayer real', 'PENDENTE', 'Não conecta aparelhos, não autentica usuários' in html,'Texto explicita fixture e ausência de auth'),
('Segurança server-side Mestre/Party comprovada', 'PENDENTE', 'nenhuma alteração em Party' in html and "connect-src 'none'" in html,'Site TEST sem rede real, não prova filtro server-side'),
('Três Android conectados', 'PENDENTE', 'Não conecta aparelhos' in html,'Não há teste físico no código/artefato'),
]
result=[]
for label,kind,ok,note in checks:
 result.append({'check':label,'expected_class':kind,'assertion_supported':bool(ok),'evidence_note':note})
if not all(r['assertion_supported'] for r in result):
 raise SystemExit('Falha de PREMISSA em audit estática: '+json.dumps([r for r in result if not r['assertion_supported']],ensure_ascii=False))
report={'source_name':path.name,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(), 'method':'inspecao estatica deterministica, NEGATIVOS sao bloqueios e nao testes funcionais','coverage':len(result),'present_test':sum(r['expected_class']=='IMPLEMENTADO_TEST' for r in result), 'pending_blocker':sum(r['expected_class']=='PENDENTE' for r in result),'checks':result,'disclaimer':'NÃO mede mecânica VLAB, não executa Android, não testa servidores WSS e não substitui aceite funcional por jogador'}
out=Path(__file__).with_name('ACEITE_COMBATE_TEST36_BASELINE.json')
out.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
print(json.dumps({k:report[k] for k in ['source_sha256','coverage','present_test','pending_blocker']},ensure_ascii=False))
print('PREMISSAS '+str(len(result))+'/'+str(len(result))+' demonstradas por inspeção estática; 6 são lacunas e NÃO PASS funcional')
