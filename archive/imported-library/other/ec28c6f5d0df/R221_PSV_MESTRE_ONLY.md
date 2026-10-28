# PSV R221 — PAREAMENTO POR ÍNDICE DE OCORRÊNCIA DE HABILIDADE

**Ambiente:** RPG DO MESTRE / ASSIMILAÇÃO, MESTRE-SIDE TEST. **Identidade:** CM-000006 lógica / WS0001. **Operação persistente:** OP-VLAB-FUSION-SANDBOX-01. **Data-base:** 21/10/2026. **Produção e Party/O Primeiro/fichas/normas:** HOLD / NO-WRITE.

## ANTES → DEPOIS

**ANTES:** R218 demonstrou iniciativa efetivamente rolada em propostas ON5, com 13 pares completos e invariância terminal restrita à fixture. Dados oficiais de iniciativa ON5 4d6+29 (Varok), 4d6+25 (Arveth), 4d6+30 (Eristan). Motor R18/v0.8.1 e o resolvedor R216 permanecem reutilizados sem refatoração. Condições normativas de empate, blocos e metade ímpar seguem abertas.

**DEPOIS:** Mesma família de fixture R220, mas magia e cura recebem streams determinísticos pelo n-ésimo uso da habilidade, não pela rodada. 3 pares tiveram escolhas Cura/Esporos em ordem diferente e nenhum par apresentou HP terminal diferente. A coorte possui seeds distintas da R220, portanto não serve como contrafactual exato para a diferença de 34 PV; abriu o experimento fatorial R222.

## DENOMINADORES AUDITADOS

- **Combates TEST novos admitidos:** 33. Tentativas bloqueadas: 15. Seeds pareadas completas / unidades fatoriais: 13. Unidades com ordem de iniciativa alterada: 9.
- **Commits:** 396; **eventos nativos:** 2409; **movimentos:** 99; **ataques físicos:** 297; **ataques de oportunidade:** 33; **curas:** 30; **magias:** 104.
- **Censuras:** 33; KO: 0; vitórias atribuídas a censura: 0; reexecuções de combates históricos: 0.
- **Bloqueios:** 11 empates de iniciativa pré-commit; 4 metade ímpar UNKNOWN em bancos com intenção pendente.
- **Pré-registro congelado antes de novos bancos:** `sources/R221_PREREG_BEFORE_NEW_COMBATS.json`.
- **Auditoria:** `code/` sem imports de engine no validador independente, `evidence/reports/R221_INDEPENDENT_STABLE_TAPE_AUDIT.json`, eventos e head SHA R18 auditados, recursos HP/PA/Reação e habilidades verificadas, rolling iniciativa source-bound.

## CLASSIFICAÇÃO DE FONTE

- **VERIFICADO em fontes Mestre-side:** ON5 4d6+bonificação própria para cada personagem, cura Eristan Pulso 45 PA/3m e Reconstituição 75PA/5m, Esporos 80 PA/raio5m/CD76, ataques Varok/Arveth e defesas de Reação dos dois.
- **PROPOSTO / TEST:** NPCs e equipamentos da Família Asa Prateada; cenas de movimento, velocidade e adjacência declaradas em fixture; RD mágica 0 apenas no laboratório; comparadores de estratégia e mapeamento RNG. Não canonizar.
- **PENDENTE/HOLD:** desempate universal da iniciativa, dimensão de bloco, movimento interrompido por KO, arredondamento de metade ímpar, primeira transformação Prata1+ integral, Controle de Besta source-completo e Bateria E homologável.

## CIÊNCIA, BENCHMARK E NAC-PASS

O denominador inferencial é **seed completa**; braços, turnos e ataques não são observações independentes. Estes casos informam o estrato exploratório R91 C20 (Equipe Ouro Negro5★), porém a fonte oficial C20 permanece `SOURCE_MISSING`, sem clone canônico e **0 homologação**. Contratos terminais 0/17; matriz oficial 0/1.875.

**NAC-PASS:** gate mecânico local TEST condicional; científico global / rank / produção **HOLD**. Nenhuma mensagem duplicada IBX-125/126, nenhum ACK ou writer/INSTANCE-ID autoatribuído. IBX-138 adotada apenas como interpretação de encaminhamento integral.

## NO-REPEAT / RETOMADA

Nenhum runner histórico reexecutado. Usar `R221_COLD_PORTABLE_RECOVERY.py` em extração limpa para auditar arquivos e SQLite sem criar lutas. Próxima pergunta é dependência causal entre ordem da iniciativa, decisão tática e atribuição da stream RNG, exigindo comparação controlada e evidência de fonte para os ramos desconhecidos.
