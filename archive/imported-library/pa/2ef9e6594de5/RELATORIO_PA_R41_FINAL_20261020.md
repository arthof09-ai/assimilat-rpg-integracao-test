# PSV R41 — Auditoria de RE, R44/R48 e bloqueio produtivo CRAFT

**Data:** 20/10/2026. **Ambiente:** RPG DO MESTRE / MESTRE-SIDE / LAB TEST. **Objeto existente:** `LAB-CRAFT-VIGILIA-BOREAL-20261020-001`. **NÃO é implantação em produção.**

## Decisão do Mestre e critérios
- **RI** (rank do item) e **RE** (rank do efeito/habilidade) são ambos reais e independentes, conforme Atlas PR-ECO Anexo A. RIn (material), RU (usuário) distintos. O RI orienta o piso diário e o RE a tarifa por habilidade. Sem estrelas públicas de itens comuns.
- Tarifas vigentes: passiva 100% da base/dia; ativa floor(50% base)/dia e floor(60% base) por uso; piso item Bronze/Prata/Ouro/Ouro Negro/Lendário 8/11/21/35/90. PA original R26/R27 preservado.
- A autorização do Mestre habilita TEST e atos administrativamente legítimos, **não transfere credenciais, mutex externo, writer/lease/epoch/fencing, nem fornece observação de magia**.

## RE — duas perguntas diferentes
- As 26 fichas classificadas da coleção Mestre **Técnicas & Pergaminhos** documentam RE próprio: Bronze 2, Prata 6, Ouro 12, Ouro Negro 5, Lendário 1; outras 2 fichas sem rank. Este benchmark não deduz RE de RI.
- A mecânica das 26 técnicas permanece nos blocos de imagem e **não foi extraída com evidência binária recuperável nesta execução**. Não alegar 26/26 acertos ou 0%: **n_label_E0=26, n_mecanicas_lidas=0, n_predicoes_cegas_validas=0, acuracia=null**.
- Implementado `benchmark_re_r41.py`: separa rótulos oficiais ocultos do modelo, oculta o nome e os preços, exige texto mecânico independente com SHA, congela previsão e só então calcula acertos. 12/12 testes de isolamento, vazamento e denominadores PASS. Teste unitário de caso inventado é apenas teste de *software de avaliação*, NÃO acerto em habilidade real.
- Para finalizar acurácia, obter as imagens do Notion por canal autorizado que entregue bytes; transcrever e conferir mecânica sem ver o rótulo; congelar previsão; comparar com RE oficial.

## R48/R44 — prova executável real, não fantasia
- O R48 original vem do pacote autenticado R40 (SHA256 **899ea34d81025356af26b462272273244c8405f05493f6f664aa05ad9d481f11**) e mantém intactos `r48_factory.py` SHA **872dc5bf1e588a9ba6f4c45421a4dddbbe7d261842a4e951fd684bfc374c6801** e `r48_store.py` SHA **e6f684e80e0d5c95dff8ea94cbae985b0a8e046b48886d593d6e49534f046bd1**.
- Canário R48 ORIGINAL do Pingente continua rejeitado **`ONLY_TWO_EXISTING_RECIPES`**; duas receitas sintéticas históricas continuam aceitas. A whitelist original não foi editada.
- **Novo avanço LAB**: executado o componente `SandboxEngine` R44 AUTÊNTICO que a fábrica R48 já importa, com contrato aditivo e três insumos simulados (1 cristal, 1 erva e 45 cm de fibra), 4 estágios propostos e QA explícito para o Pingente. O R44 executa, mas não cria produto real nem transfere magia.
- Controle de QA incompleto: `REJECTED_QUALITY`. Transferência indicada como FALSE: `REJECTED_QUALITY`. Um valor TRUE FALSAMENTE INSERIDO numa *fixture* produz `EXPERIMENTAL_QA_PASS`: demonstra exatamente por que um QA sintético sem fonte independente NÃO valida RC5.
- `gate_material_R41.py` fail-closed: impede converter valores de fixture em P4, RC5 ou fabricação. **21/21 testes LAB PASS**; 0 produção, 0 inventário real, 0 receitas oficiais.
- **Primeira dependência de engenharia:** contrato R46/R47 para material mágico real e admissão no topo R48, sob autoridade do Executor CRAFT; nunca forjar assinaturas do fixture (raízes criptográficas do R47 são declaradamente públicas/fictícias).

## CRAFT/F5 — conclusão da investigação de controles
- Fontes oficiais: `AUTO-RUNTIME-CRAFT-01` e `OP-ARQ-RIN-REC-01`. P0 STOP/HOLD/RED vigente, C19-021 último PRE, `STOP-ACK=AWAITING-EXECUTOR`, release de lease não confirmado e `FENCING-CAPABILITY=NOT-DEMONSTRATED` na autoridade disponível.
- A intervenção sobre o runtime oficial não pode ser chamada de implantação se não há endpoint produtivo nem prova de exclusividade. Modificar palavras num registro **não impediria um writer anterior de escrever novamente**.
- **PA de consulta** permanece funcional de forma assistida sem fabricar: R39 replay fresco 510/510 e R48 original 40/40; nova bateria R41 33/33; **583/583 execuções de teste de suítes nesta passagem**, não taxa de acerto.
- **Pendente externo intransponível nesta sessão:** operador legítimo do CRAFT efetuar STOP-ACK/safe-point e revogação/release efetivos, confrontar C19-021, demonstrar fencing no caminho de escrita e autorizar explicitamente produção pela norma. Quem apenas lê Notion ou roda cópia LAB não pode atestar isso.

## Integridade e retenção
- Pacote R41 em Biblioteca pessoal do Mestre; guarda R40 e R39 originais por SHA; o runner de recuperação fria reextrai, reexecuta 510+40+33 e verifica hashes do R48 antes/depois.
- Nenhuma escrita sobre fichas, Party, O Primeiro, recursos, recipes REC-LIB ou estoque oficial. Apenas artefatos LAB locais, Biblioteca e registro documental no Laboratório/Inbox existentes.

## Gate NAC-PASS proporcional
- **PASS LAB:** consulta energética, distinção RI/RE, rótulos oficiais, integridade R48, execução R44 sintética, negativas e detecção de falso positivo, replay.
- **HOLD objetivo 1:** acurácia de RE mecânico sem imagens legíveis/verificáveis.
- **HOLD objetivo 2:** instalação no runtime CRAFT e TEE PROD sem writer/fence.
- **HOLD objetivo 3:** Pingente RC5/F5 sem instrumento/prova mágica, mecanismo canônico suficiente e gate C19.
- Conclusão: solucionamos defeitos/ausência de código e produzimos testes reais adicionais. Os bloqueios restantes não são falta de vontade ou autorização textual; são **dados/controles ausentes** que não podem ser fabricados.

**Links internos:** Atlas https://app.notion.com/p/3eec2b324ede81ea8920c52473ecc3ab; Técnicas https://app.notion.com/p/3edc2b324ede81a5b6a8c5a27f0f3aff; LAB https://app.notion.com/p/3fbc2b324ede811db848d35d4739eb00; Runtime https://app.notion.com/p/3f1c2b324ede811c8a42e1416b5c7774; Inbox IBX116 https://app.notion.com/p/3ffc2b324ede817aa3abea3cb7ba8c08.

## Aditivo final de auditoria do bloqueio C19 (leitura posterior ao selo R41)

Reabertos ainda os registros competentes [CRAFT-C19 — Ato externo de fencing exigido pela ferramenta](https://app.notion.com/p/3f3c2b324ede817fb888ca32aacaf2de), [CRAFT-C19 — decisão de revogação](https://app.notion.com/p/3f3c2b324ede813eb449f4fdfa887069) e [R02 — Montanhas Congeladas ao Norte](https://app.notion.com/p/3f3c2b324ede817790d7dde7f9d9cb5e).

**A revogação ADMINISTRATIVA do writer antigo I0014/C19 já foi aprovada pelo Coordenador**, sem criar posse material de I0015/I0016. O próprio pedido técnico comprova que o conector Notion de escrita autentica pelo mesmo link de conta e não expõe validação obrigatória de epoch, token de lease nem owner no ponto de mutação. Portanto, não há como atestar que a sessão I0014 deixou de conseguir escrever apenas porque sua permissão administrativa foi revogada em texto. O R02 vigente lista 5 minérios e 5 drops, **0/5 essências**, e o C19-021 continua em PRE/UNKNOWN; busca negativa e índice não provam inexistência física absoluta de tentativa pendente.

**Única ação externa realmente indispensável para F5:** operador com acesso à sessão/conector da I0014 efetuar bloqueio *técnico de escrita*, ou a própria I0014 fornecer STOP-ACK/safe-point/RELEASE; em seguida, reconciliar C19-021, exigir nova reserva monotônica, canário e readback. Se a plataforma não admitir isolamento seletivo, F5 continua RED. Essa condição **não é removível por engenharia Python em sandbox nem por inserção de uma linha GREEN no Notion**.

Este aditivo documental é posterior à assinatura do pacote R41; não modifica seu conteúdo, seu SHA nem o denominador de testes. Resultado de produção segue HOLD.
