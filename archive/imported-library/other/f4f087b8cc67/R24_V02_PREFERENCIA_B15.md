# R24-v02 — Fonte mais adequada para ensaio B15: Jaku Nadta

**Origem da melhoria:** após fechar R24-v01, foi encontrada uma combinação de arma e item NO MESMO INVENTÁRIO de uma ficha Mestre. R24-v01 permanece aninhado byte-idêntico.

## Novas fontes do Notion reabertas

- [Jaku Nadta — ficha Mestre](https://app.notion.com/p/07dc2b324ede82aeb27501f9414bfc81), as-of 2026-09-30T04:36:35.745Z: lança `2d8+2`, e Manoplas da Fúria Flamejante NO MESMO INVENTÁRIO; a mesma lança também mostra infusão espiritual flamejante `+2d8+2`, que deve ser conciliada, não apagada arbitrariamente.
- [Manoplas da Fúria Flamejante — ficha do item](https://app.notion.com/p/592c2b324ede8385b926013aac7146ca), as-of 2026-09-30T04:45:48.615Z: cada arma sob chamas causa `+1d8+2` **de Fogo extra em um golpe**; armas não mágicas agarradas pela manopla são tratadas como mágicas; exige `ação bônus`, chamas até baixar/soltar arma, custo `13 PA por dia`.
- [Dragão de Gelo Azul — besta](https://app.notion.com/p/4fac2b324ede824da70d0189f19533de): vulnerável a **ataques mágicos de Fogo**, Ouro 1, Vida 523, CA39.

## Exemplo de ensaio condicionado, NUNCA evento real

Se o golpe com a lança **legalmente** mantém pool físico `2d8+2`, se as manoplas estão ativas e concedem `+1d8+2` de Fogo, e se essa instância conta como *ataque mágico de Fogo* perante o Dragão, o Sistema de Combate dá `+3d8 de Fogo` somente no pool elemental.

Rolagens manuais do ensaio, NÃO dados de combate: lança `[5,3]`+2=10; Fogo da manopla `[6]`+2=8; fraqueza Fogo `[3,7,4]`=14. Total bruto hipotético sem fraqueza=18; com fraqueza=32; delta +14 somente no componente Fogo. Médias exatas do modelo condicional: **17,5** sem fraqueza, **31,0** com fraqueza, delta **13,5**.

**Falhas de gate que permanecem:** disponibilidade viva de Jaku no epoch da cena, arma e manoplas equipadas, ativação já realizada (`ação bônus` legado não reconciliada automaticamente com economia atual), PA e janela de ação, natureza física da lança, regra e stacking da infusão espiritual flamejante `+2d8+2`, dano efetivamente mágico Fogo, RD/mitigação e reações do Dragão, rolagem real de acerto/dano, HP antes/depois, recibo de commit e readback independente.

**Comparação com R24-v01:** Jaku é candidata preferida porque a ficha mostra posse simultânea dos dois objetos e a manopla declara expressamente `Fogo extra`; Ong tinha possível `Morto` em espelho Party e concatenação menos clara. A melhoria é documental, não evento: certificado **1/18**, B15 **PARTIAL**, STRICT **0/2**, CSV **0/9**, decisões Mestre **0/5**.

## Próxima execução legítima

Pedir ao operador autorizado (CM-000006) que confirme as interfaces e o estado de cena antes de qualquer evento; observar NAC-CONT-03, NAC-NORM-01, NAC-PASS e autorização expressa. Se o campo `ação bônus` ou stacking físico/espiritual/Fogo não tiver interpretação vigente, não improvisar decisão; escolher outra ação completamente fonte-gated, não alterar regra. O episódio precisa de id, epoch, mapa, PA, acerto, rolagens reais, dano por tag, RD, HP/Alma antes/depois, commit único, readback e auditoria. Nenhum dos testes locais fornece esse evento.
