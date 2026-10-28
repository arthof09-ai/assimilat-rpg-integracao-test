#!/usr/bin/env python3
"""Reconstruct R23 decision artifact entirely from verified R22 checkpoint; no external writes."""
from __future__ import annotations
import json,hashlib,csv,shutil,datetime,zipfile
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parent
R22=Path('/mnt/data/DMG-F1-R22-RESOLUCAO-NORMATIVA-E-CENA-v02.zip')
R22_FOLDER=Path('/mnt/data/DMG_R22_DECISIVE_EVIDENCE_SANDBOX')

def r22_source_bytes(basename):
    archive=ROOT/'R22_ORIGINAL_READONLY.zip'
    if archive.exists():
        with zipfile.ZipFile(archive) as z:
            return z.read('DMG_R22_DECISIVE_EVIDENCE_SANDBOX/'+basename)
    return (R22_FOLDER/basename).read_bytes()
R22_SHA='b95b51239ee3e74bf96599a7aa119c73ebb7667a2d434f5f61100a02d6a4d972'
DATE='2026-10-09'
CORRELATION='DIR-MESTRE-DMG-R23-DECISION-20261009-001'
SOURCES={
 'IBX76':{'id':'3f4c2b324ede81f1bc88e140c79817da','asof':'2026-10-09T15:30:49.084Z','role':'suplemento R23, Estado NOVA sem ACK'},
 'COMBAT':{'id':'3ebc2b324ede81f1be4be8804ac113c0','asof':'2026-10-07T23:51:04.971Z','role':'Sistema de Combate vigente §§6,11'},
 'MAGIA':{'id':'3ebc2b324ede81f7b343f7270ff91373','asof':'2026-10-07T23:51:07.044Z','role':'Sistema de Magia vigente: magia não critica sem exceção'},
 'DMGRANK':{'id':'3f2c2b324ede815498cddb7844245f7e','asof':'2026-10-08T02:44:17.195Z','role':'DMG-RANK v1.1 §§15,16,21–23,31–32'},
 'LIU':{'id':'0b4c2b324ede837cb6be818dc8e36010','asof':'2026-10-01T09:40:50.721Z','role':'ficha Mestre Liu, Crítico Brutal e Decepadora +18'},
 'DECEP-CATALOGO':{'id':'377c2b324ede82f9b4a181aed3e10f5a','asof':'2026-09-30T04:46:02.488Z','role':'Decepadora +30, espelho Party/Mestre, evidência comparativa NÃO autoridade Liu'},
 'DECEP-GEMEAS':{'id':'302c2b324ede83e8948581b1766d0008','asof':'2026-09-30T04:45:25.697Z','role':'Decepadora +30, outra instância Party/Mestre'},
 'SERPENTE':{'id':'3edc2b324ede811787a0de913622b14d','asof':'2026-10-03T04:47:17.045Z','role':'Adaga da Serpente vigente, 3d12/turno após CON CD25'},
 'SERPENTE-ANTIGA':{'id':'4a9c2b324ede83f78dc581e101e93948','asof':'2026-09-30T04:42:57.423Z','role':'versão histórica excluída, omissão preexistente'},
 'VENENO-OUTRO':{'id':'fcac2b324ede8260a9cf01d141dae809','asof':'2026-09-30T04:45:54.256Z','role':'outro item, 1 minuto não transferível'},
 'VENENO-SUSS':{'id':'85ec2b324ede837f95b6010118e38f5e','asof':'2026-09-30T04:45:06.471Z','role':'outro item, CD80 por turno e acumulação expressa não transferíveis'},
 'MACACO':{'id':'301c2b324ede828caccb813d3979267a','asof':'2026-10-01T18:00:42.589Z','role':'Macaco Rei, Patada 2d6+FOR54'},
}
for s in SOURCES.values():s['url']='https://app.notion.com/p/'+s['id']

def option(id,short,mechanic,risk):return {'option_id':id,'title':short,'mechanic':mechanic,'risk':risk,'status':'PROPOSED_NOT_ADOPTED'}

DECISIONS=[
 dict(id='DEC-B11-A',title='Crítico Brutal — vigência e operador',criterion='B11',original='Ficha Liu: “Seu multiplicador de crítico com armas pesadas aumenta em +2”. Sistema de Combate §6 vigente define dano crítico de forma ADITIVA: dados normais + fixo + máximo dos dados; limita margem do terceiro d6 a +4. Sistema de Magia exclui crítico comum em magias, salvo exceção expressa.',gap='“Multiplicador +2” não tem operador de tradução definido para a fórmula aditiva. Não há prova de que represente margem de crítico nem de que multiplique todos os bônus, rider ou dano elemental.',choices=[
 option('A1','Suspender efeito extra até compatibilização','Preservar a habilidade na ficha, mas sem bônus mecânico de Crítico Brutal em evento calculado pela regra atual. Aplicar apenas o crítico geral enquanto houver HOLD.','Protege contra power creep e conflitos, mas adia benefício legado do personagem.'),
 option('A2','Traduzir +2 para dois máximos extras dos dados elegíveis','Em ataque com arma pesada comprovadamente elegível, além do máximo já somado pelo crítico vigente, somar 2×M (M=máximo dos dados intrínsecos da arma definidos pela fonte); componentes de outros efeitos e riders não entram sem fonte específica.','Preserva identidade de crítico brutal, mas aumenta dano bastante e precisa reavaliação de equilíbrio, do que é “dado da arma” e de efeitos mistos.'),
 option('A3','Retornar ao multiplicador clássico de dano, com escopo fixado','Definir explicitamente fator, operandos, sequência e quais bônus/riders participam; não igualar automaticamente +2 a ×2 ou ×3 sem decisão escrita.','Maior divergência da fórmula atual, grande risco de explosão de dano e incompatibilidade com composição por tags.')],
 recommended='A1 para aplicação conservadora imediata; se o objetivo político-mecânico for preservar a vantagem, A2 é a transposição mais auditável após calibragem, fonte congelada e NAC-NORM. Nenhuma das duas é adotada neste dossiê.',recommendation_option='A1',basis=['COMBAT','MAGIA','LIU','DMGRANK'],worked='EXEMPLO EXCLUSIVAMENTE MATEMÁTICO 1d10+5: crítico geral =1d10+15, DME20,5; A2 =>1d10+35, DME40,5; não são fórmulas reais da arma de Liu. Para magia comum, ambas preservam “sem crítico”.',negative='Converter “+2 multiplicador” automaticamente em +2 margem, em ×2 do total, ou em duplo crítico é não demonstrado.',remaining='Após decisão, provar arma pesada equipada, dados-base/tags, crítico sequencial fonte-gated, bônus e recibo do ataque para certificar B11.'),
 dict(id='DEC-B11-B',title='Decepadora — elegibilidade e +18 no machado',criterion='B11',original='Ficha Mestre de Liu coloca Decepadora no Machado de Guerra Elétrico, mas a descrição literal usa “esta espada”. A ficha Liu estipula +18 cortante no primeiro crítico; outras versões documentadas de Decepadora estipulam +30, mas pertencem a outras instâncias.',gap='Não há decisão expressa se “espada” restringe o aprimoramento do machado, nem se +18 entra como componente adicional após o cálculo de crítico e com que ordem de RD/mitigação.',choices=[
 option('B1','Leitura estrita de arma-espada','O efeito não dispara no machado até correção explícita de fonte/montagem; +18, rechecagem e amputação ficam inaplicáveis ao machado.','Menor improvisação textual; colide com a instalação visível do aprimoramento na ficha Liu.'),
 option('B2','Reconhecer instalação específica de Liu no machado','Autorizar explicitamente a instância montada nesse machado; quando crítico válido, aplicar exatamente +18 dano cortante adicional UMA vez, em componente separado após crítico-base, sujeito às regras de resistência por tag. Não herdar +30 alheio.','Alinha ficha e gameplay mas requer decisão especial para afastar a palavra “espada” e fixar ordem para bypass/mitigação.'),
 option('B3','Uniformizar todos os homônimos em +30','Substituir o +18 da ficha Liu por +30 usado por outros itens; requer alteração formal da ficha/equipamento e regra de migração.','Não recomendado: apaga a identidade de fonte, aplica mudança retroativa não autorizada e viola separação de instâncias.')],
 recommended='B2, CONDICIONADO à confirmação do Mestre de que o aprimoramento estava instalado e apto no machado naquele epoch. Na ausência dessa confirmação, comportar-se como B1 em execução STRICT (fail-closed), sem alterar a ficha.',recommendation_option='B2',basis=['LIU','DECEP-CATALOGO','DECEP-GEMEAS','COMBAT','DMGRANK'],worked='Exemplo matemático 1d10+5, crítico elegível geral: 1d10+15; B2 acrescenta +18 cortante separado => total nominal 1d10+33 antes de RD específica; NÃO soma +30 da outra instância.',negative='Não converter duas descrições homônimas em bônus de +18+30; Decepadora contra OBJETOS tem máximo dos dados, não implica amputação de objeto ou segundo golpe.',remaining='Verificar slot de aprimoramento, status ativo, PA/dia, classe da arma, legalidade do golpe, tag cortante e tabela de resistência do alvo.'),
 dict(id='DEC-B11-C',title='Decepadora — segunda verificação e amputação',criterion='B11',original='Decepadora prevê: em crítico de ataque contra criatura, efeito extra, depois “role os dados de novo”; se também critar, membro pode ser decepado. Sistema de Combate exige 3d6 em ordem e limitação de margem; DMG-RANK §31 distingue amputação (bypass) de dano.',gap='“Dados de novo” não identifica explicitamente se são 3d6 de verificação ou novo ataque/dano; faltam regra de margem da segunda tentativa, momento, defesa/alcance e elegibilidade anatômica.',choices=[
 option('C1','Segundo check independente de crítico, sem novo ataque','Após primeiro crítico legal e efeito autorizado, rolar novamente apenas os 3d6 sequenciais sob a MESMA margem documentada para o gatilho, sem novo hit, ação, gasto de PA ou dano; só então, se houver crítico, verificar alvo anatômico/aplicabilidade do bypass.','Mais reprodutível e conservador quanto ao orçamento de ações; precisa norma clara para margem ao segundo check e alvo imune/inadequado.'),
 option('C2','Novo ataque completo como segunda etapa','Executar segunda jogada de ataque e dano conforme regra explicitamente aprovada, incluindo economia/alcance/defesa e custos; amputar somente após segundo crítico válido.','Muda drasticamente economia e potência, não está apoiado pelo texto literal da habilidade.'),
 option('C3','Sem segundo gatilho mecânico até esclarecimento','Somente o primeiro crítico e bônus legal são computados; amputação fica suspensa.','Evita mutilação não autorizada, mas neutraliza parte da função específica do item.')],
 recommended='C1 quando B11-B reconhecer elegibilidade; caso contrário C3 por falta do primeiro gatilho. Exigir recibos separados `crit_1` e `crit_2`, mesma margem fonte-comprovada, validade de alvo e decisão de consequência do Mestre.',recommendation_option='C1',basis=['COMBAT','LIU','DMGRANK'],worked='Probabilidade apenas teórica, sem bônus de margem: 2/216 = 1/108 para cada check; dois independentes e válidos =1/11664. NÃO é taxa empírica de amputação. Com margem diferente, recalcular; não reutilizar 1/11664.',negative='(6,5,6) não é crítico; segundo check bem-sucedido não cria automaticamente ataque extra nem ultrapassa imunidade/anatomia.',remaining='Receber formato de segunda rolagem aprovado, margem, recibos RNG sequenciais, alvo/biologia e eventos de ação/recursos.'),
 dict(id='DEC-B12-A',title='Serpente — duração e instante do primeiro tick',criterion='B12',original='Adaga da Serpente vigente e sua cópia histórica excluída: se falhar CON CD25, causa 3d12 VENENO por turno; ambas omitem duração, fase do primeiro tick e número máximo de ticks. Dano direto 5d4+5d8+10 e custo35 PA não determinam duração.',gap='Sem evento inicial/expiração temporal, qualquer `3d12×N` com N>1 é hipótese; não tomar emprestado 1 minuto de outra adaga nem CD80 de outra.',choices=[
 option('D1','Dois ticks elegíveis no fim do turno do alvo','Após falha na salvaguarda, aplicar estado sem dano imediato adicional; primeiro 3d12 no final do PRIMEIRO turno do alvo que ocorrer após aplicação, segundo no final do turno seguinte; expirar após 2 oportunidades. Reaplicação só RENOVA duração, nunca soma pilhas.','Simples de auditar, mas adiciona prazo inexistente e pode criar 39 pontos médios condicionais de veneno ao longo de duas janelas.'),
 option('D2','Um único tick no próximo fim de turno','Aplicação após falha e 3d12 apenas ao final do primeiro turno subsequente do alvo, depois expira, salvo reaplicação legal.','Conservador em dano, talvez enfraqueça identidade de veneno “contínuo” da arma.'),
 option('D3','Duração fixa de um minuto com tick por turno','Definir explicitamente quanto tempo/quantas oportunidades representa na campanha e primeiro tick; não importar por analogia a duração de outra adaga.','Pode multiplicar dano de forma relevante e requer converter minuto em turnos sem pressupor equivalência não registrada.')],
 recommended='D2 como ponto de partida conservador: 1 tick tem DME 19,5, enquanto o dano imediato tem DME 45; soma condicional 64,5 (~143,3% do impacto), próxima da referência típica de 110–140% do orçamento citada no DMG-RANK §23, sem que essa referência seja teto obrigatório. D1 resultaria em soma condicional 84 (~186,7%) e requer justificativa explícita de economia, salvaguarda e cura antes de aprovação. Nenhuma proposta está aprovada.',recommendation_option='D2',basis=['SERPENTE','SERPENTE-ANTIGA','DMGRANK','VENENO-OUTRO'],worked='DME impacto 5d4+5d8+10 = 45. Média por tick 3d12 = 19,5. D2: impacto+1 tick = 64,5 (~143,3% do impacto), condicionado a hit, falha CON CD25 e sem RD. D1: impacto+2 ticks=84 (~186,7%). A referência 110–140% do DMG-RANK §23 é orientação de orçamento, não corte automático; duração real continua UNKNOWN.',negative='Não aplicar 3d12 ao atingir E também no mesmo instante/turno por ambiguidade, nem usar 1 minuto como fonte da Serpente.',remaining='Depois da decisão, obter ata de hit real, salvaguarda CON CD25, event_id/turnos e timestamps dos ticks para B12.'),
 dict(id='DEC-B12-B',title='Serpente — remoção, novas salvaguardas e imunidade',criterion='B12',original='Adaga só especifica salvaguarda inicial CON CD25. DMG-RANK §§23/32: reaplicação sem regra específica RENOVA e não empilha indefinidamente; veneno é tag TÓXICA; resistência/imunidade se aplicam apenas por tags expressamente atestadas.',gap='Serpente não informa se há novo save a cada turno, em que fase, que efeito remove o veneno, se cura genérica remove status, nem quais imunidades específicas determinado alvo possui.',choices=[
 option('E1','Somente salvaguarda inicial; remoção explícita ou expiração','Após falha inicial, NÃO conceder novas salvaguardas periódicas automaticamente. Encerrar na duração aprovada ou por habilidade/item cuja fonte declare remover Veneno/estado correspondente; aplicar resistência/imunidade tipada só quando comprovada.','Menos regras inventadas, mas venenamento pode durar prazo inteiro, dependendo de cura explícita existente.'),
 option('E2','Salvaguarda repetida ao fim de cada turno após tick','Após cada tick válido, permitir CON CD25 para encerrar efeito antes de futuros ticks. Falha mantém; sucesso encerra. Aplicar janela e ordenação aprovadas.','Oferece contrajogo, mas introduz novo teste, aumenta carga de evento e requer resolver empate e tempo.'),
 option('E3','Salvaguarda no início do turno ANTES do tick','Após a falha inicial, repetir CON CD25 no início do turno; sucesso evita tick daquele turno.','Reduz dano esperado de forma importante e cria janela não escrita no item; requer testar em balanceamento.')],
 recommended='E1 por preservar estritamente uma salvaguarda textual, com exceções exclusivamente fonte-comprovadas; E2 é alternativa preferível se o Mestre quiser contrajogo periódico. Não presumir remoção por cura de Vida, nem imunidade por espécie.',recommendation_option='E1',basis=['SERPENTE','DMGRANK','VENENO-OUTRO','VENENO-SUSS'],worked='D1+E1 (ambos PROPOSTOS) permitiria no máximo dois ticks após falha inicial e se não houver cura/imunidade documentada. D1+E2 poderia encerrar após o primeiro tick por nova CON CD25. São resultados de políticas ainda NÃO aprovadas.',negative='Não transferir a salvaguarda Fortitude CD80 no final de cada turno da OUTRA Adaga do Sussurro Mortal; nem converter uma imunidade a Veneno em imunidade automática ao dano imediato sem tag.',remaining='Aprovar política de remoção; verificar capacidade específica de antídoto/limpeza, condição do alvo, imunidade tipada, status antes/depois e execuções com recibo.'),
]

# This is a decision-prep, not a policy patch; precisely no state is marked adopted.
for d in DECISIONS:
 d['approval_state']='AWAITING_EXPLICIT_MASTER_DECISION'
 d['adopted']=False
 d['master_choice']=None
 d['master_comment']=None
 d['classification']='PROPOSED_ANALYSIS'
 d['formal_review_required']='NAC-NORM-01, hierarchical check, independent validation, physical readback, NAC-PASS before any official declaration'
 d['source_urls']=[SOURCES[s]['url'] for s in d['basis']]

B15={
 'id':'EVENT-B15-PROSPECTIVE-01','status':'PROSPECTIVE_PLAN_NOT_EXECUTED','criterion':'B15','real_events_recovered':0,
 'requires_actual_source_not_only_example':True,'canonical_example_is_only_rule_fixture':'1d8 cortante + 2d6 Fogo; fraqueza a Fogo acrescenta 3d6 Fogo; componente cortante inalterado',
 'prerequisites':[
 'Autorização da cena pelo Mestre, identificador, data/epoch e escopo; CM-000006 permanece dono do VLAB oficial',
 'Atacante e alvo com IDs físicos, formulário/versão e fontes congeladas (last_edited_at e fingerprints)',
 'Fonte de ataque REAL existente e legal, com dois pools de dano explicitamente tagueados físico e Fogo; o exemplo do Sistema não equivale a item possuído',
 'Fraqueza a Fogo explicitamente fonte-confirmada no alvo, não só inferida de ser criatura de Gelo',
 'Mapa, alcance, linha de visão, turnos, ações, Reação, economia PA e demais pré-condições da ação',
 'Defesa/rolagem de acerto ou resolução mágica prevista na fonte, não impor rolagem de acerto a toda magia',
 'Resistências/RD/RDF/imunidades por tag e ordem de mitigação conforme autoridade vigente',
 'Rolagens físicas 1d8, 2d6, +3d6 e event_id com recibo de cada dado se dados dessa expressão estiverem na ação real',
 'HP/Alma/PA e status completos antes/depois; prova de execução única e replay determinístico',
 'Reabertura independente e aceitação NAC-PASS/contrato integral B15 antes de declarar PASS',
 ],
 'steps':[
 {'phase':'PRE-FLIGHT','action':'Selecionar fonte operacional realmente existente e alvo com Fraqueza a Fogo expressa; congelar versão e tags. Se qualquer elemento faltar, não iniciar combate STRICT.'},
 {'phase':'BEFORE','action':'Persistir fotografia assinada cena/atores, pools separados, mitigação, PA, alcance/LoS, inventário e ações autorizadas.'},
 {'phase':'DECLARE/HIT','action':'Registrar ação escolhida, testes e reação legal, ataque aplicável; confirmar um hit ou efeito válido conforme fonte.'},
 {'phase':'DAMAGE','action':'Registrar cada dado do pool físico e Fogo, +3 dados DO MESMO maior dado Fogo por fraqueza; manter componentes separados para RD/mitigação.'},
 {'phase':'COMMIT','action':'Registrar dano efetivo por componente e Vida/Alma antes/depois, status e custos; não dobrar efeito em retry.'},
 {'phase':'CONTROL','action':'Executar contraprova DOCUMENTAL OU EVENTO TESTE ADICIONAL autorizado: alvo sem fraqueza/ataque sem tag Fogo não recebe +3d6. Contraprova não equivale ao evento positivo.'},
 {'phase':'REPLAY/PASS','action':'Recuperar recibos e fontes independentemente, refazer cálculo, provar igualdade com COMMIT e submeter critério integral e gates ao aceite; não confundir EVENT-B15 com full-fight STRICT.'}
 ],
 'minimal_event_fields':['scene_id','event_id','event_timestamp','authorizing_master_decision_id','source_epoch','actor_id','actor_source_sha256','target_id','target_source_sha256','action_id','action_economy','source_action_url','source_tag_physical','source_tag_fire','target_fire_weakness_source','target_weakness_active','range_los_receipt','hit_save_receipt','reaction_slot_before_after','rolls_physical','rolls_fire_base','rolls_fire_bonus','damage_physical_raw','damage_fire_raw','rd_resistance_by_tag','rounding_and_mitigation_rule','net_damage_physical','net_damage_fire','target_hp_before','target_hp_after','pa_before_after','commit_id','executor_identity','proof_of_no_duplicate','independent_readback','strict_source_gate','nac_pass_verdict'],
 'illustrative_only':{'physical_roll':6,'fire_base_rolls':[4,2],'fire_bonus_rolls':[3,5,1],'pre_weakness_raw':12,'post_weakness_raw':21,'excluded_from_evidence':True},
 'acceptance':'PASS documental de B15 somente após regra, tags, fraqueza efetiva, mitigação e evento real completo passarem readback independente; 1 evento positivo mínimo não é automaticamente luta STRICT de ponta a ponta.',
 'current_strict_fights':'0/2',
}

# Matrix remains strictly status-identical to R22. R23 adds decision/vote and acquisition paths only.
old=json.loads(r22_source_bytes('R22_B01_B18_MATRIX.json').decode('utf8'))
rows=[]
for row in old['rows']:
 c=dict(row)
 c['estado_R22']=row['state_after_R22']
 c['estado_R23']=row['state_after_R22']
 c['predicado_original']=row['original_predicate']
 c['proximo_ato']=row['next_decisive_act']
 c['R23_decision_ids']=([d['id'] for d in DECISIONS if d['criterion']==row['criterion']])
 c['R23_source_delta']='Nenhuma nova fonte de cena ou regra promotora de PASS. Consolidação decisória, sem alterar predicado original.'
 c['R23_acceptance_blocker']=row['R22_minimal_missing']
 if row['criterion']=='B11':
  c['R23_source_delta']='DEC-B11-A/B/C convertidas em opções mutuamente rastreáveis, com recomendação NÃO APROVADA; dados e recibos reais ainda ausentes.'
  c['R23_acceptance_blocker']='Decisão Mestre B11-A/B/C quando aplicável + prova da arma, ataque/crítico serial e gatilhos realmente executados; NAC-NORM/NAC-PASS.'
 elif row['criterion']=='B12':
  c['R23_source_delta']='DEC-B12-A/B propostas: duração/tick e remoção/save, sem reabrir proibição de stacking infinito; comparação legada preservada.'
  c['R23_acceptance_blocker']='Decisão Mestre B12-A/B + evento real de hit e CON CD25, tick/remoção/imunidade fontes e readback; NAC-NORM/NAC-PASS.'
 elif row['criterion']=='B15':
  c['R23_source_delta']='EVENT-B15-PROSPECTIVE-01 plano mínimo de aquisição de um evento REAL, não simulação certificada; regra mista preservada.'
  c['R23_acceptance_blocker']='Evento real positivo com tags, fraqueza, mitigação, roladas e resultado/HP verificados; sem nova regra geral necessária.'
 c['new_certification_R23']=False
 c['provenance_class']='DOCUMENTAL_OR_PROPOSAL__NOT_SCENE'
 rows.append(c)

matrix={'operation':'CM-000001/OP-DMG-CORPUS-EMP-01','version':'R23','source_parent_R22_SHA256':R22_SHA,'denominator':18,'rows':rows,'certified_total':1,'strict_fights':{'completed':0,'required':2},'i0003_original_csv':{'authenticated':0,'expected':9},'notion_writes':0,'proposals_adopted':0,'nac_pass_terminal':'HOLD','ibx76_status':'NOVA_NO_ACK'}
assert len(rows)==18 and len({r['criterion'] for r in rows})==18
assert sum(r['estado_R23']=='PASS_DOCUMENTAL' for r in rows)==1
assert {r['criterion'] for r in rows if r['estado_R23']=='PASS_DOCUMENTAL'}=={'B02'}
assert all(r['estado_R23']==r['state_after_R22'] for r in rows)

scene=json.loads(r22_source_bytes('R22_LIU_SCENE_AND_STRICT_GAPS.json').decode('utf8'))
scene['R23']={
 'real_event_new':0,
 'source_search_behavior':'Somente pista nova e verificável, sem repetir busca ampla por variantes da ficha',
 'liu_ledger':'NO_SIGNED_EVENT_ID_EFFECTIVE_AT_OR_SOURCE_EPOCH',
 'known_facts':{'PA_printed':'170+50−15−30−60−42=73','perdido_printed':'−46 without time or inclusion proof','CA_normal':46,'CA_transformed':60,'DODGE_printed_normal':49,'DODGE_printed_transformed':63},
 'minimum_new_evidence':'Um snapshot de cena datado e assinado: actor source, evento cronológico de PA/−46/equipamento, proficiências, reação e janela, posições, acerto/defesa/dano/vida/Alma e replay',
 'strict_1':'0/1 Liu-Macaco; event receipts missing; engine belongs CM-000006',
 'strict_2':'0/1 second pairing not source-designated and not signed',
 'no_automatic_certification':True
}
index={'file_scope':'R23_FOCUSED_ONLY','R21_R22_denominator':'130 históricos + 111 locais − 43 interseção = 198; 46 formula occurrences/20 sources','original_authentication':'0/9','new_I0003_locator':'NONE','search_escalation_trigger':'Somente 1 novo ID, nome bruto, original arquivo, hash ou manifesto predecessor identificando os nove lotes','existing_derived_not_primary':True,'methods_not_repeated':'R21 47 CSV+114 ZIP; R22 targeted filename checks; R23 não repetiu', 'stop_reason':'no additional physical locator; prioritize normative decision dossier'}

ROOT.mkdir(parents=True,exist_ok=True)
if not (ROOT/'R22_ORIGINAL_READONLY.zip').exists():
    shutil.copyfile(R22,ROOT/'R22_ORIGINAL_READONLY.zip')
(ROOT/'r13_oracle.py').write_bytes(r22_source_bytes('r13_oracle.py'))

def jsondump(filename,obj): (ROOT/filename).write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf8')
jsondump('R23_DECISION_REGISTER.json',{'operation':'CM-000001/OP-DMG-CORPUS-EMP-01','revision':'R23','date':DATE,'correlation':CORRELATION,'proposal_status':'NOT_APPROVED__NO_NORMATIVE_EFFECT','decisions':DECISIONS,'approval_count':0,'source_count':len(SOURCES),'src_source':'R22 and direct R23 readback'})
jsondump('R23_SOURCE_PROVENANCE.json',{'readback':'Notion Mestre-side, as-of source content dates (R23 current fetch)','sources':SOURCES,'authority_warning':'Party copies comparative only; historical deleted page not current authority; references do not imply source epoch of a combat','ibx_ack':'NOT_PROVEN'})
jsondump('R23_B15_EVENT_CONTRACT.json',B15)
jsondump('R23_B01_B18_MATRIX.json',matrix)
jsondump('R23_LIU_STRICT_STATUS.json',scene)
jsondump('R23_I0003_HOLD.json',index)
fieldnames=['criterion','predicado_original','estado_R22','estado_R23','R23_decision_ids','R23_source_delta','R23_acceptance_blocker','new_certification_R23','provenance_class','proximo_ato']
with (ROOT/'R23_B01_B18_MATRIX.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=fieldnames);w.writeheader()
 for r in rows:
  w.writerow({k:'; '.join(r[k]) if isinstance(r.get(k),list) else r.get(k,'') for k in fieldnames})

# Dossier is the only authoritative DELIVERABLE for consideration; accompanying json for audit.
links=lambda *keys:' · '.join(f'[{k}]({SOURCES[k]["url"]})' for k in keys)
text=[]
text.extend([
 '# OP-DMG-CORPUS-EMP-01 | R23 — Dossiê Único de Decisões do Mestre',
 '',
 '**MESTRE-SIDE · NÃO CANÔNICO · SEM ESCOLHAS APROVADAS**',
 f'**Data:** {DATE} · **Correlação:** `{CORRELATION}` · **IBX-76:** NOVA, ACK por instância NÃO VERIFICADO.',
 f'**Pai preservado:** R22 SHA256 `{R22_SHA}`; R01–R21 preservados pela cadeia de ZIPs. Fonte das decisões: documentos vigentes reabertos no Notion e R22 revalidado.',
 '**Contrato científico:** 1/18 (somente B02 documental). STRICT 0/2. I0003 bruto 0/9. NAC-PASS terminal HOLD. Sem escrita em Notion, fichas, Party/O Primeiro, DMG-RANK ou VLAB.',
 '',
 '## Como decidir (sem canonização automática)',
 '',
 'O Mestre pode indicar uma alternativa por identificador A1/A2/A3, B1/B2/B3, C1/C2/C3, D1/D2/D3 e E1/E2/E3, ou determinar texto próprio. **A indicação pelo Mestre continua uma decisão a registrar e validar; ela não significa que este dossiê, por si só, alterou o cânone.** Recomendações abaixo são análises, não votos preenchidos. Após decidir: revisão de precedência NAC-NORM-01, escopo e época, redação numa autoridade existente, reserva legítima de writer, readback, regressão e NAC-PASS antes de promulgar.',
 '',
 '### Folha única de deliberação (DEIXAR EM BRANCO)',
 '',
 '| ID | Tema | Recomendação técnica (não aprovada) | Escolha expressa do Mestre |',
 '|---|---|---|---|',
 ])
for d in DECISIONS:text.append(f'| `{d["id"]}` | {d["title"]} | `{d["recommendation_option"]}` condicional | **PENDENTE: ______** |')
text.extend(['','**Data/escopo/versão autorizados pelo Mestre:** __________________','**Decisões do Mestre (texto adicional):** __________________','**Revisão e registro canônico posterior:** PENDENTES; este arquivo não é ata de aprovação.',''])
for d in DECISIONS:
 text.extend([f'## {d["id"]} — {d["title"]}','',f'**Regra/fonte existente:** {d["original"]}','',f'**Conflito/omissão exata:** {d["gap"]}','',f'**Fontes:** {links(*d["basis"])}','',
  '| Alternativa | Implementação, apenas se aprovada | Consequência/risco |','|---|---|---|'])
 for a in d['choices']:text.append(f'| **{a["option_id"]} — {a["title"]}** | {a["mechanic"]} | {a["risk"]} |')
 text.extend(['',f'**Recomendação fundamentada (PROPOSTA):** {d["recommended"]}','',f'**Impacto numérico condicional:** {d["worked"]}','',f'**Contraexemplo que impede aplicação indevida:** {d["negative"]}','',f'**O que ainda faltará para B{d["criterion"][1:]} receber PASS:** {d["remaining"]}','',f'**Campo de decisão:** `{d["id"]}` = [ PENDENTE ]   **Justificativa/ressalva do Mestre:** __________________',''])
text.extend([
 '## Avaliação conjunta e precedência',
 '',
 'As três decisões B11 interagem: A especifica Crítico Brutal, B identifica elegibilidade e dano extra do aprimoramento, C identifica a segunda verificação e eventual amputação. **Não** se deve multiplicar automaticamente +18 da Decepadora, somar +30 alheio, conferir crítico a magia sem exceção ou transformar segundo check em nova ação. Primeiro verificar fonte legal, depois crítico-base, depois bônus por fonte, mitigação e bypass, com registro de evento independente.',
 '',
 'As duas decisões B12 interagem: D fixa duração e primeiro tick; E fixa remoção/retestes. Reaplicação sem pilhas infinitas e renovação de duração **já é regra vigente** em DMG-RANK §23, portanto não existe sexta decisão sobre acumulação. Veneno só afeta tag venenosa, e cura/imunidade do alvo deve estar fonte-comprovada.',
 '',
 '### Após as decisões: o que PODERÁ e NÃO PODERÁ ser certificado',
 '',
 '| Critério | Efeito da aprovação formal + gates | Prova independente ainda indispensável |',
 '|---|---|---|',
 '| B11 | Regra de crítico e efeitos B11-A/B/C aplicável a novas cenas; testes de conformidade documental | Fonte, equipamento, ataque elegível, 3d6 ordenados, economia, defesa, dano, event_id, mitigação, readback, NAC-PASS |',
 '| B12 | Regra de duração/tick e remoção aplicável à Serpente, preservando não empilhamento padrão | Hit, CON CD25 real, turno, início/fim status, cada tick, cura/removal, imunidade real, readback, NAC-PASS |',
 '| B15 | Não necessita mudança normativa geral | Um evento real com físico+Fogo, fraqueza ativa, mitigação por componente, dados e estados finais; see plano B15 |',
 '| B04/B09 | Cinco decisões não resolvem -46, PA ou reação de Liu | Ledger temporal legítimo da cena, proficiências, reação e geometria |',
 '| B01–B10/B13–B18 restantes | Não se tornam PASS por votação B11/B12 | Cada predicado integral individual da matriz com evidência e aceite |',
 '| 2 STRICT | 0/2 permanecem sem mudança | Dois combates completos e autorizados, com fontes, turnos, replay e NAC-PASS pelo executor competente CM-000006 |',
 '',
 '## B15 — contrato prospectivo, sem combate certificado',
 '',
 'A regra vigente admite exemplo `1d8 cortante + 2d6 Fogo` que contra fraqueza documentada a Fogo se torna `1d8 cortante + 5d6 Fogo`. Médias matemáticas 11,5 e 22; variação +10,5. Isto **não prova ataque real** e não cria uma arma equipada. Para certificar é necessário um **evento real mínimo** com fonte de ataque legal e efetiva, tag Fogo explícita, alvo comprovadamente fraco a Fogo, rolagem, acerto/defesa, mitigação por pool, HP/PA pré/pós e readback independente. Detalhes em `PLANO_EVIDENCIA_REAL_B15_R23.md` e `R23_B15_EVENT_CONTRACT.json`.',
 '',
 '## Fronteiras não resolvidas e não reabertas desnecessariamente',
 '',
 '- **Liu × Macaco Rei:** zero ledger real com `event_id`, PA temporal/“Perdido -46”, proficiências, Reação, geometria, rolagens e estado pré/pós. Valores de ficha não são evento. B04 BLOCKED, B09 PARTIAL. STRICT-1 HOLD.',
 '- **STRICT-2:** segundo par de combatentes nem foi designado com snapshot assinado; HOLD.',
 '- **I0003:** 0/9 CSV originais autenticados; 198 IDs nominalmente reconciliados e 46 fórmulas em 20 páginas. Reabrir apenas se surgir novo identificador/arquivo/manifesto; não repetir busca de 47 CSV/114 ZIP.',
 '- **Matriz:** 1 PASS_DOCUMENTAL B02, 9 PARTIAL, 6 BLOCKED, 2 NOT_TESTED integrais; nenhum novo PASS R23. Não prometer 9/18 antes da prova.',
 '',
 '## Gate e ponto exato de retomada R24',
 '',
 '1. Aguardar ou receber cinco decisões expressas do Mestre, sem marcação implícita de alternativas recomendadas.',
 '2. Avaliar sobreposição entre decisões, dependências e precedência pelo NAC-NORM-01; não sobrescrever versões antigas ou alterar ficha sem autorização específica.',
 '3. Só com escritor exclusivo/fencing, registrar no objeto canônico EXISTENTE, reabrir, testar e aplicar NAC-PASS; sem escritor, preservar ata como minuta Mestre-side, não afirmar publicação.',
 '4. Após regras autorizadas, preparar eventos B11/B12 completos com recibos; B15 começa pelo protocolo prospectivo com ator/alvo/ataque reais e fonte pré-congelada.',
 '5. Para B04/B09, aceitar apenas novo snapshot/event_id de Liu; I0003 somente novo localizador de primário.',
 '',
 '**Status final:** dossiê apresentado para decisão, NÃO APROVADO, NÃO CANONIZADO, NAC-PASS terminal HOLD.',''
])
(ROOT/'DOSSIER_DECISORIO_R23.md').write_text('\n'.join(text),encoding='utf8')

b15doc=[
 '# R23 — Plano prospectivo de evidência EMPÍRICA B15 (não executado)','',
 '**Estado:** PROPOSTO/MESTRE-SIDE. Contrato original B15 `ELEMENTAL_WEAKNESS`. **STRICT** 0/2. Uma ação B15 comprovada não fecha automaticamente luta completa.','',
 '## Premissas oficiais',
 f'- Sistema de Combate vigente: {SOURCES["COMBAT"]["url"]}',
 f'- DMG-RANK v1.1 §21–22 e §32: {SOURCES["DMGRANK"]["url"]}',
 '- Dano físico e elemental devem permanecer em pools separados; bônus de 3 dados incide SOMENTE no maior dado elemental ao qual o alvo tem fraqueza fonte-confirmada. Não aplicar automaticamente a veneno.',
 '- Exemplo canônico é ilustração normativa; é proibido transformá-lo em arma real inventada.',
 '',
 '## Escolha mínima da cena prospectiva',
 '1. Mestre designa uma cena válida para coleta, consentimento/escopo do teste e atores; CM-000006 mantém execução oficial quando autorizada.',
 '2. Fonte física existente do ataque deve discriminar dois pools: cortante/impacto e Fogo com quantidade/tamanho de dados, custos, ação, alcance e elegibilidade. Se nada fonte-comprovado existir, **HOLD**, sem adaptar uma arma à força.',
 '3. Alvo da cena precisa comprovar Fraqueza a Fogo em regra/vigência específica. A palavra “Gelo” na espécie não basta sozinha; vulnerabilidade genérica precisa autoridade de correspondência.',
 '4. Congelar fonte de ataque/target, effective_at, epoch, estado de combate, geometria, fontes da RD, eventual resistência/imunidade, e ação/reação antes de executar.',
 '',
 '## Evento mínimo a recolher, ordenado',
]
for i,x in enumerate(B15['steps'],1):b15doc.append(f'{i}. **{x["phase"]}:** {x["action"]}')
b15doc.extend(['','## Dados necessários para aceitação','','Cada chave abaixo exige valor e fonte, não `UNKNOWN` inventado nem 0 presumido:',''])
for f in B15['minimal_event_fields']:b15doc.append('- `'+f+'`')
b15doc.extend(['','## Ilustração aritmética (SINTÉTICA, NÃO É CENA)','','- Ataque fonte *hipotético* com `1d8 físico` e `2d6 Fogo`, alvo com fraqueza Fogo; rolagens demonstrativas `1d8=6`, `2d6=[4,2]`, `3d6` extras `[3,5,1]`.','- Bruto sem fraqueza: `6 + 4 + 2 = 12`. Bruto com fraqueza: `6 + 4 + 2 + 3 + 5 + 1 = 21`. O aumento `+9` afeta apenas o pool Fogo. Mitigação e resultado líquido desconhecidos: **NÃO APROVADOS** sem fonte da cena.','- Controle negativo: com a MESMA ação e alvo sem Fraqueza Fogo documentada, não são adicionados os três dados. Mesmo personagem elemental sem tag de dano Fogo não ativa bônus.','',
'## Aceite B15 e separação de STRICT','','O B15 recebe PASS somente com fonte concreta + evento real + execução legal + estado final + reprodução independente e NAC-PASS aplicável. Um registro isolado de dano pode suprir B15, mas não pode ser contado como combate STRICT completo. Os dois confrontos STRICT seguem 0/2 até cumprir seus demais 18 predicados e o executor CM-000006 legítimo.','',
'## Falha mínima e retomada','','Se não houver fonte operacional de ataque misto ou alvo com fraqueza expressa, registrar exatamente `MISSING_ATTACK_SOURCE` ou `MISSING_TARGET_WEAKNESS` e não propor combate. Se houver fonte, próximo passo é congelar cena+event_id na autoridade existente, obter execução legal de CM-000006, readback e cálculo por componente.',''])
(ROOT/'PLANO_EVIDENCIA_REAL_B15_R23.md').write_text('\n'.join(b15doc),encoding='utf8')

worksheet=['# R23 — Folha de decisão do Mestre (minuta, não canônica)','',f'Correlação `{CORRELATION}`. Não escrever em ficha, Notion ou Party a partir desta folha sem gates.','','| Decisão | Escolhas disponíveis | Recomendação PROPOSTA | Escolha do Mestre |','|---|---|---|---|']
for d in DECISIONS:worksheet.append(f'| {d["id"]} | '+', '.join(a['option_id'] for a in d['choices'])+f' ou texto próprio | {d["recommendation_option"]} | **________** |')
worksheet.extend(['','**Confirmo essas decisões, com escopo e vigência explicitados por mim:** [  ] SIM  [  ] NÃO  [  ] REVISAR', '**Escopo/epoch/equipamentos afetados:** ____________________________________','**Exceções/ressalvas:** ____________________________________','**Responsável por registrar no cânone após NAC-NORM/NAC-PASS e fencing:** _____________________','**Estado atual:** 0/5 decisões aprovadas; documento pendente de deliberação.',''])
(ROOT/'FOLHA_DECISOES_MESTRE_R23.md').write_text('\n'.join(worksheet),encoding='utf8')

report=f'''# R23 — Relatório objetivo de avanço decisório e continuidade

**Operação:** CM-000001 / OP-DMG-CORPUS-EMP-01. **Estado:** análises entregues, decisão Mestre pendente; writer canônico HOLD.

## Pré-requisitos e provas recuperadas
- R22 ZIP `b95b51239ee3e74bf96599a7aa119c73ebb7667a2d434f5f61100a02d6a4d972`: SHA validado em arquivo real, CRC aprovado, 21 entradas, recuperação limpa R22 e R21 completos (34/34 +36/36 testes históricos, cópia do oráculo R13 original). `R22_ORIGINAL_READONLY.zip` preservado byte-idêntico.
- IBX-76 `https://app.notion.com/p/3f4c2b324ede81f1bc88e140c79817da` aberta e lida de modo consultivo; `Estado NOVA`, Lida por e Concluída por vazios; sem claim de instância, ACK nem writer.
- Notion vigente Sistema de Combate, Sistema de Magia, DMG-RANK, ficha Mestre Liu e Adaga Serpente reabertos. Fontes comparativas Party read-only, sem escrita/replicação Party-facing.

## R22 → R23: delta comprovável
1. Cinco decisões lacunares convertidas em objeto **único** com alternativas e riscos independentes, recomendação explicitamente NÃO promulgada e campo Mestre vazio (`DOSSIER_DECISORIO_R23.md`, DOCX, `R23_DECISION_REGISTER.json`).
2. Dossiê isola interação entre decisões B11-A/B/C e B12-A/B: escopo de item, operador e segunda janela; temporalidade do veneno versus remoção, **sem reabrir stacking infinito**.
3. B15 dispõe de procedimento prospectivo com preflight, evento mínimo, contrato machine-readable, contraprova e gates (`PLANO_EVIDENCIA_REAL_B15_R23.md`); **nenhum evento foi fingido**.
4. Matriz B01–B18 atualizada com dependências pós-decisão, sem alterar estados; duas STRICT 0/2 e I0003 0/9 formalmente congeladas em estado atual.
5. Rejeitadas inferências indevidas: +30 de Decepadora de outro item, operador implícito de Crítico Brutal, tick do veneno sem prazo, B15 positivo sintético como real.

## Estado científico atual
- **1/18 PASS_DOCUMENTAL** apenas B02; **9/18 PARTIAL**, **6/18 BLOCKED**, **2/18 NOT_TESTED integral** (B14/B17 examinados documentalmente).
- **0/2 STRICT**. Liu-Macaco sem scene_id real, epoch, PA/−46 temporal, reação legal, proficiências, posição, dados e recibo de engine. Segundo par sem scene snapshot.
- **0/9** CSV I0003 originais autenticados. Índice derivado 198 nominal, 46 fórmulas em 20 páginas, nenhum aumento de denominador.
- **0/5** decisões adotadas: recomendações são apenas opções para o Mestre; nenhuma alteração canônica em Notion.

## Gates para certificação pós-resposta Mestre
- Aprovação expressa das cinco escolhas NÃO equivale a PASS B11/B12. Primeiro checar precedência e compatibilidade NAC-NORM-01; depois writer/fencing legítimo, atualização no objeto EXISTENTE e readback; então fonte/versão congelada e evento real ou ensaio documental completo exigido pelo predicado, independente auditoria NAC-PASS.
- B15 não exige regra geral nova; exige evento real com componentes documentados, fraqueza de alvo, mitigação, acerto/salvaguarda e HP/PA antes/depois, não full-fight automaticamente.

## Próximo ponto de retomada
**FIRST-PENDING:** receber opções expressas do Mestre (cinco campos ainda em branco), validar colisões/precedência e planejar a redação canônica via escritor legítimo; em paralelo preparar a seleção de uma ação existente de dois pools com tag Fogo e alvo comprovadamente fraco a Fogo para a futura cena B15. Sem escolha Mestre, avançar somente coleta empírica sandbox e preservação, sem inventar vigência.

**NAC-PASS terminal:** HOLD. **Estado de leitura IBX:** sem ACK. **Partição:** 0 writes Party/O Primeiro/VLAB/DMG-RANK/fichas.
'''
(ROOT/'RELATORIO_R23_CONSOLIDADO.md').write_text(report,encoding='utf8')

handoff=f'''# R23 → R24 | Handoff de retomada exata

CM-000001, OP-DMG-CORPUS-EMP-01. Revalidar **R23 ZIP SHA** divulgado pelo checkpoint e manifesto, reabrir IBX-76/IBX-73; não criar outra OP. O pacote contém `R22_ORIGINAL_READONLY.zip` byte-idêntico ao R22 SHA `{R22_SHA}`; sua cadeia preserva R21→R14 e cópia R13.

**Denominadores imutáveis até prova contrária:** B02 1/18 documental, 9 PARTIAL, 6 BLOCKED, B14/B17 NOT_TESTED integral, 0/2 STRICT, 0/9 CSV I0003 originais. 198 IDs derivados e 46 fórmulas/20 fontes permanecem sem soma global.

**PONTO EXATO:** cinco campos de escolha do Mestre **ainda vazios**, ids DEC-B11-A/B/C e DEC-B12-A/B. Inicie lendo `DOSSIER_DECISORIO_R23.md` ou `.docx` + `FOLHA_DECISOES_MESTRE_R23.md`, não recalcule as mesmas matemáticas. Não aplicar recomendação como decisão.

**Após deliberação expressa:** gerar minuta de decisão, verificar conflito normativo e precedência NAC-NORM-01, escopo/epoch/instância, usar somente escritor exclusivo provado para registrar na página EXISTENTE, reabrir e testar, operar NAC-PASS/REPA/NAC-CONT. Sem escritor, manter hold e documentar proposta.

**B11:** fontes Combat/Magia, Liu +18 Decepadora em Machado, outros itens +30 não vinculam, Bruto +2 operador desconhecido. Exigir evento de crítico válido e recibo para PASS.
**B12:** Serpente 3d12/tick depois falha CON25 sem duração; DMG-RANK não stack infinito, renova; recuperar evento e política aprovada de tick/removal. Sem cena ainda sem PASS.
**B15:** usar `PLANO_EVIDENCIA_REAL_B15_R23.md`; escolher fonte real mista+fraqueza expressa, não usar exemplo como item; coletar dano por tag e replay com CM-000006 executor oficial, se autorizado.
**Liu:** evento sem recibos; B04 BLOCKED, B09 PARTIAL; nunca reinterpretar `Perdido -46` sem timeline. **I0003:** sem locator novo, 0/9, não repetir busca 47 CSV/114 ZIP. **STRICT:** 0/2.
**IBX-76:** NOVA / leitura/ACK não demonstrados; nenhum claim de instância, lease, epoch, fencing ou envio bilateral.
'''
(ROOT/'HANDOFF_R23_FAST_RESUME.md').write_text(handoff,encoding='utf8')
jsondump('REGISTRO_LOCAL_R23.json',{'operation':'CM-000001/OP-DMG-CORPUS-EMP-01','scope':'MESTRE_SIDE_LOCAL_SANDBOX_ONLY','R22_parent_sha256':R22_SHA,'record_before':{'B_certified':'1/18','strict':'0/2','I0003':'0/9','decisions_adopted':0},'record_after':{'B_certified':'1/18','strict':'0/2','I0003':'0/9','decisions_adopted':0},'notion_writes':0,'ack_ibx76':'NOT_AUTHENTICATED','safety_hold':True,'next_act':'Mestre choose A/B/C/D/E; then independent normative gate; B15 real event collection'})
(ROOT/'README_R23.md').write_text('# DMG R23 — dossiê decisório MESTRE-SIDE\n\n1. Leia `DOSSIER_DECISORIO_R23.md`/`.docx`, depois `FOLHA_DECISOES_MESTRE_R23.md`.\n2. `R23_DECISION_REGISTER.json` contém decisões PROPOSTAS sem aprovação.\n3. `PLANO_EVIDENCIA_REAL_B15_R23.md` não é relato de execução.\n4. `R23_B01_B18_MATRIX.csv/json` preserva os 18 predicados originais e status.\n5. `R22_ORIGINAL_READONLY.zip` é a cadeia imutável de pesquisa.\n6. Execute `python verify_clean_r23.py caminho_do_zip_R23` para validar pacote e regressões (após versão final empacotada).\n\nSem escrita em Notion/Party/O Primeiro/VLAB/DMG-RANK.\n',encoding='utf8')
print(json.dumps({'R23_BUILD':'PASS','decisions':len(DECISIONS),'matrix':len(rows),'files':[p.name for p in ROOT.iterdir() if p.is_file()]},ensure_ascii=False,indent=2))
