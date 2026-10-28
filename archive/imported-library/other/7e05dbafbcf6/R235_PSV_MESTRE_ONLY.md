# R235 — Grifo VZ físico × Descarga Curta com Salvaguarda, RD e arredondamento · TEST / MESTRE-SIDE

**Estado:** PASS técnico/científico delimitado, não P4; produção HOLD. Baseline R234 de 8 encontros 1x1/2x1 multi-round native physically verified; R235 usa 4 seeds novas × 4 braços fatoriais = 16 combates 1x1 de 6 rodadas, mais 4 casts focais em Roc L3, todos sem replay histórico.

## Fontes verificadas

- [BEAST-FULLSPEC-VZ-06](https://app.notion.com/p/3f3c2b324ede813987deda0b382e83c7) PRECREATE Mestreside não-P4, lido em 21/10/2026. Grifo-Matriarca L3 (Vida4315/PA4016, CA153, RD75, Des116), Crocodilo Ancião L3 (Vida5580/PA3625, CA112, RD75, DES64), Roc L3 (Vida4200, PA3740, CA164, RD75, DES128).
- Ataque físico Grifo 6d6+138, 20d10 Talão, 0 PA. `Descarga Curta`: Padrão 55PA, **14d10 Raio em linha curta, Reflexo CD94: sucesso = metade**. Salvaguarda atributo puro DES em testes Lendários 6d6, exceder CD; Mestreside floor para dano ímpar já confirmado. A largura/métrica da linha são desconhecidas, por isso SÓ cenas com um inimigo, distância curta declarada em TEST, sem aliados expostos.
- Fonte adicional `Criação de Besta` e `Sistema de Combate`; módulo RD geral de v0.8.1 permanece condicional a governança; o braço RD0 é contra-factual explicitamente não canônico.

## Novidade funcional

- **16 cenas nativas** de 6 rodadas, com agenda e movimento legal dos dois atores e ataques standard; 4 políticas fatoriais: `PHYSICAL_SOURCE_RD75`, `MIXED_SOURCE_RD75`, `PHYSICAL_RD0_TEST`, `MIXED_RD0_TEST`. MIXED usa Descarga nos turnos próprios 2,4,6, sem ganhar outra ação. Custos nativos debitados uma vez por uso.
- **4 casts focais de Salvaguarda contra Roc** (sem segundo inimigo): quatro sucessos, três danos ímpares cuja metade foi arredondada para baixo, antes de RD75; quatro cobranças de 55 PA apesar de Vida do Roc intacta.
- **Auditoria independente READ-ONLY:** 20 SQLite nativos, 196 commits, 816 eventos, 168 ataques físicos, 140 acertos, 28 conjurações, quatro saves e três odd-halves, 32 movimentos, 1.540 PA debitados. Cinco adulterações com hashes reconstruídos recusadas, incluindo devolução indevida de PA, teto em metade ímpar, fonte falsamente P4, save falso e bypass de RD.

## Resultado científico, unidade = 4 seeds fatorial

- Na configuração **RD75 real da ficha PRECREATE**, físico puro retirou **394 PV adicionais do Crocodilo** agregados em relação a alternar três ataques por três descargas (quatro seeds; diferenças físicas−mixed: 94,53,117,130). Na configuração **RD0 LAB**, a diferença foi **434 PV** (119,53,128,134). Ambas as políticas tiveram mesma fita de Crocodilo nos 6 turnos e os mesmos ataques físicos correspondentes de Grifo; os braços trocam ações em turnos pares, portanto não há “dado da mesma ação” nesses turnos.
- A política MIXED gastou **165 PA por cena** (3×55), com dano elétrico residual pequeno ou nulo sob RD75. RD75 não se interpreta como conclusão oficial sobre resistência mágica em qualquer espécie; e as cenas censuraram, não declararam vitórias.
- A amostra é **4 clusters seed, não 16 amostras independentes**. Não calcular TTK / winrate canônicos, nem atribuir superioridade geral de físico sobre magia, pois outras magias e elementos têm contratos próprios.

## Limites e continuidade

A pré-criação VZ continua sem página física P4. Não há uso de geometria larga de linha, empurrão, transformação, reações ou suportes complexos. Nenhum overwrite do baseline R234; `LAB` limiares HP0, iniciativa não rolada e RD mágica carecem de avaliação normativa. Sem Party, O Primeiro, DMG, LEVEL-UP, regras ou benchmark oficial writes.

**NAC-PASS:** local PASS estritamente condicionado; 0/17 contratos terminais, 0/1.875 matriz oficial. **LAST-VERIFIED-UNIT:** R235 (após frio); **FIRST-PENDING:** R236 candidate — ramo Fraco e HP0 com a mesma fonte física de Bestas pré-criadas, sem fabricar KO canônico; posterior alargamento D de espécies distintas e fontes P4 para E.
