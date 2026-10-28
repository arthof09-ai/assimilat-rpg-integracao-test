"""Research memo for 12 Mestre Notion sources re-opened in the conversation.
No claim of independently measured accuracy; ranks are proposals, not gold labels.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
corpus=json.loads((ROOT/'CORPUS_12_FONTE_NOTION.json').read_text())
META={
'ARM-01':('Prata','BAIXA','SC-2','Dano +8 somente contra criaturas Grandes ou maiores e anulação situacional de tamanho em manobras. Comparador de escala com bônus situacionais de armas; a fonte não traz rank.','Condicionalidade e qualidade do efeito anti-manobra carecem de comparação de campanha; 8 PA históricos não são âncora para rank.'),
'ARM-02':('Prata','BAIXA','SC-2','Quase invisibilidade ao ativar difere de invisibilidade plena documentada em Sombra Sussurrante; Corte Lunar anti-magia é efeito independente, mais estratégico.','Rank único insuficiente: efeitos separados, duração e potência de Corte Lunar indeterminadas. PA total não calculável.'),
'ARD-01':('Lendário','MEDIA','SC-3','Item tem rank Lendário explícito e amplia mobilidade, DES e acerto; o componente +50 dano de Vento por turno deve ser tratado como recorrente, e Duro de Matar já está incluído.','Rank do item é explícito; não significa que o rank de cada componente seja Lendário. Somar 115 PA de bônus e corrigir os 90 históricos seria ilegal.'),
'ARD-02':('Ouro','BAIXA','SC-2','Invisibilidade por turno e defesa combinada superam camuflagem estreita, comparável qualitativamente a Lâmina Eclipse e Braçadeira defensiva.','Rank do item ausente; PA 34 histórico não calibra rank. Resistências e bônus repetidos exigem mapa de camadas.'),
'ACC-01':('Prata','MEDIA','SC-1','Passos sem Pegadas tem precedente literal na Bota Caminho Veloz e é defesa de rastreamento localizada; efeito ativo +8m e adaptação de terreno merecem ranks separados.','Rank global da Bota não declarado; custo histórico 18 PA/dia e 5 por uso não define novas tarifas.'),
'ACC-02':('Ouro Negro','MEDIA','SC-3','Converter falha DES em sucesso por reação é superior a mero bônus de salvaguarda (+18 na Aurora), porém limitado a três cargas e recarga 1/dia.','Classe do item não declarada; risco estratégico situacional. Duração/ação reação sim, PA por uso não explicitado.'),
'ACC-03':('Ouro','MEDIA','SC-2','Item Ouro explícito; ativação de filtro especializado (10min, 15 PA), mitigação até 20 e +6 CON somente contra partículas não é imunidade geral.','Rank do efeito individual pode ser inferior a Ouro. Não inferir custo diário a partir de 15 PA/ativação.'),
'ART-01':('Lendário','BAIXA','SC-3','Dominação CD45 por 24h e Selo de Dor 25d12/3 usos combinam coerção de criatura e dano alto; abaixo do status cosmológico, mas efeito estratégico.','Rank do artefato e PA não documentados. Propor Lendário para o efeito mais forte sem fingir benchmark exato; requer decisão Mestre SC-3.'),
'ART-02':('Lendário','MEDIA','SC-3','Artefato Lendário explícito com +130 PA reserva, +25 INT, copia magia e nega magia; o sacrifício com multiplicador de dano tem alto impacto.','Rank individual de cada efeito deve ser separado; bônus +130 PA não é PA diário gasto; custos por ativação ausentes.'),
'INS-01':('Lendário','MEDIA','SC-2','Item Lendário explícito; reação contra múltiplos controles com +18 salvaguarda limitada não equivale a sucesso automático da evasão.','Rank de efeito discutível sem ranking independente; 60 PA histórico por ativação não pode ser trocado pelos 30 PA prospectivos de um RE Lendário.'),
'INS-02':('Lendário','MEDIA','SC-3','Fonte declara Lendário, 7 criaturas por 5 turnos em raio de 9m, RD 70 e +8 salvaguardas. A multiplicidade eleva risco tático sem ser fato divino.','PA histórico 65 por ativação preservado. Não usar banda de dano monoalvo; área e stacking RD próprios.'),
'INS-03':('Ouro Negro','BAIXA','SC-3','Classificação pública Ouro Negro explícita; explosão cataclísmica com energia oposta pode ter consequências estratégicas e geometria não definida.','Não há área, dano, salvaguarda, custo, duração ou alvo calibráveis. Proposta de RE Ouro Negro acompanha rank item como HIPÓTESE, não evidência independente; PA total indeterminado.'),
}
for c in corpus['cases']:
    rank,conf,risk,just,limits=META[c['id']]
    c['parecer_semicanonico_r35']={
       'rank_efeito_principal_proposto':rank,'confianca':conf,'risco_sc':risk,
       'fundamentacao':just,'restricoes_de_evidencia':limits,
       'comparadores_genericos':[
          'https://app.notion.com/p/3eec2b324ede81ea8920c52473ecc3ab',
          'https://app.notion.com/p/3f2c2b324ede815498cddb7844245f7e'
       ],
       'notas':'Parecer de Comestre, E3, revisável; não refaz PA histórico nem autoriza uso material.',
       'reuniao_de_evidencias':'Notion Mestre lido nesta execução; resumo manual, não byte-autenticado da plataforma'
    }
    c['source_url']='https://app.notion.com/p/'+c['notion_id']
(ROOT/'BENCHMARK_R35_12_PARECERES.json').write_text(json.dumps(corpus,ensure_ascii=False,indent=2)+'\n')
print('CASOS=',len(corpus['cases']))
for c in corpus['cases']:
    p=c['parecer_semicanonico_r35']
    print(c['id'],c['name'],'->',p['rank_efeito_principal_proposto'],p['confianca'],p['risco_sc'],'PA histórico:',c['daily'],c['activation'])
