# PSV — PA R27 / Implantação da ponte CRAFT e registro Notion

**AS-OF:** 19/10/2026, MESTRE-SIDE, ambiente TEST; a leitura Notion foi registrada com timestamps de edição 20/10 UTC.

## 1. Estado antes

- PA R26: motor experimental funcional e matematicamente testado.
- CRAFT QMC-05: interoperabilidade PA R05 fora do entrypoint, descrita como `INTERFACE_EXTERNA_NAO_CONTRATADA` no registro vigente.
- Integração Notion: nenhum registro físico R27 até esta execução.
- CRAFT/F5: `RED`, C19-021 `UNKNOWN-EFFECT`, writer/lease/epoch/fencing não demonstrados.

## 2. Execução nova R27

- Foi construído o adaptador Python `ponte_pa_craft_r27.py` que **importa o motor R26 original** preservado; hash SHA-256 de `parecer_semicanonico_r26.py` = `7d18b43220c18e3797c9e5bac3532392ac10a30f976911c1e259e1117b13c3a8`, idêntico ao original local.
- API `consultar_ficha_craft(registro: dict) -> dict` recebe item, família, rank do item, bônus, habilidades com modo, duração/frequência/condições, usos, pesquisa comparativa e risco SC. Devolve classificação de cada habilidade, confiança, tarifa/dia, tarifa/uso, total do cenário, histórico preservado, pendências, gate e recibo SHA-256 de entrada.
- A interface rejeita comandos de publicação/produção, rejeita entrada inválida e nunca reprecifica o histórico. Resultados sem dados suficientes continuam parciais (null, não zero). Riscos SC-3/4 exigem revisão/decisão aplicável para uso material.
- Exemplo TEST ponta a ponta: item Ouro com +2 SAB (10 PA/dia), passiva Prata (12 PA/dia), ativa Bronze (3 PA/dia, 3 PA/uso). Piso Ouro (21). **25 PA/dia + 6 PA por duas ativações = 31 PA no cenário.** São pareceres semicanônicos revisáveis, não fatos P4.

## 3. QA e rastreabilidade

- **22/22** testes novos da ponte + **26/26** testes R26 + **163/163** testes de R22–R25 = **211/211** testes de regressão/contrato nesta execução.
- Pacote `/mnt/data/PA_R27_PONTE_CRAFT_NOTION_TEST_20261019.zip`: **476.279 bytes**, SHA-256 `912db6db289d0e90e6fd4e824c7028b7af5fe05ad2934d4ac07df563ebdfab9d`.
- Manifesto interno SHA-256 para 102 arquivos; CRC do ZIP íntegro, extração limpa, reexecução integral das três suítes, mesma resposta JSON da fixture.
- Fonte: `/mnt/data/pa_r27_integracao/README_R27.md`, `ponte_pa_craft_r27.py` e `fixture_craft_acessorio.json` no ZIP.

## 4. Notion — operação física e readback

- **Destino existente, não duplicado:** LABORATÓRIO CRAFT — Produção e Validação Experimental: https://app.notion.com/p/3fbc2b324ede811db848d35d4739eb00
- ID do registro: `PA-R27-CRAFT-INTEROP-20261019-001`.
- **ANTES:** 1 ocorrência física, readback verificado.
- **DEPOIS:** 1 ocorrência física, readback verificado.
- SHA do pacote, resultados, fontes, bloqueios de produção e ponto de retomada lidos de volta.
- Documento adicional `CONTRATO_PA_R27_CRAFT_TEST.md` **anexado fisicamente** à mesma página. `notion-file-block://.../CONTRATO_PA_R27_CRAFT_TEST.md` recuperado em readback; documento contratual, não executável.
- A tentativa de anexar o ZIP executável nativamente não completou porque o runtime bloqueou acesso de rede à URL de upload; **ZIP NÃO está anexado ao Notion**. Disponível para baixar nesta conversa.

## 5. GATE DE HOMOLOGAÇÃO

| Marco | Veredito |
|---|---|
| Motor R26 real consumido pelo adaptador | PASS (bytes locais preservados) |
| Contrato CRAFT compatível QMC-05 e recibo JSON | PASS em TEST |
| Regressões e replay limpo | PASS 211/211 |
| Registro documental Notion no LAB existente | PASS, ANTES/DEPOIS 1/1 e arquivo contratual |
| Integração no **entrypoint original** QMC-05 | **HOLD** — bytes binários QMC-05 não materializados; nome/assinatura real não fingidos |
| TEE da regra-mãe chamando a implementação em runtime | **HOLD** |
| CRAFT produção e REC-LIB, writer/lease/fencing | **HOLD/RED** — C19-021 UNKNOWN |
| NAC-NORM/GNN/GP-NAC e NAC-PASS terminal produtivo | **HOLD** |
| Party / O Primeiro / fontes canônicas | **ZERO ESCRITA** |

## 6. Primeiro passo pendente exato

Recuperar o ZIP **autêntico** QMC-05 que já está na Library e conseguir seus bytes em runtime confiável. O responsável legítimo CRAFT deve autenticar SHA e mapear seu entrypoint real para `consultar_ficha_craft()`; executar no LAB um canário de chamada do código QMC05 real, prova positiva e negativa e readback de resultados, cobrindo a MIE/TEE. Somente depois avaliar homologação sob os gates normativos e de writer produtivo. A recuperação do executável QMC05 não é necessária para usar a ponte TEST atual em avaliação manual.

**Resultado geral:** progresso material e rastreável em integração TEST e Notion documental; **não homologação plena do sistema PA/CRAFT em produção**. Não criar nova OP, LAB ou motor. Nem corrigir silenciosamente itens históricos.
