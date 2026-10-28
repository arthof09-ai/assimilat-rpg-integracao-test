# PSV — VLAB após R315 (MESTRE-ONLY / TEST)

**Operação física:** `OP-VLAB-FUSION-SANDBOX-01` · **Executor lógico:** `CM-000006`, instância e writer não reivindicados.

**LAST-VERIFIED:** `R315` — auditor e recusa transacional de Contra-atacar; **não** implementação completa. **FIRST-PENDING:** `R316` — contrato de ataque nativo consumindo Reação, com fonte de crítico e Vantagem corretamente resolvida; somente TEST até gates.

## Antes/depois

Antes: R311 trouxe Defender, Esquivar, relatório Android, mas não há ataque `REACTION` no core. Após R315: gatilho R50/R51 classificado com base em recibos v0.8.1; R22 informa HOLD e recusa Contra-atacar antes de qualquer intenção. Nenhum contra-ataque executado. Recusar explicitamente é melhor do que uma falsa implementação consumindo Ação Padrão.

## Provas

- **128 ataques nativos R314:** 52 erros normais; 64 acertos zerados por RD100; 12 casos de máximo d6 segregados como HOLD crítico. 128/128 classificados, zero respostas.
- **19/19 testes de gate/interface** e **instalação a frio R22 + overlays R289–R311 + R315 PASS**.
- **8/8 R18**; cinco testes R22 selecionados individualmente `STATUS:0`. Teste monolítico R22 timeout, sem certificado global.
- Os testes de bloqueio cobriram R51, declaração prévia, slot de Reação esgotado, dados de origem malformados, idempotência e continuação de ataque normal após recusa.

## Bloqueios

1. v0.8.1 `execute_turn`/`apply_weapon_attack`: `attack` somente STANDARD. `execute_attack_with_defense`: reação somente DEFENDER/ESQUIVAR. Falta efeito native staged de `counterattack` consumindo Reação, validando crítico e Vantagem, mantendo 1 commit.
2. R27 tem política de crítico negativo apenas científica LAB, não substitui fonte e exceções da R18.
3. Fonte P4/combates R91, autorização writer/epoch/lease, NAC-PASS terminal e ACKs ainda pendentes. Histórico original preservado.
4. Não reaplicar protótipo R314 como versão homologada; reconstrução precisa de adaptador competente.

**Gate:** artefato LAB validado proporcionalmente; produção HOLD, Party/O Primeiro NO-WRITE. **0/17 terminais, 0/1.875 R91**. GitHub CI não executada. Continue por R316 sem gerar motor paralelo.
