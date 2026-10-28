from artifact_tool import Workbook,SpreadsheetFile
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
rows=list(csv.DictReader((ROOT/'ATIVACOES_HISTORICAS_R21.csv').open(encoding='utf-8-sig',newline='')))
stats=json.loads((ROOT/'SINTese_ATIVACOES_R21.json').read_text(encoding='utf8'))
OUTPUT=ROOT/'PA_R21_HABILIDADES_ATIVAS_PASSIVAS_TEST_20261019.xlsx'
wb=Workbook.create()
summary=wb.worksheets.add('Regras R21')
obs=wb.worksheets.add('Ativações 16')
dashboard=wb.worksheets.add('Estatísticas')
model=wb.worksheets.add('Simulador novo item')
notes=wb.worksheets.add('Método e fontes')
NAVY='#16283B';TEAL='#126E75';WHITE='#FFFFFF';PALE='#E7F2F3';LIGHT='#F1F5F9';AMBER='#FCF4DA'

def hdr(sh, addr):
    sh.get_range(addr).format={'fill':NAVY,'font':{'bold':True,'color':WHITE},'row_height':30}
def banner(sh,range_,title):
    sh.merge_cells(range_)
    cell=range_.split(':')[0]
    sh.get_range(cell).values=[[title]]
    sh.get_range(range_).format={'fill':NAVY,'font':{'bold':True,'color':WHITE,'size':16},'row_height':37}

banner(summary,'A1:E1','R21 · TARIFAS DE HABILIDADES — NOVOS ITENS · TEST')
summary.merge_cells('A2:E2');summary.get_range('A2').values=[['Pisos oficiais definidos; coluna C = tarifas passivas por rank AINDA NÃO DEFINIDAS. Preencha somente hipóteses em TEST.']]
summary.get_range('A3:E3').values=[['Rank do item / habilidade','Piso ITEM PA/dia','Passiva PA/dia — X (EDITAR)','Ativa PA/dia = piso(X/2)','Estado da hipótese']];hdr(summary,'A3:E3')
ranks=[('Bronze',8),('Prata',11),('Ouro',21),('Ouro Negro',35),('Lendário',90)]
summary.get_range('A4:C8').values=[[r,p,None] for r,p in ranks]
for i in range(4,9):
    summary.get_range(f'D{i}').formulas=[[f'=IF(ISNUMBER(C{i}),ROUNDDOWN(C{i}/2,0),"PENDENTE")']]
    summary.get_range(f'E{i}').formulas=[[f'=IF(ISNUMBER(C{i}),"CANDIDATO TEST","PENDENTE")']]
summary.get_range('C4:C8').format.fill=AMBER
summary.get_range('A10:E10').values=[['REGRA CONFIRMADA: ativa = piso(passiva/2) de seu PRÓPRIO rank; custo por ativação é adicional.',None,None,None,None]]
summary.get_range('A11:E11').values=[['PROSPECTIVO: valores anteriores preservados; habilidades são CLASSIFICADAS pelo Atlas antes do cálculo.',None,None,None,None]]
summary.get_range('A12:E12').values=[['CUSTO DIÁRIO DO ITEM = máx(piso do RI, tarifas de magnitude + tarifas base de passivas + tarifas base de ativas).',None,None,None,None]]
summary.get_range('A13:E13').values=[['INTERPRETAÇÃO TEST: base da habilidade + magnitude são camadas distintas; não contar repetição textual do mesmo efeito.',None,None,None,None]]
summary.get_range('A3:E3').format.wrap_text=True
summary.get_range('A:A').format.column_width=31
summary.get_range('B:B').format.column_width=23
summary.get_range('C:C').format.column_width=35
summary.get_range('D:D').format.column_width=31
summary.get_range('E:E').format.column_width=24
summary.freeze_panes.freeze_rows(3)

banner(obs,'A1:J1','CORPUS: 16 ATIVAÇÕES COM PA/USO EXPRESSO · 13 ITENS')
colheads=['Item','Habilidade ativa','PA por ativação','Tipo unidade','RI oficial E0','RI provisório E3 (item)','Efeito (faixa E3 preliminar)','Resumo mecânico','Origem de leitura','URL fonte']
obs.get_range('A3:J3').values=[colheads];hdr(obs,'A3:J3')
mat=[]
for r in rows:
    mat.append([r['item'],r['ability'],int(r['activation_pa']),r['charge_unit'],r['item_rank_E0'] or 'Sem rank E0',
       r['item_rank_E3_R06'] or '—',r['ability_rank_preliminary_band'],r['effect_short'],r['source_method'],r['source_link']])
obs.get_range('A4:J19').values=mat
for col,w in [('A',27),('B',27),('C',17),('D',24),('E',19),('F',23),('G',37),('H',51),('I',35),('J',55)]:obs.get_range(f'{col}:{col}').format.column_width=w
obs.get_range('A4:J19').format.row_height=24
obs.get_range('G4:J19').format.wrap_text=True
obs.freeze_panes.freeze_rows(3)

banner(dashboard,'A1:E1','PA/USO — DISTRIBUIÇÃO OBSERVADA (NÃO É TABELA NORMATIVA)')
dashboard.get_range('A3:B10').values=[
 ['Métrica','Valor'],['Habilidades com custo explícito',stats['abilities']],['Itens independentes',stats['distinct_items']],
 ['Custo mínimo',stats['min_pa']],['Mediana',stats['median_pa']],['Média',stats['mean_pa']],
 ['Moda',stats['mode_pa'][0]],['Custo máximo',stats['max_pa']]]
hdr(dashboard,'A3:B3')
dashboard.get_range('D3:E7').values=[['Subcoorte SEM 60 PA','Valor'],['N',stats['without_60']['n']],
 ['Menor',stats['without_60']['min_pa']],['Mediana',stats['without_60']['median_pa']],['Média',stats['without_60']['mean_pa']]];hdr(dashboard,'D3:E3')
dashboard.get_range('A13:B13').values=[['PA/uso','N habilidades']];hdr(dashboard,'A13:B13')
hist=[(int(k),v) for k,v in stats['histogram'].items()]
dashboard.get_range(f'A14:B{13+len(hist)}').values=[[cost,n] for cost,n in hist]
dashboard.get_range('D10:E14').values=[['Confiabilidade de rank','N'],['Rank do ITEM E0 (não da habilidade)',2],['Rank da HABILIDADE E0',0],['Item sem RI explícito E0',14],['Observações são históricas','Sem correção']];hdr(dashboard,'D10:E10')
dashboard.get_range('A25:E25').values=[['OBS: 6 PA é moda (6/16), mas não confirma tarifa universal nem por rank.',None,None,None,None]]
dashboard.get_range('A26:E26').values=[['Somente Ouro E0 (15 PA/uso) e Lendário E0 (60 PA/uso) têm RI documental na amostra; RE da habilidade é independente.',None,None,None,None]]
dashboard.get_range('A:A').format.column_width=38
dashboard.get_range('B:B').format.column_width=21
dashboard.get_range('C:C').format.column_width=4
dashboard.get_range('D:D').format.column_width=48
dashboard.get_range('E:E').format.column_width=24
try:
    chart=dashboard.charts.add('bar',dashboard.get_range(f'A13:B{13+len(hist)}'))
    chart.title_text='Ocorrências por custo de ativação'
    chart.set_position('G3','O19')
except Exception as e:
    print('Chart opcional indisponível:',str(e)[:180])

banner(model,'A1:H1','SIMULADOR · NOVO ITEM (TARIFAS X EM ABERTO)')
model.get_range('A3:B6').values=[['Rank do item','Ouro'],['Custo de efeitos numéricos conhecidos (PA/dia)',15],
 ['Piso diário do item (PA/dia)',None],['Estado dos valores-base','Preencher coluna C em Regras R21']]
model.get_range('B5').formulas=[['=VLOOKUP(B3,\'Regras R21\'!$A$4:$B$8,2,FALSE)']]
model.get_range('A9:H9').values=[['ID','Habilidade','Rank da habilidade','Tipo','Base PA/dia','PA/uso','Usos hoje','Ativações PA hoje']];hdr(model,'A9:H9')
model.get_range('A10:D11').values=[['P1','Exemplo passiva','Ouro','PASSIVA'],['A1','Exemplo ativa','Ouro','ATIVA']]
model.get_range('F10:G11').values=[[None,0],[6,2]]
for i in range(10,18):
    model.get_range(f'E{i}').formulas=[[f'=IF(C{i}="","",IFERROR(IF(VLOOKUP(C{i},\'Regras R21\'!$A$4:$E$8,5,FALSE)="PENDENTE","PENDENTE",IF(D{i}="PASSIVA",VLOOKUP(C{i},\'Regras R21\'!$A$4:$E$8,3,FALSE),VLOOKUP(C{i},\'Regras R21\'!$A$4:$E$8,4,FALSE))),"RANK INVÁLIDO"))']]
    model.get_range(f'H{i}').formulas=[[f'=IF(C{i}="","",IF(D{i}="ATIVA",IF(F{i}="","PENDENTE",F{i}*G{i}),0))']]
model.get_range('A20:B27').values=[['CÁLCULO','Resultado'],['Piso conhecido',None],['Magnitude sem tarifas habilidade',None],
 ['Subtotal tarifas diárias habilidades',None],['Subtotal efeito + habilidade',None],['PA por dia final',None],
 ['PA ativado hoje',None],['PA total hoje',None]]
hdr(model,'A20:B20')
model.get_range('B21').formulas=[['=B5']]
model.get_range('B22').formulas=[['=B4']]
model.get_range('B23').formulas=[['=IF(COUNTIF(E10:E17,"PENDENTE")>0,"PENDENTE",SUM(E10:E17))']]
model.get_range('B24').formulas=[['=IF(ISNUMBER(B23),B22+B23,"PENDENTE")']]
model.get_range('B25').formulas=[['=IF(ISNUMBER(B24),MAX(B21,B24),"PENDENTE")']]
model.get_range('B26').formulas=[['=IF(COUNTIF(H10:H17,"PENDENTE")>0,"PENDENTE",SUM(H10:H17))']]
model.get_range('B27').formulas=[['=IF(AND(ISNUMBER(B25),ISNUMBER(B26)),B25+B26,"PENDENTE")']]
model.get_range('D21:H21').values=[['ATENÇÃO: resultado PENDENTE até X por rank ser fundamentado / preenchido.',None,None,None,None]]
model.get_range('D22:H22').values=[['Não confundir rank da habilidade com rank do item; RE/RI via Atlas antes do PA.',None,None,None,None]]
model.get_range('D23:H23').values=[['Não somar ativação de uma habilidade que não foi usada hoje.',None,None,None,None]]
model.get_range('D24:H24').values=[['Em dúvida sobre PA/uso, deixe vazio: motor indica PENDENTE.',None,None,None,None]]
model.get_range('B3:B4').format.fill=AMBER
model.get_range('A10:D17').format.fill=LIGHT
model.get_range('F10:G17').format.fill=AMBER
for col,w in [('A',42),('B',24),('C',24),('D',18),('E',20),('F',15),('G',14),('H',23)]:model.get_range(f'{col}:{col}').format.column_width=w
model.freeze_panes.freeze_rows(9)

banner(notes,'A1:D1','PROVENIÊNCIA · ESCOPO · GATES')
notesdata=[
 ['Estado','TEST LOCAL / Mestre-side. Produção HOLD. Sem alteração de fichas ou PA histórico.'],
 ['Decisão do Mestre','Piso ITEM por rank (8/11/21/35/90); habilidade PASSIVA X por rank; ATIVA floor(X/2) por dia + PA por uso.'],
 ['Desconhecido','Valores X por rank; curva de custo por ativação; individualização E0 da classificação de cada habilidade.'],
 ['Rank da habilidade','PR-ECO-01 Anexo A (Atlas canônico) exige classificar efeito independente de preço/PA e do RI.'],
 ['Atlas canônico','https://app.notion.com/p/3eec2b324ede81ea8920c52473ecc3ab'],
 ['Operação vinculada','https://app.notion.com/p/3f1c2b324ede81d7aa79c83106240516'],
 ['Corpus original','R05 108 originais; R06 94 auditorias; R09 94 reconciliados; R20 49 observações de bônus. Corpus não somado como universos independentes.'],
 ['16 ativações','13 itens distintos reabertos em Notion Mestre em 19/10/2026; 2 RI E0, 14 custos com RI não documental.'],
 ['Party','Três fichas adicionais estão no espelho Mestre: pesquisa somente; Party original não foi escrito ou sincronizado.'],
 ['Controles','Ativação/unidade por uso vs por turno elegível; nome da habilidade, efeito mecânico, custo separado; sem rank pela quantidade de PA.'],
 ['Comparação entre efeitos','Mobilidade +8m/5 PA e salto 4.5m/4 PA; cegueira 6 PA (duas fontes); RDF 10/6, 15/10, especial 20/15; não provar causalidade.'],
 ['Modelo aditivo (TEST)','Tarifa-base por habilidade + magnitude já tarifada pode conviver, mas mesmo bônus textual duplicado não deve ser somado novamente.'],
 ['Incerteza','X vazio é PENDENTE, jamais zero; mínimos antigos do corpus não mudam novos pisos; modo ativável mantém piso.'],
 ['NAC','Documentação normativo-operacional do objetivo não foi escrita no Notion; writer, lease e fencing não reivindicados.'],
]
notes.get_range(f'A3:B{2+len(notesdata)}').values=notesdata
hdr(notes,'A3:B3')
notes.get_range('A:A').format.column_width=36
notes.get_range('B:B').format.column_width=118
notes.get_range(f'B4:B{2+len(notesdata)}').format.wrap_text=True
notes.get_range(f'A3:B{2+len(notesdata)}').format.row_height=27

# Verify key outputs before export
print('INSPECT summary:',wb.inspect({'kind':'table','range':'Regras R21!A3:E9','include':'values,formulas','table_max_rows':7,'table_max_cols':5}).ndjson[:2400])
print('INSPECT simulator:',wb.inspect({'kind':'table','range':'Simulador novo item!A20:B27','include':'values,formulas','table_max_rows':8,'table_max_cols':2}).ndjson[:2200])
errs=wb.inspect({'kind':'match','search_term':'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A','options':{'use_regex':True,'max_results':60},'summary':'formula errors R21'})
print('ERROR SCAN:',errs.ndjson[:900])
SpreadsheetFile.export_xlsx(wb).save(str(OUTPUT))
print('EXPORTED:',OUTPUT,OUTPUT.stat().st_size)
