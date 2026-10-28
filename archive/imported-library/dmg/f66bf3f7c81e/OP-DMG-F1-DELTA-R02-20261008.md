# OP-DMG-CORPUS-EMP-01 — Checkpoint científico incremental R02
**Data:** 08/10/2026. **Superfície:** Projeto Comestre, MESTRE-SIDE. **Baseline:** DMG-RANK-01 v1.1 permanece oficial e intacta.

## 1. Estado antes
IBX-28 continha 239 pais / 412 ponteiros estruturais do predecessor I0003, 104 subfichas locais distintas (48 Gelo + 43 Fogo diretas + 13 referências cruzadas), 49 expressões ofensivas de 34 fichas, 69 conflitos textuais pelo parser v0.2, 6 indeterminados. Conjunto original de 149 IDs não recuperado em bytes. Fogo: 44 ponteiros de predecessor versus 43 diretos observados. Não existe lease/epoch transferido para escrita científica.

## 2. Estado depois — leitura física desta execução
- Fontes focalizadas reabertas no Notion: 13 IDs distintos (7 não constavam dos 104 anteriores; INTERSEÇÃO com 149 originais = INDETERMINADA). Seis já estavam no corpus 104. Destes 13, 32 efeitos/ações observados no lote focal, dos quais 20 portam pools de dados numéricos; NÃO somar como novos efeitos independentes aos 49 anteriores.
- Fechamento metodológico 71×69: 69 conflitos de rank textual que o parser reconhece + 2 ocorrências de corpo 'Épico' fora dos 25 ranks oficiais = 71 anomalias de rank, sob uma taxonomia única. Restam 24 concordâncias completas, 5 estrelas ausentes e 4 indeterminados (incluindo página só com imagem). **Nenhum dos 71 é erro canônico adjudicado por esta análise.**
- 49 fórmulas de 34 páginas anteriores reduzem-se a 19 strings literais normalizadas distintas. Isto NÃO são 19 definições únicas (o mesmo pool pode aparecer em efeitos distintos; múltiplos componentes/condições têm semânticas diferentes).
- v0.9 do Laboratório fisicamente reaberto no Notion. Software relata suíte 251/251; isso é relatório da equipe de engenharia, não reexecução científica nem FULL-FIGHT canônico.

## 3. Fila de integração ED × Besta
1. **Prata 5 / primeiro match documental:** Liu Xiaua (ED, fonte 0b4c2b324ede837cb6be818dc8e36010), Vida 235, Alma 73 (expressão aritmética escrita), CA 46, RDF 10 na armadura, atributos e habilidades (Fúria 12 PA, Extensão Corporal 30 PA, ataque 2d6+37 em contexto de alternativas), versus Macaco Rei/Símio Demoníaco Gelo (301c2b324ede828caccb813d3979267a), Vida 750, Alma 700, CA 67, Patada 2d6+FOR, Mordida 1d6+FOR, Poder Elemental 1d10+INT 10PA. **STRICT-REJECT/FULL-FIGHT BLOCKED:** ficha viva/currentness, mecanismo de acerto, ação, RD da Besta, alcance, reação, status, equipamento ativo e relógio não certificados.
2. **Prata 5 / caso de stress:** mesma Liu versus Behemoth Glacial (1fdc2b324ede82bd9d4f811abb689440), Vida 500, Alma 560, CA 61, Estilhaços 2d6+DES, Mordida 3d6+FOR, Armadura de Gelo +3 CA, reflexão de 15% apenas do dano elegível — EXCLUI magias/projéteis, 20 PA ativação e 3 PA/turno. Temporização da reflexão, arredondamento e distinção ataque físico/arma/projétil pendentes; não simular automaticamente.
3. **Bronze 5 / caso somente histórico:** Chen Yi-Min M (90ac2b324ede8220b226816fd255c9cb) apresenta Bronze V, Vida 32/cheia 88, Alma 64/total 70, CA 24, Foice de Vento 2d6+INT alcance 9m/custo 2 PA, Defesa de Vento +2 CA (3 PA +1 PA/turno), proficiência +4 e armas. Sua página posterior (189c2b324ede834ab29081b0282c7b1f) apresenta Ouro II, de modo que Bronze 5 não é fixture CURRENT e só pode informar estudo histórico/condicional. Parceiro bestial B5: Frígido Ossário (f0dc2b324ede820ab9470168d4a53315), Rabada 1d6+FOR, Lâminas +1d4 Gelo, Passos CD15, Sopro Fortitude CD6+INT, sem duração/área.
4. **Bronze 1 / bestas verificadas, ED faltante:** Cabra de Chifres (391c2b324ede8252b0cc810423cdbfa6), Galinha Demoníaca (eddc2b324ede829f8a75011e8acbf429), Rato Flamejante (e29c2b324ede83708b2181332d26422a); fichas possuem Vida/Alma/CA/atributos/fórmula básica, mas não ataque vs CA, ação, defesas/RD nem ED Bronze1 qualificado. Continuar procurando ED físico sem gerar personagem fictício.
5. **Bronze 4 / conflitos:** Shen Yue possui registros Bronze 4 em página com múltiplas formas históricas (3d6c2b324ede835c8add8134c22a8a7d), não certificar as-of; Escorpião de Fogo (109c2b324ede8206bee481f992b7f800) e Veado das Montanhas (8acc2b324ede827b9bc801746ae97409) têm título Bronze4 e corpo Bronze2, não resolver por mutação.

## 4. Bloqueios e matemática
- MATH-ONLY: 20 ocorrências do lote focal possuem pool de dados identificável; outros 12 são buffs, percentuais, controle, dreno ou menções não redutíveis a DME normal. O total 20 não prova 20 ações READY e não pode ser somado às 49 históricas sem dedupe de ocorrência por ID+efeito.
- DAMAGE-ON-HIT: não liberado para simulação estrita — separar média dos dados, bônus fixo intrínseco e FOR/DES/INT externos; a expressão `2d6+37 (5d12+3d8+1d6+45)` de Liu contém duas alternativas cujo relacionamento exige fonte competente.
- FULL-FIGHT: 0/13 certificados no lote. A ausência de `FrozenRuleEvidence` SHA256 real, action economy, hit/save e source currentness barra execução canônica.
- Reações/reflexão: Behemoth exige gatilho cronológico e exclusão de magia/projétil. Escorpião de Fogo tem percentual de reflexão INDETERMINADO. Não emprestar 15% de outra espécie.
- DoT/área: trilhas flamejantes, tempestade, gelo e sangramento sem frequência/duração/área definida não recebem dano inventado.
- Dreno Alma: Aranha das Cavernas B5 tem Sucção de 2d6 **Alma**, não 2d6 Vida.

## 5. Governança e integração
Nenhuma ficha, besta, Party, regra, código de Laboratório ou ledger foi editado. Instância científica/writer/epoch/lease atuais **não comprovados**; não usar I0004/I0005 nem herdar I0003. Envio bilateral somente INBOX-COMESTRE-01, origin-instance não atribuída, target-instance não identificada. ACK pendente; análise documental anterior de IBX28 reportada pelo Mestre não substitui leitura formal.

## 6. FIRST-PENDING (próxima operação material)
1. Obter bytes autorizados dos manifestos CSV físicos de I0003 (incluindo 149 IDs, Fogo 01–12/13–24), calcular interseção/união com 104 e localizar exatamente Fogo 44º vínculo. URLs assinadas por Notion existem, mas download para runtime local falhou por conectividade; não alegar bytes recuperados.
2. Reabrir apenas as fontes selecionadas do par Prata5 e suas autoridades de ação, ataque/CA/RD, RD específica e crítica; mapear `AbilitySource` sem inventar efeitos; snapshot hash SHA256 do corpo FULL ainda pendente.
3. Continuar busca ED Bronze1 vigente em Personagens e considerar mais um exemplo P5 de ED/BE para holdout agrupado.
4. Solicitar ao Laboratório v0.9 contratos de entrada estritos (versão atual de ActionCatalog, FrozenRuleEvidence, resolvers/timing suportados, ordem de precedência entre RDF, reflexão e armas e gatilhos), sem alterar engine.
5. Persistir dados e registro completo no Diário/OP quando reserva de escrita material estiver validada; até lá apenas arquivo local + comunicação Inbox explicitamente autorizada.

**QA:** arquivo local JSON 13 fontes únicas + efeitos 32 + ranking 104, fonte Notion da amostra diretamente reaberta; nenhuma simulação de combate executada; nenhum NAC-PASS científico terminal. F0–F18 % global e D0–D9 denominator: NÃO DETERMINÁVEL.
