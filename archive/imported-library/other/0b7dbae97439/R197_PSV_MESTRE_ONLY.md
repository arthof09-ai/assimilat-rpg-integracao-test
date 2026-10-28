# PSV R197 — Bancada de Avaliação de Poder do VLAB (MESTRE-SIDE)

**AS-OF** 19/10/2026 · **OPERATION** `OP-VLAB-FUSION-SANDBOX-01` · **IDENTIDADE lógica** `CM-000006` · **INSTANCE** `CM-000006-I0001` NÃO consumida · **WORKSTREAM** `CM-000006-WS0001` condicionado · **PRODUÇÃO HOLD**.

## Mudança funcional autorizada pelo Mestre

A decisão expressa do Mestre reorienta a prioridade operacional da **mesma** operação. O produto do VLAB passa a ser diagnóstico de poder de fichas com simulação proporcional, sem substituir normas, fichas nem reclassificar criaturas. R18/v0.8.1, R01–R196, 17 contratos originais e 1.875 células históricas permanecem intactos; certificação terminal não é pré-requisito para **diagnóstico TEST proporcional**. Nenhuma norma canônica nova promulgada.

## Resultado funcional efetivamente entregue

**MODO RÁPIDO (funcional):** `code/r197_power_bench.py` recebe snapshot de ficha em JSON, calcula dano mínimo/médio/máximo EXATO a partir da expressão, Vida/CA/PA, perfis de RD identificados por autoridade, probabilidade de acerto ordinário por distribuição exata dos dados sob proficiências explícitas/hipotéticas, comparação com pares de mesma classificação/estrela/natureza e relatório de sensibilidade de lacunas. O campo `power_index` permanece `null` até calibração; `rank_reclassification_authorized=false`.

**MODO PADRÃO (projeção analítica funcional, NÃO luta integral):** o dashboard offline aceita CA e RD de cenário, calcula a distribuição de acerto e valor esperado de dano após RD para o golpe selecionado, mostra ramos de Luta, sem simular críticos, tempo, Reações, movimentos, magias, KO nem habilidades. **É uma estimativa analítica**, não um novo motor de combate nem uma vitória fictícia. Para combate event-sourced usa-se R18/v0.8.1 já recuperado.

**MODO DETALHADO (reuso real, NÃO novas lutas):** o dashboard consulta resumo auditado R196 com **cinco seeds**, **oito ramos por seed**, **40 transações de combate condicionais** sob R18, todas Liu×Concha com Liu vencedora na terceira rodada. Nenhum comando histórico foi reexecutado, nenhum RUN-ID usado novamente. O modo detalhado para novos combates continua entregue pelo motor legado R18; a bancada não o reimplementa.

**ACESSIBILIDADE:** `ui/VLAB_R197_BANCADA_PODER_OFFLINE.html` funciona sem rede, é responsivo para Android, permite escolher nove snapshots Mestre recuperados, alternar três abas e alterar adversário, CA e RD. O arquivo não tem acesso às páginas do Notion quando aberto; para nova ficha, o Comestre deve recuperar e congelar sua fonte e executar `--source novo.json` ou atualizar a base Mestre TEST versionada.

## Corpus dirigido — n=9 fichas com fonte Mestre

**Cinco Bestas Prata1:** Concha Marinha Luminosa, Tigris Sombrio, Lobo da Caverna, Cabra de Chifres, Raios de Tempestade. **Duas Bestas Prata5:** Macaco Rei (Titã publicado, status de página/ramo conflitante) e Behemoth Glacial (status Titã não publicado, página sob Ouro1). Por isso NÃO são agrupadas numa mediana homogênea. **Dois EDs:** Liu Xiaua Prata5 e Sikong Auren Lendário3, nunca misturados à coorte de Bestas.

Amostra estrita Prata1 n=5, mediana de dano nominal médio **30**, Vida **216**, CA **34**. Valores individuais:

| Besta | Dano nominal esperado por expressão | HP | CA | Dano relativo à mediana n=5 |
|---|---:|---:|---:|---:|
| Concha Marinha Luminosa | 40,5 | 210 | 40 | +35,0% |
| Tigris Sombrio | 31 | 198 | 33 | +3,33% |
| Lobo da Caverna | 27,5 | 240 | 34 | -8,33% |
| Cabra de Chifres | 30 | 240 | 39 | 0% |
| Raios de Tempestade | 30 | 216 | 33 | 0% |

A Concha apresenta dano NOMINAL e CA elevados nessa amostra, mas isso **não demonstra** sobrepotência real. Exemplo: contra CA46 de Liu, usando teste `2d6+FOR30` sob hipótese de ausência de Luta específica, chance ordinária de acerto **0%**; sob hipótese de Luta Prata normal +8 especificamente adquirida, **10/36 = 27,78%**. Críticos excluídos explicitamente. Assim, o campo de proficiência é decisivo para a ofensiva real, ao contrário de um diagnóstico baseado apenas em média de dano.

Se uma RD10 fosse aplicável à totalidade do golpe da Concha, dano esperado **por acerto** seria **30,5**, mas essa hipótese NÃO está canonizada, porque a fonte não tipa literalmente sua Mordida. A diferença entre per-hit nominal, per-hit pós-RD e dano esperado por tentativa é exibida separadamente.

**Outros exemplos:** Macaco Rei P5 (Titã) patada `2d6+54` = 61 nominal, HP750; Behemoth P5 Mordida `3d6+15` = 25,5 nominal, HP500; por flag Titã e conflitos de ramo, n=1 para cada subcoorte, SEM declarar um mais equilibrado. Liu P5 Ataque Básico `5d12+3d8+1d6+45` = 94,5 nominal agregado e não tipado por componente; Auren L3 lança `8d8+211` = 247 nominal, não comparável por ranking com P1.

## Classificação do resultado útil

- **SOURCE_DOCUMENTED_PROFILE:** Vida, CA, Alma/PA e dano nominal que constam nas páginas recuperadas (link, UUID, última edição e excerto preservados em `source/R197_SOURCE_SNAPSHOTS.json`).
- **CONDITIONAL_SOURCE_INTERPRETATION:** proficiência de Luta não escrita, tipo de dano não documentado, RD aplicada por regra de criação, efeito especial e equipamentos condicionais. Conclusões sempre por sensibilidade ou explicitamente não calculadas.
- **BLOCKED_FOR_POWER_INDEX_OR_OFFICIAL_RANK:** nenhuma calibração de âncoras suficientes para índice geral, nenhuma alteração oficial de rank/estrela, nenhuma célula oficial.

## Auditoria e recuperação

`code/test_r197_power_bench.py`: **24/24 PASS**, somente novas métricas e limites científicos. `legacy/test_monster_calibration_v01.py`: **9/9 PASS** do componente histórico intocado. `code/r197_independent_audit.py`: auditor separado do produtor rederivou aritmética, 9 âncoras UUID/fórmulas e 5 pares P1 e rejeitou **7/7 clones semânticos**, mesmo com JSON reserializado, sem importar o produtor. **Não é auditoria externa humana.** Dashboard: navegador Chromium em viewport Android (390×844), navegação de abas, mudança de CA, atualização de cálculo e 5 linhas de histórico, sem erros JS. R196 ZIP conservado por SHA256 `7dc3a95aafa7dfc4db6ae0d99f7c0474e630ea86f0f70dff4112abf771403786`.

## Governança / PSV

- **LAST-VERIFIED-UNIT:** R197 TEST — bancada e auditoria local. **FIRST-PENDING:** ampliação do corpus de mesma classificação/estrela, controle de tipagem mista, calibração de referências, primeira avaliação oficial submetida a Mestre e gate competente.
- **FONTES:** Criação de Besta, Sistema de Combate, Criação de Ficha, nove páginas Mestre; URLs e versões dentro do source freeze. Snapshots são excertos curados, não dumps autenticados de páginas inteiras. A inferência de normalidade da espécie não substitui habilidade específica.
- **NO-REPEAT:** nenhum histórico R01–R196 alterado; nenhum combate R196 repetido; verificador opera sobre recibos lidos. **UNKNOWN-EFFECT:** nenhum retry; todos os tombstones anteriores permanecem HOLD.
- **CONTRATOS:** 0/17 terminais. **BENCHMARKS:** 0/1.875 oficiais. **OBSERVAÇÕES INDEPENDENTES NOVAS DE COMBATE:** 0. Dados rápidos novos representam 9 perfis, não 9 experimentos de batalha.
- **AUTHORITY/WRITER:** nenhuma instância reclamada; writer/lease/epoch/fencing não comprovados; páginas originais, Party, O Primeiro, DMG-RANK, produção e OP protegida no Notion sem escrita.
- **NAC-CONT-03:** LER → ANTES preservado no R196 → TEST aditivo → auditoria fria → DEPOIS em pacote/PSV; não houve DEPOIS oficial do Notion por falta de writer. **NAC-NORM-01:** prioridade operacional do Mestre, não nova regra. **NAC-PASS:** TEST local PASS após verificador de distribuição; terminal/produção HOLD.

## NEXT-5 sem burocracia nova

1. Atender imediatamente a próxima ficha solicitada pelo Mestre com o modo rápido; retornar perfil e comparação em poucas operações, sem esperar contrato terminal.
2. Expandir **mesma estrela/papel e forma normal/Titã separadamente** para referências estatísticas menos frágeis (pelo menos 5–10 por subcoorte antes de conclusões comparativas fortes).
3. Investigar primeiro as lacunas de maior impacto no confronto: Luta e tipo/RD da Concha; depois testar habilidades que mudem o duelo.
4. Solicitar execução R18 detalhada somente para hipótese decisiva, mantendo seus recibos/eventos e separando amostras independentes de ramos de sensibilidade.
5. Introduzir índice global **apenas após calibração com âncoras e aprovação**; preservar 17 contratos e 1.875 células como trilha de certificação, sem contaminar diagnósticos TEST.

**Critério principal atingido em TEST:** Mestre escolhe qualquer um dos 9 snapshots congelados e obtém instantaneamente um diagnóstico multidimensional reproduzível, comparação contextual e sensibilidade das lacunas — sem executar luta longa nem alegar rank oficial.
