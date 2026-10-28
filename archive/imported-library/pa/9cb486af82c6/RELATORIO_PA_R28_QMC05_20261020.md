# RELATÓRIO R28 — NATIVE QMC-05 × MOTOR UNIVERSAL DE PA

**MESTRE-SIDE · continuação do R27 · escopo TEST e auditoria documental.**

## Resultado objetivo

**CONCLUÍDO EM TEST:** o bloqueio técnico do R27 (indisponibilidade do código QMC-05) foi superado. A biblioteca forneceu o ZIP `CRAFT-QMC05-DELTA01-20261018.zip` com integridade `e41fb3ca05dc15be244a6c9d301e20ac5aa961f78e39cf7a43bfe8862eee8de1`; seu baseline QMC-05 original tem hash `f2471657eed68b7349518d0a7d902004bd6969e1add7fc0b29741957675a52ff` e 129 entradas. O fornecedor PA R05 original foi também recuperado SHA `6f69fd1ef197851e128c2fc7becbad1f2a14a1438e7bf9ac71742b835f99078e`.

O `qmc05.py` real, em cópia TEST, recebeu somente uma opção `--pa-r28` e uma opção de cenário `--pa-projeto-json`. `PATCH_QMC05_ORIGINAL_R28.diff` registra alteração; a baseline está guardada e não foi reescrita no cânone. A chamada efetiva é `QMC05 real → R28 adapter → R27 real → R26 real` e retorna classificação, confiança, custos tipados e proveniência. A CLI prévia não foi quebrada.

## Demonstrações e denominadores

1. **Lâmina Eclipse histórica:** 2/2 efeitos QMC05 identificados; 1 sem modalidade explicitamente suficiente; todos preservados com literal e UUID. A rotina externa executa consulta histórica sem reprecificação. PA histórico ausente permanece ausente, não zero.
2. **Cenário TEST derivado de E01:** rank Prata com confiança MÉDIA, 6 PA/dia do efeito ativo e 7 PA por uso conforme R27; falta duração exata; projeção do item total = NULL / pendente, sem criação de item, custo ou exceção oficial.
3. **R27 anterior como regressão:** item sintético Ouro com +2 SAB, passiva Prata, ativa Bronze: 25 PA/dia, 3 PA/uso, duas ativações 6 PA, 31 PA no cenário. Não constitui preço do item histórico.
4. **Auditabilidade:** 179/179 testes CRAFT, 28/28 extensão DELTA01, 30/30 novos R28, 211/211 regressões PA R22–R27 = **448/448** após execução do runner. Casos de materialidade, duplicidade, UUID, custo histórico, origem, modo de habilidade e chamada real via CLI cobertos. Estes testes não comprovam acerto universal de ranks ou execução mágica física.

## Estado canônico, TEE e NAC

- **TEE(TEST): PASS** — `qmc05.py` em CÓPIA LAB efetivamente chama a ponte, inclusive por subprocesso de entrada nativa. **TEE(PRODUÇÃO): HOLD** — nenhum runtime oficial alterado.
- **NAC-CONT-03 documentação(TEST):** Notion LAB é destino único, ANTES seguido de DEPOIS e readback. Originais QMC05, R27, R26 e R05 preservados.
- **NAC-PASS-02 proporcional TEST:** PASS de integridade dos artefatos, regres­sões, contrato e ligação nativa local, sujeito ao readback deste DEPOIS; **NAC-PASS produtivo: HOLD**.
- **NAC-NORM / GNN / GP-NAC:** promoção da nova interface e norma de tarifas para produção **PENDENTE**. PR-SC exige revisão JIT e não elimina prioridades canônicas; SC-3/4 dependem de autorização própria.
- **Governança CRAFT:** F5 RED, C19-021 UNKNOWN, writer/lease/epoch/fencing não demonstrados. Esse HOLD é produtivo, não impede LAB.
- **Validação externa:** Notion Mestre da Lâmina Eclipse reaberto na execução, `last_edited_at=2026-10-03T13:19:53.073Z`, igual ao as-of do readback de teste; texto de Eclipse Total e Corte Lunar localizado na fonte. Isso não autentica automaticamente byte a byte cada arquivo histórico pela plataforma.
- **TARIFA:** motor herdado usa 60% da tarifa passiva por ativação. O R28 não altera esse valor. Confirmar origem normativa expressa antes de P4; divergência documental eventual tem precedência de Mestre, não de suposição do motor. Custos históricos intactos.

## Primeira pendência verificável

A etapa técnica QMC05 original → PA R27 em TEST está concluída. Para homologação produtiva falta uma instância CRAFT competente e sem concorrência instalar a alteração testada no entrypoint de produção autorizado, executar readback/TEE no runtime destinatário, resolver F5 RED/C19-021 de modo legítimo e promover interface/tarifa via NAC-NORM-01 + NAC-PASS-02. Não exigir outro laboratório, item/receita ou reconstrução do motor.

**Não houve:** alteração de Party/O Primeiro, produção, item, receita, REC-ID, C19, runtime oficial ou preço histórico.
