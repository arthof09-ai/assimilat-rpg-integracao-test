# OP-DMG-CORPUS-EMP-01 — R04: primeiro replay isolado verificável

**Função:** CM-000001, ciência do dano, MESTRE-SIDE. **Vigência:** somente pesquisa; não reivindica writer/epoch do Laboratório. **Origem:** fixture R03 (IBX-34). **Estado:** matemático PASS; HIT-ONLY condicional, DAMAGE-RESOLUTION condicional; FULL-FIGHT NÃO.

## LAST-VERIFIED / Delta material em relação a R03
- Reabertas fontes Mestre de Liu Xiaua P5, Macaco Rei/Símio Demoníaco P5, Behemoth P5, Sistema de Combate, Criação de Ficha, Criação de Besta corrente, **Criação de Besta — Versão Antiga (registro)**, Sistema de Magia, DMG-RANK, LAB AI08 RD, AI09 runtime v0.9 e ActionCatalog v0.7.
- Criação de Besta antiga é explicitamente **somente histórica** e traz incrementos por patamar mas **não declara base inicial Vida/Alma 30/60**. A versão vigente explicita bases e refaz progressão quando sobe de classificação. A diferença exata 30/60 fica explicada aritmeticamente pela ausência da base na ficha, mas sua origem editorial/retroatividade efetiva ainda NÃO é comprovada. Preservar A literal e B hipotética.
- A fonte física do Macaco é uma variante ÚNICA de ID `301c2b324ede828caccb813d3979267a` sob o pai `f42c2b324ede82f1a62c81d6274d7d37`, Símio Demoníaco (Gelo); seu **corpo** chama `macaco rei` e a **página** tem título `Prata 5 (titã)`. Nem duplicar identidade nem canonizar aliases. O título informa Titã PROVISORIAMENTE.
- LAB v0.9 opera ataque básico/fonte-gated parcialmente com scheduler de turno MANUAL/EXTERNO, **não** completa iniciativa, reações ou tempo automaticamente. 

## O primeiro REPLAY CIENTÍFICO MATEMÁTICO (ataque isolado)
**Evento:** Macaco Rei aplica Patada `2d6 + FOR` (impacto) contra Liu não transformada, sem buff extra demonstrado. A ficha registra FOR54, CA46, Reflexo49 e RDF10 no equipamento de Liu. Sistema de Combate exige `resultado de ataque > defesa` e 1 Ação Padrão para ataque normal; uma Reação pode ser usada antes, se ainda disponível.

**Pré-condições ainda a certificar para um evento real:** Patada como ataque legal, alvo em alcance, sem penalidades de status, proficiência Luta não negativa (mas valor não conhecido), escolha explícita de nenhuma reação ou Esquivar se elegível, ordem de turnos válida, força passiva +2 já incluída em 54 OU não. O teste é condicional e **não afirma** essas premissas como observadas na cena.

**Vetores reprodutíveis independentes:** rolagem de ATAQUE 2d6=(3,4) → piso `3+4+54=61` + proficiência *p* desconhecida; se *p* ≥0, supera CA46 e a Esquiva49. Verificação de crítico sequencial `3d6=(2,3,4)` é ordinária. Rolagem de DANO independente 2d6=(5,3) → `5+3+54=62` bruto do componente de IMPACTO. A regra do Mestre documentada em DEV-AI08 usa `max(0, bruto−RD aplicável)` para um componente simples, mas ainda falta **provar que RDF10 é aplicável especificamente a IMPACTO** e a ordem completa. Se RDF10 aplicável: **52 dano líquido**, Vida Liu documental 235→**183**. Se não aplicável: **62**, Vida 235→**173**. **Nenhuma dessas ramificações foi promovida a dano canônico executado.**

**Teste EXAUSTIVO das 36 combinações:** `2d6+54` atinge 56…66, média 61; sob precondições o piso excede CA46 e Esquiva49 em **36/36** combinações (hit condicional). Após RD10 quando aplicável: dano46…56, média51; se não aplicável: 56…66, média61. A ficha diz `Força Titânica +2 FOR`; desconhecido se 54 já incorpora +2. Se for adicional, variante condicional `2d6+56` =58…68, média63; não duplicar bônus. DME intrínseco dos dados =7, não 61.

**Regra de estados neste golpe:** mesmo no ramo FOR56 e sem mitigação, o dano bruto máximo de Patada seria 68, deixando Liu com pelo menos **167 Vida** a partir de 235; assim esta ÚNICA Patada não atinge metade (117,5) para oferecer Fúria nem a faixa estritamente inferior a 10% (23,5) da condição Fraco. Esse resultado só vale sem outros efeitos, crítico ou golpes adicionais. Não prova que tais capacidades possam ser ignoradas na luta inteira.

**Iniciativa:** Prata rola 2d6+DES+proficiência; Liu possui DES16 e Instinto Selvagem +4, Macaco DES40. A diferença entre os máximos/mínimos implica Macaco antes para **1296/1296** pares de rolagem de iniciativa sempre que `prof_Liu − prof_Macaco ≤ 9`, sem outros modificadores ou desempates. Proficiências exatas não certificadas, logo isso NÃO fecha a ordem do combate. Exemplo: rolagens Liu (4,4)→28+pL, Macaco (2,3)→45+pM, Macaco primeiro somente se pL−pM<17.

**Liu atacando:** fonte anota `H - Ataque Básico: 2d6+37 (5d12+3d8+1d6+45)`. Se, e SOMENTE SE, `2d6+37` denotar a rolagem de ataque e nenhuma outra fonte vigente entrar, o máximo49 não supera CA67 do Macaco nem CA61 do Behemoth; isto é sensibilidade, não certifica taxa real de acerto, TTK ou vitória.

## Gate ciência vs gate FULL-FIGHT
**MATH-ONLY:** propriedades e distribuição de dados aprovadas pelo verificador independente (18 testes independentes; 36 outcomes 2d6 e 216 outcomes 3d6). **HIT-ONLY:** resultado condicionado a p≥0, alcance, ausência de penalidades e escolha de defesa; **não** é aceito como evento legal incondicional. **DAMAGE-RESOLUTION:** fórmula unitária comprovada como direção do Mestre para componente simples, mas ramo RDF Impacto **pendente**. **FULL-FIGHT:** 0/2, nenhuma vitória, derrota, tempo de abate ou replay no runtime.

**Dos 18 critérios R03:** **0/18 FULL-FIGHT terminalmente certificados**; as evidências parciais se aprofundaram. **B12/B14/B16** tornam-se NÃO APLICÁVEIS a **este evento básico isolado** quando habilidades opcionais estão inativas, sem encerrar seus gates para o combate inteiro. Não inventar progresso sobre os 18; seu denominador é por confronto, não as 19 fases F0–F18.

## Duas decisões genuinamente reservadas ao Mestre (em conjunto, sem interromper matemática)
1. **Vida/Alma histórica vs reconstrução:** A = Macaco 750/700, Behemoth 500/560; B, hipotética da regra vigente = 810/760 e 530/590. Recomendo preservar A como snapshot histórico da ficha e B para stress científico; qualquer baseline canônico do combate precisa de decisão de autoridade. A regra vigente só determina recálculo quando passa de classificação; não prova por si só atualização automática de fichas existentes sem mudança de classificação.
2. **Bônus e defesa física:** Força Titânica +2 já está em FOR54? E RDF10 da armadura da Liu reduz Patada de IMPACTO e em qual ordem frente a RD geral/elemental? Recomendo não aplicar duplamente +2 e não assumir RDF antes da decisão competente. O Laboratório já tem a direção `max(0, bruto−RD aplicável)` por componente único, pendentes NAC-NORM e interação.

## Integração com v0.9
O ActionCatalog espera AbilitySource/ActorActionState/FrozenRuleEvidence e retorna SourcedOption; v0.9 registra runtime de ATAQUE simples parcial, mas scheduler de iniciativa/reação/tempo é MANUAL/EXTERNO. Entregar o **oráculo isolado** como dados de teste, não como opção SourcedOption já aprovada. Caso o gateway STRICT requeira PA Free, LoS, ação resolvível ou prova humana de congelamento, rejeitar e registrar motivo. Sem alteração do software.

## Continuidade
- **NO-REPEAT:** não tocar Fogo 44×43, 198 IDs da união parcial, nove manifestos nem refazer IBX-28/32/34. Predecessor 149 IDs permanece PENDING sem obstruir o fixture.
- **FIRST-PENDING:** resolver política de RDF de impacto e força passiva, PA Livre da Liu (73 na linha de Alma e `Perdido -46`, podendo ser 27 se adicional), source-gate das proficiências e estados iniciais; obter da engenharia a aceitação da entrada isolada e interfaces atuais; construir replay real de ataque **sob o executor dela** e então progressivamente encerrar 18 gates do confronto.
- **ORIGIN-INSTANCE-ID:** não comprovada; nenhuma reserva/lease científica ou código do LAB assumidos. Escrita, se ocorrer, somente comunicação incremental na **mesma IBX-34** autorizada pelo Mestre, com readback e ACK mantido independente.
- **NAC-PASS científico terminal:** PENDENTE; o ensaio matemático isolado passou seus testes locais.
