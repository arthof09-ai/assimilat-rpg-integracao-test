# PSV — Handoff de sessão CRAFT conversacional (sandbox)

**CM-000002-I0016 / WS0001 — continuidade funcional após Oficina v02.**

## Estado físico realmente verificado

- **Motor e ferramenta:** `CRAFT-COMESTRE-CHAT-v03.zip`, SHA-256 `5a9af3ae0568031a59a0248843a3f40b8c020c070b8f00c20eb678d9ec844434`; arquivo persistido na Biblioteca, `libfile_49178762599c8191afecc9512458e022`.
- **Oficina v02 original:** ZIP SHA-256 `8dfc15b054d3416aa10717bf3d4e3039a291fd813aca42e1bf1c42bc284d1eaa`. 197 membros preservados byte a byte no v03; motor R48 inalterado 174/174. v01/R52 históricos conservados dentro do original v02.
- **Backup ativo:** `CRAFT-CHAT-SESSAO-MESTRE-v03.zip` SHA-256 `02a3643c75cd49d13cbfdffdedaa42fcc1442f877042b4d398a540610aaed57f`, Biblioteca `libfile_306f1425f96481918f9a4a259f2f60df`.
- **Session ID:** `sim-75192d55b85e`.
- **PREVIEW ID:** `SBX-R48-BATCH-UI-2afb696406a6e839`.
- **Intent ID:** `CHAT-MESTRE-20261014-3T-2M-01`.
- **HEAD esperado:** `31e7963ce846705a5c8545087dc270dbd80a5a67adae39d06d857d80ab91774a`.
- **Não confirmado:** `disk_sequence=0`, ledger `batches=0`, `can_confirm=true`, 0 recursos consumidos nessa sessão.
- **Escolhas da prévia:** `B30-01=3`, `B30-03=2`, seleção dos lotes aptos originais sintéticos, QA por tentativa apenas fixtures padrão de TESTE. Nenhuma escolha humana real ainda; o Mestre deverá confirmar ou mudar os valores.
- **Estoque de TESTE:** Ardósia apta 8; Mica A 8; Mica B 8; mais 1 ardósia trincada e 1 pequena na fixture não selecionada.
- **Projeção R48:** 5 tentativas/7 peças, 5 QA `EXPERIMENTAL_QA_PASS`, consumo de 3 lâminas +2 folhas A +2 folhas B, saldos 5/6/6.
- **Fontes PS:** Ardósia `3f3c2b32-4ede-81ac-af28-c66a6b46e0b2`, Mica `3f3c2b32-4ede-81e1-b179-e194e2838c84`. Fontes são PS, não stock canônico.

## Próximo passo exato para o Comestre após mensagem do Mestre

1. Se o Mestre disser **“Confirmo fabricar o lote experimental...”**, recuperar o backup da Biblioteca se `/mnt/data/CRAFT-CHAT-SESSOES` não existir. **Não criar sessão substituta pelo mesmo nome**; verifique SHA-256 da cópia recebida.
2. Reexecutar `python craft_chat.py --data <pasta de sessão> status` e `preview --batch SBX-R48-BATCH-UI-2afb696406a6e839`, conferir ID, `HEAD`, estoque e elegibilidade.
3. Após confirmação humana inequívoca do Mestre, executar **uma vez**: `python craft_chat.py --data <pasta de sessão> confirm --batch SBX-R48-BATCH-UI-2afb696406a6e839 --ack CONFIRMO-SANDBOX`. Esse `ack` é argumento técnico; a autorização vem **da mensagem humana do Mestre**.
4. Reabrir `status`, `history` e recibo (o comando `confirm` também faz readback). Se erro/efeito desconhecido, não inventar sucesso e não repetir sem reconciliação.
5. Exportar novo backup, fazer upload **com controle de versão** para substituir ou versionar o arquivo de sessão na Biblioteca, sem apagar versão anterior até readback. Comunicar IDs de pedido/produto e saldos sintéticos em português.
6. Se o Mestre disser **“Cancelo”**, executar `cancel --batch ...` e exportar backup novo; não executar `confirm`.

**NÃO FAZER:** presumir processo vivo, fabricar fisicamente, promover QA de TESTE, consumir estoque oficial, atribuir REC-ID, mexer em Notion/Party/O Primeiro. Antes/depois oficial continua gaps 0/26, RC5 0/30, F5 RED, C19-021 UNKNOWN-SIDE-EFFECT, NAC-PASS material HOLD.

**Demonstração separada** (`CRAFT-CHAT-CLEAN-DEMO.json`) executou testes A–H com escolhas AUTOMATIZADAS; não foi a sessão acima e não é UAT humana.
