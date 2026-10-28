# DMG — Handoff READ-ONLY do sucessor (08/10/2026)

**Operação:** OP-DMG-CORPUS-EMP-01. **Identidade:** CM-000001. **Predecessor:** I0003; **I0004** pertence a outro workstream de comunicação; **I0005** apenas candidata, NÃO RESERVADA. **Writer:** nenhum para esta execução, nenhuma escrita no Notion. **Segredo:** Mestre-only.

## Proveniência
- OP: https://app.notion.com/p/3f3c2b324ede813e9fa0c87ebdea0b29
- Central: https://app.notion.com/p/3edc2b324ede81569f84c77a50708f93
- Perfil CM-000001: https://app.notion.com/p/3f1c2b324ede81238a39cc28e148af1f
- DMG-RANK v1.1: https://app.notion.com/p/3f2c2b324ede815498cddb7844245f7e
- F1 piloto: https://app.notion.com/p/3f3c2b324ede8123986ff96c1326c6ab
- Gelo: https://app.notion.com/p/85fc2b324ede82c99db101ab105f182f
- Fogo: https://app.notion.com/p/988c2b324ede8398b6f8019b49e032ea

## Estado PREDECESSOR / evidência persistida
27 CSV anexados à Central; crosswalk root, armas, técnicas, artefatos, inscrições, 12 famílias Bestas; 239/239 pais e 412 apontamentos imediatos, NO REPEAT. As quantidades 149 IDs e 53 refs CRAFT não foram corroboradas por leitura dos bytes desses manifestos. O último checkpoint de Gelo da Central certificava 25/25 pais e 48 ponteiros, não extração integral.

## Trabalho NOVO verificável, sem escrita
- REOPEN individual de 48/48 páginas variantes de Gelo (25 pais); extração preliminar de rank título/corpo, nomes, exemplos de Vida/CA/atributos, expressões ofensivas e exceções.
- REOPEN individual de 43 variantes de Fogo nas 24 páginas-pai diretas (Agny tem zero), além de 13 variantes em seis pais por mention-page (Basilisco 7, Tatu Bola 2, Golem 1, Salamence 1, Ravengale 1, infernalis electricus 1), fora das 24 páginas-pai diretas. Os registros de 44 ponteiros da Central versus 43 diretos observados permanecem em CONFLITO DE CENSO.
- Discrepâncias de identidade e rank, fichas só com imagem, habilidades descritivas sem dados, dano reativo, controle e fontes mistas. Nenhuma promoção ou correção de cânone.
- Não confundir dado `1d6` em loot com dano, nem rank do título com rank de conteúdo, nem vínculo com ficha analítica deduplicada.

## FIRST-PENDING exato
1. Antes de write, resolver alloc de nova INSTANCE e gate legítimo de claim/epoch/lease. I0004 está ocupado; I0005 é apenas possibilidade, sem COMMIT.
2. Recobrar bytes do CSV crosswalk (inclui 149 IDs referidos em conversa?) e anexos de Gelo; contrastar checksum/ID/timestamps com o ledger 48 rows presente no JSON anexo. Não repetir leituras já feitas sem delta/lacuna.
3. Adjudicação Mestre dos conflitos de rank/identidade; preservar título e corpo independentemente. Produzir DEFINITION-ID/OCCURRENCE-ID e fórmula/efeito/componente, apenas research docs quando writer válido.
4. Fogo: o primeiro gap é 44 apontamentos registrados na Central versus 43 subfichas diretas observadas, exigindo conferência do CSV original e das seis menções cruzadas agora reabertas (13 variantes), sem creditá-las duas vezes. Agny não exibiu corpo/filhos e exige recuperação por fonte alternativa.
5. D0-D9 globais indeterminados; FULL-COMBAT validado 0 demonstrado neste censo. Sem ajuste DMG-RANK v1.1.

## Protocolo científico
DME intrínseco separado de FOR/DES/INT externos. Ex.: Mamute Prata 1, Chifrada 2d6+2d4+FOR: média dos dados 12, mínimo dos dados 4, máximo dos dados 20, sem presumir valor fixo de FOR. Em alvo real, exigem-se acerto, RD/CA, defesa, ação/custo, crítico e condições. Espelho Party e conteúdo histórico nunca entram dobrados.

## Status formal
RECUPERAÇÃO LEITURA = VERIFICADA para as páginas e links descritos; EXTRAÇÃO = PARCIAL; DOC NOTION WRITE = 0; RESERVED/WRITER = PENDING; NAC-PASS terminal da pesquisa = NÃO APLICÁVEL COMO CONCLUSÃO TOTAL; fechamento operacional desta execução = handoff de leitura.

## Contadores científicos da amostra lida (N=104 páginas; NÃO equivalem ao corpus global)
- 48 Gelo diretas + 43 Fogo diretas + 13 ligações cruzadas de Fogo = 104 IDs de variantes distintos neste handoff.
- 49 expressões ofensivas em dados/bonus capturadas preliminarmente em 34 páginas; **não** são 49 definições deduplicadas, nem ataques completos validados. Páginas restantes podem possuir efeitos narrativos e não têm dano 0.
- Auditoria de rank título × corpo: **71 conflitos inequívocos** entre classe/estrela explicitada nos dois locais, **24 concordâncias detectáveis**, **5 corpos sem estrela explícita** onde a classe coincide, **4 indeterminados**. Comparação por classe, com estrela cotejada apenas quando ambas foram declaradas; os conflitos são sinalizadores e não corregendas canônicas.
- 0 simulações FULL-COMBAT desta coleta. Combate não pode ser concluído a partir de dados de dano sem ataques, saves, CA, RD, custo e política de ação completos.

## Três casos críticos diretamente reabertos
1. [Símio Demoníaco Prata 5](https://app.notion.com/p/301c2b324ede828caccb813d3979267a): Patada 2d6+FOR (DME intrínseco dos dados=7); Mordida 1d6+FOR (3,5); Poder elemental 1d10+INT (5,5) por 10 PA. Três fontes de dano diferentes em uma ficha; não converter atributos em DME intrínseco.
2. [Behemoth Glacial Prata 5](https://app.notion.com/p/1fdc2b324ede82bd9d4f811abb689440): Estilhaços 2d6+DES (média de dados 7), Mordida 3d6+FOR (10,5) e Armadura +3 CA refletindo 15% do dano elegível, custo de entrada 20 PA e manutenção. Reflexão não é dano-base adicional constante, pois depende do ataque recebido.
3. [Símio Demoníaco Fogo Prata 1](https://app.notion.com/p/383c2b324ede8266ad2b819fc078a66a): título Prata 1 versus **Classificação Épico** no corpo. Épico não integra os cinco ranks oficiais × cinco estrelas. Possui Lança-chamas 3d6+INT, Ataque colossal 2d6+FOR e +5 dano em habilidade distinta. Não inventar 26º rank.

## Gelo/ Fogo fora do denominador fechado
As 13 variantes das seis menções cruzadas têm URLs preservadas no JSON, mas não compõem os 43 filhos diretos das 24 páginas-pai de Fogo. Sem ID-map global deduplicado, nenhuma delas deve receber contagem aditiva no universo de 412 links das doze famílias.
