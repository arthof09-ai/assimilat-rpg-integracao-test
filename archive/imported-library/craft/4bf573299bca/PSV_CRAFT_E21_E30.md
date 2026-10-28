# PSV — CRAFT E21–E30 | R48 nativa + PA R39 + Pingente v1.3

**AS-OF:** 20/10/2026 · **MESTRE-SIDE** · `CM-000002 / CM-000002-WS0001` · `OP-ARQ-RIN-REC-01` · **LAB TEST**. Unicidade da receita: `LAB-CRAFT-VIGILIA-BOREAL-20261020-001`.

## Resposta às sete perguntas da Coordenação

1. **R48 original executável nesta instância? SIM.** R40 pacote autêntico SHA-256 `899ea34d81025356af26b462272273244c8405f05493f6f664aa05ad9d481f11`; manifesto 185/185; script R40 canário executado nesta instância `PASS_R48_NATIVE_ORIGINAL_CANARY`, TLI/MICA exclusivamente `SYNTHETIC`; rejeição original do Pingente `ONLY_TWO_EXISTING_RECIPES` preservada como baseline, **não** resultado novo da extensão. Arquivos R48 originais hash: `r48_factory.py` `872dc5bf1e588a9ba6f4c45421a4dddbbe7d261842a4e951fd684bfc374c6801`; `r48_store.py` `e6f684e80e0d5c95dff8ea94cbae985b0a8e046b48886d593d6e49534f046bd1`; `r46_evidence.py` `c869d80f243b349d817c63bd0c40fc08d7b43c98ce54ec9c91d62cd42c73c85e`.
2. **R48 estendida reconhece Pingente? SIM, LAB TEST.** Diff mínimo em **cópia**: 1) `r48_factory.py`: exceção da terceira chave só com identidade do mesmo caso, separação `STRUCTURAL_TEST` / `MAGIC_TEST`, consulta ao **envelope qualificado real do R39**, trava PA-Livre TEST e trava de magia; 2) `r46_evidence.py`: registro do terceiro tipo TEST. `ALLOWED_RECIPES` histórico mantém TLI/MICA. Arquivos originais, R44, R47, R26 e R27 não editados. Diff: `R48_TEST_DIFF.patch`.
3. **Superou a barreira de duas receitas? SIM.** Pedido nativo novo da terceira chave `SBX-VIGILIA-BOREAL-R48-TEST-v1` processado via `IntegratedFactory.process_batch`, R44 engine, R46 EvidenceVault, R47 AuthenticityVault, R48 journal e `DurableFactory.commit_batch` em store TEST recém-criado. `SBX-R48-BATCH-VIGILIA-DURABLE-STRUCTURAL-NEW` / ordem `SBX-R48-ORDER-48322` → `EXPERIMENTAL_QA_PASS`, **apenas QA estrutural totalmente SINTÉTICO**; amostra = `SYNTHETIC_OUTPUT_ONLY`, magic_transfer_proven = false. Recibo SHA-256 `394132efe12a1f83e7f2fd62dd0dca09a7a3374a4ef080fac25426f8355b8c37`. O mesmo pedido tipo `MAGIC_TEST` foi **rejeitado nativamente** `MAGIC_TRANSFER_NOT_DEMONSTRATED`, antes do commit. Chave estranha continua com rejeição.
4. **PA correto? SIM, como consulta prospectiva.** R39 pacote SHA `daf7d6d5058fca308df62bc593795868df080cded1107edb2f80cf8a11a71b32`; módulo original `envelope_craft_qualificado` realmente executado, encadeando `CONSULTA_MOBILE_R34 → R27 → R26`. Envelope entregue SHA-256 `1d4e43e1f8b21106e0c8fee25bab53a81528e4a903f3184852b768dade48c4ea`. **RI Prata E3; RE Bronze E3 PASSIVA, RE Prata E3 ATIVA; RIn separados**. **12 PA/dia**, **7 por ativação**, **26 com duas**. R39 auditou cinco trechos de quatro fontes, sem prova RE E0 independente; ressalvas: rank de cristal/erva não comprova transferência. `r48_pa_gate.py` é **somente consumidor de envelope/hash/versão** e compara recibo escopado, não classifica nem calcula PA. `pa_livre_fixture` é saldo fictício para testar bloqueio, não débito real.
5. **Estoque/journal?** R48 store original reaberto (`DurableFactory`): sequência **0→1**, duas versões imutáveis em commits, R44 e R47 um evento cada, estoque exclusivamente sintético: cristal 1→0 un, erva 1→0 un, fibra 45→0 cm; TLI/MICA inalterados, **estoque real/oficial 0 efeitos**. Reenvio idêntico mantém sequência 1, sem consumo repetido. Pedido mágico rejeitado não gerou journal nem alterou o store. Reabertura por `recover(expected_head=...)` e `factory.audit()['ok']` PASS.
6. **Magia demonstrada? NÃO.** H1 alojamento de materiais ativos, H2 transferência própria, H3 gatilho PA real, H4 retenção após uso continuam **PROPOSTAS**. R46/R47 usam certificados e instrumentos de fixture **públicos e falsos**, sinal `SIMULATED_CRYPTO_VALID_NOT_REAL`: uma assinatura válida em TEST não é prova de calibração real. O R48 nativo processou transições de software e **nenhum componente material observado**. A passiva 1m e a faixa ativa 1m/1 turno continuam sem medição. Nenhuma % de retenção/quantidade física foi inferida.
7. **Próxima dependência real:** observador e método legítimos de QA mágico que permitam verificar **efeito da fonte antes/depois da montagem**, em contraste com os controles E11–E20, mais materiais e especialista/ferramentas efetivamente disponíveis. Mestre/autoridade de magia deve decidir a competência de transferência/inscrição apropriada, **sem inventar norma**. Executor CRAFT pode vincular prova independente futura aos contratos R46/R47 e submeter novo pedido mágico à **mesma árvore** em cópia TEST. Enquanto ausentes, o ramo mágico deve seguir `MAGIC_TRANSFER_NOT_DEMONSTRATED`.

## Superfícies de aceite — não colapsar

| Superfície | Estado | O que foi comprovado |
|---|---|---|
| Classificação de item e efeitos | **PASS parecer E3 TEST** | RI/RE separados, fontes, hash e ressalvas R39; não RE E0 |
| Consumo energético | **PASS fornecedor TEST** | R39→R34→R27→R26, 12 / 7 / 26; não gasto histórico nem debitado |
| Integração nativa R48 | **PASS LAB** | Chave terceira, negativos, R44→R46→R47→R48, journal, readback |
| Montagem estrutural | **PASS software sintético; material NÃO OBSERVADO** | Transição de quatro operações e amostra *simulada* |
| Transferência/retensão mágica | **NÃO DEMONSTRADA** | Rejeição correta, sem observação |
| Produção oficial / RC5 / P4 | **HOLD** | F5 RED, C19-021 UNKNOWN-EFFECT, sem writer/lease/epoch/fencing |

## Testes novos realmente executados nesta instância

- **40/40** regressões originais R48 na árvore estendida, após corrigir interferência inicial no `ALLOWED_RECIPES` histórico.
- **32/32** testes do R39 original, sem reconstruir fornecedor.
- **28/28** testes adversariais da extensão em R48 original: falsificação de URL, alteração de classificação, tarifa/recibo, falta de PA em TEST, R47 adulterado, ferramenta/QA faltante, rollback, replay, store órfão, lote, coexistência de três receitas e ausência de material oficial.
- **100/100 no total de métodos distintos** dessas três suítes, também reexecutados num `replay_e21_e30.py` portátil com extração integral dos pacotes autênticos em pasta temporária limpa. O canário e o pedido estrutural são atos funcionais adicionais, **não mais testes contados**. Testes históricos R39 478 ou R40 273 não foram adicionados ao denominador.

## Artefatos e governança

**Arquivos preservados:** R39 ZIP e R40 ZIP originais, hashes, diff TEST dos dois arquivos modificados na cópia, módulo consumidor de envelope, mesma receita v1.3/identidade, testes, nova ordem, recibos, store TEST e script de replay. Não duplicar motor ou REC-ID. Notion Mestre fontes reabertas (cristal, erva, fibra, Véu, Atlas), registrados IDs, versões e limites em `R39_SOURCE_READBACK_20261020.json`; Python não faz live Notion.

**NAC-CONT-03:** ANTES registrado no LAB existente `CRAFT-E21-E30-20261020-ANTES-001`; operação E21–E30 registrada DEPOIS com hashes após pacote concluído. **NAC-PASS proporcional = PASS** para LAB software, código, integridade e recibo sintético nativo. **NAC-PASS produtivo = HOLD**. Sem escrita de Party, O Primeiro, fontes de itens, REC-LIB, PA original, R48 original ou stores FC04 históricos.

**Primeiro ponto retomável:** receber *evidência observacional independente* da mecânica de transferência/retensão; registrar fonte, experimento, amostra, instrumentos/competência, antes/depois e contraprovas; verificar o novo laudo contra R46/R47, recalcular PA **só se efeito realmente mudar** por interface R39/R27 e submeter `MAGIC_TEST` à cópia R48. Produto físico e RC5 permanecem sem autorização.
