# PSV — VLAB R177–R186 · MESTRE-SIDE · 18/10/2026

| Campo | Estado após ciclo |
|---|---|
| AS-OF | 2026-10-18, fuso America/Recife |
| IDENTIDADE | CM-000006 lógica; INSTANCE `I0001` CANDIDATA, não consumida |
| OPERATION | OP-VLAB-FUSION-SANDBOX-01 EXISTENTE |
| WORKSTREAM | CM-000006-WS0001 sujeito ao gate |
| BASELINE | R01–R176 preservadas, R176 ZIP imutável pinado |
| LAST-VERIFIED-UNIT | R186 pacote, verificador portátil cold/read-only |
| FIRST-PENDING | pleno ED×Besta, iniciativa nomeada da Besta, alcance métrico natural, ficha Besta física e validação externa |
| FONTES REABERTAS | Combate, Criação de Besta, Criação de Ficha, BEAST-FULLSPEC-VZ-06, Varok, Iskiel, Veyun, Auren, auditoria Bestas, OP VLAB/Laboratório/Plano Mestre |
| INICIATIVA | 0/6 perfis bestiais com proficiência nomeada nas fontes checadas; ordem Leviatã>Varok provada sem bônus específico sob ausência de modificadores externos |
| GEOMETRIA | preflight numérico Iskiel 80m e Veyun 30m, 2/2 admissão e 4/4 recusa, 1 commit de prova, zero ataque real de arco/cetro; melee = contato TEST |
| COMBATENTES | Varok ON5 NPC proposto versus Leviatã L4 Besta precriada (não ED×BE certificado) |
| COMBATES NOVOS | 1 matchup, 10 execuções condicionais = 5 seeds ×2 políticas |
| COMBATES FONTE-ADMISSÍVEIS | 0 plenamente homologáveis; 10 execuções TEST com efeitos físicos de fonte |
| REAÇÕES COM EFEITO REAL | Armadura Varok -70 após RD, 50PA, 1/cena, 5 ativações em 5 bancos distintos; uma em cada execução ativa |
| HABILIDADES E PA | 50 PA de ativação por execução ARMOR_ON; 0 PA pela política ARMOR_OFF; PA/dia das peças não recobrado |
| REPLAY/AUDITORIA | 10/10 SQLite verificados por auditor de código separado; 202 tentativas ofensivas, 212 commits, 616 eventos nativos; 10/10 forgeries rehashed rejeitados |
| FALHAS | 2 bancos novos: 1 PENDING/UNKNOWN_EFFECT sem retry, 1 AFTER_COMMIT confirmado uma vez, duplicata rejeitada |
| HOLDOUT | 3 seeds pré-registradas de um mesmo matchup ×2 políticas, 0/3 vencedores alterados, 2/3 duelos prolongados, adicional de dano à Besta 34/26/42 nos braços de armadura |
| CENSURA | 0/10 combates censurados; nenhuma operação histórica censurada reclassificada |
| CONTRATOS | 0/17 certificados terminais; 17 IDs originais preservados |
| BENCHMARKS | 0/1875 oficiais |
| NO-REPEAT | R01–R176 não executados; nenhum RUN-ID histórico reutilizado; arquivos dos bancos antigos intocados |
| UNKNOWN-EFFECT | Histórico intocado. Novo tombstone TEST R183 AFTER_INTENT = NO-RETRY |
| CONFLITOS | Varok não é ED; Leviatã não é Besta materializada/homologada; iniciativa nomeada ausente; alcance corpo a corpo/posicionamento natural pendentes; efeitos auxiliares e controle não usados |
| AUTHORITY/WRITER | Notion/Party/O Primeiro/DMG-RANK 0 writes; writer/lease/epoch/fencing não comprovados |
| NAC-PASS | integridade e replay técnico TEST; terminal/admin/benchmark PROD HOLD |

**NEXT-5:** 1) obter proficiências nomeadas em Besta física; 2) fonte de alcance e geometria para combate natural; 3) ED legítimo com capacidade ofensiva e defensiva mutuamente relevante frente à Besta; 4) pilotar habilidade PA e efeito temporal completo em ED×BE; 5) holdout separado por espécies/atores, parecer humano externo e gate de célula/contrato.

### Comparação de capacidade
R176 provava iniciativa *apenas dentro de intervalo limitado* e contato TEST para Auren×Grifo, sem impacto ofensivo adversário. R177–R186 acrescentou **ordem invariável de iniciativa entre Varok e Leviatã**, gate **numérico** de alcance baseado em fontes de armas, Reação **de item com débito energético e redução parcial após RD** no mesmo commit R18, dez duelos curtos pareados auditados, holdout pré-registrado e dez clones rehashed reprovados. Isso é incremento mecânico source-scoped e não completa a principal missão de duelo ED×BE fonte-admissível.

### Demonstração inicial verificável · seed desenvolvimento 17718001

Leviatã: 6d6+142 resulta 164 contra CA83 de Varok; 20d10 = 116 impacto; RD físico35 ⇒ 81 pós-RD.

**Sem armadura:** Varok 734→653 HP, PA324, Reação disponível.

**Com armadura declarada antes da rolagem:** redução de 70 após RD ⇒ somente **11 de perda**, Varok 734→723 HP, PA324→274 e Reação consumida no gatilho; renovada posteriormente por `begin_source_turn` do v0.8.1. Eventos originais e mitigação do item vinculados no mesmo commit. Varok depois ataca 4d6+100 =118 contra CA110 da Besta; 10d10+48 =99 impacto; RD75 ⇒ 24 de dano efetivo. Esta execução terminou no round 10 com vitória condicional do Leviatã em ambas políticas. Verifique os recibos em `evidence/`.
