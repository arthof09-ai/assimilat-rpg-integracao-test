# PSV VLAB R209 — Tempestade de Esporos, área 5m, três alvos reais em combate TEST

**AS-OF:** 20/10/2026. `OP-VLAB-FUSION-SANDBOX-01`; CM-000006 lógico; LAB local isolado. **Party, O Primeiro, regras, DMG-RANK e fichas originais NO-WRITE**. Nenhum writer/epoch/lease/fencing ou I0001 herdado; produção HOLD. Não repetir R01–R208.

## Fonte e escopo

`https://app.notion.com/p/3f6c2b324ede819cae98ec0f6a63de76` — Sikong Eristan, NPC de encontro Mestre-side **PROPOSTO**, com habilidade própria **Tempestade de Esporos**: Ação Padrão, 80 PA, círculo **raio 5 m** centro até **25 m** (especificidade suplanta 6/9 m gerais), 10d10+10 Planta, **Fortitude CD76**, sucesso metade, instantânea. Sem crítico mágico. Sua fonte não estabelece arredondamento de dano ímpar reduzido pela metade; experimento deliberadamente não encontrou salvaguarda bem-sucedida, pois testes máximos dos alvos não superam a CD; o caminho de redução/rounding continua **HOLD**. O dano é rolado uma vez por conjuração e compartilhado entre alvos (convenção TEST explícita, não canonização de como todas as magias de área rolam dano).

Dois **Dracolions hipotéticos TEST** da mesma fonte `https://app.notion.com/p/a3dc2b324ede8398b446017325a70d76` (classificação Ouro corpo versus ON1 árvore; ataques básicos genéricos LAB). Posição Eristan(0,0), Dracolions (1.5,0) e (0,1.5), centro da conjuração (1.5,0) inclui os **três**; o texto da magia afeta *todos na área*, e **o próprio conjurador não foi excluído automaticamente**. Seus testes Fortitude são 4d6+CON45 e os das Bestas 3d6+CON29, sob fonte/atributo e hipótese sem proficiência extra inventada. Resistência mágica dos três não publicada; RD mágico=0 **LAB somente**, nunca afirmada zero canônico. Ataques físicos de Dracolion interpretados R205 e RD físico25 de Eristan, fonte proposta.

## Execução nova efetiva

4 seeds candidatas 20909101–20909104, braços SPELL_OFF/SPELL_ON. A última seed teve empate iniciativa e seus **2 braços ficaram pré-commit**. Em 3 seeds restantes foram iniciados 6 combates reais em **R18+v0.8.1**, 240 commits SQLite, 795 eventos, 156 ataques físicos, **30 conjurações**, **90 resoluções separadas de alvo** (30 conjurador, 60 Bestas), custo 80 PA/cast = **2.400 PA**, 5.779 pontos de Vida efetivamente removidos por magia (1.875 no próprio conjurador, 3.904 nas Bestas), 3 KO e 3 censuras por horizonte. `1 KO` em cada braço SPELL_ON foi **autoexposição do conjurador à própria área** (não eficiência da Besta). Os 3 SPELL_OFF foram censurados. Esses resultados demonstram que **posição, dano por alvo e custo único importam**, não que a magia é inferior ou Besta é forte globalmente.

Não confundir 90 eventos de alvo com 90 combates, nem 6 braços com 6 seeds independentes. Um RUN-ID por combate; 3 pares independentes. Não existe agora benchmark cânon das Bestas nem Bateria E homologada.

## Auditoria de causalidade

Auditor independente SQLite read-only sem importar motor: `PASS_R209_INDEPENDENT_R18_MULTITARGET_GEOMETRY_AREA_WITH_CASTER`. Verificou hash chain 240 commits, 795 eventos, 30 cast receipts com gasto PA uma única vez por conjuração, todos os 90 targets em posição geométrica real, 10d10+10, três saves por cast e diferença de Vida/custo, overkill e estados terminais. `R209_INDEPENDENT_AUDIT.json` e bancos/snapshots acompanham entrega. Zero R205/R206B/R207/R208 reexecutados.

## Limites e continuidade

**Magia ofensiva circular funcional em LAB TEST: SIM.** Contrato de fonte integral para benchmark canônico: **NÃO** (NPC PROPOSTO, Besta conflitante, compartilhamento do dado TEST, salvaguarda com metade/rounding não exercitada). Cone ainda sem ângulo; controle Besta, transformação com Espírito, equip CANÔNICO para E e paridade Orc Level-Up seguem HOLD. Equipe 2×1 TEST (R207/R208) não significa referência ED-REF02 homologada. Esquema R91 de 104 posições com B e D 27 patamares continua, oficial 0/17 e 0/1.875.

Próximo trabalho funcional: **R210 candidato** reposicionar centro para excluir caster sem isentar indevidamente qualquer alvo dentro do círculo, comparar política ofensiva com e sem autoexposição e testar salvaguarda de sucesso com dano par quando admissível; obter alvo Bestas fonte-completo e contratos de defesa. Não executar RUN-IDs R209 outra vez. Interface científica DMG apenas READ-ONLY, sem envio/ACK artificial. Produção HOLD.
