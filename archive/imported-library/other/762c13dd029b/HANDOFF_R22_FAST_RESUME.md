# HANDOFF FAST-RESUME — CM-000001 / OP-DMG-CORPUS-EMP-01 → R23

## Entrada exata

Abra `RELATORIO_R22_CONSOLIDADO.md`, `DECISOES_NORMATIVAS_R22.md`, `R22_B11_B12_B15_RESOLUTIONS.json`, `R22_SERPENTE_LEGACY_COMPARISON.json`, `R22_B01_B18_MATRIX.json`, `R22_LIU_SCENE_AND_STRICT_GAPS.json`, `R22_I0003_FOCUSED_AUDIT.json`. R21 inteiro está preservado em `R21_ORIGINAL_READONLY.zip`. R13 oráculo em `r13_oracle.py` byte-idêntico. Não refazer motores, 198 IDs, 46 fórmulas, buscas 47 CSV/114 ZIP ou runs massivos.

## Ponto atual da ciência

B02 1/18 PASS_DOCUMENTAL, outros 9 PARTIAL, 6 BLOCKED, 2 NOT_TESTED integrais; STRICT 0/2; I0003 originais 0/9; Meta≥9/18 NÃO atingida; NAC-PASS-02 HOLD. R22 adicionou evidência PRIMÁRIA de DMG-RANK v1.1 §23: sem stacking infinito de DoT; reapplication renova duração, mesmo sem número de duração conhecido. **Página histórica excluída da Serpente foi reaberta** em `https://app.notion.com/p/4a9c2b324ede83f78dc581e101e93948`; mesma mecânica e duração omissa ANTES da repaginação; não é fonte vigente. **Não usar 1 minuto de outra adaga para Serpente**. Separou Decepadora +18 da ficha Mestre Liu de +30 em outros itens; Machado chama objeto de espada, sem elegibilidade legitimada. B15 norma global suficiente, faltam cenas tipadas.

## Próximo ato mais produtivo

1. **DEC-B11-A:** Mestre/instância legítima decide se Crítico Brutal legado `multiplicador +2` vigora sob crit aditivo v1.1; se sim, fórmula exata e arma pesada.
2. **DEC-B11-B:** Decepadora no MACHADO Liu ativa? texto diz espada; se sim +18 e ordem de dano, nunca +30 de outro item.
3. **DEC-B11-C:** segunda verificação para decepar é 3d6 sequencial independente, qual margem/condição/alvo e event receipt? Não executar amputação por inferência.
4. **DEC-B12-A/B:** duração e tick inicial do veneno Serpente, salvaguardas de remoção/cura; imunidades por tag concreta. Stacking infinito JÁ resolvido pela norma v1.1, não reabrir sem conflito superior.
5. **B15:** buscar cena certificada com pools físico+Fogo e fraqueza fonte, RD, dados e engine signed. Não pedir regra nova para exemplo explicitamente governado.
6. **B04/B09:** só perseguir ledgers reais da cena (PA livre/Perdido -46, reflexo e action/reaction, proficiência, rolagem, tempo, geometria). O retorno de busca Notion aponta fichas e hipóteses, NÃO evento. ZERO CM-000006 writes.
7. **I0003:** 0/9 raw individual original; só retomar se achar nome/Library ID/manifesto bruto/ZIP e hashes. Os 198 são índice derivado com 130+111−43 e 46 em 20 páginas, não global.

## Governança operacional

IBX-73 https://app.notion.com/p/3f4c2b324ede81ce9d33d46554ac98ff consultada em estado NOVA/Lida por em branco. Sem INSTANCE-ID, writer, fencing ou ACK; Notion/DMG-RANK/fichas/Party/O Primeiro/CM-000006 0 writes. Análise Mestre-side e arquivo local apenas. Qualquer decisão normativa deve atravessar NAC-NORM-01, NAC-CONT-03, REPA/NAC-PASS e readback real, sem auto-promover esta análise.

## Reprodução e integridade

Na extração limpa do pacote R22: `python verify_clean_r22.py <R22.zip>`; internamente `python build_r22.py` determinístico, `python -m unittest discover -p test_r22_contracts.py -q`. `R21_ORIGINAL_READONLY.zip` SHA `06d7a30aa2ae9d9c482ae69c9e8c912741334a8a99e784d66546dd5167ccf3ba`. `r13_oracle.py` preservado exato em R21, verificador compara hashes. Arquivos `manifest_R22_SHA256.json`, `QA_R22_REPORT.json` e `R22_ZIP_SHA256.txt` preservam integridade. O pacote local não é promoção canônica nem ACK de Inbox.
