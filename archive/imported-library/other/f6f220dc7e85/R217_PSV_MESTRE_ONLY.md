# PSV R217 — stress de ordem física de turnos; auditor independente de scheduler (MESTRE-SIDE/TEST)

**21/10/2026** · `CM-000006` lógico (INSTANCE-ID, writer, lease não reivindicados) · Operação `OP-VLAB-FUSION-SANDBOX-01`. Produção HOLD. Party, O Primeiro, fichas e normas: NO-WRITE.

## Materialmente novo depois do R216 já publicado

A R216 confirmou invariância a **rótulo de equipe**, mas não permutação da ordem física dos atores. Esta extensão R217 TEST declarou de modo prospectivo duas agendas de quatro rodadas: V→R→E e R→V→E, com os mesmos Varok (V), Arveth (R) e Eristan (E), a mesma política protetiva e novas seeds independentes para os pares. Módulo nativo R18, resolvedores v0.8.1 e fonte TEST do R216 foram reutilizados; a alteração é somente ordem de atores no estado de cena antes do primeiro commit. Eristan permaneceu terceiro para preservar o contrato vigente de fim de rodada. Isto é um **stress de permutação experimental declarada, NÃO prova de que uma rolagem oficial de iniciativa produziria tal ordenação**.

### Denominadores e resultados

- **Seis seeds novas pré-registradas**, duas ordens por seed: 12 tentativas, 10 bancos válidos / **5 pares completos**; seed 21782003 teve os dois braços em UNKNOWN_HALF_ODD, com pending R18, sem retry.
- **Doze tentativas iniciais de preflight adicionais** com seeds 21781001–21781006 foram **rejeitadas antes de qualquer commit** por erro de empacotamento `scene(meta) != scene(state)`. As 12 ficam preservadas isoladamente, sem reutilização de seed. Elas NÃO são combates admitidos. O adaptador mínimo corrigiu o valor da cena somente para as novas seeds 21782001–21782006.
- **10 combates condicionais TEST**, cada qual com quatro rodadas e três atores ativos = 120 turnos/commits, **732 eventos**, **90 ataques físicos**, **12 curas**, **40 magias**. Dez censuras, zero KO, zero vitórias.
- **Resultados terminais por ID físico nos cinco pares:** HP, PA, posição e recursos idênticos entre as duas ordens, apesar da sequência cronológica realmente trocada. Isto é um achado NEGATIVO delimitado: a permutação não modificou os resultados terminais NESTA fixture, com streams RNG por ação/ator, Eristan sempre terceiro e nenhuma eliminação precoce. Não comprova justiça universal ou equivalência entre políticas.
- Auditor independente read-only de R18 e mecânica nativa PASS 10/10. Novo auditor do scheduler confrontou a ordem do estado com todos os 12 `turn_start`/`turn_end` por banco e os quatro turnos por ator. Dois clones adulterados com hash R18 reconstruído foram rejeitados **2/2** pelo auditor novo, embora passassem pelo auditor genérico R216.
- **14 quarantined SQLite**: 12 preflight zero-commit e 2 UNKNOWN_HALF_ODD. Não houve replay histórico ou R216 repetido.

## Proveniência, requisitos e limitações

Fonte base recuperável e independente: `VLAB_R216_INTEGRATED_MULTI_ACTOR_SCIENCE_CONTROL_COLD_AUDITED_MESTRE_ONLY.zip`, SHA-256 `2b2f3a398e6ed9886133ae531e8f603caa4e4ee509317d640c947a38b528af0e`. O pacote R217 incorpora snapshots de código/runtime, pre-registros e os novos bancos; **não altera nem copia uma luta R216**.

Variar ordem de turnos por contrafactual está autorizado apenas como TEST científico, não como iniciativa legal atribuída por dados. Fontes de personagens são propostas Mestre-side e adjacência depende de fixture R44; movimentos e cenário permanecem condicionais. Arredondamento metade ímpar, bloco↔metros, custo de Movimento interrompido, controle/transformação não homologados continuam HOLD. Células oficiais R91 **0/1.875**, contratos terminais **0/17**.

**LAST-VERIFIED-UNIT** R217 condicionado à recuperação fria+readback; **FIRST-PENDING** R218 candidato, sujeito a preflight, comparar efetiva iniciativa rolada fonte-bound e interações não-comutativas com eliminação/defesas legítimas, e avançar Controle de Besta / transformação quando fonte fechar. Não reivindicar winner nem green de produção. **NAC-PASS** técnico local após readback, científico/global HOLD.
