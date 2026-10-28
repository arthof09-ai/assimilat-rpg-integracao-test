# PSV CRAFT — LONGRUN R3 — 21/10/2026

**SUPERFÍCIE:** RPG DO MESTRE / MESTRE-SIDE. OP-ARQ-RIN-REC-01. Responsável lógico: CM-000002 / WS0001, instância atual NÃO autenticada e NÃO inferida. Origem canônica: LAB CRAFT (`3fbc2b324ede811db848d35d4739eb00`), OP CRAFT (`3f1c2b324ede81d7aa79c83106240516`), IBX-116 (`3ffc2b324ede817aa3abea3cb7ba8c08`).

## Execução R3 — fontes / delta / aceites

| Bloco | O que se demonstrou | Passes digitais | Pacote de Biblioteca Mestre | SHA256 |
|---|---|---:|---|---|
| REFLINK29 | 29 receitas-filhas; 2 menções Notion; 1 alvo válido, 1 alvo `NOT_FOUND`; quantidade `Ex` permanece pendente | 43/43 | `libfile_b912bdd8d3588191bb255afab27de25c` — `CRAFT_REC_REF_LINKS29_20261021.zip` | `b337c80d5868cca8cb298f8dbe7a3ee15c6d2658629fa3801b36641d1147a6d9` |
| P2/OIL SOURCE MAP | 12 posições de BOM (6 P2 + 2 alternativas OU + 4 óleo), 0 lotes; forma peça/pó/recipiente e Mestre/Espelho separadas | 16/16 | `libfile_9726ac58915c8191b16d76dd4384c41f` — `CRAFT_P2_OIL_SOURCE_MAP_20261021.zip` | `ec5abfd6840b80c4dfeac1fc372e71713d45d04a5c304bdca2d9850aea3750bf` |
| DECISION DOCKET34 | 21 receitas-filhas com divergência distribuídas por UUID em um único despacho decisório, sete dependências transversais e veto de commit | 13/13 | `libfile_f03a2f7d74708191b21fb51960bfd79b` — `CRAFT_DECISION_DOCKET_34_20261021.zip` | `895c712ad46311e43884ea5eb95b9802b32b053090b90d169b50c10838e347f2` |

**Denominadores desta rodada:** 3 blocos novos, **72/72 testes digitais** distintos (43+16+13); 34 padrões Mestre (9 ENC, 17 BAT, 8 MAT); 29 subpáginas de receitas, 5 receitas embutidas, 1 padrão sem receita explícita; 28/29 subpáginas dependem explicitamente de Óleo de Vedação e 1 permanece com `1x :`. Todas as três entregas ZIP passaram na verificação CRC/manifesto, execução/replay frio e comparação byte-idêntica com cópias materializadas da Biblioteca Mestre. Os 221 testes R2 e os anteriores **não** são recontados como novos.

## Evidência técnica recuperada

1. Menção ao Pó de Diamante Noturno `3edc2b324ede816aaa04d698822055c2` abre em Mestre Itens/Minérios. Menção não rotulada em Matriz Cultivo `/p/707d83314e7c40cd89bc70fb240e6076` retorna `NOT_FOUND`; texto vizinho sobre óleo não autentica esse target. Matriz Proteção mantém quantidade literal `Ex`, assim como sua versão histórica de leitura.
2. BOM Mestre P2: 3 Argila Terra, 1 Água Benta, 2 Sal Geodo Santo, 3 Pó Ferro Meteoro, 1 Essência Barreira, 1 Óleo, 2 Pedra da Luz OU 2 Pote de Essência Mágica. Processo diz Sal Geodo Encantado e não registra energização. **P2-SALT-01** e **P2-ENERGY-02** continuam sem decisão autoritativa; não foram recriados.
3. Óleo Mestre: 1 Mandrágora +8 Orvalho do Amanhecer +3 Pó de Ferro Celestial +1 Essência Lua Minguante. Histórico 2 ferro, mas não prevalece. Mestre Ferro Celestial é **peça**, não pó homologado; Pó Meteoro não prova Pó Ferro Meteoro; Essência Mágica genérica não prova unidade `Pote`. Etapa de óleo cita Orvalho Dragão / Essência Vórtice, sem conciliação. Zero lotes físicos verificados na busca dirigida.
4. As pesquisas por Água Benta de Santuário, Essência de Barreira Mística e Pedra da Luz retornaram fichas homônimas sob **Mestre Espelho da Party** e não ficha separada exata Mestre no escopo dirigido. **Não** se pode afirmar ausência global nem transpor fonte de Espelho para regra Mestre.
5. 21 receitas com divergência são lista operacional do mesmo envelope IBX-116, **não 21 novos tickets**. As oito receitas com cobertura lexical não têm efeito físico/magia homologados.

## Persistência

- LAB CRAFT: três checkpoints R3 inseridos com artefatos/hash, readback final do REFLINK29 confirmado.
- OP CRAFT: comentário `CRAFT-LONGRUN-R3-20261021`, ID `400c2b324ede819f91b5001db67ee5a9` na discussão já existente, criado e relido, sem mutação do corpo gigante da página.
- IBX-116: devolutiva consolidada `CRAFT-LONGRUN-R3-20261021-001` inserida e relida; `Estado=NOVA`, `Exige ACK=SIM` preservados. Nenhuma identidade de instância/autorização foi forjada.
- Biblioteca Mestre `/Comestre/`: três ZIPs acima; nenhum objeto do jogo alterado.

## Gate proporcional e próximo passo

**PASS** apenas análise documental, testes TEST, integridade e recuperação. **HOLD** estoque, QA material, forma física/porções, operador, instalação/magia H2-3A/B, P2 sal/energia, efeito e PA, REC-ID/RC5/P4/F5. C19-021=UNKNOWN-SIDE-EFFECT; F5 P0 RED. Party/O Primeiro 0 writes; receitas, recursos, PA, inventários, preços, runtime R48 0 alteração nesta execução.

**Retomada prioritária:**
1. Verificar **IBX-38** (fencing seletivo efetivo de I0014 e reqs in-flight) e **R51/IBX-78** (parent físico único REC-LIB) no Notion; ambos continuam sem devolutiva técnica externa nas discussões relidas em 21/10, cuja última entrada recuperada era 13/10. Não repostar pedidos duplicados.
2. Receber decisão competente P2-SALT-01/P2-ENERGY-02 e revisão da fórmula atual Óleo; então provar lote, conversão peça→pó, recipiente/pote, especialista e testemunha antes de H2-3A.
3. Após fencing e GREEN específico, somente um microbloco de receita/produto com checkpoint ANTES/DEPOIS, verificação material e NAC-PASS. Nunca declarar RC5 baseado apenas em uma suíte digital.
4. Frentes independentes ainda seguras: B30-01 Tábua Lamelar de Ardósia possui PRE-REC-TLI-METROLOGY-001 e R42 PROPOSTOS (130×90×9 → 120×80×8 mm, QA ±1 mm etc), sem lote real; NÃO recriar especificação. Obter medições materiais futuras, comparar madeira/ardósia comum, B30-21 para evitar redundância, registrar somente evidência legítima.

**Critério de sucessão:** abrir LAB e a IBX-116, ler este PSV e ZIPs fixados, verificar se houve decisão nova do Mestre, prosseguir pela primeira dependência desbloqueada. Nunca declarar PROD GREEN, ACK, writer, lease, epoch, fencing ou autorização de Party sem prova real.
