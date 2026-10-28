# HANDOFF — Sucessão operacional e auditoria do DMG

**Data de referência (Mestre, UTC−03):** 21/10/2026  
**Âmbito:** MESTRE-SIDE / MESTRE-ONLY · Operação existente `OP-DMG-CORPUS-EMP-01` · DMG-RANK-01 v1.1 preservada  
**Natureza:** recuperação + verificações físicas novas + proteção TEST. Não é novo Comestre-ID, não transfere writer/lease/epoch/Assignment e não habilita revisão normativa.

## 1. Fontes de verdade e reconciliação

- OP e Plano Supremo: https://app.notion.com/p/3f3c2b324ede813e9fa0c87ebdea0b29
- DMG-RANK-01 vigente: https://app.notion.com/p/3f2c2b324ede815498cddb7844245f7e
- F0 preregistro: https://app.notion.com/p/3f3c2b324ede815faee6f277392b0bb7
- Mestre IBX-102, anexos A5 e ordem de realinhamento: https://app.notion.com/p/3fbc2b324ede813285ebfeaeee964f25
- Laboratório de Cálculo de Dano: https://app.notion.com/p/3fbc2b324ede80869ab5da839b6789de
- GitHub TEST transversal GH-RP-01: https://app.notion.com/p/400c2b324ede8147bc9af2160e0b1a8e
- Diretório persistente já existente: `/Comestre/OP-DMG-CORPUS-EMP-01/`.
- Registro predecessor recuperado: `REGISTRO_OPERACIONAL_DMG_C22_A_C29_20261021_MESTRE_ONLY.md` (Biblioteca). Contas C22–C27 abaixo vêm desse relato e **não foram recenseadas novamente nesta sucessão**.

## 2. Histórico recuperado: unidades não intercambiáveis

| Fase/campanha | Fonte do resultado | Resultado | Qualificador |
|---|---|---|---|
| C22 | Registro predecessor | +104 G1; 104/411 | 36 ocorrências numéricas, sem extrapolação global |
| C23 | Registro predecessor | +36; 140/411 | 25 conflitos reexaminados, 6 insolúveis |
| C24 | Registro predecessor | +55; 195/411 | Defesa, bypass, VLAB R214 em leitura |
| C25 | Registro predecessor | +61; 256/411 | Duração, Alma, atributo, controle |
| C26 | Registro predecessor | +89; 345/411 | 26 candidatas numéricas |
| C27 | Registro predecessor | +66; 411/411 | **Fechamento do manifesto G1**, não D0 do RPG |
| C28 | Registro predecessor | 12 externas, 19 efeitos | Reações, RI/FIP vs RE, R205 read-only |
| C29 original | ZIP localizado e revalidado nesta sucessão | Plano F0–F18, técnicas VZ, 7 admissões negativas | RE históricos dependentes do sandbox; nenhum novo RE oficial |
| C29-A6 | ZIP localizado e revalidado nesta sucessão | 60 páginas: 26 Magias, 19 Armas, 15 Artefatos | A6 D0 global ainda parcial |
| C29-A6T | ZIP localizado e revalidado nesta sucessão | 28 Técnicas | 25 homônimas das Magias, 20/25 preços distintos |
| C29-FF | ZIP localizado e revalidado nesta sucessão | Corrigidas 3 expressões de ataques | Adendo corretivo; original histórico preservado |

### Qualidade dos identificadores da coorte externa

Leitura local NOVA dos CSVs C29-A6 e C29-A6T: **60/60 Page-IDs únicos** no primeiro arquivo, **28/28 únicos** no segundo, **0 interseção por Page-ID** e portanto **88/88 IDs físicos únicos somente nessas quatro árvores**. Crosswalk exibe 25 pares com nomes em comum, 25 IDs distintos de cada lado, divergência textual de preço em 20/25, **25/25 identidades mecânicas PENDENTES** por imagens não comparadas. Esses números não fecham D0 global, não provam que os efeitos sejam iguais e não são 88 observações independentes de dano.

## 3. Verificação material nova nesta sucessão

Quatro ZIPs recuperados por ID exato da Biblioteca existente e materializados no runtime. SHA-256 integral confirmado, `zipfile.testzip() = None` (CRC ok) e todos os hashes internos dos manifestos comparados; nas entradas com tamanho esperado declarado, o tamanho também foi comparado:

| Pacote | SHA-256 do ZIP | Hashes internos aprovados |
|---|---|---:|
| C29 principal | `c5e261aacaa5227ed6ebeb8958baeda944613d43b7fe2a1272be930a964e1882` | 18/18 |
| C29-A6-60 | `cf5044cd878434cf039821fbbf6ffea66046e2fdbab82ba80e2aed73d7a083` | 3/3 |
| C29-A6T-28 | `5b804af84617e5950c4a9ef418d575265c96e4c64da8f31bb71ce9b3d1d1f454` | 4/4 |
| C29-FF | `aaeea72d27f5577ae0ff19108e14cd9d0b8809f09b8e302a5bc5cfaa5d709279` | 6/6 |

**Saldo: 4/4 CRC, 31/31 hashes internos e 13/13 tamanhos esperados declarados PASS.** Integridade dos artefatos, não revisão humana cega de fontes, não homologação de regras.

### Correção FF/chassi que deve sempre prevalecer sobre C29 antigo

- Darek, normal: `10d10+1d8+3`, DME bruto condicional **62,5**. Transformado apenas se ativado: `10d10+1d8+5`, DME **64,5**.
- Rhovan Corte, normal: `10d10+1d6+4`, DME **62,5**. Transformado apenas se ativado: `10d10+1d6+19`, DME **77,5**.
- Rhovan Tempestade, normal: `18d12+1d6+4`, DME **124,5**. Transformado apenas se ativado: `18d12+1d6+19`, DME **139,5**.
- **Não somar novamente FF ou bônus já dentro do chassi.** Os valores são brutos condicionais, sem RDF, sem chance de acerto; fonte VZ TEST/histórica, não canonização universal.

Ação efetuada: PR DRAFT [#17](https://github.com/arthof09-ai/assimilat-rpg-integracao-test/pull/17) no repositório TEST existente, branch `test/dmg-c29-ff-consumption-20261021`, head `15f827c0ddf0a616d7ad3d94d29f537cf445b320`. Acrescentadas exclusivamente `experiments/dmg_c29/errata_ff_c29.json` e `tests/test_dmg_c29_ff_errata.py` (6 testes contra fórmulas desatualizadas/double-counting, transformações condicionais e interpretação indevida). **6/6 testes específicos PASS locais**; workflow GitHub Actions `Test Integrity Auditor` **run 39701452295 SUCCESS** no head exato, inclusive replay original já existente. **PR em rascunho, sem merge, sem alteração do GitHub main nem Notion de produção.** Os scripts históricos C29 e `golden.json` permaneceram inalterados.

## 4. Estado do Plano Supremo F0–F18

- Plano de **19 fases F0–F18**, 24 garantias metodológicas E01–E24 e oito gates transversais continua único. Não criar novo plano.
- **F0 histórico: 4/8 DOCUMENTAL; 4/8 HOLD; 0 novo certificado nesta sucessão.** A1–A8 formam crosswalk operacional das exigências, não oito certificados normativos autônomos.
- **A5**: 7 arquivos Markdown anexados fisicamente na IBX-102; hoje as referências privadas resolveram URLs assinadas. **0/7 downloads de bytes pós-upload conferidos por hash**. `notion_download_attachment` não aceitou IDs de bloco/arquivo porque exige `file_upload_id` gerado na mesma integração; tentativas retornaram NOT_FOUND. Isso NÃO invalida a existência dos anexos, mas mantém o gate de integridade física pendente. Resolver por rota privada autorizada de transferência dos bytes, sem expor URLs ou baixar na Party.
- **A6**: censo G1 411/411 + outras árvores delimitadas 88/88. **D0 global UNKNOWN**, cobertura recursiva, espelhos, fontes com imagens e genealogia pendentes. Localmente a coorte externa 88 foi deduplicada por Page-ID nesta sucessão; não confundir com fecho global.
- **A7**: reserva/holdout prévia existe em relato, mas blindagem, genealogia e ausência de vazamento NÃO certificadas; não abrir dados blindados como teste de treino.
- **A8**: segundo leitor humano realmente independente e writer/epoch/lease/fencing material ainda não demonstrados. Esta janela não assumiu INSTANCE-ID/COMESTRE-ID numérico nem Writer; não marcou Inbox lida/ACK nem escreveu OP/Diário.
- **F1–F6**: execução de dados/extrações/normalização/taxonomia parcial; F6 sem fonte real admissível para prova v1.1 sem dano literal na coorte C29 (0/7 casos triados).
- **F7–F12**: análises exploratórias/estratificadas parciais, sem fechamento sistêmico.
- **F13–F14**: candidata DMG v2 e regressão total não iniciadas; v1.1 vigente.
- **F15**: stress local não equivale a stress global certificado.
- **F16**: playtest humano não feito; VLAB TEST é suporte contextual e não autoriza concluir equilíbrio.
- **F17–F18**: decisão/promulgação/migração HOLD; nenhuma escrita Party, O Primeiro ou canon.

## 5. Pendências P0–P2, prioridade baseada em gates

| Prioridade | Pendência | Próxima ação auditável, sem repetição |
|---|---|---|
| P0 | F0-A5 bytes 0/7 | Recuperar 7 anexos por canal privado legítimo, comparar SHA e cobertura de texto × mídia × filhos; congelar versão temporal de fontes |
| P0 | F0-A6 D0 global | Continuar censo recursivo a partir dos manifests/IDs existentes; não repetir G1 411/411 nem A6 88/88 |
| P0 | F0-A8 identidade/writer | Resolver sucessão com claim próprio, collision, Inbox prioritária e autoridade antes de mutar Notion OP/Diário |
| P0 | F0-A8 segundo codificador | Obter segunda codificação humana independente de amostra pré-registrada, divergências documentadas |
| P1 | F0-A7 blind holdout | Verificar reserva/linhagem/versionamento, novo seal somente antes de hipótese candidata e evitando vazamento |
| P1 | F6 prova de v1.1 | Encontrar efeito sem dano com RE/FIP competente, custo/ação/entrega completos; se inexistente conservar negativa e buscar outra família |
| P1 | Magias/Técnicas imagens | Acesso visual privado e avaliação de efeitos individuais, nunca inferir equivalência por nome/preço |
| P1 | /301, /220, Serpentáqua +105 | Preservar conflito original, encontrar autoridade específica para origem de bônus, sem ajuste silencioso |
| P1 | DoT e resists | Determinar turnos, stacking, veneno e imunidades por fonte canônica |
| P1 | VLAB matched-pairs | Protocolar fixtures, seeds e custo/ação equivalentes e enviar a executor VLAB; não tomar motor VLAB |
| P2 | F7–F18 | Só avançar conforme cobertura e aceite; candidate v2 após evidência suficiente e decisão Mestre |

## 6. Checkpoint resumido para sucessor

- **AS-OF:** 21/10/2026; MESTRE-SIDE; fonte mais recente do DMG C29 e adendos.
- **LAST-VERIFIED-UNIT nesta janela:** quatro ZIPs C29 recuperados, 31/31 hashes e 13/13 tamanhos de manifesto autenticados, crosswalk independente 88 IDs externos; PR #17 CI SUCCESS no head exato.
- **FIRST-PENDING:** F0-A5: 7 anexos com URL privada resolvida, mas sem leitura pós-upload de bytes/hash (0/7); em paralelo A6 ampliação recursiva e A8 identidade/codificação. Não transformar bloqueio A5 em loop.
- **D0–D9 GLOBAL:** NÃO FECHADOS. **G1 apenas 411/411** e externo 88 IDs físicos deduplicados em recorte — nunca declarar D0=499 global.
- **NO-REPEAT:** C22–C29, R02–R04, 24 fichas R01, VLAB R205/R214, 684 recibos R71, análises 116/148, conjunto A6 60+A6T 28 e PR #17 não devem ser recriados por hábito.
- **UNKNOWN/CONFLICT:** falta de bytes A5, segunda leitura e Writer; 25 homônimos de efeito pendentes; 0/7 fonte v1.1 admissível; fórmulas /301 /220, Serpentáqua +105, duração/DoT.
- **WRITE SET efetuado:** somente PR DRAFT TEST no GitHub + este handoff de Biblioteca; zero escrita Notion canônica, fichas, Party, O Primeiro, DMG-RANK, laboratório VLAB.
- **GATES/NAC-PASS:** integridade de 4 ZIPs PASS, CI GitHub PASS, F0 formal HOLD, NAC-PASS sistêmico/normativo HOLD. Quando gravar no Notion, só após recuperar identidade e writer e fazer ANTES→DEPOIS→REOPEN. Nada marcado ACK retroativamente.

**Status honesto:** sucessão analítica e manutenção de testes efetivadas; tomada de posse de writer do DMG no Notion **não certificada**. Não há comprovação técnica do “bug” do runtime do chat antigo; há falta de continuidade da instância relatada pelo Mestre e handoff material preservado.
