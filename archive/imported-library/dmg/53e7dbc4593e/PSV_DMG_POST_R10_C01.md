# PSV — Continuidade pós-R10, C01 | OP-DMG-CORPUS-EMP-01

**Data de referência:** 15/10/2026, America/Recife · **Ambiente:** MESTRE-SIDE · **Estado:** conclusão da rodada científica com pendências explícitas, nenhuma escrita canônica. **Este é o checkpoint `POST-R10-C01`, NÃO o R11 antigo de 09/10/2026.**

## 1. ANTES e recuperação física

- R10: manifestação local `R10_CHECKPOINT_SHA256.json` reaberta, 12/12 hashes iguais; scripts, JSON, PSV e handoff imutáveis. `R10_RESULTS.json` é estado intermediário Notion-R40-only; `R10_SECONDARY_AUDIT.json` e PSV são evidência posterior de readback independente do ZIP R40. Cronologia reconciliada sem editar histórico.
- O Notion contém `DMG R11→R12 — suplemento técnico sucessão preventiva`, registro datado 09/10/2026, anterior ao eixo R01–R10 de 15/10; também `DMG R13` daquela sucessão. IDs e identidade temporal distintos; nenhuma retomada/falso R11 canônico foi afirmado.
- VLAB ao início da pesquisa apresentava R41 REGISTRO DEPOIS e R42 REGISTRO ANTES. Durante a rodada, R42 passou a REGISTRO DEPOIS. Ambos os ZIPs foram materializados read-only da Biblioteca original da OP-VLAB existente e auditados por verificadores stand-alone fornecidos nos próprios pacotes; nenhum escritor VLAB usado.
- R41 ZIP SHA256 `105615717ddb62b84e51f2232bde067133e3c576a14340dac3b5427e0078306b`, CRC +59 hashes +6 cenas, 475 eventos, 469 ataques, nove críticos positivos PASS. R42 ZIP SHA256 `36f99ca5e77ea6aae0d4537f1cc64ba69ea6242c1c67a24b4a1bebc17e98c966`, CRC +30 hashes +6 SQLite, 931 eventos, 928 ataques, nove críticos positivos e sete negativos PASS. Todos **eventos do VLAB, não da DMG**.
- R41 já possui integração experimental de crítico positivo automático, não repetir a tarefa pré-R41. R42 já aplica decisão LAB-ONLY prévia do Mestre para falha crítica negativa (erro, dano0, ação consumida, custos preservados, nenhuma penalidade automática adicional). Não confundir com norma geral publicada. R42 estabeleceu ordem **relativa** de iniciativa para instâncias da MESMA ficha com bônus comum B desconhecido, mas NÃO prova bônus de iniciativa entre fichas diferentes. Dois Ataques de Oportunidade concorrentes e Luta do Contra-atacar continuam bloqueados por autoridade/fonte. Contratos VLAB terminais 0/17; células 0/1875.

## 2. Perguntas e pré-registro

Antes de ler novos corpos Notion, congelei queries rank/efeito/custo, primeiros resultados elegíveis por título, ID e limites de amostra. `C01_PREREG_SAMPLE_FROZEN.json` SHA256 `3c76ad28703b54858e93f7f227324fb44cb57512927915f4155378e3424ae6a0`. A seleção é **dirigida, não aleatória nem holdout independente**; material em que o resultado já era conhecido ficou fora da amostra nova quando o ID era conhecido. Novo pool de 18 páginas não garante não sobreposição com os 10 IDs antigos fora do índice preexistente de 43 IDs.

Perguntas independentes testadas: (i) quanto tempo efetivo e quantas ações extras são consumidas por críticos e empurrões; (ii) quando a RD faz crítico acertar sem lesar; (iii) se o conteúdo real permite progressão por rank sem confundir título/corpo/árvore; (iv) se custo e reações mudam benefício sem inventar Vida↔PA; (v) se os novos resultados contradizem nativos R41/R42.

## 3. Expansão física de corpus e falsificação documental

18 páginas Notion diretamente abertas: 17 Mestre, 1 espelho Party identificado e excluído de todos os dados científicos Mestre. Entre as 17 Mestre: **12 Bestas**, 2 fontes não bélicas (veneno narrativo e Traje águia celeste), 2 propostas PS e 1 NPC de encontro ainda proposto. Nessas 12 Bestas, **7/12** divergem no rank MAIOR do título versus corpo; **10/12** não exibem correspondência literal exata rank/estrela título-corpo (incluindo ausência de estrela). Somente **2/12** têm concordância título/corpo integral. Essa taxa é da coorte dirigida, **não estimativa populacional**.

Entre as 12 Bestas, apenas **2 páginas** possuem ações completas com fórmula inicial de dano, produzindo **4 ações numéricas**, **3 expressões distintas**: veado das montanhas, título Bronze4 mas corpo Bronze2, `Galha mortal 1d6+FOR11`; Regalis voltmane sob Ouro2, corpo Ouro2, *nome individual em branco*, `Raio eletrizante 2d4+INT72`, `Raio purificador 2d4+INT72`, `Toque macabro 1d4+INT72`. Todas sem Luta/PA individual comprovados. O raio eletrizante tem rolagem condicional 1d4=1 para teste de Fortitude, porém **CD da defesa, acerto e ação/custo** não foram autenticados. Sem codificação de magia como ataque critável, **não aplicar automaticamente crítico às três habilidades elementais**.

Os outros campos são tão importantes quanto as fórmulas: Escorpião de Fogo inclui queimadura/retorno sem magnitude; Cão Infernal (título ON1, corpo Ouro) contém aura persistente e magia de área sem número; Guardião Etéreo (título Lendário1, corpo Bronze) cita DoT/área sem dano/duração. Os dados ausentes **não viraram dano zero**, nem equipamento drop virou arma ativa. As fichas PS e o NPC proposto ficaram fora do cânone executável.

**Conflito de classificação é um bloqueio mecânico real, não mero problema cosmético:** rank define dados de acerto, RD e outras tabelas; não se pode ordenar essas Bestas por dano efetivo apenas pelo título.

## 4. Pesquisa transversal de 33 fórmulas e fronteira crítico↔RD

O CSV preservacional R04 contém 29 ações iniciais de dano explicitamente normalizadas; somei as quatro novas ações numéricas, sem duplicar páginas conhecidas. Estudei **33 fórmulas** frente a nove hipóteses de RD escalar (5,15,25,30,35,45,60,75,120), testando os limites do dano crítico conforme os dados e bônus literais. Isso dá 297 **comparações numéricas**, NÃO 297 combates, NÃO certificações de elegibilidade de crítico, NÃO evidência estatística de cenários enfrentados em jogo.

- RD25: 2/33 expressões têm máximo crítico incapaz de superar a RD.
- RD45: 6/33; RD60: **20/33**; RD75: **26/33**; RD120: 33/33.
- As restrições ficam condicionadas à aplicação competente da RD ao TIPO de ataque e à elegibilidade da habilidade para crítico; não converter raio/magia em golpe físico nem atribuir Luta.

**Fronteira normativa matemática ainda mais forte:** a tabela vigente de Criação de Besta define para Besta normal Bronze um chassi **3d6** e para Besta normal Ouro Negro **RD35**. Se os acertos comuns forem impossíveis e nenhum atributo/bônus externo entrar nesse chassi, o crítico vale `3d6+18`; ele só ultrapassa RD35 quando os três dados de dano forem 6, em **1/216 críticos positivos**. Com chance de positivo 1/108 independente, a chance conjunta de *acerto crítico e dano positivo* é **1/23328 por ataque**. RD45 do Titã Ouro impede qualquer dano desse chassi mesmo no crítico. Esses não são ataques fonte-completos de uma Besta inventada: são os **componentes normativos genéricos** com exclusão explícita de FOR/FF/equipamentos.

Sensibilidade de dano fixo (contrafactual, nunca atributo atribuído): +1 ao chassi 3d6 multiplica por 4 a frequência de crítico com dano positivo contra RD35, +2 multiplica por 10. A transição é altamente não linear. **Uma correção tática/buff pequeno pode alterar a existência de progresso**, mesmo sem alterar a chance de crítico; a prova de bônus real ainda seria necessária.

A ficha nova veado Bronze (rank por estrela conflitante) tem `Galha mortal 1d6+FOR11`: máximo bruto normal17, crítico23, portanto não supera RD25 de uma Besta Ouro normal **se essa RD mitigar a galhada e não houver bônus extra**. Não se trata de dizer que a Besta inteira não pode ferir; a fonte informa somente essa ação com número.

## 5. Contraste físico entre criaturas já autorizadas: Frígido × Behemoth

Rabada Frígido Bronze5 `1d6+FOR18`, Luta+6 exclusivo, versus Behemoth Ouro1 CA68/RD25. O ataque comum 25..30 não chega perto da CA. O crítico acerta automaticamente por ordem expressa do Mestre, mas o dano líquido crítico, depois da RD25, é **0,1,2,3,4,5**, cada resultado condicionado ao dado uniforme. Assim, por tentativa de ataque:

- P(crítico positivo e dano líquido >0) = **5/648 = 0,7716%**.
- Dano líquido esperado por tentativa = **5/216 = 0,02315 Vida**, sem outros efeitos e com as fontes originais.
- Contra RD30 competente, a MESMA Rabada causa **zero Vida mesmo no crítico**.

A Armadura de Gelo acrescenta CA+3, mas seu componente de CA evita **zero** acertos comuns extras nesse alvo específico, visto que CA68 e CA71 já excedem 30, e não impede críticos. A reflexão de 15% é derivada do dano recebido; sem arredondar, seu valor nominal antes da RD do agressor seria **1/288 por ataque**; truncando por acerto vira zero; ceil seria 5/648. Se a RD5 do Frígido for competente sobre a reflexão, qualquer dessas variantes inteiras é mitigada a zero. Ativação20 PA +3 PA/turno continua custo real, sem converter PA em Vida. **A Armadura não é globalmente ineficiente; aqui o benefício de CA é nulo**, retorno e economia final dependem de tipologia/tempo de ação ainda não resolvidos.

## 6. Movimento, Reação e falha crítica em combate longo

Em R10, Cabra × Cabra sempre Esquivando tem expectativa exata de **205,7537868 rodadas** e **411,0066938 oportunidades totais de ataque**. Cada oportunidade tem P(crítico positivo)=1/108; pelo argumento de recompensa por parada, há média **3,8056175 críticos positivos** por combate e **2,8056175 empurrões não terminais que exigiriam reposicionamento**, se cada crítico causar dano e empurrar 1,5m e o alvo continuar vivo. Quando existe capacidade de Ação de Movimento para recuperar adjacência antes da próxima Ação Padrão, a duração em rodadas NÃO se altera pelo empurrão nesse controle de corredor aberto, mas Movimentos são consumidos. Se terreno, velocidade, geometria ou economia de ação não permitirem, a duração NÃO É DETERMINÁVEL; não se presume movimento grátis.

A R41 tem uma cena nativa DIRECIONADA de 84 rodadas, quatro positivos, quatro empurrões e três Movimentos — material compatível com a previsão condicional, **não uma amostra aleatória de duração**. R42 já executou em LAB a regra de falha crítica negativa declarada pelo Mestre: erro automático, dano zero, Ação Padrão consumida, sem dano próprio/arma perdida/penalidade presumida. Sob o modelo Cabra↔Cabra em que ataques não críticos já não ferem, a política LAB negativa não modifica a expectativa de duração; prevê em média **3,8056175 falhas críticas negativas** em todo o combate, mas não efeitos adversos novos. Esse é um resultado NEGATIVO científico válido, não licença para publicá-la mundialmente.

**Verificação externa ao cálculo primário:** oráculo independente recontou os 216 resultados críticos3d6, 16 checagens adversariais e uma bateria Monte Carlo PRÉ-FIXADA de **12.000 duelos**, seed20261015, limite2000 rodadas. Média observada **206,1092**, mediana186, p90≈365, erro padrão≈1,0720; desvio de 0,332 erro padrão da R10. Zero censuras nessa bateria, frequência de vitória do primeiro ≈50,125%; movimentos não terminais ≈2,8076 por duelo, negativos≈3,8068. Isto valida a implementação estatística local do modelo, **não é VLAB nativo, não é arena real, não é estudo representativo entre ranks**.

A R42 tem três cenas novas de Esquiva contínua: uma vitória HP0 na rodada154 e duas observações censuradas em130/180 rodadas, com 928 ataques no conjunto e sete críticos negativos processados. O mesmo oráculo analítico prevê **71,08%** de duelos ainda ativos em130 rodadas e **52,19%** em180. A amostra n=3 de horizontes diferentes é muito pequena para estimar taxa ou contradizer o controle. R42 continua LAB CONDICIONAL por iniciativa numérica individual desconhecida.

## 7. Economia de recursos e tipos de fonte

Fonte mestre equipamento <https://app.notion.com/p/3edc2b324ede816cbad5ca3880ce144d>: Traje águia celeste compromete 20 PA/dia e a ativação `Voo da Águia` consome 4 PA, no máximo uma vez por turno, para pulo4,5m. Para k ativações no mesmo dia, **20+4k PA** quando admissíveis; 3 ativações→32 PA/dia, 10→60 PA/dia. Não atribuí o Traje a nenhum portador, nem declarei sua ativação Ação Livre/Padrão sem fonte. O bônus +2 CA vale durante **Contra-atacar**, não CA passiva universal.

Fonte nova Ouro2 (nome do corpo em branco, árvore Regalis voltmane) tem dois raios iguais `2d4+INT72`, bruto médio77, e `Toque macabro 1d4+INT72`, médio74,5. O atributo representa 72/77≈93,51% da média do raio e 72/74,5≈96,64% do Toque. O efeito `Raio eletrizante` acrescenta um gatilho 1/4 para teste Fortitude, mas chance efetiva de paralisia depende de acerto, CD e salvaguarda desconhecidos. A comparação por custo/PA ou taxa real de crítico não está admitida. **Isso mostra por que DME intrínseco e dano final não são intercambiáveis**; a aplicação de banda por rank de efeito (RE) exige autoridade própria, não o simples rank nominal da criatura.

## 8. Hipóteses refutadas / resultados negativos

1. Refutada: o impasse da Cabra seria matematicamente infinito após decisão Mestre do crítico. Já refutada R10, preservada.
2. Refutada: a ponte de crítico positivo VLAB ainda não teria prova nativa posterior à R40. R41 foi fisicamente recuperada e auditada.
3. Refutada: falha crítica negativa ainda precisa ser perguntada ao Mestre para o VLAB LAB. R42 recuperou e exercitou decisão LAB prévia; persistência normativa geral segue pendente.
4. Refutada: cada novo nome de página de Besta serve para calcular progressão. Somente 2 de 12 têm fórmula inicial completa; 7 têm divergência de rank maior, 10 não coincidem exatamente em rank/estrela; nenhuma Luta real nova admitida.
5. Refutada: aumentar CA sempre traz benefício marginal. Contra Rabada Frígido acima, CA68→71 evita zero acertos comuns extras, enquanto PA de ativação/manutenção permanece.
6. Confirmada como limite real: RD pode impedir Vida positiva mesmo sob crítico automático; número de ataques necessários pode tornar-se INFINITO para aquela ação isolada sem outros bônus.

## 9. F0–F18, denominadores, aceites

- **F0 continua 4/8 marcos documentais**. `DMG-F0-PREREG-01` e `DMG-QA-ACCEPT-01` foram reabertos; o primeiro lista fontes primárias7/7 indexadas, com **fingerprints completos pendentes**, **root map + holdout pendentes**, atribuição de writer material não comprovada. O segundo afirma 4/8 de F0, mas não enumera inequivocamente os oito sub-IDs com estados individualizados; logo **não inventei mapeamento exato 4 PASS/4 HOLD**. Os oito gates de EVIDÊNCIA citados nessa página são conceito contratual diferente dos 4/8 marcos F0.
- C01 entregou contribuição PARCIAL real a F1 (descoberta18 IDs), F2 (proveniência, anti-dup contra43 IDs conhecidos; um Party mirror excluído; versões/PS segregados), F3/F4 (quatro novos números completos e 297 fronteiras por RD numérica), F7–F12 (fronteiras e falsificadores), Q-MATH/Q-TARGET/Q-REDTEAM/Q-TRACE; **nenhuma fase terminal canonizada e nenhuma cobertura global alegada**.
- **Lote003: 0/71 unidades individualmente autenticadas**; título Notion de nova fonte não autentica pertencimento ao lote histórico. Corpus histórico R03+R04 29 ações numéricas mantido; o delta novo4 ações em duas páginas é conhecido não coincidente com os 43 IDs arquivados como conhecidos, mas **não comprova disjunção com os demais IDs de páginas antigas sem ledger completo**. Não houve soma oficial de população global.
- Classificação por RN da fonte, RE da habilidade, FIP e tipo elemental permanecem eixos distintos. Não existe candidato DMG v2 em uso.

## 10. Handoff VLAB e próxima fronteira

O `C01_VLAB_DELTA_READONLY.json` vincula o handoff imutável R10 sem duplicar e lista oráculos dos quais **nenhum foi executado nativamente pela DMG**. VLAB já possui R41 positivo e R42 negativo; não pedir rerun nem retrabalho. Permanecem AoO simultâneos sem precedência normativa, Luta específica do ataque NORMAL de Contra-atacar, valores individuais de iniciativa entre espécies diferentes, natureza e mitigação da reflexão e fonte de dados canônica terminal.

**Checkpoint DEPOIS:** R10 12/12 hashes preservados; R41/R42 CRC/manifest/standalone cold audit PASS; corpus novo18 páginas localmente reconciliadas, com escopo Mestre/Party preservado; 33 expressões exploratórias, 297 fronteiras aritméticas, 12.000 duelos MC locais, zero novos combates VLAB DMG, 0/17 contratos VLAB terminais, 0/1875 células, F0 4/8, L003 0/71, DMG-RANK v1.1 inalterada, NAC-PASS produtivo HOLD.

**Primeira fronteira verificável:** source-complete ranking e Luta dos dois novos atacantes numéricos (veado título Bronze4/corpo Bronze2 e Regalis Ouro2 corpo sem nome) em uma cena legal, mais resolução de tipologia RD, contra-ataque e iniciativa; se não houver autoridade, continuar taxa de lacunas e cross-rank sob amostra independente sem homologação. Preservar a numeração de 09/10 e usar `POST-R10-C02` para continuação desta mesma OP, não recriar DMG R11 antigo.
