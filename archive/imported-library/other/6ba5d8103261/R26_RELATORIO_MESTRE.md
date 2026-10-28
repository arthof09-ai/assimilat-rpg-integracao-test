# VLAB R26 — Decisões expressas de iniciativa, renovação de Reação e baseline derivada

**OP-VLAB-FUSION-SANDBOX-01 · CM-000006 lógico · Mestre-side · Sandbox · não canonizado fisicamente.**

## Objetivo e autoridade

Retomada legítima da R25 sem substituir A1, o planejador v0.7, resolvedor v0.8.1, BENCHMARK_AUTO ou SQLite. Decisões expressas do Mestre (14/10/2026): desempate por DES, rerrolagem sucessiva só dos ainda empatados e reposição de uma Reação no início do próximo turno do próprio combatente. Essas decisões são autoridade do Mestre para a execução R26; **não** alegar atualização física do Sistema de Combate nem NAC-PASS normativo/produtivo. IBX-92 foi reaberta em leitura, permanece NOVA sem ACK; não foi duplicada nem editada.

## Novo caminho executável

`fusion_stage12/vlab_r26_master_rulings.py` acrescenta ao R25 um pequeno orquestrador novo. Para iniciar o turno, o desempate chama a mesma função de dados determinísticos de R18, aplica primeiro maior DES e rerrola somente grupos ainda empatados. Ordenação de terceiros já fixada não é alterada. Não há prioridade por ID/nome. Há limite de segurança operacional de 128 rerrolagens sem desempate, retornando HOLD, não sorteio substitutivo.

Na publicação de um ataque, a R26 executa `R25.native()` → reserva do planejador original v0.7 → `UnifiedSyntheticGateway`/`RebuiltManualRuntime` → efeito v0.8.1; único efeito mecânico de ataque. `A1ExternalScheduler`/`A1WindowReducer` produzem os eventos de turno e rodada sem refazer danos. `core._next_turn()` permanece intocado; o adaptador reabre o orçamento de Reação **somente** do participante cujo próprio `TURN_START` ocorre. O recibo guarda separadamente a chamada histórica (que continua reportando `reaction_auto_refresh=false`) e a alteração R26, antes=0/1, depois=1, sem acúmulo.

Crítico positivo: a identificação segue 3 dados d6 rolados sequencialmente; para o chassi 3d6 da Besta virtual, seu máximo 18 é somado à rolagem normal 3d6 e passado como dano solicitado ao v0.8.1. Essa regra não implementa crítico para todas as categorias de efeito/arma, nem resolve falha crítica. Evento negativo detectado gera censura **antes** de criar intenção durável, sem aplicar ataques. O cálculo da rolagem/atributos é extraído das regras citadas, enquanto seleção de treinamento Luta +6, tipo de dano técnico `impacto` e término experimental HP0 continuam condicionais.

## Resultados A — testes afetados

- Empate com DES diferente: prevalece maior DES sem rerrolar.
- DES iguais: rerrola os empatados; empates sucessivos continuam; empate de 3 com outra ordem já resolvida preserva não empatados.
- Três atores: B ataca A, que usa DEFENDER nativo; Reação A passa 1→0. C ataca antes de novo turno de A; nenhuma reação é reposta e segunda solicitação é rejeitada previamente. Apenas em `TURN_START(A)` ocorre 0→1. Reabertura em 1 não gera 2.
- ESQUIVAR diretamente no resolvedor v0.8.1: consome 1→0 e segunda declaração é rejeitada. CONTRA-ATACAR e OPORTUNIDADE: compartilham o orçamento por decisão do Mestre, mas **não possuem caminho completo de efeito/elegibilidade integrado pela R26**, permanecendo indisponíveis, não executados falsamente.
- Testes dirigidos R26: **38/38 verificações** (assertivas), incluindo checkpoints restaurados sem sobrescrever, rejeição de revisão antiga, integridade de A1 e dano nativo.
- Regresso: R25 **430/430 verificações**, R24 **14/14 testes**, R23 **9/9 testes**; anteriores permanecem íntegros, não foi repetida a bateria histórica de 32 confrontos do R23.

## Resultados B — oito sementes R25, comparação congelada

| Semente | R25 | R26 | Ataques nativos R26 | Rodadas R26 |
|---|---|---|---:|---:|
| 11 | completa | completa | 17 | 9 |
| 23 | completa | completa | 21 | 11 |
| 37 | completa | completa | 19 | 10 |
| 41 | censura: empate | **completa após desempate** | 14 | 7 |
| 53 | completa | completa | 14 | 7 |
| 67 | completa | completa | 14 | 7 |
| 71 | censura: crítico positivo | **completa após crítico positivo nativo** | 13 | 7 |
| 83 | censura: falha crítica | **continua censurada** | 3 | 2 |

Resumo: R25 5/8 completas, 3/8 censuradas; R26 **7/8 completas**, **1/8 censurada**, **115 ataques nativos e 343 eventos A1**. Três replays R26 independentes (sementes 41, 71, 83) retornaram a mesma revisão, hash de estado, cadeia A1, todos os efeitos e o **SHA dos bytes SQLite**. Oito SQLite, oito recibos e oito checkpoints verificados preservados em `reconstruction/r26_delivery/`.

## Resultados C — sensibilidade CA/atributos/RD

48 ataques nativos isolados e auditáveis: quatro pares de distribuições de 43 pontos cada, ambos Bronze 1, RD 5, dano 3d6, atributo FOR para acerto, 1d6 + FOR + 6 (proficiência Luta +6 alocada como escolha de laboratório). Foram enumeradas as seis faces do dado por direção; nenhuma chance de acerto foi calculada por novo resolvedor: os 48 recebimentos `hit`, mitigação, Vida e dano têm recibos v0.8.1.

- Configuração R25: 6/6 acertos nas duas direções.
- DES-foco × FOR-foco: 4/6 e 4/6.
- Assimetria extrema: 1/6 e 2/6.
- Baixo potencial de acerto: 0/6 e 1/6.

São **sondagens de ataques**, NÃO 48 lutas completas, NÃO frequência amostral independente e NÃO conclusão sobre uma Besta real. Criticidade, defesa ativa e movimentação foram isoladas fora desta matriz; análise condicionada de acerto contra CA e RD constante.

## Fontes reais e bloqueios

Galidemus (fonte `eddc2b32-4ede-829f-8a75-011e8acbf429`): Patada `1d4+DES13`, FOR5, CA explícita21, Vida32, Alma32. A norma geral de acerto usa FOR para Luta, salvo autorização de DES. Em Bronze, sem bônus adicional o máximo da Patada como ataque físico ordinário é 1d6+FOR5=11; mesmo se Luta receber a proficiência Bronze normal +6, máximo 17. Ambos ficam abaixo de CA20 da Cabra e CA21 da Galidemus. Logo o chassi básico não consegue acertar essas CA sem outras capacidades. Isso **não** prova ausência de outros ataques, vantagens, passivas ou que a Galidemus deve usar FOR em todas as ações; falta contrato da Patada integral, treinamento individual e fonte congelada.

A regra de Besta normal Bronze fornece RD geral5 e proficiência geral+6, mas a ficha da Galidemus diverge do cálculo geral de Vida/Alma/CA; valores específicos não são automaticamente errados. O R31 documenta **0 ações autorizadas integralmente** e continua sem bytes nativos legíveis para uma integração real. Não se autoproclamou gate aprovado nem ACK IBX-90. O confronto Macaco Rei Prata5 (fonte revisada historicamente e no censo DMG) pode ter maior potencial de acerto, mas suas passivas/ação/custo/contratos de despacho seguem incompletos; não foi executado como luta canônica nesta versão.

## Limitações, governança e ponto de retomada

- Falha crítica: confirmação positiva/negativa da sequência existente, porém **efeito/consequência da falha crítica não está normativamente resolvido**. Mestre precisa definir se o ataque apenas falha e consome ação ou se há consequência adicional, e qual; sem essa decisão, semente83 censurada.
- Reação: regeneração por turno próprio implementada no subconjunto R26 e testada com 3 atores **em trilha controlada**, sem alegar suporte total a lutas de três participantes.
- Reações `CONTRA-ATACAR` e ataques de oportunidade: disponibilidade orçamentária compartilha o mesmo slot; efeito completo ainda HOLD. Sem magia, transformação, PA positivo, falhas críticas resolvidas ou mecânicas de alcance indisponíveis.
- Diferenças do R25: as novas 7 conclusões continuam **RULE-DERIVED-VIRTUAL CONDICIONADAS**, não são 7 células científicas canônicas.
- VLAB terminal 0/17; DMG 1/18; STRICT 0/2; matriz oficial 0/1875; writer, lease, epoch, fencing, GREEN, NAC-PASS produção HOLD; IBX-56 BLOCKED-EXTERNAL; IBX-90/91/92 sem ACK presumido; nenhuma escrita em Party, O Primeiro, fichas oficiais, DMG-RANK, Notion ou regras canônicas.

**Primeiro alvo para retomada:** após canonização competente das duas decisões já expressas, decidir apenas a consequência da falha crítica, submeter via IBX-92 existente e testar a reexecução da semente 83; em paralelo fechar legalidade e proveniência da primeira ação real de Besta e integrar fornecedor DMG R31 somente por recibo autêntico. Não duplicar operação nem reiniciar motor.
