# Recuperação técnica — 28/10/2026 — PARCIAL / HOLD

**Executor:** Codex, operador do chat; identidade institucional Comestre não estabelecida. Ordem direta do Mestre. Escopo TEST / preservação, sem mudança de regras, fichas, Party, implantação ou promoção canônica.

## Entrega física preparada

- **941 arquivos originais distintos da Biblioteca**, incluindo os três ZIPs publicados antes do lote maior: LEVEL-UP R049, CRAFT R50BCD e Tabletop TEST42.
- **818 membros técnicos originais** extraídos, sem alterar seus bytes, de contêineres que permanecem em revisão. Para contêineres com indicadores Party, extração limitada a fontes de programas e metadados de dependências; dados/relatórios não são publicados por essa via.
- **1.759 arquivos de conteúdo; 400.062.018 bytes**, com SHA-256 por arquivo. Manifestos, relatórios e scripts de validação são evidências adicionais e não são contados como originais recuperados.
- Origem nominal, aliases, tamanho, SHA-256 e destino de cada conteúdo: [manifesto integral](../../archive/imported-library/MANIFEST_20261028.json). A origem de um membro extraído inclui ID do arquivo da Biblioteca e a cadeia exata de membros ZIP.
- `archive/imported-library/**` usa atributo Git `-text`, preservando também finais de linha em clones Windows.

## Reconciliação dos inventários existentes

Exatamente **3.095 registros candidatos** dos dois inventários existentes, sem novo levantamento da Biblioteca. **3.074** materializados com tamanho e SHA-256; **21** excedem o teto de transferência de 32 MiB e não têm identidade binária presumida.

| Categoria de registros | Quantidade |
|---|---:|
| Representados pelos novos originais (inclui aliases byte-idênticos) | 1312 |
| Preservados dentro de outros novos originais, sem cópia adicional | 979 |
| Originais mistos/indicadores Party: revisão de confidencialidade pendente | 631 |
| Já encontrados por SHA-256 no checkpoint inicial da PR | 138 |
| Arte visual sem programa, fora do escopo técnico priorizado | 7 |
| Bytes não materializados: limite de transferência | 21 |
| Direitos de imagens/quadros de vídeos ainda não comprovados | 7 |

**Registros não são uploads.** Os 1.312 registros representados por 941 originais incluem múltiplos IDs/nomes de bytes idênticos. Os 979 contidos em outros arquivos não receberam cópia adicional. Os 818 componentes extraídos são contados separadamente, e não transformam o contêiner retido em backup integral concluído.

O [ledger completo](LIBRARY_RECONCILIATION_20261028.json) mantém um resultado para cada ID e a cadeia de presença dentro dos ZIPs. A busca por nomes de personagens é indicador conservador de revisão, não prova de que todos os 631 registros retidos contêm dados protegidos. **54 dos 138 registros já existentes** também apresentam indicadores de conteúdo que requer revisão; presença por hash não significa autorização de publicação.

## Integridade dos Códigos-Mãe

R323/R324 já estavam fisicamente na PR ao iniciar a execução: não foram reenviados. Ambos foram novamente baixados da conta Drive correta e comparados byte a byte aos ZIPs reconstruídos dos objetos Git.

| Versão | Bytes | SHA-256 | Manifesto interno | ZIPs internos com CRC válido |
|---|---:|---|---|---:|
| R323 | 15634470 | `0ecf4897aa6d05cda373c4bd1a0f8f3d6f83d34add8725b8c44cd2ca2ad15fd8` | 81 conferidos | 17 |
| R324 | 15698603 | `2a52c00d2199e40c5635def308349d1dce21ca061212666595e5742dce5d68f0` | 86 conferidos | 18 |
| R325 | 15836459 | `a322ff311199643e1230b7e1cd3ea31445e1c3155615235df047a928ca58f502` | 98 conferidos | 19 |
| R326 | 15951561 | `420fa4c9f084df449e68075e30fec50ad392bfe041070433b9a4feaf4daf17d5` | 95 conferidos; 3 divergências históricas | 20 |

R326 mantém três divergências no manifesto interno histórico (`README_MESTRE_ONLY.md`, `index.html`, `manifest.json`); o ZIP original e seu SHA-256 foram preservados. Não houve reparação dos bytes originais.

Correção dos reconstrutores R323/R324: falha de abertura exclusiva agora preserva um destino preexistente. Dois ensaios de regressão com arquivo sentinela passaram.

## Segurança e bloqueio de merge

**HOLD concreto da PR inteira:** os Códigos-Mãe R323/R324/R325, já publicados na PR antes desta execução, contêm um pacote histórico de integração que inclui dados derivados de fichas da Party. O mesmo membro existe no R326 já presente na main. Evidência física: cadeia `source_archives/VLAB_STAGE12_A1A2A3_CHAT_R22_SANDBOX.zip` → `originais_imutaveis/SIM-DMG-VLAB-INDEPENDENTE-ITEM-AIN-BRIDGE-v0.5.0.zip` → `artifacts/ain_compat_bridge_v0.5.json`, SHA-256 do membro `439df09e7a476b0a9c24df3b8c5c84c6af2fe01a335f3a0112edfbe1ad6ba847`. O relatório predecessor declara uso do espelho de fontes Party. Nenhum valor de ficha é reproduzido neste recibo.

A autorização Mestre-side permite o arquivamento técnico; a restrição específica a dados Party continua aplicável. Os ZIPs R323/R324 íntegros permanecem nos links Drive oficiais já informados pelo Mestre. Não reenviar o mesmo material, codificar para ocultá-lo, reescrever o histórico ou declarar segurança da main sem resolver esta dívida preexistente. A PR deve continuar **OPEN / DRAFT / NÃO MESCLADA**.

Os 631 originais em revisão continuam preservados nas suas fontes. Parte de seus programas pôde ser recuperada por extração exata de membros elegíveis. Os sete contêineres de vídeos retidos incluem quadros/imagens de terceiros com direitos ainda não demonstrados. Os 21 registros grandes não puderam ser lidos pela ferramenta; não são classificados como duplicatas por nome/tamanho.

**Segredos:** Gitleaks 8.24.2 leu 247.743.973 bytes de textos únicos decodificados, incluindo membros ZIP recursivos, fontes xz/base64 e texto dos PDFs. Os 82 alertas foram revisados como falsos positivos (digests, IDs documentais/de receitas, sentinelas de testes); não foi usada uma supressão geral por arquivo ou desativação do detector. [Decisões exatas por hash/regra/linha](SECRET_SCAN_REVIEW_20261028.json). Triagem de Party é independente do scanner de credenciais.

## Testes e evidências

- Verificador de arquivo: 1.759 tamanhos/SHA-256, quatro pontes originais, quatro reconstruções segmentadas, 440 objetos ZIP distintos e 12.331 membros com CRC conferido — PASS local. Lê dados, sem executar programas arquivados.
- Testes existentes do repositório: 55/55 PASS local.
- Ponte 0.4.0 original: **76/76 testes Python**, incluindo Chromium Linux, typecheck TypeScript e duas demos sintéticas PASS. Os 50 testes Node são aninhados na orquestração e não somados como casos independentes. [Recibo](evidence/bridge040-20261028/receipt.json) e logs presentes. Android físico e motor canônico continuam não certificados.
- CI remoto do commit de ferramentas `b50b8bdb8e2e4013ed44541f5efabb3efcac4053`: [Auditor SUCCESS](https://github.com/arthof09-ai/assimilat-rpg-integracao-test/actions/runs/40774169307) e [Archive integrity SUCCESS](https://github.com/arthof09-ai/assimilat-rpg-integracao-test/actions/runs/40774169478). Essa execução precede o lote maior; o novo commit deve ter verificação própria.

## Estado de publicação deste recibo

O lote maior foi verificado localmente. **Readback do commit remoto e CI do lote: PENDENTES até recibo específico.** O recibo posterior deve fixar o commit relido e contar apenas bytes efetivamente recuperados do GitHub.

Main no início: `a31438287ed6d3eee8880ca70cb44ae81d432340`, 94 arquivos. PR no início: `29e819da054fafb2d87f912009432214132f8852`, 145 arquivos, aberta/draft. Nenhuma mesclagem foi autorizada por um PASS de integridade isolado.

**NAC-PASS:** comunicação/preservação permitida com ressalvas; conclusão global e merge em HOLD. Diário Mestre-side existente GH-RP, sem nova identidade, Inbox ou laboratório. Próximo passo bloqueado: revisar/separar material Party dos pacotes integrais e resolver a dívida já publicada, obter via de transferência autorizada para os 21 registros grandes e comprovar direitos dos sete contêineres de vídeo.
