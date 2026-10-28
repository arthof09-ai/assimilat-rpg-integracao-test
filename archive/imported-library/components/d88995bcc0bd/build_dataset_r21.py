"""Reconcilia custos históricos R05 (108 itens) + 3 R06 + 1 ficha extra.
Todos os 13 IDs de Notion foram readback Mestre-Side em 19/10/2026.
Nao busca novas fichas nem altera fonte; preserva modalidades per_use distintas de per_turn.
"""
import csv,io,json,zipfile,hashlib
from pathlib import Path
from pa_r21_habilidades import activation_summary
ROOT=Path(__file__).resolve().parent
R05=ROOT/'BASELINES'/'PA_UNIVERSAL_R05_TEST_20261017.zip'
R06=ROOT/'BASELINES'/'PA_P0_AUDITORIA_94_RANKS_CORRECOES_TEST_20261017.zip'
R09=ROOT/'BASELINES'/'PA_P0_R09_CORRIGENDA_TEST_20261018.zip'
EXPECTED={'R05':'6f69fd1ef197851e128c2fc7becbad1f2a14a1438e7bf9ac71742b835f99078e',
 'R06':'6d00306079ac4578d0191d424742a3c746c2a9f73327b9d8563e9267b4f25eb6',
 'R09':'90ceedc8513b09fe6b6938d0c747a4eba77feb854f8834b791791de9fd320d90'}
for key,fp in [('R05',R05),('R06',R06),('R09',R09)]:
 got=hashlib.sha256(fp.read_bytes()).hexdigest()
 if got!=EXPECTED[key]: raise ValueError(key+' baseline corrompido: '+got)
with zipfile.ZipFile(R05) as z:
 path=next(n for n in z.namelist() if n.endswith('corpus_pa_v3.json'))
 source={r['item_id']:r for r in json.loads(z.read(path))['items']}
 assert len(source)==108
with zipfile.ZipFile(R06) as z:
 r06={r['uuid']:r for r in json.loads(z.read('PA_P0_AUDITORIA_20261017/AUDITORIA_INTEGRAL_94.json'))['rows']}
assert len(r06)==94
READBACK_EXTRAS={
 '089c2b324ede837c9e590174fcc33291':('Couraça de Eos','Clarão do Alvorecer',6,'cegueira, CD 12+INT+meio nível; efeito de luz','USO'),
 '56cc2b324ede823586be01440f7a68ef':('Bracelete Calma Elemental','Absorção mágica',10,'15 RDF versus magias elementais, 2 usos por dia','USO'),
 'd6fc2b324ede82e0b26981462a737826':('Relicário dos Segredos','Preservação de Memórias',15,'armazena uma memória ou conhecimento de cada vez','USO'),
 '48cc2b324ede8318a51f81f51bcb1f46':('Bracelete Força Titânio','Resistência Inabalável',6,'10 RDF para golpes/quedas, 2 usos por dia','USO'),
 '48cc2b324ede8318a51f81f51bcb1f46#ACT2':('Bracelete Força Titânio','Energia Vital',6,'3d6 de vida temporária, 1 uso por dia','USO'),
}
ALIAS={
 'Lança Sopro Congelante':('Estilhaço de Gelo',8,'4d6+INT, projéteis de gelo','USO'),
 'SOMBRA SUSSURRANTE':('Invisibilidade',6,'invisível por 6 segundos ou 1 turno','USO'),
 'Bota Caminho Veloz':('Velocidade Sobrenatural',5,'+8m de deslocamento sob ativação','USO'),
 'Traje águia celeste':('Voo da Águia',4,'salto de 4,5m por turno elegível; cobrar POR USO, não custo de manutenção automática','USO_POR_TURNO_ELIGIVEL'),
 'Amuleto Tempo Eterno':('Aceleração Temporal',15,'tempo passa mais rápido para o usuário, máximo 1 vez a cada 2 dias; intensidade ausente','USO'),
 'Braçadeira do Pulmão de Ferro':('Filtro de Partículas',15,'proteção 10min, RD ambiental 20; +6 CON condicional, 1 uso/descanso 8h','USO'),
 'Inscrição da Aurora que Rompe Correntes':('Purificação reativa',60,'Reação; +18 à salvaguarda contra medo/paralisia/selamento etc, preparado até 7 dias','USO'),
 'Lâmina Aurora Boreal': [('Luz da Aurora',6,'cegueira com CD', 'USO'),('Harmonia dos Elementos',7,'+2d6 de dano radiante 1 vez ao dia','USO')],
 'CAJADO VÓRTEX SOMBRIO': [('Força Negra',6,'remove luz local, portador não afetado','USO'),('Gravidade Abissal',14,'campo gravitacional retém inimigos, área/duração sem quantificação','USO')],
}
# Índices apenas investigativos de rank de habilidade; precificação NÃO usa essas hipóteses.
ABILITY_RANK_BAND={
 'Estilhaço de Gelo':'Bronze–Prata',
 'Invisibilidade':'Prata–Ouro',
 'Velocidade Sobrenatural':'Prata–Ouro',
 'Voo da Águia':'Bronze–Prata',
 'Aceleração Temporal':'INDETERMINADO (efeito temporal sem intensidade)',
 'Filtro de Partículas':'Ouro (especialização ambiental)',
 'Purificação reativa':'Lendário (efeito principal do item E0)',
 'Luz da Aurora':'Prata–Ouro',
 'Harmonia dos Elementos':'Bronze–Prata',
 'Força Negra':'Prata–Ouro',
 'Gravidade Abissal':'Ouro–Ouro Negro (área/duração ausentes)',
 'Clarão do Alvorecer':'Prata–Ouro',
 'Absorção mágica':'Prata–Ouro',
 'Preservação de Memórias':'Prata–Ouro',
 'Resistência Inabalável':'Prata–Ouro',
 'Energia Vital':'Bronze–Prata',
}
# Observações com efeitos incompletos são E3, não certificação de rank de habilidade.
rows=[]
def add(uuid, item, power, val, effect, unit, source_method):
 base=source.get(uuid);r=r06.get(uuid)
 doc=(base.get('rank_public') if base else None)
 if doc in ('Sem classificação','None',''):doc=None
 if r and r.get('rank_documental'):doc=r['rank_documental']
 if uuid=='48cc2b324ede8318a51f81f51bcb1f46':doc=None
 if r and r.get('selo_rank','').startswith('E0'):doc=r['rank_documental']
 anal=(r.get('rank_analitico') if r else None) or ''
 if doc in ('Bronze','Prata','Ouro','Ouro Negro','Lendário'):
  item_rank_e0=doc; rank_status='E0_DOCUMENTAL'
 else:item_rank_e0='';rank_status='SEM_RANK_OFICIAL'
 if uuid=='48cc2b324ede8318a51f81f51bcb1f46':url='https://app.notion.com/p/'+uuid
 else:url=base['source_url'] if base else r['url']
 rows.append({'item_uuid':uuid,'item':item,'ability':power,
   'activation_pa':int(val),'charge_unit':unit,'effect_short':effect,
   'item_rank_E0':item_rank_e0,'item_rank_E3_R06':anal,'item_rank_status':rank_status,
   'ability_rank_evidence':'E3' if power!='Purificação reativa' and power!='Filtro de Partículas' else 'E3_PROXIED_BY_PRIMARY_ITEM_EFFECT',
   'ability_rank_preliminary_band':ABILITY_RANK_BAND[power],
   'source_link':url,'source_readback':'NOTION_MESTRE_20261019',
   'source_method':source_method,'is_historical':True,
   'not_an_official_rank':'NÃO CONFERIR ESTRELAS A ITENS; faixa E3 exploratória de efeito'})
for id,obj in source.items():
 name=obj['name']
 if name not in ALIAS:continue
 triples=ALIAS[name]
 if not isinstance(triples,list):triples=[triples]
 expected=[]
 if obj['pa_activation']['value'] is not None: expected=[obj['pa_activation']['value']]
 else: expected=[r['value'] for r in obj.get('pa_activation_occurrences',[])]
 actual=[x[1] for x in triples]
 if expected!=actual:raise ValueError(f'R05 evidencia difere: {name} {actual} {expected}')
 for power,val,effect,unit in triples:add(id,name,power,val,effect,unit,'R05_CORPUS108_REVALIDADO_NOTION')
for key,(item,power,val,effect,unit) in READBACK_EXTRAS.items():
 uuid=key.split('#')[0]
 add(uuid,item,power,val,effect,unit,'NOTION_READBACK_DIRETO_20261019_R06_EXTRA')
assert len(rows)==16,(len(rows),[(x['item'],x['ability']) for x in rows])
assert len({x['item_uuid'] for x in rows})==13
assert len([x for x in rows if x['item_rank_E0']])==2
rows=sorted(rows,key=lambda x:(x['activation_pa'],x['item'],x['ability']))
summary=activation_summary(rows)
summary['base_sha256']=EXPECTED
summary['corpus']='R05 108 entradas, R06 94 auditadas, +1 ficha suplementar: 16 eventos individuais de 13 itens sem duplicar ocorrencias'
summary['known_e0']='Braçadeira Ouro 15 PA uso, Inscrição Lendário 60 PA uso; E0 DO ITEM, NÃO DO RANK DA HABILIDADE'
summary['candidate_implicit_pattern']='6 PA é moda (6/16); defesa especializada, duração e ação podem alterar, não tarifa validada por rank'
summary['status']='TEST_MESTRE_SIDE_NAO_CANONICO_NAO_REPRECIFICA'
summary['rules']={'passive_ability_daily_by_rank':'P_B,P_P,P_O,P_ON,P_L (a pesquisar)',
   'active_ability_daily_by_rank':'floor(P_rank/2)',
   'item_daily_floor':{'Bronze':8,'Prata':11,'Ouro':21,'Ouro Negro':35,'Lendário':90},
   'item_daily_formula':'max(item_floor, pricing_of_magnitude + sum(passive_fee) + sum(active_fee))',
   'activation_per_use':'separate cost, empirically calibrated',
   'separate_ability_vs_item_rank':True}
fields=list(rows[0])
with open(ROOT/'ATIVACOES_HISTORICAS_R21.csv','w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
(ROOT/'SINTese_ATIVACOES_R21.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'n':summary['abilities'],'distinct_items':summary['distinct_items'],'mean':summary['mean_pa'],'median':summary['median_pa'],'modal':summary['mode_pa'],'rank_E0_items':summary['rank_item_explicit_E0_count'],'histogram':summary['histogram']},ensure_ascii=False))
