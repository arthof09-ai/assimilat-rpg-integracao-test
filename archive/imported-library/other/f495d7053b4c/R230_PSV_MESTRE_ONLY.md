# VLAB R230 — Bateria B / movimento e ataque de Bestas sob fonte — PSV MESTRE-ONLY

**Executor lógico:** CM-000006, ambiente TEST, produção/Party/O Primeiro/fic​​has NO-WRITE. **ANTES:** R228 movimento fonte-delimitado de Iskiel mas velocidade 12 m de Varok apenas fixture. **DEPOIS:** cinco velocidades de Besta efetivamente calculadas a partir da **Regra 8 — Velocidade** de `Criação de Besta`, [página Mestre](https://app.notion.com/p/3ebc2b324ede81f4992ac88a3588cacd), congeladas em extrato reaberto; atributos `DES` escolhidos explicitamente por fábrica LAB L04. Outros parâmetros provêm das Regras 4/7 e da fábrica L04, mas a habilidade de ataque-base como Ação Padrão continua uma **hipótese transportadora TEST**, não uma certificação completa da espécie.

**Mecânicas executadas:** `move_via_verified_path` e `apply_weapon_attack` da cópia nativa v0.8.1, com um commit R18 por cena. Movimento usa limite exato racional e percorre um segmento reto aberto de teste cujo comprimento inteiro foi escolhido **dentro** do limite, não calculado arredondando a velocidade como norma geral. O ataque de cada Besta é físico contra ED sintético Bronze1 desarmado, sem crítica (fita de crítico NORMAL dirigida). Não existem turnos adversários, reação ou combate completo neste experimento.

| Rank da Besta virtual | Velocidade exata | Distância percorrida | ED após golpe |
|---|---:|---:|---:|
| Bronze1 | 39/4 m | 9 m | 11 PV |
| Prata1 | 27/2 m | 13 m | 3 PV |
| Ouro1 | 69/4 m | 17 m | 0 PV |
| Ouro Negro1 | 83/4 m | 20 m | 0 PV |
| Lendário1 / Titã | 209/4 m | 52 m | 0 PV |

**Resultados físicos:** cinco SQLite válidos, **5 commits, 15 eventos, 5 movimentos nativos, 5 ataques nativos**. O auditor externo lê `sqlite3 mode=ro`, valida journal R18/chain/state, fórmula de velocidade recalculada independentemente, ordenação movimento→RNG→ataque, bônus de proficiência, 3d6–20d10, CA, dano e PV final; `PASS_R230_INDEPENDENT_R18_NATIVE_BEAST_SPEED_TEST_CONDITIONAL`.

**Quarentenas:** três RUN-IDs não reutilizados, dos quais dois falharam antes de intenção e um preserva intenção pendente `UNKNOWN-EFFECT` após reconstrução incorreta da CA racional; nenhuma das três cenas entrou no denominador ou sofreu replay.

**Fonte e limites:** não existe espécie canônica física nos cinco ator snapshots; rank/star e atributos são combinações virtuais genéricas. ED Bronze1 mais fraco e HP0 não provam morte canônica ou vitória. Adjacência/range foi verificada apenas na fixture aberta; blocos↔metros do mundo continuam HOLD. Fonte matemática da Regra8 foi recuperada, mas não confunde hash de extrato com hash de página Notion integral.

**NAC-PASS local:** PASS TEST condicional; **oficial** HOLD, 0/17 e 0/1.875. **LAST-VERIFIED-UNIT:** R230 cold readback quando publicado. **FIRST-PENDING:** combate multiturmo de uma Besta com ficha completa e adversário/controle real, não multiplicar seeds de uma única cena.
