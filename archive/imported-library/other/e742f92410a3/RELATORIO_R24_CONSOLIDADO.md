# OP-DMG-CORPUS-EMP-01 — R24 | Relatório científico: prova empírica independente

**CM-000001 · R24 · MESTRE-SIDE · decisão normativa 0/5 · NAC-PASS HOLD.**

## 1. Verificação e preservação
R23 original SHA-256 `b9e81b0c6744c9d60830bee4d557d9dd7df312ab134562b3b9bc8bfc1d9cbac2` validado por recuperação limpa (24 membros ZIP, 23/23 hashes, 33/33 testes R23 e herança de 34/34 R22 e 36/36 R21), preservado como `R23_ORIGINAL_READONLY.zip` neste pacote; `r13_oracle.py` copiado sem mudança de bytes. 0 escrita em Notion, Party, Primeiro ou VLAB. Registro Notion e Diário permanece **PENDENTE DE SINCRONIZAÇÃO** pela ausência de writer/instância legítimos; a ordem do Mestre não aprova as cinco decisões anteriores.

## 2. B15: evidência nova e teste condicionado
**FONTE VERIFICADA:** ficha Mestre Ong Natsu `<https://app.notion.com/p/f77c2b324ede823892ea01513a35f1b4>` descreve soqueira `3d6+6`, Punhos de Fogo `+2d6` Fogo `14 PA`, Infusão Flamejante `+1d8` (outro efeito). **FONTE VERIFICADA:** Dragão de Gelo Azul `<https://app.notion.com/p/4fac2b324ede824da70d0189f19533de>` declara Ouro 1, Vida 523, CA39 e vulnerabilidade a **ataques mágicos baseados em Fogo**. Fonte regra: Sistema Combate §11 e DMG-RANK v1.1 §§21,22,32.

**COLISÃO DE CONTINUIDADE REAL:** página no espelho Party do mesmo nome `<https://app.notion.com/p/6adc2b324ede82fbbc28016d86c4bdb2>` tem título `Ong Natsu (Filho do Chefe) (Morto)`. Não há recibo de morte nem `effective_at`. Isso NÃO prova cronologia, porém impede declarar Ong disponível para evento futuro. A ficha Mestre possui variantes P3/P4; seus itens não são entidades independentes nem se empilham automaticamente.

**HIPÓTESES NÃO PROVADAS:** (a) o dano `3d6+6` de soqueira deve possuir tag física declarada, não apenas inferida; (b) Punhos de Fogo atua em conjunto com a soqueira, sem somar ilegalmente `+1d8 Flamejante`; (c) o golpe se qualifica como *ataque mágico de Fogo* para ativar a fraqueza específica do Dragão; (d) o ator está legalmente disponível no `scene_epoch`; (e) PA, acerto, reação, mitigação e estado final precisam ser comprovados.

**ENSAIO CONTROLADO NÃO CANÔNICO**, apenas para verificar aritmética sob as condições (a–c): 3d6 `[4,2,5]` +6 =17; Fogo 2d6 `[4,3]`=7; fraqueza +3d6 `[2,5,6]`=13; bruto sem fraqueza=24; bruto condicional=37; variação=+13 **apenas Fogo**. Médias exatas calculadas pela enumeração finita do oráculo R13: 23,5 e 34,0; delta esperado +10,5. Estes dados são escolhidos por script, NÃO rolagens de combate; HP líquido fica UNKNOWN sem RD/mitigação e recibos. Sem fraqueza demonstrada, sem tag de Fogo ou sem golpe mágico elegível, o bônus deve ser recusado.

A combinação física+Fogo nesta ficha é **candidata**, não comprovada como uma mesma ação legal. Também não se pode simplesmente chamar `+1d8 Flamejante` de `Fogo` ou preservar dano-base físico após uma infusão sem conferir o texto específico. Protocolo R23 preservado como instrumento de coleta. **PASS B15 = PENDENTE**, eventos reais recuperados=0. Execução futura só no operador legal CM-000006 e após congelar fonte, autorização, estado e recibos; nenhum ensaio é combate STRICT.

## 3. Reavaliação independente B01–B18
Matriz `R24_MATRIX_18.csv` e `.json` preserva predicados originais. Resultado: B02 PASS documental; B01/B05/B06/B08/B09/B11/B12/B15/B16 PARTIAL; B03/B04/B07/B10/B13/B18 BLOCKED; B14/B17 NOT-TESTED integral. Nenhuma fonte documental desta rodada fecha um predicado de evento além de B02 já certificado. Testes de cálculo não são certificação.

- B01 fonte atual e congelada faltante; B05 ação legal/adapter; B06 custo e janela real; B08 ataque/hit com mods; B10 RD e dano misto com estado; B13 geometria; B16 transformação; B18 replay legítimo.
- B11 e B12 seguem com DEC-B11-A/B/C e DEC-B12-A/B **PENDENTES**, sem deliberação antecipada.
- B14 proteção Behemoth requer evento, ordem RD/reflexo e arredondamento. B17 exaustão e condição final requer evento e autoridade de fim de combate.

## 4. Liu/STRICT/CSV
Sem identificador de cena novo Liu × Macaco, **nenhuma busca negativa repetida**. B04 BLOCKED; B09 PARTIAL; `Perdido -46` sem fonte temporal; não há ledger real de PA, Reação, defesa e rolagens. STRICT **0/2**, não houve combate canônico/experimental executado por CM-000001. CSV I0003 originais **0/9**, nenhuma pista nova de path/hash, sem revarrer 47 CSV/114 ZIP. Corpus derivado 198 IDs, 46 ocorrências/20 páginas mantido sem novo censo.

## 5. Comparação R23 → R24
**NOVO:** (i) par NOMINAL de fonte de atacante/arma/buff e alvo com vulnerabilidade expressa a Fogo; (ii) fonte comparativa mostra Ong marcado Morto, descobrindo risco de invalidade temporal da cena prospectiva; (iii) ensaio auditável com pools de dados escolhidos e média exata, em que falta dano líquido por falta de RD/resultado; (iv) blockers de B15 transformados em verificação de elegibilidade, não mais só em pesquisa genérica. **NÃO OBTIDO:** evento efetivo, novo PASS, CSV bruto, ledger Liu, combate STRICT, aprovação das cinco decisões.

## 6. Próximo ato concreto
Reconciliar status vivo/morto e `effective_at` de Ong antes de propor cena. Se morto no estado escolhido, selecionar **outro ator efetivamente elegível**, sem ressuscitar/falsificar cenário. Verificar natureza física da arma e autorização de combinar Punhos de Fogo com soqueira; resolver RD/reação/PA do alvo e preparar episódio prospectivo **somente se autoridade do Mestre + executor CM-000006 permitirem**. Recolher evento de fonte real, separar rolagens física/Fogo, snapshot pré/pós e conferir em readback. Não converter evento isolado em FULL FIGHT STRICT. Decisões B11/B12 aguardam Mestre separadamente.

## PSV terminal R24
B02 1/18 = 5,56% documental certificado (não inteiro 5,56/18); 9 PARTIAL; 6 BLOCKED; 2 NOT-TESTED; 0/2 STRICT; 0/9 I0003; decisões 0/5; NAC-PASS terminal HOLD. Diário/OP/Inbox sem escrita e ACK não comprovado; evidências preservadas em sandbox independente, sincronização pendente de writer válido.
