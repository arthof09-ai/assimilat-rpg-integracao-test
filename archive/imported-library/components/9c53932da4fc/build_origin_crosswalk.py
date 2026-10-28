#!/usr/bin/env python3
"""R08 read-only crosswalk. Based on original Notion Party identifiers fetched in this turn.
No Notion writes. A title match is evidence of identity candidate, not a hash/parity proof.
"""
from pathlib import Path
import csv,json,re,unicodedata,collections
ROOT=Path(__file__).resolve().parent
BASE=ROOT/'BASELINE_R07_READONLY/AUDITORIA_94_ORIGINAL_FIRST.csv'
ORIG = [
# Arsenal original / Armas / Aprimoramento
('Mira Apurada','4219c16dd495821d86db0162f009e523'),('Juramento','37a9c16dd4958298b9390193ee91e53a'),('Defensora','d259c16dd495837fa7978187bf53b889'),('Alerta','b459c16dd49582df9da801e978936b7c'),('Viciada','add9c16dd49582789293017f1b876b98'),('Arremessável','f1d9c16dd495834a96088145b45c15b3'),('Relâmpago Avassalador','2d39c16dd4958246b43d01d358ac0050'),('Decepadora','fe29c16dd495833c859201dc5d513c6a'),('Sangramento','2c19c16dd495820199e601f1e1f04aec'),('Vorpal','e3e9c16dd49582a39b140175c8a75c3c'),('Arma Mortal','c5a9c16dd495837caa12013edad447de'),('Impacto Estonteante','f449c16dd4958343ba298144ff57dd88'),('Trespassar','d949c16dd49582fc9c3481e31e5c4656'),('Infusão Mágica','da99c16dd495821e801e0118f70e8aa8'),('Exterminadora de Monstros','0f49c16dd49582b4acea0111c17e1b2a'),('Foco Arcano','84a9c16dd495835d8ebe011eef65e6c2'),('Escudo Apanhador de Flechas','5e69c16dd4958220a997010131fdbc11'),('Escudo de Atração de Projéteis','c0b9c16dd495837d9db90138b1fd08b0'),('Escudo de Proteção Contra Magia','af49c16dd4958352838001d19a8afd30'),('Escudo Sentinela','9ae9c16dd4958204bc7a81fcf6a2332b'),('Olhos nas Costas','31a9c16dd49582438d06013aed618408'),('Alcance Aprimorado','67d9c16dd495824aae76017b811f7976'),('Eficiência Mágica','cfd9c16dd49582849893010fc4600c17'),('Magias Devastadoras','5a29c16dd49582dab7b5017eaab320e1'),('Magia Aprimorada','3a39c16dd49582c9b99c81b800af127d'),('Força Bruta','3879c16dd49583989d4f812fc8383079'),('Sai da Frente','a419c16dd49583289c8f01a12cb862b5'),('Potencializar Magia','6d79c16dd49583a4a1b3011a79fd5f5a'),('Estender Magia','d7c9c16dd49582b3bd6d01bb3155c63f'),('Magia Implacável','cf19c16dd49583ec82ac01d43e071b18'),
# Armadura original / Aprimoramentos
('Armadura Anã','cde9c16dd495838f8b708160c9113a15'),('Adamante','7759c16dd49583c0a8ae01efcc5121c6'),('Invulnerabilidade','3bb9c16dd4958243bdad01a3532e46fd'),('Mitral','b2d9c16dd495834e8e1401bb22137dc4'),('Resistência','bd69c16dd49582bd876e8138f3d9a917'),('Marítima','29f9c16dd4958230bd09816d3123d9d4'),('Duro de Matar','c7c9c16dd49583389a550189453e5feb'),('Mobilidade','fc89c16dd4958243ba2e81abebd42145'),('Olhos nas Costas Armadura','09a9c16dd49583bfa827817c8f26e058'),('Vitalidade','e119c16dd4958324b79d01ed56f4f67a'),
# Party artefatos/aquelas fichas do catálogo
('Anel de Evasão','29b9c16dd49583379a8b81875cacf8ed'),('Anel de Queda Suave','e2e9c16dd4958208b38d81adc8a26548'),('Anel de Andar na Água','4599c16dd49583a78c4c0199dc9fea5f'),('Anel de Cativar Criaturas','98e9c16dd495826c9cd3011e70f92233'),('Anel de Escudo Mental','0979c16dd4958383b72e814413eff7ff'),('Anel de Resistência','7b19c16dd4958348857981c91b81a8fc'),('Chifre do Alarme Silencioso','e7f9c16dd495828ba44981b69ef3fe02'),('Diamante de Sangue','5339c16dd49583d1ace8812a278e2db9'),('Máscara do Dragão Negro','4b79c16dd495838fb8c2015fb6537358'),('Olho de Ersatz','c489c16dd4958377b1930130f22d485d'),('Óculos Noturnos S.P','8279c16dd495829b8d5281ccb4d4883b'),('Amuleto da Dor','29e9c16dd49582f6a7a281617dd427cd'),('Tiara Intelectual','aa09c16dd49583ce8dd601dbb8f9e548'),('Talismã Pura Bondade','7e19c16dd49582f59a69819fe207c957'),('Talismã Mal Supremo','e249c16dd4958262a061017e434bf06b'),('Sucesso Atrai Sucesso','62c9c16dd4958279a7d601e826798fd7'),('Amuleto dos Ventos','9069c16dd49583a0985301d0010791c0'),('Olho Mágico','de79c16dd49583158cbb0116a45de7fa'),
# Party roupas originais
('Botas de Pegadas Falsas','2aa9c16dd49583fca187813959b63396'),('Botas do Inverno','d5b9c16dd49582449ab081b2b42e209b'),('Manto da Arachnida','0349c16dd4958259972a0188708f22c2'),('Manto de Elvenkind','4649c16dd495828eae040132da5e5096'),('Manto da Moda','f8e9c16dd49582cb833f81548014479d'),('Manto Resistência Mágica','3bc9c16dd49582908baf010f5075e54e'),('Manto de Proteção','1199c16dd49582d28c82816f25f7e2fc'),('Manto Olhar Verdadeiro','83f9c16dd4958224873101ec3a3eb4e1'),
# Outros nomes originais e inventários identificados e lidos
('Adaga de Envenenamento Mortal','a939c16dd49583df91d8019e9ae43819'),('Arco Justiça Celestial','9899c16dd4958254921601de754d9b2c'),('Manopla de Combatente 2.0 S.P','65d9c16dd495821c8dde0192536ed33a'),('Bastião de Virilia','1b89c16dd495825db9990116e44e2361'),('Couraça de Eos','aa39c16dd49582c7b8de814ea732762b'),('Manto do Arquimago','2409c16dd49583f798e2014bf06d0b91'),('Arma Inteligente','6a89c16dd4958226bcd681d8ddb86160'),('Opala de Inscrição Ild','1e79c16dd495827ba00081b3d2bab5e4'),('Amplificador de Atributo','2229c16dd49582c0a6d301aa252d29e7'),('(AI) Amuleto de Inteligência','8009c16dd49583869bc401883dee2d79'),('Relicário dos Segredos','8919c16dd495838a808d01a30c051575'),('Anel Dimensional Vinculado V²','6bd9c16dd4958267828001061a697d32'),('Adaga Mortal Jaku','c2a9c16dd495823e952001e9677a3535'),('Bracelete da Calma','f559c16dd49583c4b68281c135fe79e5'),('Armadura de Zephyr (L)','5c09c16dd49582d286d90111d663dd4c'),('CAJADO VÓRTEX SOMBRIO','b659c16dd49583aa816301574596bc0e'),('Lâmina Aurora Boreal','cec9c16dd4958223852c81467b4c38e7')]
# Items not re-read this turn are *not* marked verified simply by being present in the index.
ORIGINAL_READBACK_IDS=set(x[1] for x in ORIG) - {'bd69c16dd49582bd876e8138f3d9a917'} # read but no numeric, not part of 80
# Manual explicit variants because title differs.
aliases={'olhos nas costas arma':'Olhos nas Costas','olhos nas costas':'Olhos nas Costas Armadura',
    'adaga mortal jaku':'Adaga Mortal Jaku','bracelete da calma':'Bracelete da Calma',
    'anel dimensional vinculado v2':'Anel Dimensional Vinculado V²',
    'manto olhar verdadeiro':'Manto Olhar Verdadeiro'}
def norm(s):
 s=unicodedata.normalize('NFKD',s.casefold())
 s=''.join(c for c in s if not unicodedata.combining(c))
 s=s.replace('²','2');s=re.sub(r'\([^)]*\)',' ',s)
 s=re.sub(r'[^a-z0-9]+',' ',s)
 return ' '.join(s.split())
from collections import defaultdict
index=defaultdict(list)
for n,u in ORIG:index[norm(n)].append((n,u))
with BASE.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f,delimiter=';'))
assert len(rows)==94
out=[]
for row in rows:
 o={'uuid_espelho':row['uuid'],'item':row['item'],'origem':row['fonte'],'PA_historico':row['pa_dia_historico'],'URL_espelho_ou_mestre':row['url_espelho']}
 if row['fonte']=='PARTY_MESTRE_ESPELHO':
  key=norm(row['item']);key=norm(aliases.get(key,key));matches=index.get(key,[])
  # Duas habilidades com mesmo titulo, mas linhagens e categorias originais distintas.
  if row['item'].endswith('(arma)'):matches=index.get(norm('Olhos nas Costas'),[])
  elif row['item']=='Olhos nas Costas':matches=index.get(norm('Olhos nas Costas Armadura'),[])
  if len(matches)!=1 and 'olhos nas costas' in key:
   matches=[(n,u) for n,u in ORIG if norm(n)==norm('Olhos nas Costas Armadura' if 'arma' not in key else 'Olhos nas Costas')]
  if len(matches)==1:
   n,u=matches[0]
   o.update(original_party_uuid=u,original_party_url=f'https://app.notion.com/p/{u}',status_original='READBACK_ORIGINAL_P0_R08' if u in ORIGINAL_READBACK_IDS else 'ORIGINAL_INDEX_MATCH_ONLY',match_method='NORMALIZED_TITLE_OR_ALIASED',original_title=n)
  else:
   o.update(original_party_uuid='',original_party_url=row['original_party_url'],status_original='UNMATCHED_NEEDS_DIRECT_RECONCILIATION',match_method='NO_UNIQUE_MATCH',original_title='')
 else:
  o.update(original_party_uuid='',original_party_url='',status_original='MASTER_READONLY_BASELINE',match_method='N/A',original_title='')
 out.append(o)
ct=collections.Counter(x['status_original'] for x in out)
(ROOT/'ORIGINAIS_CROSSWALK_R08.json').write_text(json.dumps({'as_of':'2026-10-18','sources':'notion_party_direct_fetched_this_turn','denominator':94,'by_status':dict(ct),'rows':out},ensure_ascii=False,indent=2),encoding='utf-8')
with (ROOT/'ORIGINAIS_CROSSWALK_R08.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=out[0].keys(),delimiter=';');w.writeheader();w.writerows(out)
print(json.dumps({'status':dict(ct),'unmatched':[(x['item'],x['uuid_espelho']) for x in out if x['status_original']=='UNMATCHED_NEEDS_DIRECT_RECONCILIATION'],'readback_count':sum(x['status_original']=='READBACK_ORIGINAL_P0_R08' for x in out)},ensure_ascii=False,indent=2))
