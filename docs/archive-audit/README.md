# Reconciliação do arquivo técnico — GitHub × Notion × Drive × Biblioteca

**Data de corte:** 2026-10-28  
**Projeto:** RPG Assimilação / Mestre-side  
**Classificação:** AUDITORIA PARCIAL DE SINCRONIZAÇÃO; evidência documental, **não** motor homologado, deploy nem NAC-PASS terminal.

## Princípio corrigido pelo Mestre

O GitHub é autorizado pelo Mestre como repositório geral de código-fonte, programas, testes, documentação, ferramentas e artefatos de desenvolvimento RPG, inclusive Mestre-side, mesmo quando público. A antiga objeção genérica de que “é Mestre-only, portanto não pode estar no GitHub” foi **revogada** por decisão expressa do Mestre em 28/10/2026, registrada no Kit Essencial de Integração do Notion. 

Permanece a distinção: um commit público **não é** aprovação das players, canonização, promoção de produção, writer de OP ou autorização para incluir credenciais, dados pessoais, segredos de autenticação ou material de terceiros sem direitos de redistribuição. Nunca transmitir Mestre-only diretamente às páginas Party/O Primeiro.

## Fontes consultadas e cobertura real

| Superfície | Verificação | Resultado |
|---|---|---|
| GitHub [repo oficial](https://github.com/arthof09-ai/assimilat-rpg-integracao-test) | árvore recursiva antes/depois, conteúdo com readback | 60 entradas na linha inicial; 92 entradas após recuperação e depuração, antes das últimas escritas desta auditoria; contagens variam com commits posteriores |
| Biblioteca Mestre `/Comestre` | paginação completa de Files, 18 páginas | 3.476 entradas, sendo 3.467 arquivos + 9 pastas |
| Biblioteca — técnicos | extensões indexadas no inventário | 3.095 entradas de tipos técnicos; **não** equivalem a 3.095 fontes distintas/verificadas |
| Biblioteca — ZIPs | metadados do arquivo | 1.205 entradas ZIP; **nenhum ZIP binário da Biblioteca importado neste trabalho** |
| Notion Mestre | leitura seletiva das OP e normas competentes | combate, magia, criação de ficha, transformação, dano, itens, portal 2.5D, VLAB, LEVEL-UP |
| Drive antigo / novo | buscas de inventário e relatório de migração no Drive novo | relatório externo registra 5.993 arquivos RPG e 5.263 conteúdos SHA únicos; contagem **reportada**, não recontada nesta auditoria |

**Limites de busca:** não foi feito hash de cada um dos 3.467 arquivos da Biblioteca nem varredura binária completa do notebook Windows; portanto, não declarar 100% de cobertura de conteúdo/hashes. O relatório de migração no Drive é fonte documentada, mas suas métricas não substituem nova prova independente. Arquivos históricos duplicados nominalmente e de mesmo tamanho ainda exigem SHA256 para deduplicação definitiva.

## Entregas realmente publicadas (conteúdo recuperado e conferido)

1. **Programas HTML TEST:** [Tabletop TEST42](../../archive/tabletop/TABLETOP_ASSIMILACAO_TEST42_OFFLINE.html), [CRAFT R49](../../archive/craft/CRAFT_R49_REVISOR_ANDROID_MESTRE_TEST.html) e [Orc LEVEL-UP R049](../../archive/levelup/R049_ORC_ANDROID_OFFLINE_MESTRE_ONLY_TEST.html). Esses são cópias históricas executáveis em navegador, sem ensaio funcional reproduzido nesta importação e sem alterar publicação de produção.
2. **Documentação de integração:** [produção 2.5D](../production/PROTOCOLO_INTEGRADO_PRODUCAO_2_5D_v1_0_TEST.md) e [PA ↔ CRAFT](../pa/GUIA_PA_CRAFT_CONVERSACIONAL_MESTRE_ONLY.md).
3. **Manifesto de backup VLAB:** [VLAB R326](../../archive/vlab/VLAB_BACKUP_MANIFEST_MESTRE_ONLY_2026-10-27.json). É somente manifesto; a presença dele não representa os ZIPs R325/R326.
4. **Cópias documentais de Notion:** [docs/canonical-snapshots](../canonical-snapshots), fonte viva Notion sempre indicada por link. Incluem combate, magia, criação de ficha, transformação, DMG, itens, portal 2.5D, auditoria de backup VLAB e fluxo LEVEL-UP.
5. **Registros de Drive:** [docs/drive-source](../drive-source), contendo START_HERE, protocolo de colaboração com retificação de política e relatório de migração (dados reportados).
6. **Códigos avulsos efetivamente recuperados:** [archive/library-source](../../archive/library-source) — somente quatro módulos Python verificados por conteúdo completo; os outros scripts da Biblioteca não forneceram bytes/texto confiáveis pela interface de leitura.
7. **LEVEL-UP / Claude:** [recuperação P12 → P23](../levelup/RECUPERACAO_R216_P23_CLAUDE_20261028.md) e [manifesto dos 25 links Notion](../levelup/R216_P23_NOTION_MANIFEST.json). **Adendo obrigatório:** a Biblioteca possui entregas R048/R049 TEST posteriores ao checkpoint P23-045 do Notion, sem prova de promoção do motor.

Todos os links locais acima são versões em Git; há comprovação de leitura posterior para as entregas explicitadas. Não atribuir status CANÔNICO ou PROD aos snapshots.

## Inventários integrais (metadados, sem conteúdo binário)

- [Parte 01](./LIBRARY_TECHNICAL_INVENTORY_20261028_PART01.json): páginas 1–15; 3.000 entradas, 2.991 arquivos, 2.654 candidatos técnicos.
- [Parte 02](./LIBRARY_TECHNICAL_INVENTORY_20261028_PART02.json): páginas 16–18; 476 entradas e 441 candidatos técnicos.
- Total de candidatos **3.095**; `github_state=NOT_MIRRORED_OR_UNVERIFIED` nos índices é **estado conservador do inventário inicial**, não resultado individual de comparação definitiva pós-publicação.
- No corte da árvore conferida, nenhum dos 1.205 nomes ZIP da Biblioteca apareceu como arquivo Git com o mesmo nome. Alguns pacotes históricos podem conter fontes equivalentes em outros formatos; a equivalência deve ser verificada por conteúdo/hash.

## Integridade: correção de placeholders indevidos

Uma tentativa de ler vários `.py`/`.js`/`.html` da Biblioteca retornou a mensagem **“No readable content was found in this file for the requested mode.”** no lugar dos bytes originais. O texto foi inicialmente confundido com fonte em parte da importação; houve **depuração imediata**, remoção em bloco de **62 arquivos de 66 bytes** idênticos e verificação de **0 placeholders remanescentes**. Outros quatro HTML placeholders foram removidos individualmente. O GitHub preserva o histórico de commits e a correção; **NÃO** contar tais tentativas como migração de código válida.

## Lacunas prioritárias que seguem HOLD

| Frente | Pacote na Biblioteca | Estado |
|---|---|---|
| VLAB | `VLAB_CODIGO_MAE_R326_COMPLETO.zip` (15.951.561 B) | ZIP no índice Library, bytes não disponibilizados a esta conexão para upload |
| VLAB | `VLAB_R326_RECUPERACAO_HASH_E_FULLFIGHT_TEST_MESTRE_ONLY.zip` (47.695 B) | Mesma pendência |
| LEVEL-UP | `LEVELUP_ORC_R049_GATES_E_PATCHES_PRONTOS_MESTRE_ONLY_TEST_20261024.zip` (42.008 B) | Pacote TEST posterior ao Notion P23-045; confirmar fonte, hash e testes |
| CRAFT | Pacotes CRAFT R49 e auditorias de receita, múltiplas versões | Conteúdo binário ainda não importado |
| PA | `PA_10_RODADAS_R05_CATALOGO_REAL_USO_CRAFT_MESTRE_ONLY_TEST_20261024.zip` (4.635.940 B) | Houve materialização local por Files, mas GitHub não recebeu bytes; não alegar sincronização |
| INOVADOR / Tabletop | pacotes técnicos TEST40–42 e ZIPs de assets | Apenas alguns HTMLs publicados; ZIPs não |
| VISUAL | ZIPs de Orc, Capríleo, Besta Cristalina e assets volumosos | Dependem de hash, proveniência e Git LFS |

**Regra de recuperação:** ZIP da Biblioteca / arquivo no Drive / hash indicado por documento não equivale a conteúdo no GitHub. Não criar ZIP substituto sem bytes e não converter recibo TEST em aprovação de produção.

## Importação funcional em ambiente local autorizado

Foi criado [scripts/audit_and_import_library.py](../../scripts/audit_and_import_library.py), programa **sem acesso à rede**, que identifica versões já indexadas por nome+tamanho, calcula SHA256, testa CRC e paths de ZIP, sinaliza possíveis duplicatas e colisões, mantém dry-run como padrão e usa Git LFS como requisito para os ZIPs. Arquivos binários ficam em `archive/imported-library/<area>/`, com política em [`.gitattributes`](../../archive/imported-library/.gitattributes).

Exemplo **PowerShell no notebook**:

```powershell
git lfs install
python scripts/audit_and_import_library.py --source-dir "C:\CAMINHO\PACOTES_RPG" --limit 50 --receipt "auditoria_local.json"
# Somente após examinar o dry-run e confirmar que os bytes são íntegros:
python scripts/audit_and_import_library.py --source-dir "C:\CAMINHO\PACOTES_RPG" --apply --receipt "auditoria_local.json"
git status --short
```

Nenhum commit/push é automático. O operador deve analisar credenciais, licenças, repetição de hashes, efeito no limite do Git LFS, `git diff --cached`, tamanho total e continuidade. GitHub **não** deve receber cópias redundantes só para aumentar cobertura de arquivos. Arquivos históricos superiores a 100 MB exigem **LFS adequado ou estratégia de releases/artefatos**, sem forçar commits comuns acima dos limites do serviço. Preservar os hashes e recibos em catálogo.

## Estado e retomada

**LAST-VERIFIED:** a árvore GitHub após limpeza de placeholders, os HTMLs/snapshots válidos lidos de volta, os dois índices completos de metadados da Library, os documentos de Drive fonte-conferidos.  
**FIRST-PENDING:** transferência BYTE-A-BYTE e readback do primeiro ZIP técnico essencial (preferencialmente R049 LEVEL-UP ou recuperação VLAB R326), a partir de sessão local com arquivos e Git LFS.  
**NEXT:** fechar por famílias: LEVEL-UP → VLAB → CRAFT/PA → DMG → Tabletop/visual; promover **somente** após testes e autorizações competentes.  
**NO-REPEAT:** não recriar motores nem duplicar 1.205 ZIPs; não inserir placeholders como código; não refazer migração de Drive já registrada sem detectar divergência; não alterar Party, fichas nem produção por simples audit Git.

**NAC-PASS proporcional:** PASS de escrituras/readbacks documentais citados; HOLD de espelhamento integral, integridade dos ZIPs não obtidos e homologação sistêmica. O trabalho descrito foi executado de forma síncrona nesta consulta; não há tarefa em background.
