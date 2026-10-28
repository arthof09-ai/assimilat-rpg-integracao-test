# R05 — Decisões mecânicas, oráculo de ataque e gate do Laboratório
**OP:** OP-DMG-CORPUS-EMP-01 · **Fonte:** R03/R04/R04B, não reiniciados · **MESTRE-SIDE** · 08/10/2026
**Estado:** pesquisa de dano READ-ONLY; writer formal da OP não comprovado; FULL-FIGHT 0/2; NAC-PASS terminal PENDENTE.

## Resultado material 1 — Esquiva CA46 / Reflexo49
- **Verificado fisicamente:** Liu normal na mesma ficha `CA 46 (Reflexo 49)`; Liu transformada `CA60 (Reflexo63)`; Jaku `29→35` e `39→45`; Yin `29→37` e `42→50` no mesmo template precomputado. Fórmula do Sistema de Combate `Esquiva=CA+Reflexo`; Criação de Ficha: bonificação da proficiência de Reflexo soma à CA; Ficha Base tem campos CA e Reflexo lado a lado. Arquivo histórico de Criação de Ficha preserva a mesma semântica.
- **Conclusão operacional forte (ainda sujeita à competência de verificação de fonte):** o valor `Reflexo 49` no resumo é **defesa final de Esquivar**, não o bônus bruto +49. Bônus agregado do campo: `49-46=3`, mas o bônus estritamente advindo da proficiência isolada permanece UNKNOWN. **Não usar `46+49=95`.**
- A CA passiva46 é distinta de uma Reação Esquivar legal e disponível cujo limiar indicado é49. Sem reação declarada/disponível, usa-se CA46 ou defesa competente; não usar Esquiva automática.

## Resultado material 2 — FOR54/56
- Só 1 página encontrada para o personagem Macaco Rei com `FOR54` e passiva `Força Titânica +2 força`; nenhuma conta de construção mostra se 54 já a incorpora. A=FOR54 literal; B=FOR56 somente sensibilidade. É **inadequado declarar 56 vigente**.
- Ambos os ramos tornam ataque 2d6+FOR superior a CA46 e Esquiva49 em 36/36 combinações se a Patada for ação legal, sem penalidades, com Luta>=0.
- A FOR54 produz ataque mínimo56/máximo66 e dano 2d6+54 (56…66, média61); a FOR56 produz mínimo58/máximo68 e dano 2d6+56 (58…68, média63). DME intrínseco dos dados2d6=7, o atributo externo não integra esse DME.
- Replay dados ataque (3,4), crítico sequencial(2,3,4) ordinário, dano (5,3): A ataque61 bruto62; B ataque63 bruto64. Se RDF10 aplicável, líquidos A52/B54 e Vida Liu235→183/181. Caso não seja, A62/B64 e Vida→173/171. NUNCA mesclar.

## Resultado material 3 — RDF10 / impacto
- Liu inscreve `RDF10` na Armadura Pesada Anã. Taxonomia DMG-TAX-DATA-01 classifica IMPACTO/CONTUNDENTE em FÍSICO. Rinolupo Prata4 escreve `resistência adicional contra ataques físicos, RDF10`. Evidência forte da **família física** de RDF; Patada é literal `impacto`.
- **Ainda não CERTIFICADO para dano canônico:** nenhuma autoridade reaberta estabelece expressamente neste equipamento que *todo* impacto usa RDF10, relação RDF↔RD geral simultâneas, stacking, desgaste de armadura ou a ordem completa em outros danos. DEV-AI08 Mestre determina `max(0,gross−RD aplicável)` para componente simples, e bloqueia RD geral+específica sem prioridade. Por isso os ramos líquidos continuam condicionais, embora agora justificados taxonomicamente.

## Resultado material 4 — Proficiências e tempo
- Criação de Ficha vigente: bônus **inicial** de perícia selecionada =+2. A fonte de Liu enumera habilidades mas não identifica com confiança quais estão em negrito/selecionadas, nem o bônus exato de Luta, Iniciativa ou Reflexo no instante do encontro. `Instinto Selvagem+4` em Iniciativa é literal. A diferença final de Esquiva (+3) não basta para determinar qual parte vem da proficiência versus outra fonte.
- Criação de Besta: Proficiência Prata Titã +11; Prata normal +8. Como o título estrutural do Macaco é `Prata5 (titã)`, +11 é o valor normativo **condicional a Titã e aplicabilidade ao teste**, não bônus de Luta individual já auditado. Não inventar bônus exato para o actor.
- Iniciativa Prata `2d6+DES+bônus Iniciativa`; sob ausência de modificadores adicionais, Macaco sempre antes de Liu nos 1296 pares de rolagens **se** `pL−pM<=9`; desempate universal desconhecido.
- Sistema de Combate: ataque normal consome Ação Padrão; Reação defensiva anunciada antes; alvo escolhe não reagir legalmente no ensaio isolado, desde que cena e competência confirmadas. Alcance da Patada, posição, LoS e disponibilidade de ação/reação ainda requerem dados, não se presumem de “corpo a corpo”.

## Oráculo operacional de engenharia
**Designado:** `OP-DMG-F1-R05-ATTACK-PATADA-01`; *não é action_id já aprovado pelo Laboratório*.
1. `SOURCE`: ator Macaco Rei `301c...`, alvo Liu `0b4c...`, Combate `3ebc...`, taxonomia `3f3c...`, RD Lab `3f3c...`. Refetch hash/fingerprint e aceite do Lab obrigatório.
2. `NORMAL`: sem transformação, Fúria, Extensão, magia, reflexo ofensivo, buffs adicionais; defensora com escolha explícita entre NÃO REAGIR e ESQUIVAR. Caso reação seja inválida, não substituir silenciosamente.
3. `PARAMETRIZAR SOB CONDIÇÃO`: turno e Ação Padrão disponíveis, posição/distância/linha de visão com confirmação de alcance da Patada, PA Livre conhecido conforme contrato (não colocar 0 por omissão), cooldown/estado, proficiências efetivas, seed ou vetor de dados fixo, janela da reação, categoria e aplicabilidade da RDF.
4. `MATH-ONLY`: avaliar `FOR=54` e `FOR=56` como cenários distintos, ataque vs CA46 e dodge49, dano 2d6+FOR, crítico sequencial (2,3,4) ordinário.
5. `HIT-ONLY`: só marcar PASS no evento quando o contrato da cena e o ataque estiverem fisicamente legais, dados da rolagem e reação provados. Sob premissas R05, 36/36 ataques superam ambas as defesas; NÃO converter distribuição condicional em evento ocorrido.
6. `DAMAGE`: ramo RDF10 se aplicável e nenhuma outra RD conflitante; 62→52 (54), 64→54 (56); alternativa RDF não aplicável mantém bruto. Não declarar a redução canônica até interpretação competente da armadura.
7. `STRICT`: pedir ao motor `action_menu`/preflight com fontes, `AbilitySource/ActorActionState/FrozenRuleEvidence/SourcedOption` no contrato já existente. Deve REJEITAR enquanto fonte frozen não aceita, PA livre, alcance, LoS, action state e janela de reação estiverem UNKNOWN. Primeiro aceite legítimo deve retornar versão, input, opções rejeitadas, event trace/seed, replay byte-idêntico e verificação independente.

## Decisões ainda reservadas ao Mestre (consolidadas)
- **D-01 — FOR:** 54 já incorpora passiva +2? Opção A preserva 54; B aplica 56, com +2 ao ataque e ao dano. Recomendo **A literal para baseline histórico** e B apenas sensibilidade, até confirmação da construção/decisão Mestre.
- **D-02 — RDF:** confirmar oficialmente que `RDF10` é mitigação física especializada que cobre impacto, se há outro RD geral e como acumular/priorizar; recomendação técnica: tratar IMPACTO como FÍSICO pela taxonomia, aplicar subtração simples apenas quando não haja RD concorrente e o Mestre confirmar cobertura.
- **D-03 — Vida/Alma:** Macaco documental750/700 vs cálculo atual hipotético810/760; Behemoth documental500/560 vs hipótese530/590. Fonte antiga não possui base inicial; atual explicita30/60. Recomendo preservar literal como histórico, não recalcular ficha sem decisão.
- **D-04 — Nomenclatura de Titã:** ID físico único sob pai Símio Demoníaco, nome interno Macaco Rei, título P5 (titã). Não criar/atribuir entidade nova nem canonizar sinônimo; confirmar se restrição de Titã realmente aplicável ao encontro em questão.
- **D-05 — valores de perícias:** primeiro recuperar anotação real; se fonte não as determina, decisão de valor/estado no cenário é do Mestre, sem fingir proficiência universal para a ficha.

## Último gate
LAST-VERIFIED: R03/R04/R04B preservados; R05 oráculo 32/32 testes novos independentes PASS; página Notion fonte em leitura, sem modificação. 18 critérios do combate completo ainda não terminalmente certificados. Nenhum ataque executado no runtime do Lab nesta pesquisa.
FIRST-PENDING: preflight do Engenheiro e ACK; regra de RDF; proficiências e carga; posição/alcance/estado inicial; adição de passiva; decisões D-01/D-05 por autoridade.
NO-REPEAT: 198 IDs, Fogo44×43, R03, R04/R04B, 29/29 testes.
NAC-PASS terminal: PENDING. Escopo F0–F18 global: % NÃO DETERMINÁVEL.
