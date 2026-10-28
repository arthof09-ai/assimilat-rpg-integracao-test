# AUTH-NOTION-01 — MATRIZ S4 BU25 + BE12 (MSE)

**ESTADO:** CANDIDATA NÃO HOMOLOGADA; não confundir LAB PASS com NAC-STRESS S4 completo. **Fonte:** NAC-STRESS-01 na mãe Comestre, classe S4 mínimo de 25 testes distintos e mínimo de 8 testes especializados. **Este documento é matriz de rastreamento, não certidão.**

## Bateria Universal — 25 famílias oficiais

| ID | Família NAC-STRESS | Estado honesto | Prova / faltante |
|---|---|---|---|
| BU01 | Caminho nominal | LIVE PASS | get_self Mestre/Party + fetch nas raízes respectivas |
| BU02 | Não-gatilho | MOCK PASS / FIELD PENDING | conversa sem Notion não requer reconexão; sem ensaio por outro Comestre |
| BU03 | Entrada complexa | LIVE PARCIAL | dois workspaces autenticados; não cobriu permissões heterogêneas de escrita |
| BU04 | Limite/borda | MOCK PASS | credencial revogada, destino desconhecido, rótulo desconhecido apenas simulados |
| BU05 | Conflito de regras | HOLD | norma-mãe NAC-CONT v2 não chama AUTH-NOTION; conflito/precedência precisa bridge |
| BU06 | Precedência | DOCUMENTAL PASS / FIELD HOLD | conta mestre vs Party, writer separado de ferramenta; sem auditor independente |
| BU07 | Fonte histórica × vigente | DOCUMENTAL PASS | mãe v2 vigente e v1 histórica; candidato AUTH ainda não oficial |
| BU08 | Evidência insuficiente | MOCK PASS | ambiguidade fica indeterminada; live insuficiência sem writer ainda HOLD |
| BU09 | Busca sem resultado | LIVE PASS RESTRITO | NOT_FOUND em leitura cruzada; não certifica 100% das causas de NOT_FOUND |
| BU10 | Falha de ferramenta | LIVE PASS RESTRITO | omitir link gera erro de parâmetro; indisponibilidade real não testada |
| BU11 | Efeito parcial | LOCAL PASS / NOTION HOLD | rollback/commit isolados em SQLite; nenhum timeout real Notion |
| BU12 | Idempotência/NO-OP | LOCAL PASS / NOTION HOLD | SQLite duplicate e timeout+commit readback; sem escritor Notion |
| BU13 | Retry | MOCK+SQL PASS / NOTION HOLD | bloqueio de retry idêntico e readback antes da repetição; sem casos reais destrutivos |
| BU14 | Recuperação de chat | DOCUMENTAL PASS / FIELD HOLD | Modelo Recuperação tem S1–S5; nenhum chat sucessor cego usado |
| BU15 | Sucessor cego | HOLD | requer instância distinta aplicando ordem sem exposição ao chat de criação |
| BU16 | IA em execução durante mudança | HOLD | sem ativação/promoção da candidata e sem cenário real de cutover |
| BU17 | IA nova após mudança | HOLD | bootstrap tem candidata explicitamente inativa; não houve cutover vivo |
| BU18 | Concorrência/Multi-Comestre | LOCAL PASS / NOTION HOLD | epoch e token de escritor simulados em SQLite; lease real não disponível |
| BU19 | Progresso/denominador | PASS METODOLÓGICO | R2 192 parametrizações/38 combinações distintas; R5 248/63 separadas |
| BU20 | Rollback/reversibilidade | LOCAL PASS / NOTION HOLD | rollback pré-commit e histórico preservado; sem reversão Notion oficial |
| BU21 | Player-safe | LOCAL+READ PASS / FIELD HOLD | R5 vetou não-party_safe, conta Party somente leitura; fluxos player-safe end-to-end não ensaiados |
| BU22 | Cross-workspace/Sync | LIVE READ PASS / WRITE HOLD | NOT_FOUND cruzado em páginas; sem mutação de Party ou espelho |
| BU23 | Work/ferramentas | LIVE PARCIAL | notion_get_tool_access confirma ferramentas; Work Cloud Computer não testado |
| BU24 | Comunicação/NAC-PASS | DOCUMENTAL PASS / GATE HOLD | carta Coordenador e Central com distinção NOVA/ACK; PSV-LOCK/terminal não certificado |
| BU25 | Regressão/dependências | MOTHER TEE FAIL | 12 canários de fonte PASS (ausência hook observada); mãe E0–E11 sem chamada AUTH |

## Bateria Especializada — 12 riscos específicos do Notion

| ID | Risco | Estado honesto | Prova / faltante |
|---|---|---|---|
| BE01 | Erro exato link_id omitido | LIVE PASS | ambas contas: before/erro/after com identidade idêntica |
| BE02 | Link elegível incorreto | MOCK PASS / FIELD HOLD | ferramenta restringe enum; não forçar token indevido em conta oficial |
| BE03 | NOT_FOUND ≠ desconexão | LIVE PASS RESTRITO | leitura cruzada sem acesso; autenticação ainda válida |
| BE04 | Duas contas simultâneas | LIVE PASS | get_self Mestre e Party com IDs distintos |
| BE05 | Revogação real | HOLD | não revogar credenciais produtivas para fabricar teste |
| BE06 | Timeout pós-write | SQL TEST PASS / NOTION HOLD | 8 cenários SQLite commit-then-timeout; sem Notion real |
| BE07 | Alteração de vínculo mid-session | MOCK PASS / FIELD HOLD | sessão não foi artificialmente revogada |
| BE08 | Writer disponível ≠ writer concedido | LIVE TOOL + SQL PASS | get_tool_access demonstra ferramenta, não Assignment; SQLite nega token stale |
| BE09 | Rótulo mestre_only/Party | SECURITY REGRESSION TEST PASS | bug sintético R3 reproduzido; R5 fail-closed corrigido |
| BE10 | Rótulo party_safe sem prova | MOCK PASS | R5 default content_class_verified=False; falta integração física com fontes |
| BE11 | Retry após resultado incerto | SQL TEST PASS / NOTION HOLD | 8 commit-timeout/idempotency e 8 rollback-precommit em arquivo TEST |
| BE12 | Sucessão motivada só por login | MODEL+BOOTSTRAP PASS / FIELD HOLD | S1–S5 no Modelo, sem substituição artificial de chat |

## Cuidado com contagens

- **Piso oficial:** S4 >=25 provas materialmente distintas, incluindo BU e >=8 BE/MSE; variedade nominal e casos parametrizados não são automaticamente experiências independentes.
- **Evidência até aqui:** 248 parametrizações de mock/63 estados de entrada distintos/19 mutações detectadas; 65.536 verificações combinatórias de propriedades; 80 transações reais SQLite TEST; 2 provas metamórficas de recuperação de `link_id` live READ-ONLY; 12 readbacks estruturais de entrypoint. Essas unidades não são somadas para declarar 25 testes S4 homologados.
- **Bloqueios:** TEE na mãe, blind successor, migração IA já em execução, revogação/timeout/concorrência controlados no Notion sem afetar produção, writer legítimo, regressão pós-patch e julgamento GNN/GP-NAC/NAC-PASS.
- **NAC-PASS:** a matriz satisfaz mapeamento de cobertura PREPARATÓRIO, **não** o gate de promoção.

## Primeiro conjunto executável após writer legítimo

1. Reabrir a mãe, aplicar patch AUTH inativo/identificado nos estágios E0/E1/E3/E5/E6/E9/E11, reabrir e verificar.
2. Testar 12 canários de texto e 1 teste cego sem expor código/histórico ao avaliador.
3. Executar BE01–BE12 no ambiente TEST autorizado, marcando N/A somente com justificativa de risco.
4. Conferir BU05, BU15–BU18, BU23–BU25 e consultar dependências NAC-NORM/NAC-EVOL.
5. GNN/GP-NAC/NAC-PASS final apenas se zero FAIL bloqueante; atualizar Kit e carta somente após resultado de promoção.

**Fonte canônica:** [Comestre — NAC-CONT-03/NAC-NORM/NAC-STRESS](https://app.notion.com/p/3ecc2b324ede8197911cdd9fe0a4998c). **Ponte candidata:** [Kit Essencial](https://app.notion.com/p/3edc2b324ede81d0b25ec2f3be128db6). **Estado:** [Central](https://app.notion.com/p/3edc2b324ede81569f84c77a50708f93).