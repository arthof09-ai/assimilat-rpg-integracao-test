# LOTE 04 — RPG Assimilação / Pesquisas de vídeos

**Data do pacote:** 24/10/2026
**Fonte:** quatro vídeos MP4 enviados pelo Mestre; preservados na conversa (não redistribuídos no ZIP).
**IDs:** 496036, 496038, 496040 e 496042.
**Duração total:** aproximadamente 105 min 45 s; 144 quadros amostrados, nove folhas de contato.
**Escopo:** referência técnica exclusivamente MESTRE-SIDE e TEST. Nenhum dado Party ou VLAB canônico incluído.

## Comece por aqui

1. `COMPENDIO_4_RELATORIOS_LOTE04_20261024.pdf`: os quatro relatórios profissionais, inclusive contatos visuais e fontes públicas.
2. `relatorios/RELA...md`: textos individuais para busca e revisão.
3. `experimento/ARENA_TEST36_PREVIA_GEOMETRIA_VISUAL_OFFLINE.html`: cópia da Arena existente com prévia de ponto, linha, cone e círculo. É uma **PRÉVIA VISUAL — NÃO ENVIA COMANDOS**, não modifica dados do RPG. Arquivo para teste local, sem garantia de funcionamento em Android.
4. `experimento/test_geom.py` e `experimento/resultados_test_geom.json`: teste Chromium Linux em 360x740, 390x844 e 412x915. **15/15 checks PASS** (quatro formatos + integridade/fidelidade), 49 casas, zero rede, zero erro JS. Não é teste Android físico.
5. `contratos/`: quatro especificações JSON de implementação para o Desenvolvedor, sem regras inventadas; validação estrutural **16/16 PASS**.
6. `contatos/`: os quadros amostrados dos vídeos como EVIDÊNCIA DE PESQUISA, não como assets utilizáveis no jogo.
7. `meta.json`, `MANIFEST_SHA256.json`: materialização, checksum, denominação e reexecução.

## Estado do áudio

Os MP4 contêm áudio AAC. Não há legendas embutidas e o ambiente da análise não possuía modelo ASR local com pesos disponíveis. **Nenhum relatório afirma transcrever integralmente a narração**. Não exigir do Mestre transcrição paga nem áudio recortado para concluir o que foi verificável visualmente.

## Prioridade de desenvolvimento

1. Reaproveitar a Arena TEST36, nunca criar um novo jogo ou nova engine.
2. Tornar a ação/turno/alvo selecionáveis e mostrar visualização de áreas APÓS contrato da habilidade e autorização competente.
3. Mecânica real, custo PA, alcance, dano e resultado de ataque somente por interface VLAB homologada; sem autossimulação concorrente.
4. Mestre/Party filtrados por servidor antes da transmissão; HTML TEST não comprova multiplayer.
5. Nenhum commit, merge, deploy ou cópia de assets de terceiros.

## Fontes públicas consultadas

- Unity/Google, anúncio Playground e Unity Spark 07/10/2026: https://unity.com/news/google-and-unity-partner-on-new-ai-gaming-platform-for-the-next-era-of-interactive-entertainment
- Antigravity pricing oficial: https://antigravity.google/pricing
- Antigravity desktop/CLI: https://www.antigravity.google/docs/overview
- Kenney Roguelike/RPG pack CC0: https://kenney.nl/assets/roguelike-rpg-pack

**NAC-PASS proporcional:** relatório/custódia TEST PASS, homologação VLAB/WSS/Android/segredos reais HOLD.
