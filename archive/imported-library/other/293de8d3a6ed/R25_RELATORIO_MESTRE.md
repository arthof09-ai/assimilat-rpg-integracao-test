# VLAB R25 — Primeira bateria RULE-DERIVED-VIRTUAL vinculada às regras vigentes

**MESTRE-SIDE / CM-000006 lógico / OP-VLAB-FUSION-SANDBOX-01 / sem INSTANCE-ID, writer, lease ou NAC-PASS de produção.**

## 1. Veredito executivo

**ENTREGA DE ENGENHARIA CIENTÍFICA CONDICIONAL, NÃO PRIMEIRO COMBATE CANÔNICO.**

- A R24 foi recuperada e os 2.516 membros do ZIP original preservados para inclusão aditiva. Todos os motores R01–R24 permanecem inalterados; é reutilizado o mesmo `RebuiltManualRuntime`/v0.8.1, v0.7, A1 e o WAL/SQLite do R18–R22.
- **8 sementes pré-fixadas, 5 confrontos concluídos em HP 0, 3 censurados antes da intenção; 94 ataques nativos, 283 eventos A1.** Todos com dois arquétipos bestiais virtuais **não canônicos**, usando regras atuais de Besta Bronze 1, com hipóteses experimentais explicitadas. Nenhuma batalha dos Vigias ou fixture R23 foi reexecutada na bateria nova.
- **0 ações da Galidemus integralmente admitidas, 0 eventos legais completos de entidade real, 0 confrontos de duas fontes reais e 0/1.875 células canônicas.** O ganho é medição executável do subconjunto matemático do sistema vigente com RD efetiva e stop/censura apropriados, não promoção de canonicidade.
- O termo **BASELINE** significa aqui *medição preliminar condicionada às hipóteses da fixture*. **Não** designa baseline canônica já aprovada para futura comparação DMG ANTES×DEPOIS.

## 2. Fonte e rastreabilidade

Autoridades Mestre-side reabertas em Notion (READ ONLY):

1. [Sistema de Combate](https://app.notion.com/p/3ebc2b324ede81f1be4be8804ac113c0), editado 07/10/2026 23:51Z: ataque padrão 1 Ação Padrão, teste por rank + atributo Luta + bônus Luta; iniciativa rank+DES; uma Reação por turno, defesa anunciada antes do ataque; crítico/falha crítica dependem de sequência de 3d6.
2. [Criação de Besta](https://app.notion.com/p/3ebc2b324ede81f4992ac88a3588cacd), editado 07/10/2026 20:58Z: Besta normal Bronze 1, pontos 35+8, proficiência Bronze +6, Vida/Alma, CA, RD Bronze 5, dano-base especializado **3d6**.
3. [Plano Mestre VLAB](https://app.notion.com/p/3f3c2b324ede81d480dbf11732734463): são exatamente duas finalidades — pesquisar dano vigente e potência de Bestas/combatedores; modalidade RULE-DERIVED-VIRTUAL existe; distinção entre 1.875 células centrais e runs locais.
4. [Galidemus Bronze 1](https://app.notion.com/p/eddc2b324ede829f8a75011e8acbf429), editado 01/10/2026 18:00Z: `Patada: 1d4+DES13 cortante`, FOR5, CA21, HP32, Alma32.
5. [Cabra Bronze 1](https://app.notion.com/p/391c2b324ede8252b0cc810423cdbfa6), editado 01/10/2026 18:00Z: CA20, FOR13, Investida `1d6+FOR` **com empurrão obrigatório**, ainda sem distância/consequência resolvida.
6. [DMG-RANK-01 v1.1](https://app.notion.com/p/3f2c2b324ede815498cddb7844245f7e): dano explícito/sistema de Besta prevalece sobre fallback universal. **Nenhuma fórmula desta norma foi alterada**.

O ZIP preserva os recortes observados de R24, com hashes **da transcrição**, não assinatura de fonte original. A camada técnica usa hashes de configuração/evento, e não declara autoridade Notion delegada.

### 2.1 Reutilização do L04 antigo

`working/historical_v081_verified_original/comestre_vlab/vlab_l04.py` **já continha** o gerador RULE-DERIVED-VIRTUAL. A R25 **não o canoniza**: o L04 marca a Besta gerada como `missing_for_full_fight` em proficiência/precisão, contrato de ataque, reação, posição, tática e PA. `pa_total` é `None` no L04, apesar da Alma calculável. Estes gates **continuam pendentes**. A R25 usa combinações próprias de atributos legalmente compatíveis com o orçamento, mas não declara que substituem o L04/essa pendência.

## 3. Experimento executado

**Dois atores completamente virtuais, ambos Besta normal Bronze 1 (sem traços, itens ou magias), com alocação de 43 pontos cada.**

| Fonte de valor | Besta Virtual A | Besta Virtual B |
|---|---:|---:|
| FOR/DES/CON/INT/SAB/CAR | 17/6/10/4/3/3 | 12/11/10/4/3/3 |
| Vida = 30+1(10+CON) | 50 | 50 |
| Alma pela fórmula de Besta | 44 | 44 |
| CA = 10+DES+CON/5 (inteira) | 18 | 23 |
| RD geral | 5 | 5 |
| Dano-base por ataque físico normal | 3d6 | 3d6 |
| Teste de iniciativa | 1d6+DES | 1d6+DES |
| Teste de Luta na fixture | 1d6+FOR+6 | 1d6+FOR+6 |

**Condições que impedem promoção à baseline estritamente canônica:** atribuição de +6 da tabela de proficiência da Besta à Luta **é uma escolha de laboratório não individualmente atestada**; o pressuposto de ação normal sem gasto positivo de PA é restrito ao módulo experimental e **NÃO prova custo zero de Patada**; PA 44 foi inicializado pela Alma calculada, embora seu mapeamento oficial não esteja atestado no L04; o tag `impacto` é exigência técnica do contrato R20 e **não tipo oficial demonstrado da fonte de dano-base genérico**; o posicionamento é adjacência fixa escolhida; reações foram **voluntariamente não declaradas**, sem desativar o slot; efeitos de crítico/falha crítica são **censurados antes da mutação**, nunca aplicados por aproximação. Não há personagem/espécie canônica representados por essas alocações. O encerramento HP=0 é contrato do **laboratório**, não adjudicação da morte canônica.

### 3.1 Métricas observadas

| Indicador | Valor | Denominador |
|---|---:|---:|
| Sementes executadas | 8 | 8 registradas previamente |
| Combates condicionais concluídos | 5 | 8 tentativas |
| Censuras | 3 | 8 tentativas |
| Ataques aplicados pelo v0.8.1 | 94 | 94 eventos de ataque |
| Ataques que superaram CA | 94 | 94 ataques (escolha de atributos causa acerto garantido) |
| Dano bruto dos ataques acertados | 986 | 94 |
| RD nominal encontrada nos acertos | 470 | 94×5 |
| Dano mitigado de fato | 467 | 94 eventos (excede dano em algumas rolagens baixas) |
| Dano líquido dos recibos nativos | 519 | 94 |
| Vida efetivamente retirada | 503 | 94, considerando HP remanescente |
| Overkill | 16 | diferença de dano líquido e Vida efetivamente retirada |
| Eventos A1 | 283 | 8 runs |
| PA debitado | 0 observado | 8 runs; não certifica custo real de habilidades |
| Rodadas médias nas cinco conclusões | 8,8 | 5 conclusões |
| Vitórias A/B no subconjunto concluído | 2 / 3 | 5; **3 censuradas não são derrotas** |

Os 94 acertos não significam que Bestas Bronze 1 acertam 100% universalmente: sob estas duas alocações, **o mínimo ataque de cada um já supera a CA do outro**. Isso caracteriza a configuração, não uma descoberta global de equilíbrio. Cinco desfechos não sustentam diagnóstico estatístico amplo nem IC representativo. A variável *tipo de dano* permanece placeholder, ainda que RD geral não dependa do tag nesta fixture; o mecanismo geral RD simples é baseado na decisão do Mestre registrada no plano, com canonização normativa documental pendente.

**Censuras auditáveis:** semente 41 — empate da iniciativa, nenhuma ação ou evento; 71 — gatilho de crítico positivo identificado antes da intenção; 83 — gatilho de falha crítica identificado antes da intenção. Foram preservados banco/recibo/checkpoint de todos os oito casos, sem imputação de vencedores.

**Replay:** semente 11 reproduzida em novo diretório: **mesmos 17 ataques nativos, 51 eventos A1, hash de cadeia, eventos, vencedor, Vida final e bytes do SQLite**. Exportação e restauração portátil foram validadas. Cada caso tem recibo `.json`, estado `.sqlite` e checkpoint `.zip` sob `reconstruction/r25_delivery/`.

## 4. Galidemus: bloqueio reduzido a um quadro mecânico específico

No **Sistema de Combate** o ataque normal usa normalmente FOR; DES no teste de Luta só quando arma/estilo o permite. A ficha declara DES **no dano** da Patada, não na precisão. Aplicando a regra geral sem exceção inventada:

- FOR5 e Bronze 1d6, bônus individual de Luta ainda pendente. Com +0, máximo de acerto=11. Mesmo assumindo condicionalmente todo +6 da proficiência Bronze na Luta, máximo=17.
- A CA da Cabra Bronze 1 é 20; a própria Galidemus tem CA21. Logo **esses ataques básicos não podem superar essas CA** sem buff, vantagem, habilidade diferente ou modificação legítima. O analisador existente `vlab_rd_v08.possible_basic_hit` confirmou os quatro casos.
- Patada é `1d4+DES13` **cortante** (bruto máximo 17); a RD Bronze normal é 5, produz máximo líquido 12 **se houver acerto**. Não autoriza acertar automaticamente nem transforma DES em perícia de Luta.
- Cabra não permite contornar o problema substituindo Investida por golpe sem empurrão; Raposa requer o efeito integral de Bola de Fogo e Passos Flamejantes. Fonte real individual ainda não tem envelope C/D/E integralmente comprovado.
- Não foi executado ataque real nativo adicional neste lote. O ensaio R24 de dano condicionado permanece histórico. **0 eventos legais de fonte real são contados.**

**Pendências específicas:** (a) proficiência da fonte aplicada ou não à Luta natural; (b) enquadramento de Patada como ataque padrão genérico e custo de PA/ações quando for habilidade especial; (c) posicionalidade do golpe e destinatário; (d) reação e efeitos críticos/falha crítica integralmente implementados; (e) ficha corrente vs fórmula geral HP/Alma/CA e snapshot source-native/epoch; (f) recebimento, gate E e commit independente de contrato real DMG. **DMG/source-owner** reconcilia corpus e identidade; **Mestre/NAC-NORM** decide divergência normativa genuína; **VLAB** prova v0.8.1/SQLite no evento completo após admissão.

## 5. Única decisão normativa sobre DEFENDER

A regra vigente diz **uma Reação por turno** e declaração defensiva **antes do ataque**; o v0.8.1 consome o slot uma única vez. A R18/R23 **não renova** esse slot. Fonte consultada não determina inequivocamente o marco do refresh para defesa **durante o turno alheio**. Este é o mesmo assunto da **IBX-92**; nenhum pedido duplicado foi criado.

**Pergunta reservada ao Mestre:** quando uma Reação gasta volta a ficar disponível para o combatente? **(A)** na abertura de seu próprio próximo turno; **(B)** na abertura de cada nova rodada para todos; **(C)** outro instante definido expressamente. A e B divergem quando o personagem é atacado antes de seu turno ou em múltiplas janelas. Até decisão formal, as reações defensivas seguem HOLD para baseline canônica. R25 fez **não uso voluntário** em vez de impor uma reação por combate.

## 6. Integração R31 e governança

R31 fornecedor original indicado: `libfile_03db9a6705b08191ad5347c55332207c`. A materialização binária continuou indisponível pela superfície Project raw; o texto do fornecedor R31 já recuperado no R24 e os cinco gates foram preservados. **0 envelopes reais assinados consumidos**, 0 ações despachadas com R31, nenhuma autorização via campo `PERMITIDA`. Conflitos/solicitações IBX-56/90/91/92 preservados; a IBX-92 e a IBX-91 foram reabertas, ambas `NOVA`/sem ACK verificado. Nenhum writer, lease, epoch, fencing ou GREEN novo foi reivindicado.

**0/17 certificações VLAB; DMG 1/18; STRICT 0/2; 0/1.875 células canônicas; 0 alterações em DMG-RANK, Bestas, Party, O Primeiro ou fichas oficiais.**

## 7. Prova de software e continuidade

- 430/430 verificações dirigidas R25 aprovadas (incluem verificações por ataque, não são 430 testes unitários independentes).
- Regressão R24: 14/14 unidades reexecutadas nesta rodada. A versão anterior R24 tinha 15 ensaios relatados incluindo CLI smoke; **não** inflar este denominador a 15. Regressão R23: 9/9 unidades reexecutadas. Sem repetição das 32 lutas históricas.
- Checkpoints R25: 8/8 exportados, reabertos, hashes confirmados; restauração em novo SQLite sem sobrescrever a origem demonstrada.
- Eventos antes/depois, source reference, procedimento de escolha, `hit`/RD/dano e HEAD persistidos. Falha de inicialização durante desenvolvimento gerou WALs de QA em quarentena, **não republicados como batalhas**; no lote final empates/críticos são censurados **antes de gravar a intenção**.

**Ponto exato de retomada:** usar R25 B1 derivado para verificar variação de bônus/CA sob gate consciente (não alterar marco de ciência); obter da autoridade o marco de renovação de Reação, e do corpus uma confirmação específica do acerto/custo/alcance da Patada; somente então executar uma ação **integral** de Galidemus e dar 1 crédito de fonte real. Não avançar em 2×1/3×1, nem criar novos adaptadores genéricos antes disso.
