# PSV R06 — FAST-RESEARCH | OP-DMG-CORPUS-EMP-01

**Teste:** Armadura de Gelo do Behemoth Ouro 1: CA68→71, reflexão de 15% do dano recebido exceto magias/projéteis, 20 PA para ativar + 3 PA/turno. Reutilizados R05, RD25, duas tentativas físicas corpo a corpo do Símio (Patada Luta+6 e Mordida +7, bônus hipotéticos), sem crítico/Reações.

**Resultados exatos:** +3 CA reduz expectativa de dano recebido da Patada 10→1 (9 evitados) e da Mordida 13,5417→2,7083 (10,8333 evitados). Total de 19,8333 de Vida evitada por uma tentativa de cada golpe, **não por turno garantido**. Sob reflexão sobre dano **após RD**, antes de eventual mitigação do agressor: Patada 0,1500 e Mordida 0,40625 por tentativa; total nominal 0,55625. Por arredondamento em cada acerto: truncar 0,49769, mais próximo 0,56713, teto 0,60725. Se a RD do agressor incidir normalmente sobre a reflexão, RD≥7 elimina todos os valores refletidos nesse cenário, inclusive com teto.

**Custo separado:** 1 turno protegido: 20 ou 23 PA, conforme manutenção comece no turno da ativação; T turnos: 20+3(T−1) ou 20+3T PA. Sem conversão PA↔Vida. Ativação pode impedir a proteção antes dos ataques; ação necessária não resolvida.

**Conclusão:** a redução de acerto domina numericamente a reflexão neste cenário, cujo retorno pode ser anulado pela resistência do agressor. Proximidade de ataque, tipo de reflexão, ordem de mitigação e arredondamento permanecem condicionais.

**Próxima hipótese:** comparar reflexão bypassando RD versus não bypassando, com timing e economia de ações certificados. Fonte mestre: Behemoth `5dac2b324ede83f39cdb01a904ce3cfd`; Símio `301c2b324ede828caccb813d3979267a`. Baseline v1.1 intacta. VLAB não executado, canônico sem escrita, NAC-PASS produtivo HOLD.
