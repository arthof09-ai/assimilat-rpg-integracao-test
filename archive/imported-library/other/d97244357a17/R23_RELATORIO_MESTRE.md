# VLAB R23 — BENCHMARK_AUTO / Relatório Mestre-side

**OP:** `OP-VLAB-FUSION-SANDBOX-01` · **data:** 14/10/2026 · **privacidade:** MESTRE-ONLY · **status:** EXPERIMENTAL / NÃO CANÔNICO · **certificação terminal:** 0/17.

## 1. Missão executada e evidência física

A diretriz corretiva expressa substitui a prioridade de UAT manual por **benchmark automatizado de confrontos completos**. Mantidos intactos R01–R22, inclusive R22 CHAT e R21 A1, SQLite, WAL, checkpoints e o checkpoint UAT dos Vigias revisão 1. **Nenhum novo turno dos Vigias foi executado.**

O R22 fonte veio da Biblioteca (`libfile_81c167d16b908191b92c615646bb532f`), ZIP SHA-256 `04ddf83ba2df69059a9f00f0f46e3bee24e9adbd59094400bf3671fd72942ca6`, 2.286 membros, CRC PASS. A versão R23 acrescenta `fusion_stage12/vlab_r23_benchmark_auto.py` + o lançador `INICIAR_VLAB_BENCHMARK_R23.py`, sem reconstruir resolvedor, scheduler, interface web ou gateway.

**Ponte real:** `BENCHMARK_AUTO` → `vlab_r22_chat_adapter.run()` → `vlab_r21_dynamic_a1.validated_step()` → R18 preflight v0.7 e resolvedor v0.8.1. O decisor automático usa somente `battle.available` **reaberto após cada commit**. O núcleo nativo, não o novo código, calcula os dados, acerto, reação, dano, Vida, PA e avanço de turnos; A1 registra ROUND_START/TURN_START/TURN_END/ROUND_END.

## 2. Método vigente reutilizado

Consulta read-only a:
- `OP-DMG-CORPUS-EMP-01`: https://app.notion.com/p/3f3c2b324ede813e9fa0c87ebdea0b29
- `DMG-METHOD-EMP-01`: https://app.notion.com/p/3f3c2b324ede81ab8d8ec1c7cce760b3
- `SIM-DMG-PAIRED-01`: https://app.notion.com/p/3f3c2b324ede818eaedafc5536adebf1
- `SPEC-SIM-DMG-VLAB-L00-L03`: https://app.notion.com/p/3f3c2b324ede81768b38d416ef3c9e3b
- `DMG-F1-RECON-LOT-001`: https://app.notion.com/p/3f3c2b324ede8123986ff96c1326c6ab

Mantidos denominadores separados por **célula, run, seed, fonte, regra e certificação**. O DMG define fontes, regras, admissibilidade e metodologia; o VLAB é executor restrito de ações nativamente resolvíveis. Célula de categoria sem dados suficientes é BLOCKED, nunca preenchida com fixture fictícia sem rótulo. Baseline atual antes de qualquer proposta v2.

## 3. Primeira bateria real: 16/16 combates técnicos completos

**Uma célula técnica, 0 células canônicas; 2 fichas fictícias Bronze 1 e 2 políticas × 8 sementes pareadas** `[11,23,37,41,53,67,71,83]`.

| Medida | Política BASIC_ATTACK | Política DEFENDER_IF_ELIGIBLE |
|---|---:|---:|
| Lutas completas | 8/8 | 8/8 |
| Bloqueadas ou censuradas | 0 | 0 |
| Vitórias fictício 1 | 1 | 0 |
| Vitórias fictício 2 | 7 | 8 |
| Ataques com recibo v0.8.1 | 49 | 50 |
| Defesa nativa | 0 | 16 |
| Vida removida total | 384 | 325 |
| Média de rodadas | 3,125 | 3,125 |
| Taxa de ataque acima CA básica | 100% | 100% |
| Débito PA positivo | 0 | 0 |

A CI de Wilson 95% condicionada à fixture e a **somente 8 seeds** para vitória do fictício 2 é aprox. `[52,9%, 97,8%]` no BASIC e `[67,6%,100%]` no DEFENDER. **Não equivale a intervalo de confiança do balanceamento canônico.** Reações não são renovadas automaticamente pela regra histórica delimitada; `DEFENDER` é no máximo uma vez por combatente nessa simulação. A precisão de acerto básica alta é efeito dos atributos altos de FOR versus CA artificialmente baixa, **não prova do Sistema de Assimilação.**

O relatório diferencia ataque que ultrapassou CA, reação DEFENDER que negou dano, bruto pedido, bruto recebido pelo núcleo, dano líquido nativo, Vida realmente retirada (cap HP), excesso, tipo do efeito, PA e recibo/hashes.

## 4. Sensibilidade controlada: 16/16 combates técnicos

Oito sementes iguais em duas configurações de personagens fictícios, política BASIC. Única diferença: `damage_bonus` do fictício 1 de **+4 → +7**. Outros atributos, Vida, cenário, política e sementes congelados. **8/8 pares concluídos; 7/8 mudaram o vencedor; delta médio de Vida retirada pelo ator 1 +5,875 por combate.** Cada variação de resultado pode alterar a duração e o número de ataques; a diferença total não deve ser atribuída linearmente a +3 em cada golpe. A medição demonstra procedimento de isolamento causal útil; **nenhuma arma, título, habilidade ou rank real foi testado.**

Total primário: **32 batalhas completas** (16 por política e 16 por sensibilidade), mais QA separado e 3 replays independentes não computados na amostra. A repetição de configuração entre experimentos **não cria uma nova fonte independente**.

## 5. Reprodutibilidade e intertravamentos

Cada run possui ID derivado da especificação congelada+política+semente, contexto de run, arquivo SQLite real, histórico de evento R22, cadeia A1, digest de estado, relatório e checkpoint ZIP de `chat.checkpoint()`. Especificações/bases não podem ser alteradas por nova execução; recibo terminal imutável impede repetir efeito confirmado. Após interrupção segura, ler estado e retomar somente novas revisões. Uma intenção pendente após queda **bloqueia** (`BLOCKED_UNCERTAIN_EFFECT`) sem aplicar nova mutação.

**3/3 replays de execução individual PASS** com cópias SQLite distintas: estado, cadeia A1, sequência de rolagens, recibos nativos, recursos, vitória e rodadas iguais. O hash da linha SQL das duas cópias pode diferir pelo caminho/ID físico do combate; comparar hashes entre cópias sem essa distinção daria um falso erro. Os hashes do próprio diário individual são revalidados inteiramente pelos verificadores R18–R22.

## 6. Limitações e fontes que NÃO foram usadas

A fonte atual `Galidemus Bronze 1` indica Patada `1d4+DES`, mas tem escopo `DOCUMENTARY_MATH_ONLY` e depende de admissão/proficiência/acerto, tempo, custo, alcance, defesa e adaptador nativo antes de FULL-FIGHT. Cabra de Chifres Bronze1 tem lacunas no empurrão; Raposa Flamejante Bronze2, na Bola de Fogo e rastro. **0/3 fontes documentais piloto elegíveis para um full-fight R23; 0 combates com fonte canônica.** Não foi usado `Jaku × Dragão` nem alterada IBX-90. O compilador DMG R30, caso disponível em versão legitimamente congelada, poderá alimentar o pré-flight; nenhuma ação R30 é reivindicada como nativamente integrada hoje.

| Cobertura | Planejada/documentada | Elegível canônica | Executada canônica |
|---|---:|---:|---:|
| Posições rank/estrela | 25 | 0 | 0 |
| ED×ED (ordenadas) | 625 | 0 | 0 |
| ED×BE | 625 | 0 | 0 |
| BE×BE | 625 | 0 | 0 |
| **TOTAL células centrais** | **1.875** | **0** | **0** |
| Fixtures técnicas isoladas 1×1 | 1 | 1 (somente laboratório) | 1 |

**Suportado no BENCHMARK_AUTO R23:** dois combatentes fictícios, seed isolada, iniciativa sem empate, ataque padrão 1d6 de fixture, DEFENDER 0PA, fim por HP zero local, limiar de rodadas e limite de eventos, determinismo por política, histórico e checkpoint. **Não suportado nem simulado:** ação real de personagem/besta, multigrupo, equipamento e RI/FIP real, magia, passiva, transformação, controle, DOT, crítico canônico, buff/debuff, gasto positivo PA, renovação normativa da reação, desempate de iniciativa, precedência simultânea e cobertura Lendário/ADM/Titã/Divina. Em pedidos que dependam destes itens, HOLD explícito e fonte não imputada.

## 7. QA, preservação e estados de governança

**56/56 testes distintos PASS por grupos:** R18–R21 35; R22 12; R23 9. Uma invocação monolítica inicial da suíte R22 excedeu timeout após 5 PASS; os 12 casos foram *posteriormente reexecutados em grupos* de 5+2+5 PASS, sem inflar numerador. R23 inclui teste real de processo terminado entre intent e commit e recusa de reaplicação.

**UAT dos Vigias congelada:** combate `vlab_54b9a268bf9e492c85a24fa4963bac10`, revisão 1, checkpoint Biblioteca `libfile_ce5587e0cafc819182a0c8955aaca966`, SHA `41f832a0bd01eab35c9269cd2985e36b3158537062d54700575cf4c693128fd3`; R23 não alterou seu combate nem leu/modificou decisões futuras.

Permanece: VLAB certificados terminais 0/17, DMG 1/18 conforme ordem do Mestre, STRICT 0/2, IBX-56 BLOCKED-EXTERNAL, IBX-90/91/92 sem ACK assumido, gateway/writer/lease/epoch/fencing/GREEN/NAC-PASS produtivo HOLD. Nenhuma escrita no Notion, fontes canônicas, Party, O Primeiro ou fichas oficiais. Sem reivindicação de auditoria científica ou certificação de produção.

## 8. Ponto exato de retomada

**P0 próximo:** consumir contratos congelados do compilador legal DMG e reconciliar pelo menos **uma** habilidade/ação de Besta real até os critérios completos `actor snapshot + custo/ação/alcance + ataque/defesa + mitigação + nativo + recibo`; executar primeira célula canônica elegível somente após gates aplicáveis, mantendo artefatos anteriores intactos. **P1:** avançar adaptador de múltiplos participantes sobre o scheduler A1 histórico, sem reimplementar a física; grupos 2×1 e 3×1 condicionados às mesmas fontes. **P2:** expandir por 25 posições e 1.875 células da matriz pré-registrada com combate pareado baseline ANTES antes de propostas. **Não retornar ao fluxo de Mestre comandar ataque a cada turno.**
