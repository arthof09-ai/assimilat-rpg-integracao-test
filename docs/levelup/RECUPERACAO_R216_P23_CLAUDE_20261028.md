# LEVEL-UP — Recuperação auditável para Claude (P12 → P14/P23)

**28/10/2026 · RPG Assimilação · MESTRE-SIDE · handoff de leitura e análise; NÃO é um novo motor ou aprovação de escrita.**

## Resposta à pergunta do Mestre

O arquivo encontrado em `legado_consulta` é a **base executável histórica R216-P12**. O índice P12 foi expressamente preservado como histórico após a apresentação P13. As **25 fichas TEST válidas** estão no [índice R216-P14](https://app.notion.com/p/400c2b324ede8137a06bff45c3b5b1bb), e foram modificadas/diagnosticadas até P23-037. O último checkpoint localizado na [OP LEVEL-UP/IBX-17](https://app.notion.com/p/3f2c2b324ede81f48f80f6d27449d107) é **R216-P23-045 (24/10/2026)**, um *handoff/sucessão*, não uma nova versão do motor nem uma mudança de 25 fichas. Em **P23-044** foram produzidos **75 cenários de loadout** em três perfis (Balanceado, Ofensivo, Guarda); o preset candidato é Balanceado, mas **0/25 fichas físicas receberam esses novos números**, e não há homologação VLAB/T9.

## Fontes de verdade / ponto de entrada

1. [OP LEVEL-UP/IBX-17 — Diário e checkpoint P23-045](https://app.notion.com/p/3f2c2b324ede81f48f80f6d27449d107). Localizar seção `IBX17-R216-P23-045 — PSV / HANDOFF PREPARADO` e ler P23-040–045, antes de qualquer inferência sobre o que foi publicado.
2. [IBX-114 — envelope já existente do Executor](https://app.notion.com/p/3ffc2b324ede81aab557fd267efc02ce). Não abrir operação, motor nem atribuir-se writer por herança.
3. [Laboratório LEVEL-UP](https://app.notion.com/p/3fbc2b324ede804a95fafcb7b293c92c) e [índice das fichas R216-P14](https://app.notion.com/p/400c2b324ede8137a06bff45c3b5b1bb). Reabrir URLs do `R216_P23_NOTION_MANIFEST.json` para os 25 níveis.
4. [Índice histórico P12](https://app.notion.com/p/400c2b324ede81299714df814e9bc33e) e [runner Python atual](https://github.com/arthof09-ai/assimilat-rpg-integracao-test/blob/main/.github/workflows/native-engines.yml). A CI, no momento desta consulta, continua pinada no **P12**.
5. Pacote **P44** na Biblioteca Mestre: `/Comestre/LEVELUP_ORC_ALMA_R044_OTIMIZACAO_MESTRE_TEST_20261024.zip`, Library-ID `libfile_862b6ad9007881918e98458df9557ec2`, SHA256 `15d11a4bcd5beb5167340616c2ca8af0290940c75de1df418c0f297303a89c10`. É **pacote de otimização TEST**, não engine novo. Verificar bytes e hash ao recuperar. Se faltar acesso autorizado aos bytes, marcar `P44_BYTES_UNAVAILABLE`; não fabricar um arquivo substituto.
6. [Cópia Markdown da OP no Drive novo](https://drive.google.com/file/d/1FbVU_DUu_vPXONgNG1l6rC8XU1OQ-I9s/view) (snapshot de leitura); Notion vivo tem precedência em caso de mudança posterior.

## Reconstituição técnica sem perder desenvolvimento

**Etapa A — baseline P12 (read-only).** Localizar o ZIP no clone/Notebook, verificar nome e SHA256 `619fe210a2e8469df59f7db001220c97309cae79054b7574284a5047c633e4de` com `Get-FileHash <arquivo> -Algorithm SHA256` ou `sha256sum`. Só executar em diretório de testes com Python 3.11, nunca sobre origem:

```powershell
Get-FileHash 'lab-inputs/IBX114_SUCESSOR_R216P12_MESTRE_CORRIGIDO_20261021_MESTRE_ONLY.zip' -Algorithm SHA256
python -I -B scripts/native_engine_ci.py --engine levelup --archive 'lab-inputs/IBX114_SUCESSOR_R216P12_MESTRE_CORRIGIDO_20261021_MESTRE_ONLY.zip'
python -I -B scripts/native_full_regression.py --engine levelup --archive 'lab-inputs/IBX114_SUCESSOR_R216P12_MESTRE_CORRIGIDO_20261021_MESTRE_ONLY.zip'
```

Esperados pelo **código atual**: **184 testes dirigidos** e **2.026 regressões históricas**, não alegar execução até obter os recibos reais. Se o P12 falhar, registrar stdout/stderr e não reescrever o ZIP.

**Etapa B — ler o P23 físico.** Abrir a operação e os 25 URLs do manifesto com a conexão Notion Mestre. Conferir: 25/25 fichas, 16 slots por ficha (400), 20 alternantes de Transformação Demoníaca nos ranks Prata–Lendário, 400 diagnósticos RI/RE/FIP como metadado TEST do P23-037. O título da pasta diz P14 porque essa é a **matriz de apresentação**, não porque as páginas não receberam modificações posteriores. Comparar física ANTES com as 75 propostas P44, identificando diferenças sem aplicar nada.

**Etapa C — reconstruir as mudanças em ordem.** P23-039: GitHub só P12; P23-040: censo e custos; P23-041: sete níveis com déficit para uma T9; P23-042: simulação de margem; P23-043: riscos de INT/Alma e drenagem; P23-044: três perfis e 75 candidatos, perfil Balanceado selecionado como **candidato**; P23-045: handoff/ausência de writer e zero mudanças materiais de ficha. Preservar separação VERIFICADO / TEST-PROPOSTO / PENDENTE, sem completar lacunas de inventário inventando itens.

**Etapa D — integração segura.** NÃO promover P44 para motor em CI nem alterar os 25 sheets sem possuir efetivamente pacote, fonte, identidade, autorização de writer, proteção transacional e regressão VLAB/NAC-PASS. Se necessário, criar um adaptador de dados **subordinado ao motor existente** em branch experimental, importando dados/testes P23 verificáveis. Abrir PR para revisão; NÃO substituir automaticamente o pinned P12 nem forçar release. Priorizar uma diferença concreta, preflight, diff pequeno, rollback e evidência. O Claude tem autonomia técnica para decidir abordagem dentro da governança.

## Conjunto de evidências exigido para concluir a análise

- Path real local do ZIP P12 + SHA256, módulos/testes executados e resultado observado.
- Confirmação por leitura do último checkpoint em Notion, com data e estados.
- 25 IDs do manifesto localizados, amostra e censo de fichas REAL, diferenças em relação ao P44, sem reescritas.
- P44 ZIP: `BYTE_VERIFIED` com hash ou `UNAVAILABLE`; nunca tratar notícia de pacote como bytes.
- Matriz P12 | P13 | P14/P23-037 | P23-044 | P23-045, indicando se é código executável, view, ficha Notion, plano ou handoff.
- Pendências explícitas: T9/PA/dreno/RI-RE/VLAB/autoridade de writer, sem inventar PASS.
- Checkpoint e próximos atos na OP original quando houver autorização legítima, e relatório resumido ao Mestre.

## Decisão expressa de governança do Mestre (28/10/2026)

**GitHub é repositório autorizado para materiais Mestre-side**, inclusive códigos, programas, testes, artefatos e documentação técnica do RPG. Não há proibição genérica de usar GitHub público para conteúdo Mestre-side. A separação Mestre ↔ Party continua impedindo enviar conteúdo restrito **diretamente** ao espaço das players sem autorização. Não commitar chaves, tokens, senhas, dados pessoais ou material terceiro sem licença. Publicar documento no GitHub não significa homologá-lo como regra de jogo. Essa correção prevalece sobre a redação antiga e foi incorporada ao Kit de Integração do Notion.

**Classificação:** VERIFICADO = URLs/arquivos GitHub e Notion reabertos nesta consulta; REPORTADO/TEST = recibos P44 publicados na OP; PENDENTE = bytes P44 e execução local no notebook. Este documento não carrega conteúdo binário P44, não proclama integração P23 já existente e não reivindica writer do LEVEL-UP.
