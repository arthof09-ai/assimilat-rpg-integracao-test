# VLAB — Pós-auditoria científica e admissibilidade de fontes R223–R224

**Ambiente:** OP-VLAB-FUSION-SANDBOX-01 / CM-000006 lógico / MESTRE-SIDE TEST / 21-10-2026  
**Autoridade produtiva:** NÃO DEMONSTRADA. **Produção:** HOLD. **Party/O Primeiro:** NO-WRITE.

## 1. A orientação do Mestre e seu estatuto

O Mestre afirmou: **“Dano ímpar se não me engano e se não tiver nenhuma regra é arredonda para baixo.”** Isso foi interpretado como orientação **provisória, expressamente incerta e subsidiária**: executar `floor(D/2)` somente em novas réplicas TEST, sob gate de origem e sem consolidar uma regra global por conta própria. As fontes `Sistema de Combate`, `Sistema de Magia` e `DMG-RANK` consultadas registram “metade” sem definir, nos trechos recuperados, o arredondamento de metade ímpar. **R223–R224 não corrigiram nenhuma decisão normativa do Mestre; entregaram dados para ela.**

## 2. Comparação efetiva de estados

R223 (pré-registro congelado antes de executar): 12 seeds, 4 braços por seed, 48 tentativas. Foram 40 combates TEST admitidos, 8 impedidos antes de criar banco devido ao empate de iniciativa, 8 unidades fatoriais completas e 4 efeitos efetivamente arredondados para baixo. 480 commits, 2.942 eventos. Cinco adulterações adversariais e quatro preflights ilegais corretamente rejeitados.

R224 (novo pré-registro, **nenhuma seed histórica repetida**): 24 seeds e pares **STRICT_HOLD** vs **TENTATIVE_FLOOR** por seed, 48 braços propostos. Quatro seeds causaram 8 bloqueios pré-DB por empate; os 20 pares remanescentes conservam idênticas rolagens e prefixos de eventos até a primeira eventual metade ímpar. `STRICT_HOLD` alcançou horizonte em 18/20 pares, e preservou `UNKNOWN-EFFECT` em 2/20; `TENTATIVE_FLOOR` alcançou horizonte em 20/20. São 38 bancos terminais válidos e 2 com intenção pendente (465 commits, 2.841 eventos), com os efeitos não publicados intactos. Cinco adulterações novas rejeitadas.

**Leitura científica correta:** Na fixture estudada, **2/20 = 10% dos pares** deixaram de apresentar endpoint no braço estrito exclusivamente pela lacuna normativa do arredondamento. O intervalo binomial exato de 95% para uma taxa abstrata, se fossem observações IID comparáveis, seria cerca de **1,23%–31,70%**; não transportar esse intervalo para o RPG como população geral. Os intervalos binomiais aqui são ilustração de incerteza, não modelo comprovado de amostragem da campanha. Os 18 pares em que ambos concluíram não devem ser tratados como amostra neutra de todos os 20 sem advertir sobre seleção pelo sucesso de resolução. Os dois braços estritos interrompidos **não têm HP terminal**; não imputar zero, vitória, derrota ou igualar ao braço piso.

**Fato verificável:** evento com dano inteiro D=61 e sucesso de salvaguarda deu 30 sob a política provisória R223, com 80PA cobrados uma vez. O valor de teto seria 31, mas isto não é uma política alternativa autorizada para rodar combates. Os resultados de R223–R224 são teste de implementação e viés de seleção, não homologação de dano.

## 3. Fontes recuperadas para próximas capacidades

### Controle de Besta — Candidato 1: Constrição Prismática

- [SPIRIT-BEAST-RUNTIME-VZ-08](https://app.notion.com/p/3f3c2b324ede810a8208c364d64f808d), pré-criação de Besta-fonte, versão consultada 08/10/2026.
- VERIFICADO: Serpente Prismática — Padrão, 55 PA, 14d10 Gelo/Luz + contenção; Reflexo CD122, sucesso reduz metade do dano e evita imobilização.
- PENDENTE: duração explícita da condição de contenção, quando e como pode escapar, alcance/alvo exato da Constrição e ficha física integral criada na autoridade final.
- Decisão: **NÃO executar imobilização plena como controle legítimo**, nem usar o arredondamento provisório para encobrir esses requisitos. Pode-se investigar uma versão fonte-admissível da parcela de dano após definir alvo e alcance, sem promover o pacote inteiro.

### Controle de Besta — Candidato 2: Raiz de Ressonância

- [BEAST-FULLSPEC-VZ-06](https://app.notion.com/p/3f3c2b324ede813987deda0b382e83c7), estudo Mestre-side de pré-criação.
- VERIFICADO: Padrão, 120 PA, 16d12 Planta/Spectral, imobilização em falha; sucesso reduz dano e evita a condição.
- PENDENTE: duração, CD da resistência específica, escape, alcance/área, ficha física canônica (a própria fonte registrou `PHYSICAL PAGES = 0/6`).
- Decisão: **HOLD específico**, não resolver por suposição.

### Dominação por artefato — Coleira de Subjugação

- [Coleira de Subjugação — registro de inventário/cena](https://app.notion.com/p/3d5c2b324ede82d49a9d81d4b8c4d91e).
- VERIFICADO na descrição: Dominação Infernal, ativa 1x/dia; contato/colocar coleira em Besta/criatura demoníaca; Vontade CD45; falha obedece comandos simples por 24h; após 24h 1d6 e resultado 1–2 torna-se hostil.
- PENDENTE para combate auditável: economia de ações para **colocação física no alvo**, distância/condições de imposição, classificação/elegibilidade do usuário e vítima e possíveis meios de escapar antes de 24h. Habilidades secundárias mencionam “ação bônus” — reconciliar com as ações do sistema oficial antes de adaptá-las.
- Decisão: **não presumir que tocar/alocar a coleira seja ação gratuita**; combate de dominação integral HOLD enquanto faltar gate.

### Transformação Espiritual

- [Sistema de Transformação Espiritual v1.0](https://app.notion.com/p/3f2c2b324ede81c0ae0ee4e66212edc9) — VERIFICADO: Bronze 1–5 **não ativa**, Prata1+ necessário; BAP/2=TAP e carry fracionário conservado.
- [Pendência contrato Besta→Transformação](https://app.notion.com/p/3f2c2b324ede81668d5cc5b07b2736fe) — verificou ausência de derivação universal indiscriminada sem projeto de reconciliação.
- PENDENTE: selecionar **o mesmo** ED Prata1+ com Espírito real, Besta de origem e ficha transformada completos, duração/turn tick, gastos e ativação idempotente em condições atuais. Não usar pré-criação de terceira operação como personagem vivo sem permissões.
- Decisão: HOLD para primeiro combate integral, prosseguir inspeção de candidatos.

### Bateria E

- Comparação requer **o mesmo chassi físico** com efeito mágico ligado/desligado, rank reconhecido e custo/ação demonstrados. Os objetos pessoais dos NPCs Varok/Arveth/Eristan são propostas Mestre-side e não bastam à homologação canônica. O estudo de Coleira não supre o comparador SEM da Bateria E.
- Decisão: buscar item canônico com chassi/efeito isoláveis; não preencher matriz R91 por conveniência.

## 4. Critérios de continuidade e passagem ao Mestre

1. O Mestre confirmar se **piso** vale para toda redução à metade (salvaguarda, Reflexão, redução de dano, Vida temporária) ou só dano de salvaguarda; a declaração original não enumera escopos. Não redeliberar outras regras.
2. Confirmar prioridade de aplicação **RD versus metade** caso o tipo de efeito exija; não universalizar a fixture de RD mágica 0.
3. Resolver desempate de iniciativa por fonte competente, sem usar o precedente R43 de prioridade de oportunidades como autorização automática para iniciativas.
4. Solicitar ao autor de Bestas o *contrato de duração/escape/CD/alcance* da primeira contenção física real, preservando o design original e as páginas existentes.
5. Usar as análises de missingness para desenhar holdouts com qualidade de fontes, não promover automaticamente NPCs propostos para o estrato R91 C20.

## 5. GATES / NAC-PASS

- R223: execução de regra provisória **PASS TEST fonte-condicional** e readback frio PASS; não prova norma canônica.
- R224: controle científico do bloqueio versus piso **PASS TEST** e readback frio PASS; não existe resultado terminal de braço interrompido.
- Transformação, Controle de Besta, Bateria E, empate de iniciativa, metragem universal de blocos e custo de movimento interrompido: **PENDING/HOLD** nos seus escopos.
- Produção HOLD, writer/INSTANCE-ID não demonstrados, Party/O Primeiro NO-WRITE, 0/17 contratos terminais e 0/1.875 células oficiais homologadas.

**LAST-VERIFIED-UNIT:** R224. **FIRST-PENDING:** confirmação normativa de piso/escopo e desambiguação de controle de Besta. **NO-REPEAT:** nenhuma seed, banco ou quarentena anterior foi modificada.
