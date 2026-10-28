# PSV — Auditoria e correção CRAFT × Sistema Universal PA

**Data:** 20/10/2026. **Ambiente:** MESTRE-SIDE / LABORATÓRIO CRAFT existente. **Origem:** correção expressa do Mestre ao relatório do Executor CRAFT. **Identidade/writer CRAFT:** não reivindicados. **F5:** RED. **C19-021:** UNKNOWN-EFFECT.

## Decisão expressa

O motor R26/R27 estava certo. O pré-validador CRAFT interpretou incorretamente as tarifas de habilidade ativa. Correto: PASSIVA 100% da base/dia; ATIVA floor(50% da base) por dia + floor(60% da base) por uso. O piso do rank do ITEM é separado.

| Rank habilidade | Tarifa base | Passiva diária | Ativa diária | Ativação | Piso diário ITEM |
|---|---:|---:|---:|---:|---:|
| Bronze | 6 | 6 | 3 | 3 | 8 |
| Prata | 12 | 12 | 6 | 7 | 11 |
| Ouro | 24 | 24 | 12 | 14 | 21 |
| Ouro Negro | 35 | 35 | 17 | 21 | 35 |
| Lendário | 50 | 50 | 25 | 30 | 90 |

## Diagnóstico físico

Recuperado `CRAFT_RECIPE_PA_FLUXOS_E_TEST_20261020.zip` (SHA256 `9c2e299de21a36a8c3d93c781c32ad1cb946ba264b9429e3d46478c2fd3990e9`, 19 entradas, manifesto 18/18). A função `MASTER_POLICY` do arquivo `pa_nac_preflight.py` exigia ativa 60% base/dia e ativação de 100% base, configurando falsa incompatibilidade. Os testes originais aprovavam essa configuração equivocada: 41/41 +26/26; portanto seus PASS não demonstravam conformidade com a última decisão do Mestre.

Motor R27/R26 original reexecutado, sem modificação de seu código, com a entrada original `815b6600c3fca27b030da4326159ea740fda98709e6581caf92eed37b85bd379`. A saída foi idêntica ao recibo preservado: Pingente TEST Prata, passiva Bronze 6 PA/dia, ativa Prata 6 PA/dia +7 por uso, duas ativações 14 PA, total 12+14=26 PA no dia. Piso do item Prata 11 já coberto pela soma diária de 12.

## Correções implementadas

- CRAFT v1.2: pré-validador e testes adaptados à decisão correta, com checagem independente de totais e negativo para tentativa de exigir 60%/100%.
- Documentação v1.2 limpa; versões v1.1 e ZIP original preservados em histórico para auditoria.
- `PA_TARIFF_VERSION_MISMATCH` por essa falsa incompatibilidade retirado; a consulta real fica válida como **parecer energético prospectivo E3 TEST**, não item canônico.
- Segundo problema revelado: depois de preencher PA, o auditor estático subiu de RC4 para `RC5(TEST)` por campos preenchidos. O gate de materialidade v1.2 limita a `RC4(TEST)` porque não há demonstração de transferência mágica.
- Sete páginas Mestre originais corrigidas por errata identificada `PA-CRAFT-TARIFA-ERRATA-MESTRE-20261020-001`; **7/7 reabertas, uma ocorrência por destino**, sem apagar a versão histórica.
- Inbox existente CM-000002 atualizado no mesmo item: `PA-R29-R38-CRAFT-HANDOFF-20261020-001`. Status NOVA, sem ACK presumido.

## Engenharia da receita TEST — parecer

**Acertos:** fluxograma geral coerente e PA obrigatório; função de produto antes de ingredientes; busca e separação de fontes; receita com BOM, mecanismo falsificável, controles de QA, perdas e riscos sinalizados; separa produção do laboratório; protege Party e itens antigos. Fonte do Cristal Aurora e da Erva do Norte reabertas no Notion Mestre: iluminação/dissipação, reserva luminosa respectivamente. Fibra PS é ligante físico e não recebe poder inventado.

**Falhas e limites:** leitura da política PA errada e falso HOLD energético; testes originais assertavam regra inválida. O mecanismo mágico entre cristal e pingente não foi demonstrado. `0,45 m` de fibra e `55 minutos` são premissas TEST; espécie-fonte, unidades, perdas, ferramentas, especialista e custos MED ainda exigem prova. O QA estático sozinho não pode promover RC5. Rank Prata de item e habilidades Bronze/Prata são E3 revisáveis, não certificação universal nem P4.

## R48 autêntico recuperado

`CRAFT-COMESTRE-CHAT-v03.zip` SHA256 `5a9af3ae0568031a59a0248843a3f40b8c020c070b8f00c20eb678d9ec844434`: fábrica R48 original extraída e **40/40 testes executados PASS** nesta sessão. FC04 delta SHA256 `5756bdf2e6e0550336d483c0c749a411ab345bf39b1168d585d1a883f077bf9b` recuperado e auditado em cópia: quatro stores saudáveis, um estado órfão corretamente rejeitado; apenas produtos TEST sintéticos. R48 reconhece TLI/Mica e FC04 inclui B30-22: **não possui adaptador nem execução do Pingente**. A dificuldade de obtenção do binário foi superada; o teste de nova família/mecanismo ainda falta.

## Auditoria final

- **56/56** testes novos e revisados de CRAFT v1.2 — PASS.
- **26/26** regressões do pré-auditor anterior — PASS.
- **40/40** testes da fábrica R48 original — PASS, suíte separada.
- **7/7** erratas Notion, readback único — PASS.
- **38/38** arquivos manifestados no pacote — SHA256 PASS; 39 membros ZIP incluindo manifesto; CRC PASS; extração limpa e replay **82/82** CRAFT — PASS.
- **Primeiro efeito indevido detectado e evitado:** falso positivo RC5 do auditor após PA correto; gate efetivo RC4(TEST), fabricação negada.
- **NAC-PASS documental/TEST:** PASS no escopo preciso. **NAC-PASS de fabricação e produção:** HOLD. `CRAFT/F5 RED`, `C19-021 UNKNOWN`, writer/lease/fencing sem comprovação, sem produtos/REC-IDs/Party/O Primeiro alterados.

## Artefato corrigido

Biblioteca Mestre: `/Comestre/CRAFT_PA_CORRIGENDA_MESTRE_TEST_20261020.zip`, Library ID `libfile_73688a2aa70881918e7cbdd247c08b84`, 410894 bytes, SHA256 `ab880817ca732743011ee1f8f0269e303f6564e3a98c9a50fdf57ef7cd6320fa`.

**Notion:** [Laboratório CRAFT](https://app.notion.com/p/3fbc2b324ede811db848d35d4739eb00), [PR-ITEM-02](https://app.notion.com/p/3eec2b324ede81ecb058f59f5b67e4f4), [PR-SC-01](https://app.notion.com/p/3f1c2b324ede815e939ff6fd3a8726b1), [Inbox CM-000002](https://app.notion.com/p/3ffc2b324ede81669f23c74ef48ceef8).

**Primeira pendência real:** engenharia e ensaio discriminatório de transferência mágica, e adaptador TEST da receita de Pingente ao motor R48, com parâmetros de processo e materiais verificáveis. Produção oficial requer gates de writer/fence e liberação F5 independentes. Não pedir ao PA para reimplementar tarifas já corretas.
