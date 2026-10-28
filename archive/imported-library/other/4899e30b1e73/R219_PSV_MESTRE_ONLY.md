# PSV R219 — FERIMENTO PRÉ-EXISTENTE E INICIATIVA ROLADA

**Ambiente:** RPG DO MESTRE / ASSIMILAÇÃO, MESTRE-SIDE TEST. **Identidade:** CM-000006 lógica / WS0001. **Operação persistente:** OP-VLAB-FUSION-SANDBOX-01. **Data-base:** 21/10/2026. **Produção e Party/O Primeiro/fichas/normas:** HOLD / NO-WRITE.

## ANTES → DEPOIS

**ANTES:** R218 demonstrou iniciativa efetivamente rolada em propostas ON5, com 13 pares completos e invariância terminal restrita à fixture. Dados oficiais de iniciativa ON5 4d6+29 (Varok), 4d6+25 (Arveth), 4d6+30 (Eristan). Motor R18/v0.8.1 e o resolvedor R216 permanecem reutilizados sem refatoração. Condições normativas de empate, blocos e metade ímpar seguem abertas.

**DEPOIS:** Preexistência de ferimento em Varok (614/734 PV) mudou comportamento do suporte, mas os 16 pares completos conservaram o mesmo estado terminal; 15 tiveram agenda rolada diferente. A fixture permaneceu comutativa para a comparação; não alegar equivalência universal de iniciativa. Auditor R216 clonado teve sua expressão de crítico negativo corrigida (parênteses) sem alterar núcleo ou histórico.

## DENOMINADORES AUDITADOS

- **Combates TEST novos admitidos:** 36. Tentativas bloqueadas: 12. Seeds pareadas completas / unidades fatoriais: 16. Unidades com ordem de iniciativa alterada: 15.
- **Commits:** 432; **eventos nativos:** 2636; **movimentos:** 108; **ataques físicos:** 324; **ataques de oportunidade:** 36; **curas:** 70; **magias:** 96.
- **Censuras:** 36; KO: 0; vitórias atribuídas a censura: 0; reexecuções de combates históricos: 0.
- **Bloqueios:** 7 empates de iniciativa antes de commit; 5 sucessos de salvaguarda com metade de dano ímpar sob UNKNOWN-EFFECT em SQLite isolado.
- **Pré-registro congelado antes de novos bancos:** `sources/R219_PREREG_BEFORE_NEW_COMBATS.json`.
- **Auditoria:** `code/` sem imports de engine no validador independente, `evidence/reports/R219_INDEPENDENT_CHRONOLOGY_AUDIT.json`, eventos e head SHA R18 auditados, recursos HP/PA/Reação e habilidades verificadas, rolling iniciativa source-bound.

## CLASSIFICAÇÃO DE FONTE

- **VERIFICADO em fontes Mestre-side:** ON5 4d6+bonificação própria para cada personagem, cura Eristan Pulso 45 PA/3m e Reconstituição 75PA/5m, Esporos 80 PA/raio5m/CD76, ataques Varok/Arveth e defesas de Reação dos dois.
- **PROPOSTO / TEST:** NPCs e equipamentos da Família Asa Prateada; cenas de movimento, velocidade e adjacência declaradas em fixture; RD mágica 0 apenas no laboratório; comparadores de estratégia e mapeamento RNG. Não canonizar.
- **PENDENTE/HOLD:** desempate universal da iniciativa, dimensão de bloco, movimento interrompido por KO, arredondamento de metade ímpar, primeira transformação Prata1+ integral, Controle de Besta source-completo e Bateria E homologável.

## CIÊNCIA, BENCHMARK E NAC-PASS

O denominador inferencial é **seed completa**; braços, turnos e ataques não são observações independentes. Estes casos informam o estrato exploratório R91 C20 (Equipe Ouro Negro5★), porém a fonte oficial C20 permanece `SOURCE_MISSING`, sem clone canônico e **0 homologação**. Contratos terminais 0/17; matriz oficial 0/1.875.

**NAC-PASS:** gate mecânico local TEST condicional; científico global / rank / produção **HOLD**. Nenhuma mensagem duplicada IBX-125/126, nenhum ACK ou writer/INSTANCE-ID autoatribuído. IBX-138 adotada apenas como interpretação de encaminhamento integral.

## NO-REPEAT / RETOMADA

Nenhum runner histórico reexecutado. Usar `R219_COLD_PORTABLE_RECOVERY.py` em extração limpa para auditar arquivos e SQLite sem criar lutas. Próxima pergunta é dependência causal entre ordem da iniciativa, decisão tática e atribuição da stream RNG, exigindo comparação controlada e evidência de fonte para os ramos desconhecidos.
