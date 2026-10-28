# PSV — OP-VLAB-FUSION-SANDBOX-01 — R187–R196

**AS-OF:** 2026-10-19. **AMBIENTE:** MESTRE-SIDE, laboratório TEST isolado.
**IDENTIDADE:** CM-000006 lógica; `CM-000006-I0001` candidata **não reclamada**, workstream `CM-000006-WS0001` condicionado.
**OPERATION:** `OP-VLAB-FUSION-SANDBOX-01` original, produção **HOLD**.
**BASELINE:** R01–R186 preservada por ZIP R186 original SHA-256 `83465276a9b2822cf2791d206dd570b6fe6a9fa5711c85d1cd164ebd4d9ab3b7`.
**LAST-VERIFIED-UNIT:** R196 distribuição TEST / auditor independente DE CÓDIGO, sujeito a readback.
**FIRST-PENDING:** atribuição específica Luta/Iniciativa da Concha, Iniciativa de Liu, distribuição dos tipos do dano básico de Liu e interpretação de componentes mistos/RD. A habilidade Fúria requer ação/duração/+80 Vida.

## R187 — Censo dirigido
25 páginas distintas de Bestas existentes no bestiário Notion foram reabertas; arquivo `source/R187_BEAST_MATERIALIZATION_CENSUS.json`. Isto não constitui censo global das 411 páginas e a mera página não prova admissão em um encontro oficial. Uma candidata física própria selecionada: Concha Marinha Luminosa (`474c2b324ede82d08ea6819069c17043`). **Bestas oficiais fonte-completas confirmadas: 0 entre 25 inspecionadas.**

## R188 — Iniciativa
- Liu P5: dado `2d6`, DES16, Instinto Selvagem +4; +0 ou +2 de Iniciativa específica pela ambiguidade de marcação, somente em hipóteses experimentais.
- Concha P1: dado `2d6`, DES27, proficiência específica não escrita. Testadas hipóteses binárias +0/+8, jamais assumidas como valor canônico.
- Empate não resolvido normativamente: **PRE-COMMIT HOLD**, nenhum desempate fabricado.

## R189 — Geometria
Geometria TEST: superfícies em contato, mesma camada, linha de efeito confirmada, sem movimento. Não se alega distância natural de campanha, alcance métrico de mordida, velocidade derivada ou linha de efeito por fora do recorte. O preflight bloqueia ausência de contato ou movimento não documentado.  **Geometria natural da campanha: PENDENTE**.

## R190–R191 — Combatentes / seletor
- **ED real:** Liu Xiaua, Prata 5, HP235, PA73, CA46, RDF10, ataque `2d6+37`, dano agregado literal `5d12+3d8+1d6+45`; fonte `https://app.notion.com/p/0b4c2b324ede837cb6be818dc8e36010`, revisada em 2026-10-01.
- **Besta fisicamente materializada:** Concha Marinha Luminosa, Prata 1, HP210, PA70, CA40, FOR30, DES27, Mordida `3d6+FOR`; fonte `https://app.notion.com/p/474c2b324ede82d08ea6819069c17043`, revisada em 2026-10-01.
- RD básica da Concha 15 deriva de Criação de Besta normal Prata vigente; a aplicação a essa página legada e tipagem exata da mordida dependem de autoridade. **Não se declarou novo atributo canônico na ficha.**
- **Importante:** o produtor calculou o dano agregado de Liu como um único componente físico `impacto` e a mordida como `perfurante`, **interpretações LAB**, não tipagem literal homologada. Tal hipótese poderia alterar o dano pós-RD em um verdadeiro acerto misto. Logo não se pode homologar a batalha nem alegar universalidade do vencedor.

## R192 — PA
O gasto novo do combate é 0 PA, pois ambos usaram somente ações normais. A ficha de Liu documenta Fúria 12 PA, disparada a meia Vida (+15 FOR/+80 Vida), mas **ação, duração e semântica de +80 Vida** não estão fechadas. Gate R192 4/4 PASS por rejeitar ativação não legitimada; nenhuma redução artificial de PA. A defesa de 50 PA R186 permanece comprovada historicamente e intocada.

## R193 — Execução funcional nova
`R193_PRE_REGISTRATION.json` foi gravado **antes** do primeiro combate; SHA256 `fc5b4be4191da4f6c4a3cbcfe8a46d96b3a1aef8ed8b0739759b1fc5e03a58b6`.
Cinco seeds congeladas — uma desenvolvimento (`18719301`), uma validação (`18719311`) e três holdout (`18719321`,`18719322`,`18719323`) — cada uma com **8 hipóteses sobre proficiências**, total **40 bancos TEST**, **UM confronto e UMA espécie** (não 40 observações independentes).
Todos os 40 ramos chegaram a HP0 na 3ª rodada com Liu vencedora **sob as hipóteses físicas delimitadas**. A Vida final de Liu dependeu da proficiência da Concha:

| Seed | Grupo | Vida final Liu entre ramos | Concha final | Rodada | Vencedor sob hipótese |
|---|---|---|---|---|---|
|18719301|desenvolvimento|201–235|0|3|Liu|
|18719311|validação|235|0|3|Liu|
|18719321|holdout|209–235|0|3|Liu|
|18719322|holdout|178–235|0|3|Liu|
|18719323|holdout|205–235|0|3|Liu|

**Contraindicação explícita:** o resultado não é prova de vitória independentemente de modificadores não documentados, tipagem elemental alternativa, geometria não testada ou habilidade não utilizada. A amplitude dos HP confirma relevância documental da proficiência; certificar por constância do vencedor seria erro.

## R194 — Auditoria + ciência
- **276 commits R18 SQLite**, **708 eventos nativos**, **236 recibos ofensivos** em 40 bancos legítimos, reconstruídos por `code/r194_independent_replay.py`, que não importa o produtor R193.
- Código auditor reproduz iniciais, fita RNG por ator/turno, ataque, crítico sequencial, Vida, RD, dano e overkill, ordem de turnos, PA e checkpoint. **PASS_R194_INDEPENDENT_LOCAL_SEMANTIC_AUDIT**.
- **10 clones semânticos**: identidade, iniciativa, RD, acerto, PA, geometria, tipo de dano, fita RNG, overkill, sequência de eventos. Todos os hashes de cadeia SQL recompostos; o validador estrutural R18 aprovou 10/10, enquanto o auditor semântico REJEITOU 10/10. Auditor **não é humano externo**.
- Holdout: três seeds **pré-registradas antes da execução**, políticas e regras congeladas, mas três blocos de uma mesma dupla não permitem generalização entre espécies/personagens. O resultado é condicionado e deve manter esta classificação.

## R195 — Contratos e células
- Original 17/17 IDs do crosswalk histórico preservados em `R195_17_CONTRACT_CROSSWALK.json`, com coluna R187–R196 aditiva e nenhum terminal fabricado.
- **Contratos certificados:** 0/17.
- **Benchmarks oficialmente admitidos:** 0/1875. Célula *potencial* ED×Besta permanece sem ID ou aprovação; detalhes em `source/R195_OFFICIAL_BENCHMARK_GATE.json`.
- Recibos potenciais para DMG mantidos somente na Biblioteca Mestre em `evidence/R195_DMG_ED_BE_OFFENSIVE_RECEIPTS.csv`, não ingeridos automaticamente na coorte DMG.

## R196 — Continuidade e autoridade
- **NO-REPEAT:** nenhum RUN-ID histórico R01–R186 reutilizado, nenhum duelo antigo reexecutado, nenhum tombstone ressuscitado.
- **UNKNOWN-EFFECT:** incidentes históricos HOLD preservados. Novas transações R193 possuem estado `FINISHED`, 0 tentativas de retry, 0 UNKNOWN-EFFECT reexecutados.
- **AUTHORITY / WRITER:** perfil CM-000006 segue PAUSED/PROFILE-V1; instancia I0001 não consumida; writer/lease/epoch/fencing não comprovados. Produção HOLD. **Notion operacional, Party, O Primeiro, fichas oficiais e DMG-RANK: 0 escrita**.
- **NAC-CONT-03:** leitura de fontes antes, execução em réplicas, readback binário e PSV local. Registro documental protegido DEPOIS não efetuado por falta de writer.
- **NAC-NORM-01:** nenhuma interpretação nova promulgada. Questões de autoridade estão em `source/R196_AUTHORITY_DECISIONS_REQUIRED.json`.
- **NAC-PASS:** técnico LAB PASS local, **TERMINAL HOLD**, sem atestado externo de homologação.

### NEXT-5
1. Submeter as seis decisões pontuais do arquivo de autoridade ao Mestre/canal normativo autorizado; não resolvê-las por inferência.
2. Após decisões, congelar novos snapshots por versão, com autor competente e readback Notion; não modificar páginas originais sem writer.
3. Reutilizar os módulos v0.8.1 e R18 em uma execução **nova**, sem reaproveitar os 40 RUN-IDs anteriores.
4. Completar dano misto tipado e economia de Fúria antes de incluí-los, ou escolher outro ED cujo dano esteja integralmente tipado.
5. Submeter ao auditor externo/contratos e ao programa de 1.875 células somente a cena que superar integralmente os gates.

## Comparação essencial
R186 tinha NPC Varok **não ED** × Leviatã **pré-criada** com defesa energética eficaz. R193 agora possui **ED real Liu × Besta com página física própria Concha**, 5 blocos de seeds e sensibilidade estruturada às proficiências ausentes. Avançou identidade/admissibilidade e a capacidade de provar invariância restrita de vencedor sem transformar proficiências desconhecidas em fatos. **Ainda não entregou combate pleno fonte-admissível.**
