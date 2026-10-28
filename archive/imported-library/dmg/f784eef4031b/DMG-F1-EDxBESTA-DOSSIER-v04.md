# Dossiê científico DMG — Prata 5 · fixture v0.4 (MESTRE-ONLY / READ-ONLY)

**OP:** OP-DMG-CORPUS-EMP-01 | **pares:** Liu Xiaua × Símio Demoníaco (“Macaco Rei”) e Liu Xiaua × Behemoth Glacial | **DMG-RANK-01 v1.1:** OFICIAL/INTACTO.
**Fonte:** 9 páginas Notion físicas, cada uma com URL, last_edited_at e hash SHA256 do conteúdo Markdown extraído (anexo CSV). O algoritmo SHA256 foi testado contra abc e string vazia. O escopo do hash NÃO inclui imagens binárias, subpáginas, anexos externos ou certificação de vigência de entidade.
**Classe:** 10 expressões matemáticas anotadas, 8 checagens de consistência; 2 fixtures científicos, 18 gates por cenário, **0 FULL-FIGHT liberado**, 0 lutas executadas nesta pesquisa.

## 1. Conclusão de nomenclatura e patamar
- Variante física: [Prata 5 (titã)](https://app.notion.com/p/301c2b324ede828caccb813d3979267a) ID 301c2b324ede828caccb813d3979267a, sob pai [Símio Demoníaco❄](https://app.notion.com/p/f42c2b324ede82f1a62c81d6274d7d37). Corpo diz “macaco rei”; título diz “Prata 5 (titã)”. Trata-se de **uma única ficha física**, com nomes divergentes por camada. Não criar alias/entidade nova.
- Patamar físico de Macaco: Prata 5 em título/corpo; flag Titã em título, corroborada pelo cálculo de CA mas pendente de adjudicação; não tornar categoria Titã um sexto rank.
- Behemoth: Prata 5 corpo/título, normal provisório, fórmula normal de CA confere.
- Liu: primeiro bloco da página física rotulado Espiritualista Demoníaco Prata 5; há seção transformada separada no mesmo documento. A forma normal é o candidato deste fixture, transformação não habilitada automaticamente.

## 2. Estado-fonte nominal (não são estatísticas corrigidas)
| Ator | Fonte | Vida | Alma registrada | CA | FOR/DES/CON/INT | defesa nominal derivada |
|---|---|---:|---:|---:|---|---|
| Liu Xiaua ED P5 | 0b4c2b324ede837cb6be818dc8e36010 | 235 | 73 = 170+50−15−30−60−42 | 46 | 29/16/16/11 | RDF 10 da armadura; outros RD UNKNOWN |
| Símio (Macaco Rei) BE P5 Titã-título | 301c2b324ede828caccb813d3979267a | 750 | 700 | 67 | 54/40/35/30 | RD Prata Titã 30 se flag validada |
| Behemoth BE P5 normal-provisório | 1fdc2b324ede82bd9d4f811abb689440 | 500 | 560 | 61 | 15/45/30/36 | RD Prata normal 15 se classe validada |

## 3. Anomalia de Vida/Alma versus Criação de Besta vigente
| Fonte | Valor escrito | Derivado pela regra vigente | Diferença |
|---|---:|---:|---:|
| Macaco Vida | 750 | 60+10×(40+35)=810 | -60 |
| Macaco Alma | 700 | 60+10×(40+30)=760 | -60 |
| Behemoth Vida | 500 | 30+10×(20+30)=530 | -30 |
| Behemoth Alma | 560 | 30+10×(20+36)=590 | -30 |

Os quatro valores da ficha coincidem exatamente com o cálculo **sem o valor inicial da categoria**. A omissão é **hipótese explicativa**; confirmar origem/histórico antes de classificar como erro efetivo. O sistema especializado de Criação de Besta e as fontes específicas exigem decisão de precedência para escolher HP/PA no replay. Não corrigir ficha nem reescrever canonicamente.
**CA prova de consistência:** Macaco 20+40+35÷5=67; Behemoth 10+45+30÷5=61; Liu 6+16+15+4+3+2=46 quando FF observado é aplicável. Isso não prova identidade nem que bônus situacionais estejam ativos.

## 4. Fórmulas físicas e estágio de uso
- Liu: “H - Ataque Básico: 2d6+37 (5d12+3d8+1d6+45)”. O primeiro termo parece **to-hit**, o segundo parece **dano**, mas essa semântica precisa prova específica. Como leitura matemática literal (não DME intrínseco CERTIFICADO): 5d12+3d8+1d6+45 tem **média 94,5, mínimo 54 e máximo 135**, condicionais à interpretação e sem rerrolagens de Destruidor, buffs ou RD. 2d6+37 é candidato a rolagem de ataque, NÃO efeito de dano, e varia de 39 a 49; se for to-hit, não supera CA61 nem CA67 **sob esse submodelo**, não uma sentença de combate real. Arma “Machado de Guerra Elétrico” 5d12; “Infusão Elétrica” 3d8+6; ordem de adição e tags precisam conferência.
- Macaco: Patada 2d6+FOR (impacto); Mordida 1d6+FOR (perfurante); Poder Elemental 1d10+INT (10 PA; elemento/range/defesa UNKNOWN). Com FOR 54/INT30 literais, dano condicional médio 61 / 57,5 / 35,5. DME **intrínseco** respectivo 7 / 3,5 / 5,5.
- Behemoth: Mordida 3d6+FOR (média condicional 25,5; DME intrínseco 10,5), Estilhaços de Gelo 2d6+DES (média condicional 52; DME intrínseco 7). Armadura de Gelo: +3CA, reflexão de 15% **do dano recebido elegível, excluindo magias e projéteis**, ativação 20 PA + sustentação 3/turno; não substituir pela Reação geral de Refletir Magias. Tempestade de Neve 15PA, Sopro Congelante CD=6+INT=42, 10PA; controle sem timing/range/save completos.
- **Nota:** as médias são apenas álgebra literal; não convertem ações em ataques legais, não incluem ACERTO, crítico, RDF, RD, exaustão nem taxa de vitória.

## 5. Regras verificadas versus bloqueios
- Sistema de Combate: Prata usa 2d6; 1 ação padrão + 1 movimento + 1 reação; iniciativa 2d6+DES+bônus, falta bônus/tie; ataque 2d6+Luta (FOR ou DES quando permitido)+proficiência, sucesso apenas quando supera defesa; contra-atacar/Defender/Esquivar têm reações e resoluções; crítico de arma requer sequência de 3d6, magias não usam crit universal.
- Criação de Besta: Prata normal prof+8 RD15, Prata Titã prof+11 RD30, base Vida/Alma 30 normal ou 60 Titã, CA normal 10+DES+CON/5 e Titã 20+DES+CON/5; velocidade P5 normal 10+DES/4, Titã 20+DES/4; regra de dano-base de Besta NÃO reescreve expressões explícitas atuais da ficha.
- Sistema de Magia: PA Livre precisa estar comprovado antes de custo; 1 ação padrão padrão quando magia não determina tempo; exaustão espiritual por custo sem PA livre leva à inconsciência 2d10 dias (na batalha, colapso tratado como morte). Liu 73 permanece um valor histórico com gastos embutidos, sem certificação de recursos na cena.
- Laboratório v0.9: scheduler ainda MANUAL/EXTERNO; iniciativa empatada, reação/DoT/tick de duração e efeito multiator aguardam integração/gates; STRICT exige `FrozenRuleEvidence` real. Não assumir que tests unitários equivalem a combate canônico completo.
- Sistema Transformação T9-A: uma ativação por cena e um descanso completo após uso em cena distinta; sem prova de Espírito/TAP/overlay atual da Liu, não habilitar Transformação. 

## 6. Matriz de bloqueios
Anexo CSV com **18 gates × 2 confrontos = 36 classificações**. 18/18 tópicos de cada cenário examinados como documentalmente resolvidos, pendentes ou não aplicáveis, **não 18 PASS**. Sob avaliação estrita, resultado = **STRICT-REJECT / NOT-EXECUTABLE**, porque há gates impeditivos.

## 7. Contrato de integração e resultado esperado
Permanecer no contrato vigente do laboratório: `AbilitySource`, `ActorActionState`, `FrozenRuleEvidence`, `SourcedOption`. Cada null é UNKNOWN e não zero. IDs determinísticos de source, action e cenário; caso sem snapshot de dado completo ou sem custo/ação legal é rejeitado no menu, e o motor não recebe permissão implícita.
**Resultados esperados testáveis antes de combate:** (a) IDs estáveis e SHA do corpus presentes; (b) parser de dados matemático retorna valores do CSV; (c) os quatro conflitos de Vida/Alma são sinalizados; (d) todos os 18 blockers avaliados em cada cenário; (e) FULL-FIGHT rejeitado; (f) nenhuma probabilidade de vitória reportada. Quando resolvidos os gates, o laboratório responsável poderá produzir iniciativa, turnos, ações, respostas, consumos, impactos, mitigação, estados e desfecho com seed e log, então passar por validação independente NAC-PASS.

## 8. Continuidade após o lote
- Manifesto predecessor suposto 149 IDs permanece **não identificado como lista original**; 7 CSV I0003 recuperados têm 87 IDs únicos, vs 111 locais interseção 0, união parcial 198. NÃO chamar de união 149×111.
- Fogo original CSV I0003 = 21 linhas 01–12 (20 IDs + Agny sem variante `NO_LEVEL`) + 23 linhas 13–24 (23 IDs) = **44 linhas de censo, 43 IDs variantes**. Os 43 IDs coincidem nominalmente, um por um, com os 43 filhos diretos locais. Treze menções cruzadas são outro denominador.
- READ-ONLY em fichas, normas, Party, O Primeiro e código do laboratório. Sem writer/epoch/lease reivindicado para ciência. A entrega à Inbox do laboratório, se feita, é comunicação mestre-side documental, não aceite do engenheiro.

**FIRST-PENDING EXATO:** (1) identificar origem e lista dos 149 sem inferência; (2) adjudicar formalmente vida/alma e Titã/alias; (3) resolver proficiências, ação, PA livre, dano misto/RD, reflexão e scheduler junto ao laboratório; (4) reabrir snapshots e comparar SHA no pré-flight de cada combate; (5) somente após FULL-FIGHT gate liberar 1 combate e auditar no LAB.
