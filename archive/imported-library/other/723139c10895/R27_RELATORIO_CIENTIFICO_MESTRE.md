# VLAB R27 — Primeiro relatório científico de balanceamento da baseline vigente

**Classificação:** MESTRE-SIDE · EXPERIMENTAL CONDICIONAL · DMG-RANK v1.1 INALTERADO · OP-VLAB-FUSION-SANDBOX-01.  
**Objeto:** regra vigente de combate e criação de Besta, perfis virtuais Bronze 1; nenhuma criatura canonizada ou luta STRICT.  
**Motores:** histórico R18 SQLite, A1 real, planejador v0.7 e resolvedor v0.8.1, com overlays de Mestre R26 e política R27 somente laboratório.  
**Pré-registro de amostra:** quatro perfis, 16 células ordenadas, 20 sementes por célula (320 configurações), denominador mantido mesmo quando inexecutável.  
**Política experimental:** falha crítica `1→1→1` e `1→1→2` gera perda da Ação Padrão e dano zero; sem efeito adicional, NUNCA regra de mesa oficial. Crítico positivo mantém bônus máximo +18 em 3d6.

## 1. Sumário executivo: o que sabemos e o que NÃO sabemos

**Observações físicas do executor:** **320/320** configurações avaliadas; **120** encerramentos condicionais, **200** impasses matemáticos identificados antes de atacar; **2506** ataques nativos, **1890** acertos, **7454** eventos A1. Dentro das seis células que admitem acertos, as **120/120** lutas da amostra chegaram ao encerramento experimental HP0, não a uma morte canonizada.

**Descoberta científica mais importante:** a possibilidade de superar a CA, mediada por FOR, DES e bônus de Luta, domina o resultado destes perfis mais que a potência intrínseca de 3d6. **10/16** células ordenadas ficaram sem possibilidade de acertar em qualquer direção com o repertório limitado a ataque básico: **200/320** tentativas censuradas no preflight. Não é 200 empates resolvidos, tampouco fracasso de software; é **limitação estrutural do cenário/política testado**.

**Segundo achado:** o perfil Equilibrado derrotou o Ofensivo em **28/40** confrontos espelhados, embora seu FOR seja menor, porque ambos atingem os respectivos alvos em todas as seis faces do dado básico e a DES maior influencia a iniciativa. As 40 observações compartilham sementes pareadas entre inversões e **não** são 40 famílias biológicas independentes; este resultado é uma **hipótese de saturação da precisão e de papel da iniciativa**, não prova universal.

**Terceiro achado:** o Ofensivo derrotou o Defensivo em **40/40** confrontos espelhados; o primeiro pode acertar em todas as faces do dado, e o segundo apenas em 2/6 quando o Ofensivo o enfrenta. Sob o único ataque escolhido, investir recursos em CA/CON sem precisão mínima sacrifica capacidade ofensiva.

**O que NÃO foi demonstrado:** equilíbrio de Galidemus, de Bestas reais ou das 25 posições; nenhuma ação real integralmente admitida; nenhuma das 1.875 células da grade foi creditada. Uma solução para uma fixture virtual não corrige a falta de fonte/ação completa de Besta real.

## 2. Desenho: quatro perfis com o mesmo orçamento

A regra geral de Criação de Besta concede **35 pontos iniciais +8 na primeira progressão Bronze 1 =43 pontos**; os valores abaixo são **distribuições de experimento, não fichas oficiais**. A modalidade `RULE-DERIVED-VIRTUAL` é prevista no Plano Mestre. CON foi escolhido múltiplo de 5 para evitar arredondamento de CA sem autoridade. Não existem traços de espécie, magia, título, transformação ou habilidades especiais.

| Perfil | FOR | DES | CON | INT | SAB | CAR | CA pela regra | Vida | Alma |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| OFENSIVO | 20 | 4 | 10 | 3 | 3 | 3 | 16 | 50 | 43 |
| DEFENSIVO | 6 | 12 | 15 | 4 | 3 | 3 | 25 | 55 | 44 |
| EQUILIBRADO | 12 | 9 | 10 | 4 | 4 | 4 | 21 | 50 | 44 |
| ASSIMETRICO | 2 | 22 | 10 | 3 | 3 | 3 | 34 | 50 | 43 |

**Camadas documentais preservadas:** ataque normal `1d6 + FOR + bônus Luta`; proficiência Bronze normal +6; foi **alocada experimentalmente** em Luta para ambos, sem comprovação de treinamento de uma Besta individual. Dano-base 3d6, RD geral 5, escolha de ação padrão sem PA positivo em contrato de teste, tag `impacto` usada apenas para transporte ao resolvedor. A ausência de ações adicionais e de reações voluntárias foi uma política específica; não é a exclusão dessas ações da regra canônica. HP0 é limite de laboratório, não morte decretada. A legitimidade integral de uma criatura de fonte real NÃO é reivindicada.

## 3. Resultados observados das 16 células

**Cada célula contém 20 sementes**. Valor = vitórias da personagem experimental da linha; travessão = impossibilidade de acerto demonstrada sob a política. As inversões de lados foram medidas separadamente.

| Perfil atacante (esquerda) | Ofensivo | Defensivo | Equilibrado | Assimétrico |
|---|---:|---:|---:|---:|
| **Ofensivo** | 9/20 | 20/20 | 5/20 | — (0/20 aptos) |
| **Defensivo** | 0/20 | — (0/20 aptos) | — (0/20 aptos) | — (0/20 aptos) |
| **Equilibrado** | 13/20 | — (0/20 aptos) | 7/20 | — (0/20 aptos) |
| **Assimetrico** | — (0/20 aptos) | — (0/20 aptos) | — (0/20 aptos) | — (0/20 aptos) |

**Amostragem e censura por célula:**

| Célula ordenada | Tentadas | Completas | Censuradas | Vitórias esquerda | IC 95% indicativo* | Rodadas médias (completas) |
|---|---:|---:|---:|---:|---|---:|
| OFENSIVO × OFENSIVO | 20 | 20 | 0 | 9 | 25.8–65.8% | 8.85 |
| OFENSIVO × DEFENSIVO | 20 | 20 | 0 | 20 | 83.9–100.0% | 10.40 |
| OFENSIVO × EQUILIBRADO | 20 | 20 | 0 | 5 | 11.2–46.9% | 8.75 |
| OFENSIVO × ASSIMETRICO | 20 | 0 | 20 | 0 | 0.0–16.1% | n/d |
| DEFENSIVO × OFENSIVO | 20 | 20 | 0 | 0 | 0.0–16.1% | 10.85 |
| DEFENSIVO × DEFENSIVO | 20 | 0 | 20 | 0 | 0.0–16.1% | n/d |
| DEFENSIVO × EQUILIBRADO | 20 | 0 | 20 | 0 | 0.0–16.1% | n/d |
| DEFENSIVO × ASSIMETRICO | 20 | 0 | 20 | 0 | 0.0–16.1% | n/d |
| EQUILIBRADO × OFENSIVO | 20 | 20 | 0 | 13 | 43.3–81.9% | 8.75 |
| EQUILIBRADO × DEFENSIVO | 20 | 0 | 20 | 0 | 0.0–16.1% | n/d |
| EQUILIBRADO × EQUILIBRADO | 20 | 20 | 0 | 7 | 18.1–56.7% | 16.45 |
| EQUILIBRADO × ASSIMETRICO | 20 | 0 | 20 | 0 | 0.0–16.1% | n/d |
| ASSIMETRICO × OFENSIVO | 20 | 0 | 20 | 0 | 0.0–16.1% | n/d |
| ASSIMETRICO × DEFENSIVO | 20 | 0 | 20 | 0 | 0.0–16.1% | n/d |
| ASSIMETRICO × EQUILIBRADO | 20 | 0 | 20 | 0 | 0.0–16.1% | n/d |
| ASSIMETRICO × ASSIMETRICO | 20 | 0 | 20 | 0 | 0.0–16.1% | n/d |

*O intervalo Wilson 95% utiliza vitórias do lado esquerdo sobre TODAS as 20 configurações daquela célula, e a censura é informada em separado; quando há censura, esse intervalo **NÃO** estima uma probabilidade incondicional de vitória em combate legal completo. 20 sementes não permitem precisão estatística fina nem controle por família de Besta canônica.*

## 4. Preciso acerto vs. CA vs. RD: três causas distintas

Sob **apenas o acerto básico 1d6+FOR+6**, a probabilidade **exata pelas seis faces do d6**, ANTES de aplicar a ocorrência rara da política de falha crítica automática, é:

| Atacante × defensor | Ofensivo | Defensivo | Equilibrado | Assimétrico |
|---|---:|---:|---:|---:|
| **Ofensivo** | 100.0% | 100.0% | 100.0% | 0.0% |
| **Defensivo** | 33.3% | 0.0% | 0.0% | 0.0% |
| **Equilibrado** | 100.0% | 0.0% | 50.0% | 0.0% |
| **Assimetrico** | 0.0% | 0.0% | 0.0% | 0.0% |

**Precisão:** FOR extra deixa de gerar mais chance de acerto quando o valor mínimo do teste já supera a CA: Offensivo já possui 100% de acerto básico contra Ofensivo, Defensivo e Equilibrado. No lado oposto, o Assimétrico quase intocável tem **0% de chance de acertar qualquer um** com esse ataque, e os outros também têm 0% de atingi-lo. Não é uma vantagem ofensiva; é um **impasse condicional**.

**RD e dano líquido:** o núcleo histórico entregou **19913** de dano bruto em acertos, **9391** efetivamente absorvidos por RD, **10522** de dano líquido e **10131** de Vida realmente retirada. O excedente **391** decorre do corte de Vida em zero ao encerrar a luta. Dano bruto **não** é a soma de dados lançados durante ataques errados; esse valor está separadamente nos rastros. A redução por RD contabiliza `raw - net`, não cinco pontos integrais quando o dano bruto é inferior a cinco.

**Combinatória exata do dano Bronze:** um 3d6 tem bruto médio 10,5; com RD5 compatível, `E[max(3d6−5,0)] = 1193/216 = 5,5231`. Há **10/216 = 4,63%** de distribuições que não superam RD5, mesmo quando ocorre acerto. Isso é uma função analítica do dano isolado, **não** uma rolagem feita por novo resolvedor; combate real segue o v0.8.1. Com acerto não garantido, o dano efetivo médio por ação cai novamente. Iniciativa e condição de crítico não devem ser confundidas com RD.

**Críticos observados nesta matriz:** **28 positivos** e **18 falhas críticas experimentais**, sobre **2506** ataques nativos. Probabilidade-base teórica para cada gatilho: `2/216 ≈ 0,926%`, pois os dados são examinados sequencialmente. O dado de crítico não foi incorporado à rolagem normal de acerto; o positivo acrescenta o máximo do pool de dano e o negativo consome a ação, sem dano, somente no sandbox.

## 5. Exame matemático das transições entre os cinco ranks

A análise independente enumerou todas as combinações de dados do **dano genérico da Besta normal contra RD geral da mesma faixa**; o Lendário usa Titã por determinação expressa da Criação de Besta. Os dados de ataque por classificação vêm do Sistema de Combate. Nenhum combatente real de rank superior foi criado.

| Rank | Dados de acerto | Dano normal genérico | RD da mesma faixa | Dano bruto médio | Média positiva após RD* | P(dano não superar RD) |
|---|---|---|---:|---:|---:|---:|
| BRONZE | 1d6 | 3d6 | 5 | 10.50 | 5.523 | 4.63% |
| PRATA | 2d6 | 6d6 | 15 | 21.00 | 6.133 | 9.65% |
| OURO | 3d6 | 9d6 | 25 | 31.50 | 6.743 | 12.28% |
| OURO_NEGRO | 4d6 | 12d6 | 35 | 42.00 | 7.339 | 13.76% |
| LENDARIO_TITA | 6d6 | 20d10 | 75 | 110.00 | 35.010 | 0.33% |

*Após RD = expectativa combinatória de `max(0, pool−RD)`, para uma instância de dano compatível, **SE** o ataque atingir e sem buffs/fraquezas. Não inclui chance de acerto, atributos, críticos, PA, habilidades nem contratos de ação. Não é uma previsão de vitória.*

**Indicador a investigar:** o dano médio líquido condicional da Besta normal sobe relativamente pouco de Bronze até Ouro Negro (~5,52→7,34 sob RD da própria classificação); na transição para Titã Lendário, o mesmo cálculo sobe para ~35,01. A tabela não prova desbalanceamento: os atributos, a retroatividade Titã, Vida, ataques, efeitos e armamentos também mudam. A próxima etapa deverá confrontar esses componentes **em atores integralmente construídos**, em especial Bronze5→Prata1, Prata5→Ouro1, Ouro5→OuroNegro1 e OuroNegro5→Lendário1.

**Cobertura honesta:** foram examinados cinco grupos de rank nos fatores matemáticos e as quatro fronteiras correspondentes, com todas as 25 posições presentes como índice de progressão; **não** foram executados 25 builds, nem combates completos além do Bronze1. Patamares com confronto condicionado: **1/25**; patamares com confronto canônico real: **0/25**.

## 6. Frente real: quatro fichas reabertas, despacho integral ainda 0

| Fonte Notion (ID abreviado) | Evidência explícita | Bloqueio mínimo para execução integral |
|---|---|---|
| Galidemus / Galinha Demoníaca (eddc...429) | Bronze1, Patada `1d4+DES` cortante, FOR5, DES13, CA21 | atributo de Luta da Patada e treinamento aplicável, enquadramento/custo e alcance, versão de ficha e transação válida; FOR é padrão e DES no dano não prova DES no acerto |
| Cabra de Chifres (391c...fa6) | Bronze1, Investida `1d6+FOR` impacto, CA20 | empurrão exige distância, posicionamento, possível salvaguarda e ordem; proibição de omitir o rider |
| Raposa Flamejante (4d0c...60ca) | Bronze2, Bola de Fogo `1d4+5`, rastro de fogo | custo, alvo, mecanismo da magia e janela/DoT do rastro insuficientes |
| Macaco Rei Titã (301c...267a) | Prata5, Patada `2d6+FOR54`, Mordida `1d6+FOR54`, Poder Elemental com 10PA | fornecedor R31 registra gates B–E ainda não fechados; efeitos/passivas/recibo/autoridade nativa faltam |

**Galidemus contra Cabra — separação de causalidade:** sob o ataque **comum hipotético** com FOR5 e Luta+6, o máximo de teste Bronze é `6+5+6=17`, abaixo da CA20 da Cabra. Mesmo uma Patada que efetivamente cause dano alto **não consegue atingir esse alvo** por esse contrato condicional. Isso não autoriza afirmar que a Galidemus não possa usar ação especial, DES de Luta, vantagens ou outras fontes; falta o contrato completo para esse evento.

**Admissão real:** **0 ações de fontes reais integralmente admitidas**, **0 eventos legais reais processados**, **0 combates de fontes reais**, **0/1.875 células canônicas**. A R24 continua fornecendo apenas uma prova de componente documental com acerto forçado, sem crédito de Patada válida. O R31 do DMG ainda exige os cinco gates A–E, e o ZIP binário de seu fornecedor não ficou materializável nesta sessão; nenhum ACK, despacho ou permissão forjada foi criado. A IBX-90 existente permanece o canal de coordenação, assim como a IBX-92 para pendências normativas.

## 7. Lacunas, hipóteses futuras e riscos de interpretar mal os dados

| Severidade de investigação | Hipótese / achado observado | Causa provável | Freq. neste recorte | Próximo teste discriminante |
|---|---|---|---|---|
| Alta | Impasse de acerto | FOR+Luta insuficientes frente à CA por distribuição; política ofensiva única | 200/320 tentativas (10/16 células) | Adicionar SOMENTE ações e equipamentos legalmente documentados e comparar mesmas sementes |
| Alta | Retornos decrescentes da FOR após acerto saturado | Mais FOR não aumenta 3d6 intrínseco sem fonte específica; DES favorece iniciativa | Equilibrado venceu 28/40 contra Ofensivo no par espelhado | Repetir com outras CA e alocação de Luta documentada |
| Média | RD absorve grande fração do dano bruto observado | RD5 genérica contra 3d6; composição de ataque e precisão | {t['sum_rd_mitigation_actual']}/{t['sum_raw_damage_observed']} pontos de dano bruto dos acertos | Variar RD apenas com autoridade e comparar componentes de hit isolados |
| Média | Formulação de progressão entre ranks pede exame de descontinuidade | Dados de dano e RD crescem em degraus, Titã Lendário altera categoria | Cinco grupos de rank matematicamente examinados; 0 combate cross-rank | Reconciliar primeiro ator Bronze5/Prata1 de fonte completa |
| Alta | Fontes de habilidades específicas continuam não executáveis | Custo, alcance, ações especiais, atributos, contrato nativo de efeito | 4 fontes examinadas, 0 ações admitidas | Resolver primeiro campo de Patada que falta, fechar gates A–E sem inventar custo |

**Melhorias futuras são hipóteses, NÃO decisões de alteração:** (1) investigar se incentivos de atributo/proficiência produzem armadilhas de criação de build; (2) comparar bandas de dano-base vigentes ANTES de propor nova escala; (3) ensaiar reação renovável em matriz separada para não contaminar a presente política sem defesa; (4) priorizar integração de uma fonte real com ação completa. Qualquer reclassificação de Besta ou item pertence à autoridade competente, não ao VLAB.

## 8. Repetibilidade, exceções transacionais e baseline ANTES

- O ZIP preserva **320 recibos JSON + bancos SQLite de cada célula**, com uma exceção de transporte registrada: duas corridas preliminares tiveram intenção `UNKNOWN_EFFECT` e seus bancos originais ficaram intocados em HOLD. As duas células/seed foram repetidas somente como **novas sessões isoladas**, explicitamente identificadas, mantendo os bancos originais para auditoria. Assim há 320 resultados analisados e 2 tentativas preliminares abortadas adicionais, sem replay inseguro.
- Contém **24 checkpoints ZIP**: um por célula na semente 11 e os oito testes originais R25/R26; todos verificados pelo histórico e manifestos SHA. Os demais resultados são recuperáveis diretamente dos SQLite.
- **Quatro replays independentes** coincidiram em revisão, hashes, eventos do resolvedor, A1, vencedor, Vida e SHA exato dos bytes SQLite (inclusive a semente 83).
- A bateria R25 original permanece 5/8; R26 7/8; **R27 8/8** sob a política laboratorial aprovada pelo Mestre. Não são mesmas normas canônicas: os resultados divergem pela disponibilidade operacional das regras Mestre-LAB, não por candidata nova do DMG-RANK.
- Configuração congelada em cada SQLite e digest do experimento; sementes de cada célula: `{list(D['universe']['profiles'])}` usam a lista exata em JSON. Os textos das páginas oficiais foram consultados read-only; o SHA dos trechos transcritos serve à consistência local, **não é assinatura nativa do Notion**.
- **BASELINE ANTES:** `DMG-RANK v1.1` em vigor e as hipóteses declaradas de cenário; nenhuma versão candidata DEPOIS foi introduzida. Comparação futura deve manter corpus, streams RNG, políticas, atores, equipamentos e classificações sob equivalência verificável, e reportar quando divergir.
- **Sem escrita produtiva:** fichas reais, Party, O Primeiro, bestas, DMG-RANK v1.1 e regras Notion intactos. IBX-56 BLOCKED-EXTERNAL; IBX-90/91/92 sem ACK presumido; writer, lease, epoch, fencing, GREEN e NAC-PASS produtivo HOLD. VLAB 0/17, DMG 1/18, STRICT 0/2.

## 9. PSV / contabilidade

| Objeto | Antes (R26) | Depois (R27) | Denominador |
|---|---|---|---|
| Sementes originais completas | 7 | **8** | 8 pré-fixadas |
| Células Bronze1 cruzadas planejadas | 0 R26 | **16 avaliadas** | 16 ordenadas |
| Células com combate viável sob política | n/d | **6** | 16 |
| Tentativas científicas cruzadas | 0 R26 | **320** | 16 × 20 |
| Combates cruzados condicionais completos | 0 R26 | **120** | 320 tentativas |
| Pré-flight com impossibilidade matemática de acerto | 0 R26 | **200** | 320 tentativas |
| Testes nativos do sistema derivados de criações reais | 0 | **0** | Quatro fichas reais consultadas |
| Ranks/estrelas com combate condicionado | 1 | **1** | 25 |
| Grupos de rank com análise matemática de base | Bronze apenas | **5** | 5 principais |
| Fights canônicos completos | 0 | **0** | Evidência efetiva |
| Células canônicas creditadas | 0 | **0** | 1.875 |
| Certificação VLAB | 0 | **0** | 17 |
| Critérios DMG certificados | 1 | **1** | 18 |

**Ponto de retomada material:** consumar uma ação de fonte real só após comprovar campo essencial pendente sem hipótese substitutiva; em paralelo obter uma coorte de construções Bronze1 com treino e tipo de ação plenamente source-attested, testar política defensiva separada agora que o refresh está disponível, e completar as fronteiras Bronze5→Prata1 com fontes e estatutos normativos suficientes. **Não retornar aos Vigias manuais.**
