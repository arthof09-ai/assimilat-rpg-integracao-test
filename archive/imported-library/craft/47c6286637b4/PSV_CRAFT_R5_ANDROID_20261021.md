# PSV CRAFT R5 — Bancada Android v1.2 e auditoria JSON

**MESTRE-SIDE • TEST • 21/10/2026 • CM-000002 lógico / WS0001 • OP-ARQ-RIN-REC-01**  
**TRACE:** `CRAFT-R5-MOBILE-GATE-20261021-001`

## Situação de origem (ANTES)

Baseline R4 recuperado do LAB/IBX-116 Mestre em 21/10/2026. Bancada v1.1 ZIP SHA `021ce37de171e4ebb04c1a1b777d6f4e56191d0746e9d2ccb00e0e49145b8282`; revisor v1.1 ZIP SHA `456ba432343d5d70ce9dfac49b7180bd7de212b10722143b079d4985c5063b2e`. Pré-Q2/R50 B30-01, B30-02, B30-03, QMC, R45/R46 e REC-LIB relidos; não duplicar motores, receitas ou fichas.

## Alterações funcionais realmente implementadas

1. **Incerteza simétrica nos limites:** o valor da medição isolada não basta para reprovação conclusiva quando ±u alcança o intervalo permitido (caso 121,03 ±0,08 mm diante de limite 121 mm). Faixa inteiramente fora do limite permanece `OUTSIDE_PROPOSED_TOLERANCE`; cruzamento do limite resulta `INDETERMINATE_UNCERTAINTY`. Medidas negativas inválidas não são classificadas como mera reprovação; contagens discretas exigem inteiros.
2. **Revisão JSON pelo próprio Android:** seção 4 abre arquivo externo apenas para conferir avaliação, resumos, origem, IDs, duplicatas e alegações de autoridade sem acrescentar registros na sessão. Um JSON adulterado fica `REVIEW_QUARANTINE`; JSON internamente consistente fica `REVIEW_REQUIRED_NO_AUTOCANON`. Importação é condicionada à mesma auditoria. Relatório de revisão exportável; SHA somente se WebCrypto estiver disponível, senão `UNAVAILABLE_IN_BROWSER` explicitamente.
3. **Revisor Node sem segundo motor:** `review_capture.js` utiliza o MESMO `logic.js` do HTML v1.2, com pin SHA; revisão CLI concorda com relatório no browser no mesmo arquivo sintético. Revisor não autentica medição, independência ou cadeia de custódia.
4. **CSV seguro com aviso por linha:** inclui `evidence_status=TEST_ONLY_SELF_DECLARED`, fonte Mestre UUID, `authority`, `physical_verified=false`, `rc5=false`, `production_authorized=false`, `independence_verified=false` e `official_writes=0`; manteve neutralização de células passíveis de fórmula.
5. **Conservação:** v1.1 não sobrescrita neste ciclo; fonte Mestre e receita/estoque/R48/Party/O Primeiro inalterados.

## Testes da versão FINAL local

- `node tests.js`: **63/63 PASS**.
- `node test_review.js`: **26/26 PASS**.
- `node stress_guardband.js`: **2.000/2.000 vetores TEST**, SHA dos resultados `3e93033e62d035f3365797d16bbc808819a8a563c128cc2e764aed4c3bb57211`.
- Playwright/Chromium: E2E completo no viewport Android 390x844; layouts 320, 360, 390, 412 e 768 px sem overflow; formulário 3 projetos, export JSON/CSV, revisão somente leitura, rejeição de arquivo adulterado, importação de duplicata negada, sem erros JS.
- CLI Node versus parecer de navegador para o mesmo JSON de 3 amostras **SINTÉTICAS**: mesmo `review_status`, issues e contagem, sem autoverificação.
- ZIP local extraído em diretório limpo, manifesto 17/17 SHA, CRC PASS e replay frio PASS.

## Artefatos finais locais — exportáveis nesta conversa

| Artefato | Tamanho | SHA-256 |
|---|---:|---|
| `CRAFT_R5_BANCADA_ANDROID_V12_REVIEW_20261021.zip` | 345.204 B | `29b4bfb61a726bd4e12bffa8e245552831003ca5f3e1b7e4f5edcbd7f65eb6e8` |
| `CRAFT_BANCADA_MESTRE_ANDROID_V12_OFFLINE.html` | 30.028 B | `d340a1adc529f05677cb24c8ed3bc5557414477744668481000874f111cf0a2c` |

**Persistência Library — gate separado:** a Biblioteca Mestre confirmou upload de uma revisão INTERMEDIÁRIA R5 (ZIP `libfile_acff737ee9a08191b9d6b5b15e6e10f7` 342.104 B SHA `10bfc11fa879c189779f3780e998adb5e897e7d82a2d5211d7cf1c97af3bc277`, HTML `libfile_a39f91c4224c81919dcdd3d441baf5a8` 29.681 B SHA `e5f5ccf5eef06eb29afb7edf95d451527029877ec5c06c6585711c37c0a90757`). O readback do HTML **passou**; readback do ZIP INTERMEDIÁRIO acabou passando após erro temporário de 429. **A revisão FINAL local acima NÃO foi sobrescrita na Biblioteca**, porque `files.manage_library` responde `container_session_expired` para o caminho local e o novo source_file_ref exportável não foi obtido. Não chamar a versão intermediária de versão final. Pacotes finais continuam acessíveis no contexto desta conversa por seus caminhos sandbox localmente verificados.

## NAC-PASS proporcional

- **PASS:** comportamento digital, testes, navegador com viewport Android, ZIP local/CRC/manifest/replay e readback parcial da revisão intermediária.
- **HOLD:** publicação/readback do ZIP FINAL na Biblioteca, abertura específica `file://` em Android (bloqueada pela política deste ambiente), autenticação de operador/instrumento/calibração/custódia, superioridade material, magia, PA oficial, produção, RC5/P4/F5.
- **Permissões:** F5 RED, C19-021 UNKNOWN-EFFECT, IBX-38 NOVA sem fencing técnico; R51 sem parent físico único REC-LIB identificado. IBX-116 permanece NOVA/ACK exigido. Nenhuma INSTANCE-ID, writer, lease, epoch, ACK ou GREEN reivindicado. Nenhuma escrita em ficha/estoque/Party/O Primeiro.

## Próximo ponto exato

(1) Recuperar `source_file_ref` da revisão FINAL já gerada em conversa e atualizar os **mesmos** dois arquivos R5 na Biblioteca, readback final byte idêntico, sem tocar R4. (2) Coletar e adjudicar dados reais com instrumento/operador/cadeia de custódia e R45/R46 quando houver; sem fazê-los surgir por TEST. (3) Resolver IBX-38/C19 e R51 antes de qualquer RC5; P2-SALT-01/P2-ENERGY-02 e Óleo de Vedação seguem pendentes. (4) Manter LAB/OP/IBX existentes como rastros, não criar outro motor/OP/Inbox.

## ADENDO POSTERIOR VERIFICADO — R5-GATE-LIBRARY-RECOVERED-20261021-001

Este adendo **substitui somente o estado HOLD de publicação final na Biblioteca mencionado acima**, preservando o relato e a causa histórica da falha de transferência.

A ferramenta de exportação passou a fornecer `source_file_ref` concreto para os DOIS artefatos finais, e a Biblioteca Mestre confirmou a **substituição dos mesmos IDs de versão intermediária**, sem criar duplicações nem tocar na v1.1:

- **ZIP R5 final:** Biblioteca `/Comestre/CRAFT_R5_BANCADA_ANDROID_V12_REVIEW_20261021.zip`, ID `libfile_acff737ee9a08191b9d6b5b15e6e10f7`, **345.204 B**, **SHA256 `29b4bfb61a726bd4e12bffa8e245552831003ca5f3e1b7e4f5edcbd7f65eb6e8`**. Upload overwrite confirmado, materialização da Biblioteca independente, bytes idênticos, CRC PASS, manifesto 17/17 SHA PASS, replay frio extraído da cópia 63 testes JS + 26 reviewer + 2.000 vetores sintéticos + Chromium E2E + Node×browser PASS.
- **HTML R5 final:** Biblioteca `/Comestre/CRAFT_BANCADA_MESTRE_ANDROID_V12_OFFLINE.html`, ID `libfile_a39f91c4224c81919dcdd3d441baf5a8`, **30.028 B**, **SHA256 `d340a1adc529f05677cb24c8ed3bc5557414477744668481000874f111cf0a2c`**. Upload overwrite confirmado, readback byte-idêntico.

**NAC-PASS atualizado:** PASS **publicação, recuperabilidade e execução digital da revisão final R5**. Continuam HOLD abertura `file://` em Android específico, autenticidade de medições, efeitos reais, magia, produção, RC5/P4/F5, C19-021 e R51. Não alegar que os dados de demonstração sejam físicos. A documentação no LAB, OP e IBX116 deve referenciar este adendo antes do bloco anterior de publicação pendente.

**NEXT pós-gate:** só avançar com dados reais e testemunho/aferição apropriada via R45/R46, ou outra frente independente já existente; preservar os checksums acima. Não recriar motored QMC/R48 nem mexer na Party/O Primeiro.
