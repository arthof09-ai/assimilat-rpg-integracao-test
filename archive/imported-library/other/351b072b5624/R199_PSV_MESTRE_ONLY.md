# PSV VLAB R199 — Combates com Magia, Transformação e Habilidade de Besta

**AS-OF:** 2026-10-19 · **OP:** `OP-VLAB-FUSION-SANDBOX-01` · **WORKSTREAM:** `CM-000006-WS0001` condicionado · **ID:** `CM-000006` lógico; I0001 candidata, sem claim/lease/writer. **PRODUÇÃO:** HOLD.

## Resultado científico primeiro

- **32 combates novos em TEST** (mesmos dois pares já explorados em R198; são novas políticas/seed/RUN-ID, não duas espécies inéditas), dos quais **30 concluíram por KO e 2 foram censurados pelo horizonte**. **16 blocos de seeds distintos**; 2 políticas por bloco. Nenhum resultado de censura contou como vitória.
- **Ong Mefita P2 × Lobo P1**, 8 seeds × 2 políticas: sem transformação, **0 vitórias de Ong / 8 do Lobo / 0 censuras**; com transformação + Chicote de Água, **3 Ong / 3 Lobo / 2 censuras**. 8 ativações de forma (40 PA), 6 encerramentos em combate; 101 lançamentos de Chicote somados nos dois braços Ong; **808 PA gastos em magias** + **320 PA em transformação**. O final antecipado da batalha pode deixar a forma ainda ativa, não é registrado falsamente como expiração.
- **Capanga P3 × Lobo P1**, 8 seeds × 2 políticas: Lobo vence **8/8** em ambos os braços; com `+2 FOR` condicional de **Força Ancestral**, sua média de rodadas passa **7,63 → 7,00**, KO antecipado em 5/8 seeds. 56 ataques foram executados com aplicação do bônus TEST; sem assumir que o bônus não está pré-incorporado à ficha.
- **Errata R198:** `magic_hp_removed` da auditoria histórica usava HP de Ong quando a política declinava magia. Nova projeção *somente derivada*: **0 HP mágicos no braço DECLINE_WHIP**, **163 HP efetivamente retirados por Chicote** nos quatro ramos com lançamento. **Original R198 imutável**.

## Material de execução e evidência

**Motor:** código v0.8.1 `apply_weapon_attack` + RD existente + `begin_source_turn`/`end_source_turn` + R18 `event_commit` nativo. Nenhum novo resolvedor de ataque/dano. `r199_transform_spell_combat.py` é uma **ponte condicional de estado publicado** para a transformação documentada de Ong, **não** prova universal do motor T1/T6 e **não** chama `activate_transformation` v0.8.1 (gate fonte incompleto de Espírito/TAP). A projeção de PA/hp da forma usa a própria ficha como hipótese explicitada, com pools independentes; testes não dão autoridade canônica à hipótese.

**Dados materiais:** 32 SQLite de combate, 575 commits, 1.775 eventos nativos, 488 ataques, roll-tapes e checkpoints; 8/8 adulterações adversariais v2 rejeitadas mesmo após refazer hashes. Auditor de código separado do produtor, porém **não homologação externa**. Preservado incidente `DRY_V1_R199` com um `UNKNOWN_EFFECT/PENDING` oriundo de PA insuficiente, sem retry e sem RUN-ID reutilizado; nova coorte v2 fecha falta de PA com passagem explícita. Histórico R01–R198 não alterado.

**Bancada:** modos antigos R197/R198 preservados; quinta aba de lutas R199 mostra comparação por seed, dano, críticos, HP, RD, PA, eventos de transformação e magia. HTML offline consulta recibos SQLite previamente exportados e **não inicia Python**. 0 novas células oficiais, 0/17 contratos terminais, 0/1.875 benchmarks oficiais.

## Estados científicos

- **VERIFICADO TECNICAMENTE (TEST):** nova sequência luta → magia de Água → débito de 8 PA → forma ativa com INT/CA da ficha publicada → contra-ataque físico do Lobo → dano com RD → duração/expiração/reversão em seis execuções. Ataques normais, críticos positivos/negativos e condições de KO resolvidos por v0.8.1.
- **CONDICIONAL:** Espírito assimilado não identificado no campo Ong; `Vida (__)+54`, `Alma (__)+63`, T6-B sem total homologado; prioridade de debitagem de reservas espirituais; gasto de Reação na Ação Completa; marco exato de expiração; alcance e economia de ação da magia de ataque; R42 para críticos mágicos; proficiência de Luta da Besta; RD0 de Ong LAB; status `+2 FOR` da Força Ancestral (pode já estar nos 24 publicados); alcance/contato fixado como cenário TEST. Essas condições são suficientes para **não** certificar vitória canônica nem poder total de Ong/Lobo.
- **PENDENTE:** Agarrar/Investida, outras magias, duração/manutenção complexa, escolha tática por observação (política atual é pré-declarada), critérios de T1 BAP/TAP da ficha Ong, renovação entre cenas com descanso demonstrado; calibração estatística ampla, auditoria externa e benchmarks oficiais.

## Continuidade / NAC-PASS

**BASELINE:** R198 original ZIP SHA `b7fc08a1cee2891c52fbf8e446ef96da8193430a45268cc141abcbc7a9f6f11b`, com R197/R196 preservados. **P0-A errata corrigida**; **P0-B magia real lançada**; **P0-C transformação real publicada exercitada com hipótese condicional**; **P0-D magia durante forma**; **P0-F habilidade da Besta +2 FOR exercitada condicionalmente**; **P0-G comparação**; **P0-J dashboard**. Requisitos de generalização universal e transformação documental terminal continuam pendentes.

**AUTHORITY:** Notion Mestre e normas em leitura; perfil CM-000006 PAUSED; escritor e instância não reclamados. Nenhuma escrita em Party, O Primeiro, fichas, OP Notion, regras, produção, DMG-RANK. **NAC-PASS:** QA/recuperação TEST proporcional; terminal e normativo HOLD.

**FIRST-PENDING / NEXT-5:** (1) verificar identidade do Espírito de Ong e máximos T6-B sem supor blanks; (2) adjudicar fonte de ação/range/crit do Chicote e prioridade das reservas; (3) verificar se +2 FOR do Lobo já está incorporado; (4) adicionar ao catálogo uma segunda magia e controle/Agarrar com especificação suficiente; (5) novo holdout segregado por identidades e sementes com auditoria externa, jamais validar poder canônico antes da evidência.

**RECUPERAÇÃO:** extrair ZIP em diretório novo, executar `python R199_COLD_PORTABLE_RECOVERY.py /caminho/pacote.zip`. Verificador lê SQLite, não chama produtor nem repete ataques, verifica manifesto/hashes, baseline R198, 32 replays, 8 falsificações e incidente pendente. `new/r199/evidence/R199_BENCHMARK_FROM_REAL_FIGHTS.json` contém métricas por ator/seeds; `R199_DMG_HANDOFF_ATTACK_RECEIPTS.csv` é um handoff **não transmitido** ao DMG.
