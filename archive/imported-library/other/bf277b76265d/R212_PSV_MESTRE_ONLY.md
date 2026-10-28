# PSV R212 — OP-VLAB-FUSION-SANDBOX-01 — MESTRE-ONLY

AS-OF 2026-10-20 | CM-000006 lógico, INSTANCE-ID/WRITER/LEASE/EPOCH/FENCING não comprovados | MESTRE-SIDE TEST | PRODUÇÃO HOLD, Party/O Primeiro/fichas/regras CANÔNICAS NO-WRITE.

LAST-VERIFIED-UNIT: R211 recuperada fria localmente (SHA256 837243621dd3631a0f3b92bbca305fe4f4de29ec9b5ae5e735761d38004505d7, 346 entradas CRC PASS, sem replay). R212 executada com ACEITE TÉCNICO **PARCIAL** apenas da ligação MOVIMENTO+ATAQUE FÍSICO: novo checkpoint; R43 AOO permanece BLOQUEADO. FIRST-PENDING: R212-R43-ADJACENCY-SOURCE. Próximo identificador R213 não atribuído.

ANTES: movimento nativo e alvo dinâmico R211, ataque físico e AoO não exercitados nessa coorte. DEPOIS: R212 movimento 5m da réplica Raya, alcance de ataque expresso da arma em cena de 40→35m, uma Ação Movimento + uma Padrão em mesmo turno, ataque source-labelled pela função nativa v081 e RD25 física CONDICIONAL por fonte de Eristan. Transação R18 com 2 commits/run (início e movimento+ataque juntos), readback e hash chain, movimento antes de ataque, Reações preservadas. Dados impressos Raya 6d6+245 e 16d8+12d6+4d12+294; fonte composta não separa completamente magia/impacto físico — hipótese TEST, NÃO homologação.

DENOMINADORES: seis seeds novas [21241001..21241006], seis lutas de uma ação/turno, seis movimentos 5m, seis ataques nativos, seis acertos, zero AoO, zero reação gasta, zero KO, seis censuras, 2490 de Vida efetivamente retirada NO TEST CONDICIONAL. Críticos/rejeições preservados, sem repetir quaisquer seeds históricas. Não tratar seis acertos como classificação universal de Raya/Eristan.

AUDITORIA: R212_INDEPENDENT_SQL_AUDIT.json; SQL read-only independente de runner, valida hash cadeia, HP, PA, ordem, custo de Movimento/Padrão, fita de dados e RD condicional; seis testes negativos em memória sem alterações de journal, incluindo caminho inválido e bloqueio source. O pacote foi projetado para cold recovery sem executar qualquer runner histórico. Para hash/CRC definitivo, consultar readback do pacote.

CONFLITOS: mapeamento bloco-adjacente para coordenadas métricas ausente em fonte competente. `BLOCKED-SOURCE-ADJACENCY`; zero AOO realmente executados, zero prioridade R43 provada. R50/R51 preservadas, não exercitadas. Classificação/efeitos do ataque impresso Raya condicionais; dano e RD não benchmark canonizado. Espada do Lendário sem separação físico/mágico para E, transformação Prata1+, controle de Besta e Orc LEVEL-UP B1→B2/B5→P1 seguem pendentes.

INBOX: IBX-101/99/95/120/90 consultadas anteriormente, sem alterações de estado persistente nem ACK. Relatórios LEVEL-UP e DMG preparados, NÃO enviados ou recebidos. Sem claim de writer compartilhado da OP/Diário/Inbox.

BENCHMARK: R91 104 posições; Bestas 27 incluindo ADM/Divina, ED 25; 0/17 contratos terminais homologados, 0/1.875 células históricas homologadas. Apenas seis lutas TEST no novo subconjunto R212.

NEXT-5: (1) obter contrato de blocos para AoO R43 e integrar no movimento nativo, com casos A/B/C e D/E somente quando admitidos; (2) interface contratual Orc × Level-UP pela Inbox quando autor legítimo; (3) entregar recibos VLAB R209–R212 ao DMG quando rota legítima; (4) item E físico/mágico separável em canário TEST; (5) transformação Prata1+ ou habilidade de controle Besta fonte-completa, iniciar ED-REF02 com papéis reais.

NAC-PASS: PASS LOCAL para coorte de ataque pós-movimento sob hipóteses declaradas; HOLD AOO R43, HOLDER/NAC-PASS terminal e produção. NÃO declarar R212 integralmente concluída só por ter produzido arquivo. Sem rewrite de checkpoints anteriores.
