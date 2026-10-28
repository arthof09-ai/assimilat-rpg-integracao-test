import re,csv,json
from fractions import Fraction
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'publication';p.mkdir(exist_ok=True)
source='https://app.notion.com/p/3f2c2b324ede812d8c21fe3afc4748b7'
B={'Bronze':{'Entrada':(4,6),'Baixa':(7,9),'Média':(10,12),'Alta':(13,15),'Ápice':(16,18)},'Prata':{'Entrada':(14,18),'Baixa':(19,22),'Média':(23,26),'Alta':(27,31),'Ápice':(32,36)},'Ouro':{'Entrada':(22,28),'Baixa':(29,35),'Média':(36,44),'Alta':(45,52),'Ápice':(53,62)},'Ouro Negro':{'Entrada':(38,48),'Baixa':(49,58),'Média':(59,69),'Alta':(70,82),'Ápice':(83,96)},'Lendário':{'Entrada':(58,72),'Baixa':(73,90),'Média':(91,112),'Alta':(113,136),'Ápice':(137,160)}}
def me(s):
 v=Fraction();
 for tok in re.findall(r'[+-]?[^+-]+',s.replace(' ','').replace('−','-')):
  m=re.fullmatch(r'([+-]?)(\d+)d(\d+)',tok)
  v+=(-1 if tok.startswith('-') else 1)*(Fraction(int(m[2])*(int(m[3])+1),2) if m else int(tok.lstrip('+-')))
 return v
def csvw(name,arr):
 with (p/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=arr[0].keys());w.writeheader();w.writerows(arr)
def fmt(q):return str(float(q)) if q.denominator!=1 else str(q.numerator)
# Source: VZ-SANDBOX-CANON v1.0, eight explicit effect-level labels. NOT independent of DMG.
d=[
('VZ01','Serah','Descarga de Vetor','Lendário','Entrada','10d12','10d12','Padrão',45,'alvo único'),
('VZ02','Darek','Corte de Falha','Lendário','Entrada','10d10','10d10+1d8','Padrão',35,'arma 1d8'),
('VZ03','Nym','Fio de Aurora Fria','Lendário','Baixa','12d12','12d12','Padrão',40,'Luz/Gelo'),
('VZ04','Urosh','Sopro de Retorno','Lendário','Entrada','6d12','6d12','Padrão',55,'cone curto, save metade'),
('VZ05','Sel-Myr','Agulha de Memória','Ouro Negro','Baixa','10d10','10d10','Padrão',35,'Spectral'),
('VZ06','Kael','Fratura Fria','Lendário','Entrada','9d12','9d12','Padrão',45,'linha, controle, save metade'),
('VZ07','Rhovan','Corte de Fase','Lendário','Entrada','10d10','10d10+1d6','Padrão',40,'arma 1d6'),
('VZ08','Rhovan','Tempestade de Um Golpe','Lendário','Alta','18d12','18d12+1d6','Completa',90,'burst com arma 1d6')]
rows=[]
for id_,actor,skill,rnk,fip,dice,intr,action,pa,delivery in d:
 lo,hi=B[rnk][fip];raw=me(dice);full=me(intr)
 adjusted=delivery.startswith('cone')
 adjlo=Fraction(lo*55,100) if adjusted else Fraction(lo)
 adjhi=Fraction(hi*70,100) if adjusted else Fraction(hi)
 rows.append(dict(ID=id_,personagem=actor,tecnica=skill,RE_historico=rnk,FIP_historica=fip,formula_literal=dice,chassi_intrinseco_reconciliado=intr,DME_pool=fmt(raw),DME_chassi=fmt(full),faixa_low=lo,faixa_high=hi,pool_dentro=lo<=raw<=hi,chassi_dentro=lo<=full<=hi,ajuste_cone_aplicado=adjusted,faixa_teste_low=fmt(adjlo),faixa_teste_high=fmt(adjhi),dentro_condicional=adjlo<=full<=adjhi,acao=action,custo_pa=pa,entrega=delivery,autoridade='VZ_SANDBOX_v1.0_HISTORICA_NAO_GLOBAL',notion_url=source,edited='2026-10-07T23:57:53.511Z'))
csvw('C29_VZ_8_RE_FIP_EXPLICITOS.csv',rows)
# Effects available in distinct modes are dependent occurrences of a single technique.
modes=[('VZ01','controle','8d12','deslocamento'),('VZ02','controle','6d10+1d8','mobilidade'),('VZ03','controle','9d12','visibilidade'),('VZ04','transformado','7d12','overlay'),('VZ04','transformado_reserva','9d12','consome Reserva'),('VZ05','controle','7d10','concentracao'),('VZ06','transformado','10d12','overlay'),('VZ07','sabotagem','7d10+1d6','sensor')]
csvw('C29_MODOS_DEPENDENTES_8.csv',[dict(effect_id=i,modo=m,formula=f,DME=fmt(me(f)),contrapartida=note,independent_effect=False) for i,m,f,note in modes])
missing=[('Serah','Pulso de Tempestade','7d12','Completa',80),('Nym','Mergulho de Aurora','8d12','Padrão',45),('Kael','Constrição Prismática','7d12','Padrão',55),('Rhovan','Descarga Concentrada','10d12','Padrão',50),('Rhovan','Grito de Pressão','7d12','Completa',70)]
csvw('C29_5_EFEITOS_HERDADOS_SEM_RE.csv',[dict(personagem=a,efeito=b,formula=c,DME=fmt(me(c)),acao=act,PA=pa,RE_individual='PENDENTE_NO_BLOCO',nao_calibra_global=True) for a,b,c,act,pa in missing])
chains=[('Serah','Descarga Direcional','Descarga de Vetor','10d12+10d12','10d12','mesma cadeia'),('Urosh','Onda de Retorno','Sopro de Retorno','7d12+7d12','7d12','mesma cadeia'),('Rhovan','Descarga Concentrada','Corte de Fase','10d10+10d12','10d12','substituicao'),('Kael','Pos-Imagem','Fratura Fria','9d12+9d12','9d12','nao gera ataque'),('Asha','Pulso de Protecao','N/A','7d12','0','nao ofensivo'),('Darek','Espada Juramentada','Corte de Falha','10d10+10d10','10d10','conducao nao gera segundo ataque')]
csvw('C29_6_PROVAS_ANTI_STACK.csv',[dict(personagem=a,fonte=b,relacionado=c,soma_ILICITA=wrong,saida_LEGAL=right,inflacao_DME=fmt(me(wrong)-me(right)),razao=why,observacao='STRESS_DIDATICO_NAO_OBSERVACAO_COMBATE') for a,b,c,wrong,right,why in chains])
phases=['Preflight writer collision e freeze','Descoberta exaustiva','Deduplicacao e genealogia','Extracao forense','Normalizacao matematica','Taxonomia universal','Vinculacao de classificacao','Dossies tipo x rank','Estatistica robusta','Matched pairs entrega','Fronteiras de rank','Biblioteca benchmarks','Auditoria vieses','Candidato DMG v2','Regressao total','Stress adversarial','Playtest humano','Revisao Mestre e promocao','Migracao JIT']
states=['HOLD 4/8','PARTIAL G1 ONLY','PARTIAL G1 ONLY','PARTIAL','PARTIAL MATH','PARTIAL','PARTIAL HISTORIC','PENDING','PENDING','PARTIAL','PENDING','PARTIAL','PARTIAL','NOT_STARTED','NOT_STARTED','PARTIAL TEST','NOT_TESTED','HOLD','NOT_STARTED']
csvw('C29_PLANO_SUPREMO_19_FASES.csv',[dict(fase=f'F{i}',requisito=phases[i],evidencia_local=states[i],gates_formais_novos=0,autoridade='OP-DMG-CORPUS-EMP-01',fonte='https://app.notion.com/p/3f3c2b324ede813e9fa0c87ebdea0b29',NEXT='F0-A5/A6/A7/A8; sem promocao automatica') for i in range(19)])
f0=[('Autorizacao escopo baseline','DOCUMENTADO_HISTORICO'),('7 autoridades RN/RE','DOCUMENTADO_HISTORICO'),('Preregistro','DOCUMENTADO_HISTORICO'),('Protocolo antes/depois','DOCUMENTADO_HISTORICO'),('7 SNAP bytes originais','PARCIAL 7 REFERENCIAS 0 BYTES'),('D0 global mapa de raizes','PARCIAL APENAS G1 411'),('holdout independente','PENDENTE'),('writer e segundo codificador','PENDENTE')]
csvw('C29_F0_OITO_REQUISITOS_OPERACIONAIS.csv',[dict(id=f'F0-A{i+1}',requisito=f0[i][0],estado=f0[i][1],formal_new_pass=False,OBS='8 IDs e nomeacao sao CROSSWALK historico, nao norma nova',source='F0_OITO_REQUISITOS_CROSSWALK.json; COORD_DMG_F0_A5_SNAPSHOT_ATTACHMENT_MANIFEST') for i in range(8)])
att=[('01','DMG_RANK_v11',21413),('02','SISTEMA_COMBATE',20800),('03','CRIACAO_FICHA',30904),('04','CRIACAO_BESTA',23667),('05','SISTEMA_MAGIA',12975),('06','TRANSFORMACAO',24663),('07','ATLAS_PR_ECO',33226)]
csvw('C29_A5_REFERENCIAS_SETE_SEM_BYTES.csv',[dict(item=i,nome=n,bytes_no_upload_original=b,notion_file_ref_encontrada=True,signed_URL_resolved=True,actual_original_bytes_downloaded=False,byte_sha_verified=False,F0_A5_PASS=False,documento_notional='https://app.notion.com/p/3fbc2b324ede813285ebfeaeee964f25') for i,n,b in att])
negative=[('Descarga de Vetor','already documented damage','INELIGIBLE'),('Sopro de Retorno','already documented damage','INELIGIBLE'),('Pulso Protecao Asha','utility explicitly no damage','INELIGIBLE'),('Besta G1 sem formula','RE individual missing','INELIGIBLE'),('Manopla Trovão','already documented extra damage and only item FIP','INELIGIBLE'),('Selo Ultimo Refugio','defensive non damage','INELIGIBLE'),('Cajado Eclipse','numeric damage but no independent RE','INELIGIBLE')]
csvw('C29_PROVA_NEGATIVA_ADMISSAO_V11.csv',[dict(nome=n,motivo=reason,status=st,nao_aplicar_v11_em_original=True,possivel_proposta_TEST=True)for n,reason,st in negative])
assert len(rows)==8 and sum(x['pool_dentro'] for x in rows)==5 and sum(x['chassi_dentro'] for x in rows)==7 and sum(x['dentro_condicional'] for x in rows)==8
assert rows[1]['DME_chassi']=='59.5' and rows[6]['DME_chassi']=='58.5' and rows[3]['faixa_teste_low']=='31.9'
assert all(me(x[3])>=me(x[4]) for x in chains)
res={'count_re_labeled':8,'pool_standard_fit':5,'with_weapon_standard_fit':7,'conditional_delivery_fit':8,'inherited_no_RE':5,'F0_FORMAL':'4/8 HOLD','F0_A5_BYTES':'0/7 HOLD','CANONICAL_DMG_CHANGE':0,'replay_tests':'PASS','source_genealogy':'VZ uses DMG v1.0, so v1.1 crosswalk is NOT independent validation'}
(p/'C29_SUMMARY_METRICS.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
print('C29 Build:',res)
