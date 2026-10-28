# PSV R213 — INTEGRAÇÃO HISTÓRICA R43–R49 + MOTOR NATIVO R18/v0.8.1

AS-OF: 20/10/2026 · CM-000006 lógico · OP-VLAB-FUSION-SANDBOX-01 · MESTRE-SIDE TEST.
LAST-VERIFIED-UNIT ANTES: R212 (recuperação fria PASS; físico pós-movimento parcial).
PRÓXIMO MARCO: R213 candidato; sem página canônica homônima VLAB localizada no preflight dirigido; biblioteca reconsultada antes de publicação.
PRODUÇÃO: HOLD. Party/O Primeiro/fichas/regras: NO-WRITE. INSTANCE-ID/WRITER: não reivindicados.

## ANTES → DEPOIS
Antes: AOO funcional em janelas R44–R49, mas desacoplada do movimento nativo R211/R212; R212 físico após movimento sem AOO.
Depois: R213 usa um único journal R18 para oportunidade nativa v0.8.1 (`attack_origin=OPPORTUNITY`) antes de `move_via_verified_path`; dano/recursos nativos; fixture de adjacência historicamente declarada e explicitamente TEST. A segunda frente integrou refresh de ações em múltiplos turnos, sem repetir R212.

## Denominadores — Bateria AOO
9 tentativas pre-registradas em 4 famílias: 8 SQLite admitidos, 1 SQLite retido com `pending` sem commit (`R213_AOO_DOUBLE_S21331001`).
Em 8 janelas admitidas: 8 commits; 8 AOO nativas; 8 acertos; 8 Reações gastas; 6 movimentos concluídos; 2 interrupções letais da Cabra; 461 PV efetivamente retirados; 0 vitórias canônicas. 2 controles de não adjacência, 2 fixtures com Reação Feryn já gasta, 2 com duas oportunidades, 2 com KO interrompendo movimento. Todas as sementes novas e diferentes de R43–R212.

## Denominadores — Bateria MULTITURNO
3 seeds, 3 combates TEST (unilaterais), 9 commits, 30 eventos, 6 movimentos nativos, 6 ataques físicos após movimento, 6 acertos, 3 passes do NPC, 3 KO condicionais com 630 HP efetivo por cenário; NÃO significam 3 vitórias oficiais. Ciclo RAYA→ERISTAN→RAYA; renovação de ação/Movimento/Reação comprovada, duas rodadas iniciadas.

## Auditoria independente
`PASS_R213_INDEPENDENT_R18_NATIVE_OPPORTUNITY_FIXTURE_CONDITIONAL` — 8 janelas válidas, 1 pending em quarentena; cadeia SHA do SQLite, recibos de Vantagem, HP/RD, ordem física e commit revisados sem importar runner.
`PASS_R213_MULTITURN_R18_READONLY_INDEPENDENT` — 3 bancos multiturmo e replay read-only do journal, 9 commits.
5 testes negativos sem alterar bancos válidos: falta Vantagem, prova ausente, velocidade insuficiente, ausência de mutação, corrupção intencional em CÓPIA auditora. IDs committed duplicados rejeitados pelo R18.

## Limites impeditivos
- Universal bloco↔metro/diagonais/tamanho: `BLOCKED-SOURCE-ADJACENCY`.
- Adjacência de R213 declarada como grafo TEST, sem conversão normativa; Arveth/Cabra com `speed=3m` como hipótese TEST (sem fonte fechada da velocidade).
- Débito da Reação nativo ocorre dentro do resolvedor de ataque, após rolagem em memória, embora a intenção venha antes; paridade R45B não certificada.
- Reação previamente gasta em cenário é snapshot pré-registrado, não efeito gerado por ação anterior.
- Em KO antes do movimento, custo de movimento `UNKNOWN-EFFECT/HOLD`.
- Fonte NPCs PROPOSTA, físico/RD de Raya/Eristan TEST condicional, Eristan passa turnos sem reação ofensiva; não benchmark universal.
- Empates R49, retirada segura, R50/R51 e condições controladas não executados neste novo conjunto.

## Controles de autoridade e comunicação
NAC-PASS técnico local: PASS TEST CONDICIONAL às cenas. NAC-PASS global/produção: HOLD.
Contratos terminais 0/17; benchmark oficial 0/1.875.
Inbox histórico IBX-101,99,95,120 e IBX90 consultados em continuidade; nenhuma alteração de ACK.
LEVEL-UP/DMG/consulta normativa: prepared_not_sent, nenhuma prova de envio ou recebimento.

## FIRST-PENDING / NEXT-5
1. Resolver paridade causal R45B: reserva de Reação anterior ao RNG de ataque, mantendo núcleo v0.8.1 e commit atômico.
2. Obter decisão normativa bloco↔métrico e custo do movimento interrompido.
3. Integrar R43 empate DES com ordenador R49 em janela nova de movimento (sem replay).
4. Evoluir para multiturmo bilateral com oponente source-completo e reações reais, sem passes impostos por falta de fonte.
5. Desbloquear interface LEVEL-UP Orc e enviar recibos DMG por rota legitimamente autorizada; continuar controle, transformação e Bateria E.

NO-REPEAT: preservar R43/R44/R45B/R46/R49 e R211/R212, seus seeds e bancos; manter quarentena original R45 e nova intent R213.
