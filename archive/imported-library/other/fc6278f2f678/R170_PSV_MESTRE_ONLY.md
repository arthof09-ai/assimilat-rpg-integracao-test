# PSV — VLAB R161–R170 | Motor nativo e ciência experimental

**AS-OF:** 17/10/2026 (America/Recife)  
**OPERATION:** `CM-000006 / OP-VLAB-FUSION-SANDBOX-01`  
**AMBIENTE:** MESTRE-SIDE, desenvolvimento de cópia controlada  
**BASELINE:** R01–R160 intacta, importada do ZIP R160 SHA-256 `7b208fe553809df6a999a1e4f9a70d7ad116033e929256bc71dbcd61843f3410`  
**PRODUÇÃO:** HOLD, sem writer/lease/epoch/fencing/INSTANCE-ID/ACK IBX-101.

## ANTES → DEPOIS, sem falsificação de escopo

**ANTES R160:** motor v0.8.1, R18/R26, R42 LAB-ONLY, R43, Casulo com CA+22, dano físico/PA e 154 recibos de nove bancos. Três recibos categorizavam dano pós-RD como Vida perdida quando o alvo alcançava zero. R150 histórico de readback e R138 espacial em HOLD preservados.

**DEPOIS R170:** classificador prospectivo de recibos baseado nos campos efetivos do estado nativo; Flecha de Trava com modificador real de −6m até o fim expresso do próximo turno; Casulo original com CA+22 e velocidade −4m aplicados juntos, duração exata ainda HOLD; duas cadeias de AoO R43/R42 com KO interrompendo movimento, e dois duelos completos adicionais Auren L3 × Crocodilo L3 condicionado em política básica física. Cada nova execução tem RUN-ID único, ledger R18, prereg de desenvolvimento, checkpoint e auditor independente de dados, eventos e estado.

### R161 — Integridade histórica e reconciliação 154/154

Reabertura **dos nove bancos R160** e dos 466 commits, cadeia hash física íntegra, sem modificar originals. Sobre o agregado antigo: pós-RD **11.870**, Vida retirada **11.808**, overkill **62**. Produtor antigo registrava 11.845 como Vida retirada — excesso **37** em três golpes finais (R157 BASIC 13, R157 WIND 13 e R158 11). Fonte documental do ZIP de auditoria da Coordenação não foi assumida; reconciliação produzida diretamente dos bancos.

### R162 — Correção da exportação, não do resolvedor

`r162_receipt_producer_v1.py` aceita somente recibos nativos completos: `real_lost = before_HP − after_HP`, `post_RD = max(0, raw − RD)`, `overkill = post_RD − real_lost`, com auditoria de limites e rejeição de inconsistências. Saída histórica **NOVA**: `R162_CORRECTED_RECEIPTS_R160_HISTORICAL_UNMODIFIED.csv` (154 linhas, sem alterar arquivo exportado originalmente). Testes diretos: 6 aritméticos + 2 adversariais, e 4 asserts adicionais de salvaguarda em `R162_MAGIC_SAVE_SEMANTICS_READONLY.json`: no R159 original, dano bruto dos 14 dados 74, dano nativo **pós-salvaguarda/pré-RD 37**, Vida retirada 37; metade ímpar recusada sem arredondamento. O campo `raw` nativo não é sempre o dano antes da salvaguarda.

### R163 — Fencing contra duplicação de efeitos após falha

Bancos novos: `R163_FRESH_AFTER_INTENT_S1163103` com **0 eventos / 1 intenção pendente / UNKNOWN_EFFECT-HOLD**, estado intacto, sem replay; e `R163_FRESH_AFTER_COMMIT_S1163104` com **1 evento commit único / 0 pending**, pós-RD 100, Vida retirada 30, overkill 70. Falha de publicação do CSV não reverte/reexecuta o commit. Um diagnóstico anterior com comando impróprio foi segregado (`R163_AFTER_INTENT_S1163101`, nenhum evento). Não é combate.

### R164 — Autoridades de dano e Bestas, com HOLD localizado

- Grifo-Matriarca Sílica L3, fonte `BEAST-FULLSPEC-VZ-06`: Vida 4.315, CA 153, RD 75, DES 116, Prof geral +22; **NÃO há prova de Prof específica de Iniciativa**. Descarga Curta 55 PA, 14d10 Lightning, Ref CD 94, “linha curta”, **sem distância métrica explícita**.
- Auren L3: Vida 523, CA 225, RD física 35, RD Dark 60, Iniciativa 6d6+166 comprovada; RD Lightning **não documentada**, não imputar zero.
- Crocodilo de Lodo Astral Ancião L3: Vida 5.580, CA 112, RD 75, DES 64; mordida 6d6+134 e 20d10 físico, iniciativa natural específica **não demonstrada**. Mistura impacto/Água e tipo de dano indecomponível ficam HOLD individuais.
- Feryn/Eristan possuem RD física; RD elemental Vento/Planta não determinada no corpus inspecionado. Não importar não-resistência por silêncio da ficha.

Fontes diretamente reabertas no Notion Mestre: Sistema de Combate, Sistema de Magia, Criação de Besta, BEAST-FULLSPEC-VZ-06, P3-01 Grifo, SPIRIT-BEAST-RUNTIME-VZ-08, Auren, Feryn, Eristan, Varok, Iskiel, OP original R42/R43. Esse readback é **documental**, não hash de congelamento binário da fonte canônica.

### R165 — Efeito temporal que realmente altera deslocamento

Flecha de Trava, Sikong Iskiel: 55 PA, ataque documentado Luta DES vs CA com alcance 65 m, dano físico; **−6 m até o fim do turno seguinte**. Cena dirigida **R165 V3 seed 1185114**: 7 commits, evento positivo crítico da Flecha com dano físico legítimo, velocidade de Auren **16 → 10 → 16 m**; movimento de 9 m válido, tentativa de 11 m rejeitada antes da intenção, encerramento do próximo turno remove o modificador. Auditor frio reproduziu RNG, Vida, PA, ações, speed e hashes; checkpoint do estado ainda ativo reaberto.

R165 V1 (4 commits, sem pending) e V2 (4 commits +1 pending) são **diagnósticos não aprovados**, V2 UNKNOWN_EFFECT/HOLD. A duração do Casulo “2 turnos” permanece **HOLD sem inventar expiração**.

### R166 — Duas oportunidades concorrentes durante Casulo

Fixture técnica de quatro fichas distintas (Eristan, Auren, Feryn, Varok). Casulo custa 60 PA, dá CA Auren **225→247**, velocidade **16→12 m**. Prioridade R43: Feryn DES80 antes de Varok DES29. Duas cenas discriminantes **R166 V2**:

- `R166_V2_CASULO_AOO_NEGATIVE_DEV_S1195557`: cinco commits, Feryn R42 `1→1→2` falha automática e 0 dano, Varok segundo AoO não acerta, ambas Reações consumidas, Auren sai por caminho métrico de 1,5 m explicitamente fornecido.
- `R166_V2_CASULO_AOO_KO_DEV_S1205088`: cinco commits, Auren inicialmente ferido em fixture HP 60 (máx 523); primeiro AoO Feryn `6→6→6` crítico positivo, 114 pós-RD, **60 HP reais, 54 overkill**; Varok não ataca, Reação dele permanece **1**, Auren não se desloca.

Auditor frio independente do resolvedor recomputou 10/10 commits e fitas RNG. PRIMEIRA tentativa R166, seed 1195392, teve 1 commit e 1 intenção pendente porque adaptador de fonte incompleto, **UNKNOWN_EFFECT/HOLD, jamais retomada**. V2 usa seeds e identidades novas, código corrigido.

### R167 — Segundo ED e C-team

Sete candidatos concretos examinados: Auren (fonte útil como ED 1), Sikong Hongyue (Espírito em branco), Pan Tueimor (Espírito não comprovado), Sikong Yip (lore sem combate fechado), Sel-Myr Ivara e Kael Soryn (literais `MECH-PENDING`) e Nym Rhae (`MECH-PENDING-RACE`). **Segundo ED admitido: 0** neste lote, não censo do Notion inteiro. Feryn/Eristan/Iskiel/Varok sem Espírito: NPCs técnicos, não contam ED para A/C.

### R168 — Duas batalhas completas NOVAS ED × espécie Besta distinta

Auren Lendário3 × **Crocodilo de Lodo Astral Ancião Lendário3** (distinto do Grifo); fonte besta `BEAST-FULLSPEC-VZ-06` + dossiê P3-02. Política fixa: ataque básico físico efetivo quando ator vivo e em alcance experimental controlado, sem abdicação deliberada. Abertura exógena de Besta por Iniciativa específica ausente. Seeds **1168001 DEV e 1169001 RESERVADA NÃO CEGA**; 66 turnos individuais, 198 commits, 66 ataques cada execução, **Auren venceu ambas** por HP de Crocodilo=0, Vida Auren=523. Auditor frio em dois bancos 396/396 R18 commits, 132/132 ofensivas e replay RNG.

**Hipótese discriminante:** Crocodilo ataque 6d6+134 tem máximo comum 170, **abaixo de CA Auren225**; apenas crítico positivo autoacerto teria possibilidade de atingir nessa política. O ataque 6d6+193 de Auren tem mínimo 199 **acima de CA Crocodilo112**, salvo falha crítica LAB-ONLY. Realização observada: Crocodilo **0/66** hits, Auren **66/66** hits, agrupados em somente **dois combates condicionais**, não 132 amostras independentes. No combate DEV Auren fez um crítico positivo. **Sem taxa universal de vitória**, sem poder declarar espécie impossível de vencer com outros repertórios, sem célula oficial.

### R169 — Ciência, reprodutibilidade e red team

Os **cinco bancos novos selecionados** (R165 V3, R166 V2 duas fixtures, R168 dois combates) somam **413 commits R18, 137 recibos ofensivos**, danos agregados **11.831 pós-RD = 11.563 Vida real + 268 overkill**. Esta nova coorte não foi concatenada aos 154 históricos R160; `R169_NEW_NATIVE_RECEIPTS_137_SOURCE_SCOPED.csv` contém ID/seed/ator/alvo, crítico, ataque, mitigação e HP. Auditor frio de cada família verifica dados, sequência, causalidade, estado final e checkpoint. Dois bancos **adversariais V2**, em cópias com row-SHA e `meta.head` refeitos e WAL consolidado, alteraram `hp_loss_actual` e expiração temporal: **2/2 rejeitados pela auditoria semântica**, não por mera ausência de hash válido. Primeira tentativa redteam com mutação WAL não congelada é diagnóstico excluído.

Pré-registros documentais distinguem DEV e reserva NÃO CEGA. **Holdout cego independente: 0**. Não comparar consumos RNG de políticas diferentes por ordinal sem alinhamento causal. Dois confrontos básicos versus a mesma espécie não justificam probabilidade de vitória ou intervalo populacional.

### R170 — Continuidade, contratos e gates

**CONTRATOS:** 17/17 requisitos originais e IDs preservados literalmente, **0/17 homologação terminal**; evolução individual em `R170_17_CONTRACTS_BEFORE_AFTER.{json,md}`. **BATERIAS A–D:** 0/1875 células oficiais. Crocodilo espécie diferente é prova LAB, não preenchimento oficial.

**DENOMINATORS — separado:** R160 histórico = 9 bancos, 466 commits, 154 ataques; R161–170 novo selecionado = 5 bancos, 413 commits, 137 ofensivas; 2 lutas completas Crocodilo (2 seeds), 3 cenas/fix técnicas (1 temporal, 2 concorrência), 3 diagnósticos não aprovados principais (R165 V1/V2, R166 V1), R163 fault-copies fora dos combates, R169 redteam-copies fora dos combates, 2/2 adversários rejeitados; 0/17 contratos terminal e 0/1875 células poder oficial. Não fundir coortes ou denominar RUN-IDs correlacionados replicações independentes.

**LAST-VERIFIED-UNIT:** R169 auditores independentes dos cinco bancos, R161 forensic original; arquivo R170 requer manifesto de congelamento externo e readback limpo após geração do ZIP.  
**FIRST-PENDING:** identificar Iniciativa natural/proficiência da Besta e política de iniciativa competente para admitir verdadeiramente confrontos ED×Besta em combate oficial; em paralelo, expiração Casulo e RD elemental.  
**NO-REPEAT:** R01–R160 intocados; nenhum RUN histórico R157/R158/R159 reaplicado. Bancos R163/R165/R166 novos incompletos segregados e não reexecutados; R169 redteam V1 mantido diagnóstico.  
**CONFLICTS:** Fonte Auren transformação 100+15/turn vs Sistema Lendário 320PA; Casulo dois turnos sem boundary; meia-dano ímpar; RD Lightning; alcance Grifo “linha curta”; dano misto sem decomposição.  
**UNKNOWN-EFFECT:** R123, R134, R143, R156 permanecem; novos R163 fresh after-intent, R165 V2, R166 V1 preservados pending/HOLD; R130 QA_FAIL, R138 SPATIAL_PARITY_HOLD, R124 5×5 censurado, R159 meia-ímpar bloqueado; nenhuma reexecução.  
**AUTHORITY/WRITER:** CM-000006 perfil PAUSED, sem writer, lease, epoch, fencing, INSTANCE-ID ou IBX-101 ACK comprovados. Nenhuma escrita no Notion OP/Diário/Party/O Primeiro/fichas/regras/DMG. Biblioteca de arquivos tem autorização de artefatos não-canônicos existentes, não homologação.  
**NEXT-5:** (1) formalizar proficiência específica de iniciativa Grifo/Croc; (2) resolver RD Lightning e alcance Descarga; (3) autoridade de duração dois turnos e Casulo full-cycle; (4) localizar/fechar segundo ED e equipe válida; (5) independent external blind prereg/holdout para confronto com especiais/admissão de células.  
**TARGET-REMAINDER:** 17 gates terminais originais, cada um documentado na matriz; cenários fonte-completos ED×Besta e escala de equipe, RD/mistura e sangramento, transformação e revisão oficial.  
**NAC-PASS:** somente PASS técnico local nos recibos, controles de R18, duas lutas fonte-condicionadas, temporal fonte-explicita e oportunidades; **HOLD terminal 0/17**. Reconciliação NAC-NORM apenas documental, nenhuma nova regra aprovada.

**O que consegue agora que não conseguia R160:** exportar corretamente a Vida efetivamente retirada, manter −6 m e remover explicitamente no próximo turno, acoplar ao Casulo modificação de CA e deslocamento e interromper segunda oportunidade após morte, executar outra espécie Besta em luta completa e separar causalmente ciência/overkill. Ainda **não** tem segundo ED completo nem confronto oficialmente admitido com uso integral das habilidades especiais da Besta.

**DMG:** Handoff somente preparado, com coorte corrigida de R160 (154) e nova coorte R161–170 (137) mantidas separadas, sem ACK do executor DMG.
