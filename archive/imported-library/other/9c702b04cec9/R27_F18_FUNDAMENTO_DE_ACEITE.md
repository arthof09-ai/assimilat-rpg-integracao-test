# F18 — Verificação de aceite terminal: contratos de TODAS as raças gerais (Mestre-side)

**ID oficial:** F18. **Critério original imutável:** `Casos oficiais de cada raça aprovados com pontos/CA/derivados por nível`. **Critério-pai:** `Contratos de progressão para todas raças gerais`. **Status R26:** PARCIAL. **Decisão R27:** CONCLUÍDO **exclusivamente como contrato mecânico geral**, nunca como evolução nativa ou da Party.

## Fonte física / contra-provabilidade

Fonte oficial Notion, reaberta na R27: `Criação de Ficha`, ID `3ebc2b32-4ede-8144-9222-f3c06b840613`, edit `2026-10-09T04:07:06.313Z`; regras R2/R3/R4/R5/R7. O R17 R26 limitava `validate_r17` a Humano `normal_rate=2`; as quatro outras raças eram NEGADAS. R27 mudou `engine_r17.py` EXISTENTE, não `engine_r13.py` histórico, leitor R21 ou gateway R04.

R2 oficial verificada: Humano 25/+2/d6,d6/CA 6+DES+armadura; Orc 25+12 físicos/+5/Vida+2 dados/CA 12+DES÷4+CON+armadura+bônus; Abissiano 25+12 mentais/+5/Alma+2 dados/CA 9+DES+armadura+bônus; Asa Prateada 25+5 DES/+4/Alma+1 dado/CA 9+DES+armadura+bônus; Raça Superior 25+20/+8/Vida e Alma +2 dados/CA 9+armadura+bônus e Velocidade 8+DES÷4. Respeitados limites de criação da R2 sem inventar limites pós-criação. R5: iniciais 10+CON,10+INT; bônus de dado de raça empilhados na categoria; mudança Bronze5→Prata1 rebase 6 níveis pela nova categoria sem cumulatividade indevida. R7 proficiências iniciais =2+INT inicial, SEM conceder proficiências específicas.

## Casos com cálculo fonte oficial; dados de entrada declaradamente ilustrativos

| Raça canônica | Pontos por nível | Bronze HP máx (1→2) | Bronze Alma máx (1→2) | CA (1→2) | Rebase Prata HP/Alma |
|---|---:|---:|---:|---:|---|
| Humano | +2 | 24→33 | 22→30 | 13→15 | 75 / 116 |
| Orc | +5 | 32→46 | 24→34 | 24.0→25.0 | 108 / 225 |
| Abissiano | +5 | 22→30 | 34→49 | 15→20 | 68 / 235 |
| Asa Prateada | +4 | 20→27 | 27→38 | 19→23 | 61 / 184 |
| Raça Superior | +8 | 32→46 | 30→47 | 11→11 | 108 / 341 |

Os arrays iniciais, armadura 2 e escolhas de distribuição nesses 10 cenários são **exemplos fictícios autorizados apenas para teste**. Os números e fórmulas de raça provêm da fonte canônica. FF de exemplos vem de locks DANO fictícios separados, não há CA fictícia de FF no oráculo. Para Orc `1/4 DES` e velocidade Superior `DES/4`, **nenhum arredondamento foi inventado**; as frações são preservadas como quartos exatos representáveis (0,25/0,5/0,75), com decisão específica somente se futuras regras exigirem arredondar.

## Gate original — critério × evidência × resultado

1. **As cinco raças gerais da regra R2:** Cobertura 5/5, nomes e progressões correspondem literalmente à fonte — PASS.
2. **Pontos iniciais e bônus raciais:** 25 / 37 / 37 / 30 / 45; proibição de bônus Orc fora FOR/DES/CON, Abissiano fora INT/SAB/CAR, Asa Prateada fora +5 DES, limites de criação Humano e Superior — PASS, inclusive rejeições negativas.
3. **Progressão por estrela e derivados oficiais:** +2/+5/+5/+4/+8; HP/Alma inicial+categoria, sem apagar recursos atuais; CA por fórmula e deslocamento Superior; proficiências iniciais R7 — PASS por oráculo independente de valores e comparações em memória do motor.
4. **Mudança de categoria:** 5/5 regressões Bronze5→Prata1 com 6 dados da nova categoria racial, recálculo dos máximos e resultado físico do estado local — PASS.
5. **Transação e restauração local:** 10/10 casos em MESMO motor R17/R25/R26 com diálogo de taxa, FIXO, distribuição e CONFIRMO, commit local NORMAL/TRANSFORM/LOCKS, readback dos máximos, segunda execução NOOP, inversão, readback com digest exato — PASS.
6. **Regressão pré-existente:** suíte herdada R26 245/245 preservada, nova suíte 9 testes adicionais e total 254/254 PASS, com `test_fixed_silver_exact_mechanical_parity_r16` PASS; arquivo `engine_r13.py` e pacote R26 originais intocados — PASS.
7. **Fonte correta / autorização:** os contratos são gerais, não escolhas de uma player. Nunca afirmam evolução real, nem autorizam writer, Spirit não humano, equipamentos/títulos verdadeiros ou Party. Prova de teste fonte-canônica não substitui UAT nominal M09–M14/F17 — INDEPENDENTE DE F18.

**Aceite terminal F18 — PASS proporcional ao escopo contratual R20:** a referência M02 já considera o contrato Humano local como CONCLUÍDO apesar de não haver ficha nativa; F18 exige contratos das outras raças, não canário Notion. Não conte os 10 casos como 10 requisitos; conte **apenas F18**. NAC-PASS material do sistema de evolução permanece HOLD.

## Trilha

- Golden independente: `tests/test_r27_all_official_races.py` (expected estático, diferente do código de cálculo).
- Executado com estado e hashes: `evidence/R27_F18_CANONICAL_RACE_CASES.json`.
- Matriz oficial 32 linhas: `R27_ACCEPTANCE_GATE_32.json`, F18 = CONCLUÍDO, F30 ainda PARCIAL.
- Arquivo R26 original SHA `4dff605beb6add83741d57bdfe9cf72ff27c8741836c71db4c1bd7accefae948` mantido aninhado sem modificações.
