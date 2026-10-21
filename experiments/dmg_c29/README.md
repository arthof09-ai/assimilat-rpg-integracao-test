# DMG C29 — replay nativo, independente e não canônico (TEST)

Este ensaio roda **os dois scripts Python originais** (sem alteração de bytes) do pacote `DMG_C29_VZ_RE_FIP_F0_PLANO_SUPREMO_20261021_MESTRE_ONLY.zip`, previamente recuperado da Biblioteca do Mestre.

O código original foi preservado em `original_scripts.xz.b64` apenas para transporte textual pelo conector GitHub. A execução o descompacta em um diretório temporário, checa **SHA-256 de ambos os scripts** contra o manifesto de origem, e verifica os **10 SHA-256 dos resultados**. Não mantém um segundo motor de dano, não roda um writer Notion, não muda regras e não executa outros laboratórios.

## Reprodução

`python -I -B tests/run_dmg_c29_native.py`

Resultado esperado: `PASS_C29_NATIVE_COLD_TEST_ONLY`, **43 validações numéricas**, **10 saídas regeneradas e byte-idênticas**, `CANONICAL_DMG_CHANGE=0`, F0 4/8 HOLD e fontes A5 0/7 HOLD. O workflow do GitHub executa também os 8 testes sintéticos anteriores.

## Integridade

Fonte original SHA-256: `c5e261aacaa5227ed6ebeb8958baeda944613d43b7fe2a1272be930a964e1882`. Manifesto e hashes do subconjunto encontram-se em `golden.json`.

Isso valida **reprodutibilidade matemática e persistência do teste na nuvem**, não a conclusão científica da OP DMG, não o mérito dos efeitos mágicos e não uma mudança no cânone. Os próprios resultados registram que o revisor humano independente está pendente e a genealogia VZ não calibra DMG global.

## Segurança e responsabilidades

Executa com Python padrão, sem rede, chaves, segredos, conector Notion nem conta Replit. Os únicos arquivos gerados vivem em `TemporaryDirectory` e são eliminados no final. A origem e os laboratórios de DMG/VLAB/CRAFT/LEVEL-UP permanecem **somente leitura**. O diário e a diretriz do laboratório continuam no [Notion do Mestre](https://app.notion.com/p/400c2b324ede816e8bccef35bd18f3da).
