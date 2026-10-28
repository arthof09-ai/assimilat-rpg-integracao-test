# PSV PARCIAL — LEVEL-UP-ENGINE / IBX-17 / R197–R206

**AS-OF:** 2026-10-19, America/Recife. **OPERATION:** `LEVEL-UP-ENGINE / IBX-17`. **BASELINE:** R01–R196 preservada. **AUTHOR:** `CM-000001-I0010` documental; **coordenação:** `CM-000001-I0009`. **PRIORITY:** P0 MVP-LAB FINISH-FIRST. **PRODUÇÃO:** HOLD. **REVIEW:** SELF_REVIEW_ONLY.

## Estado físico recuperado

- **R187–R196 ZIP recuperado da Biblioteca:** 639.079 bytes, SHA256 `8635489c94066f591372a9f81fb83b81b8337f0634b93adc3a90b462b0823f84`, 69 entradas, CRC íntegro. 68/68 entradas do manifesto autenticadas conforme auditoria independente comunicada pelo Coordenador; nesta recuperação foram certificados SHA total e CRC do ZIP, sem repetir os 29 testes históricos.
- **R190** `3fec2b324ede81d1bed5d6d0a7d60681`, última edição `2026-10-19T16:53:02.716Z`, reaberto LIVE. TX `IBX17-R190-MVP-VERTICAL-20261019-01`, nível19, INT13, HPmax307, PAmax360, journal com o mesmo TX, alternante PRE nível17 no fim; 8 observações de leitura verificadas; **zero mutações**.
- **R144** `3fcc2b324ede81868256e6db67ece28e`, `2026-10-17T12:04:36.271Z`, reaberto LIVE: nível17, INT8, HPmax309, PAmax273, FF290, título+2SAB, equipamento sintético+3DES, estrutura coluna/tabela/alternante/filho 1/1.
- **R201** nova cópia justificada do layout R144 sob o laboratório preexistente: `3fec2b324ede8179a8d4f94886ff7510`; título atualizado `IBX17-R201 — Ficha Complexa para Level-Up Conversacional / TEST`. Reaberta após ANTES documental na página, última versão conhecida `2026-10-19T19:47:50.723Z` (UTC). Inventário raiz: 1 colunas, 1 tabela com 3 linhas de dados, 1 alternante, 1 filho nativo novo ID `9f0c2b324ede8353baac813e05669b90`, 0 menções a outras páginas, 0 mídias representadas. Filho reaberto com **zero descendentes** e sentinela preservada. Mídia binária ausente na fonte; nenhum hash de mídia alegado. Dados mecânicos ainda **BEFORE**: nível17, FOR6, DES10 natural +3 equipamento, CON10, INT8, SAB7 natural +2 título, CAR4, Vida240/309, PA150/273, comprometidos30, FF290, CA23.
- Os recibos R144 copiados na réplica são **legado documental** do original, NÃO eventos R201 consumidos. A subpágina copiada ainda referencia o ID de origem no próprio conteúdo histórico; esse referencial arquival não se torna ID do novo pai. Foi preservado.

## R197–R206 — Capacidade anterior, intervenção, evidência, veredito

| Etapa | Implementação/intervenção | Evidência | Estado |
|---|---|---|---|
| R197 | Recuperação de ZIP e R190; sem replay | SHA baseline/CRC, fetch R190, 8 checks de histórico e journal | PASS READONLY |
| R198 | `r198_dynamic_source.py`: parse source-observed `KEYED_R190` ou `COLUMN_TABLE_R144`, distingue valores naturais e camadas, sem `initial_test_state()` fixo | Dois readbacks diretos no Notion: níveis19/17, INT13/8, HP307/309, PA360/273, pais LAB e versões distintos; teste adversarial ID/parent/campo duplicado | PASS LOCAL + LIVE HOST ORCHESTRATION; não host assinado |
| R199 | `r199_r200_live_mobile.py`: revalidar source fingerprint/target/version contra novo snapshot, proibir certificação por booleanos de caller, `verify_native_effect()` baseado em texto físico e journal | teste de `trusted=True`/hash antigo/target divergente rejeitados, R190 lido fisicamente sem mutação | PASS LOCAL; commit native novo não executado |
| R200 | `MobileSession` recebe fonte derivada do readback, solicita duas alocações, calcula granularmente e permite revisar/cancelar | testes revisões +2INT/+2SAB versus ordem inversa: paMax307 vs305, HPmax343 em ambos | PASS CONTROLADOR LOCAL; **ESCOLHAS HUMANAS PENDENTES** |
| R201 | Cópia estrutural LAB independente do R190 preparada com ANTES e inventário | leitura pai LAB, raiz e filho, campos originais intactos, 6 seletores únicos | PASS FÍSICO PREPARAÇÃO |
| R202 | `r202_structural_writeset.py` produz e valida edit set único para colunas e tabela; não reescreve filhos/histórico | ensaio seco com escolha ilustrativa não autorizada, 6 edits, 1 filho e 1 alternante preservados | PASS LOCAL WRITESET; **COMMIT PENDENTE ESCOLHAS+PRÉVIA+CONFIRMAÇÃO** |
| R203 | Verificador independente do journal R190 reaberto e verificador geral sem flags | R190 journal, TX, snapshot PRE e 8 checks reabertos | PARCIAL; R202 não consumado |
| R204 | `r204_r205_extended_previews.py` rank Bronze5→Prata1 rebase 42→54, 86→142; sem reaplicar R129 | caso histórico como teste matemático com fonte competente, sem native write | PASS LOCAL; novo rank nativo HOLD |
| R205 | Fonte `NORMAL-STATS-VZ-08` para Kael L1→L2 (espírito TEST): TAP10,5 e distribuível220→231, carry1/2→0; sem forma ativa | fonte Notion `3f2c2b324ede8168b50ee4254134d821` @2026-10-07T21:52:35.997Z, matemática reconciliada | PASS SOURCE-BOUND SANDBOX READONLY; evolução nativa não executada |
| R206 | Pacote delta e PSV PARCIAL, guardando ponto exato | teste de reconstrução local/manifesto CRC, checksum; auditor externo não realizado | PARCIAL / CORE-LAB HOLD |

## Escolhas humanas e isolamento

**PONTO ATUAL DO FLUXO:** R201 está PREPARADA e aguardando o Mestre informar, PARA O PERSONAGEM TEST, **uma distribuição de 2 pontos no nível18 e outra de 2 pontos no nível19**, e escolher `60% FIXO` ou rolagens com prova. Não há escolhas ainda, portanto **NÃO EXISTE PRÉVIA FINAL CONGELADA NEM HASH DE AUTORIZAÇÃO**. Texto hipotético `18:+2INT;19:+2SAB` aparece apenas como caso local dirigido, jamais como escolha do Mestre. Em seguida: PREVIEW → revisão/cancelamento → aprovação real vinculada ao hash → novo preflight Notion → intenção, escrita mínima → readback → journal → alternante histórico final. A consulta ao host não oferece CAS universal nem assinatura de player.

**LAST-VERIFIED-UNIT:** R201 prepared, filial nativo reaberto. **FIRST-PENDING:** R200 alocações reais de dois níveis. **TX R202:** NÃO DESPACHADA. **UNKNOWN-EFFECT novo:** nenhum; todos os writes desta rodada foram criação/rotulagem/preparação documental da réplica; campos mecânicos BEFORE. **NO-REPEAT:** R190 e R144 originais intactos; R145 não tratado como confirmação, R155/R158/R129/R130/R110/R121 proibidos de replay; Party/O Primeiro 0 writes.

**AUTHORITY/WRITER STATE:** `DIR-MESTRE-LABS-REPLICAS-20261016-001` apenas TEST, `CM-000001-I0010` documental, sem writer/lease/epoch de produção. **NAC-PASS:** LAB gate ainda HOLD até escolha real + preview + execução nativa complexa + readback e auditoria proporcional. **MVP-CORE-LAB:** HOLD; **MVP-EXTENDED-LAB:** HOLD; **PRODUÇÃO PARTY:** HOLD.

**NEXT-5:** 1) receber escolhas e modo de crescimento do Mestre; 2) reabrir R201 e apresentar prévia com fonte/versão/hash; 3) receber confirmação real da prévia, não da ordem geral; 4) aplicar TX nova minimal com PRE e alternante histórico, somente se conector permitir, readback+diário/journal; 5) auditoria de estrutura e idempotência, extensão rank/spirito controlada e auditor externo.

**TARGET REMAINDER:** MVP conversacional real completo em segunda ficha LAB estruturada; extensão rank/spirit. **EXACT RESUME:** R201 `3fec2b324ede8179a8d4f94886ff7510` nível17, sem TX nova, fonte física `2026-10-19T19:47:50.723Z` sujeita a reabertura, opções nível18 e19 pendentes; root 1 child `9f0c2b324ede8353baac813e05669b90`; R190 consumido e sem writes.
