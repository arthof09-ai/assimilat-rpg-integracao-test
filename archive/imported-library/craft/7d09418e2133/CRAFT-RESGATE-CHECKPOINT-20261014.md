# PSV — Recuperação CRAFT v03 / 14-10-2026

**Operação:** CM-000002 / WS0001; retomada Mestre-side do sandbox, sem assumir INSTANCE-ID, writer, lease, epoch ou fencing.

## Prova técnica independente, 14/10/2026
- Pacote `CRAFT-COMESTRE-CHAT-v03.zip`: SHA-256 `5a9af3ae0568031a59a0248843a3f40b8c020c070b8f00c20eb678d9ec844434`; ZIP CRC PASS; manifesto 205/205 SHA-256 e tamanhos PASS; verificador incluído `verificar_v03.py` PASS; 197 arquivos de Oficina v02 preservados, motor R48 174/174 byte-identical conforme verificador.
- Backup `CRAFT-CHAT-SESSAO-MESTRE-v03.zip`: SHA-256 `02a3643c75cd49d13cbfdffdedaa42fcc1442f877042b4d398a540610aaed57f`; ZIP CRC PASS; manifesto 7/7 SHA-256 PASS.
- `craft_chat.py restore` reabriu backup em diretório de sandbox separado e retornou auditoria `ok=true`.
- Comandos reexecutados sobre a restauração: `status`, `history`, `preview` (nenhum `prepare`, `confirm`, `cancel`, `replay` ou `rollback` executado).

## Estado restaurado
- `session_id=sim-75192d55b85e`
- `batch_id=SBX-R48-BATCH-UI-2afb696406a6e839`
- `intent_id=CHAT-MESTRE-20261014-3T-2M-01`
- `r48_head=31e7963ce846705a5c8545087dc270dbd80a5a67adae39d06d857d80ab91774a`
- `disk_sequence=0`, `batch_count=0`, `orders_count=0`; ledger sem produção e sem consumo.
- Plano `DRAFT`, `can_confirm=true`; QA simulado de cinco tentativas 5/5 PASS; projeção 3 tábuas B30-01 e dois pares de espaçadores B30-03 (7 peças).
- Estoque sintético ANTES: Ardósia boa 8, Mica A 8, Mica B 8; trincada 1, pequena 1.
- Estoque PROJETADO (NÃO COMMIT): Ardósia boa 5, Mica A 6, Mica B 6; trincada 1, pequena 1.
- `official_stock_effect=0`. MED e ensaio/estoque reais indeterminados.

## Restrições e fronteira
- v03 compreendida e verificada; operador original reutilizado; UAT humana de confirmação ainda PENDENTE.
- Gaps F5 0/26 resolvidos; RC5 0/30 homologadas; F5 RED; C19-021 UNKNOWN-SIDE-EFFECT; NAC-PASS material HOLD. Não ocorreu escrita Notion, fichas, Party, O Primeiro, estoque real ou produto canônico nesta retomada.
- Próximo passo depende de ordem humana expressa de confirmar ou cancelar **o plano original**, após informar prévia. Confirmar somente uma vez e fazer readback/histórico/recibos e novo backup com versão preservada; cancelar somente sob ordem. Se não houver decisão, manter plano e backup intactos.
- Esta cópia restaurada constitui prova do backup recuperado, não prova que nenhuma outra sessão privada tenha sido criada depois da exportação.
- Nenhuma nova operação/Inbox/INSTANCE-ID nem alegação de posse de writer foi criada.
