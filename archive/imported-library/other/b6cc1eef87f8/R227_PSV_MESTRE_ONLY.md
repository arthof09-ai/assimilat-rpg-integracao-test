# PSV R227 — RESISTÊNCIA ELÉTRICA VERSUS DESCARGA SEMICANÔNICA (MESTRE-SIDE / TEST)

**As-of:** 21/10/2026 · `CM-000006` lógico · `OP-VLAB-FUSION-SANDBOX-01` · Produção HOLD · Party/O Primeiro NO-WRITE.

## Novidade material desde R226

R226 provou COM/SEM magia mantendo chassi físico. R227 usa **o mesmo item fonte-delimitado e golpe físico** para testar outro gate: como se comportam custo, efeito, lentidão e expiração quando o componente Raio é integralmente bloqueado por proteção. Não reutiliza seeds R226.

**Fonte:** Manopla do Trovão Cativo `https://app.notion.com/p/3f5c2b324ede81f5ac62fb940204cdac`, SEMICANÔNICO / INCUBAÇÃO. Regras documentadas: +5d8+3 de Raio com golpe acertado, 22 PA após acerto antes do dano, sem ação extra, uma vez por descanso de oito horas; se ao menos 1 Raio efetivo atingir o alvo, -3m de velocidade até final de seu próximo próprio turno. Não ultrapassa resistência, não impõe lentidão quando Raio é 0.

**R227 fixture TEST:** Arveth proposto ON5 usa seu ataque físico `4d6+72`, `8d10+35` e mesmo armamento nos dois braços, contra Varok proposto CA83/RD35 física. **RD de Raio hipotética** é 0 no braço A e 100 no braço B; `RD100` NÃO é a RD verdadeira de Varok. A hipótese é contrafactual de imunização quantitativa, e não uma nova regra de resistência nem registro de item canônico. Velocidade-base 4m também é premissa TEST, não velocidade canônica.

## Denominador e resultados

- **6 seeds pareadas**, **12 braços TEST**, **24 commits R18**, **132 eventos**, seis janelas de dois turnos por braço. **Zero lutas completas**; 12 censuras de janela.
- **Quatro golpes físicos acertaram**, dois erraram, com ataque e dano físicos idênticos entre braços por seed.
- Cada acerto ativou o item em ambos os braços: **8 ativadores**, **176 PA consumidos** no agregado. Não houve gasto em qualquer braço que errou.
- RD Raio0: **100 PV extras** efetivos na amostra; quatro lentidões de -3m e quatro expirações corretas.
- RD Raio100: **0 PV** retirados por Raio; **zero lentidões**; **22 PA por acerto ainda consumidos**; nenhuma recarga automática.
- Controle de conservação: `100 PV preservados com RD100` nos quatro pares acertados; resultam exclusivamente dos quatro pools mágicos das seeds. Não declaram resistência real do NPC, balanço universal ou poder oficial.

## Auditoria

`r227_independent_magic_rd_audit.py` reconstituiu 24 commits, hashes, BEFORE/AFTER, RNG de ataque/crítico/dano físico e 5d8 mágico, CA83, RD física35, RD elétrica por braço, PA22, Vida, turno e fronteira de expiração, sem importar motor/executor. `PASS_R227_INDEPENDENT_MAGIC_RD_SOURCE_CONTROL_PAIR_TEST`.

Quatro adulterações adversariais em cópias com row/HEAD reconstruídos — RD declarada, PA, falsa lentidão, dano mágico — foram **rejeitadas 4/4**. Zero replay histórico, zero operação produtiva, zero fichas alteradas.

## Conclusão funcional

A ativação legítima de um item custa PA quando declarada, mesmo que proteções absorvam todo o Raio. A **lentidão é condicionada a Raio realmente efetivo**: gasto de 22 PA não basta para aplicá-la. O caso atingido no braço RD100 **não fica lento**, como exige o texto da peça. Tais resultados são PASS TEST condicional, não homologação da Bateria E.

**LAST-VERIFIED-UNIT:** R227 local; readback ao momento de escrita PENDENTE. **FIRST-PENDING:** resolução de velocidade fonte-completa e contexto corpo a corpo para levar a redução à trajetória nativa; Busca adicional de equipamento CANÔNICO integralmente separável; controle de Besta/Transformação com fontes completas.

**Gates:** R225 direção do arredondamento confirmada pelo Mestre (propagação canônica via NAC-NORM ainda pendente); R226 físico+magia PASS TEST; R227 proteção elétrica PASS TEST; Bateria E homologada 0; contratos terminais 0/17; matriz oficial 0/1.875; produção HOLD.
