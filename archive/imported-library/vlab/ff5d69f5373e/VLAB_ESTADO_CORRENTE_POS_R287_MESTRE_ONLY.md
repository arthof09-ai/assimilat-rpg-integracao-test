# PSV — VLAB | Checkpoint MESTRE-SIDE após R287

**Operação única:** `OP-VLAB-FUSION-SANDBOX-01` • **perfil lógico:** `CM-000006` • **ambiente:** LAB/TEST Mestre-only • **origem:** LAST-VERIFIED R283 • **retomada:** FIRST-PENDING CANDIDATE R288.

## ANTES

R273 tinha ampliado compatibilidade, auditoria e proteção de cenas originais R234–R240. R274–R283 acrescentaram cura sintética pela CLI R18, preflight, auditor de recibos, detecção de adulteração, recuperação crash/WAL e 64 sementes diretas, publicados como ZIP separado na Biblioteca. O R19 web histórico permanecia compatível com o R18 original mas não disponibilizava a nova opção de cura. Os dados originais, contratos e o writer Notion não foram substituídos.

## DEPOIS físico: R284–R287

- **R284:** web R19 integra o mesmo comando `HEAL` e preflight do R18, acionando v0.6 histórico com fixture `1d6/0 PA` fictícia exclusivamente TEST; botão só surge no turno correto e com Vida ferida. Histórico, página do combate e recibo exibem cura LAB. Nenhuma magia real ou custo normativo implementado.
- **R285:** rotas web de visualização de índice, execução de nova ação, backup, restauração e reinício verificam origem pelo auditor independente **antes** de promover um registro de hash genérico a recibo considerado válido. Oito testes adversariais/positivos novos PASS. Journal adulterado não rende backup, restauração, nova ação ou resultado aparentemente verificado.
- **R286:** 64 seeds únicas via HTTP localhost, cenas A/B em TEST, 64 curas aceitas, 249 Vida sintética restaurada; todas auditadas independentemente, sem conflitos ou retries falsos. Não são 64 confrontos completos.
- **R287:** 8 pares de combates com cura, backup HTTP, restauração em outro SQLite e continuação à conclusão, 16 combates sintéticos e 146 eventos HTTP somados. Mesmo estado final e mesmos detalhes de efeito por par. Reinício de servidor local em 1 par, sem alegação de recuperação distribuída.

**COLD-EXECUTION:** R19 histórico de 15.107.959 bytes / SHA256 `927e7fbee7fa25bac2bd4f84254552c9a7b2bf697c700cad10cab3170fdecfe9` / 2.223 entradas / CRC PASS; em extração *limpa* foram aplicados sequencialmente R269+R283+R284+R285. Motor R18 final SHA `cc0527522e09f0a8b732adaf962f5ca3e018441b804cd9bf5fe32bcba0becc3d`, web R19 final SHA `f3b7810e9d5b4743f49aed92b0f4963fc50f439ffe16f4e062aeff49c088de8b`. Auditores sem importação do motor para a lógica de auditoria. Resultado histórico **16/16 PASS**, novos web **8+8 PASS**, R286 **64/64 PASS** e R287 **8/8 pares PASS**. A primeira tentativa longa foi interrompida pelo timeout do operador, mas a subsequente resultou em relatório físico completo e verificável (`evidence/FINAL_COLD_EXECUTION_R284_R287.json`). Não equiparar timeout da ferramenta a erro do código.

**PACOTE DELTA:** `/Comestre/OP-VLAB-FUSION-SANDBOX-01/VLAB_R284_R287_WEB_HEAL_RECOVERY_MESTRE_ONLY.zip`, 36.120 bytes, SHA256 `9189f69e3311c078cfdcc66b0b45b0b04c59ae6dea6deb706b652c906ec365d0`. Não contém engine R19 nem outro executor, só quatro patches source-pinned, auditor, testes, relatórios e verificadores. `PORTABLE_VERIFY_BUNDLE.py` checou CRC, 17 arquivos e 16 SHA no manifesto. **Checar publicação/readback da Biblioteca antes de tratar o nome como persistido.**

## Fontes e Inbox

- Fonte física `VLAB_STAGE12_A1A2A3_WEB_R19_SANDBOX.zip` preservada em Library; relatório histórico R19 confirma controlador localhost e ausência de UAT humana. R18 e resolvedores v0.6/v0.7/v0.8.1 preservados.
- Fonte Notion exemplo de magia de cura de campanha `Sikong Eristan — Médico da Seiva` é proposta Mestre-side, com `Pulso de Estabilização` Reação 45PA / 3d10+10 / aliado até 3 m após dano. **Não foi confundida** com cura fictícia 1d6/0PA.
- Caixa `INBOX-COMESTRE-01` read-only: 17 mensagens ao COMESTRE-ID, quatro urgentes (IBX-40, 62, 70, 86), 14 exigem ACK, continuam NOVA em último sweep verificado. Recentes IBX-160 e IBX-152: GitHub opcional, operação pode prosseguir com testes locais sem gastar CI, `GH-NOT-RUN` não equivale a CI-PASS. IBX-138: cópia integral de resposta da coordenação não gera segunda ordem.
- `CM-000006` em perfil Notion: INSTANCE-ID ainda não atestada, `BLOCK-PERMIT=RED`, `GREEN=HOLD`, writer/epoch/lease/fencing UNVERIFIED. **Nenhum ACK ou atualização Notion** executados nesta retomada.

## GATE PSV / NAC-PASS

- **PASS delimitado**: fonte ZIP/hashes, patch sobre base original, 16+16 testes HTTP+nativos e baterias R286/R287 reproduzíveis, manifesto e readback posterior da Biblioteca sujeito a verificação explícita.
- **HOLD global**: 0/17 contratos terminais certificados, 0/1.875 células R91 homologadas, source P4 de Bestas/equipamento E pendente, empate de iniciativa/negativo crítico/geometry ainda normativos; nenhuma promoção ao uso de campanha.
- **Não realizado**: Notion OP/Diário/Inbox/Party/O Primeiro/fichas, operação DMG/LEVEL-UP, GitHub CI, merge remoto, UAT humana. Nenhum writer assumido; nenhum motor paralelo.

## NEXT exato

`LAST-VERIFIED R287 → FIRST-PENDING CANDIDATE R288`, após buscar colisão de artefato/Inbox. Trabalhar em capacidade funcional/source gates reais, mas **não** converter `Pulso` de 45PA de uma fonte com Reação/alcance em autotratamento Padrão 0PA. Priorizar admissão de uma ação com fonte completa e custo positivo com recibo transacional, geometria se efetivamente definida, adversários real-fonte admissíveis, ou contrato de multi-ator A1. Se o writer oficial continuar vermelho, persistir resultados **somente na Biblioteca Mestre** com readback.
