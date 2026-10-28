# PSV — Estado operacional do VLAB após R295 (MESTRE-ONLY)

**Operação persistente:** `OP-VLAB-FUSION-SANDBOX-01` · **Comestre lógico:** `CM-000006` · **Ambiente:** sandbox isolado TEST · **LAST-VERIFIED LOCAL:** `R295` · **FIRST-PENDING CANDIDATE:** `R296` (sujeito ao preflight de colisão com outros executores).

## Antes e novo delta funcional

**ANTES:** até R288, a cura fictícia `1d6/0 PA` estava implementada no terminal R18 e navegador R19; o fluxo de decisão R21/A1 e o adaptador conversacional R22 ainda não permitiam HEAL. A versão histórica R22 tinha 15.403.014 bytes e SHA-256 `04ddf83ba2df69059a9f00f0f46e3bee24e9adbd59094400bf3671fd72942ca6`; sua fonte original está preservada na Biblioteca.

**DEPOIS:** o patch incremental `VLAB_R289_R295_A1_CHAT_HEAL_MESTRE_ONLY.zip` permite ao Mestre escolher curar-se pelo adaptador R22 (JSON em chamadas independentes) e pelo navegador R21. O controlador R21 registra uma decisão `HEAL` e um `TURN_END` por turno, com efeito único do **resolvedor original v0.6**; R18 v0.8.1 continua dono do ataque e reação; R21 A1 continua dono do turno. Nenhum novo motor paralelo, nenhuma mudança de regra física.

### Unidades entregues

- **R289:** confronto R288 versus R21/R22; ponte de cura fictícia, pré-validação sob transação e ação `HEAL` no protocolo de comandos. A origem interna permanece marcada `LAB-V06-MAGIC-HEAL-1D6`, **sem custo real**.
- **R290:** interface web R21 recebe botão de cura fictícia, com validação estrita do formulário e apresentação da rolagem/HP no histórico. Os demais comandos funcionais herdados permanecem intactos.
- **R291:** o auditor de cura independente passa a executar obrigatoriamente antes de exibir estados/recibos R21. Resumo de cura adulterado (mesmo com hashes recalculados) resulta em HOLD.
- **R292:** fechamento adicional de continuidade entre Vida após ataque, Vida antes/depois da cura e Vida no estado final. Reproduziu antes a falha na qual `hp_before`/`hp_after` eram aumentados juntos com receipt coerente; o auditor anterior aprovava; o novo **rejeita**.
- **R293:** 4 cenas TEST multirrodada com 4 sementes, **36 decisões**, **24 ataques**, **8 curas**, **8 defesas**, **104 eventos A1**; 4/4 source-audit PASS. Uma tentativa anterior de 16 sementes × 15 decisões **não concluiu no limite de execução** e não entra nesses denominadores.
- **R294:** entrada de comandos JSON em subprocessos rejeita chaves duplicadas inclusive em objetos aninhados, NaN/Infinity e requisição acima de 64 KiB. 6/6 testes novos PASS.
- **R295:** prova real do fluxo Chat JSON, cada chamada em **processo separado**: criar → iniciativa → atacar → curar-se → exportar checkpoint → restaurar em outra base → novo ataque → repetir intenção antiga sem reaplicar efeito. Tentativa de disfarçar `Pulso` com custo 45 PA foi rejeitada sem gravar evento. Recibos auditados 2/2 PASS.

## Evidências executadas (não inflar denominadores)

| Evidência | Medida | Estado |
|---|---:|---|
| Testes novos R289–R292 | 12/12 | PASS em TEST |
| Regressões históricas R18–R22 com auditor pós-R292 | 47/47 | PASS em TEST |
| Testes novos R294, execução subprocesso | 6/6 | PASS em TEST |
| Cenas multirrodada R293 | 4/4, 36 decisões | PASS delimitado |
| Chat cross-process R295 | 1 fluxo de 3 commits + checkpoint e restauração | PASS delimitado |
| Instalação a frio R22 original + oito arquivos overlay + 18 testes novos + R293 + R295 | SHA/CRC + execução | PASS delimitado |
| Regressão a frio `--deep` | Execução adicional opcional | **verificar relatório antes de declarara conclusão** |
| Certificação terminal | 0/17 | HOLD |
| Células oficiais R91 | 0/1.875 | HOLD |

As 4 cenas R293 não são novas células R91; o R295 é roteiro demonstrativo, não combate oficial; os 18 testes novos e os 47 herdados não são 65 contratos científicos.

## Integridade e disponibilidade

O ZIP novo contém **somente overlay e verificadores**, não uma segunda distribuição integral do motor. Fonte congelada R22 SHA-256 `04ddf83ba2df69059a9f00f0f46e3bee24e9adbd59094400bf3671fd72942ca6`; todos os arquivos sobrepostos são verificados contra hashes da fonte e contra hashes finais. `COLD_REPLAY_R289_R295.py --source ...` extrai temporariamente a fonte original, aplica o overlay somente à cópia e comprova execução funcional. `VERIFY_BUNDLE_R289_R295.py` verifica todos os arquivos internos. CRC/manifest e SHA do arquivo publicado devem ser lidos de volta da Biblioteca antes de rotular a entrega como totalmente persistida.

**NÃO DEMONSTRADO:** implementação de Pulso de Estabilização ou Cura espiritual como habilidade real; custo positivo de PA, ação Reação em aliado a 3 m, morte/KO canônicos, geometria, 3+ atores, vínculo de item real P4, magia real, hospedagem Android ou UAT humana. Não declarar que o hardening R265–R288 do núcleo R18 foi migrado integralmente para R22: esta atualização cobre apenas a ação HEAL, preflight e guardas descritos.

## Inbox, autoridade e segurança

No último sweep canônico da INBOX-COMESTRE-01, **17 envelopes** dirigidos ao CM-000006 permanecem `NOVA`; **14 exigem ACK**. IBX-160/152 permitem continuidade local sem GitHub; IBX-138 orienta deduplicar encaminhamentos; IBX-40/62/70/86 permanecem urgentes sem ACK legitimado. `CM-000006-I0001` não foi consumida formalmente; o perfil indica `BLOCK-PERMIT=RED`, `GREEN=HOLD` e writer/lease/epoch/fencing sem prova. Nenhuma alteração em Notion OP/Diário/Inbox, Party, O Primeiro, fichas reais, DMG-RANK, LEVEL-UP ou catálogo; nenhum ACK presumido; GitHub Actions não executado.

## Próxima execução sem reinício

**NEXT:** checar colisão pós-R295; verificar readback Library; avaliar R296 como otimização comprovável da repetição de controles A1/replay para cenas longas **sem cache não autenticado e sem segundo motor**, preservando os 17 contratos e 1.875 células em HOLD. Alternativamente priorizar um alvo fonte-admissível P4 ou testes source-gated de PA positivo quando normas forem suficientes. Não reiniciar R01–R295, não repetir seeds sem hipótese nem elevar aceites por analogia. Correções canônicas dependem dos gates de writer e NAC-PASS competentes.
