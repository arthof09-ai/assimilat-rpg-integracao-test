# CRAFT — REGISTRO CONSOLIDADO DE EXECUÇÃO, PENDÊNCIAS E RETOMADA (até R6)

**Projeto:** RPG Assimilação · **lado:** MESTRE-SIDE · **operação canônica única:** OP-ARQ-RIN-REC-01 · **workstream lógico histórico:** CM-000002 / WS0001.  
**Emissão:** 21/10/2026, com confronto das fontes existentes em Notion e dos artefatos locais nesta retomada.  
**TRACE de registro:** `CRAFT-CONT-REG-R1R6-20261021-001`.  
**Escopo:** consolidar o trabalho do CRAFT recuperado na conversa — não certificar execução física, admitir receitas RC5, assumir identidade de instância, emitir ACK ou alterar Party/O Primeiro.  
**Fontes persistentes:** [LAB CRAFT](https://app.notion.com/p/3fbc2b324ede811db848d35d4739eb00), [Diário da OP CRAFT](https://app.notion.com/p/3f1c2b324ede81d7aa79c83106240516), [IBX-116](https://app.notion.com/p/3ffc2b324ede817aa3abea3cb7ba8c08), [IBX-38](https://app.notion.com/p/3f3c2b324ede817fb888ca32aacaf2de), [R51 — REC-LIB](https://app.notion.com/p/3f4c2b324ede812a9153d39281b488f8) e [norma REC-LIB-01](https://app.notion.com/p/3f1c2b324ede81e2901adb9ae10b2702).

## 1. COMO LER ESTE REGISTRO — CUSTÓDIA E AUTORIDADE

- **VERIFICADO NESTA RETOMADA:** objetos Notion reabertos, contagens documentais verificadas dentro do escopo indicado, hashes/CRC dos 17 ZIPs disponíveis na pasta de trabalho e SHA dos PSVs locais. Nenhuma leitura de página/arquivo equivale a ensaio físico.
- **VERIFICADO EM PSVs/REGISTROS HISTÓRICOS:** testes/replays, readback de Biblioteca, horários e autorizações registrados nas fases anteriores. Não atribuir a esta retomada a reexecução de cada suíte antiga.
- **TEST/SINTÉTICO:** amostras, lotes, cenários, estoque, carga, massa, umidade e qualquer efeito declarado nos testes são fixtures; não são fatos de mundo, fabricação ou inventário.
- **PENDENTE/HOLD:** falta fonte/decisão competente, autorização técnica, amostra real ou gate físico. Dado desconhecido continua desconhecido.
- **Limite de competência:** Party e O Primeiro NO-WRITE. Fonte Party não substitui fonte Mestre. Não modificar receita/item/mercado/estoque/PA canônico, executar writer R48, criar novo REC-ID ou afirmar lease/epoch/fencing/ACK sem prova legítima.
- **Governança:** aplicar BOOTSTRAP-COMESTRE, NAC-CONT-03, NAC-NORM-01, NAC-PASS-02, REG-ROUTE-03, PR-ITEM-02, PR-CRN-01, REC-LIB-01 e módulos existentes, respeitando decisões posteriores expressas do Mestre. A errata PA de 20/10 afirma que o motor R26/R27 estava correto; não retornar à interpretação CRAFT superada.

## 2. LINHA DE REALIZAÇÕES — ANTES → DEPOIS

| Fase | Trabalho executado | Evidência e denominador | Estado legítimo |
|---|---|---|---|
| Histórico anterior / H2-P2 | Reuso da fábrica nativa experimental R48 seq1; prévias de Pingente, barreiras de magia, lotes e variantes; integração PA e verificadores TEST (P2/H23/ARTARD). | R48 testemunho de pedido estrutural/teste e idempotência; R48 registrou journal 0→1 TEST, 0 produtos físicos. P2 Variant Chain 56/56, ARTARD 32/32 e H23 Variant Integration 30/30 nas respectivas suítes documentadas. | Engenharia digital PASS; transferência mágica, ingrediente real, fabricação/RC5 HOLD. |
| B30-06 inicial | Sandbox Bolsa Secante de Zeólita, fonte PS, BOM fictícia, transações isoladas, idempotência/rollback, lote de 2 bolsas, comparação RH com branco. | 56/56 testes da Bolsa + 27/27 do analisador pareado; as 30 fontes B30 foram individualmente reabertas no ciclo anterior. | TEST; 0 sorção ou estoque material comprovados. |
| **R2 / B30-06** | Corrigida a interpretação de 5 medições repetidas do mesmo par de recipientes: não presumir cinco unidades experimentais independentes; auditoria de massa líquida apenas aparente. | **55/55 novos**; pacote Trial Integrity, SHA/CRC/readback/extração limpa PASS. | Pseudorreplicação identificada; avaliação física HOLD. |
| **R2 / B30-13** | Validador de Substrato de Germinação. Encontrada inconsistência 750 mL húmus + até 250 mL areia condicional versus alvo 1 L. Ensaios sintéticos transacionais/controle de sementes. | **61/61 novos**; pacote Volume Causal e replay frio. | Fórmula REAL e rendimento aguardam reconciliação/medições. |
| **R2 / F5 dual** | Integrador dos módulos B30-06/B30-13 com identidade PS e veto à autodeclaração de GREEN. | **46/46 novos**; 30 fontes PS referenciadas, 2 candidatos TEST. | 0 RC5 criados nessa rodada. |
| **R2 / BOM** | Auditoria 8 receitas Mestre + 1 variante histórica (óleo) e divergências de ingredientes/etapas; P2 Sal Santo x Encantado, energia sem etapa, Óleo divergente. | **59/59 novos**, matriz por UUID, pacote BOM Differential. | 2/8 Mestre cobertura literal; 6/8 necessitam reconciliação. |
| **R3 / acervo 34** | Inspeção de 9 Encantamentos, 17 Batalha e 8 Matrizes: 34 padrões; 29 subpáginas físicas de receita, 5 embutidas e uma ficha sem receita explícita. Matriz Invocação tem 2 receitas P/ON. | Grafo 34, **85/85** TEST; 28/29 páginas filhas explicitam Óleo de Vedação. | Identidade de receita não é produção nem disponibilidade de óleo. |
| **R3 / R51** | Migração a seco EXISTING-FIRST dos 29 IDs físicos, 5 receitas embutidas e 1 ausência explícita, sem realocar páginas nem inventar REC-ID. | **54/54** TEST, plano com 35 unidades de classificação; 0 movimentos. | HOLD destino físico/parent e fencing. |
| **R3 / BOM29** | QA de presença de ingredientes no processo em todas as 29 páginas-filhas. | **44/44** TEST; 8 cobertura textual e 21 divergências/etapas/erros de formatação. | Não retificar por sinônimo presumido. |
| **R3 / referências** | Inspeção de menções Notion: Pó Diamante Noturno resolvido, UUID sem rótulo da Matriz Cultivo NOT_FOUND; quantidade `Ex` na Matriz Proteção. | **43/43 novos**; 29/29 páginas-filhas relidas; 2 menções de bloco. | Identidade/quantidade continuam PENDENTES. |
| **R3 / fontes P2/óleo** | Matriz de 12 linhas BOM; diferença material peça Ferro Celestial ≠ pó, Pó Meteoro ≠ Pó Ferro Meteoro, essência genérica ≠ pote comprovado. | **16/16 novos**; busca dirigida, não censo global; 0 lotes verificados. | Sem substituição automática/estoque presumido. |
| **R3 / decisões** | Despacho único das 21 divergências e 7 dependências transversais, reaproveitando IBX/R51 existentes. | **13/13 novos**; fila por IDs, sem 21 tickets novos. | Apenas decisão preparada; 0 escrita em receitas. |
| **R4 / Android v1.0** | Primeira interface de coleta offline B30-01 Ardósia e B30-03 Mica, JSON/CSV, inspeção preliminar e navegador móvel. | **31/31** testes v1.0, E2E Chromium; ZIP histórico preservado. | TEST e dados autodeclarados. |
| **R4 / Android v1.1** | Mesma interface ampliada para B30-02 Cordão, sem inventar carga de serviço. Conversão mm→cm; propagação conservadora da incerteza e tri-state obrigatório em inspeções visuais. | **40/40** regressão v1.1 + E2E Chromium; ZIP e HTML publicados e readback. | Pré-validação, não segurança de uso físico. |
| **R4 / revisor JSON** | Revisor Node usa QA igual ao da bancada; recalcula resultado, evita aceitar falsos PASS e sinaliza pseudorreplicação entre lotes. | **18/18** regressão, replay frio, Library readback. | Arquivo coerente ≠ amostra autêntica. |
| **R5 / v1.2** | Cálculo simétrico da faixa ±incerteza: cruzamento de limite -> indeterminado; revisão de JSON diretamente no Android antes de importar; CSV seguro; mesmo QA de browser/Node. | **63/63 bancada + 26/26 revisor**, 2.000 vetores de fronteira e E2E Chromium; versão FINAL Biblioteca recuperada. | PASS digital; file:// em Android físico específico e provas materiais HOLD. |
| **R6 / custódia CLI (esta linha)** | Corrigida sobrescrita indevida do arquivo de origem/parecer pelo wrapper Node do revisor R5; saída agora exige criação exclusiva e rejeita path igual, destino existente, symlink/hardlink e diretório. | **12/12 testes NOVOS de custódia + 26/26 regressões**, ZIP R6 12.440 bytes, SHA/CRC/readback PASS. | Patch **separado**; não alegar que já foi fundido ao HTML/ZIP R5 nem ao ramo R6/R46. |

**Contagem responsável:** não apresentar a soma de testes de versões R4/R5 e das regressões R6 como quantidade de casos científicos independentes. R2 tem 221 novos nos quatro blocos, R3 tinha 72 novos em sua devolutiva específica (43+16+13), R4 reportou 40+18 nas suítes atuais, R5 63+26 e R6-custódia acrescentou 12 novos (reexecutando 26 anteriores). B30-06 inicial 56+27 é baseline. Grafo34/R51/BOM29 ocorreram na sequência precedente à devolutiva R3, com denominadores próprios. Todos os testes são DIGITAIS; nenhum equivale a fabricação.

### 2.1. Operações paralelas/documentos homônimos recuperados — NÃO FUNDIR

Na mesma LAB há um **outro R6**, `CRAFT-R6-R46-MOBILE-PREDOSSIER-20261021-001`, que evoluiu a interface para um **pré-dossiê declarativo R46**, 35/35 novos testes e pacotes publicados (Library `libfile_2ab2ea33eb248191b586d079f8f42c62` e `libfile_802988569364819191fb0c45ceb7444d`). Esse fluxo R46 não transforma declaração em laudo nativo; requer identidade, custódia e anexos reais. **Não está demonstrado que o patch de custódia do wrapper R6 descrito acima tenha sido incorporado nessa linha paralela.** Conferir antes de mesclar ou declarar compatibilidade.

Também há `CRAFT-R53-ITEMS-RESOURCES-QA-20261021-001` no LAB com dois exemplares **ITEM NOVO-P/TEST** (sonda de estática e tônico), sem criação de item canônico/estoque. É atividade adjacente; não confundir com as entregas físicas deste registro.

## 3. INVENTÁRIO DE ARQUIVOS — IDENTIDADE, SHA E STATUS

**Regra de retenção:** histórico não é substituído; o SHA abaixo é do arquivo efetivamente presente e conferido localmente nesta retomada. Links são caminhos da Biblioteca Mestre `/Comestre/` quando publicados em rodadas anteriores. O estado de upload/readback particular é documentado nos PSVs/Notion; inspeção local nesta retomada **não é uma nova materialização da Biblioteca**.

| Artefato resumido | SHA-256 integral | Library ID conhecido | Comprovação local atual |
|---|---|---|---|
| Bolsa B30-06 inicial (56) | `f9e5d494956039566417df0edf9e6b22bfef7e9a38190875e37c06329d0b2166` | `libfile_97733040a0ac819196d852893053c8fa` | ZIP CRC PASS |
| RH pareado B30-06 (27) | `e2ee9cdfa8a03cb615d183b69399bfa31ce002cbb9bf9ff9102e11e20cdbc343` | `libfile_9d35c509b4f08191bf8589122459a85e` | ZIP CRC PASS |
| Trial Guard B30-06 (55) | `5159f0c207a68216af07202186388db580532607d33e2c4a67688b6d015e6654` | `libfile_93597be5cdb081918b023e79094afbea` | ZIP CRC PASS |
| B30-13 Volume (61) | `9acaa3284b7cf9fedf05e12586b942ee72062fe1d1a5a2f24621787ed30dec77` | `libfile_ef6d5a12ddd88191a93ee19392376ec8` | ZIP CRC PASS |
| F5 Dual Replay (46) | `706d38ac23c09044a2567d55d099eedc2ae631fe68f4288b31c68efac28ad825` | `libfile_cd0475cf5c508191a60db793ce80587a` | ZIP CRC PASS |
| BOM Process Differential (59) | `d5f6cad06bdd7555d5dd42368d46f64f876fac510fc70bb06454ec00b355f44d` | `libfile_4d25b5cf45ec81919cf736e32429dcf9` | ZIP CRC PASS |
| Corpus34 Oil Graph (85) | `cf4268a3178dd99a55fcb60add082e8537d8dd33c5e6eeaa59afdabe0f9db0f4` | `libfile_3355e4f0b5608191a7ede176c4b0f4ad` | ZIP CRC PASS |
| REC-LIB R51 Dryrun34 (54) | `7c07e0e0aac747e2fad561965777887db1a0e0489b839d8c467dc0088608399d` | `libfile_047e92a4d828819195cad87d5d302228` | ZIP CRC PASS |
| BOM29 Preexec (44) | `671a13cc1904ff0f8b03e1e8d7b93894c7879888aa49b9dfee251f2719ea9d97` | `libfile_de43456b3f088191b9addd519e588d44` | ZIP CRC PASS |
| REC Reference Links29 (43) | `b337c80d5868cca8cb298f8dbe7a3ee15c6d2658629fa3801b36641d1147a6d9` | `libfile_b912bdd8d3588191bb255afab27de25c` | ZIP CRC PASS |
| P2 Oil Source Map (16) | `ec5abfd6840b80c4dfeac1fc372e71713d45d04a5c304bdca2d9850aea3750bf` | `libfile_9726ac58915c8191b16d76dd4384c41f` | ZIP CRC PASS |
| Decision Docket34 (13) | `895c712ad46311e43884ea5eb95b9802b32b053090b90d169b50c10838e347f2` | `libfile_f03a2f7d74708191b21fb51960bfd79b` | ZIP CRC PASS |
| Android v1.0 | `5df67b41eb29aee687c6ed01dbd23cb404fd830582b836defa29df81fbdd0fdb` | `libfile_4d186ea70a4081919c8709b34248debf` | ZIP CRC PASS |
| Android v1.1 final | `021ce37de171e4ebb04c1a1b777d6f4e56191d0746e9d2ccb00e0e49145b8282` | `libfile_cf9aec52e4a0819186eb0103f4cf6dcc` | ZIP CRC PASS |
| Revisor JSON v1.1 | `456ba432343d5d70ce9dfac49b7180bd7de212b10722143b079d4985c5063b2e` | `libfile_57f0ba3599108191947acaf9ca5b435d` | ZIP CRC PASS |
| Android R5/v1.2 final | `29b4bfb61a726bd4e12bffa8e245552831003ca5f3e1b7e4f5edcbd7f65eb6e8` | `libfile_acff737ee9a08191b9d6b5b15e6e10f7` | ZIP CRC PASS |
| Custódia R6 CLI | `03aa75511da00ffae13bed4d6c095dd0528dfa12ac003e409b17b3975a2e0505` | `libfile_4c480071b010819183889c21304f70f8` | ZIP CRC PASS |

**Arquivos HTML atuais da linha R5:** `CRAFT_BANCADA_MESTRE_ANDROID_V12_OFFLINE.html`, SHA256 `d340a1adc529f05677cb24c8ed3bc5557414477744668481000874f111cf0a2c` (Biblioteca `libfile_a39f91c4224c81919dcdd3d441baf5a8`). Em paralelo, v1.3 do R6/R46 possui outro HTML/artefato e não deve substituir este sem decisão técnica explícita.

**PSVs originais:** `PSV_CRAFT_LONGRUN_R2_20261021.md`, `PSV_CRAFT_LONGRUN_R3_20261021.md`, `PSV_CRAFT_LONGRUN_R4_MOBILE_20261021.md`, `PSV_CRAFT_R5_ANDROID_20261021.md` e `PSV_CRAFT_R6_REVIEW_CUSTODY_20261021.md`. Conservá-los por referência. Este registro CONSOLIDA, não apaga ou revoga as observações originais.

## 4. ESTADO DE PERSISTÊNCIA CANÔNICA — AGORA

**Notion verificadamente lido nesta retomada:**

- `LAB CRAFT` recebeu R2/R3/R4/R5 e **outras** frentes R6/R46 e R53, mas **NÃO tinha entrada própria confirmada para a correção de custódia R6 CLI** quando esta auditoria começou; a tentativa original foi BLOQUEADA pela ferramenta. Não transformar essa tentativa em escrita efetiva.
- `OP CRAFT` possui notas e comentários de outras frentes, incluindo R6/R46; antes deste registro, **não havia confirmação de adendo específico da R6 de custódia CLI**.
- `IBX-116` continua `NOVA` e exige ACK; ela já possui handoffs até R6/R46, mas esse fato não é autorização de execução física ou de ACK.
- `IBX-38` continua `NOVA`; a resposta de fencing da antiga instância não foi evidenciada. `R51/IBX-78` continua `NOVA`; nenhum parent físico único da REC-LIB foi certificado. Não concluir inexistência global da pasta apenas por não aparecer como filha direta.

**OBSERVAÇÃO:** A seção final abaixo deve ser atualizada após as tentativas de gravação desta resposta com o status de cada readback. Caso a conexão bloqueie Notion, o arquivo presente na Biblioteca e neste chat é o PSV que resguarda a continuidade, mas NÃO substitui automaticamente o Notion canônico.

## 5. PENDÊNCIAS ATIVAS — ORDEM DE RESOLUÇÃO, DONO DO GATE E EVIDÊNCIA REQUERIDA

| Prioridade | Pendência | Evidência/decisão para desbloquear | O que pode avançar sem ela |
|---|---|---|---|
| **P0** | **IBX-38 — fencing técnico da antiga instância + C19-021** | Atestado externo do bloqueio seletivo, reqs in-flight, STOP-ACK/release, safe-point; delta-check C19; claim-verification, epoch/lease e writer exclusivos legítimos. | TEST digital e documentação MESTRE apenas; 0 writes de produção. |
| **P0** | **R51/IBX-78 — parent físico único REC-LIB** | Descoberta/reconciliação autoritativa de parent, anti-duplicata global REC-ID+produto+versão, preservação de IDs/histórico, microbloco migratório após fencing. | Dry-run de vínculos sem mover páginas. |
| **P0** | **F5 BACKFILL-30/RC5** | F5 P0 RED/c19 UNKNOWN impedem meta 30 receitas físicas RC5; só reconhecer como físico após writer, materialidade e NAC-PASS. | Revisão de 30 fichas PS e QA/teste sem produção. |
| **P1** | **P2-SALT-01** | Decisão Mestre: Sal Geodo Santo BOM x Encantado processo. Confirmar identidade, dosagem e atualização rastreada pela autoridade. | Teste de variantes em LAB, sem aplicação. |
| **P1** | **P2-ENERGY-02** | Decidir emprego/etapa de Pedra da Luz OU Pote de Essência Mágica; não tratar OU como os dois nem ignorar energização. | Preparar vetor de teste, sem magia validada. |
| **P1** | **Óleo de Vedação e 28/29 dependências documentais** | Conciliar BOM Mestre atual 3 pó ferro x histórico 2; nomes Orvalho/Essências divergentes; conversão peça→pó, lote/custódia/quantidade, fornecedor/operador, rendimento. | Diagnóstico BOM/escassez, sem assumir óleo em estoque. |
| **P1** | **H2-3A/B magia/instalação P2** | Ingredientes físicos JIT, sal/energia/óleo resolvidos, aplicação TEST testemunhada e recebimento PA versão correta; avaliar transferência/retensão mágica em cena. | Prévia/testes sintéticos; sem item mágico RC5. |
| **P1** | **R6-custódia → ramo R6/R46** | Confirmar qual CLI/versão é entrypoint competente, comparar wrappers e incorporar correção `wx`/anti-alias sem regredir SHA do QA, aprovar e testar no ramo utilizado. | Usar pacote R6 CLI como ferramenta separada TEST, sem alegar integração. |
| **P1** | **Dados reais de B30-01 Ardósia / B30-03 Mica** | Amostras/operador/serial/calibração/custódia, instrumentos, medições C0-C3, comparador comum, rendimento, tempo, perdas, foto/laudo, custo CTE/MED; submeter R45/R46 NATIVO. | Interface Android/offline e pré-dossiê TEST. |
| **P1** | **B30-02 Cordão** | Homologar limiar/carga de serviço; tração, ruptura, nó, comprimento e comparator com fibra comum, origem da casca e impacto ecológico. | Coletar somente medições declaradas; sem “seguro para uso”. |
| **P2** | **B30-06 Bolsa Secante** | Invólucro com porosidade e retenção de pó provados, lotes reais, massa seca/água e RH com branco, unidades experimentais realmente independentes, comparador comum. | Auditoria de desenho e fixture, sem dizer adsorção medida. |
| **P2** | **B30-13 Substrato** | Reconciliação 750mL + areia condicional x saída 1L, volumetria medida, pH/contaminação, sementes/lotes/controle e comparação com solo comum. | Análise dimensional TEST, sem declarar substrato produzido. |
| **P2** | **Divergências em receitas e menções** | Revisão autoritativa das 21/29 divergências, UUID órfão da Matriz Cultivo e quantidade `Ex` da Proteção; respeitar variantes e identidade física. | Mapa QA/decisões e busca dirigida read-only, sem corrigir sinônimos por conta própria. |
| **P2** | **Experiência Android real** | Teste por aplicativo Android efetivamente usado, importação/exportação local, permissões de arquivos e anexos; Chromium viewport não comprova abertura `file://` em todos os celulares. | APK não é necessário; manter HTML e exportação TEST. |
| **P3** | **Custos, UTE/CTE/MED, mercado e escala** | Custos e rendimentos de lotes reais, época e rota, comparação econômica de substitutos, impactos de 1ª–3ª ordem. | Fórmulas abertas e parâmetros PENDENTES, sem preços inventados. |

## 6. CHECKPOINT DE REINÍCIO EXATO — SEM LOOP DOCUMENTAL

1. Ler este registro e os PSVs R5/R6, depois reabrir LAB, IBX116, IBX38, R51 e o Diário da OP. Comparar timestamps/decisões **por evidência**, não apenas por data de modificação.
2. Confirmar se a escrita de custódia R6 e este consolidado constam efetivamente do LAB/OP/IBX; caso não, usar ferramenta canônica permitida e ler novamente. Nunca registrar êxito com base na intenção de escrever.
3. Se IBX38/C19 ainda sem fencing, manter **F5 P0 RED** e priorizar blocos digitais TEST não duplicados. Não solicitar múltiplas vezes o mesmo fencing nem criar parent REC-LIB especulativo.
4. A correção R6-custódia é artefato separado. Comparar com o revisor do **ramo v1.3/R46** antes de qualquer merge; preservar SHA do QA e os test vectors R5/R6.
5. Se houver **dados reais**, checar identidade/custódia/operador/calibração e quatro anexos R46; submeter ao protocolo nativo competente e revisão humana, sem autocanonização. Se não houver, não fabricar novos números por necessidade de progresso.
6. Para P2/Óleo, usar despacho único e páginas Mestre originais. Somente após decisões oficiais e lotes, executar teste material testemunhado H2-3A; H2-3B condicionado à observação anterior.
7. Na criação de qualquer item/recurso futuro, aplicar EXISTING-FIRST, PR-ITEM/PR-CRN/REC-LIB e módulos especializados, sem sobrescrever casos P3/R53 já existentes e sem duplicar motores.
8. Encerrar cada microbloco com ANTES→EXECUÇÃO→DEPOIS, testes/denominador, hashes, readback, NAC-PASS proporcional e sucessão. O progresso validado é por **novas capacidades reais ou correções comprováveis**, não por horas presumidas ou quantidade de dossiês.

## 7. ESTADO DE SAÍDA

**PASS:** preservação de dados e código TEST, protocolos e auditorias, regressões digitais documentadas, pacotes SHA/CRC localmente íntegros, ferramentas Android e wrapper de custódia separado; alterações no Notion apenas onde readback confirmar.

**HOLD:** fabricação material, estoque, QA físico/custódia certificada, PA aplicado a item produzido, magias H2, REC-ID/RC5/P4/F5, exclusividade writer, fencing C19, R51 e correções de fórmulas não decididas pelo Mestre.

**Zero escritas materiais em Party/O Primeiro, zero novas receitas canônicas por esta consolidação.** Não chamar TEST de produto oficial.
