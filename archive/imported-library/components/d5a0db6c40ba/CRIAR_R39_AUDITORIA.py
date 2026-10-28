#!/usr/bin/env python3
"""R39: evidence readback audit as an ADDITIVE layer to the existing R34 -> R27 -> R26 flow.
No tariff arithmetic, no classification heuristics, no Notion API, no protected writes.
"""
import json
from pathlib import Path
B=Path(__file__).parent
sources=[
('ATLAS','3eec2b324ede81ea8920c52473ecc3ab','PR-ECO-01 — Atlas Canônico','2026-10-07T23:51:11.338Z','METODO','Efeito antes do rótulo: classificar pelo que realmente faz.'),
('BOTA_RASTRO','3edc2b324ede8135b199fd0cdbb5463c','Bota Caminho Veloz','2026-10-03T19:35:07.748Z','RI_AUSENTE','Enquanto usa as botas, o usuário não deixa rastros, tornando-se impossível de ser seguido.'),
('BOTA_MOV','3edc2b324ede8135b199fd0cdbb5463c','Bota Caminho Veloz','2026-10-03T19:35:07.748Z','RI_AUSENTE','+8m de deslocamento.'),
('SOMBRA','3edc2b324ede812c9b54c261934696e6','Sombra Sussurrante','2026-10-03T19:35:02.305Z','RI_AUSENTE','Fica invisível por 6 segundos ou 1 turno. 6 PA'),
('ANEL','780c2b324ede82f69ae8818e612b7ad2','Anel de Evasão','2026-09-30T04:45:36.972Z','RI_AUSENTE','gastar 1 das cargas dele para obter sucesso no teste de resistência'),
('BRACADEIRA','3f5c2b324ede81eaa080cad94c16dd3b','Braçadeira do Pulmão de Ferro','2026-10-10T18:38:07.195Z','RI_OURO','reduz em até **20 pontos** cada ocorrência de dano ambiental'),
('AURORA','3f5c2b324ede818296fbd64921861d83','Inscrição Aurora que Rompe Correntes','2026-10-10T22:15:26.933Z','RI_LENDARIO','recebe **+18 na salvaguarda** contra o efeito desencadeador'),
('BASTIAO','3f5c2b324ede8130ba03debae3541590','Inscrição do Bastião das Sete Almas','2026-10-10T22:15:26.933Z','RI_LENDARIO','Redução de Dano 70 contra dano físico e mágico por 5 turnos'),
('GRIMORIO','9e9c2b324ede837b96888157b709bb98','Grimório do Arcanista Proibido','2026-10-09T04:37:28.667Z','RI_LENDARIO','Concede +130 de PA para lançar magias'),
('CRISTAL','3edc2b324ede818b9d7ad75d42f2afa2','Cristal de Aurora Boreal','2026-10-06T11:27:35.499Z','RIN_OURO_E2_PS','Emite uma luz calmante que pode dissipar a escuridão e curar a cegueira mágica.'),
('ERVA','3edc2b324ede81deb8cec70bf5ca7150','Erva da Luz do Norte','2026-10-06T04:42:59.190Z','RIN_PRATA_E2_PS','Ilumina o caminho em noites escuras e pode revelar magias ocultas.'),
('VEU','3edc2b324ede813e8efaf8de2050fd9b','Véu de Eärendil','2026-10-03T13:19:33.559Z','RI_AUSENTE','Proteção Luminosa: A armadura emite uma aura suave que protege o usuário contra magias de escuridão.'),
('DMG','3f2c2b324ede815498cddb7844245f7e','DMG-RANK-01 v1.1','2026-10-08T00:01:28.857Z','METODO','**DME = Dano Médio Esperado dos dados + bônus fixo intrínseco do efeito.**')]
registry={'escopo':'Excertos curtos de fontes Notion Mestre reabertas fisicamente em 20/10/2026','aviso':'Estes extratos foram transcritos de readback nesta conversa; isto nao e autenticacao online automatica pelo Python','fontes':{}}
for key,ident,name,dt,rtype,excerpt in sources:
    registry['fontes'][key]={'url':'https://app.notion.com/p/'+ident,'title':name,'last_edited_at_readback':dt,'tipo_rank_rotulado':rtype,'trecho_mecanico':excerpt}
(B/'EVIDENCIAS_MECANICAS_READBACK_R39.json').write_text(json.dumps(registry,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf8')
