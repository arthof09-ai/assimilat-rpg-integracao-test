# PSV DE SUCESSÃO — CRAFT LONG-RUN R2 / 21-10-2026 / MESTRE-SIDE

**OP única:** OP-ARQ-RIN-REC-01 — https://app.notion.com/p/3f1c2b324ede81d7aa79c83106240516  
**Sala original:** LABORATÓRIO CRAFT — https://app.notion.com/p/3fbc2b324ede811db848d35d4739eb00  
**Inbox existente:** IBX-116 — https://app.notion.com/p/3ffc2b324ede817aa3abea3cb7ba8c08  
**Workstream lógico:** CM-000002 / WS0001; NÃO atribuir instance ID atual sem autenticação.  
**Proibição:** Party e O Primeiro não recebem writes de conteúdo Mestre; não criar REC-ID, produto, loja, inventário, norma, lote ou regra com base em TEST.  

## 1. Autoridade e entrada

Reabertos o Kit Essencial/BOOTSTRAP, a IBX-116, a IBX-118 do consultor PA, a OP, LAB, REC-LIB-01 e as páginas-fonte Mestre necessárias. A correção do Mestre à tarifa PA é vigente (R26/R27 corretos): ativa diária 50% da base com floor; por uso 60% da base com floor; passiva 100%. Esta R2 não mexeu em PA. P2 SALT-01 e ENERGY-02, óleo/lote/operador e aplicação H2-3A/B continuam sem comprovação de resolução. F5 P0/RED e C19-021 UNKNOWN-EFFECT persistem; fencing, lease e writer exclusivos NÃO comprovados; sem auto-ACK da Inbox.

## 2. ANTES verificável

O último ciclo anterior (LAB e IBX-116) havia entregado B30-06 Bolsa Sintética 56/56 testes e analisador descritivo de RH 27/27, com 30/30 fichas-fonte B30 reabertas individualmente; não executou adsorção física nem RC5. CRAFT H2/P2 variant guard e R48 seq1 são históricos, não reiniciados nesta R2. B30-22 possui saída sintética no R44 (FC03) e sem mérito diferencial físico provado FC05. B30-03 já tinha QA sintético; não contar como novo. Históricos de R51 e C19 preservados.

## 3. R2 DELTA-1: integridade experimental B30-06

**Fonte:** pacote PAIRED anterior com cinco leituras de RH que reutilizam os mesmos IDs `SBX-TRT` e `SBX-BLK`.

**Defeito corrigido metodologicamente:** cinco leituras não demonstram cinco unidades experimentais independentes; risco de pseudorreplicação. Novo verificador TEST mapeia unidade, branco, batch e ciclo; rejeita alias e aceita apenas metadados estruturais como *alegados*, nunca certificação física. Massa: variação APARENTE líquida da montagem em g/g, não água adsorvida; RH percentual não é massa.

- Pacote: `CRAFT_B30_06_TRIAL_INTEGRITY_TEST_20261021.zip`
- Library: `libfile_93597be5cdb081918b023e79094afbea` / `/Comestre/`
- Bytes: **23.743**; SHA-256 `5159f0c207a68216af07202186388db580532607d33e2c4a67688b6d015e6654`
- **55/55 testes novos** + ZIP CRC, manifesto SHA11/11, extração limpa e Library byte-readback/cold replay PASS.
- Incidente real: primeira versão empacotou `__pycache__` fora do manifesto e REPROVOU replay frio; foi substituída no MESMO caminho da Library, sem duplicata ativa. Somente SHA acima é válido.
- Output TEST: média de 9pp da fixture original, massa APARENTE 0,0095 g/g em fixture nova, ambos sem qualquer medida real.

## 4. R2 DELTA-2: B30-13 Substrato de Germinação

**Fontes Mestre reabertas:**
- Húmus de Agulhas Frias PS: https://app.notion.com/p/3f3c2b324ede812b84b2fe10adb88d8e
- Areia de Brecha Granulada PS CRUA: https://app.notion.com/p/3f3c2b324ede816f9af4fdd6758bbe6c (NÃO é produto B30-04).

**Problema real de especificação:** BOM 750 mL húmus + até 250 mL areia condicional, com alvo 1 L. Sem areia, apenas 750 mL nominais. Com areia, volumes de agregados não são necessariamente aditivos depois de mistura/compactação. Não retificar fonte por conta própria.

**Funcionalidade TEST:** validador fonte/quantidade/volume, qualidade sintética, inventário exclusivamente fixture, transação unitária e duas unidades atômicas, rejeição terceira por oversell e rollback, idempotência, hash chain. Teste read-only de germinação 3 potes por braço, mesmo lote declarado, contagens/cálculo, controle solo comum, sem ganho mágico ou prova de eficácia.

- Pacote: `CRAFT_B30_13_VOLUME_CAUSAL_TEST_20261021.zip`
- Library: `libfile_ef6d5a12ddd88191a93ee19392376ec8` / `/Comestre/`
- Bytes: **12.178**; SHA-256 `9acaa3284b7cf9fedf05e12586b942ee72062fe1d1a5a2f24621787ed30dec77`
- **61/61 testes novos**, manifesto SHA7/7, ZIP CRC, readback byte-idêntico e replay frio PASS.
- 0 substratos reais, 0 avaliação de pH/contaminação/crescimento realizada.

## 5. R2 DELTA-3: integração F5 de dois candidatos

**Reaproveita sem reconstruir:** pacote B30-06 Bolsa, B30-06 Trial e B30-13 Volume em três ZIPs SHA-pinned. Um integrador read-only verifica identidade 30/30 fichas PS (inventário de origem anterior, sem alegar novo live reopen), liga B30-06 a Zeólita e B30-13 a Húmus + areia BRUTA B30-04, executa as funções originais e imprime os dois resultados. Autodeclaração `writer_green=True` junto de todos os demais campos não libera RC5 nem writer.

- Pacote: `CRAFT_F5_B30_DUAL_REPLAY_GATE_20261021.zip`
- Library: `libfile_cd0475cf5c508191a60db793ce80587a` / `/Comestre/`
- Bytes: **70.783**; SHA-256 `706d38ac23c09044a2567d55d099eedc2ae631fe68f4288b31c68efac28ad825`
- **46/46 testes novos**, manifesto SHA9/9, ZIP CRC, Library byte-readback e replay frio PASS.
- Denominadores distintos: 30 fontes PS lidas PREVIAMENTE, 2 candidatos TEST exercitados, **0 REC-ID/RC5 oficiais nesta operação R2**, contagem GLOBAL atual RC5 = **NÃO AUDITADA** nesta R2. Não converter PS em produto.

## 6. R2 DELTA-4: auditoria BOM↔processo

**Busca dirigida:** nove páginas reais (oito Mestre, uma versão histórica de Óleo), lidas no Notion por ID, caminho e conteúdo. Matriz transcrita manualmente com UUID e papel da fonte, NÃO snapshots físicos nem censo universal.

- **2/8 Mestre** com presença textual de ingredientes BOM no processo: Terra Fértil P e Chama Relâmpago P (PASS lexical, não execução).
- **6/8 Mestre** com identidade/consumo textual pendente: Vedação P2 (Sal Santo vs Encantado + energizador OR não processado); Vento Ártico B (Folhas Sussurro Congelados vs Mintaur); Nevasca P (Pó de/do e Sopro congelante/do, sinônimos candidatos não aprovados); Matriz Espacial ON (Ess Portal vs Buraco Negro; Lírio Vazio vs Fragmentos Cometa; Cinza Besta Cósmica vs Dragão Cósmico; óleo/energizador omitidos); Matriz Ilusória O (óleo/energizador BOM não explícitos); Óleo Mestre (Orvalho Amanhecer vs Dragão, Lua Minguante vs Vórtice, processo truncado).
- Óleo histórico alternativo apresenta **2** Pó Ferro Celestial; fonte Mestre apresenta **3**. Não transferir quantidade por semelhança/cópia. Ter página de item/preço Óleo não comprova lote disponível.
- Pacote: `CRAFT_REC_BOM_PROCESS_DIFFERENTIAL_TEST_20261021.zip`
- Library: `libfile_4d25b5cf45ec81919cf736e32429dcf9` / `/Comestre/`
- Bytes: **12.082**; SHA-256 `d5f6cad06bdd7555d5dd42368d46f64f876fac510fc70bb06454ec00b355f44d`
- **59/59 testes novos**, manifesto SHA7/7, ZIP CRC, Library byte-readback e replay frio PASS.
- Não alterar nove fontes, criar sinônimos obrigatórios, reclamar que magia nunca pode funcionar, nem transformar revisão lexical em NAC-PASS físico.

## 7. REGRESSÃO FRIA / GATE

**Quatro arquivos originais + quatro cópias Library** comparados com igualdade binária. Cada cópia recuperada foi extraída em diretório limpo e executada pelo `code/run_replay.py` próprio, aprovando respectivamente 55, 61, 46 e 59 testes distintos. **Total R2 NOVO = 221/221**, não adicionar 56+27 históricos ou contar os 55/61 reexecutados dentro de integração como testes novos.

Recibo local auditável: `REGRESSION_CRAFT_B30_R2_20261021.json` (na pasta de trabalho; sua inclusão em Library é opcional no checkpoint final). Todos os artefatos contêm README/manifests; nenhum deles escreve Notion/Party/estoque via scripts.

## 8. PERSISTÊNCIA CERTA vs PENDENTE

**VERIFICADO:** LAB CRAFT recebeu ANTES e DEPOIS para cada novo componente, a mesma página foi reaberta e continha os hashes de Trial e BOM. OP principal não pôde receber adendo no CORPO no ciclo anterior; nesta R2, alternativa competente **comentário Mestre-SIDE** realmente criado no thread de Diário existente, ID `400c2b32-4ede-814b-ad9f-001d452f3e09`, relido via discussão. Isso **não equivale** a alteração do corpo, estado, propriedades ou escritor produtivo da OP.

**VERIFICADO:** devolutiva consolidada `CRAFT-LONGRUN-R2-20261021-001` escrita exatamente UMA vez na IBX-116 já existente e readback confirmando os quatro hashes principais; Notion AS-OF 2026-10-21T12:01:41Z. Propriedades permaneceram `Estado=NOVA` e `Exige ACK=true`. Isto é entrega documental, **NÃO ACK, não LIDA por outra instância, nem writer/GREEN**. Nenhuma nova Inbox criada.

## 9. NAC-PASS proporcional

**PASS:** pesquisa Mestre Notion em escopo limitado; engenharia/testes digitais TEST 221/221; ZIP CRC; hash/manifestos; execução limpa; Biblioteca byte-readback; rastreio no LAB e comentário OP.

**HOLD:** fabricação e eficácia físicas, testemunho de magia e consumo PA, lotes/operadores/estoque material, decisões P2-SALT-01 e P2-ENERGY-02, Óleo lote, H2-3A/B e H2-4/5, JIT/PS/P4, F5/RC5/PROD; C19-021 UNKNOWN-EFFECT, STOP-ACK/RELEASE, fencing I0014, exclusividade writer/epoch/lease/GREEN; REC-LIB físico R51. Não há autorização tácita de criação de receita ou de sincronização à Party/O Primeiro.

## 10. FIRST-PENDING E PRÓXIMOS 5

1. **Administrativo concluído nesta R2:** retorno na IBX-116 persistido e readback confirmado, sem ACK. Próxima ação administrativa é apenas consumir alguma decisão competente nova se ela realmente chegar, sem duplicar a devolutiva.
2. **P2/H2:** decisão formal competente do Mestre sobre Sal de Geodo Santo/Encantado e etapa/carga de energização; comprovar fonte de óleo em lote, quantidade e operador/testemunha; só então executar H2-3A TEST autorizado antes de H2-3B.
3. **F5 R51/C19:** destinatário REC-LIB único e fencing externo da instância antiga; sem writer GREEN preservar HOLD. Nenhum recurso PS deve ser criado por quota.
4. **B30-06:** comprovar invólucro poroso, retenção de pó, massa seca/sorção real com branco e unidades experimentais independentes, custo MED e controle comum. A impressão de 5 linhas não é independência física.
5. **B30-13 / receitas existentes:** autoridade da BOM de 1L, medição final sob compactação, ensaio de germinação e pH real; resolver divergências de ingredientes BOM↔processo uma receita por vez pela fonte competente, preservando histórico e não corrigindo com sinônimos inferidos.

## 11. Regras de sucessão

NÃO recriar operação, laboratório, Inbox, REC-LIB, B30-22 R44, B30-03 QA ou projeto Pingente H2. Reusar os quatro ZIPs SHA fixos e os baselines históricos por referência; executar replay frio por arquivo antes de derivar novos resultados. Não reivindicar owner/INSTANCE-ID/escrita concorrente. Para cada atividade registrar `AS-OF`, fonte/dados, ANTES/DEPOIS, denominador, código de caso, SHA, sucesso/erro, NAC-PASS, `FIRST-PENDING`, efeito no estoque real (0), Party/O Primeiro (0), próximo bloqueio de autoridade sem prometer conclusão futura. Separar VERIFICADO, INFERIDO, PROPOSTO, PENDENTE. F5 RED sempre vence testes sintéticos. Nenhuma data/horário de partida do jogo é alterado por este relatório.
