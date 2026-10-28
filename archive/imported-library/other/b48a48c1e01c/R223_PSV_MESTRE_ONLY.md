# PSV R223 — Orientação provisória do Mestre para metade ímpar (somente LAB TEST)

**CM-000006 / MESTRE-SIDE / OP-VLAB-FUSION-SANDBOX-01 / 2026-10-21**

## Ordem recebida e precedência

O Mestre disse **“Dano ímpar se não me engano e se não tiver nenhuma regra é arredonda para baixo”**. A formulação é expressamente incerta e condicional. Em pesquisa no Sistema de Combate, Sistema de Magia e DMG-RANK, as fontes examinadas indicam metade de dano, mas não fixam arredondamento de metade ímpar. Logo esta execução estabelece **política LAB TEST provisória** `FLOOR_MASTER_TENTATIVE_TEST`; NÃO cria decisão normativa mundial nem altera página canônica.

## Baseline e ANTES

R222 foi preservada com SHA256 d2820b7bab02e294805848ef0d7a7d7898d7c1c5a1b0b0495edddd41eb58d5cd. Núcleo v0.8.1 da cópia original bloqueava qualquer sucesso SAVE-HALF com dano ímpar antes de lançar efeito. Iniciativa empatada continua bloqueada pela ausência de desempate.

## DEPOIS R223

Uma cópia isolada de `vlab_effects_v08.cast_source_specified_spell` preserva por padrão `EffectBlocked` para SAVE-HALF ímpar e somente admite piso positivo sob política+origem específicas, em cena cujo `provenance` contém TEST. `damage//2` do próprio núcleo resolve o valor: não há motor paralelo, não há RD ou custos inventados. Cada sucesso ímpar registra recibo `R223_TENTATIVE_ROUNDING_EVIDENCE` e campos da conjuração com `TENTATIVE_MASTER_NOT_CANON`.

**Pré-registro:** SHA256 `12e3ea819270e97e754ca22995ec3f0b9da5e140ece93c45f638a040a124fd9b` antes das lutas.

**Resultados:** 12 seeds novas, 48 braços previstos (2 iniciativas × 2 modos de associação RNG por seed); 40 admitidos, 8 bloqueados pré-commit por empates; 8 unidades fatoriais completas. 40 combates censurados por horizonte, 0 KO, 480 commits, 2.942 eventos, 120 movimentos, 360 ataques físicos (40 oportunidades), 30 curas, 138 magias e **4 sucessos SAVE-HALF com dano ímpar arredondado por piso sob hipótese LAB**. Nenhuma luta antiga foi reexecutada.

**Auditoria:** independent `r223_independent_factorial_audit.py` não importa motor nem runner, valida SQLite em modo ro/immutable, SHA256 R18, rolagens, precisão, RD, Vida, PA, geometria, Reação, prereg, ordem, streams e `floor(D/2)`. Todos os 40 bancos PASS. Testes negativos de fonte 4/4 rejeitados **sem mutação pré-commit**; demonstração positiva 61→30 PV, 80 PA debitados uma vez; 5 clones adversariais com hashes finais reconstruídos rejeitados 5/5.

## Fonte e limitações

Os NPCs Varok, Arveth, Eristan continuam propostas Mestre-side; RD mágica foi 0 apenas na fixture. A adjacência é declarada na cena, não regra métrica geral. A mitigação da metade ímpar via piso está **condicional à ratificação normativa expressa do Mestre**. Não reeditar R215–R222 ou suas quarentenas.

## Governança

INSTANCE-ID/writer/fencing não comprovados. Operação em TEST isolado, produção HOLD, Party/O Primeiro NO-WRITE. 0/17 contratos terminais e 0/1.875 células oficiais homologadas. Ciência local condicional, NAC-PASS global HOLD.

## LAST VERIFIED / FIRST PENDING

LAST-VERIFIED: R223 auditada em cópia TEST e empacotamento frio; FIRST-PENDING: decisão de regra mundial para arredondamento, empate de iniciativa, fonte de controle de Besta, transformação Prata1+ e Bateria E com separação física/mágica. NEXT-5: (1) decisão normativa; (2) comparação exclusiva sob regra alternativa quando Mestre ratificar; (3) fechar iniciative tie; (4) buscar controle plenamente source-complete; (5) estudo exploratório R91 sem promoção oficial.
