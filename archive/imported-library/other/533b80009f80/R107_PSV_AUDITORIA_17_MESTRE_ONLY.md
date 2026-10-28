# PSV — VLAB R102–R107 | Auditoria dos 17 Contratos & Ciência pós-R101

**AS-OF:** 16/10/2026 · **OP:** `CM-000006 / OP-VLAB-FUSION-SANDBOX-01` · **BASELINE:** R01–R101 integralmente preservada. **DOMÍNIO:** MESTRE-SIDE · apenas sandbox e Biblioteca da OP existente. **NAC-PASS:** técnico local para delta R102–R107; produção/terminal HOLD.

## A. Diagnóstico de integridade, antes/depois

| Pendência herdada | Evidência até R101 | Nova evidência material R102–R107 | Estado atualizado | Restante mínimo |
|---|---|---|---|---|
| 17 contratos auditados individualmente | R17/R18 originais; R60/R70/R81/R91/R101 heranças; 0 terminais | `R105_ORIGINAL_17_CONTRACTS_MATRIX.{json,md}` reconcilia IDs, texto exato do requisito, história, pendente, bloqueio, gate terminal | **17/17 documental**; **0/17 terminal** | Subtestes reais e auditor/autoridade para cada gate; não herdar certificado por 24 duelos |
| R95 assimetria de precisão | R95 16 duelos, Auren 448/448, Bestas 4/444, 8 censuras | `R102_CAUSAL_R95_READONLY.json`, 16 resultados, 8 blocos espelhados, **apenas 2 seeds numéricas distintas**, decomposição CA/RD/Vida/dano/crit/abertura | **explicação causal matemática PASS; paridade normativa HOLD** | Resolver crítico/Fraco e esforço final em adaptador nativo e testar novas seeds/holdout |
| Iniciativa natural da Besta | R95 primeira ação exógena; R93 3 atores com iniciativa experimental | `R104_INITIATIVE_INTERVAL_GATE.json` demonstra fórmula legal e falta da proficiência específica; no Grifo `6d6+116+X`, Auren `6d6+166`; Croco nem +22 permitiria começar antes | **HOLD no X da Iniciativa** | Obter autoridade se Besta é proficiente em Iniciativa / ficha individual com bônus; empates conforme Sistema de Combate existente |
| Primeiro efeito especial e gasto positivo PA | R101 zero PA de habilidade especial, apenas ataques básicos | R103 Descarga Curta Grifo 14d10 Lightning, 55 PA, Reflexo Auren vs CD94: **6 commits**, 3 seeds x 2 espelhos, PA 55/evento, 15/15 bancos frios; 6 tentativas sem commit por metade ímpar e 3 negativas por pré-validação | **prova UNITÁRIA aditiva/não nativa; contrato terminal HOLD** | Adaptar v0.8.1 SAVE-HALF (nativo atualmente bloqueia) e fonte de arredondamento/alcance; falta whole-turn & multiround recovery |
| Crítico correto | R95: +10 em `20d10` (norma +200); R93: +8 em `8d8` (norma +64) | R102 errata individualiza **6 recibos de 2 famílias de seed**, sem editar old SQLite; R106 **20/20 probes unitários** da regra atual sem combate | **Norma resolvida; integração no motor HOLD** | Novo resolver com crítico total + testes causais; R95/R93 originais NÃO promovíveis |
| Equipe equilibrada 2×1 | R93 8/8 técnicos, Feryn ON5 sem Espírito, morreu 8/8 | Nova triagem de fontes: Auren completo L3; SERAH/DAREK VZ têm autoria/roles mas status físico `MECH-PENDING`, PRECREATE HANDOFF 0/8; sem criação de versão fictícia | **HOLD por fonte comparável/economia/reação** | Segundo ED da mesma potência com Espírito, ficha e armamentos mecanicamente completos + política legit de cooperação/target/KO/rollback |
| Linhagem Besta | Grifo L3 Lendário3 do dossiê PRECREATE VZ; L2 parcial | L2 Grifo mesma espécie calculado por Criação de Besta: FOR110 DES112 CON80 INT70 SAB90 CAR35; Vida4020 Alma3800 CA148 RD75 Ataque`6d6+134`; prova retro L3 retorna Vida4315 Alma4016 CA153 | **derivação experimental legal PASS, ficha física oficial HOLD** | Validar versão/atributos de Matriarca L2 e materialização competente + progressão demais patamares sem fabricar skills |
| Painel diverso 27 | 7 espécies candidatas, 0 referências homologadas | `R106_PANEL_BESTAS_27_STATUS.json`, sete distintas em **4** posições (5,23,24,27), 22 Grifo L2 não nova espécie; 26 ADM e 27 Divina são patamares SUPERIORES a Lendário5 | **7 candidatas / 27 posições, 4 posições com candidata, 0/27 homologadas** | Outras fontes por patamar, habilidades/rank confiáveis, combate admissível e fonte oficial |
| DMG handoff | 1.344 recibos originais de R97 tecnicamente verificados | `R105_DMG_HANDOFF_READONLY.md`, hash congelado e delta crítico R102; unidades 24 RUNs/12 pares; bruto, pósRD, Vida, overkill, PA/censura | **pronto para consulta, não recebido oficialmente** | Responsável DMG deve receber pela via competente, sem preempção, análise causal e revisão crítica independente |

## B. Descoberta crítica que altera o status dos resultados antigos

**Fonte** `Sistema de Combate`, Regra 6: dano crítico = rolagem normal + bônus fixo + **valor máximo de TODOS os dados normais de dano**.

- `20d10` Grifo: bônus correto **200**, adaptador R95 somou **10**; diferença +190 por acerto positivo, **4 recibos espelhados da mesma seed 495101**. Exemplo 1 evento: bruto histórico 104; bruto contrafactual correto 294; com RD35 do Auren líquido259 (histórico69). **Não é um combate corrigido.**
- `8d8` Feryn: bônus correto **64**, adaptador R93 somou **8**; diferença +56, dois espelhos da seed 493112, contra RD75 da Besta histórico13 → contrafactual69 no evento.
- R95 também não demonstrou `Fraco` (<10% Vida com desvantagem) nem a oportunidade de esforço final aplicável à Besta. Esses defeitos foram **descobertos agora**, sem alterar R95/R93, cujos auditores antigos ainda podem certificar replay do adaptador.

**Status R93 e R95:** `HISTORICAL_TECHNICAL_PASS / CURRENT_NORMATIVE_PARITY_HOLD`. Não desconsiderar a trilha histórica nem usá-la como benchmark oficial integralmente admissível.

## C. Decomposição causal da diferença Grifo × Crocodilo L3 no R95

- **Rank nominal:** idêntico Lendário3; dossiês PRECREATE VZ, não fichas live. Grifo 4.315 Vida, CA153, RD75; Croco 5.580 Vida, CA112, RD75.
- **Ataque de Auren:** 6d6+193, intervalo 199–229, CA dos dois abaixo do mínimo; **448/448 acertos** independentemente das seeds. Dano normal de lança 8d8+211: média **247 bruto**, **172 após RD75**, sujeito a outras dependências; coeficiente bruto/dano após RD são expectativas condicionais, não média de dano realizado no combate.
- **Ataques das Bestas:** Grifo 6d6+138 = 144–174; Croco 6d6+134 = 140–170; CA Auren225. Acerto comum matematicamente impossível, 4/444 críticos positivos oriundos de uma seed, NÃO quatro eventos estocasticamente independentes.
- **Vida:** Croco tem +1.265 HP, equivalentes a ~7,35 acertos de Auren com dano pósRD esperado172. Sob só ataques básicos o Croco atingiu a censura em 60 turnos com Vida 406–411; Grifo terminou derrotado. Isso não comprova melhor defesa de espécie: CA Croco menor, RD igual, Vida superior, e a censura impede adjudicar vitória.
- **Iniciativa:** abertura pré-fixada B/E, não rolagem natural. A comparação não mede vantajosidade de Iniciativa.
- **Critical defect:** R95 usou máximo facial, além da omissão de `Fraco` e esforço final. Assim, duração e chance de sobrevivência não podem ser promovidas sob a norma atual até reparo e novo lote independente.

## D. Auditoria individual vinculante — todos os 17 contratos

Ver `R105_ORIGINAL_17_CONTRACTS_MATRIX.md` para **cada ID, requisito original VERBATIM, evidência histórica estratificada R01–R101, avanço novo, testes faltantes, bloqueio e certificação terminal**. Referências de definição R17/R18 foram recuperadas e autenticadas. Distribuição: **17 documentados, 17 HOLD terminais**. Reações R50/R51 e séries nativas de R62–R71 permanecem evidências de subpropriedades, não licenças para afirmar cobertura geral. Contratos particularmente afetados:
- `AUTHORITATIVE_RULES_AND_ADAPTERS`, `ED_VS_BE_DAMAGE`, `GENERAL_SPECIFIC_RD`, `BATTLE_1X1_2X1_20X20`, `TURN_SCHEDULER_EVENT_SOURCING`: crítico e Fraco impedem elevar R95/R93; 20×20 não testado.
- `PA_AND_PREBUFF_COSTS`, `ACTION_CATALOG_AIN01`, `RNG_REPLAY_STATISTICS`: R103 dá evidência de habilidade+PA em transação isolada, mas motor v0.8.1 `cast_source_specified_spell()` recusa `SAVE-HALF`, por ausência de regra de arredondamento; não certificar rota nativa. R106 20 unit tests de crítico corretos mas não combateram.
- `REACTION_TRIGGER_AND_SINGLE_USE`, `TRANSFORMATION_OVERLAY_AI08`, `TRANSFORMATION_PER_SCENE_AI09`, `BLEED_AND_HEAL_RESTRICTIONS`, `TACTICAL_AI_AB_FAIRNESS`, `OFFICIAL_QA_NAC_LEDGERS`: conservar bloqueios e provas históricas detalhadas em matriz; não foram testados terminalmente neste ciclo.

## E. Observações de proveniência e veto à fabricação

1. A matriz de 27 patamares de potência é **1–25** regulares Bronze1★…Lendário5★, **26 ADM**, **27 Divina**, ambas superiores ao Lendário5★; não exigir rank/estrela adicional das posições especiais.
2. Cinco Bestas principais do `BEAST-FULLSPEC-VZ-06` são specs do `PRECREATE-CHAR-VZ-01` Cientista 1, não fichas live; HANDOFF registra 0/14 entidades físicas. Grifo e seus predecessores contam como mesma espécie. Espelhos compartilham seed e não são duplicações independentes.
3. Nenhuma ficha original, Party, O Primeiro, DMG-RANK, OP ou Diário foi editado. Perfil CM-000006 permanece `PAUSED`, `WRITER_VERIFIED=UNKNOWN`, sem lease/epoch/INSTANCE-ID/fencing ou ACK IBX-101. Não prometer ou alegar sincronização canônica.

## F. Auditorias desta execução e perímetro exato

- Fonte histórica R101 original SHA-256 `582bc31c08787a8528b7c35fa3c68c202aeaa4f2198a2995bed00a72a6f3b66b` preservada. Arquivos `R97` CSV e R17/R18 intactos, seus hashes dentro do manifesto novo.
- Auditor R103 `r103_independent_cold_auditor.py` **15/15** bancos PASS: 6 eventos PA55 e 9 ações pré-validadas sem commit (6 metade ímpar, 3 negativas). Não se disparou ação histórico e não se reivindica nativo.
- Auditor R106 `r106_critical_normative_probes.py` **20/20** provas aritméticas com seeds inéditas sobre crítico de 4 perfis, nenhum combate e nenhuma SQLite antiga reescrita.
- Gate estático fonte nativo `R106_NATIVE_EFFECT_SAVE_HALF_BLOCKER.json`: linha235 da implementação histórica ORIGINAL `vlab_effects_v08.py` confirma `raise EffectBlocked('rounding of half damage needs source convention')` se efeito `SAVE-HALF`. Teste de leitura estática, não ação integrada.
- `R102_CAUSAL_R95_READONLY.json`, `R102_R93_R95_CRITICAL_PARITY_ERRATA.json` e `R105_DMG_INTEROP_RECEIPT.json` são leituras congeladas sem mutar dados antigos.

## G. PSV de continuidade

**LAST-VERIFIED-UNIT:** Delta R102–R107, auditoria 17/17 documental, 15/15 ledgers R103, 20/20 probes R106, hashes original R17/R18/R97 verificados, prova nativa estática, checkpoint imutável.

**FIRST-PENDING:** paridade crítica nativa + gatilho `Fraco`/esforço final; fonte de proficiência em Iniciativa de Besta, ou regra autoral competente; resolução SAVE-HALF ímpar; **então** ensaio novo, jamais replay silencioso dos históricos.

**DENOMINATORS:** contratos 17 (0 terminais); células 1.875 (0 oficiais); fonte Grifo L2 uma derivação não materializada; painel sete espécies candidatas em quatro slots, 0/27 homologados; fontes 2×1 ED comparáveis 1 completo localizado (Auren), 1 pendente; R103 3 seeds espelhadas, 6 eventos, 15 DBs; R106 20 unidades, não lutas; R93/R95 24 fights históricos tecnicamente íntegros em HOLD normativo.

**NO-REPEAT:** R59 UNKNOWN_EFFECT e tentativa inicial R72 HOLD; R82 collision; R92/R94 falha horizon; não repetir os históricos de R71, R81, R91, R93 e R95 por rotina. Unidades com efeitos desconhecidos e rejeição pré-commit não são forçadas.

**NAC-PASS:** check local documentário e experimental PASS nas unidades descritas; `HOLD` em writer/IBX, produção, replicação oficial e terminais 17/17. **Este PSV não altera OP/Diário nem reivindica ACK**.

**NEXT-5:** (1) selecionar autoridade de iniciativa de Besta por página competente; (2) resolver meia-dano ímpar e alcance da Descarga Curta, confirmar efeito do native original; (3) reparar crítico e Fraco e executar adversarial novos, pré-registrados e independentes de R95; (4) procurar segundo ED de mesmo patamar/papel complementar com ficha válida antes do 2×1; (5) consolidar Grifo L2 e painel sem inventar espécie/atributo e encaminhar recibos ao DMG via routing autorizado.

**TARGET REMAINDER:** 17 contratos individuais com subgates e homologação; nenhuma declaração de conclusão sem autoridade, replay causal, aceite independente e NAC-PASS-02 por contrato.
