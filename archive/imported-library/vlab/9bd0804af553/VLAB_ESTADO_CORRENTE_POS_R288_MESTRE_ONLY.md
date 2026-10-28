# PSV — Estado recuperável do VLAB após R288 (MESTRE-ONLY)

**Operação:** OP-VLAB-FUSION-SANDBOX-01 • COMESTRE-ID lógico CM-000006 • TEST • **LAST VERIFIED: R288** • **FIRST PENDING CANDIDATE: R289**. Não declarar identidade de instância, writer, lease, epoch ou GREEN.

## ANTES / DEPOIS

**Antes:** R273 verificado; R274–R283 implementaram cura fictícia por CLI; R284–R287 disponibilizaram-na na interface web R19 com auditoria de origem, backup/restauração e 64 seeds + 8 pares HTTP. ZIP da série publicado na Biblioteca Mestre e confirmado byte a byte. Nenhuma magia oficial implementada.

**Depois (R288):** detectado e fechado vetor semântico no formulário web `/act`: metadados de `spell_id`, `pa_cost`, `ability` e campos duplicados eram ignorados, permitindo interpretar erroneamente intenção de habilidade/magia real como cura LAB `1d6/0PA`; HEAL também ignorava alvo e reação. Patch isolado de 1.678 caracteres recusa esses parâmetros antes de qualquer journal e mantém curas/ataques válidos. Módulo R18 anterior SHA `cc0527522e09f0a8b732adaf962f5ca3e018441b804cd9bf5fe32bcba0becc3d` preservado; R19 atualizado SHA `97ba521ba29b29fc85e3f022effb4520a143d13bd3d473a43f4c7db63ac020a1`.

**PROVA:** instalação fria com fonte R19 `927e7fbee7fa25bac2bd4f84254552c9a7b2bf697c700cad10cab3170fdecfe9`, delta R284–R287 `9189f69e3311c078cfdcc66b0b45b0b04c59ae6dea6deb706b652c906ec365d0`, patch R288 SHA `1077225631332b37b6d783cdd4693acf6c4c68b4a8803358c08521bfaf51dee0`. 16 testes históricos + 8 R284 + 8 R285 + 8 R288 = **40/40 PASS**. Sobre a mesma árvore executável SHA-pin: R286 **64/64** curas HTTP e R287 **8/8** pares de backup/restart, 16 bancos e 146 eventos PASS. O teste cold `--deep` em comando único não concluiu perante timeout de ferramenta; estas duas últimas evidências foram executadas separadamente, não declaradas cold deep PASS.

**Artefato:** `VLAB_R288_FORM_SOURCE_GUARD_MESTRE_ONLY.zip`, 11.775 bytes, SHA `213c3e4aae8bf1a12f0548f056739f01a34d0ee58bc20b62285af02bb15810a5`, com patch novo, 8 testes, prova cold 40, métricas independentes 64+8, verificadores e README. `VERIFY_R288_BUNDLE.py` aprovou CRC e SHA dos 9 arquivos, sem binário motor. Destino Biblioteca Mestre existente `/Comestre/OP-VLAB-FUSION-SANDBOX-01/`; sincronização/recuperação de bytes deverão ser verificadas antes de declarar upload concluído.

## Fonte e comunicação

A cura do NPC proposto Sikong Eristan (`Pulso de Estabilização`) exige Reação, 45PA, 3d10+10 Vida e aliado a até 3m após dano; nada disso é intercambiável com o TEST 1d6/0PA. `M Cura espiritual` no espelho tem 1d4+INT/6 mana com ação e equivalência PA ainda sem prova. Nenhuma conversão foi feita. Na Inbox, 17 mensagens a CM-000006 e 14 exigindo ACK permaneciam NOVA no último sweep verificado; IBX-160 e IBX-152 deixam GitHub opcional. CM-000006 no Notion `BLOCK-PERMIT=RED`, GREEN HOLD. Zero Notion writes; zero ACK inventado.

## Gate e próxima execução

**PASS delimitado somente ao sandbox e integridade dos arquivos.** `NAC-PASS` terminal/global HOLD; **0/17 contratos terminais**, **0/1.875 células R91**; nenhuma certificação de campanha ou publicação à Party. UAT humana e host Android/externo não demonstrados; browser funciona só em 127.0.0.1 do computador com Python.

**NEXT:** checar colisão em Library e novas decisões de Inbox antes de numerar R289. Priorizar capacidade de PA positivo e magia real somente com fonte admissível e solver com reação/alvo/alcance; ou ligar multi-ator A1 ao mesmo núcleo, com fonte de iniciativa e disputa resolvida; deixar normativas negativas/crítico, P4, E e geometry HOLD se sem fonte. Manter motores originais, histórico, denominadores e Diário/NAC. Writer/instance Notion só após gate material; não usar OP/Inbox/Party como destino experimental.
