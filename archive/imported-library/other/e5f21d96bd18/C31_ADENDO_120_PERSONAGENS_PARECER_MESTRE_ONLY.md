# C31 — ADENDO DE CONTINUIDADE: fechamento do índice direto Personagens e auditoria anti-duplicação

**Operação persistente:** `OP-DMG-CORPUS-EMP-01` — **MESTRE-SIDE / TEST**, notação aditiva posterior à C31 publicada, não C32 sem verificação. **Baseline:** DMG-RANK-01 v1.1 OFICIAL/INALTERADA. F0 formal **4/8 HOLD**. OP, Diário, Inbox, fichas, Party, O Primeiro: **NO-WRITE** sem writer/lease/evidência competente. Nenhum ACK ou segunda pessoa inventada.

## Evidência MATERIAL — 120 fontes adicionais fisicamente reabertas

Parti do índice Mestre de Personagens com 233 links físicos diretos. Os conjuntos de 29 páginas de Personagens C30, 32 fichas de Personagens da C31 e 52 páginas sem marcador textual de título da C31 somavam **113 Page-IDs distintos**. Subtraí esses IDs dos **233 IDs** e abri pessoalmente o conteúdo de cada um dos **120 restantes** pelo conector Notion Mestre, em dez lotes de leitura de 10 a 14 páginas (nenhuma escrita), com verificações de texto de dano, token de dado, RE/FIP e corpo. Em **36** dessas 120 fontes, observei pools textuais do tipo NdM (não prova que cada ocorrência é ofensiva; dados também representam duração, atributo e outras métricas).

**RESULTADO:** as **233/233 páginas-filhas diretas existentes no índice Personagens estão agora cobertas por leitura do corpo renderizado Notion**, entre C30 e C31 principal e este adendo. Isso NÃO fecha todos os descendentes internos de Personagens, outros ramos globais, imagens, efeitos, versões, alias, D0–D9, revisão independente nem fonte A5 original. O CSV anexo contém os 120 IDs, URL por página e estados/limites; o campo de título só traz rótulos que foram preservados do retorno nesta auditoria e fica vazio nos outros em vez de inventar o nome.

Reconstituí os 411 IDs físicos de G1 dos arquivos C27 preservados (256+89+66), os 88 IDs externos C29 A6/A6T, os 49 C30 e os 131 C31 anteriores. O cruzamento direto confirmou **interseção ZERO** dos 120 IDs novos com todos esses quatro conjuntos; por esta enumeração delimitada, a união documental agora é **411+88+49+131+120 = 799 Page-IDs físicos distintos**, NÃO 799 definições de dano nem D0 global.

## F6 — impedimento de origem comprovado, sem criar dano

Nos 120 corpos novos a triagem literal identificou **zero tokens isolados `RE` e zero `FIP`** no texto recuperado. A fonte pode conter rank do espiritualista, rank nominal da técnica ou item, sem que isso certifique um RE/FIP individual da ofensiva. A ausência de token na página não demonstra inexistência de autoridade externa específica nem autoriza F6 PASS: estado **0 novas provas de aplicação genuína de fallback v1.1**. Existem ataques textuais numéricos preservados, mas estes não são casos de efeito sem dano.

Em Ravin (`14bc2b324ede834daba501e769feda9d`) estão `Atk: 2d6+37 (7d6+20)`; médias brutas 44 e 44,5, **não somar duas anotações**. Em Onopio (`2ebc2b324ede82cfbd1c81b7a2107bb9`) está `1d8+4d6+16`, média 34,5, sem acerto/defesa. A fonte não informa para estes o RE/FIP próprio nem resolve eventual equivalência de versões/método de ataque.

## D0 — identidade, classificação e não-independência

**Zhu Feng:** reabertas a versão `412c2b324ede83669d3a81f8b55523c4` (já C30) e a versão `3f4c2b324ede81369e4cccf6776d7803`. Os corpos Notion renderizados diferem como markup bruto, porém, após remoção de imagens e tags e normalização de espaços, o texto mecânico/narrativo de ambas ficou **idêntico**, inclusive **similaridade 1,00000 em sequências de cinco palavras**. A identidade mecânica entre os textos renderizados tem suporte técnico; a autoridade de escolher cópia oficial, a genealogia e o histórico temporal continuam pendentes. **Não contar como dois efeitos independentes.**

**Pan Tueimor:** a página Mestre `8f6c2b324ede82c88e5d8184dc3a3b90` está no índice como “Pan Tueimor”, mas o início do corpo é **“Lan Treimor (ON1)”**. Não resolver silenciosamente qual nome é o efetivo nem reescrever a ficha.

**Do Ze:** a página `1c7c2b324ede83648b6e0104f9bd2146` abre com **“Do ze (O5)”** e em seguida **“Espiritualista Demoníaco Ouro 2”**. Conflito de classificação do mesmo corpo, requer precedência/decisão da fonte competente. Não usar rank ambíguo na estratificação científica.

**Nie Li/Niel Fùhuóle:** o índice físico `86bc2b324ede827699688140e82db00b` dá título “Niel Fùhuóle” mas corpo começa `Nie Li (BDL3)`, com anotação não convencional de “Espiritualista Demoníaco 16,5”; não transformar esse fragmento em classificação padrão ou trocar identidade por suposição.

**Sieren/Nereis:** registro com “Nereis, P3” e “Espiritualista Demoníaco Ouro 2” na mesma fonte — conflito a preservar.

**Outros dados não agregáveis:** Vários personagens Lendários contêm pools e modificadores de FF/atributos/transformações; não somar tudo como DME intrínseco nem inferir o tipo e a ação de cada trecho. As fichas não são observações independentes garantidas.

## Fases/gates e próxima ação

- **D0/F0-A6**: novo progresso documental 120 fontes e fechamento **da leitura dos filhos diretos Personagens 233/233**, sem D0 global. Sem promover A6.
- **F6**: ausência de RE/FIP independente na presente fonte de Personagens e casos com dano literal; efeito real sem dano e com RE/FIP autorizado não demonstrado, HOLD.
- **F0-A5**: 0/7 anexos históricos por bytes, HOLD; sem repetição improdutiva de rota bloqueada.
- **F0-A7**: holdout histórico não tratado como cego; nenhuma fonte selada aberta para treinamento; HOLD.
- **F0-A8**: protocolo existente, sem codificador humano externo designado; HOLD.
- **VLAB**: nenhum combate executado, nenhum banco ou writer alterado; fórmulas de Ravin/Onopio e conflitos de rank propostos como insumos matemáticos, só VLAB pode executar fixture de combate.
- **PR #17**: permanece DRAFT, CI local historicamente PASS, não promover universalmente.

**FIRST-PENDING de maior valor:** navegação *recursiva* de outros ramos Mestre com Page-ID e mídia protegida, pesquisa F6 dirigida por efeito e fonte especializada com RE/FIP efetivo, e adjudicação de alias/precedência de Pan/Do Ze/Zhu Feng/Ronki antes de usar corpora em modelagem ou holdout. Nunca reexecutar G1/C22–C30 nem estressar biblioteca por contagem sem propósito. Caso não haja fontes admissíveis, produto negativo é científico e não vira regra.

## Proveniência e estados

VERIFICADO: leitura direta dos Page-IDs e reconciliação aritmética de datasets preservados, soma 799 de coortes delimitadas, comparação textual de Zhu Feng, rankings conflitantes literais. RELATADO/pendente: verdade canônica de identidade, adjudicação e segunda revisão, bytes integrais das sete fontes A5, world-wide RE/FIP. PROPOSTO: fila de reconciliação e casos para laboratório. **NAC-PASS de integridade local** separado de **NAC-PASS normativo global HOLD**. Nenhuma escrita canônica.
