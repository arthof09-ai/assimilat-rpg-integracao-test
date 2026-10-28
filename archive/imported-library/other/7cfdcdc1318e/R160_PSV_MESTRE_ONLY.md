# PSV R160 — DEZ ETAPAS DE DESENVOLVIMENTO FUNCIONAL / MESTRE-ONLY

**AS-OF:** 2026-10-16, fuso America/Recife (sessão atual, evidências Notion podem datar 17/10 UTC)  
**OPERATION:** CM-000006 / OP-VLAB-FUSION-SANDBOX-01, **MESTRE-SIDE**.  
**BASELINE:** R01–R150 preservada sem modificações; ZIP R150 aninhado com hash idêntico.  
**LAST-VERIFIED:** R160 — auditoria fria de 9 bancos selecionados, 466 commits, regressões nativas, arquivos de recuperação, manifesto ZIP; ver recibo cold.  
**FIRST-PENDING:** fechar fonte de iniciativa natural do Grifo, alcance de Descarga Curta e RD Lightning de Auren; expiração de Casulo 2 turnos e Marca 3 turnos; consolidar 2º ED.  
**DENOMINATORS:** 9 bancos selecionados **466** commits (R157/R158 3×49=147; ED×Grifo 2×150=300; R153 9; R154 4+2; R155 4). 3 combates táticos ON5 concluídos +2 combates ED×Besta LAB-condicionados concluídos; Casulo e AoOs são fixtures, não combates. 2 sementes numéricas pareadas para A/B (997617 e 998803), uma por família: **não n=4 independente**. R156+R159 S998801 separadas, não seleção. **Terminais 0/17; potência oficial 0/1875**.  
**NO-REPEAT:** os RUN-IDs existentes e as intenções pendentes não foram retomados; não executar runners sobre DBs já criados.  
**CONFLICTS:** Auren transformação 100+15/turno ficha versus 320 ativação sistema; temporalidade Casulo e Marca indefinida; RD Vento/Planta/Lightning ausente não equivale zero oficial; Grifo bônus iniciativa +22 geral não prova proficiência específica; meia-dano ímpar sem arredondamento competente.  
**UNKNOWN_EFFECT:** R123/R134/R143 históricos preservados, além R156 nova intenção pendente; R130 QA_FAIL, R138 SPATIAL_PARITY_HOLD, R124 5×5 CENSORED, R93/R95 errata.  
**AUTHORITY/WRITER STATE:** CM-000006 PAUSED, sem writer, lease, epoch, fencing, INSTANCE-ID ou IBX-101 ACK; nenhuma escrita na OP, Diário, Party, O Primeiro, fichas, regras ou DMG. Library original é a superfície de artefatos permitida; handoff DMG preparado sem ACK.  
**NAC-PASS:** engenharia local PASS delimitado, certificação oficial/terminal HOLD.

## Dez etapas — fatos físicos versus restante

1. **Linhagem:** ZIP R150 verificado, R145/R137 aninhados, módulo v0.8.1 original corrigido copiado, R18/R26 usados; scripts de patch declarados. Nenhum motor concorrente.
2. **R42 crítico negativo:** native `apply_weapon_attack` param `lab_negative_critical_policy=True` (default original bloqueia); R158 F score107 contra CA76, rola [1,1,1], miss automático sem dano, Ação consumida e luta completa em 8 rodadas; R155 AoO negativo sem dano e reação gasta. Auditor frio não importou resolvedor.
3. **Casulo:** R153 conjuração60PA, CA76→98, ataque rolou98 e errou no empate embora acertasse CA76. Persistência ativa verificada; duplicação mesmo conjurador rejeitada pré-intent. **Expiração 2turnos HOLD**; redução -4m armazenada apenas simbolicamente por falta velocidade Eristan; não anunciar efeito temporal fechado.
4. **AoOs concorrentes R43:** R154 ordem Auren DES164 primeiro, Feryn DES80 segundo; fixture full 2 reações, HP479→253 e posição OUT; fixture alvo HP200 morre no primeiro ataque, segunda não executa, Reação F1 preservada e deslocamento interrompido. R155 primeira oportunidade negativa R42, segunda executada; sem geometrias universais.
5. **Ofensivas PA positivas:** Feryn Turbilhão60PA e Eristan Tempestade80PA nativos, salvaguardas documentadas; bônus fixo mágico `documented_flat_bonus` reparado sem mudar default. Fonte de RD elemental dos alvos não especificada => condição LAB zero, exclui terminal fonte-completo. Corte misto Retaguarda12d12 cortante/Vento continua HOLD divisão.
6. **Tática funcional:** R157 duas políticas executadas até Vida0 após oito rodadas sem abdicações, Eristan vence ambas LAB condicionado; BASIC 49 commits/PA640/Feryn8 golpes, EHP197; WIND49 commits/PA1060/7 Turbilhões+1 golpe, EHP181. R158 mesma política BASIC com crítico negativo dirigido e E vencedor HP234, 49 commits.
7. **ED×Besta:** R159 Auren ED L3 vs Grifo-Matriarca L3, seed998803 mesmo estado e política exceto Grifo abre com Descarga55PA vs básico; 150 commits e 50 turnos por corrida, Auren vence as duas, AHP486 vs523. Iniciativa Grifo exógena, alcance LAB de curta linha 1.5m, RD Lightning Auren incerta. S998801 Descarga ímpar abortou sem efeito depois de 1 evento; NÃO reexecutado; caso basic S998801 não entra pareamento.
8. **Elegibilidade A–D:** matriz com Auren, Hongyue, Yip, Pan, Feryn, Eristan, Grifo L3/L2, Crocodilo L3 e Vaelthyr pré-criado. Não promover candidatos por título. ADM26 e Divina27 são posições de potência. A-D todos 0 oficiais.
9. **Ciência comparativa:** R157 BASIC vs WIND contraste efetivo dano912→928 (+16), PA640→1060 (+420) em 1 seed pareada; R159 Grifo special vs basic perda Vida Auren37 vs0, PA Grifo55 vs0, vencedora Auren em ambas sob fontes condicionais. Auditor frio de estado completo e fita de dados nos combates e 2/2 redteam hash-rebuilt rejeitados. NÃO atribuir chance universal de vitória a n=1.
10. **Dezessete contratos:** 17/17 IDs/requisitos/linhagem anteriores copiados; ANTES R150 e DEPOIS R160, 0/17 terminal. R42 reparado LAB-only; catálogo, R43 AoO, tática e ED Besta mostram redução funcional; temporalidade final, RD específica e 2º ED ainda HOLD.

## Fronteiras e explicações de exclusão
- R156 fracassou **após intenção durável** devido a bônus plano +10 da Tempestade não implementado na cópia daquela revisão. Não retentar; nativo R157 corrigido em cópia, seed e DB novos. Nova condição `UNKNOWN_EFFECT/HOLD` adicionada.
- R159 seed998801 special interrompida por rolagem ímpar e ausência de regra de metade. O banco basic S998801 concluiu mas o par não: ambos fora da amostra pareada selecionada; auditar separadamente sem chamar comparação.
- R153 e R154 são cenários técnicos de fontes existentes, inclusive clones identificados; não são 3 NPCs novos canônicos nem benchmarking de equipe ED.
- Políticas são explícitas, simplificadas, sem tática onisciente e pressuposições de RD elemental zero exclusivamente **LAB**. Não 4 seeds blind e não 5 observações independentes de potência.
- Fontes mestre somente-leitura: Sistema de Combate, Sistema de Magia, Criação de Besta, Sikong Auren, Feryn, Eristan, BEAST-FULLSPEC, OP-VLAB R42/R43/R50/R51.

## NEXT-5 — prioridade de engenharia
1. Recuperar fonte competente do bônus de Iniciativa específico do Grifo e da extensão/posicionamento da Descarga, reduzir bloqueio ED×Besta.
2. Consultar NAC-NORM-01 para o marco exato de expiração de Casulo/Marca e custo de transformação, sem tocar fichas originais.
3. Integrar dano Dark com RD60 comprovada de Auren usando atacante real; danos multicomponentes somente após divisão competente.
4. Concluir ao menos uma cena tática com ED e segunda ficha ED completa, não NPC sem Espírito.
5. Pré-registrar e auditar holdout independente de desenvolvimento para comparação de política, com cenário/condições fonte-completos.

**TARGET-REMAINDER:** 17 contratos originais menos 0 terminais; não implica progresso zero nas propriedades técnicas. Gate terminal requer requisitos originais completos, parecer independente competente, suporte de fontes e NAC-PASS.
