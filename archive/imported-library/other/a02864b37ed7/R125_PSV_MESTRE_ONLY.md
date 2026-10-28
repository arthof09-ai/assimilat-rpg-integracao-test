# PSV — OP-VLAB-FUSION-SANDBOX-01 / R118–R125

**AS-OF:** 16/10/2026 · **AMBIENTE:** MESTRE-SIDE · **IDENTIDADE FUNCIONAL:** CM-000006, perfil Notion PAUSED / instância NÃO REIVINDICADA.
**BASELINE:** R01–R117 preservada integralmente. **NAC-PASS:** PASS técnico restrito às cópias e gates executados; TERMINAL HOLD. **TERMINAIS:** 0/17.

## 1. Resultado material, sem repetir R117

A continuidade copiou **um único módulo competente** `vlab_effects_v08.py` da entrega R117 e **acrescentou** `declare_counterattack` e `execute_declared_counterattack` conforme as decisões R50/R51 do Mestre registradas na operação Notion existente. Reutilizou `vlab_r18_interactive.event_commit` para intenção→cálculo na cópia→commit WAL e `vlab_r26_master_rulings.tie_order` para ordem de Iniciativa. Não abriu novo motor e não alterou fontes, motor ou bancos históricos.

**R50 confirmado em teste dirigido:** Contra-atacar declarado antes do ataque consome Reação. Se o ataque original errar, uma resposta recebe Vantagem (duas rolagens, maior valor e +2). Se o golpe original acertar **por crítico positivo**, não existe resposta, inclusive quando score comum não supera CA. No caso dirigido seed `918515`, o contra foi declarado, uma ofensiva de Feryn resultou em crítico positivo e a resposta de Auren foi corretamente suprimida. **R51:** contra-ataque jamais pode abrir uma segunda janela de Contra-atacar; o comando de origem COUNTER foi rejeitado antes de intenção.

### Três atores com Iniciativa natural documentada

| Cena | Família / seed | Eventos R18 | Ataques normais | Resultado |
|---|---|---:|---:|---|
| R119-DEV | desenvolvimento `918201` | 22 | 7 | Auren vence ambas as instâncias técnicas Feryn |
| R119-RESERVED | reserva sem cegamento independente `928801` | 25 | 8 | Auren vence; 1 crítico positivo |
| R121-R50 | seed **dirigida**, não holdout `918515` | 28 | 9 | Auren vence; crítico de Feryn cancela resposta R50 |
| **TOTAL** | **3 seeds distintas / 3 cenas** | **75** | **24** | **3 concluídas; 0 oficial** |

**Outros denominadores nos três bancos:** 9 declarações de Contra-atacar, 8 respostas executadas, 1 resposta suprimida por acerto crítico, 7 Esquivas, 3 Defesas Defender, 2 críticos positivos totais e 14 renovações de Reação de zero para um slot em abertura de turno próprio. R50/R51 estão autenticados no texto da OP existente. Iniciativa Auren `6d6+166` (DES164 + proficiência Iniciativa2); Feryn `4d6+82` (DES80 + proficiência2), **sem atribuir proficiência à Besta**. Desempate R26 aplica DES antes de rerrolar somente empatados. São **1 instância Auren e 2 cópias técnicas do mesmo NPC Feryn**; não são três personagens distintos nem equipe de dois ED equivalentes.

### Escala progressiva — mesmos perfis técnicos, não 40 indivíduos existentes

| Escala | Seed | Resultado técnico | Eventos | Ataques | Reações declaradas | KO técnicos |
|---|---|---|---:|---:|---:|---:|
| 5×5 | `938211` | **CENSURADO** antes de falha crítica não normatizada; intenção do evento faltante não aberta | 38 | 12 | 5 | 2 |
| 10×10 | `938311` | **FINISHED** técnico, auditor frio PASS | 118 | 39 | 14 | 10 |
| 20×20 | `938411` | **FINISHED** técnico, auditor frio PASS | 232 | 77 | 23 | 20 |
| **TOTAL** | **3 seeds** | 2 concluídas, 1 censurada | **388** | **128** | **42** | **32** |

As cópias de Auren L3 e Feryn ON5 partilham dois perfis reais, não são personagens/squad reais, e o cenário não contém movimento posicional, mapas 20×20, repertório completo, Descarga Curta ou PA positivo. O ganho é **robustez técnica do scheduler + reação + RD física + KO + escala**, não prova do contrato terminal `BATTLE_1X1_2X1_20X20`.

### Integridade adversarial

- **8/8 pré-validações negativas** confirmadas em READBACK, sem intenção ou mudança de ledger. Incluem R51 nesting, segundo gatilho com Reação já consumida, alvos ilegais, evento de ação falsificado e fontes fora de janela. O teste inicial de `NO_SLOT` foi **INVÁLIDO** porque ainda havia slot; foi preservado e não contado.
- **R123 2/2 falhas de processo:** AFTER_INTENT → 1 pending, 0 alterações de HP, banco em `UNKNOWN_EFFECT/HOLD`, sem tentativa de continuar; AFTER_COMMIT → 1 evento de ataque publicado e recuperado exatamente uma vez.
- **R125 2/2 cópias adulteradas detectadas pelo auditor sem importar motor:** modificações de dano líquido e bônus de Vantagem rejeitadas, embora a cadeia de hashes tenha sido recalculada e fosse estruturalmente consistente.
- **Regressão 28/28 do módulo histórico v0.8.1** passou no módulo aditivamente estendido. R117 23/23 adicionais preservados como base histórica, **não recontados como nova prova**.

## 2. ANTES → DEPOIS / pendências e menor restante

| Pendência | ANTES R117 | Nova prova R125 | Aceite restrito | Menor restante |
|---|---|---|---|---|
| Reações | Sem janelas em duelos R112 | 9 declarações Contra, 8 respostas, 1 supressão R50; 7 Esquivas, 3 Defender; duplo gatilho DENY | **PASS LOCAL** | simultaneidade genuína, AoO posicional, demais reações, paridade total |
| Scheduler | R117 cenas 1×1 de abertura condicionada | 3 atores com iniciativa natural e KO, 10×10 e 20×20 técnicos concluídos | **PASS TÉCNICO ESCOPADO** | variedade de atores, efeitos/PA/posição/reações completas |
| RNG/Replay | três seeds R112 e auditor R113 | 6 novas seeds, 463 eventos selecionados incluindo censurado, auditor causal independente por fita RNG/R26 | **PASS LOCAL** | família holdout realmente cega e validação externa |
| Crítico | Corrigido e 51 regressões R117 | Críticos exercidos com reação R50, sem refazer testes aritméticos | **PASS LOCAL AMPLIADO** | falha crítica sem efeito normativo; conjunções restantes |
| RD | Física em duelos R112 | Geral-física Auren 35 e Feryn 22 usada em contrarrespostas e golpes | **PASS PARCIAL** | Dark específica, Lightning desconhecida, mista e stacking |
| PA/Descarga | Quatro Descargas 55 PA, 220 PA R117 | Não foram reexecutadas; reações sem PA positivo não drenaram recursos | **BASE RETIDA** | PA positivo com reação/3 atores, meia ímpar e alcance |
| Potência ED×Besta | R112 Grifo L3 × Auren | nenhum avanço oficial: Auren×Feryn é confronto de postos DESIGUAIS | **HOLD CIENTÍFICO** | Besta iniciativa documentada, segunda ED completa, poder efetivo comparável |
| Transformação Auren | 100PA+15/turno ficha vs 320PA especializadas | conflito reaberto no Notion; sem ativação | **HOLD DA TRANSFORMAÇÃO** | NAC-NORM-01 competente, snapshot e custos autorizados |
| Contratos 17 | 0/17 terminal | matriz original R117→R125 atualizada linha a linha | **0/17** | gate histórico de cada linha + revisão externa + NAC-PASS |

Matriz detalhada: `R125_17_CONTRACTS_BEFORE_AFTER.md` e `.json`, contendo **exatamente os 17 IDs e os requisitos terminais originais sem mudança de denominador**.

## 3. Baterias A–D e poder efetivo

- **A (25 posições):** confrontos técnicos Auren/Feryn não produzem perfil ED balanceado nem ranking. Zero linha promovida.
- **B (27 posições):** Grifo L2 continua derivação experimental legítima pré-R117; Grifo L3 permanece precreation Mestre-side. ADM posição 26 e Divina 27 > L5 mantidas. Zero promoção.
- **C (25 posições):** 5×5/10×10/20×20 avançam a integridade do scheduler, **não** 25 tiers de poder efetivo. Zero promoção.
- **D (27 posições):** sete candidatas históricas preservadas; nenhum indivíduo fictício de escala contado como espécie adicional. Zero promoção.

**Grade:** 0/1.875 células oficiais; nenhum benchmark homologado. Experiências têm amostras interdependentes, políticas fixas e nenhuma inferência populacional sobre vitória/precisão.

## 4. DMG e contratos

`R125_NATIVE_RECEIPTS_165_FOR_DMG.csv` contém **165 recibos de ataque** nos seis cenários: 152 golpes normais e 13 respostas de Contra-atacar (R119 24+8 e escala 128+5). RUN-ID, seed, tipo, fonte, bruto, RD, Vida retirada, overkill, crítico e censura estão individualizados. São observações dependentes e não devem se unir automaticamente a R97 (1.344) ou R116 (212). As erratas R93/R95, o histórico R97 e o handoff R116 estão preservados dentro do ZIP R117 aninhado. **Entrega DMG preparada, nenhum ACK recebido, nenhum write DMG.**

## 5. Quarentena e continuidade

R01–R117, incluindo R59/R72, R92/R94, R93/R95, R109/R110, R111 e R115 permanecem intocados. O primeiro teste R122 com slot existente (`R122_NO_SLOT_939101`) foi aceito por construção incorreta da prova negativa e está isolado sem crédito. Testes diagnósticos R122 posteriores ficaram isolados; R123 usou bancos **novos** e comprovou os dois cortes. `R123_FRESH_AFTER_INTENT_939906` permanece **pending=1 / UNKNOWN_EFFECT** e nunca poderá ser repetido sem reconciliação competente. O banco 5×5 censurado também permanece tal como registrado, sem substituição.

**Autoridade:** CM-000006 `PAUSED`, `INSTANCE-ID/WRITER/EPOCH/LEASE/FENCING/IBX-101 ACK = NÃO COMPROVADOS`. OP/Diário/Party/O Primeiro/regras/fichas/DMG **WRITE=0**. Biblioteca de artefatos isolados apenas. `NAC-PASS` local apenas; `17/17` revisados, **0/17 terminais**.

**LAST-VERIFIED-UNIT:** R125 auditor frio 3+3 DBs, 8 negativas, 2 fault, 2 redteam, 28 regressões, readback físico do ZIP.
**FIRST-PENDING:** janelas simultâneas/AoO e reação contra efeitos com fonte, integração de PA positivo no scheduler 3+, prova de cura/condições, fonte para iniciativa de Besta, segundo ED comparável, reconciliação de transformação Auren e garantia de cegamento do holdout.
**NO-REPEAT:** nunca rerodar R119/R121/R122/R123/R124 nos mesmos RUN-ID, nem qualquer histórico R01–R117; um comando com intenção desconhecida permanece HOLD.

## 6. Fontes Notion primárias reabertas (Mestre-side)

- Sistema de Combate: https://app.notion.com/p/3ebc2b324ede81f1be4be8804ac113c0
- Criação de Besta: https://app.notion.com/p/3ebc2b324ede81f4992ac88a3588cacd
- Sistema de Transformação Espiritual: https://app.notion.com/p/3f2c2b324ede81c0ae0ee4e66212edc9
- Sikong Auren: https://app.notion.com/p/3ebc2b324ede814bb730d47dd7bd5f02
- Sikong Feryn: https://app.notion.com/p/3f6c2b324ede81ce9c61db8127bf0e31
- OP-VLAB existente com decisões Mestre R50/R51: https://app.notion.com/p/3f3c2b324ede819496ddd7f93bd7e5d2

