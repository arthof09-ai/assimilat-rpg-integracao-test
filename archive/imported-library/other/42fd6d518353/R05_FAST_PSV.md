# PSV R05 — FAST-RESEARCH — OP-DMG-CORPUS-EMP-01

**15/10/2026 | MESTRE-SIDE | MATH_ONLY | DMG-RANK-01 v1.1 inalterada**

**Hipótese única:** uma diferença pequena na precisão pode inverter a eficiência líquida de dois ataques físicos, mas RD alta pode reverter essa inversão.

**Fonte atacante:** página oficial Símio Demoníaco, id `301c2b324ede828caccb813d3979267a`, título/corpo Prata5 (titã)/Prata5 e árvore Ouro Negro5 **em conflito**. Patada `2d6+FOR54` impacto; Mordida `1d6+FOR54` perfurante. Ambas físicas com RD genérica comum, na ausência de resistência diferencial. **Alvo:** Behemoth Glacial Ouro1, id `5dac2b324ede83f39cdb01a904ce3cfd`, CA68; RD25 apenas se normal Ouro sem modificadores especiais. Sua Armadura de Gelo documenta +3CA quando ativa, 20PA ativação e 3PA por turno de manutenção; reflexão de 15% do dano físico recebido precisa contrato de resolução. Não se conhece a economia de ação completa de ativação.

**Parâmetros contrafactuais declarados (NÃO são bônus oficiais):** Patada `Luta+6`; Mordida `Luta+7`. Ataque Prata `2d6+FOR+Luta`, supera CA estritamente. Independência dos dados de dano e do acerto; sem crítico, reação, reflexão, terreno, buffs ou resistência física por subtipo.

| Cenário | Patada por acerto | Mordida por acerto | P Patada | P Mordida | E por tentativa Patada | E Mordida |
|---|---:|---:|---:|---:|---:|---:|
| CA68, RD25 | 36 | 32,5 | 10/36 | 15/36 | 10 | 325/24 = 13,5417 |
| CA68, RD35 | 26 | 22,5 | 10/36 | 15/36 | 65/9 = 7,2222 | 75/8 = 9,375 |
| CA68, RD50 | 11 | 7,5 | 10/36 | 15/36 | 55/18 = 3,0556 | 25/8 = 3,125 |
| CA68, RD51 | 10 | 6,5 | 10/36 | 15/36 | 25/9 = 2,7778 | 65/24 = 2,7083 |
| CA68, RD55 | 6 | 2,5 | 10/36 | 15/36 | 5/3 = 1,6667 | 25/24 = 1,0417 |
| CA71, RD25 | 36 | 32,5 | 1/36 | 3/36 | 1 | 65/24 = 2,7083 |

**Verificado matematicamente:** mesma precisão e mesmas condições de ação implicam dominância da Patada sob qualquer RD escalar comum: Patada = Mordida + 1d6, acoplável estocasticamente. Sob os bônus **hipotéticos** diferentes, a vantagem por tentativa pode migrar para Mordida em RD25, e voltar à Patada em RD51. CA +3 da Armadura causa queda no acerto, mas a ativação não foi admitida como evento nativo.

**Balanceamento:** comparar só o dano bruto aprova incorretamente a melhor habilidade; precisão e RD devem integrar a decisão. Nenhum destes percentuais pode ser atribuído à criatura real enquanto Luta, subtipos, crítico, reação e ações não forem documentados.

**ANTES:** R04, 29 fórmulas em 53 páginas Mestre, 93/93 testes; Lote003 71 relatadas, 0/71 individualmente autenticadas. **DEPOIS:** R05, 1 hipótese, 2 habilidades da mesma página, 1 alvo de fonte real, 16 cenários exatos, testes locais e readback; nenhuma nova página aberta ou escrita Notion; F0 4/8, L003 0/71, R01–R04 preservadas, writer/NAC-PASS em HOLD.

**Próximo experimento executável:** obter bônus Luta documentados de duas habilidades físicas e testar contra mesmo alvo com `CA68` e Armadura de Gelo ativada, incorporando o custo defensivo e a reflexão sem inventar contrato. Até lá, VLAB caso `MATH_ONLY`; não foi enviado automaticamente ao VLAB nem houve combate novo.

**Checkpoint:** `R05_RESULTS_FAST.json` + `R05_REPLAY_FAST.py`, arquivos novos no diretório existente `r04/`, sem ZIP novo e sem sobrescrita de R01–R04.
