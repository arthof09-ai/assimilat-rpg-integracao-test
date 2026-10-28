# R23 — Plano prospectivo de evidência EMPÍRICA B15 (não executado)

**Estado:** PROPOSTO/MESTRE-SIDE. Contrato original B15 `ELEMENTAL_WEAKNESS`. **STRICT** 0/2. Uma ação B15 comprovada não fecha automaticamente luta completa.

## Premissas oficiais
- Sistema de Combate vigente: https://app.notion.com/p/3ebc2b324ede81f1be4be8804ac113c0
- DMG-RANK v1.1 §21–22 e §32: https://app.notion.com/p/3f2c2b324ede815498cddb7844245f7e
- Dano físico e elemental devem permanecer em pools separados; bônus de 3 dados incide SOMENTE no maior dado elemental ao qual o alvo tem fraqueza fonte-confirmada. Não aplicar automaticamente a veneno.
- Exemplo canônico é ilustração normativa; é proibido transformá-lo em arma real inventada.

## Escolha mínima da cena prospectiva
1. Mestre designa uma cena válida para coleta, consentimento/escopo do teste e atores; CM-000006 mantém execução oficial quando autorizada.
2. Fonte física existente do ataque deve discriminar dois pools: cortante/impacto e Fogo com quantidade/tamanho de dados, custos, ação, alcance e elegibilidade. Se nada fonte-comprovado existir, **HOLD**, sem adaptar uma arma à força.
3. Alvo da cena precisa comprovar Fraqueza a Fogo em regra/vigência específica. A palavra “Gelo” na espécie não basta sozinha; vulnerabilidade genérica precisa autoridade de correspondência.
4. Congelar fonte de ataque/target, effective_at, epoch, estado de combate, geometria, fontes da RD, eventual resistência/imunidade, e ação/reação antes de executar.

## Evento mínimo a recolher, ordenado
1. **PRE-FLIGHT:** Selecionar fonte operacional realmente existente e alvo com Fraqueza a Fogo expressa; congelar versão e tags. Se qualquer elemento faltar, não iniciar combate STRICT.
2. **BEFORE:** Persistir fotografia assinada cena/atores, pools separados, mitigação, PA, alcance/LoS, inventário e ações autorizadas.
3. **DECLARE/HIT:** Registrar ação escolhida, testes e reação legal, ataque aplicável; confirmar um hit ou efeito válido conforme fonte.
4. **DAMAGE:** Registrar cada dado do pool físico e Fogo, +3 dados DO MESMO maior dado Fogo por fraqueza; manter componentes separados para RD/mitigação.
5. **COMMIT:** Registrar dano efetivo por componente e Vida/Alma antes/depois, status e custos; não dobrar efeito em retry.
6. **CONTROL:** Executar contraprova DOCUMENTAL OU EVENTO TESTE ADICIONAL autorizado: alvo sem fraqueza/ataque sem tag Fogo não recebe +3d6. Contraprova não equivale ao evento positivo.
7. **REPLAY/PASS:** Recuperar recibos e fontes independentemente, refazer cálculo, provar igualdade com COMMIT e submeter critério integral e gates ao aceite; não confundir EVENT-B15 com full-fight STRICT.

## Dados necessários para aceitação

Cada chave abaixo exige valor e fonte, não `UNKNOWN` inventado nem 0 presumido:

- `scene_id`
- `event_id`
- `event_timestamp`
- `authorizing_master_decision_id`
- `source_epoch`
- `actor_id`
- `actor_source_sha256`
- `target_id`
- `target_source_sha256`
- `action_id`
- `action_economy`
- `source_action_url`
- `source_tag_physical`
- `source_tag_fire`
- `target_fire_weakness_source`
- `target_weakness_active`
- `range_los_receipt`
- `hit_save_receipt`
- `reaction_slot_before_after`
- `rolls_physical`
- `rolls_fire_base`
- `rolls_fire_bonus`
- `damage_physical_raw`
- `damage_fire_raw`
- `rd_resistance_by_tag`
- `rounding_and_mitigation_rule`
- `net_damage_physical`
- `net_damage_fire`
- `target_hp_before`
- `target_hp_after`
- `pa_before_after`
- `commit_id`
- `executor_identity`
- `proof_of_no_duplicate`
- `independent_readback`
- `strict_source_gate`
- `nac_pass_verdict`

## Ilustração aritmética (SINTÉTICA, NÃO É CENA)

- Ataque fonte *hipotético* com `1d8 físico` e `2d6 Fogo`, alvo com fraqueza Fogo; rolagens demonstrativas `1d8=6`, `2d6=[4,2]`, `3d6` extras `[3,5,1]`.
- Bruto sem fraqueza: `6 + 4 + 2 = 12`. Bruto com fraqueza: `6 + 4 + 2 + 3 + 5 + 1 = 21`. O aumento `+9` afeta apenas o pool Fogo. Mitigação e resultado líquido desconhecidos: **NÃO APROVADOS** sem fonte da cena.
- Controle negativo: com a MESMA ação e alvo sem Fraqueza Fogo documentada, não são adicionados os três dados. Mesmo personagem elemental sem tag de dano Fogo não ativa bônus.

## Aceite B15 e separação de STRICT

O B15 recebe PASS somente com fonte concreta + evento real + execução legal + estado final + reprodução independente e NAC-PASS aplicável. Um registro isolado de dano pode suprir B15, mas não pode ser contado como combate STRICT completo. Os dois confrontos STRICT seguem 0/2 até cumprir seus demais 18 predicados e o executor CM-000006 legítimo.

## Falha mínima e retomada

Se não houver fonte operacional de ataque misto ou alvo com fraqueza expressa, registrar exatamente `MISSING_ATTACK_SOURCE` ou `MISSING_TARGET_WEAKNESS` e não propor combate. Se houver fonte, próximo passo é congelar cena+event_id na autoridade existente, obter execução legal de CM-000006, readback e cálculo por componente.
