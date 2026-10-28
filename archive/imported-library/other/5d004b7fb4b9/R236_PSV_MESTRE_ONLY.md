# R236 — FRACO <10%, DESVANTAGEM, VELOCIDADE MEIA, INTERRUPÇÃO HP0 / BESTAS FULLSTATS PRECREATE TEST

**21/10/2026 · CM-000006, OP-VLAB-FUSION-SANDBOX-01 · MESTRE-SIDE / LAB / produção HOLD · Party/O Primeiro/fichas/normas NO-WRITE**.

## Fonte, antes e novo trabalho

Fontes Notion relidas em 21/10: [Sistema de Combate, Regra 7 — Fraco](https://app.notion.com/p/3ebc2b324ede81f1be4be8804ac113c0): Vida <10%, movimento pela metade, ataque com Desvantagem. [Criação de Besta, Regra 9](https://app.notion.com/p/3ebc2b324ede81f4992ac88a3588cacd): Esforço Final é escolha possível e causa imobilidade de um turno, **NÃO AUTOMÁTICO**. [BEAST-FULLSPEC-VZ-06](https://app.notion.com/p/3f3c2b324ede813987deda0b382e83c7): Grifo-Matriarca L3 Vida4315; Crocodilo Ancião L3 Vida5580; Roc L3 Vida4200, CA/RD/velocidade/ataques no extrato R234. Bestas PRECREATE Mestre-side, nunca P4 por inferência.

**ANTES R235:** ataques de 1x1/2x1 com actor fonte-completo em seis rodadas, todos censurados; magia do Grifo validada sem KO. **DEPOIS R236:** nova fixture com Crocodilo em **95/5580 PV iniciais** — ferimento PRÉ-EXISTENTE LAB declarado, NÃO dano inventado na cena — foi executada nas mesmas variantes Grifo×Croc e Grifo+Roc×Croc.

## Resultados medidos (seis seeds pareadas, 12 cenas novas)

- **12/12 terminais `STOP_HP0_LAB_ONLY`**, 59 commits, 264 eventos nativos, 59 ataques, 41 acertos, 28 movimentações.
- **20 ataques com Fraco**, com duas tentativas de 6d6 e uso da menor rolagem, além do modificador da desvantagem nativa; **11 deslocamentos sob Fraco** com `base_speed50 / 2 =25 m` (Croc). PA, Vida e danos reconstruídos independentemente; HP nunca negativo. Um ator com HP0 não recebe outra Ação ou turno.
- **121 espaços potenciais de turno do horizonte original de seis rodadas não executados** por terminação antecipada dos combates; não são ações gastas ou direitos removidos a personagens reais.
- Braço SOLO: rounds de parada Croc por seed: **4,4,4,4,3,2**. Braço TEAM: **2,2,2,2,2,1**, todos menores na fixture. Crocodilo teve 15 turnos efetivos em SOLO vs 5 em TEAM; controle de economia de ação, não avaliação de causa universal ou vitória canônica.
- R236 não habilita automaticamente Esforço Final e não interpreta HP0 como morte; o encerramento é protocolo LAB. 12 unidades são braços aninhados em seis pares, não 12 seeds independentes.

## Evidência adversarial

Auditor SQLite READ-ONLY independente de motor/runner: linha R18 SHA/head/state, fonte e prereg, desempenho de Fraco, ataque/disadvantage e crítico, movimento/source-speed, matemática física e RD, HP0 clamp, cancelamento imediato de turnos e ausência de promoção P4. **5/5 ataques com hashes reconstruídos rejeitados**: reanimação fictícia HP0, continuação após HP0, velocidade fonte falsificada, overkill alterado, promoção indevida de PRECREATE. Engenharia sem modificar os DBs admitidos. Uma mutação em representação equivalente `50`→`50/1` foi corretamente tratada como equivalência numérica, não adulteração; o teste válido alterou para `75`, rejeitado. Versão final audita comportamento, não strings arbitrárias.

## Governança

- ZERO escritores externos, Party, O Primeiro, DMG, LEVEL-UP, sistema canônico ou página de Besta. Zero replays R01–R235. Somente cópias TEST e biblioteca.
- **NAC-PASS local:** PASS técnico condicional. **NAC-PASS global:** HOLD. 0/17 contratos terminais homologados, 0/1.875 células oficiais.
- **LAST-VERIFIED-UNIT:** R236 após readback frio, 12 SQLite; **FIRST-PENDING:** R237 candidato — reproduzir primárias fontes Bestas não PRECREATE P4 para transição oficial, geometria mágica de linha e AoO se normas permitirem, nova Bateria E com chassi físico+encantamento P4; benchmarking 1×1/2×1 em várias espécies sem misturar estatutos.
