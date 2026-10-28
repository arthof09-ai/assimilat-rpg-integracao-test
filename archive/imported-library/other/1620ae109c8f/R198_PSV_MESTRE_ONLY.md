# VLAB R198 — PSV MESTRE-SIDE / EXPERIMENTAL

AS-OF: 2026-10-19
IDENTIDADE: CM-000006 lógico. INSTANCE CM-000006-I0001 somente candidata; nenhuma writer/epoch/lease/fencing legítima confirmada.
OPERATION: OP-VLAB-FUSION-SANDBOX-01. WORKSTREAM CM-000006-WS0001 condicionado.
BASELINE: R01–R197 preservado; SHA256 físico R197 6b63f53ea35627f390feee8b695380ee9ea1bba8654c5ca2e0e4447219029602.
MOTOR UTILIZADO: R18 `event_commit` SQLite local + v0.8.1 `apply_weapon_attack`/`begin_source_turn`/`end_source_turn` + `vlab_rd_v08`; agregador da R197 e código aditivo limitado, sem reescrita dos históricos.

## RESULTADO FUNCIONAL P0

- MICROBENCHMARK PRINCIPAL: 4 pares de páginas reais × 10 seeds pré-registradas (2 desenvolvimento e 8 reservadas) = 40 tentativas. 38 lutas COMPLETAS por KO, 2 empates de iniciativa não julgados **antes do commit** (0 censuras pós-início). 389 ataques, 427 commits, 1.167 eventos. Sem repetição R196.
- Pares: Capanga 1 (ED P3) × Lobo P1: 0 vitórias ED, 9 Lobo, 1 empate precommit; Capanga × Cabra P1: 0 ED, 10 Cabra. Liu Xiaua (ED P5 normal) × Lobo P1: 10 ED, 0 Besta; Liu × Cabra P1: 9 ED, 0 Besta e 1 empate precommit.
- MÉDIAS RODADAS terminadas: respectivamente 7,78 / 7,0 / 3,4 / 3,67.
- MECÂNICA EXPLICATIVA: Ataque literal do Capanga `2d6+25`, máximo comum 37; CA da Cabra =39, impossível acertar sem crítico positivo no recorte. Cabra `2d6+25` para acertar com DES25 LAB sem Luta nomeada; supera CA25 de Capanga nos dados comuns. Zero acertos de Capanga contra Cabra em 60 tentativas observadas; 70/70 acertos da Cabra contra Capanga. Isso evidencia desvantagem grave do *recorte*, NÃO prova rank canônico inválido.
- 4 críticos POSITIVOS e 2 NEGATIVOS documentados no microbenchmark (R42 negativa LAB, não regra homologada).
- PILOTO ENERGÉTICO SEPARADO: Ong Mefita ED P2 × Lobo P1; 4 seeds × 2 políticas pareadas = 8 combates completos. 20 Chicotes de Água executados em v0.8.1 bridge, 160 PA debitados em mesmo `event_commit`; com recusa da magia, 0 lançamentos e 0 PA. Lobo ganhou as oito lutas; em duas seeds a magia causou dano ao Lobo, em duas não acertou. Não há influência demonstrada sobre o vencedor. R198 magia = 96 commits e 284 eventos / 68 ataques normais ou mágicos.
- TOTAL DESTA ENTREGA: 46 combates completos de TEST, 2 empates de iniciativa recusados antes do commit, 523 commits, 1.451 eventos, 457 ataques; 5 pares distintos, 14 seeds distintas entre duas coortes (10 na matriz, 4 no piloto de magia). 0 amostras de espécies independentes além das fichas escolhidas; seeds pareadas de políticas não aumentam a diversidade de adversários.
- INTERFACE: R197 preservada. Nova quarta aba `Combates executados` exibe os 38 confrontos R18, 8 do piloto PA, taxas observadas por par, resultados por seed e eventos ofensivos com dano/RD/HP/crit/PA. HTML offline CONSULTA recibos embutidos, NÃO inicia Python nem cria luta nova. Testado em viewport celular com zero exceções JavaScript.

## ADMISSIBILIDADE E SEGURANÇA

- **RESULTADO CONDICIONAL COM SENSIBILIDADE CONHECIDA**, não combate fonte-completo nem benchmark oficial. Nomeação de proficiências de Bestas, tipo exato de danos agregados e RD do Capanga são lacunas: Hipótese LAB sem Luta/Init nomeadas; RD Capanga 0 apenas como cenário; `impacto` para agregados não tipados é somente hipótese LAB; Besta Prata RD geral15 condicionalmente derivada.
- Cena de contato inicial adjacente, sem deslocamento, voo, terreno, magia/efeitos não usados. Cabra Investida/duplo e Lobo Força Ancestral/agarrão fora do recorte: não aferir poder integral da Besta. Não houve Reações novas; armadura e Defesa R174/R186 continuam preservadas como evidência, não reexecutadas.
- Ong: chicote `Ataque 4d6+INT`, `8d6+28`, 8 PA. Extensão usa resolvedor nativo de acerto e dano, mas seu protocolo de crítico para magia, economia de ação, desconto de Evocação, bônus de itens e alcance permanecem condicionais TEST. Nenhuma conclusão de magia plenamente homologada.
- Auditor por código separado reproduziu 38 bancos físicos/389 ataques e 8 bancos mágicos/20 PA eventos, sem executar novos ataques. Falsificações de campos semânticos após recomputação dos hashes SQLite 7/7 rejeitadas por auditores separados. NÃO é homologação independente externa.
- NAC-CONT-03: leitura física de fontes e estados; escrita Notion NÃO realizada por falta de writer; Biblioteca utilizada como persistência experimental versionada autorizada. NAC-NORM-01: regras oficiais intactas. NAC-PASS técnico TEST condicionado; terminal/produção HOLD.
- Contratos: **0/17** certificados. Grade oficial: **0/1.875**. Piloto experimental não preenche automaticamente células oficiais. UNKNOWN_EFFECT históricos intocados. RUN-IDs novos R198 nunca reutilizados.

## NEXT-5

1. Priorizar adversários Prata 1–3 e ajustar comparações com patamar semelhante (não alterar stats).
2. Testar impacto da hipótese de RD do Capanga / proficiências nomeadas por ramos pré-registrados, sem refazer R198.
3. Integrar uma habilidade especial relevante da Cabra ou Lobo quando literal de ação/condição/alcance permitir.
4. Expandir o núcleo magic-attack source-gated com decisões normativas de crítico e ação/alcance, antes de chamar magia homologada.
5. Investigar UX conversacional para solicitar novas lutas sem terminal; manter offline como leitor honesto até integração autorizada.

FIRST-PENDING: fonte de Luta/Iniciativa de Bestas, tipagem/RD Capanga e adjudicação formal de magia; nenhuma writer Notion comprovada.
