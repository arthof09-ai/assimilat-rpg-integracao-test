# VLAB — Estado operacional após R298 (MESTRE-ONLY)

**Único escopo:** `OP-VLAB-FUSION-SANDBOX-01`, **COMESTRE-ID lógico:** `CM-000006`, **autoridade material:** instância e writer/epoch/lease/fencing/GREEN não comprovados. **Denominadores oficiais:** 0/17 contratos terminais, 0/1.875 células R91, 0 Party/O Primeiro writes.

## Contínuo nesta execução — fatos físicos (TEST)

- **R289–R295:** fusão da cura fictícia 1d6/0PA ao controlador R21/A1 e ao chat R22, 1 decisão = 1 commit, R21 A1 controla turno, resolvedor de cura original v0.6, ataque/defesa v0.8.1. Auditor R291/R292 detecta recibos falsificados e HP descontinuado; JSON estrito; subprocesso CHAT checkpoint/restauração. 4 combates fictícios em TEST, 36 decisões/24 ataques/8 curas/8 defesas. Instalação R22 original + patch: 65/65 testes PASS, pacote original imutável publicado na Biblioteca.
- **R296:** vulnerabilidade comprovada em snapshot anterior ao primeiro evento; adulterações de PA, Reação, rodada e vencedor sem journal eram aceitas (HP já era bloqueado). Aplicou guarda de recursos completos, roster e cabeçalho apenas em revisão 0 da cópia R20. 8/8 testes novos PASS; 73/73 testes amplos (47 históricos +26 novos) PASS após patch. Cold install profundo 73/73 PASS via original R22+R295+R296. Novo ZIP com overlay, evidências, manifest SHA e instalador frio publicado, baixado de volta e comparado bytes/CRC. Nada de canonical promotion.
- **R297, diagnóstico SEM correção:** 3 sementes independentes 297350–297352, **23 decisões por execução (1 START+22 PASS)**, 69 decisões / 66 PASS; benchmarks não são combates. Média da primeira PASS 0,0811s; da vigésima segunda 2,1455s (**~26,4x**). `checked_load` 0,0130s na primeira PASS → 0,2965s na vigésima segunda. Cronometria 1 host, Python local e disco, não extrapolar para 20x20; arquivo executável portátil e três relatórios com seed já no pacote R297.
- **R298, cProfile SEM correção:** uma semente 298354, 1 START +14 PASS com perfil Python: 19,587s instrumentados, 27.977.993 calls / 25.156.519 primitives; `_fresh` R21: 129 calls, 18,773s *cumulativos* (filhos inclusos); scheduler `step`: 2.864, checkpoints de redutor: 17.184, verify_pins: 23.173, chamadas `pathlib.open`: 162.211. Demonstra recomputação A1/fonte em cascata como hipótese concreta, não prova assintótica nem autoriza remover validação de origem.

## Fontes, evidências e checkpoints na Biblioteca Mestre

- Fonte original R22: SHA256 `04ddf83ba2df69059a9f00f0f46e3bee24e9adbd59094400bf3671fd72942ca6`.
- Overlay R289–R295: SHA256 `7c9ac7b1930bf673d745e65140e5a2fd3e5b6ce422e03558a6eb31f4c79d42ec`.
- R296 módulo `vlab_r20_configured.py` protegido SHA256 `00e41827fe3fd5b921e479b51594bc3db620484268b60eac96e4b0009b552311`; ZIP R296 publicado SHA256 `ecc473187158acea3e815ed5f06ee2d3b32db5743b5bb04e07e66ed856637e9d`.
- R297: `VLAB_R297_A1_REPLAY_PERFORMANCE_DIAGNOSTIC_MESTRE_ONLY.zip`, bundle SHA256 `94228e4a5504380ad3e3777ae642693658050c81f97cd61ed28a3e02a417c1ef`.
- R298: `VLAB_R298_REPLAY_CPROFILE_SOURCE_DIAGNOSTIC_MESTRE_ONLY.zip`, bundle SHA256 `73eac20e88df3023fc73db9756d74e59d46a5c2304e9c786766d046e7877dcd4`.
- Os dois benchmarks só produzem dados locais; sua simples execução não altera sistema ou fontes. No R297 são três execuções; no R298 uma; não se deve somar contadores de perfis como lutas nem usar tempos sob profiler como latência de jogo.

## Restrições e pendências

- **Inbox consultada no início da execução:** 17 envelopes para CM-000006, 14 exigem ACK, todos `NOVA`; IBX-40/62/70/86 urgentes. Nenhuma mensagem conferiu writer. Não foram feitas alterações em Notion OP, Diário, Inbox ou perfil. Carta GitHub autoriza uso opcional, CI NÃO RODADO.
- Sem source P4 elegível de criatura/equipamento E, nenhuma nova célula homologada; falta regra de empate de iniciativa, crítico negativo, HP0 oficial, reação PA positivo e bloco↔metro. Cura aqui é ficção de laboratório, não Pulso do NPC nem regra de campanha.
- **R299 primeiro candidato** após preflight de colisão: profiling por função/escopo e, se justificado, cache estritamente de requisição de verificações de fonte/pins imutáveis ou redução de replay A1, comprovando invalidação e os 73 testes herdados, resistência a arquivos adulterados, no-double-commit, crash e igualdade byte a byte dos eventos. Não trocar segurança por performance ou construir outro motor.

**LAST-VERIFIED LOCAL R298; NEXT-PENDING CANDIDATE R299.** O presente markdown é checkpoint Mestre-only; não foi publicado no Diário/Notion por ausência de autorização de writer. `NAC-PASS` somente proporcional ao ZIP/TEST; terminal/global HOLD.
