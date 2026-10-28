# R22 — Decisões normativas mínimas: B11, B12, B15

**Escopo:** MESTRE-SIDE, OP-DMG-CORPUS-EMP-01. **Estado:** análise PROPOSTA, nunca norma promulgada. **Precedência:** DMG-RANK v1.1 e Sistema de Combate/Magia vigentes, sem substituição. Encaminhamento quando autorizado por NAC-NORM-01 / NAC-PASS e readback. Nenhuma alteração em Notion, fichas, Party ou VLAB.

## B11 — Crítico: a verdadeira fronteira normativa

Fontes primárias (consultadas diretamente no R22):

- [Sistema de Combate](https://app.notion.com/p/3ebc2b324ede81f1be4be8804ac113c0): 3d6 rolados **sequencialmente**; base `(6,6,5)`/`(6,6,6)` dá crítico. `(6,5,6)` NÃO dá. Dano = dados normais + fixo + soma dos máximos dos dados. Margem máxima do terceiro dado +4; 2 primeiros permanecem 6.
- [Sistema de Magia](https://app.notion.com/p/3ebc2b324ede81f7b343f7270ff91373): magia NÃO herda crítico normal, salvo exceção expressa específica.
- [Liu Mestre](https://app.notion.com/p/0b4c2b324ede837cb6be818dc8e36010): Crítico Brutal `multiplicador ... aumenta em +2`; no `Machado de Guerra Elétrico (ON)` está Decepadora `+18 de dano cortante extra` e rechecagem para decepar; o primeiro trecho diz `esta espada`, criando contradição tipológica Machado × Espada.
- [Decepadora independente em catálogo, espelho Mestre](https://app.notion.com/p/377c2b324ede82f9b4a181aed3e10f5a): `+30` cortante, mas é **outra instância**. [Decepadora em Gêmeas Estreladas](https://app.notion.com/p/302c2b324ede83e8948581b1766d0008) também `+30`; **não substituir** o `+18` impresso na ficha Mestre de Liu.
- [DMG-RANK §15–16 e §31](https://app.notion.com/p/3f2c2b324ede815498cddb7844245f7e): Crítico regido pelo Sistema de Combate; amputação é bypass sujeito a condição/alvo apropriado/defesa aplicável, não dano numérico gratuito.

### Parte resolvida sem decisão

- Patada do Macaco `2d6+54` → se um ataque físico *elegível* critar, `2d6+66`; não exige escolher multiplicador legado para **este ataque do Macaco**, pois Crítico Brutal é habilidade impressa de Liu, não do Macaco.
- Exemplo matemático: 216 resultados **ordenados**, dois críticos, `2/216=1/108`; a segunda confirmação, **se** for independente e da mesma margem, cria probabilidade conjunta condicional `1/11664` de duas verificações positivas sucessivas. **Não** é probabilidade de amputação real.
- Magia sem exceção explícita não crita nem com `(6,6,6)`; um item que concede crítico a ataque furtivo não é permissão para converter todas as magias em críticos.

### Menores decisões reservadas (não respondidas automaticamente)

1. **DEC-B11-A — Crítico Brutal:** seu `multiplicador +2` legado continua ativo na regra v1.1 aditiva? Se NÃO, fica inaplicável enquanto não houver compatibilização. Se SIM, é necessário fixar o operador matemático e o tipo exato de arma elegível; `+2 máximos`, `×2 dano` e `+2 margem` são conceitos diferentes e **nenhum foi comprovado**.
2. **DEC-B11-B — Decepadora montada no Machado:** o texto `esta espada` é erro descritivo ou restrição efetiva? Se elegível, usar **+18 da ficha Liu** e declarar se é bônus fixo aplicado uma vez por crit; **não importar +30** da cópia de outros itens.
3. **DEC-B11-C — Segundo crítico/decapitação:** exigir confirmação se `role os dados de novo` significa **apenas** nova verificação 3d6, com qual margem e condição de eficácia contra aquele alvo, ou evento adicional; segunda rolagem não pode produzir golpe/dano extra tacitamente. Documentar recibo da segunda verificação quando houver cena.

**Veredito integral:** PARTIAL. Toda conclusão que dependa dessas 3 decisões permanece sem PASS. Não modificar o sistema para resolver a situação unilateralmente.

## B12 — Adaga da Serpente: redução normativa EFETIVA no R22

Fontes:

- [Adaga da Serpente Enfeitiçada (ON)](https://app.notion.com/p/3edc2b324ede811787a0de913622b14d): dano imediato `5d4+5d8+10`; **se falha CON CD25** → `3d12` de **veneno por turno**; nenhuma duração numérica ou fase do primeiro tick apresentada.
- [DMG-RANK v1.1 §21–23 e §32](https://app.notion.com/p/3f2c2b324ede815498cddb7844245f7e): veneno = **tag tóxica**, não Elemento automaticamente; reaplicação sem regra específica **não acumula infinitamente, renova duração**; resistência/imunidade só por **tag efetivamente declarada**.
- [Adaga da Serpente — página histórica antiga/excluída](https://app.notion.com/p/4a9c2b324ede83f78dc581e101e93948): fonte legada aberta nesta pesquisa, repete `5d4+5d8+10`, `CON CD25`, `3d12/turno`, `35 PA` e **também não define duração**. Não é autoridade live; evidencia que a lacuna já existia antes da repaginação. Crosswalk `R22_SERPENTE_LEGACY_COMPARISON.json`.
- [Adaga de Envenenamento Mortal (ON)](https://app.notion.com/p/fcac2b324ede8260a9cf01d141dae809): **outro** veneno com duração `1 minuto`, efeito e CD próprios. Prova de que durações são locais à fonte.
- [Adaga do Sussurro Mortal](https://app.notion.com/p/85ec2b324ede837f95b6010118e38f5e): **outro** veneno com acumulação expressa e Fortitude CD80 a cada fim de turno. **Não transferir** essas regras para Serpente.

### Parte agora resolvida

`3d12` é dano/tick condicional: mínimo 3, máximo 36, média exata `39/2 = 19,5`. Ao reaplicar a Serpente, **não** se podem criar pilhas ilimitadas de ticks: a regra geral manda **renovar duração**, ainda que essa duração esteja **desconhecida**. A comparação com fonte histórica refuta a explicação não demonstrada de que a duração se perdeu durante a repaginação. Isso dispensa decisão nova sobre *stacking infinito*, mas **não** autoriza estabelecer um valor para a duração por aproximação. A imunidade tipada a Veneno, **quando a fonte do alvo a confirmar**, afeta componente Veneno; não anula automaticamente o dano imediato cuja natureza não foi classificada explicitamente na página.

### Menor decisão ainda necessária

- **DEC-B12-A (temporalidade):** tempo de duração ou condição de término e fase exata do **primeiro tick**. Sem isso, nem segundo tick nem duração total são computáveis integralmente.
- **DEC-B12-B (remoção/reaferição):** existe nova CON CD25 no fim de turno, cura específica, gasto de ação ou outra regra? A página Serpente **não diz**. Exigir decisão ou fonte primária da condição; imunidades concretas continuam por ficha do alvo.
- **EVENT-B12:** prova de golpe da adaga, resultado real de salvaguarda, ativações e turnos; não existe evento confirmado no R22.

**Veredito integral:** PARTIAL, com **uma ambiguidade efetivamente eliminada** pelo texto vigente DMG-RANK: reempilhamento arbitrário NÃO é padrão.

## B15 — Fraqueza elemental: regra completa no exemplo, cena ainda ausente

Fontes: [Sistema de Combate](https://app.notion.com/p/3ebc2b324ede81f1be4be8804ac113c0), [Sistema de Magia](https://app.notion.com/p/3ebc2b324ede81f7b343f7270ff91373), [DMG-RANK v1.1 §21–22 e §32](https://app.notion.com/p/3f2c2b324ede815498cddb7844245f7e).

**Exemplo canônico literal:** `1d8 cortante + 2d6 Fogo` torna-se `1d8 cortante + 5d6 Fogo` **somente** quando o alvo tem Fraqueza a Fogo e o ataque traz tag Fogo comprovada. DME antes `11,5`, depois `22`, acréscimo `10,5`. O `1d8` físico não muda. Veneno não é Fogo; Patada `IMPACTO` do Macaco não se torna Fogo por estar em um contexto com criatura elemental.

**Conclusão normativa:** a regra geral para o exemplo já é suficiente e não exige reforma. A lacuna B15 integral agora é **evidencial**, não uma escolha matemática: falta golpe com componentes fonte-tipados, fraqueza de alvo em cena, reação/resistência/imunidade/RD, rolagens e replay legítimos. **Veredito:** PARTIAL, sem PASS de evento.

## Escalonamento recomendado

Não decidir por analogia de equipamentos ou por média matemática. Submeter **DEC-B11-A/B/C** e **DEC-B12-A/B** com alternativas e impacto à via de decisão Mestre/NAC-NORM-01 apropriada quando houver gateway de escrita competente. B15 **não precisa nova decisão normativa geral**, só evidência de cena. Os contratos B04/B09 e STRICT continuam exigindo ledger real, não hipotético.
